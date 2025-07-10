import os
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QGraphicsItem, QFileDialog, QLineEdit, QGraphicsProxyWidget, QComboBox, QGraphicsPixmapItem, QCheckBox
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QIntValidator, QFontMetricsF, QPixmap
from PyQt6.QtCore import Qt
from niaaml.classifiers import ClassifierFactory
from niaaml.preprocessing.feature_transform import FeatureTransformAlgorithmFactory
from niaaml_gui.widgets.multi_selection_dialog import MultiSelectDialog
from niaaml.preprocessing.feature_selection import FeatureSelectionAlgorithmFactory
from niaaml.fitness import FitnessFactory
from niaaml.preprocessing.encoding import EncoderFactory
from niaaml.preprocessing.imputation import ImputerFactory
from niapy.util.factory import _algorithm_options


class PipelineCanvas(QGraphicsView):
    __niaamlFitnessFunctions = FitnessFactory().get_name_to_classname_mapping()
    __niaamlEncoders = EncoderFactory().get_name_to_classname_mapping()
    __niaamlImputers = ImputerFactory().get_name_to_classname_mapping()
    __niapyAlgorithmsList = list(_algorithm_options().keys())   
    __niaamlFitnessFunctionsList = list(__niaamlFitnessFunctions.keys())
    __niaamlEncodersList = list(__niaamlEncoders.keys())
    __niaamlImputersList = list(__niaamlImputers.keys())
    
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
        
    def get_value(self):
        return self.value
    
    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            text = event.mimeData().text()
            pos = self.mapToScene(int(event.position().x()), int(event.position().y()))
            self.add_config_block(text, pos.x(), pos.y())
            event.acceptProposedAction()

    def add_config_block(self, label: str, x: int = 50, y: int = 50):
        is_file = label == "Select CSV File"
        is_folder = label == "Pipeline Output Folder"
        is_number_input = label in [
            "Population Size (Components Selection)",
            "Population Size (Parameter Tuning)",
            "Number of Evaluations (Component Selection)",
            "Number of Evaluations (Parameter Tuning)"
        ]

        dropdown_options = []
        if label == "Missing Imputer":
            dropdown_options = self.__niaamlImputersList
        elif label == "Categorical Encoder":
            dropdown_options = self.__niaamlEncodersList
        elif label in ["Optimization Algorithm (Selection)", "Optimization Algorithm (Tuning)"]:
            dropdown_options = self.__niapyAlgorithmsList
        elif label == "Fitness Function":
            dropdown_options = self.__niaamlFitnessFunctionsList

        icon_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "icons")
        icon_map = {
            "Select CSV File": "file.png",
            "Categorical Encoder": "encode.png",
            "Missing Imputer": "imputation.png",
            "Feature Selection": "feature_selection.png",
            "Feature Transform": "feature_transformation.png",
            "Classifier": "classifier.png",
            "Optimization Algorithm": "optimization_algorithm.png",
            "Fitness Function": "fitness.png",
            "Pipeline Output Folder": "folder.png",
            "Optimization Algorithm (Selection)": "optimization_algorithm.png",
            "Optimization Algorithm (Tuning)": "decision_tree.png",
            "Population Size (Components Selection)": "numbers.png",
            "Population Size (Parameter Tuning)": "numbers.png",
            "Number of Evaluations (Component Selection)": "numbers.png",
            "Number of Evaluations (Parameter Tuning)": "numbers.png"
        }
        icon_path = os.path.join(icon_dir, icon_map.get(label, "placeholder.png"))

        if is_number_input:
            block = NumericInputBlock(label, icon_path=icon_path)
        elif dropdown_options:
            block = InteractiveConfigBlock(label, dropdown_options=dropdown_options, icon_path=icon_path)
        else:
            block = InteractiveConfigBlock(label, is_file=is_file, is_folder=is_folder, icon_path=icon_path)


        block.setPos(x, y)
        self.scene.addItem(block)
        self.block_data[block] = {'label': label, 'path': None}
         
    def handle_block_click(self, block):
        label = block.label

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
    __niaamlFeatureSelectionAlgorithmsMap = FeatureSelectionAlgorithmFactory().get_name_to_classname_mapping()
    __niaamlFeatureTransformAlgorithmsMap = FeatureTransformAlgorithmFactory().get_name_to_classname_mapping()
    __niaamlClassifiersMap = ClassifierFactory().get_name_to_classname_mapping()

    __niaamlFeatureSelectionDisplayOptions = list(__niaamlFeatureSelectionAlgorithmsMap.keys())
    __niaamlFeatureTransformDisplayOptions = list(__niaamlFeatureTransformAlgorithmsMap.keys())
    __niaamlClassifiersDisplayOptions = list(__niaamlClassifiersMap.keys())

    def __init__(self, label: str, value: str = "", is_file: bool = False, is_folder: bool = False, is_number_input: bool = False, dropdown_options=None, icon_path: str = None):
        self.icon_path = icon_path
        self.label = label
        self.value = value
        self.is_file = is_file
        self.is_folder = is_folder
        self.is_number_input = is_number_input
        self.dropdown_options = dropdown_options or []
        self.selected_options = []

        # Dummy values to measure
        temp_combo = QComboBox()
        temp_combo.addItems(self.dropdown_options)
        combo_width = temp_combo.sizeHint().width() if self.dropdown_options else 0

        block_width = max(220, combo_width + 20)  
        block_height = 80  

        super().__init__(0, 0, block_width, block_height)

        self.setBrush(QBrush(QColor("#005f85")))
        self.setPen(QPen(QColor("white")))
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)

        # ICON
        label_x_offset = 10
        if self.icon_path and os.path.exists(self.icon_path):
            pixmap = QPixmap(self.icon_path).scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.icon_item = QGraphicsPixmapItem(self)
            self.icon_item.setPixmap(pixmap)
            self.icon_item.setOffset(5, 5)
            label_x_offset = 30

        # LABEL
        self.label_item = QGraphicsTextItem(self)
        self.label_item.setDefaultTextColor(QColor("white"))
        self.label_item.setPlainText(self.label)
        self.label_item.setPos(label_x_offset, 5)

        current_y = 30

        # DROPDOWN
        if self.dropdown_options:
            self.dropdown = QComboBox()
            self.dropdown.addItems(self.dropdown_options)
            self.proxy = QGraphicsProxyWidget(self)
            self.proxy.setWidget(self.dropdown)
            self.proxy.setPos(10, current_y)
            current_y += self.dropdown.sizeHint().height() + 10

        elif self.is_number_input:
            self.input_field = QLineEdit()
            self.input_field.setValidator(QIntValidator(0, 999999))
            self.input_field.setFixedWidth(100)
            self.input_field.setText(self.value)
            self.proxy = QGraphicsProxyWidget(self)
            self.proxy.setWidget(self.input_field)
            self.proxy.setPos(10, current_y)
            current_y += self.input_field.sizeHint().height() + 10

        else:
            self.value_item = QGraphicsTextItem(self)
            self.value_item.setDefaultTextColor(QColor("white"))
            self.value_item.setPlainText("Click to select...")
            self.value_item.setPos(10, current_y)
            current_y += 30

        # CSV CHECKBOX
        if self.is_file and self.label == "Select CSV File":
            self.csvHasHeader = True
            cb = QCheckBox("Has Header")
            cb.setChecked(True)
            proxy = QGraphicsProxyWidget(self)
            proxy.setWidget(cb)
            cb_width = cb.sizeHint().width()
            proxy.setPos(block_width - cb_width - 5, 5)

            cb.stateChanged.connect(
                lambda state: setattr(self, "csvHasHeader", state == Qt.CheckState.Checked)
            )

        # Update block height
        self.setRect(0, 0, block_width, max(80, current_y + 10))
            
    def _add_dropdown(self, x, y):
        self.dropdown = QComboBox()
        self.dropdown.addItems(self.dropdown_options)
        proxy = QGraphicsProxyWidget(self)
        proxy.setWidget(self.dropdown)
        proxy.setPos(x, y)

    def _add_number_input(self, x, y):
        le = QLineEdit()
        le.setValidator(QIntValidator(0, 999999))
        le.setFixedWidth(100)
        proxy = QGraphicsProxyWidget(self)
        proxy.setWidget(le)
        proxy.setPos(x, y)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            local_pos = event.pos()
            if 40 <= local_pos.y() <= 80 and not self.is_number_input:
                if self.label in ["Feature Selection", "Feature Transform", "Classifier"]:
                    self.getMultiSelection()
                elif self.is_file or self.is_folder:
                    self.getPath()
            else:
                super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)

    def getPath(self):
        if self.is_file:
            path, _ = QFileDialog.getOpenFileName(None, "Select File", "", "CSV Files (*.csv);;All Files (*)")
            if path:
                self.value = path
                self.update_value_display()
        elif self.is_folder:
            folder = QFileDialog.getExistingDirectory(None, "Select Folder")
            if folder:
                self.value = folder
                self.update_value_display()

    def getMultiSelection(self):
        # Mape za prikaz → class name
        if self.label == "Feature Selection":
            display_options = self.__niaamlFeatureSelectionDisplayOptions
            mapping = self.__niaamlFeatureSelectionAlgorithmsMap
        elif self.label == "Feature Transform":
            display_options = self.__niaamlFeatureTransformDisplayOptions
            mapping = self.__niaamlFeatureTransformAlgorithmsMap
        elif self.label == "Classifier":
            display_options = self.__niaamlClassifiersDisplayOptions
            mapping = self.__niaamlClassifiersMap
        else:
            display_options = []
            mapping = {}

        dialog = MultiSelectDialog(f"Select {self.label}(s)", display_options)
        if dialog.exec():
            selected_display_items = dialog.selected_items()
            #  prikaz → class name
            self.selected_options = [mapping[disp] for disp in selected_display_items if disp in mapping]
            display_text = "\n".join(selected_display_items)
            self.value_item.setPlainText(display_text)
            self.value = "\n".join(self.selected_options)

            new_height = InteractiveConfigBlock.calculate_block_height(display_text)
            self.setRect(0, 0, self.rect().width(), new_height)
            self.value_item.setTextWidth(self.rect().width() - 20)


    def update_value_display(self):
        if hasattr(self, "value_item"):
            if self.selected_options:
                value_text = "\n".join(self.selected_options)
            elif self.value:
                value_text = self.value
            else:
                value_text = "Click to select..."

            self.value_item.setPlainText(value_text)
            self.value_item.setTextWidth(self.rect().width() - 20)

            # Recalc and update block height
            new_height = InteractiveConfigBlock.calculate_block_height(value_text)
            self.setRect(0, 0, self.rect().width(), new_height)

    @staticmethod
    def calculate_block_height(text: str, width: int = 200, base_height: int = 70) -> int:
        fm = QFontMetricsF(QGraphicsTextItem().font())
        line_h = fm.lineSpacing()
        lines = text.split("\n")
        total = 0
        for ln in lines:
            w = fm.horizontalAdvance(ln)
            total += max(1, int(w / width) + 1)
        h = 30 + total * line_h + 20
        return max(base_height, int(h))

            
class NumericInputBlock(QGraphicsRectItem):
    def __init__(self, label: str, icon_path: str = None):
        super().__init__(0, 0, 220, 70)
        self.label = label
        self.icon_path = icon_path
        
        self.setBrush(QBrush(QColor("#005f85")))
        self.setPen(QPen(QColor("white")))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        
        if self.icon_path and os.path.exists(self.icon_path):
            pixmap = QPixmap(self.icon_path).scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.icon_item = QGraphicsPixmapItem(self)
            self.icon_item.setPixmap(pixmap)
            self.icon_item.setOffset(5, 5)      
        
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
