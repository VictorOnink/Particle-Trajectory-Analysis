import pims
import particle_tracking
import numpy as np


class particle_analysis:
    def __init__(self, file_name):
        self.file_name = file_name
        self.fps = 25
        self.dt = 1 / self.fps
        self.gray_scale_direc = particle_tracking.convert_video_to_grayscale_frames(file_name=self.file_name)
        self.video_frames = pims.open(self.gray_scale_direc + '*.png')
        self.y_pixels, self.x_pixels = self.video_frames.frame_shape
        self.pixel_to_mm = 6 / self.y_pixels

    def calculate_particle_speeds(self, linked_dataframe):
        particle_id_list = np.unique(linked_dataframe.particle)
        v_x, v_y, weight = np.array([], dtype=float), np.array([], dtype=float), np.array([], dtype=float)
        for p_id in particle_id_list:
            p_id_dataframe = linked_dataframe[linked_dataframe['particle'] == p_id].reset_index(drop=True)
            # First, we calculate the velocities over the entire track
            dy_path = p_id_dataframe[-1:].y.values - p_id_dataframe[:1].y.values
            dx_path = p_id_dataframe[-1:].x.values - p_id_dataframe[:1].x.values
            frame_number = (p_id_dataframe[-1:].frame.values - p_id_dataframe[:1].frame.values)[0]
            p_v_x, p_v_y = dx_path * self.pixel_to_mm * self.fps / frame_number, \
                           dy_path * self.pixel_to_mm * self.fps / frame_number
            # Then we calculate the velocity for each point
            dy = p_id_dataframe[1:].y.values - p_id_dataframe[:-1].y.values
            dx = p_id_dataframe[1:].x.values - p_id_dataframe[:-1].x.values
            vx, vy = dx * self.pixel_to_mm * self.fps, dy * self.pixel_to_mm * self.fps
            # Now, we see if a particle has a velocity lower than the threshold for more than a second.
            # If yes, we consider the particle stuck for some period of time and we don't consider it in the analysis
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
    """
    average = np.average(values, weights=weights)
    # Fast and numerically precise:
    variance = np.average((values - average) ** 2, weights=weights)
    return average, np.sqrt(variance)


def contiguous_regions(condition):
    """Finds contiguous True regions of the boolean array "condition". Returns
    a 2D array where the first column is the start index of the region and the
    second column is the end index.
    https://stackoverflow.com/questions/4494404/find-large-number-of-consecutive-values-fulfilling-condition-in-a-numpy-array
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
    idx.shape = (-1,2)
    return idx
