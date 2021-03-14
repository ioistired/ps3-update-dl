#!/usr/bin/env python3

import re
import setuptools
import sys
from pathlib import Path

HERE = Path(__file__).parent

with open(HERE / 'ps3_update_dl' / '__init__.py') as f:
	VERSION = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not VERSION:
	raise RuntimeError('version is not set')

with open(HERE / 'README.md') as f:
	README = f.read()

setuptools.setup(
	name='ps3-update-dl',
	author='io mintz',
	url='https://github.com/iomintz/ps3-update-dl',
	version=VERSION,
	packages=['ps3_update_dl'],
	package_data={'ps3_update_dl': ['*.crt']},
	license='AGPLv3+',
	description='Download all updates for a given PS3 game',
	long_description=README,
	long_description_content_type='text/markdown; variant=GFM',
	install_requires=[
		'requests>=2.23.0,<3.0.0',
		'tqdm>=4.49.0,<5.0.0',
	],
	extras_requires=[{'dev': ['pytest>=6.0.2,<7.0.0']}],
	python_requires='>=3.7.0',
	classifiers=[
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
		'Development Status :: 3 - Alpha',
		'Environment :: Console',
		'Intended Audience :: End Users/Desktop',
		'Topic :: Games/Entertainment',
		'Topic :: System :: Emulators',
		'Topic :: Utilities',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9',
		'Programming Language :: Python :: Implementation',
		'Programming Language :: Python :: Implementation :: CPython',
	],
	entry_points={
		'console_scripts': ['ps3udl = ps3_update_dl:main'],
	},
)
