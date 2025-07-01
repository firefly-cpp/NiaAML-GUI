from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QFileDialog
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag , QIcon, QPixmap
import os

class ComponentSidebar(QWidget):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.setFixedWidth(220)
        layout = QVBoxLayout(self)

        title = QLabel("Drag Components:")
        title.setStyleSheet("color: white; font-weight: bold; padding: 5px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.listWidget = QListWidget(self)

        items_with_icons = {
            "Select CSV File": "file.png",
            "Categorical Encoder": "encode.png",
            "Missing Imputer": "imputation.png",
            "Feature Selection": "feature_selection.png",
            "Feature Transform": "feature_transformation.png",
            "Classifier": "classifier.png",
            "Optimization Algorithm": "placeholder.png",
            "Fitness Function": "placeholder.png",
            "Pipeline Output Folder": "folder.png",
            "Optimization Algorithm (Selection)": "placeholder.png",
            "Optimization Algorithm (Tuning)": "placeholder.png",
            "Population Size (Components Selection)": "placeholder.png",
            "Population Size (Parameter Tuning)": "placeholder.png",
            "Number of Evaluations (Component Selection)": "placeholder.png",
            "Number of Evaluations (Parameter Tuning)": "placeholder.png"
        }

        icon_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "icons")
        
        for label_text, icon_name in items_with_icons.items():
            icon_path = os.path.join(icon_dir, icon_name)
            if not os.path.exists(icon_path):
                icon_path = os.path.join(icon_dir, "placeholder.png")
           # print("Looking for icon at:", icon_path)
            
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, label_text)
            widget = QWidget()
            h_layout = QHBoxLayout(widget)
            h_layout.setContentsMargins(5, 2, 5, 2)

            icon_label = QLabel()
            icon_label.setPixmap(QPixmap(icon_path).scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            h_layout.addWidget(icon_label)

            text_label = QLabel(label_text)
            text_label.setWordWrap(True)
            text_label.setStyleSheet("color: white;")
            text_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            h_layout.addWidget(text_label)

            widget.setLayout(h_layout)
            item.setSizeHint(widget.sizeHint())
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, widget)

        self.listWidget.setDragEnabled(True)
        self.listWidget.mouseMoveEvent = self._wrapped_start_drag
        self.listWidget.itemClicked.connect(self.handle_click)

        layout.addWidget(self.listWidget)
        self.setLayout(layout)

    def _wrapped_start_drag(self, event):
        item = self.listWidget.itemAt(event.pos())
        if not item:
            return

        text = item.data(Qt.ItemDataRole.UserRole)

        mime = QMimeData()
        mime.setText(text)
        drag = QDrag(self.listWidget)
        drag.setMimeData(mime)
        drag.exec()
        print(f"START DRAG: {item.text()}")
    
    def handle_click(self, item):
        label = item.data(Qt.ItemDataRole.UserRole)
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