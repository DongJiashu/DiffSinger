import numpy as np
import librosa
import os
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import argparse


def compute_mfcc(wav_path, sr=22050, n_mfcc=13, hop_length=256):
    y, _ = librosa.load(wav_path, sr=sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, hop_length=hop_length)[1:]
    mfcc = (mfcc - np.mean(mfcc, axis=1, keepdims=True)) / (np.std(mfcc, axis=1, keepdims=True) + 1e-6)
    mfcc = np.clip(mfcc, -5.0, 5.0)
    print(f"MFCC shape for {wav_path}: {mfcc.T.shape}")
    return mfcc.T  # shape: (frames, n_mfcc)


parser = argparse.ArgumentParser()
parser.add_argument("--truth_dir", type=str, required=True)
parser.add_argument("--test_dir", type=str, required=True)
parser.add_argument("--output_dir", type=str, required=True)
parser.add_argument("--speaker", type=str, default=None)
args = parser.parse_args()

truth_dir = args.truth_dir
test_dir = args.test_dir
output_dir = args.output_dir
os.makedirs(output_dir, exist_ok=True)

nat_files = os.listdir(truth_dir)
syn_files = os.listdir(test_dir)
syn_map = {f.replace("_truth", ""): f for f in syn_files}

log_const = 10.0 / np.log(10.0)

mcd_results = []
for wav_name in tqdm(nat_files, desc="Computing MCD"):
    if args.speaker and not wav_name.startswith(args.speaker):
        continue
    key_name = wav_name.replace("_truth", "")
    if key_name not in syn_map:
        print(f"Unmatched file: {wav_name} (no match in synth)")
        continue
    synth_name = syn_map[key_name]
    try:
        mfcc_nat = compute_mfcc(os.path.join(truth_dir, wav_name))
        mfcc_syn = compute_mfcc(os.path.join(test_dir, synth_name))

        dist, path = fastdtw(mfcc_nat, mfcc_syn, dist=euclidean)
        print(f"DTW path length for {wav_name}: {len(path)}")
        x = np.array([mfcc_nat[i] for i, _ in path])
        y = np.array([mfcc_syn[j] for _, j in path])
        diff = x - y
        frame_dists = np.sqrt(2 * np.sum(diff**2, axis=1))
        total = np.sum(frame_dists)
        if len(frame_dists) == 0:
            print(f"Skipping {wav_name} due to empty alignment.")
            continue
        mcd = log_const * (total / len(frame_dists))
        mcd_results.append((wav_name, mcd))

        # Save dual-line MFCC norm plot without shaded difference
        plt.figure(figsize=(10, 4))
        plt.plot(np.linalg.norm(x, axis=1), label="GT (norm)", color='blue')
        plt.plot(np.linalg.norm(y, axis=1), label="Synth (norm)", color='red')
        plt.xlabel("Frame Index")
        plt.ylabel("MFCC Norm")
        plt.title(f"GT vs Synth MFCC Norm: {wav_name}")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"frame_diff_{wav_name.replace('.wav', '')}.png"))
        plt.close()
    except Exception as e:
        print(f"Error processing {wav_name}: {e}")
        if 'mfcc_nat' in locals() and 'mfcc_syn' in locals():
            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            plt.imshow(mfcc_nat.T, aspect='auto', origin='lower')
            plt.title(f"GT MFCC: {wav_name}")
            plt.subplot(1, 2, 2)
            plt.imshow(mfcc_syn.T, aspect='auto', origin='lower')
            plt.title(f"Syn MFCC: {synth_name}")
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"mfcc_debug_{wav_name.replace('.wav', '')}.png"))
            plt.close()
        continue

df = pd.DataFrame(mcd_results, columns=["filename", "mcd"])
# df.columns = df.columns.str.lower()
df.to_csv(os.path.join(output_dir, "mcd_scores.csv"), index=False)

mean_mcd = df["mcd"].mean()
std_mcd = df["mcd"].std()
min_mcd = df["mcd"].min()
max_mcd = df["mcd"].max()

print(f"Summary Statistics:")
print(f"Mean MCD: {mean_mcd:.3f}")
print(f"Std  MCD: {std_mcd:.3f}")
print(f"Min  MCD: {min_mcd:.3f}")
print(f"Max  MCD: {max_mcd:.3f}")

plt.figure(figsize=(10, 5))
plt.bar(df["filename"], df["mcd"])
plt.xticks(rotation=45, ha='right')
plt.ylabel("MCD Score")
plt.title("Mel-Cepstral Distortion (MCD) per file")
plt.axhline(mean_mcd, color='red', linestyle='--', label=f"Mean: {mean_mcd:.2f}")
plt.fill_between(df.index, mean_mcd - std_mcd, mean_mcd + std_mcd, color='red', alpha=0.1, label=f"±1 Std")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "mcd_plot.png"))
plt.close()
