import sys
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QShortcut
from PyQt5.QtCore import Qt, QEvent
from classes.StickyNoteJson import StickyNoteJson

import time

if __name__ == "__main__":
    from Sticky_Note.StickyNoteWidget import StickyNote
else:
    from .Sticky_Note.StickyNoteWidget import StickyNote
    from .ChatBox.Chat import Chat
    

class Dashboard(QWidget):
    def __init__(self, persistance):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setGeometry(100, 100, 800, 600)
        self.persistance: dict = persistance
        self.sticky_notes:dict = dict()
        self.chats:dict = dict()
        # Main layout
        self.layout = QVBoxLayout(self)

        # Add button for creating StickyNotes
        self.add_button = QPushButton("Add Sticky Note")
        self.add_button.clicked.connect(self.add_sticky_note)
        

        # Create a container for sticky notes
        self.notes_container = QFrame(self)
        self.notes_container.parent_obj = self
        self.notes_container.setFrameShape(QFrame.StyledPanel)
        self.notes_container.setMinimumHeight(500)
        
        self.layout.addWidget(self.notes_container)
        self.layout.addWidget(self.add_button)
        self.installEventFilter(self)
        
        self.add_note_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.add_note_shortcut.setContext(Qt.WidgetWithChildrenShortcut)  # Ensure shortcut works with child focus
        self.add_note_shortcut.activated.connect(self.add_sticky_note)
        self.add_chat_shortcut = QShortcut(QKeySequence("Ctrl+Backslash"), self)
        self.add_chat_shortcut.setContext(Qt.WidgetWithChildrenShortcut)  # Ensure shortcut works with child focus
        self.add_chat_shortcut.activated.connect(self.add_chat)

    def keyPressEvent(self, event):
            print(f"dashboard: {event.key()}")
            if event.key() == Qt.Key_Return and event.modifiers() == Qt.ControlModifier:
                print("adding note")
                self.add_sticky_note()
            if event.key() == Qt.Key_Backslash and event.modifiers() == Qt.ControlModifier:
                print("adding chat")
                self.add_chat()
            else:
                super().keyPressEvent(event)

                
    def add_sticky_note(self):
        # Create a StickyNote within notes_container
        created_time = int(time.time()*10000)
        note = StickyNote(persistance=self.persistance, created_time=created_time, parent=self.notes_container)
        note.setGeometry(50, 50, 200, 150)  # Position and size
        note.show()  # Make sure it's visible
        note.raise_()  # Bring it to the front, just in case
        self.sticky_notes[created_time] = note  # Add to the list of StickyNotes
        
    def add_chat(self):
        # Create a Chat within notes_container
        created_time = int(time.time()*10000)
        chat = Chat(self.persistance, created_time, parent=self.notes_container, isActive=True)
        chat.setGeometry(50, 50, 400, 600)  # Position and size
        chat.show()  # Make sure it's visible
        chat.raise_()  # Bring it to the front, just in case
        self.chats[created_time] = chat  # Add to the list of StickyNotes

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            for note in self.sticky_notes.values():
                if not note.geometry().contains(note.mapFromGlobal(event.globalPos())):
                    print(f"Mouse clicked outside StickyNote {id(note)}")
                    if note.text_editor.isEnabled():
                        note.text_editor.setDisabled(True)
                        note.save()
                    # Handle the event as needed
        return super().eventFilter(source, event)
    
    def load(self):
        for created_time, SN in self.persistance["Notes"].items():
            print(f"Trying {created_time}")
            try:
                SNJson = StickyNoteJson(SN["relative_pos"][0],
                                        SN["relative_pos"][1],
                                        SN["width_height"][0],
                                        SN["width_height"][1],
                                        created_time,
                                        due_date=SN["due_date"],
                                        content=SN["content"],
                                        is_active=SN["is_active"],
                                        background_color=SN["background_color"])
                if SNJson.is_active:
                    note = StickyNote(persistance=self.persistance, SNJson=SNJson, parent=self.notes_container)
                    note.show()
                    note.raise_()
                    self.sticky_notes[created_time] = note  # Add to the list of StickyNotes
            except TypeError as e:
                print(f"failed on {created_time}\n{SN}\n{'-'*20}")
                print(e)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())