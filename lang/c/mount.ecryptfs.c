/*

 A Sloppy Setuid Ecryptfs Wrapper

 Copyright (C) 2016 Zhou Mo <cdluminate@gmail.com>
 License: MIT License (Expat)

 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/*

Example:

$ gcc -Wall mount.ecryptfs.c -o mount.ecryptfs
$ sudo chmod u+s mount.ecryptfs
$ sudo chown root:root mount.ecryptfs
$ ./mount.ecryptfs t test test                  # OK
$ ./mount.ecryptfs u test                       # umount

 */

void
Usage (const char * progname)
{
  printf("Usage:\n\
  %s\n\
    t <SRCDST>           -- Mount SRC to DST, s+e Test\n\
    e <SRCDST>           -- Mount SRC to DST, Enhanced\n\
    s <SRCDST>           -- Mount SRC to DST by Shortcut\n\
    p <SRC> <DST>        -- Mount SRC to DST\n\
    u <DST>              -- Umount DST\n",
  progname);
  return;
}

void
wrap_umount (char * dst, char ** envp)
{
  printf ("umount %s\n", dst);
  setuid(geteuid());
  char * umount_ecryptfs_argv[] = { "umount", dst, NULL };
  execve ("/bin/umount", umount_ecryptfs_argv, envp);
  return;
}

void
wrap_plain_mount (char * src, char * dst, char ** envp)
{
  printf ("mount -t ecryptfs %s %s\n", src, dst);
  setuid(geteuid());
  char * mount_ecryptfs_argv[] = {
      "mount", "-t", "ecryptfs", src, dst, NULL
  };
  execve ("/bin/mount", mount_ecryptfs_argv, envp);
  return;
}

void
wrap_shortcut_mount (char * srcdst, char ** envp)
{
  printf ("mount -t ecryptfs -o *** %s %s\n", srcdst, srcdst);
  setuid(geteuid());
  char * shortcut_opt=""
"key=passphrase,ecryptfs_cipher=aes,ecryptfs_key_bytes=16,"
"ecryptfs_passthrough=n,ecryptfs_enable_filename_crypto=n,no_sig_cache";
  char * mount_ecryptfs_argv[] = {
      "mount", "-t", "ecryptfs", srcdst, srcdst, "-o", shortcut_opt, NULL
  };
  execve ("/bin/mount", mount_ecryptfs_argv, envp);
  return;
}

void
wrap_shortcut_enhanced (char * srcdst, char ** envp)
{
  printf ("mount -t ecryptfs -o *** %s %s\n", srcdst, srcdst);
  setuid(geteuid());
  char * shortcut_opt = ""
"key=passphrase,ecryptfs_cipher=aes,ecryptfs_key_bytes=16,"
"ecryptfs_passthrough=n,ecryptfs_enable_filename_crypto=y,no_sig_cache";
  char * mount_ecryptfs_argv[] = {
      "mount", "-t", "ecryptfs", srcdst, srcdst, "-o", shortcut_opt, NULL
  };
  execve ("/bin/mount", mount_ecryptfs_argv, envp);
  return;
}

void
wrap_shortcut_enhanced_test (char * srcdst, char ** envp)
{
  printf ("mount -t ecryptfs -o *** %s %s\n", srcdst, srcdst);
  setuid(geteuid());
  char * shortcut_opt = ""
"key=passphrase,ecryptfs_cipher=aes,ecryptfs_key_bytes=16,"
"ecryptfs_passthrough=n,ecryptfs_enable_filename_crypto=y,no_sig_cache,"
"ecryptfs_fnek_sig=d395309aaad4de06"; // f("test") = d395309aaad4de06
  char * mount_ecryptfs_argv[] = {
      "mount", "-t", "ecryptfs", srcdst, srcdst, "-o", shortcut_opt, NULL
  };
  execve ("/bin/mount", mount_ecryptfs_argv, envp);
  return;
}

int
main (int argc, char ** argv, char ** envp)
{
  // Must specify action
  if (argc < 2) {
    printf ("E: Missing Action.\n");
    Usage (argv[0]);
    return 1;
  }
  // Select action and jump.
  switch (argv[1][0]) {
  case 'u': // umount
    if (argc != 3) {
      printf ("E: Argument List Error.\n");
      return 2;
    }
    printf ("* Select UMOUNT\n");
    wrap_umount(argv[2], envp);
    break;
  case 'p': // plain mount
    if (argc != 4) {
      printf ("E: Argument List Error.\n");
      return 4;
    }
    printf ("* Select PLAIN MOUNT\n");
    wrap_plain_mount (argv[2], argv[3], envp);
    break;
  case 's': // shortcut mount
    if (argc != 3) {
      printf ("E: Argument List Error.\n");
      return 8;
    }
    printf ("* Select SHORTCUT MOUNT\n");
    wrap_shortcut_mount (argv[2], envp);
    break;
  case 'e': // enhanced shortcut mount
    if (argc != 3) {
      printf ("E: Argument List Error.\n");
      return 16;
    }
    printf ("* Select SHORTCUT MOUNT\n");
    wrap_shortcut_enhanced (argv[2], envp);
    break;
  case 't': // enhanced shortcut mount test
    if (argc != 3) {
      printf ("E: Argument List Error.\n");
      return 32;
    }
    printf ("* Select SHORTCUT MOUNT TEST\n");
    wrap_shortcut_enhanced_test (argv[2], envp);
    break;
  default:
    Usage (argv[0]);
    return 64;
  } // switch argv[1][1]
  return 0;
}
