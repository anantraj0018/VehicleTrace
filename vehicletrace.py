
#!/usr/bin/env python3

import re
import json
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo


def view_history():
    print("\n====================================")
    print("       VehicleTrace History")
    print("====================================")

    with open("history.json", "r") as file:
        history = json.load(file)

    if not history:
        print("\n[-] No search history found")
        return

    for i, entry in enumerate(history, start=1):
        print(f"\n{i}. Vehicle: {entry['vehicle_number']}")
        print(f"   Investigation ID: {entry['investigation_id']}")
        print(f"   Timestamp: {entry['timestamp']}")


def search_vehicle():
    vehicle_number = input("\n[?] Enter vehicle number: ")
    vehicle_number = vehicle_number.replace(" ", "").upper()

    pattern = r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}$"

    if not re.match(pattern, vehicle_number):
        print("\n[-] Invalid vehicle number")
        return

    investigation_id = str(uuid.uuid4())[:8].upper()
    timestamp = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%Y-%m-%d %H:%M:%S")

    print("\n[+] Investigation ID:", investigation_id)
    print("[+] Timestamp:", timestamp)
    print("[+] Valid vehicle number")

    with open("vehicles.json", "r") as file:
        vehicles = json.load(file)

    if vehicle_number not in vehicles:
        print("\n[-] Vehicle not found in database")
        return

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


print("""
====================================
        VehicleTrace
   Vehicle OSINT Investigation Tool
====================================
""")

while True:
    print("\n1. Search Vehicle")
    print("2. View Search History")
    print("3. Exit")

    choice = input("\n[?] Choose an option: ")

    if choice == "1":
        search_vehicle()
    elif choice == "2":
        view_history()
    elif choice == "3":
        print("\n[+] Exiting VehicleTrace. Goodbye!")
        break
    else:
        print("\n[-] Invalid option. Choose 1, 2 or 3.")
