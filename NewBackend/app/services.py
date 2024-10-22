import os
import pandas as pd
from flask import jsonify, request, current_app, send_file
from .utils import allowed_file, load_custom_prompts, save_custom_prompt, load_prebuilt_prompt
from .prompts import exp_summarize_feedback, cust_summarize_feedback
from datetime import datetime
from werkzeug.utils import secure_filename


def upload_file():
    if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
        os.makedirs(current_app.config['UPLOAD_FOLDER'])

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        data = pd.read_csv(filepath)
        
        # Group by emp_id and aggregating questions into lists
        grouped_data = data.groupby('emp_id').agg({
            'subject': 'first',      # Keep the first subject for each emp_id
            'level': 'first',        # Keep the first level for each emp_id
            'job_title': 'first',    # Keep the first job title for each emp_id
            'function_code': 'first',# Keep the first function code for each emp_id
            'manager': 'first',      # Keep the first manager for each emp_id
            'question1': lambda x: list(x),  # Aggregate question1 responses into a list
            'question2': lambda x: list(x),  # Aggregate question2 responses into a list
            'question3': lambda x: list(x),  # Aggregate question3 responses into a list
            'question4': lambda x: list(x)   # Aggregate question4 responses into a list
        }).reset_index()
        
        # Convert the grouped DataFrame to a dictionary format
        result = grouped_data.to_dict(orient='records')
        return jsonify(result)


def summarize_feedback():
    data = request.json
    feedbacks = data.get('feedbacks', [])

    if not feedbacks:
        return jsonify({"error": "No feedback provided"}), 400

    prompt = "Provide a comprehensive summary in only 100 words of the following feedbacks, focusing on leadership, project management skills, and the overall impact and contributions on the team and company:\n\n" + "\n".join(feedbacks)

    try:
        summary = cust_summarize_feedback(feedbacks, prompt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"summaries": [summary]})


def upload_feedback():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    use_custom_prompt = request.form.get('use_custom_prompt', type=int)

    if use_custom_prompt == 2:
        custom_prompts = load_custom_prompts()
        if not custom_prompts:
            return jsonify({"error": "No custom prompt available. Please provide one or use the prebuilt prompt."}), 400
        current_prompt = custom_prompts[-1].strip()
    elif use_custom_prompt == 1:
        current_prompt = "Provide a comprehensive summary in only 100 words of the following feedbacks, focusing on leadership, project management skills, and the overall impact and contributions on the team and company"
    else:
        return jsonify({"error": "Invalid parameter for prompt selection."}), 400
    
    print(use_custom_prompt,current_prompt)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        df = pd.read_csv(file_path)
        summaries = []
        grouped = df.groupby('subject')

        for employee, group in grouped:
            level = group['level'].iloc[0]
            job_title = group['job_title'].iloc[0]
            function_code = group['function_code'].iloc[0]
            manager = group['manager'].iloc[0]
            emp_id = int(group['emp_id'].iloc[0])  # Convert to standard int

            for idx, question in enumerate(['question1', 'question2', 'question3', 'question4']):
                feedbacks = group[question].dropna().tolist()
                
                start_time = datetime.now()
                summary = exp_summarize_feedback(feedbacks, current_prompt)  
                final_summary = ' '.join(summary)
                end_time = datetime.now()
                
                duration = (end_time - start_time).total_seconds() 
                str_timestamp = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                end_timestamp = end_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

                if idx == 0:
                    summaries.append({
                        "subject": employee,
                        "level": level,
                        "job_title": job_title,
                        "function_code": function_code,
                        "manager": manager,
                        "emp_id": emp_id,  # Already converted
                        "question": question,
                        "summary": final_summary,
                        "start_timestamp": str_timestamp,
                        "end_timestamp": end_timestamp,
                        "duration": duration
                    })
                else:
                    summaries.append({
                        "subject": "", 
                        "level": "",   
                        "job_title": "",
                        "function_code": "",
                        "manager": "", 
                        "emp_id": None,  # Set to None for JSON serialization
                        "question": question,
                        "summary": final_summary,
                        "start_timestamp": str_timestamp,
                        "end_timestamp": end_timestamp,
                        "duration": duration
                    })

        output_filename = 'summarized_feedback.csv'
        output_path = os.path.join(current_app.config['UPLOAD_FOLDER'], output_filename)

        output_df = pd.DataFrame(summaries)
        output_df.to_csv(output_path, index=False)

        return jsonify({"message": "Summarization complete", "summaries": summaries}), 200

    return jsonify({"error": "Invalid file type"}), 400


def download_feedback():
    output_filename = 'summarized_feedback.csv'
    output_path = os.path.join(current_app.config['UPLOAD_FOLDER'], output_filename)

    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    
    return jsonify({"error": "File not found"}), 404


def custom_summarize():
    data = request.get_json()

    if not data or 'feedbacks' not in data or 'prompt' not in data:
        return jsonify({"error": "Invalid input. Please provide both 'feedbacks' and 'prompt'."}), 400

    feedbacks = data['feedbacks']
    prompt = data['prompt']

    # Saving the custom prompt
    save_custom_prompt(prompt)

    summary = cust_summarize_feedback(feedbacks, prompt)

    return jsonify({"summary": summary})


def get_summarized_feedback():
    # Get the manager's name from the request
    manager_name = request.args.get('manager')

    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'summarized_feedback.csv')
    
    # Read the summarized_feedback CSV file
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        return jsonify({'error': f'Error reading the CSV file: {str(e)}'})

    # Fill forward the employee details to the empty rows
    df.fillna(method='ffill', inplace=True)

    # Filter by manager name if provided
    if manager_name:
        df = df[df['manager'].str.lower() == manager_name.lower()]

    employees = {}

    # Iterate over each row in the filtered DataFrame
    for _, row in df.iterrows():
        # Convert emp_id to int to avoid float representation
        emp_id = int(row['emp_id']) if pd.notna(row['emp_id']) else None
        subject = row['subject']
        level = row['level']
        job_title = row['job_title']
        function_code = row['function_code']
        question_number = row['question']

        # Only initialize a new employee entry if the subject is found
        if emp_id is not None and emp_id not in employees:
            employees[emp_id] = {
                'emp_id': emp_id,
                'subject': subject,
                'function_code': function_code,
                'job_title': job_title,
                'level': level,
                'questions': {}
            }
        
        if pd.notna(question_number):
            employees[emp_id]['questions'][question_number] = {
                'summary': row['summary'],
                'start_time': row['start_timestamp'] if pd.notna(row['start_timestamp']) else None,
                'end_time': row['end_timestamp'] if pd.notna(row['end_timestamp']) else None,
                'duration': row['duration'] if pd.notna(row['duration']) else None
            }

    # Convert the employee dictionary to a list of values (to get the desired JSON structure)
    return jsonify(list(employees.values()))


def get_feedback_data():
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'newEmpData.csv')

        try:
            data = pd.read_csv(filepath)
        except Exception as e:
            return jsonify({'error': f'Error reading the CSV file: {str(e)}'})

        
        # Group by emp_id and aggregating questions into lists
        grouped_data = data.groupby('emp_id').agg({
            'subject': 'first',      # Keep the first subject for each emp_id
            'level': 'first',        # Keep the first level for each emp_id
            'job_title': 'first',    # Keep the first job title for each emp_id
            'function_code': 'first',# Keep the first function code for each emp_id
            'manager': 'first',      # Keep the first manager for each emp_id
            'question1': lambda x: list(x),  # Aggregate question1 responses into a list
            'question2': lambda x: list(x),  # Aggregate question2 responses into a list
            'question3': lambda x: list(x),  # Aggregate question3 responses into a list
            'question4': lambda x: list(x)   # Aggregate question4 responses into a list
        }).reset_index()
        
        # Convert the grouped DataFrame to a dictionary format
        result = grouped_data.to_dict(orient='records')
        return jsonify(result)
