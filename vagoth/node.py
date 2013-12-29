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

import utils

class Node(object):
    """
    A Node represents a node entry in the Registry.

    Node is an extensible wrapper for an INodeDoc instance, which is
    a read-only snapshot of a node from the registry.

    It's expected that specific node types will inherit this Node
    and add python-API-friendly functionality to it.
    """
    def __init__(self, manager, node_doc):
        """
        :param manager: vagoth.manager.Manager instance
        :param node_id: ID of node
        :param node_doc: must implement INodeDoc
        """
        self._manager = manager
        self._node_id = node_doc.id
        self._doc = node_doc

    def refresh(self):
        """
        Refresh node data by querying the registry for the latest INodeDoc
        """
        self._doc = self._manager.registry.get_node(self.node_id)

    # ensure it's read-only
    @property
    def node_id(self):
        """The unique and immutable id of this node"""
        return self._node_id

    @property
    def node_type(self):
        """The immutable type of this node"""
        return self._doc.type

    @property
    def name(self):
        """The unique but mutable name of this node"""
        return self._doc.name

    @property
    def definition(self):
        """The definition dictionary"""
        return self._doc.definition

    @property
    def metadata(self):
        """The metadata dictionary"""
        return self._doc.metadata

    @property
    def parent_id(self):
        """The node id of the parent node of this one, if set"""
        parent_id = self._doc.parent
        if parent_id:
            return parent_id

    @property
    def parent(self):
        """The parent node of this one, if set"""
        parent_id = self._doc.parent
        if parent_id:
            return self._manager.get_node(parent_id)

    @property
    def tags(self):
        """Dict of all tags for this node"""
        return self._doc.tags

    @property
    def tenant(self):
        return self._doc.tenant

    @property
    def unique_keys(self):
        """List of all unique keys for this node"""
        return list(self._doc.unique_keys)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Node %s at %x>" % (self.node_id, id(self))

    def __eq__(self, other):
        assert other is None or isinstance(other, Node)
        if other is None:
            return False
        return self.node_id == other.node_id

    def __ne__(self, other):
        return not self == other

    def matches_tags(self, tag_matches):
        """Does this node match the given tags?

        For each key/value pair, check if the tag exists, and if the value is
        not None, if the value matches.
        """
        return utils.matches_tags(tag_matches, self._doc.tags or {})
