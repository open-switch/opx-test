#!/bin/bash

cmd=$(traceroute -f 1 -m 1 8.8.8.8 | awk '{print $2}'| grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
cmd1=$(ip route show | grep $cmd|grep -oP '(?<=src).*'| awk '{print $1}')
echo $cmd1
