from flask import request, jsonify, send_file
from .services import (
    upload_file,
    expectations_summarize,
    upload_feedback,
    download_feedback,
    custom_summarize,
    get_summarized_feedback,
    get_feedback_data,
    vanilla_summarize_feedback
)

def register_routes(app):
    app.add_url_rule('/upload', 'upload_file', upload_file, methods=['POST'])
    app.add_url_rule('/get_summarized_feedback', 'get_summarized_feedback', get_summarized_feedback, methods=['GET'])
    app.add_url_rule('/get_feedback_data', 'get_feedback_data', get_feedback_data, methods=['GET'])
    app.add_url_rule('/vanilla_summarize_feedback', 'vanilla_summarize_feedback', vanilla_summarize_feedback, methods=['POST'])
    app.add_url_rule('/expectations_summarize', 'expectations_summarize', expectations_summarize, methods=['POST'])
    app.add_url_rule('/upload_feedback', 'upload_feedback', upload_feedback, methods=['POST'])
    app.add_url_rule('/download_feedback', 'download_feedback', download_feedback, methods=['GET'])
    app.add_url_rule('/custom_summarize', 'custom_summarize', custom_summarize, methods=['POST'])
