###################################
### Automate Cleaning a Dataset ###
###################################

#load libraries
import re
import os
import pandas as pd

#change directories to cropped folder
main_dir = '~/workshop_2022/Session4_Automate/interest_rates/data/raw'
os.chdir(main_dir)

#######################
# Individualzied Fixes

# Read in one File
ir2000 = pd.read_csv ('ir2000.csv', encoding='utf8')

# Change one Value - The interest rate in April 2021 is off by a decimal
# print(ir2000[11,4])
print(ir2000.iloc[10,3])
ir2000.iloc[10,3] = 7.8
print(ir2000.iloc[10,3])

# Remove an Extra Header Row
print(ir2000.iloc[6,])
ir2000 = ir2000.drop(index=6)
#ir2000 = ir2000[ir2000.Int != 'Month']
print(ir2000.iloc[6,])

# Change NDs to NAs
print(ir2000.iloc[22,4])
ir2000.iloc[22,4] = pd.NA
print(ir2000.iloc[22,4])

# Save Results
# ir2000.to_csv('ir2000_new.csv', sep=',', encoding='utf-8', index="False")


########################
# Generalizing Changes

# read in all data files
all_files = os.listdir(main_dir)    
csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))
print(csv_files)

# combine datasets
ir = pd.concat(map(pd.read_csv, csv_files), ignore_index=True)
print(ir.shape)

# Remove all rows with header values
ir = ir[ir.Month != 'Month']
print(ir.iloc[6,])

# check all prime rates for errors at once
print(ir.iloc[10,3])
print(ir['Prime_Rate'].dtype)
ir['Prime_Rate'] = ir['Prime_Rate'].astype('float')
ir.loc[ir['Prime_Rate'] < 1, 'Prime_Rate'] = ir['Prime_Rate'] * 10

# replace NDs with NAs
ir.loc[ir['Treasury_Rate_3_Month'] == "ND", 'Treasury_Rate_3_Month'] = pd.NA

# Save Results
up_dir = '~/workshop_2022/Session4_Automate/interest_rates/data'
os.chdir(up_dir)
ir.to_csv('interest_rate_update.csv', sep=',', encoding='utf-8', index=False)

# Return a Message when file is run to completion
print("Sucessfully cleaned interest rate data.")

######################
# In Class Exercise: 
######################
# Use regex to automate separating the year and month from the "Month" variable.
# Then sort the dataset by year and month before saving. 
# HINT: I like the "re" library.












# ######################
# # Potential Solution: 
# ######################
ir['Year'] = ir['Month'].str.extract(pat='(\d{4})', expand=True)
ir['Month'] = ir['Month'].str.extract(pat = '-(\d{2})', expand=True)
ir = ir.sort_values(by = ['Year', 'Month'], ascending = [True, True])
ir.to_csv('interest_rate_update.csv', sep=',', encoding='utf-8', index=False)




