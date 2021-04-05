# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 14:09:42 2021

@author: Giles Lanowy
"""

#client for final project

import socket

IP_ADDR = "192.168.1.156"
PORT = 9607
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():                  #connect to raspi server
    s.connect((IP_ADDR, PORT))
    return

def send_msg(no_appt):          #send appointment number to raspi server
    msg = no_appt
    s.sendall(msg.encode('ascii'))
    return

def end_conn():                 #send end connection message close client side
    msg = "-1"
    s.sendall(msg.encode('ascii'))
    s.close()