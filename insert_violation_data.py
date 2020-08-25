#%%
import cx_Oracle

#%%

def pushViolationData(df, connStr):
    print(connStr)
    # prepare list of angle data
    #print(df['% violation'])
    df['Schedule1'] = df['Schedule1'].apply(lambda x: round(x,0))
    df['Drawal1'] = df['Drawal1'].apply(lambda x: round(x,0))
    df['Deviation1'] = df['Deviation1'].apply(lambda x: round(x,0))
    df['Date'] = df['Date'].astype(str)
    df['Entity1'] = df['Entity1'].astype(str)
    df['Schedule1'] = df['Schedule1'].astype(str)
    df['Drawal1'] = df['Drawal1'].astype(str)
    df['Deviation1'] = df['Deviation1'].astype(str)
    recrd= df.to_records(index=False)
    data= list(recrd)
    #print(data)

    # create connection to database for pushing records
    con= cx_Oracle.connect(connStr)
    cursor= con.cursor()
    print(con.version)

    insert_sql = "INSERT INTO IEGC_VIOLATION_DATA(Message,DATE_TIME,Entity,SCHEDULE,DRAWAL,DEVIATION) VALUES(:col1,:col2,:col3,:col4,:col5,:col6)"
    cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
    
    cursor.executemany(insert_sql, data)
    # closing the connection
    con.commit()
    print("Record Inserted")
    cursor.close()
    con.close()


# %%
