import os
import datetime

# just to make sure the directory is clean
os.system('rm -rf *')

with open('/tmp/log.txt', 'a') as f:
    f.write(f'[{datetime.datetime.now()}] init.py executed, sandbox id: {__file__.split('/')[-2]}\n')