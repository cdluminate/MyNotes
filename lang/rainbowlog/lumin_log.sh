#!/bin/bash
# Rainbow log in BASH
# Copyright (C) 2016 Zhou Mo <cdluminate AT gmail DOT com>
# This file also appears in my repo: https://github.com/CDLuminate/withLinux
# MIT License
set -e

debug () {
  if [ -z "$@" ]; then
    printf "\n"
  else
    printf "[36;1mD%s %s %s %s:%s] %s[m\n" \
      "$(date +%m%d)" \
      "$(date +%H:%M:%S)" \
      "$$" "$0" "$BASH_LINENO" \
      "$@"
  fi
}

info () {
  if [ -z "$@" ]; then
    printf "\n"
  else
    printf "[32;1mI%s %s %s %s:%s] %s[m\n" \
      "$(date +%m%d)" \
      "$(date +%H:%M:%S)" \
      "$$" "$0" "$BASH_LINENO" \
      "$@"
  fi
}

warn () {
  if [ -z "$@" ]; then
    printf "\n"
  else
    printf "[33;1mW%s %s %s %s:%s] %s[m\n" \
      "$(date +%m%d)" \
      "$(date +%H:%M:%S)" \
      "$$" "$0" "$BASH_LINENO" \
      "$@"
  fi
}

error () {
  if [ -z "$@" ]; then
    printf "\n"
  else
    printf "[31;1mE%s %s %s %s:%s] %s[m\n" \
      "$(date +%m%d)" \
      "$(date +%H:%M:%S)" \
      "$$" "$0" "$BASH_LINENO" \
      "$@"
  fi
}

fatal () {
  if [ -z "$@" ]; then
    printf "\n"
  else
    printf "[35;1mF%s %s %s %s:%s] %s[m\n" \
      "$(date +%m%d)" \
      "$(date +%H:%M:%S)" \
      "$$" "$0" "$BASH_LINENO" \
      "$@"
  fi
}
