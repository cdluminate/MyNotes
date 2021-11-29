Emulate other CPUs with QEMU
===

# MIPS

check the supported processors

```
qemu-system-mips -cpu '?'
qemu-system-mips64 -cpu '?'
```

check the supported system architectures

```
qemu-system-mips -M '?'
```

# AMD64

```
qemu-x86_64 -cpu qemu64,-sse4.1,-sse4.2 /usr/bin/chafa
```
