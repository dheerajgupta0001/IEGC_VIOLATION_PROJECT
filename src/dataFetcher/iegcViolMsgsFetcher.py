import cx_Oracle
import psycopg2
import pandas as pd
import datetime as dt
from typing import List, Tuple
from src.typeDefs.iegcViolationFetcherSummary import IViolationMessageFetcherSummary
from src.config.appConfig import getAppConfig
from psycopg2 import extras

class IegcViolMsgsFetcher():
    """This class fetches iegc violation messages for UI
    """

    def __init__(self, con_string: str):
        """constructor method
        Args:
            con_string ([str]): connection string
        """

        self.connString = con_string

    def fetchIegcViolMsgs(self, startDate: dt.datetime, endDate: dt.datetime) -> List[IViolationMessageFetcherSummary]:
        """fetch derived frequency from mis_warehouse db 
        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        Returns:
            List[IViolationMessageFetcherSummary]: List of IEGC violation messages for UI
        """
        dbConfig = getAppConfig()
        dbConn = None
        dbCur = None

        try:
            dbConn = psycopg2.connect(host=dbConfig['db_host'], dbname=dbConfig['db_name'],
                                      user=dbConfig['db_username'], password=dbConfig['db_password'])
            dbCur = dbConn.cursor()

            # sqlTxt = 'SELECT t1."msgId", t1."time_stamp" as date, t2."name" as entity, t2.schedule, t2.drawal FROM sch_drwl_viol_msgs t1 LEFT JOIN sch_drwl_viol_rows t2 ON t1."Id"  = t2."msgLogId" where t1.time_stamp BETWEEN %(col1)s AND %(col2)s order by date, t1."msgId"'
            params = {'col1': startDate, 'col2': endDate}
            sqlTxt = """
                    SELECT 
                    t1."msgId", 
                    t1."time_stamp" AS date, 
                    t2."name" AS entity, 
                    t2.schedule, 
                    t2.drawal 
                    FROM 
                    sch_drwl_viol_msgs t1 
                    LEFT JOIN sch_drwl_viol_rows t2 ON t1."Id" = t2."msgLogId" 
                    WHERE 
                    t1.time_stamp BETWEEN %(col1)s AND %(col2)s 
                    ORDER BY 
                    date, 
                    t1."msgId"
                """

            df = pd.read_sql(sqlTxt, params=params, con=dbConn)
            # df = pd.read_sql(sqlTxt, params=[startDate, endDate], con=dbConn)
            # print(df)

        except Exception as ex:
            print(ex)
            print('Error while fetching data from db')
        finally:
            # closing database cursor and connection
            if dbCur is not None:
                dbCur.close()
            dbConn.close()
            print('closed db connection after iegc violation messages fetching')

        violMsgList: List[IViolationMessageFetcherSummary] = []
        for i in df.index:
            violMsg: IViolationMessageFetcherSummary = {
                'msgId': df['msgId'][i],
                'date': dt.datetime.strftime(df['date'][i], "%Y-%m-%d"),
                'entity': df['entity'][i],
                'schedule': int(round(df['schedule'][i])),
                'drawal': int(round(df['drawal'][i])),
                'deviation': int(round(df['schedule'][i] - df['drawal'][i]))
            }
            violMsgList.append(violMsg)
        return violMsgList
