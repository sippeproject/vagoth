"""
A basic VirtualMachine instance.
"""

class VirtualMachine(object):
    def __init__(self, name, manager, config=None):
        assert isinstance(name, basestring)
        self.name = name
        self.scheduler = manager.scheduler
        self.vm_registry = manager.vm_registry
        self.manager = manager
        self.config = config

    def get_name(self):
        return self.name

    def get_node(self):
        node_name = self.vm_registry.get_vm_location(self.name)
        if node_name:
            return self.manager.get_node(node_name)
  
    def get_definition(self):
        return self.vm_registry.get_vm_definition(self.name)
        
    def get_metadata(self):
        return self.vm_registry.get_vm_metadata(self.name)

    def get_state(self):
        return self.vm_registry.get_vm_state(self.name)

    # definition's don't change
    #def set_definition(self, definition):
    #    return self.vm_registry.set_vm_definition(definition)
    #
    def set_metadata(self, metadata):
        return self.vm_registry.set_vm_metadata(self.name, metadata)

    def set_state(self, state):
        return self.vm_registry.set_vm_state(self.name, state)

    def start(self):
        self.scheduler.start_vm(self)

    def stop(self):
        self.scheduler.stop_vm(self)

    def reboot(self):
        self.scheduler.reboot_vm(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<VirtualMachine %s at %x>" % (self.name, id(self))
