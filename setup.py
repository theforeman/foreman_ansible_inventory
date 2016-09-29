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

from setuptools import setup

setup(name="foreman_ansible_inventory",
      version="0.0.4",
      author=u'Guido Günther',
      author_email='agx@sigxcpu.org',
      description='Ansible dynamic inventory that queries the Foreman',
      license='GPLv3+',
      classifiers=[
          'Environment :: Console',
          'Programming Language :: Python :: 2',
          'Operating System :: POSIX :: Linux',
      ],
      scripts=['foreman_ansible_inventory.py'],
      requires=["requests"],
      tests_require=['responses'],
      )
