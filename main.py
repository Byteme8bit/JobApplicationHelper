import argparse
import os
from datetime import date
import json
from run_gui import run_gui
from utils import generate_document, load_config, extract_placeholders, handle_external_program


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate documents from templates.", prog="Document Generator",
                                     usage="%(prog)s [options]")
    parser.add_argument("--config", help="Path to the config file")
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
            config = load_config(config_filepath)
        except (FileNotFoundError, ValueError, IOError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    elif args.config:  # If config is not passed as an argument, prompt for it
        print(f"Config provided. File: {config_path}")
        config = load_config(config_path)
        try:
            bookends = config["bookends"]
        except KeyError or TypeError or ValueError:
            bookends = None
        placeholders = config["placeholders"]
    else:
        print("No arguments provided. Use -h for help.")
        exit(1)
    proceed = False
    openConfig = input(f"Open {config_path if config_path else config_filepath} with external program? (y/n): ")
    if openConfig == 'y':
        program = input(f"Open '{config_path if config_path else config_filepath}' "
                        f"with which program? (e.g., notepad, notepad++, word): ")
        config = handle_external_program(config_path if config_path else config_filepath, program)

    else:
        config = load_config(config_path if config_path else config_filepath)

    placeholders = config["placeholders"]

    while not proceed:
        print(f"Config file: {config_path if config_path else config_filepath}")
        print("Placeholders:")
        for key, value in placeholders.items():
            print(f"- {key}: {value}")
        while bookends is None:
            bookends = input("Enter up to 2 placeholder bookends (e.g., %% for %%placeholder%%) [Default is %]: ")
        while config is None:
            config = load_config(config_path if config_path else config_filepath)
        proceed = input("OK to proceed to generate document? (y / n): ").lower()
        if proceed == 'y':
            break
        elif proceed == 'n':
            openConfig = input(f"Open {config_path if config_path else config_filepath} with external program? (y/n): ")
            if openConfig == 'y':
                program = input(f"Open '{config_path if config_path else config_filepath}' "
                                f"with which program? (e.g., notepad, notepad++, word): ")
                config = handle_external_program(config_path if config_path else config_filepath, program)
            else:
                config = load_config(config_path if config_path else config_filepath)
            placeholders = config["placeholders"]
            continue
        else:
            print("Please enter a valid option y or n\n")
    #config = load_config(config_path if config_path else config_filepath)
    generate_document(config, bookend=bookends)
    print("Document generated successfully!")
