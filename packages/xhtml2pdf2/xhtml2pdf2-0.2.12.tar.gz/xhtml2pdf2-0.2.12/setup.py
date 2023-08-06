#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2010 Dirk Holtwick, holtwick.it
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import xhtml2pdf
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


setup(
    name="xhtml2pdf2",
    version=xhtml2pdf.__version__,
    description="PDF generator using HTML and CSS",
    license="Apache License 2.0",
    author="Dirk Holtwick",
    maintainer="Bruno Miglioretto",
    maintainer_email="brunomiglioretto@gmail.com",
    url="http://github.com/brunomiglioretto/xhtml2pdf",
    keywords="PDF, HTML, XHTML, XML, CSS",
    install_requires=[
        "arabic-reshaper>=3.0.0",
        "html5lib>=1.0.1",
        "Pillow>=8.1.1",
        "pyHanko>=0.12.1",
        "pyhanko-certvalidator>=0.19.5",
        "pypdf>=3.1.0",
        "python-bidi>=0.4.2",
        "reportlab>=3.5.53,<4",
        "svglib>=1.2.1",
    ],
    include_package_data=True,
    packages=find_packages(exclude=["tests", "tests.*", "manual_test", "manual_test.*"]),
    #    test_suite = "tests", They're not even working yet
    entry_points={
        'console_scripts': [
            'pisa = xhtml2pdf.pisa:command',
            'xhtml2pdf = xhtml2pdf.pisa:command',
        ]
    },
    long_description=README,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Documentation',
        'Topic :: Multimedia',
        'Topic :: Office/Business',
        'Topic :: Printing',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Fonts',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Utilities',
    ]
)
