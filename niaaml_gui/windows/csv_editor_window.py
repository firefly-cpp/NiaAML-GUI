from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QTableView, QMessageBox, QVBoxLayout, QPushButton
from PyQt5.QtCore import QSize
import csv
import qtawesome as qta

class CSVEditorWindow(QMainWindow):
    def __init__(self, src):
        super(CSVEditorWindow, self).__init__()
        self.setMinimumSize(QSize(640, 480))

        self.__src = src
        self.__table = QTableView(self)
        self.__model = QtGui.QStandardItemModel(self)
        self.__table.setModel(self.__model)

        try:
            with open(src, 'r') as f:
                for row in csv.reader(f):
                    items = [
                        QStandardItem(field) for field in row
                    ]
                    self.__model.appendRow(items)
        except:
            self.__errorMessage = QMessageBox(QMessageBox.Critical, 'Error', 'File could not be read.')
            self.__errorMessage.show()
            return

        centralWidget = QWidget(self)
        layout = QVBoxLayout(centralWidget)
        
        toolBar = QHBoxLayout(centralWidget)
        toolBar.setAlignment(QtCore.Qt.AlignLeft)
        saveBtn = self.__createButton(None, self.__save, None, qta.icon('fa5.save'))
        toolBar.addWidget(saveBtn)

        layout.addItem(toolBar)
        layout.addWidget(self.__table)

        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def __createButton(self, text, callback = None, objectName = None, icon = None):
        btn = QPushButton(self)
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
    
    def __save(self):
        self.__writeCsv(self.__src)
    
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Delete or e.key() == QtCore.Qt.Key_Backspace:
            rows = self.__table.selectionModel().selectedRows()
            for index in rows:
                self.__model.removeRow(index.row())

            cols = self.__table.selectionModel().selectedColumns()
            for index in cols:
                self.__model.removeColumn(index.column())
            
            cells = self.__table.selectedIndexes()
            for index in cells:
                if self.__model.item(index.row(), index.column()) is not None:
                    self.__model.item(index.row(), index.column()).setText(None)

    def __writeCsv(self, fileName):
        try:
            with open(fileName, 'w', newline='') as fileOutput:
                writer = csv.writer(fileOutput)
                for rowNumber in range(self.__model.rowCount()):
                    fields = [
                        self.__model.data(
                            self.__model.index(rowNumber, columnNumber),
                            QtCore.Qt.DisplayRole
                        )
                        for columnNumber in range(self.__model.columnCount())
                    ]
                    writer.writerow(fields)
        except:
            self.__errorMessage = QMessageBox(QMessageBox.Critical, 'Error', 'File could not be saved.')
            self.__errorMessage.show()
            return
