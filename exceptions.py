#
# The extra exceptions that you'll encounter in Vagoth
#

class ActionException(RuntimeError):
    """An exception raised during execution of an action"""

class VMAlreadyAssignedException(RuntimeError):
    """VM is already assigned to a machine"""

class VMNotAssignedException(RuntimeError):
    """VM is not assigned to a hypervisor"""

class VMStillAssignedException(RuntimeError):
    """
    VM is currently assigned to a machine when it shouldn't
    be for this call.
    """

class NodeNotFoundException(RuntimeError):
    """Node not found in registry"""

class NodeStillUsedException(RuntimeError):
    """Node is still in use when trying to undefine it"""

class VMNotFoundException(RuntimeError):
    """VM not found in registry"""

class NodeAlreadyExistsException(RuntimeError):
    """Tried to create the same node twice"""

class VMAlreadyExistsException(RuntimeError):
    """Tried to create the same VM twice"""

class DriverException(RuntimeError):
    """Exception while calling the driver"""

class ProvisioningException(RuntimeError):
    """Could not provision the VM definition in the cluster"""
