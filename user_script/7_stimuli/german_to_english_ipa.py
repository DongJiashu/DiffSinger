#this tool is used to convert german ipa to english ipa
import os
import json
import argparse

# First-stage German to Phoible replacements
german_to_phoible = {
    'aj': 'aɪ', 'aw': 'aʊ', 'ɔʏ': 'ɔɪ', 'cʰ': 'kʰ', 'ɟ': 'ɡ',
    'ɲ': 'ŋ', 'm̩': 'm', 'n̩': 'n', 'aː': 'a'
}

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

def map_phoneme(ph):
    if ph in ('SP', 'AP'):  # skip silence/appendix tokens
        return ph
    ph = german_to_phoible.get(ph, ph)
    return phoneme_mapping.get(ph, ph)  # fallback to itself if not mapped

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

def main(in_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    if os.path.isfile(in_dir):
        if in_dir.endswith(".ds"):
            out_path = os.path.join(out_dir, os.path.basename(in_dir))
            process_file(in_dir, out_path)
            print(f"Converted: {os.path.basename(in_dir)}")
    else:
        for fname in os.listdir(in_dir):
            if fname.endswith(".ds"):
                in_path = os.path.join(in_dir, fname)
                out_path = os.path.join(out_dir, fname)
                process_file(in_path, out_path)
                print(f"Converted: {fname}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_dir', type=str, required=True, help='Input directory of .ds files')
    parser.add_argument('--out_dir', type=str, required=True, help='Output directory for converted .ds files')
    args = parser.parse_args()
    main(args.in_dir, args.out_dir)