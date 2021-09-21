import particle_tracking
import particle_analysis
import particle_visualization
import utils
from utils_filenames import *
import numpy as np


if settings.SERVER == 'remote_server':
    """
    On the remote_server, we run the initial feature analysis, and save the pd.Dataframe containing the unlinked
    features.
    """
    def run():
        file_name = settings.DATA_DIREC + settings.VIDEO_LIST[settings.JOB_ID]
        tracking = particle_tracking.particle_tracking(file_name=file_name)
        unlinked_dataframe = tracking.batch_feature_locator(frame_number=-1)
        unlinked_dataframe_name = unlinked_trajectory_file_name(file_name=file_name)
        utils.save_obj(filename=unlinked_dataframe_name, item=unlinked_dataframe)
else:
    """
    On the local laptop, we run all subsequent analysis of the unlinked features within the unlinked feature dataframe
    to link the features into trajectories and then either analyse the velocities or plot the trajectories.
    
    The video_id indicates which 3D print shape videos to analyze, where:
        - video_id in [0, 1, 2] => Schwarz D videos
        - video_id in [3, 4, 5] => Schwarz G videos
        - video_id in [6, 7, 8] => Schwarz P videos
        
    Calculating the mean velocity:
        To calculate the mean particle velocity for a particular 3D print shape, the code must run over all video files
        for that 3D print shape. Furthermore, within tracking.feature_linking() it is vital that filter_xspan=False so 
        that all trajectories are accounted for in the analysis.
        
    Plotting the trajectories:
        To simplify the plots of the trajectories, we only plot a subset of all trajectories that run the entire length
        of the x axis. Therefore, in tracking.feature_linking() we set filter_xspan=True. To recreate the plotted 
        trajectories for each 3D print shape, use the following video_ids:
        - Schwarz D: video_id in [0]
        - Schwarz G: video_id in [3]
        - Schwarz P: video_id in [6, 7, 8]
        We loop over all video files for Schwarz P due to the lower number of full length trajectories within any one
        video file.
    """
    def run():
        v_x, weights = np.array([]), np.array([])
        linked_dataframe_list = []
        for video_id in [0]:
            """
            Getting the file name of the video that is being analyzed and loading the associated unlinked trajectory
            dataframe
            """
            file_name = settings.DATA_DIREC + settings.VIDEO_LIST[video_id]
            print(settings.VIDEO_LIST[video_id])
            unlinked_dataframe = utils.load_obj(unlinked_trajectory_file_name(file_name=file_name))

            # Link the features into trajectories
            tracking = particle_tracking.particle_tracking(file_name=file_name)
            linked_dataframe = tracking.feature_linking(unlinked_dateframe=unlinked_dataframe,
                                                        filter_frame_cutoff=True, filter_xspan=True)
            """
            If the linked_dataframe is not empty after the filtering operations in tracking.feature_linking(), then
            add linked_dataframe to linked_dataframe_list
            """
            if linked_dataframe.shape[0] > 0:
                linked_dataframe_list.append(linked_dataframe)

            """
            If you want to plot a certain frame from the video, uncomment the following line and set frame_number to
            whatever frame you want to take a look at.
            """
            # tracking.feature_locator_frame(frame_number=10, feature_dataframe=linked_dataframe, particle_id=0)

            """
            Calculating the mean speed for all particles within the linked_dataframe
            """
            if linked_dataframe.shape[0] > 0:
                analysis = particle_analysis.particle_analysis(file_name=file_name)
                v_x_part, _, weight_part = analysis.calculate_particle_speeds(linked_dataframe=linked_dataframe)
                v_x = np.append(v_x, v_x_part)
                weights = np.append(weights, weight_part)

        # Plotting all trajectories within the linked_dataframe's in the linked_dataframe_list
        visual = particle_visualization.particle_visualization(file_name=file_name)
        visual.plot_trajectories(linked_dataframe_list=linked_dataframe_list)

        # Calculate the overall mean and standard deviation of the speed in the x direction, where these are weighed by
        # the length of each individual trajectory
        v_x_mean, v_x_std = particle_analysis.weighted_avg_and_std(v_x, weights)
        particle_number = v_x.size
        str_format = settings.VIDEO_LIST[video_id], v_x_mean, v_x_std, particle_number
        print('for {}, we have speed {:.3f}±{:.3f} mm/s (N={})'.format(*str_format))


if __name__ == '__main__':
    run()