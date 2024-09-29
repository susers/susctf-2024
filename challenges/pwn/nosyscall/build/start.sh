#!/bin/sh
# Add your startup script

echo -n $GZCTF_FLAG > flag
unset GZCTF_FLAG

# DO NOT DELETE
/etc/init.d/xinetd start;
sleep infinity;
