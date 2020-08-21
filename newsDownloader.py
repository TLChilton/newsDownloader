#! python3
# newsDownloader.py
# Created by Thomas Chilton
import PyPDF2, os, traceback
import requests, bs4, lxml
from colorama import init
init()

print('Downloading pdfs...')
res = requests.get('https://www.newseum.org/todaysfrontpages/?tfp_display=gallery&tfp_region=USA&tfp_sort_by=state&tfp_id=AZ_AR')
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, 'lxml')
element = soup.select('#contentPrimary > div > div > div > div.tfp-pane.tfp-pane-detail > p.tfp-meta > span.tfp-meta-controls > a:nth-child(2)')
pdfLink = element[0].get('href')
res = requests.get(pdfLink)
res.raise_for_status()

azPdf = open('azRepublic.pdf', 'wb')
azPdf.write(res.content)
azPdf.close()

res = requests.get('https://www.newseum.org/todaysfrontpages/?tfp_display=gallery&tfp_region=USA&tfp_sort_by=state&tfp_state_letter=N&tfp_id=NY_NYT')
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, 'lxml')
element = soup.select('#contentPrimary > div > div > div > div.tfp-pane.tfp-pane-detail > p.tfp-meta > span.tfp-meta-controls > a:nth-child(2)')
pdfLink = element[0].get('href')
res = requests.get(pdfLink)
res.raise_for_status()

nytPdf = open('NYT.pdf', 'wb')
nytPdf.write(res.content)
nytPdf.close()

pdfWriter = PyPDF2.PdfFileWriter()

pdfFileObj1 = open('azRepublic.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj1)
for pageNum in range(0, pdfReader.numPages):
    pageObj = pdfReader.getPage(pageNum)
    pdfWriter.addPage(pageObj)

pdfFileObj2 = open('NYT.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj2)
for pageNum in range(0, pdfReader.numPages):
    pageObj = pdfReader.getPage(pageNum)
    pdfWriter.addPage(pageObj)

print('\u001b[95mPlease enter a name for the combined news PDF file: \u001b[0m', end='')
savedFile = input()
if savedFile.endswith('.pdf') == False:
    savedFile = savedFile + '.pdf'
savedFile = os.path.abspath(savedFile)
while os.path.exists(savedFile):
    print('\u001b[95mERROR: ' + savedFile + ' already exists, \nPlease enter a new name: \u001b[0m', end= '')
    savedFile = input()
    if savedFile.endswith('.pdf') == False:
        savedFile = savedFile + '.pdf'
    savedFile = os.path.abspath(savedFile)
print('Daily news PDF saving as ' + savedFile)
try:
    pdfOutput = open(savedFile, 'wb')
    pdfWriter.write(pdfOutput)
    pdfOutput.close()
except:
    errorFile = open('errorInfo.txt', 'w')
    errorFile.write(traceback.format_exc())
    errorFile.close()
    print('\u001b[91mFatal error encountered. Traceback info written to errorInfo.txt.\u001b[0m')

pdfFileObj1.close()
pdfFileObj2.close()

os.remove('NYT.pdf')
os.remove('azRepublic.pdf')