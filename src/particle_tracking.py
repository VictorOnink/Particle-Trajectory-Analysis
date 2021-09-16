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
        self.file_name = file_name
        self.fps = 25
        self.dt = 1 / self.fps
        self.gray_scale_direc = convert_video_to_grayscale_frames(file_name=self.file_name)
        self.video_frames = pims.open(self.gray_scale_direc + '*.png')
        self.y_pixels, self.x_pixels = self.video_frames.frame_shape
        self.pixel_to_mm = 6 / self.y_pixels
        self.feature_size_pixels = 29
        self.max_pixel_displacement = 40
        self.feature_mass_cutoff = 10000
        self.feature_frame_cutoff = 25 # frames, so equivalent to ~ 4 seconds

    def batch_feature_locator(self, frame_number=800):
        print('Looping through the frames to identify the features')
        tp.quiet()
        if frame_number is not None:
            frames = self.video_frames[:frame_number]
        else:
            frames = self.video_frames
        return tp.batch(frames, diameter=self.feature_size_pixels, minmass=self.feature_mass_cutoff)

    def feature_locator_frame(self, frame_number, feature_dataframe, particle_id=None):
        # frame_selection = convert_frame_to_grayscale(self.video_frames[frame_number])
        frame_selection = self.video_frames[frame_number]
        plt.figure(frame_number)
        if particle_id is None:
            selection = feature_dataframe.frame == frame_number
        else:
            selection = (feature_dataframe.frame == frame_number) & (feature_dataframe.particle == particle_id)
        tp.annotate(feature_dataframe[selection], frame_selection)

    def feature_linking(self, unlinked_dateframe, filter_frame_cutoff=False, filter_xspan=False,
                        filter_size_cutoff=False):
        print('Linking the features')
        tp.quiet()
        # Linking the particles into trajectories
        linked_features = tp.link(unlinked_dateframe, self.max_pixel_displacement, memory=20)
        print(linked_features.shape)
        # Removing all trajectories shorter than self.feature_frame_cutoff
        if filter_frame_cutoff:
            linked_features = tp.filter_stubs(linked_features, threshold=self.feature_frame_cutoff)
            print(linked_features.shape)
        if filter_size_cutoff:
            pass
        # Removing all trajectories that don't cover the full span of the video
        if filter_xspan:
            linked_features = filter_begin_end_point(linked_features, x_pixels=self.x_pixels)
            print(linked_features.shape)
        return linked_features


def filter_begin_end_point(linked_features, x_pixels, x_limit=200):
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
    return video_frame[:, :, 1]


def convert_video_to_grayscale_frames(file_name):
    gray_scale_direc = file_name.split('Schwarz')[0] + file_name.split('/Data/')[1].split('.mp4')[0] + '/'
    if not utils.check_direc_exist(gray_scale_direc) and settings.SERVER == 'ubelix':
        os.system('echo "creating the greyscale png files of the frames"')
        utils.check_direc_exist(gray_scale_direc, create_direc=True)
        reader = imageio.get_reader(file_name)
        for image_index, image in enumerate(reader):
            gray_file_name = grayscale_filename(file_name.split('Data/')[1], index=image_index)
            frame = convert_frame_to_grayscale(image)
            imageio.imwrite(gray_scale_direc + gray_file_name, frame)
    return gray_scale_direc


