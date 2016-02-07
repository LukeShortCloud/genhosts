#!/usr/bin/python

# Version: 0.2.0
# Author: ekultails@gmail.com
# URL: https://github.com/ekultails

from multiprocessing import Process
from os import remove
from re import search
from sys import argv, exit, version_info
import urllib


class GenHosts:


    def get_hosts(self, url, save_file):
    
        # create an empty list for storing ad hosting domains
        domains_list = []

        filedownload(url, save_file)
        open_file = open(save_file, "r")
        
        for line in open_file:
            
            # skip commented out lines
            if line[0] is "#" or line[0] is ";":
                continue
            
            # convert to lowercase string characters
            line = line.lower()
            # do a regular expression match for domain names;
            #   all top level domains are letters only so we do not need to worry about
            #   stripping out IP addresses for false positives
            regex_domains_search = search('[a-z0-9]*\.*[a-z0-9]+\.+[a-z]+', line)
            
            # if a match is found, append it to our list of hosts
            if regex_domains_search:
                domains_list.append(regex_domains_search.group())

        # close the hosts file we were readying
        open_file.close()
        # clean-up, delete the downloaded hosts file
        remove(save_file)

        return domains_list


    def gen_hosts(self, dns_server, domains_list, ipaddr):


        host_dns_entries = []

        for domain in domains_list:
        
            if dns_server == "dnsmasq":
                # format:
                #address=/domain.tld/127.0.0.1
                dns_entry = "address=/%s/%s" % (domain, ipaddr)
                host_dns_entries.append(dns_entry)
            elif dns_server == "unbound":
                # format:
                #local-zone: "domain.tld." static
                #local-data: "domain.tld. 10800 IN A 127.0.0.1"
                dns_entry = ("local-zone: \"%s\" static\n"
                             "local-data: \"%s\" 10800 IN A %s" % (domain, domain, ipaddr))
                host_dns_entries.append(dns_entry)
            elif dns_server == "unix":
                # format:
                #127.0.0.1 domain.tld
                dns_entry = ("%s\t%s" % (ipaddr, domain))
                host_dns_entries.append(dns_entry)    
            elif dns_server == "windows":
                # format:
                #127.0.0.1 domain.tld
                # note: Windows uses \r\n for new lines instead of the Unix \n
                dns_entry = ("%s\t%s\r\n" % (ipaddr, domain))
                host_dns_entries.append(dns_entry)    

        return host_dns_entries
    

    def exec_threads(self, run_func, run_args):
     
   
        # provide (A) the target function (string) and 
        # (B) the arguments to that function (a list is preferred);
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
        exit(1)

    hostsObj = GenHosts()
    # format:
    # {"http://url_name_here.tld": "/tmp/save_file_name.txt"}
    url_hosts = {}
    
    # sort out our dictionary
#    for url in url_hosts:
#        save_file = url_hosts[url]

        # multi-threaded execution of getting the domain names
        # note: this does NOT return values; the use of Pools or Queues should be used
        #hostsObj.exec_threads(hostsObj.get_hosts, [url, save_file])

#        result = hostsObj.get_hosts(url, save_file)
#        print(result)

    # skip the first command line option which should
    # always be the "genhosts" command itself
    cli_options_count = len(argv)
    counter = 0

    for cli_option in argv:
        
        if counter == 0:
            counter += 1
            continue
        
        if argv[counter] == "-h" or argv[counter] == "--help":
            print("Usage: genhosts -s {dnsmasq|unbound|unix|windows} <IP address>"
                  " -u <URL>\n"
                  "-s, --server\tspecify DNS/hosts server as \"dnsmasq\", \"unbound\", \"unix\", \"windows\"\n"
                 "-u, --url\tprovide a list of comma seperated URLs of hosts files")
        elif argv[counter] == "-s" or argv[counter] == "--server":
            counter += 1
            dns_server = argv[counter]
            
            # if no IP address is given after "--server",
            # then use "127.0.0.1" as the default
            if counter + 1 >= len(argv):
                ipaddr = "127.0.0.1"
                continue
            elif search('[0-9]+\.+[0-9]+\.+[0-9]+\.+[0-9]+', argv[counter + 1]):
                ipv4_found = True

            if ipv4_found == True:
                ipaddr = argv[counter + 1]
                counter += 1

        elif argv[counter] == "-u" or argv[counter] == "--url":
            url_hosts = argv[counter + 1].split(",")

        elif argv[counter] == "-v" or argv[counter] == "--version":
            print("GenHosts 0.2.0") 

        counter += 1
    
        if counter >= cli_options_count:
            break
        
    for url in url_hosts:
        # get the file name of the file being downloaded
        # save it into the "save_file" variable
        url_split = url.split("/")
        url_length = len(url_split)
        save_file = url_split[url_length - 1]

        domains_list = hostsObj.get_hosts(url, save_file)
        
        try: 
            host_dns_entries = hostsObj.gen_hosts(dns_server, domains_list, ipaddr)
        except:
            print("Invalid or missing arguments. Please use \"--help\" to see valid entries.")
            exit(1)       

        for entry in host_dns_entries:
            print(entry)
    
    exit(0)
