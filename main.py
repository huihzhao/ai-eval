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

def get_project_info():
    """Interactively gathers project information from the user."""
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

def generate_summary(analyses):
    """Generates a summary using the LLM."""
    template = """
Please analyse the project by crawling the twitter account and webpage of the project, and document if available from the following perspectives(score from 1 to 10, the higher the better):\

1. UX/UI design: to see if the UX of the project can be attractive for users. \
2. Technology innovations: to identify if the project has a innovative and solid tech design. \
3. Feedback from users: analyse the feedbacks in the official X account \
4. github repo: analyze the popularity of the github repo, like number of forks, stars, etc. \
5. token: analyze if the token has been listed on CMC, coingecko or similar sites \
6. Team: analyze the team information to identify if the team has a strong background like from famous companies or strong academic background. \

Please make the evaluation extremely strict and give a summary that includes the overall score. If the overall score is higher than 6, it should be emphasised. \
Please double confirm the official account of X to make sure the account is correct before you start evaluation. The precision is very important. \
Please analyze the pinned post of X account of the project as well to identify the current status of the project. 

{analyses}

Provide a concise and informative summary.
    """
    prompt = PromptTemplate(
        input_variables=["analyses"], template=template
    )
    prompt_text = prompt.format(analyses=analyses)
    response = llm.generate_content(prompt_text)  # Use the correct method
    summary = response.text  # Access the content attribute
    return summary

# Main interaction loop
project_info = get_project_info()

while True:
    analyses = []
    for source_type, identifier in project_info.items():
        analyses.append(analyze_source(source_type, identifier))

    summary = generate_summary("\n\n".join(analyses))
    print(summary)

    if input("Is this summary sufficient (yes/no)? ").lower() == "yes":
        break  # Exit if summary is sufficient

    # Ask for more data sources if needed
    print("Please provide additional information.")
    project_info.update(get_project_info())