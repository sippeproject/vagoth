"""
A basic VirtualMachine instance.
"""

class VirtualMachine(object):
    def __init__(self, name, manager, config=None):
        assert isinstance(name, basestring)
        self.name = name
        self.scheduler = manager.scheduler
        self.registry = manager.registry
        self.manager = manager
        self.config = config

    def get_name(self):
        return self.name

    def get_node(self):
        node_name = self.registry.get_vm_location(self.name)
        if node_name:
            return self.manager.get_node(node_name)

    def get_definition(self):
        return self.registry.get_vm_definition(self.name)

    def get_metadata(self):
        return self.registry.get_vm_metadata(self.name)

    def get_state(self):
        return self.registry.get_vm_state(self.name)

    # definition's don't change
    #def set_definition(self, definition):
    #    return self.registry.set_vm_definition(definition)
    #
    def set_metadata(self, metadata):
        return self.registry.set_vm_metadata(self.name, metadata)

    def set_state(self, state):
        return self.registry.set_vm_state(self.name, state)

    def start(self, hint=None):
        self.scheduler.action(self.name, "start", vm_name=self.name, hint=hint)

    def stop(self):
        self.scheduler.action(self.name, "stop", vm_name=self.name)

    def shutdown(self):
        self.scheduler.action(self.name, "shutdown", vm_name=self.name)

    def reboot(self):
        self.scheduler.action(self.name, "reboot", vm_name=self.name)

    def undefine(self):
        self.scheduler.action(self.name, "undefine", vm_name=self.name)

    def deprovision(self):
        self.scheduler.action(self.name, "deprovision", vm_name=self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<VirtualMachine %s at %x>" % (self.name, id(self))
