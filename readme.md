# AlphaSight

AlphaSight is a project that uses AI to analyze various data sources and generate summaries. It leverages the `google.generativeai` package to interact with Google's generative AI models.


# Files
**analysisengine.py:** Contains the main logic for analyzing and evaluating projects.
**batch.py:** Script for batch processing multiple project evaluations.
**datacleaner.py:** Utility for cleaning and preprocessing data.
**hackathon_analysis.txt:** Prompt for hackathon analysis.
**project_analysis.txt:** Prompt for project analysis.



## Installation

To install the required dependencies, run:

```sh
pip install -r requirements.txt
```

## Configuration
Ensure you have a .env file in the root directory of the project with the following content

```sh
GOOGLE_API_KEY=your_google_api_key_here
```

Replace your_google_api_key_here with your actual Google API key.

## Usage

Data Cleaning: Clean and preprocess data using:

```
python datacleaner.py --header 2 --columns "Name, Description, Github, Deck" --input <your_input_file.xlsx> --output my_output.tsv

# Note: <your_input_file.xlsx> should be replaced with your actual input file.

```

Batch Processing: Use the batch script to process multiple evaluations:

```
python batch.py -i my_output.tsv -p hackathon_analysis -sc "Name, Description, Github, Deck"
```

## Project Structure
main.py: The main script that runs the project.
requirements.txt: The list of dependencies required for the project.
.env: The file containing environment variables, including the Google API key.
Dependencies
The project relies on the following main dependencies:

## Architecture 
google-generativeai: For interacting with Google's generative AI models.
langchain: For handling prompt templates and chaining.
dotenv: For loading environment variables from a .env file.
For a full list of dependencies, refer to the requirements.txt file.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

Contact
For any questions or inquiries, please contact the project maintainer.

