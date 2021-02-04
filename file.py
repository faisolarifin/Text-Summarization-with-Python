from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QMessageBox
from ui.UI_file import Ui_Form
from module.OpenFile import OpenFile
from module.TextSummarization import TextSummarization

class SumberFile(QDialog, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Aplikasi Ringkasan Dokumen - FTIF-UTM')
        self.setFixedSize(981, 544)
        self.openfile.clicked.connect(self.getOpenFile)
        self.ringkasan.clicked.connect(self.prosesRingkasan)
        self.save.clicked.connect(self.Save)
        
    def getOpenFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', 'C:/', 'Document (*.pdf;*.doc;*.docx)')
        if filename:
            self.loc.setText(filename)
            extensi = filename.split('.')[-1]
            openf = OpenFile()
            if extensi=='pdf':
                document = openf.openpdf(filename)
            elif extensi=='docx':
                document = openf.opendocx(filename)
            elif extensi=='doc':
                document = openf.opendoc(filename)
                               
            self.textsumber.setText(document)
    
    def prosesRingkasan(self):
        textsumber=self.textsumber.toPlainText()
        if textsumber:
            textsum = TextSummarization()
            ringkasan = textsum.Summary(textsumber, preprocess=True)
            self.textringkasan.setText(ringkasan)
    
    def Save(self):
        summary=self.textringkasan.toPlainText()
        if summary:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', 'C://', 'Text (*.txt)')
            if filename:
                with open(filename, 'w', encoding="utf-8") as f:
                    f.write(summary.replace("", ""))
                QMessageBox.information(self, "Success", "Ringkasan berhasil di simpan!", QMessageBox.Ok)
            