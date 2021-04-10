# Requests deals with making HTTP requests, better than urllib and urllib2
import requests
# BeautifulSoup extracts data from html or xml
from bs4 import BeautifulSoup
# Selenium is used to render webpages, especially executing Javascript Code
# import selenium
# Pandas is used for creating and modifying dataframes
import pandas as pd
# datetime for getting the current time
from datetime import datetime

# Scrapy is a framework built for web scraping
# import Scrapy

# -*- coding: utf-8 -*-
# Using PEP8 Style Guidelines
"""
Created on Mon Mar 29 14:06:59 2021

@author: John Hunter and Giles Lanowy
"""
"""
References:
    https://www.zyte.com/learn/what-python-web-scraping-tools-are-available/
    https://www.youtube.com/watch?v=XVv6mJpFOb0&ab_channel=freeCodeCamp.org
"""


def scrapevaccineappt(zipcode):
    """
        Inputs:
            zipcode: a string of 5 digits
        Outputs:
            vaccData: a PANDAS dataframe of Location, Date, Appointments Available
    """
    zipcode = str(zipcode)  # make sure areacode is a string for concatenation into html link
    # Note that the zip code for the RI GOV Vaccination website doesn't really matter,
    # the site by default shows all locations in RI
    # govwebsite = 'https://covid.ri.gov/vaccination'

    current_time = datetime.now()
    current_time = current_time.strftime("%d%m%Y_%H%M%S")  # This is DDMMYY_HHMMSS
    print("Current Time is ", current_time)

    # Initialize the dataframe that will be output
    vaccdata = pd.DataFrame(columns=['Location', 'Date', 'Address', 'Vaccine', 'Appointments', 'Link', 'Time Accessed'])

    for i in range(10):  # Scan through 10 pages
        i = str(i + 1)  # account for 0 index
        govwebsiteschedule = 'https://www.vaccinateri.org/clinic/search?location=' + zipcode + \
                             '&search_radius=All&q%5Bvenue_search_name_or_venue_name_i_cont' + \
                             '%5D=&clinic_date_eq%5Byear%5D=&clinic_date_eq%5Bmonth%5D=&clinic_date_eq' + \
                             '%5Bday%5D=&q%5Bvaccinations_name_i_cont%5D=&commit=Search&page=' + i + '#search_results'
        result = requests.get(govwebsiteschedule)  # get the webpage data
        print("Page: ", i, "/ STATUS CODE: ", result.status_code)  # If code == 200, page is accessable
        src = result.content  # Page content of the website
        soup = BeautifulSoup(src, 'lxml')  # Beautiful Soup object

        # This is every location item on the gov website
        # inside of this div is the location, number of appts, links
        # I refer to this div as a 'card' or 'section'
        vaccine_cards = soup.find_all('div', 'md:flex justify-between -mx-2 md:mx-0 px-2 md:px-4 pt-4 pb-4 ' +
                                      'border-b border-gray-200')

        for card in vaccine_cards:  # for every section (location/date) on the website
            location = card.find('p', 'text-xl font-black')  # tag and text of location with class='text-xl font-black'
            location = location.text.lstrip().rstrip()  # text of location without tag, leading, or tailing spaces
            date = location[-10:]  # DD/MM/YYYY at the end of Location title
            location = location.replace(location[-10:], '')  # Make location only have location name, remove date
            location = location.replace(' on ', '')
            print(location)
            print(date)
            address = card.find('p', '')  # first generic paragraph tag in the card
            address = address.text.lstrip().rstrip()
            print(address)
            vaccine_type = card.find_all('strong', limit=2)
            vaccine_type = vaccine_type[1].text.lstrip().rstrip()
            print(vaccine_type)
            appointments = card.find_all('p')
            for appts in appointments:  # scan every paragraph tag for a specific string
                if "Appointments Available" in appts.text:
                    appointments = int(appts.text.replace(appts.strong.text, ''))
                    # Spanish
                if "Citas disponibles" in appts.text:
                    appointments = int(appts.text.replace(appts.strong.text, ''))
                    # Portuguese
                if "Agendamentos disponíveis" in appts.text:
                    appointments = int(appts.text.replace(appts.strong.text, ''))
            print("Appointments Availabull: ", appointments)
            signuplink = card.find_all('a', 'button-primary px-4')
            for link in signuplink:
                signuplink = link.get('href')
            signuplink = 'https://www.vaccinateri.org' + str(signuplink)  # hyperlink to schedule an appt at this site
            print(signuplink)

            # Create a dictionary of the card's data to append into dataframe
            card_dict = {
                'Location': location,
                'Date': date,
                'Address': address,
                'Vaccine': vaccine_type,
                'Appointments': appointments,
                'Link': signuplink,
                'Time Accessed': current_time  # DDMMYY_HHMMSS
            }

            # Append data into Dataframe
            # columns=['Location', 'Date', 'Address', 'Vaccine', 'Appointments', 'Link']
            vaccdata = vaccdata.append(card_dict, ignore_index=True)
            # end of card data extraction
        # end of this webpage
    # end of scanning all webpages

    # Put Dataframe into a unique csv file every time the function runs
    # We will use these csv files later to analyze the data over a long period of time (~2 weeks)
    csv_filename = 'data/apptDataVaccine_' + current_time + '.csv'
    vaccdata.to_csv(csv_filename, index=False, header=True)  # Put the dataframe into the csv file
    return vaccdata


def displayavailableappts(vaccdata):
    """
    Displays number of appointments, on this date, at this location, if there are appts available
    :param vaccdata: Dataframe of Location, Date, Appointments
    :return:
    """
    if vaccdata[vaccdata.Appointments >= 1].empty:
        print("No available appointments.")
    return vaccdata[vaccdata.Appointments >= 1]


def apptsmatchingdate(vaccdata, date):
    """
    Displays appointments matching the date selected by user, displays zero appts too
    :param vaccdata: Dataframe of Location, Date, Appointments
    :param date: MM/DD/YYYY format string
    :return:
    """
    date = str(date)
    if vaccdata[vaccdata.Date == date].empty:
        print("No data for this date yet.")
    return vaccdata[vaccdata.Date == date]


def vaccinedatadump(vaccdata, areacode):
    vaccdataframe = scrapevaccineappt(str(areacode))

    # Go through every row of dataframe, and do things with the columns
    totalappts = 0
    for index, row in vaccdataframe.iterrows():
        # print(row['Date'], row['Appointments'], row['Location'])
        totalappts += row['Appointments']
    print("Total Appointments Available: ", totalappts)

    # Number of unique locations with available appointments
    locationdataframe = displayavailableappts(vaccdataframe)
    locationset = set(locationdataframe['Location'])
    print("Number of Locations with Available Appointments: ", len(displayavailableappts(vaccdataframe)))


# Main testing here
vaccdataframe = scrapevaccineappt('02852')
print(vaccdataframe)
# print(vaccdataframe.to_string(index=False))
# print(displayavailableappts(vaccdataframe).to_string(index=False))
# print(apptsmatchingdate(vaccdataframe, '04/20/2021').to_string(index=False))
# print("Number of Locations with Available Appointments: ", len(displayavailableappts(vaccdataframe)))

# print("Hey I want available appointments on this date")
# print(displayavailableappts(apptsmatchingdate(vaccdataframe, '04/11/2021')).to_string(index=False))
