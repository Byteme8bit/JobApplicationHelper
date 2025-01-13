import json
import os
import re
from docx import Document

# ... (Existing functions remain unchanged) ...

def extract_placeholders(template_path, bookends):
    """Extracts placeholders from a template file using specified bookends."""
    placeholders = {}
    try:
        if template_path.endswith((".docx", ".doc")):
            doc = Document(template_path)
            for paragraph in doc.paragraphs:
                matches = re.findall(rf"{re.escape(bookends)}(.*?){re.escape(bookends)}", paragraph.text)
                for match in matches:
                    placeholder_name = match.strip()
                    if placeholder_name:
                        placeholders[placeholder_name] = ""
        elif template_path.endswith(".txt"):
            with open(template_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
                matches = re.findall(rf"{re.escape(bookends)}(.*?){re.escape(bookends)}", file_content, re.DOTALL)
                for match in matches:
                    placeholder_name = match.strip()
                    if placeholder_name:
                        placeholders[placeholder_name] = ""
        else:
            raise ValueError("Unsupported file type. Please use .docx, .doc, or .txt.")
        return placeholders
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file not found: {template_path}")
    except Exception as e:
        raise IOError(f"An error occurred while extracting placeholders: {e}")

