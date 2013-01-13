Getting Started
===============

Vagoth is designed to be pluggable, and it doesn't come with defaults in the
code.  This means that you have to create a configuration file before you
start.  In examples/vagoth.conf you will find an example configuration
file with sane defaults.


Web interface
-------------

The only interface to Vagoth is the Python API.  If you want a web GUI or a
REST API, you'll have to write it yourself.  For virtualisation, I recommend a
design where you don't give users direct access to the cluster controller, but
rather have a separate `Cloud Manager` which does user management, access
control, and tracks which VMs are running in which clusters.
