import argparse
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.url_checker import process_path
from utils.version_finder import find_versions
from utils.screen_utils import clear_screen_with_results
from config.settings import DEBUG, banner
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

def main():
    parser = argparse.ArgumentParser(description='Check npm paths and find versions.')
    parser.add_argument('--url', type=str, required=True, help='Base URL of the JavaScript folder')
    parser.add_argument('-t', '--threads', type=int, default=4, help='Number of threads to use for scanning')
    parser.add_argument('-w', '--wordlist', type=str, required=True, help='Path to the wordlist file')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    base_url = args.url
    num_threads = args.threads
    wordlist_path = args.wordlist
    global DEBUG
    DEBUG = args.debug

    all_results = {}
    path_results = {}
    found_urls = set()

    try:
        with open(wordlist_path) as file:
            paths = file.read().splitlines()
            total_paths = len(paths)
            
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = {executor.submit(process_path, base_url, path): path for path in paths}
                for index, future in enumerate(as_completed(futures)):
                    result = future.result()
                    
                    if result:
                        full_url = result
                        versions, version_details = find_versions(full_url)
                        if versions:
                            found_urls.add(full_url)
                            path_results[full_url] = (versions, version_details)
                            all_results[full_url] = version_details
                            results = [f"{Fore.YELLOW}[Position: {position}]: {version}{Style.RESET_ALL}\n   Line number: {line_number}\n   Line content: {line_content}" for position, version, line_number, line_content in version_details]
                            clear_screen_with_results(
                                f"{banner}\n{Fore.BLUE}[+] Scanning libraries... [{index + 1}/{total_paths}]{Style.RESET_ALL}",
                                results,
                                found_urls,
                                all_results
                            )
                    
                    if (index + 1) % 100 == 0 or index + 1 == total_paths:
                        results = [f"{Fore.YELLOW}[Position: {position}]: {version}{Style.RESET_ALL}\n   Line number: {line_number}\n   Line content: {line_content}" for position, version, line_number, line_content in version_details]
                        clear_screen_with_results(
                            f"{banner}\n{Fore.BLUE}[+] Scanning libraries... [{index + 1}/{total_paths}]{Style.RESET_ALL}",
                            results,
                            found_urls,
                            all_results
                        )

    except Exception as e:
        print(f"{Fore.RED}Error reading paths file: {e}{Style.RESET_ALL}")

    print(f"{Fore.BLUE}[+] All Results:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}URL\t\tVersions{Style.RESET_ALL}")
    for url, (versions, details) in path_results.items():
        print(f"{url}\t{', '.join(versions)}")

if __name__ == "__main__":
    main()
