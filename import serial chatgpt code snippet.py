import serial
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume, IAudioSessionEnumerator
import pygetwindow as gw
from pycaw.utils import AudioUtilities as AppAudioUtilities, IAudioSessionManager2, IAudioSessionControl2
import time
import sys
import pycaw
import _ctypes

def set_volume(level):
    # Convert potentiometer value (0-1023) to system volume (0.0 - 1.0)
    volume = level / 1023.0
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
    volume_interface.SetMasterVolumeLevelScalar(volume, None)

def set_active_window_volume(level):
    volume = level / 1023.0
    active_window = gw.getActiveWindow()
    if not active_window:
        print("No active window detected")
        return

    # Get the session enumerator from the default speakers
    devices = AppAudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioSessionManager2._iid_, CLSCTX_ALL, None)
    session_manager = cast(interface, POINTER(IAudioSessionManager2))
    session_enum_ptr = session_manager.GetSessionEnumerator()
    session_enum = cast(session_enum_ptr, POINTER(IAudioSessionEnumerator))
    session_count = session_enum.GetCount()

    for i in range(session_count):
        try:
            session_ptr = session_enum.GetSession(i)
            if not session_ptr:
                continue

            session_control = cast(session_ptr, POINTER(IAudioSessionControl2))
            try:
                process_id = session_control.GetProcessId()
            except (OSError, _ctypes.COMError):
                # If getting the process ID fails, skip this session.
                continue

            if process_id == 0:
                # Ignore system sounds.
                continue

            try:
                session_name = session_control.GetProcess.name()
            except OSError:
                # If we cannot retrieve the process name, skip this session.
                continue

            # Debug: print session info (optional)
            # print(f"Session {i}: Process ID {process_id}, Name {session_name}")

            if active_window.title.lower() in session_name.lower():
                simple_audio_volume_ptr = session_control.QueryInterface(ISimpleAudioVolume._iid_)
                simple_audio_volume = cast(simple_audio_volume_ptr, POINTER(ISimpleAudioVolume))
                simple_audio_volume.SetMasterVolume(volume, None)
                print(f"Set volume for {session_name} to {volume}")
                return
        except (OSError, _ctypes.COMError):
            continue  # Skip problematic sessions

    print("No matching session found for the active window.")

def read_serial(port="COM3", baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected to {port} at {baudrate} baud")
    except serial.SerialException as e:
        print(f"Error: {e}")
        return

    try:
        while True:
            # Use errors='ignore' to skip any bytes that cannot be decoded
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                if line == "FIREFOX":
                    print("firefox")
                elif line == "BUTTON_1":
                    print("Button 1 Pressed")
                elif line == "BUTTON_2":
                    print("Button 2 Pressed")
                else:
                    try:
                        pot_values = list(map(int, line.split(',')))
                        if len(pot_values) == 5:
                            print(f"Pot A: {pot_values[0]}, Pot B: {pot_values[1]}")
                            set_volume(pot_values[0])  # Master volume
                            set_active_window_volume(pot_values[1])  # Active window volume
                    except ValueError:
                        pass  # Ignore malformed lines
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    import comtypes
    print(f"comtypes version: {comtypes.__version__}")
    read_serial("COM3", 9600)  # Change COM3 to match your port
