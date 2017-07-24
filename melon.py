#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import _winreg
import json,sys,codecs
import subprocess
from shutil import copyfile

reload(sys)
sys.setdefaultencoding("utf-8")

def remove_duplicates(path,file):
	try:
		filename = str(path) + str(file)

		copyfile(filename, path + str(file.split(".")[0] + ".bak"))
		print "[*] Backup Complete"

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
		print "[*] Jobs done"
	except Exception, err:
		print "Fail!! Reason: ", err
		sys.exit(1)

if __name__ == "__main__":
	print "Starting removing duplicates songs.."
	print "This program is from https://github.com/songmw90/melon-playlist-duplicates-remover and can be freely distributed."
	print "If you have any questions, please send it to admin@fantazm.net."
	print "----------------------------------------------------------"

	try:
		s = subprocess.check_output('tasklist', shell=True)
		if "Melon.exe" in s:
			raw_input("Program will terminate Melon App. If you're ready, press enter or exit program")
			kill_proc = os.system("taskkill /f /im Melon.exe")
	except Exception, err:
		print "[-] Fail! Reason: ", err
		sys.exit(1)

	try:
		key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Software\\Melon40")
		path =  _winreg.QueryValueEx(key, "InstallPath")[0]
		path = path + "\\Playlist\\"
		print ""
	except Exception, Err:
		print "[-] Fail! Reason: ", Err
		sys.exit(1)

	try:
		if len(os.listdir(path)) > 0:
			print "The program will make a backup. The extension of the backup file is .bak. In case of trouble, please change the extension name to .alst."

			for file in os.listdir(path):
				if ".alst" in file:
					remove_duplicates(path,file)
		else:
			raise "Can't not find playlist"
	except Exception, err:
		print "[-] Fail! Reason: ", err
		sys.exit(1)
		
raw_input("")
