History
-------

Like most software projects, Vagoth came about because of an itch that begged
to be scratched.

A couple of years ago, for my company, I programmed a simple wrapper for
libvirt which would take a simple dictionary as input, create the libvirt XML,
and had pluggable storage since libvirt storage plugins nor its hooks fit
our needs. This is a similar approach to how oVirt's VDSM works.  This would
run on a single server and manage the VMs running on it, and it has no idea
about the other servers or VMs in the cluster.

At the same time, I had a file-based version-controlled database which kept
track of what IPs and MACs were allocated to nodes, which was used to generate
DHCP, DNS records, and TFTP PXE configuration files.  It seemed logical to
store a little more information in the same place -- enough to define VM
characterics (RAM, CPU, storage, & network devices).  Most organisations have
something similar - often an SQL or LDAP database with an entry for each
machine, and a collection of attributes.

I wanted a centralised way to bring up VMs and to make use of this "database"
of VM definitions.  I invested a little time and created an mcollective agent
which wrapped the local VM manager and an mcollective client allowing VMs to be
created and managed remotely.  I added basic locking to ensure that the same
VM could not be brought up on two servers at the same time, and that VMs would
not start automatically on reboot (since I had no automatic means to fence off
misbehaving servers).  It was a very lightweight wrapper and it wasn't very
user friendly, as you still needed to understand what is going on behind the
scenes.  When you wanted to instantiate a VM, it would lookup the VM by name in
the resource database, run some sanity checks, and then request the remote
hypervisor to create the VM. The system got deployed in multiple datacenters,
became integrated with our system configuration tool (Puppet), and it soon
proved to be reasonably useful and popular in the company, even with its lack
of polish.

Of course, as it got used more and more, it's weaknesses became more apparent.
Using the FQDN of a machine as the primary key meant that we couldn't rename
systems easily, but more importantly it was the only uniqueness key.  A VM was
also only "in the system" after it was assigned to a server, so it wasn't easy
to see what machines are assigned to a cluster.

Around this time I started looking around seriously at external virtualisation
and cloud solutions that we could leverage.  I was hoping to find some existing
software that would plug into our local VM manager instances, since it had been
extended over time and was working quite well, now supporting containers and
several different storage backends, as well as nifty features like live
migration.  I came away from my search disappointed.  Almost every piece of
software out there is purpose built for a specific technology, and those that
are designed to be flexible aren't very hackable.  For me, hackability also
means that it's extensible using a scripting language.

In discussions with a colleague, we analysed the different layers of existing
cloud solutions, and realised that most cloud systems combined the component
that managed individual servers with user management and VM management, and
most cloud software only splits that as an afterthought (OpenNebula is a case
in point).  A common approach seems to be to have multiple internal clouds and
then use an aggregation frontend such as Aoelus, which makes sense for multiple
different clouds, but for a single cloud, it doesn't necessarily make sense.
It's obvious that big cloud providers like Amazon have these components already
separate.

The company leaned toward commercial solution, I was already hooked on the
idea, and I decided to investigate the problem further.

After some more thought, I decided that it would be relatively simple to write
a generic cluster controller.  I initially wrote Vagoth with the fixed concept
of hypervisor servers and VMs, but I discovered a lot of code duplication and
refactored it to have a generic `node`, which could be inherited and extended.
Moving in this direction also opened up the possibily of using Vagoth for other
use-cases.  For example, a `node` might also be a VM in another cloud, or a
`storage device` which could be attached to a VM, or an abstract `service`
which might have VMs as its children.

Vagoth is fundamentally a framework to help you develop a nice API to manage a
cluster of `whatevers`, supplying a simple set of components that will help you
get started, but that you can replace at your leisure.

You'll almost certainly want to extend it yourself, and I hope to see people
using it in weird and wonderful ways that I never imagined.

