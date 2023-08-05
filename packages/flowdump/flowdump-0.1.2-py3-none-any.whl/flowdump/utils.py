import pathlib as pl
from os import PathLike
from typing import Callable, Optional, Union

from .core import WorkflowRaw
from .workflow_json import WorkflowJSONMeta, save_workflow_json


def run_and_save_workflow(
    workflow: WorkflowRaw,
    out_dir: Union[PathLike, str],
    workflow_name: Optional[str] = None,
    custom_serializer: Optional[
        Callable[[Callable[[object], object], object], object]
    ] = None,
) -> None:
    """
    Run a workflow and save the results to a directory.

    Parameters
    ----------
    workflow : The workflow to run.
    out_dir : The directory to save the results to.
    workflow_name : The name of the workflow. If None, the name will be "Workflow".
    custom_serializer : An optional custom serializer to use when saving the workflow JSON.
        Accepts a function that takes the default flowdump serializer and an object and
        returns the serialized object.

    Returns
    -------
    None
    """

    out_dir = pl.Path(out_dir)
    workflow_name = "Workflow" if workflow_name is None else workflow_name

    workflow_meta = WorkflowJSONMeta(pipeline_name=workflow_name, stage="pre")
    save_workflow_json(
        filename=out_dir / workflow_meta.filename(),
        workflow=workflow,
        meta=workflow_meta,
        custom_serializer=custom_serializer,
    )

    amazing_workflow_result = workflow.run()

    workflow_meta.stage = "post"
    save_workflow_json(
        filename=out_dir / workflow_meta.filename(),
        workflow=amazing_workflow_result,
        meta=workflow_meta,
        custom_serializer=custom_serializer,
    )
