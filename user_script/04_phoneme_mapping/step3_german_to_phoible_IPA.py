import argparse
import os
import pandas as pd

# mapping to phoible symbols
german_to_phoible = {
    'aj': 'aɪ', 'aw': 'aʊ', 'ɔʏ': 'ɔɪ', 'cʰ': 'kʰ', 'ɟ': 'ɡ',
    'ɲ': 'ŋ', 'm̩': 'm', 'n̩': 'n', 'aː': 'a'
}

def replace_phonemes(ph_seq: str) -> str:
    phones = ph_seq.strip().split()
    replaced = [german_to_phoible.get(p, p) for p in phones]
    return ' '.join(replaced)

def main(input_path):
    df = pd.read_csv(input_path)
    df['ph_seq'] = df['ph_seq'].apply(replace_phonemes)

    input_dir = os.path.dirname(input_path)
    input_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(input_dir, f"{input_name}_to_phoible.csv")

    df.to_csv(output_path, index=False)
    print(f"Saved converted file to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True, help='Path to the input CSV file')
    args = parser.parse_args()
    main(args.input)