import sys
import os
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QSize
from niaaml_gui.widgets import OptimizationWidget, UsePipelineWidget


class MainAppWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(1024, 768))
        self.setWindowTitle("NiaAML - GUI")

        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu("&File")
        exitAction = QAction(text="Exit", parent=self)
        exitAction.triggered.connect(QApplication.quit)
        newPipelineAction = QAction(text="New Pipeline", parent=self)
        newPipelineAction.triggered.connect(self.__setOptimizationView)
        newPipelineActionV1 = QAction(text="New Pipeline V1", parent=self)
        newPipelineActionV1.triggered.connect(self.__setOptimizationV1View)
        useExistingPipelineAction = QAction(text="Use Existing Pipeline", parent=self)
        useExistingPipelineAction.triggered.connect(self.__setUsePipelineView)

        fileMenu.addAction(newPipelineAction)
        fileMenu.addAction(newPipelineActionV1)
        fileMenu.addAction(useExistingPipelineAction)
        fileMenu.addAction(exitAction)

        self.setCentralWidget(OptimizationWidget(self))

        self.errorMessage = QMessageBox()
        self.errorMessage.setIcon(QMessageBox.Icon.Critical)
        self.errorMessage.setWindowTitle("Error")
        self.errorMessage.setStandardButtons(QMessageBox.StandardButton.Ok)

    def __setOptimizationView(self):
        self.setCentralWidget(OptimizationWidget(self))

    def __setOptimizationV1View(self):
        self.setCentralWidget(OptimizationWidget(self, True))

    def __setUsePipelineView(self):
        self.setCentralWidget(UsePipelineWidget(self))


def run():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles.qss'), 'r') as f:
        style = f.read()
        app.setStyleSheet(style)

    mainWin = MainAppWindow()
    mainWin.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
