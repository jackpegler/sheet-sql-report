# sheet-sql-report
Inspired by a need for this kind of inter-functionality I've seen in my own work, this is python package to help anyone to make use of their data stored in google sheets and SQL databases.

## Features
* connect to google sheets or sql (tested on redshift, but should work for more) as datasource
* `get_gheet_data(workbook_name, sheet_name, cell=False)` grab data from entire sheet or selected cell
* `sql_query(query)` run (no result) queries in a database
* `get_sql_data(self, query)` query the SQL database and return data as pandas dataframe
* `data_to_sql(df, db_schema, db_table, delete_old = True)` insert data into a sql database
* `data_to_gsheet(self, df_data, workbook_name, sheet_name, starting_cell = 'A2')` insert data into a google sheet


## Requirements

### Connecting to Google SheetToSQL
You'll need to make sure to:
1. Enable access to Google Sheets by enabling API access / generating a JSON key that you store in the project where you're working. Follow [these instructions](https://gspread.readthedocs.io/en/latest/oauth2.html#service-account) to set up access and download the `.json` credentials
2. Make sure that the `client_email` address (in the `.json` file) has been granted edit access to the google sheets you want to access with your program

When supplying the credentials it should be in format of a string with the path to the `.json` credentials file


### Connecting to SQL databases
You can only connect to databases that you already have access to, obviously :D. So first need to make sure to get login details from the database administrator. To connect you need the details as a string the format `dialect+driver://username:password@host:port/database` (driver not always needed can just supply as `postgresql` for example)

## Installation and import

To install simply use `pip install sheet-to-sql`

Then to use in your project simply import using `import sheet_sql_report`

## Getting Started

### Configure connection to datasources
To work with the **sheet-sql_report** package you first need to create a `SheetToSQL` object. You can initialise with connection info for Google and SQL - Both, either or neither; although the connection info is needed to run other methods.
The `SheetToSQL()` object takes two optional arguments:

* **google_cloud_credentials** which is a string with a path to your gcloud JSON credentails file
* **sql_connection** a string of your database connection info as described above (*dialect+driver://username:password@host:port/database*)

#### Updating connection info
To update the connection info, either if you didn't add at the start or want to switch databases/google logins you can use:
* `update_google_details()`
* `update_sql_connection()`

### Grab data from google Sheet
`get_gheet_data(workbook_name, sheet_name, cell=False)`
* **worksheet_name**: the name of our Google Sheet that has the data we want
* **sheet_name**: name of the sheet within the workbook we want to access
* **cell**: (OPTIONAL) a sting with the cell to pull the data from e.g. 'A2' otherwise pulls whole sheet

### Grab data from sql
`sql_query(query)`
* **query (string)** a string containing the query to run on the database w/o returning data. Careful of certain characters that need to be different for Python e.g. % -> %%

`get_sql_data(query)`
* **query (string)**: a string containing the query to run on the database and return data. Careful of certain characters that need to be different for Python e.g. % -> %%

### add data to google sheet
`data_to_gsheet(df_data, workbook_name, sheet_name, starting_cell = 'A2')`
* **df_data (dataframe)**: the new data to add to the google sheet
* **workbook_name (string)**: the name of the workbook to update
* **sheet_name (string)**: the name of the worksheet to update
* **starting_cell (string)**: the cell location to input the new data. Defualt at A2

### add data to sql
`data_to_sql(df, db_schema, db_table, delete_old = True)`
* **df (dataframe)**: data to feed to the database
* **db_table (string)**: is name of the target table in the database
* **db_schema (string)**: is name of the target schema in the database
* **delete_old (bool)**: if True then will delete old data and replace with new, otherwise append
