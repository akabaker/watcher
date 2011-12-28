#!/usr/bin/env python
from subprocess import Popen, PIPE
from os import path
from random import random
import gzip
import pyscreenshot
import time
import sys
import sha

def take_screenshot(filename):
	print "Saving screenshot {0}.gz\r".format(filename)
	pyscreenshot.grab_to_file(filename)
	file_in = open(filename, 'rb')
	file_out = gzip.open(filename + '.gz', 'wb')
	file_out.writelines(file_in)
	file_out.close()
	file_in.close()
	Popen('rm -f {0}'.format(filename), shell=True, stdout=PIPE).communicate()

def start_stream():
	pipe = Popen('vlc -vvv v4l2:///dev/video0 --sout "#transcode{vcodec=theo}:standard{access=http,mux=ogg,dst=:8080}" -I dummy', shell=True, stdout=PIPE)

def save_screenshot():
	sha_value = sha.new(str(random())).hexdigest()
	output_dir = '/tmp'
	name = "{0}_{1}.png".format('capture', sha_value)
	filename = path.join(output_dir, name)
	return filename

while True:
	try:
		filename = save_screenshot()
		take_screenshot(filename)
		time.sleep(10)
	except KeyboardInterrupt:
		print "\rClosing.."
		sys.exit()
