Provisioner
===========

Overview
--------

The provisioner is responsible for checking and modifying the definition of a
node before it is saved to the registry.

An example usage would be to convert a definition with vm_size=small into an
appropriate definition, complete with allocated IPs and storage information.

The provisioner is run in the foreground (but it could, for example, queue
background actions by calling manager.scheduler.whatever()
