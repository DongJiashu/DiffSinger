#this tool is used to clean corpus folder for only wavs listed in csv. 

import os
import pandas as pd

# === configuration ===
csv_path = '/path/to/your/transcriptions.csv'
wavs_dir = '/path/to/your/wavs'
column_name = 'name'             # CSV clumn name（w/o .wav）

# === read csv===
df = pd.read_csv(csv_path)
csv_names = set(df[column_name].astype(str).str.strip())

# === scan folders ===
for fname in os.listdir(wavs_dir):
    if fname.endswith('.wav'):
        name_without_ext = os.path.splitext(fname)[0]
        if name_without_ext not in csv_names:
            path_to_delete = os.path.join(wavs_dir, fname)
            print(f"❌ Deleting: {path_to_delete}")
            os.remove(path_to_delete)

print("✅ clean up done， wavs in CSV is kept.")