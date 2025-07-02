
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --- USER CONFIGURATION ---
# IMPORTANT: Make sure this filename exactly matches the CSV file in the same folder.
# It is highly recommended to rename your CSV to something simpler to avoid errors.
CSV_FILENAME = 'Histogram of C1-ig430ffusedcropped8bitonecolor.csv'

OUTPUT_FILENAME = 'Micrograph_Intensity_Histogram_LinearY.png'
# --------------------------


def plot_micrograph_histogram(csv_path, output_path):
    """
    Loads data from a histogram CSV and generates a styled bar chart.
    """
    print(f"--- Loading Histogram Data ---")
    print(f"Attempting to read file: {csv_path}")

    # 1. Load the data from the CSV file
    try:
        # We assume the CSV has two columns: Intensity Value and Count
        df = pd.read_csv(csv_path)
        print("✓ Successfully loaded CSV file.")
    except FileNotFoundError:
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"[FATAL ERROR] File not found at the specified path.")
        print(f"Please ensure the file '{csv_path.name}' is in the same directory as the script.")
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return
    except Exception as e:
        print(f"[FATAL ERROR] An error occurred while reading the CSV: {e}")
        return

    # 2. Identify the intensity and count columns. We assume they are the first two.
    if len(df.columns) < 2:
        print("[FATAL ERROR] The CSV file does not have at least two columns.")
        return
        
    intensity_col = df.columns[0]
    count_col = df.columns[1]
    print(f"Using columns: '{intensity_col}' for X-axis and '{count_col}' for Y-axis.")
    
    x_values = df[intensity_col]
    y_values = df[count_col]

    # 3. Create the plot
    print("--- Generating Plot ---")
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Use a color from the viridis map for a consistent style
    bar_color = plt.cm.viridis(0.5)

    # For a linear scale, we can plot the data directly without filtering zeros.
    ax.bar(x_values, y_values, width=1.0, color=bar_color, align='center')

    # 4. Style the plot to match the previous charts
    # ax.set_yscale('log') # This line has been removed for a linear scale.
    ax.set_xlim(-1, 256) # Standard 8-bit intensity range (0-255)
    ax.set_xlabel('Intensity (8-bit)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Frequency (Pixel Count)', fontsize=14, fontweight='bold') # Label updated
    ax.grid(True, which='major', axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()

    # 5. Save the plot to a file
    plt.savefig(output_path, dpi=300)
    print(f"✓ Successfully saved histogram to: {output_path}")


def main():
    """Main function to define paths and run the plotting function."""
    try:
        base_path = Path(__file__).resolve().parent
        print(f"--- Script running in directory: {base_path} ---")
    except NameError:
        base_path = Path.cwd()
        print(f"--- Using current working directory: {base_path} ---")

    csv_full_path = base_path / CSV_FILENAME
    output_full_path = base_path / OUTPUT_FILENAME

    plot_micrograph_histogram(csv_full_path, output_full_path)


if __name__ == '__main__':
    main()
