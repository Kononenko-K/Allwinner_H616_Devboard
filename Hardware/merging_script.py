#!/usr/bin/env python3
'''
===============================================================================
Filename: merging_script.py
-------------------------------------------------------------------------------
Created on: 2026-02-12

License:
    MIT License
    Copyright (c) 2026 Kirill Kononenko
===============================================================================
'''
import sys
import os
import glob
from pypdf import PdfWriter
from PIL import Image
import img2pdf

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input_directory>")
        return
    
    input_dir = sys.argv[1]
    
    if not os.path.isdir(input_dir):
        print(f"Error: Directory '{input_dir}' not found.")
        return
    
    output_filename = 'project.pdf'
    a4inpt = (img2pdf.mm_to_pt(297), img2pdf.mm_to_pt(210))
    layout_fun = img2pdf.get_layout_fun(a4inpt)
    
    temp_files = []
    os.chdir(input_dir)
    
    # Process existing PDF files
    for i in glob.glob('*.pdf'):
        if not i == output_filename:  # Skip the output file itself
            temp_file_name = i
            with open(temp_file_name, 'rb') as f:
                content = f.read()
            # Write to a temporary file to avoid duplicates
            with open(f'~{os.path.splitext(i)[0]}.pdf', 'wb') as f:
                f.write(content)
            temp_files.append(f'~{os.path.splitext(i)[0]}.pdf')
    
    # Process image files
    for i in glob.glob('*.png') + glob.glob('*.jpg'):
        image = Image.open(i)
        pdf_bytes = img2pdf.convert(image.filename, layout_fun=layout_fun)
        temp_file_name = f'~{os.path.splitext(i)[0]}.pdf'
        with open(temp_file_name, 'wb') as f:
            f.write(pdf_bytes)
        temp_files.append(temp_file_name)
    
    merger = PdfWriter()
    for temp in temp_files:
        try:
            with open(temp, 'rb') as f:
                merger.append(fileobj=f)
        except Exception as e:
            print(f"Error merging {temp}: {e}")
    
    if not merger.pages:
        print("No pages to merge. Exiting.")
        return
    
    with open(output_filename, 'wb') as output:
        merger.write(output)
    
    merger.close()
    
    # Clean up temporary files
    for temp in temp_files:
        try:
            os.remove(temp)
        except Exception as e:
            print(f"Error deleting {temp}: {e}")

if __name__ == "__main__":
    main()