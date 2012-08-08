class Node(object):
    def __init__(self, name, manager, driver, *args, **kwargs):
        assert isinstance(name, basestring)
        self.name = name
        self.manager = manager
        self.registry = manager.node_registry
        self.driver = driver
        self.args = args
        self.kwargs = kwargs

    def get_name(self):
        return self.name

    def get_driver(self):
        return self.driver

    def get_definition(self):
        return self.registry.get_node_definition(self.name)

    def get_state(self):
        return self.registry.get_node_state(self.name)

    def status(self):
        return self.driver.status(self)

    def get_metrics():
        self.driver.get

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Node %s at %x>" % (self.name, id(self))
