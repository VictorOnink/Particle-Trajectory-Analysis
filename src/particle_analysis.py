import pims
import particle_tracking
import numpy as np


class particle_analysis:
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

    def calculate_particle_speeds(self, linked_dataframe):
        """
        Calculate the average particle speed for each trajectory in the x and y directions.
        :param linked_dataframe: pd.Dataframe containing linked features
        :return:
        """
        # Getting a list unique particle ids
        particle_id_list = np.unique(linked_dataframe.particle)
        # Initializing the speed in x direction (v_x), speed in y direction (v_y) and length of the trajectory for later
        # weighing of the average (weight) list
        v_x, v_y, weight = np.array([], dtype=float), np.array([], dtype=float), np.array([], dtype=float)
        # Loop through all the unique particles
        for p_id in particle_id_list:
            # Getting just the features for the given particle trajectory
            p_id_dataframe = linked_dataframe[linked_dataframe['particle'] == p_id].reset_index(drop=True)
            # First, we calculate the velocities over the entire track
            dy_path = p_id_dataframe[-1:].y.values - p_id_dataframe[:1].y.values
            dx_path = p_id_dataframe[-1:].x.values - p_id_dataframe[:1].x.values
            frame_number = (p_id_dataframe[-1:].frame.values - p_id_dataframe[:1].frame.values)[0]
            p_v_x, p_v_y = dx_path * self.pixel_to_mm * self.fps / frame_number, \
                           dy_path * self.pixel_to_mm * self.fps / frame_number

            # Then we calculate the velocity for each point in the particle trajectory
            dy = p_id_dataframe[1:].y.values - p_id_dataframe[:-1].y.values
            dx = p_id_dataframe[1:].x.values - p_id_dataframe[:-1].x.values
            vx, vy = dx * self.pixel_to_mm * self.fps, dy * self.pixel_to_mm * self.fps

            # Now, we see if a particle has a velocity lower than the threshold for more than a second.
            # If yes, we consider the particle stuck for some period of time and we don't consider it in the analysis
            # The threshold velocity was set through trial and error, looking at which trajectories were being removed
            # from consideration or not
            below_threshold = vx < 0.01  # mm/s
            keep_data = True
            for start, stop in contiguous_regions(below_threshold):
                if stop - start > self.fps:
                    keep_data = False
                    break
            if keep_data:
                v_x = np.append(v_x, p_v_x)
                v_y = np.append(v_y, p_v_y)
                weight = np.append(weight, frame_number)
        return v_x, v_y, weight


def weighted_avg_and_std(values, weights):
    """
    Return the weighted average and standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    Original source: https://stackoverflow.com/questions/2413522/weighted-standard-deviation-in-numpy
    """
    average = np.average(values, weights=weights)
    # Fast and numerically precise:
    variance = np.average((values - average) ** 2, weights=weights)
    return average, np.sqrt(variance)


def contiguous_regions(condition):
    """
    Finds contiguous True regions of the boolean array "condition". Returns
    a 2D array where the first column is the start index of the region and the
    second column is the end index.
    Original source: https://stackoverflow.com/questions/4494404/find-large-number-of-consecutive-values-fulfilling-condition-in-a-numpy-array
    """

    # Find the indicies of changes in "condition"
    d = np.diff(condition)
    idx, = d.nonzero()

    # We need to start things after the change in "condition". Therefore,
    # we'll shift the index by 1 to the right.
    idx += 1

    if condition[0]:
        # If the start of condition is True prepend a 0
        idx = np.r_[0, idx]

    if condition[-1]:
        # If the end of condition is True, append the length of the array
        idx = np.r_[idx, condition.size] # Edit

    # Reshape the result into two columns
    idx.shape = (-1, 2)
    return idx
