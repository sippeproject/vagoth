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

class IRegistry(ZI.Interface):
    """
    The registry provides the data store for Vagoth.  It maintains
    nodes, their type, definition, metadata, tags, unique keys,
    blobs, and whether they have a parent.  It lets you add new nodes,
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
        """Return the node identified by node_id

        :param node_id: node identifier
        :returns: INodeDoc
        """

    def get_node_by_name(node_name):
        """Return an the node with the name of node_name

        :param node_name: human-friendly (but still unique) name of node
        :returns: INodeDoc
        """

    def get_node_by_key(unique_key):
        """Return the node with the given unique key

        :param unique_key: unique key to search for
        :returns: INodeDoc
        """

    def get_nodes(tenant=None, node_type=None, tags=None, parent=None):
        """
        Returns all nodes which match the supplied filters.

        :returns: Iterable of INodeDoc's
        """

    def get_nodes_with_type(node_type):
        """Return all nodes with a matching type

        :param node_type: node type to match
        :returns: Iteratable of INodeDoc's
        """

    def get_nodes_with_tags(tag_matches):
        """Returns all nodes which match the given tags

        :param tag_matches: dict of key-value pairs that must match
        :returns: Iterable of INodeDoc's
        """

    def get_nodes_with_parent(node_parent):
        """Returns all node who have the given parent

        :param node_parent: parent's node id
        :returns: Iterable of INodeDoc's
        """

    def set_parent(node_id, parent_node_id):
        """
        Set the child's parent to parent_node_id.

        If parent_node_id is None, this will remove the child-parent relationship.

        If a parent is already assigned, this will throw an exception.
        """

    def add_node(node_id, node_name, node_type, tenant, definition=None, metadata=None, tags=None, unique_keys=None):
        """
        Add a node to the registry
        """

    def set_node(node_id, node_name=None, tenant=None, definition=None, metadata=None, tags=None, unique_keys=None):
        """
        Change attributes of an existing node in the registry.
        All parameters except node_id are optional.

        :param node_id: unique ID of the node
        :param node_name: unique name of the node
        :param tenant: name/identifier of the tenant (owner/project)
        :param definition: definition dictionary
        :param metadata: metadata dictionary
        :param tags: tags dictionary
        :param unique_keys: list of unique keys to claim
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

        :param node_id: unique ID of the node
        :param extra_metadata: dict of metadata to add to existing metadata dict
        :param delete_keys: list of metadata keys to delete
        """

    def set_blob(node_id, key, value):
        """
        Set a blob for the given node_id and (string) key to value.

        Blobs are undefined types, and may be stored separately to
        the rest of the node metadata in a given registry implementation.

        It's recommended to use 'metadata' instead, if it makes sense.
        """

    def get_blob(node_id, key):
        """
        Return the blob for the given node_id and (string) key.
        """

    def __contains__(node_id):
        """
        A shortcut to see if the given node is in the registry
        """
