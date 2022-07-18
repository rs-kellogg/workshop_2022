#!/bin/bash

clear

# activate conda environment
# moduel load python/anaconda3.6
# source activate automate_env

# load modules
module load python/anaconda3.6
module load R/4.1.1

# Run python script
python 1_fec_extract.py

# only run next step if file exists
{
if [ ! -f ~/workshop_2022/Session4_Automate/FEC/weball20.txt ]; then
    echo "FEC 2020 file not found!"
    #mail -s "KLC FEC script error" <email_address_here> <<< "2020 FEC file not found!"	
    exit 0
fi
}

# Run R script
Rscript 2_fec_process.R

