# Requests deals with making HTTP requests, better than urllib and urllib2
import requests
# BeautifulSoup extracts data from html or xml
from bs4 import BeautifulSoup
# Selenium is used to render webpages, especially executing Javascript Code
# import selenium
import pandas as pd
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
    
"""  


def scrapevaccineappt(zipcode):
    """
        Inputs:
            zipcode: a string of 5 digits
        Outputs:
            vaccData: a PANDAS dataframe of Location, Date, Appointments Available
    """
    zipcode = str(zipcode)  # make sure areacode is a string for concatenation into html link
    # govwebsite = 'https://covid.ri.gov/vaccination'

    vaccdata = pd.DataFrame()
    titlelist = []
    datelist = []
    apptnumlist = []
    
    for i in range(10):  # Scan through 10 pages
        i = str(i + 1)
        print("Page: ", i)
        govwebsiteschedule = 'https://www.vaccinateri.org/clinic/search?location=' + zipcode + \
                             '&search_radius=All&q%5Bvenue_search_name_or_venue_name_i_cont' + \
                             '%5D=&clinic_date_eq%5Byear%5D=&clinic_date_eq%5Bmonth%5D=&clinic_date_eq' + \
                             '%5Bday%5D=&q%5Bvaccinations_name_i_cont%5D=&commit=Search&page=' + i + '#search_results'
        result = requests.get(govwebsiteschedule)
        print("STATUS CODE: ", result.status_code)  # If code == 200, page is accessable
    
        # Page content of the website
        src = result.content
    
        # Beautiful Soup object
        soup = BeautifulSoup(src, 'lxml')

        ptitle = soup.find_all("p", "text-xl font-black")
        
        for x in range(len(ptitle)):
            title = str(ptitle[x].text).replace('\n', '')
            title = title.lstrip()
            title = title.rstrip()
            title = title.replace(' on ', '')
            datelist.append(title[-10:])
            title = title.replace(title[-10:], '')
            title = title.rstrip()  # some locations have an extra space at the end, like Sockanosset POD
            titlelist.append(title)
        print(titlelist)
        print(datelist)
    
        paragraphs = soup.find_all("p")
        
        for paragraph in paragraphs:
            if "Appointments Available" in paragraph.text:
                apptnumber = int(paragraph.text.replace(paragraph.strong.text, ''))
                apptnumlist.append(apptnumber)
            # Spanish
            if "Citas disponibles" in paragraph.text:
                apptnumber = int(paragraph.text.replace(paragraph.strong.text, ''))
                apptnumlist.append(apptnumber)
            # Portuguese
            if "Agendamentos disponíveis" in paragraph.text:
                apptnumber = int(paragraph.text.replace(paragraph.strong.text, ''))
                apptnumlist.append(apptnumber)
        print(apptnumlist)
        
    print("Title Length: ", len(titlelist))
    print("Date length: ", len(datelist))
    print("Appt Length: ", len(apptnumlist))

    apptdataset = list(zip(titlelist, datelist, apptnumlist))
    vaccdata = pd.DataFrame(data=apptdataset, columns=['Location', 'Date', 'Appointments'])
    vaccdata.to_csv('data/apptDataVaccine.csv', index=False, header=True)
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
        #print(row['Date'], row['Appointments'], row['Location'])
        totalappts += row['Appointments']
    print("Total Appointments Available: ", totalappts)

    # Number of unique locations with available appointments
    locationdataframe = displayavailableappts(vaccdataframe)
    locationset = set(locationdataframe['Location'])
    print("Number of Locations with Available Appointments: ", len(displayavailableappts(vaccdataframe)))



# Main testing here
vaccdataframe = scrapevaccineappt('02852')
print(vaccdataframe.to_string(index=False))
print(displayavailableappts(vaccdataframe).to_string(index=False))
print(apptsmatchingdate(vaccdataframe, '04/20/2021').to_string(index=False))
print("Number of Locations with Available Appointments: ", len(displayavailableappts(vaccdataframe)))

# print("Hey I want available appointments on this date")
# print(displayavailableappts(apptsmatchingdate(vaccdataframe, '04/11/2021')).to_string(index=False))
