# `flowdump`

[![Build](https://github.com/cmi-dair/flowdump/actions/workflows/python_tests.yaml/badge.svg?branch=main)](https://github.com/cmi-dair/flowdump/actions/workflows/python_tests.yaml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/cmi-dair/flowdump/branch/main/graph/badge.svg?token=22HWWFWPW5)](https://codecov.io/gh/cmi-dair/flowdump)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![L-GPL License](https://img.shields.io/badge/license-L--GPL-blue.svg)](LICENSE)

NiPype-1 workflow serializer for use with [`flowview`](https://cmi-dair.github.io/flowview/).

## Installation

`flowdump` is available on PyPI and can be installed with `pip`:

```bash
pip install flowdump
```

## Usage

Using `flowdump` is as simple as calling `run_and_save_workflow` on a NiPype-1 workflow object.
This will execute the workflow and save the pre- and post-execution workflow data to JSON files.

```Python
import nipype.pipeline.engine as pe  # pypeline engine
from flowdump import run_and_save_workflow

# Typical NiPype workflow creation
amazing_workflow = pe.Workflow(name="main_workflow")
# amazing_workflow.connect(...)
# amazing_workflow.connect(...)
# amazing_workflow.connect(...)

# Let `flowdump` execute and save pre- and post-execution data.
run_and_save_workflow(
    amazing_workflow,
    out_dir='my/target/dir'
)
```

### Advanced:

If more control over the workflow execution is needed, the workflow can be
serialized manually.


```Python
import nipype.pipeline.engine as pe  # pypeline engine
import os.path
from flowdump import WorkflowJSONMeta, save_workflow_json

# Typical NiPype workflow creation
amazing_workflow = pe.Workflow(name="main_workflow")
# amazing_workflow.connect(...)
# amazing_workflow.connect(...)
# amazing_workflow.connect(...)

# Create workflow metadata object (traces execution time and stage)
workflow_meta = WorkflowJSONMeta(
    pipeline_name='My amazing pipeline',
    stage='pre'
)
# Dump pre-execution workflow
save_workflow_json(
    filename=os.path.join('my/target/dir', workflow_meta.filename()),
    workflow=amazing_workflow,
    meta=workflow_meta
)

# Execute NiPype workflow
amazing_workflow_result = amazing_workflow.run()

# Update metadata
workflow_meta.stage = 'post'
# Dump post-execution workflow
save_workflow_json(
    filename=os.path.join('my/target/dir', workflow_meta.filename()),
    workflow=amazing_workflow_result,
    meta=workflow_meta
)
```

### Custom field serialization

Custom serializers can be implemented for projects with custom NiPype Node types.
The serializer is a function that takes a the default `flowdump` serializer 
function (to optionally fall back to) and an object and returns a JSON-serializable 
object.

```Python
def my_custom_serializer(
        flowdump_serializer: Callable[[object], object],
        obj: object
):
    if isinstance(obj, MyType):
        return my_make_string(obj)
    return flowdump_serializer(obj)

save_workflow_json(
    filename=os.path.join('my/target/dir', workflow_meta.filename()),
    workflow=amazing_workflow_result,
    meta=workflow_meta
)
```