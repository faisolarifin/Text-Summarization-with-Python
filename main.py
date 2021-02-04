import sys
from os import path
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from ui.UI_main import Ui_Form
from file import SumberFile
from url import SumberURL

class Main(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Aplikasi Ringkasan Dokumen - FTIF-UTM')
        self.setFixedSize(602, 292)
        self.file.clicked.connect(self.windowFile)
        self.url.clicked.connect(self.windowURL)
    
    def cekstopword(self):
        if path.exists('./stopwords.txt'):
            return True
        QMessageBox.critical(self, "Error", "file stopwords.txt tidak ditemukan!", QMessageBox.Ok)
        
    def windowFile(self):
        if not self.cekstopword():
            return
        sf = SumberFile()
        sf.exec_()

    def windowURL(self):
        if not self.cekstopword():
            return
        surl = SumberURL()
        surl.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    exe = Main()
    exe.show()
    sys.exit(app.exec_())

