from PyQt5.QtWidgets import QWidget, QScrollArea, QApplication, QTextEdit, QLabel, QVBoxLayout, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt, QTimer, QCoreApplication


import time
from .Message import Message
from .sendLLM import send_openai
import sys




    
class MessageWidget(QWidget):
    def __init__(self, index: int, message: str):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.msgWidget = QLabel()
        self.msgWidget.setStyleSheet("""
            background-color: #FFEB3B; /* A softer yellow */
            border: 1px solid black; /* Thin black border for distinction */
            border-radius: 10px; /* Rounded corners */
            padding: 8px;
            margin: 5px;
        """)
        self.msgWidget.setText(message)
        self.msgWidget.setWordWrap(True)  # Enable wrapping
        self.msgWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Exact size for content
        self.msgWidget.adjustSize()
        
        if index % 2:  # Left aligned
            self.layout.addWidget(self.msgWidget)
            self.layout.addStretch(1)
        else:  # Right aligned
            self.layout.addStretch(1)
            self.layout.addWidget(self.msgWidget)
    
    def edit_message(self, message):
        self.msgWidget.setText(message)
        self.repaint()
        QCoreApplication.processEvents()

class MessagePane(QScrollArea):
    def __init__(self, parent=None, messages: list[Message]=[]):
        super().__init__(parent)
        # Attributes
        self.parent_obj = parent
        self.messages:list[str] = []
        self.scroll_to_bottom = lambda : self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
        
        
        self.scroll_widget:QWidget = QWidget()
        self.layout:QVBoxLayout = QVBoxLayout(self.scroll_widget)
        
        
        self.layout.setAlignment(Qt.AlignTop) # Set the alignment to top to avoid centering
        
        # Add each message in the message
        for i, message in enumerate(messages):
            self.layout.addWidget(MessageWidget(i, message))



        self.scroll_widget.setLayout(self.layout)
        self.setWidget(self.scroll_widget)
        self.setWidgetResizable(True)
        QTimer.singleShot(1, self.scroll_to_bottom)
        

    def addMessage(self, message: str):
        
        self.messages.append(message)
        self.layout.addWidget(MessageWidget(len(self.messages)-1, message))
        QTimer.singleShot(1, self.scroll_to_bottom)
        
        responseWidget = MessageWidget(len(self.messages), "")
        self.layout.addWidget(responseWidget)
        result = send_openai(self.messages)
        msg = ""
        for chunk in result:
            if chunk.choices[0].delta.content is not None:
                msg = msg + chunk.choices[0].delta.content
                print(chunk)
                responseWidget.edit_message(msg)
                QCoreApplication.processEvents()
        self.messages.append(msg)
        QTimer.singleShot(1, self.scroll_to_bottom)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MessagePane()
    window.setWindowTitle("Notify")
    window.resize(600, 400)
    window.show()
    while (response := input()) != "":
        window.addMessage(Message(True, response))
    sys.exit(app.exec_())
            
        
        
        
        
        