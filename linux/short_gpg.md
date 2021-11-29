short GnuPG use
---
> https://www.gnupg.org, docs

1. generate the key pair `gpg --gen-key`

```Makefile
entropy:
	find / -type f -exec hd '{}' \; > /dev/null
```

2. export keys

* public key `gpg -o filename [--armor] --export keyID`. Note, when `--armor`
is specified the output will be in ASCII format instead of binary format.  

* private key `gpg -o filename [--armor] --export-secret-keys keyID`  

* import keys `gpg --import filename`

3. encryption `gpg -e`, accordingly decryption `gpg -d`, e.g. `gpg -u MY_SECRET_KEY -R RECIPIENT -se file`

4. symmetric encryption `gpg -o filename -c` or `gpg --symmetric`, decryption `gpg -d`

5. download key from keyserver `gpg -keyserver hkp.example.org --recv-key FINGERPRINT`

6. upload key to keyserver `gpg --send-key KEYID`

7. list pub keys `gpg -k`, and `gpg -K` for private keys

8. list signatures `gpg --list-sigs`

9. edit keys `gpg --edit-key KEYID`

10. sign a file  `gpg -u KEYID -s file`

11. verify signature `gpg --verify file`. Note, encrypted file cannot be verified.

12. sign a pub key with your secret key `gpg --sign-key`

13. change configuration of the default key `gpg --default-key`, and use `gpg -u KEYID` to override this config.

14. Encryption recipient `gpg -r name`, or `gpg -R name` (in this case the recipient will be hidden)

NOTE

use `gpg -v`, the verbose flag to debug should gpg fail.
