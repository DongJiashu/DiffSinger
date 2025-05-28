#this tool is used to check whether lab files contains unseen words from dictionary.
#if found please add the word and pronounciation in the dictionary

import os
from pathlib import Path
import argparse


def extract_and_compare_words(input_dir, lexicon_path=None):
    input_dir = Path(input_dir)
    all_words = set()

    # Collect all words from .lab files
    for lab_path in input_dir.rglob("*.lab"):
        with open(lab_path, "r", encoding="utf-8") as f:
            for line in f:
                all_words.update(line.strip().split())

    # Save all unique words
    with open("word.txt", "w", encoding="utf-8") as f:
        for word in sorted(all_words):
            f.write(word + "\n")

    # Check lexicon and find missing words
    if lexicon_path:
        lexicon_path = Path(lexicon_path)
        if not lexicon_path.exists():
            print(f"⚠️ Lexicon file not found: {lexicon_path}")
            return

        with open(lexicon_path, "r", encoding="utf-8") as f:
            lexicon_words = {line.split("\t")[0] for line in f if "\t" in line}

        missing_words = sorted(word for word in all_words if word not in lexicon_words)

        with open("word_miss.txt", "w", encoding="utf-8") as f:
            for word in missing_words:
                f.write(word + "\n")

        print(f"✅ Done. Found {len(missing_words)} missing words.")
        print("🔍 Missing words written to: word_miss.txt")

    print(f"✅ All words written to: word.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract unique words from .lab files and compare with lexicon.")
    parser.add_argument("input_dir", type=str, help="Directory containing subfolders with .lab files")
    parser.add_argument("--lexicon", type=str, default=None, help="Optional lexicon file to check against")

    args = parser.parse_args()
    extract_and_compare_words(args.input_dir, args.lexicon)