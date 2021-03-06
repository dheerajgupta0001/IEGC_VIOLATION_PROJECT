import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple
from src.typeDefs.iegcViolationFetcherSummary import IViolationMessageFetcherSummary


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

        try:
            connection = cx_Oracle.connect(self.connString)
            cursor = connection.cursor()

            sql_fetch = """ SELECT * FROM mis_warehouse.IEGC_VIOLATION_MESSAGE_DATA 
                        where (date_time BETWEEN TO_DATE(:col1, 'YYYY-MM-DD') and TO_DATE(:col2, 'YYYY-MM-DD'))
                        and not(entity='nan') 
                        order by date_time, message
                        """
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
            df = pd.read_sql(sql_fetch, params={
                             'col1': startDate, 'col2': endDate}, con=connection)

        except:
            print('Error while fetching data from db')
        finally:
            # closing database cursor and connection
            if cursor is not None:
                cursor.close()
            connection.close()
            print('closed db connection after iegc violation messages fetching')

        violMsgList: List[IViolationMessageFetcherSummary] = []
        for i in df.index:
            violMsg: IViolationMessageFetcherSummary = {
                'msgId': df['MESSAGE'][i],
                'date': dt.datetime.strftime(df['DATE_TIME'][i], "%Y-%m-%d"),
                'entity': df['ENTITY'][i],
                'schedule': int(round(df['SCHEDULE'][i])),
                'drawal': int(round(df['DRAWAL'][i])),
                'deviation': int(round(df['DEVIATION'][i]))
            }
            violMsgList.append(violMsg)
        return violMsgList
