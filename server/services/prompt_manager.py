import os
from string import Template

class PromptManager:
    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = os.getcwd()
        self.prompts_dir = os.path.join(base_dir, "prompts")
        print(f"Prompts directory: {self.prompts_dir}")  # Debug print
        
    def load_prompt(self, template_name: str) -> Template:
        """Load a prompt template from file"""
        template_path = os.path.join(self.prompts_dir, f"{template_name}.txt")
        print(f"Loading prompt from: {template_path}")  # Debug print
        
        try:
            with open(template_path, 'r') as file:
                template_content = file.read()
            return Template(template_content)
        except FileNotFoundError as e:
            print(f"Failed to load prompt: {str(e)}")  # Debug print
            raise FileNotFoundError(f"Prompt template '{template_name}' not found at {template_path}")
            
    def format_prompt(self, template_name: str, **kwargs) -> str:
        """Load and format a prompt template with given parameters"""
        template = self.load_prompt(template_name)
        return template.safe_substitute(**kwargs)
