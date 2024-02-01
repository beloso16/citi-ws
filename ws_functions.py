import fitz  # PyMuPDF

def extract_between_keywords(file_path, target_page):
    # Open the PDF file
    pdf_document = fitz.open(file_path)

    # Check if the target page is valid
    if target_page < 1 or target_page > pdf_document.page_count:
        print(f"Error: Invalid target page {target_page}.")
        pdf_document.close()
        return

    # Get the specified page
    page = pdf_document[target_page - 1]

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

        # Print the result
        print(f"Page {target_page}: Text between '{start_keyword}' and '{end_keyword}':\n{result_text}\n")
    else:
        print(f"Page {target_page}: Keywords not found.\n")

    # Close the PDF document
    pdf_document.close()

# Example usage for page 6
file_path = '/Users/faustine/Downloads/CertStmtCMLT06AMC10610.pdf'
target_page = 6
extract_between_keywords(file_path, target_page)

