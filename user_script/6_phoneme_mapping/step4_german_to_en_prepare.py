"""Compute phoneme similarity between German and English phonemes based on PHOIBLE features,
and output a mapping and top similarity scores.
All input files are assumed to be in the same directory as this script:
- phoneset_german.json: List of German phonemes
- phoneset_english.json: Dictionary of English phoneme -> frequency
- phoible_deu.csv: German phoneme features from PHOIBLE
- phoible_eng.csv: English phoneme features from PHOIBLE
Outputs:
- german_to_english_phoneme_mapping.json
- phoneme_similarity_scores.json (includes frequency of each English phoneme)
"""

import json
import csv
import numpy as np
from collections import defaultdict

# File paths (relative to this script's directory)
phone_set_de_path = 'phoneset_german.json'
phone_set_en_path = 'phoneset_english.json'
phoible_deu_path = 'phoible_deu.csv'
phoible_eng_path = 'phoible_eng.csv'
output_similarity_path = 'phoneme_similarity_scores.txt'
output_mapping_path = 'german_to_english_phoneme_mapping.py'

def remove_length_markers(phoneme):
    """Remove length markers (ː) from phonemes."""
    return phoneme.replace('ː', '')

# Load German phonemes
with open(phone_set_de_path, 'r', encoding='utf-8') as f:
    german_phonemes = json.load(f)

# Load German PHOIBLE features
deu_features = {}
with open(phoible_deu_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        phoneme = remove_length_markers(row['Phoneme'])
        features = []
        for key in list(row.keys())[10:47]:  # From 'tone' to 'click'
            value = row[key]
            if value == '+':
                features.append(1)
            elif value == '-':
                features.append(-1)
            else:
                features.append(0)
        deu_features[phoneme] = np.array(features)

# Load English PHOIBLE features
eng_features = {}
with open(phoible_eng_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        phoneme = remove_length_markers(row['Phoneme'])
        features = []
        for key in list(row.keys())[10:47]:  # From 'tone' to 'click'
            value = row[key]
            if value == '+':
                features.append(1)
            elif value == '-':
                features.append(-1)
            else:
                features.append(0)
        eng_features[phoneme] = np.array(features)

def calculate_similarity(features1, features2):
    """Calculate similarity as the number of matching feature values."""
    return np.sum(features1 == features2)

# Load English phonemes with frequencies
with open(phone_set_en_path, 'r', encoding='utf-8') as f:
    english_phonemes_data = json.load(f)

# Convert to dict if necessary
if isinstance(english_phonemes_data, dict):
    english_phoneme_freq = {remove_length_markers(k): v for k, v in english_phonemes_data.items()}
else:
    english_phoneme_freq = {remove_length_markers(p): 0 for p in english_phonemes_data}

english_phoneme_set = set(english_phoneme_freq.keys())

# Compute similarities and build mapping
similarity_results = defaultdict(list)
final_mapping = {}

for de_phoneme in german_phonemes:
    de_phoneme_clean = remove_length_markers(de_phoneme)

    if de_phoneme_clean not in deu_features:
        base_phoneme = ''.join(c for c in de_phoneme_clean if not (0x300 <= ord(c) <= 0x36F))
        if base_phoneme in deu_features:
            de_phoneme_clean = base_phoneme
        else:
            final_mapping[de_phoneme] = 'NOT_FOUND'
            continue

    de_features = deu_features[de_phoneme_clean]

    similarities = []
    for en_phoneme, en_features in eng_features.items():
        similarity = calculate_similarity(de_features, en_features)
        freq = english_phoneme_freq.get(en_phoneme, 0)
        similarities.append((en_phoneme, int(similarity), freq))

    similarities.sort(key=lambda x: x[1], reverse=True)
    similarity_results[de_phoneme] = similarities[:10]

    best_match = None
    for candidate, score, freq in similarities:
        if candidate in english_phoneme_set:
            best_match = candidate
            break

    final_mapping[de_phoneme] = best_match if best_match else 'NOT_FOUND'

# Save similarity results
output_similarity_txt_path = output_similarity_path.replace('.json', '.txt')

with open(output_similarity_txt_path, 'w', encoding='utf-8') as f:
    for de_phoneme, matches in similarity_results.items():
        match_str = ', '.join(
            f"{en}(sim={score}, freq={freq})" for en, score, freq in matches
        )
        f.write(f"{de_phoneme} → {match_str}\n")

# Save final mapping
with open(output_mapping_path, 'w', encoding='utf-8') as f:
    f.write("# German to English phoneme mapping\n")
    f.write("# You can check frequency from phoneme_similarity_scores.txt and adjust base on your need.\n")
    f.write("phoneme_mapping = {\n")
    for de_phoneme, en_phoneme in final_mapping.items():
        f.write(f"    '{de_phoneme}': '{en_phoneme}',\n")
    f.write("}\n")

print("Processing complete. Results saved to:")
print(f"- Phoneme similarity scores: {output_similarity_path}")
print(f"- German to English phoneme mapping: {output_mapping_path}")