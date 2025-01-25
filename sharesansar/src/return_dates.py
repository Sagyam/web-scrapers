from datetime import date, timedelta

def get_dates(start_date: date, end_date: date) -> list:
    """Generate a list of dates between start_date and end_date, skipping Saturdays."""
    dates = []
    current_date = start_date
    saturdays_count = 0
    while current_date <= end_date:
        # Skip Saturdays (weekday() returns 5 for Saturday)
        if current_date.weekday() != 5:
            dates.append(current_date.strftime("%Y-%m-%d"))  # Format the date as needed
        else:
            saturdays_count += 1
        current_date += timedelta(days=1)

    if saturdays_count:
        print(f"Skipped {saturdays_count} Saturdays")
    return dates