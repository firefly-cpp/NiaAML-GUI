import os

from PyQt6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsRectItem,
    QGraphicsTextItem,
    QGraphicsItem,
    QFileDialog,
    QLineEdit,
    QGraphicsProxyWidget,
    QComboBox,
    QGraphicsPixmapItem,
    QCheckBox,
    QPushButton,
    QMessageBox,
    QGraphicsEllipseItem,
    QGraphicsPathItem
)

from PyQt6.QtGui import (
    QPainter,
    QColor,
    QBrush,
    QPen,
    QIntValidator,
    QFontMetricsF,
    QPixmap,
    QIcon,
    QPainterPath
)

from PyQt6.QtCore import Qt, QSize, QPointF, QRectF, pyqtSignal

from niaaml.classifiers import ClassifierFactory
from niaaml.preprocessing.feature_transform import FeatureTransformAlgorithmFactory
from niaaml.preprocessing.feature_selection import FeatureSelectionAlgorithmFactory
from niaaml.preprocessing.encoding import EncoderFactory
from niaaml.preprocessing.imputation import ImputerFactory
from niaaml.fitness import FitnessFactory

from niapy.util.factory import _algorithm_options

from niaaml_gui.widgets.connection_line import ConnectionLine
from niaaml_gui.widgets.multi_selection_dialog import MultiSelectDialog
from niaaml_gui.windows.csv_editor_window import CSVEditorWindow

class PipelineCanvas(QGraphicsView):
    __niaamlFitnessFunctions = FitnessFactory().get_name_to_classname_mapping()
    __niaamlEncoders = EncoderFactory().get_name_to_classname_mapping()
    __niaamlImputers = ImputerFactory().get_name_to_classname_mapping()
    __niapyAlgorithmsList = list(_algorithm_options().keys())
    __niaamlFitnessFunctionsList = list(__niaamlFitnessFunctions.keys())
    __niaamlEncodersList = list(__niaamlEncoders.keys())
    __niaamlImputersList = list(__niaamlImputers.keys())
    
    pipelineStateChanged = pyqtSignal()
    
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
        self.current_connection_line = None
        self.pending_output_block = None
        self.line_start = None
        self._highlighted_circles = []
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setSceneRect(0, 0, 5000, 5000) 
        
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
        categories = {
            "Data": {
                "Select CSV File", "Pipeline Output Folder"
            },
            "Pre-processing": {
                "Categorical Encoder", "Missing Imputer"
            },
            "Feature Eng.": {
                "Feature Selection", "Feature Transform"
            },
            "Modeling": {
                "Classifier",
                "Optimization Algorithm (Selection)",
                "Optimization Algorithm (Tuning)"
            },
            "Population": {
                "Population Size (Components Selection)", "Population Size (Parameter Tuning)"
            },
            "Evaluation": {
                "Number of Evaluations (Component Selection)", "Number of Evaluations (Parameter Tuning)"
            },
            "Fitness": {
                "Fitness Function"
            }
        }
        def _category_for(lbl: str) -> str:
            for cat, items in categories.items():
                if lbl in items:
                    return cat
            return "Data"
        cat = _category_for(label)

        category_shapes = {
            "Data": "rounded",                      
            "Pre-processing": "cut-corner",        
            "Feature Eng.": "parallelogram",             
            "Modeling": "hexagon",                
            "Population": "octagon",               
            "Evaluation": "rounded",             
            "Fitness": "ellipse"                   
        }

        shape = category_shapes.get(cat, "rect")

        is_file = label == "Select CSV File"
        is_folder = label == "Pipeline Output Folder"
        is_number_input = label in [
            "Population Size (Components Selection)",
            "Population Size (Parameter Tuning)",
            "Number of Evaluations (Component Selection)",
            "Number of Evaluations (Parameter Tuning)",
        ]

        # dropdowni
        dropdown_options = []
        if label == "Missing Imputer":
            dropdown_options = self.__niaamlImputersList
        elif label == "Categorical Encoder":
            dropdown_options = self.__niaamlEncodersList
        elif label in [
            "Optimization Algorithm (Selection)",
            "Optimization Algorithm (Tuning)",
        ]:
            dropdown_options = self.__niapyAlgorithmsList
        elif label == "Fitness Function":
            dropdown_options = self.__niaamlFitnessFunctionsList

        # ikona
        icon_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "resources", "icons"
        )
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
            "Number of Evaluations (Parameter Tuning)": "numbers.png",
        }
        icon_path = os.path.join(icon_dir, icon_map.get(label, "placeholder.png"))

        if is_number_input:
            block = NumericInputBlock(label, icon_path=icon_path, shape=shape)
        elif dropdown_options:
            block = InteractiveConfigBlock(
                label, dropdown_options=dropdown_options, icon_path=icon_path, shape=shape
            )
        else:
            block = InteractiveConfigBlock(
                label, is_file=is_file, is_folder=is_folder,
                icon_path=icon_path, shape=shape
            )

        block.setPos(x, y)
        self.scene.addItem(block)
        self.block_data[block] = {"label": label, "path": None}
        self.pipelineStateChanged.emit()
        
        if hasattr(block, "input_field"):
            block.input_field.textChanged.connect(self.pipelineStateChanged.emit)
        elif hasattr(block, "dropdown"):
            block.dropdown.currentTextChanged.connect(self.pipelineStateChanged.emit)

    def handle_block_click(self, block):
        label = block.label

        if "file" in label.lower():
            path, _ = QFileDialog.getOpenFileName(self, "Select File")
            if path:
                self.block_data[block] = {"label": label, "path": path}
                block.path_display.setPlainText(os.path.basename(path))
            self.pipelineStateChanged.emit()

        elif "folder" in label.lower():
            path = QFileDialog.getExistingDirectory(self, "Select Folder")
            if path:
                self.block_data[block] = {"label": label, "path": path}
                block.path_display.setPlainText(os.path.basename(path))
            self.pipelineStateChanged.emit()

        else:
            pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            for item in self.scene.selectedItems():
                if isinstance(item, ConnectionLine):
                    if hasattr(item.source_block, "connections"):
                        if item in item.source_block.connections:
                            item.source_block.connections.remove(item)
                    if hasattr(item.target_block, "connections"):
                        if item in item.target_block.connections:
                            item.target_block.connections.remove(item)
                self.scene.removeItem(item)
            self.pipelineStateChanged.emit()
            
        else:
            super().keyPressEvent(event)


    def progress_start(self, maximum: int | None = None) -> None:
        if maximum is None:
            self._progressBar.setMaximum(0)
            self._progressBar.setTextVisible(False)
        else:
            self._progressBar.setMaximum(maximum)
            self._progressBar.setValue(0)
            self._progressBar.setTextVisible(True)

        r = self.sceneRect()
        self._progressBar.setGeometry(
            int(r.x()), int(r.bottom() - 22), int(r.width()), 18
        )
        self._progressBar.show()
        self.update()

    def progress_set(self, value: int) -> None:
        if self._progressBar.isVisible() and self._progressBar.maximum() != 0:
            self._progressBar.setValue(value)

    def progress_finish(self) -> None:
        self._progressBar.hide()
        
    def mousePressEvent(self, event):
        view_pos  = event.pos()               
        scene_pos = self.mapToScene(view_pos) 
        item = self.itemAt(view_pos)           

        if isinstance(item, QGraphicsEllipseItem):
            item = item.parentItem()

        if isinstance(item, (InteractiveConfigBlock, NumericInputBlock)):
            local = item.mapFromScene(scene_pos)
            if item.output_circle.contains(local):
                self.pending_output_block = item

                self.line_preview = QGraphicsPathItem()
                self.line_preview.setZValue(99)
                self.line_preview.setPen(QPen(QColor("black"), 2, Qt.PenStyle.DashLine))
                self.line_preview.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIgnoresTransformations)
                self.line_preview.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemDoesntPropagateOpacityToChildren)

                self.scene.addItem(self.line_preview)
                self.line_start = item.output_point()

                self._highlight_connection_targets(item)
                return  

        super().mousePressEvent(event)


    def mouseMoveEvent(self, event):
        if getattr(self, "line_preview", None):
            end = self.mapToScene(event.pos())
            path = QPainterPath()
            path.moveTo(self.line_start)
            dx = (end.x() - self.line_start.x()) * 0.5
            cp1 = QPointF(self.line_start.x() + dx, self.line_start.y())
            cp2 = QPointF(end.x() - dx, end.y())
            path.cubicTo(cp1, cp2, end)
            self.line_preview.setPath(path)
        else:
            super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        if getattr(self, "line_preview", None):
            self.scene.removeItem(self.line_preview)
            self.line_preview = None

        self._clear_connection_highlights()

        if self.pending_output_block:
            view_pos = event.pos()
            scene_pos = self.mapToScene(view_pos)
            item = self.scene.itemAt(scene_pos, self.transform())
            if isinstance(item, QGraphicsEllipseItem):
                item = item.parentItem()

            if isinstance(item, (InteractiveConfigBlock, NumericInputBlock))  and item is not self.pending_output_block:
                local = item.mapFromScene(scene_pos)
                if item.input_circle.contains(local):
                    if self._is_valid_connection(self.pending_output_block, item):
                        connection = ConnectionLine(self.pending_output_block, item)
                        self.scene.addItem(connection)
                        self.pending_output_block.add_connection(connection)
                        item.add_connection(connection)

            self.pending_output_block = None
            self.pipelineStateChanged.emit()

        else:
            super().mouseReleaseEvent(event)
            self.pipelineStateChanged.emit()

            
    def _is_valid_connection(self, source, target) -> bool:
        if source is target:
            return False
        source_label = getattr(source, "label", "").lower()
        target_label = getattr(target, "label", "").lower()
        if "csv" in source_label and not any(k in target_label for k in ["encoder", "imputer"]):
            return False
        for conn in source.connections:
            if conn.target_block is target:
                return False
        return True
    
    def _highlight_connection_targets(self, source_block):
        for item in self.scene.items():
            if item is source_block:
                continue

            if isinstance(item, (InteractiveConfigBlock, NumericInputBlock)):
                is_valid = self._is_valid_connection(source_block, item)
                color = QColor("green") if is_valid else QColor("red")
                item.input_circle.setBrush(QBrush(color))
                self._highlighted_circles.append(item.input_circle)


    def _clear_connection_highlights(self):
        for circle in self._highlighted_circles:
            circle.setBrush(QBrush(QColor("white")))
        self._highlighted_circles.clear()        
        
    def is_pipeline_ready(self) -> bool:
        for block, info in self.block_data.items():
            if hasattr(block, "get_value"):
                value = block.get_value()
                if not value or (isinstance(value, str) and not value.strip()):
                    return False
            elif info.get("path") is None:
                return False
        return True



class InteractiveConfigBlock(QGraphicsPathItem):
    __niaamlFeatureSelectionAlgorithmsMap = (
        FeatureSelectionAlgorithmFactory().get_name_to_classname_mapping()
    )
    __niaamlFeatureTransformAlgorithmsMap = (
        FeatureTransformAlgorithmFactory().get_name_to_classname_mapping()
    )
    __niaamlClassifiersMap = ClassifierFactory().get_name_to_classname_mapping()

    __niaamlFeatureSelectionDisplayOptions = list(__niaamlFeatureSelectionAlgorithmsMap)
    __niaamlFeatureTransformDisplayOptions = list(__niaamlFeatureTransformAlgorithmsMap)
    __niaamlClassifiersDisplayOptions      = list(__niaamlClassifiersMap)

    def __init__(
        self,
        label: str,
        *,
        shape: str = "rect",
        value: str = "",
        is_file: bool = False,
        is_folder: bool = False,
        is_number_input: bool = False,
        dropdown_options=None,
        icon_path: str | None = None,
        is_sidebar=True,
        readonly=False  
    ):
        super().__init__()
        self.readonly = readonly  
        self.shape            = shape.lower()
        self.icon_path        = icon_path
        self.label            = label
        self.value            = value
        self.is_file          = is_file
        self.is_folder        = is_folder
        self.is_number_input  = is_number_input
        self.dropdown_options = dropdown_options or []
        self.selected_options : list[str] = []
        self.connections      : list      = []
        
        tmp = QComboBox(); tmp.addItems(self.dropdown_options)
        combo_w   = tmp.sizeHint().width() if self.dropdown_options else 0
        self.w    = max(220, combo_w + 20)
        self.h    = 80

        self._set_shape_path()
        self.setBrush(QBrush(QColor("#005f85")))
        self.setPen  (QPen  (QColor("white")))
        self.setFlags(
            QGraphicsPathItem.GraphicsItemFlag.ItemIsMovable            |
            QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable         |
            QGraphicsPathItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

        lbl_x = 10
        if self.icon_path and os.path.exists(self.icon_path):
            pm = QPixmap(self.icon_path).scaled(
                20, 20, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.icon_item = QGraphicsPixmapItem(pm, self)
            self.icon_item.setOffset(5, 5)
            lbl_x = 30

        self.label_item = QGraphicsTextItem(self)
        self.label_item.setDefaultTextColor(QColor("white"))
        self.label_item.setPlainText(self.label)
        self.label_item.setPos(lbl_x, 5)

        y = 30
        if self.dropdown_options:
            dd = QComboBox(); dd.addItems(self.dropdown_options)
            pr = QGraphicsProxyWidget(self); pr.setWidget(dd); pr.setPos(10, y)
            self.dropdown = dd
            y += dd.sizeHint().height() + 10

        elif self.is_number_input:
            le = QLineEdit(); le.setValidator(QIntValidator(0, 999999)); le.setFixedWidth(100)
            pr = QGraphicsProxyWidget(self); pr.setWidget(le); pr.setPos(10, y)
            self.input_field = le
            y += le.sizeHint().height() + 10

        else:
            self.value_item = QGraphicsTextItem("Click to select…", self)
            self.value_item.setDefaultTextColor(QColor("white"))
            self.value_item.setTextWidth(self.w - 20)  
            self.value_item.setZValue(1)


            text_rect = self.value_item.boundingRect()
            text_x = 10
            text_y = y
            self.value_item.setPos(text_x, text_y)

            self.click_button = QPushButton("")
            self.click_button.setFlat(True)
            self.click_button.setStyleSheet("background-color: transparent; border: none;")
            self.click_button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.click_button.setFixedSize(int(text_rect.width()), int(text_rect.height()))

            self.click_button.clicked.connect(lambda: self._handle_click_action())

            self.click_proxy = QGraphicsProxyWidget(self)
            self.click_proxy.setWidget(self.click_button)
            self.click_proxy.setPos(text_x, text_y)

            if self.is_file and self.label == "Select CSV File":
                self._add_csv_helpers()

        self.input_circle  = QGraphicsEllipseItem(self)
        self.output_circle = QGraphicsEllipseItem(self)
        for circ in (self.input_circle, self.output_circle):
            circ.setBrush(QBrush(QColor("white")))
            circ.setZValue(1)
        self._reposition_io()
        self._layout_contents()

    def _handle_click_action(self):
        
        if self.readonly:
            return
        if self.dropdown_options:
            return 
        elif self.label in ["Feature Selection", "Feature Transform", "Classifier"]:
            self.getMultiSelection()
        elif self.is_file or self.is_folder:
            self.getPath()
        
    def _set_shape_path(self):
        """Definira QPainterPath glede na izbrano obliko."""
        p = QPainterPath()
        w, h = self.w, self.h

        if self.shape == "rounded":
            p.addRoundedRect(0, 0, w, h, 10, 10)

        elif self.shape == "diamond":
            p.moveTo(w / 2, 0)
            p.lineTo(w, h / 2)
            p.lineTo(w / 2, h)
            p.lineTo(0, h / 2)
            p.closeSubpath()

        elif self.shape == "octagon":
            r = 10
            p.moveTo(r, 0)
            p.lineTo(w - r, 0)
            p.lineTo(w, r)
            p.lineTo(w, h - r)
            p.lineTo(w - r, h)
            p.lineTo(r, h)
            p.lineTo(0, h - r)
            p.lineTo(0, r)
            p.closeSubpath()

        elif self.shape == "hexagon":
            r = 15
            p.moveTo(r, 0)
            p.lineTo(w - r, 0)
            p.lineTo(w, h / 2)
            p.lineTo(w - r, h)
            p.lineTo(r, h)
            p.lineTo(0, h / 2)
            p.closeSubpath()

        elif self.shape == "cut-corner":
            r = 10
            p.moveTo(r, 0)
            p.lineTo(w - r, 0)
            p.lineTo(w, r)
            p.lineTo(w, h - r)
            p.lineTo(w - r, h)
            p.lineTo(r, h)
            p.lineTo(0, h - r)
            p.lineTo(0, r)
            p.closeSubpath()

        elif self.shape == "notched":
            notch = 10
            p.moveTo(notch, 0)
            p.lineTo(w - notch, 0)
            p.lineTo(w, notch)
            p.lineTo(w, h - notch)
            p.lineTo(w - notch, h)
            p.lineTo(notch, h)
            p.lineTo(0, h - notch)
            p.lineTo(0, notch)
            p.closeSubpath()
        elif self.shape == "notched":
            notch = 10
            p.moveTo(notch, 0)
            p.lineTo(w - notch, 0)
            p.lineTo(w, notch)
            p.lineTo(w, h - notch)
            p.lineTo(w - notch, h)
            p.lineTo(notch, h)
            p.lineTo(0, h - notch)
            p.lineTo(0, notch)
            p.closeSubpath()
        elif self.shape == "parallelogram":
            slant = 20
            p.moveTo(0, 0)
            p.lineTo(self.w - slant, 0)
            p.lineTo(self.w, self.h)
            p.lineTo(slant, self.h)
            p.closeSubpath()
        else:  
            p.addRect(0, 0, w, h)

        self.setPath(p)

    def _reposition_io(self):
        self.input_circle .setRect(-6,        self.h/2 - 6, 12, 12)
        self.output_circle.setRect(self.w - 6, self.h/2 - 6, 12, 12)

    def _add_csv_helpers(self):
        self.csvHasHeader = True
        cb = QCheckBox("Header"); cb.setChecked(True)
        p_cb = QGraphicsProxyWidget(self); p_cb.setWidget(cb)
        p_cb.setPos(self.w - cb.sizeHint().width() - 5, 5)
        cb.stateChanged.connect(
            lambda s: setattr(self, "csvHasHeader", s == Qt.CheckState.Checked)
        )
        
        icon_dir  = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "icons")
        edit_icon = os.path.join(icon_dir, "placeholder.png")
        btn = QPushButton(); btn.setIcon(QIcon(edit_icon)); btn.setIconSize(QSize(18, 18))
        btn.setFixedSize(24, 24)
        p_btn = QGraphicsProxyWidget(self); p_btn.setWidget(btn)
        p_btn.setPos(self.w - 24 - 5, self.h - 24 - 5)
        btn.clicked.connect(self._open_csv_editor)
        self._edit_btn_proxy = p_btn

    def input_point (self) -> QPointF: return self.mapToScene(0,      self.h/2)
    def output_point(self) -> QPointF: return self.mapToScene(self.w, self.h/2)

    def _open_csv_editor(self):
        if not getattr(self, "value", ""):
            QMessageBox.warning(None, "No CSV", "Please pick a CSV file first.")
            return
        self.csv_editor_window = CSVEditorWindow(self.value)
        self.csv_editor_window.show()

    def getPath(self):
        dlg = QFileDialog
        if self.is_file:
            path, _ = dlg.getOpenFileName(None, "Select File", "", "CSV Files (*.csv);;All Files (*)")
        else:
            path = dlg.getExistingDirectory(None, "Select Folder")
        if path:
            self.value = path
            self.update_value_display()

    def getMultiSelection(self):
        if self.label == "Feature Selection":
            disp, mp = self.__niaamlFeatureSelectionDisplayOptions, self.__niaamlFeatureSelectionAlgorithmsMap
        elif self.label == "Feature Transform":
            disp, mp = self.__niaamlFeatureTransformDisplayOptions, self.__niaamlFeatureTransformAlgorithmsMap
        elif self.label == "Classifier":
            disp, mp = self.__niaamlClassifiersDisplayOptions     , self.__niaamlClassifiersMap
        else:
            disp, mp = [], {}

        dlg = MultiSelectDialog(f"Select {self.label}(s)", disp)
        if dlg.exec():
            chosen = dlg.selected_items()
            self.selected_options = [mp[d] for d in chosen if d in mp]
            txt = "\n".join(chosen)
            self.value_item.setPlainText(txt)
            self.value = "\n".join(self.selected_options)
            self._adjust_height(txt)

    def update_value_display(self):
        if hasattr(self, "value_item"):
            if self.selected_options: txt = "\n".join(self.selected_options)
            elif self.value:          txt = self.value
            else:                     txt = "Click to select…"
            self.value_item.setPlainText(txt)
            self._adjust_height(txt)
            
        if hasattr(self, "click_button"):
            text_rect = self.value_item.boundingRect()
            text_x = (self.w - text_rect.width()) / 2
            text_y = self.value_item.pos().y()
            self.click_button.setFixedSize(int(text_rect.width()), int(text_rect.height()))
            if hasattr(self, "click_proxy"):
                self.click_proxy.setPos(text_x, text_y)

    def _adjust_height(self, text: str):
        new_h = self.calculate_block_height(text)
        if new_h != self.h:
            dh = new_h - self.h
            self.h = new_h
            self._set_shape_path()
            self._reposition_io()
            if hasattr(self, "click_proxy"):
                p = self.click_proxy.pos()
                self.click_proxy.setPos(p.x(), p.y() + dh)


    def itemChange(self, ch, val):
        if ch == QGraphicsPathItem.GraphicsItemChange.ItemPositionChange:
            for c in self.connections:
                c.update_path()
        return super().itemChange(ch, val)

    @staticmethod
    def calculate_block_height(text: str, width: int = 200, base: int = 70) -> int:
        fm = QFontMetricsF(QGraphicsTextItem().font())
        line_h = fm.lineSpacing()
        lines  = text.split("\n")
        tot = sum(max(1, int(fm.horizontalAdvance(ln) / width) + 1) for ln in lines)
        return max(base, int(30 + tot * line_h + 20))

    def add_connection(self, conn):
        if conn not in self.connections:
            self.connections.append(conn)
    
    def _layout_contents(self):
        margin = 10
        icon_size = 20
        spacing = 5
        label_x = margin

        if hasattr(self, "icon_item"):
            self.icon_item.setOffset(label_x, margin)
            label_x += icon_size + spacing

        text_width = self.label_item.boundingRect().width()
        self.label_item.setPos((self.w - text_width) / 2, margin)

        if hasattr(self, "input_field"):
            proxy = QGraphicsProxyWidget(self)
            proxy.setWidget(self.input_field)
            field_y = margin + self.label_item.boundingRect().height() + spacing
            proxy.setPos((self.w - self.input_field.width()) / 2, field_y)

    def boundingRect(self):
        return QRectF(0, 0, self.w, self.h)
            


class NumericInputBlock(QGraphicsPathItem):
    def __init__(
        self,
        label: str,
        *,
        shape: str = "rect",
        icon_path: str | None = None
    ):
        super().__init__()
        self.label = label
        self.icon_path = icon_path
        self.shape = shape.lower()
        self.connections = []

        self._w = 220
        self._h = 70

        label_x = 10
        if self.icon_path and os.path.exists(self.icon_path):
            pm = QPixmap(self.icon_path).scaled(
                20, 20,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.icon_item = QGraphicsPixmapItem(pm, self)
            self.icon_item.setOffset(5, 5)
            label_x = 30

        self.label_item = QGraphicsTextItem(self)
        self.label_item.setDefaultTextColor(QColor("white"))
        self.label_item.setTextWidth(self._w - label_x - 10)
        self.label_item.setPlainText(self.label)

        edit_y = 10 + self.label_item.boundingRect().height()
        self.input_field = QLineEdit()
        self.input_field.setValidator(QIntValidator(0, 999999))
        self.input_field.setFixedWidth(100)

        proxy = QGraphicsProxyWidget(self)
        proxy.setWidget(self.input_field)
        proxy.setPos(10, edit_y)

        self._h = edit_y + self.input_field.sizeHint().height() + 10

        self._set_shape_path()

        self.input_circle = QGraphicsEllipseItem(-6, self._h / 2 - 6, 12, 12, self)
        self.output_circle = QGraphicsEllipseItem(self._w - 6, self._h / 2 - 6, 12, 12, self)
        for circ in (self.input_circle, self.output_circle):
            circ.setBrush(QBrush(QColor("white")))
            circ.setZValue(1)

        self.setBrush(QBrush(QColor("#005f85")))
        self.setPen(QPen(QColor("white")))
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemSendsGeometryChanges)

        self._layout_contents()

    def _set_shape_path(self):
        p = QPainterPath()
        if self.shape == "rounded":
            p.addRoundedRect(0, 0, self._w, self._h, 12, 12)
        elif self.shape == "ellipse":
            p.addEllipse(0, 0, self._w, self._h)
        elif self.shape == "diamond":
            p.moveTo(self._w / 2, 0)
            p.lineTo(self._w, self._h / 2)
            p.lineTo(self._w / 2, self._h)
            p.lineTo(0, self._h / 2)
            p.closeSubpath()
        elif self.shape == "octagon":
            r = 12
            p.moveTo(r, 0)
            p.lineTo(self._w - r, 0)
            p.lineTo(self._w, r)
            p.lineTo(self._w, self._h - r)
            p.lineTo(self._w - r, self._h)
            p.lineTo(r, self._h)
            p.lineTo(0, self._h - r)
            p.lineTo(0, r)
            p.closeSubpath()
        elif self.shape == "hexagon":
            p.moveTo(self._w * 0.25, 0)
            p.lineTo(self._w * 0.75, 0)
            p.lineTo(self._w, self._h * 0.5)
            p.lineTo(self._w * 0.75, self._h)
            p.lineTo(self._w * 0.25, self._h)
            p.lineTo(0, self._h * 0.5)
            p.closeSubpath()
        elif self.shape == "trapezoid":
            p.moveTo(self._w * 0.2, 0)
            p.lineTo(self._w * 0.8, 0)
            p.lineTo(self._w, self._h)
            p.lineTo(0, self._h)
            p.closeSubpath()
        else:
            p.addRect(0, 0, self._w, self._h)
        self.setPath(p)

    def input_point(self) -> QPointF:
        return self.mapToScene(self.input_circle.boundingRect().center())

    def output_point(self) -> QPointF:
        return self.mapToScene(self.output_circle.boundingRect().center())

    def add_connection(self, conn):
        if conn not in self.connections:
            self.connections.append(conn)

    def itemChange(self, change, value):
        if change == QGraphicsPathItem.GraphicsItemChange.ItemPositionChange:
            for conn in self.connections:
                conn.update_path()
        return super().itemChange(change, value)

    def get_value(self) -> str:
        return self.input_field.text()

    def _layout_contents(self):
        margin = 10
        icon_size = 20
        spacing = 5
        label_x = margin

        if hasattr(self, "icon_item"):
            self.icon_item.setOffset(label_x, margin)
            label_x += icon_size + spacing

        if hasattr(self, "label_item"):
            if hasattr(self, "icon_item"):
                self.label_item.setPos(label_x, margin)
            else:
                text_width = self.label_item.boundingRect().width()
                self.label_item.setPos((self._w - text_width) / 2, margin)


    def boundingRect(self):
        return QRectF(0, 0, self._w, self._h)
