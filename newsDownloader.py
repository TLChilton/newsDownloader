#! python3
# newsDownloader.py - this program was created in order to download the AZ Republic front page
#   and the New York Times front page from the Newseum website and to combine them into a single
#   PDF file
# Created by Thomas Chilton
import PyPDF2, os, traceback
import requests, bs4, lxml
from colorama import init
init()

# Messages are mostly unneccessary but they let the user know the program is working
print('Downloading pdfs...')

# Downloading the latest AZ Republic front page
res = requests.get('https://www.newseum.org/todaysfrontpages/?tfp_display=gallery&tfp_region=USA&tfp_sort_by=state&tfp_id=AZ_AR')
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, 'lxml')
element = soup.select('#contentPrimary > div > div > div > div.tfp-pane.tfp-pane-detail > p.tfp-meta > span.tfp-meta-controls > a:nth-child(2)')
pdfLink = element[0].get('href')
res = requests.get(pdfLink)
res.raise_for_status()

# Write the AZ Republic data to a file
azPdf = open('azRepublic.pdf', 'wb')
azPdf.write(res.content)
azPdf.close()

# Downloading the latest NY Times front page
res = requests.get('https://www.newseum.org/todaysfrontpages/?tfp_display=gallery&tfp_region=USA&tfp_sort_by=state&tfp_state_letter=N&tfp_id=NY_NYT')
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, 'lxml')
element = soup.select('#contentPrimary > div > div > div > div.tfp-pane.tfp-pane-detail > p.tfp-meta > span.tfp-meta-controls > a:nth-child(2)')
pdfLink = element[0].get('href')
res = requests.get(pdfLink)
res.raise_for_status()

# Write the NY Times data to a file
nytPdf = open('NYT.pdf', 'wb')
nytPdf.write(res.content)
nytPdf.close()

# Creating our combined PDF
pdfWriter = PyPDF2.PdfFileWriter()

# Adding the AZ Republic page
pdfFileObj1 = open('azRepublic.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj1)
for pageNum in range(0, pdfReader.numPages):
    pageObj = pdfReader.getPage(pageNum)
    pdfWriter.addPage(pageObj)

# Adding the NY Times page
pdfFileObj2 = open('NYT.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj2)
for pageNum in range(0, pdfReader.numPages):
    pageObj = pdfReader.getPage(pageNum)
    pdfWriter.addPage(pageObj)

# File saving section
print('\u001b[95mPlease enter a name for the combined news PDF file: \u001b[0m', end='')
savedFile = input()
# If the user left out the .pdf file extension add it at the end
if savedFile.endswith('.pdf') == False:
    savedFile = savedFile + '.pdf'
savedFile = os.path.abspath(savedFile)

# If the file name exists ask the user for a new file name
while os.path.exists(savedFile):
    print('\u001b[95mERROR: \u001b[93m' + savedFile + '\u001b[95m already exists, \nPlease enter a new name: \u001b[0m', end= '')
    savedFile = input()
    if savedFile.endswith('.pdf') == False:
        savedFile = savedFile + '.pdf'
    savedFile = os.path.abspath(savedFile)
print('Daily news PDF saving as ' + savedFile)
try:
    pdfOutput = open(savedFile, 'wb')
    pdfWriter.write(pdfOutput)
    pdfOutput.close()
# If there is an error in writing the file output the error code to a .txt file
except:
    errorFile = open('errorInfo.txt', 'w')
    errorFile.write(traceback.format_exc())
    errorFile.close()
    print('\u001b[91mFatal error encountered. Traceback info written to errorInfo.txt.\u001b[0m')

pdfFileObj1.close()
pdfFileObj2.close()

# Remove the individual New York Times and AZ Republic files
os.remove('NYT.pdf')
os.remove('azRepublic.pdf')

# Keep the program from automatically closing so the user can review the information displayed
print ('Execution successful, hit enter to close')
input()