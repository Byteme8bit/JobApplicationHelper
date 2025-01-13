import json
import os
import re
from docx import Document


def generate_document(template_path, output_path, placeholders):
    """Generates a document from a template and placeholders."""
    try:
        if os.path.exists(output_path):
            if not config.get("overwriteOutput", False):
                overwrite = input(f"Output file '{output_path}' already exists. Overwrite? (y/n): ").lower()
                if overwrite != 'y':
                    raise FileExistsError(f"Output file '{output_path}' already exists and overwrite is not allowed.")

        if template_path.endswith((".docx", ".doc")):
            doc = Document(template_path)
            for paragraph in doc.paragraphs:
                for placeholder, value in placeholders.items():
                    paragraph.text = paragraph.text.replace(f"%%{placeholder}%%", value)
            doc.save(output_path)
        elif template_path.endswith(".txt"):
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            for placeholder, value in placeholders.items():
                template_content = template_content.replace(f"%%{placeholder}%%", value)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(template_content)
        else:
            raise ValueError("Unsupported file type. Please use .docx, .doc, or .txt.")

    except FileNotFoundError:
        raise FileNotFoundError(f"Template file not found: {template_path}")
    except FileExistsError as e:
        raise e
    except Exception as e:
        raise IOError(f"An error occurred while generating the document: {e}")


def load_config(config_path):
    """Loads a JSON configuration file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {config_path}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Invalid JSON format in config file: {config_path}", None, None)
    except Exception as e:
        raise IOError(f"An error occurred while loading the config file: {e}")


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
