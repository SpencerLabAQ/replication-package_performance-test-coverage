#!/bin/bash -l
#SBATCH -n 1                                  # Number of tasks (single task for your script)
#SBATCH -o /NFSHOME/mimran/out/artigenz/artigenz_withoutComments_twoShot_output.out  # Standard output file path
#SBATCH -e /NFSHOME/mimran/out/artigenz/artigenz_withoutComments_twoShot_error.err   # Standard error file path
#SBATCH -J artigenz_twoShot                  # Job name
#SBATCH -p cuda                              # GPU partition (verify if “cuda” is correct with admins)
#SBATCH -c 8                                  # Request 8 CPU cores per task
#SBATCH --gres=gpu:1                          # Request GPU

# Set environment variables to limit library threading and prevent CPU overload
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export OPENBLAS_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export MKL_NUM_THREADS=${SLURM_CPUS_PER_TASK}
export VECLIB_MAXIMUM_THREADS=${SLURM_CPUS_PER_TASK}
export NUMEXPR_NUM_THREADS=${SLURM_CPUS_PER_TASK}

# Activate your Conda environment
source ~/.bashrc
conda activate imrenv

# Run your batch script
bash ~/codebert/code/train.sh