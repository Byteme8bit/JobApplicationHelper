import argparse
import os
from datetime import date
import json
from run_gui import run_gui
from utils import generate_document, load_config, extract_placeholders, handle_external_program


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate documents from templates.", prog="Document Generator",
                                     usage="%(prog)s [options]")
    parser.add_argument("--config", help="Path to the config file", nargs='?')
    parser.add_argument("-GUI", action="store_true", help="Load the GUI")
    parser.add_argument("-BUILD", help="Build config file from template."
                                       "Enter a path to a template file. (.docx, .doc, or .txt)", nargs='?')
    args = parser.parse_args()
    config_path = args.config if not None else input("Enter path to config file: ")

    if args.GUI:
        run_gui()

    elif args.BUILD:
        template_path = args.BUILD if args.BUILD else input("Enter path to template file: ")
        while not os.path.exists(template_path):
            template_path = input("File not found. Enter valid path to template file: ")
        bookends = input("Enter up to 2 placeholder bookends (e.g., %% for %%placeholder%%) [Default is %]: ")
        try:
            filename_parts = os.path.basename(template_path).split('-')
            config_filename = '-'.join(filename_parts[:2]) + "-config.json"
            config_filepath = os.path.join(os.path.dirname(template_path), config_filename)
            date = date.today().strftime("%Y-%m-%d")
            placeholders = extract_placeholders(template_path, bookends)
            config_data = {
                "configFileName": config_filename,
                "templateFilePath": template_path,
                "outputFilePath": config_filename.replace("-config.json", f"-Cover Letter-{date}.docx"),
                "overwriteOutput": False,
                "bookends": bookends,
                "placeholders": placeholders
            }
            placeholders["Date"] = date
            with open(config_filepath, 'w') as outfile:
                json.dump(config_data, outfile, indent=4)
            print(f"Config file '{config_filepath}' created.")
            print("Placeholders:")
            for key, value in placeholders.items():
                print(f"- {key}: {value}")
            # config = load_config(config_filepath)
        except (FileNotFoundError, ValueError, IOError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    elif args.config:  # If config is not passed as an argument, prompt for it
        print(f"Config provided. File: {config_path}")

    else:
        print("No arguments provided. Use -h for help.")
        exit(1)

    #config_path = args.config if not None else input("Enter path to config file: ")
    config = load_config(config_path)
    openConfig = input(f"Open {config_path} with external program? (y/n): ")
    if openConfig == 'y':
        program = input(f"Open '{config_path}' with which program? (e.g., notepad, notepad++, word): ")
        handle_external_program(config_path, program)
    try:
        bookends = config_path["bookends"]
    except KeyError:
        bookends = None
    if bookends is None:
        bookends = input("Enter up to 2 placeholder bookends (e.g., %% for %%placeholder%%) [Default is %]: ")
    generate_document(config, bookend=bookends)
    print("Document generated successfully!")
