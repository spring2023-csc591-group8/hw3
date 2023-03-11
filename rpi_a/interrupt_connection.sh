#!/bin/bash
iptables -I OUTPUT -m tcp -p tcp --dport 1883 -j DROP
netstat | grep 1883 | awk '{print substr($4, index($4, ":") + 1)}' | xargs -I dest_port iptables -I INPUT -m tcp -p tcp --dport dest_port -j DROP
iptables -L OUTPUT
iptables -L INPUT
read -p "Press [Enter] key to allow internet again"
iptables -D OUTPUT 1
iptables -D INPUT 1
