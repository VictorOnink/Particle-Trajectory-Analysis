import trackpy as tp
import pims
import utils
import imageio
import numpy as np
import os
from utils_filenames import *
import matplotlib.pyplot as plt


class particle_tracking:
    def __init__(self, file_name):
        # Video file name
        self.file_name = file_name
        # video frames per second
        self.fps = 25
        # directory containing greyscale files
        self.gray_scale_direc = convert_video_to_grayscale_frames(file_name=self.file_name)
        # frames object containing greyscale files
        self.video_frames = pims.open(self.gray_scale_direc + '*.png')
        # Number of pixels in xy directions
        self.y_pixels, self.x_pixels = self.video_frames.frame_shape
        # conversion from pixel number to mm
        self.pixel_to_mm = 6 / self.y_pixels
        # Size of feature in pixels to identify particle
        self.feature_size_pixels = 29
        # Max pixel displacement between frames for linking features into trajectories
        self.max_pixel_displacement = 40
        # Minimum "mass" of identified feature to be marked as a particle
        self.feature_mass_cutoff = 10000
        # Minimum length of a trajectory (in number of frames) for the trajectory to be retained
        self.feature_frame_cutoff = 25

    def batch_feature_locator(self, frame_number=800):
        """
        Identifying features in all frames within self.video_frames.
        :param frame_number: if not None, we only do feature identification in the first :frame_number frames
        :return: unlinked features dataframe
        """
        print('Looping through the frames to identify the features')
        tp.quiet()
        if frame_number is not None:
            frames = self.video_frames[:frame_number]
        else:
            frames = self.video_frames
        return tp.batch(frames, diameter=self.feature_size_pixels, minmass=self.feature_mass_cutoff)

    def feature_locator_frame(self, frame_number, feature_dataframe, particle_id=None):
        """
        Plotting the frame_number frame with annotated features.
        :param frame_number: Which frame within self.video_frames do you want to plot
        :param feature_dataframe: pd.Dataframe containing the linked features
        :param particle_id: If not None, we only plot the feature with id == particle_id
        :return:
        """
        frame_selection = self.video_frames[frame_number]
        plt.figure(frame_number)
        if particle_id is None:
            selection = feature_dataframe.frame == frame_number
        else:
            selection = (feature_dataframe.frame == frame_number) & (feature_dataframe.particle == particle_id)
        tp.annotate(feature_dataframe[selection], frame_selection)

    def feature_linking(self, unlinked_dateframe, filter_frame_cutoff=False, filter_xspan=False):
        """
        Linking the features within the unlinked_dataframe into trajectories, and applying various filtering steps on
        the subsequently calculated trajectories
        :param unlinked_dateframe: pd.Dataframe containing unlinked particle data
        :param filter_frame_cutoff: if True, remove all trajectories whose length is shorter than self.feature_frame_cutoff
        :param filter_xspan: if True, only leave particles that start within the first 200 pixels in the x direction and
                             end within the final 200 pixels in the x direction.
        :return: dataframe containing the linked features.
        """
        print('Linking the features')
        tp.quiet()
        # Linking the particles into trajectories
        linked_features = tp.link(unlinked_dateframe, self.max_pixel_displacement, memory=20)
        print(linked_features.shape)
        # Removing all trajectories shorter than self.feature_frame_cutoff
        if filter_frame_cutoff:
            linked_features = tp.filter_stubs(linked_features, threshold=self.feature_frame_cutoff)
            print(linked_features.shape)
        # Removing all trajectories that don't cover the full span of the video
        if filter_xspan:
            linked_features = filter_begin_end_point(linked_features, x_pixels=self.x_pixels)
            print(linked_features.shape)
        return linked_features


def filter_begin_end_point(linked_features, x_pixels, x_limit=200):
    """
    For particles within the linked_features dataframe, remove all that do not start within the first x_limit pixels in
    the x direction and do not end within the final (x_pixels - x_limit) pixels in the x direction.
    :param linked_features: pd.Dataframe containing linked features.
    :param x_pixels: number of pixels in the x direction
    :param x_limit: Cutoff value (number of pixels) for start and end blocks in the x direction.
    :return: dataframe containing the linked features
    """
    retained_id = []
    for p_id in np.unique(linked_features.particle):
        p_id_dataframe = linked_features[linked_features.particle == p_id]
        min_frame, max_frame = p_id_dataframe.frame.min(), p_id_dataframe.frame.max()
        start_x, end_x = p_id_dataframe.x[min_frame], p_id_dataframe.x[max_frame]
        if start_x < x_limit and end_x > (x_pixels - x_limit):
            retained_id.append(p_id)
    within = np.zeros(linked_features.shape[0], dtype=bool)
    for index, p_id in enumerate(linked_features.particle):
        if p_id in retained_id:
            within[index] = True
    return linked_features[within]


def convert_frame_to_grayscale(video_frame):
    """
    Convert a RGB array into greyscale.
    :param video_frame:
    :return:
    """
    return video_frame[:, :, 1]


def convert_video_to_grayscale_frames(file_name):
    """
    Convert the original video file into a series of greyscale png files.
    :param file_name:
    :return:
    """
    gray_scale_direc = file_name.split('Schwarz')[0] + file_name.split('/Data/')[1].split('.mp4')[0] + '/'
    """ 
    Only carry out the conversion if a) the conversion hasn't been done yet
                                     b) we are currently running on the remote server
    """
    if not utils.check_direc_exist(gray_scale_direc) and settings.SERVER == 'remote_server':
        os.system('echo "creating the greyscale png files of the frames"')
        utils.check_direc_exist(gray_scale_direc, create_direc=True)
        reader = imageio.get_reader(file_name)
        for image_index, image in enumerate(reader):
            gray_file_name = grayscale_filename(file_name.split('Data/')[1], index=image_index)
            frame = convert_frame_to_grayscale(image)
            imageio.imwrite(gray_scale_direc + gray_file_name, frame)
    return gray_scale_direc


