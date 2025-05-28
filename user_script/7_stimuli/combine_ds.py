#this tool is to combine ds files 
import json
import os
import argparse
from glob import glob

def merge_ds_files(input_dir, first_offset=0):
    ds_files = sorted(glob(os.path.join(input_dir, "*.ds")))
    if not ds_files:
        raise ValueError(f"No .ds files found in directory: {input_dir}")

    merged_items = []
    current_offset = first_offset  

    for file_path in ds_files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):  
                for item in data:
                    item["offset"] = current_offset
                    merged_items.append(item)
                    ph_dur_sum = sum(float(dur) for dur in item["ph_dur"].split())
                    current_offset += ph_dur_sum
            else:  #
                data["offset"] = current_offset
                merged_items.append(data)
                ph_dur_sum = sum(float(dur) for dur in data["ph_dur"].split())
                current_offset += ph_dur_sum

    output_path = os.path.join(input_dir, "_combined.ds")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged_items, f, indent=4, ensure_ascii=False)

    print(f"Done！Saved in {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combined .ds file and according to ph_dur calculate  offset")
    parser.add_argument("--input_dir", type=str, required=True, help="folder（contains .ds files）")
    args = parser.parse_args()

    merge_ds_files(args.input_dir)