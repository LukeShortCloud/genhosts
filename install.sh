#!/bin/bash

PREFIX="/usr/local"

if [[ "$1" == "--help" ]]
    then echo -e "GenHosts installer help options:"
    echo -e "\t--prefix <prefix>"
    echo -e "\t\tDefault: /usr/local"
    echo -e "\t--uninstall [prefix]"
    exit 0
elif [[ "$1" == "--prefix" ]]
    then PREFIX="$2"
elif [[ "$1" == "--uninstall" ]]
   
     then if [[ "$2" == "" ]]
        then PREFIX="$2"
        echo PASS
    fi

    uninstall_genhosts
    exit 0

fi

install_genhosts
exit 0

install_genhosts() {
    cp ./genhosts.py ${PREFIX}/bin/genhosts
    chmod 755 ${PREFIX}/bin/genhosts
}

uninstall_genhosts() {
    rm -f ${PREFIX}/bin/genhosts
}
