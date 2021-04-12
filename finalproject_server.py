# Server for final project
# Run this program on the Server (the raspberry pi)

from sense_hat import SenseHat
import socket
import time

sense = SenseHat()

host = '192.168.1.156'
port = 9607
s = socket.socket()
s.bind((host, port))
s.listen(10)
z = (0,255,0) 
image = [
    z, z, z, z, z, z, z, z,
    z, z, z, z, z, z, z, z,
    z, z, z, z, z, z, z, z,
    z, z, z, z, z, z, z, z,
    z, z, z, z, z, z, z, z,
    z, z, z, z, z, z, z, z,
    z, z, z, z, z, z, z, z,
    z, z, z, z, z, z, z, z
    ]
while True:
    try:
        conn, addr = s.accept()
        if conn:
            print('Connection established from: %s'%str(addr))
            while True:
                message = conn.recv(10).decode("ascii")
                if int(message) <= 9 and int(message) >= 5:
                    sense.show_letter(message, text_colour = (255,255,0))
                    print("Appointments Available: " + message)
                elif int(message) < 5 and int(message) > 0:
                    sense.show_letter(message, text_colour = (255,0,0))
                    print("Appointments Available: " + message)
                elif int(message) > 9:
                    sense.set_pixels(image)
                    print("Appointments Available: " + message)
                elif int(message) == -1:
                    print("Disconnected from: %s"%str(addr))
                    conn.close()
                else:
                    time.sleep(5)
    except:
        conn.close()