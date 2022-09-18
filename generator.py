#!/usr/bin/env python3

import sys
import csv
import os 

slave = 1

print("""modbus:
  - name: "meterkast"
    type: tcp
    host: 192.168.5.251
    port: 502
    sensors:""")

filename = sys.argv[1]
device_type = os.path.basename(filename).split('.')[0]

with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        scan_interval = int(row[7])
        if scan_interval == 0:
            continue

        input_type = 'holding'
        if row[0] == '01':
            input_type = 'coil'
        elif row[0] == '02':
            input_type = 'discrete'
        elif row[0] == '03':
            input_type = 'holding'
        elif row[0] == '04':
            input_type = 'input'

        name = row[2]
        address = row[1].lower()
        data_type = row[6]
        unit_of_measurement = row[8]
        device_class = row[9]
        state_class = row[10]
      
        print("""      - name: {}
        unique_id: {}_{}
        scan_interval: {}
        slave: {}
        input_type: {}
        address: 0x{}
        data_type: {}""".format(name, device_type, address, scan_interval, slave, input_type, address, data_type))
        
        if input_type.startswith('float'):
            print("        precision: 1")

        if unit_of_measurement != '':
            print("        unit_of_measurement: '{}'".format(unit_of_measurement))

        if device_class != '':
            print("        device_class: {}".format(device_class))
            
        if state_class != '':
            print("        state_class: {}".format(state_class))
            
