#!/bin/sh
set -x -e

SEQ=$(seq -w 0 100);
for I in $SEQ; do
  sed -e "1a const C=${I}/100.0+0.0im" -e '2d' \
      -e '6a const samples = 640' -e '7d' \
      ljrjulia.jl > tmp.jl
  julia tmp.jl
  pnmtopng julia.pgm > frame_$I.png
done
rm *.pgm
rm tmp.jl

ffmpeg -f image2 -framerate 7 -i frame_%03d.png -s 1000x1000 tmp.avi
ffmpeg -i tmp.avi -vcodec h264 demo.mp4
rm *.png
rm tmp.avi
