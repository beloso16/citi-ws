from bs4 import BeautifulSoup
import pandas as pd
import os
import shutil
import re
import requests

# Replace 'your_html_file.html' with the actual path to your HTML file
html_file_path = 'view-source_https___sf.citidirect.com_stfin_ATS_DealServlet.html'

with open(html_file_path, 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

soup = BeautifulSoup(html_content, 'html.parser')

links = soup.find_all('a', href=True)

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
output_folder = '/Users/faustine/Desktop/trex_tech_exam/citi-ws/downloaded_files'
os.makedirs(output_folder, exist_ok=True)

for index, row in df.iterrows():
    chs_file = os.path.join(output_folder, row['CHS_file'])  # Full path for the downloaded file
    chs_link = 'http://' + row['CHS_link']
    print(chs_file)
    print(chs_link)

    response = requests.post(chs_link)

    if response.status_code == 200:
        # Save the file to the specified output folder
        with open(chs_file, "wb") as file:
            file.write(response.content)
        print(f"File downloaded successfully to: {chs_file}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


"""from bs4 import BeautifulSoup
import pandas as pd
import os
import shutil
import re
import requests

# Replace 'your_html_file.html' with the actual path to your HTML file
html_file_path = 'view-source_https___sf.citidirect.com_stfin_ATS_DealServlet.html'

with open(html_file_path, 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

soup = BeautifulSoup(html_content, 'html.parser')

links = soup.find_all('a', href=True)

# Extract text after 'href="' and ending with '.pdf'
pdf_links = [link['href'][link['href'].find('://') + 3:] for link in links if '.pdf' in link['href']]

filtered_links = [link for link in pdf_links if 'CertStmtCMLT06AMC'.lower() in link.lower()]

#print(filtered_links)
#print(len(pdf_links))
#print(len(filtered_links))

not_filtered_links = [link for link in pdf_links if link not in filtered_links]
#print(not_filtered_links)

df = pd.DataFrame(filtered_links, columns=['CHS_link'])

# Extract year and month from the 'CHS' column using regular expressions
df[['Year', 'Month']] = df['CHS_link'].str.extract(r'(\d{2})(\d{2})\.pdf$')

df['CHS_file'] = df['CHS_link'].apply(lambda x: re.sub('.*?(CertStmtCMLT06AMC)', r'\1', x, flags=re.IGNORECASE))

#df['Year'] = '20' + df['Year']

# Display the updated DataFrame
print(df)

df.to_csv('/Users/faustine/Desktop/trex_tech_exam/citi-ws/dataframe.csv', index=False)

# Create a folder to store downloaded files
output_folder = '/Users/faustine/Desktop/trex_tech_exam/citi-ws/downloaded_files'
os.makedirs(output_folder, exist_ok=True)

for index, row in df.iterrows():
    chs_file = os.path.join(output_folder, row['CHS_file'])  # Full path for the downloaded file
    chs_link = row['CHS_link']
    print(chs_file)
    print(chs_link)

    response = requests.get('http://'+chs_link)

    if response.status_code == 200:
        # Save the file to the specified output folder
        with open(chs_file, "wb") as file:
            file.write(response.content)
        print(f"File downloaded successfully to: {chs_file}")

        # Move the file to the output folder
        try:
            shutil.move(chs_file, os.path.join(output_folder, os.path.basename(chs_file)))
            print(f"File moved to: {os.path.join(output_folder, os.path.basename(chs_file))}")
        except Exception as e:
            print(f"Error moving file: {e}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")"""