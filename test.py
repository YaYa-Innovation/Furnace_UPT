#!/usr/bin/python3
import os
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client import ModbusTcpClient
from fractions import Fraction
import time
from datetime import datetime

def full_night():

    now = datetime.now()
    current_time = now.strftime("%I:%M:%S:%P")
    print("TIME : " + current_time)
    current_date = now.strftime("%d-%m-%Y")
    print("DATE : " + current_date)

    # Read HMI_Doller_Address from input.txt file
    try:
        with open('input.txt', 'r') as input_file:
            HMI_Doller_Address = int(input_file.read().strip())
    except FileNotFoundError:
        print("Input file not found. Please create an 'input.txt' file with the HMI_Doller_Address.")
        return
    except ValueError:
        print("Invalid data in input file. Please provide a valid integer for HMI_Doller_Address.")
        return

    ip_address = "172.1022.4.237"
    client = ModbusTcpClient(ip_address, port=502)
    client.connect()
    data = client.read_holding_registers(HMI_Doller_Address, 2, slave=1)
    decoder = BinaryPayloadDecoder.fromRegisters(data.registers, Endian.Big, wordorder=Endian.Little)
    address_result = decoder.decode_32bit_float()
    string_convert = str(address_result)
    length_of_number = len(string_convert)
    print("The Register Address Value Is :  ", (address_result))
    Round_Value = address_result
    kwh = Round_Value / 1000000000
    kwh_data = round(kwh, 14)
    print("FULL", kwh_data)
    data1 = kwh_data

    # Save the result to a text file
    output_file_path = "output.txt"  # Specify your desired output file path
    with open(output_file_path, 'w') as output_file:
        output_file.write(f"Time: {current_time}\n")
        output_file.write(f"Date: {current_date}\n")
        output_file.write(f"The Register Address Value Is: {address_result}\n")
        output_file.write(f"FULL: {kwh_data}\n")

    print(f"Results written to {output_file_path}")

full_night()
