import sys
from PySide6.QtWidgets import QApplication
from app import Notepad

def main():
    app = QApplication(sys.argv)
    notepad = Notepad()
    notepad.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()