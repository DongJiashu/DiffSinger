# this tool is used to seperate lyric.lab from txt by each line. 

import os
import argparse

def generate_lab_files(txt_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    for fname in os.listdir(txt_dir):
        if not fname.endswith(".txt"):
            continue

        file_path = os.path.join(txt_dir, fname)
        base_name = os.path.splitext(fname)[0]

        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        for idx, line in enumerate(lines):
            lab_name = f"{base_name}_{idx}.lab"
            lab_path = os.path.join(out_dir, lab_name)
            with open(lab_path, "w", encoding="utf-8") as lab_file:
                lab_file.write(line.lower() + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate .lab files from lyrics.txt files.")
    parser.add_argument("--txt_dir", required=True, help="Directory containing input lyrics .txt files")
    parser.add_argument("--out_dir", required=True, help="Directory to save output .lab files")
    args = parser.parse_args()

    generate_lab_files(args.txt_dir, args.out_dir)