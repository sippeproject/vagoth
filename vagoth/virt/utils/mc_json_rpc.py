#!/usr/bin/python
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

from subprocess import Popen, PIPE
from os.path import abspath, dirname, join
import json

class MCollectiveException(Exception): pass


def mcollective_call(agent, action, identity=None, timeout=None, **kwargs):
    mcdict = {
        "agent": agent,
        "action": action,
        "arguments": kwargs,
    }
    if identity is not None:
        mcdict["identity"] = identity
    if timeout is not None:
        mcdict["timeout"] = timeout
    mcjson = json.dumps(mcdict)
    ruby_script=join(abspath(dirname(__file__)), "mc_json_rpc.rb")
    process = Popen([ruby_script, "-"], stdin=PIPE, stdout=PIPE)
    process.stdin.write(mcjson)
    process.stdin.close()
    result = process.stdout.read()
    process.stdout.close()
    process.wait()
    if process.returncode == 0:
        return json.loads(result)
    else:
        raise MCollectiveException(
            "mc-json-rpc.rb exited with {0}: {1}".format(
                process.returncode, result))
