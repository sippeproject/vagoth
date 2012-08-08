"""

"""

class DummyRegistry(object):
    def __init__(self):
        self.nodes = {}
        self.vms = {}

    def _get_vm_attr(vm_name, key):
        vm = self.vms.get(vm_name, None)
        if vm is None:
            return None
        return vm[key]

    def _set_vm_attr(vm_name, definition=None, metadata=None, state=None):
        vm = self.vms.get(vm_name, None)
        if vm is None:
            self.vms[vm_name] = {
                "definition": definition,
                "metadata": metadata,
                "state": state,
            }
            return
        if definition is not None:
            vm["definition"] = definition
        if metadata is not None:
            vm["metadata"] = metadata
        if state is not None:
            if not isinstance(state, basestring):
                raise TypeError("state must be a string value, not %s" % type(state))
            vm["state"] = state

    def get_vm_definition(self, vm_name):
        return self._get_vm_attr("definition")

    def set_vm_definition(self, vm_name, definition):
        self._set_vm_attr(vm_name, definition=definition)

    def get_vm_metadata(self, vm_name):
        return self._get_vm_attr("metadata")

    def set_vm_metadata(self, vm_name, metadata):
        self._set_vm_attr(vm_name, metadata=metadata)

    def get_vm_state(self, vm_name):
        return self._get_vm_attr("state")

    def set_vm_state(self, vm_name, state):
        return self._get_vm_attr("state", state=state)

    def define_vm(self, vm_name, definition, metadata=None, state='defined'):
        pass
