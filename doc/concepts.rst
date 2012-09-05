Concepts
========

Vagoth is just one component in a larger system for systems management,
virtualisation, and service management.

I wrote Vagoth in part because I wanted to test my ideas on the correct layers
and abstractions of a "cloud".  Existing solutions (both commercial and open
source) seem to lock you in to their way of doing things, and all have a high
barrier to entry if you want to change anything.  Vagoth, along with its sister
projects, are the proof of concept for my ideas, implemented as a component
framework in the Python language so that it's easy for myself and others to
hack on it. My primary tenets were for clean abstractions, clean code, and a
clean and obvious end-user API.

The Model::

   Local VM/Resource Manager
     (eg. geats, libvirt)
             |
     Cluster Controller
          (Vagoth)
             |
        Cloud Manager
          (Vagoth?)
             |
       Service Manager
           (???)

These are the layers that I think are important in a cluster solution.  You
may have other components involved (such as a storage provisioning system, and
integration with DHCP, TFTP, and DNS), but the core components are the above,
and they each have their domain of specialty, and rely on the level below
it.

A `Local VM/Resource Manager` is responsible for running the VMs or
services on a single system.  It doesn't need to concern itself with other
systems or resources, only with itself and the those it manages.  The local
manager should be given all the information (in Vagoth terminology, a
definition) it needs to bring up a resource, and it's OK to remove a resource
and add it again if the definition needs to change. It should have the means to
do full lifecycle management of the resource, including the decomissioning of
VMs (eg.  wiping storage, at least)

A `Cluster Controller` is responsible for maintaining a cluster of
these local managers, and ensuring that they don't step on each others toes by
trying to use the same resources (eg. IPs, MACs, shared storage volumes).

A `Cloud Manager` should be logically separate to the cluster
controller, and the cloud manager tracks relationships between users, projects
and VM instances running in various clusters.  For IaaS, you would typically
have the REST API and web interface at this layer.

A `Service Manager` manages services as a whole, and associates them
with instances running in one or more clouds.  A PaaS (of the upload code &
go variety) would sit at this layer.

Each of these layers need to talk to the layer above, and there will
necessarily be some glue to do that. I refer to this glue code as a `driver`,
and it will typically be pluggable, so as to easily communicate with different
systems.


