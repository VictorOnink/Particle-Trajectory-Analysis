import settings


def grayscale_filename(file_name, index):
    split_file = file_name.split('.mp4')[0]
    return split_file + '_gray_{}.png'.format(index)


def linked_trajectory_file_name(file_name):
    return settings.OUTPUT_DIREC + file_name.split('Data/')[1].split('.mp4')[0] + '_linked_trajectories'


def unlinked_trajectory_file_name(file_name):
    return settings.OUTPUT_DIREC + file_name.split('Data/')[1].split('.mp4')[0] + '_unlinked_trajectories'