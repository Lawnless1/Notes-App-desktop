import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont, QColor, QTextImageFormat, QPainter, QPixmap, QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QColorDialog, QComboBox, QFileDialog, QGraphicsView, QGraphicsScene, QShortcut
try:
    from assets.colors import colors as color_set
except ModuleNotFoundError:
    try:
        from ...assets.colors import colors as color_set
    except ImportError:
        colors = {}

shortened_colors = {
    "r": "red",
    "g": "green",
    "b": "blue",
    "bl": "black",
    "o": "orange",
    "p": "purple",
    "y": "yellow",
}

class Terminal(QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_obj = parent
    
    def interpret_command(self, command:str) -> None:
        print(type(self.parent_obj))
        # Invalid input or no Parent
        if self.parent_obj == None or not command:
            print("No parent or command")
        # Font Size Change
        elif command.isnumeric():
            self.parent_obj.change_font_size(int(command))
            print("Font change")
        # Color Change
        elif command.split()[0].lower() in {"c", "color"}:
            if len(command.split()) > 1:
                color = command.split()[1].lower()
                if color in shortened_colors:
                    color = shortened_colors[color]
                self.parent_obj.change_color(color)
            print("color change")
        elif (color := command.lower()) in shortened_colors or color in color_set:
            print(color)
            self.parent_obj.change_color(color)
            print("color change")
        # Backgroud color change
        elif command.split()[0].lower() in {"b", "background", "bcolor"}:
            if len(command.split()) > 1:
                color = command.split()[1].lower()
                self.parent_obj.parent_obj.setStyleSheet(f"background-color: {color}; /* A softer yellow */ \
                                                        border: 1px solid black; /* Thin black border for distinction */ \
                                                        border-radius: 10px; /* Rounded corners */")
            print("Backgrund Color change")
        else:
            print("no mapping")
        
                
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            print("Enter key detected")
            command = self.toPlainText()
            if self.parent_obj:
                self.parent_obj.text_edit.setFocus()
            self.interpret_command(command)
            self.deleteLater()  # Schedule the QTextEdit for deletio
            # Add your custom logic here
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Terminal()
    window.show()
    sys.exit(app.exec_())
        
