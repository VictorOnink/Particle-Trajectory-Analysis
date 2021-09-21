import settings


def grayscale_filename(file_name, index):
    """
    Setting the name of each grayscale file for the i-th frame where i == index
    :param file_name:
    :param index:
    :return:
    """
    split_file = file_name.split('.mp4')[0]
    return split_file + '_gray_{}.png'.format(index)


def linked_trajectory_file_name(file_name):
    """
    Setting the filename of the pd.Dataframe containing the linked features
    :param file_name:
    :return:
    """
    return settings.OUTPUT_DIREC + file_name.split('Data/')[1].split('.mp4')[0] + '_linked_trajectories'


def unlinked_trajectory_file_name(file_name):
    """
    Setting the filename of the pd.Dataframe containing the unlinked features
    :param file_name:
    :return:
    """
    return settings.OUTPUT_DIREC + file_name.split('Data/')[1].split('.mp4')[0] + '_unlinked_trajectories'