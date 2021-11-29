#!/bin/sh
# Simple Debian Source Syncer
# Lumin <cdluminate@gmail.com>
# BSD-2-Clause
set -e

# core program
RSYNC=/usr/bin/rsync

# parameter
RSYNC_ARG="-4avH -h --delete-during --delete-excluded --partial --progress"
# SRC= (this variable is set in ./config)
# BW= (this variable is set in ./config)
TIMEOUT=--timeout=30
DST="./debian/"
EXCLUDE="./exclude.txt"
LOG="./debian.log"
# Source ./config as SHELL script
. ./config

# do check first
printf "I: Checking Debian Archive Directory ... "
if [ -d debian ]; then
  printf "[ OK ]\n"
else
  mkdir debian
  printf "[ Created new directory ]\n"
fi

# start syncing
printf "I: Starting to rsync Debian Source ... \n"
${RSYNC} ${RSYNC_ARG} ${BW} ${TIMEOUT} \
  --exclude-from=${EXCLUDE} \
  --log-file=${LOG} \
  ${SRC} ${DST}

# vim
