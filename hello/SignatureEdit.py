import json
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import time
import os
import base64


packet2 = io.BytesIO()


# create a new PDF with Reportlab
can4 = canvas.Canvas(packet2, pagesize=letter)
#Fourth Page of PDF
can4.drawImage('cashmoneySignature.png', 55, 430, 240, 46, mask='auto') ## at (15, 320) with size 160x160
can4.save()


# move to the beginning of the StringIO buffer for page 4
packet2.seek(0)
new_pdf4 = PdfFileReader(packet2)

# read your existing PDF
curDir = os.getcwd()
existing_pdf = PdfFileReader(open(curDir + "/static/images/pdfs/cashmoneypdf.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page2 = existing_pdf.getPage(1)
page3 = existing_pdf.getPage(2)
page4 = existing_pdf.getPage(3)

pageN4 = new_pdf4.getPage(0)
page4.mergePage(pageN4)

output.addPage(page)
output.addPage(page2)
output.addPage(page3)
output.addPage(page4)


clientName = 'WITHSIGNATURE'
# finally, write "output" to a real file
curDir = os.getcwd()
outputStream = open(curDir + "/static/images/pdfs/{}pdf.pdf".format(clientName), "wb")
output.write(outputStream)
outputStream.close()



"""
# Create the watermark from an image
c = canvas.Canvas('joshMillionairesignature.pdf')

# Draw the image at x, y. I positioned the x,y to be where i like here
c.drawImage('joshMillionaireSignature.png', 15, 720)

# Add some custom text for good measure
c.drawString(15, 320,"Hello World")
c.save()

# Get the watermark file you just created
watermark = PdfFileReader(open("joshMillionairesignature.pdf", "rb"))

# Get our files ready
output_file = PdfFileWriter()
curDir = os.getcwd()
input_file = PdfFileReader(open(curDir + "/static/images/pdfs/joshMillionairepdf.pdf", "rb"))

# Number of pages in input document
page_count = input_file.getNumPages()


# merge the watermark with the page
input_page = input_file.getPage(3)
input_page.mergePage(watermark.getPage(0))
# add page from input file to output document
output_file.addPage(input_page)

# finally, write "output" to document-output.pdf
with open("document-output.pdf", "wb") as outputStream:
    output_file.write(outputStream)
"""
'''
packet = io.BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
can.drawString(10, 100, "Hello world")
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
curDir = os.getcwd()
existing_pdf = PdfFileReader(open(curDir + "/static/images/pdfs/joshMillionairepdfpdf.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = open("destination.pdf", "wb")
output.write(outputStream)
outputStream.close()
'''
