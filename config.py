"""
sippe.cimbri.Conf - plugin manager
"""

def get_config(config_searchpaths):
    from configobj import ConfigObj
    import os.path

    for path in config_searchpaths:
        path = os.path.expanduser(path)
        if os.path.exists(path):
            return ConfigObj(path)
    return ConfigObj()

def dynamic_lookup(moduleColonName):
    modulestr, name = moduleColonName.split(":")
    try:
        module = __import__(modulestr, fromlist=[name])
    except ImportError:
        raise ImportError("Could not import module: %s" % (modulestr,))
    try:
        return getattr(module, name)
    except AttributeError:
        raise AttributeError("Could not load %s from module %s" % (name, modulestr))

_static_config = None

class Config(object):
    def __init__(self, config_searchpaths=None):
        global _static_config
        if _static_config != None:
            self.config = _static_config
        else:
            searchpath = config_searchpaths or ["~/.config/sippe/vagoth.conf", "/etc/sippe/vagoth.conf"]
            _static_config = self.config = get_config(searchpath)
        self.node_registry = None
        self.registry = None
        self.allocator = None
        self.driver = None
        self.scheduler = None

    def _get_factory(self, section, factory_key="factory"):
        """return a factory and its configuration dict"""
        if section in self.config:
            if factory_key in self.config[section]:
                factory_str = self.config[section][factory_key]
                return dynamic_lookup(factory_str), self.config[section]
        return None, None

    def get_registry(self):
        """Return the registry singleton"""
        if self.registry is not None:
            return self.registry
        factory, config = self._get_factory("registry", "factory")
        if factory:
            self.registry = factory(config, self)
            return self.registry

    def get_allocator(self):
        """Return the allocator singleton"""
        if self.allocator is not None:
            return self.allocator
        factory, allocator_config = self._get_factory("allocator", "factory")
        if factory:
            self.allocator = factory(allocator_config, self)
            return self.allocator

    def get_driver(self):
        """Return the hypervisor driver singleton"""
        if self.driver is not None:
            return self.driver
        factory, driver_config = self._get_factory("driver", "factory")
        if factory:
            self.driver = factory(driver_config, self)
            return self.driver

    def get_name(self):
        """return the name, if set, for this vagoth controller"""
        return self.config.get('name', "name_unset")

    def get_description(self):
        """return a description, if set, for this vagoth controller"""
        return self.config.get('description', "description_unset")

    def get_provisioner_factory(self):
        """Cluster provisioner/deprovisioner for VMs"""
        factory, config = self._get_factory("provisioner", "factory")
        return factory, config

    def get_vm_factory(self):
        """Return the VM factory - used by vm_registry"""
        factory, vm_config = self._get_factory("vm", "factory")
        return factory, vm_config

    def get_node_factory(self):
        """Return the node factory - used by node_registry"""
        factory, node_config = self._get_factory("node", "factory")
        return factory, node_config

    def get_scheduler_factory(self):
        """Job Scheduler - called to do asynchronous jobs"""
        factory, config = self._get_factory("scheduler", "factory")
        return factory, config

    def get_monitor_factory(self):
        factory, config = self._get_factory("monitor", "factory")
        return factory, config

    def get_action(self, action):
        actions = self.config["actions"]
        if action in actions:
            return dynamic_lookup(actions[action])

    def get_logger(self):
        """Implements ILogger interface"""
        factory, config = self._get_factory("logger", "factory")
        return factory(config, self)
