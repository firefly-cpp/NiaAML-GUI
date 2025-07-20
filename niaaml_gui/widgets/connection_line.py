import math
from PyQt6.QtWidgets import QGraphicsPathItem, QGraphicsPolygonItem
from PyQt6.QtGui import QPen, QColor, QPainterPath, QBrush, QPolygonF
from PyQt6.QtCore import QPointF, Qt


class ConnectionLine(QGraphicsPathItem):
    def __init__(self, source_block, target_block):
        super().__init__()
        self.source_block = source_block
        self.target_block = target_block

        self.setZValue(100)
        self.setPen(QPen(QColor("black"), 2))
        self.setFlags(
            QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable
        )

        self.arrow_shape = QPolygonF([
            QPointF(0, 0),
            QPointF(-12, -6),
            QPointF(-12, 6)
        ])

        self.arrow_item = QGraphicsPolygonItem(self.arrow_shape, self)
        self.arrow_item.setBrush(QBrush(QColor("black")))
        self.arrow_item.setPen(QPen(Qt.PenStyle.NoPen))
        self.arrow_item.setZValue(101)
        self.arrow_item.setTransformOriginPoint(QPointF(0, 0))

        self.update_path()

    def mousePressEvent(self, event):
        """Ob kliku samo izberi povezavo – ne izbriši."""
        self.setSelected(True)
        super().mousePressEvent(event)

    def update_path(self):
        start = self.source_block.output_point()
        end = self.target_block.input_point()

        path = QPainterPath()
        path.moveTo(start)

        pre_end = QPointF(end.x() - 20, end.y())

        dx = (pre_end.x() - start.x()) * 0.5
        cp1 = QPointF(start.x() + dx, start.y())
        cp2 = QPointF(pre_end.x() - dx, pre_end.y())
        path.cubicTo(cp1, cp2, pre_end)

        path.lineTo(end)
        self.setPath(path)

        arrow_size = 12
        arrow = QPolygonF([
            QPointF(0, 0),
            QPointF(-arrow_size, -arrow_size / 2),
            QPointF(-arrow_size, arrow_size / 2)
        ])

        if hasattr(self, "arrow_item") and self.arrow_item:
            if self.arrow_item.scene():
                self.arrow_item.scene().removeItem(self.arrow_item)
            self.arrow_item = None

        self.arrow_item = QGraphicsPolygonItem(arrow, self)
        self.arrow_item.setBrush(QBrush(QColor("black")))
        self.arrow_item.setPen(QPen(Qt.PenStyle.NoPen))
        self.arrow_item.setZValue(101)

        self.arrow_item.setRotation(0)
        self.arrow_item.setPos(end)


