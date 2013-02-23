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

class IDriver(object):
    def __init__(manager, config):
        """
        """
    def provision(node, vm):
        """
        Request the node to provision the VM (eg. define then re-init)
        """
    def define(node, vm):
        """
        Request the node to define the VM
        """
    def undefine(node, vm):
        """
        Request the node to undefine the VM
        """
    def deprovision(node, vm):
        """
        Request the node to deprovision the VM (eg. undefine & wipe disks)
        """
    def start(node, vm):
        """
        Request the node to start the VM (ie. power-on)
        """
    def reboot(node, vm):
        """
        Request the node to reboot the VM (poweroff/poweron)
        """
    def stop(node, vm):
        """
        Request the node to stop the VM (power-off)
        """
    def shutdown(node, vm):
        """
        Request the node to nicely shutdown the VM (eg. ACPI poweroff)
        """
    def info(node, vm):
        """
        Request the information dict about this VM.
        It should include "definition" with a dict, as well as "state",
        and possibly others.
        """
    def status(node=None):
        """
        Request the "status" for the entire node. This should include a
        "vms" dict, containing the info for each VM.
        """
    def migrate(node, vm, destination_node):
        """
        Request the node to migrate the VM to the destination_node.
        """
