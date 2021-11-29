UFW
===

## install

```
sudo apt install ufw gufw
```

## simple configuration

```
sudo ufw enable
sudo ufw default deny
sudo ufw status verbose
sudo ufw show raw
sudo ufw allow ssh
sudo ufw allow 22
sudo ufw allow http
```

See ufw(8) for detail.

```
systemctl enable ufw
```
