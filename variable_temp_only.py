import socket
import serial
import time
from functions import *
from KeithleyConnect import *
from constants import TEMP_LIST

# Another  comment
# try:
channels = "108, 110, 112"
ip_address = "169.254.124.238"
channel_count = len(channels.split(","))
folder_path = r"D:\Abdul Sennain\thermal_testing_data"

data_socket = socket.socket()
ser = serial.Serial("COM3", 250000)

connect_keithley_optional_temp(
    ip_address=ip_address,
    channels=channels,
    data_socket=data_socket,
    measure_temp=True,
)

heat_bed_collect_data(
    TEMP_LIST=TEMP_LIST,
    folder_path=folder_path,
    channels=channels,
    ip_address=ip_address,
    data_socket=data_socket,
    ser=ser,
    trial_name="temp_in_chamber_only",
)

# finally:
#     heat_bed(temp=0, ser=ser)
#     ser.close()
