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
import vaccine_scraper as vac
import vaccine_machinelearning as vacml
import rpi_client as rpi

print("Running Vaccine Scraper GUI Application")

titleList = []
apptNumList = []
rpi.connect()  # Run client on the user's desktop
class COVID(tk.Tk):
    
    def make_an_appointment(self, location, date, appt):            #New window to enter personal information
    
        rpi.send_msg(str(appt))
        newWin = tk.Toplevel(root)
        newWin.title("Enter information here")
        newWin.geometry("500x200")
        
        #Variables for entries
        self.fname = tk.StringVar()
        self.lname = tk.StringVar()
        
        """Entry declarations for required fields"""
        #First and Last name
        ttk.Label(newWin, text = "First Name: ").grid(column = 0, row = 0, pady = 5)
        ttk.Entry(newWin, width = 15, textvariable = self.fname).grid(column = 1, row = 0, pady = 10)
        ttk.Label(newWin, text = "Last Name: ").grid(column = 2, row = 0, pady = 5)
        ttk.Entry(newWin, width = 15, textvariable= self.lname).grid(column = 3, row = 0)
        
        
        
        print(location)
        return
    
    def Scrape(self):                                    #Method to isolate and display available appointments with respect to date
        self.button = []
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
                x = row["Location"]
                y = row["Date"]
                z = row["Appointments"]
                self.button.append(ttk.Button(self, text = "Book Here!", command = lambda x=x, y=y, z=z: self.make_an_appointment(x, y, z)).grid(column = 3, row = i))
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
                x = row["Location"]
                y = row["Date"]
                z = row["Appointments"]
                self.button.append(ttk.Button(self, text = "Book Here!", command = lambda x=x, y=y, z=z: self.make_an_appointment(x, y, z)).grid(column = 3, row = i))
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
rpi.end_conn()
