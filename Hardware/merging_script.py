#!/usr/bin/python3

import os
import glob
import img2pdf
from pypdf import PdfWriter
from PIL import Image

output_filename = 'project.pdf'

png_files = sorted(glob.glob('*.png'))

a4inpt = (img2pdf.mm_to_pt(297),img2pdf.mm_to_pt(210))
layout_fun = img2pdf.get_layout_fun(a4inpt)

remove_list = []

for i in png_files:
    image = Image.open(i)
    pdf_bytes = img2pdf.convert(image.filename, layout_fun=layout_fun)
    remove_list.append(f'~{i[:-4]}.pdf')
    file = open(f'~{i[:-4]}.pdf', 'wb')
    file.write(pdf_bytes)
    file.close()

pdf_files = sorted(glob.glob('*.pdf'))

try:
    pdf_files.remove(output_filename)
except Exception:
    pass

merger = PdfWriter()

input_list = []

for i in pdf_files:
    input_list.append(open(i, 'rb'))

for i in input_list:
    merger.append(fileobj=i)

output = open(output_filename, 'wb')
merger.write(output)

merger.close()
output.close()

for i in remove_list:
    try:
        os .remove(i)
    except Exception as e:
        print(e)
