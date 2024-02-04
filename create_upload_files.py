from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import ws_functions

#download_folder = str(input("download folder: "))
html_file_path = 'view-source_https___sf.citidirect.com_stfin_ATS_DealServlet.html'

with open(html_file_path, 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

soup = BeautifulSoup(html_content, 'html.parser')

links = soup.find_all('a', href=True)

#extract all links
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

df['month_year'] = '20'+df['year']+df['month']

#print(df)


# folder to store downloaded files
output_folder = '/Users/faustine/Desktop/trex_tech_exam/citi-ws/downloaded_files/'
os.makedirs(output_folder, exist_ok=True)
############################################################################################################################################################################ FILE DOWNLOAD
###### DOWNLOAD CHS FILES

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
}

#download all CHS files - Certificate Holders Statement
ws_functions.download_files(df[df['type'] == 'chs'].to_dict('records'), output_folder+"raw_chs_files", headers, file_type='chs')

############################################################################################################################################################################ FILE DOWNLOAD
######## EXTRACT PRINCIPAL FUNDS
#get total principal funds
for index, row in df[df['type'] == 'chs'].iterrows():
    file_path = output_folder + row['file']
    total_principal_funds = ws_functions.extract_fund_value(file_path, "Total Principal Funds Available:", "Other Funds Available")
    df.at[index, 'total_principal_funds'] = total_principal_funds

#save the chs results as csv
chs_df = df[df['type'] == 'chs'][['file', 'link', 'month_year', 'total_principal_funds']]
print(chs_df)
chs_df.to_csv('/Users/faustine/Desktop/trex_tech_exam/citi-ws/downloaded_files/chs_df.csv', index=False)


############################################################################################################################################################################ FILE DOWNLOAD
###### DOWNLOAD ELLT FILES
ws_functions.download_files(df[df['type'] == 'ellt'].to_dict('records'), output_folder+"raw_ellt_files", headers, citi_file_type='ellt')

############################################################################################################################################################################ FILE DOWNLOAD
###### DOWNLOAD LLD FILES
ws_functions.download_files(df[df['type'] == 'lld'].to_dict('records'), output_folder+"raw_lld_files"+"raw_lld_files", headers, citi_file_type='lld')
