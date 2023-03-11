#!/bin/bash
iptables -I OUTPUT -m owner --gid-owner no-internet -s 0/0 -d 0/0 -j DROP
iptables -I INPUT -m owner --gid-owner no-internet -s 0/0 -d 0/0 -j DROP
read -p "Press [Enter] key to allow internet again"
iptables -D OUTPUT 1
iptables -D INPUT 1
