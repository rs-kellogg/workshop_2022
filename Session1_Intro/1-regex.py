import re
import os

# Loop over 10-K files for year 2021
for filename in os.listdir("/kellogg/data/EDGAR/10-K/2021"):
    f = os.path.join("/kellogg/data/EDGAR/10-K/2021", filename)
    if os.path.isfile(f):
        with open(f, 'r') as file:
            text = file.read()

            name = ""
            cik  = ""
            zip  = ""

            name_r = re.compile('COMPANY CONFORMED NAME:\s+(.*)\s*\n')
            cik_r  = re.compile('CENTRAL INDEX KEY:\s+(\d+)\s*\n')
            zip_r  = re.compile('ZIP:\s+(\d{5}).*\n')

            if re.search(name_r, text):
                name = re.search(name_r, text).group(1)

            if re.search(cik_r, text):
                cik  = re.search(cik_r, text).group(1)

            if re.search(zip_r, text):
                zip  = re.search(zip_r, text).group(1)
 
            print(name,cik,zip)

            #print(text)

            

