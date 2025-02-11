from flask import Blueprint, request, jsonify
from dataclasses import dataclass
from services.project_analyzer import analyze_project
from typing import Optional
import validators

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

@blueprint.route("/analyze", methods=['POST'])
async def analyze():
    try:
        data = request.get_json()
        project_request = ProjectRequest.from_json(data)
        
        result = await analyze_project(
            project_name=project_request.project_name,
            project_website=project_request.project_website,
            project_description=project_request.project_description,
            project_x_account=project_request.project_x_account,
            project_deck_url=project_request.project_deck_url,
            analysis_type=project_request.analysis_type
        )
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
