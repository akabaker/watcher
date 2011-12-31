#!/usr/bin/env python
from subprocess import Popen, PIPE
from datetime import datetime
from os import path
import gzip
import pyscreenshot
import time
import sys

def take_screenshot(filename):
	"""
	Take a screenshot of entire screen. 
	Compresses output png with gzip and deleted the original file.
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
	pipe = Popen('vlc-wrapper v4l2:///dev/video0 --sout "#transcode{vcodec=theo}:standard{access=http,mux=ogg,dst=:8080}" -I dummy &> /dev/null', shell=True, stdout=PIPE)

def generate_filename():
	time = datetime.now()
	time_str = datetime.strftime(time, "%d-%m-%y_%H-%M-%S")
	output_dir = '/tmp'
	name = "{0}_{1}.png".format('capture', time_str)
	filename = path.join(output_dir, name)
	return filename

def main():
	try: 
		start_stream()
	except Exception, e:
		print e
		sys.exit(1)

	filename = generate_filename()
	take_screenshot(filename)
	time.sleep(10)

while True:
	try:
		main()
	except KeyboardInterrupt:
		print "\rClosing.."
		sys.exit()
