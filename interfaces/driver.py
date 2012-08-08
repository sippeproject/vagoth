class IDriver:
    def __init__(local_config, global_config):
        """
        """
    def provision(node, vm):
        """
        Request the node to provision the VM (eg. define then re-init)
        """
    def define(node, vm):
        """
        Request the node to define the VM
        """
    def undefine(node, vm):
        """
        Request the node to undefine the VM
        """
    def deprovision(node, vm):
        """
        Request the node to deprovision the VM (eg. undefine & wipe disks)
        """
    def start(node, vm):
        """
        Request the node to start the VM (ie. power-on)
        """
    def reboot(node, vm):
        """
        Request the node to reboot the VM (poweroff/poweron)
        """
    def stop(node, vm):
        """
        Request the node to stop the VM (power-off)
        """
    def shutdown(node, vm):
        """
        Request the node to nicely shutdown the VM (eg. ACPI poweroff)
        """
    def info(node, vm):
        """
        Request the information dict about this VM.
        It should include "definition" with a dict, as well as "state",
        and possibly others.
        """
    def status(node=None):
        """
        Request the "status" for the entire node. This should include a
        "vms" dict, containing the info for each VM.
        """
    def migrate(node, vm, destination_node):
        """
        Request the node to migrate the VM to the destination_node.
        """
