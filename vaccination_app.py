# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 14:11:21 2021

@author: Giles Lanowy
"""

import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import vaccine_appt2 as vac

titleList = []
apptNumList = []
    
class COVID(tk.Tk):
    
    def Scrape(self):
            vac.scrapevaccineappt(self.zipcode.get())
    
    # def Scrape(self):
    #     # print("get list of appointments close to: " + str(self.zipcode.get()))
    #     for i in range(3):
    #         i = str(i + 1)
    #         print("Page: ", i)
    #         govWebsiteSchedule = 'https://www.vaccinateri.org/clinic/search?location=' + str(self.zipcode.get()) + '&search_radius=All&q%5Bvenue_search_name_or_venue_name_i_cont%5D=&clinic_date_eq%5Byear%5D=&clinic_date_eq%5Bmonth%5D=&clinic_date_eq%5Bday%5D=&q%5Bvaccinations_name_i_cont%5D=&commit=Search&page=' + i + '#search_results'
    #         result = requests.get(govWebsiteSchedule)
    #         # If code == 200, page is accessable
    #         print("STATUS CODE: ", result.status_code)
        
    #         # Page content of the website
    #         src = result.content
        
    #         # Beautiful Soup object
    #         soup = BeautifulSoup(src, 'lxml')
        
                
    #         pTitle = soup.find_all("p", "text-xl font-black")
            
    #         for x in range(len(pTitle)):
    #             title = str(pTitle[x].text).replace('\n', '')
    #             title = title.lstrip()
    #             title = title.rstrip()
    #             if self.date_entry.get() == 'MM/DD/YYYY':
    #                 titleList.append(title)
    #             elif self.date_entry.get() in title:
    #                 titleList.append(title.replace(' on ' + str(self.date_entry.get()), ''))
    #         print(titleList)
        
    #         paragraphs = soup.find_all("p")     #Attempt: Search just for appointments available on the date
    #         title = str(pTitle[x].text).replace('\n', '')
    #         title = title.lstrip()
    #         title = title.rstrip()
            
    #         if self.date_entry.get() == 'MM/DD/YYYY':           #Get all available places 
    #             for paragraph in paragraphs:
    #                 if "Appointments Available" in paragraph.text:
    #                     apptNumber = int(paragraph.text.replace(paragraph.strong.text, ''))
    #                     if apptNumber != 0: 
    #                         apptNumList.append(apptNumber)
    #                 # Spanish
    #                 if "Citas disponibles" in paragraph.text:
    #                     apptNumber = int(paragraph.text.replace(paragraph.strong.text, ''))
    #                     if apptNumber != 0:
    #                         apptNumList.append(apptNumber)
    #                 # Portuguese
    #                 if "Agendamentos disponíveis" in paragraph.text:
    #                     apptNumber = int(paragraph.text.replace(paragraph.strong.text, ''))
    #                     if apptNumber != 0:
    #                         apptNumList.append(apptNumber)
    #         else:                                               #Get available places with respect to date
    #             for paragraph in paragraphs:
    #                 if "Appointments Available" in paragraph.text and self.date_entry.get() in title:
    #                     apptNumber = int(paragraph.text.replace(paragraph.strong.text, ''))
    #                     if apptNumber != 0: 
    #                         apptNumList.append(apptNumber)
    #                 # Spanish
    #                 if "Citas disponibles" in paragraph.text and self.date_entry.get() in title:
    #                     apptNumber = int(paragraph.text.replace(paragraph.strong.text, ''))
    #                     if apptNumber != 0:
    #                         apptNumList.append(apptNumber)
    #                 # Portuguese
    #                 if "Agendamentos disponíveis" in paragraph.text and self.date_entry.get() in title:
    #                     apptNumber = int(paragraph.text.replace(paragraph.strong.text, ''))
    #                     if apptNumber != 0:
    #                         apptNumList.append(apptNumber)
    #         print(apptNumList)
    #     return
    
    def __init__(self):
        super().__init__()
        self.title("COVID-19 Vaccine Appointments")
        self.geometry("400x180")
        
        self.zipcode = tk.StringVar()
        self.date_entry = tk.StringVar()
        
        zip_c = ttk.Button(self, text = "Enter Zip Code: ", command = self.Scrape)
        date_label = ttk.Label(self, text = "Enter Date: ")
        zip_entry = ttk.Entry(self, width = 8, textvariable = self.zipcode)
        date_entry = ttk.Entry(self, width = 14, textvariable = self.date_entry)
        date_entry.insert(tk.END, 'MM/DD/YYYY')
        
        date_entry.grid(column = 3, row = 0, sticky = "N")
        date_label.grid(column = 2, row = 0)
        zip_c.grid(column = 0, row = 0, sticky = "N")
        zip_entry.grid(column = 1, row = 0, sticky = "W")
        
        no_appointments = ttk.Label(self, text = "Available Appointments")
        no_appointments.grid(column = 1, row = 1)
        
        #for entry in titleList:         #Find out how to update placeholder list
        site1 = ttk.Label(self, text = "Placeholder Site 1")
        site2 = ttk.Label(self, text = "Placeholder Site 2")
        site3 = ttk.Label(self, text = "Placeholder Site 3")
        
        site1_app = ttk.Label(self, text = "4").grid(column = 1, row = 2)
        site2_app = ttk.Label(self, text = "2").grid(column = 1, row = 3)
        site3_app = ttk.Label(self, text = "0").grid(column = 1, row = 4)
        
        site1.grid(column = 0, row = 2)
        site2.grid(column = 0, row = 3)
        site3.grid(column = 0, row = 4)
    
        
root = COVID()
root.mainloop()