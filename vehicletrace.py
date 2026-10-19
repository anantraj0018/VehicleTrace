
#!/usr/bin/env python3

import re
import json
import uuid
import os
from datetime import datetime
from zoneinfo import ZoneInfo


def get_timestamp():
    return datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%Y-%m-%d %H:%M:%S")


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
            and str(entry.get("vehicle_number", "")).upper() == number
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


def save_report(report):
    try:
        os.makedirs("reports", exist_ok=True)

        filename = f"reports/{report['investigation_id']}.json"

        with open(filename, "w") as file:
            json.dump(report, file, indent=4)

        print("\n[+] Investigation report saved:", filename)

    except (OSError, KeyError):
        print("\n[-] Could not save investigation report")


def view_report():
    print("\n====================================")
    print("       Investigation Reports")
    print("====================================")

    try:
        files = sorted(
            filename for filename in os.listdir("reports")
            if filename.endswith(".json")
        )

    except FileNotFoundError:
        print("\n[-] Reports folder not found")
        return
    except OSError:
        print("\n[-] Could not access reports folder")
        return

    if not files:
        print("\n[-] No investigation reports found")
        return

    print("\nAvailable Reports:")

    for i, filename in enumerate(files, start=1):
        print(f"{i}. {filename}")

    choice = input("\n[?] Enter report number: ")

    if not choice.isdigit():
        print("\n[-] Invalid choice. Enter a number.")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(files):
        print("\n[-] Report not found")
        return

    filepath = os.path.join("reports", files[index])

    try:
        with open(filepath, "r") as file:
            report = json.load(file)

        if not isinstance(report, dict):
            print("\n[-] Report data format is invalid")
            return

        print("\n========== Investigation Report ==========")
        print("Investigation ID :", report.get("investigation_id", "Unknown"))
        print("Timestamp        :", report.get("timestamp", "Unknown"))
        print("Vehicle Number   :", report.get("vehicle_number", "Unknown"))
        print("Source           :", report.get("source", "Unknown"))

        details = report.get("vehicle_details", {})

        if not isinstance(details, dict):
            print("\n[-] Vehicle details format is invalid")
            return

        print("\nVehicle Details")
        print("------------------------------------------")
        print("RTO          :", details.get("rto", "Unknown"))
        print("Manufacturer :", details.get("manufacturer", "Unknown"))
        print("Model        :", details.get("model", "Unknown"))
        print("Fuel         :", details.get("fuel", "Unknown"))
        print("Status       :", details.get("status", "Unknown"))
        print("PUC          :", details.get("puc", "Unknown"))

    except json.JSONDecodeError:
        print("\n[-] Report file is corrupted")
    except OSError:
        print("\n[-] Could not read report file")


def search_vehicle():
    vehicle_number = input("\n[?] Enter vehicle number: ")
    vehicle_number = vehicle_number.replace(" ", "").upper()

    pattern = r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}$"

    if not re.match(pattern, vehicle_number):
        print("\n[-] Invalid vehicle number")
        return

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

    if not isinstance(data, dict):
        print("\n[-] Vehicle record format is invalid")
        return

    investigation_id = str(uuid.uuid4())[:8].upper()
    timestamp = get_timestamp()

    print("\n[+] Investigation ID:", investigation_id)
    print("[+] Timestamp:", timestamp)
    print("[+] Valid vehicle number")

    report = {
        "investigation_id": investigation_id,
        "timestamp": timestamp,
        "vehicle_number": vehicle_number,
        "source": "Local sample database",
        "vehicle_details": data
    }

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

    save_report(report)


print("""
====================================
        VehicleTrace
   Vehicle OSINT Investigation Tool
====================================
""")

while True:
    print("\n1. Search Vehicle")
    print("2. View Search History")
    print("3. View Investigation Report")
    print("4. Exit")

    choice = input("\n[?] Choose an option: ")

    if choice == "1":
        search_vehicle()
    elif choice == "2":
        view_history()
    elif choice == "3":
        view_report()
    elif choice == "4":
        print("\n[+] Exiting VehicleTrace. Goodbye!")
        break
    else:
        print("\n[-] Invalid option. Choose 1, 2, 3 or 4.")
