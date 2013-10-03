#!/usr/bin/ruby
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

#
# mc-json-rpc takes a JSON dictionary on either standard
# input or in a filename and treats it as an mcollective
# RPC request. The responses are printed on standard
# output in JSON format.
#
# The input dictionary must have, at a minimum,
# agent & action defined. Optional arguments are
# identity, timeout, and arguments.
# arguments, if provided, must be a dictionary of
# key-value pairs to be passed in as arguments.
#

require 'mcollective'
require 'json'

include MCollective::RPC

if ARGV.count == 0
  $stderr.puts("Syntax: #{$0} [-|filename.json]")
  exit 1
end
if ARGV[0] == "-"
    hash = JSON.load($stdin.read())
else
    open(ARGV[0]) do |fd|
        hash = JSON.load(fd.read())
    end
end

if hash.class != Hash
  exit 2
end

agent = hash['agent']
action = hash['action']
arguments = hash['arguments'] || {}
identity = hash['identity']
timeout = hash['timeout'] || 60

newargs = {}
arguments.each do |k,v|
  if k[0..4] == "_SYM_" # a hack to support symbols
    newargs[k[5..-1].to_sym] = v
  else
    newargs[k] = v
  end
end

if agent and action
    mc = rpcclient(agent)
    mc.progress = false
    mc.timeout = timeout
    if identity != nil
      mc.identity_filter identity
    else
      mc.discover
    end
    result = mc.send(action, newargs).map{|r| r.results}
    puts JSON.dump(result)
    exit 0
end

exit 3
