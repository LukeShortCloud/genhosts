#!/usr/bin/python

# Version: 0.1.0
# Author: ekultails@gmail.com
# URL: https://github.com/ekultails

from multiprocessing import Process
from os import remove
from re import search
from sys import version_info
import urllib


class GenHosts:


	def get_hosts(self, url, save_file):
	
		# create an empty list for storing ad hosting domains
		ad_hosts = []

		filedownload(url, save_file)
		open_file = open(save_file, "r")
		
		for line in open_file:
			
			# skip commented out lines
			if line[0] is "#" or line[0] is ";":
				continue
			
			# convert to lowercase string characters
			line = line.lower()
			# do a regular expression match for domain names;
			# 	all top level domains are letters only so we do not need to worry about
			# 	stripping out IP addresses for false positives
			regex_domains_search = search('[a-z0-9]*\.*[a-z0-9]+\.+[a-z]+', line)
			
			# if a match is found, append it to our list of hosts
			if regex_domains_search:
				ad_hosts.append(regex_domains_search.group())

		# close the hosts file we were readying
		open_file.close()
		# clean-up, delete the downloaded hosts file
		remove(save_file)

		print(ad_hosts)
		return ad_hosts

	
	def exec_threads(self, run_func, run_args):
		
		# provide (A) the target function and (B) the arguments to that function;
		# initiate/start the new process, and then have it join it's own thread
		p = Process(target=run_func, args=(run_args))
		p.start()
		p.join()


if __name__ == "__main__":

	# compatibility fixes ensure that Python can easily download files
	# using both Python versions 2 or 3
	if version_info[:1] == (2,):
	
		try:
			from urllib import urlretrieve
			def filedownload(url, filename):
				urllib.urlretrieve(url, filename)
		except NameError:
			pass

	elif version_info[:1] == (3,):
		
		try:
			from urllib import request
			def filedownload(url, filename):
				urllib.request.urlretrieve(url, filename)
		except NameError:
			pass

	else:
		print("Unsupported Python version. Please use 2.x or 3.x")
		sys.exit(1)

	hostsObj = GenHosts()
	# Format:
	# "http://url_name_here.tld", "/tmp/save_file_name.txt"
	listOfHosts = {}
		
	# sort out our dictionary
	for url in listOfHosts:
		save_file = listOfHosts[url]

		# multi-threaded execution of getting the domain names
		hostsObj.exec_threads(hostsObj.get_hosts, [url, save_file])

