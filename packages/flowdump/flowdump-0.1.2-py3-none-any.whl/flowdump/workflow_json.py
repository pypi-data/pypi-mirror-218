import dataclasses
import json
import pathlib as pl
from dataclasses import dataclass
from datetime import date, datetime
from os import PathLike
from typing import Callable, Dict, List, Optional, Union

import networkx
from nipype.interfaces.base.support import Bunch
from traits.has_traits import HasTraits
from traits.trait_base import _Undefined  # noqa

from .core import NodeRaw, WorkflowRaw, workflow_container
from .nipype_report_parser import ReportSection, read_report_rst


def _object_as_strdict(obj: object) -> Dict[str, str]:
    """
    Extracts and converts all fields of an object to a {str: str} dict.
    """
    if isinstance(obj, dict):
        obj_dict = obj
    elif hasattr(obj, "__dict__"):
        obj_dict = obj.__dict__
    else:
        return {"value": str(obj)}
    return {str(k): str(v) for k, v in obj_dict.items()}


def _serialize_inout(obj: object) -> object:
    """
    Simple recursive string serialization for NiPype node input and output arguments.

    Parameters
    ----------
    obj : The object to serialize.

    Returns
    -------
    The serialized object.
    """
    if isinstance(obj, dict):
        return {str(k): _serialize_inout(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_serialize_inout(i) for i in obj]
    if isinstance(obj, tuple):
        return (_serialize_inout(i) for i in obj)
    if isinstance(obj, HasTraits):
        return _serialize_inout(obj.trait_get())
    if isinstance(obj, (int, float, str)):
        return obj
    if isinstance(obj, _Undefined):
        return "[Undefined]"
    if isinstance(obj, Bunch):
        return {str(k): _serialize_inout(v) for k, v in obj.items()}
    if obj is None:
        return None
    return str(obj)


def _workflow_get_graph(wf: WorkflowRaw) -> networkx.DiGraph:
    """Get graph from workflow instance."""
    return wf._graph  # noqa


def _node_get_wd_path(node: NodeRaw) -> pl.Path:
    """
    Get working directory path for a given node.
    """
    return pl.Path(node.output_dir())  # noqa


@dataclass
class EdgeData:
    """Data class for serializing workflow edges."""

    origin: str
    target: str


@dataclass
class NodeResultData:
    """Data class for serializing workflow node results."""

    inputs: dict
    outputs: dict
    runtime_info: dict
    wd_path: str
    read_success: bool
    command_txt: Optional[str] = None


@dataclass
class NodeData:
    """Data class for serializing workflow nodes."""

    name: str
    type: str

    inputs: dict
    outputs: dict

    result: Optional[NodeResultData] = None

    nodes: List["NodeData"] = dataclasses.field(default_factory=lambda: [])
    edges: List["EdgeData"] = dataclasses.field(default_factory=lambda: [])

    @classmethod
    def from_obj(
        cls, obj, serializer: Callable[[object], object], serialze_postex: bool = True
    ):
        if isinstance(obj, (NodeRaw, WorkflowRaw)):
            node_data = cls(
                name=obj.name,
                type="node" if isinstance(obj, NodeRaw) else "workflow",
                inputs=_object_as_strdict(serializer(obj.inputs)),
                outputs=_object_as_strdict(serializer(obj.outputs)),
            )
        elif isinstance(obj, networkx.DiGraph):
            node_data = cls(name="exgraph", type="exgraph", inputs={}, outputs={})

            # Infer name from first node
            node_list: List[NodeRaw] = list(obj.nodes)
            if len(node_list) > 0:
                node_data.name = node_list[0].itername.split(".", 1)[0]

        else:
            raise TypeError(f"Unknown Node type found in graph: {type(obj)}")

        if isinstance(obj, NodeRaw):
            if serialze_postex:
                node_data.name = obj.itername.split(".", 1)[-1]
                wd_path = _node_get_wd_path(obj)
                node_data.result = NodeResultData(
                    inputs={},
                    outputs={},
                    runtime_info={},
                    wd_path=wd_path.as_posix(),
                    read_success=True,
                )
                report_path = wd_path / "_report" / "report.rst"
                if report_path.exists():
                    report_data = read_report_rst(report_path)
                    node_data.result.inputs = report_data.get(
                        ReportSection.EXECUTION_INPUTS, {}
                    )
                    node_data.result.outputs = report_data.get(
                        ReportSection.EXECUTION_OUTPUTS, {}
                    )
                    node_data.result.runtime_info = report_data.get(
                        ReportSection.EXECUTION_INFO, {}
                    )
                else:
                    node_data.result.read_success = False

                command_txt_path = wd_path / "command.txt"
                if command_txt_path.exists():
                    with open(command_txt_path, "r", encoding="utf8") as file:
                        node_data.result.command_txt = file.read()

            return node_data

        graph = _workflow_get_graph(obj) if isinstance(obj, WorkflowRaw) else obj

        for child_node in graph.nodes:
            node_data_child = cls.from_obj(
                child_node, serialze_postex=serialze_postex, serializer=serializer
            )
            node_data.nodes.append(node_data_child)

        for child_edge in graph.edges:
            node_origin, node_target = child_edge

            if serialze_postex:
                name_origin = node_origin.itername.split(".", 1)[-1]
                name_target = node_target.itername.split(".", 1)[-1]
            else:
                name_origin = node_origin.name
                name_target = node_target.name

            edge_data_child = EdgeData(origin=name_origin, target=name_target)
            node_data.edges.append(edge_data_child)

        return node_data


@dataclass
class WorkflowJSONMeta:
    """Data class for meta information."""

    pipeline_name: str
    stage: str
    time: datetime = dataclasses.field(
        default_factory=lambda: datetime.now().astimezone()
    )

    def filename(self) -> str:
        """Generate filename from fields"""
        timestamp = self.time.strftime("%Y-%m-%d_%H-%M-%S")
        return f"workflow_{self.stage}_{timestamp}_{self.pipeline_name}.json"


class WorkflowJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder. Unpacks dataclasses to dicts."""

    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return super().default(o)


def _save_workflow_json(
    workflow: WorkflowRaw,
    meta: WorkflowJSONMeta,
    custom_serializer: Optional[
        Callable[[Callable[[object], object], object], object]
    ] = None,
):
    node_data = NodeData.from_obj(
        workflow,
        serializer=_serialize_inout
        if custom_serializer is None
        else lambda o: custom_serializer(_serialize_inout, o),  # type: ignore
        serialze_postex=meta.stage == "post",
    )
    return workflow_container(workflow=node_data, meta=meta)


def save_workflow_json(
    filename: Union[str, PathLike],
    workflow: WorkflowRaw,
    meta: WorkflowJSONMeta,
    custom_serializer: Optional[
        Callable[[Callable[[object], object], object], object]
    ] = None,
) -> None:
    """
    Serialize and save workflow object to a file.
    Parameters
    ----------
    filename : Filename to save to.
    workflow : Workflow object.
    meta : Meta information. meta.stage has to be 'post' to trigger post-execution data serialization.
    custom_serializer : Optional function to convert custom node input and output data types.
        First argument is the internal serialization function, second any given object.
    """
    obj = _save_workflow_json(workflow, meta, custom_serializer)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(obj, file, indent=2, cls=WorkflowJSONEncoder)


def save_workflow_json_string(
    workflow: WorkflowRaw,
    meta: WorkflowJSONMeta,
    custom_serializer: Optional[
        Callable[[Callable[[object], object], object], object]
    ] = None,
) -> str:
    """
    Serialize and save workflow object to a file.
    Parameters
    ----------
    workflow : Workflow object.
    meta : Meta information. meta.stage has to be 'post' to trigger post-execution data serialization.
    custom_serializer : Optional function to convert custom node input and output data types.
        First argument is the internal serialization function, second any given object.
    """
    obj = _save_workflow_json(workflow, meta, custom_serializer)
    return json.dumps(obj, indent=2, cls=WorkflowJSONEncoder)
