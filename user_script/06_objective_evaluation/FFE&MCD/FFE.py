import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import librosa
from tqdm import tqdm
import argparse

def compute_ffe(f0_gt, vuv_gt, f0_pred, vuv_pred, threshold_cent=50):
    assert len(f0_gt) == len(f0_pred)
    total = len(f0_gt)
    voiced_gt = vuv_gt > 0
    voiced_pred = vuv_pred > 0
    vuv_mismatch = vuv_gt != vuv_pred
    eps = 1e-10
    cent_diff = 1200 * np.abs(np.log2((f0_gt + eps) / (f0_pred + eps)))
    cent_error = (cent_diff > threshold_cent) & voiced_gt & voiced_pred
    ffe = np.sum(vuv_mismatch | cent_error) / total
    return ffe

def extract_f0_vuv(wav_path, sr=44100, hop_length=512):
    y, _ = librosa.load(wav_path, sr=sr)
    f0, voiced_flag, _ = librosa.pyin(y, fmin=50, fmax=1000, sr=sr, hop_length=hop_length)
    vuv = voiced_flag.astype(int)
    f0[np.isnan(f0)] = 0
    return f0, vuv

def evaluate_folder(truth_dir, test_dir, output_dir, sr=44100, hop_length=512, speaker_prefix=None):
    os.makedirs(output_dir, exist_ok=True)
    records = []
    files = sorted(os.listdir(truth_dir))
    for file in tqdm(files, desc="Computing FFE"):
        if not file.endswith(".wav"):
            continue
        if speaker_prefix and not file.startswith(speaker_prefix):
            continue
        ref_path = os.path.join(truth_dir, file)
        test_path = os.path.join(test_dir, file.replace("_truth", ""))
        if not os.path.exists(test_path):
            print(f"Skipping {file}, no match found.")
            continue
        f0_gt, vuv_gt = extract_f0_vuv(ref_path, sr, hop_length)
        f0_pred, vuv_pred = extract_f0_vuv(test_path, sr, hop_length)
        min_len = min(len(f0_gt), len(f0_pred))
        f0_gt, vuv_gt = f0_gt[:min_len], vuv_gt[:min_len]
        f0_pred, vuv_pred = f0_pred[:min_len], vuv_pred[:min_len]
        ffe = compute_ffe(f0_gt, vuv_gt, f0_pred, vuv_pred)
        records.append((file, ffe))

    df = pd.DataFrame(records, columns=["filename", "FFE"])
    df.to_csv(os.path.join(output_dir, "ffe_scores.csv"), index=False)

    plt.figure(figsize=(12, 4))
    plt.bar(df["filename"], df["FFE"])
    plt.xticks(rotation=90)
    plt.ylabel("FFE")
    plt.title("F0 Frame Error (FFE) per File")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "ffe_barplot.png"))
    print(f"Saved FFE results to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute FFE between ground truth and synthesized audio.")
    parser.add_argument("--truth_dir", type=str, required=True, help="Path to ground truth wav files.")
    parser.add_argument("--test_dir", type=str, required=True, help="Path to synthesized wav files.")
    parser.add_argument("--output_dir", type=str, required=True, help="Path to save outputs.")
    parser.add_argument("--speaker", type=str, default=None, help="Prefix to filter files by speaker.")
    args = parser.parse_args()

    evaluate_folder(args.truth_dir, args.test_dir, args.output_dir, speaker_prefix=args.speaker)