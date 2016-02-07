# GenHosts
* OS: Unix-like and Windows
* Language: Python 2 and 3
* Version: 0.2.0

GenHosts will generate custom hosts files or DNS zones (A records only) based on another host file. 
The primary goal is to provide greater flexibility for redirecting traffic. 
This is useful for redirecting domains to internal servers or blocking malicious websites at the DNS level.

## Help
At a bare minimum, GenHosts requires two options.
(1) The DNS server that the hosts file will be generated for and 
(2) a URL to a downloadable host file. 
This program will parse through the contents of the original hosts file to regenerate or convert it into a new format.
```
# genhosts.py --help
```

### Examples
In this example, a host file will be downloaded from 
"http://example.tld/path/to/hosts.txt" and "http://example2.tld/some/dir/domains.txt". 
It will then create a hosts file designed for dnsmasq that redirects all of the domains to 127.0.0.1 (localhost). 
Finally, standard output is redirected to a file to save to. Otherwise it will print the file contents to your screen.
```
# genhosts.py -s dnsmasq 127.0.0.1 -u http://example.tld/path/to/hosts.txt,http://example2.tld/some/dir/domains.txt >> dnsmasq_hosts.conf
```

## License
This software is licensed under the GPLv3. More information about this can be found in the included "LICENSE" file or online at: http://www.gnu.org/licenses/gpl-3.0.en.html
