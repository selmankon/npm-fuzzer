import requests
from colorama import Fore, Style
from config.settings import DEBUG
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_path_exists(base_url, path):
    try:
        if base_url.endswith('/'):
            url = f"{base_url}{path.lstrip('/')}"
        else:
            url = f"{base_url}/{path.lstrip('/')}"
        
        if DEBUG:
            print(f"{Fore.YELLOW}Debug: Checking URL: {url}{Style.RESET_ALL}")
        
        response = requests.head(url, verify=False)
        status_code = response.status_code
        
        if DEBUG:
            print(f"{Fore.YELLOW}Debug: HEAD Response Status Code: {status_code}{Style.RESET_ALL}")
        
        return status_code != 404
    except requests.RequestException as e:
        if DEBUG:
            print(f"{Fore.RED}Debug: Error checking URL {url}: {e}{Style.RESET_ALL}")
        return False

def process_path(base_url, path):
    if check_path_exists(base_url, path):
        full_url = f"{base_url}/{path.lstrip('/')}" if not base_url.endswith('/') else f"{base_url}{path.lstrip('/')}"
        if DEBUG:
            print(f"{Fore.YELLOW}Debug: Full URL: {full_url}{Style.RESET_ALL}")
        return full_url
    return None
