import colorama

colorama.init(True)

BLUE = colorama.Fore.BLUE
CYAN = colorama.Fore.CYAN
GREEN = colorama.Fore.GREEN
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED

RESET = colorama.Style.RESET_ALL

def Alert(message):
    print(f"{YELLOW}[{RED}!{YELLOW}] {BLUE}{message}{RESET}")

def Succed(message):
    print(f"[{GREEN}+{RESET}] {CYAN}{message}{RESET}")

def info(message):
    print(f"[{BLUE}*{RESET}] {GREEN}{message}{RESET}")