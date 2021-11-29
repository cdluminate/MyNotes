#!/bin/sh
# Keep the PPPoE connection
set -e

# check permission
sudo true

# register helper functions

function kill_all_pppd () {
	for PID in $(pgrep pppd); do
		kill -9 $PID
	done
}
function dial () {
	pon dsl-provider
}
function redial () {
	echo "I: Re-dialling ..."
	kill_all_pppd
	sleep 10
	dial
}
function check_if_ppp_linkup () {
	if test -z "`ip a | grep ppp`"; then
		false # problematic
	else
		true  # linkup
	fi
}
function pppoe_keeper () {
	check_if_ppp_linkup && true || redial
}

# main loop
while true; do
	pppoe_keeper
	sleep 300
done
