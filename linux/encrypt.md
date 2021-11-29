# Encrypt a file

https://stackoverflow.com/questions/16056135/how-to-use-openssl-to-encrypt-decrypt-files/31552829#31552829


OpenSSL
```
openssl enc -aes-256-cbc -in raw.data -out encrypted.data
openssl enc -d -aes-256-cbc -in encrypted.data -out raw.data
```

GPG
```
gpg --output encrypted.data --symmetric --cipher-algo AES256 raw.data
gpg --output raw.data --decrypt encrypted.data
```
