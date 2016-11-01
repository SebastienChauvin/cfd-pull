from lxml import html
import requests
import unicodedata
import re
import urllib

import os
from slackclient import SlackClient

page = requests.get('http://parapente.ffvl.fr/cfd/liste/2016/last')
for flightUrl in html.fromstring(page.content).xpath(".//a[contains(@href, '/vol/')]/@href"):
	tree = html.fromstring(requests.get(flightUrl).content)
	nameObject = re.match(".*: Le vol de (.*) du (.*)", tree.xpath(".//h1[@class='title']/text()")[0])
	name = re.sub("/", "_", nameObject.group(2)) + " " + nameObject.group(1) 
	print name
	urllib.urlretrieve(tree.xpath(".//a[contains(@href, 'get3d')]/@href")[0], name + ".kml")
