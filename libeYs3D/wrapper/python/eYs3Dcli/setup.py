#! /usr/bin/env python
'''
 Copyright (C) 2015-2019 ICL/ITRI
 All rights reserved.

 NOTICE:  All information contained herein is, and remains
 the property of ICL/ITRI and its suppliers, if any.
 The intellectual and technical concepts contained
 herein are proprietary to ICL/ITRI and its suppliers and
 may be covered by Taiwan and Foreign Patents,
 patents in process, and are protected by trade secret or copyright law.
 Dissemination of this information or reproduction of this material
 is strictly forbidden unless prior written permission is obtained
 from ICL/ITRI.
'''

from setuptools import setup

__version__ = ''
exec(open('eYs3Dcli/version.py').read())

setup(
    name = 'eYs3Dcli',
    version = __version__,
    description = 'An administration shell for eYs3D.',
    license = 'Apache 2.0',
    maintainer = 'K.T. Alumi',
    maintainer_email = 'ktAlumi@itri.org.tw',
    url = '',
    packages = ['eYs3Dcli'],
    scripts = [
               'scripts/eYs3Dcli'
              ],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    )
