#this tool is used to calculate duration of corpus

import os
import argparse
import torchaudio
import matplotlib.pyplot as plt

def print_wav_info(folder):
    print(f"\nScanning folder and subdirectories: {folder}\n")
    durations = {}
    counts = {}
    
    for root, dirs, files in os.walk(folder):
        total_duration = 0.0
        wav_files_found = False
        wav_count = 0
        for filename in files:
            if filename.lower().endswith(".wav"):
                wav_files_found = True
                wav_count += 1
                filepath = os.path.join(root, filename)
                try:
                    waveform, sample_rate = torchaudio.load(filepath)
                    duration_sec = waveform.shape[1] / sample_rate
                    if duration_sec > 15:
                        print(f"WARNING: {filename} exceeds 15 seconds ({duration_sec:.2f}s)")
                    total_duration += duration_sec
                except Exception as e:
                    print(f"{filename}: Failed to load ({e})")
        if wav_files_found:
            relative_path = os.path.relpath(root, folder)
            durations[relative_path] = total_duration / 60  # convert to minutes
            counts[relative_path] = wav_count

    if durations:
        # Sort by subdir name
        subdirs = sorted(durations.keys())
        dur_values = [durations[subdir] for subdir in subdirs]
        wav_counts = [counts[subdir] for subdir in subdirs]
        grand_total = sum(dur_values)
        total_items = sum(wav_counts)

        plt.figure(figsize=(10, 6))
        bars = plt.bar(subdirs, dur_values, color='skyblue')
        plt.xlabel('Subdirectory')
        plt.ylabel('Total Duration (minutes)')
        plt.title('Duration distribution of wav per singer')
        plt.xticks(rotation=45, ha='right')
        plt.ylim(0, max(dur_values) + 2)

        # Annotate duration + item count on top of each bar
        for bar, dur, count in zip(bars, dur_values, wav_counts):
            height = bar.get_height()
            label = f"{dur:.1f}min,{count}items"
            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.3, label, ha='center', va='bottom', fontsize=9)

        # Annotate grand total duration and item count at bottom right
        plt.annotate(f'Total: {grand_total:.1f}min, {total_items}items',
                     xy=(1.0, 0.01), xycoords='axes fraction',
                     ha='right', fontsize=10)

        plt.tight_layout()
        save_path = os.path.join(folder, 'duration_summary.png')
        plt.savefig(save_path)
        print(f"\nSaved duration summary plot to: {save_path}")
    else:
        print("No WAV files found in any subdirectory.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print sample rate and duration of WAV files in a folder.")
    parser.add_argument("folder", type=str, help="Path to folder containing .wav files")
    args = parser.parse_args()
    
    print_wav_info(args.folder)