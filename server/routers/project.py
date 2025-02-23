from quart import Blueprint, request, jsonify
from dataclasses import dataclass
from services.project_analyzer import ProjectAnalyzer
from services.auth import require_auth
from typing import Optional
import validators
import traceback
import asyncio

blueprint = Blueprint('project', __name__)

@dataclass
class ProjectRequest:
    project_name: str
    project_website: str
    project_description: str
    project_x_account: str
    project_deck_url: str
    analysis_type: Optional[str] = None

    @staticmethod
    def from_json(data):
        if not all(k in data for k in ['project_name', 'project_website', 'project_description', 'project_x_account', 'project_deck_url']):
            raise ValueError("Missing required fields")
        
        if not validators.url(data['project_website']):
            raise ValueError("Invalid project website URL")
        
        if not validators.url(data['project_deck_url']):
            raise ValueError("Invalid project deck URL")
            
        return ProjectRequest(
            project_name=data['project_name'],
            project_website=data['project_website'],
            project_description=data['project_description'],
            project_x_account=data['project_x_account'],
            project_deck_url=data['project_deck_url'],
            analysis_type=data.get('analysis_type')
        )

# Create analyzer instance
analyzer = ProjectAnalyzer()

@blueprint.route("/analyze", methods=['POST'])
@require_auth
async def analyze():
    try:
        data = await request.get_json()
        project_data = {
            "project_name": data.get('project_name'),
            "project_website": data.get('project_website'),
            "project_description": data.get('project_description'),
            "project_x_account": data.get('project_x_account'),
            "project_deck_url": data.get('project_deck_url'),
            "analysis_type": data.get('analysis_type')
        }
        
        result = await analyzer.analyze_project(project_data=project_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
