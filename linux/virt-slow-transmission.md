virt-slow-transmission
---

This is due to inproper network adapter configuration.
By default virtualbox attaches default network adapter
to `NAT` and the adapter type (advanced) is
`Intel PRO/1000MT (82540EM)`. Switching the adapter
type from it to something else solves this issue,
e.g. `Paravirtualized Network (virtio-net)`.

P.S. virtualbox guest is able to ping host IP's, and
one can assign an private IP to host's loop device by
`ip addr add 192.168.0.1 dev loop`, and then communicate
with host by that IP.
