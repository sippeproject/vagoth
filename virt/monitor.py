from .. import exceptions
import logging

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
        provisioner = self.manager.provisioner
        logging.info("Creating VM %r on %r: %r" % (vm_name, node, vm_status))
        provisioner.provision(vm_name, node_name=vm_name, node_type='vm',
            definition = vm_status['definition'],
            metadata = { 'state': vm_name }
        )
        vm = self.manager.get_node(vm_name)
        self.manager.registry.set_parent(vm_name, node.node_id)

    def unassign_vm(self, vm):
        self.manager.registry.set_parent(vm.node_id, None)
        vm.state = "unassigned"

    def update_node(self, node, status):
        vms = {}
        for vm_status in status:
            vm_name = vm_status["definition"]["name"]
            vms[vm_name] = vm_status
            vm_state, vm_target_state = vm_status["state"]
            try:
                vm = self.manager.get_node(vm_name)
            except exceptions.NodeNotFoundException:
                if self.create_missing:
                    self.create_vm(vm_name, vm_status, node)
                    vm = self.manager.get_node(vm_name)
                else:
                    logging.warn("VM {0} not found. Skipping.".format(vm_name))
                    continue

            # inconsistency detected:
            # if VM is running on a node, but isn't assigned to it, then assign it
            if vm and not vm.parent:
                self.manager.registry.set_parent(vm_name, node.node_id)
                logging.warn("Auto-assigning {0} to {1}".format(vm_name, node.node_id))

            # update state:
            if vm and vm.parent == node:
                if vm.state != vm_state:
                    vm.state = vm_state
                    logging.debug("Setting VM state for {0} to {1}".format(vm_name, vm_state))

        for vm in self.manager.get_nodes_with_parent(node.node_id):
            # any VMs assigned to node, but not active?
            if vm.node_id not in vms:
                logging.debug("Unassigning VM {0} from {1}".format(vm.node_id, node.node_id))
                self.unassign_vm(vm)

    def poll_nodes(self):
        for node in self.manager.get_nodes_with_type("hv"):
            driver = node.driver
            if driver:
                try:
                    node_status = driver.status(node)
                    self.update_node(node, node_status)
                except: # FIXME
                    raise
