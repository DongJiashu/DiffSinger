import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
from scipy.stats import f_oneway, ttest_ind
from itertools import combinations
from statannotations.Annotator import Annotator

def collect_mcd_scores(parent_dir):
    all_data = []

    for model_name in os.listdir(parent_dir):
        model_path = os.path.join(parent_dir, model_name)
        csv_path = os.path.join(model_path, "mcd_scores.csv")

        if os.path.isdir(model_path) and os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path)
                df.columns = df.columns.str.lower()
                if 'mcd' in df.columns and 'filename' in df.columns:
                    all_data.append(df[['filename', 'mcd']].assign(model=model_name))
                else:
                    print(f"Skipping {csv_path}: missing 'mcd' or 'filename' column.")
            except Exception as e:
                print(f"Error reading {csv_path}: {e}")
        else:
            print(f"Skipping {model_name}: no mcd_scores.csv found.")

    if not all_data:
        raise ValueError("No valid mcd_scores.csv files found.")

    return pd.concat(all_data, ignore_index=True)

def plot_mcd_comparison(df, output_path):
    plt.figure(figsize=(12, 8))
    custom_palette = {
        '0514_baseline_german_gt_180min': '#4760BB', 
        '0514_english_to_german_gt_60min': '#353E7A',  # Purple (previously gt_180)# Deep Purple
        '0514_english_to_german_gt_30min': '#353E7A',  # Purple (previously gt_180)
        '0514_english_to_german_gt_15min': '#60568B',  # Dodger Blue (new for gt_15)
        '0515_english_to_german_ohr_15min': '#8E739C',  # Medium Blue (previously shrimpchen_15)
        '0515_english_to_german_shrimpchen_15min': '#AF84A0'  # Bright Blue (previously gt_30)
    }
    sns.boxplot(
        data=df,
        x='model',
        y='mcd',
        palette=custom_palette,
        order=[
            '0514_baseline_german_gt_180min',
            '0514_english_to_german_gt_30min',
            '0514_english_to_german_gt_15min',
            '0515_english_to_german_ohr_15min',
            '0515_english_to_german_shrimpchen_15min'
        ],
        boxprops=dict(alpha=0.8)
    )

    plt.title("MCD Comparison Across Models")
    plt.ylabel("Mel Cepstral Distortion (MCD)")
    plt.xlabel("Model")
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "mcd_comparison_boxplot.png"))
    print(f"Saved plot to {output_path}/mcd_comparison_boxplot.png")

    # Save raw data as summary
    df.groupby("model")["mcd"].agg(['mean', 'std', 'min', 'max']).to_csv(os.path.join(output_path, "mcd_summary.csv"))
    print(f"Saved MCD summary statistics to {output_path}/mcd_summary.csv")


# Statistical analysis functions
def perform_anova(df):
    grouped = df.groupby("model")["mcd"]
    model_scores = [group.values for name, group in grouped]
    stat, p = f_oneway(*model_scores)
    print(f"ANOVA result: F={stat:.3f}, p-value={p:.5f}")
    return stat, p

def pairwise_ttests(df, output_path):
    results = []
    for model1, model2 in combinations(df['model'].unique(), 2):
        data1 = df[df['model'] == model1]['mcd']
        data2 = df[df['model'] == model2]['mcd']
        stat, pval = ttest_ind(data1, data2, equal_var=False)
        results.append((model1, model2, stat, pval))
    
    results_df = pd.DataFrame(results, columns=["Model1", "Model2", "T-stat", "P-value"])
    results_df.to_csv(os.path.join(output_path, "ttest_results.csv"), index=False)
    print(f"Saved pairwise t-test results to {output_path}/ttest_results.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, required=True, help="Folder containing model subfolders with mcd_scores.csv files")
    parser.add_argument("--output_dir", type=str, default=".", help="Where to save the result plot and summary")

    args = parser.parse_args()
    df = collect_mcd_scores(args.input_dir)
    plot_mcd_comparison(df, args.output_dir)
    pairwise_ttests(df, args.output_dir)