import datetime as dt
from src.typeDefs.iegcViolationSummary import IViolationMessageSummary
from typing import List
import os
import pandas as pd


def fetchIegcViolationData(iegcViolationDataFolderPath: str) -> List[IViolationMessageSummary]:
    """fetched transmission constraint data for a quarter
    Args:
        targetDt (dt.datetime): date for which quarter is to be extracted
    Returns:
        List[IPairAngleSummary]: list of transmission records fetched from the excel data
    """
    # sample excel filename - Transmission Constraints.xlsx
    #fileDateStr = dt.datetime.strftime(targetDt, '%d_%m_%Y')
    targetFilename = 'Significant Violation of IEGC.xlsx'
    targetFilePath = os.path.join(iegcViolationDataFolderPath, targetFilename)
    #print("transmission file :{0}".format(targetFilePath))

    # check if excel file is present
    if not os.path.isfile(targetFilePath):
        return []

    # read excel file
    df = pd.read_excel(targetFilePath)
    
    # test start
    data= pd.DataFrame()
    print(type(data))
    for i in range(df.shape[0]):
        dfSubset = df.iloc[i:i+1, :]
        #print("row= {0}".format(i))
        df1=dfSubset[['Message no.','Date','Entity1','Schedule1','Drawal1','Deviation1']]
        if not (pd.isnull(dfSubset['Entity2'].iloc[0])):
            #print("value present")
            df2=dfSubset[['Message no.', 'Date','Entity2','Schedule2','Drawal2','Deviation2']]
            df2.rename(columns={'Entity2': 'Entity1'}, inplace=True)
            df2.rename(columns={'Schedule2': 'Schedule1'}, inplace=True)
            df2.rename(columns={'Drawal2': 'Drawal1'}, inplace=True)
            df2.rename(columns={'Deviation2': 'Deviation1'}, inplace=True)
            df3=df1.append(df2,ignore_index=True,verify_integrity=False,sort=None)
            #print(df1)
            if not (pd.isnull(dfSubset['Entity3'].iloc[0])):
                #print("value present")
                df2=dfSubset[['Message no.', 'Date','Entity3','Schedule3','Drawal3','Deviation3']]
                df2.rename(columns={'Entity3': 'Entity1'}, inplace=True)
                df2.rename(columns={'Schedule3': 'Schedule1'}, inplace=True)
                df2.rename(columns={'Drawal3': 'Drawal1'}, inplace=True)
                df2.rename(columns={'Deviation3': 'Deviation1'}, inplace=True)
                df3=df3.append(df2,ignore_index=True,verify_integrity=False,sort=None)
                #print(df1)
                if not (pd.isnull(dfSubset['Entity4'].iloc[0])):
                    #print("value present")
                    df2=dfSubset[['Message no.', 'Date','Entity4','Schedule4','Drawal4','Deviation4']]
                    df2.rename(columns={'Entity4': 'Entity1'}, inplace=True)
                    df2.rename(columns={'Schedule4': 'Schedule1'}, inplace=True)
                    df2.rename(columns={'Drawal4': 'Drawal1'}, inplace=True)
                    df2.rename(columns={'Deviation4': 'Deviation1'}, inplace=True)
                    df3=df3.append(df2,ignore_index=True,verify_integrity=False,sort=None)
                    #print(df1)
        else:
            #print("value not present")
            df3=df1
            #print(df3)

        data=data.append(df3,ignore_index=True,verify_integrity=False,sort=None)
    #print(data)
    data_final= data.drop_duplicates(subset=['Message no.', 'Date','Entity1'], keep='last', ignore_index=True)
    #print(data_final)
    print(data_final.columns)
    # test done
    
    # convert nan to None
    data_final = data_final.where(pd.notnull(data_final), None)

    # convert dataframe to list of dictionaries
    iegcViolationRecords = data_final.to_dict('records')
    #print(iegcViolationRecords.columns)

    return iegcViolationRecords