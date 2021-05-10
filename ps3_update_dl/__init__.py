#!/usr/bin/env python3

__version__ = '0.0.2'

import io
import sys
import typing
import hashlib
import pkg_resources
from http import HTTPStatus
from functools import partial
import xml.etree.ElementTree as et
from pathlib import Path, PurePosixPath
from dataclasses import dataclass, field
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
	from typing import Literal

import requests
from tqdm import tqdm

import warnings
import urllib3.connection
# the PS3 update server uses a funky certificate but there's nothing we can do about that
warnings.filterwarnings('ignore', category=urllib3.connection.SubjectAltNameWarning)
# the server also uses old ciphers, but some ciphers are better than none (issue #2)
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

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
	r.raise_for_status()
	return parse_updates(et.fromstring(r.text))

def _file_size(fp: typing.io.BinaryIO) -> int:
	old_pos = fp.tell()
	fp.seek(0, io.SEEK_END)
	size = fp.tell()
	fp.seek(old_pos)
	return size

# unused for now as the PS3 servers seem to return incorrect hashes
def _verify_hash(fp: typing.io.BinaryIO, update: Update) -> None:
	h = sha1()
	fp.seek(0)
	for chunk in iter(lambda: fp.read(io.DEFAULT_BUFFER_SIZE), b''):
		h.update(chunk)
	if h.digest() != update.sha1sum:
		raise VerificationFailed(
			f'{path}: expected SHA-1 hash {update.sha1sum.hex()}, got {h.hexdigest()}', path, update,
		)

def download_update(*, output_dir: Path, update: Update, overwrite=False):
	output_path = output_dir / f'v{update.version} - {PurePosixPath(update.url).name}'
	downloaded = 0
	if output_path.is_file():
		with open(output_path, 'rb') as f:
			downloaded = _file_size(f)
			if not overwrite and downloaded == update.size:
				print(output_path.name, 'seems to already be downloaded. Pass --force if not.', file=sys.stderr)
				return
			if not overwrite and downloaded > update.size:
				print(output_path.name, 'is larger than expected. Pass --force to re-download it.', file=sys.stderr)
				return

	headers = {}
	if downloaded < update.size:
		mode = 'ab'
		headers['Range'] = f'bytes={downloaded}-{update.size}'
	else:
		mode = 'wb'

	with open(output_path, mode) as f:
		r = session.get(update.url, headers=headers, stream=True)
		if r.status_code == HTTPStatus.OK:
			# server wants to give us the whole file
			f.seek(0)
		elif r.status_code != HTTPStatus.PARTIAL_CONTENT:
			print(f'Warning: download failed for {output_path.name}. Skipping.', file=sys.stderr)
			return

		with tqdm(
			r.iter_content(chunk_size=1024),
			total=update.size//1024,
			unit='KB',
			desc=output_path.name,
			leave=True,
		) as bar:
			bar.update(downloaded//1024)
			for chunk in bar:
				f.write(chunk)

def download_updates(*, base_dir: Path, title_id: str, overwrite=False):
	try:
		(title, *_), updates = download_info(title_id)
	except requests.HTTPError:
		print(f"Error downloading “{title_id}”. Make sure it's a valid game ID.", file=sys.stderr)
		return

	output_dir = base_dir / title
	output_dir.mkdir(exist_ok=True)
	print(f'Downloading “{title}” [{title_id}]...', file=sys.stderr)
	for update in updates:
		download_update(output_dir=output_dir, update=update, overwrite=overwrite)

USAGE = """\
Usage: ps3udl -o BASE_DIR TITLE_ID_1 [TITLE_ID_2...]

Download all updates for all given titles to the given base directory.
A subdirectory inside the base directory will be created for each title.

Options:
	-o, --base-dir
	The directory that all titles will be downloaded to. It must exist.

	-f, --force
	Whether to overwrite existing files.

	-h, --help
	Display this message.
"""

def parse_args(args):
	import getopt

	opts, args = getopt.gnu_getopt(
		args,
		'o:fh',
		['base-dir', 'force', 'help'],
	)
	opts = dict(opts)
	if not opts or not args or '-h' in opts or '--help' in opts:
		print(USAGE, file=sys.stderr)
		sys.exit(0)

	if ('--base-dir' in opts) == ('-o' in opts):
		print('Must specify exactly one of -o, --base-dir.', file=sys.stderr)
		sys.exit(1)

	overwrite = '-f' in opts or '--force' in opts
	base_dir = Path(opts.get('-o', opts.get('--base-dir')))
	return dict(overwrite=overwrite, base_dir=base_dir, title_ids=args)

def _main():
	kwargs = parse_args(sys.argv[1:])
	title_ids = kwargs.pop('title_ids')
	for title_id in title_ids:
		download_updates(**kwargs, title_id=title_id)
		print(file=sys.stderr)

def main():
	try:
		_main()
	except KeyboardInterrupt:
		pass

if __name__ == '__main__':
	main()
