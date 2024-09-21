Project's Title: ETL Task

Project Description: Write a Python program that scrapes all Hockey Team Stats starting from this page: https://www.scrapethissite.com/pages/forms/. Make sure to get all data for all subpages.


Dependencies: This applications requires some libraries installed to run the task. The dependent libraries are mentioned in file 'requirements.txt' in projects parent directory.


How to Install and Run the Project:
Setup and running the application:
1. Go to project directory (i.e Scrapping)
2. Run 'python -m pip install -r requirements.txt' to install the dependencies
3. Run 'py main.py' to perform the scrapping task.

Outputs:
The application generates 2 notable outputs:
1. A zip file named 'ZipFile.zip' that contains all the webpages HTMLs where the data is scrapped from.
2. An excel workbook named 'excel_file.xls' that contains 2 sheets, named "NHL Stats 1990-2011" (containing the data scrapped from webpages in raw form) and another sheet named "Winner and Loser per Year" that contains yearwise winning and losing teams and their total wins.

Running testcases:
The test cases are defined in file named 'test_main.py'. To run the test cases, run command 'pytest' in project directory.
