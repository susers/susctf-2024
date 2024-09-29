#!/bin/sh

echo $GZCTF_FLAG > /flag
export GZCTF_FLAG=""

chown -R app:app /flag
chmod 400 /flag

cd /app && su app -c "python3 main.py"
