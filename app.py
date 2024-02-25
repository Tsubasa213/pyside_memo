import os
import json
from PySide6.QtWidgets import (QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout,
                               QWidget, QPushButton, QApplication, QMessageBox,
                               QFileDialog)
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression

CONFIG_FILE = 'notepad_config.json'

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.note_path = None
        self.loadConfig()
        self.initUI()

    def loadConfig(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as file:
                config = json.load(file)
                self.note_path = config.get('note_path')
        else:
            self.note_path = None

    def saveConfig(self):
        with open(CONFIG_FILE, 'w') as file:
            json.dump({'note_path': self.note_path}, file)

    def initUI(self):
        self.setWindowTitle('メモ帳')
        self.setGeometry(100, 100, 800, 600)

        self.textEdit = QTextEdit()

        self.fileNameEdit = QLineEdit()
        self.fileNameEdit.setPlaceholderText('ファイル名(.txtを除く)')
        regex = QRegularExpression("^[a-zA-Z0-9]*$")
        validator = QRegularExpressionValidator(regex)
        self.fileNameEdit.setValidator(validator)

        self.newButton = QPushButton('新規(&N)')
        self.newButton.clicked.connect(self.newFile)

        self.openButton = QPushButton('開く(&O)...')
        self.openButton.clicked.connect(self.openFile)

        self.saveButton = QPushButton('保存(&S)')
        self.saveButton.clicked.connect(self.saveFile)

        self.mailTemplateButton = QPushButton('メールテンプレ')
        self.mailTemplateButton.clicked.connect(self.insertMailTemplate)

        self.exitButton = QPushButton('終了(&X)')
        self.exitButton.clicked.connect(self.close)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.newButton)
        buttonLayout.addWidget(self.openButton)
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.mailTemplateButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.exitButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.fileNameEdit)
        mainLayout.addWidget(self.textEdit)

        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

    def newFile(self):
        self.textEdit.clear()

    def openFile(self):
        if not self.note_path:
            self.note_path = QFileDialog.getExistingDirectory(self, '保存場所を選択')
            if not self.note_path:
                return  # User cancelled the dialog
            self.saveConfig()

        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, 'ファイルを開く', self.note_path,
                                                  'テキストファイル (*.txt);;すべてのファイル (*)', options=options)
        if fileName:
            with open(fileName, 'r', encoding='utf-8') as file:
                self.textEdit.setText(file.read())

    def saveFile(self):
        if not self.note_path:
            self.note_path = QFileDialog.getExistingDirectory(self, '保存場所を選択')
            if not self.note_path:
                return  # User cancelled the dialog
            self.saveConfig()

        fileName = self.fileNameEdit.text()
        if not fileName:
            QMessageBox.warning(self, '警告', 'ファイル名を入力してください。')
            return
        if not fileName.lower().endswith('.txt'):
            fileName += '.txt'
        filePath = os.path.join(self.note_path, fileName)

        if not os.path.isdir(self.note_path):
            try:
                os.makedirs(self.note_path)
            except OSError as e:
                QMessageBox.warning(self, '保存エラー', f'ディレクトリの作成に失敗しました。\nエラー: {e}')
                return

        if os.path.exists(filePath):
            reply = QMessageBox.question(self, 'ファイルの上書き確認',
                                         "すでに同じ名前のファイルが存在します。上書きしますか?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return

        try:
            with open(filePath, 'w', encoding='utf-8') as file:
                file.write(self.textEdit.toPlainText())
            QMessageBox.information(self, '情報', 'ファイルが正常に保存されました。')
        except IOError as e:
            QMessageBox.warning(self, '保存エラー', f'ファイルを保存できませんでした。\nエラー: {e}')

    def insertMailTemplate(self):
        template = """○○先生

いつもお世話になっています。〇年〇コースの○○です。
本日は～について連絡させていただきました。

ご迷惑おかけしますがよろしくお願いいたします。"""
        self.textEdit.insertPlainText(template)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '終了',
                                     "本当に終了しますか？", QMessageBox.Yes |
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