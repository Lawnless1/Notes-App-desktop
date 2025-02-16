from PyQt5.QtWidgets import QTextEdit, QApplication
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

from .Message import Message
import sys


class PromptBox(QTextEdit):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_obj = parent
        
    def process_prompt(self, command:str):
        self.parent_obj.messagePane.addMessage(command)
        self.clear()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            print("Enter key detected")
            command = self.toPlainText()
            self.process_prompt(command)
            print("Pressed")
            # Add your custom logic here
        else:
            super().keyPressEvent(event)
    

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PromptBox()
    window.setWindowTitle("Notify")
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())