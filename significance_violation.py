# %%
import pandas as pd
from appConfig import getConfig
from insert_violation_data import pushViolationData

#%%
#df = pd.read_excel('Significant Violation of IEGC.xlsx')
violationData, connStr= getConfig('violationData','connStr')
df = pd.read_excel(violationData)
print(violationData)


# %%
# get the cells from 9 to 13 row indexes but all columns
count =0
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

# %%
pushViolationData(data_final, connStr)