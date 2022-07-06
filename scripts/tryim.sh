#!/bin/bash
set -e

IMAGE=${1}
test -z "${0}" && (echo "usage: ${0} <image>"; exit 1)

DIR=$(mktemp -p . -d)

# copy
step0=${DIR}/step0.png
echo step 0 ${step0}
convert ${IMAGE} ${step0}
chafa ${step0} -f sixel

# resize
step1=${DIR}/step1.png
echo step 1 ${step1}
convert ${step0} -blur 0x4 ${step1} 
chafa ${step1} -f sixel

# blur
step2=${DIR}/step2.png
echo step 2 ${step2}
convert ${step1} -sharpen 0x4 ${step2}
chafa ${step2} -f sixel

# vector
stepz=${DIR}/stepz.svg
echo step z ${stepz}
vtracer --input ${step2} \
    -f16 -m polygon --hierarchical cutout \
    --output ${stepz}
chafa ${stepz} -f sixel
