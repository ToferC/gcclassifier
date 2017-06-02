from docx import Document
import os

# script for parsing and returning docx text

def process_document(file):

    url = "/home/chris/GitHub/gcclassifier/gc_classifier/"+file

    document = Document(url)

    text = ""

    for paragraph in document.paragraphs:
        text += f"{paragraph.text}\n\n"

    return text