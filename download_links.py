import pandas as pd
import requests
import os
import time
from pdf_merger import pdf_merger, pdf_merger_receipt
from reorder_patients import reorder_patients_by_tiny_number
from fpdf import FPDF

def download_links_manual():
    # Define the path to the Excel file
    excel_file_path_in = '.\output\download_list.xlsx'
    excel_file_path_out  = '.\output\download_list_reordered.xlsx'

    # Reordena o arquivo de excel em ordem alfabética
    reorder_patients_by_tiny_number(excel_file_path_in, excel_file_path_out)

    # Read the Excel file
    df = pd.read_excel(excel_file_path_out)

    # Define the columns containing the URLs
    prescription_pdf_column = 'Prescription PDF'
    receipt_link_column = 'Receipt Link'
    cpf_column = 'CPF'
    date_column = 'data_pedido'
    tiny_column = 'Tiny'

    # Create a directory to save the downloaded files
    download_dir = 'downloads_receitas_manual'
    os.makedirs(download_dir, exist_ok=True)

    # Iterate over the rows in the DataFrame and download the files
    for index, row in df.iterrows():
        prescription_pdf_url = row[prescription_pdf_column]
        receipt_link_url = row[receipt_link_column]
        cpf = row[cpf_column]
        order_number = row[tiny_column]

        # Create a directory to save files from the given date
        date = row[date_column]
        date = date.split('/')
        date = f'{date[2]}-{date[1]}-{date[0]}'
        date_dir = os.path.join(download_dir, date)
        os.makedirs(date_dir, exist_ok=True)
        
        # Path and name for the files to be downloaded
        prescription = os.path.join(date_dir, f'{cpf}_{order_number}_prescription_{index}.pdf')
        receipt = os.path.join(date_dir, f'{cpf}_{order_number}_receipt_{index}.pdf')

        # Download the Prescription file
        if pd.notna(prescription_pdf_url):
            while True:
                download_file(prescription_pdf_url, prescription)
                break
        else:
            # If the prescription PDF URL is missing, create a blank PDF
            if pd.isna(prescription_pdf_url):
                pdf = FPDF()
                pdf.add_page()
                pdf.output(prescription)
                print(f"Created blank PDF: {prescription}")

        # Download the Receipt file
        if pd.notna(receipt_link_url):
            while True:
                download_file(receipt_link_url, receipt)
                break
        else:
            # If the receipt PDF URL is missing, create a blank PDF
            if pd.isna(receipt_link_url):
                pdf = FPDF()
                pdf.add_page()
                pdf.output(receipt)
                print(f"Created blank PDF: {receipt}")

        # Merge the downloaded PDF files
        try:
            # pdf_merger(prescription, receipt)
            pdf_merger_receipt(receipt)
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
