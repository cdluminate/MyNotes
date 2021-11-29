
/* the simplest kernel module */
/*

https://segmentfault.com/a/1190000004448907
https://segmentfault.com/a/1190000004455101

https://wiki.archlinux.org/index.php/Kernel_modules
http://tldp.org/LDP/lkmpg/2.6/html/index.html

 */
/*
   all the functions you can use here are listed at
     $ cat /proc/kallsyms
 */

#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h>

static int __init
init_my_module (void) {
  printk (KERN_INFO "Hello world!\n");
  return 0;
}

static void __exit
exit_my_module (void) {
  printk (KERN_INFO "Bye world!\n");
}

module_init(init_my_module);
module_exit(exit_my_module);

MODULE_LICENSE("MIT");
MODULE_AUTHOR("Anonymous");
