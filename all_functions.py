import json
import os

# Validating Activities ----------
def validate_activity_data(name,category, hours_str, importance_str):

    if not name or not hours_str or not importance_str:
        return False, "Please enter all required information."

    try:
        hours = float(hours_str)
        importance = int(importance_str)
    except ValueError:
        return False, "Hours must be a valid number."

    valid_activity = {
        "name": name,
        "category": category,
        "hours": hours,
        "importance": importance
    }

    return True, valid_activity

# Calculating Tab 2 Information ----------
def calculate_optimal_schedule(database, total_available_time):
    sorted_activities = sorted(database, key=lambda x: x["importance"], reverse=True)

    feasible = []
    rejected = []
    current_time = 0.0

    for activity in sorted_activities:
        if current_time + activity["hours"] <= total_available_time:
            feasible.append(activity)
            current_time += activity["hours"]
        else:
            rejected.append(activity)

    return feasible, rejected

# Saving & Loading Data ----------

DATA_FILE = "user_activities.json"

def save_data(database):

    try:
        with open(DATA_FILE, "w", encoding='utf_8') as f:
            json.dump(database, f, indent=4)
    except Exception as e:
        print(f"Warning: Could not save the data: {e}")

def load_data():

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding='utf_8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load the data: {e}")
        return []