from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QFileDialog
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag

class ComponentSidebar(QWidget):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.setFixedWidth(200)
        layout = QVBoxLayout(self)
        
        title = QLabel("Drag Components:")
        title.setStyleSheet("color: white; font-weight: bold; padding: 5px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        self.listWidget = QListWidget(self)
        for item_text in [
            "Select CSV File",
            "Categorical Encoder",
            "Missing Imputer",
            "Feature Selection",
            "Feature Transform",
            "Classifier",
            "Optimization Algorithm",
            "Fitness Function",
            "Pipeline Output Folder",
            "Optimization Algorithm (Selection)",
            "Optimization Algorithm (Tuning)",
            "Population Size (Components Selection)",
            "Population Size (Parameter Tuning)",
            "Number of Evaluations (Component Selection)",
            "Number of Evaluations (Parameter Tuning)",
        ]:
            item = QListWidgetItem()
            label = QLabel(item_text)
            label.setWordWrap(True)
            label.setStyleSheet("color: white; padding: 5px;")
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, label)
            item.setSizeHint(label.sizeHint())

        self.listWidget.setDragEnabled(True)
        self.listWidget.mouseMoveEvent = self._wrapped_start_drag
        self.listWidget.itemClicked.connect(self.handle_click)
        
        layout.addWidget(self.listWidget)
        self.setLayout(layout)

    def _wrapped_start_drag(self, event):
        item = self.listWidget.itemAt(event.pos())
        if not item:
            return

        widget = self.listWidget.itemWidget(item)
        text = widget.text() if isinstance(widget, QLabel) else item.text()

        mime = QMimeData()
        mime.setText(text)
        drag = QDrag(self.listWidget)
        drag.setMimeData(mime)
        drag.exec()
        print(f"START DRAG: {item.text()}")
    
    def handle_click(self, item):
        label = item.text()
        if label == "Select CSV File":
            path, _ = QFileDialog.getOpenFileName(
                self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)"
            )
            if path:
                print(f"Selected CSV: {path}")
                self.canvas.add_config_block("CSV File", [], value=path)
        elif label == "Pipeline Output Folder":
            path = QFileDialog.getExistingDirectory(
                self, "Select Output Folder", ""
            )
            if path:
                print(f"Selected Folder: {path}")
                self.canvas.add_config_block("Output Folder", [], value=path)
                
    def dropEvent(self, event):
        if event.mimeData().hasText():
            label = event.mimeData().text()
            drop_pos = self.mapToScene(event.position().toPoint())
            self.add_config_block(label, x=drop_pos.x(), y=drop_pos.y())
            event.acceptProposedAction()
            
    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()