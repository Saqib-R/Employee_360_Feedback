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
        
        # Group by subject and aggregating questions into lists
        grouped_data = data.groupby('subject').agg({
            'level': 'first',
            'job_title': 'first',
            'function_code': 'first',
            'question1': lambda x: list(x),
            'question2': lambda x: list(x),
            'question3': lambda x: list(x),
            'question4': lambda x: list(x)
        }).reset_index()
        
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
        current_prompt = load_prebuilt_prompt()
    else:
        return jsonify({"error": "Invalid parameter for prompt selection."}), 400

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
