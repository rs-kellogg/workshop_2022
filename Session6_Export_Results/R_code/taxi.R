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

# From a FastX webbrowser or Desktop client
# Select R/4.1.1 
# module load R/4.1.1
# Rscript <file_name> OR
# rstudio 

# clear workspace
rm(list=ls())

# set working directory
setwd("~/workshop_20202/Session6_Export_Results/data")

# install packages
#install.packages('stargazer')

# load libraries
library(dplyr)
library(plyr)
library(tidyr)
library(ggplot2)
library(vtable) # summary stats in latex
library(stargazer) # regression results table
#####################################
# 1.) Import Taxi Data

# read in the dataframe
taxi <- read.csv(file="taxi_backup.csv", header=TRUE, sep=",")


#####################################
# 2.) Reformat the Taxi Data

# Remove Invalid time observations
taxi <- subset(taxi, taxi$trip_time_in_secs > 0) 

# Separate Pickup_DateTime into Two Variables for Date and Time
colnames(taxi)

names(taxi)[4] <- "pickup"
names(taxi)[5] <- "dropoff"

taxi <- separate(taxi, pickup, into = c("pickup_date", "pickup_time"), sep = " ")
taxi <- separate(taxi, dropoff, into = c("dropoff_date", "dropoff_time"), sep = " ")

# Create a miles per hour variable
taxi$trip_MPH <- taxi$trip_distance/((taxi$trip_time_in_secs/60)/60)

taxi <- subset(taxi, taxi$trip_MPH <75 & taxi$passenger_count < 5)


# Merge Taxi data with Weather Data
weather <- data.frame(pickup_date=c("2013-05-20", "2013-06-20"), 
                      Condition=c('sunny', 'cloudy/rain'))

taxi <- join(taxi, weather, by="pickup_date", type="left", match="all")

# Summarize the variables
summary(taxi)
summary_taxi <- vtable(taxi,out='return') # create a summary dataframe
setwd("~/workshop_2022/Session6_Export_Results/R_code/latex_files")
vt(taxi,out='latex',file='taxi_summary.tex') # create a latex table file

#####################################
# 3.) Run a Regression and graph results
taxi.mod <- lm(trip_MPH ~ passenger_count + factor(Condition), data=taxi)
summary(taxi.mod)
stargazer(taxi.mod, type='latex', title="Taxi Regression", out="taxi_reg.tex")


taxi.predict <- cbind(taxi, predict(taxi.mod, interval = 'confidence'))

# create a pdf file for the graph
pdf("taxi_plot.pdf")

ggplot(taxi.predict, aes(y=trip_MPH, x= passenger_count, color=Condition)) +
  geom_point()+
  geom_line(aes(passenger_count,fit))+
  geom_ribbon(aes(ymin=lwr, ymax=upr), alpha=0.3)+
  xlab("Passengers") + ylab("Trip MPH")

dev.off()
