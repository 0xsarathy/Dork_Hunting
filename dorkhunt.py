#!/usr/bin/env python3
import argparse
import requests

EXTENSIONS = [
    "doc","docx","odt","pdf","rtf","ppt","pptx","csv",
    "xls","xlsx","txt","xml","json","zip","rar",
    "md","log","bak","conf","sql"
]

DUCKDUCKGO_API = "https://duckduckgo.com/html/"

def build_dork(domain, extensions):
    ext_query = " OR ".join([f"ext:{e}" for e in extensions])
    return f"site:*.{domain} ({ext_query})"

def search(dork):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.post(DUCKDUCKGO_API, data={"q": dork}, headers=headers, timeout=15)
    return r.text

def extract_links(html):
    results = []
    for line in html.splitlines():
        if "result__url" in line and "http" in line:
            try:
                url = line.split('href="')[1].split('"')[0]
                results.append(url)
            except:
                pass
    return list(set(results))

def main():
    parser = argparse.ArgumentParser(
        description="DorkHunt - Public document & sensitive file finder using dorks"
    )
    parser.add_argument("-d", "--domain", required=True, help="Target domain (example.com)")
    parser.add_argument("-o", "--output", default="dorkhunt_results.txt", help="Output file")
    args = parser.parse_args()

    dork = build_dork(args.domain, EXTENSIONS)
    print(f"[+] Dork used:\n{dork}\n")

    html = search(dork)
    links = extract_links(html)

    with open(args.output, "w") as f:
        for link in links:
            f.write(link + "\n")

    print(f"[+] Found {len(links)} exposed files")
    print(f"[+] Results saved to {args.output}")

if __name__ == "__main__":
    main()

