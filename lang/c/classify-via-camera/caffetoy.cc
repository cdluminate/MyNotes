// CaffeToy
// (C) 2015 lumin <cdluminate@gmail.com>
// BSD-2-Clause
#include <iostream>

#include <unistd.h>

#include <glog/logging.h>
#include <opencv2/opencv.hpp>
#include <Magick++.h>

#define WINDOW "CaffeToy"

//using namespace std;
//using namespace cv;
//using namespace Magick;

int main (int argc, char** argv)  
{
	std::cout << "\x1b[31m\x1b[m";
	// Init google-glog
	FLAGS_logtostderr = 1;
	google::InitGoogleLogging (argv[0]);
	LOG(INFO) << "Welcome to CaffeToy";

	IplImage* pFrame = NULL;  
	Magick::Image image;
	Magick::Geometry geom = Magick::Geometry (227, 227);
	geom.aspect(1);

	LOG(INFO) << "Create Camera Capture";
	CvCapture* pCapture = cvCreateCameraCapture(-1);  
	CHECK (pCapture != NULL) << "cvCreateCameraCapture [failed]";

	//cvSetCaptureProperty (pCapture, CV_CAP_PROP_FPS, 1);

	LOG(INFO) << "Creating named window";
	cvNamedWindow(WINDOW, 1);  
	
	LOG(INFO) << "Showing Images";
	while( NULL != (pFrame = cvQueryFrame (pCapture)) )  
	//while (1)
	{
		system ("clear");
		//cvGrabFrame (pCapture);
		//pFrame = cvRetrieveFrame (pCapture);
		if (!pFrame) break;  
		LOG(INFO) << "cvQueryFrame [OK]";
		cvShowImage (WINDOW, pFrame);  
		cvSaveImage ("Frame.jpg", pFrame);

		//system ("avconv -i Frame.jpg -s 227x227 Frame.jpg");
		//sync();
		image.read ("./Frame.jpg");
		image.zoom (geom);
		image.write ("./Frame.jpg");
		LOG(INFO) << "Resize picture with Magick++ [OK]";
		sync();
		LOG(INFO) << "Sync captured Image [OK]";

		LOG(INFO) << "Classify resized frame";
		// the program is from caffe source / examples / cpp-classification
		system ("classification m/deploy.prototxt m/bvlc_reference_caffenet.caffemodel m/imagenet_mean.binaryproto m/synset_words.txt Frame.jpg");

		// reset capture
		LOG(INFO) << "Releasing capture";
		cvReleaseCapture (&pCapture);  
		LOG(INFO) << "Create Camera Capture";
		pCapture = cvCreateCameraCapture(-1);  
		CHECK (pCapture != NULL) << "cvCreateCameraCapture [failed]";

		std::cout << "\x1b[31m----------------------------------------------\x1b[m"
			<< std::endl;
		// wait for any key to trigger next time classification
		// ESC for exit.
		if ( 27 == (char)cvWaitKey(0)) {
			LOG(INFO) << "ESC arrived. Exiting ...";
			break;
		}
	}  
	cvReleaseCapture (&pCapture);  
	cvDestroyWindow (WINDOW);  
	LOG(INFO) << "Release Memory [OK]";
}
