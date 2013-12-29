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
# A wrapper for a Node Document/Dict
#

import zope.interface as ZI

class INodeDoc(ZI.Interface):
    """
    INodeDoc represents a node as returned from an IRegistry.
    """
    type = ZI.Attribute("node type as string")
    id = ZI.Attribute("node id as string")
    name = ZI.Attribute("node name as string")
    tenant = ZI.Attribute("node tenant as string")
    definition = ZI.Attribute("node definition as dict")
    metadata = ZI.Attribute("node metadata as dict")
    parent = ZI.Attribute("node parent")
    tags = ZI.Attribute("node tags as dict")

    def get_blob(key):
        """Return the node blob for the given key (or None)"""
