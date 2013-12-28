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

class Hypervisor(Node):
    """
    A basic Hypervisor class.  A hypervisor has a driver

    It inherits vagoth.Node_
    """

    # FIXME, duplicated in VirtualMachine (but not really a Node thing)
    @property
    def state(self):
        """Retrieve the state attribute from the metadata"""
        return self._doc.metadata.get('state', 'unknown')

    @state.setter
    def state(self, state):
        """Set the state attribute in the metadata"""
        self._doc.registry.update_metadata(self.node_id, { "state": state, })
        self.refresh()

    @property
    def children(self):
        """Return the children of this hypervisor"""
        return self._manager.get_nodes_with_parent(self._node_id)

    @property
    def driver_name(self):
        """Return the driver name for this hypervisor, or default"""
        driver_name = self.definition.get('driver', 'default')
        assert isinstance(driver_name, basestring)
        return driver_name

    @property
    def driver(self):
        """Return the driver for this hypervisor"""
        return self._manager.config.make_factory("virt/drivers/%s" % (self.driver_name,), self._manager)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Hypervisor %s at %x>" % (self.node_id, id(self))
