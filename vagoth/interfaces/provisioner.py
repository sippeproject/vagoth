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

class IProvisioner(object):
    """
    The provisioner is called immediately before a VM is created in
    the cluster, and immediately before it is removed from the cluster.

    It will be given the vm_name and the vm_definition that were given
    when the provisioning API call was made.

    Depending on how you want to use Vagoth, you could simply pass through
    the VM definition as-is, or you may want to convert "vm_size": "small"
    into a fully fledged VM definition with IPs, storage, etc.

    You may also like to hook this into some DNS and DHCP API to create
    entries for the host.

    If an exception is raised during the provision() call, or None is
    returned, then the provisioning will not take place.

    If an exception is raised during the deprovision() call, then the
    VM will remain in the cluster, but keep a state of "DELETED", so
    that a future cleanup job can finish the deprovisioning.
    """
    def __init__(manager, config, global_config):
        """Takes the manager, local config dict and the global config object"""
    def provision(node_id, node_name=None, node_type=None, definition=None, metadata=None, tags=None, unique_keys=None):
        """Return a valid vm definition for this cluster"""
    def deprovision(vm_name, vm_definition):
        """
        Do any cleanup of resources etc. before this VM definition is
        removed from the cluster.
        """
