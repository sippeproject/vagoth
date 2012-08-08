# Test Manager class

import unittest

from ..manager import Manager
from ..registry.dictregistry import DictRegistry

class ManagerTest(unittest.TestCase):
    def setUp(self):
        self.manager = Manager()
        # use the in-memory DictRegistry for testing...
        reg = DictRegistry({}, {})
        self.manager.vm_registry = reg
        self.manager.node_registry = reg

    def test_define_node(self):
        node_definition = {
            "fqdn": "nator.home.corporatism.org",
            "description": "Nator LXC HV",
            "tags": "vmtype-lxc",
            "ram": 8192,
            "cpu": 4,
        }
        node_metadata = {}
        self.manager.define_node("nator", node_definition, node_metadata)
        vm = self.manager.get_node("nator")

    def test_define_vm(self):
        vm_definition = {
            "name": "dummy",
            "description": "Dummy VM",
            "cpu": 1,
            "ram": 512,
            "vm_type": "dummy",
        }
        vm_metadata = {}
        self.manager.define_vm("dummy", vm_definition, vm_metadata)
        vm = self.manager.get_vm("dummy")

