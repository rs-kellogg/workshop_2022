###################################
### Automate Cleaning a Dataset ###
###################################
# Clear Workspace
rm(list=ls())

# Set Working Directory
setwd("~/workshop_2022/Session4_Automate/interest_rates/data/raw")

# Install and load necessary libraries
if(!require("dplyr")) install.packages("dplyr")
if(!require("fs")) install.packages("fs")
if(!require("stringr")) install.packages("stringr")

#load packages
library(dplyr)
library(fs)
library(stringr)


#########################################
# Individualized Fixes

# Read in one File
ir2000 <- read.csv("ir2000.csv", encoding="UTF-8", header=TRUE)

# Change one Value - The interest rate in April 2021 is off by a decimal
print(ir2000[11,4])
ir2000[11,4] <- 7.8

# Remove an Extra Header Row
print(ir2000[7,])
ir2000 <- ir2000[-7,]

# Change NDs to NAs
print(ir2000[23,5])
ir2000[23,5] <- NA

# Save Results
#setwd("~/workshop_2022/Session4_Automate/interest_rates/data")
#write.csv(ir2000, file="ir2000_new.csv", row.names=FALSE)
rm(ir2000)

########################
# Generalizing Changes

# read in all data files
filenames <- dir_ls(glob = "*.csv") %>% as.character() %>% sort()
filenames

# combine datasets
ir <- data.frame()
for (filename in filenames){
  ir_add <- read.table(filename, header = TRUE, sep = ",", quote = "\"", comment.char = "")
  ir <- rbind(ir, ir_add)
}
rm(ir_add, filename, filenames)

# Remove all rows with header values
ir <- ir[ir$Month != "Month",] 


# check all prime rates for errors at once
class(ir$Prime_Rate)
ir$Prime_Rate <- as.numeric(ir$Prime_Rate)
ir$Prime_Rate <- ifelse(((lead(ir$Prime_Rate)/ir$Prime_Rate)-1) > 1, 
                         ir$Prime_Rate*10,
                         ir$Prime_Rate)

print(ir[10,4]) # check if error is corrected

# replace NDs with NAs
ir$Treasury_Rate_3_Month <- ifelse(ir$Treasury_Rate_3_Month=="ND",
                                   NA,
                                   ir$Treasury_Rate_3_Month)

# Save Results
setwd("~/workshop_2022/Session4_Automate/interest_rates/data")
write.csv(ir, file="interest_rate_update.csv", row.names=FALSE)

# Return a Message when file is run to completion
print("Sucessfully cleaned interest rate data.")

######################
# In Class Exercise: 
######################
# Use regex to automate separating the year and month from the "Month" variable.
# Then sort the dataset by year and month before saving. 
# HINT: I like the "stringr" library.












######################
# Potential Solution: 
######################
ir$Year <- str_extract(ir$Month, "\\d{4}")
ir$Month <- str_match(ir$Month, "-(\\d{2})")[,2]
ir <- ir[order(ir$Year, ir$Month),]
write.csv(ir, file="interest_rate_update.csv", row.names=FALSE)




