import os
from PyPDF2 import PdfReader, PdfWriter

def pdf_merger(prescription, receipt):
    curr_dir = os.getcwd()
    new_dir = curr_dir + '\\downloads'
    output_file = 'print_file.pdf'
    
    if output_file not in os.listdir():
        input_files = [prescription, receipt]
    elif output_file in os.listdir():
        input_files = [output_file, prescription, receipt]
    print(input_files)

    merger = PdfWriter()

    for pdf in input_files:
        with open(pdf, 'rb') as f:
            reader = PdfReader(f)
            for page in range(len(reader.pages)):
                merger.add_page(reader.pages[page])

    with open(output_file, 'wb') as f_out:
        merger.write(f_out)
    return
