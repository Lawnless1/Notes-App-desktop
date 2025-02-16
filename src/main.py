from PyQt5.QtWidgets import QApplication
from windows.Main_window import MainWindow
import sys
    
    
app = QApplication(sys.argv)
window = MainWindow(persistance={"Chats": {}, "Notes": {}})
window.setWindowTitle("Notify")
window.resize(600, 400)
window.show()

sys.exit(app.exec_())