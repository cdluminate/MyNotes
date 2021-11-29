CXX ?= /usr/bin/g++
CXXFLAGS := -g -Wall
INCLUDE := -I/usr/include/ImageMagick-6/ -I/usr/include/ImageMagick-6/Magic++/ -I/usr/include/ImageMagick-6/magick/ -I/usr/include/x86_64-linux-gnu/ImageMagick-6/
LIBS := -lglog -lMagick++-6.Q16
CONFIG := `pkg-config pkg-config --cflags --libs Magick++`
# CONFIG := -fopenmp -DMAGICKCORE_HDRI_ENABLE=0 -DMAGICKCORE_QUANTUM_DEPTH=16 -fopenmp -DMAGICKCORE_HDRI_ENABLE=0 -DMAGICKCORE_QUANTUM_DEPTH=16 -fopenmp -DMAGICKCORE_HDRI_ENABLE=0 -DMAGICKCORE_QUANTUM_DEPTH=16 -I/usr/include/x86_64-linux-gnu//ImageMagick-6 -I/usr/include/ImageMagick-6 -I/usr/include/x86_64-linux-gnu//ImageMagick-6 -I/usr/include/ImageMagick-6 -I/usr/include/x86_64-linux-gnu//ImageMagick-6 -I/usr/include/ImageMagick-6 -lMagick++-6.Q16 -lMagickWand-6.Q16 -lMagickCore-6.Q16

caffetoy: clean
	$(CXX) $(CXXFLAGS) $(LIBS) $(CONFIG) $(INCLUDE) -o imgcropper main.cc
	$(CXX) $(CXXFLAGS) $(LIBS) $(CONFIG) $(INCLUDE) -o imgcropper2 main2.cc

clean:
	-$(RM) *.o imgcropper imgcropper2
