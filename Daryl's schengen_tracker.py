#!/usr/bin/env python3

from datetime import datetime, timedelta

WINDOW_DAYS = 180
MAX_DAYS = 90

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

def daterange(start, end):
    for n in range((end - start).days + 1):
        yield start + timedelta(days=n)

def get_used_days(trips, reference_date):
    window_start = reference_date - timedelta(days=WINDOW_DAYS)
    used_days = set()

    for trip in trips:
        entry = trip['entry']
        exit = trip['exit'] if trip['exit'] else reference_date

        for day in daterange(entry, exit):
            if window_start < day <= reference_date:
                used_days.add(day)

    return len(used_days)

def calculate_status(trips, today):
    used = get_used_days(trips, today)
    remaining = MAX_DAYS - used
    return used, remaining

def find_latest_exit_date(trips, today):
    current = today

    while True:
        used = get_used_days(trips, current)
        if used > MAX_DAYS:
            return current - timedelta(days=1)
        current += timedelta(days=1)

def get_trip_input():
    trips = []

    print("\nEnter your travel history.")
    print("Format: YYYY-MM-DD (example: 2024-06-15)\n")

    while True:
        entry_str = input("Entry date: ").strip()
        entry_date = parse_date(entry_str)

        if not entry_date:
            print("Invalid date format. Try again.\n")
            continue

        exit_str = input("Exit date (or press Enter if still inside): ").strip()

        if exit_str == "":
            exit_date = None
        else:
            exit_date = parse_date(exit_str)
            if not exit_date:
                print("Invalid exit date format.\n")
                continue
            if exit_date < entry_date:
                print("Exit date cannot be before entry date.\n")
                continue

        trips.append({
            "entry": entry_date,
            "exit": exit_date
        })

        more = input("Add another trip? (y/n): ").strip().lower()
        if more != "y":
            break

    return trips

def main():
    print("=" * 40)
    print(" Schengen 90/180 Day Calculator ")
    print("=" * 40)

    trips = get_trip_input()

    today = datetime.today()
    used, remaining = calculate_status(trips, today)

    print("\n--- RESULTS ---")
    print(f"Days used in last 180 days: {used}")
    print(f"Remaining days: {remaining}")

    if remaining > 0:
        exit_date = find_latest_exit_date(trips, today)
        print(f"Latest allowed exit date: {exit_date.strftime('%Y-%m-%d')}")
    else:
        print("You have exceeded the 90-day limit.")

    print("\nDone.\n")

if __name__ == "__main__":
    main()
