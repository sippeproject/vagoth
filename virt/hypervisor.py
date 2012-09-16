from ..node import Node

class Hypervisor(Node):
    """
    A basic Hypervisor class.  A hypervisor has a driver

    It inherits vagoth.Node_
    """

    def __init__(self, manager, node_id, node_doc):
        super(Hypervisor, self).__init__(manager, node_id, node_doc)

    # FIXME, duplicated in VirtualMachine (but not really a Node thing)
    @property
    def state(self):
        """Retrieve the state attribute from the metadata"""
        return self._doc['metadata'].get('state', 'unknown')

    @state.setter
    def state(self, state):
        """Set the state attribute in the metadata"""
        self._manager.registry.update_metadata(self.node_id, { "state": state, })
        self.refresh()

    @property
    def children(self):
        """Return the children of this hypervisor"""
        return self._manager.get_nodes_with_parent(self._node_id)

    @property
    def driver(self):
        """Return the driver for this hypervisor"""
        return self._manager.config.make_factory("virt/driver", self._manager)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Hypervisor %s at %x>" % (self.node_id, id(self))
