#!/usr/bin/env python3

import re
import json

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

    with open("vehicles.json", "r") as file:
        vehicles = json.load(file)

    if vehicle_number in vehicles:

        data = vehicles[vehicle_number]

        print("\n[+] Vehicle Found")
        print("----------------------------")
        print("RTO          :", data["rto"])
        print("Manufacturer :", data["manufacturer"])
        print("Model        :", data["model"])
        print("Fuel         :", data["fuel"])
        print("Status       :", data["status"])
        print("PUC          :", data["puc"])

    else:
        print("\n[-] Vehicle not found in database")

else:
    print("\n[-] Invalid vehicle number")
