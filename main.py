import os
import json
import requests
import colorama
from colorama import Fore
import ctypes

colorama.init()
os.system('mode con: cols=75 lines=18')
ctypes.windll.kernel32.SetConsoleTitleW('FiveM Server Info | Created by Ali')

def load_anti_cheat_names(filepath='./data/anticheat.txt'):
    """Load anti-cheat names from a file."""
    with open(filepath, 'r') as file:
        return [line.strip().lower() for line in file]

def sanitize_filename(filename):
    """Sanitize filenames by replacing invalid characters with underscores."""
    return ''.join(c if c.isalnum() or c in (' ', '_') else '_' for c in filename)

def save_json_data(filepath, data):
    """Save data to a JSON file."""
    os.makedirs('saved', exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_config(filepath='./data/config.json'):
    """Load configuration from a JSON file."""
    with open(filepath, 'r') as file:
        return json.load(file)

def fetch_fivem_server_info():
    """Fetch and display FiveM server information."""
    anti_cheat_names = load_anti_cheat_names()
    config = load_config()

    while True:
        server_cfx = input(f"{Fore.LIGHTYELLOW_EX}[{Fore.RESET}+{Fore.LIGHTYELLOW_EX}] Enter the server CFX: {Fore.RESET}")
        url = f"https://servers-frontend.fivem.net/api/servers/single/{server_cfx}"
        headers = {
            'accept': 'application/json',
            'accept-language': 'en',
            'user-agent': 'ios:2.65.0:488:14:iPhone13,3',
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json().get("Data", {})

            if not data:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"{Fore.LIGHTRED_EX}[{Fore.RESET}-{Fore.LIGHTRED_EX}] Error: Server data not found. Please try again.")
                continue

            ip = data.get("connectEndPoints", ["IP not found"])[0]
            name = data.get("hostname", "Server Name not found")
            players = data.get("clients", "Players count not found")
            boosts = data.get("upvotePower", "UpVotes not found")
            max_players = data.get("sv_maxclients", "Max Players not found")
            owner_name = data.get("ownerName", "Owner Name not found")

            found_anti_cheats = [anti_cheat for anti_cheat in anti_cheat_names if any(anti_cheat in str(value).lower() for value in data.values())]

            if config.get("save_cfx_json", False):
                filename = f"{sanitize_filename(server_cfx)}.json"
                save_json_data(os.path.join('saved', filename), data)

            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Server IP: {Fore.RESET}{ip}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Server Name: {Fore.RESET}{name}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Players: {Fore.RESET}{players}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] UpVotes: {Fore.RESET}{boosts}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Max Players: {Fore.RESET}{max_players}")
            print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}${Fore.LIGHTGREEN_EX}] Owner Name: {Fore.RESET}{owner_name}")

            if found_anti_cheats:
                print(f"{Fore.LIGHTRED_EX}[{Fore.RESET}!{Fore.LIGHTRED_EX}] Anti-Cheat Detected: {', '.join(found_anti_cheats)}")
            else:
                print(f"{Fore.LIGHTGREEN_EX}[{Fore.RESET}!{Fore.LIGHTGREEN_EX}] No Anti-Cheat Detected")

            break

        except requests.RequestException as e:
            print(f"{Fore.LIGHTRED_EX}[{Fore.RESET}-{Fore.LIGHTRED_EX}] Request error: {str(e)}. Please try again.")

    input(f"{Fore.LIGHTYELLOW_EX}Press Enter to exit...")

if __name__ == "__main__":
    fetch_fivem_server_info()