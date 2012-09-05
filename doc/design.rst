Design
======

At it's core, Vagoth has a a Manager object which is the starting point of the
python API.  With the help of vagoth.config, it loads all other components
dynamically.  The core components are:

* The Manager, your entry point to Vagoth.
* The Node Registry, storing node information, and their
  relationships.
* The Provisioner, to add new nodes into the system, and
  remove old ones.
* The Scheduler and Actions, to schedule a call to an action.

By itself, these components don't do much.  The initial purpose of Vagoth was
to be a cluster coordinator for virtual machines.  In other words, manage
multiple (tens or even hundreds of) physical servers hosting thousands of
virtual machines and containers.  The next layer around the core is therefore
the virtualisation layer, which consists of several components:

* VirtualMachine and Hypervisor classes
* A pluggable driver to communicate with different hypervisors
* A pluggable Allocator, to help decide on the best hypervisor/server for a VM.
* A pluggable Monitor, which will poll the state of the cluster and update
  the registry with the latest information about the cluster.

`vagoth.manager` uses `vagoth.config` to lookup modules and classes based on a
configuration file.  It uses a `registry` to store `node` records.  Nodes have
a `node_id`, a `name`, a `definition`, `metadata`, zero or more `tags`, and
zero or more unique `keys`.  Based on the node_type, the manager will
instantiate different classes when you call `manager.get_node(node_id)` and
related methods.

Node Attributes
---------------

definition
  A node's definition is generally where you'd store information that's used to
  deploy a node, which makes sense for VMs, but maybe not for other types of
  `node`.  For a VM, the definition shouldn't change while it's deployed.  In
  other scenarios, it's up to the developer to decide the purpose of the
  definition. It can be accessed with the `node.definition` property.

metadata
  Metadata is private to Vagoth, and is usually used to store information such
  as a VM or a hypervisor's `state`, system load, free RAM, etc.  Metadata can
  be accessed with the `node.metadata` property.

tags
  Multiple tags can be associated with a node, which can be be accessed with
  the `node.tags` property on a node instance, or used in a search with
  `manager.get_nodes_with_tag(tag)`.

keys
  Unique keys are a special concept in Vagoth.  One of the most important
  jobs for a cluster controller is to keep a healthy cluster, and one
  aspect is to ensure consistency.  You shouldn't have two systems using
  the same IP address or MAC address or storage device.  Unique keys simply
  map a string (such as "ip-1.2.3.4") to a node_id.  When a node is removed
  from the cluster, so are all its unique keys.  When a node is added, its
  unique keys are added, or an exception is thrown if they're not unique.
  Keys can be accessed with the `node.keys` property.

Core Components
---------------

Provisioner
  In order to add a VM to Vagoth, you have to the call
  `manager.provisioner.provision()` method, passing in at least a
  unique node_id, the node type, and a definition.  The provisioner
  will work its magic, and create a new node in the registry, or it
  will spit out an exception. The provisioner is the gatekeeper of
  what nodes are added to and removed from the cluster.

Scheduler and actions
  The scheduler can be called to run actions in the background.  It's a
  pluggable component, so you can swap in your preferred job scheduler
  here, or decide to use the SyncScheduler class if you don't mind
  waiting.  It has a concept of queues, where actions in a queue must
  be run in order.

  Actions are just functions that are called by the scheduler's worker.  They
  are given a pointer to the manager, and the keyword arguments that were passed
  to `manager.scheduler.action(queue_name, action_name, **kwargs)`

  Actions can also be called directly with `manager.action(name, **kwargs)`

Node Registry
  The node registry is the interface to the database that stores all the
  information about nodes in the cluster.  It's really its job to ensure that
  unique keys such as the node_id, node_name, and extra unique keys stay unique
  in the cluster.  Any good implementation will ensure that the database is
  redundant, or at least backed up regularly (if downtime is permissible).  You
  may also have a design where a lost DB can be re-created by the Monitor when
  it polls reality.

Configuration
  The configuration file is in <code>.ini</code> format, but is wrapped by the
  `vagoth.config.Config` class.  An instance of this class can be
  passed to `vagoth.get_manager(config=None)`.  It comes with a few
  helper methods to instantiate or return classes or methods dynamically
  based on configuration.  You're free to replace this component also.


Virtualisation-Specific Components
----------------------------------

Node class: Hypervisor
  The Hypervisor class has a helper method to list the children of the class, and
  it also has a driver property and a state property.

Node class: VirtualMachine
  VM instances have a few helper methods, but they simply make calls to the
  `job scheduler`.  The scheduler will ensure that requested actions are
  executed.  It will typically be asynchronous, but Vagoth includes a
  synchronous scheduler implementation also.  `VirtualMachine` also has
  a `.parent` property, and a `.state` property.

Driver
  A `driver` is the interface to control a real hypervisor node.  It's
  the real workhorse behind managing remote VMs, and is only separate to
  the Hypervisor class so that the Hypervisor class can keep a simple and
  generic interface itself.  It has methods to `define` a VM, as well
  as `start`, `stop`, `shutdown`, `reboot`, `migrate`, and `undefine` too.
  It also has the methods `provision` and `deprovision` which can be
  called explicitly when a VM should be installed afresh, or wiped before
  decommissioning.

Allocator
  When a VM is requested to `start` and it isn't yet assigned to a node,
  it will ask the `allocator` component to find a suitable node.  The
  allocator can take a single 'hint' argument, but it should search
  through the definitions, metadata, and its knowledge of VM assignments
  to select the best node for the VM.

Monitor
  In the background, Vagoth has a `Monitor`, which will regularly poll
  all the nodes for VM and node `status`.  This information can then be
  used by other components (such as the allocator, or web or command line
  tools).

Virtualisation Actions
----------------------

The module `virt.actions` defines a set of default actions for controlling
virtual machines.  These actions work together with the monitor and the
hypervisor driver to manage the lifecycle of VMs in the cluster.  It's expected
that actions will, as necessary, dive into any bit of code in Vagoth, as they
are written for a specific set of components in Vagoth.

Python API: An Example
----------------------

The component design of Vagoth is intended to encourage a clean API so that
other tools can be easily written to use it::

   >>> import vagoth
   >>> manager = vagoth.get_manager()
   >>> manager.list_nodes()
   [u'pm01', u'dummy', u'neuro', u'centos', u'foobox', u'dummy2', u'debian',u'nator',u'delta']
   >>> list(manager.get_nodes_with_type('hv'))
   [<Node delta at 0x7f994ee88110>, <Node nator at 0x7e49ab241770>]
   >>> vm = manager.get_node("centos")
   >>> vm.definition
   {u'vm_type': u'lxc', u'template': u'centos-6-x86_64-devel', u'network': {u'hwaddr': u'02:bc:8a:e9:f1:05', u'netmask': u'255.255.255.0', u'ipaddr': u'192.168.1.41', u'gateway': u'192.168.1.1', u'name': u'eth0'}, u'name': u'centos', u'description': u'CentOS 6.2 Dev'}
   >>> vm.state
   u'stopped'
   >>> vm.metadata
   {'state': u'stopped'}
   >>> vm.parent
   <Node delta at 0x7f994ee88110>
   >>> vm.parent.driver
   <vagoth.virt.drivers.geats.GeatsMcollective object at 0x7f994ee882d0>
   >>> vm.start()
   >>> vm.state
   u'starting'

When the monitor runs in the background and updates state, `vm.state` should
then appear as `running`.  The "stopped" and "running" states come from Geats's
LXC driver.
