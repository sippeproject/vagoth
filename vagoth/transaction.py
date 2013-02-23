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
