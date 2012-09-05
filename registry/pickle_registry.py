#
# Registry of nodes
#

import pickle
import os.path
from dict_registry import DictRegistry
import fcntl

class LockFile(object):
    """
    A simple lock file that can be used in a "with x" statement.
    """
    def __init__(self, lockfile):
        self.lockfile = lockfile
        self.locked = False
        self.loaded = False
    def __enter__(self):
        self.fd = open(self.lockfile, 'w')
        fcntl.lockf(self.fd, fcntl.LOCK_EX)
        self.locked = True
    def __exit__(self, *args):
        self.locked = False
        self.loaded = False
        fcntl.lockf(self.fd, fcntl.LOCK_UN)
        self.fd.close()

class PickleRegistry(DictRegistry):
    """
    A simple registry based on DictRegistry but saving the contents
    to a python pickle.  It uses a lockfile to ensure process-safety.

    Config variable `lockfile` will set the location of the lockfile.
    Config variable `filename` will set the location of the pickle file.
    """

    def __init__(self, manager, config):
        lock = LockFile(config.get("lockfile", "/var/lock/vagoth.pickledb.lock"))
        DictRegistry.__init__(self, manager, config, lock=lock)
        # replace lock with our own file-based lock

    def _load(self):
        if self.lock.locked and self.lock.loaded:
            return # locked and loaded, Sir!
        self.lock.loaded = True
        filename = self.config.get('filename', None)
        if filename and os.path.exists(filename):
            with open(filename,'rw') as fd:
                self.data = pickle.load(fd)
        else:
            self.data = {"vms":{},"nodes":{}}
        self.vms = self.data["vms"]
        self.nodes = self.data["nodes"]

    def _save(self):
        filename = self.config.get('filename', None)
        with open(filename+".new", 'w') as fd:
            pickle.dump(self.data, fd)
        os.rename(filename+".new", filename)
