from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QFileDialog
from niaaml_gui.windows import CSVEditorWindow
from PyQt5 import QtCore

class BaseMainWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        self._parent = parent
        self._processWindow = None
        self.__csvEditWindow = None

    def _createButton(self, text, callback = None, objectName = None, icon = None):
        btn = QPushButton(self._parent)
        btn.setText(text)
        font = btn.font()
        font.setPointSize(12)
        btn.setFont(font)

        if callback is not None:
            btn.clicked.connect(callback)
        
        if objectName is not None:
            btn.setObjectName(objectName)

        if icon is not None:
            btn.setIcon(icon)
            btn.setIconSize(QtCore.QSize(21, 21))

        return btn

    def _isNoneOrWhiteSpace(self, text):
        if text is None or text.isspace() or len(text) == 0:
            return True

    def _openCSVFile(self):
        fname = QFileDialog.getOpenFileName(parent=self._parent, caption='Select CSV File', filter='CSV files (*.csv)')
        self.findChild(QLineEdit, 'csvFile').setText(fname[0])
        self.findChild(QPushButton, 'editCSVButton').setEnabled(True)

    def _editCSVFile(self):
        src = self.findChild(QLineEdit, 'csvFile').text()
        self.__csvEditWindow = CSVEditorWindow(src)
        self.__csvEditWindow.show()