#!/usr/bin/env python3

import xml.etree.ElementTree as et
from dataclasses import dataclass, field
from typing import List, Tuple

import requests

URL_FORMAT = 'https://a0.ww.np.dl.playstation.net/tpl/np/{id}/{id}-ver.xml'

@dataclass
class Update:
	version: str
	size: int
	sha1sum: bytes
	url: str
	ps3_system_ver: str

	def __post_init__(self):
		self.sha1sum = bytes.fromhex(self.sha1sum)
		self.size = int(self.size)

def parse_updates(tree: et.ElementTree) -> Tuple[str, List[Update]]:
	root = tree.getroot()
	return (
		# for some reason, i can only get iter() to return results here, not find() or findall()
		next(root.iter('TITLE')).text,
		[Update(**pkg.attrib) for pkg in root.iter('package')],
	)

