import time
import os
import csv
from KeithleyConnect import instrument_connect, instrument_write
from KeithleyConnect import instrument_query


def connect_keithley_temp_only(ip_address: str, channels: str, data_socket):
    """Used for reading one temperature channel only. If reading multiple channels, use function below."""
    channels_list = [channel.strip() for channel in channels.split(",")]
    last_channel_string = channels_list[0]
    print(f"Last channel: {last_channel_string}")

    # ***************INSTRUMENT SET UP***************
    instrument_connect(data_socket, ip_address, 5025, 10000, 0, 1)
    # reset the device
    instrument_write(data_socket, "*RST")

    # define the measurement channels

    # define the scan list, set scan count to infinite, and channel delay of 75 um
    instrument_write(
        data_socket, ":ROUTe:SCAN:CRE (@{0})".format(last_channel_string)
    )  # Create channels

    # Infinite scan count
    instrument_write(data_socket, ":ROUTe:SCAN:COUN:SCAN 100,000,000")

    instrument_write(
        data_socket, ":ROUTe:DEL 0.0002, (@{0})".format(last_channel_string)
    )  # Channel delay
    instrument_write(data_socket, ":ROUTe:SCAN:INT .1")  # Scan to scan interval

    # choose the buffer and assign all data to the buffer after clearing it
    instrument_write(data_socket, 'TRACe:CLEar, "defbuffer1"')
    instrument_write(data_socket, ':TRAC:FILL:MODE CONT, "defbuffer1"')
    instrument_write(data_socket, ':ROUT:SCAN:BUFF "defbuffer1"')

    #! Temperature settings only
    instrument_write(data_socket, "FUNC 'TEMP', (@{0})".format(last_channel_string))
    instrument_write(data_socket, "TEMP:TRAN TC, (@{0})".format(last_channel_string))
    instrument_write(data_socket, "TEMP:TC:TYPE K, (@{0})".format(last_channel_string))

    instrument_write(
        data_socket, "TEMP:DEL:AUTO ON, (@{0})".format(last_channel_string)
    )

    instrument_write(data_socket, "TEMP:UNIT CELS, (@{0})".format(last_channel_string))
    instrument_write(data_socket, "TEMP:NPLC 1, (@{0})".format(last_channel_string))
    instrument_write(data_socket, "TEMP:AZER OFF, (@{0})".format(last_channel_string))
    instrument_write(
        data_socket, "TEMP:LINE:SYNC OFF, (@{0})".format(last_channel_string)
    )

    #! Specify internal junction
    instrument_write(
        data_socket, "TEMP:TC:RJUN:RSEL INT, (@{0})".format(last_channel_string)
    )

    # enable the graph to plot the data
    instrument_write(data_socket, ":DISP:SCR HOME")
    instrument_write(data_socket, "DISP:WATC:CHAN (@{0})".format(last_channel_string))
    instrument_write(data_socket, ":DISP:SCR GRAP")


def connect_keithley_optional_temp(
    ip_address: str, channels: str, data_socket, measure_temp: bool
):
    """Used for reading mutliple channels, if reading temperature set measure_temp=True. If not reading temperature set temp=False. If reading one temp only, then use function connect_keithley_temp_only."""

    #! Go into Windows and set the Ethernet connection to manual
    # define the instrament's IP address. the port is always 5025 for LAN connection.
    # establish connection to the LAN socket. initialize and connect to the Keithley
    # Close the connection if one already exists
    # Establish a TCP/IP socket object

    channels_list = [channel.strip() for channel in channels.split(",")]
    all_but_last_list = channels_list[:-1]
    all_but_last_string = ", ".join(all_but_last_list)
    last_channel_string = channels_list[-1]

    print(f"All channels except last: {all_but_last_string}")
    print(f"Last channel: {last_channel_string}")

    instrument_connect(data_socket, ip_address, 5025, 10000, 0, 1)
    # reset the device
    instrument_write(data_socket, "*RST")

    #! Scan count and basic config same for volt and temp channels
    instrument_write(
        data_socket, ":ROUTe:SCAN:CRE (@{0})".format(channels)
    )  # Create channels
    instrument_write(data_socket, ":ROUTe:SCAN:COUN:SCAN 0")  # Infinite scan count
    instrument_write(
        data_socket, ":ROUTe:DEL 0, (@{0})".format(channels)
    )  # Channel delay
    instrument_write(data_socket, ":ROUTe:SCAN:INT .2")  # Scan to scan interval

    # choose the buffer and assign all data to the buffer after clearing it
    instrument_write(data_socket, 'TRACe:CLEar, "defbuffer1"')
    instrument_write(data_socket, ':TRAC:FILL:MODE CONT, "defbuffer1"')
    instrument_write(data_socket, ':ROUT:SCAN:BUFF "defbuffer1"')

    if measure_temp == True:
        """***************CHANNEL SET UP***************"""
        #! VOLT:DC channels only
        # # define the channel functions
        instrument_write(
            data_socket, "FUNC 'VOLT:DC', (@{0})".format(all_but_last_string)
        )

        # # define channel parameters such as range to 1 volt, autozero off, and line sync on
        instrument_write(
            data_socket, "VOLT:DC:RANG 1, (@{0})".format(all_but_last_string)
        )  # Range
        instrument_write(
            data_socket, "VOLT:DC:AZER OFF, (@{0})".format(all_but_last_string)
        )  # Auto-zero off
        instrument_write(
            data_socket, "VOLT:DC:LINE:SYNC ON, (@{0})".format(all_but_last_string)
        )  # Line sync on
        instrument_write(
            data_socket, "VOLT:DC:DEL:AUTO ON, (@{0})".format(all_but_last_string)
        )  # Auto-delay off
        instrument_write(
            data_socket, ":SENS:VOLT:DC:NPLC 1, (@{0})".format(all_but_last_string)
        )  # NPLC
        instrument_write(
            data_socket, "VOLT:DC:INP MOHM10, (@{0})".format(all_but_last_string)
        )  # Input impedance

        #! Temperature settings only
        instrument_write(data_socket, "FUNC 'TEMP', (@{0})".format(last_channel_string))
        instrument_write(
            data_socket, "TEMP:TRAN TC, (@{0})".format(last_channel_string)
        )
        instrument_write(
            data_socket, "TEMP:TC:TYPE K, (@{0})".format(last_channel_string)
        )

        instrument_write(
            data_socket, "TEMP:DEL:AUTO ON, (@{0})".format(last_channel_string)
        )

        instrument_write(
            data_socket, "TEMP:UNIT CELS, (@{0})".format(last_channel_string)
        )
        instrument_write(data_socket, "TEMP:NPLC 1, (@{0})".format(last_channel_string))
        instrument_write(
            data_socket, "TEMP:AZER OFF, (@{0})".format(last_channel_string)
        )
        instrument_write(
            data_socket, "TEMP:LINE:SYNC OFF, (@{0})".format(last_channel_string)
        )
        #! Specify internal junction
        instrument_write(
            data_socket, "TEMP:TC:RJUN:RSEL INT, (@{0})".format(last_channel_string)
        )

        # enable the graph to plot the data
        instrument_write(data_socket, ":DISP:SCR HOME")
        instrument_write(data_socket, "DISP:WATC:CHAN (@{0})".format(channels))
        instrument_write(data_socket, ":DISP:SCR GRAP")

    else:  #! No temp, only VOLT:DC channels
        """***************CHANNEL SET UP***************"""

        # Create channels
        instrument_write(data_socket, ":ROUTe:SCAN:CRE (@{0})".format(channels))

        # Infinite scan count
        instrument_write(
            data_socket, ":ROUTe:SCAN:COUN:SCAN 100,000,000"
        )  # i smell funny

        # Channel delay
        instrument_write(data_socket, ":ROUTe:DEL 0.0002, (@{0})".format(channels))

        instrument_write(data_socket, ":ROUTe:SCAN:INT .1")  # Scan to scan interval

        # choose the buffer and assign all data to the buffer after clearing it
        instrument_write(data_socket, 'TRACe:CLEar, "defbuffer1"')
        instrument_write(data_socket, ':TRAC:FILL:MODE CONT, "defbuffer1"')
        instrument_write(data_socket, ':ROUT:SCAN:BUFF "defbuffer1"')

        # # define the channel functions
        instrument_write(data_socket, "FUNC 'VOLT:DC', (@{0})".format(channels))

        # # define channel parameters such as range to 1 volt, autozero off, and line sync on
        instrument_write(
            data_socket, "VOLT:DC:RANG 1, (@{0})".format(channels)
        )  # Range
        instrument_write(
            data_socket, "VOLT:DC:AZER OFF, (@{0})".format(channels)
        )  # Auto-zero off
        instrument_write(
            data_socket, "VOLT:DC:LINE:SYNC ON, (@{0})".format(channels)
        )  # Line sync on
        instrument_write(
            data_socket, "VOLT:DC:DEL:AUTO ON, (@{0})".format(channels)
        )  # Auto-delay off
        instrument_write(
            data_socket, ":SENS:VOLT:DC:NPLC 1, (@{0})".format(channels)
        )  # NPLC
        instrument_write(
            data_socket, "VOLT:DC:INP MOHM10, (@{0})".format(channels)
        )  # Input impedance

        # enable the graph to plot the data
        instrument_write(data_socket, ":DISP:SCR HOME")
        instrument_write(data_socket, "DISP:WATC:CHAN (@{0})".format(channels))
        instrument_write(data_socket, ":DISP:SCR GRAP")


def stop_trail_export_csv(
    file_name, directory_name, data_socket, channels, serial_port
):
    readings_count = int(instrument_query(data_socket, "TRACe:ACTual?", 16).rstrip())
    #! total number of readings should be even, if not then one reading is larger than the other for two channels, so data will not be recorded and is skipped
    if readings_count % 2 == True:
        readings_count -= 1

    channel_count = len(channels.split(","))

    # preallocate counters and a Data list
    start_index = 1
    end_index = channel_count
    accumulated_readings = 0
    Data = []

    # read the buffer and place measurements into Data: list
    while accumulated_readings < readings_count:
        Data.append(
            instrument_query(
                data_socket,
                'TRACe:DATA? {0}, {1}, "defbuffer1", REL, READ'.format(
                    start_index, end_index
                ),
                128,
            ).split(",")
        )
        start_index += channel_count
        end_index += channel_count
        accumulated_readings += channel_count

    if not os.path.exists(f"{directory_name}"):
        os.makedirs(f"{directory_name}")

    newFile = open("{0}{1}.csv".format(directory_name, file_name), "w", newline="")
    newWriter = csv.writer(newFile, dialect="excel")
    for i in range(len(Data)):
        if i > 1:
            newWriter.writerow(Data[i])
    newFile.close()

    time.sleep(3)  # Sleep after the last trial to reset gel signal to zero


def step_down(
    iterations: int, time_interval: int, serial_port, increment_distance: float
):
    """ "
    time_interval is in whole seconds, if for fraction of second
    then modify function
    """

    for _ in range(iterations):  # argument in range() is the total number of steps
        serial_port.write("G91\n".encode())
        time.sleep(1)
        serial_port.write((f"G1 Z{increment_distance}\n").encode())
        time.sleep(
            time_interval - 1
        )  # Total wait time, add one second to number in time.sleep(), so time.sleep(3) is 4 seconds between all

    serial_port.write((f"G1 Z{-increment_distance * iterations}\n").encode())
    time.sleep(3)


def heat_bed(temp: int, ser):
    time.sleep(10)
    #! Change bed temp
    ser.write(f"M140 S{int(temp)}\n".encode())
    time.sleep(900)


def collect_repeated_data(
    weight_ratio_and_plasticizer: str,
    step_iterations: int,
    trial_iterations: int,
    increment_distance: float,
    time_interval: int,
    folder_path: str,
    channels: str,
    data_socket,
    ser,
):
    i = 1
    while (
        i <= trial_iterations
    ):  # Parameter in range() is how many trials are being repeated
        # open ports, connect instruments

        instrument_write(data_socket, "INIT")
        time.sleep(1)

        step_down(
            iterations=step_iterations,
            serial_port=ser,
            increment_distance=increment_distance,
            time_interval=time_interval,
        )

        #! Stop data collection
        instrument_write(data_socket, "ABORT")

        # identify how many readings there are
        readings_count = int(
            instrument_query(data_socket, "TRACe:ACTual?", 16).rstrip()
        )

        #! total number of readings should be even, if not then one reading is larger than the other for two channels, so data will not be recorded and is skipped

        stop_trail_export_csv(
            file_name=f"{weight_ratio_and_plasticizer}_trial_{i}",
            directory_name=f"{folder_path}\\",
            data_socket=data_socket,
            channels=channels,
            serial_port=ser,
        )

        i += 1


def heat_bed_collect_data(
    TEMP_LIST: list,
    folder_path: str,
    channels: str,
    ip_address: str,
    data_socket,
    ser,
    trial_name,
):
    instrument_write(data_socket, "INIT")
    time.sleep(1)

    for TEMP in TEMP_LIST:
        heat_bed(temp=TEMP, ser=ser)

    #! Stop data collection
    instrument_write(data_socket, "ABORT")

    stop_trail_export_csv(
        file_name=f"{trial_name}",
        directory_name=f"{folder_path}\\",
        data_socket=data_socket,
        channels=channels,
        serial_port=ser,
    )
