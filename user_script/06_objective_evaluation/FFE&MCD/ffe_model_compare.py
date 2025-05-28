import argparse
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def collect_ffe_scores(input_dir):
    all_data = []
    for root, dirs, files in os.walk(input_dir):
        if "ffe_scores.csv" in files:
            model_name = os.path.basename(root)
            df = pd.read_csv(os.path.join(root, "ffe_scores.csv"))
            if "FFE" in df.columns and "filename" in df.columns:
                df["model"] = model_name
                all_data.append(df)
            else:
                print(f"Skipping {os.path.join(root, 'ffe_scores.csv')}: missing 'FFE' or 'filename' column.")
    return pd.concat(all_data, ignore_index=True) if all_data else None

def plot_ffe_comparison(df, output_dir):
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="model", y="FFE", palette="coolwarm")
    plt.xticks(rotation=45)
    plt.title("FFE Comparison Across Models")
    plt.tight_layout()
    plot_path = os.path.join(output_dir, "ffe_comparison_boxplot.png")
    plt.savefig(plot_path)
    print(f"Saved plot to {plot_path}")

    # Save summary stats
    summary = df.groupby("model")["FFE"].agg(["mean", "std"]).reset_index()
    summary_path = os.path.join(output_dir, "ffe_summary.csv")
    summary.to_csv(summary_path, index=False)
    print(f"Saved FFE summary statistics to {summary_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, required=True, help="Root directory containing model subdirectories")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the output")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    df = collect_ffe_scores(args.input_dir)
    if df is not None:
        plot_ffe_comparison(df, args.output_dir)
    else:
        print("No valid FFE scores found.")
