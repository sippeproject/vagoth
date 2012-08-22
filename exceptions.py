#
# The extra exceptions that you'll encounter in Vagoth
#

class UniqueConstraintViolation(RuntimeError):
    """Some unique key is already taken in the cluster"""

class NodeNotFoundException(RuntimeError):
    """Node not found in registry"""

class UnknownNodeType(RuntimeError):
    """Cannot instantiate node because of an unknown node type"""

class NodeStillUsedException(RuntimeError):
    """Node is still in use when trying to undefine it"""

class NodeAlreadyHasParentException(RuntimeError):
    """VM is already assigned to a machine"""

class NodeAlreadyExistsException(RuntimeError):
    """Tried to create the same node twice"""

class ProvisioningException(RuntimeError):
    """Could not provision the VM definition in the cluster"""

# a generic class for action specific exceptions
class ActionException(RuntimeError):
    """An exception raised during execution of an action"""

class RegistryException(RuntimeError):
    """Error while writing to the Registry."""
