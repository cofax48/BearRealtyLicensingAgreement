from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt


import json
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import time
import os
import base64

#email stuff
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

@csrf_exempt
def pdfEdit(request):

    data = json.loads(request.body.decode('utf-8'))
    print(data, '25')
    clientName = data["clientName"]
    clientAddress = data["Address"]
    clientEmail = "Email: " + str(data["Email"])
    clientPhoneNumber = "Phone Number: " + data["PhoneNum"]
    clientNameAndAdress = clientName + ', ' + clientAddress
    print(clientName, '25')

    six_months_in_seconds = int(int(time.time()) + 15552000)
    todays_date = datetime.fromtimestamp(int(time.time())).strftime('%B-%d-%Y')
    six_months_from_now = datetime.fromtimestamp(six_months_in_seconds).strftime('%B-%d-%Y')

    packet = io.BytesIO()
    packet2 = io.BytesIO()

    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    #First page of PDF
    can.setFont('Helvetica', 10)

    can.drawString(96, 588, "{}".format(clientNameAndAdress))


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
    can4.drawString(100, 320, "{}".format(clientEmail))
    can4.drawString(390, 320, "{}".format(clientPhoneNumber))


    can4.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)

    # move to the beginning of the StringIO buffer for page 4
    packet2.seek(0)
    new_pdf4 = PdfFileReader(packet2)

    # read your existing PDF
    curDir = os.getcwd()
    existing_pdf = PdfFileReader(open(curDir + "/hello/static/images/pdfs/EXR_Buyer_Broker_AgreementSansComission.pdf", "rb"))
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

    real_file_address = curDir + "/hello/static/images/pdfs/{}pdf.pdf".format(clientName)
    # finally, write "output" to a real file
    outputStream = open(real_file_address, "wb")
    output.write(outputStream)
    outputStream.close()
    print(real_file_address, 'output complte 101')

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@csrf_exempt
def pdfServe(request):
    print(request)
    time.sleep(3)
    ABRV_table_name = str(request)[45:]
    ABRV_table_name = ABRV_table_name[:-2]
    ABRV_table_name != 'favicon.ico'
    ABRV_table_name != '/favicon.ico'
    ABRV_table_name = ABRV_table_name.replace('%20', ' ', 3)

    print(ABRV_table_name)
    list_return = []

    curDir = os.getcwd()
    response_adrress = curDir + "/hello/static/images/pdfs/{}".format(ABRV_table_name)
    print(response_adrress, '106')
    response = FileResponse(open(response_adrress, 'rb'), content_type="application/pdf")
    response["Content-Disposition"] = "filename={}".format(ABRV_table_name)
    return response

@csrf_exempt
def signatureCapture(request):
    time.sleep(3)
    print('112')
    #Gets the name of the most recent pdf created-does not scale
    from hello.static.images.pdfs.Most_recent_file_return_prog import return_most_recent_file


    #bytes of images
    sigData = request.body
    sigString = sigData[22:]
    #sigDataToUSE = decode_base64(sigData)
    #print(sigDataToUSE)
    sigName = return_most_recent_file()

    curDir = os.getcwd()
    #saves new image
    with open(curDir + "/hello/static/images/pdfs/{}Signature.png".format(sigName), "wb") as fh:
        fh.write(base64.decodebytes(sigString))

    #initialize new stream
    packet2 = io.BytesIO()

    # create a new PDF with Reportlab
    can4 = canvas.Canvas(packet2, pagesize=letter)
    #Fourth Page of PDF
    can4.drawImage(curDir + '/hello/static/images/pdfs/{}Signature.png'.format(sigName), 55, 430, 240, 46, mask='auto') ## at (15, 320) with size 160x160
    can4.save()


    # move to the beginning of the StringIO buffer for page 4
    packet2.seek(0)
    new_pdf4 = PdfFileReader(packet2)

    # read your existing PDF
    existing_pdf = PdfFileReader(open(curDir + "/hello/static/images/pdfs/{}pdf.pdf".format(sigName), "rb"))
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
    outputStream = open(curDir + "/hello/static/images/pdfs/{}SignedAgreement.pdf".format(sigName), "wb")
    output.write(outputStream)
    outputStream.close()

    #Removes the previously edited pdf and signature
    os.remove(curDir + "/hello/static/images/pdfs/{}pdf.pdf".format(sigName))
    os.remove(curDir + '/hello/static/images/pdfs/{}Signature.png'.format(sigName))

    ###################
    #Email Stuff
    #################

    fromaddr = "joshwillrealtyproductions@gmail.com"
    toaddr = "redcupnyc@gmail.com"

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Agreement With: {}".format(sigName)

    body = "Licensing Agreement From: {}".format(sigName)

    msg.attach(MIMEText(body, 'plain'))

    FileNameToUSe = sigName.replace(' ', '_', 3)

    filename = "{}SignedAgreement.pdf".format(FileNameToUSe)
    attachment = open(curDir + "/hello/static/images/pdfs/{}SignedAgreement.pdf".format(sigName), "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "JoshAndWill2018")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print('170')

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@csrf_exempt
def SignedAgreement(request):
    ABRV_table_name = str(request)[36:]
    ABRV_table_name = ABRV_table_name[:-2]
    ABRV_table_name != 'favicon.ico'
    ABRV_table_name != '/favicon.ico'
    ABRV_table_name = ABRV_table_name.replace('%20', ' ', 3)

    print(ABRV_table_name)
    list_return = []

    curDir = os.getcwd()
    response_adrress = curDir + "/hello/static/images/pdfs/{}SignedAgreement.pdf".format(ABRV_table_name)
    print(response_adrress, '106')
    response = FileResponse(open(response_adrress, 'rb'), content_type="application/pdf")
    response["Content-Disposition"] = "filename={}".format(ABRV_table_name)
    return response
