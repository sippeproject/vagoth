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

from threading import Thread
from Queue import Queue

class Worker(object):
    """
    Worker class for `ThreadScheduler`
    """
    def __init__(self, manager):
        self.manager = manager
        self.queue = Queue()

    def run(self):
        while True:
            action, kwargs = self.queue.get()
            if action is None:
                break
            try:
                self.manager.action(action, **kwargs)
            except Exception as e:
                print e # FIXME

    def stop(self):
        """Signal to the thread that it should quit"""
        self.queue.put( (None, None) )

    def action(self, action, **kwargs):
        """Add an action to the queue"""
        self.queue.put( (action, kwargs) )

class ThreadScheduler(object):
    """
    Runs a single worker in a Thread to process
    all actions in the background.
    """
    def __init__(self, manager, config):
        self.manager = manager
        self.config = config
        self.worker = Worker(manager)
        self.thread = Thread(target=self.worker.run)
        self.thread.start()

    def action(self, queue_name, action, **kwargs):
        """Schedule the specified action, ignoring queue_name"""
        self.worker.action(action, **kwargs)

    def cleanup(self):
        """Request the worker thread to exit"""
        self.worker.stop()
