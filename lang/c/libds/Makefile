CXX=g++-6
CXXFLAGS=-Wall -Wpedantic -g
main:
	$(CXX) $(CXXFLAGS) ds.hpp -c -o ds.o
	$(CXX) $(CXXFLAGS) test_ds.cc -o test_ds
	./test_ds
dox:
	doxygen
clean:
	-$(RM) -rf doxygen
	-$(RM) test_ds ds.o
