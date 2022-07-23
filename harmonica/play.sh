#!/bin/sh
LY=${1}
lilypond ${LY}
wildmidi ${LY%.ly}.midi
