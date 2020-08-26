from typing import List, Tuple, TypedDict
import cx_Oracle
from src.typeDefs.iegcViolationSummary import IViolationMessageSummary


class Outages(TypedDict):
    columns: List[str]
    rows: List[Tuple]


class IegcViolationSummaryRepo():
    """Repository class for transmission data
    """
    localConStr: str = ""

    def __init__(self, dbConStr: str) -> None:
        """constructor method
        Args:
            dbConf (DbConfig): database connection string
        """
        self.localConStr = dbConStr
        # print(dbConStr)

    def pushTransmissionRecord(self, iegcDataRecords: List[IViolationMessageSummary]) -> bool:
        """inserts iegc violation data into the app db
        Args:
            iegcDataRecords (List[IViolationMessageSummary]): iegc violation data to be inserted
        Returns:
            bool: returns true if process is ok
        """
        # get connection with raw data table
        connection = cx_Oracle.connect(self.localConStr)

        isInsertSuccess = True
        if len(iegcDataRecords) == 0:
            return isInsertSuccess
        try:
            # keyNames names of the raw data
            keyNames = ['Message no.', 'Date', 'Entity1',
                        'Schedule1', 'Drawal1', 'Deviation1']
            colNames = ['MESSAGE', 'DATE_TIME', 'ENTITY',
                        'SCHEDULE', 'DRAWAL', 'DEVIATION']
            # get cursor for raw data table
            cursor = connection.cursor()
            # print("connection version :{0}".format(connection.version))

            # text for sql place holders
            sqlPlceHldrsTxt = ','.join([':{0}'.format(x+1)
                                        for x in range(len(keyNames))])

            # delete the rows which are already present
            existingIegcViolationData = [(x['Date'], )
                                         for x in iegcDataRecords]
            # print(existingIegcViolationData)
            # print(type(iegcDataRecords))
            cursor.executemany(
                "delete from mis_warehouse.iegc_violation_message_data where DATE_TIME=:1", existingIegcViolationData)

            # insert the raw data
            sql_insert = "insert into mis_warehouse.iegc_violation_message_data({0}) values ({1})".format(
                ','.join(colNames), sqlPlceHldrsTxt)

            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
            cursor.executemany(sql_insert, [tuple(
                [r[col] for col in keyNames]) for r in iegcDataRecords])

            # commit the changes
            connection.commit()
        except Exception as e:
            isInsertSuccess = False
            print(
                'Error while bulk insertion of transmission constraints data into database')
            print(e)
        finally:
            # closing database cursor and connection
            if cursor is not None:
                cursor.close()
            connection.close()

        return isInsertSuccess
