Gitlab notes
===

1. download .deb file from gitlab.com  
2. dpkg -i gitlab-ce_*.deb  
3. vim /etc/gitlab/gitlab.rb  
4. gitlab-ctl reconfigure  
5. gitlab-ctl restart
6. start your browser
7. login with the default account `root`, with password `5iveL!fe`.`.
Note, with respect to gitlab-ce with version higher than `8.7.0`,
when the first time you visit the index page you are asked to
enter new password for `root` account directly, and there is
no need to memorize the `5iveL!fe` password.  

# Change domain after installation

Tested on gitlab-ce 10.6.4 omnibus

```
vim /etc/gitlab/gitlab.rb
 # change the hostname
gitlab-ctl reconfigure
gitlab-ctl restart
```

# Gitlab Backup

First make sure that your gitlab service is running. Then
```
$ sudo gitlab-ctl start
[ make sure gitlab is running ]
$ sudo gitlab-rake gitlab:backup:create
$ sudo ls /var/opt/gitlab/backups/
```

# Gitlab Restore

> localhost/help/raketasks/backup_restore.md  

Fist copy backup archive to backup directory
```
sudo cp 1393513186_gitlab_backup.tar /var/opt/gitlab/backups/
sudo chown git:git that_archive.tar
```

Stop database clients
```
sudo gitlab-ctl stop unicorn
sudo gitlab-ctl stop sidekiq
# Verify
sudo gitlab-ctl status
```

Overwrite the whole gitlab database
```
sudo gitlab-rake gitlab:backup:restore BACKUP=1393513186
```

Check and fix problems
```
sudo gitlab-ctl reconfigure # different from official document
sudo gitlab-ctl start
sudo gitlab-rake gitlab:check SANITIZE=true
```

Note, check log for debugging. `/var/log/gitlab/gitlab-rails/production.log`  

Note, for gitlab version `8.9.6` there is a bug where a restored gitlab
instance returns 500 (`OpenSSL::Cipher::CipherError`) when you are accessing any old data.
See https://www.unixhot.com/article/53 and https://gitlab.com/gitlab-org/gitlab-ce/issues/19073#note_12712670  

# Gitlab Docker Image

https://docs.gitlab.com/omnibus/docker/

# How to reset root password?

```
GITLAB_SERVER/help/security/reset_root_password.md
```

### Troubleshot

#### freeze on xx\_redis\_sleep
Start an instance of /opt/gitlab/embedded/bin/runsvdir-start, then
reconfigure. or start service gitlab-runsvdir.service

#### How to disable "sign up" for accounts ?
For gitlab 8.3.2, login with admin account, then find related settings
in admin area.

#### Reference
1. Gitlab official doc
2. archwiki gitlab

### See Also

Gogs -- gitlab alternative
