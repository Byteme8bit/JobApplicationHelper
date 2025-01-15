import argparse
import os
from datetime import date
import json
from run_gui import run_gui
from utils import generate_document, load_config, extract_placeholders, open_config, build_config_from_template


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate documents from templates.", prog="Document Generator",
                                     usage="%(prog)s [options]")
    parser.add_argument("--config", help="Path to the config file")
    parser.add_argument("-GUI", action="store_true", help="Load the GUI")
    parser.add_argument("-BUILD", help="Build config file from template."
                                       "Enter a path to a template file. (.docx, .doc, or .txt)", nargs='?')
    args = parser.parse_args()

    if args.GUI:
        run_gui()
        exit(0)  # Exit after GUI is launched

    if args.BUILD:
        template_path = args.BUILD
        if not template_path:
            template_path = input("Enter path to template file: ")
        while not os.path.exists(template_path):
            template_path = input("File not found. Enter valid path to template file: ")
        bookends = input("Enter up to 2 placeholder bookends (e.g., %% for %%placeholder%%) [Default is %]: ") or "%"
        config_filepath = build_config_from_template(template_path, bookends)
        if config_filepath:
            print(f"Config file '{config_filepath}' created successfully.")
            config = load_config(config_filepath)
            if config:
                print("Placeholders:")
                for key, value in config["placeholders"].items():
                    print(f"- {key}: {value}")
            else:
                print("Error loading newly created config file.")
        else:
            print("Error creating config file.")
        exit(0) #Exit after config creation

    config_path = args.config
    if config_path is None:
        config_path = input("Enter path to config file: ")
        while not os.path.exists(config_path):
            config_path = input("File not found. Enter valid path to config file: ")

    try:
        config = load_config(config_path)
        bookends = config.get("bookends", "%") #Handle missing bookends gracefully
    except FileNotFoundError:
        print(f"Error: Config file not found at {config_path}")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in config file {config_path}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while loading config: {e}")
        exit(1)


    proceed = False
    while not proceed:
        print(f"Config file: {config_path}")
        print("Placeholders:")
        for key, value in config["placeholders"].items():
            print(f"- {key}: {value}")
        openConfig = input(f"Open {config_path} with external program? (y/n): ")
        if openConfig.lower() == 'y':
            program = input(f"Open '{config_path}' with which program? (e.g., notepad, notepad++, word): ")
            try:
                config = open_config(config_path, program)
            except FileNotFoundError:
                print(f"Error: Program '{program}' not found.")
                exit(1)
            except Exception as e:
                print(f"An error occurred while running external program: {e}")
                exit(1)

        proceed = input("OK to proceed to generate document? (y / n): ").lower()
        if proceed == 'y':
            break
        elif proceed == 'n':
            continue
        else:
            print("Please enter a valid option y or n\n")

    try:
        generate_document(config, bookend=bookends)
        print("Document generated successfully!")
    except Exception as e:
        print(f"An error occurred during document generation: {e}")
        exit(1)

