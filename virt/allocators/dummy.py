class DummyAllocator(object):
    def __init__(self, manager, allocator_config):
        self.config = allocator_config
        self.registry = manager.registry
    def _find_best_host_for(self, vm, hint=None):
        if hint:
            return hint
        return self.config.get('node', None)
    def allocate(self, vm, hint):
        hv_node_id = self._find_best_host_for(vm, hint)
        if hv_node_id:
            self.registry.set_parent(vm.node_id, hv_node_id)
            return hv_node_id
