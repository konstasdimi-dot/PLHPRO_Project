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
