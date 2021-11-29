#!/usr/bin/luajit

log = require 'lumin_log'
LOG = log

log.info "lumin's rainbowlog demo in lua"

LOG.DEBUG("debug")
LOG.INFO("hello")
LOG.WARN("warn")
LOG.ERROR("err")
LOG.FATAL("fatal!")

LOG.INFO("Happy hacking!")
