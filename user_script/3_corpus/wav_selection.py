# This tool is used to select wavs for corpus depends on the target total duration
import os
import random
import shutil
import soundfile as sf
import pandas as pd

# configuration
wav_folder = '/path/to/your/wavs'
output_csv_path = '/path/to/your/transcriptions_updated.csv'
delete_wav_folder = '/path/to/your/wavs_deleted'
original_csv_path = '/path/to/your/transcriptions.csv'

target_min = 15 * 60         # minimal kept minutes 15 mins e.g. in this case
target_max = 15.5 * 60       # maximal kept minutes.

os.makedirs(delete_wav_folder, exist_ok=True)

audio_durations = {}
for fname in os.listdir(wav_folder):
    if fname.endswith('.wav'):
        path = os.path.join(wav_folder, fname)
        try:
            with sf.SoundFile(path) as f:
                duration = len(f) / f.samplerate
                audio_durations[fname.replace('.wav', '')] = duration
        except Exception as e:
            print(f"读取失败 {fname}: {e}")

all_items = list(audio_durations.items())
best_keep = []
best_total = 0

# random selection
for _ in range(1000):
    random.shuffle(all_items)
    temp_list = []
    total = 0
    for name, dur in all_items:
        if total + dur > target_max:
            break
        temp_list.append(name)
        total += dur
    if target_min <= total <= target_max and total > best_total:
        best_keep = temp_list
        best_total = total
        if abs(best_total - target_min) < 30:  
            break

print(f"kept {len(best_keep)} items，total duration {best_total/60:.2f} minutes")

df = pd.read_csv(original_csv_path)
filtered_df = df[df['name'].isin(best_keep)]
filtered_df.to_csv(output_csv_path, index=False)
print(f"Saved updated CSV in {output_csv_path}")

keep_set = set(best_keep)
for fname in os.listdir(wav_folder):
    if fname.endswith('.wav'):
        name = fname.replace('.wav', '')
        if name not in keep_set:
            src = os.path.join(wav_folder, fname)
            dst = os.path.join(delete_wav_folder, fname)
            shutil.move(src, dst)

print(f"Deleted wavs saved in {delete_wav_folder}")