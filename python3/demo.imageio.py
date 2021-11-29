'''
https://stackoverflow.com/questions/29718238/how-to-read-mp4-video-to-be-processed-by-scikit-image
'''
import pylab
import imageio
import sys

vid = imageio.get_reader(sys.argv[1], 'ffmpeg')
for i, image in enumerate(vid):
    print(image.shape)
    pylab.figure()
    pylab.suptitle(f'image #{i}', fontsize=20)
    pylab.imshow(image)
    pylab.show()
