FFmpeg
======

Converting Video and Audio, using 'avconv' or 'ffmpeg'

print supported codecs and formats
----------------------------------

::

    avconv -formats
    avconv -codecs

print the media file's information
----------------------------------

::

    avconv -i <media.file>

converting videos
-----------------

::

    e.g. convert avi to mp4(x264):
    avconv -i <media.file> -vcodec libx264 -acodec ac3 <output.file>
        where 'vcodec' specifies the codec of video stream, 'acodec' specifies audio codec.

convertion between video and image
----------------------------------

::

    avconv -i foo.avi -r 1 -s WxH -f image2 foo-%05d.png
    -r 1  :  1 frame per sec.
    WxH   : e.g. 1920x1080

resize a picture
----------------

::

    avconv -i fox.jpg -s 64x64 fox_resized.jpg

    ref: man avconv section << Video and Audio file format conversion >>
    http://ffmpeg.org/ffmpeg.html#Video-and-Audio-file-format-conversion

ffmpeg\_resize\_picture.txt
---------------------------

::

    ffmpeg -i input.jpg -vf scale-1920:1080 output.jpg
    https://trac.ffmpeg.org/wiki/Scaling%20(resizing)%20with%20ffmpeg

reference
---------

avconv(1)
