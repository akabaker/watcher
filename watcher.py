#!/usr/bin/env python
from subprocess import Popen
from datetime import datetime
from os import path
import gzip
import pyscreenshot
import time
import sys

def take_screenshot(filename):
	"""Takes a screenshot of entire screen. 

	Compresses output png with gzip and deletes the original file. This function 
	should eventually save the file to Amazon s3 or at the least scp/rsync to another
	host.

	"""

	try:
		print "Saving screenshot {0}.gz\r".format(filename)
		pyscreenshot.grab_to_file(filename)
		file_in = open(filename, 'rb')
		file_out = gzip.open(filename + '.gz', 'wb')
		file_out.writelines(file_in)
		Popen('rm -f {0}'.format(filename), shell=True, stdout=PIPE).communicate()
	except IOError, e:
		print e
		sys.exit(1)
	finally:
		file_out.close()
		file_in.close()

def start_stream():
	"""Opens vlc http stream using subprocess, kind of messy"""

	Popen('vlc-wrapper v4l2:///dev/video0 --sout "#transcode{vcodec=theo}:standard{access=http,mux=ogg,dst=:8080}" -I dummy &> /dev/null', shell=True)

def generate_filename():
	"""Generates a timestamp for the screenshot which is used as the file name."""

	time = datetime.now()
	time_str = datetime.strftime(time, "%d-%m-%y_%H-%M-%S")
	output_dir = '/tmp'
	name = "{0}_{1}.png".format('capture', time_str)
	filename = path.join(output_dir, name)
	return filename

def main():
	"""Start the vlc process and save a screenshot every n seconds"""
	try: 
		start_stream()
	except Exception, e:
		print e
		sys.exit(1)

	filename = generate_filename()
	take_screenshot(filename)
	time.sleep(15)

while True:
	try:
		main()
	except KeyboardInterrupt:
		print "\rClosing.."
		sys.exit()
