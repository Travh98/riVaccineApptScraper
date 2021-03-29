# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 14:06:59 2021

@author: John Hunter and Giles Lanowy
"""
"""
References:
    https://www.zyte.com/learn/what-python-web-scraping-tools-are-available/
    
"""  

# Requests deals with making HTTP requests, better than urllib and urllib2
import requests
# BeautifulSoup extracts data from html or xml
from bs4 import BeautifulSoup
# Selenium is used to render webpages, especially executing Javascript Code
#import selenium
import pandas as pd

import csv

# Scrapy is a framework built for web scraping
#import Scrapy

govWebsite = 'https://covid.ri.gov/vaccination'
areaCode = '02852'
titleList = []
apptNumList = []

for i in range(3): # Scan all 3 pages
    i = str(i + 1)
    print("Page: ", i)
    govWebsiteSchedule = 'https://www.vaccinateri.org/clinic/search?location=' + areaCode + '&search_radius=All&q%5Bvenue_search_name_or_venue_name_i_cont%5D=&clinic_date_eq%5Byear%5D=&clinic_date_eq%5Bmonth%5D=&clinic_date_eq%5Bday%5D=&q%5Bvaccinations_name_i_cont%5D=&commit=Search&page=' + i + '#search_results'
    result = requests.get(govWebsiteSchedule)
    # If code == 200, page is accessable
    print("STATUS CODE: ", result.status_code)

    # Page content of the website
    src = result.content

    # Beautiful Soup object
    soup = BeautifulSoup(src, 'lxml')

        
    pTitle = soup.find_all("p", "text-xl font-black")
    
    for x in range(len(pTitle)):
        title = str(pTitle[x].text).replace('\n', '')
        title = title.lstrip()
        title = title.rstrip()
        titleList.append(title)
    print(titleList)

    paragraphs = soup.find_all("p")
    
    for paragraph in paragraphs:
        if "Appointments Available" in paragraph.text:
            apptNumber = int(paragraph.text.replace(paragraph.strong.text, ''))
            apptNumList.append(apptNumber)
        # Spanish
        if "Citas disponibles" in paragraph.text:
            apptNumber = int(paragraph.text.replace(paragraph.strong.text, ''))
            apptNumList.append(apptNumber)
        # Portuguese
        if "Agendamentos disponíveis" in paragraph.text:
            apptNumber = int(paragraph.text.replace(paragraph.strong.text, ''))
            apptNumList.append(apptNumber)
    print(apptNumList)
    
print("Title Length: ", len(titleList))
print("Appt Length: ", len(apptNumList))



apptDataSet = list(zip(titleList, apptNumList))
df = pd.DataFrame(data = apptDataSet, columns = ['Location', 'Appointments'])
df.to_csv('apptDataVaccine.csv', index=False, header=True)
