import trackpy as tp
import pims
import utils
import imageio
import settings
import os


class particle_tracking:
    def __init__(self, file_name):
        self.file_name = file_name
        self.fps = 25
        self.dt = 1 / self.fps
        self.gray_scale_direc = convert_video_to_grayscale_frames(file_name=self.file_name)
        self.video_frames = pims.open(self.gray_scale_direc + '*.png')
        self.x_pixels, self.y_pixels = self.video_frames.frame_shape
        self.pixel_to_mm = 6 / self.y_pixels
        self.feature_size_pixels = 29
        self.max_pixel_displacement = 10
        self.feature_mass_cutoff = 10000
        self.feature_frame_cutoff = 100 # frames, so equivalent to ~ 4 seconds

    def feature_locator_frame(self, frame_number):
        # frame_selection = convert_frame_to_grayscale(self.video_frames[frame_number])
        frame_selection = self.video_frames[frame_number]
        frame_features = tp.locate(frame_selection, diameter=self.feature_size_pixels, minmass=self.feature_mass_cutoff)
        tp.annotate(frame_features, frame_selection)

    def batch_feature_locator(self, frame_number=800):
        print('Looping through the frames to identify the features')
        tp.quiet()
        if frame_number is not None:
            frames = self.video_frames[:frame_number]
        else:
            frames = self.video_frames
        return tp.batch(frames, diameter=self.feature_size_pixels, minmass=self.feature_mass_cutoff)

    def feature_linking(self, feature_dateframe):
        print('Linking the features')
        tp.quiet()
        linked_features = tp.link(feature_dateframe, self.max_pixel_displacement, memory=3)
        linked_features = tp.filter_stubs(linked_features, threshold=self.feature_frame_cutoff)
        utils.save_obj(linked_trajectory_file_name(self.file_name), item=linked_features)
        return linked_features


def convert_frame_to_grayscale(video_frame):
    return video_frame[:, :, 1]


def convert_video_to_grayscale_frames(file_name):
    gray_scale_direc = file_name.split('Schwarz')[0] + file_name.split('/Data/')[1].split('.mp4')[0] + '/'
    os.system('echo "The data is in {}"'.format(gray_scale_direc))
    if not utils.check_direc_exist(gray_scale_direc):
        os.system('echo "creating the greyscale png files of the frames"')
        utils.check_direc_exist(gray_scale_direc, create_direc=True)
        reader = imageio.get_reader(file_name)
        for image_index, image in enumerate(reader):
            gray_file_name = grayscale_filename(file_name.split('Data/')[1], index=image_index)
            frame = convert_frame_to_grayscale(image)
            imageio.imwrite(gray_scale_direc + gray_file_name, frame)
    return gray_scale_direc


def grayscale_filename(file_name, index):
    split_file = file_name.split('.mp4')[0]
    return split_file + '_gray_{}.png'.format(index)


def linked_trajectory_file_name(file_name):
    return settings.OUTPUT_DIREC + file_name.split('Data/')[1].split('.mp4')[0] + '_linked_trajectories'


def unlinked_trajectory_file_name(file_name):
    return settings.OUTPUT_DIREC + file_name.split('Data/')[1].split('.mp4')[0] + '_unlinked_trajectories'