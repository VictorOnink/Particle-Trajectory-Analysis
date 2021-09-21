import pims
from utils_filenames import *
import particle_tracking
import numpy as np
import matplotlib.pyplot as plt


class particle_visualization:
    def __init__(self, file_name):
        self.file_name = file_name
        self.fps = 25
        self.dt = 1 / self.fps
        self.gray_scale_direc = particle_tracking.convert_video_to_grayscale_frames(file_name=self.file_name)
        self.video_frames = pims.open(self.gray_scale_direc + '*.png')
        self.y_pixels, self.x_pixels = self.video_frames.frame_shape
        self.pixel_to_mm = 6 / self.y_pixels
        self.fig_size = (8, 6)
        self.font_size_label = 14
        self.font_size_title = 16
        self.title = self.file_name.split('Data/')[1].split('_')[0]

    def plot_trajectories(self, linked_dataframe_list):
        fig = plt.figure(figsize=self.fig_size)
        ax = fig.add_subplot(111)
        ax.set_ylim([0, self.y_pixels * self.pixel_to_mm])
        ax.set_xlim([0, 11])
        ax.set_ylabel('y (mm)', fontsize=self.font_size_label)
        ax.set_xlabel('x (mm)', fontsize=self.font_size_label)
        ax.set_title(self.title, fontsize=self.font_size_label + 2)
        ax.tick_params(axis='both', labelsize=self.font_size_label)
        # The number of unique particles in the video
        counter = 0
        for linked_dataframe in linked_dataframe_list:
            counter += np.unique(linked_dataframe.particle).size
        colors = plt.cm.viridis(np.linspace(0, 1, counter))
        color_index_list = [i for i in range(counter)]
        for linked_dataframe in linked_dataframe_list:
            for p_id in np.unique(linked_dataframe.particle):
                color_index = color_index_list.pop(np.random.randint(len(color_index_list)))
                p_id_data = linked_dataframe[linked_dataframe['particle'] == p_id].reset_index(drop=True)
                ax.plot(p_id_data.x * self.pixel_to_mm, p_id_data.y * self.pixel_to_mm, '-', c=colors[color_index])
        plt.savefig(settings.FIGURE_DIREC + '{}.png'.format(self.title), bbox_inches='tight', dpi=300)