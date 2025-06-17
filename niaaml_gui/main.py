import sys
import os
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QSize
from niaaml_gui.widgets import OptimizationWidget, UsePipelineWidget
from niaaml_gui.widgets.results_widget import ResultsWidget
from niaaml_gui.widgets.help_authors_widget import HelpAuthorsWidget
from niaaml_gui.widgets.help_documentation_widget import HelpDocumentationWidget
from niaaml_gui.widgets.help_license_widget import HelpLicenseWidget


class MainAppWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(1024, 768))
        self.setWindowTitle("NiaAML - GUI")

        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu("&File")
        helpMenu = menuBar.addMenu("&Help")
        exitAction = QAction(text="Exit", parent=self)
        exitAction.triggered.connect(QApplication.quit)
        newPipelineAction = QAction(text="New Pipeline", parent=self)
        newPipelineAction.triggered.connect(self.__setOptimizationView)
        newPipelineActionV1 = QAction(text="New Pipeline V1", parent=self)
        newPipelineActionV1.triggered.connect(self.__setOptimizationV1View)
        useExistingPipelineAction = QAction(text="Use Existing Pipeline", parent=self)
        useExistingPipelineAction.triggered.connect(self.__setUsePipelineView)

        authorsAction = QAction(text="Authors", parent=self)
        authorsAction.triggered.connect(self.__setHelpAuthorsView)
        documentationAction = QAction(text="Documentation", parent=self)
        documentationAction.triggered.connect(self.__setHelpDocumentationView)
        licenseAction = QAction(text="License", parent=self)
        licenseAction.triggered.connect(self.__setHelpLicenseView)

        fileMenu.addAction(newPipelineAction)
        fileMenu.addAction(newPipelineActionV1)
        fileMenu.addAction(useExistingPipelineAction)
        fileMenu.addAction(exitAction)

        helpMenu.addAction(authorsAction)
        helpMenu.addAction(documentationAction)
        helpMenu.addAction(licenseAction)

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

    def __setHelpAuthorsView(self):
        self.setCentralWidget(HelpAuthorsWidget(self))

    def __setHelpDocumentationView(self):
        self.setCentralWidget(HelpDocumentationWidget(self))

    def __setHelpLicenseView(self):
        self.setCentralWidget(HelpLicenseWidget(self))
        
    def setResultsView(self, resultsData, pipelineSettings):
        self.setCentralWidget(ResultsWidget(self, resultsData, pipelineSettings))


    
def run():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles.qss'), 'r') as f:
        style = f.read()
        app.setStyleSheet(style)

    mainWin = MainAppWindow()
    mainWin.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
