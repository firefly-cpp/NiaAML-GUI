import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import qApp, QMainWindow, QMessageBox, QAction
from PyQt5.QtCore import QSize
from niaaml_gui.widgets import OptimizationWidget, UsePipelineWidget

class WriteStream(object):
    def __init__(self,queue):
        self.queue = queue

    def write(self, text):
        self.queue.append(text)

class MainAppWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(1024, 768))
        self.setWindowTitle('NiaAML - GUI')

        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu('&File')
        exitAction = QAction(text='Exit', parent=self)
        exitAction.triggered.connect(qApp.quit)
        newPipelineAction = QAction(text='New Pipeline', parent=self)
        newPipelineAction.triggered.connect(self.__setOptimizationView)
        newPipelineActionV1 = QAction(text='New Pipeline V1', parent=self)
        newPipelineActionV1.triggered.connect(self.__setOptimizationV1View)
        useExistingPipelineAction = QAction(text='Use Existing Pipeline', parent=self)
        useExistingPipelineAction.triggered.connect(self.__setUsePipelineView)

        fileMenu.addAction(newPipelineAction)
        fileMenu.addAction(newPipelineActionV1)
        fileMenu.addAction(useExistingPipelineAction)
        fileMenu.addAction(exitAction)

        self.setCentralWidget(OptimizationWidget(self))

        self.errorMessage = QMessageBox()
        self.errorMessage.setIcon(QMessageBox.Critical)
        self.errorMessage.setWindowTitle('Error')
        self.errorMessage.setStandardButtons(QMessageBox.Ok)

    def __setOptimizationView(self):
        self.setCentralWidget(OptimizationWidget(self))

    def __setOptimizationV1View(self):
        self.setCentralWidget(OptimizationWidget(self, True))

    def __setUsePipelineView(self):
        self.setCentralWidget(UsePipelineWidget(self))

def run():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWin = MainAppWindow()
    mainWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()
