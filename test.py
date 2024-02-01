from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import ws_functions

#download_folder = str(input("download folder: "))
# Replace 'your_html_file.html' with the actual path to your HTML file
html_file_path = 'view-source_https___sf.citidirect.com_stfin_ATS_DealServlet.html'

with open(html_file_path, 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

soup = BeautifulSoup(html_content, 'html.parser')

links = soup.find_all('a', href=True)
print(links)

# Extract text after 'href="' and ending with '.pdf'
file_extensions = ['.pdf', '.csv']
links = [link['href'][link['href'].find('://') + 3:] for link in links if any(link['href'].endswith(ext) for ext in file_extensions)]

# chs link if starts with CertStmtCMLT06AMC and is pdf
filtered_chs_links = [link for link in links if 'CertStmtCMLT06AMC'.lower() in link.lower() and link.lower().endswith('.pdf')]

df = pd.DataFrame(filtered_chs_links, columns=['link'])
df['type'] = 'chs'
df['file'] = df['link'].apply(lambda x: re.sub('.*?(CertStmtCMLT06AMC)', r'\1', x, flags=re.IGNORECASE))
df[['year', 'month']] = df['link'].str.extract(r'(\d{2})(\d{2})\.pdf$')

# ellt link if starts with LoanDetailCMLT06AMC and is csv
filtered_ellt_links = [link for link in links if 'LoanDetailCMLT06AMC'.lower() in link.lower() and link.lower().endswith('.csv')]
ellt_df = pd.DataFrame(filtered_ellt_links, columns=['link'])
ellt_df['type'] = 'ellt'
ellt_df['file'] = ellt_df['link'].apply(lambda x: re.sub('.*?(LoanDetailCMLT06AMC)', r'\1', x, flags=re.IGNORECASE))
ellt_df[['year', 'month']] = ellt_df['link'].str.extract(r'(\d{2})(\d{2})\.csv$')

# lld link if ColExtCMLT06AMC and ends with csv
filtered_lld_links = [link for link in links if 'ColExtCMLT06AMC'.lower() in link.lower() and link.lower().endswith('.csv')]
lld_df = pd.DataFrame(filtered_lld_links, columns=['link'])
lld_df['type'] = 'lld'
lld_df['file'] = lld_df['link'].apply(lambda x: re.sub('.*?(ColExtCMLT06AMC)', r'\1', x, flags=re.IGNORECASE))
lld_df[['year', 'month']] = lld_df['link'].str.extract(r'(\d{2})(\d{2})\.csv$')

# combine all in the original dataframe
df = pd.concat([df, ellt_df, lld_df], ignore_index=True)

# Extract year and month from the 'link' column using regular expressions


# Display the updated DataFrame
print(df)


# Create a folder to store downloaded files
output_folder = '/Users/faustine/Desktop/trex_tech_exam/citi-ws/downloaded_files/'
os.makedirs(output_folder, exist_ok=True)
############################################################################################################################################################################ FILE DOWNLOAD

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
}

#download all CHS files
#ws_functions.download_files(df[df['type'] == 'chs'].to_dict('records'), output_folder, headers, file_type='chs')

#download all 
df['total_principal_funds'] = ''

# Iterate over 'chs' rows in the DataFrame
for index, row in df[df['type'] == 'chs'].iterrows():
    file_path = output_folder + row['file']
    total_principal_funds = ws_functions.extract_principal_funds(file_path)

    # Assign the extracted value to the 'total_principal_funds' column
    df.at[index, 'total_principal_funds'] = total_principal_funds


print(df)
df.to_csv('/Users/faustine/Desktop/trex_tech_exam/citi-ws/dataframe.csv', index=False)
