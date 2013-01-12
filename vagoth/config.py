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

def get_config(config_searchpaths):
    """
    Given a list of config searchpaths, instantiate the config object for
    the first path, or instantiate an empty config object.  This uses
    the configobj library to load the config.
    """
    from configobj import ConfigObj
    import os.path

    for path in config_searchpaths:
        path = os.path.expanduser(path)
        if os.path.exists(path):
            return ConfigObj(path)
    return ConfigObj()

def dynamic_lookup(moduleColonName):
    """
    Dynamically lookup an object in a module, given input of the form
    modulename:objectname
    """
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
    """
    Config is a wrapper class around the real config object,
    supplying methods to return or instantate class factories
    found in the configuration.
    """
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
        """Return a tuple for a factory and its configuration dict"""
        config = self._lookup_config_section(section)
        factory_str = config[factory_key]
        return dynamic_lookup(factory_str), config

    def make_factory(self, section, context, factory_key="factory"):
        """
        Instantate a factory, passing in a context object and the section
        config to the initialiser.
        """
        factory_class, factory_config = self.get_factory(section, factory_key)
        return factory_class(context, factory_config)

    def get_node_factory(self, node_type):
        """
        Return the class for a given node type
        """
        node_types = self.config["node_types"]
        if node_type in node_types:
            return dynamic_lookup(node_types[node_type])

    def get_action(self, action):
        """
        Return the named action callable
        """
        actions = self.config["actions"]
        if action in actions:
            return dynamic_lookup(actions[action])
