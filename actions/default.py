"""
Actions are called by the job scheduler to perform tasks.
They contain a dictionary of arguments, but will be called
with an instance of Vagoth's Manager as the first argument.
"""

from ..exceptions import ActionException

def define(manager, vm_name, hint=None, **kwargs):
    manager.log.log_vm_action(vm_name, "define")
    vm = manager.get_vm(vm_name)
    node = vm.get_node()
    if node:
        return
    manager.allocate_vm(vm, hint)
    node = vm.get_node()
    if node:
        vm.set_state("defined")
        node.get_driver().define(node, vm)

def provision(manager, vm_name, hint=None, **kwargs):
    manager.log.log_vm_action(vm_name, "provision")
    vm = manager.get_vm(vm_name)
    node = vm.get_node()
    if node:
        return
    manager.allocate_vm(vm, hint)
    node = vm.get_node()
    if node:
        vm.set_state("defined")
        node.get_driver().define(node, vm)


def start(manager, vm_name, **kwargs):
    manager.log.log_vm_action(vm_name, "start")
    vm = manager.get_vm(vm_name)
    node = vm.get_node()
    if not node:
        manager.action("define", vm_name=vm_name, **kwargs)
        node = vm.get_node()
    if node:
        vm.set_state("starting")
        node.get_driver().start(node, vm)
    else:
        raise ActionException("VM not assigned")

def stop(manager, vm_name, **kwargs):
    manager.log.log_vm_action(vm_name, "stop")
    vm = manager.get_vm(vm_name)
    node = vm.get_node()
    if node:
        vm.set_state("stopping")
        node.get_driver().stop(node, vm)

def shutdown(manager, vm_name, **kwargs):
    manager.log.log_vm_action(vm_name, "stop")
    vm = manager.get_vm(vm_name)
    node = vm.get_node()
    if node:
        vm.set_state("shutting down")
        node.get_driver().shutdown(node, vm)

def reboot(manager, vm_name, **kwargs):
    manager.log.log_vm_action(vm_name, "reboot")
    vm = manager.get_vm(vm_name)
    node = vm.get_node()
    if node:
        vm.set_state("rebooting")
        node.get_driver().reboot(node, vm)

def undefine(manager, vm_name):
    manager.log.log_vm_action(vm_name, "undefine")
    vm = manager.get_vm(vm_name)
    node = vm.get_node()
    if not node:
        return
    node.get_driver().undefine(node, vm)

def deprovision(manager, vm_name):
    manager.log.log_vm_action(vm_name, "deprovision")
    vm = manager.get_vm(vm_name)
    node = vm.get_node()
    if not node:
        return
    node.get_driver().deprovision(node, vm)

def poll(manager, **kwargs):
    manager.monitor
