"""
This scheduler is suitable for small installations and frontend tools where
making synchronous calls to the hypervisor driver is appropriate.

For example, a command line VM management tool.
"""

from .. import exceptions

class SyncJobScheduler(object):
    """A synchronous job "scheduler" """
    def __init__(self, manager, config):
        self.manager = manager
        self.config = config

    def action(self, queue_name, action, **kwargs):
        """Simply calls self.manager.action(action, **kwargs)"""
        self.manager.action(action, **kwargs)

    def cleanup(self):
        pass
