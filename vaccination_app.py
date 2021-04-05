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
import vaccine_scrapper as vac

titleList = []
apptNumList = []
    
class COVID(tk.Tk):
    
    def make_an_appointment(self, location, date):            #New window to enter personal information
        newWin = tk.Toplevel(root)
        newWin.title("Enter information here")
        newWin.geometry("200x200")
        self.name = tk.StringVar()
        ttk.Label(newWin, text = "Enter Name: ").grid(column = 0, row = 0, pady = 10)
        ttk.Entry(newWin, width = 15, textvariable = self.name).grid(column = 1, row = 0, pady = 10)
        print(location)
        return
    
    def Scrape(self):                                    #Method to isolate and display available appointments with respect to date
        if self.date_entry.get() == "MM/DD/YYYY":
            vaccdata = vac.scrapevaccineappt(self.zipcode.get())
            vac_available = vac.displayavailableappts(vaccdata).to_string(index=False)
            print(vac_available)
            vac_data = vac.displayavailableappts(vaccdata)
            i = 2
            for index, row in vac_data.iterrows():
                sitei = ttk.Label(self, text = str(row["Location"])).grid(column = 0, row = i)
                appi = ttk.Label(self, text = str(row["Appointments"])).grid(column = 1, row = i)
                datei = ttk.Label(self, text = str(row["Date"])).grid(column = 2, row = i)
                buttoni = ttk.Button(self, text = "Book Here!", command = lambda : self.make_an_appointment(row["Location"], row["Date"])).grid(column = 3, row = i)
                i += 1 
        else:
            vaccination_data = vac.scrapevaccineappt(self.zipcode.get())
            vaccdata = vac.apptsmatchingdate(vaccination_data, self.date_entry.get())
            vac_available = vac.displayavailableappts(vaccdata).to_string(index=False)
            print(vac_available)
            vac_data = vac.displayavailableappts(vaccdata)
            i = 2
            for index, row in vac_data.iterrows():
                sitei = ttk.Label(self, text = str(row["Location"])).grid(column = 0, row = i)
                appi = ttk.Label(self, text = str(row["Appointments"])).grid(column = 1, row = i)
                datei = ttk.Label(self, text = str(row["Date"])).grid(column = 2, row = i)
                buttoni = ttk.Button(self, text = "Book Here!", command = lambda : self.make_an_appointment(row["Location"], row["Date"])).grid(column = 3, row = i)
                i += 1     
    
    def __init__(self):
        super().__init__()
        self.title("COVID-19 Vaccine Appointments")
        self.geometry("650x180")
        
        self.zipcode = tk.StringVar()
        self.date_entry = tk.StringVar()
        
        scrape = ttk.Button(self, text = "Find Appointments", command = self.Scrape).grid(column = 4, row = 0, pady = 10)
        
        zip_c = ttk.Label(self, text = "Enter Zip Code: ") #lambda : vac.scrapevaccineappt(self.zipcode.get())   
        date_label = ttk.Label(self, text = "Enter Date: ")
        zip_entry = ttk.Entry(self, width = 8, textvariable = self.zipcode)
        date_entry = ttk.Entry(self, width = 14, textvariable = self.date_entry)
        date_entry.insert(tk.END, 'MM/DD/YYYY')
        
        date_entry.grid(column = 3, row = 0)
        date_label.grid(column = 2, row = 0)
        zip_c.grid(column = 0, row = 0)
        zip_entry.grid(column = 1, row = 0, sticky = "W")
        
        loc_appointments = ttk.Label(self, text = "Location").grid(column = 0, row = 1)
        no_appointments = ttk.Label(self, text = "Available Appointments").grid(column = 1, row = 1)
        date_appointments = ttk.Label(self, text = "Date").grid(column = 2, row = 1)    
        
root = COVID()
root.mainloop()
