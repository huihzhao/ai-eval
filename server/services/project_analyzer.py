import google.generativeai as genai
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import os, re
import traceback
from dotenv import load_dotenv
from .prompt_manager import PromptManager

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

@dataclass
class ProjectScores:
    sustainability_score: float
    innovation_score: float
    team_score: float
    total_score: float
    
    def to_dict(self):
        return asdict(self)

def extract_scores(content: str) -> ProjectScores:
    """Extract all scores from the content"""
    # Default scores
    scores = {
        'sustainability': 0,
        'innovation': 0,
        'team': 0,
        'total': 0
    }
    
    # Pattern to match scores like (4/5) or 4/5
    score_pattern = r'(?:Rate:|Score:|\()?(\d+)\/(\d+)\)?'
    
    # Extract individual category scores
    if re.search(r'Sustainability.*?(\d+)/5', content, re.DOTALL):
        scores['sustainability'] = float(re.search(r'Sustainability.*?(\d+)/5', content, re.DOTALL).group(1))
    
    if re.search(r'Innovation.*?(\d+)/5', content, re.DOTALL):
        scores['innovation'] = float(re.search(r'Innovation.*?(\d+)/5', content, re.DOTALL).group(1))
    
    if re.search(r'Overall excellence.*?(\d+)/5', content, re.DOTALL):
        scores['team'] = float(re.search(r'Overall excellence.*?(\d+)/5', content, re.DOTALL).group(1))
    
    # Extract final score
    final_score_match = re.search(r'(?:Final|Total)\s+Score:\s*(\d+)/15', content)
    if final_score_match:
        scores['total'] = float(final_score_match.group(1))
    else:
        # Calculate total if not explicitly stated
        scores['total'] = sum([scores['sustainability'], scores['innovation'], scores['team']])

    return ProjectScores(
        sustainability_score=scores['sustainability'],
        innovation_score=scores['innovation'],
        team_score=scores['team'],
        total_score=scores['total']
    )

def analyze_project(
    project_name: str,
    project_website: str,
    project_description: str,
    project_x_account: str,
    project_deck_url: str,
    analysis_type: Optional[str] = None
) -> Dict:
    try:
        # Initialize prompt manager with correct path
        current_dir = os.path.dirname(os.path.dirname(__file__))
        prompt_manager = PromptManager(current_dir)
        
        # Format prompt with project details
        prompt = prompt_manager.format_prompt(
            'project_analysis',
            project_name=project_name,
            project_website=project_website,
            project_description=project_description,
            project_x_account=project_x_account,
            project_deck_url=project_deck_url
        )

        response = model.generate_content(prompt)
        content = response.text
        
        # Extract scores
        scores = extract_scores(content)
        
        # Return both raw response and structured scores
        return {
            "response": content,
            "scores": scores.to_dict()
        }

    except Exception as e:
        print(f"Error during project analysis: {str(e)}")
        print(traceback.format_exc())
        raise Exception(f"Failed to analyze project: {str(e)}")
