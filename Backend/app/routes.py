from flask import request, jsonify, send_file
from .services import (
    upload_file,
    summarize_feedback,
    upload_feedback,
    download_feedback,
    custom_summarize
)

def register_routes(app):
    app.add_url_rule('/upload', 'upload_file', upload_file, methods=['POST'])
    app.add_url_rule('/summarize', 'summarize_feedback', summarize_feedback, methods=['POST'])
    app.add_url_rule('/upload_feedback', 'upload_feedback', upload_feedback, methods=['POST'])
    app.add_url_rule('/download_feedback', 'download_feedback', download_feedback, methods=['GET'])
    app.add_url_rule('/custom_summarize', 'custom_summarize', custom_summarize, methods=['POST'])
