import json
import pandas as pd
from src.typeDefs.appConfig import IAppConfig

# initialize the app config global variable
appConf = {}

def getConfig(configFilename='config.xlsx') -> IAppConfig:
    """
    Get the application config from config.xlsx file
    Returns:
        IAppConfig: The application configuration as a dictionary
    """

    df = pd.read_excel(configFilename, header=None, index_col=0)
    #print(df)
    configDict = df[1].to_dict()
    return configDict


def loadAppConfig(fName="config.json"):
    # load config json into the global variable
    with open(fName) as f:
        global appConf
        appConf = json.load(f)
        return appConf
    
def getAppConfig():
    # get the cached application config object
    global appConf
    return appConf