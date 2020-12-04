from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QFileDialog

class BaseMainWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        self._parent = parent

    def _createButton(self, text, callback = None):
        btn = QPushButton(self._parent)
        btn.setText(text)
        font = btn.font()
        font.setPointSize(12)
        btn.setFont(font)

        if callback is not None:
            btn.clicked.connect(callback)
        
        return btn

    def _isNoneOrWhiteSpace(self, text):
        if text is None or text.isspace() or len(text) == 0:
            return True

    def _openCSVFile(self):
        fname = QFileDialog.getOpenFileName(parent=self._parent, caption='Select CSV File', filter='CSV files (*.csv)')
        self.findChild(QLineEdit, 'csvFile').setText(fname[0])