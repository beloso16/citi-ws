from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import requests

download_folder = str(input("download folder: "))
# Replace 'your_html_file.html' with the actual path to your HTML file
html_file_path = 'view-source_https___sf.citidirect.com_stfin_ATS_DealServlet.html'

with open(html_file_path, 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

soup = BeautifulSoup(html_content, 'html.parser')

links = soup.find_all('a', href=True)
print(links)

# Extract text after 'href="' and ending with '.pdf'
pdf_links = [link['href'][link['href'].find('://') + 3:] for link in links if '.pdf' in link['href']]

filtered_links = [link for link in pdf_links if 'CertStmtCMLT06AMC'.lower() in link.lower()]

df = pd.DataFrame(filtered_links, columns=['CHS_link'])

# Extract year and month from the 'CHS' column using regular expressions
df[['Year', 'Month']] = df['CHS_link'].str.extract(r'(\d{2})(\d{2})\.pdf$')

df['CHS_file'] = df['CHS_link'].apply(lambda x: re.sub('.*?(CertStmtCMLT06AMC)', r'\1', x, flags=re.IGNORECASE))

# Display the updated DataFrame
print(df)

df.to_csv('/Users/faustine/Desktop/trex_tech_exam/citi-ws/dataframe.csv', index=False)

# Create a folder to store downloaded files
output_folder = '/Users/faustine/Desktop/trex_tech_exam/citi-ws/downloaded_files/'+download_folder
os.makedirs(output_folder, exist_ok=True)
############################################################################################################################################################################CHS FILE DOWNLOAD
#download all CHS files
"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
}

for index, row in df.iterrows():
    chs_file = os.path.join(output_folder, row['CHS_file'])  # Full path for the downloaded file
    chs_link = 'https://' + row['CHS_link']
    print(chs_file)
    print(chs_link)

    response = requests.get(chs_link, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Create the download folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Save the PDF content to a file in the specified folder
        pdf_path = os.path.join(output_folder, row['CHS_file'])
        with open(pdf_path, 'wb') as file:
            file.write(response.content)

        print(f"PDF downloaded to {pdf_path}")
    else:
        print(f"Error: {response.status_code} - {response.text}")
###################################################################
        ###################################################
"""