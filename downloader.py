import os

import re
import requests
from lxml import html
from glob import glob

class XKCDDownloader:
	def __init__(self, downloadFrom=1, directory="images"):
		self.directory=directory
		if (not os.path.exists(self.directory)):
			os.mkdir(self.directory)

		for i in range(191,1701):
			if not self.imageExists(i):
				self.download(i)


	def imageExists(self, n):
		p = os.path.join(self.directory, "{n} - *".format(n=n))
		if (len(glob(p)) > 0):
			return True
		return False

	def download(self, n):
		url = getURL(n)
		try:
			imageURL,imageName = getImageInfo(url)
		except:
			return
		dwl_filename = os.path.basename(imageURL)
		fileExt = os.path.splitext(dwl_filename)[1]
		filename = "{n} - {imageName}{file_ext}".format(n=n, imageName=imageName, file_ext=fileExt)
		localpath = os.path.join(self.directory, filename)
		if not os.path.exists(localpath):
			command = "curl -o \"{path}\" \"{imgURL}\"".format(path=localpath, imgURL=imageURL)
			print(command)
			os.system(command)
		else:
			print ("{path} already exists, skipping".format(path=localpath))

def getURL(n):
	return "https://xkcd.com/{n}/".format(n=n)

def getImageInfo(url):
	htmlData = requests.get(url).content
	htmlTree = html.fromstring(htmlData)
	imgTree = htmlTree.xpath('//*[@id=\"comic\"]/img')
	try:
		if (len(imgTree) == 0):
			imgTree = htmlTree.xpath('//*[ @ id = "comic"] / a / img')
		img = imgTree[0]
	except:
		raise Exception("Error downloading \"{n}\"".format(n=url))


	imgURL = img.attrib['src'].replace("//","https://")
	imgName = img.attrib['alt']
	imgName = re.sub(r'<.*?>', '', imgName)
	return (imgURL, imgName)


