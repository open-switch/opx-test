#!/bin/bash

URL="http://dell-networking.bintray.com/opx-images/opx-onie-installer_1.1_amd64.bin"
#output="`/usr/bin/wget -O - ${URL}` | ssh  -t -o StrictHostKeyChecking=no root@10.11.136.32 'cat >/tmp/filename'"
result=$(wget -O - http://dell-networking.bintray.com/opx-images/opx-onie-installer_1.1_amd64.bin | ssh -o StrictHostKeyChecking=no root@10.11.136.32 2>&1 'cat >/tmp/opx-onie-installer_1.1_amd64.bin') 2>&1
echo "${result}"
#if [ $result ]
#then
#  echo "Success"
#else
#  echo "FAIL"
#fi
