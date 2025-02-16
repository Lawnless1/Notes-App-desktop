import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFrame, QTextEdit
from PyQt5.QtGui import QFont, QColor, QMouseEvent, QFocusEvent, QPalette
from PyQt5.QtCore import Qt, QRect,  QPoint, QEvent


from ..abstract_windows.DragWidget import DragWidget
from .MessagePane import MessagePane
from .PromptBox import PromptBox

class Chat(DragWidget):
    
    def __init__(self, persistance:dict, created_time:int=0, ChatJson=None,parent=None, isActive = True):
        super().__init__(parent)
        self.messages = []
        self.setStyleSheet(f"background-color: white; /* A softer yellow */ \
                color: black; \
                border: 1px solid black; /* Thin black border for distinction */ \
                border-radius: 10px; /* Rounded corners */")
        
        if ChatJson:
            pass
        self.persistance = persistance
        self.created_time = created_time
        self.parent_obj = parent
        self.close_button = QPushButton("X")
        self.close_button.clicked.connect(self.remove)
        self.messagePane = MessagePane(self)
        self.promptBox = PromptBox(self)
        # Styling
        self.layout: QVBoxLayout = QVBoxLayout()
        self.promptBox.setMinimumHeight(100)  # Minimum height in pixels
        self.layout.addWidget(self.close_button, 1)
        self.layout.addWidget(self.messagePane, 16)
        self.layout.addWidget(self.promptBox, 4)
        
        self.setLayout(self.layout)
        
    def remove(self):
        self.deleteLater()
        

