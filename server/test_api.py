import requests
import json
import os
from dotenv import load_dotenv
import urllib3
import ssl
from pathlib import Path
import aiohttp
import asyncio
from typing import Dict
from datetime import datetime

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://localhost:3443/api")

def make_request(method, endpoint, data=None, headers=None):
    try:
        full_url = f"{BASE_URL}/{endpoint}"
        response = requests.request(
            method,
            full_url,
            json=data,
            headers=headers,
            verify=False  # Allow self-signed certificates
        )
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Request to {full_url} failed: {str(e)}")
        raise Exception(f"Request failed: {str(e)}")

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

# SSL context for local development
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

class APITester:
    def __init__(self):
        self.base_url = "https://localhost:3443/api"
        self.timeout = aiohttp.ClientTimeout(total=120)
        self.test_projects = [
            {
                "project_name": "Uniswap",
                "project_website": "https://uniswap.org",
                "project_description": "Decentralized protocol for automated token exchange on Ethereum",
                "project_x_account": "@Uniswap",
                "project_deck_url": "https://uniswap.org/whitepaper-v3.pdf"
            }
        ]

    async def test_api(self):
        connector = aiohttp.TCPConnector(ssl=ssl_context, force_close=True)
        
        async with aiohttp.ClientSession(
            timeout=self.timeout,
            connector=connector
        ) as session:
            try:
                # Register user first
                register_data = {
                    "username": "test_user",
                    "email": "test@example.com",
                    "password": "test123!"
                }
                
                print("Attempting registration...")
                async with session.post(
                    f"{self.base_url}/auth/register",
                    json=register_data
                ) as response:
                    response_text = await response.text()
                    if response.status == 409:
                        print("User already exists, proceeding to login")
                    elif response.status in [200, 201]:
                        print("Registration successful")
                    else:
                        print(f"Registration failed with status {response.status}: {response_text}")
                        return

                # Then attempt login
                login_data = {
                    "username": "test_user",
                    "password": "test123!"
                }
                
                print("\nAttempting login...")
                async with session.post(
                    f"{self.base_url}/auth/login",
                    json=login_data
                ) as response:
                    if response.status != 200:
                        print(f"Login failed: {await response.text()}")
                        return
                    token = (await response.json())['token']
                    print("Login successful")

                # Test project analysis
                headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
                project_data = {
                    "project_name": "Test Project",
                    "project_website": "https://test.com",
                    "project_description": "A blockchain project focusing on DeFi solutions",
                    "project_x_account": "@testproject",
                    "project_deck_url": "https://test.com/deck"
                }
                
                print("\nStarting analysis...")
                start_time = datetime.now()
                
                async with session.post(
                    f"{self.base_url}/project/analyze",
                    headers=headers,
                    json=project_data,
                    raise_for_status=True
                ) as response:
                    result = await response.json()
                    print(result)
                    duration = (datetime.now() - start_time).total_seconds()
                    
                    print(f"\nAnalysis completed in {duration:.2f} seconds")
                    print("\nResult:")
                    print(json.dumps(result, indent=2))

            except aiohttp.ClientResponseError as e:
                print(f"\nAPI error: {e.status} - {e.message}")
            except aiohttp.ClientError as e:
                print(f"\nConnection error: {str(e)}")
            except asyncio.TimeoutError:
                print("\nRequest timed out")
            except Exception as e:
                print(f"\nTest failed with error: {str(e)}")
                raise
            finally:
                await connector.close()

def main():
    tester = APITester()
    asyncio.run(tester.test_api())

if __name__ == "__main__":
    main()
