from threading import Thread
from Queue import Queue

class Worker(object):
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
        self.queue.put( (None, None) )

    def action(self, action, **kwargs):
        self.queue.put( (action, kwargs) )

class ThreadScheduler(object):
    def __init__(self, manager, config):
        self.manager = manager
        self.config = config
        self.worker = Worker(manager)
        self.thread = Thread(target=self.worker.run)
        self.thread.start()

    def action(self, queue_name, action, **kwargs):
        self.worker.action(action, **kwargs)

    def cleanup(self):
        self.worker.stop()
