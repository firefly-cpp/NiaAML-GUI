from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPlainTextEdit,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtCore import QSize, Qt
from niaaml_gui.progress_bar import ProgressBar
from niaaml_gui.windows.threads import OptimizeThread, RunThread
import copy
import re

class ProcessWindow(QMainWindow):
    def __init__(self, parent, data, pipelineSettings):
        super(ProcessWindow, self).__init__(parent)
        self.setMinimumSize(QSize(640, 480))
        self._parent = parent  
        centralWidget = QWidget(self)
        layout = QVBoxLayout(centralWidget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.__progressBar = ProgressBar()
        layout.addWidget(self.__progressBar)

        self.__pipelineSettings = pipelineSettings
        
        self.__textArea = QPlainTextEdit(parent=self)
        self.__textArea.setReadOnly(True)
        layout.addWidget(self.__textArea)

        confirmBar = QHBoxLayout(self)
        confirmBar.addStretch()

        self.__btn = QPushButton(self)
        self.__btn.setText("Cancel")
        font = self.__btn.font()
        font.setPointSize(12)
        self.__btn.setFont(font)
        self.__btn.clicked.connect(self.cancelClose)
        confirmBar.addWidget(self.__btn)

        layout.addItem(confirmBar)

        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.__data = copy.deepcopy(data)
        if self.__data.isOptimization is True or self.__data.isOptimization == "v1":
            self.__progressBar.setMaximum(100)
            self.__currentEvals = 0
            self.__totalEvals = (
                data.numEvals * data.numEvalsInner
                if data.isOptimization is True
                else data.numEvals
            )
            optimizer = OptimizeThread(self.__data)
            optimizer.optimized.connect(self.onOptimizationComplete)
            optimizer.progress.connect(self.onOptimizationProgress)
            self.__runningThread = optimizer
            optimizer.start()
            self.__textArea.appendPlainText("Pipeline optimization running...\n")
        else:
            self.__progressBar.setMaximum(0)
            self.__progressBar.setTextVisible(False)
            runner = RunThread(self.__data)
            runner.ran.connect(self.onRunComplete)
            self.__runningThread = runner
            runner.start()
            self.__textArea.appendPlainText("Pipeline running...\n")

    def cancelClose(self):
        self.close()
        try:
            self.__runningThread.terminate()
        except BaseException:
            return

    def onOptimizationComplete(self, data):
        self.__progressBar.setValue(100)
        self.__textArea.appendPlainText(data + "\n")
        self.__textArea.appendPlainText("Pipeline optimization complete.")
        self.__textArea.appendPlainText(
            "Results exported to: " + self.__data.outputFolder
        )
        self.__btn.setText("Close")
        
        results_data = parse_optimization_output(data)
        self._parent.setResultsView(results_data, self.__pipelineSettings)


    def onOptimizationProgress(self, data):
        if data.startswith("Evaluation"):
            self.__currentEvals += 1
            val = int((self.__currentEvals / self.__totalEvals) * 100)
            self.__progressBar.setValue(val)

    def onRunComplete(self, data):
        self.__progressBar.setMaximum(100)
        self.__progressBar.setValue(100)
        self.__textArea.appendPlainText("Predictions: " + data + "\n")
        self.__textArea.appendPlainText("Pipeline run complete.")
        self.__btn.setText("Close")



def parse_optimization_output(text: str):
    results_data = {}

    accuracy = re.search(r"Accuracy:\s*([0-9.]+)", text)
    precision = re.search(r"Precision:\s*([0-9.]+)", text)
    f1_score = re.search(r"F1[-\s]?score:\s*([0-9.]+)", text)
    kappa = re.search(r"(?:Cohen's\s+kappa|Kappa):\s*([0-9.]+)", text)

    results_data["accuracy"] = float(accuracy.group(1)) if accuracy else 0.0
    results_data["precision"] = float(precision.group(1)) if precision else 0.0
    results_data["f1_score"] = float(f1_score.group(1)) if f1_score else 0.0
    results_data["kappa"] = float(kappa.group(1)) if kappa else 0.0

    return results_data
