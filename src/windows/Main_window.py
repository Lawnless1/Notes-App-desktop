from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QVBoxLayout, QWidget, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
import json

if __name__ == "__main__":
    from Dashboard import Dashboard
else:
    from .Dashboard import Dashboard

class MainWindow(QMainWindow):
    def __init__(self, persistance={"Chats": {}, "Notes": {}}):
        super().__init__()
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        
        self.persistance:dict = persistance
        # Initialize the menu bar
        self.initMenuBar()
        self.initDashboard()
        self.load()
        
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.save_shortcut.setContext(Qt.WidgetWithChildrenShortcut)  # Ensure shortcut works with child focus
        self.save_shortcut.activated.connect(self.save)
        self.load_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        self.load_shortcut.setContext(Qt.WidgetWithChildrenShortcut)  # Ensure shortcut works with child focus
        self.load_shortcut.activated.connect(self.load)


    def initDashboard(self):
        self.dashboard = Dashboard(self.persistance)
        print(self.persistance)
        self.setCentralWidget(self.dashboard)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QMenuBar {
                background-color: #333333;
                color: #FFFFFF;
            }
            QMenuBar::item {
                background-color: #333333;
                color: #FFFFFF;
            }
            QMenuBar::item:selected {
                background-color: #444444;
            }
            QMenu {
                background-color: #333333;
                color: #FFFFFF;
            }
            QMenu::item:selected {
                background-color: #444444;
            }
            QAction {
                color: #FFFFFF;
            }
            QWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #4A4A4A; /* Slightly lighter gray */
                color: #FFFFFF;
                border: 1px solid #5A5A5A;
                padding: 5px;
                border-radius: 3px;
        """)
        
    def initMenuBar(self):
        menu_bar = self.menuBar()
        
        # Create File menu
        file_menu = menu_bar.addMenu('File')

        # Create Tools menu
        tools_menu = menu_bar.addMenu('Tools')

        # Add actions to the File menu
        file_action = QAction('File Action', self)
        file_action.triggered.connect(self.file_function)
        file_menu.addAction(file_action)

        # Add actions to the Tools menu
        tools_action = QAction('Tools Action', self)
        tools_action.triggered.connect(self.tools_function)
        tools_menu.addAction(tools_action)
        
    def keyPressEvent(self, event):
        print(f"Main: {event.key()}")
        if event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            print("Saving Config")
            self.save()
        if event.key() == Qt.Key_L and event.modifiers() == Qt.ControlModifier:
            print("Loading Persistance")
            self.load()
        else:
            super().keyPressEvent(event)
            
    def load(self):
        try:
            from persistance.persistance import persistance as p
            self.persistance = p
            self.dashboard.deleteLater()
            self.initDashboard()
            self.dashboard.load()
        except ImportError as e:
            print(e)
            print("import failed")
        
        

    def save(self):
        persistance = open("persistance/persistance.py", "w")
        persistance.write(f"persistance = {self.persistance}")
        persistance.close()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()    

    def file_function(self):
        # Placeholder function for File menu
        pass

    def tools_function(self):
        # Placeholder function for Tools menu
        pass

if __name__ == '__main__':
    import sys
    
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setWindowTitle("Notify")
    window.resize(600, 400)
    window.show()

    sys.exit(app.exec_())
