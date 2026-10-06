#!/usr/bin/env python3

import re

print("""
====================================
        VehicleTrace
   Vehicle OSINT Investigation Tool
====================================
""")

vehicle_number = input("[?] Enter vehicle number: ")

vehicle_number = vehicle_number.replace(" ", "").upper()

pattern = r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}$"

if re.match(pattern, vehicle_number):
    print("\n[+] Valid vehicle number")
    print("[+] Vehicle:", vehicle_number)
else:
    print("\n[-] Invalid vehicle number")
