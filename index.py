# %%
import pandas as pd
import datetime as dt
from src.config.appConfig import getConfig
from src.fetchers.significanceViolationFetcher import fetchIegcViolationData
from src.repos.insertViolationData import IegcViolationSummaryRepo

# %%
appConfig = getConfig()
# print(appConfig)
# create outages raw data between start and end dates
systemConstraintFolderPath = appConfig['violationDataFolder']
appDbConnStr = appConfig['appDbConStr']

iegcViolationData = fetchIegcViolationData(systemConstraintFolderPath)

# get the instance of IEGC violation repository
iegcDataRepo = IegcViolationSummaryRepo(appDbConnStr)
#%%
# pushing Transmission constraints Data to database
isInsSuccess = iegcDataRepo.pushTransmissionRecord(iegcViolationData)
if isInsSuccess:
    print("IEGC violation data insertion successful")
else:
    print("IEGC violation data insertion UNsuccessful")

# %%
