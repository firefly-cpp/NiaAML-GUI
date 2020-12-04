import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import qApp, QMainWindow, QMessageBox, QAction
from PyQt5.QtCore import QSize
from niaaml_gui.widgets import OptimizationWidget, UsePipelineWidget

class HelloWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle('NiaAML - GUI')

        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu('&File')
        exitAction = QAction(text='Exit', parent=self)
        exitAction.triggered.connect(qApp.quit)
        newPipelineAction = QAction(text='New Pipeline', parent=self)
        newPipelineAction.triggered.connect(self.__setOptimizationView)
        useExistingPipelineAction = QAction(text='Use Existing Pipeline', parent=self)
        useExistingPipelineAction.triggered.connect(self.__setUsePipelineView)

        fileMenu.addAction(newPipelineAction)
        fileMenu.addAction(useExistingPipelineAction)
        fileMenu.addAction(exitAction)

        self.setCentralWidget(OptimizationWidget(self))

        self.errorMessage = QMessageBox()
        self.errorMessage.setIcon(QMessageBox.Critical)
        self.errorMessage.setWindowTitle('Error')
        self.errorMessage.setStandardButtons(QMessageBox.Ok)

    def __setOptimizationView(self):
        self.setCentralWidget(OptimizationWidget(self))

    def __setUsePipelineView(self):
        self.setCentralWidget(UsePipelineWidget(self))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit(app.exec_())