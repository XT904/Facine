import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init

init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def chttp(ip_str, tfind):
    try:
        curl = "http://" + ip_str
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51'}
        r = requests.get(curl, verify=False, timeout=1, headers=headers)
        listed = []
        if not r.status_code in [404, 403, 500]:
            for ftexts in tfind:
                if ftexts in r.text:
                    listed.append(ftexts)
            for ftexts in tfind:
                if ftexts in listed:
                    print(Fore.GREEN + f"       [+] {ip_str} ~ Text: {listed} \r")
                    with open('listed/live.txt', '+a') as f:
                        f.write(f"[+] {ip_str} ~ Text: {listed} \n")
                    return
                else:
                    print(Fore.YELLOW + f"       [-] {ip_str}\r")
                    return
        else:
            print(Fore.RED + f"       [OFFLINE] {ip_str}\r")
            return
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"       [OFFLINE] {ip_str}\r")
        return

def ip_range(IPA, IPS, tfind):
    executor = ThreadPoolExecutor(max_workers=5)  # Define o número máximo de threads
    start_octets = list(map(int, IPA.split('.')))
    end_octets = list(map(int, IPS.split('.')))
    start = start_octets[0] * 256**3 + start_octets[1] * 256**2 + start_octets[2] * 256 + start_octets[3]
    end = end_octets[0] * 256**3 + end_octets[1] * 256**2 + end_octets[2] * 256 + end_octets[3]

    for ip_num in range(start, end + 1):
        octetos = [(ip_num >> i) & 255 for i in (24, 16, 8, 0)]
        ip_str = '.'.join(map(str, octetos))
        executor.submit(chttp, ip_str, tfind)

if __name__ == "__main__":
    print(Fore.RED + f"""
    ▪               ·
   ▄█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄██▄
  ███    ███   █████╗  ██████╗██╗███╗   ██╗███████╗          .    ▀█
  ███    █▀   ██╔══██╗██╔════╝██║████╗  ██║██╔════╝ ▪
 ▄███▄▄▄   ▪  ███████║██║  .  ██║██╔██╗ ██║█████╗              ▪
▀▀███▀▀▀      ██╔══██║██║     ██║██║╚██╗██║██╔══╝      ▪
  ███         ██║  ██║╚██████╗██║██║ ╚████║███████╗ 
  ███   .     ╚═╝  ╚═╝ ╚═════╝╚═╝╚═╝  ╚═══╝╚══════╝ .
  ███          .                ▪
    █        
         ░▒▓█| Exemple: php css html
         ░▒▓█| Supports multiple keywords
""")
    th6 = input(Fore.LIGHTRED_EX + " [THREADS]: ")
    IPA = input(Fore.LIGHTRED_EX + " [IP-START]: ")
    IPS = input(Fore.LIGHTRED_EX + " [IP-STOP]: ")
    r = input(Fore.LIGHTRED_EX + " [KEYWORD]: ")
    tfind = r.split()
    ip_range(IPA, IPS, tfind)
