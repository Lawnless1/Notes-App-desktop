import sys
from PyQt5.QtCore import Qt, QRect, QEvent, QObject
from PyQt5.QtGui import QFont, QColor, QTextImageFormat, QPainter, QPixmap, QKeySequence, QTextCursor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QColorDialog, QComboBox, QFileDialog, QGraphicsView, QGraphicsScene, QShortcut
try:
    from Terminal import Terminal
except ModuleNotFoundError:
    from .Terminal import Terminal


class TextEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent_obj = parent
        self.initUI()
        self.add_shortcut()
        self.setObjectName("TextEditorWidget")
        self.setStyleSheet("""
            border: 0px solid black; /* Thin black border for distinction */
            border-radius: 10px; /* Rounded corners */
            color: black;
        """)
        # Sets tab to 4 spaces length
        font_metrics = self.text_edit.fontMetrics()
        self.text_edit.setTabStopWidth(4 * font_metrics.width(' '))
        
    def add_shortcut(self):
        self.terminal_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.terminal_shortcut.setContext(Qt.WidgetWithChildrenShortcut)  # Ensure shortcut works with child focus
        self.terminal_shortcut.activated.connect(self.toggle_terminal)
        
        self.bold_shortcut = QShortcut(QKeySequence("Ctrl+B"), self)
        self.bold_shortcut.setContext(Qt.WidgetWithChildrenShortcut)  # Ensure shortcut works with child focus
        self.bold_shortcut.activated.connect(self.toggle_bold)
        
        self.italic_shortcut = QShortcut(QKeySequence("Ctrl+I"), self)
        self.italic_shortcut.setContext(Qt.WidgetWithChildrenShortcut)  # Ensure shortcut works with child focus
        self.italic_shortcut.activated.connect(self.toggle_italic)
        
        self.underline_shortcut = QShortcut(QKeySequence("Ctrl+U"), self)
        self.underline_shortcut.setContext(Qt.WidgetWithChildrenShortcut)  # Ensure shortcut works with child focus
        self.underline_shortcut.activated.connect(self.toggle_underline)
        
        self.overline_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.overline_shortcut.setContext(Qt.WidgetWithChildrenShortcut)  # Ensure shortcut works with child focus
        self.overline_shortcut.activated.connect(self.toggle_overline)
        
        self.select_line_shortcut = QShortcut(QKeySequence("Ctrl+K"), self)
        self.select_line_shortcut.setContext(Qt.WidgetWithChildrenShortcut)  # Ensure shortcut works with child focus
        self.select_line_shortcut.activated.connect(self.select_line)

        self.remove_shortcut = QShortcut(QKeySequence("Ctrl+Backspace"), self)
        self.remove_shortcut.setContext(Qt.WidgetWithChildrenShortcut)  # Ensure shortcut works with child focus
        self.remove_shortcut.activated.connect(self.parent_obj.remove)
        
        
    
    

    def keyPressEvent(self, event):
            if event.key() == Qt.Key_Q and event.modifiers() == Qt.ControlModifier:
                self.toggle_terminal()
            elif event.key() == Qt.Key_B and event.modifiers() == Qt.ControlModifier:
                self.toggle_bold()
            elif event.key() == Qt.Key_I and event.modifiers() == Qt.ControlModifier:
                self.toggle_italic()
            elif event.key() == Qt.Key_U and event.modifiers() == Qt.ControlModifier:
                self.toggle_underline()
            elif event.key() == Qt.Key_O and event.modifiers() == Qt.ControlModifier:
                self.toggle_overline()
            elif event.key() == Qt.Key_K and event.modifiers() == Qt.ControlModifier:
                self.select_line()
            elif event.key() == Qt.Key_Backspace and event.modifiers() == Qt.ControlModifier:
                self.parent_obj.remove()
            else:
                super().keyPressEvent(event)
    
            
    def initUI(self):
        self.setWindowTitle("Rich Text Editor with Image Resizing and Cropping")
        self.setGeometry(100, 100, 600, 400)

        # Create QTextEdit widget for rich text editing
        self.text_edit = QTextEdit(self)
        self.text_edit.setAcceptDrops(True)  # Allow drag-and-drop
        
        # Layout for the UI components
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)

    def toggle_terminal(self):
        terminal = Terminal(self)
        self.layout.addWidget(terminal)
        terminal.adjustSize()
        terminal.setFixedHeight(30)
        terminal.setFocus()
        

    def toggle_bold(self):
        current_format = self.text_edit.textCursor().charFormat()
        current_format.setFontWeight(QFont.Bold if current_format.fontWeight() != QFont.Bold else QFont.Normal)
        self.text_edit.setCurrentCharFormat(current_format)
    
    def toggle_italic(self):
        current_format = self.text_edit.textCursor().charFormat()
        current_format.setFontItalic(not current_format.fontItalic())
        self.text_edit.setCurrentCharFormat(current_format)

    def toggle_underline(self):
        current_format = self.text_edit.textCursor().charFormat()
        current_format.setFontUnderline(not current_format.fontUnderline())
        self.text_edit.setCurrentCharFormat(current_format)

    def toggle_overline(self):
        current_format = self.text_edit.textCursor().charFormat()
        current_format.setFontStrikeOut(not current_format.fontStrikeOut())
        self.text_edit.setCurrentCharFormat(current_format)
    
    def select_line(self):
        print("select line activated")
        cursor = self.text_edit.textCursor()  # Get the current text cursor
        cursor.movePosition(QTextCursor.StartOfLine)  # Move to the start of the line
        cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)  # Select to the end of the line
        self.text_edit.setTextCursor(cursor)  # Set the modified cursor back to the text edit
        
        
    def change_color(self, input_color):
        color = QColor(input_color)
        if color.isValid():
            current_format = self.text_edit.textCursor().charFormat()
            current_format.setForeground(color)
            self.text_edit.setCurrentCharFormat(current_format)

    def change_font_size(self, size:int):
        current_format = self.text_edit.textCursor().charFormat()
        font = current_format.font()
        font.setPointSize(int(size))
        print(f"new size: {size}")
        current_format.setFont(font)
        self.text_edit.setCurrentCharFormat(current_format)
        

    def insert_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Insert Image", "", "Images (*.png *.xpm *.jpg *.bmp)")
        if file_name:
            cursor = self.text_edit.textCursor()
            image_format = QTextImageFormat()
            image_format.setName(file_name)
            image_format.setWidth(200)  # Resize width of the image
            image_format.setHeight(150)  # Resize height of the image
            cursor.insertImage(image_format)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage() or event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):
        # Handle the drop of an image or file
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    cursor = self.text_edit.textCursor()
                    image_format = QTextImageFormat()
                    image_format.setName(file_path)
                    image_format.setWidth(200)  # Set initial width after drag
                    image_format.setHeight(150)  # Set initial height after drag
                    cursor.insertImage(image_format)

    # You would add a custom cropping widget or logic here, if needed
    # This part would require additional coding for cropping functionality.


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TextEditorWidget()
    window.show()
    sys.exit(app.exec_())
