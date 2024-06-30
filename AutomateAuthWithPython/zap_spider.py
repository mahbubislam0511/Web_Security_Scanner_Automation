from zapv2 import ZAPv2
import time

# Configure ZAP
zap_url = 'http://localhost:8084'
target_url = 'https://myforestchild.savethechildren.net'
api_key = 'mahbub0510'  # Set your API key if you have one

# Initialize the ZAP API
zap = ZAPv2(apikey=api_key, proxies={'http': zap_url, 'https': zap_url})

# Start spidering the target URL
print(f'Starting spider on {target_url}')
spider_id = zap.spider.scan(target_url)

# Poll the status until the spidering is complete
while int(zap.spider.status(spider_id)) < 100:
    print(f'Spider progress: {zap.spider.status(spider_id)}%')
    time.sleep(2)

print('Spidering completed')
# Give the passive scanner a chance to finish
time.sleep(10)

# Start active scanning
print(f'Starting active scan on {target_url}')
scan_id = zap.ascan.scan(target_url)

# Poll the status until scanning is complete
while int(zap.ascan.status(scan_id)) < 100:
    print(f'Scan progress: {zap.ascan.status(scan_id)}%')
    time.sleep(5)

print('Scanning completed')

# Generate an HTML report
report = zap.core.htmlreport()
with open('zap_report.html', 'w') as file:
    file.write(report)

print('HTML report generated as zap_report.html')
