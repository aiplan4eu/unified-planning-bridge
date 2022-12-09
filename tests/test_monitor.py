# Copyright 2022 Sebastian Stock, DFKI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from unified_planning.engines import SequentialSimulator
from unified_planning.model import UPCOWState
from unified_planning.test.examples import get_example_problems

from up_bridge.plexmo.monitor import SequentialPlanMonitor


class TestSequentialMonitor(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._example = get_example_problems()["hierarchical_blocks_world"]

    def test_check_preconditions(self):
        instance = self._example.plan.actions[0]
        monitor = SequentialPlanMonitor(self._example.problem)
        state = UPCOWState(self._example.problem.initial_values)
        self.assertTrue(monitor.check_preconditions(instance, state)[0])

        # after applying the first action, its preconditions are not fulfilled, anymore
        simulator = SequentialSimulator(self._example.problem)
        events = simulator.get_events(instance.action, instance.actual_parameters)
        state = simulator.apply(events[0], state)
        self.assertFalse(monitor.check_preconditions(instance, state)[0])
