import json
from datetime import datetime

def check_po_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    errors = 0
    for index, item in enumerate(data):
        city = item.get('city', 'Unknown')
        v_date = item.get('visited_date')

        # Check 1: Is it a valid type for JSON?
        if v_date is not None and not isinstance(v_date, str):
            print(f"❌ ROW {index} ({city}): Data is {type(v_date)}, expected string or null.")
            errors += 1
            continue

        # Check 2: Can it be parsed?
        if v_date and str(v_date).lower() != 'none':
            try:
                datetime.fromisoformat(v_date)
            except ValueError:
                print(f"❌ ROW {index} ({city}): Invalid Format -> '{v_date}'")
                errors += 1

    if errors == 0:
        print("✅ All dates are valid strings or nulls!")
    else:
        print(f"\nFound {errors} errors in your JSON file.")

check_po_json('po.json')
