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
from ..registry.couch_registry import CouchRegistry
import uuid
import couchdb
from .. import exceptions

rev_counter = 0

NO_DEFAULT=uuid.uuid4()

# an in-memory couchdb table mocker
class CouchTableMock:
    def __init__(self):
        self.data = {}
    def __setitem__(self, k, v):
        global rev_counter
        assert type(v) == dict
        if "_id" in v:
            if v["_id"] != k:
                raise couchdb.http.ResourceConflict("differing id in dict value")
        else:
            v["_id"] = k
        if k in self.data:
            if self.data[k]["_id"] != k:
                raise couchdb.http.ResourceConflict("differing id")
            if "_rev" in self.data[k] and v.get("_rev", None) != self.data[k]["_rev"]:
                raise couchdb.http.ResourceConflict("stale rev")
        if "_rev" not in v:
            v["_rev"] = rev_counter
            rev_counter += 1
        self.data[k] = v
    def __iter__(self):
        return iter(self.data)
    def __getitem__(self, k):
        return self.data[k]
    def __delitem__(self, k):
        del self.data[k]
    def get(self, k, default=NO_DEFAULT):
        if default == NO_DEFAULT:
            return self.data.get(k)
        else:
            return self.data.get(k, default)
    def __contains__(self, k):
        return k in self.data
    def save(self, doc):
        if "_id" in doc:
            self[doc["_id"]] = doc
    def delete(self, doc):
        if "_id" in doc and "_rev" in doc:
            _id, _rev = doc["_id"], doc["_rev"]
            if _id in self.data:
                if self.data[_id]["_rev"] == _rev:
                    del self.data[_id]
                else:
                    raise couchdb.http.ResourceConflict("stale rev")
            else:
                raise KeyError("not found in table")
        else:
            raise Exception("trying to delete a doc w/o _id and _rev: %r" % (doc,))

class CouchServer:
    def __init__(self, server):
        self.server = server
    def __getitem__(self, table_name):
        return CouchTableMock()

class test_CouchRegistry(unittest.TestCase):
    def setUp(self):
        self.tmp_Server = couchdb.Server
        couchdb.Server = CouchServer
        self.registry = CouchRegistry(None, {
            "couch_server": "http://example.com:5934",
            "couch_nodes_table": "vagoth/nodes",
            "couch_unique_table": "vagoth/nodes",
        })
        self.registry.add_node("0xdeadbeef",
            node_type="hv",
            node_name="node001.example.com",
            definition={ "name": "0xdeadbeef", "fqdn": "node001.example.com" },
            tags={"tag1":True, "tag2":"somevalue"},
            unique_keys=["node001_uniquekey"])

    def tearDown(self):
        # restore sanity to the world
        couchdb.Server = self.tmp_Server

    def test_contains(self):
        self.assertIn("0xdeadbeef", self.registry)

    def test_claim_unique_keys(self):
        self.registry._claim_unique_keys("0x1", ["NEW"])
        self.assertEqual(len(self.registry.unique.data), 3)
        self.assertIn("NEW", self.registry.unique.data)
        self.assertTrue(self.registry.unique.data["NEW"]["node_id"] == "0x1")
        self.registry._claim_unique_keys("0x1", ["NEWER"], ["NEW"])
        self.assertTrue(len(self.registry.unique.data) == 3)
        self.assertNotIn("NEW", self.registry.unique.data)
        self.assertIn("NEWER", self.registry.unique.data)
        self.assertEqual(self.registry.unique.data["NEWER"]["node_id"], "0x1")

    def test_claim_unique_keys_with_conflict(self):
        self.registry._claim_unique_keys("0x1", ["NEW"])
        self.assertRaises(exceptions.UniqueConstraintViolation,
            self.registry._claim_unique_keys, "0x2", ["NEW"])
        self.assertEqual(self.registry.unique.data["NEW"]["node_id"], "0x1")

    def test_initial_object(self):
        self.assertEqual(len(self.registry.nodes.data), 1)
        self.assertTrue("0xdeadbeef" in self.registry.nodes.data)
        self.assertEqual(len(self.registry.unique.data), 2)
        self.assertIn("VAGOTH_NAME_node001.example.com", self.registry.unique)
        self.assertIn("node001_uniquekey", self.registry.unique)

    def test_change_name(self):
        self.registry.set_node("0xdeadbeef", node_name="foo.example.com")
        self.assertEqual(self.registry.nodes['0xdeadbeef']['name'], 'foo.example.com')
        self.assertIn("VAGOTH_NAME_foo.example.com", self.registry.unique)
        self.assertNotIn("VAGOTH_NAME_node001.example.com", self.registry.unique)

    def test_change_tags(self):
        self.registry.set_node("0xdeadbeef", tags={"xyzzy":"xyzzy"})
        self.assertIn("xyzzy", self.registry.nodes['0xdeadbeef']['tags'])

    def test_change_keys(self):
        self.registry.set_node("0xdeadbeef", unique_keys=["MASTER"])
        self.assertIn("MASTER", self.registry.unique)
        self.assertNotIn("node001_uniquekey", self.registry.unique)
        node_keys = self.registry.nodes['0xdeadbeef']['unique_keys']
        self.assertEqual(node_keys, ["MASTER"])

    def test_get_node_by_name(self):
        node = self.registry.get_node_by_name("node001.example.com")
        self.assertEqual(node.id, '0xdeadbeef')

    def test_get_node_by_key(self):
        node = self.registry.get_node_by_key("node001_uniquekey")
        self.assertEqual(node.id, '0xdeadbeef')

    def test_get_nodes_with_tags_existence(self):
        nodes = list(self.registry.get_nodes_with_tags({"tag1": None}))
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].id, '0xdeadbeef')

    def test_get_nodes_with_tags_value(self):
        nodes = list(self.registry.get_nodes_with_tags({"tag2": "somevalue"}))
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].id, '0xdeadbeef')

    def test_get_nodes_with_type(self):
        nodes = list(self.registry.get_nodes_with_type("hv"))
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].id, '0xdeadbeef')

    def test_set_parent(self):
        self.registry.set_parent('0xdeadbeef', 'othernode')
        self.assertEqual(self.registry.nodes['0xdeadbeef']['parent'], 'othernode')

    def test_get_nodes_with_parent(self):
        self.registry.set_parent('0xdeadbeef', 'othernode')
        nodes = list(self.registry.get_nodes_with_parent("othernode"))
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].id, '0xdeadbeef')

    def test_list_nodes(self):
        nodes = self.registry.list_nodes()
        self.assertEqual(nodes, ['0xdeadbeef'])

    def test_delete_node(self):
        self.registry.delete_node('0xdeadbeef')
        self.assertEqual(len(self.registry.nodes.data), 0)
        self.assertEqual(len(self.registry.unique.data), 0)

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

    def test_blobs(self):
        mydict = {"mykey": "myvalue"}
        self.registry.set_blob("0xdeadbeef", "blob_one", "one")
        self.registry.set_blob("0xdeadbeef", "blob_two", 2)
        self.registry.set_blob("0xdeadbeef", "blob_dict", mydict)
        self.assertEqual(self.registry.get_blob("0xdeadbeef", "blob_one"), "one")
        self.assertEqual(self.registry.get_blob("0xdeadbeef", "blob_two"), 2)
        self.assertEqual(self.registry.get_blob("0xdeadbeef", "blob_dict"), mydict)
        self.assertEqual(self.registry.get_blob("0xdeadbeef", "blob_unset"), None)
