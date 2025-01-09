from docx import Document
import os


def generate_document(template_path, output_path, data):
    """Generates a document, replacing placeholders and resizing text to fit.

    Supports .docx and .txt files.

    Args:
        template_path: Path to the template file.
        output_path: Path to save the generated document.
         Dictionary containing placeholder names and their replacements.
    """

    try:
        if template_path.endswith(".docx"):
            doc = Document(template_path)
            for paragraph in doc.paragraphs:
                for key, value in data.items():
                    paragraph.text = paragraph.text.replace(f"%{key}%", value)
            doc.save(output_path)

        elif template_path.endswith(".txt"):
            with open(template_path, "r") as infile, open(output_path, "w") as outfile:
                for line in infile:
                    for key, value in data.items():
                        line = line.replace(f"%{key}%", value)
                    outfile.write(line)
            raise ValueError("Unsupported file type. Only .docx and .txt are supported.")

    except FileNotFoundError:
        raise FileNotFoundError(f"Template file not found: {template_path}")
    except Exception as e:
        raise IOError(f"Error processing template: {e}")

    # Check for unmatched placeholders
    if template_path.endswith(".docx"):
        unmatched = [key for paragraph in doc.paragraphs for key in data if f"%{key}%" in paragraph.text]
    elif template_path.endswith(".txt"):
        with open(output_path, "r") as outfile:
            unmatched = [key for line in outfile for key in data if f"%{key}%" in line]
    if unmatched:
        raise ValueError(f"Unmatched placeholders found: {', '.join(unmatched)}")


if __name__ == "__main__":
    while True:
        template_path = input("Enter template file path: ")
        if not os.path.exists(template_path):
            print("Error: Template file not found. Please enter a valid path.")
            continue  # Ask for input again
        break

    while True:
        output_filename = input("Enter output file name: ")
        if os.path.exists(output_filename):
            overwrite = input(f"File '{output_filename}' already exists. Overwrite? (y/n): ")
            if overwrite.lower() == 'y':
                break
            else:
                continue  # Ask for input again
        break

    data = {}
    while True:
        key = input("Enter placeholder name (or type 'done'): ")
        if key == "done":
            break
        value = input(f"Enter value for {key}: ")
        data[key] = value

    generate_document(template_path, output_filename, data)
