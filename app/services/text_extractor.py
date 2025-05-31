import io
from pdfminer.high_level import extract_text as extract_pdf_text


def extract_text(file):
    """
    Extract text from a file (PDF or TXT).
    """
    print('extract_text')
    filename = file.filename.lower()
    if filename.endswith('.pdf'):
        return extract_pdf_text(file)
    elif filename.endswith('.txt'):
        return file.read().decode('utf-8')
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or TXT file.")
