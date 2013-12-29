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
This scheduler is suitable for small installations and frontend tools where
making synchronous calls to the hypervisor driver is appropriate.

For example, a command line VM management tool.
"""

from .. import exceptions

class SyncJobScheduler(object):
    """
    A synchronous job "scheduler"
    """
    def __init__(self, manager, config):
        self.manager = manager
        self.config = config

    def action(self, queue_name, action, **kwargs):
        """
        This calls self.manager.action() to run the action
        in the current thread.
        """
        self.manager.action(action, **kwargs)

    def cleanup(self):
        pass
