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

#
# A wrapper for a Node Document/Dict
#

class NodeDoc(object):
    """
    An encapsulation of the node dictionary, implementing INodeDoc
    """
    def __init__(self, registry, node_dict):
        self.registry = registry
        self.node_dict = node_dict
        assert "type" in node_dict
        assert "node_id" in node_dict
        assert "name" in node_dict
        assert "parent" in node_dict
        assert "definition" in node_dict
        assert "unique_keys" in node_dict
        if "tenant" not in node_dict:
            node_dict["tenant"] = None
        if "metadata" not in node_dict:
            node_dict["metadata"] = {}
        if "tags" not in node_dict:
            node_dict["tags"] = {}
        elif type(node_dict["tags"]) == list: # migrate to dict..
            node_dict["tags"] = dict([(x,True) for x in node_dict["tags"]])

    @property
    def type(self):
        return self.node_dict["type"]

    @property
    def id(self):
        return self.node_dict["node_id"]

    @property
    def name(self):
        return self.node_dict["name"]

    @property
    def definition(self):
        return self.node_dict["definition"]

    @property
    def metadata(self):
        return self.node_dict["metadata"]

    @property
    def parent(self):
        return self.node_dict["parent"]

    @property
    def tags(self):
        return self.node_dict["tags"]

    @property
    def unique_keys(self):
        return self.node_dict["unique_keys"]

    @property
    def tenant(self):
        return self.node_dict["tenant"]

    def get_blob(self, key):
        return self.registry.get_blob(self.id, key)

    def __getitem__(self, key):
        raise NotImplementedError

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def __str__(self):
        return "NodeDoc for %s" % (self.id,)

    def __repr__(self):
        return "<NodeDoc for %s at 0x%x>" % (self.id, id(self))
