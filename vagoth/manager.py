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

from config import Config
import exceptions
import logging

class Manager(object):
    """
    The Manager class is the front door to the Vagoth API.
    Use manager.get_manager() and it will be cached and returned multiple times.

    You can pass in a different config object, otherwise it will instantiate
    vagoth.config_.Config
    """
    def __init__(self, config=None):
        config = self.config = config or Config()
        # self.registry
        registry_factory, registry_config = config.get_factory("registry")
        self.registry = registry_factory(self, registry_config)

        # self.scheduler
        sched_factory, sched_config = config.get_factory("scheduler")
        self.scheduler = sched_factory(self, sched_config)

        # self.provisioner
        provisioner_factory, provisioner_config = self.config.get_factory("provisioner")
        self.provisioner = provisioner_factory(self, provisioner_config)

    def _instantiate_node(self, nodedoc):
        if nodedoc:
            node_factory = self.config.get_node_factory(nodedoc.type)
            if node_factory:
                return node_factory(self, nodedoc)
            else:
                raise exceptions.UnknownNodeType("Unknown node type: %r" % (nodedoc.type))

    def get_node(self, node_id):
        """Return the node instance for this node_id"""
        nodedoc = self.registry.get_node(node_id) # can throw exception
        return self._instantiate_node(nodedoc)

    def get_nodes(self, tenant=False, node_type=False, tags=False, parent=False):
        """Return an iterable of all node instances"""
        for nodedoc in self.registry.get_nodes(tenant=tenant, node_type=node_type, tags=tags, parent=parent):
            yield self._instantiate_node(nodedoc)

    def get_node_by_name(self, node_name):
        """Return the node instance for the given node_name"""
        nodedoc = self.registry.get_node_by_name(node_name) # can throw exception
        return self._instantiate_node(nodedoc)

    def get_node_by_key(self, node_key):
        """Return the node instance which has the given unique key"""
        nodedoc = self.registry.get_node_by_key(node_key)
        return self._instantiate_node(nodedoc)

    def list_nodes(self):
        """Return an iterable of all the node_id in the registry"""
        return self.registry.list_nodes()

    def action(self, action, **kwargs):
        """Call the given action with the given arguments"""
        action_func = self.config.get_action(action)
        if action_func:
            try:
                action_func(self, **kwargs)
            except:
                logging.debug("Exception while executing action %s" % (action,), exc_info=True)
                raise

    def cleanup(self):
        """This must be called at shutdown time"""
        self.scheduler.cleanup()

manager = None
def get_manager(config=None):
    """
    Instantiate a new Manager instance and cache it,
    or return the cached instance.
    """
    global manager
    if manager is None:
        manager = Manager(config=config)
    return manager

