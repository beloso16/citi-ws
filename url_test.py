import requests

url = "https://sf.citidirect.com/stfin/docs/634288/CertStmtCMLT06AMC12301.pdf"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
}

response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Save the PDF content to a file
    with open('CertStmtCMLT06AMC12301.pdf', 'wb') as file:
        file.write(response.content)
else:
    print(f"Error: {response.status_code} - {response.text}")
