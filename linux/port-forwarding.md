Port forwarding
===

# Via SSH

```
-C compression
-N do not execute remote command
-f go background
-g allow remote hosts to connect to local forwarded ports.
```

```
# Local Forwarding
# Connections to local:6666 will be forwarded to remote:22
ssh -L 6666:remote:22 master@local -fgNC
```

```
# Remote Forwarding
# Connections to remote:6666 will be forwarded to local:22
ssh -R 6666:local:22 root@remote -fgNC
```

# Example

Host A exposed a web service at tcp port 8000. The port is filtered
by the firewall. Our machine host B can access host A via ssh. We
want to map A:8000 to B:8000 via ssh.
```
HostB> ssh -L 8000:localhost:8000 HostA
```
-L listen locally. -R listen remotely. The last two fields in the
argument of -L/-R is processed by the ssh target machine.

# Example 2

https://www.ssh.com/ssh/tunneling/example

In OpenSSH, local port forwarding is configured using the -L option:

```
ssh -L 80:intra.example.com:80 gw.example.com
```

Thilinux: s example opens a connection to the gw.example.com jump server, and forwards any connection to port 80 on the local machine to port 80 on intra.example.com.

In OpenSSH, remote SSH port forwardings are specified using the -R option. For example:

```
ssh -R 8080:localhost:80 public.example.com
```

This allows anyone on the remote server to connect to TCP port 8080 on the
remote server. The connection will then be tunneled back to the client host,
and the client then makes a TCP connection to port 80 on localhost. Any other
host name or IP address could be used instead of localhost to specify the host
to connect to.

# Example: tcp -> unix -> tcp | double forwarding

```
~/Socket $ ssh -gNC -L ./x.sk:localhost:8000 localhost
~/Socket $ ssh -gNC -L 8001:/home/lumin/Socket/x.sk localhost
```

Relative directory won't work.

# troubleshooting

When `ssh -R` always bind the loopback address on the target machine
whatsoever command you typed, check the "GatewayPorts" option of the
sshd config on the target machine.
