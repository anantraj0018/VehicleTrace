#!/usr/bin/env python3

import re
import json
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

print("""
====================================
        VehicleTrace
   Vehicle OSINT Investigation Tool
====================================
""")

vehicle_number = input("[?] Enter vehicle number: ")
vehicle_number = vehicle_number.replace(" ", "").upper()

investigation_id = str(uuid.uuid4())[:8].upper()
timestamp = datetime.now(
    ZoneInfo("Asia/Kolkata")
).strftime("%Y-%m-%d %H:%M:%S")

print("\n[+] Investigation ID:", investigation_id)
print("[+] Timestamp:", timestamp)

pattern = r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}$"

if re.match(pattern, vehicle_number):

    print("\n[+] Valid vehicle number")
    print("[+] Vehicle:", vehicle_number)

    with open("vehicles.json", "r") as file:
        vehicles = json.load(file)

    if vehicle_number in vehicles:

        data = vehicles[vehicle_number]

        history_entry = {
            "investigation_id": investigation_id,
            "timestamp": timestamp,
            "vehicle_number": vehicle_number
        }

        with open("history.json", "r") as file:
            history = json.load(file)

        history.append(history_entry)

        with open("history.json", "w") as file:
            json.dump(history, file, indent=4)

        print("\n[+] Vehicle Found")
        print("----------------------------")
        print("RTO          :", data["rto"])
        print("Manufacturer :", data["manufacturer"])
        print("Model        :", data["model"])
        print("Fuel         :", data["fuel"])
        print("Status       :", data["status"])
        print("PUC          :", data["puc"])

        print("\n[+] Search saved to history")

    else:
        print("\n[-] Vehicle not found in database")

else:
    print("\n[-] Invalid vehicle number")
