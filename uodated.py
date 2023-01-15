import threading
import os
import socket
import json
import whois
import requests
import subprocess

# Define the target domain
domain = "domain.com"

# Create a directory to store the gathered information
if not os.path.exists(domain):
    os.mkdir(domain)

# Create a cache for the Shodan API
shodan_cache = {}

def gather_dns_info():
    # Gather DNS information
    print("Gathering DNS information for {}...".format(domain))
    ip_address = socket.gethostbyname(domain)
    print("IP address: {}".format(ip_address))
    with open(f'{domain}/dns_info.txt', 'w') as f:
        f.write(f'IP address: {ip_address}')

def gather_whois_info():
    # Gather WHOIS information
    print("Gathering WHOIS information for {}...".format(domain))
    whois_info = whois.whois(domain)
    print("Registrar: {}".format(whois_info.registrar))
    print("Creation date: {}".format(whois_info.creation_date))
    with open(f'{domain}/whois_info.txt', 'w') as f:
        f.write(f'Registrar: {whois_info.registrar}\nCreation date: {whois_info.creation_date}')

def gather_public_info():
    # Gather publicly available information
    print("Gathering publicly available information for {}...".format(domain))
    webpage = requests.get("http://" + domain)
    print("Webpage status code: {}".format(webpage.status_code))
    print("Webpage headers: {}".format(webpage.headers))
    with open(f'{domain}/webpage_info.txt', 'w') as f:
        f.write(f'Webpage status code: {webpage.status_code}\nWebpage headers: {webpage.headers}')

def gather_passive_recon():
    # Gather passive reconnaissance information
    print("Gathering passive reconnaissance information for {}...".format(domain))
    if domain in shodan_cache:
        shodan_info = shodan_cache[domain]
    else:
        shodan_info = requests.get("https://api.shodan.io/shodan/host/{}?key=YOUR_API_KEY".format(domain)).json()
        shodan_cache[domain] = shodan_info
    print("Shodan information: {}".format(json.dumps(shodan_info, indent=2)))
    with open(f'{domain}/shodan_info.txt', 'w') as f:
        f.write(json.dumps(shodan_info, indent=2))

def port_scan():
    # Perform port scan
    print("Performing port scan for {}...".format(domain))
    port_scan = subprocess.run(["nmap", "-sS", "-sV", "-p-", domain], capture_output=True)
    with open(f'{domain}/nmap_scan.txt', 'w') as f:
        f.write(port_scan.stdout.decode())

def directory_enum():
    # Perform directory enumeration
    print("Performing directory enumeration for {}...".format(domain))
    dirb_scan = subprocess.run(["dirb", "http://"+domain], capture_output=True)
    with open(f'{domain}/dirb_scan.txt', 'w') as f:
        f.write(dirb_scan.stdout.decode())

def sql_vuln_scan():
    # Check for SQL injection vulnerabilities
    print("Checking for SQL injection vulnerabilities for {}...".format(domain))
    sqlmap_scan = subprocess.run(["sqlmap", "-u", "http://"+domain+"/index.php?id=1", "--batch"], capture_output=True)
    with open(f'{domain}/sqlmap_scan.txt', 'w') as f:
        f.write(sqlmap_scan.stdout.decode())

def web_server_audit():
    # Perform web server and application audit
    print("Performing web server and application audit for {}...".format(domain))
    nikto_scan = subprocess.run(["nikto", "-h", domain], capture_output=True)
    with open(f'{domain}/nikto_scan.txt', 'w') as f:
        f.write(nikto_scan.stdout.decode())

def check_ssl_config():
    # Check SSL Configuration
    print("Checking SSL Configuration for {}...".format(domain))
    sslscan_scan = subprocess.run(["sslscan", domain], capture_output=True)
    with open(f'{domain}/sslscan_scan.txt', 'w') as f:
        f.write(sslscan_scan.stdout.decode())

    print("Checking SSL Configuration for {}...".format(domain))
    testssl_scan = subprocess.run(["testssl.sh", domain], capture_output=True)
    with open(f'{domain}/testssl_scan.txt', 'w') as f:
        f.write(testssl_scan.stdout.decode())

# Create threads
dns_thread = threading.Thread(target=gather_dns_info)
whois_thread = threading.Thread(target=gather_whois_info)
public_thread = threading.Thread(target=gather_public_info)
passive_thread = threading.Thread(target=gather_passive_recon)
port_thread = threading.Thread(target=port_scan)
dir_thread = threading.Thread(target=directory_enum)
sql_thread = threading.Thread(target=sql_vuln_scan)
web_thread = threading.Thread(target=web_server_audit)
ssl_thread = threading.Thread(target=check_ssl_config)

# Start threads
dns_thread.start()
whois_thread.start()
public_thread.start()
passive_thread.start()
port_thread.start()
dir_thread.start()
sql_thread.start()
web_thread.start()
ssl_thread.start()

# Wait for threads to finish
dns_thread.join()
whois_thread.join()
public_thread.join()
passive_thread.join()
port_thread.join()
dir_thread.join()
sql_thread.join()
web_thread.join()
ssl_thread.join()

# Visualizing the results
print("Script finished!")
print("Results are available in the {} directory".format(domain))



