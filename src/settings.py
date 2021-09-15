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
                   'ubelix': '/storage/homefs/vo18e689/PauProject/'}
ROOT_DIREC = ROOT_DIREC_DICT[SERVER]
DATA_DIREC = ROOT_DIREC + 'Data/'
FIGURE_DIREC = ROOT_DIREC + 'Figures/'
OUTPUT_DIREC = ROOT_DIREC + 'Output/'

# Video filenames
VIDEO_LIST = ['SchwarzD_1.mp4', 'SchwarzD_2.mp4', 'SchwarzD_3.mp4', 'SchwarzG_1.mp4', 'SchwarzG_2.mp4',
              'SchwarzG_3.mp4', 'SchwarzP_1.mp4', 'SchwarzP_2.mp4', 'SchwarzP_3.mp4', 'SingleChannel_1.mp4',
              'SingleChannel_2.mp4', 'SingleChannel_3.mp4']