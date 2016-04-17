#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json,codecs,sys

reload(sys)
sys.setdefaultencoding("utf-8")

filename = ""
#Insert your MelOn path

encoded_text = open(filename, 'rb').read()
bom = codecs.BOM_UTF16_LE
assert encoded_text.startswith(bom)
encoded_text = encoded_text[len(bom):]
decoded_text = encoded_text.decode('utf-16le').encode('utf-8')

jsonObj = json.loads(decoded_text)['NowPlaylist']

unique_stuff = { each['ID'] : each for each in jsonObj }.values()
dat = json.dumps(unique_stuff,ensure_ascii=False)

melon = '{"NowPlaylist":' + dat.encode('utf-8') + "}"

f = codecs.open(filename, "wb", 'utf-16')
f.write(melon)
f.close()
