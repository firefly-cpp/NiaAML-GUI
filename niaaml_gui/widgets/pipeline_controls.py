from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import pyqtSignal

class PipelineControlsWidget(QWidget):
    runClicked = pyqtSignal()
    resetClicked = pyqtSignal()
    savePipelineClicked = pyqtSignal()
    loadPipelineClicked = pyqtSignal()
    exportPipelineClicked = pyqtSignal()
    validatePipelineClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        self.run_button = QPushButton("▶ Run Pipeline")
        self.run_button.setObjectName("run_button")
        self.run_button.clicked.connect(self.runClicked.emit)
        self.setRunEnabled(False)
        layout.addWidget(self.run_button)
        
        self.reset_button = QPushButton("🔄 Reset Pipeline")
        self.reset_button.clicked.connect(self.resetClicked.emit)
        layout.addWidget(self.reset_button)

        self.save_button = QPushButton("💾 Save Pipeline")
        self.save_button.clicked.connect(self.savePipelineClicked.emit)
        layout.addWidget(self.save_button)

        self.load_button = QPushButton("📂 Load Pipeline")
        self.load_button.clicked.connect(self.loadPipelineClicked.emit)
        layout.addWidget(self.load_button)

        self.export_button = QPushButton("📤 Export Results")
        self.export_button.clicked.connect(self.exportPipelineClicked.emit)
        layout.addWidget(self.export_button)

        layout.addStretch()

    def setRunEnabled(self, enabled: bool):
        self.run_button.setEnabled(enabled)
        
        if enabled:
            self.run_button.setStyleSheet("""
                QPushButton {
                    background-color: #008569;
                    color: white;
                    border: 1px solid #006f59;
                    border-radius: 6px;
                    padding: 5px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #001D85;
                }
            """)
        else:
            self.run_button.setStyleSheet("""
                QPushButton {
                    background-color: #444;
                    color: #aaa;
                    border: 1px solid #222;
                    border-radius: 6px;
                    padding: 5px;
                    font-weight: 600;
                }
            """)
