CXX ?= /usr/bin/g++
CXXFLAGS := -g -Wall
LIBS := -lopencv_core -lopencv_highgui -lglog -lMagick++-6.Q16
INCLUDE := -I/usr/include/ImageMagick-6/ -I/usr/include/ImageMagick-6/Magic++/ -I/usr/include/ImageMagick-6/magick/ -I/usr/include/x86_64-linux-gnu/ImageMagick-6/
CONFIG := `pkg-config pkg-config --cflags --libs Magick++`

caffetoy: clean
	$(CXX) $(CXXFLAGS) $(INCLUDE) $(LIBS) $(CONFIG) -o caffetoy caffetoy.cc
#	$(CXX) $(CXXFLAGS) $(INCLUDE) -c caffetoy.cc -o caffetoy.cc.o 
#	$(CXX) $(CXXFLAGS) $(INCLUDE) caffetoy.cc.o $(LIBS) -o caffetoy 

clean:
	-$(RM) *.o caffetoy Frame.jpg
