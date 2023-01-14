import requests
import re
from concurrent.futures import ThreadPoolExecutor

# set the target URL
url = "http://target.com"

# fetch historical HTML content from Wayback Machine
timestamp = "20200101000000" # timestamp in the format YYYYMMDDHHMMSS
wayback_url = f"http://archive.org/wayback/available?url={url}&timestamp={timestamp}"
response = requests.get(wayback_url)
data = response.json()
if "archived_snapshots" in data:
    if "closest" in data["archived_snapshots"]:
        if "url" in data["archived_snapshots"]["closest"]:
            wayback_url = data["archived_snapshots"]["closest"]["url"]
            response = requests.get(wayback_url)
            html_content = response.text
else:
    print("URL not found in archive.")

def get_domains(html_content):
    try:
        # use regular expression to extract all domains from the HTML content
        domains = re.findall(r'(?:https?://)?(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+(?:[a-zA-Z]{2,6})', html_content)
        return domains
    except:
        return None

with ThreadPoolExecutor() as executor:
    result = executor.submit(get_domains, html_content)
    domains = result.result()
    if domains:
        with open("external_domains.txt", "w") as file:
            for domain in domains:
                file.write(domain + "\n")
        print(f"{len(domains)} external domains saved to external_domains.txt")
    else:
        print("An error occured or no external domains found.")
