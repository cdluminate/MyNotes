#!/bin/bash
set -e

if ! command -v vtracer; then
    echo please download vtracer and put it under $$PATH
    exit 1
fi

sp='/-\|'
DIR=${1}
PNGS=( $(find ${DIR} -type f -name '*.png') )
for PNG in ${PNGS[@]}; do
    printf '\b%.1s' "$sp"; sp=${sp#?}${sp%???}  # progress bar
    input=${PNG}
    output=${PNG%.png}.svg
    echo ${input} '->' ${output}
    if ! test -e ${output}; then
    vtracer --colormode bw -f 2 --hierarchical stacked --mode polygon \
        --input ${input} --output ${output} 
    fi
    #json=${PNG%.png}.json
    #if ! test -e ${json}; then  # XXX: too slow
    #python3 -m veccls.svg2json -s ${output} -j ${json}
    #fi
done
