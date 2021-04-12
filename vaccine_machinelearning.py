import pandas as pd  # for DataFrames
import numpy as np  # for multi-dimensional arrays
import matplotlib  # for plotting and graphing
import sklearn  # Scikit-Learn, machine learning library that provides algorithms

# Libraries for combining csv files
import os
import glob

# Library for determining day of week
import datetime


# Machine Learning Python Tutorial: https://www.youtube.com/watch?v=7eh4d6sabA0&ab_channel=ProgrammingwithMosh
# 1. Import Data
# 2. Clean Data (no duplicates or irrelevant data, convert text to numerical values)
# 3. Split the Data into Training/Test Sets
# 4. Create a Model using Algorithm
# 5. Train the Model
# 6. Make Predictions
# 7. Evaluate Predictions and Improve

print("Hello world")


def combine_csv():
    # Tutorial: https://www.freecodecamp.org/news/how-to-combine-multiple-csv-files-with-8-lines-of-code-265183e0854/
    os.chdir("C:\\Users\\Travis\\Documents\\GitHub\\riVaccineApptScraper\\data")  # set mydir as the working directory
    if os.path.exists("combined_csv.csv"):
        os.remove("combined_csv.csv")  # delete the old csv
    else:
        print("The file does not exist")
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*{}'.format(extension))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])  # combine all files in the list
    combined_csv.to_csv("combined_csv.csv", index=False, encoding='utf-8-sig')  # export to csv
    print("Combined all csv files in Data folder")


def convert_date_to_weekday(date):
    # Reference: https://www.codespeedy.com/find-the-day-of-week-with-a-given-date-in-python/
    # Date is in format MM/DD/YYYY
    date = str(date)
    datelist = list(map(int, date.split('/')))  # outputs a integer list of [date, month, year]
    day_of_week = datetime.date(datelist[2], datelist[1], datelist[0]).weekday()  # returns integer (0 thru 6)

    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print(week_days[day_of_week])
    return day_of_week  # returns integer (0 - 6)


def mango():
    combine_csv()
    vaccdata = pd.read_csv('combined_csv.csv')  # dataframe from our csv file
    vaccdata = vaccdata.drop_duplicates()  # remove duplicates
    # We need an input set and an output set
    # I'm thinking input = [location, day of week]
    # output = [appointments]
    # vaccdata_X = [location, date]

    vaccdata_X = vaccdata.drop(columns=['Address', 'Vaccine', 'Appointments', 'Link', 'Time Accessed'])  # Input Set
    vaccdata_X['Date'] = convert_date_to_weekday(vaccdata_X['Date'].to_string(index=False))
    vaccdata_Y = vaccdata['Appointments']  # Output Set, only Appointments
    print(vaccdata_X)
    print(vaccdata_Y)


mango()

