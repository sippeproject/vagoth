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

"""
Registry of Nodes, backed by dictionaries

It also calls _load and _save methods before hand after any
operations, even though it's probably a no-op here.  It uses
a lock (by default threading.RLock) to lock write operations.

A different lock can passed in as an extra argument.
"""

from .. import exceptions
from .. import utils
from nodedoc import NodeDoc
from threading import RLock

class DictRegistry(object):
    """
    A simple thread-safe (but not process-safe) registry.

    self.nodes is set to the nodes dictionary.

    Example node dict::

        self.nodes = { "node001": {
            "node_id": "node001",
            "name": "node001",
            "type": "vm",
            "definition": { ... node definition ... },
            "metadata": { ... node metadata ... },
            "tags": [ "tag1", "tag2" ],
            "unique_keys": [ "ip-1.2.3.4" ],
            "parent": None,
        } }
    """
    def __init__(self, manager, config, lock=None):
        self.manager = manager
        self.config = config
        self.lock = lock or RLock()
        self.nodes = {}
        self.unique = {}

    def _load(self):
        """Override to load the nodes and unique dicts"""
        pass

    def _save(self):
        """Override to save the nodes and unique dicts"""
        pass

    def __contains__(self, node_id):
        return node_id in self.nodes

    def list_nodes(self):
        """Return a list of all node_id"""
        return self.nodes.keys()

    def _get_node(self, node_id):
        """Return a node doc for the given node_id"""
        self._load()
        try:
            return self.nodes[node_id]
        except KeyError:
            raise exceptions.NodeNotFoundException("Node %s not found in registry" % (node_id,))

    def get_node(self, node_id):
        return NodeDoc(self, self._get_node(node_id))

    def get_node_by_name(self, node_name):
        """Return a node doc for the node with the given node_name"""
        self._load()
        for node in self.nodes.itervalues():
            if node.get('name', None) == node_name:
                return NodeDoc(self, node)
        raise exceptions.NodeNotFoundException("Node not found in registry with name: %s" % (node_name,))

    def get_node_by_key(self, key):
        """Return a node doc for the node with the given key"""
        self._load()
        node_id = self.unique.get(key, None)
        if node_id:
            return self.get_node(node_id)
        raise exceptions.NodeNotFoundException("Node not found in registry with key: %s" % (key,))

    def get_nodes(self, tenant=False, node_type=None, tags=None, parent=False):
        """Return an iterable of node docs"""
        self._load()
        for node in self.nodes.values():
            if tenant is not False and node["tenant"] != tenant:
                continue
            if node_type and node["type"] != node_type:
                continue
            if parent is not False and not node["parent"] == parent:
                continue
            if tags and not utils.matches_tags(tags, node["tags"]):
                continue
            yield NodeDoc(self, node)

    def get_nodes_with_type(self, node_type):
        """Return an iterable of node docs with the given type"""
        self._load()
        for node in self.nodes.itervalues():
            if node['type'] == node_type:
                yield NodeDoc(self, node)

    def get_nodes_with_tags(self, tag_matches):
        """Return an iterable of node docs with the given tag

        :param tag_matches: key/value pairs to match. If the value is None,
            check for key existence only.
        :returns: iterable of node dict's
        """
        self._load()
        for node in self.nodes.itervalues():
            tags = node.get('tags', {})
            if type(tags) == list:
                tags = dict([(x,True) for x in tags])
            for tag_name, tag_value in tag_matches.items():
                if tag_name not in tags:
                    continue
                if tag_value is not None and tag_value != tags[tag_name]:
                    continue
                yield NodeDoc(self, node)

    def get_nodes_with_parent(self, node_parent):
        """Return an iterable of node docs with the given parent id"""
        self._load()
        for node in self.nodes.itervalues():
            if node.get('parent', None) == node_parent:
                yield NodeDoc(self, node)

    def set_parent(self, node_id, parent_node_id):
        """
        Set the parent node id, but only if it's not already set.
        It can also be used to set the parent back to to None.
        """
        with self.lock:
            self._load()
            try:
                node = self.nodes[node_id]
            except KeyError:
                raise exceptions.NodeNotFoundException("Node not found: %s" % (node_id,))
            parent = node.get("parent", None)
            if parent_node_id is None:
                node["parent"] = None
            elif parent is None:
                if parent_node_id in self.nodes:
                    node['parent'] = parent_node_id
                else:
                    raise exceptions.NodeNotFoundException("Parent node not found: %s" % (parent_node_id,))
            else:
                raise exceptions.NodeAlreadyHasParentException("Node already has a parent. Unassign it first: %s" % (node_id,))
            self._save()

    def add_node(self, node_id, node_name, node_type, tenant, definition=None, metadata=None, tags=None, unique_keys=None):
        """
        Add a new node to the registry, ensuring that the node_id,
        node_name, and keys are unique.
        """
        with self.lock:
            self._load()
            if node_id in self.nodes:
                raise exceptions.NodeAlreadyExistsException("Node already exists in registry: %s" % (node_id,))
            node = {
                "node_id": node_id,
                "name": node_name,
                "tenant": tenant,
                "type": node_type,
                "definition": definition or {},
                "metadata": metadata or {},
                "tags": tags or [],
                "unique_keys": unique_keys or [],
                "parent": None,
            }
            namekey = "VAGOTH_NAME_%s" % node_name
            if namekey in self.unique:
                raise exceptions.UniqueConstraintViolation("Node name already taken: %s" % (node_name,))
            for key in (unique_keys or []):
                if key in self.unique:
                    raise exceptions.UniqueConstraintViolation("Unique key is already taken: %s" % (key,))
            self.unique[namekey] = node_id
            for key in (unique_keys or []):
                self.unique[key] = node_id
            self.nodes[node_id] = node
            self._save()

    def set_node(self, node_id, node_name=None, tenant=None, definition=None, metadata=None, tags=None, unique_keys=None):
        """
        Update the node specified by node_id, ensuring that all uniqueness constraints are
        still valid. No changes will be made if there is the chance of a name or unique key
        collision.
        """
        with self.lock:
            self._load()
            try:
                node = self.nodes[node_id]
            except KeyError:
                raise exceptions.NodeNotFoundException("Node not found: %s" % (node_id,))
            if node_name and node_name != node["name"]:
                namekey = "VAGOTH_NAME_%s" % (node_name,)
                if namekey in self.unique:
                    raise exceptions.UniqueConstraintViolation("Node name already taken: %s" % (node_name,))
            if unique_keys:
                for key in unique_keys:
                    if key in self.unique and self.unique[key] != node_id:
                        raise exceptions.UniqueConstraintViolation("Unique key is already taken: %s" % (key,))
            if tenant:
                node["tenant"] = tenant
            if definition:
                node["definition"] = definition
            if metadata:
                node["metadata"] = metadata
            if tags:
                node["tags"] = tags
            if unique_keys: # unique_keys are the new set of keys
                for key in node["unique_keys"]:
                    if key in self.unique and self.unique[key] == node_id and key not in unique_keys:
                        del self.unique[key]
                for key in unique_keys:
                    if key not in self.unique:
                        self.unique[key] = node_id
                node["unique_keys"] = unique_keys
            if node_name:
                oldnamekey = "VAGOTH_NAME_%s" % (node["name"],)
                newnamekey = "VAGOTH_NAME_%s" % (node_name,)
                if oldnamekey != newnamekey:
                    del self.unique[oldnamekey]
                    self.unique[newnamekey] = node_id
                node["name"] = node_name
            self._save()

    def set_blob(self, node_id, key, value):
        """Set a blob for the given node_id and key to the given value"""
        with self.lock:
            self._load()
            try:
                node = self.nodes[node_id]
            except KeyError:
                raise exceptions.NodeNotFoundException("Node not found: %s" % (node_id,))
            if not node.has_key("blobs"):
                node["blobs"] = {}
            if value is None and key in node["blobs"]:
                del node["blobs"][key]
            else:
                node["blobs"][key] = value
            self._save()

    def get_blob(self, node_id, key):
        """Return the blob for the given node_id and key, or None"""
        node = self._get_node(node_id)
        blobs = node.get("blobs", {})
        return blobs.get(key, None)

    def update_metadata(self, node_id, extra_metadata, delete_keys=None):
        """Atomically update the metadata dict, or delete keys from it"""
        with self.lock:
            self._load()
            try:
                node = self.nodes[node_id]
            except KeyError:
                raise exceptions.NodeNotFoundException("Node not found: %s" % (node_id,))
            metadata = node.get('metadata', {})
            for key in (delete_keys or []):
                if key in metadata:
                    del metadata[key]
            if extra_metadata:
                metadata.update(extra_metadata)
            self._save()

    def delete_node(self, node_id):
        """Delete the given node, freeing up its resources"""
        with self.lock:
            try:
                node = self.nodes[node_id]
            except KeyError:
                raise exceptions.NodeNotFoundException("Node not found: %s" % (node_id,))
            if node.get("parent", None):
                raise exceptions.NodeStillUsedException("Node still has a parent: %s" % (node_id,))
            children = list(self.get_nodes_with_parent(node_id))
            if children:
                raise exceptions.NodeStillUsedException("Node still has children: %s" % (node_id,))
            # not in use, so delete it and its unique keys
            namekey = "VAGOTH_NAME_%s" % (node["name"],)
            if namekey in self.unique and self.unique[namekey] == node_id:
                del self.unique[namekey]
            for key in node.get("unique_keys", []):
                if key in self.unique and self.unique[key] == node_id:
                    del self.unique[key]
            del self.nodes[node_id]
            self._save()
