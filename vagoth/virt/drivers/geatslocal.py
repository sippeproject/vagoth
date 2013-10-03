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

from ..exceptions import DriverException
import subprocess
import json
import os

def local_call(action, **kwargs):
    p = subprocess.Popen(["geats_jsonagent"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    request = json.dumps({"action": action, "data": kwargs})
    p.stdin.write(request)
    p.stdin.close()
    result = p.stdout.read()
    exit_code = p.wait()
    if exit_code == 0:
        jresult = json.loads(result)
        assert type(jresult) == dict
        if jresult.get("success", False):
            return jresult.get("data", None)
        else:
            errorcode = jresult.get("errorcode", "undefined")
            message = jresult.get("message", "check logs")
            exceptionmsg = "%s: %s" % (errorcode, message)
            raise DriverException(exceptionmsg)
    else:
        raise DriverException("geats_jsonagent exited with %d" % (exit_code,))




class GeatsLocal(object):
    """
    Driver to talk to a local Geats install.
    """
    def __init__(self, manager, local_config):
        self.config = local_config

    def _call(self, action, node=None, timeout=60, **kwargs):
        return local_call(action, **kwargs)

    def _call_single(self, action, node, vm, timeout=60, **kwargs):
        vm_name = vm.node_id
        return local_call(action, vm_name=vm.node_id, **kwargs)
    _call_single_exc = _call_single

    def _call_boolean(self, action, node, vm, timeout=60, **kwargs):
        result = self._call_single(action, node, vm, timeout, **kwargs)
        return True

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
        node_name = os.uname()[1]
        if node is None:
            pass # just us, then
        elif node.node_id != node_name:
            # we only return information about the current node..
            raise DriverException("Cannot contact remote node '%s' using GeatsLocal driver" % (node.node_id,))
        for vm in res["vms"].values():
                vm[u"_parent"] = node_name
                vm[u"_name"] = vm["definition"]["name"]
                vm[u"_type"] = "vm"
                nodes.append(vm)
        # add hypervisor server
        hv = res.get("status", {})
        hv[u"_parent"] = None
        hv[u"_name"] = node_name
        hv[u"_type"] = "hv"
        nodes.append(hv)
        return nodes

    def migrate(self, node, vm, destination_node):
        """Request the node to migrate the given VM to the destination node"""
        return NotImplemented
