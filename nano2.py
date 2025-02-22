# notes: constantly reads serial monitor, see if you can get rid of this
# arduino code needs to send pot data as println, seems like python can't read the print lines
# discord and arduino IDE shortcuts don't work but it's a path issue

import serial  # Correct import
import webbrowser
import os
import time
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# Set up the Serial connection (replace 'COM3' with your actual port)
try:
    ser = serial.Serial('COM3', 9600, timeout=1)  # Adjust COM port as needed
    time.sleep(2)  # Allow time for the connection to initialize
except serial.SerialException:
    print("Error: Could not open Serial port. Check the port name and connection.")
    exit()

# Set up Windows audio control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_control = cast(interface, POINTER(IAudioEndpointVolume))

# Function to set system volume (0-100%)
def set_system_volume(volume):
    volume = max(0, min(100, volume))  # Ensure volume stays within range
    volume_control.SetMasterVolumeLevelScalar(volume / 100.0, None)
    print(f"System Volume Set to: {volume}%")

# Function to open applications
def open_firefox():
    webbrowser.open("https://www.mozilla.org/firefox/")

def open_discord():
    os.system("start discord")

def open_arduino_ide():
    os.system("start arduino")

# Store the last volume value to prevent unnecessary updates
last_system_volume = None

# Main loop to listen for button presses and potentiometer values
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
            else:
                try:
                    # Expecting a single potentiometer value
                    potValueA = int(message)

                    # Map potentiometer values to volume range (0-100%)
                    system_volume = int((potValueA / 1023) * 100)

                except ValueError:
                    print("Invalid potentiometer data received:", message)
        
    except serial.SerialException as e:
        print("Serial error:", e)
        break

    time.sleep(0.1)  # Small delay to avoid overwhelming the Serial port
