Registry
========

Overview
--------

Vagoth's registry is used to store the state of all nodes in Vagoth.

The registry should not concern itself with logic, only with the consistency of
its own database.

All implementations should be read- and write-safe from multiple threads and
processes.

Rules
-----

A node stores the representation of a system, whether physical or virtual.

A node has a type, a system id, a name, a definition, a state, metadata, tags,
relationships in the form of one parent but many children, and a set of unique
keys.

A node can only have one parent, but many children.

Terminology
-----------

Node
    A node stores the representation of a logical system, no matter
    if it's a physical machine, a virtual machine, or an instance of
    some service.  In particular, a node is the configuration.

Node Type
    This is used to identify the type of the node.  You can return a list
    of all nodes with a named type.  This would probably be used to
    distinguish a hypervisor from a virtual machine, for example.  This
    is also used to lookup which class is instantiated for this node.

System ID
    The system ID is the behind-the-scenes name for this node.  It must
    be unique within the cluster, but (as a recommendation) be as unique
    as possible (eg. a UUID).  It doesn't have to be human readable.

Name
    The name must also be unique, but this can change over time.
    Looking up a node by name is (probably) a two-step process - first
    by name, then by system id.

Definition
    A definition is a dictionary describing a currently deployed instance.
    For virtualisation, it is used by the driver to create the virtual
    machine instance remotely.  For this reason, it shouldn't change for a
    deployed instance, as this could lead to inconsistencies in the
    cluster.

Metadata
    The Metadata dictionary stores dynamic information about the node,
    and can be used by any component in Vagoth to associate
    information with a node.  Each key in metadata should be namespaced,
    so as not to conflict with other keys in the component system. Vagoth
    uses VAGOTH\_ for its key prefix.

Tags
    Key/Value pairs can be associated with a node.  The purpose is to store
    end-user configurable information that doesn't directly affect the
    running node.

Parent
    This is either set to None, or to another Node.

Children
    When queried, this returns a list of Nodes whose parent is set to
    this node.  If stored as separate attributes, Parent & Children
    _must_ be kept in sync.

Unique Keys
    A cluster needs to be able to retain its integrity and consistency. In most
    cases, a set of unique keys is sufficient.  When creating a node, all of
    its unique keys _must_ be unique within the cluster.  Once a node is
    defined, then no other node can be defined with these unique keys.  A node
    may be looked up using any of its unique keys.  VAGOTH_NAME is reserved for
    the node name.
