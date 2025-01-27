import pandas as pd
import requests
import os
import time
from pdf_merger import pdf_merger
from reorder_patients import reorder_patients_by_name, reorder_patients_by_tiny_number

def download_links_manual():
    # Define the path to the Excel file
    excel_file_path_in = 'download_list.xlsx'
    excel_file_path_out  = 'download_list_reordered.xlsx'

    # Reordena o arquivo de excel em ordem alfabética
    # reorder_patients_by_name(excel_file_path_in, excel_file_path_out)
    reorder_patients_by_tiny_number(excel_file_path_in, excel_file_path_out)

    # Read the Excel file
    df = pd.read_excel(excel_file_path_out)

    # Define the columns containing the URLs
    prescription_pdf_column = 'Prescription PDF'
    receipt_link_column = 'Receipt Link'

    # Create a directory to save the downloaded files
    download_dir = 'downloads'
    os.makedirs(download_dir, exist_ok=True)

    # Iterate over the rows in the DataFrame and download the files
    for index, row in df.iterrows():
        prescription_pdf_url = row[prescription_pdf_column]
        receipt_link_url = row[receipt_link_column]

        if prescription_pdf_url == '' or receipt_link_url == '':
            continue

        prescription = os.path.join(download_dir, f'prescription_{index}.pdf')
        receipt = os.path.join(download_dir, f'receipt_{index}.pdf')

        # Download the files
        if prescription_pdf_url != '':
            while True:
                if pd.notna(prescription_pdf_url):
                    download_file(prescription_pdf_url, prescription)

                    break
        else:
            continue

        if receipt_link_url != '':
            while True:
                if pd.notna(receipt_link_url):
                    download_file(receipt_link_url, receipt)
                    break
        else:
            continue

        # Merge the downloaded PDF files
        try:
            pdf_merger(prescription, receipt)
        except Exception as e:
            print(f"Error merging PDF files {index}: {e}")
    
# Function to download a file from a URL
def download_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {save_path}")
    else:
        print(f"Failed to download: {url}")


download_links_manual()
