import socket
import os
# Checking which computer this is all running on
HOSTNAME = 'Victors-MBP.home'
if socket.gethostname() == HOSTNAME:
    SERVER = 'laptop'
else:
    SERVER = 'ubelix'
    JOB_ID = int(os.environ["JOB_ID"]) 

# Directory paths
ROOT_DIREC_DICT = {'laptop': '/Users/victoronink/Desktop/Pau data analysis/',
              'ubelix': ''}
ROOT_DIREC = ROOT_DIREC_DICT[SERVER]
DATA_DIREC = ROOT_DIREC + 'Data/'
FIGURE_DIREC = ROOT_DIREC + 'Figures/'
OUTPUT_DIREC = ROOT_DIREC + 'Output/'