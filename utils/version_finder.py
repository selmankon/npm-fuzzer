import re
import requests
from colorama import Fore, Style
from config.settings import DEBUG

# Regex for matching version numbers
version_regex = re.compile(r'[vV]?(ersion\s*)?([0-9]+\.[0-9]+(?:\.[0-9]+){0,2}(?:[-+][a-zA-Z0-9\.]+)?)')

def find_versions(url):
    try:
        response = requests.get(f"{url}/README.md", verify=False)
        response.raise_for_status()
        
        if DEBUG:
            print(f"{Fore.YELLOW}Debug: GET Response Status Code: {response.status_code}{Style.RESET_ALL}")
        
        content = response.text
        lines = content.splitlines()
        
        matches = version_regex.findall(content)
        versions = set()
        results = []
        
        for match in matches:
            version = match[1]
            position = content.find(version)
            line_number = next((i + 1 for i, line in enumerate(lines) if version in line), None)
            results.append((position, version, line_number, lines[line_number - 1] if line_number else ""))
            versions.add(version)
        
        if DEBUG:
            print(f"{Fore.YELLOW}Debug: Found Versions: {versions}{Style.RESET_ALL}")
        
        return versions, results
    except requests.RequestException as e:
        if DEBUG:
            print(f"{Fore.RED}Debug: Error fetching {url}: {e}{Style.RESET_ALL}")
        return set(), []
