from flask import Flask, request, jsonify, send_file
import pandas as pd
import os
from flask_cors import CORS
from openai import AzureOpenAI
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['ALLOWED_EXTENSIONS'] = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Initialize Azure OpenAI client
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION") 
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

client = AzureOpenAI()

app.config['UPLOAD_FOLDER'] = 'uploads'

# EXPORT SUMMARY TO CSV
def exp_summarize_feedback(feedbacks):
    if not feedbacks:
        return "No feedback provided."

    summaries = []

    # Create two nuanced prompts for comprehensive summaries
    prompts = [
        "Provide a comprehensive summary in only 100 words of the following feedbacks, focusing on key strengths and areas for improvement:\n\n" + "\n".join(feedbacks),
    ]

    for prompt in prompts:
        try:
            res = client.chat.completions.create(
                model="gpt-4o",  # Use the appropriate model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150,  # Adjust token count based on desired output length
                top_p=0.9,
                frequency_penalty=0.5
            )

            # Extract summary from the response
            summary = res.choices[0].message.content.strip()  # Adjusted to match the response structure
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
    prompts = [
        "Provide a comprehensive summary in only 100 words of the following feedbacks, focusing on leadership, project management skills, and the overall impact and contributions on the team and company:\n\n" + "\n".join(feedbacks),
        "Generate a detailed summary in only 50 words of the following feedbacks, highlighting achievements, teamwork, and how his\her efforts have enhanced the company's market position and operational efficiency:\n\n" + "\n".join(feedbacks)
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
def upload_feedback():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Read the CSV file using Pandas
        df = pd.read_csv(file_path)

        # Initialize a list to store the summaries
        summaries = []

        # Group by employee (subject)
        grouped = df.groupby('subject')

        for employee, group in grouped:
            level = group['level'].iloc[0]
            job_title = group['job_title'].iloc[0]
            function_code = group['function_code'].iloc[0]

            # Summarize feedback for each question
            for question in ['question1', 'question2', 'question3', 'question4']:
                feedbacks = group[question].dropna().tolist() 
                summary = exp_summarize_feedback(feedbacks)  
                cleaned_summary = [s.strip("[]'") for s in summary]
                final_summary = ' '.join(cleaned_summary) 
                summaries.append({
                    "subject": employee,
                    "level": level,
                    "job_title": job_title,
                    "function_code": function_code,
                    "question": question,
                    "summary": final_summary
                })

        # Write summaries to a new CSV file
        output_filename = 'summarized_feedback.csv'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
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

    # Call the summarization function
    summary = cust_summarize_feedback(feedbacks, prompt)

    # Return the response as JSON
    return jsonify({"summary": summary})


if __name__ == '__main__':
    app.run(debug=True)