from texttable import Texttable
import json

def save_user_data(user_id, user_data):
    """
        Save User Information
    """    
    # Read data
    try:
        with open('database.json', 'r', encoding='utf-8') as json_file:
            users_data = json.load(json_file)
    except ValueError:
        users_data = {} # Default: empty

    # Update data
    users_data[str(user_id)] = user_data

    # Save data
    with open('database.json', 'w', encoding='utf-8') as json_file:
        json.dump(users_data, json_file, indent=4, sort_keys=True)

def get_user(user_id):
    """
        Read User Information
    """
    user_id = str(user_id)
    try:
        with open('database.json', 'r', encoding='utf-8') as json_file:
            users_data = json.load(json_file)
        if user_id in users_data:
            return users_data[user_id]
    except ValueError:
        return None

def draw_table(number):
    """
        Draw percentages table.
    """
    percentages = [50, 55, 60, 62, 63, 65, 66, 67, 68, 70, 72, 73, 75, 76, 78, 80, 82, 85, 88, 90, 95, 98, 102, 105, 107]
    records = [['%', 'Weight']] # Headers

    for p in percentages:
        weight = round(float(p*number/100), 2)
        records.append([f'{p}%', f'{weight:.2f}\tKg'])

    # Table Creation
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.add_rows([row for row in records])

    return f"```{table.draw()}```"