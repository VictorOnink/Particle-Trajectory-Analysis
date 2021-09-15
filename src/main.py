import particle_tracking
import settings
import utils

if settings.SERVER == 'ubelix':
    def run():
        file_name = settings.DATA_DIREC + settings.VIDEO_LIST[settings.JOB_ID]
        tracking = particle_tracking.particle_tracking(file_name=file_name)
        frame_features = tracking.batch_feature_locator(frame_number=-1)
        frame_features_name = particle_tracking.unlinked_trajectory_file_name(file_name=file_name)
        utils.save_obj(filename=frame_features_name, item=frame_features)

else:
    def run():
        file_name = settings.DATA_DIREC + 'SchwarzD_1.mp4'
        tracking = particle_tracking.particle_tracking(file_name=file_name)
        frame_features = tracking.batch_feature_locator()
        linked_features = tracking.feature_linking(feature_dateframe=frame_features)

if __name__ == '__main__':
    run()