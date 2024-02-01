from bs4 import BeautifulSoup
import requests
import re
import os

# Replace 'your_html_file.html' with the actual path to your HTML file
html_file_path = 'view-source_https___sf.citidirect.com_stfin_ATS_DealServlet.html'

with open(html_file_path, 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Find all 'A' tags with class 'nodec1bold' and href attribute matching the pattern
# Find all 'A' tags with class 'nodec1bold' and href attribute pointing to PDF files
links = soup.find_all('a', class_='nodec1bold', href=re.compile(r'\.pdf$'))

# ... rest of the script remains unchanged

# Create a folder to store downloaded files
output_folder = 'downloaded_files'
os.makedirs(output_folder, exist_ok=True)

for i in df['CHS_file']:
    print(i)
"""
# Build the path for the downloaded file within the output folder
file_name = os.path.join(output_folder, "downloaded_file.zip")

# Download the file
response = requests.get(url)

if response.status_code == 200:
    # Save the file to the specified output folder
    with open(file_name, "wb") as file:
        file.write(response.content)
    print(f"File downloaded successfully to: {file_name}")
else:
    print(f"Failed to download file. Status code: {response.status_code}")
"""