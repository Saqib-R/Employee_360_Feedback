import os
import pandas as pd
from flask import jsonify, request, current_app, send_file
from .utils import allowed_file, load_custom_prompts, save_custom_prompt, load_prebuilt_prompt
from .prompts import exp_summarize_feedback, cust_summarize_feedback
from datetime import datetime
from .faiss_embeddings import query_faiss
from .query_expectations import get_query_expectations
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from openai import AzureOpenAI


load_dotenv()
# Initialize Azure OpenAI client
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL")


client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)


# Service to upload CSV and read all employee data
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


# Service to generate vanilla summary of feedbacks
def vanilla_summarize_feedback():
    data = request.json
    feedbacks = data.get('feedbacks', [])

    if not feedbacks:
        return jsonify({"error": "No feedback provided"}), 400

    # prompt = "Provide a comprehensive summary of the following feedbacks.:\n\n" + "\n".join(feedbacks)
    # prompt = (
    #     "Summarize the following feedback comprehensively, retaining critical keywords and core themes to capture the context and sentiment accurately:\n\n"
    #     + "\n".join(feedbacks)
    # )

    # prompt = (
    # "Summarize the following feedback comprehensively, retaining critical keywords and core themes to capture the context and sentiment accurately. "
    # "Where possible, indicate the source of each summarized point with reference to the feedback number in parentheses (e.g., '(1)', '(2)').:\n\n"
    # + "\n".join(f"[{i+1}] {feedback}" for i, feedback in enumerate(feedbacks))
    # )

    prompt = (
    "Summarize the following feedback comprehensively in a paragraph, focusing on key achievements, contributions, strengths, weakness, area of improvement and skills. Retain essential keywords and themes, and refer to feedback sources by including their feedback numbers in parentheses (e.g., '(1)', '(3)') as appropriate to highlight relevant examples, without requiring a sequential order:\n\n"
    + "\n".join(f"[{i+1}] {feedback}" for i, feedback in enumerate(feedbacks))
    )

    
    
    # Concatenate feedbacks
    # feedbacks_text = "\n".join(feedbacks)

    # Define prompt with formatted output without asterisks
    # prompt = f"""
    # Format the following feedback into a comprehensive summary using plain text with line breaks indicated by "\n" for clear separation. Do not include Markdown symbols like asterisks or hashtags. Please follow this structure, using "\n" where specified to ensure proper formatting:

    # \n
    # 1. Leadership Qualities:\n
    # - Key Strengths: Summarize key strengths,  .\n
    # - Influence on Team Dynamics: Summarize impact on team morale,  .\n
    # - Growth Opportunities: Outline growth opportunities,  .\n
    # \n
    # 2. Project Management Skills:\n
    # - Execution and Organization: Summarize project execution skills,  .\n
    # - Problem-Solving Abilities: Summarize problem-solving abilities,  .\n
    # - Opportunities for Development: List areas for improvement,  .\n
    # \n
    # 3. Overall Contributions:\n
    # - Impact on Company Objectives: Summarize impact on objectives,  .\n
    # - Collaboration and Teamwork: Summarize collaboration efforts,  .\n
    # - Innovation and Initiative: List contributions to innovation,  .\n
    # \n
    # 4. Measurable Impact:\n
    # - Key Outcomes: Summarize results and key outcomes,  .\n
    # - Stakeholder Satisfaction: Summarize feedback on stakeholder satisfaction,  .\n
    # - Overall Value Added: Summarize unique value contributions,  .\n
    # \n
    # Summary Statement:\n
    # Provide a concise overall summary of contributions, key strengths, and areas for growth.\n
    # \n
    # Text to Format:\n
    # {feedbacks_text}

    # """


    try:
        summary = cust_summarize_feedback(feedbacks, prompt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"summaries": [summary]})


# Function for batch summarization
# def upload_feedback():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     use_custom_prompt = request.form.get('use_custom_prompt', type=int)

#     if use_custom_prompt == 2:
#         custom_prompts = load_custom_prompts()
#         if not custom_prompts:
#             return jsonify({"error": "No custom prompt available. Please provide one or use the prebuilt prompt."}), 400
#         current_prompt = custom_prompts[-1].strip()
#     elif use_custom_prompt == 1:
#         current_prompt = "Summarize the following feedback comprehensively, focusing on key achievements, contributions, strengths, weakness, area of improvement and skills. Retain essential keywords and themes, and refer to feedback sources by including their feedback numbers in parentheses (e.g., '(1)', '(3)') as appropriate to highlight relevant examples, without requiring a sequential order:\n\n"
#     else:
#         return jsonify({"error": "Invalid parameter for prompt selection."}), 400
    
#     print(use_custom_prompt,current_prompt)

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)

#         df = pd.read_csv(file_path)
#         summaries = []
#         grouped = df.groupby('subject')

#         for employee, group in grouped:
#             level = group['level'].iloc[0]
#             job_title = group['job_title'].iloc[0]
#             function_code = group['function_code'].iloc[0]
#             manager = group['manager'].iloc[0]
#             emp_id = int(group['emp_id'].iloc[0])  # Convert to standard int

#             for idx, question in enumerate(['question1', 'question2', 'question3', 'question4']):
#                 feedbacks = group[question].dropna().tolist()
                
#                 start_time = datetime.now()
#                 summary = exp_summarize_feedback(feedbacks, current_prompt)  
#                 final_summary = ' '.join(summary)
#                 end_time = datetime.now()
                
#                 duration = (end_time - start_time).total_seconds() 
#                 str_timestamp = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
#                 end_timestamp = end_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

#                 if idx == 0:
#                     summaries.append({
#                         "subject": employee,
#                         "level": level,
#                         "job_title": job_title,
#                         "function_code": function_code,
#                         "manager": manager,
#                         "emp_id": emp_id,  # Already converted
#                         "question": question,
#                         "summary": final_summary,
#                         "start_timestamp": str_timestamp,
#                         "end_timestamp": end_timestamp,
#                         "duration": duration
#                     })
#                 else:
#                     summaries.append({
#                         "subject": "", 
#                         "level": "",   
#                         "job_title": "",
#                         "function_code": "",
#                         "manager": "", 
#                         "emp_id": None,  # Set to None for JSON serialization
#                         "question": question,
#                         "summary": final_summary,
#                         "start_timestamp": str_timestamp,
#                         "end_timestamp": end_timestamp,
#                         "duration": duration
#                     })

#         output_filename = 'summarized_feedback.csv'
#         output_path = os.path.join(current_app.config['UPLOAD_FOLDER'], output_filename)

#         output_df = pd.DataFrame(summaries)
#         output_df.to_csv(output_path, index=False)

#         return jsonify({"message": "Summarization complete", "summaries": summaries}), 200

#     return jsonify({"error": "Invalid file type"}), 400


def upload_feedback():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    use_custom_prompt = request.form.get('use_custom_prompt', type=int)
    custom_prompts = load_custom_prompts() if use_custom_prompt == 2 else []
    
    if use_custom_prompt == 2 and not custom_prompts:
        return jsonify({"error": "No custom prompt available. Please provide one or use the prebuilt prompt."}), 400
    current_prompt = custom_prompts[-1].strip() if use_custom_prompt == 2 else (
        "Summarize the following feedback comprehensively in a paragraph, focusing on key achievements, contributions, strengths, weaknesses, areas of improvement, and skills. "
        "Retain essential keywords and themes, and refer to feedback sources by including their feedback numbers in parentheses (e.g., '(1)', '(3)').\n\n"
    )

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
            emp_id = int(group['emp_id'].iloc[0])  

            # Step 1: Get and group expectations by attribute
            chroma_expectations = get_query_expectations(job_title)
            attribute_expectations = {}
            for expectation in chroma_expectations:
                if isinstance(expectation, str) and ", " in expectation:
                    parts = expectation.split(", ")
                    attribute = parts[1].split(": ")[1]  
                    expectation_text = parts[3].split(": ")[1]  

                    if attribute not in attribute_expectations:
                        attribute_expectations[attribute] = []
                    attribute_expectations[attribute].append(expectation_text)

            # Step 2: Create a combined prompt for all attributes
            expectations_prompt = "\n".join(
                f"{attr}:\n" + "\n".join(expectations)
                for attr, expectations in attribute_expectations.items()
            )

            for idx, question in enumerate(['question1', 'question2', 'question3', 'question4']):
                feedbacks = group[question].dropna().tolist()
                
                start_time = datetime.now()
                feedback_summary = exp_summarize_feedback(feedbacks, current_prompt)  
                feedback_summary_text = ' '.join(feedback_summary)
                
                # Create a comprehensive prompt with all attributes and their expectations
                combined_prompt = (
                    f"Summarize feedback for each attribute listed below as they apply to the role '{job_title}'. "
                    "For each attribute, provide a structured response in 2-3 sentences that captures key skills, strengths, achievements, "
                    "and areas for growth relevant to the attribute’s expectations. Focus on concise, varied phrasing and avoid repetitive language. "
                    "Organize each attribute summary clearly under its attribute name and ensure a unique summary style for each.\n\n"
                    "Attributes and Expectations:\n\n"
                    + "\n".join([f"{attribute}:\n- " + "\n- ".join(expectations) for attribute, expectations in attribute_expectations.items()])
                    + "\n\nFeedback:\n"
                    + "\n".join(feedbacks)
                )


                # Generate expectation summary using the combined prompt
                try:
                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": combined_prompt}
                        ],
                        temperature=0.7,
                        max_tokens=1500,
                        top_p=0.9,
                        frequency_penalty=0.5
                    )
                    expectations_summary = res.choices[0].message.content.strip()
                except Exception as e:
                    print(f"Error generating expectations summary: {e}")
                    expectations_summary = "Error in summarization."

                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                str_timestamp = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                end_timestamp = end_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

                # Store feedback and expectation summaries for each question
                if idx == 0:
                    summaries.append({
                        "subject": employee,
                        "level": level,
                        "job_title": job_title,
                        "function_code": function_code,
                        "manager": manager,
                        "emp_id": emp_id,  
                        "question": question,
                        "feedback_summary": feedback_summary_text,
                        "expectation_summary": expectations_summary,
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
                        "emp_id": None, 
                        "question": question,
                        "feedback_summary": feedback_summary_text,
                        "expectation_summary": expectations_summary,
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


# Function to download the batch summarized feedback csv file
def download_feedback():
    output_filename = 'summarized_feedback.csv'
    output_path = os.path.join(current_app.config['UPLOAD_FOLDER'], output_filename)

    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    
    return jsonify({"error": "File not found"}), 404


# Function to generate custom summary based on user prompt 
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


# Function  to get the employees summarized feedback data for managerial view
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
                'summary': row['feedback_summary'],
                'expec_summary': row['expectation_summary'],
                'start_time': row['start_timestamp'] if pd.notna(row['start_timestamp']) else None,
                'end_time': row['end_timestamp'] if pd.notna(row['end_timestamp']) else None,
                'duration': row['duration'] if pd.notna(row['duration']) else None
            }

    # Convert the employee dictionary to a list of values (to get the desired JSON structure)
    return jsonify(list(employees.values()))


# Function to get original feedbacks data of employees
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


# Function to generate summary against expectaion (Includes RAG [ChromaDB])
# Function to generate a summary and rate feedback based on expectations
def generate_summary_and_rating_for_attribute(feedback_list, expectations_list, attribute=None, role=None):
    try:
        # Combine the expectations and feedback into the summarization prompt
        # prompt = f"Provide a concise summary of the following feedback considering the expectations for the {attribute} attribute for the role {role}. Expectations:\n" + "\n".join(expectations_list) + "\n\nFeedback:\n" + "\n".join(feedback_list)

        # prompt = (
        #     f"Summarize the following feedback concisely, focusing on essential points related to the '{attribute}' attribute for the role '{role}'. "
        #     "Highlight expectations briefly, then capture only the main themes from the feedback in 2-3 sentences:\n\n"
        #     "Expectations:\n" + "; ".join(expectations_list) + "\n\n"
        #     "Feedback:\n" + "\n".join(feedback_list)
        # )

        prompt = (
            f"Summarize the feedback below for '{attribute}' in the role '{role}' using varied language and avoiding repeated phrases. "
            "Provide a brief, cohesive overview highlighting key skills, achievements, and areas for growth. Avoid redundancy and focus on unique aspects for a concise summary of 60 words only:\n\n"
            "Expectations:\n" + "; ".join(expectations_list) + "\n\n"
            "Feedback:\n" + "\n".join(feedback_list)
        )


        
        # Log the prompt for debugging purposes
        # print(f"Summarization prompt: {prompt}")
        
        # Example of the call to the GPT or other model (assumed to be OpenAI's GPT here)
        res = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150,
            top_p=0.9,
            frequency_penalty=0.5
        )
        
        # Extract the summary and return it
        summary = res.choices[0].message.content.strip()

        # Generate a rating based on the summary (can be more sophisticated later)
        rating = generate_rating_from_summary(summary)
        
        # Return the summary and rating
        return summary, rating
    
    except Exception as e:
        # Log the exact error for debugging purposes
        print(f"Error during summarization: {str(e)}")
        
        # Return a default error message to ensure the API does not crash
        return "Error in summarization", 0  # Default to rating 0 on error


# Rating generation logic (can be enhanced with NLP sentiment analysis later)
def generate_rating_from_summary(summary):
    # Mock logic: You can improve this with actual sentiment analysis or more advanced logic
    if "excellent" in summary.lower() or "outstanding" in summary.lower():
        return 5
    elif "good" in summary.lower():
        return 4
    elif "average" in summary.lower():
        return 3
    else:
        return 2


# Main function to handle summarization and rating generation
def expectations_summarize():
    data = request.json
    feedbacks = data.get('feedbacks', [])
    role = data.get('role')
    # print("REQUEST DATA...\n", data)

    if not feedbacks:
        return jsonify({"error": "No feedback provided"}), 400
    
    # Step 1: Query expectations for the role (e.g., Vice President) from ChromaDB
    chroma_expectations = get_query_expectations(role)
    # print("CHROMA EXPECTATIONS DATA...\n", chroma_expectations)
    
    # Step 2: Group expectations by attributes
    attribute_expectations = {}
    for index, expectation in enumerate(chroma_expectations):
        # Ensure the data is in the expected format
        if isinstance(expectation, str) and ", " in expectation:
            # Extracting the attribute and expectation
            parts = expectation.split(", ")
            attribute = parts[1].split(": ")[1]  # Get the attribute
            expectation_text = parts[3].split(": ")[1]  # Get the expectation

            if attribute not in attribute_expectations:
                attribute_expectations[attribute] = []
            attribute_expectations[attribute].append(expectation_text)
        else:
            print(f"Unexpected format for expectation: {expectation}")

    # print("ATTRIBUTE EXPECTATIONS DATA...\n", attribute_expectations)

    summaries = {}
    ratings = {}
    
    # Step 3: Summarize feedback for each attribute by passing both feedback and expectations
    for attribute, expectations_list in attribute_expectations.items():
        # Pass all feedback along with each attribute's expectations into the summarization
        summary, rating = generate_summary_and_rating_for_attribute(feedbacks, expectations_list, attribute, role)
        summaries[attribute] = summary
        ratings[attribute] = rating

    # Return only the summaries and ratings by attributes (no general category)
    return jsonify({"summaries": summaries, "ratings": ratings})
