##############################
### Taxi Trip Data Example ###
##############################

# Main Questions: Are Taxi Rides Faster on Sunny Days?

# Steps:
# 1.) Import Taxi Data
# 2.) Reformat Data to Answer Question
#     a. Separate Dropoff_DateTime into 2 variables for date and time
#     b. Calculate a variable for trip_MPS (Miles per Second)
#     c. Merge taxi data with weather data
#     d. Create descriptive statistics for the variables
# 3.) Run a Linear Regression and Graph Results

#####################################
# Connecting on KLC

### Connecting on KLC ####

# From a FastX webbrowser or Desktop client
# module load python/anaconda3.6
# python taxi.py 
# OR
# spyder


# set working directory
import os
wd = "/home/<netid>/workshop_2022/Session6_Export_Results/data"
os.chdir(wd)

# load other libraries
import pandas as pd
import numpy as np
from sklearn import linear_model
import seaborn as sns; sns.set(color_codes=True)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from stargazer.stargazer import Stargazer
import statsmodels.api as sm
import matplotlib.pyplot as plt

#####################################
# 1.) Import Taxi Data

# read in the dataframe
taxi = pd.read_csv("taxi_backup.csv")
len(taxi)
taxi.head()

#####################################
# 2.) Reformat the Taxi Data

# print column list
print(list(taxi))

# Remove invalid time observations
taxi['trip_time_in_secs'] = pd.to_numeric(taxi['trip_time_in_secs'])
taxi = taxi[taxi.trip_time_in_secs > 0]
len(taxi)

# Separate Pickup_DateTime into Two Variables for Date and Time
taxi.rename(columns = {'pickup_datetime':'pickup'}, inplace = True) 
taxi.rename(columns = {'dropoff_datetime':'dropoff'}, inplace = True) 

taxi[['pickup_date','pickup_time']] = taxi.pickup.str.split(" ",expand=True)
taxi[['dropoff_date','dropoff_time']] = taxi.dropoff.str.split(" ",expand=True)

taxi.head()

# Create a miles per hour variable
taxi['trip_distance'] = pd.to_numeric(taxi['trip_distance'])
taxi['passenger_count'] = taxi['passenger_count'].astype(int)
taxi['trip_MPH'] = taxi.trip_distance/((taxi.trip_time_in_secs/60)/60)
taxi = taxi[(taxi.trip_MPH < 75) & (taxi.passenger_count < 5)]

taxi.head()


# Merge Taxi data with Weather Data
weather_data = {'pickup_date':['2013-05-20', '2013-06-20'], 'condition':['sunny', 'cloudy/rain']} 
weather = pd.DataFrame(weather_data)
weather
    
taxi = pd.merge(taxi, weather, on="pickup_date")
taxi.head()


# navigate to output directory
out_files = "/home/<netid>/workshop_2022/Session6_Export_Results/python_code/latex_files"
os.chdir(out_files)


# Summarize the variables
print(taxi.describe())
taxi_desc = taxi.describe()
with open('taxi_summary.tex','w') as tf:
    tf.write(taxi_desc.to_latex())

#####################################
# 3.) Run a Regression and graph results
# replace underscores in column names (can produce a latex error)
taxi.columns = taxi.columns.str.replace('_', '')

# create objects for outcome and predictor variables
y = taxi["tripMPH"]
conditiondummy = pd.get_dummies(taxi['condition'])
taxi = pd.concat([taxi, conditiondummy], axis=1)

X = taxi[['passengercount', 'sunny']]
X[:5]

# run the regression
lm = linear_model.LinearRegression()
model = lm.fit(X,y)
print(model.coef_)

# run regression again
est = sm.OLS(endog=y, exog=sm.add_constant(X)).fit()
stargazer = Stargazer([est])

# save latex reg file
tex_file = open( 'taxi_reg.tex', "w" ) 
tex_file.write( stargazer.render_latex() )
tex_file.close()

# graph the results
sns.lmplot(x="passengercount", y="tripMPH", hue="condition", data=taxi)
plt.savefig('taxi_plot.pdf')
