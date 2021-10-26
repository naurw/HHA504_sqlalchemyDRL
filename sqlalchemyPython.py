#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 17:03:30 2021

@author: William
"""

import pandas as pd 
from sqlalchemy import create_engine
import sqlalchemy
from dotenv import load_dotenv
import os 


mysqluser = os.getenv('mysqluser')
mysqlpassword = os.getenv('mysqlpassword')

MYSQL_HOSTNAME = '20.62.193.224:3305'
MYSQL_USER = 'williamruan'
MYSQL_PASSWORD = 'williamruan2021'
MYSQL_DATABASE = 'synthea'

connection_string = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}/{MYSQL_DATABASE}'
engine = create_engine(connection_string)
print (engine.table_names())

### Way 1A - using engine.execute
engine.execute("SELECT * FROM allergies LIMIT 100").fetchall()

### Way 1B - using engine.execute wrapped in pd.DataFrame
tempTable = pd.DataFrame(engine.execute("SELECT * FROM allergies LIMIT 100").fetchall())

### Way 2A - using PANDAS function: read_sql OR readL_sql_table 
tempTable2 = pd.read_sql('SELECT * FROM allergies LIMIT 100', engine)

### Way 2B - using PANDAS function: read_sql OR readL_sql_table using variables to house
query = 'select * from allergies limit 100;'
tempTable3 = pd.read_sql(query, engine)

####################
####################
### PANDAS MERGE ###
####################
####################

### CREATE THE MSSQL QUERIES 
query1 = 'select * from patients;'
query2 = 'select * from allergies;'

patients = pd.read_sql(query1, engine)
len(patients)
patients.Id.nunique()
### 1171 unique patients; 1171 TOTAL 

allergies = pd.read_sql(query2, engine)
len(allergies)
allergies.PATIENT.nunique()
### 141 unique patients; 597 TOTAL

"""

select * 
from allergies <== table 1 
left join patients <== table 2 ==> table 1 will be ENRICHED with table 2 info 
on allergies.patient = patients.id; <== primary key 

"""

# =============================================================================
# DataFrame.merge(right, 
#                 how='inner', {'right','outer','cross', <== DEFAULT 'inner'}
#                 on=None, 
#                 left_on=None, 
#                 right_on=None, 
#                 left_index=False, 
#                 right_index=False, 
#                 sort=False, 
#                 suffixes=('_x', '_y'), 
#                 copy=True, 
#                 indicator=False, 
#                 validate=None)[source]
# =============================================================================
allergiesPatients = allergies.merge(patients, 
                                    how='left', 
                                    left_on= 'PATIENT', 
                                    right_on= 'Id')
len(allergiesPatients)
### Merging allergies means we are including ALL of the columns in allergies table 
### And then enriching with information that is shared from patients table 
## Therefore, total column return value is 597

"""

select * 
from patients 
left join allergies
on allergies.patient = patients.id; 

"""

patientsAllergies = patients.merge(allergies, how='left', left_on= 'Id', right_on= 'PATIENT')
len(patientsAllergies)
### Merging patients means we are including ALL of the columns in patients table 
### And then enriching with information that is shared from allergies table 
### BUT because allergies table has DUPLICATES based on the nunique() of that column
### Total column return table is 1627 = (1171 + 597) - 141 

#####################
#####################
### PANDAS CONCAT ### <== merging two tables together WITH the SAME COLUMNS to give additional rows
#####################
##################### (merging two tables together WITH the SAME COLUMNS to give additional rows)
df1 = patients.sample(10)
df2 = patients.sample(10)
df3 = pd.concat([df1, df2])

df4 = pd.concat([df1, allergies]) ## Forced two datasets together; did not match based on same columns <== AVOID
df5 = allergies.sample(10)
df6 = pd.concat([df1, df5]) ## Forced two datasets together; did not match based on same columns <== AVOID
