import exceptions

class Monitor(object):
    """
    For each node, call driver.status, and update VM state.
    """
    def __init__(self, manager, config):
        self.manager = manager
        if config.get('create_missing', False) in ('true','yes',True):
            self.create_missing = True
        else:
            self.create_missing = False

    def create_vm(self, vm_name, vm_status, node):
        self.manager.define_vm(vm_name, vm_status["definition"], {})
        vm = self.manager.get_vm(vm_name)
        self.manager.vm_manager.set_vm_location(vm_name, node.get_name())

    def update_node(self, node, status):
        vms = []
        for vm_status in status:
            vm_name = vm_status["definition"]["name"]
            vm_target_state, vm_state = vm_status["state"]
            try:
                vm = self.manager.get_vm(vm_name)
            except exceptions.VMNotFoundException:
                if self.create_missing:
                    self.create_vm(vm_name, vm_status, node)
                else:
                    print "VM {0} not found. Skipping.".format(vm_name)
                    continue

            # inconsistency detected:
            # if VM is running on a node, but isn't assigned to it, then assign it
            if vm and not vm.get_node():
                self.manager.vm_registry.set_vm_location(vm_name, node.get_name())

            # update state:
            if vm and vm.get_node().get_name() == node.get_name():
                if vm.get_state() != vm_state:
                    self.manager.vm_registry.set_vm_state(vm_name, vm_state)
                    print "Setting VM state for {0} to {1}".format(vm_name, vm_state)

    def poll_nodes(self):
        for node_name in self.manager.list_nodes():
            node = self.manager.get_node(node_name)
            driver = node.get_driver()
            if driver:
                try:
                    node_status = driver.status(node)
                    self.update_node(node, node_status)
                except: # FIXME
                    raise
