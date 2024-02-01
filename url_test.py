import requests

url = 'https://example.com'

response = requests.get(url)

if response.status_code == 200:
    print(f"Success! Status code: {response.status_code}")
    # Further processing if needed
else:
    print(f"Failed. Status code: {response.status_code}")
    # Handle the failure, check response.text for details if needed
