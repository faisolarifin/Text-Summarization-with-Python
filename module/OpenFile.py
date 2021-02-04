import PyPDF2
import win32com.client
import docx2txt

class OpenFile:
    def __init__(self):
        pass

    def openpdf(self, file):
        pdfFileObj = open(file, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        document = ''
        for page in range (pdfReader.getNumPages()):
            pageObj = pdfReader.getPage(page)
            document += pageObj.extractText()
        return document.replace('\n','')

    def opendocx(self, file):
        return docx2txt.process(file)
    
    def opendoc(self, file):
        word = win32com.client.Dispatch("Word.Application")
        wb = word.Documents.Open(file.replace('/', '\\'))
        doc = word.ActiveDocument
        return doc.Range().Text