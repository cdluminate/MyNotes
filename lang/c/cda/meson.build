project('cda', 'c')

cc = meson.get_compiler('c')

cda_srcs = '''
cda.c
cda.h
lumin_log.h
'''.strip().split('\n')

deps = dependency('libarchive')  # through pkg-config

executable('cda', sources: cda_srcs, dependencies: deps)
