#! /bin/python3

import getopt
import os
from sys import argv
from downloader import XKCDDownloader

import sys


def printHelp():
	print("""Welcome to XKCD Comic Downloader,
usage : downloader.py [options]
options:
\t-d, --directory=DIR\tSpecify a directory to download to.""")


def main():
	try:
		opts, args = getopt.getopt(argv[1:], "hd:", ["directory=", "help"])
	except getopt.GetoptError as err:
		print(err)
		return

	path = "./images"
	for opt,arg in opts:
		if opt in ("-h", "--help"):
			printHelp()
			sys.exit(0)
		if opt in ("-d", "--directory"):
			path = arg
			if not os.path.exists(path):
				print ("Error, {path} does not exist.".format(path=path))
				sys.exit(-1)

	downloader = XKCDDownloader(directory=path)

if __name__ == "__main__":
	main()