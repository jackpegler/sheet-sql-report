### Connect to Google API
import gspread
from oauth2client.service_account import ServiceAccountCredentials

### Connect to mzee
from sqlalchemy import create_engine

### General Libraries
import pandas as pd

class SheetToSQL():

    def __init__(self, google_cloud_credentials, sql_connection):
        """Class to sync a table in a SQL database with data in a Google Sheet

        Attributes:
            google_cloud_credentials (JSON file) stores our access credentials to google cloud
            sql_connection (String) stores the connection info for the database for use in sql_academy.create_engine().
                                    dialect+driver://username:password@host:port/database


        """
        ### TODO: COULD MAKE THE CREDENTIALS OPTIONAL? LET HAVE METHOD TO ADD LATER? (POINTLESS?)
        ### TODO: REFACTOR TO MAKE SURE
        self.gc_credentials = google_cloud_credentials
        self.sql_connection = sql_connection

    ### ADD FUNCTION TO ADD THE CONNECTION DETAILS THEN LET JUST ADD ONE/NEITHER IN INIT
    ### SHOULD THE WHOLE THING JUST FULLY INHERIT FROM GSPREAD?

    def get_gheet_data(self, workbook_name, sheet_name, cell=False):
        """Method to connect to and grab data from the google sheet. If cell supplied grabs just that cell
           otherwise defaults to get all the data in the sheet

        Args:
            - gc_credentials: a JSON file of the access creddentials for the Google API. Need to use the Google Cloud website to set up a project for this and generate the creddentials
            - worksheet_name: the name of our Google Sheet that has the data we want
            - cell: a sting with the cell to pull the data from e.g. 'A2'

        Returns:
            - data: if Cell supplied is a string otherwise is a pandas dataframe


        """

        ### USE SAVED CREDENTIALS TO CONNECT TO THE GOOGLE SHEETS API
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.gc_credentials, scope)
        ### TODO: error handling if can't connect
        gc = gspread.authorize(credentials)

        ### OPEN THE RELEVANT GOOGLE SHEET AND LOAD INTO A DATAFRAME
        ### TODO: add exception to remind to give access to the sheet
        wks = gc.open(workbook_name).worksheet(sheet_name)

        ### TODO: GIVE OPTION TO ONLY GET CERTAIN DATA
        if not cell:
            raw_data = wks.get_all_values()
            headers = raw_data.pop(0)
            data = pd.DataFrame(raw_data, columns=headers)
            print("Successfully pulled {0} records from {1}-{2}".format(len(data), workbook_name, sheet_name))

        else:
            data = wks.acell(cell).value

        ### RETURN A DATAFRAME FILLED WITH THE DATA FROM OUR GOOGLE SHEET
        return data

    def get_sql_data(self, query):
        """Method to connect to SQL database, query it and return the result

        Args:
            - query: a string containing the query to run on the database. Careful of certain characters that need to be different for Python e.g. % -> %%

        Returns:
            - df_result: a dataframe containing the result of the query

        """
        ## read sql method
        engine = create_engine(self.sql_connection)
        df_result = pd.read_sql(query,con=engine)

        print("Successfully pulled {0} records".format(len(df_result)))

        return df_result

    def data_to_sql(self, df, db_schema, db_table):
        ### TODO: MORE DESCRIPTIVE NAME? LIKE DATA TO SQL?
        """Method to feed the data to mzee

        # https://stackoverflow.com/questions/48006551/speeding-up-pandas-dataframe-to-sql-with-fast-executemany-of-pyodbc
        # https://stackoverflow.com/questions/23103962/how-to-write-dataframe-to-postgres-table

        Args:
            - db_table (string): is name of the target table in the database
            - db_schema (string): is name of the target schema in the database
            - df (dataframe): data to feed to the database

        Returns:
            - none
        """

        ### CONNECT TO OUR DATA BASE AND REPLACE THE EXISTING SQL TABLE WITH OUR GSHEET DATA
        ### TODO: ALLOW TO APPEND DATA NOT JUST REPLACE
        engine = create_engine(self.sql_connection)
        df.to_sql(db_table, schema=db_schema, con=engine, if_exists='replace', index=False, method="multi")
        ### TODO: CLOSE THE SQL ENGINE? OR GIVE OPTION TO LEAVE OPEN? MAYBE SHOULD BE OTHER METHODS SO CAN USE SAME ENGINE TWICE

        print("Successfully added {0} records to {1}.{2}".format(len(df), db_schema, db_table))

    def data_to_gsheet(self, df_data, workbook_name, sheet_name, starting_cell = 'A2'):
        """Method to clear the data in a gsheet and update with new data

        Args:
            - df_data (dataframe): the new data to add to the google sheet
            - workbook_name (string): the name of the workbook to update
            - sheet_name (string): the name of the worksheet to update
            - starting_cell (string): the cell location to input the new data. Defualt at A2
        """
        ### TODO: REFACTOR TO CONNECT HAVE METHOD TO CONNECT TO THE GSHEET
        ### USE SAVED CREDENTIALS TO CONNECT TO THE GOOGLE SHEETS API
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.gc_credentials, scope)
        gc = gspread.authorize(credentials)

        ### OPEN THE RELEVANT GOOGLE SHEET AND CLEAR OLD DATA
        wkb = gc.open(workbook_name)
        wkb.values_clear("'{}'!A2:AZ70001".format(sheet_name))

        ### TODO: GIVE OPTION TO USE HEADERS
        ### INSERT NEW DATA INTO THE SHEET
        wks = wkb.worksheet(sheet_name)
        wks.update(starting_cell, df_data.values.tolist())

        print("Successfully updated data in {0}-{1} at Cell {2}".format(workbook_name, sheet_name, starting_cell))
