#!/bin/bash
set -e
set -x

IMAGE=${1}
test -z "${0}" && (echo "usage: ${0} <image>"; exit 1)

DIR=$(mktemp -p . -d)

# copy
step0=${DIR}/step0.bmp
echo step 0 ${step0}
convert ${IMAGE} ${step0}
chafa ${step0} -f sixel

# vector
stepz=${DIR}/stepz.svg
echo step z ${stepz}
potrace ${step0} --svg -o ${stepz}
chafa ${stepz} -f sixel
