# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 14:11:21 2021

@author: Giles Lanowy
"""

import tkinter as tk
from tkinter import ttk

class COVID(tk.Tk):
    
    def Scrape(self):
        
        print("get list of appointments close to: " + str(self.zipcode.get()))
        return
    
    def __init__(self):
        super().__init__()
        self.title("COVID-19 Vaccine Appointments")
        self.geometry("400x180")
        
        self.zipcode = tk.StringVar()
        zip_c = ttk.Button(self, text = "Enter Zip Code: ", command = self.Scrape)
        zip_c.grid(column = 0, row = 0, sticky = "N")
        zip_entry = ttk.Entry(self, width = 8, textvariable = self.zipcode)
        zip_entry.grid(column = 1, row = 0, sticky = "N")
        
        no_appointments = ttk.Label(self, text = "Available Appointments")
        no_appointments.grid(column = 1, row = 1)
        
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