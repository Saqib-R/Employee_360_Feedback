from flask import Flask, request, jsonify, send_file
import pandas as pd
import os
from flask_cors import CORS
from openai import AzureOpenAI
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os
import time
from datetime import datetime



load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Define a path for prompts
PROMPT_FILE = 'prompts.txt'

# Load prebuilt prompt
def load_prebuilt_prompt():
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, 'r') as file:
            return file.read().strip()
    return ""

# Save custom prompt
def save_custom_prompt(prompt):
    with open(PROMPT_FILE, 'a') as file:
        file.write(f"{prompt}\n")

# Load custom prompts
def load_custom_prompts():
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, 'r') as file:
            return file.readlines()
    return []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Initialize Azure OpenAI client
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION") 
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

client = AzureOpenAI()

app.config['UPLOAD_FOLDER'] = 'uploads'

# EXPORT SUMMARY TO CSV
# def exp_summarize_feedback(feedbacks):
#     if not feedbacks:
#         return "No feedback provided."

#     summaries = []

#     # Create two nuanced prompts for comprehensive summaries
#     prompts = [
#         "Provide a comprehensive summary in only 100 words of the following feedbacks, focusing on key strengths and areas for improvement:\n\n" + "\n".join(feedbacks),
#     ]

#     for prompt in prompts:
#         try:
#             res = client.chat.completions.create(
#                 model="gpt-4o",  # Use the appropriate model
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.7,
#                 max_tokens=150,  # Adjust token count based on desired output length
#                 top_p=0.9,
#                 frequency_penalty=0.5
#             )

#             # Extract summary from the response
#             summary = res.choices[0].message.content.strip()  # Adjusted to match the response structure
#             summaries.append(summary)

#         except Exception as e:
#             return f"Error during summarization: {str(e)}"

#     return summaries
def exp_summarize_feedback(feedbacks, prompt):
    if not feedbacks:
        return "No feedback provided."

    summaries = []
    
    # Create the prompt
    full_prompt = f"{prompt}:\n\n" + "\n".join(feedbacks)

    # Call to the chat completion model
    try:
        res = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_tokens=150,
            top_p=0.9,
            frequency_penalty=0.5
        )
        summary = res.choices[0].message.content.strip()
        print(summary)
        summaries.append(summary)

    except Exception as e:
        return f"Error during summarization: {str(e)}"

    return summaries



# CUSTOM PROMT SUMMARY
def cust_summarize_feedback(feedbacks, user_prompt):
    if not feedbacks:
        return "No feedback provided."

    # Create a prompt based on user input
    prompt = f"{user_prompt}\n\n" + "\n".join(feedbacks)

    try:
        res = client.chat.completions.create(
            model="gpt-4o",  # Use the appropriate model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150,
            top_p=0.9,
            frequency_penalty=0.5
        )

        # Extract summary from the response
        summary = res.choices[0].message.content.strip()  # Get the generated summary

    except Exception as e:
        return f"Error during summarization: {str(e)}"

    return summary

# Upload CSV and Read API
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        data = pd.read_csv(filepath)
        
        # Group by subject and aggregate questions into lists
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
        # print(result)
        return jsonify(result)

# Individual Summary API
@app.route('/summarize', methods=['POST'])
def summarize_feedback():
    # Get the feedback array from the request
    data = request.json
    feedbacks = data.get('feedbacks', [])

    if not feedbacks:
        return jsonify({"error": "No feedback provided"}), 400

    summaries = []

    # Create two nuanced prompts for comprehensive summaries
    # "Generate a detailed summary in only 50 words of the following feedbacks, highlighting achievements, teamwork, and how his\her efforts have enhanced the company's market position and operational efficiency:\n\n" + "\n".join(feedbacks)
    prompts = [
        "Provide a comprehensive summary in only 100 words of the following feedbacks, focusing on leadership, project management skills, and the overall impact and contributions on the team and company:\n\n" + "\n".join(feedbacks)
    ]

    for prompt in prompts:
        try:
            res = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=256,
                top_p=0.6,
                frequency_penalty=0.7
            )

            # Extract summary from the response
            summary = res.choices[0].message.content.strip()
            summaries.append(summary)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"summaries": summaries})

# Batch Summarization API
@app.route('/upload_feedback', methods=['POST'])
# def upload_feedback():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)

#         # Read the CSV file using Pandas
#         df = pd.read_csv(file_path)

#         # Initialize a list to store the summaries
#         summaries = []

#         # Group by employee (subject)
#         grouped = df.groupby('subject')

#         for employee, group in grouped:
#             level = group['level'].iloc[0]
#             job_title = group['job_title'].iloc[0]
#             function_code = group['function_code'].iloc[0]

#             # Summarize feedback for each question
#             for question in ['question1', 'question2', 'question3', 'question4']:
#                 feedbacks = group[question].dropna().tolist() 
#                 summary = exp_summarize_feedback(feedbacks)  
#                 cleaned_summary = [s.strip("[]'") for s in summary]
#                 final_summary = ' '.join(cleaned_summary) 
#                 summaries.append({
#                     "subject": employee,
#                     "level": level,
#                     "job_title": job_title,
#                     "function_code": function_code,
#                     "question": question,
#                     "summary": final_summary
#                 })

#         # Write summaries to a new CSV file
#         output_filename = 'summarized_feedback.csv'
#         output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
#         output_df = pd.DataFrame(summaries)
#         output_df.to_csv(output_path, index=False)

#         return jsonify({"message": "Summarization complete", "summaries": summaries}), 200

#     return jsonify({"error": "Invalid file type"}), 400
# Batch Summarization API
def upload_feedback():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    use_custom_prompt = request.form.get('use_custom_prompt', type=int)

    if use_custom_prompt == 1:
        custom_prompts = load_custom_prompts()
        if not custom_prompts:
            return jsonify({"error": "No custom prompt available. Please provide one or use the prebuilt prompt."}), 400
        current_prompt = custom_prompts[-1].strip()  # Use the latest custom prompt
    elif use_custom_prompt == 0:
        current_prompt = load_prebuilt_prompt()  # Use prebuilt prompt
    else:
        return jsonify({"error": "Invalid parameter for prompt selection."}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Read the CSV file using Pandas
        df = pd.read_csv(file_path)

        summaries = []
        grouped = df.groupby('subject')

        for employee, group in grouped:
            level = group['level'].iloc[0]
            job_title = group['job_title'].iloc[0]
            function_code = group['function_code'].iloc[0]

            # Summarize feedback for each question
            for idx, question in enumerate(['question1', 'question2', 'question3', 'question4']):
                feedbacks = group[question].dropna().tolist() 
                
                # Start timestamp for each question
                start_time = datetime.now()
                summary = exp_summarize_feedback(feedbacks, current_prompt)  
                final_summary = ' '.join(summary)
                end_time = datetime.now()
                
                duration = (end_time - start_time).total_seconds()  # Duration for this question
                str_timestamp = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                end_timestamp = end_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

                # Append summary with employee details only for the first question
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
                    # Only include question-specific details for subsequent questions
                    summaries.append({
                        "subject": "",  # Leave blank for subsequent rows
                        "level": "",    # Leave blank for subsequent rows
                        "job_title": "", # Leave blank for subsequent rows
                        "function_code": "", # Leave blank for subsequent rows
                        "question": question,
                        "summary": final_summary,
                        "start_timestamp": str_timestamp,
                        "end_timestamp": end_timestamp,
                        "duration": duration
                    })

        # Write summaries to a new CSV file
        output_filename = 'summarized_feedback.csv'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        # Prepare DataFrame for output
        output_df = pd.DataFrame(summaries)

        output_df.to_csv(output_path, index=False)

        return jsonify({"message": "Summarization complete", "summaries": summaries}), 200

    return jsonify({"error": "Invalid file type"}), 400  


# Download Summary CSV
@app.route('/download_feedback', methods=['GET'])
def download_feedback():
    output_filename = 'summarized_feedback.csv'
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    
    return jsonify({"error": "File not found"}), 404

# Custom Summary API
@app.route('/custom_summarize', methods=['POST'])
def summarize():
    data = request.get_json()

    if not data or 'feedbacks' not in data or 'prompt' not in data:
        return jsonify({"error": "Invalid input. Please provide both 'feedbacks' and 'prompt'."}), 400

    feedbacks = data['feedbacks']
    prompt = data['prompt']

    # Save the custom prompt
    save_custom_prompt(prompt)

    # Call the summarization function
    summary = cust_summarize_feedback(feedbacks, prompt)

    # Return the response as JSON
    return jsonify({"summary": summary})


if __name__ == '__main__':
    app.run(debug=True)