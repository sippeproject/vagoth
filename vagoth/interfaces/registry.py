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

class IRegistry(object):
    """
    The registry provides the data store for Vagoth.  It maintains
    nodes, their type, definition, metadata, tags, unique keys,
    and whether they have a parent.  It lets you add new nodes,
    change node attributes, and atomically set the parent and
    update metadata.
    """
    def __init__(manager, config):
        """
        Registry is initialized with the manager, and its config dict
        """

    def list_nodes():
        """
        Return an iterable of node_id's in the registry
        """

    def get_node(node_id):
        """
        Return a dictionary of a single node's data.

        For example:
        {
            "node_id": "node001",
            "name": "nice node name",
            "type": "vm",
            "definition": { ... node definition ... },
            "metadata": { ... node metadata ... },
            "keys": [ "ip-1.2.3.4", "mac-aa:bb:cc:dd:ee:ff", "storage-nfs-VMS1/node001" ],
            "tags": [ "user-foobar" ]
            "parent": None,
        }
        """

    def get_node_by_name(node_name):
        """
        Return the node with the given name of node_name
        """

    def get_node_by_key(key=None):
        """
        Return the node with given unique key
        """

    def get_nodes():
        """
        Returns an iterator returning each node's dictionary (see get_node)
        """

    def get_nodes_with_type(node_type=None):
        """
        Returns an iterator, returning each node's dictionary (see get_node)
        if node_type is the same.
        """

    def get_nodes_with_tags(tag_matches=None):
        """
        Returns an iterator, returning each node's dictionary (see get_node),
        where the given tags are set for the node.
        """

    def get_nodes_with_parent(node_parent=None):
        """
        Returns an iterator, returning each node's dictionary (see get_node),
        where the given node has a parent of node_parent
        """

    def set_parent(node_id, parent_node_id):
        """
        Set the child's parent to parent_node_id.

        If parent_node_id is None, this will remove the child-parent relationship.

        If a parent is already assigned, this will throw an exception.
        """

    def add_node(node_id, node_name, node_type, definition, metadata=None, tags=None, unique_keys=None):
        """
        Add a node to the registry
        """

    def set_node(node_id, node_name, definition=None, metadata=None, tags=None, unique_keys=None):
        """
        Change attributes of an existing node in the registry
        """

    def update_metadata(node_id, extra_metadata, delete_keys=None):
        """
        Atomically call metadata.update(extra_metadata) and delete each key
        in delete_keys.

        This is available because set_node() will overwrite the existing
        metadata en-masse, which with multiple systems could lead to a race
        condition and unexpected results.

        Metadata, unlike definition, tags, and keys, is likely to be changed
        regularly by multiple processes, and it therefore justifies an extra
        method.
        """

    def __contains__(node_id):
        """
        A shortcut to see if the given node is in the registry
        """
