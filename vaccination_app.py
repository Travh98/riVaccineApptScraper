# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 14:11:21 2021

@author: Giles Lanowy and John Hunter
"""

import tkinter as tk
from tkinter import ttk
import rpi_client as rpi
import webbrowser
#Comment or Uncomment next two lines as necessary
#import vaccine_scraper as vax
import vax_scrapper as vax


titleList = []
apptNumList = []
rpi.connect()

class COVID(tk.Tk):
    
    def eliminate(self):
        for label in self.grid_slaves():
            if int(label.grid_info()["row"]) > 1:
                label.grid_forget()
    
    def make_an_appointment(self, j, link, location, appt):            #New window to enter personal information... Vac, date not included
    
        rpi.send_msg(str(appt))                                    # send message with number of appointments to rpi
        
        #Open web page for making an appointment
        if location == "Matt's Local Pharmacy":
            print("Call here")
            ttk.Label(self, text = "401-619-5020").grid(column = 4, row = j)
        elif link[-2:] == '[]':
            print("no available website /n")
            print("Try looking for a phone number for", location)
            ttk.Label(self, text = "NA").grid(column = 4, row = j)
        else:
            print(link)
            webbrowser.open(link)

        print(location)
        return
    
    def Scrape(self):                                    #Method to isolate and display available appointments with respect to date and zip
        self.button = []
        
        self.eliminate()
        
        if self.date_entry.get() == "MM/DD/YYYY" or self.date_entry.get() == "":
            vaccdata = vax.scrapevaccineappt(self.zipcode.get())
            vac_available = vax.displayavailableappts(vaccdata).to_string(index=False)
           
        else:
            vaccination_data = vax.scrapevaccineappt(self.zipcode.get())                #includes date reference
            vaccdata = vax.apptsmatchingdate(vaccination_data, self.date_entry.get())
            vac_available = vax.displayavailableappts(vaccdata).to_string(index=False)
              
        print(vac_available)
        vac_data = vax.displayavailableappts(vaccdata)
            
        i = 2
        for index, row in vac_data.iterrows():
            sitei = ttk.Label(self, text = str(row["Location"])).grid(column = 0, row = i)
            appi = ttk.Label(self, text = str(row["Appointments"])).grid(column = 1, row = i)
            datei = ttk.Label(self, text = str(row["Date"])).grid(column = 2, row = i)
            vaxi = ttk.Label(self, text = str(row["Vaccine"]).replace("COVID-19 Vaccine", '')).grid(column = 3, row = i)
            v = row["Link"]
            x = row["Location"]
            z = row["Appointments"]
            self.button.append(ttk.Button(self, text = "Book Here!", command = lambda i=i, v=v, x=x, z=z: self.make_an_appointment(i, v, x, z)).grid(column = 4, row = i))
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
        no_appointments = ttk.Label(self, text = "           Available Appointments or \nAppointments Currently Being Booked").grid(column = 1, row = 1)
        date_appointments = ttk.Label(self, text = "Date").grid(column = 2, row = 1)  
        vax_type = ttk.Label(self, text = "Vaccine").grid(column = 3, row = 1)
        
root = COVID()
root.mainloop()
rpi.end_conn()
