#!/bin/sh
PHOTOPATH=/tmp/t/
find ${PHOTOPATH} -type f -name '*.jpg' -exec classification m/deploy.prototxt m/bvlc_reference_caffenet.caffemodel m/imagenet_mean.binaryproto m/synset_words.txt '{}' \;
