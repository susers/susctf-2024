#!/bin/bash

echo $GZCTF_FLAG > /flag
export GZCTF_FLAG=""

chmod 700 /flag

python3 main.py
