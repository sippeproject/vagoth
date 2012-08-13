#
# Registry of VMs and Hypervisors
#
# The registry is not concerned with reality, only in maintaining
# its database of nodes and vms, and the DB consistency.
#

import pickle
import os.path
from .. import exceptions
from threading import RLock

class DictRegistry(object):
    """
    A simple thread-safe (but not process-safe) registry.

    self.vms is set to the VM dictionary.
    self.nodes is set to the nodes dictionary.

    Example VM dict:
    self.vms = { "vm_name": {
      "definition": { ... vm definition ... },
      "metadata": { ... vm metadata ... },
      "state": "defined"|"autostart"|"stopped"|"migrating",
      "parent": "node001"
    } }

    Example node dict:
    self.nodes = { "node001": {
        "definition": { ... node definition ... },
        "metadata": { ... node metadata ... },
        "state": { "up"|"down"|"locked" },
        "children": [ "node001", ],
    } }
    """
    def __init__(self, config, global_config, lock=None):
        self.config = config
        self.global_config = global_config
        self.lock = lock or RLock()
        self.nodes = {}
        self.vms = {}
        self._load()

    def _load(self):
        pass

    def _save(self):
        pass

    def get_vms(self, load=True):
        if load: self._load()
        return self.vms.keys()

    def get_vm(self, vm_name, load=True):
        if load: self._load()
        if vm_name in self.vms:
            return self.vms[vm_name]
        else:
            raise exceptions.VMNotFoundException("VM %s not found in registry" % (vm_name,))

    def get_nodes(self, load=True):
        if load: self._load()
        return self.nodes.keys()

    def get_node(self, node_name, load=True):
        if load: self._load()
        if node_name in self.nodes:
            return self.nodes[node_name]
        else:
            raise exceptions.NodeNotFoundException("Node %s not found in registry" % (node_name,))

    # VM definition, as set at creation time
    def get_vm_definition(self, vm_name, load=True):
        vm = self.get_vm(vm_name, load)
        if vm:
            return vm["definition"]

    def set_vm_definition(self, vm_name, vm_definition):
        # TODO: ensure that VM isn't assigned anywhere first
        with self.lock:
            self._load()
            if self.get_node():
                raise VMStillAssignedException("Cannot change VM definition while VM is assigned to node")
            self.vms[vm_name]["definition"] = vm_definition
            self._save()

    # Metadata
    def get_vm_metadata(self, vm_name, load=True):
        vm = self.get_vm(vm_name)
        if vm:
            return vm["metadata"]

    def set_vm_metadata(self, vm_name, metadata):
        with self.lock:
            vm = self.get_vm(vm_name, load=True)
            if vm["metadata"] != metadata:
                vm["metadata"] = metadata
                self._save()

    # VM state, as last returned by hypervisor
    def get_vm_state(self, vm_name, load=True):
        return self.get_vm(vm_name).get("state", "unknown")

    def set_vm_state(self, vm_name, state):
        with self.lock:
            vm = self.get_vm(vm_name, load=True)
            if vm["state"] != state:
                vm["state"] = state
                self._save()

    # VM target state, as maintained by Vagoth
    def get_vm_target_state(self, vm_name, load=True):
        return self.get_vm(vm_name).get("target_state", None)

    def set_vm_target_state(self, vm_name, target_state):
        with self.lock:
            vm = self.get_vm(vm_name, load=True)
            if vm["target_state"] != state:
                vm["target_state"] = state
                self._save()
        return self.get_vm(vm_name).get("target_state", None)

    # VM location
    def get_vm_location(self, vm_name, load=True):
        vm = self.get_vm(vm_name, load=load)
        return vm.get("parent", None)

    # last polled VM status from node
    def set_vm_last_status(self, vm_name, status):
        with self.lock:
            vm = self.get_vm(vm_name, load=True)
            if vm.get("last_status", None) != status:
                vm["last_status"] = status
                self._save()

    def get_vm_last_status(self, vm_name):
        vm = self.get_vm(vm_name, load=True)
        return vm.get('last_status', None)

    # last polled node status
    def set_node_last_status(self, node_name, status):
        with self.lock:
            node = self.get_node(node_name, load=True)
            if node.get("last_status", None) != status:
                node["last_status"] = status
                self._save()

    def get_node_last_status(self, node_name):
        node = self.get_node(node_name, load=True)
        return node.get('last_status', None)

    # children names
    def get_node_children(self, node_name):
        node = self.get_node(node_name, load=True)
        return node.get('children')[:]

    def define_vm(self, vm_name, vm_definition, vm_metadata, vm_state="defined"):
        """Create a new VM entry in the DB"""
        with self.lock:
            self._load()
            if vm_name in self.vms:
                raise exceptions.VMAlreadyExistsException("VM already exists in registry: %s" % (vm_name,))
            # TODO: check for all unique keys before creating VM
            self.vms[vm_name] = {
                "definition": vm_definition,
                "metadata": vm_metadata,
                "state": vm_state,
                "node": None,
            }
            self._save()


    def undefine_vm(self, vm_name):
        with self.lock:
            self._load()
            if vm_name not in self.vms:
                raise VMNotFoundException("VM %s not found in registry when undefining" % (vm_name,))
            if vm_name in self.vms and self.vms[vm_name].get("parent", None) != None:
                raise exceptions.VMStillAssignedException("VM %s is still assigned to %s" % (vm_name, self.vms["node"]))
            del self.vms[vm_name]
            self._save()

    def define_node(self, name, definition, metadata, state="available"):
        with self.lock:
            self._load()
            if name in self.nodes:
                raise exceptions.NodeAlreadyExistsException("Node already exists in registry: %s" % (name,))
            self.nodes[name] = {
                "definition": definition,
                "metadata": metadata,
                "state": state,
            }
            self._save()

    def undefine_node(self, node_name):
        with self.lock:
            self._load()
            if node_name not in self.nodes:
                raise exceptions.NodeNotFoundException("Node %s not found in registry" % (node_name,))
            node = self.nodes[name]
            if len(node["children"]) > 0:
                raise NodeStillUsedException("Cannot undefine node %s because it still has VMs assigned to it" % (node_name,))
            del self.nodes[name]
            self._save()

    # Node state, as set by vagoth
    def get_node_state(self, node_name, load=True):
        return self.get_node(node_name)["state"]

    def set_node_state(self, node_name, state):
        with self.lock:
            node = self.get_node(node_name, load=True)
            if node["state"] != state:
                node["state"] = state
                self._save()

    # Node state, as set by vagoth
    def get_node_definition(self, node_name, load=True):
        return self.get_node(node_name)["definition"]

    def set_node_definition(self, node_name, definition):
        with self.lock:
            node = self.get_node(node_name, load=True)
            if node["definition"] != definition:
                node["definition"] = definition
                self._save()

    def set_vm_location(self, vm_name, node_name):
        # TODO: add force (to support migration)
        with self.lock:
            vm = self.get_vm(vm_name)
            if node_name is None:
                old_parent = vm.get("parent", None)
                if old_parent is not None:
                    # unassign it from the previous node
                    if old_parent in self.nodes:
                        node = self.get_node(old_parent, load=False)
                        node_children = node.get("children", None)
                        if node_children and vm_name in node_children:
                            node_children.remove(vm_name)
                    vm["parent"] = None
                    self._save()
                return None
            node = self.get_node(node_name, load=False)
            if vm.get("parent", None) and vm["parent"] != node_name:
                raise exceptions.VMAlreadyAssignedException("VM %s is assigned to another node, not reassigning" % (vm_name,))
            children = node.get("children", [])
            if vm_name not in children:
                children.append(vm_name)
                children.sort()
                node["children"] = children
            vm["parent"] = node_name
            self._save()
