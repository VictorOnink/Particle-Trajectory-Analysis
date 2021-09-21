import socket
import os

# Checking which computer the code is running on
HOSTNAME = 'Victors-MBP.home'
if socket.gethostname() == HOSTNAME:
    SERVER = 'laptop'
else:
    SERVER = 'remote_server'
    JOB_ID = int(os.environ["JOB_ID"]) 

# Setting directory paths
machine_home_directory = os.path.expanduser('~')
ROOT_DIREC_DICT = {'laptop': machine_home_directory + '/Desktop/Pau data analysis/',
                   'remote_server': machine_home_directory + '/PauProject/'}
ROOT_DIREC = ROOT_DIREC_DICT[SERVER]
DATA_DIREC = ROOT_DIREC + 'Data/'
FIGURE_DIREC = ROOT_DIREC + 'Figures/'
OUTPUT_DIREC = ROOT_DIREC + 'Output/'

# Names of the video files
VIDEO_LIST = ['SchwarzD_1.mp4', 'SchwarzD_2.mp4', 'SchwarzD_3.mp4', 'SchwarzG_1.mp4', 'SchwarzG_2.mp4',
              'SchwarzG_3.mp4', 'SchwarzP_1.mp4', 'SchwarzP_2.mp4', 'SchwarzP_3.mp4']