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

#
# Some utility functions
#

def matches_tags(tag_matches, tags):
    """Do the given tag_matches match the given tags?

    If the tag_matches value is None, it only checks for tag existence.

    If the tag_matches value is not None, it does a direct comparison.
    For each key/value pair, check if the tag exists, and if the value is
    not None, if the value matches.

    :param tag_matches: key-value pairs we want to check for
    :param tags: key-value pairs that we'll check against
    :returns: bool
    """
    assert tag_matches
    assert type(tags) == dict

    for tag_name, tag_value in tag_matches.items():
        if tag_name not in tags:
            return False
        if tag_value is not None and tag_value != tags[tag_name]:
            return False
    return True

