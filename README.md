# Stibo UTC Datetime Validator

## Purpose

The purpose of this project is to compare an existing UTC datetime with a programmatically constructed and converted UTC datetime to see if they match. Please reach out to Cory Robinson (corobinson@mgmresorts.com) for any questions, comments, or feature requests. You can also submit a PR with whatever fixes/features you want to add.

## Function

This program takes in a database export Excel file from /project_root/data_files/input/ containing the following data points:

* ID (Column header "<ID>")
* Event UTC datetime (Column header "EventTz")
* Event standalone Date (Column header "Event Date")
* Event standalone time (Column header "Event Time")
* Property Timezone (Column header "Timezone")

NOTE: Column header values can be altered in report.py lines 17 - 21.

The program will parse the above data points and create two datetime objects for comparison:

1. The Stibo UTC datetime: This object is created by converting the "EventTz" column value into a UTC datetime object.
2. The converted UTC datetime: This object is created by constructing a datetime object from the "Event Date" and "Event Time" column values, localizing it to the timezone from the "Timezone" column value, and then converting that timezone aware datetime into a UTC datetime.

The program will then create a report in the form of an Excel file named "stibo_utc_validatedYYYY-mm-DDTHH-MM.xlsx" in the /project_root/data_files/output/ directory.

The report will contain the following fields:

* ID: The event ID
* Stibo UTC: The UTC datetime currently in the database.
* Converted Event UTC: The UTC datetime calculated by the Python program.
* Stibo Matches Converted: A Boolean stating whether Stibo UTC == Converted Event UTC.
* Event Date: The standalone YYYY-mm-DD date of the event (used for Converted Event UTC).
* Event Time: The standalone HH:MM:SS time of the event (used for Converted Event UTC).
* Property Timezone: This is the timezone of the property hosting the event (used for Converted Event UTC).

## Running the program

Place the database export Excel file into /data_files/input/ (file name does not matter). Currently only the first file in the directory will be used. Once the file is in place, you can run the program and look for the report in /data_files/output/.

## Altering runtime variables

Some values can be altered to effect some runtime operations such as which columns are read from the input Excel file, what the columns in the output Excel report are called, the directory where the output report goes, and the name of the output report.

### Editing input file columns

The data points needed cannot be altered but, the column header names where the data can be read from can be altered by editing the script directly. Go to report.py and edit the key values passed on lines 17 - 21.

### Editing output file columns

The data put into the output file will remain the same but the column header names can be edited. First go to report.py line 10 and edit the strings in the list for columns:List[str]=. Next go to report_entry.py and edit the String key values on lines 19 - 25.

Editing the names will not change what values are put there, just the column header name.

## Editing output report directory and/or file name

To edit the directory the output report is written to or the name of the file go to main.py line 13 and add to the .to_excel_file() function call:

* file_location="/path/"
* file_name="whatever_file_name"

Example: report.to_excel_file(file_location="c:\Users\Cory\Documents\", file_name="test_name")

The current datetime and .xlsx will always be added.