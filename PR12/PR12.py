# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

def read_json(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        data = []
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        data = []
    return data

def write_json(filename, data):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)
    except Exception as e:
        print(f"Error writing to file {filename}: {e}")

def display_contents(filename):
    data = read_json(filename)
    print("Contents of the JSON file:")
    print(json.dumps(data, indent=2))

def add_record(filename, record):
    data = read_json(filename)
    data.append(record)
    write_json(filename, data)
    print("Record added successfully.")

def delete_record(filename, record_index):
    data = read_json(filename)
    if 0 <= record_index < len(data):
        del data[record_index]
        write_json(filename, data)
        print("Record deleted successfully.")
    else:
        print("Invalid record index.")

def search_by_field(filename, field, value):
    data = read_json(filename)
    results = [record for record in data if record.get(field) == value]
    print(f"Search results for {field} = {value}:")
    print(json.dumps(results, indent=2))

def calculate_total_cost(filename, cutoff_date):
    data = read_json(filename)
    total_cost = 0

    for record in data:
        production_date_str = record.get('production_date')
        if production_date_str:
            production_date = datetime.strptime(production_date_str, '%Y-%m-%d')
            
            # Перевірка, чи дата належить тому ж тижню, що і вказана cutoff_date
            if (cutoff_date - timedelta(days=cutoff_date.weekday())) <= production_date <= (cutoff_date + timedelta(days=(6 - cutoff_date.weekday()))):
                total_cost += record.get('details_cost', 0)

    print(f"Total cost of details for the week of {cutoff_date}: {total_cost}")

def main():
    input_filename = 'details_data.json'
    output_filename = 'results.json'

    while True:
        print("\nMenu:")
        print("1. Display contents of JSON file")
        print("2. Add a new record to JSON file")
        print("3. Delete a record from JSON file")
        print("4. Search data in JSON file by field")
        print("5. Calculate total cost of details for the week")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            display_contents(input_filename)
        elif choice == '2':
            try:
                new_record = json.loads(input("Enter a new record in JSON format: "))
                add_record(input_filename, new_record)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        elif choice == '3':
            record_index = int(input("Enter the index of the record to delete: "))
            delete_record(input_filename, record_index)
        elif choice == '4':
            field = input("Enter the field to search: ")
            value = input("Enter the value to search for: ")
            search_by_field(input_filename, field, value)
        elif choice == '5':
            try:
                cutoff_date_str = input("Enter the cutoff date (YYYY-MM-DD): ")
                cutoff_date = datetime.strptime(cutoff_date_str, '%Y-%m-%d')
                calculate_total_cost(input_filename, cutoff_date)
            except ValueError:
                print("Invalid date format. Please enter date in YYYY-MM-DD format.")
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
