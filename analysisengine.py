import logging
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

# Configure the API key
genai.configure(api_key=google_api_key)

# Initialize your LLM
llm = genai.GenerativeModel('gemini-1.5-pro')  # Adjust initialization as needed

# Directory to store prompt templates
PROMPTS_DIR = "prompts"

def load_prompt(prompt_name):
    """Loads a prompt template from a file."""
    filepath = os.path.join(PROMPTS_DIR, f"{prompt_name}.txt")  # Or .prompt
    try:
        with open(filepath, "r") as f:
            template = f.read()
        return PromptTemplate(input_variables=["analyses"], template=template)
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt '{prompt_name}' not found.")

def get_project_info():
    project_info = {}
    while True:
        source_type = input(
            "Enter a data source type (website, github, etc.) or 'done': "
        )
        if source_type.lower() == "done":
            break
        identifier = input(f"Enter the identifier for {source_type}: ")
        project_info[source_type] = identifier

    return project_info

def analyze_source(source_type, identifier):
    """Placeholder - Replace with actual analysis logic for each source."""
    # This function should fetch and analyze data based on the source type.
    # (Use web scraping, API calls, etc. as appropriate)
    analysis = f"Placeholder analysis of {source_type}: {identifier}"  
    return analysis

def generate_summary(analyses, prompt_name="project_analysis"):
    """Generates a summary using the specified prompt."""

    raw_prompt = load_prompt(prompt_name) # returns a PromptTemplate object

    # Format the prompt - This will return a string.
    prompt_text = raw_prompt.format(analyses=analyses)
    logging.info(f"Prompt: {analyses}")

    #Now make sure to remove any unintended curly braces:
    prompt_text = prompt_text.replace("{", "{{").replace("}", "}}")
    response = llm.generate_content(prompt_text)
    summary = response.text
    return summary



# # Main interaction loop (for cli testing purposes)
# project_info = get_project_info()

# while True:
#     analyses = []
#     for source_type, identifier in project_info.items():
#         analyses.append(analyze_source(source_type, identifier))

#     summary = generate_summary("\n\n".join(analyses))
#     print(summary)

#     if input("Is this summary sufficient (yes/no)? ").lower() == "yes":
#         break  # Exit if summary is sufficient

#     # Ask for more data sources if needed
#     print("Please provide additional information.")
#     project_info.update(get_project_info())