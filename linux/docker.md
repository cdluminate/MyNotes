Docker.io
===

https://docs.docker.com/get-started

https://docs.docker.com/install/linux/docker-ce/debian/

# installation

There is official Debian package for `docker.io`.  
```
apt install docker.io
adduser $USER docker     # grant the docker group permission to avoid sudo
```

Test docker installation
```
docker run hello-world
```

# use a mirror

For systemd-based systems, edit `/etc/docker/daemon.json`

```
{
  "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn/"]
}
```

# docker image preparation by oneself

1. Setup a basic system via debootstrap
```
$ debootstrap jessie ./jessie http://127.0.0.1/debian
$ cd ./jessie
$ tar zcvf ../jessie.stage3.tar.gz .
```
alternatively, one can download archlinux bootstrap tarball or gentoo
stage3 tarball or something else in favour of other distributions.

2. import it into docker
```
$ cat jessie.stage3.tar | sudo docker import - jessie:19700101
```

# import docker image from docker
```
$ docker search alpine
$ docker pull alpine
```

# docker run

* Hello world test
```
$ sudo docker run ubuntu:14.04 /bin/echo "Hello World!"
```

* Call a shell from container.
```
$ sudo docker run -t -i ubuntu:14.04 /bin/bash
```

* re-enter a previously created container
```
docker ps -as                 # show all containers
docker start -ai 01234567     # container ID
```

* save a session as an image `docker commit ID NAME`

# deletion
```
docker ps -as # list containers
docker rm 1234567 # remove container
docker images -a # list images
docker rmi 1234567 # remove image
```

# Deploy archlinux containers and expose ssh port to the wild
```
docker run -t -i archlinux:20161001 /bin/bash
(docker)# echo 'root:toor' | chpasswd
(docker)# pacman -S openssh
(docker)# /usr/bin/sshd -D # make sure it works
docker commit 01234567 archlinux:ssh

docker run -d -p 22:22 archlinux:ssh /usr/bin/sshd -D
OR
docker run -d -P archlinux:ssh /usr/bin/sshd -D # choose random port mapping
```

# Change docker image storage path

```
sudo vim /etc/docker/daemon.json
  {
      "graph": "/my-docker-images"
  }
```

When the storage driver is ZFS, docker will automatically utilize the ZFS
filesystem functionalities, such as snapshots.

# Use GPU within containers

The container driver version must be identical to that of the host machine.
For example, when the host driver version is 375.26, you must install 375.26
in the container or it will not work.

```
$ nvidia-smi 
Failed to initialize NVML: Driver/library version mismatch
```

We first bind the nvidia devices from the host to the container when running
an container:

```
docker run -d -p6666:22 \
  --device=/dev/nvidia0:/dev/nvidia0 \
  --device=/dev/nvidiactl:/dev/nvidiactl \
  --device=/dev/nvidia-modeset:/dev/nvidia-modeset \
  --device=/dev/nvidia-uvm:/dev/nvidia-uvm \
  --device=/dev/nvidia-uvm-tools:/dev/nvidia-uvm-tools
```

Download and copy the driver into the container and install it without kernel modules.

```
docker cp NVIDIA-Linux-x86_64-375.26.run ded2cbfcc208:/root/
(container): sudo sh NVIDIA-Linux-x86_64-375.26.run --no-kernel-module
```

test wether it works correctly

```
(container): nvidia-smi
```

reference: https://github.com/NVIDIA/nvidia-docker/wiki/NVIDIA-driver
reference: https://stackoverflow.com/questions/25185405/using-gpu-from-a-docker-container

# Remove all the containers with a single line

```
docker ps -a -q | xargs docker rm

docker system prune
```
