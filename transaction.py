"""
Wrap any code block in a transaction in order to get
a transaction id in the logs.

Example:

>>> with Transaction(username):
...    manager.action("start", vm_name="my_vm")

Nested transaction's will retain the first transaction ID, instead of generating a
new one.
"""

import threading
import uuid

threadlocal = threading.local()
threadlocal.vagoth_txid = None
threadlocal.source = None

def get_txid():
    """
    Return the current transaction ID, or "0"
    """
    global threadlocal
    try:
        return threadlocal.vagoth_txid or "0"
    except AttributeError:
        return "0"

def get_source():
    """
    Return the current transaction source, or "0"
    """
    global threadlocal
    try:
        return threadlocal.source or "0"
    except AttributeError:
        return "0"

class Transaction(object):
    """
    Transaction(source=None, txid=None)

    source might be a username, or the name of the process.

    If a transaction is already set for the current thread, it
    will be used instead of the passed-in txid.

    If txid is not specified, a random one will be generated.
    """
    def __init__(self, source=None, txid=None):
        self.source = source
        self.desired_txid = txid
        
    def __enter__(self):
        global threadlocal
        self.txid = None
        if threadlocal.vagoth_txid == None:
            self.txid = self.desired_txid or uuid.uuid4().hex[:8]
            threadlocal.vagoth_txid = self.txid
            threadlocal.source = self.source

    def __exit__(self, *args, **kwargs):
        global threadlocal
        if self.txid != None:
            threadlocal.vagoth_txid = None
            threadlocal.source = None
