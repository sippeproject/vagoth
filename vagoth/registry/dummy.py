#
# Vagoth Cluster Management Framework
# Copyright (C) 2013  Robert Thomson
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#

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
