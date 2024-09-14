import os
from colorama import Fore, Style

def clear_screen_with_results(header, results, found_urls, all_results):
    os.system('clear')
    print(header)
    for url in found_urls:
        print(f"{Fore.GREEN}[+] {url}{Style.RESET_ALL}")
    
    print(f"{Fore.BLUE}\nPreviously found versions:{Style.RESET_ALL}")
    for url, details in all_results.items():
        print(f"{Fore.YELLOW}{url}:{Style.RESET_ALL}")
        for position, version, line_number, line_content in details:
            print(f"  [Position: {position}]: {version}\n   Line number: {line_number}\n   Line content: {line_content}")

    print("\n" + "\n".join(results))
