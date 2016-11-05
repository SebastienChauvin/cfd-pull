from lxml import html
from pathlib import Path
import requests
import unicodedata
import re
import urllib

import os
from slackclient import SlackClient

downloaded_lst = []
try:
	downloaded_lst = [line.rstrip('\n') for line in open('downloaded_lst.txt', "r")]
except OSError:
	print "no download list"
except IOError:
	print "no download list"

page = requests.get('http://parapente.ffvl.fr/cfd/liste/2016/last')
for flightUrl in html.fromstring(page.content).xpath(".//a[contains(@href, '/vol/')]/@href"):
	if not (flightUrl in downloaded_lst):
		tree = html.fromstring(requests.get(flightUrl).content)
		nameObject = re.match(".*: Le vol de (.*) du (.*)", tree.xpath(".//h1[@class='title']/text()")[0])
		name = re.sub("/", "_", nameObject.group(2)) + " " + nameObject.group(1) 
		print name
		filename = name + ".kml"
		files = tree.xpath(".//a[contains(@href, 'get3d')]/@href")
		if (len(files) > 0):
			if (not Path(filename).is_file()):
				urllib.urlretrieve(files[0], filename)
			else:
				print "skipped"
		with open("downloaded_lst.txt", "a") as f:
			f.write(flightUrl + "\n")
	else:
		print "already donwloaded " + flightUrl
