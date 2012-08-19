"""
A basic VirtualMachine class, wrapping the node attributes.

It extends Node, which exposes the underlying node_doc
"""

from ..node import Node

class VirtualMachine(Node):
    def __init__(self, manager, node_id, node_doc):
        super(VirtualMachine, self).__init__(manager, node_id, node_doc)
        self._scheduler = manager.scheduler
        self._registry = manager.registry

    @property
    def state(self):
        return self._doc['metadata'].get('state', 'unknown')

    @state.setter
    def state(self, state):
        self.refresh()
        metadata = self._doc['metadata']
        metadata['state'] = state
        self._registry.set_node(self.node_id, metadata=metadata)

    def start(self, hint=None):
        self._scheduler.action(self.node_id, "start", vm_name=self.node_id, hint=hint)

    def stop(self):
        self._scheduler.action(self.node_id, "stop", vm_name=self.node_id)

    def shutdown(self):
        self._scheduler.action(self.node_id, "shutdown", vm_name=self.node_id)

    def reboot(self):
        self._scheduler.action(self.node_id, "reboot", vm_name=self.node_id)

    def undefine(self):
        self._scheduler.action(self.node_id, "undefine", vm_name=self.node_id)

    def deprovision(self):
        self._scheduler.action(self.node_id, "deprovision", vm_name=self.node_id)

    def __str__(self):
        return self.node_id

    def __repr__(self):
        return "<VirtualMachine %s at %x>" % (self.node_id, id(self))

