// CaffeToy :: imgcropper
// (C) 2015 lumin <cdluminate@gmail.com>
// BSD-2-Clause

#include <iostream>
#include <string>

#include <unistd.h>

#include <glog/logging.h>
#include <ImageMagick-6/Magick++.h>

#define USAGE "Usage: imgcroper2 image.jpg ctx cty radius"

using namespace std;
//using namespace Magick;

int main (int argc, char** argv)  
{
	string target_filename;
	int ctx, cty;
	int radius;

	// Init google-glog
	FLAGS_logtostderr = 1;
	google::InitGoogleLogging (argv[0]);
	LOG(INFO) << "Init main()";

	// check argv
	CHECK_EQ(argc, 5) << "missing arguments.\n\n" << USAGE << endl;
	target_filename = string(argv[1]) + ".target.jpg";
	ctx = atoi (argv[2]);
	cty = atoi (argv[3]);
	radius = atoi (argv[4]);
	LOG(INFO) << "Cropping: Centre={" << ctx << ","
		<< cty << "} Radius=" << radius;

	// read original picture
	LOG(INFO) << "Reading image " << argv[1];
	Magick::Image image;
	image.read (argv[1]);
	Magick::Image target = Magick::Image (image);
	LOG(INFO) << "Image size " << image.size().width() << "x"
		<< image.size().height();

	// crop and chop target
	target.chop (
		Magick::Geometry (
			(int)(ctx - radius/2),
			(int)(cty - radius/2)
		)
	);
	target.crop (
		Magick::Geometry (
			(int)(radius),
			(int)(radius)
		)
	);
	
	// then write the target into `target_filename`
	target.write (target_filename);
	LOG(INFO) << "Cropped Image at: " << target_filename;
	
	return 0;
}
