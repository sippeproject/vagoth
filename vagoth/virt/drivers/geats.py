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

from ..utils.mc_json_rpc import mcollective_call
from ..exceptions import DriverException

class GeatsMcollective(object):
    """
    Driver to talk to Geats using mcollective.  It uses the
    mcollective_call() function from utils.mc_json_rpc to
    launch ruby to make the call.
    """
    def __init__(self, manager, local_config):
        self.config = local_config

    def _call(self, action, node=None, timeout=60, **kwargs):
        if node:
            node_name = node.node_id
            return mcollective_call("geats", action, timeout=timeout, identity=node_name, **kwargs)
        else:
            return mcollective_call("geats", action, timeout=timeout, **kwargs)

    def _call_single(self, action, node, vm, timeout=60, **kwargs):
        if node is None:
            raise TypeError, "node argument is required"
        if vm is None:
            raise TypeError, "vm argument is required"
        node_name = node.node_id
        vm_name = vm.node_id
        responses = mcollective_call("geats", action, timeout=timeout, identity=node_name, vm_name=vm_name, **kwargs)
        # should only be one response
        for res in responses:
            return res["statuscode"], res["statusmsg"], res["data"]
        return None, None, None

    def _call_single_exc(self, action, node, vm, timeout=60, **kwargs):
        status, statusmsg, data = self._call_single(action, node, vm, timeout, **kwargs)
        if status is None:
            raise DriverException("No response received from %s" % (node,))
        if status != 0:
            raise DriverException(statusmsg) # FIXME
        return data

    def _call_boolean(self, action, node, vm, timeout=60, **kwargs):
        status, statusmsg, data = self._call_single(action, node, vm, timeout, **kwargs)
        if data:
            return True
        if status == 0:
            return True
        elif status is None:
            raise DriverException("No response received from %s" % (node,))
        else:
            raise DriverException(str(statusmsg))

    def provision(self, node, vm):
        """Request a node to define & provision a VM"""
        return self._call_single_exc("provision", node, vm, definition=vm.definition)

    def define(self, node, vm):
        """Request node to define a VM"""
        return self._call_single_exc("define", node, vm, definition=vm.definition)

    def undefine(self, node, vm):
        """Request node to undefine a VM"""
        return self._call_boolean("undefine", node, vm)

    def deprovision(self, node, vm):
        """Request node to undefine & deprovision a VM"""
        return self._call_boolean("deprovision", node, vm)

    def start(self, node, vm):
        """Request node to start the VM"""
        return self._call_boolean("start", node, vm, timeout=10)

    def reboot(self, node, vm):
        """Request node to reboot the VM"""
        return self._call_boolean("reboot", node, vm, timeout=10)

    def stop(self, node, vm):
        """Request node to stop (forcefully) the VM"""
        return self._call_boolean("stop", node, vm, timeout=10)

    def shutdown(self, node, vm):
        """Request node to shutdown (nicely) the VM"""
        return self._call_boolean("shutdown", node, vm, timeout=10)

    def info(self, node, vm):
        """Request information about the given VM from the node"""
        info = self._call_single_exc("info", node, vm, timeout=5)
        if info:
            info[u"node"] = unicode(node.node_id)
        return info

    def status(self, node=None):
        """Request information about all VMs from the node"""
        res = self._call("status", node, timeout=5)
        if len(res) == 0:
            raise DriverException("No results received for %s" % (node))
        nodes = []
        for node in res:
            if node["statuscode"] == 0:
                for vm in node["data"]["vms"].values():
                    vm[u"_parent"] = node["sender"]
                    vm[u"_name"] = vm["definition"]["name"]
                    vm[u"_type"] = "vm"
                    nodes.append(vm)
                # add hypervisor server
                hv = node["data"].get("status", {})
                hv[u"_parent"] = None
                hv[u"_name"] = node["sender"]
                hv[u"_type"] = "hv"
                nodes.append(hv)
        return nodes

    def migrate(self, node, vm, destination_node):
        """Request the node to migrate the given VM to the destination node"""
        return NotImplemented
