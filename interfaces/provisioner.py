class IProvisioner(object):
    """
    The provisioner is called immediately before a VM is created in
    the cluster, and immediately before it is removed from the cluster.

    It will be given the vm_name and the vm_definition that were given
    when the provisioning API call was made.

    Depending on how you want to use Vagoth, you could simply pass through
    the VM definition as-is, or you may want to convert "vm_size": "small"
    into a fully fledged VM definition with IPs, storage, etc.

    You may also like to hook this into some DNS and DHCP API to create
    entries for the host.

    If an exception is raised during the provision() call, or None is
    returned, then the provisioning will not take place.

    If an exception is raised during the deprovision() call, then the
    VM will remain in the cluster, but keep a state of "DELETED", so
    that a future cleanup job can finish the deprovisioning.
    """
    def __init__(config, global_config):
        """Takes the local config dict and the global config object"""
    def provision(vm_name, vm_definition):
        """Return a valid vm definition for this cluster"""
    def deprovision(vm_name, vm_definition):
        """
        Do any cleanup of resources etc. before this VM definition is
        removed from the cluster.
        """
