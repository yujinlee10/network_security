#!/bin/sh
set -eu

AUTH_DELAY_MS="${AUTH_DELAY_MS:-5000}"
AUTH_DELAY_IFACE="${AUTH_DELAY_IFACE:-eth0}"

if command -v tc >/dev/null 2>&1; then
    tc qdisc del dev "$AUTH_DELAY_IFACE" root 2>/dev/null || true
    tc qdisc add dev "$AUTH_DELAY_IFACE" root netem delay "${AUTH_DELAY_MS}ms"
fi

exec named -g -c /etc/bind/named.conf -u bind
