import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson.objectid import ObjectId

from app.services.text_extractor import extract_text
from app.services.summarizer import summarize_text
# from app.services.diagnosis_predictor import predict_diseases
from app.services.diagnosis_predictor import predict_diagnosis
import uuid

api = Blueprint('api', __name__)

client = MongoClient(os.getenv("MONGODB_URI", "mongodb://mongo:27017/"))
db = client["clinical_notes"]
collection = db["documents"]

UPLOAD_FOLDER = 'uploaded_notes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@api.route("/upload", methods=["POST", "OPTIONS"])
def upload_file():
    if request.method == "OPTIONS":
        return '', 200

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(filepath)

    # Example response - you would trigger NLP analysis here
    try:
        text = extract_text(file)
        print(f'text extracted {text}')
        summary = summarize_text(text)
        print(f'summary {summary}')
        diseases = predict_diagnosis(text)
        print(f'The diseases are {diseases}')

        document = {
            'filename': filename,
            'text': text,
            'summary': summary,
            'diseases': diseases
        }

        result = collection.insert_one(document)

        return jsonify({'message': 'File processed and saved'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/document/<doc_id>', methods=['GET'])
def get_document(doc_id):
    try:
        document = collection.find_one({'_id': ObjectId(doc_id)})
        if not document:
            return jsonify({'error': 'Document not found'}), 404

        document['_id'] = str(document['_id'])
        return jsonify(document)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"}), 200
