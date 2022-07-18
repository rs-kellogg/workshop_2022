##########################################
# Download FEC Data on Candidates Spending
##########################################

# libraries used
import requests
import zipfile
import io
import re 
import csv 
import math
import datetime as dt
import time
import os
import argparse
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

###################
# Command Line Args
###################
parser = argparse.ArgumentParser()
parser.add_argument('--start', type=int, required=True)
parser.add_argument('--end', type=int, required=True)
args = parser.parse_args()



#############
# Functions
#############

# check if a number is even
def iseven(num_input):
        if (num_input % 2) == 0:
                return num_input
        else:
                num_input = num_input+1
                return num_input


##############################
# Downloading Pages
##############################

# input years
#start_year = "2018"
start_year = args.start 
#end_year = "2020"
end_year = args.end

# fix years by rounding 
start_year = iseven(int(start_year))
end_year = iseven(int(end_year))

# obtain a file count
files = round((int(end_year) - int(start_year))/2) + 1
print("We have " + str(files) + " files to download today.")

# find url and save dataset
for year in range(start_year,end_year+1):
        if (year % 2) == 1:
                pass
        else:
                # find url for first document
                y2 = int(str(year)[-2:])
                url = "https://www.fec.gov/files/bulk-downloads/" + str(year) + "/weball" + str(y2) + ".zip"
                print(url)

                # current time
                t = dt.datetime.now()

                # download page
                try:
                        r = requests.get(url, verify=False)
                        z = zipfile.ZipFile(io.BytesIO(r.content))
                        z.extractall()
                        year_range = str(int(year)-1) + "_" + str(year)
                        file_name = "y" + str(year_range) + ".txt"

                        # print which files were saved
                        print("At " + time.strftime("%X") + ", we successfully saved data for " + str(year_range) + ".")
                        
                        # sleep time
                        time.sleep(15)



                except Exception as e:
                        print(str(e))
                        pass
                        
                





