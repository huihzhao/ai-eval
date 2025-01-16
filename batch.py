import csv
from analysisengine import generate_summary, analyze_source
import os
from dotenv import load_dotenv
import pandas as pd
import time
import logging
import argparse  # Import the argparse module
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

CSV_FILE = os.environ.get("CSV_FILE", "cleaned_projects.tsv")
RATE_LIMIT_DELAY = int(os.environ.get("RATE_LIMIT_DELAY", 2))  # Delay in seconds

def analyze_projects_from_csv(csv_filepath=CSV_FILE, prompt_name="project_analysis", save_interval=1, source_columns=None, project_name_column="Name"):
    """Analyzes projects with flexible source columns and periodic saving."""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tsv", delete=False) as temp_file:
            temp_filepath = temp_file.name

            df = pd.read_csv(csv_filepath, sep='\t')

            if "Summary" not in df.columns:
                df["Summary"] = ""

            for index, row in df.iterrows():
                project_name = row.get(project_name_column) 
                logging.info(f"start analyzing: {project_name}")

                if pd.notna(project_name):
                    analyses = []
                    if source_columns:  # Use provided columns
                        logging.info(f"Analyzing {project_name} with specified source columns: {source_columns}")
                        for source_type in source_columns:
                            identifier = row.get(source_type)
                            logging.info(f"identifier: {identifier}")
                            if identifier and pd.notna(identifier):
                                analyses.append(analyze_source(source_type.lower(), identifier))
                    else:    # If no columns specified, use all except "Name", "Summary"
                        for source_type in [col for col in df.columns if col not in ["Name", "Summary"]]:
                            identifier = row.get(source_type)
                            if identifier and pd.notna(identifier):
                                analyses.append(analyze_source(source_type.lower(), identifier))

                    if analyses:
                        try:
                            summary = generate_summary("\n\n".join(analyses), prompt_name)
                            df.loc[index, "Summary"] = summary
                            logging.info(f"Summary generated for {project_name}: {summary}") # Log the summary
                            time.sleep(RATE_LIMIT_DELAY)

                        except Exception as e:
                            logging.error(f"Error generating summary for {project_name}: {e}")
                            df.loc[index, "Summary"] = "Error generating summary"

                if (index + 1) % save_interval == 0:
                    try:
                        df.to_csv(temp_filepath, sep='\t', index=False)  # Save to temp file
                        logging.info(f"Progress saved to {temp_filepath} (processed {index+1} rows)")
                    except Exception as e:
                        logging.error(f"Error saving progress: {e}")

            # Final save, replace original
            df.to_csv(temp_filepath, sep='\t', index=False)
        os.replace(temp_filepath, csv_filepath)  # Replace original after processing all rows
        logging.info(f"Analysis complete. Results saved to: {csv_filepath}")

    except FileNotFoundError:
        logging.error(f"File not found: {csv_filepath}")
    except pd.errors.ParserError as e:
        logging.error(f"Error parsing CSV/TSV: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze projects from a CSV/TSV file.")
    parser.add_argument("--prompt", "-p", help="Name of the prompt file (without extension)", default="project_analysis")
    parser.add_argument("--input", "-i", help="Path to the input CSV/TSV file", default=CSV_FILE)
    parser.add_argument("--save_interval", "-s", type=int, help="Save interval (number of rows)", default=1)
    parser.add_argument("--source_columns", "-sc", help="Source columns (comma-separated)", default=None)
    parser.add_argument("--project_name_column", "-pn", help="Name of the project name column", default="Name")  # Add argument
    args = parser.parse_args()

    source_cols = None
    if args.source_columns:
        source_cols = [col.strip() for col in args.source_columns.split(',')]

    logging.info(f"Analyzing projects from: {args.input} with prompt: {args.prompt}, save interval: {args.save_interval}, source columns: {source_cols}")

    analyze_projects_from_csv(
        prompt_name=args.prompt,
        csv_filepath=args.input,
        save_interval=args.save_interval,
        source_columns=source_cols,
        project_name_column=args.project_name_column
    )

