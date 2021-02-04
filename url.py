from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QFileDialog
from ui.UI_url import Ui_Form
from module.Crawling import Crawling
from module.TextSummarization import TextSummarization

class SumberURL(QDialog, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Aplikasi Ringkasan Dokumen - FTIF-UTM')
        self.setFixedSize(981, 544)
        self.url.clicked.connect(self.getCrawlData)
        self.ringkasan.clicked.connect(self.prosesRingkasan)
        self.save.clicked.connect(self.Save)
    
    def getCrawlData(self):
        url = self.texturl.text()
        if not url:
            return
        try:
            crawler = Crawling(url)
            result = crawler.crawl()
            self.textsumber.setText(result)
        except Exception:
            QMessageBox.critical(self, "Error", "Tidak ada koneksi internet!", QMessageBox.Ok)

    def prosesRingkasan(self):
        textsumber = self.textsumber.toPlainText()
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
            