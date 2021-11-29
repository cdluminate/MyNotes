/* dlopen demo
  @ref dlopen(3)
  @compile cc *.c -ldl
 */

#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <gnu/lib-names.h> // for LIBM_SO
#include <link.h>

int
main(void)
{
  void * handle;
  double (*cosine)(double);
  char * error;
  Dl_info dl_info;
  struct link_map * l_map = malloc(sizeof(struct link_map));

  // open and mmap the libm.so
  handle = dlopen(LIBM_SO, RTLD_LAZY);
  if (!handle) {
    fprintf(stderr, "%s\n", dlerror());
    exit(EXIT_FAILURE);
  }
  dlerror(); // flush error state

  // dump the information of opened libm.so
  if (dlinfo(handle, RTLD_DI_LINKMAP, &l_map) ) {
    fprintf(stderr, "%s\n", dlerror());
    exit(EXIT_FAILURE);
  } else {
    fprintf(stdout, "dlinfo: l_addr: 0x%lx\n", l_map->l_addr);
    fprintf(stdout, "dlinfo: l_name: %s\n", l_map->l_name);
    fprintf(stdout, "dlinfo: l_ld  : %p\n", l_map->l_ld);
    fprintf(stdout, "dlinfo: l_next: %p\n", l_map->l_next);
    fprintf(stdout, "dlinfo: l_prev: %p\n", l_map->l_prev);
  }

  // load the cosine symbol
  cosine = (double (*)(double)) dlsym(handle, "cos");
  if (! dladdr( (void *)cosine, &dl_info) ) {
    fprintf(stderr, "Error getting dl_info\n");
  } else {
    fprintf(stdout, "Opened cosine function @%p\n", (void *)cosine);
    fprintf(stdout, "  offset to l_addr -> @%p\n", (void *)cosine - l_map->l_addr);

    fprintf(stdout, "dladdr: dli_fname: %s\n", dl_info.dli_fname);
    fprintf(stdout, "dladdr: dli_fbase: %p\n", dl_info.dli_fbase);
    fprintf(stdout, "dladdr: dli_sname: %s\n", dl_info.dli_sname);
    fprintf(stdout, "dladdr: dli_saddr: %p\n", dl_info.dli_saddr);
  }
  
  error = dlerror();
  if (error != NULL) {
    fprintf(stderr, "%s\n", error);
    exit(EXIT_FAILURE);
  }

  printf("%f\n", (*cosine)(2.0));
  dlclose(handle);
  return 0;
}
