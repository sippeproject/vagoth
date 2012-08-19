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

    def __getitem__(self, key):
        return self.config[key]

    def _lookup_config_section(self, config_path):
        current = self.config
        try:
            for part in config_path.split("/"):
                current = current[part]
            return current
        except KeyError:
            raise KeyError("Could not locate %s in config file" % (config_path,))

    def get_factory(self, section, factory_key="factory"):
        """return a factory and its configuration dict"""
        config = self._lookup_config_section(section)
        factory_str = config[factory_key]
        return dynamic_lookup(factory_str), config

    def make_factory(self, section, context, factory_key="factory"):
        factory_class, factory_config = self.get_factory(section, factory_key)
        return factory_class(context, factory_config)

    def get_node_factory(self, node_type):
        """Return the class for a given node type"""
        node_types = self.config["node_types"]
        if node_type in node_types:
            return dynamic_lookup(node_types[node_type])

    def get_action(self, action):
        actions = self.config["actions"]
        if action in actions:
            return dynamic_lookup(actions[action])
