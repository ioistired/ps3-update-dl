#!/usr/bin/env python3

__version__ = '0.0.0'

import xml.etree.ElementTree as et
from dataclasses import dataclass, field
from typing import List, Tuple

import requests

# the PS3 update server uses a funky certificate but there's nothing we can do about that
import warnings
import urllib3.connection
warnings.filterwarnings('ignore', category=urllib3.connection.SubjectAltNameWarning)

URL_FORMAT = 'https://a0.ww.np.dl.playstation.net/tpl/np/{id}/{id}-ver.xml'

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
	r = requests.get(URL_FORMAT.format(id=title_id), verify='playstation-ca.crt')
	return parse_updates(et.fromstring(r.text))
