
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

    try:
        with open("history.json", "r") as file:
            history = json.load(file)

        if not isinstance(history, list):
            print("\n[-] History data format is invalid")
            return

    except FileNotFoundError:
        print("\n[-] History file not found")
        return

    except json.JSONDecodeError:
        print("\n[-] History file is corrupted")
        return

    print("\n[+] Total Investigations:", len(history))

    if not history:
        print("\n[-] No search history found")
        return

    print("\n1. View All History")
    print("2. Search by Vehicle Number")

    choice = input("\n[?] Choose an option: ")

    if choice == "1":
        filtered_history = history

    elif choice == "2":
        number = input("\n[?] Enter vehicle number: ")
        number = number.replace(" ", "").upper()

        filtered_history = [
            entry for entry in history
            if isinstance(entry, dict)
            and entry.get("vehicle_number", "").upper() == number
        ]

    else:
        print("\n[-] Invalid option")
        return

    if not filtered_history:
        print("\n[-] No matching history found")
        return

    for i, entry in enumerate(filtered_history, start=1):
        print(f"\n{i}. Vehicle: {entry.get('vehicle_number', 'Unknown')}")
        print(f"   Investigation ID: {entry.get('investigation_id', 'Unknown')}")
        print(f"   Timestamp: {entry.get('timestamp', 'Unknown')}")


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

    try:
        with open("vehicles.json", "r") as file:
            vehicles = json.load(file)

        if not isinstance(vehicles, dict):
            print("\n[-] Vehicle database format is invalid")
            return

    except FileNotFoundError:
        print("\n[-] Vehicle database file not found")
        return

    except json.JSONDecodeError:
        print("\n[-] Vehicle database is corrupted")
        return

    if vehicle_number not in vehicles:
        print("\n[-] Vehicle not found in database")
        return

    data = vehicles[vehicle_number]

    history_entry = {
        "investigation_id": investigation_id,
        "timestamp": timestamp,
        "vehicle_number": vehicle_number
    }

    try:
        with open("history.json", "r") as file:
            history = json.load(file)

        if not isinstance(history, list):
            print("\n[-] History data format is invalid")
            return

    except FileNotFoundError:
        history = []

    except json.JSONDecodeError:
        print("\n[-] History file is corrupted. Search not saved.")
        return

    history.append(history_entry)

    try:
        with open("history.json", "w") as file:
            json.dump(history, file, indent=4)

    except OSError:
        print("\n[-] Could not save search history")
        return

    print("\n[+] Vehicle Found")
    print("----------------------------")
    print("RTO          :", data.get("rto", "Unknown"))
    print("Manufacturer :", data.get("manufacturer", "Unknown"))
    print("Model        :", data.get("model", "Unknown"))
    print("Fuel         :", data.get("fuel", "Unknown"))
    print("Status       :", data.get("status", "Unknown"))
    print("PUC          :", data.get("puc", "Unknown"))
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
