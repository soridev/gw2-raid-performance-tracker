#!/bin/bash

while getopts "u:" opt; do
    case $opt in
        u) 
            given_user="$OPTARG"
            ;;
        *)
            echo "invalid command: no parameter included with argument $OPTARG"
            ;;
    esac
done

shift "$(( OPTIND - 1 ))"

if [ -z "$given_user" ]; then
        echo 'Missing user parameter -u' >&2
        exit 1
fi

# those dirs are required for the app to work
required_dirs=("/var/load/cbtlogs/uncategorized" "/var/load/cbtlogs/out" "/var/load/cbtlogs/archive" "/opt/GW2EI" "/var/postgres/gw2-raid-performance-tracker/data" "/var/backups/postgres")

# create dirs if not exists. Sets owner and permissions
for i in "${required_dirs[@]}"
do
    if [[ ! -e $i ]]; then
        mkdir $i
        chown $given_user:$given_user $i
        echo "created dir: $i and set owner to: $given_user"
    elif [[ ! -d $i ]]; then
        echo "$i already exists but is not a directory" 1>&2
    fi
done
