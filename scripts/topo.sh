#!/bin/bash

# if $1 is not empty

if [ -z "$1" ]; then
  sudo python topology/linear_topo.py
  exit 1
fi

sudo python topology/$1.py