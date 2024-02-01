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

# Download the pdf files
for link in links:
    pdf_url = link['href']
    print(pdf_url)
    pdf_filename = os.path.join(output_folder, pdf_url.split('/')[-1])
    response = requests.get("https://sf.citidirect.com"+pdf_url)
    
    with open(pdf_filename, 'wb') as pdf_file:
        pdf_file.write(response.content)

    print(f'Downloaded: {pdf_filename}')
