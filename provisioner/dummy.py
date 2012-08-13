class DummyProvisioner(object):
    def __init__(self, manager, config, global_config):
        pass
    def provision(self, vm_name, vm_definition):
        return vm_definition
    def deprovision(self, vm_name, vm_definition):
        pass
