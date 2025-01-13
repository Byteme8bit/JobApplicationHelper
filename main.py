import argparse
import os
import subprocess
from datetime import date
import json
from run_gui import run_gui
from utils import generate_document, load_config, extract_placeholders


def generate_output(config):
    """Generates the output document using the provided configuration."""
    if isinstance(config, dict):
        config = load_config(config.get("configFileName"))
    try:
        generate_document(config)
        print("Document generated successfully!")
    except (FileNotFoundError, json.JSONDecodeError, KeyError, IOError) as e:
        print(f"Error generating document: {e}")


def handle_external_program(config_filepath, program):
    """Handles the execution of an external program (e.g., notepad, notepad++, word) and subsequent config loading."""
    switch = {
        'notepad': 'notepad.exe',
        'notepad++': "notepad++.exe",
        'word': "WINWORD.EXE"
    }
    try:
        result = subprocess.run(
            [switch.get(program, program), config_filepath], check=True)  # check=True raises exception if program fails
        if result.returncode == 0:
            print(f"Program '{program}' finished successfully.")
            config = load_config(config_filepath)
            print("Config loaded successfully!")
            print("Placeholders:")
            for key, value in config["placeholders"].items():
                print(f"- {key}: {value}")
            generate_output(config)
        else:
            print(f"Program '{program}' exited with error code {result.returncode}.")
    except FileNotFoundError:
        print(f"Error: Program '{program}' not found.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing '{program}': {e}")
    except (FileNotFoundError, json.JSONDecodeError, KeyError, IOError) as e:
        print(f"Error loading or processing config file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate documents from templates.", prog="Document Generator",
                                     usage="%(prog)s [options]")
    parser.add_argument("--config", help="Path to the config file", nargs='?')
    parser.add_argument("-GUI", action="store_true", help="Load the GUI")
    parser.add_argument("-BUILD", help="Build config file from template."
                                       "Enter a path to a template file. (.docx, .doc, or .txt)", nargs='?')
    args = parser.parse_args()

    if args.GUI:
        run_gui()
    elif args.BUILD:
        template_path = args.BUILD if args.BUILD else input("Enter path to template file: ")
        while not os.path.exists(template_path):
            template_path = input("File not found. Enter valid path to template file: ")
        bookends = input("Enter up to 2 placeholder bookends (e.g., %% for %%placeholder%%): ")
        try:
            placeholders = extract_placeholders(template_path, bookends)
            filename_parts = os.path.basename(template_path).split('-')
            config_filename = '-'.join(filename_parts[:2]) + "-config.json"
            config_filepath = os.path.join(os.path.dirname(template_path), config_filename)
            date = date.today().strftime("%Y-%m-%d")
            config_data = {
                "configFileName": config_filename,
                "templateFilePath": template_path,
                "outputFilePath": config_filename.replace("-config.json", f"-Cover Letter-{date}.docx"),
                "placeholders": placeholders,
                "overwriteOutput": False
            }
            placeholders["Date"] = date
            with open(config_filepath, 'w') as outfile:
                json.dump(config_data, outfile, indent=4)

            program = input(f"Config file '{config_filepath}' created. Open it with which program? (e.g., notepad, notepad++, word): ")
            handle_external_program(config_filepath, program)

        except (FileNotFoundError, ValueError, IOError) as e:
            print(f"Error: {e}")
    elif args.config is None:  # If config is not passed as an argument, prompt for it
        config_path = input("Enter path to config file: ")
        while not os.path.exists(config_path):
            config_path = input("File not found. Enter valid path to config file: ")
        try:
            generate_output(config_path)
        except (FileNotFoundError, json.JSONDecodeError, KeyError, IOError) as e:
            print(f"Error: {e}")

