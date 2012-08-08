#
#
#

from .. import exceptions

class SyncJobScheduler(object):
    """
    SyncWorkQueue makes synchronous calls to the hypervisor drivers
    """
    def __init__(self, manager, config):
        self.manager = manager
        self.config = config

    def _get_node(self, vm):
        node = vm.get_node()
        if not node:
            raise exceptions.VMNotAssignedException("Action called on an unassigned VM: %s" % (vm.get_name()))
        return node

    def provision_vm(self, node, vm):
        # how will "vmmon" handle a VM which is assigned to a HV, but isn't yet defined on it?
        node.get_driver().provision(node, vm)

    def define_vm(self, node, vm):
        # how will "vmmon" handle a VM which is assigned to a HV, but isn't yet defined on it?
        node.get_driver().define(node, vm)

    def start_vm(self, vm):
        node = self._get_node(vm)
        node.get_driver().start(node, vm)
        # TODO - catch result/exception & log it

    def stop_vm(self, vm):
        node = self._get_node(vm)
        node.get_driver().reboot(node, vm)
        # TODO - catch result/exception & log it

    def stop_vm(self, vm):
        node = self._get_node(vm)
        node.get_driver().stop(node, vm)
        # TODO - catch result/exception & log it

    def shutdown_vm(self, vm):
        node = self._get_node(vm)
        node.get_driver().shutdown(node, vm)
        # TODO - catch result/exception & log it

    def undefine_vm(self, vm):
        node = self._get_node(vm)
        node.get_driver().undefine_vm(node, vm)
        # TODO - catch result/exception & log it

    def deprovision_vm(self, vm):
        node = self._get_node(vm)
        node.get_driver().deprovision(node, vm)
        # TODO - catch result/exception & log it

    def migrate_vm(self, vm, new_node):
        node = self._get_node(vm)
        node.get_driver().migrate(node, vm)

