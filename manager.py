# *-* vim: ft=python softtabstop=4 expandtab

"""
The Manager class is the front door to the Vagoth API.

Use manager.get_manager() to get a singleton.
"""

from config import Config
import exceptions
import logging

class Manager(object):
    def __init__(self, config=None):
        config = self.config = config or Config()
        self.registry = config.get_registry()
        self.allocator = config.get_allocator()
        self.driver = config.get_driver()
        self.vm_factory, self.vm_config = config.get_vm_factory()
        self.node_factory, self.node_config = config.get_node_factory()
        # scheduler
        sched_factory, sched_config = config.get_scheduler_factory()
        self.scheduler = sched_factory(self, sched_config)
        # provisioner
        provisioner_factory, provisioner_config = self.config.get_provisioner_factory()
        self.provisioner = provisioner_factory(self, provisioner_config, config)
        # monitor
        monitor_factory, monitor_config = config.get_monitor_factory()
        self.monitor = monitor_factory(self, monitor_config)
        # logger
        self.log = config.get_logger()

    def get_vm(self, vm_name):
        vmdef = self.registry.get_vm_definition(vm_name) # can throw exception
        return self.vm_factory(vm_name, self, config=self.vm_config)

    def get_node(self, node_name):
        nodedef = self.registry.get_node_definition(node_name) # can throw exception
        return self.node_factory(node_name, self, self.driver, self.registry, config=self.vm_config)

    def list_vms(self):
        return self.registry.get_vms()

    def list_nodes(self):
        return self.registry.get_nodes()

    def define_node(self, name, definition=None, metadata=None):
        node = self.registry.define_node(name, definition or {}, metadata or {})
        return node

    def undefine_node(self, node):
        return NotImplemented
        # FIXME - ensure that no VMs are on it
        self.registry.undefine_node(node.get_name())

    def define_vm(self, name, definition=None, metadata=None):
        """
        Provision a VM in the cluster. It will first call the provisioner to
        check & update the given VM definition as appropriate, then it will
        add the VM to the VM registry.  In the event of an error while adding
        the VM to the registry, the provisioner will be called again to
        deprovision the VM definition.
        """
        try:
            # should throw exception if it doesn't exist
            self.registry.get_vm_definition(name)
            raise VMAlreadyExistsException("VM %s is already in registry" % (existing_vm,))
        except exceptions.VMNotFoundException:
            pass
        provisioner = self.config.get_provisioner()
        new_definition = provisioner.provision(name, definition)
        if new_definition is not None:
            try:
                vm = self.registry.define_vm(name, new_definition, metadata or {})
                return vm
            except:
                provisioner.deprovision(name, new_definition)
                raise

    def undefine_vm(self, vm):
        """
        If a VM isn't allocated anywhere, then we will call the provisioner to
        deprovision it, then remove the vm_state entry.
        """
        node = vm.get_node()
        self.registry.undefine_vm(vm.get_name())

    def allocate_vm_to_node(self, vm, node):
        current_node = self.registry.get_vm_location(vm.get_name())
        if current_node and current_node != node:
            raise VMAlreadyAssignedException("VM %s already assigned to %s." % (vm, node))
        if not current_node:
            self.registry.set_vm_location(vm.get_name(), node.get_name())
        node.driver.define(node, vm)
        # if there's an exception, registry will be cleaned up by a separate poll

    def allocate_vm(self, vm, hint=None):
        """Find an appropriate node for this VM"""
        if vm.get_node() != None:
            print "Node is currently assigned to %s." % (vm.get_node())
        node_name = self.allocator.allocate(vm, hint) # raises AllocationException
        node = self.get_node(node_name)
        self.allocate_vm_to_node(vm, node)

    def unallocate_vm(self, vm):
        """Remove a VM from a node, but leave it in the cluster"""
        node = vm.get_node()
        if node:
            result = node.driver.undefine(node, vm)
        # if successful, registry will be cleaned up by a separate poll

    def action(self, action, **kwargs):
        action_func = self.config.get_action(action)
        action_func(self, **kwargs)

manager = None
def get_manager(config=None):
    global manager
    if manager is None:
        manager = Manager(config=config)
    return manager

