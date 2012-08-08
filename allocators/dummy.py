class DummyAllocator(object):
    def __init__(self, allocator_config, global_config):
        self.config = allocator_config
        self.global_config = global_config
        #self.node_registry = global_config.get_node_registry()
        #self.vm_registry = global_config.get_vm_registry()
    def allocate(self, vm, hint=None):
        return self.config.get('node', None)
        
