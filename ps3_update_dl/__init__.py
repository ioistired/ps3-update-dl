#!/usr/bin/env python3

__version__ = '0.3.0.post1'

import io
import sys
import yaml
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
session.headers['User-Agent'] = f'{__name__}/{__version__} ' + session.headers['User-Agent']

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
	try:
		# r.content instead of r.text because the server doesn't declare an encoding, but the XML does
		return parse_updates(et.fromstring(r.content))
	except et.ParseError as exc:
		print('Could not parse response. No update available?', file=sys.stderr)
		sys.exit(2)

def _file_size(fp: typing.io.BinaryIO) -> int:
	old_pos = fp.tell()
	fp.seek(0, io.SEEK_END)
	size = fp.tell()
	fp.seek(old_pos)
	return size

def _verify_hash(fp: typing.io.BinaryIO, filename: str, update: Update) -> None:
	h = sha1()

	# chop off last 32 bytes temporarily
	fp.seek(-32, io.SEEK_END)
	extra = fp.read()
	fp.seek(-32, io.SEEK_END)
	fp.truncate()

	fp.seek(0)
	for chunk in iter(lambda: fp.read(io.DEFAULT_BUFFER_SIZE), b''):
		h.update(chunk)

	# put those 32 bytes back
	fp.seek(0, io.SEEK_END)
	fp.write(extra)

	if h.digest() != update.sha1sum:
		print(f'{filename}: expected SHA-1 hash {update.sha1sum.hex()}, got {h.hexdigest()}')
		sys.exit(3)

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
		mode = 'a+b'
		headers['Range'] = f'bytes={downloaded}-{update.size}'
	else:
		mode = 'w+b'

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

		_verify_hash(f, output_path.name, update)

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
Usage: ps3udl [-c GAMES_YML_PATH] -o BASE_DIR [TITLE_ID_1 TITLE_ID_2...]

Download all updates for all given titles to the given base directory.
A subdirectory inside the base directory will be created for each title.

Titles are specified via command-line args or the games.yml file or both.

Options:
	-o BASE_DIR, --base-dir BASE_DIR
	The directory that all titles will be downloaded to. It must exist.

	-c GAMES_YML_PATH, --games-yml-path GAMES_YML_PATH
	Path to your RPCS3 games.yml file. All updates for all games listed in this file will be downloaded if specified.

	-f, --force
	Whether to overwrite existing files.

	-h, --help
	Display this message.
"""

def parse_args(args):
	import getopt

	opts, args = getopt.gnu_getopt(
		args,
		'o:c:fh',
		['base-dir=', 'games-yml-path=', 'force', 'help'],
	)
	opts = dict(opts)
	games_yml_path = opts.get('-c', opts.get('--games-yml-path'))
	if not opts or (not games_yml_path and not args) or '-h' in opts or '--help' in opts:
		print(USAGE, file=sys.stderr)
		sys.exit(0)

	if ('--base-dir' in opts) == ('-o' in opts):
		print('Must specify exactly one of -o, --base-dir.', file=sys.stderr)
		sys.exit(1)

	if '--games-yml-path' in opts and '-c' in opts:
		print('Can only specify one of --games-yml-path, -c.', file=sys.stderr)
		sys.exit(1)

	overwrite = '-f' in opts or '--force' in opts
	base_dir = Path(opts.get('-o', opts.get('--base-dir')))
	if games_yml_path is not None:
		games_yml_path = Path(games_yml_path)
	return dict(overwrite=overwrite, base_dir=base_dir, games_yml_path=games_yml_path, title_ids=args)

def _main():
	kwargs = parse_args(sys.argv[1:])
	title_ids = kwargs.pop('title_ids')
	games_yml_path = kwargs.pop('games_yml_path')
	if games_yml_path is not None:
		with games_yml_path.open() as games_yml:
			title_ids.extend(yaml.safe_load(games_yml))

	for title_id in title_ids:
		download_updates(**kwargs, title_id=title_id)

def main():
	try:
		_main()
	except KeyboardInterrupt:
		pass

if __name__ == '__main__':
	main()
