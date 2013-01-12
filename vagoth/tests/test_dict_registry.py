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

"""
Test vagoth.registry.couch_registry.CouchRegistry
"""

import unittest
from ..registry.dict_registry import DictRegistry
import uuid
import couchdb
from .. import exceptions

NO_DEFAULT=uuid.uuid4()

class testDictRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = DictRegistry(None, {})
        self.registry.add_node("0xdeadbeef",
            node_type="hv",
            node_name="node001.example.com",
            definition={ "name": "0xdeadbeef", "fqdn": "node001.example.com" },
            tags=["tag1", "tag2"],
            unique_keys=["node001_uniquekey"])

    def test_contains(self):
        self.assertIn("0xdeadbeef", self.registry)

    def test_initial_object(self):
        self.assertEqual(len(self.registry.nodes), 1)
        self.assertTrue("0xdeadbeef" in self.registry.nodes)
        self.assertEqual(len(self.registry.unique), 2)
        self.assertIn("VAGOTH_NAME_node001.example.com", self.registry.unique)
        self.assertIn("node001_uniquekey", self.registry.unique)

    def test_change_name(self):
        self.registry.set_node("0xdeadbeef", node_name="foo.example.com")
        self.assertEqual(self.registry.nodes['0xdeadbeef']['name'], 'foo.example.com')
        self.assertIn("VAGOTH_NAME_foo.example.com", self.registry.unique)
        self.assertNotIn("VAGOTH_NAME_node001.example.com", self.registry.unique)

    def test_change_tags(self):
        self.registry.set_node("0xdeadbeef", tags=["vm"])
        self.assertIn("vm", self.registry.nodes['0xdeadbeef']['tags'])

    def test_change_keys(self):
        self.registry.set_node("0xdeadbeef", unique_keys=["MASTER"])
        self.assertIn("MASTER", self.registry.unique)
        self.assertNotIn("node001_uniquekey", self.registry.unique)
        node_keys = self.registry.nodes['0xdeadbeef']['unique_keys']
        self.assertEqual(node_keys, ["MASTER"])

    def test_get_node_by_name(self):
        node = self.registry.get_node_by_name("node001.example.com")
        self.assertEqual(node['node_id'], '0xdeadbeef')

    def test_get_node_by_key(self):
        node = self.registry.get_node_by_key("node001_uniquekey")
        self.assertEqual(node['node_id'], '0xdeadbeef')

    def test_get_nodes_with_tag(self):
        nodes = list(self.registry.get_nodes_with_tag("tag1"))
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0]['node_id'], '0xdeadbeef')

    def test_get_nodes_with_type(self):
        nodes = list(self.registry.get_nodes_with_type("hv"))
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0]['node_id'], '0xdeadbeef')

    def test_set_parent(self):
        self.registry.nodes['othernode'] = {}
        self.registry.set_parent('0xdeadbeef', 'othernode')
        self.assertEqual(self.registry.nodes['0xdeadbeef']['parent'], 'othernode')

    def test_get_nodes_with_parent(self):
        self.registry.nodes['othernode'] = {}
        self.registry.set_parent('0xdeadbeef', 'othernode')
        nodes = list(self.registry.get_nodes_with_parent("othernode"))
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0]['node_id'], '0xdeadbeef')

    def test_list_nodes(self):
        nodes = self.registry.list_nodes()
        self.assertEqual(nodes, ['0xdeadbeef'])

    def test_delete_node(self):
        self.registry.delete_node('0xdeadbeef')
        self.assertEqual(len(self.registry.nodes), 0)
        self.assertEqual(len(self.registry.unique), 0)

    def test_update_metadata(self):
        # add new keys
        self.registry.update_metadata("0xdeadbeef", {
            "one": "two"
        })
        self.assertEqual(self.registry.nodes['0xdeadbeef']['metadata']['one'], 'two')
        # ensure it doesn't overwrite existing keys
        self.registry.update_metadata("0xdeadbeef", {"three": "four"})
        self.assertEqual(self.registry.nodes['0xdeadbeef']['metadata']['one'], 'two')
        # ensure it deletes keys..
        self.registry.update_metadata("0xdeadbeef", {}, ["one"])
        self.assertNotIn("one", self.registry.nodes['0xdeadbeef']['metadata'])
        # ..but not all keys
        self.assertIn("three", self.registry.nodes['0xdeadbeef']['metadata'])
