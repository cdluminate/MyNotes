Local DNS caching with DNSMASQ
===

# apt-get install dnsmasq

# configure
Keep in mind that NetworkManager may override your resolv.conf.
```
vim /etc/dnsmasq.conf
	+ resolv-file=/etc/???upstream-of-dnsmasq.conf
	+ listen..
	+ port
	+ ... (this configuration file is well-documented)
vim /etc/???upstream-of-dnsmasq.conf
	+ nameserver 8.8.8.8
	+ nameserver 8.8.4.4
	+ nameserver 2001:4860:4860::8888

vim /etc/resolv.conf
	nameserver 127.0.0.1
	nameserver ::1
```

# systemctl restart dnsmasq

# Troubleshooting

### WHAT if dnsmasq faild to start ?
```
/sbin/dnsmasq --test
```
then check the error message.

# reference
see archwiki, debianwiki.
