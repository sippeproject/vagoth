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

from ..exceptions import NodeAlreadyExistsException
from ..exceptions import NodeStillUsedException

class DummyProvisioner(object):
    """
    DummyProvisioner does the bare minimum for a provisioner,
    creating a node in the registry with the same
    information that was passed into it.
    """

    def __init__(self, manager, config):
        self.manager = manager

    def provision(self, node_id,
                  node_name=None,
                  node_type=None,
                  tenant=None,
                  definition=None,
                  metadata=None,
                  tags=None,
                  unique_keys=None):
        # ensure it's a new node
        if node_id in self.manager.registry:
            raise NodeAlreadyExistsException("Node {0} already exists in registry".format(node_id))
        self.manager.registry.add_node(node_id,
            node_name = node_name or node_id,
            node_type = node_type,
            tenant = tenant,
            definition = definition,
            metadata = metadata,
            tags = tags,
            unique_keys = unique_keys
        )

    def deprovision(self, node_id):
        node = self.manager.registry.get_node(node_id) # throws NodeNotFoundException
        parent_node_id = node['parent']
        # check for a parent
        if parent_node_id and parent_node_id in self.manager.registry:
            raise NodeStillUsedException("Node {0} has a parent assigned.".format(node_id))
        # check for children
        children = list(self.manager.registry.get_nodes_with_parent(node_id))
        if len(children) > 0:
            raise NodeStillUsedException("Node {0} has children assigned.".format(node_id))
        # node seems like an orphan, so it's ok to delete it
        self.manager.registry.delete_node(node_id)
