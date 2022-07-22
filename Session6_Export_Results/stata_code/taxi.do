*##############################
*### Taxi Trip Data Example ###
*##############################

*# Main Questions: Are Taxi Rides Faster on Sunny Days?

*# Steps:
*# 1.) Import Taxi Data
*# 2.) Reformat Data to Answer Question
*#     a. Separate Dropoff_DateTime into 2 variables for date and time
*#     b. Calculate a variable for trip_MPS (Miles per Second)
*#     c. Merge taxi data with weather data
*#     d. Create descriptive statistics for the variables
*# 3.) Run a Linear Regression and Graph Results

*---------------------------------------------
* Connecting on KLC

* From a terminal session on FastX, type the following:
* module load stata/17
* xstata-mp

*---------------------------------------------
* clear workspace
clear

# install outreg for saving latex output
*ssc install outreg2, replace
*ssc install estout, replace

* Set working directory
global dirin = "~/workshop_2022/Session6_Exporting_Results/data"
global dirout = "~/workshop_2022/Session6_Exporting_Results/stata_code/latex_files"


*-----------------------
* 1.) Import Taxi Data 
*------------------------

import delimited using "$dirin/taxi_backup.csv"

*-----------------------------
* 2.) Reformat the Taxi Data 
*-----------------------------
* Remove Invalid time observations
drop if trip_time_in_secs == 0


* a.) Separate Pickup_DateTime into Two Variables for Date and Time

rename pickup_datetime pickup
rename dropoff_datetime dropoff

split pickup, p(" ")
rename pickup1 pickup_date
rename pickup2 pickup_time

split dropoff, p(" ")
rename dropoff1 dropoff_date
rename dropoff2 dropoff_time

* b.) Create a miles per hour variable
gen trip_MPH = trip_distance/((trip_time_in_secs/60)/60)
**# Bookmark #1

drop if trip_MPH > 75
drop if passenger_count > 4

tempfile taxi
save taxi.dta, replace
clear

* c.) Merge Taxi data with Weather Data
import delimited using "$dirin/weather.csv"
rename v1 pickup_date
rename v2 condition


* merge datasets
merge 1:m pickup_date using taxi.dta

* d.) Summarize data
describe
outreg2 using "$dirout/taxi_summary.tex", tex(frag) replace sum(log)

*-----------------------------
* 3.) Run a Regression
*-----------------------------

xi: regress trip_MPH i.condition passenger_count
describe condition
encode condition, gen(condition2)

eststo clear
eststo: quietly regress trip_MPH i.condition2 passenger_count

esttab using "$dirout/taxi_reg.tex", label replace booktabs ///
title(Taxi Regression\label{tab1})



*ssc inst sepscatter
sepscatter trip_MPH passenger_count , sep(condition) mc(red blue) addplot(qfitci trip_MPH passenger_count if condition=="cloudy_rain", lc(red) || qfitci trip_MPH passenger_count if condition=="sunny", lc(blue)) legend(order(1 2))

graph export "$dirout/taxi_plot.pdf", replace


















