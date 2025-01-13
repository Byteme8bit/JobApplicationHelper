import argparse
import os
import subprocess
from datetime import date
import json
from run_gui import run_gui
from utils import generate_document, load_config, extract_placeholders


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate documents from templates.")
    parser.add_argument("--config", help="Path to the config file (default: config.json)")
    parser.add_argument("-GUI", action="store_true", help="Load the GUI")
    parser.add_argument("-BUILD", help="Build config file from template", nargs='?')
    args = parser.parse_args()

    if args.GUI:
        run_gui()
    elif args.BUILD:
        template_path = args.BUILD or input("Enter path to template file: ")
        bookends = input("Enter placeholder bookends (e.g., %%): ")
        try:
            placeholders = extract_placeholders(template_path, bookends)
            filename_parts = os.path.basename(template_path).split('-')
            config_filename = '-'.join(filename_parts[:2]) + "-config.json"
            config_filepath = os.path.join(os.path.dirname(template_path), config_filename)

            with open(config_filepath, 'w') as outfile:
                json.dump({"placeholders": placeholders}, outfile, indent=4)

            open_file = input(f"Config file '{config_filepath}' created. Open it? (y/n): ").lower()
            if open_file == 'y':
                program = input("Enter the program to open the file with (e.g., notepad, notepad++, word): ")
                try:
                    subprocess.run([program, config_filepath])
                except FileNotFoundError:
                    print(f"Error: Program '{program}' not found.")
                except Exception as e:
                    print(f"An error occurred while opening the file: {e}")

        except (FileNotFoundError, ValueError, IOError) as e:
            print(f"Error: {e}")
    else:
        config_path = args.config or "config.json"
        try:
            config = load_config(config_path)
            generate_document(config["templateFilePath"], config["outputFilePath"], config["placeholders"])
            print("Document generated successfully!")
        except (FileNotFoundError, json.JSONDecodeError, KeyError, IOError) as e:
            print(f"Error: {e}")

