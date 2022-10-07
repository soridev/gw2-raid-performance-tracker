# those dirs are required for the app to work
required_dirs=("/var/load/cbtlogs/uncategorized" "/var/load/cbtlogs/out" "/var/load/cbtlogs/archive" "/opt/GW2EI")

# create dirs if not exists. Sets owner and permissions
for i in "${required_dirs[@]}"
do
    if [[ ! -e $i ]]; then
        mkdir $i
        chown $USER:$USER  $i
        echo "created dir: $i and set owner to: $USER"
    elif [[ ! -d $i ]]; then
        echo "$i already exists but is not a directory" 1>&2
    fi
done
