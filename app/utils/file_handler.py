# app/utils/file_handler.py

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploaded_files"


def save_file(file_storage):
    """Save the uploaded file to disk and return the file path."""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filename = secure_filename(file_storage.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file_storage.save(filepath)
    return filepath
