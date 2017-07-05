#!/bin/bash

FILENAME="/etc/quagga/Quagga.conf"
routeCount=0
max_routes=500

exec 3>>$FILENAME

while [ $routeCount -le $max_routes ]; do
    
    octet1=$((( 98 % 100 ) + 1 ))
    if [ "$octet1" -eq 127 ]
        then
            continue
    fi
    octet2=0
    while [ $octet2 -le 255 ]; do
        octet3=0
        let octet2=octet2+1
        while [ $octet3 -le 255 ]; do
            echo "network $octet1.$octet2.$octet3.0/24" >&3
            let octet3=octet3+1
            let routeCount=routeCount+1
            if [ "$routeCount" -eq "$max_routes" ]; then
                exit
            fi
        done
    done

done

exec 3>>&-