import sys
import os
from PyQt6.QtWidgets import (
    QMainWindow, QMessageBox, QApplication, QWidget, QHBoxLayout
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QSize
from niaaml_gui.widgets.pipeline_canvas import PipelineCanvas
from niaaml_gui.widgets.sidebar import ComponentSidebar

class MainAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(1024, 768))
        self.setWindowTitle("NiaAML - GUI")

        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu("&File")
        helpMenu = menuBar.addMenu("&Help")

        exitAction = QAction(text="Exit", parent=self)
        exitAction.triggered.connect(QApplication.quit)

        fileMenu.addAction(exitAction)
        

        centralWidget = QWidget(self)
        mainLayout = QHBoxLayout(centralWidget)

        self.pipelineCanvas = PipelineCanvas()
        self.sidebar = ComponentSidebar(self.pipelineCanvas)

        mainLayout.addWidget(self.sidebar)
        mainLayout.addWidget(self.pipelineCanvas)
        centralWidget.setLayout(mainLayout)

        self.setCentralWidget(centralWidget)
        
        self.errorMessage = QMessageBox()
        self.errorMessage.setIcon(QMessageBox.Icon.Critical)
        self.errorMessage.setWindowTitle("Error")
        self.errorMessage.setStandardButtons(QMessageBox.StandardButton.Ok)

def run():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    style_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles.qss')
    if os.path.exists(style_path):
        with open(style_path, 'r') as f:
            app.setStyleSheet(f.read())

    mainWin = MainAppWindow()
    mainWin.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    run()
