#!/bin/bash

CONF="/etc/honeypotd/honeypot.conf"
TEMP_CONF="/etc/honeypotd/.honeypot.conf"

if [ -f $CONF ]; then
	echo "INFO: Main configuration file found"
	honeypotd --start
elif [ -f $TEMP_CONF ]; then
	echo "INFO: Temp configuration file found"
	honeypotd --dev
else
	honeypotd --copyconfig && echo "A Config file was generated at /etc/honeypotd/.honeypot.conf."
fi
