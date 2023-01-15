import socket
import json
import whois
import requests
import subprocess
import os

# Define the target domain
domain = "domain.com"

# Create a directory to store the gathered information
if not os.path.exists(domain):
    os.mkdir(domain)

# Gather DNS information
print("Gathering DNS information for {}...".format(domain))
ip_address = socket.gethostbyname(domain)
print("IP address: {}".format(ip_address))
with open(f'{domain}/dns_info.txt', 'w') as f:
    f.write(f'IP address: {ip_address}')

# Gather WHOIS information
print("Gathering WHOIS information for {}...".format(domain))
whois_info = whois.whois(domain)
print("Registrar: {}".format(whois_info.registrar))
print("Creation date: {}".format(whois_info.creation_date))
with open(f'{domain}/whois_info.txt', 'w') as f:
    f.write(f'Registrar: {whois_info.registrar}\nCreation date: {whois_info.creation_date}')

# Gather publicly available information
print("Gathering publicly available information for {}...".format(domain))
webpage = requests.get("http://" + domain)
print("Webpage status code: {}".format(webpage.status_code))
print("Webpage headers: {}".format(webpage.headers))
with open(f'{domain}/webpage_info.txt', 'w') as f:
    f.write(f'Webpage status code: {webpage.status_code}\nWebpage headers: {webpage.headers}')

# Gather passive reconnaissance information
print("Gathering passive reconnaissance information for {}...".format(domain))
shodan_info = requests.get("https://api.shodan.io/shodan/host/{}?key=YOUR_API_KEY".format(domain)).json()
print("Shodan information: {}".format(json.dumps(shodan_info, indent=2)))
with open(f'{domain}/shodan_info.txt', 'w') as f:
    f.write(json.dumps(shodan_info, indent=2))

# Perform port scan
print("Performing port scan for {}...".format(domain))
port_scan = subprocess.run(["nmap", "-sS", "-sV", "-p-", domain], capture_output=True)
with open(f'{domain}/nmap_scan.txt', 'w') as f:
    f.write(port_scan.stdout.decode())

# Perform directory enumeration
print("Performing directory enumeration for {}...".format(domain))
dirb_scan = subprocess.run(["dirb", "http://"+domain], capture_output=True)
with open(f'{domain}/dirb_scan.txt', 'w') as f:
    f.write(dirb_scan.stdout.decode())

# Check for SQL injection vulnerabilities
print("Checking for SQL injection vulnerabilities for {}...".format(domain))
sqlmap_scan = subprocess.run(["sqlmap", "-u", "http://"+domain+"/index.php?id=1", "--batch"], capture_output=True)
with open(f'{domain}/sqlmap_scan.txt', 'w') as f:
    f.write(sqlmap_scan.stdout.decode())

# Perform web server and application audit
print("Performing web server and application audit for {}...".format(domain))
nikto_scan = subprocess.run(["nikto", "-h", domain], capture_output=True)
with open(f'{domain}/nikto_scan.txt', 'w') as

# Perform web server and application audit
print("Performing web server and application audit for {}...".format(domain))
nikto_scan = subprocess.run(["nikto", "-h", domain], capture_output=True)
with open(f'{domain}/nikto_scan.txt', 'w') as f:
    f.write(nikto_scan.stdout.decode())

# Check SSL Configuration
print("Checking SSL Configuration for {}...".format(domain))
sslscan_scan = subprocess.run(["sslscan", domain], capture_output=True)
with open(f'{domain}/sslscan_scan.txt', 'w') as f:
    f.write(sslscan_scan.stdout.decode())

# Check SSL Configuration
print("Checking SSL Configuration for {}...".format(domain))
testssl_scan = subprocess.run(["testssl.sh", domain], capture_output=True)
with open(f'{domain}/testssl_scan.txt', 'w') as f:
    f.write(testssl_scan.stdout.decode())
    
# Visualizing the results
print("Script finished!")
print("Results are available in the {} directory".format(domain))
