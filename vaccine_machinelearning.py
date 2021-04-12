import pandas as pd  # for DataFrames
import numpy as np  # for multi-dimensional arrays
import matplotlib  # for plotting and graphing
from sklearn.tree import DecisionTreeClassifier  # Scikit-Learn, machine learning library that provides algorithms
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

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
    # print("Converting to weekday")
    # Reference: https://www.codespeedy.com/find-the-day-of-week-with-a-given-date-in-python/
    # Date is in format MM/DD/YYYY
    date = str(date)
    datelist = list(map(int, date.split('/')))  # outputs a integer list of [date, month, year]
    day_of_week = datetime.date(datelist[2], datelist[0], datelist[1]).weekday()  # returns integer (0 thru 6)

    # week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # print(week_days[day_of_week])
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

    locationSet = set(vaccdata_X['Location'])  # Set of every unique Location name
    locationList = list(locationSet)  # List of every unique Location

    for index, row in vaccdata_X.iterrows():  # Go through each row of the dataframe
        row['Location'] = locationList.index(row['Location'])   # Convert each location to the index of locationSet
        row['Date'] = convert_date_to_weekday(row['Date'])  # Convert each date to weekday int
    # Input set now consists of [index of location, day of week (int between 0 and 6)]

    vaccdata_Y = vaccdata['Appointments']  # Output Set, only Appointments

    """# split data into training and testing sets
    # test_size determines how much of the train data to save for testing
    x_train, x_test, y_train, y_test = train_test_split(vaccdata_X, vaccdata_Y, test_size=0.2)

    # This is where we train the model, which we do not want to do every time
    model = DecisionTreeClassifier()  # sklearn model
    model.fit(x_train, y_train)  # pass only the training sets

    print("Dumping Model")
    joblib.dump(model, 'weeklyvaccdata.joblib')"""

    location1 = locationList.index('Sockanosset POD ')
    model = joblib.load('weeklyvaccdata.joblib')
    predictions = model.predict([[location1, 4]])
    print(predictions)

    """# Manual machine learning test with our input
    location1 = locationList.index('Sockanosset POD ')
    # location2 = locationList.index('Woonsocket POD')
    print("Predicting # of Appts at", locationList[location1], "for every weekday")
    predictions = model.predict([[location1, 0], [location1, 1], [location1, 2], [location1, 3], [location1, 4], [location1, 5], [location1, 6]])
    print(predictions)

    predictions = model.predict(x_test)  # predict using the test set

    score = accuracy_score(y_test, predictions)  # how accurate the machine learning is (this varies every time)

    print(round(score, 3), "% Accuracy")"""
# End of machine learning function


def see_predicted_week(location):
    """

    :param location: string - will need to lstrip and rstrip
    :return: plot of predicted number of appts over the 7 days of the week
    """

    # hey figure out how to run this twice a day

    return plot


# Main testing
mango()

