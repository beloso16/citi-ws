import fitz  # PyMuPDF
import os
import requests

def download_files(links, output_folder, headers, file_type):
    for data in links:
        # Check if the 'type' matches the specified type
        if data['type'] != file_type:
            continue

        file = os.path.join(output_folder, data['file'])  # Full path for the downloaded file
        full_link = 'https://' + data['link']
        print(file)
        print(full_link)

        response = requests.get(full_link, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Create the download folder if it doesn't exist
            os.makedirs(output_folder, exist_ok=True)

            # Save the PDF or CSV content to a file in the specified folder
            path = os.path.join(output_folder, data['file'])
            with open(path, 'wb') as file:
                file.write(response.content)

            print(f"File downloaded to {path}")
        else:
            print(f"Error: {response.status_code} - {response.text}")


def extract_principal_funds(file_path):
    # Open the PDF file
    pdf_document = fitz.open(file_path)

    # Initialize the result variable
    total_principal_funds = None

    # Iterate over all pages in the document
    for target_page in range(pdf_document.page_count):
        # Get the specified page
        page = pdf_document[target_page]

        # Extract text from the page
        text = page.get_text()

        # Define the keywords
        start_keyword = "Total Principal Funds Available:"
        end_keyword = "Other Funds Available"

        # Find the start and end indices
        start_index = text.find(start_keyword)
        end_index = text.find(end_keyword)

        # Check if both keywords are found
        if start_index != -1 and end_index != -1:
            # Extract the text between the two keywords
            result_text = text[start_index + len(start_keyword):end_index].strip()

            # Convert the text to a float (assuming it may contain commas)
            total_principal_funds = float(result_text.replace(',', ''))
            
            # Print the result
            print(f"Page {target_page + 1}: Text between '{start_keyword}' and '{end_keyword}':\n{result_text}\n")

            # Break the loop if principal funds are found
            break
        else:
            print(f"Page {target_page + 1}: Keywords not found.\n")

    # Close the PDF document
    pdf_document.close()

    return total_principal_funds


