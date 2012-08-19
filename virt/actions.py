"""
Actions are called by the job scheduler to perform tasks.
They contain a dictionary of arguments, but will be called
with an instance of Vagoth's Manager as the first argument.
"""

from ..exceptions import ActionException
from .. import get_manager
from .. import transaction
import logging

Manager = get_manager()
Allocator = Manager.config.make_factory("virt/allocator", context=Manager)

def log_vm_action(vm_name, action, msg=None):
    txid = transaction.get_txid()
    source = transaction.get_source()
    if msg:
        logging.info("vagoth: txid={0} source={1} action={2} vm={3}: {4}".format(txid, source, action, vm_name, msg))
    else:
        logging.info("vagoth: txid={0} source={1} action={2} vm={3}".format(txid, source, action, vm_name))

def define(manager, vm_name, hint=None, **kwargs):
    global Allocator
    log_vm_action(vm_name, "define")
    vm = manager.get_node(vm_name)
    node = vm.parent
    if node:
        return
    Allocator.allocate(vm, hint)
    vm.refresh()
    node = vm.parent
    if node:
        vm.state = "defined"
        node.driver.define(node, vm)

def provision(manager, vm_name, hint=None, **kwargs):
    global Allocator
    log_vm_action(vm_name, "provision")
    vm = manager.get_node(vm_name)
    node = vm.parent
    if node:
        return
    Allocator.allocate(vm, hint)
    vm.refresh()
    node = vm.parent
    if node:
        vm.state = "defined"
        node.driver.define(node, vm)

def start(manager, vm_name, **kwargs):
    log_vm_action(vm_name, "start")
    vm = manager.get_node(vm_name)
    node = vm.parent
    if not node:
        manager.action("define", vm_name=vm_name, **kwargs)
        vm.refresh() # pick up state change
        node = vm.parent
    if node:
        vm.state = "starting"
        node.driver.start(node, vm)
    else:
        raise ActionException("VM not assigned")

def stop(manager, vm_name, **kwargs):
    log_vm_action(vm_name, "stop")
    vm = manager.get_node(vm_name)
    node = vm.parent
    if node:
        vm.state = "stopping"
        node.driver.stop(node, vm)

def shutdown(manager, vm_name, **kwargs):
    log_vm_action(vm_name, "stop")
    vm = manager.get_node(vm_name)
    node = vm.parent
    if node:
        vm.state = "shutting down"
        node.driver.shutdown(node, vm)

def reboot(manager, vm_name, **kwargs):
    log_vm_action(vm_name, "reboot")
    vm = manager.get_node(vm_name)
    node = vm.parent
    if node:
        vm.state = "rebooting"
        node.driver.reboot(node, vm)

def undefine(manager, vm_name):
    log_vm_action(vm_name, "undefine")
    vm = manager.get_node(vm_name)
    node = vm.parent
    if not node:
        return
    node.driver.undefine(node, vm)

def deprovision(manager, vm_name):
    log_vm_action(vm_name, "deprovision")
    vm = manager.get_node(vm_name)
    node = vm.parent
    if not node:
        return
    node.driver.deprovision(node, vm)

def poll(manager, **kwargs):
    monitor = Manager.config.make_factory("virt/monitor", context=Manager)
    monitor.poll_nodes()
