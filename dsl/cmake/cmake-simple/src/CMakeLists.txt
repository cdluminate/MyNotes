set (libsrcs b.cc c.cc)
set (utilsrcs a.cc)

add_library (b SHARED ${libsrcs}) # static or shared
add_executable (a ${utilsrcs})     # elf name + source

add_library (b1 SHARED ${libsrcs})
set_property (TARGET b1 PROPERTY INTERFACE_POSITION_INDEPENDENT_CODE ON)

target_link_libraries (a b)
