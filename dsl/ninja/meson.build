project('tutorial', 'c')
blas = dependency('blas')
executable('hello', 'hello.c', dependencies: blas)
shared_library('libhello', 'libhello.c', 'libhello.h')
message(run_command(['find', '.']).stdout())
#shared_library('libhello', run_command(
#	['find', '.', '-type', 'f', '-name', 'libhello*', '']).stdout().strip().split('\n'))
#	meson doesn't support source globbing
