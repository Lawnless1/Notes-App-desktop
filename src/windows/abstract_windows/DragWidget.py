import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFrame
from PyQt5.QtGui import QFont, QColor, QMouseEvent, QFocusEvent, QPalette
from PyQt5.QtCore import Qt, QRect,  QPoint, QEvent

class DragWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Dragging and resizing flags
        self.dragging = False
        self.resizing = False
        self.drag_start_position = QPoint()
        self.setAttribute(Qt.WA_StyledBackground, True)  # Force Styling, even as child widget
        
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            print("Mouse Pressed")
            
            if self.is_in_resize_area(event.pos()):
                self.resizing = True
                self.resize_start_position = event.globalPos()
                self.resize_start_geometry = self.geometry()
            else:
                self.dragging = True
                self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_in_resize_area(event.pos()):
            self.setCursor(Qt.SizeFDiagCursor)  # Change cursor to diagonal resize
        else:
            self.setCursor(Qt.ArrowCursor)  # Restore default cursor

        if self.dragging:
            new_pos:QPoint = event.globalPos() - self.drag_start_position
            self.move(new_pos)
        elif self.resizing:
            delta = event.globalPos() - self.resize_start_position
            new_width = max(100, self.resize_start_geometry.width() + delta.x())
            new_height = max(100, self.resize_start_geometry.height() + delta.y())
            self.resize(new_width, new_height)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.dragging = False
        self.resizing = False

    def is_in_resize_area(self, pos):
        corner_size = 20
        return self.rect().adjusted(self.width() - corner_size, self.height() - corner_size, 0, 0).contains(pos)
    