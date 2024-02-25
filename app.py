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

        # ファイル名を入力するテキストボックスを作成
        self.fileNameEdit = QLineEdit()
        self.fileNameEdit.setPlaceholderText('ファイル名(.txtを除く)')  # プレースホルダーテキストを設定
        # 半角英数字のみを受け入れるバリデータを設定
        regex = QRegularExpression("^[a-zA-Z0-9]*$")
        validator = QRegularExpressionValidator(regex)
        self.fileNameEdit.setValidator(validator)

        # ボタンを作成
        self.newButton = QPushButton('新規(&N)')
        self.newButton.clicked.connect(self.newFile)

        self.openButton = QPushButton('開く(&O)...')
        self.openButton.clicked.connect(self.openFile)

        self.saveButton = QPushButton('保存(&S)')
        self.saveButton.clicked.connect(self.saveFile)

        self.exitButton = QPushButton('終了(&X)')
        self.exitButton.clicked.connect(self.close)

        # ボタンのレイアウトを作成
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.newButton)
        buttonLayout.addWidget(self.openButton)
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.exitButton)

        # メインレイアウトを作成
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

        # ディレクトリが存在するか確認し、存在しなければ作成する
        if not os.path.isdir(self.note_path):
            try:
                os.makedirs(self.note_path)
            except OSError as e:
                QMessageBox.warning(self, '保存エラー', f'ディレクトリの作成に失敗しました。\nエラー: {e}')
                return

        # すでに同じ名前のファイルが存在するか確認する
        if os.path.exists(filePath):
            reply = QMessageBox.question(self, 'ファイルの上書き確認',
                                         "すでに同じ名前のファイルが存在します。上書きしますか?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return

        # ファイルの保存処理
        try:
            with open(filePath, 'w', encoding='utf-8') as file:
                file.write(self.textEdit.toPlainText())
            QMessageBox.information(self, '情報', 'ファイルが正常に保存されました。')
        except IOError as e:
            QMessageBox.warning(self, '保存エラー', f'ファイルを保存できませんでした。\nエラー: {e}')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'メッセージ',
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