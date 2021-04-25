import pandas as pd  # for DataFrames
import numpy as np  # for multi-dimensional arrays
from matplotlib import pyplot as plt  # for plotting and graphing
from sklearn.tree import DecisionTreeClassifier  # Scikit-Learn, machine learning library that provides algorithms
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import tree
import graphviz
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

# Global Variables
locationList = []


def combine_csv():
    # Tutorial: https://www.freecodecamp.org/news/how-to-combine-multiple-csv-files-with-8-lines-of-code-265183e0854/
    os.chdir("C:\\Users\\Travis\\Documents\\GitHub\\riVaccineApptScraper\\data")  # set mydir as the working directory
    if os.path.exists("combined_csv.csv"):
        os.remove("combined_csv.csv")  # delete the old csv
    else:
        print("The file does not exist")
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*{}'.format(extension))]  # all csv files
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])  # combine all files in the list
    combined_csv.to_csv("combined_csv.csv", index=False, encoding='utf-8-sig')  # export to csv
    print("Combined all csv files in Data folder")
# End of combining csv file function


def convert_date_to_weekday(date):
    # Reference: https://www.codespeedy.com/find-the-day-of-week-with-a-given-date-in-python/
    date = str(date)  # Date is in format MM/DD/YYYY
    datelist = list(map(int, date.split('/')))  # outputs a integer list of [date, month, year]
    day_of_week = datetime.date(datelist[2], datelist[0], datelist[1]).weekday()  # returns integer (0 thru 6)
    # week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return day_of_week  # returns integer (0 - 6)
# End of convert date to weekday function


def generate_model_location_weekday():
    """
    Generates a .joblib machine learning tree model to predict appts given a location and weekday
    Prints the accuracy of the model from testing 20% of the input data
    """
    combine_csv()  # Combine all data csv's in data folder
    vaccdata = pd.read_csv('combined_csv.csv')  # dataframe from our csv file
    vaccdata = vaccdata.drop_duplicates()  # remove duplicates

    # The input set (X), columns [Location, Date]
    vaccdata_X = vaccdata.drop(columns=['Address', 'Vaccine', 'Appointments', 'Link', 'Time Accessed'])  # Input Set

    # Our inputs into the machine learning algorithm have to be floats or integers
    global locationList
    locationSet = set(vaccdata_X['Location'])  # Set of every unique Location name
    locationList = list(locationSet)  # List of every unique Location
    for x in range(len(locationList) - 1):
        locationList[x] = str(locationList[x]).rstrip()  # some location names still have random spaces after
    # We will use the index of the string in the list of locations to represent the location

    for index, row in vaccdata_X.iterrows():  # Go through each row of the dataframe
        row['Location'] = row['Location'].rstrip()  # This dataframe wasn't impacted by the above rstrip()
        row['Location'] = locationList.index(row['Location'])   # Convert each location to the index of locationList
        row['Date'] = convert_date_to_weekday(row['Date'])  # Convert each date to weekday int
    # Input set (X) now consists of [index of location, day of week (int between 0 and 6)]

    # We are trying to see what the predicted number of appointments are when we input a Location and Weekday
    vaccdata_Y = vaccdata['Appointments']  # Output Set, only Appointments

    # split data into training and testing sets
    # test_size determines how much of the train data to save for testing
    x_train, x_test, y_train, y_test = train_test_split(vaccdata_X, vaccdata_Y, test_size=0.2)

    # This is where we train the model, which we do not want to do every time
    model = DecisionTreeClassifier()  # sklearn model
    model.fit(x_train, y_train)  # pass only the training sets

    predictions = model.predict(x_test)  # predict using the test set
    score = accuracy_score(y_test, predictions)  # how accurate the machine learning is (this varies every model)
    print(round(score, 3), "% Machine Learinging Model Accuracy")

    joblib.dump(model, 'weeklyvaccdata.joblib')  # save the machine learning model to the data folder

    # Visualizing the tree. This outputs a dot file which you can visualize using addons for Visual Studio
    # I don't have Visual Studio yet so I just got a dot Online Graphviz thing to output an image
    tree.export_graphviz(model, out_file='weeklyvaccdata.dot', feature_names=['Location', 'Date'], class_names=str(sorted(vaccdata_Y.unique())), label='all', rounded=True, filled=True)
# End of machine learning model generation


def predict_appointment(location_name, weekday):
    """
    Predicts number of appts given location and weekday using the model generated in generate_model_location_weekday()
    :param location_name: string, already rstripped()
    :param weekday: int of weekday (0 to 6)
    :return: int of ammount of appts predicted
    """
    global locationList
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    location1 = locationList.index(str(location_name))  # set location1 to the index of the name of the location
    # weekday_int = week_days.index(str(weekday))
    model = joblib.load('weeklyvaccdata.joblib')
    predictions = model.predict([[location1, weekday]])  # predict and store results in a list
    print("Predicting", locationList[location1], "on", week_days[weekday], ":", str(predictions[0]), "appts")
    return predictions[0]  # return the 1 item in the predicted list
# End of machine learning prediction function


def see_predicted_week(location):
    """
    Predict the number of appts for a location for every day of the week, and plot it
    :param location: string - will need to lstrip and rstrip
    :return: plot of predicted number of appts over the 7 days of the week
    """
    location = str(location)
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    this_week_predicted = []
    for x in range(len(week_days)):
        this_week_predicted.append(predict_appointment(location, x))  # predict for every weekday
    predicted_plot = plt.plot(week_days, this_week_predicted, marker='o')  # plot the week's predictions
    title_str = "Predicted Appointments for " + location
    plt.title(title_str)
    plt.xlabel("Day of Week")
    plt.ylabel("Appointments")
    return predicted_plot
# End of predicted week plotting


# hey figure out how to run this twice a day

# Main testing
generate_model_location_weekday()
see_predicted_week('Sockanosset POD')
# predict_appointment('Sockanosset POD', 'Friday')
