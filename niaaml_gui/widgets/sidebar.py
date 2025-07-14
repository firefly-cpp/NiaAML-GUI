from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QHBoxLayout,
    QFileDialog, QToolBox
)
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDrag, QPixmap
import os


class ComponentSidebar(QWidget):
    """Verzija, kjer je vsak zavihek prikazan eden pod drugim z uporabo QToolBox.
    Logika metod in MIME ostane nespremenjena.
    """

    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self._base_width = 220
        self._item_height = 30

        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignmentFlag.AlignTop)
        root.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Drag Components:")
        title.setStyleSheet("color: white; font-weight: bold; padding: 5px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)
        root.addSpacing(6)

        from PyQt6.QtWidgets import QToolBox
        self.tabs = QToolBox(self)
        root.addWidget(self.tabs)

        self.listWidget = None

        categories = {
            "Data": {
                "Select CSV File": "file.png",
                "Pipeline Output Folder": "folder.png",
            },
            "Pre‑processing": {
                "Categorical Encoder": "encode.png",
                "Missing Imputer": "imputation.png",
            },
            "Feature Engineering": {
                "Feature Selection": "feature_selection.png",
                "Feature Transform": "feature_transformation.png",
            },
            "Modeling": {
                "Classifier": "classifier.png",
                "Optimization Algorithm": "optimization_algorithm.png",
                "Optimization Algorithm (Selection)": "optimization_algorithm.png",
                "Optimization Algorithm (Tuning)": "decision_tree.png",
            },
            "Fitness": {
                "Fitness Function": "fitness.png",
            },
            "Number of evaluations": {
                "Number of Evaluations (Component Selection)": "numbers.png",
                "Number of Evaluations (Parameter Tuning)": "numbers.png",
            },
            "Population Size": {
                "Population Size (Components Selection)": "numbers.png",
                "Population Size (Parameter Tuning)": "numbers.png",
            },
        }

        icon_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "icons")

        for cat_name, items in categories.items():
            lst = QListWidget()
            lst.setSpacing(2)
            lst.setDragEnabled(True)
            lst.mouseMoveEvent = self._wrapped_start_drag
            lst.itemClicked.connect(self.handle_click)

            for label, icon_file in items.items():
                icon_path = os.path.join(icon_dir, icon_file)
                if not os.path.exists(icon_path):
                    icon_path = os.path.join(icon_dir, "placeholder.png")

                item = QListWidgetItem()
                item.setData(Qt.ItemDataRole.UserRole, label)

                widget = QWidget()
                hlyt = QHBoxLayout(widget)
                hlyt.setContentsMargins(5, 2, 5, 2)

                icon_lbl = QLabel()
                icon_lbl.setPixmap(
                    QPixmap(icon_path).scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                )
                hlyt.addWidget(icon_lbl)

                text_lbl = QLabel(label)
                text_lbl.setWordWrap(True)
                text_lbl.setStyleSheet("color: white;")
                text_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                hlyt.addWidget(text_lbl)

                widget.setLayout(hlyt)
                item.setSizeHint(widget.sizeHint())
                lst.addItem(item)
                lst.setItemWidget(item, widget)

            self.tabs.addItem(lst, cat_name)

        self.listWidget = self.tabs.currentWidget()
        self.tabs.currentChanged.connect(self._on_tab_changed)
        self._adjust_width()

    def _on_tab_changed(self, idx: int):
        self.listWidget = self.tabs.widget(idx)
        self._adjust_width()

    def _wrapped_start_drag(self, event):
        item = self.listWidget.itemAt(event.pos()) if self.listWidget else None
        if not item:
            return
        text = item.data(Qt.ItemDataRole.UserRole)
        mime = QMimeData()
        mime.setText(text)
        drag = QDrag(self.listWidget)
        drag.setMimeData(mime)
        drag.exec()

    def handle_click(self, item):
        label = item.data(Qt.ItemDataRole.UserRole)
        if label == "Select CSV File":
            path, _ = QFileDialog.getOpenFileName(
                self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)"
            )
            if path:
                self.canvas.add_config_block("CSV File", [], value=path)
        elif label == "Pipeline Output Folder":
            path = QFileDialog.getExistingDirectory(self, "Select Output Folder", "")
            if path:
                self.canvas.add_config_block("Output Folder", [], value=path)

    def _adjust_width(self):
        if not self.listWidget:
            return
        self.setFixedWidth(self._base_width)

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
