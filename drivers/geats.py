
from ..utils.mc_json_rpc import mcollective_call

class GeatsMcollective(object):
    def __init__(self, local_config, global_config):
        self.config = local_config
        self.global_config = global_config
        #self.node_registry = global_config.get_registry()

    def _call(self, action, node=None, timeout=60, **kwargs):
        if node:
            node_name = node.get_name()
            return mcollective_call("geats", action, timeout=timeout, identity=node_name, **kwargs)
        else:
            return mcollective_call("geats", action, timeout=timeout, **kwargs)

    def _call_single(self, action, node, vm, timeout=60, **kwargs):
        if node is None:
            raise TypeError, "node argument is required"
        if vm is None:
            raise TypeError, "vm argument is required"
        node_name = node.get_name()
        vm_name = vm.get_name()
        responses = mcollective_call("geats", action, timeout=timeout, identity=node_name, vm_name=vm_name, **kwargs)
        # should only be one response
        for res in responses:
            return res["statuscode"], res["data"]
        return None, None

    def _call_single_exc(self, action, node, vm, timeout=60, **kwargs):
        status, data = self._call_single(action, node, vm, timeout, **kwargs)
        if status is None:
            raise DriverException("No response received from %s" % (node,))
        if status != 0:
            raise DriverException(node["statusmsg"])
        return data

    def _call_boolean(self, action, node, vm, timeout=60, **kwargs):
        status, data = self._call_single(action, node, vm, timeout, **kwargs)
        if status == 0:
            return True
        elif status is None:
            raise DriverException("No response received from %s" % (node,))
        else:
            raise DriverException(node["statusmsg"])

    def provision(self, node, vm):
        """Request a node to define & provision a VM"""
        return self._call_single_exc("provision", node, vm, definition=vm.get_definition())

    def define(self, node, vm):
        """Request node to define a VM"""
        return self._call_single_exc("define", node, vm, definition=vm.get_definition())

    def undefine(self, node, vm):
        """Request node to undefine a VM"""
        return self._call_boolean("undefine", node, vm)

    def deprovision(self, node, vm):
        """Request node to undefine & deprovision a VM"""
        return self._call_boolean("deprovision", node, vm)

    def start(self, node, vm):
        return self._call_boolean("start", node, vm, timeout=10)

    def reboot(self, node, vm):
        return self._call_boolean("reboot", node, vm, timeout=10)

    def stop(self, node, vm):
        return self._call_boolean("stop", node, vm, timeout=10)

    def shutdown(self, node, vm):
        return self._call_boolean("shutdown", node, vm, timeout=10)

    def info(self, node, vm):
        info = self._call_single_exc("info", node, vm, timeout=5)
        if info:
            info[u"node"] = unicode(node.get_name())
        return info

    def status(self, node=None):
        res = self._call("status", node)
        vms = []
        for node in res:
            if node["statuscode"] == 0:
                for vm in node["data"]["vms"].values():
                    vm[u"node"] = node["sender"]
                    vms.append(vm)
        return vms

    def migrate(self, node, vm, destination_node):
        return NotImplemented

    def metrics(self, node=None):
        return NotImplemented # FIXME
        polled_metrics = self._call("metrics", node)
        results = []
        for metric in polled_metrics:
            if node["statuscode"] == 0:
                res = node["data"]["metrics"]
                res["node"] = node["sender"]
            else:
                res = { "node": res["sender"] }
            results.append(res)
        if node:
            if len(results) > 0:
                return results[0]
            return {}

