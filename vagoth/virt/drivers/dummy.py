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

from ..utils.mc_json_rpc import mcollective_call
from ..exceptions import DriverException

ERRMSG = "Cannot manage VMs on a Hypervisor using DummyDriver"

class DummyDriver(object):
    """
    The Dummy Driver never has info and raises a DriverException if you try to use it.
    """
    def __init__(self, manager, local_config):
        self.config = local_config

    def provision(self, node, vm):
        """Request a node to define & provision a VM"""
        raise DriverException(ERRMSG)

    def define(self, node, vm):
        """Request node to define a VM"""
        raise DriverException(ERRMSG)

    def undefine(self, node, vm):
        """Request node to undefine a VM"""
        raise DriverException(ERRMSG)

    def deprovision(self, node, vm):
        """Request node to undefine & deprovision a VM"""
        raise DriverException(ERRMSG)

    def start(self, node, vm):
        """Request node to start the VM"""
        raise DriverException(ERRMSG)

    def reboot(self, node, vm):
        """Request node to reboot the VM"""
        raise DriverException(ERRMSG)

    def stop(self, node, vm):
        """Request node to stop (forcefully) the VM"""
        raise DriverException(ERRMSG)

    def shutdown(self, node, vm):
        """Request node to shutdown (nicely) the VM"""
        raise DriverException(ERRMSG)

    def info(self, node, vm):
        """Request information about the given VM from the node"""
        return {}

    def status(self, node=None):
        """Request information about all VMs from the node"""
        return []

    def migrate(self, node, vm, destination_node):
        """Request the node to migrate the given VM to the destination node"""
        return NotImplemented
