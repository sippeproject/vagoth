class DummyProvisioner(object):
    def __init__(self, config, global_config):
        self.config = config
        self.global_config = global_config
    def provision(self, vm_name, vm_definition):
        return vm_definition
    def deprovision(self, vm_name, vm_definition):
        pass
