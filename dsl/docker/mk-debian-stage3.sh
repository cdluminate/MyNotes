#!/bin/sh
set -e

sudo true # require superuser

echo "=> Making Debian's Stage3 Tarball"
echo "   Usage: $0 DISTRO MIRROR"
test -z "$1" && (echo ?? missing DISTRO; false)
test -z "$2" && (echo ?? missing MIRROR; false)

TEMP=$(mktemp -d)
ROOT=$TEMP/root
TIMESTAMP=$(date +%Y%m%d)
NAME="Debian-Stage3-$TIMESTAMP.tgz"

# Prefer cdebootstrap than debootstrap
DEBS=cdebootstrap
which $DEBS || DEBS=debootstrap
EMD=eatmydata
which $EMD && DEBS="$EMD $DEBS"

mkdir -p $ROOT
sudo $DEBS $1 $ROOT $2
cd $ROOT; sudo tar zcvf ../$NAME .
sudo rm -rf $ROOT

echo "=> Tarball Available here: $TEMP/$NAME"
ls -lh $TEMP/

# docker import $TEMP/$NAME debian:$1.$TIMESTAMP
