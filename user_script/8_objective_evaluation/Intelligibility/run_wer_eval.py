#this tool is used to get wer
from pathlib import Path
import csv
from jiwer import wer

# Set your ground truth .lab folder here
GT_DIR = "wav_ground_truth"

# List of model output folders
MODEL_DIRS = [
    "0501_english_zero_shot",
    "0514_baseline_german_gt_180min",
    "0514_english_to_german_gt_15min",
    "0514_english_to_german_gt_30min",
]

# Output CSV
OUTPUT = "wer_summary.csv"

# List of utterance IDs to ignore (no file extension)
IGNORE_LIST = [
    "wie_schone_du_bist_combined",
    "kaputt_combined",
]

def read_lab_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().strip()

def main():
    gt_dir = Path(GT_DIR)
    model_dirs = [Path(d) for d in MODEL_DIRS]
    ignore_set = set(IGNORE_LIST)

    # Collect all utterance IDs from ground truth directory
    utterance_ids = []
    for p in gt_dir.glob("*.lab"):
        stem = p.stem
        if stem.endswith("_truth"):
            stem = stem[:-6]
        if stem not in ignore_set:
            utterance_ids.append(stem)

    # Prepare CSV header
    header = ["utterance_id"] + [d.name for d in model_dirs]

    # Open CSV for writing
    with open(OUTPUT, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

        rows = []
        for utt_id in utterance_ids:
            gt_path_with_truth = gt_dir / f"{utt_id}_truth.lab"
            gt_path_default = gt_dir / f"{utt_id}.lab"
            gt_path = gt_path_with_truth if gt_path_with_truth.exists() else gt_path_default
            if not gt_path.exists():
                print(f"Warning: Ground truth file {gt_path} not found, skipping.")
                continue
            gt_text = read_lab_file(gt_path)

            row = [utt_id]
            for model_dir in model_dirs:
                pred_path = model_dir / f"{utt_id}.lab"
                if not pred_path.exists():
                    print(f"Warning: Prediction file {pred_path} not found, writing empty WER.")
                    row.append("")
                    continue
                pred_text = read_lab_file(pred_path)
                error = wer(gt_text, pred_text)
                row.append(f"{error:.4f}")
            writer.writerow(row)
            rows.append(row)

    # Compute average WER per model
    model_names = [d.name for d in model_dirs]
    model_sums = [0.0] * len(model_names)
    model_counts = [0] * len(model_names)

    for row in rows:
        for i, val in enumerate(row[1:]):
            if val != "":
                try:
                    model_sums[i] += float(val)
                    model_counts[i] += 1
                except ValueError:
                    pass

    averages = []
    for s, c in zip(model_sums, model_counts):
        avg = s / c if c > 0 else None
        averages.append(avg)

    # Write averages to second CSV
    avg_output = "wer_summary_avg.csv"
    with open(avg_output, 'w', newline='', encoding='utf-8') as avg_csvfile:
        writer = csv.writer(avg_csvfile)
        writer.writerow(["Model", "Average_WER"])
        for model_name, avg in zip(model_names, averages):
            if avg is None:
                writer.writerow([model_name, ""])
            else:
                writer.writerow([model_name, f"{avg:.4f}"])

if __name__ == "__main__":
    main()
