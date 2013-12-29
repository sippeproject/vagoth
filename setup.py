#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name = "vagoth",
    version = "0.9.3",
    description = "Pluggable cluster controller (eg. for VM management)",
    packages = find_packages(),
    package_data = {
        'vagoth.virt.utils': [ "*.rb", ],
    },
    scripts = ["bin/vagoth"],
    license = "LGPL 2.1",
    keywords = "Cluster Management Framework",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: No Input/Output (Daemon)",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
    ]
)
