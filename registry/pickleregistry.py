#
# Registry of VMs and Hypervisors
#

import pickle
import os.path
from .. import exceptions
from threading import RLock
from dictregistry import DictRegistry

class PickleRegistry(DictRegistry):
    """
    A simple thread-safe (but not process-safe) registry.

    self.vms is set to the VM dictionary.
    self.nodes is set to the nodes dictionary.

    Example VM dict:
    self.vms = { "vm_name": {
      "definition": { ... vm definition ... },
      "metadata": { ... vm metadata ... },
      "state": "defined"|"autostart"|"stopped"|"migrating",
      "parent": "node001"
    } }

    Example node dict:
    self.nodes = { "node001": {
        "definition": { ... node definition ... },
        "metadata": { ... node metadata ... },
        "state": { "up"|"down"|"locked" },
        "children": [ "node001", ],
    } }
    """
    def _load(self):
        filename = self.config.get('filename', None)
        if filename and os.path.exists(filename):
            with open(filename,'r') as fd:
                self.data = pickle.load(fd)
        else:
            self.data = {"vms":{},"nodes":{}}
        self.vms = self.data["vms"]
        self.nodes = self.data["nodes"]

    def _save(self):
        filename = self.config.get('filename', None)
        with open(filename, 'w') as fd:
            pickle.dump(self.data, fd)
