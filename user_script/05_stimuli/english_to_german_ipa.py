#this tool is used to conver english ipa to german ipa
import os
import json
import argparse

# First-stage German to Phoible replacements
german_to_phoible = {
    'aj': 'aɪ', 'aw': 'aʊ', 'ɔʏ': 'ɔɪ', 'cʰ': 'kʰ', 'ɟ': 'ɡ',
    'ɲ': 'ŋ', 'm̩': 'm', 'n̩': 'n', 'aː': 'a'
}

# Reverse of german_to_phoible
reverse_phoible_to_german = {v: k for k, v in german_to_phoible.items()}

# Second-stage mapping to English-like phonemes
phoneme_mapping = {
    'a': 'ɑ', 'aɪ': 'aɪ', 'aʊ': 'aʊ', 'b': 'b', 'd': 'd',
    'eː': 'ə', 'f': 'f', 'h': 'h', 'iː': 'i', 'j': 'j',
    'k': 'k', 'kʰ': 'k', 'l': 'l', 'm': 'm', 'n': 'n',
    'oː': 'ɔ', 'p': 'p', 'pf': 'f', 'pʰ': 'p', 's': 's',
    't': 't', 'ts': 's', 'tʰ': 't', 'uː': 'u', 'v': 'v',
    'x': 'h', 'yː': 'u', 'z': 'z', 'ç': 'ʃ', 'øː': 'ɔ',
    'ŋ': 'ŋ', 'œ': 'ɔ', 'ɐ': 'ə', 'ɔ': 'ɔ', 'ɔɪ': 'ɔɪ',
    'ə': 'ə', 'ɛ': 'ɛ', 'ɡ': 'ɡ', 'ɪ': 'ɪ', 'ʁ': 'h',
    'ʃ': 'ʃ', 'ʊ': 'ʊ', 'ʏ': 'ʊ'
}

# Reverse of phoneme_mapping
reverse_phoneme_mapping = {v: k for k, v in phoneme_mapping.items()}

def map_phoneme(ph):
    if ph in ('SP', 'AP'):  # skip silence/appendix tokens
        return ph
    ph = german_to_phoible.get(ph, ph)
    return phoneme_mapping.get(ph, ph)  # fallback to itself if not mapped

# Reverse mapping function
def reverse_map_phoneme(ph):
    if ph in ('SP', 'AP'):
        return ph
    # First, reverse phoneme_mapping
    orig_ph = reverse_phoneme_mapping.get(ph, ph)
    # Then, reverse german_to_phoible
    orig_ph = reverse_phoible_to_german.get(orig_ph, orig_ph)
    return orig_ph

def process_file(in_path, out_path):
    with open(in_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, list):
        items = data
    else:
        items = [data]

    for item in items:
        original_seq = item.get("ph_seq", "")
        tokens = original_seq.split()
        mapped = [map_phoneme(p) for p in tokens]
        item["ph_seq"] = ' '.join(mapped)
        item["text"] = item["ph_seq"]  # optional: update "text" as well

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(items if isinstance(data, list) else items[0], f, ensure_ascii=False, indent=2)

# Reverse process: map English-like phonemes back to German
def reverse_process_file(in_path, out_path):
    with open(in_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, list):
        items = data
    else:
        items = [data]

    for item in items:
        mapped_seq = item.get("ph_seq", "")
        tokens = mapped_seq.split()
        reversed_tokens = [reverse_map_phoneme(p) for p in tokens]
        item["ph_seq"] = ' '.join(reversed_tokens)
        item["text"] = item["ph_seq"]

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(items if isinstance(data, list) else items[0], f, ensure_ascii=False, indent=2)

def main(in_dir, out_dir, reverse=False):
    os.makedirs(out_dir, exist_ok=True)
    process_fn = reverse_process_file if reverse else process_file
    if os.path.isfile(in_dir):
        if in_dir.endswith(".ds"):
            out_path = os.path.join(out_dir, os.path.basename(in_dir))
            process_fn(in_dir, out_path)
            print(f"{'Reversed' if reverse else 'Converted'}: {os.path.basename(in_dir)}")
    else:
        for fname in os.listdir(in_dir):
            if fname.endswith(".ds"):
                in_path = os.path.join(in_dir, fname)
                out_path = os.path.join(out_dir, fname)
                process_fn(in_path, out_path)
                print(f"{'Reversed' if reverse else 'Converted'}: {fname}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_dir', type=str, required=True, help='Input directory of .ds files')
    parser.add_argument('--out_dir', type=str, required=True, help='Output directory for converted .ds files')
    parser.add_argument('--reverse', action='store_true', help='Reverse mapping: English-like phonemes back to German')
    args = parser.parse_args()
    main(args.in_dir, args.out_dir, reverse=args.reverse)