import requests
import json
import os
from dotenv import load_dotenv
import urllib3

# Disable SSL warnings (only for testing with self-signed certificates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

# Update base URLs to use port 3443 for HTTPS
BASE_URL = os.getenv("BASE_URL", "https://localhost:3443/api")
FALLBACK_URL = "http://localhost:3000/api"  # HTTP fallback

def make_request(method, endpoint, data=None, headers=None):
    urls = [BASE_URL, FALLBACK_URL]
    for url in urls:
        try:
            full_url = f"{url}/{endpoint}"
            response = requests.request(
                method,
                full_url,
                json=data,
                headers=headers,
                verify=False  # Disable SSL verification (only for testing)
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Request to {url} failed: {str(e)}")
    raise Exception("All connection attempts failed")

def get_auth_token(username: str, password: str) -> str:
    """Get authentication token by logging in"""
    try:
        response = make_request("POST", "auth/login", data={"username": username, "password": password})
        return response.json()['token']
    except Exception as e:
        print(f"Login failed: {str(e)}")
        raise

def register_user(username: str, password: str):
    """Register a new user"""
    try:
        response = make_request("POST", "auth/register", data={"username": username, "password": password})
        print("User registered successfully")
        return True
    except Exception as e:
        print(f"Registration failed: {str(e)}")
        return False

def test_analyze_project():
    # Test credentials
    username = "testuser"
    password = "testpass123"
    
    # Try to register (ignore if already exists)
    register_user(username, password)
    
    try:
        # Get authentication token
        token = get_auth_token(username, password)
        
        # Project analysis request
        data = {
            "project_name": "PancakeSwap",
            "project_website": "https://pancakeswap.finance",
            "project_description": "PancakeSwap is a decentralized exchange running on Binance Smart Chain, with lots of other features that let you earn and win tokens.",
            "project_x_account": "@pancakeswap",
            "project_deck_url": "https://docs.pancakeswap.finance"
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        response = make_request("POST", "project/analyze", data=data, headers=headers)
        
        print("Status Code:", response.status_code)
        print("\nResponse:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error during API request: {str(e)}")

if __name__ == "__main__":
    test_analyze_project()
