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
