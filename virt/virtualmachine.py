from ..node import Node

class VirtualMachine(Node):
    """
    `VirtualMachine` represents a VirtualMachine node type.

    It inherits vagoth.Node_

    Each method requests the scheduler to execute the related action.
    """
    def __init__(self, manager, node_id, node_doc):
        super(VirtualMachine, self).__init__(manager, node_id, node_doc)
        self._scheduler = manager.scheduler
        self._registry = manager.registry

    @property
    def state(self):
        """Retrieve the state attribute from the metadata"""
        return self._doc['metadata'].get('state', 'unknown')

    @state.setter
    def state(self, state):
        """Set the state attribute in the metadata"""
        self._registry.update_metadata(self.node_id, { "state": state, })
        self.refresh()

    def start(self, hint=None):
        """Schedule the start action"""
        self._scheduler.action(self.node_id, "vm_start", vm_name=self.node_id, hint=hint)

    def stop(self):
        """Schedule the stop action"""
        self._scheduler.action(self.node_id, "vm_stop", vm_name=self.node_id)

    def shutdown(self):
        """Schedule the shutdown action"""
        self._scheduler.action(self.node_id, "vm_shutdown", vm_name=self.node_id)

    def reboot(self):
        """Schedule the reboot action"""
        self._scheduler.action(self.node_id, "vm_reboot", vm_name=self.node_id)

    def undefine(self):
        """Schedule the undefine action"""
        self._scheduler.action(self.node_id, "vm_undefine", vm_name=self.node_id)

    def provision(self):
        """Schedule the provision action"""
        self._scheduler.action(self.node_id, "vm_provision", vm_name=self.node_id)

    def deprovision(self):
        """Schedule the deprovision action"""
        self._scheduler.action(self.node_id, "vm_deprovision", vm_name=self.node_id)

    def __str__(self):
        return self.node_id

    def __repr__(self):
        return "<VirtualMachine %s at %x>" % (self.node_id, id(self))

