import google.generativeai as genai
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import os, re
import traceback
from dotenv import load_dotenv
from .prompt_manager import PromptManager
from .grok_search import GrokSearchService  # Add this import
import asyncio
from datetime import datetime
import json

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

@dataclass
class ProjectEvaluation:
    business_score: float
    technical_score: float
    risk_score: float
    total_score: float
    recommendation: str

    def to_dict(self):
        return asdict(self)

def extract_scores(content: str) -> ProjectScores:
    """Extract all scores from the content"""
    # Extract scores using regex patterns
    patterns = {
        'sustainability': r'Sustainability Assessment.*?Score:\s*(\d+)/5',
        'innovation': r'Technical Innovation.*?Score:\s*(\d+)/5',
        'security': r'Security & Risk Management.*?Score:\s*(\d+)/5',
        'team': r'Team & Execution.*?Score:\s*(\d+)/5',
        'total': r'Total Score:\s*(\d+)/20'
    }
    
    scores = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.DOTALL)
        scores[key] = float(match.group(1)) if match else 0.0
    
    return ProjectScores(
        sustainability_score=scores['sustainability'],
        innovation_score=scores['innovation'],
        team_score=scores['team'],
        total_score=scores['total']
    )

class ProjectAnalyzer:
    def __init__(self):
        self.grok_service = GrokSearchService()
        self.prompt_manager = PromptManager()
        self.timeout = 60  # 60 seconds timeout

    def _clean_gemini_response(self, response_text: str) -> str:
        """Clean Gemini response by removing markdown code blocks"""
        # Remove markdown code block markers and any language identifier
        pattern = r'```(?:json)?\s*(.*?)```'
        match = re.search(pattern, response_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return response_text.strip()

    async def analyze_project(self, project_data: Dict) -> Dict:
        try:
            # Get community analysis
            community_analysis = await self.grok_service.analyze_community_sentiment(
                project_data['project_name']
            )
            community_dict = community_analysis.to_dict()

            # Create prompt
            prompt = self.prompt_manager.create_analysis_prompt(
                project_data=project_data,
                community_analysis=community_dict
            )
            
            # Use run_in_executor for the blocking Gemini call
            loop = asyncio.get_running_loop()
            gemini_response = await loop.run_in_executor(
                None,
                lambda: model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.1,
                        "top_p": 0.8,
                        "top_k": 40,
                    }
                )
            )

            try:
                # Clean and parse response
                cleaned_response = self._clean_gemini_response(gemini_response.text)
                print(f"Cleaned response: {cleaned_response[:200]}...")  # Debug log
                
                analysis = json.loads(cleaned_response)
                return {
                    "community_insights": {
                        "sentiment": community_dict["sentiment_score"],
                        "engagement": community_dict["engagement_metrics"],
                        "incidents": community_dict["recent_incidents"]
                    },
                    "final_evaluation": analysis["final_evaluation"],
                    "metadata": {
                        "analysis_date": datetime.now().isoformat(),
                        "analysis_duration": "completed",
                        "data_sources": community_dict["data_sources"]
                    }
                }
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {str(e)}")
                print(f"Response text: {gemini_response.text}")
                raise ValueError(f"Invalid JSON format: {str(e)}")

        except Exception as e:
            print(f"Error during project analysis: {str(e)}")
            print(traceback.format_exc())
            raise
