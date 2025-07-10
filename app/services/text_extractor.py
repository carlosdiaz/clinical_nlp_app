import io
import os
from pdfminer.high_level import extract_text as extract_pdf_text


def extract_text(file):
    """
    Extract text from a file (PDF or TXT).
    :param file:
    :return:
    """
    filename = file.filename.lower()

    if filename.endswith('.pdf'):
        print('We have a pdf file')
        return extract_pdf_text(file)
    elif filename.endswith('.txt'):
        try:
            file.seek(0)
            binary_data = file.read()
            decoded_text = binary_data.decode('utf-8')
            return decoded_text
        except FileNotFoundError:
            print("Error: The file was not found.")
        except UnicodeDecodeError:
            print("Error: Could not decode the file using UTF-8. The file might be in a different encoding.")
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or TXT file.")
