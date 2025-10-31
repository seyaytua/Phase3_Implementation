"""
各種ダイアログ（編集機能追加版）
"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QTextEdit, QPushButton, QComboBox,
                               QFormLayout)
from PySide6.QtCore import Qt

class RequestDialog(QDialog):
    """コード依頼ダイアログ"""
    
    def __init__(self, parent=None, edit_data=None):
        super().__init__(parent)
        self.setWindowTitle("コード依頼" if not edit_data else "コード依頼編集")
        self.setMinimumWidth(500)
        self.edit_data = edit_data
        self.init_ui()
        
        if edit_data:
            self.load_data(edit_data)
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        self.function_name_edit = QLineEdit()
        form_layout.addRow("機能名:", self.function_name_edit)
        
        self.details_edit = QTextEdit()
        self.details_edit.setMinimumHeight(150)
        form_layout.addRow("依頼内容:", self.details_edit)
        
        layout.addLayout(form_layout)
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("キャンセル")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def load_data(self, data):
        """既存データを読み込み"""
        self.function_name_edit.setText(data.get('function_name', ''))
        self.details_edit.setPlainText(data.get('details', ''))
    
    def get_data(self):
        return (
            self.function_name_edit.text(),
            self.details_edit.toPlainText()
        )


class DeployDialog(QDialog):
    """コード配置ダイアログ"""
    
    def __init__(self, parent=None, edit_data=None):
        super().__init__(parent)
        self.setWindowTitle("ファイル配置記録" if not edit_data else "ファイル配置編集")
        self.setMinimumWidth(500)
        self.edit_data = edit_data
        self.init_ui()
        
        if edit_data:
            self.load_data(edit_data)
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        self.filename_edit = QLineEdit()
        form_layout.addRow("ファイル名:", self.filename_edit)
        
        self.filepath_edit = QLineEdit()
        form_layout.addRow("配置パス:", self.filepath_edit)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(['OK', 'NG', '未確認'])
        form_layout.addRow("動作確認:", self.status_combo)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setMinimumHeight(100)
        form_layout.addRow("備考:", self.notes_edit)
        
        layout.addLayout(form_layout)
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("キャンセル")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def load_data(self, data):
        """既存データを読み込み"""
        self.filename_edit.setText(data.get('filename', ''))
        self.filepath_edit.setText(data.get('filepath', ''))
        
        status = data.get('status', 'OK')
        index = self.status_combo.findText(status)
        if index >= 0:
            self.status_combo.setCurrentIndex(index)
        
        self.notes_edit.setPlainText(data.get('notes', ''))
    
    def get_data(self):
        return (
            self.filename_edit.text(),
            self.filepath_edit.text(),
            self.status_combo.currentText(),
            self.notes_edit.toPlainText()
        )


class TestDialog(QDialog):
    """テスト記録ダイアログ"""
    
    def __init__(self, parent=None, edit_data=None):
        super().__init__(parent)
        self.setWindowTitle("テスト記録" if not edit_data else "テスト記録編集")
        self.setMinimumWidth(500)
        self.edit_data = edit_data
        self.init_ui()
        
        if edit_data:
            self.load_data(edit_data)
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        self.function_name_edit = QLineEdit()
        form_layout.addRow("機能名:", self.function_name_edit)
        
        self.result_combo = QComboBox()
        self.result_combo.addItems(['OK', 'NG'])
        form_layout.addRow("結果:", self.result_combo)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setMinimumHeight(100)
        form_layout.addRow("備考:", self.notes_edit)
        
        layout.addLayout(form_layout)
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("キャンセル")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def load_data(self, data):
        """既存データを読み込み"""
        self.function_name_edit.setText(data.get('function_name', ''))
        
        result = data.get('result', 'OK')
        index = self.result_combo.findText(result)
        if index >= 0:
            self.result_combo.setCurrentIndex(index)
        
        self.notes_edit.setPlainText(data.get('notes', ''))
    
    def get_data(self):
        return (
            self.function_name_edit.text(),
            self.result_combo.currentText(),
            self.notes_edit.toPlainText()
        )


class BugDialog(QDialog):
    """バグ登録ダイアログ"""
    
    def __init__(self, parent=None, edit_data=None):
        super().__init__(parent)
        self.setWindowTitle("バグ登録" if not edit_data else "バグ編集")
        self.setMinimumWidth(500)
        self.edit_data = edit_data
        self.init_ui()
        
        if edit_data:
            self.load_data(edit_data)
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        self.title_edit = QLineEdit()
        form_layout.addRow("タイトル:", self.title_edit)
        
        self.description_edit = QTextEdit()
        self.description_edit.setMinimumHeight(100)
        form_layout.addRow("説明:", self.description_edit)
        
        self.severity_combo = QComboBox()
        self.severity_combo.addItems(['低', '中', '高', '致命的'])
        self.severity_combo.setCurrentIndex(1)
        form_layout.addRow("重要度:", self.severity_combo)
        
        layout.addLayout(form_layout)
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("キャンセル")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def load_data(self, data):
        """既存データを読み込み"""
        self.title_edit.setText(data.get('title', ''))
        self.description_edit.setPlainText(data.get('description', ''))
        
        severity = data.get('severity', '中')
        index = self.severity_combo.findText(severity)
        if index >= 0:
            self.severity_combo.setCurrentIndex(index)
    
    def get_data(self):
        return (
            self.title_edit.text(),
            self.description_edit.toPlainText(),
            self.severity_combo.currentText()
        )


class IssueDialog(QDialog):
    """問題登録ダイアログ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("問題登録")
        self.setMinimumWidth(500)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        self.title_edit = QLineEdit()
        form_layout.addRow("タイトル:", self.title_edit)
        
        self.description_edit = QTextEdit()
        self.description_edit.setMinimumHeight(100)
        form_layout.addRow("説明:", self.description_edit)
        
        self.impact_combo = QComboBox()
        self.impact_combo.addItems(['低', '中', '高'])
        self.impact_combo.setCurrentIndex(1)
        form_layout.addRow("影響範囲:", self.impact_combo)
        
        layout.addLayout(form_layout)
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("キャンセル")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def get_data(self):
        return (
            self.title_edit.text(),
            self.description_edit.toPlainText(),
            self.impact_combo.currentText()
        )


class IssueUpdateDialog(QDialog):
    """問題更新ダイアログ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("問題ステータス更新")
        self.setMinimumWidth(500)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(['発見', '対応中', '解決', '再発'])
        form_layout.addRow("ステータス:", self.status_combo)
        
        self.resolution_edit = QTextEdit()
        self.resolution_edit.setMinimumHeight(100)
        form_layout.addRow("解決策:", self.resolution_edit)
        
        layout.addLayout(form_layout)
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("キャンセル")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def get_data(self):
        return (
            self.status_combo.currentText(),
            self.resolution_edit.toPlainText()
        )