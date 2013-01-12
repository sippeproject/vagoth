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

class DummyAllocator(object):
    def __init__(self, manager, allocator_config):
        self.config = allocator_config
        self.registry = manager.registry
    def _find_best_host_for(self, vm, hint=None):
        if hint:
            return hint
        return self.config.get('node', None)
    def allocate(self, vm, hint):
        hv_node_id = self._find_best_host_for(vm, hint)
        if hv_node_id:
            self.registry.set_parent(vm.node_id, hv_node_id)
            return hv_node_id
