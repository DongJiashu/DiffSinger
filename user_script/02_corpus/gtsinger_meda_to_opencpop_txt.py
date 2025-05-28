#This tool converts GTSinger metadata to diffsinger transcriptions.
#To use this to simply maintain line 10-33 for path and requested groups. 

import os
import json
import librosa
from tqdm import tqdm

# === User Settings ===
input_metadata_path = "/path/to/your/metadata.json"  # Set your metadata path here
output_transcription_path = "/path/to/your/transcriptions.txt"  # Set your output path here

# Specify full singer/technique/group paths you want to include. Don't need to specify songs. 
# Example: "EN-Alto-1/Mixed_Voice_and_Falsetto/Mixed_Voice_Group"
# If empty list [], include all.
singer_tech_group_filters = [
    #("DE-Soprano-1", "Breathy", "Control_Group"),
    #("DE-Soprano-1","Glissando","Control_Group"),
    #("DE-Soprano-1","Mixed_Voice_and_Falsetto","Mixed_Voice_Group"),
    #("DE-Soprano-1","Mixed_Voice_and_Falsetto","Control_Group"),
    #("DE-Soprano-1","Pharyngeal","Control_Group"),
    #("DE-Soprano-1","Vibrato","Vibrato_Group"),
    #("DE-Soprano-1","Vibrato","Control_Group"),

    #("EN-Alto-2", "Breathy", "Control_Group"),
    #("EN-Alto-2","Glissando","Control_Group"),
    #("EN-Alto-2","Mixed_Voice_and_Falsetto","Mixed_Voice_Group"),
    #("EN-Alto-2","Mixed_Voice_and_Falsetto","Control_Group"),
    #("EN-Alto-2","Pharyngeal","Control_Group"),
    #("EN-Alto-2","Vibrato","Vibrato_Group"),
    #("EN-Alto-2","Vibrato","Control_Group"),
    
]

# === script start ===
def match_item_path(item_path, filters):
    for singer, technique, group in filters:
        if f"{singer}/{technique}/" in item_path and f"/{group}/" in item_path:
            return True
    return False

def main():
    with open(input_metadata_path, 'r') as f:
        metadata = json.load(f)

    output_lines = []
    total_duration_min = 0.0

    for data in tqdm(metadata, desc="Processing metadata"):
        # item name
        item_path = data['item_name'].replace('#', '/')

        if singer_tech_group_filters and not match_item_path(item_path, singer_tech_group_filters):
            continue

        txt = ' '.join(data['txt']).replace('<SP>', '').replace('<AP>', '').strip()
        phs = ' '.join(data['ph']).replace('<SP>', 'SP').replace('<AP>', 'AP').replace('_de', '').strip()

        # ⚡⚡ librosa to note 
        notes = []
        for n in data['ep_pitches']:
            if n == 0:
                notes.append('rest')
            else:
                note = librosa.midi_to_note(n, octave=True, unicode=False)  # to e.g. G#4
                notes.append(note)
        notes = ' '.join(notes)

        note_durs = ' '.join([str(d) for d in data['ep_notedurs']])
        ph_durs = ' '.join([str(d) for d in data['ph_durs']])

        # slur 
        slurs = []
        last_phoneme = None
        for ph in data['ph']:
            if ph == last_phoneme:
                slurs.append(1)
            else:
                slurs.append(0)
            last_phoneme = ph
        slurs = ' '.join([str(s) for s in slurs])

        output_line = '|'.join([item_path, txt, phs, notes, note_durs, ph_durs, slurs])
        output_lines.append(output_line)

        total_duration_min += sum(data['ph_durs']) / 60.0

    os.makedirs(os.path.dirname(output_transcription_path), exist_ok=True)
    with open(output_transcription_path, 'w') as f:
        for line in output_lines:
            f.write(line + '\n')

    print(f"\n✅ Finished! Extracted {len(output_lines)} items, total duration: {total_duration_min:.2f} minutes.")

if __name__ == "__main__":
    main()