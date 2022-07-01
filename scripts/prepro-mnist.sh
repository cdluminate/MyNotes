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
    vtracer --colormode bw -f 2 --hierarchical stacked --mode polygon \
        --input ${input} --output ${output} 
done
