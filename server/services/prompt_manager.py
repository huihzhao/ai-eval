import os
import json
from string import Template
from typing import Dict, Optional

class PromptManager:
    def __init__(self, base_dir: Optional[str] = None):
        if base_dir:
            self.template_path = os.path.join(base_dir, 'prompts/project_analysis.txt')
        else:
            self.template_path = os.path.join(
                os.path.dirname(__file__), 
                '../prompts/project_analysis.txt'
            )
        
        with open(self.template_path, 'r') as f:
            self.template = Template(f.read())

    def create_analysis_prompt(
        self, 
        project_data: Dict,
        community_analysis: Dict  # Changed from community_data to match caller
    ) -> str:
        """Create analysis prompt using project data and community analysis"""
        try:
            # Format engagement metrics with error handling
            engagement_metrics = self._format_engagement_metrics(
                community_analysis.get('engagement_metrics', {})
            )

            # Format key concerns with error handling
            key_concerns = self._format_key_concerns(
                community_analysis.get('key_concerns', [])
            )
            
            # Format incidents with error handling
            recent_incidents = self._format_incidents(
                community_analysis.get('recent_incidents', [])
            )

            template_vars = {
                'project_name': project_data.get('project_name', ''),
                'project_website': project_data.get('project_website', ''),
                'project_description': project_data.get('project_description', ''),
                'project_x_account': project_data.get('project_x_account', ''),
                'project_deck_url': project_data.get('project_deck_url', ''),
                'sentiment_score': community_analysis.get('sentiment_score', 0.0),
                'engagement_metrics': engagement_metrics,
                'key_concerns': key_concerns,
                'recent_incidents': recent_incidents,
                'risk_level': community_analysis.get('overall_risk_level', 'Unknown'),
                'analysis_period': community_analysis.get('analysis_period', 'Last 30 days'),
                'data_sources': ", ".join(community_analysis.get('data_sources', []))
            }

            return self.template.substitute(template_vars)
        except Exception as e:
            print(f"Error creating analysis prompt: {str(e)}")
            raise

    def _format_engagement_metrics(self, metrics: Dict) -> str:
        """Format engagement metrics with error handling"""
        try:
            return "\n".join([
                f"- {metric.replace('_', ' ').title()}: {value:.2f}"
                for metric, value in metrics.items()
            ])
        except Exception:
            return "No engagement metrics available"

    def _format_key_concerns(self, concerns: list) -> str:
        """Format key concerns with error handling"""
        try:
            return "\n".join([
                f"- {concern.get('category', 'Unknown')}: {concern.get('description', 'No description')}"
                for concern in concerns
            ])
        except Exception:
            return "No key concerns identified"

    def _format_incidents(self, incidents: list) -> str:
        """Format incidents with error handling"""
        try:
            return "\n".join([
                f"- {incident.get('date', 'Unknown')}: [{incident.get('severity', 'Unknown')}] "
                f"{incident.get('type', 'Unknown')} - {incident.get('description', 'No description')}"
                for incident in incidents
            ])
        except Exception:
            return "No recent incidents reported"
