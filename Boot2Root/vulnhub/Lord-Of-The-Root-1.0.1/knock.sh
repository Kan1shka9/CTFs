#!/bin/sh
HOST=$1
shift
for ARG in "$@" ; do
nmap -PN --host_timeout 201 --max-retries 0 -p $ARG $HOST
done

# Usage root@kali:~# ./knock.sh 192.168.124.138 1 2 3
