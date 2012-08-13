"""
This scheduler is suitable for small installations and frontend tools where
making synchronous calls to the hypervisor driver is appropriate.

For example, a command line VM management tool.
"""

from .. import exceptions

class SyncJobScheduler(object):
    """
    SyncJobScheduler makes synchronous calls to the hypervisor drivers
    """
    def __init__(self, manager, config):
        self.manager = manager
        self.config = config

    # deprecated
    def provision_vm(self, vm, hint=None):
        # how will "vmmon" handle a VM which is assigned to a HV, but isn't yet defined on it?
        self.manager.action("provision", vm_name=vm.get_name(), hint=hint)

    # deprecated
    def define_vm(self, vm, hint=None):
        # how will "vmmon" handle a VM which is assigned to a HV, but isn't yet defined on it?
        self.manager.action("define", vm_name=vm.get_name(), hint=hint)

    # deprecated
    def start_vm(self, vm, hint=None):
        self.manager.action("start", vm_name=vm.get_name(), hint=hint)

    # deprecated
    def stop_vm(self, vm):
        self.manager.action("stop", vm_name=vm.get_name())

    # deprecated
    def shutdown_vm(self, vm):
        self.manager.action("shutdown", vm_name=vm.get_name())

    # deprecated
    def reboot_vm(self, vm):
        self.manager.action("reboot", vm_name=vm.get_name())

    # deprecated
    def undefine_vm(self, vm):
        self.manager.action("undefine", vm_name=vm.get_name())

    # deprecated
    def deprovision_vm(self, vm):
        self.manager.action("deprovision", vm_name=vm.get_name())

    # deprecated
    def migrate_vm(self, vm, new_node):
        self.manager.action("migrate", vm_name=vm.get_name(), dest_node=new_node.get_name())

    # new style
    def action(self, queue_name, action, **kwargs):
        self.manager.action(action, **kwargs)
