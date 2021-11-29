Center Server

```
root@VM-0-9-debian:/etc/wireguard# cat cafe.conf 
[Interface]
PrivateKey = 8PD5THSPeG/zIDq+xh5Qcpx+YaHDv5aCGGXrtVyVVUA=
ListenPort = 22022
Address = cafe::e/64, cafe::/64

[Peer]
PublicKey = mKUEmvBG/6wNKuOkp3vLEO4soE8+rsLNCvKKmXc5Gg0=
AllowedIPs = cafe::10/128

[Peer]
PublicKey = ag0OdhD3gAfqS00oNHtlSKEw6V4iJ5H23bC1fQwyryg=
AllowedIPs = cafe::a/128

[Peer]
PublicKey = L+DFrT11KYxM6gmmWHvfMD8XB198uJc/votYzRmykQE=
AllowedIPs = cafe::20/128

[Peer]
PublicKey = 6TCqBYSfaoXxG98YmdMDUmfX+gzYlJ3a28DKOPcYdFc=
AllowedIPs = cafe::10:184:17:13/128

[Peer]
PublicKey = zTrhZmxZ3P6nqsonfbiKd3nc93fv5lSWWR7EMGaed3c=
AllowedIPs = cafe::10:184:17:30/128

[Peer]
PublicKey = RkXEBEl5MqkdQLOtU9megfFm9Thf/hZgfiLCzN2+Aik=
AllowedIPs = cafe::58:206:101:18/128

```


Leaf Node

```
[Interface]
Address = cafe::58:206:101:18/64
PrivateKey = GJRvgkjnLGbXhnGIdnKVYnqfmuPRcIZsS/A7rHOdW1w=

[Peer]
PublicKey = wRQbtL0ao16Fvc7ME33AVtolBr/B3zPGJxVZQ3L/LGE=
Endpoint = 42.192.50.99:22022
AllowedIPs = ::/0
PersistentKeepalive = 5
```
