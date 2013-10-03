Introduction
============

Vagoth provides a cluster management framework that you can build upon to
create interesting applications where you have the concept of `nodes` which can
have relationships to one another, finite resources that must be tracked, and a
lifecycle which starts with provisioning and ends with deprovisioning.  What
they do along the way is up to the specific implementation, but it can make use
of a job scheduler and actions to perform tasks in the background.  Is that
abstract enough for you?

A more concrete example is managing a cluster of virtual machines and the
servers they run upon.  In fact, Vagoth comes with a set of components to do
just that.

Possible Uses
-------------

I purposefully didn't want Vagoth to be just for virtualisation, because the
possibilities for a flexible resource tracking database with asynchronous
actions are quite diverse.

Here are some further ideas:

Integration point
  Register all your nodes with a Vagoth instance, and use Vagoth's
  provisioning possibilities to integrate with DHCP, DNS, TFTP/PXE services, or
  to help generate configuration for your monitoring and trending solutions.

Cloud Manager
  With a few new components, Vagoth should also fit nicely into the cloud
  manager role, where it talks with various Cluster Coordinators or other cloud
  providers, but doesn't need to care about the specifics of a cluster or its
  technologies.  A parent 'node' is simply an account on another system.

Service Manager
  It could be extended into the Service Management space, where it tracks load
  and performance information about specific services and brings up or takes down
  service instances as load demands. Similarly, it can tie into your application
  deployment system, to trigger and track releases.
