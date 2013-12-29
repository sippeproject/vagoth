from .. import exceptions

import zope.interface
from zope.interface.verify import verifyObject
from zope.interface.exceptions import BrokenImplementation
from vagoth.interfaces.registry import IRegistry
from vagoth.interfaces.nodedoc import INodeDoc

class RegistryMixin(object):
    def mixin_setUp(self):
        # declare that we implement the IRegistry zope interface
        zope.interface.implementer(IRegistry)(self.registry.__class__)
        # add an initial test node
        self.registry.add_node("0xdeadbeef",
            node_type="hv",
            node_name="node001.example.com",
            tenant="mytenant",
            definition={ "name": "0xdeadbeef", "fqdn": "node001.example.com" },
            metadata={ "mymetakey": "mymetavalue" },
            tags={"tag1":True, "tag2":"somevalue"},
            unique_keys=["node001_uniquekey"])

    def test_initial_object(self):
        node = self.registry.get_node("0xdeadbeef")
        self.assertEqual("0xdeadbeef", node.id)
        self.assertEqual("node001.example.com", node.name)
        self.assertEqual("mytenant", node.tenant)
        self.assertEqual(["node001_uniquekey"], node.unique_keys)
        self.assertEqual(node.definition,
            { "name": "0xdeadbeef", "fqdn": "node001.example.com" })
        self.assertEqual(node.metadata,
            { "mymetakey": "mymetavalue" })

    def test_get_nodes(self):
        self.assertEqual(1, len(list(self.registry.get_nodes())))
        self.assertEqual(1,
            len(list(self.registry.get_nodes(tenant="mytenant"))))
        self.assertEqual(0,
            len(list(self.registry.get_nodes(tenant="nonexistant"))))
        self.assertEqual(1,
            len(list(self.registry.get_nodes(tags={"tag1":None}))))
        self.assertEqual(1,
            len(list(self.registry.get_nodes(tags={"tag2":"somevalue"}))))
        self.assertEqual(0,
            len(list(self.registry.get_nodes(tags={"tag2":"wrongvalue"}))))
        self.assertEqual(1,
            len(list(self.registry.get_nodes(parent=None))))
        self.assertEqual(1,
            len(list(self.registry.get_nodes(node_type="hv"))))
        self.assertEqual(1,
            len(list(self.registry.get_nodes(
                tenant="mytenant",
                parent=None,
                tags={"tag2":"somevalue"},
                node_type="hv"))))
        self.assertEqual(0,
            len(list(self.registry.get_nodes(
                tenant="wrongtenant",
                parent=None,
                tags={"tag2":"somevalue"},
                node_type="hv"))))

    def test_blobs(self):
        mydict = {"mykey": "myvalue"}
        self.registry.set_blob("0xdeadbeef", "blob_one", "one")
        self.registry.set_blob("0xdeadbeef", "blob_two", 2)
        self.registry.set_blob("0xdeadbeef", "blob_dict", mydict)
        self.assertEqual(self.registry.get_blob("0xdeadbeef", "blob_one"), "one")
        self.assertEqual(self.registry.get_blob("0xdeadbeef", "blob_two"), 2)
        self.assertEqual(self.registry.get_blob("0xdeadbeef", "blob_dict"), mydict)
        self.assertEqual(self.registry.get_blob("0xdeadbeef", "blob_unset"), None)

    def test_get_nodes_with_parent(self):
        self.registry.add_node("othernode", node_name="othernode", node_type="hv", tenant=None)
        self.registry.set_parent('0xdeadbeef', 'othernode')
        nodes = list(self.registry.get_nodes_with_parent("othernode"))
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].id, '0xdeadbeef')

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
        self.registry.add_node("othernode", node_name="othernode", node_type="hv", tenant=None)
        self.registry.set_parent('0xdeadbeef', 'othernode')
        self.assertEqual(self.registry.nodes['0xdeadbeef']['parent'], 'othernode')

    def test_list_nodes(self):
        nodes = self.registry.list_nodes()
        self.assertEqual(nodes, ['0xdeadbeef'])

    def test_change_tags(self):
        self.registry.set_node("0xdeadbeef", tags={"xyzzy":"xyzzy"})
        self.assertIn("xyzzy", self.registry.get_node('0xdeadbeef').tags)

    def test_update_metadata(self):
        # add new keys
        self.registry.update_metadata("0xdeadbeef", {
            "one": "two"
        })
        metadata = self.registry.get_node('0xdeadbeef').metadata
        self.assertEqual(metadata['one'], 'two')
        # ensure initial metadata is still present
        self.assertEqual(metadata['mymetakey'], 'mymetavalue')
        # ensure it doesn't overwrite existing keys
        self.registry.update_metadata("0xdeadbeef", {"three": "four"})
        metadata = self.registry.get_node('0xdeadbeef').metadata
        self.assertEqual(metadata['one'], 'two')
        # ensure it deletes keys..
        self.registry.update_metadata("0xdeadbeef", {}, ["one"])
        metadata = self.registry.get_node('0xdeadbeef').metadata
        self.assertNotIn("one", metadata)
        # ..but not all keys
        self.assertIn("three", metadata)

    def test_change_name(self):
        self.registry.set_node("0xdeadbeef", node_name="foo.example.com")
        node = self.registry.get_node("0xdeadbeef")
        self.assertEqual(node.name, "foo.example.com")
        self.assertEqual("0xdeadbeef",
            self.registry.get_node_by_key("VAGOTH_NAME_foo.example.com").id)
        self.assertRaises(exceptions.NodeNotFoundException,
            self.registry.get_node_by_key, "VAGOTH_NAME_node001.example.com")

    def test_change_keys(self):
        self.registry.set_node("0xdeadbeef", unique_keys=["MASTER"])
        node = self.registry.get_node_by_key("MASTER")
        self.assertIn("MASTER", node.unique_keys)
        self.assertEqual(node.id, "0xdeadbeef")
        self.assertRaises(exceptions.NodeNotFoundException,
            self.registry.get_node_by_key, "node001_uniquekey")

    def test_delete_node(self):
        self.registry.delete_node("0xdeadbeef")
        self.assertRaises(exceptions.NodeNotFoundException,
            self.registry.get_node, "0xdeadbeef")

    def test_contains(self):
        self.assertIn("0xdeadbeef", self.registry)

    def test_interface(self):
        verifyObject(IRegistry, self.registry)
