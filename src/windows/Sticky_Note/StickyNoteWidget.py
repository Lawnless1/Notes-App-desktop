import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFrame
from PyQt5.QtGui import QFont, QColor, QMouseEvent, QFocusEvent, QPalette
from PyQt5.QtCore import Qt, QRect,  QPoint, QEvent

from classes.StickyNoteJson import StickyNoteJson
from .TextEditorWidget import TextEditorWidget
from ..abstract_windows.DragWidget import DragWidget


class StickyNote(DragWidget):
    def __init__(self, persistance:dict, created_time:int=0, due_date: int = 0, SNJson: StickyNoteJson= None,parent=None, isActive = True):
        super().__init__(parent)
        
        self.text_editor = TextEditorWidget(self)
        self.resize(200, 150)
        self.setStyleSheet("""
            background-color: #FFEB3B; /* A softer yellow */
            border: 1px solid black; /* Thin black border for distinction */
            border-radius: 10px; /* Rounded corners */
        """)
        if SNJson:
            created_time = SNJson.created_time
            due_date = SNJson.due_date
            self.resize(*SNJson.width_height)
            self.move(*SNJson.relative_pos)
            self.text_editor.text_edit.setHtml(SNJson.content)
            self.isActive = SNJson.is_active
            self.setStyleSheet(f"background-color: {SNJson.background_color}; /* A softer yellow */ \
                border: 1px solid black; /* Thin black border for distinction */ \
                border-radius: 10px; /* Rounded corners */")
            
        self.created_time:int = created_time
        self.persistance = persistance
        self.due_date = due_date
        self.parent_obj = parent
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.isActive = isActive
        
        self.close_button = QPushButton("X")
        self.close_button.clicked.connect(self.remove)
        self.text_editor.setDisabled(True)
        self.layout.addWidget(self.close_button)
        self.layout.addWidget(self.text_editor)
        
        
        



    
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            print("Mouse Double Clicked")
            self.text_editor.setDisabled(False)
            self.text_editor.text_edit.setFocus()
            

    
    def save(self):
        json_note = StickyNoteJson(self.x(), self.y(),
                                   self.width(), self.height(),
                                   self.created_time,
                                   due_date=self.due_date,
                                   content=self.text_editor.text_edit.toHtml(),
                                   is_active=self.isActive,
                                   background_color=self.palette().color(self.backgroundRole()).name()
                                   )
        print(self.persistance)
        self.persistance["Notes"][self.created_time] = json_note.to_dict()
    
    def remove(self):
        self.parent_obj.parent_obj.sticky_notes.pop(self.created_time)
        if not self.text_editor.text_edit.toPlainText():
            if self.created_time in self.persistance["Notes"]:
                self.persistance["Notes"].pop(self.created_time)
        else:
            self.isActive = False
            self.save()
        self.deleteLater()
    
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    note = StickyNote()
    # dashboard = StickyNote()
    note.show()
    sys.exit(app.exec_())
