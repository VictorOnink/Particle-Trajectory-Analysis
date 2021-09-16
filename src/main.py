import particle_tracking
import particle_analysis
import particle_visualization
import settings
import trackpy as tp
import utils
from utils_filenames import *
import matplotlib.pyplot as plt
import numpy as np

"""
VIDEO_LIST = ['SchwarzD_1.mp4', 'SchwarzD_2.mp4', 'SchwarzD_3.mp4', 'SchwarzG_1.mp4', 'SchwarzG_2.mp4',
              'SchwarzG_3.mp4', 'SchwarzP_1.mp4', 'SchwarzP_2.mp4', 'SchwarzP_3.mp4', 'SingleChannel_1.mp4',
              'SingleChannel_2.mp4', 'SingleChannel_3.mp4']
"""

if settings.SERVER == 'ubelix':
    def run():
        file_name = settings.DATA_DIREC + settings.VIDEO_LIST[settings.JOB_ID]
        tracking = particle_tracking.particle_tracking(file_name=file_name)
        frame_features = tracking.batch_feature_locator(frame_number=-1)
        frame_features_name = unlinked_trajectory_file_name(file_name=file_name)
        utils.save_obj(filename=frame_features_name, item=frame_features)
else:
    def run():
        v_x, weights = np.array([]), np.array([])
        linked_dataframe_list = []
        for video_id in [6, 7, 8]:
            file_name = settings.DATA_DIREC + settings.VIDEO_LIST[video_id]
            print(settings.VIDEO_LIST[video_id])
            tracking = particle_tracking.particle_tracking(file_name=file_name)
            unlinked_dataframe = utils.load_obj(unlinked_trajectory_file_name(file_name=file_name))
            linked_dataframe = tracking.feature_linking(unlinked_dateframe=unlinked_dataframe,
                                                        filter_frame_cutoff=True, filter_xspan=True,
                                                        filter_size_cutoff=True)
            if linked_dataframe.shape[0] > 0:
                linked_dataframe_list.append(linked_dataframe)
            # tracking.feature_locator_frame(10, linked_dataframe, particle_id=0)
            # plt.figure(video_id)
            # tp.plot_traj(linked_dataframe[linked_dataframe.particle < 200])

            # analysis = particle_analysis.particle_analysis(file_name=file_name)
            # v_x_part, _, weight_part = analysis.calculate_particle_speeds(linked_dataframe=linked_dataframe)
            # v_x = np.append(v_x, v_x_part)
            # weights = np.append(weights, weight_part)
        visual = particle_visualization.particle_visualization(file_name=file_name)
        visual.plot_trajectories(linked_dataframe_list=linked_dataframe_list)

        # v_x_mean, v_x_std = particle_analysis.weighted_avg_and_std(v_x, weights)
        # particle_number = v_x.size
        # str_format = settings.VIDEO_LIST[video_id], v_x_mean, v_x_std, particle_number
        # print('for {}, we have speed {:.3f}±{:.3f} mm/s (N={})'.format(*str_format))


if __name__ == '__main__':
    run()