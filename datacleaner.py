import pandas as pd
import os
import argparse  # For command-line arguments
from dotenv import load_dotenv

load_dotenv()

XLSX_FILE = os.environ.get("XLSX_FILE", "raw.xlsx")  # Keep defaults
OUTPUT_TSV = os.environ.get("OUTPUT_TSV", "cleaned_projects.tsv")

def clean_and_save_data(input_filepath=XLSX_FILE, output_filepath=OUTPUT_TSV, header_row=4, columns=None):  # input_filepath parameter
    """Cleans data from a specified input file and saves to a specified output file."""
    try:
        df = pd.read_excel(input_filepath, header=header_row)  # Use input_filepath


        if columns:
            if isinstance(columns, str):
                columns = [columns]
            # Clean column names when reading data
            cleaned_df = pd.read_excel(input_filepath, header=header_row)

            #Sanitize column names:
            cleaned_df.columns = [col.strip() for col in cleaned_df.columns]

            missing_cols = [col for col in columns if col not in df.columns]
            if missing_cols:
                raise KeyError(f"Missing columns: {missing_cols}. Check Excel file and code.")
            cleaned_df = df[columns]
        else:
            cleaned_df = df

        cleaned_df.to_csv(output_filepath, sep='\t', index=False)  # Use output_filepath
        print(f"Cleaned data saved to: {output_filepath}")

    except FileNotFoundError:
        print(f"Error: File '{xlsx_filepath}' not found.")
    except KeyError as e:
        print(f"KeyError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and save data.")
    parser.add_argument("--input", "-i", help="Input file path", default=XLSX_FILE)  # Input file argument
    parser.add_argument("--output", "-o", help="Output file path", default=OUTPUT_TSV)
    parser.add_argument("--header", "-hd", type=int, help="Header row index (0-based)", default=4)
    parser.add_argument("--columns", "-c", help="Column names (comma-separated or single)", default=None)
    args = parser.parse_args()

    column_names = None
    if args.columns:
        column_names = [col.strip() for col in args.columns.split(',')]

    clean_and_save_data(input_filepath=args.input, output_filepath=args.output, header_row=args.header, columns=column_names) # Pass input_filepath


