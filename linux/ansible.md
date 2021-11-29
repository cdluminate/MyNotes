Ansible
=======

Can be used as a parallel ssh client.

```
ssh-keygen
ssh-copy-id root@192.168.1.1  # distribute keys

export ANSIBLE_INVENTORY=~/blades.txt

ansible all -m ping # OR: ansible all -i blades.txt -m ping
ansible all -u root -m shell -a uptime
ansible all -u root -m command -a 'chdir=/root ls'
ansible all -u root -m copy -a "src=blades.txt dest=/root/blades.txt"
ansible all -u root -m file -a 'path=/data/app state=directory'
ansible all -u root -m fetch -a 'src=/data/hello dest=/data'  
ansible web -m service -a 'name=nginx state=started enabled=true'
ansible web -m script -a '/tmp/df.sh'
ansible web -m setup -a 'filter="*mem*"'
ansible all -i blades.txt -m replace -a 'path=/etc/apt/sources.list regexp=stretch replace=buster'

# add -o for condensed output
```
