Gitea
===

### https with self-signed cert

1. create certs

```
./gitea cert --host mysite.com
```

2. edit `custom/conf/app.ini` (https://docs.gitea.io/en-us/https-setup/)

```
[server]
PROTOCOL  = https
ROOT_URL  = https://git.example.com:3000/
HTTP_PORT = 3000
CERT_FILE = cert.pem
KEY_FILE  = key.pem
```

Note, the `cert.pm` and `key.pem` are relative paths. You can use absolute
paths. (https://github.com/go-gitea/gitea/issues/14401)
