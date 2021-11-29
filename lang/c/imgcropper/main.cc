// CaffeToy :: imgcropper
// (C) 2015 lumin <cdluminate@gmail.com>
// BSD-2-Clause

#include <iostream>
#include <string>

#include <unistd.h>

#include <glog/logging.h>
#include <ImageMagick-6/Magick++.h>

#define USAGE "Usage: imgcroper image.jpg tlx tly brx bry"

using namespace std;
//using namespace Magick;

int main (int argc, char** argv)  
{
	string target_filename;
	int tlx, tly;
	int brx, bry;

	// Init google-glog
	FLAGS_logtostderr = 1;
	google::InitGoogleLogging (argv[0]);
	LOG(INFO) << "Init main()";

	// check argv
	CHECK_EQ(argc, 6) << "missing arguments.\n\n" << USAGE << endl;
	target_filename = string(argv[1]) + ".target.jpg";
	tlx = atoi (argv[2]);
	tly = atoi (argv[3]);
	brx = atoi (argv[4]);
	bry = atoi (argv[5]);
	LOG(INFO) << "Cropping target: x \\in {" << tlx << ","
		<< brx << "}, y \\in {" << tly << "," << bry << "}";

	// read original picture
	LOG(INFO) << "Reading image ...";
	Magick::Image image;
	image.read (argv[1]);
	Magick::Image target = Magick::Image (image);
	LOG(INFO) << "Image size " << image.size().width() << "x"
		<< image.size().height();

	// crop and chop target
	LOG(INFO) << "Chopping and Cropping Image as you wish";
	target.chop (Magick::Geometry (tlx,tly));
	target.crop (Magick::Geometry (brx-tlx,bry-tly));
	
	// then write the target into `target_filename`
	target.write (target_filename);
	LOG(INFO) << "Image file written: " << target_filename;

	LOG(INFO) << "Exit.";
	return 0;
}
