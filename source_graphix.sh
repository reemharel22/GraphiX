#! /bin/bash
module purge
module load gcc/4.9.1
module load gnuplot/5.0.1
module load anaconda
./run_designer.sh
./run_cython.sh
