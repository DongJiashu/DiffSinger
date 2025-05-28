#this tool is to move wav from multiple folders to one folder with wav name standardization
#mainly for gtsinger corpus

import os
import shutil
import pandas as pd

# configuration
original_wav_root = "/path/to/your/GTSinger/German"  
new_wav_dir = "/path/to/your/German"  
csv_path = "/path/to/your/transcriptions.csv" 
new_csv_path = "/path/to/your/transcriptions.csv" 

os.makedirs(new_wav_dir, exist_ok=True)

df = pd.read_csv(csv_path)

new_names = []
for old_name in df['name']:
    new_name = old_name.replace('/', '_')
    new_names.append(new_name)
    
    old_wav_path = os.path.join(original_wav_root, old_name + ".wav")
    
    new_wav_path = os.path.join(new_wav_dir, new_name + ".wav")
    
    if os.path.exists(old_wav_path):
        shutil.copy2(old_wav_path, new_wav_path)
    else:
        print(f"Warning: file not exist - {old_wav_path}")

df['name'] = new_names

df.to_csv(new_csv_path, index=False)

print("Done!")