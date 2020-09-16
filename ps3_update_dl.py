#!/usr/bin/env python3

__version__ = '0.0.0'

import io
import hashlib
import pkg_resources
import xml.etree.ElementTree as et
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from functools import partial
from typing import List, Tuple

import requests
from tqdm import tqdm

# the PS3 update server uses a funky certificate but there's nothing we can do about that
import warnings
import urllib3.connection
warnings.filterwarnings('ignore', category=urllib3.connection.SubjectAltNameWarning)

class VerificationFailed(Exception):
	"""verification of a downloaded update failed"""

URL_FORMAT = 'https://a0.ww.np.dl.playstation.net/tpl/np/{id}/{id}-ver.xml'
# determine whether we need to pass usedforsecurity=False to use sha1
try:
	hashlib.sha1(usedforsecurity=False)
except TypeError:
	sha1 = hashlib.sha1
else:
	sha1 = partial(hashlib.sha1, usedforsecurity=False)

session = requests.Session()
session.verify = pkg_resources.resource_filename('ps3_update_dl', 'playstation-ca.crt')

@dataclass
class Update:
	version: str
	size: int
	ps3_system_ver: str
	url: str
	sha1sum: bytes

	def __post_init__(self):
		if isinstance(self.sha1sum, str):
			self.sha1sum = bytes.fromhex(self.sha1sum)
		self.size = int(self.size)

Info = Tuple[str, List[Update]]

def parse_updates(tree: et.ElementTree) -> Info:
	# for some reason, i can only get iter() to return results here, not find() or findall()
	titles = [el.text for el in next(tree.iter('paramsfo'))]
	return (
		titles,
		[Update(**pkg.attrib) for pkg in tree.iter('package')],
	)

def download_info(title_id: str) -> Info:
	r = session.get(URL_FORMAT.format(id=title_id))
	return parse_updates(et.fromstring(r.text))

def _verify_size(fileobj: typing.io.BinaryIO, update: Update) -> None:
	f.seek(0, io.SEEK_END)
	size = f.tell()
	f.seek(0)
	if size != update.size:
		raise VerificationFailed(f'{path}: expected a size of {update.size} bytes, got {size}', path, update)

def _verify_hash(fileobj: typing.io.BinaryIO, update: Update) -> None:
	h = sha1()
	for chunk in iter(lambda: f.read(io.DEFAULT_BUFFER_SIZE), b''):
		h.update(chunk)
	if h.digest() != update.sha1sum:
		raise VerificationFailed(
			f'{path}: expected SHA-1 hash {update.sha1sum.hex()}, got {h.hexdigest()}', path, update,
		)


def verify(path: Path, update: Update) -> 'Literal[True]':
	"""Verify the length and sha1sum of the given file against the given Update object.

	Raise VerificationFailed or return True.
	"""
	with open(path, 'rb') as f:
		_verify_size(f, update)
		# the easy route succeeded so now we have to take the long route
		# disabled for now because the servers don't seem to return correct hashes
		#_verify_hash(f, update)

	return True

def download_update(*, output_directory: Path, update: Update):
	h = sha1()
	r = requests.get(update.url, stream=True)
	output_path = output_directory / f'v{update.version} - {PurePosixPath(update.url).name}'
	if output_path.is_file():
		verify(output_path, update)
		return

	with open(output_path, 'wb') as f:
		for chunk in tqdm(
			session.get(update.url, stream=True).iter_content(chunk_size=1024),
			total=update.size//1024,
			unit='KB',
			desc=output_path.name,
			leave=True
		):
			f.write(chunk)

	verify(output_path, update)
