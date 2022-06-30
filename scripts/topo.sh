#!/bin/bash

# if $1 is empty
if [ -z "$1" ]; then
  sudo -E env PATH=$PATH python3 topology/linear_topo.py
  exit 1
fi

sudo -E env PATH=$PATH python3 topology/$1.py
