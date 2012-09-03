class Node(object):
    """
    A Node represents a node entry in the Registry.

    The node_doc dict it receives should contain the following keys:
        node_id - same as node_id passed in
        name - a string
        definition - a dict
        metadata - a dict
        parent - None, or the instance of the parent Node
        tags - list of strings
        keys - list of strings

    It exposes all of the above as attributes for reading.

    No setter's are provided for the above, as it's expected that you'll
    inherit this class and provide any methods you require there.
    """
    def __init__(self, manager, node_id, node_doc):
        self._manager = manager
        self._node_id = node_id
        self._doc = node_doc

    def refresh(self):
        self._doc = self._manager.registry.get_node(self.node_id)

    # ensure it's read-only
    @property
    def node_id(self):
        return self._node_id

    @property
    def node_type(self):
        return self._doc['type']

    @property
    def name(self):
        return self._doc['name']

    @property
    def definition(self):
        return self._doc['definition']

    @property
    def metadata(self):
        return self._doc['metadata']

    @property
    def parent(self):
        parent = self._doc['parent']
        if parent:
            return self._manager.get_node(parent)

    @property
    def tags(self):
        return list(self._doc['tags'])

    @property
    def keys(self):
        return list(self._doc['keys'])

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Node %s at %x>" % (self.node_id, id(self))

    def __eq__(self, other):
        assert other is None or isinstance(other, Node)
        return self.node_id == other.node_id
