from ..node import Node

class Hypervisor(Node):
    """
    A basic Hypervisor class.  A hypervisor has a driver
    """

    def __init__(self, manager, node_id, node_doc):
        super(Hypervisor, self).__init__(manager, node_id, node_doc)

    # FIXME, duplicated in VirtualMachine (but not really a Node thing)
    @property
    def state(self):
        return self._doc['metadata'].get('state', 'unknown')

    @state.setter
    def state(self, state):
        self.refresh()
        metadata = self._doc['metadata']
        metadata['state'] = state
        self.manager.registry.set_node(self.node_id, metadata=metadata)
        self.refresh()

    @property
    def children(self):
        return manager.get_nodes_with_parent(self._node_id)

    @property
    def driver(self):
        factory, config = self._manager.config.get_factory("virt/driver")
        return factory(config, self._manager.config)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Hypervisor %s at %x>" % (self.node_id, id(self))
