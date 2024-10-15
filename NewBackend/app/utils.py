import os
from flask import current_app


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
