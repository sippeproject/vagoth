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

import zope.interface as ZI

class IProvisioner(ZI.Interface):
    """
    The provisioner is called to add a node to the cluster, and to
    remove a node from the cluster.

    It is the responsibility of the Provisioner to ensure that a node
    is correct and valid before adding it to Vagoth.

    Depending on how you want to use Vagoth, you could simply pass through
    the definition as-is to the registry, or you may want to convert
    "vm_size": "small" into a fully fledged definition complete
    with IPs, storage, etc.

    You may also like to hook this into some DNS and DHCP API to create
    entries for the host.

    vagoth.exceptions.ProvisioningException is the only exception
    that should be handled.  All other exceptions are undefined
    behaviour.

    If ProvisioningException is raised during the provision() call
    then the node has not been provisioned in the cluster.

    If ProvisioningException is raised during the deprovision() call,
    then the node remains in the cluster.
    """
    def __init__(manager, config):
        """Takes the manager, local config dict and the global config object"""
    def provision(node_id, node_name=None, node_type=None, tenant=None, definition=None, metadata=None, tags=None, unique_keys=None):
        """
        Do all required steps to provision the given node in Vagoth, including adding to the registry.
        Throw a ProvisioningException if there were any issues.
        """
    def deprovision(node_id):
        """
        Do any cleanup of resources etc. before this VM definition is
        removed from the cluster.
        """
