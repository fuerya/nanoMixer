import serial
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Set up the serial connection (change 'COM3' to your correct port)
SERIAL_PORT = "COM3"  # Adjust for your system
BAUD_RATE = 9600

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
    time.sleep(2)  # Allow connection to establish
except serial.SerialException:
    print(f"Failed to connect to {SERIAL_PORT}. Check your port.")
    exit()

# Get system volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

while True:
    try:
        if arduino.in_waiting > 0:
            raw_value = arduino.readline().decode("utf-8").strip()
            
            if raw_value.isdigit():
                pot_value = int(raw_value)
                
                # Normalize volume (0.0 - 1.0)
                volume_level = pot_value / 1023
                volume.SetMasterVolumeLevelScalar(volume_level, None)
                
                # Scale LED brightness (0-255) and send to Arduino
                led_brightness = int(volume_level * 255)
                arduino.write(f"{led_brightness}\n".encode())  # Send brightness

                print(f"Pot: {pot_value} | Volume: {volume_level:.2f} | LED: {led_brightness}")

    except KeyboardInterrupt:
        print("\nExiting program.")
        arduino.close()
        break
    except Exception as e:
        print(f"Error: {e}")
