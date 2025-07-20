from pathlib import Path
import sys
import os
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication, QWidget, QHBoxLayout
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QSize
from niaaml_gui.widgets.pipeline_canvas import PipelineCanvas
from niaaml_gui.widgets.sidebar import ComponentSidebar
from niaaml_gui.windows.process_window import ProcessWindow
from niaaml_gui.windows.threads.optimize_thread import OptimizeThread
from niaaml_gui.widgets.pipeline_controls import PipelineControlsWidget
from niaaml_gui.process_window_data import ProcessWindowData
from niaaml.classifiers import ClassifierFactory
from niaaml.preprocessing.feature_selection import FeatureSelectionAlgorithmFactory
from niaaml.preprocessing.feature_transform import FeatureTransformAlgorithmFactory
from niaaml.preprocessing.feature_selection import FeatureSelectionAlgorithmFactory
from niaaml.preprocessing.feature_transform import FeatureTransformAlgorithmFactory
from niaaml.fitness import FitnessFactory
from niaaml.preprocessing.encoding import EncoderFactory
from niaaml.preprocessing.imputation import ImputerFactory
from niapy.util.factory import _algorithm_options
import pandas as pd
from niaaml_gui.utils.pipeline_runner import run_pipeline as nia_run


class MainAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(1024, 768))
        self.setWindowTitle("NiaAML - GUI")

        # Menu
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu("&File")
        helpMenu = menuBar.addMenu("&Help")

        exitAction = QAction(text="Exit", parent=self)
        exitAction.triggered.connect(QApplication.quit)
        fileMenu.addAction(exitAction)

        # Layout
        centralWidget = QWidget(self)
        mainLayout = QHBoxLayout(centralWidget)

        self.pipelineCanvas = PipelineCanvas()
        self.sidebar = ComponentSidebar(self.pipelineCanvas)
        self.controls = PipelineControlsWidget()

        self.controls.runClicked.connect(self.run_pipeline)
        self.controls.resetClicked.connect(self.reset_pipeline)
        self.pipelineCanvas.pipelineStateChanged.connect(self.validate_pipeline_ready)
        self._update_run_button_state()  

        mainLayout.addWidget(self.sidebar)
        mainLayout.addWidget(self.pipelineCanvas)
        mainLayout.addWidget(self.controls)

        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        # Napake
        self.errorMessage = QMessageBox()
        self.errorMessage.setIcon(QMessageBox.Icon.Critical)
        self.errorMessage.setWindowTitle("Error")
        self.errorMessage.setStandardButtons(QMessageBox.StandardButton.Ok)

    def run_pipeline(self):
        blocks = self.pipelineCanvas.block_data
        if not blocks:
            self.errorMessage.setText("Pipeline is empty!")
            self.errorMessage.exec()
            return

        data = {}
        has_header = True 
        encoder_map = EncoderFactory().get_name_to_classname_mapping()
        imputer_map = ImputerFactory().get_name_to_classname_mapping()
        fitness_map = FitnessFactory().get_name_to_classname_mapping()
        opt_algo_map = _algorithm_options()
        fs_map = FeatureSelectionAlgorithmFactory().get_name_to_classname_mapping()
        ft_map = FeatureTransformAlgorithmFactory().get_name_to_classname_mapping()
        clf_map = ClassifierFactory().get_name_to_classname_mapping()

        for block, info in blocks.items():
            label = info["label"]

            if hasattr(block, "get_value"):
                value = block.get_value()
            elif hasattr(block, "dropdown"):
                value = block.dropdown.currentText()
            else:
                value = info.get("path") or getattr(block, "value", None)
 
            if label == "Categorical Encoder":
                value = encoder_map.get(value.strip(), value)
            elif label == "Missing Imputer":
                value = imputer_map.get(value.strip(), value)
            elif label == "Fitness Function":
                value = fitness_map.get(value.strip(), value)
            elif label in [
                "Optimization Algorithm (Selection)",
                "Optimization Algorithm (Tuning)",
            ]:
                rev = {v: k for k, v in opt_algo_map.items()}
                value = rev.get(value.strip(), value)
            elif label == "Feature Selection":
                value = "\n".join(
                    fs_map.get(v.strip(), v) for v in value.split("\n") if v.strip()
                )
            elif label == "Feature Transform":
                value = "\n".join(
                    ft_map.get(v.strip(), v) for v in value.split("\n") if v.strip()
                )
            elif label == "Classifier":
                value = "\n".join(
                    clf_map.get(v.strip(), v) for v in value.split("\n") if v.strip()
                )
            if label == "Select CSV File":
                if hasattr(block, "checkbox"):
                    has_header = block.checkbox.isChecked()
                data["csvSrc"] = value
            else:
                data[label] = value
                
        data["csvHasHeader"] = has_header
        self.currentPipelineData = ProcessWindowData.from_dict(data)


        
        self._processWindow = ProcessWindow(
            parent=self,
            data=self.currentPipelineData,
            pipelineSettings={                 
                "classifiers": self.currentPipelineData.classifiers.split("\n"),
                "fs_algorithms": self.currentPipelineData.fsas.split("\n"),
                "ft_algorithms": self.currentPipelineData.ftas.split("\n"),
            },
        )
        self._processWindow.show()        
    
        # nia_run(
        #     csv_path=self.currentPipelineData.csvSrc,
        #     has_header=self.currentPipelineData.csvHasHeader,
        #     contains_classes=True,
        #     ignore_cols=[],
        #     fitness_name=self.currentPipelineData.fitnessFunctionName,
        #     pop_size=int(self.currentPipelineData.popSize or 20),
        #     inner_pop=int(self.currentPipelineData.popSizeInner or 20),
        #     evals=int(self.currentPipelineData.numEvals or 200),
        #     inner_evals=int(self.currentPipelineData.numEvalsInner or 200),
        #     opt_alg=self.currentPipelineData.optAlgName or "BatAlgorithm",
        #     classifiers=self.currentPipelineData.classifiers.split("\n"),
        #     fs_algorithms=self.currentPipelineData.fsas.split("\n"),
        #     ft_algorithms=self.currentPipelineData.ftas.split("\n"),
        #     log_fn=lambda *_: None,
        #     save_path=Path(self.currentPipelineData.outputFolder, "niaamlGUIoutput"),
        # )

    def reset_pipeline(self):
        self.pipelineCanvas.scene.clear()
        self.pipelineCanvas.block_data.clear()
        self.currentPipelineData = None

    def show_optimization_result(self, result_text):
        QMessageBox.information(self, "Pipeline Finished", result_text)
        
    def validate_pipeline_ready(self):
        all_valid = True
        for block, info in self.pipelineCanvas.block_data.items():
            label = info.get("label", "")
            if hasattr(block, "get_value"):
                value = block.get_value()
            elif hasattr(block, "dropdown"):
                value = block.dropdown.currentText()
            else:
                value = info.get("path") or getattr(block, "value", None)

            if not value or (isinstance(value, str) and not value.strip()):
                all_valid = False
                break

        self.controls.setRunEnabled(all_valid)

    def _update_run_button_state(self):
        ready = self.pipelineCanvas.is_pipeline_ready()
        self.controls.run_button.setEnabled(ready)

def run():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    style_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.qss")
    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            style_sheet = f.read()
            app.setStyleSheet(style_sheet)
            print("styles.qss loaded and applied.")
    else:
        print("styles.qss NOT found!")

    mainWin = MainAppWindow()
    mainWin.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
