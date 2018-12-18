# linker
Docker Network Driver Plugin

# Test case
Given:
 - parent interface name = "eno1"
 - interface IP = "192.168.0.151/24"
 - gateway = "192.168.0.1" 
start linker.py
docker network create -d linker --subnet 192.168.0.0/24 mynet
docker run -ti --rm --network mynet --ip 192.168.0.151 alpine /bin/sh
