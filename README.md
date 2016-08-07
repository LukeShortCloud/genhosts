# GenHosts
* OS: Unix-like and Windows
* Language: Python 2 and 3
* Version: 0.2.1

GenHosts will generate custom hosts files or DNS zones (A records only) based on another host file. 
The primary goal is to provide greater flexibility for redirecting traffic. 
This is useful for redirecting domains to internal servers or blocking malicious websites at the DNS level.

## Install
GenHosts can permanently be installed onto a system using the "install.sh" shell script. By default it will install the "genhosts.py" Python program to "/usr/local/bin/genhosts."
```
# sh install.sh --help
GenHosts installer help options:
        --prefix <prefix>
                Default: /usr/local
        --uninstall [prefix]
# sudo sh install.sh
```

## Help
At a bare minimum, GenHosts requires two options.
(1) The DNS server that the hosts file will be generated for and 
(2) a URL to a downloadable host file. 
This program will parse through the contents of the original hosts file to regenerate or convert it into a new format.
```
# genhosts --help
Usage: genhosts -s {dnsmasq|unbound|unix|windows} <IP address> -u <URL>
-s, --server    specify DNS/hosts server as "dnsmasq", "unbound", "unix", "windows"
-u, --url       provide a list of comma seperated URLs of hosts files
```

### Examples
In this example, a host file will be downloaded from 
"http://example.tld/path/to/hosts.txt" and "http://example2.tld/some/dir/domains.txt". 
It will then create a hosts file designed for dnsmasq that redirects all of the domains to 127.0.0.1 (localhost). 
Finally, standard output is redirected from the terminal to a save file. Otherwise, it will print the file contents to your screen.
```
# genhosts.py -s dnsmasq 127.0.0.1 -u http://example.tld/path/to/hosts.txt,http://example2.tld/some/dir/domains.txt >> dnsmasq_hosts.conf
```

### Developers
Unit tests are provided by the "test_genhosts.py" program. It is run without any arguments. Every method in "genhosts.py" should include a related unit test method in "test_genhosts.py." These test methods are named after the method it's testing but prefixed with "test_." This is outlined below.
```
$ grep "def " genhosts.py | cut -d'(' -f1
    def filedownload
    def validate_ipv4
    def get_hosts
    def gen_hosts
    def exec_threads
$ grep "def test_" test_genhosts.py | cut -d'(' -f1
    def test_get_hosts
    def test_filedownload
    def test_validate_ipv4
```

## License
This software is licensed under the GPLv3. More information about this can be found in the included "LICENSE" file or online at: http://www.gnu.org/licenses/gpl-3.0.en.html
