import serial  # Correct import (lowercase)
import webbrowser
import os
import time

# Set up the Serial connection (replace 'COM3' with your actual port)
try:
    ser = serial.Serial('COM3', 9600, timeout=1)  # Adjust COM port as needed
    time.sleep(2)  # Allow time for the connection to initialize
except serial.SerialException:
    print("Error: Could not open Serial port. Check the port name and connection.")
    exit()

# Function to open applications
def open_firefox():
    webbrowser.open("https://www.mozilla.org/firefox/")  # Open Firefox website

def open_discord():
    os.system("start discord")  # Windows command to open Discord

def open_arduino_ide():
    os.system("start arduino")  # Windows command to open Arduino IDE

# Main loop to listen for button presses
while True:
    try:
        if ser.in_waiting > 0:
            message = ser.readline().decode('utf-8').strip()
            
            if message == "FIREFOX":
                open_firefox()
                print("Firefox opened.")
            elif message == "DISCORD":
                open_discord()
                print("Discord opened.")
            elif message == "ARDUINO":
                open_arduino_ide()
                print("Arduino IDE opened.")
            
    except serial.SerialException as e:
        print("Serial error:", e)
        break

    time.sleep(0.1)  # Small delay to avoid overwhelming the Serial port
