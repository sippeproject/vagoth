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

from ..node import Node

class VirtualMachine(Node):
    """
    `VirtualMachine` represents a VirtualMachine node type.

    It inherits vagoth.Node_

    Each method requests the scheduler to execute the related action.
    """

    @property
    def state(self):
        """Retrieve the state attribute from the metadata"""
        return self._doc.metadata.get('state', 'unknown')

    @state.setter
    def state(self, state):
        """Set the state attribute in the metadata"""
        self._doc.registry.update_metadata(self.node_id, { "state": state, })
        self.refresh()

    def start(self, hint=None):
        """Schedule the start action"""
        self._manager.scheduler.action(self.node_id, "vm_start", vm_name=self.node_id, hint=hint)

    def define(self, hint=None):
        """Schedule the define action"""
        self._manager.scheduler.action(self.node_id, "vm_define", vm_name=self.node_id, hint=hint)

    def stop(self):
        """Schedule the stop action"""
        self._manager.scheduler.action(self.node_id, "vm_stop", vm_name=self.node_id)

    def shutdown(self):
        """Schedule the shutdown action"""
        self._manager.scheduler.action(self.node_id, "vm_shutdown", vm_name=self.node_id)

    def reboot(self):
        """Schedule the reboot action"""
        self._manager.scheduler.action(self.node_id, "vm_reboot", vm_name=self.node_id)

    def undefine(self):
        """Schedule the undefine action"""
        self._manager.scheduler.action(self.node_id, "vm_undefine", vm_name=self.node_id)

    def provision(self):
        """Schedule the provision action"""
        self._manager.scheduler.action(self.node_id, "vm_provision", vm_name=self.node_id)

    def deprovision(self):
        """Schedule the deprovision action"""
        self._manager.scheduler.action(self.node_id, "vm_deprovision", vm_name=self.node_id)

    def __str__(self):
        return self.node_id

    def __repr__(self):
        return "<VirtualMachine %s at %x>" % (self.node_id, id(self))

