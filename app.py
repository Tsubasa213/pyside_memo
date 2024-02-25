import os
from PySide6.QtWidgets import QMainWindow, QTextEdit, QFileDialog, QApplication, QMessageBox
from PySide6.QtGui import QAction, QKeySequence

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.createActions()
        self.createMenus()
        self.setWindowTitle('Simple Notepad')
        self.setGeometry(100, 100, 800, 600)

    def createActions(self):
        self.newAction = QAction('&New', self)
        self.newAction.setShortcut(QKeySequence.New)
        self.newAction.setStatusTip('Create a new document')
        self.newAction.triggered.connect(self.newFile)

        self.openAction = QAction('&Open...', self)
        self.openAction.setShortcut(QKeySequence.Open)
        self.openAction.setStatusTip('Open an existing document')
        self.openAction.triggered.connect(self.openFile)

        self.saveAction = QAction('&Save', self)
        self.saveAction.setShortcut(QKeySequence.Save)
        self.saveAction.setStatusTip('Save the document to disk')
        self.saveAction.triggered.connect(self.saveFile)

        self.exitAction = QAction('E&xit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)

    def createMenus(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)

    def newFile(self):
        self.textEdit.clear()

    def openFile(self):
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open File', desktop_path,
                                                  'Text Files (*.txt);;All Files (*)', options=options)
        if fileName:
            with open(fileName, 'r') as file:
                self.textEdit.setText(file.read())

    def saveFile(self):
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', desktop_path,
                                                  'Text Files (*.txt)', options=options)
        if fileName:
            if not fileName.lower().endswith('.txt'):
                fileName += '.txt'  # ファイル名に.txtを追加
            with open(fileName, 'w') as file:
                file.write(self.textEdit.toPlainText())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication([])
    notepad = Notepad()
    notepad.show()
    app.exec()