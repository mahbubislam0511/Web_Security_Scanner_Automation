import requests
import time

ZAP_URL = 'http://localhost:8084'
API_KEY = 'mahbub0510'
CONTEXT_NAME = 'MyAppContext'
CONTEXT_ID = 1  # Adjust based on your context ID
USER_ID = 1  # Adjust based on your user ID

# Define endpoints
login_url = f'{ZAP_URL}/JSON/authentication/action/login'
spider_url = f'{ZAP_URL}/JSON/spider/action/scanAsUser/'
scan_url = f'{ZAP_URL}/JSON/ascan/action/scan'

# Login (this is optional if context is already authenticated)
login_payload = {
    'apikey': API_KEY,
    'contextId': CONTEXT_ID,
    'userId': USER_ID
}
requests.post(login_url, data=login_payload)

# Allow some time for login to complete
time.sleep(5)

# Start spidering
spider_payload = {
    'apikey': API_KEY,
    'contextName': CONTEXT_NAME,
    'userName': '123456789',  # Adjust based on your user
    'url': 'https://myforestchild.savethechildren.net/Account/LogIn',  # Replace with your target URL
    'maxChildren': 10
}
spider_response = requests.post(spider_url, data=spider_payload)
spider_scan_id = spider_response.json().get('scan')

# Monitor spider progress
status_url = f'{ZAP_URL}/JSON/spider/view/status/?scanId={spider_scan_id}'
while True:
    response = requests.get(status_url, params={'apikey': API_KEY})
    status = response.json().get('status')
    print(f'Spider progress: {status}%')
    if status == '100':
        break
    time.sleep(10)

print('Spidering complete')

# Start active scan
scan_payload = {
    'apikey': API_KEY,
    'contextId': CONTEXT_ID,
    'recurse': True
}
scan_response = requests.post(scan_url, data=scan_payload)
scan_id = scan_response.json().get('scan')

# Monitor scan progress
status_url = f'{ZAP_URL}/JSON/ascan/view/status/?scanId={scan_id}'
while True:
    response = requests.get(status_url, params={'apikey': API_KEY})
    status = response.json().get('status')
    print(f'Scan progress: {status}%')
    if status == '100':
        break
    time.sleep(10)

print('Scan complete')

# Fetching the results
results_url = f'{ZAP_URL}/JSON/core/view/alerts'
response = requests.get(results_url, params={'apikey': API_KEY})
alerts = response.json().get('alerts')
print(alerts)