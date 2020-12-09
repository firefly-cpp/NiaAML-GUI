from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QCheckBox
from niaaml_gui.widgets.base_main_widget import BaseMainWidget
from niaaml_gui.windows import ProcessWindow
from niaaml_gui.process_window_data import ProcessWindowData
import qtawesome as qta

class UsePipelineWidget(BaseMainWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
    
        vBoxLayout = QVBoxLayout(self._parent)
        vBoxLayout.setAlignment(QtCore.Qt.AlignTop)

        selectPPLNFileBar = QHBoxLayout(self._parent)
        selectPPLNFileBar.setSpacing(0)
        fNameLine1 = QLineEdit(self._parent)
        fNameLine1.setObjectName('pplnFile')
        fNameLine1.setPlaceholderText('Select a pipeline file...')
        fNameLine1.setReadOnly(True)
        font = fNameLine1.font()
        font.setPointSize(12)
        fNameLine1.setFont(font)
        selectPPLNFileBar.addWidget(fNameLine1)
        selectPPLNFileBar.addWidget(self._createButton('Select file', self.__openPPLNFile))

        fileLayout = QHBoxLayout(self._parent)

        selectFileBar = QHBoxLayout(self._parent)
        selectFileBar.setSpacing(0)
        selectFileBar.setContentsMargins(0, 0, 5, 0)
        fNameLine = QLineEdit(self._parent)
        fNameLine.setObjectName('csvFile')
        fNameLine.setPlaceholderText('Select a CSV file with features...')
        fNameLine.setReadOnly(True)
        fNameLine.setFont(font)
        selectFileBar.addWidget(fNameLine)
        editBtn = self._createButton(None, self._editCSVFile, 'editCSVButton', qta.icon('fa5.edit'))
        editBtn.setEnabled(False)
        selectFileBar.addWidget(editBtn)
        selectFileBar.addWidget(self._createButton('Select file', self._openCSVFile))

        checkBox = QCheckBox('CSV has header')
        checkBox.setObjectName('csv')
        checkBox.setFont(font)

        fileLayout.addItem(selectFileBar)
        fileLayout.addWidget(checkBox)

        confirmBar = QHBoxLayout(self._parent)
        confirmBar.addStretch()
        confirmBar.addWidget(self._createButton('Run', self.__runPipeline))

        vBoxLayout.addItem(selectPPLNFileBar)
        vBoxLayout.addItem(fileLayout)
        vBoxLayout.addItem(confirmBar)

        self.setLayout(vBoxLayout)

    def __openPPLNFile(self):
        fname = QFileDialog.getOpenFileName(parent=self._parent, caption='Select pipeline File', filter='PPLN files (*.PPLN)')
        self.findChild(QLineEdit, 'pplnFile').setText(fname[0])
    
    def __runPipeline(self):
        err = ''

        pplnSrc = self.findChild(QLineEdit, 'pplnFile').text()
        if self._isNoneOrWhiteSpace(pplnSrc):
            err += 'Select pipeline file.\n'

        csvSrc = self.findChild(QLineEdit, 'csvFile').text()
        if self._isNoneOrWhiteSpace(csvSrc):
            err += 'Select CSV file with features.\n'

        if not self._isNoneOrWhiteSpace(err):
            self._parent.errorMessage.setText(err)
            self._parent.errorMessage.show()
            return

        self._processWindow = ProcessWindow(
            self._parent,
            ProcessWindowData(
                False,
                csvSrc=csvSrc,
                csvHasHeader=self.findChild(QCheckBox, 'csv').isChecked(),
                pipelineSrc=pplnSrc
                )
            )
        self._processWindow.show()