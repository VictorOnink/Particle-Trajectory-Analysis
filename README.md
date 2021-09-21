# Particle-Trajectory Analysis
 
Code to identify, track, analyse and visualize particle trajectories from video files for various 3D print shapes for Bernal et al. (in prep). The code was written by Victor Onink in consultation with Paulina Nunez Bernal.

The particle identification and feature linking into particle trajectories was done by the [Crocker & Grier (1996)](https://doi.org/10.1006/jcis.1996.0217) algorithm using [trackpy v0.5.0](https://doi.org/10.5281/zenodo.4682814).

The repository contains the following directories:
- `bin`: This contains the `job_submission.sh` bash file for running feature identification on a remote server using slurm job submission. 
- `src`: This contains all python code for feature identification, linking the identified features into particle trajectories, analysis of the trajectories and visualization of the trajectories. Within this directory are the following files:
 - `src/main.py`: The main file from which all tracking, analysis and visualization is directed. 
 - `src/particle_tracking.py`: Contains all code for identifying features in the video frames and linking these into particle trajectories.
 - `src/particle_analysis.py`: Contains all code for analysing the particle trajectories to calculate mean particle speeds.
 - `src/particle_visualization.py`: Contains all code for visualizing particle trajectories.
 - `src/utils.py`: Contains a number of simple utility functions
 - `src/utils_filenames.py`: Contains functions for setting the file names of various intermediate output.
 - `src/settings.py`: Contains a number of basic analysis parameters, such as directory paths and a list of all video files.
More detailed documentation of each function is contained within the respective files.
