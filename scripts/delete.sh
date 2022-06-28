#!/bin/bash
# $1 Routers

if [ -z "$1" ]; then
  echo "Usage: sudo ./scripts/delete.sh <n routers>"
  exit 1
fi

for i in $(eval echo {1..$1})
do
  ip link delete s$i-eth1
done