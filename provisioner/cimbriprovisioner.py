import cimbri.manager
from .. import exceptions

class CimbriProvisioner(object):
    def __init__(self, manager, config, global_config):
        self.config = config
        self.global_config = global_config
        self.cimbri_manager = cimbri.manager.Manager()
    def _provision(self, vm_name, vm_definition):
        cimbri_cell = self.config.get('cell')
        cimbri_node = vm_definition.get("vm_name", None)
        if cimbri_cell and cimbri_node:
            cell = self.cimbri_manager.get_cell(cimbri_cell)
            node = cell.get_node(cimbri_node)
            vm_def = {
                "name": vm_name,
                "network": node.data["network"],
                "storage": node.data["storage"],
                "cpu": node.data["cpu"],
                "vm_type": node.data["vm_type"],
                "description": node.data["description"],
                "template": node.data.get('template', 'debian')
            }
            for network in vm_def["network"]:
                if "bridge" not in network:
                    network["bridge"] = "br0"
            return vm_def
        return None
    def provision(self, vm_name, vm_definition):
        try:
            vmdef = self._provision(vm_name, vm_definition)
            if vmdef:
                return vmdef
        except KeyError:
            raise exceptions.ProvisioningException("Could not locate VM {0}".format(vm_name))

    def deprovision(self, vm_name, vm_definition):
        pass
