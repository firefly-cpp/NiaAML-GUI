import os
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QGraphicsItem, QFileDialog, QLineEdit, QGraphicsProxyWidget
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QIntValidator
from PyQt6.QtCore import Qt
from niaaml.classifiers import ClassifierFactory
from niaaml.preprocessing.feature_selection import FeatureSelectionAlgorithmFactory
from niaaml.preprocessing.feature_transform import FeatureTransformAlgorithmFactory

from niaaml_gui.widgets.multi_selection_dialog import MultiSelectDialog

class PipelineCanvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setAcceptDrops(True)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setAcceptDrops(True)
        self.block_data = {}
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        print("DRAG ENTER")

    def dragMoveEvent(self, event):
        event.acceptProposedAction()
        print("DRAG MOVE")

    def dropEvent(self, event):
        print("DROP")
        if event.mimeData().hasText():
            text = event.mimeData().text()
            print(f"Dropped text: {text}")
            pos = self.mapToScene(int(event.position().x()), int(event.position().y()))
            self.add_config_block(text, pos.x(), pos.y())
            event.acceptProposedAction()

    def add_config_block(self, label: str, x: int = 50, y: int = 50):
        print("configblock")
        is_file = label == "Select CSV File"
        is_folder = label == "Pipeline Output Folder"

        numeric_labels = [
            "Population Size (Components Selection)",
            "Population Size (Parameter Tuning)",
            "Number of Evaluations (Component Selection)",
            "Number of Evaluations (Parameter Tuning)"
        ]

        if label in numeric_labels:
            block = NumericInputBlock(label)
        else:
            block = InteractiveConfigBlock(label, is_file=is_file, is_folder=is_folder)

        block.setPos(x, y)
        self.scene.addItem(block)
        self.block_data[block] = {'label': label, 'path': None}
         
    def handle_block_click(self, block):
        label = block.label_text

        if "file" in label.lower():
            path, _ = QFileDialog.getOpenFileName(self, "Select File")
            if path:
                self.block_data[block] = {
                    'label': label,
                    'path': path
                }
                block.path_display.setPlainText(os.path.basename(path))

        elif "folder" in label.lower():
            path = QFileDialog.getExistingDirectory(self, "Select Folder")
            if path:
                self.block_data[block] = {
                    'label': label,
                    'path': path
                }
                block.path_display.setPlainText(os.path.basename(path))

        else:
            pass
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            for item in self.scene.selectedItems():
                self.scene.removeItem(item)
        else:
            super().keyPressEvent(event)
        

class InteractiveConfigBlock(QGraphicsRectItem):
    def __init__(self, label: str, value: str = "", is_file: bool = False, is_folder: bool = False, is_number_input: bool = False):
        super().__init__(0, 0, 220, 70)
        self.label = label
        self.value = value
        self.is_file = is_file
        self.is_folder = is_folder
        self.is_number_input = is_number_input

        self.setBrush(QBrush(QColor("#005f85")))
        self.setPen(QPen(QColor("white")))
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)

        self.label_item = QGraphicsTextItem(self)
        self.label_item.setDefaultTextColor(QColor("white"))
        self.label_item.setTextWidth(200)
        self.label_item.setPlainText(self.label)
        self.label_item.setPos(10, 5)

        self.value_item = QGraphicsTextItem(self.value or "Click to select...", self)
        self.value_item.setDefaultTextColor(QColor("white"))
        self.value_item.setPos(10, 30)
        self.value_item.setTextWidth(self.rect().width() - 20)

        if self.is_number_input:
            self.input_field = QLineEdit()
            self.input_field.setValidator(QIntValidator(0, 999999))  # ali karkoli ustreznega
            self.input_field.setFixedWidth(100)
            self.input_field.setText(self.value)

            self.proxy = QGraphicsProxyWidget(self)
            self.proxy.setWidget(self.input_field)
            self.proxy.setPos(10, 30)
        else:
            self.value_item = QGraphicsTextItem(self.value or "Click to select...", self)
            self.value_item.setDefaultTextColor(QColor("white"))
            self.value_item.setPos(10, 30)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            local_pos = event.pos()
            if 30 <= local_pos.y() <= 60:
                if self.label in ["Feature Selection", "Feature Transform", "Classifier"]:
                    self.getMultiSelection()
                elif self.is_file or self.is_folder:
                    self.getPath()
                else:
                    pass  
            else:
                super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)

    def getPath(self):
        if self.is_file:
            path, _ = QFileDialog.getOpenFileName(None, "Select File", "", "CSV Files (*.csv);;All Files (*)")
            if path:
                self.value = path
                self.value_item.setPlainText(path)
        elif self.is_folder:
            folder = QFileDialog.getExistingDirectory(None, "Select Folder")
            if folder:
                self.value = folder
                self.value_item.setPlainText(folder)

    def getMultiSelection(self):
        if self.label == "Feature Selection":
            options = list(FeatureSelectionAlgorithmFactory().get_name_to_classname_mapping().keys())
        elif self.label == "Feature Transform":
            options = list(FeatureTransformAlgorithmFactory().get_name_to_classname_mapping().keys())
        elif self.label == "Classifier":
            options = list(ClassifierFactory().get_name_to_classname_mapping().keys())
        else:
            options = []

        dialog = MultiSelectDialog(f"Select {self.label}(s)", options)
        if dialog.exec():
            selected = dialog.selected_items()
            self.value = selected
            self.value_item.setPlainText(", ".join(selected))
            
class NumericInputBlock(QGraphicsRectItem):
    def __init__(self, label: str):
        super().__init__(0, 0, 220, 70)
        self.label = label

        self.setBrush(QBrush(QColor("#005f85")))
        self.setPen(QPen(QColor("white")))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.label_item = QGraphicsTextItem(self)
        self.label_item.setDefaultTextColor(QColor("white"))
        self.label_item.setTextWidth(200)
        self.label_item.setPlainText(self.label)
        self.label_item.setPos(10, 5)

        label_height = self.label_item.boundingRect().height()

        self.input_field = QLineEdit()
        self.input_field.setValidator(QIntValidator(0, 999999))
        self.input_field.setFixedWidth(100)

        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.input_field)

        self.proxy.setPos(10, 10 + label_height)

        total_height = 10 + label_height + self.input_field.sizeHint().height() + 10
        self.setRect(0, 0, 221, total_height)

    def get_value(self):
        return self.input_field.text()
