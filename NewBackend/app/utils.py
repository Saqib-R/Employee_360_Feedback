import os
from flask import current_app
import csv
import pandas as pd

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}

def load_prebuilt_prompt():
    prompt_file_path = current_app.config['PROMPT_FILE']
    if os.path.exists(prompt_file_path):
        with open(prompt_file_path, 'r') as file:
            return file.read().strip()
    return ""

def save_custom_prompt(prompt):
    prompt_file_path = current_app.config['PROMPT_FILE']
    if os.path.exists(prompt_file_path):
        with open(prompt_file_path, 'a') as file:
            file.write(f"{prompt}\n")
    return ""

def load_custom_prompts():
    prompt_file_path = current_app.config['PROMPT_FILE']
    if os.path.exists(prompt_file_path):
        with open(prompt_file_path, 'r') as file:
            return file.readlines()
    return []



# def update_or_create_csv(emp_data, summary, csv_path, status="not approved"):
#     """
#     Updates or creates a CSV file to store employee data and summaries.
#     Ensures no duplicate rows for the same employee ID.
#     """
#     file_exists = os.path.exists(csv_path)
    
#     # Define the headers for the CSV file
#     headers = ['emp_id', 'subject', 'job_title', 'manager', 'function_code', 'level', 'summary', 'status']

#     # Load existing data if the file exists
#     rows = []
#     if file_exists:
#         with open(csv_path, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             rows = list(reader)
    
#     # Ensure emp_id is a string for comparison
#     emp_id = str(emp_data.get('emp_id'))  # Convert emp_id to string
    
#     # Prepare the new row
#     new_row = {
#         'emp_id': emp_id,
#         'subject': emp_data.get('subject'),
#         'job_title': emp_data.get('job_title'),
#         'manager': emp_data.get('manager'),
#         'function_code': emp_data.get('function_code'),
#         'level': emp_data.get('level'),
#         'summary': summary,
#         'status': status
#     }

#     # Filter out any existing rows with the same emp_id
#     rows = [row for row in rows if row['emp_id'] != emp_id]
    
#     # Add the new or updated row
#     rows.append(new_row)

#     # Debugging: Print rows to verify updates
#     print(f"Updated rows: {rows}")

#     # Write the updated data back to the CSV file
#     with open(csv_path, 'w', newline='') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=headers)
#         writer.writeheader()
#         writer.writerows(rows)

#     print(f"Data successfully written to {csv_path}")



def update_or_create_csv(emp_data, summary, csv_path, status="not approved"):
    """
    Updates or creates a CSV file to store employee data and summaries.
    Ensures no duplicate rows for the same employee ID and handles commas in text fields.
    """
    # print("SUMMARY", summary)
    file_exists = os.path.exists(csv_path)
    
    # Define the headers for the CSV file
    headers = ['emp_id', 'subject', 'job_title', 'manager', 'function_code', 'level', 'summary', 'status']

    # Load existing data if the file exists
    rows = []
    if file_exists:
        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
    
    # Ensure emp_id is a string for comparison
    emp_id = str(emp_data.get('emp_id'))  # Convert emp_id to string
    
    # Prepare the new row
    new_row = {
        'emp_id': emp_id,
        'subject': emp_data.get('subject'),
        'job_title': emp_data.get('job_title'),
        'manager': emp_data.get('manager'),
        'function_code': emp_data.get('function_code'),
        'level': emp_data.get('level'),
        'summary': summary,
        'status': status
    }

    # Filter out any existing rows with the same emp_id
    rows = [row for row in rows if row['emp_id'] != emp_id]
    
    # Add the new or updated row
    rows.append(new_row)

    # Write the updated data back to the CSV file
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=headers,
            quotechar='"',
            quoting=csv.QUOTE_ALL
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Data successfully written to {csv_path}")


#  Function to return the last row from summarized data
def get_last_row_of_csv():
    filepath = os.path.join(current_app.config['CSV_FILE_PATH'])
    try:
        # Read the CSV file
        df = pd.read_csv(filepath, encoding='cp1252')

        # Check if the DataFrame is empty
        if df.empty:
            return ({"status": "error", "message": "CSV file is empty"})
        
        # Get the last row of the DataFrame
        last_row = df.tail(1).to_dict(orient='records')[0] 
        return last_row

    except FileNotFoundError:
        return "CSV file not found"
    except Exception as e:
        return ({"status": "error", "message": str(e)})