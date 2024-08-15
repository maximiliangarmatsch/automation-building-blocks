import os
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams


def extract_pdf_text():
    folder_path = "./data"
    files = os.listdir(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
    text = extract_text(file_path, laparams=LAParams())
    return text
