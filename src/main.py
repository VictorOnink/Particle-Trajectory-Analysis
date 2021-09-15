import particle_tracking
import settings

if __name__ == '__main__':
    file_name = settings.DATA_DIREC + 'SchwarzD_1.mp4'
    tracking = particle_tracking.particle_tracking(file_name=file_name)
    frame_features = tracking.batch_feature_locator()
    linked_features = tracking.feature_linking(feature_dateframe=frame_features)
