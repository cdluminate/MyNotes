#!/usr/bin/lua
-- Lumin's lua Logging facility module
-- COPYRIGHT (C) 2016 Zhou Mo <cdluminate@gmail.com>
-- MIT LICENSE
-- changelog:
--   mar 13 2016, add alias for all public functions
--   apr 10 2016, add fatal logging level
-- this file is apart of rainbowlog, and it also appears in my repo:
--  https://github.com/CDLuminate/withLinux

local LOG = {}
function LOG.__CORE (level, dt, di, message)
	io.write(string.format('%s%02d%02d %02d:%02d:%02d %s:%d] %s',
		level, dt.month, dt.day, dt.hour, dt.min, dt.sec,
		di.short_src, di.currentline, message))
end
function LOG._CORE (level, message, ending)
	local ending = ending or '\n'
	local di = debug.getinfo(3, 'Sl')
	if di == nil then return end
	local dt = os.date('*t', os.time())
	if dt == nil then return end
	LOG.__CORE (level, dt, di, message .. ending)
end

function LOG.DEBUG (message)
	io.write ('\x1b[36;1m')
	LOG._CORE ('D', message)
	io.write ('\x1b[m')
end
function LOG.debug (message)
	return LOG.DEBUG (message)
end

function LOG.INFO (message)
	io.write ('\x1b[32;1m')
	LOG._CORE ('I', message)
	io.write ('\x1b[m')
end
function LOG.info (message)
	return LOG.INFO (message)
end

function LOG.WARN (message)
	io.write ('\x1b[33;1m')
	LOG._CORE ('W', message)
	io.write ('\x1b[m')
end
function LOG.warn (message)
	return LOG.WARN (message)
end

function LOG.ERROR (message)
	io.write ('\x1b[31;1m')
	LOG._CORE ('E', message)
	io.write ('\x1b[m')
end
function LOG.error (message)
	return LOG.ERROR (message)
end

function LOG.FATAL (message)
	io.write ('\x1b[35;1m')
	LOG._CORE ('F', message)
	io.write ('\x1b[m')
end
function LOG.fatal (message)
	return LOG.FATAL (message)
end

return LOG
