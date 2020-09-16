#!/usr/bin/env python3

from ps3_update_dl import download_info, Update

def test_lbp2():
	assert download_info('NPUA80662') == ([
		'LittleBigPlanet™2 Digital Version',
		'LittleBigPlanet™2 (version digitale)',
		'LittleBigPlanet™2 - Versión digital',
		'LittleBigPlanet™2: Digitale Version',
		'LittleBigPlanet™2 - versione digitale',
		'LittleBigPlanet™2 digitale versie',
		'Versão Digital LittleBigPlanet™2',
		'Электронная версия LittleBigPlanet™2',
		'LittleBigPlanet™2 디지털 에디션',
		'LittleBigPlanet™2 下載版',
		'LittleBigPlanet™2 下載版',
		'LittleBigPlanet™2-digitaaliversio',
		'LittleBigPlanet™2 - digital version',
		'LittleBigPlanet™2, digital version',
		'LittleBigPlanet™2 – Nedlastingsversjon',
		'LittleBigPlanet™2 - Edycja cyfrowa'
	], [
		Update(version='01.08', size=19340112, ps3_system_ver='03.7000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0108-V0100-PE.pkg', sha1sum=b'\x06I\xa1\xeb\xb2&\x02-\xc9\xf2u\xd6\x8d\xba\xebRA~\x10\xa4'),
		Update(version='01.09', size=23777056, ps3_system_ver='03.7000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0109-V0100-PE.pkg', sha1sum=b'[*\xc5]\x9e\xb2c\x19\xbe\xf3\x1b;\xf2\x8f\xbd\x0e\\C\x7ft'),
		Update(version='01.10', size=180512608, ps3_system_ver='03.7000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0110-V0100-PE.pkg', sha1sum=b'm\x0f0\n\x07\xda\xbc\xb9\xb7-T2\xa8\xa2\x03\xcd\x136\xab\xe1'),
		Update(version='01.11', size=71110560, ps3_system_ver='03.7000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0111-V0100-PE.pkg', sha1sum=b'\xdd\x91{-\x02\x08!\xa8l\xfau;o(\x990\xfc^\xbb\x0b'),
		Update(version='01.12', size=46763936, ps3_system_ver='03.7000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0112-V0100-PE.pkg', sha1sum=b'\n\x92\xc4\xab\x9b\x83\x06\x84\xce6\xe8\xc6\x03\xa2/\xda\xa5\x92rB'),
		Update(version='01.13', size=53142992, ps3_system_ver='03.7000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0113-V0100-PE.pkg', sha1sum=b'\xa3\x80\xf2\x18\x9c3\x93\xc5C{N\x8dU3}\x0b\xd1}\xf4\x81'),
		Update(version='01.14', size=52712272, ps3_system_ver='03.7000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0114-V0100-PE.pkg', sha1sum=b'BZ#O\xdf\x87p\xbfV\x0c)\x80\x19>\xc2|1\xc8\x1a.'),
		Update(version='01.15', size=51745216, ps3_system_ver='03.7000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0115-V0100-PE.pkg', sha1sum=b'\x9aK"\xf8\x1cG\xad\xf9K\xe2{\x91\xb3\x0b-\xb0~E\xfdl'),
		Update(version='01.16', size=47791168, ps3_system_ver='03.7000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0116-V0100-PE.pkg', sha1sum=b'\x87\x85\xce\x96\xe6\xa1%w\xf0\x80\x84~:\xee\x80hf\xea\\+'),
		Update(version='01.17', size=41628704, ps3_system_ver='03.7000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0117-V0100-PE.pkg', sha1sum=b'\x91\xd7\xdb0\x92|\x99z\x82\xb8\x0fM\xcc\xa8\x8b\xbeE\x9f\x98Z'),
		Update(version='01.18', size=48123664, ps3_system_ver='03.7000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0118-V0100-PE.pkg', sha1sum=b'\x13\x8fgX\x81E\x1ag\xd3p\xb5\xb7s@\xd7\xe0\x84t\x97\x9d'),
		Update(version='01.20', size=1042886000, ps3_system_ver='04.2000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0120-V0100-PE.pkg', sha1sum=b'\xc3\xd2\x1e\xee8\tL\xfd\xd7\xe54H\x01\x10\xe6\xb0\xb0\xe1\xde\x06'),
		Update(version='01.21', size=51878816, ps3_system_ver='04.2000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0121-V0100-PE.pkg', sha1sum=b'\xc7\xcf\x9b\xc9h\xbf\xc3\x19F\rUO\xf5\x82\xc7\x1b[\x9a\xd0N'),
		Update(version='01.22', size=57086176, ps3_system_ver='04.2000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0122-V0100-PE.pkg', sha1sum=b'm]\xd3\xd8t\xd9\x0c\xfe\xc1\xc6\x15cn\x0b\x1d\x1bP\xa6\x80j'),
		Update(version='01.23', size=50993152, ps3_system_ver='04.2000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0123-V0100-PE.pkg', sha1sum=b'A\xbc\x81<\xb1\xe62\xc0({\xe8\xb2F\x97\x14\xd4\xd4\x7fl\x01'),
		Update(version='01.24', size=48420480, ps3_system_ver='04.2000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0124-V0100-PE.pkg', sha1sum=b'\xc4\rR\x977\xebR\x02\xa5\xee\xd5|\x9e\xf9\xd8\x11[\x08[\x8d'),
		Update(version='01.25', size=67954480, ps3_system_ver='04.2000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0125-V0100-PE.pkg', sha1sum=b'\x0e\x96\xea"\x18&\x11\xd7\x98\xb1Q\xda\xde\xaa\xec-[\xdc\x84Q'),
		Update(version='01.26', size=51015680, ps3_system_ver='04.2000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0126-V0100-PE.pkg', sha1sum=b'w\xc6\xb5}\tK\xbdQ\xf0@\xf1\xc5\xeaBXI|UF\x0c'),
		Update(version='01.27', size=126827984, ps3_system_ver='04.2000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0127-V0100-PE.pkg', sha1sum=b'\xdaK\x9b.\x8e\xb9\x9b~\x13m\xa4 D\xc0\x1c\xcc\x0b\x03\xd2"'),
		Update(version='01.28', size=858697104, ps3_system_ver='04.2000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0128-V0101-PE.pkg', sha1sum=b'\xf6\x85\xc6r}Q#\xb1\xd3\xba\xa8h\x0b}\x02\x99\x0cO@\x89'),
		Update(version='01.29', size=58387008, ps3_system_ver='04.2000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0129-V0100-PE.pkg', sha1sum=b'\xe9&,r\xc9(\x04\x97T6\xbd[\xd0\xa6\x1cCh\x08\x9d\xba'),
		Update(version='01.30', size=55043440, ps3_system_ver='04.2000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0130-V0100-PE.pkg', sha1sum=b'\x00\x9f\xa8kb\xb4\x94\xa8/qi\xa5\xd1\x19\x19\x1e\xcc\xec\xec\x8a'),
		Update(version='01.31', size=74811376, ps3_system_ver='04.2000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0131-V0100-PE.pkg', sha1sum=b'\xed[\xb8\x12\x8c\xb0\xc9\x19|L\x80\x01r\x88\xd4\x9c1\xaf\x82\xd4'),
		Update(version='01.32', size=58756880, ps3_system_ver='04.2000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0132-V0100-PE.pkg', sha1sum=b'nV[\xbcH\xe2\x91St\xd6r\x19\xfc\xcf\xf6\xa8\xc3+\xbd\x01'),
		Update(version='01.33', size=51276176, ps3_system_ver='04.2000', url='http://b0.ww.np.dl.playstation.net/tppkg/np/NPUA80662/NPUA80662_T28/9c0afd5f52fd06ea/UP9000-NPUA80662_00-GLITTLEBIG000001-A0133-V0100-PE.pkg', sha1sum=b'\xb3\x08e\x8f\xff\x93\xecD\xed\xdbN\xf0T5^n\xe7r\xd8\xcc'),
	])
