#!/usr/bin/python
# vim: set fileencoding=utf-8 :
#
# Copyright (C) 2016 Guido Günther <agx@sigxcpu.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with it.  If not, see <http://www.gnu.org/licenses/>.
#
# END OF COPYRIGHT #

import subprocess
from setuptools import setup, find_packages
import os


def fetch_version():
    """Get version from debian changelog and write it to gbp/version.py"""
    version = "0.0"

    try:
        popen = subprocess.Popen('dpkg-parsechangelog', stdout=subprocess.PIPE)
        out, ret = popen.communicate()
        for line in out.decode('utf-8').split('\n'):
            if line.startswith('Version:'):
                version = line.split(' ')[1].strip()
                break
    except OSError:
        pass # Failing is fine, we just can't print the version then

    with open('gbp/version.py', 'w') as f:
        f.write('"The current gbp version number"\n')
        f.write('gbp_version="%s"\n' % version)

    return version


def readme():
    with open('README') as file:
        return file.read()

setup(name = "foreman_ansible_inventory",
      version = "0.0.1",
      author = u'Guido Günther',
      author_email = 'agx@sigxcpu.org',
      description = 'Ansible dynamic inventory that queries the Foreman',
      license = 'GPLv3+',
      classifiers = [
          'Environment :: Console',
          'Programming Language :: Python :: 2',
          'Operating System :: POSIX :: Linux',
      ],
      scripts = ['foreman_ansible_inventory.py'],
      requires = ["requests"],
)
