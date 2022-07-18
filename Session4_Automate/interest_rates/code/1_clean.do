*************
* Automate Cleaning a Dataset
*************

clear all
set more off

* Install the filelist module
/// ssc install filelist

* Set working directory
global dirin = "~/workshop_2022/Session4_Automate/interest_rates/data/raw"
global dirout = "~/workshop_2022/Session4_Automate/interest_rates/data"

* Automate Fixes
insheet using "$dirin/ir2000.csv", comma clear

foreach var of varlist * {
   rename `var' `=`var'[1]'
}
drop in 1 
destring, replace 


* Remove all rows with header values
drop if Month == "Month"

* Check all prime rates for errors at once
destring Prime_Rate, replace
replace Prime_Rate = Prime_Rate * 10 if (Prime_Rate < 1)

* replace NDs with NAs
replace Treasury_Rate_3_Month = "" if (Treasury_Rate_3_Month == "ND")

* save results
save "$dirout/ir2000_new.dta"



* In Class Exercise: 
* Use regex to automate separating the year and month from the "Month" variable.
* Then sort the dataset by year and month before saving. 
* HINT: I like the regexs command in stata












* Potential Solution
gen Year = regexs(0) if(regexm(Month, "^[0-9][0-9][0-9][0-9]"))
replace Month = regexs(0) if(regexm(Month, "-[0-9][0-9]$"))
replace Month = subinstr(Month,"-", "", .)







