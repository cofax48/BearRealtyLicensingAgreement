#from PyPDF2 import PdfFileWriter, PdfFileReader
#import io
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import letter
from datetime import datetime
import time

from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys

def return_most_recent_file():
    #Relative or absolute path to the directory
    dir_path = sys.argv[1] if len(sys.argv) == 2 else r'.'

    #all entries in the directory w/ stats
    data = (os.path.join(dir_path, fn) for fn in os.listdir(dir_path))
    data = ((os.stat(path), path) for path in data)

    # regular files, insert creation date
    data = ((stat[ST_CTIME], path)
               for stat, path in data if S_ISREG(stat[ST_MODE]))

    all_items = []
    for cdate, path in sorted(data):
        all_items.append(os.path.basename(path))
        print(time.ctime(cdate), os.path.basename(path))

    most_recent = all_items[-1]
    name_to_return = most_recent.replace('pdf.pdf', '')

    return name_to_return

"""
six_months_in_seconds = int(int(time.time()) + 15552000)
todays_date = datetime.fromtimestamp(int(time.time())).strftime('%B-%d-%Y')
six_months_from_now = datetime.fromtimestamp(six_months_in_seconds).strftime('%B-%d-%Y')

packet = io.BytesIO()
packet2 = io.BytesIO()

# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
#First page of PDF
can.setFont('Helvetica', 10)
can.drawString(246, 394, "{}".format(todays_date))
can.drawString(416, 394, "{}".format(six_months_from_now))
can.save()

# create a new PDF with Reportlab
can4 = canvas.Canvas(packet2, pagesize=letter)
#Fourth Page of PDF
can4.setFont('Helvetica', 10)
can4.setFont('Helvetica', 12)
can4.drawString(125, 398, "{}".format("Josh Woods"))
can4.drawString(416, 398, "{}".format("Will Bear"))
can4.drawString(125, 360, "{}".format(todays_date))
can4.drawString(406, 360, "{}".format(todays_date))
can4.save()

# move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)

# move to the beginning of the StringIO buffer for page 4
packet2.seek(0)
new_pdf4 = PdfFileReader(packet2)

# read your existing PDF
existing_pdf = PdfFileReader(open("EXR_Buyer_Broker_Agreement.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page2 = existing_pdf.getPage(1)
page3 = existing_pdf.getPage(2)
page4 = existing_pdf.getPage(3)
pageN = new_pdf.getPage(0)
pageN4 = new_pdf4.getPage(0)
page.mergePage(pageN)
page4.mergePage(pageN4)

output.addPage(page)
output.addPage(page2)
output.addPage(page3)
output.addPage(page4)
# finally, write "output" to a real file
outputStream = open("newpdf.pdf", "wb")
output.write(outputStream)
outputStream.close()
"""
