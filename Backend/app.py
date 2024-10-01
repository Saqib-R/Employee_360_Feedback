from flask import Flask, request, jsonify
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads'

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

if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask, request, jsonify
# import pandas as pd
# import os
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)


# app.config['UPLOAD_FOLDER'] = 'uploads'

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'})
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'})
#     if file:
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(filepath)
#         data = pd.read_csv(filepath)
#         print(data.to_dict())
#         return jsonify(data.to_dict())

# if __name__ == '__main__':
#     app.run(debug=True)
