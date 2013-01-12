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
    """Node is already assigned another parent"""

class NodeAlreadyExistsException(RuntimeError):
    """Tried to create the same node twice"""

class ProvisioningException(RuntimeError):
    """Could not provision the node in the cluster"""

# a generic class for action specific exceptions
class ActionException(RuntimeError):
    """An exception raised during execution of an action"""

class RegistryException(RuntimeError):
    """Error while writing to the Registry."""
