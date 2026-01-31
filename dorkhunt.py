
---

# 🐍 `dorkhunt.py`

```python
#!/usr/bin/env python3
import argparse
import requests
import time

DUCKDUCKGO_URL = "https://duckduckgo.com/html/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

DORKS = [
    # Documents
    "ext:pdf", "ext:doc", "ext:docx", "ext:xls", "ext:xlsx",
    "ext:csv", "ext:txt", "ext:xml", "ext:json",

    # Backup & config
    "ext:bak", "ext:backup", "ext:old", "ext:conf",
    "ext:cfg", "ext:ini", "ext:env", "ext:log",

    # Database
    "ext:sql", "ext:db", "ext:sqlite",

    # Archives
    "ext:zip", "ext:rar", "ext:7z", "ext:tar", "ext:gz",

    # Web & panels
    'intitle:"index of"',
    "inurl:admin",
    "inurl:login",
    "inurl:dashboard",
    "inurl:api",
    "inurl:swagger",
    "inurl:graphql"
]

def search(dork):
    try:
        r = requests.post(DUCKDUCKGO_URL, data={"q": dork}, headers=HEADERS, timeout=15)
        return r.text
    except Exception as e:
        print(f"[!] Error: {e}")
        return ""

def extract_links(html):
    links = set()
    for line in html.splitlines():
        if "result__url" in line and "http" in line:
            try:
                url = line.split('href="')[1].split('"')[0]
                links.add(url)
            except:
                pass
    return links

def main():
    parser = argparse.ArgumentParser(
        description="Dork_Hunting - Automated Google Dork OSINT Tool"
    )
    parser.add_argument("-d", "--domain", required=True, help="Target domain (example.com)")
    parser.add_argument("-o", "--output", default="results.txt", help="Output file")
    args = parser.parse_args()

    print("\n[+] Dork_Hunting Started")
    print(f"[+] Target: {args.domain}\n")

    all_results = set()

    for dork in DORKS:
        query = f"site:{args.domain} {dork}"
        print(f"[+] Searching: {query}")
        html = search(query)
        results = extract_links(html)
        all_results.update(results)
        time.sleep(2)

    with open(args.output, "w") as f:
        for url in sorted(all_results):
            f.write(url + "\n")

    print(f"\n[+] Scan completed")
    print(f"[+] Found {len(all_results)} results")
    print(f"[+] Saved to {args.output}")

if __name__ == "__main__":
    main()


