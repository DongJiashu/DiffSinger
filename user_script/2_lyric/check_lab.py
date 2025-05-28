#This tool is used to clean and check lab files for german. 

import os
import re

def clean_and_overwrite_lab_files(root_dir, lang=None):
    """
    Traverse all .lab files in a directory (including subfolders),
    clean each line by:
    - Removing leading/trailing whitespace
    - Removing punctuation (preserve German characters)
    - Collapsing multiple spaces into one
    Then overwrite the original file.
    """
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".lab"):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                cleaned_lines = []
                for line in lines:
                    line = line.strip()
                    line = re.sub(r"[^\wäöüÄÖÜß\s]", "", line).lower()  # remove punctuation and convert to lowercase
                    if lang == "de":
                        line = line.replace("ß", "ss")
                    line = re.sub(r"\s+", " ", line)  # normalize whitespace
                    cleaned_lines.append(line)

                with open(file_path, "w", encoding="utf-8") as f:
                    for cleaned in cleaned_lines:
                        f.write(cleaned + "\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Clean .lab files in a directory recursively.")
    parser.add_argument("lab_dir", type=str, help="Directory containing .lab files")
    parser.add_argument("--lang", type=str, default=None, help="Optional language code (e.g., 'de')")
    args = parser.parse_args()
    clean_and_overwrite_lab_files(args.lab_dir, lang=args.lang)