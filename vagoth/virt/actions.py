#
# Vagoth Cluster Management Framework
# Copyright (C) 2013  Robert Thomson
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#

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
    """
    Call logging.info(), using transaction.get_txid() and .get_source()
    along with the VM name and the message, if any.
    """
    txid = transaction.get_txid()
    source = transaction.get_source()
    if msg:
        logging.info("vagoth: txid={0} source={1} action={2} vm={3}: {4}".format(txid, source, action, vm_name, msg))
    else:
        logging.info("vagoth: txid={0} source={1} action={2} vm={3}".format(txid, source, action, vm_name))

def vm_define(manager, vm_name, hint=None, **kwargs):
    """
    If a VM isn't allocated to a hypervisor node, it will
    allocate it to a hypervisor node using the `Allocator`,
    and call driver.define(hypervisor, vm)
    """
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

def vm_provision(manager, vm_name, hint=None, **kwargs):
    """
    If a VM isn't allocated to a hypervisor node, it will
    allocate it to a hypervisor node using the `Allocator`,
    and call driver.provision(hypervisor, vm)
    """
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

def vm_start(manager, vm_name, **kwargs):
    """
    If a VM isn't allocated to a hypervisor node,
    it will call the vm_define action, and if that
    worked, call driver.start(hypervisor, vm)
    """
    log_vm_action(vm_name, "start")
    vm = manager.get_node(vm_name)
    node = vm.parent
    if not node:
        manager.action("vm_define", vm_name=vm_name, **kwargs)
        vm.refresh() # pick up state change
        node = vm.parent
    if node:
        vm.state = "starting"
        node.driver.start(node, vm)
    else:
        raise ActionException("VM not assigned")

def vm_stop(manager, vm_name, **kwargs):
    """
    call driver.stop(hypervisor, vm)
    """
    log_vm_action(vm_name, "stop")
    vm = manager.get_node(vm_name)
    node = vm.parent
    if node:
        vm.state = "stopping"
        node.driver.stop(node, vm)

def vm_shutdown(manager, vm_name, **kwargs):
    """
    call driver.stop(hypervisor, vm)
    """
    log_vm_action(vm_name, "stop")
    vm = manager.get_node(vm_name)
    node = vm.parent
    if node:
        vm.state = "shutting down"
        node.driver.shutdown(node, vm)

def vm_reboot(manager, vm_name, **kwargs):
    """
    call driver.reboot(hypervisor, vm)
    """
    log_vm_action(vm_name, "reboot")
    vm = manager.get_node(vm_name)
    node = vm.parent
    if node:
        vm.state = "rebooting"
        node.driver.reboot(node, vm)

def vm_undefine(manager, vm_name):
    """
    call driver.undefine(hypervisor, vm)
    """
    log_vm_action(vm_name, "undefine")
    vm = manager.get_node(vm_name)
    node = vm.parent
    if not node:
        return
    node.driver.undefine(node, vm)

def vm_deprovision(manager, vm_name):
    """
    call driver.deprovision(hypervisor, vm)
    """
    log_vm_action(vm_name, "deprovision")
    vm = manager.get_node(vm_name)
    node = vm.parent
    if not node:
        return
    node.driver.deprovision(node, vm)

def vm_poll(manager, **kwargs):
    """
    instantiate the monitor and poll all nodes
    """
    monitor = Manager.config.make_factory("virt/monitor", context=Manager)
    monitor.poll_nodes()
