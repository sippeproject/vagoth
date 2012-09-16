#
# A registry using a filesystem as the database.
#

import couchdb
from .. import exceptions

class CouchRegistry(object):
    """
    self.nodes is set to the nodes table.
    self.unique is set to the unique keys table.

    Example node doc::

        "node001": {
            "node_id": "node001",
            "type": "type of node",
            "name": "nice node name",
            "definition": { ... node definition ... },
            "metadata": { ... node metadata ... },
            "unique_keys": [ "one", "two", "three" ],
            "parent": None,
        }
    """
    def __init__(self, manager, config):
        self.manager = manager
        self.couchdb = couchdb.Server(config['couch_server'])
        self.nodes = self.couchdb[config['couch_nodes_table']]
        self.unique = self.couchdb[config['couch_unique_table']]

    def list_nodes(self):
        return list(self.nodes)

    def get_nodes(self):
        for node_id in self.nodes:
            yield self.nodes[node_id]

    def __contains__(self, node_id):
        return node_id in self.nodes

    def get_node(self, node_id):
        "return dict for node"
        node = self.nodes.get(node_id, None)
        if node:
            return node
        raise exceptions.NodeNotFoundException("Node {0} not found in registry.".format(node_id))

    def get_node_by_name(self, name):
        "return dict for node"
        key = "VAGOTH_NAME_"+name
        if key in self.unique:
            node_id = self.unique[key]['node_id']
            if node_id in self.nodes:
                return self.nodes[node_id]
        raise exceptions.NodeNotFoundException("Node with name {0} not found in registry.".format(name))

    def get_node_by_key(self, key=None):
        "return the node with given unique key"
        if key and key in self.unique:
            node_id = self.unique[key]['node_id']
            return self.nodes.get(node_id, None)
        raise exceptions.NodeNotFoundException("Node with key {0} not found in registry.".format(key))

    def get_nodes_with_type(self, node_type=None):
        "return list of nodes with type" 
        # FIXME: inefficient
        for node_id in self.nodes:
            node = self.nodes[node_id]
            if node['type'] == node_type:
                yield node

    def get_nodes_with_tag(self, node_tag=None):
        "return list of nodes with the given tag"
        # FIXME: inefficient
        for node_id in self.nodes:
            node = self.nodes[node_id]
            tags = node.get('tags', [])
            if node_tag in tags:
                yield node

    def get_nodes_with_parent(self, parent=None):
        "return list of nodes with given parent"
        # FIXME: inefficient
        for node_id in self.nodes:
            node = self.nodes[node_id]
            if node.get('parent', None) == parent:
                yield node

    def set_parent(self, node_id, parent_node_id):
        """Set parent_node_id atomically, and don't overwrite another"""
        doc = self.nodes[node_id]
        current_parent = doc.get('parent', None)
        if current_parent and parent_node_id is not None:
            raise exceptions.NodeAlreadyHasParentException("Node {0} already has a parent of {1}".format(node_id, current_parent))
        doc['parent'] = parent_node_id
        try:
            self.nodes.save(doc)
        except couchdb.http.ResourceConflict as e:
            raise exceptions.RegistryException(*e.args)

    def _claim_unique_keys(self, node_id, new_keys, old_keys=None):
        """
        Make a claim for node_id on new_keys, and release any old keys.

        We want to do this in a safe fashion.. so we should claim
        all new keys first, then release any old keys, and clean up
        in the event of any conflict.
        """
        assert node_id is not None
        claimed_keys = []
        for key in new_keys:
            doc = self.unique.get(key, None)
            if doc:
                if doc['node_id'] == node_id:
                    continue
                else:
                    raise exceptions.UniqueConstraintViolation("Key {0} is not unique.".format(key))
            try:
                self.unique[key] = { "node_id": node_id }
                claimed_keys.append(key)
            except couchdb.http.ResourceConflict:
                for delkey in claimed_keys:
                    del self.unique[delkey]
        if old_keys:
            for old_key in old_keys:
                if old_key in new_keys:
                    continue
                try:
                    doc = self.unique[old_key]
                except couchdb.http.ResourceNotFound:
                    continue
                if doc.get('node_id', None) == node_id:
                    try:
                        self.unique.delete(doc)
                    except couchdb.http.ResourceConflict:
                        raise # FIXME
                        # not good - let a cleanup job fix it later
                        pass
                # else: DB is out of sync - let a cleanup job fix it later
        #
        # At this point, all new keys have been claimed, and any old keys
        # should have been released.  Even if some old keys remain, our
        # claim on new keys is assured (as much as it can be without rogue
        # processes)
        #

    def add_node(self, node_id, node_name, node_type, definition, metadata=None, unique_keys=None, tags=None):
        """
        Create new node in registry
        """
        if unique_keys is None: unique_keys = []
        if metadata is None: metadata = {}
        if tags is None: tags = []
        # create a bare document as a reservation
        try:
            self.nodes[node_id] = {
                "node_id": node_id,
                "type": node_type, # only set once
                "name": None,
                "definition": {},
                "metadata": {},
                "unique_keys": [],
                "tags": [],
                "parent": None,
            }
        except couchdb.http.ResourceConflict:
            raise exceptions.NodeAlreadyExistsException("Node {0} already exists in registry".format(node_id))
        doc = self.nodes[node_id]
        # add node_name to unique keys
        node_name_key = "VAGOTH_NAME_"+node_name
        if node_name_key not in unique_keys:
            unique_keys.insert(0, node_name_key)
        # claim all unique keys, or abort
        try:
            self._claim_unique_keys(node_id, unique_keys)
        except exceptions.UniqueConstraintViolation:
            self.nodes.delete(doc)
            raise
        # all unique keys have been claimed, so populate values
        doc['definition'] = definition
        doc['metadata'] = metadata
        doc['name'] = node_name
        doc['tags'] = tags
        doc['unique_keys'] = unique_keys[1:] # treat name specially
        self.nodes.save(doc)

    def _force_node_save(self, doc, count=5):
        """
        Attempt to save a node, despite any ResourceConflict's.
        """
        while count > 0:
            count -= 1
            try:
                self.nodes.save(doc)
                return
            except couchdb.http.ResourceConflict:
                newdoc = self.nodes[doc['_id']]
                doc['_rev'] = newdoc['_rev']
        raise exceptions.RegistryException("Could not write node %s to DB" % (doc['_id']))

    def set_node(self, node_id, node_name=None, definition=None, metadata=None, unique_keys=None, tags=None):
        """Change an existing node definition"""
        try:
            doc = self.nodes[node_id]
        except couchdb.http.ResourceNotFound:
            raise exceptions.NodeNotFoundException("Node {0} not found in registry.".format(node_id))
        new_name_key = None
        old_name_key = None
        if definition:
            doc['definition'] = definition
        if metadata:
            doc['metadata'] = metadata
        if tags:
            doc['tags'] = tags
        # update name (remember to cleanup old_name_key if set,
        #               or new_name_key on failure)
        if node_name and doc['name'] != node_name:
            new_name_key = 'VAGOTH_NAME_'+node_name
            self._claim_unique_keys(node_id, [new_name_key])
            old_name_key = 'VAGOTH_NAME_'+doc['name']
            doc['name'] = node_name
        if unique_keys:
            try:
                self._claim_unique_keys(node_id, unique_keys, doc['unique_keys'])
                doc['unique_keys'] = unique_keys
            except exceptions.UniqueConstraintViolation:
                if new_name_key:
                    self._claim_unique_keys(node_id, [], [new_name_key])
                raise
        self._force_node_save(doc)
        if old_name_key:
            del self.unique[old_name_key]

    def update_metadata(self, node_id, extra_metadata=None, delete_keys=None):
        """Update metadata with extra_metadata, and delete any keys in delete_keys"""
        doc = self.nodes[node_id]
        if extra_metadata:
            doc['metadata'].update(extra_metadata)
        if delete_keys:
            for key in delete_keys:
                if key in doc['metadata']:
                    del doc['metadata'][key]
        try:
            self.nodes.save(doc)
        except couchdb.http.ResourceConflict as e:
            raise exceptions.RegistryException(*e.args)

    def delete_node(self, node_id):
        """Delete the node identified by node_id"""
        try:
            doc = self.nodes[node_id]
        except couchdb.http.ResourceNotFound:
            raise exceptions.NodeNotFoundException("Node {0} not found in registry".format(node_id))
        unique_keys = doc.get('unique_keys', [])
        name_key = 'VAGOTH_NAME_'+doc['name']
        unique_keys.insert(0, name_key)
        self._claim_unique_keys(node_id, [], unique_keys)
        del self.nodes[node_id]
