# sheet-sql-report
Inspired by a need for this kind of inter-functionality I've seen in my own work, this is python package to help anyone to make use of their data stored in google sheets and SQL databases.

## Features
* connect to google sheets or sql (tested on redshift, but should work for more) as datasource
* `get_gheet_data(workbook_name, sheet_name, cell=False)` grab data from entire sheet or selected cell
* `get_sql_data(self, query)` query the SQL database and return data as pandas dataframe
* `data_to_sql(df, db_schema, db_table)` insert data into a sql database
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

## How To:

### Configure connection to datasources

### Grab data from google Sheet

### Grab data from sql

### add data to google sheet

### add data to sql 
