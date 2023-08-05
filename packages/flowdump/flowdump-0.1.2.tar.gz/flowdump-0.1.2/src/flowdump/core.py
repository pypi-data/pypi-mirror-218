from typing import Any

from nipype import __version__ as version_nipype
from nipype.pipeline.engine import Node, Workflow

WorkflowRaw = Workflow
"""Alias for internal use."""

NodeRaw = Node
"""Alias for internal use."""

VERSION_WORKFLOW = 1
"""Placeholder for version checking. Increase when file structure changes drastically."""


def workflow_container(workflow: Any, meta: Any = None) -> dict:
    """
    Construct a container dictionary with some version information to allow version checks when reading.
    Parameters
    ----------
    workflow : Workflow object.
    meta : Meta information.
    Returns
    -------
    dict
    """
    return {
        "version": {"workflow": VERSION_WORKFLOW, "nipype": version_nipype},
        "meta": {} if meta is None else meta,
        "workflow": workflow,
    }
