Virtual Memory Subsystem
===
> http://unix.stackexchange.com/questions/196884/making-linux-read-swap-back-into-memory  

# force linux to read swap back to memory
```
swapon -sv # get list
swapoff xxx
```

# vm.swappiness

# vm.page-cluster = 13
13 for 8192 pages, while the default 3 for 8 pages.
