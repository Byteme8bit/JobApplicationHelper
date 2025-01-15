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

    if args.GUI:
        run_gui()
        exit(0) #Exit after GUI is launched

    config_path = args.config
    if config_path is None:
        config_path = input("Enter path to config file: ")
        while not os.path.exists(config_path):
            config_path = input("File not found. Enter valid path to config file: ")


    if args.BUILD:
        template_path = args.BUILD if args.BUILD else input("Enter path to template file: ")
        while not os.path.exists(template_path):
            template_path = input("File not found. Enter valid path to template file: ")
        bookends = input("Enter up to 2 placeholder bookends (e.g., %% for %%placeholder%%) [Default is %]: ") or "%"
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
            exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            exit(1)

    else:
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
                config = handle_external_program(config_path, program)
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

