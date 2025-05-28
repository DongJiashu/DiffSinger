# This tool is used to manually slice wavs. 

import argparse
import os
from pathlib import Path

import torchaudio

def split_audio(input_path, output_dir, cuts):
    waveform, sample_rate = torchaudio.load(input_path)
    total_duration = waveform.shape[1] / sample_rate

    cuts = sorted([0.0] + cuts + [total_duration])

    os.makedirs(output_dir, exist_ok=True)
    base_name = Path(input_path).stem

    for i in range(len(cuts) - 1):
        start_sec = cuts[i]
        end_sec = cuts[i + 1]
        start_sample = int(start_sec * sample_rate)
        end_sample = int(end_sec * sample_rate)
        segment = waveform[:, start_sample:end_sample]
        out_path = os.path.join(output_dir, f"{base_name}_part{i}.wav")
        torchaudio.save(out_path, segment, sample_rate)
        print(f"Saved: {out_path} ({end_sec - start_sec:.2f}s)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split audio by given timestamps.")
    parser.add_argument("input", type=str, help="Input .wav file")
    parser.add_argument("output_dir", type=str, help="Directory to save output segments")
    parser.add_argument("cuts", nargs="+", type=float, help="Timestamps in seconds to split at (e.g. 5.5 25 30)")
    args = parser.parse_args()

    split_audio(args.input, args.output_dir, args.cuts)