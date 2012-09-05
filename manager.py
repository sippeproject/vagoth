# *-* vim: ft=python softtabstop=4 expandtab

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
            node_factory = self.config.get_node_factory(nodedoc['type'])
            if node_factory:
                return node_factory(self, nodedoc['node_id'], nodedoc)
            else:
                raise exceptions.UnknownNodeType("Unknown node type: %r" % (nodedoc['type']))

    def get_node(self, node_id):
        """Return the node instance for this node_id"""
        nodedoc = self.registry.get_node(node_id) # can throw exception
        return self._instantiate_node(nodedoc)

    def get_nodes(self):
        """Return an iterable of all node instances"""
        for nodedoc in self.registry.get_nodes():
            yield self._instantiate_node(nodedoc)

    def get_node_by_name(self, node_name):
        """Return the node instance for the given node_name"""
        nodedoc = self.registry.get_node_by_name(node_name) # can throw exception
        return self._instantiate_node(nodedoc)

    def get_node_by_key(self, node_key):
        """Return the node instance which has the given unique key"""
        nodedoc = self.registry.get_node_by_key(node_key)
        return self._instantiate_node(nodedoc)

    def get_nodes_with_type(self, node_type):
        """Return an iterable of all node instances with the given type"""
        for nodedoc in self.registry.get_nodes_with_type(node_type):
            yield self._instantiate_node(nodedoc)

    def get_nodes_with_tag(self, node_tag):
        """Return an iterable of all nodes with the given tag"""
        for nodedoc in self.registry.get_nodes_with_tag(node_tag):
            yield self._instantiate_node(nodedoc)

    def get_nodes_with_parent(self, node_parent):
        """Return an iterable of all nodes with the given parent node"""
        for nodedoc in self.registry.get_nodes_with_parent(node_parent):
            yield self._instantiate_node(nodedoc)

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

