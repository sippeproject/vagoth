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

import zope.interface as ZI

class IScheduler(ZI.Interface):
    """
    Scheduler's are called to schedule the background execution of actions.
    Vagoth's default schedulers are quite basic, but you can implement your
    own so long as it matches the IScheduler interface.
    """
    def __init__(manager, config):
        """
        Instantiated with an instance of Manager and a configuration dict
        """

    def action(self, queue_name, action, **kwargs):
        """
        Schedule the given action with kwargs.

        Actions in the same queue_name should be executed in sequence.
        """

    def cleanup(self):
        """
        Called by Manager.cleanup() at shutdown time.
        It could be used to close DB connections, cleanup threads or
        child processes, etc.
        """
