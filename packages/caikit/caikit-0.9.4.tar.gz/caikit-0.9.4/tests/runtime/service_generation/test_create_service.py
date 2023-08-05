# Copyright The Caikit Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Standard
import uuid

# Local
from caikit.runtime.service_generation.create_service import (
    create_inference_rpcs,
    create_training_rpcs,
)
from sample_lib.data_model import SampleInputType, SampleOutputType, SampleTask
from sample_lib.modules import SampleModule
import caikit
import sample_lib

## Setup ########################################################################

widget_class = sample_lib.modules.sample_task.SampleModule

## Tests ########################################################################

### create_inference_rpcs tests #################################################


def test_create_inference_rpcs_uses_task_from_module_decorator():
    # make a new module with SampleTask
    @caikit.module(
        id=str(uuid.uuid4()), name="something", version="0.0.0", task=SampleTask
    )
    class NewModule(caikit.core.ModuleBase):
        def run(self, sample_input: SampleInputType) -> SampleOutputType:
            pass

    # SampleModule also implements `SampleTask`
    rpcs = create_inference_rpcs([NewModule, SampleModule])
    assert len(rpcs) == 1
    assert NewModule in rpcs[0].module_list
    assert SampleModule in rpcs[0].module_list


def test_create_inference_rpcs():
    rpcs = create_inference_rpcs([widget_class])
    assert len(rpcs) == 1
    assert widget_class in rpcs[0].module_list


def test_create_inference_rpcs_for_multiple_modules_of_same_type():
    module_list = [
        sample_lib.modules.sample_task.SampleModule,
        sample_lib.modules.sample_task.SamplePrimitiveModule,
        sample_lib.modules.other_task.OtherModule,
    ]
    rpcs = create_inference_rpcs(module_list)

    # only 2 RPCs, SampleModule and SamplePrimitiveModule have task SampleTask, OtherModule has task OtherTask
    assert len(rpcs) == 2
    assert sample_lib.modules.sample_task.SampleModule in rpcs[0].module_list
    assert sample_lib.modules.sample_task.SamplePrimitiveModule in rpcs[0].module_list
    assert sample_lib.modules.other_task.OtherModule in rpcs[1].module_list


def test_create_inference_rpcs_removes_modules_with_no_task():
    module_list = [
        sample_lib.modules.sample_task.SampleModule,  # has a task
        sample_lib.modules.sample_task.InnerModule,  # does not have a task
    ]
    rpcs = create_inference_rpcs(module_list)

    assert len(rpcs) == 1
    assert sample_lib.modules.sample_task.SampleModule in rpcs[0].module_list
    assert sample_lib.modules.sample_task.InnerModule not in rpcs[0].module_list


### create_training_rpcs tests #################################################


def test_no_training_rpcs_module_with_no_train_function():
    @caikit.module(
        id=str(uuid.uuid4()), name="something", version="0.0.0", task=SampleTask
    )
    class Foo(caikit.core.ModuleBase):
        def run(self, sample_input: SampleInputType) -> SampleOutputType:
            pass

        def train_in_progress(self):
            pass

    rpcs = create_training_rpcs([Foo])
    assert len(rpcs) == 0


def test_no_training_rpcs_for_module_with_no_task():
    @caikit.module(id=str(uuid.uuid4()), name="something", version="0.0.0")
    class Foo(caikit.core.ModuleBase):
        def train(self, foo: int) -> "Foo":
            pass

    rpcs = create_training_rpcs([Foo])
    assert len(rpcs) == 0


def test_create_training_rpcs():
    rpcs = create_training_rpcs([widget_class])
    assert len(rpcs) == 1
    assert widget_class in rpcs[0].module_list
