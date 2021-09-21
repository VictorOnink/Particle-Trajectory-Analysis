import pims
from utils_filenames import *
import particle_tracking
import numpy as np
import matplotlib.pyplot as plt


class particle_visualization:
    def __init__(self, file_name):
        # Video file name
        self.file_name = file_name
        # video frames per second
        self.fps = 25
        # directory containing greyscale files
        self.gray_scale_direc = particle_tracking.convert_video_to_grayscale_frames(file_name=self.file_name)
        # frames object containing greyscale files
        self.video_frames = pims.open(self.gray_scale_direc + '*.png')
        # Number of pixels in xy directions
        self.y_pixels, self.x_pixels = self.video_frames.frame_shape
        # conversion from pixel number to mm
        self.pixel_to_mm = 6 / self.y_pixels
        # Size of figure
        self.fig_size = (8, 6)
        # Size of figure labels
        self.font_size_label = 14
        # Size of title of figure
        self.font_size_title = 16
        # The title of the figure
        self.title = self.file_name.split('Data/')[1].split('_')[0]

    def plot_trajectories(self, linked_dataframe_list):
        """
        Function to plot all trajectories contained within the linked dataframes within linked_dataframe_list
        :param linked_dataframe_list: list of pd.Dataframe's, where each contains the linked features for separate
                                      videos
        :return:
        """
        # Creating the video
        fig = plt.figure(figsize=self.fig_size)
        ax = fig.add_subplot(111)
        # Setting the limits of the x and y axis (mm), labeling the axis and adding the title
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
        # Creating a colormap containing 'counter' different colors. Each trajectory will therefore have a slightly
        # different color from within the colormap.
        colors = plt.cm.viridis(np.linspace(0, 1, counter))
        color_index_list = [i for i in range(counter)]
        # Plotting all trajectories in each linked_dataframe within linked_dataframe_list, where each trajectory has a
        # color that is randomly chose from colors
        for linked_dataframe in linked_dataframe_list:
            for p_id in np.unique(linked_dataframe.particle):
                color_index = color_index_list.pop(np.random.randint(len(color_index_list)))
                p_id_data = linked_dataframe[linked_dataframe['particle'] == p_id].reset_index(drop=True)
                # Convert to x and y data to millimeters
                p_id_data_x_mm, p_id_data_y_mm = p_id_data.x * self.pixel_to_mm, p_id_data.y * self.pixel_to_mm
                ax.plot(p_id_data_x_mm, p_id_data_y_mm, '-', c=colors[color_index])
        # Saving the figure
        plt.savefig(settings.FIGURE_DIREC + '{}.png'.format(self.title), bbox_inches='tight', dpi=300)
