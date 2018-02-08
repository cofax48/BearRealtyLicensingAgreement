# app.py
from flask import Flask
from flask import request, render_template, jsonify
import json
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import time
import os
import base64


app = Flask(__name__)

#Homepage
@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/pdfEdit", methods=['POST'])
def pdfEdit():

    data = json.loads(request.data.decode())
    clientName = data["clientName"]

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
    can4.drawString(125, 398, "{}".format(clientName))
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
    curDir = os.getcwd()
    outputStream = open(curDir + "/static/images/pdfs/{}pdf.pdf".format(clientName), "wb")
    output.write(outputStream)
    outputStream.close()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route("/signatureCapture", methods=['POST'])
def signatureCapture():
    #Gets the name of the most recent pdf created-does not scale
    from static.images.pdfs.Most_recent_file_return_prog import return_most_recent_file

    #bytes of images
    sigData = request.data
    sigString = sigData[22:]
    print(sigData[22:])
    #sigDataToUSE = decode_base64(sigData)
    #print(sigDataToUSE)
    sigName = return_most_recent_file()

    #saves new image
    with open("{}Signature.png".format(sigName), "wb") as fh:
        fh.write(base64.decodebytes(sigString))

    #initialize new stream
    packet2 = io.BytesIO()

    # create a new PDF with Reportlab
    can4 = canvas.Canvas(packet2, pagesize=letter)
    #Fourth Page of PDF
    can4.drawImage('{}Signature.png'.format(sigName), 55, 430, 240, 46, mask='auto') ## at (15, 320) with size 160x160
    can4.save()


    # move to the beginning of the StringIO buffer for page 4
    packet2.seek(0)
    new_pdf4 = PdfFileReader(packet2)

    # read your existing PDF
    curDir = os.getcwd()
    existing_pdf = PdfFileReader(open(curDir + "/static/images/pdfs/{}pdf.pdf".format(sigName), "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page2 = existing_pdf.getPage(1)
    page3 = existing_pdf.getPage(2)
    page4 = existing_pdf.getPage(3)

    pageN4 = new_pdf4.getPage(0)
    page4.mergePage(pageN4)

    #adds the other pages
    output.addPage(page)
    output.addPage(page2)
    output.addPage(page3)
    output.addPage(page4)

    # finally, write "output" to a real file
    curDir = os.getcwd()
    outputStream = open(curDir + "/static/images/pdfs/{}SignedAgreement.pdf".format(sigName), "wb")
    output.write(outputStream)
    outputStream.close()

    #Removes the previously edited pdf and signature
    os.remove(curDir + "/static/images/pdfs/{}pdf.pdf".format(sigName))
    os.remove(curDir + '/{}Signature.png'.format(sigName))


    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

if __name__ == '__main__':
    app.run(debug=True)
