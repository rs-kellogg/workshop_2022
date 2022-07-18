#!/bin/bash -l

source ~/.bash_profile
module load python/anaconda3.6
python ~/workshop_2022/Session4_Automate/FEC/1_fec_extract.py
echo "Cron Job is running on KLC Node 202."
