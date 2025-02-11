import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:3000/api"

def get_auth_token(username: str, password: str) -> str:
    """Get authentication token by logging in"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": username, "password": password}
    )
    if response.status_code != 200:
        raise Exception(f"Login failed: {response.json().get('message')}")
    return response.json()['token']

def register_user(username: str, password: str):
    """Register a new user"""
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"username": username, "password": password}
    )
    if response.status_code != 201:
        print(f"Registration failed: {response.json().get('message')}")
    return response.status_code == 201

def test_analyze_project():
    # Test credentials
    username = "testuser"
    password = "testpass123"
    
    # Try to register (ignore if already exists)
    register_user(username, password)
    
    # Get authentication token
    token = get_auth_token(username, password)
    
    # Project analysis request
    url = f"{BASE_URL}/project/analyze"
    
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
    
    response = requests.post(url, json=data, headers=headers)
    
    print("Status Code:", response.status_code)
    print("\nResponse:")
    try:
        print(json.dumps(response.json(), indent=2))
    except json.JSONDecodeError:
        print("Raw response text:")
        print(response.text)

if __name__ == "__main__":
    test_analyze_project()
