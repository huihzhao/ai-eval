import os
import ssl
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import aiohttp
import json

@dataclass
class SecurityIncident:
    date: str
    severity: str  # Critical, High, Medium, Low
    type: str     # Security, Technical, Operational
    description: str
    resolution_status: str  # Resolved, In Progress, Unresolved
    impact: str

@dataclass
class CommunityAnalysis:
    sentiment_score: float  # 0-1 scale
    engagement_metrics: Dict[str, float]  # Different engagement metrics
    key_concerns: List[Dict[str, str]]   # Category and description
    recent_incidents: List[SecurityIncident]
    overall_risk_level: str
    analysis_period: str    # Time range of analysis
    data_sources: List[str] # Where the data comes from

    def to_dict(self) -> Dict:
        """Convert the CommunityAnalysis object to a dictionary"""
        return {
            "sentiment_score": self.sentiment_score,
            "engagement_metrics": self.engagement_metrics,
            "key_concerns": self.key_concerns,
            "recent_incidents": [asdict(incident) for incident in self.recent_incidents],
            "overall_risk_level": self.overall_risk_level,
            "analysis_period": self.analysis_period,
            "data_sources": self.data_sources
        }

class GrokSearchService:
    def __init__(self):
        self.api_key = os.getenv('GROK_API_KEY')
        if not self.api_key:
            raise ValueError("GROK_API_KEY environment variable is not set")
        self.base_url = "https://api.x.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def analyze_community_sentiment(self, project_name: str) -> CommunityAnalysis:
        """Analyze community sentiment using Grok chat API"""
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                messages = [
                    {
                        "role": "system",
                        "content": """You are analyzing blockchain projects. 
                        Provide analysis in the following JSON format:
                        {
                            "sentiment": {
                                "score": <0-1 float>,
                                "summary": "<string>"
                            },
                            "metrics": {
                                "social_activity": <0-1 float>,
                                "developer_activity": <0-1 float>,
                                "community_growth": <0-1 float>
                            },
                            "concerns": [
                                {
                                    "category": "<string>",
                                    "description": "<string>"
                                }
                            ],
                            "incidents": [
                                {
                                    "date": "<ISO date>",
                                    "severity": "<High/Medium/Low>",
                                    "type": "<string>",
                                    "description": "<string>",
                                    "resolution_status": "<string>",
                                    "impact": "<string>"
                                }
                            ],
                            "risk_level": "<High/Medium/Low>",
                            "analysis_period": "<string>",
                            "data_sources": ["<string>"]
                        }"""
                    },
                    {
                        "role": "user",
                        "content": f"Analyze the community sentiment, security incidents, and engagement metrics for {project_name}. Include the analysis period and data sources used. Return only the JSON response."
                    }
                ]

                async with session.post(f"{self.base_url}/chat/completions", json={
                    "messages": messages,
                    "model": "grok-2-latest",
                    "temperature": 0.1,
                    "stream": False
                }) as response:
                    response.raise_for_status()
                    result = await response.json()
                    
                    # Parse the chat completion response
                    analysis = json.loads(result["choices"][0]["message"]["content"])
                    
                    return CommunityAnalysis(
                        sentiment_score=analysis["sentiment"]["score"],
                        engagement_metrics=analysis["metrics"],
                        key_concerns=analysis["concerns"],
                        recent_incidents=[
                            SecurityIncident(**incident)
                            for incident in analysis["incidents"]
                        ],
                        overall_risk_level=analysis["risk_level"],
                        analysis_period=analysis.get("analysis_period", "Last 30 days"),  # From API
                        data_sources=analysis.get("data_sources", ["On-chain Data"])  # From API
                    )

        except aiohttp.ClientError as e:
            print(f"Grok API request failed: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            print(f"Invalid JSON response from Grok: {str(e)}")
            raise
        except Exception as e:
            print(f"Grok analysis failed: {str(e)}")
            raise

    # Remove unused _fetch_* methods as we're now using a single chat completion