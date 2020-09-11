# %%
import pandas as pd
import datetime as dt
from src.config.appConfig import getConfig
from src.fetchers.significanceViolationFetcher import fetchIegcViolationData, getIegcViolationMsgsFilePath
from src.repos.insertViolationData import IegcViolationSummaryRepo

# %%
appConfig = getConfig()
violationMsgsFolderPath = appConfig['violationDataFolder']
violationMsgsFilePath = getIegcViolationMsgsFilePath(violationMsgsFolderPath)

appDbConnStr = appConfig['appDbConStr']
iegcViolationData = fetchIegcViolationData(violationMsgsFilePath)

# get the instance of IEGC violation repository
iegcDataRepo = IegcViolationSummaryRepo(appDbConnStr)
# %%
# pushing Transmission constraints Data to database
isInsSuccess = iegcDataRepo.pushViolationMessages(iegcViolationData)
if isInsSuccess:
    print("IEGC violation data insertion successful")
else:
    print("IEGC violation data insertion UNsuccessful")

# %%
