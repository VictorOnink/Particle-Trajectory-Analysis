#!/bin/sh
for ((JOB_ID=0; JOB_ID<=0; JOB_ID++)); do
  part1="#!/bin/sh"
  part2="#SBATCH --mail-type=begin,end,fail"
  part3="#SBATCH --mail-user=victor.onink@climate.unibe.ch"
  part4="#SBATCH --job-name="$runname
  part5="#SBATCH --output="runOutput/$runname".o%j"
  part6="#SBATCH --mem-per-cpu=40G"
  part7="#SBATCH --time=00:19:00"
  part8="#SBATCH --partition=epyc2"
  part9='#SBATCH --qos=job_epyc2_debug'
  part10="source /storage/homefs/vo18e689/.bash_profile"
  part11="source /storage/homefs/vo18e689/anaconda3/bin/activate videotracking"
  part12='cd "/storage/homefs/vo18e689/PauProject/Particle-Trajectory-Analysis/"'
  part13="python src/main.py -p 10 -v"
  for i in {1..13}; do
    partGrab="part"$i
    echo ${!partGrab} >> jobsubmissionFile_${JOB_ID}.sh
  done
  sbatch jobsubmissionFile_${JOB_ID}.sh
  rm jobsubmissionFile_${JOB_ID}.sh
done
