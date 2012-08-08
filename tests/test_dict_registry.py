# test the DictRegistry (basis of PickleRegistry)

import unittest

from ..registry.dictregistry import DictRegistry

class DictRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = DictRegistry({}, {})

    def test_add_node(self):
        self.reg.define_node("n001", {"ram": 128*1024, "cpu": 16}, {})
        assert len(self.reg.nodes) == 1
