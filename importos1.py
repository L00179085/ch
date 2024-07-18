from dotenv import load_dotenv
import os
import requests
from requests.auth import HTTPBasicAuth
import json

# Load environment variables from .env file if present
load_dotenv()

# Jira credentials and URL from environment variables
JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
PROJECT_KEY = os.getenv("PROJECT_KEY")

# Check if environment variables are loaded correctly
if not all([JIRA_URL, JIRA_USER, JIRA_API_TOKEN, PROJECT_KEY]):
    print("Environment variables not set correctly.")
    print(f"JIRA_URL: {JIRA_URL}")
    print(f"JIRA_USER: {JIRA_USER}")
    print(f"JIRA_API_TOKEN: {JIRA_API_TOKEN}")
    print(f"PROJECT_KEY: {PROJECT_KEY}")
    exit(1)

# Jira API endpoint for searching issues in a project
search_url = f"{JIRA_URL}/rest/api/3/search"

# Query to search for all issues in the project
query = {
    "jql": f"project = {PROJECT_KEY}",
    "fields": ["key", "status"]
}

# Headers for the request
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Make the API request to search for issues in the project
response = requests.post(search_url, headers=headers, data=json.dumps(query), auth=HTTPBasicAuth(JIRA_USER, JIRA_API_TOKEN))

if response.status_code == 200:
    issues_data = response.json()
    issues = issues_data.get('issues', [])

    # Loop through each issue and print its key and status
    for issue in issues:
        issue_key = issue['key']
        issue_status = issue['fields']['status']['name']
        print(f"The status of issue {issue_key} is: {issue_status}")
else:
    print(f"Failed to retrieve issues: {response.status_code}, {response.text}")
