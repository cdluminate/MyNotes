Restrict connections with Iptables
---

> https://debian-administration.org/article/187/Using_iptables_to_rate-limit_incoming_connections  

limit incoming connections to port 22 to no more than 3 attemps in a minite:
```
iptables -I INPUT -p tcp --dport 22 -i eth0 -m state --state NEW -m recent --set
iptables -I INPUT -p tcp --dport 22 -i eth0 -m state --state NEW -m recent --update --seconds 60 --hitcount 4 -j DROP
```
