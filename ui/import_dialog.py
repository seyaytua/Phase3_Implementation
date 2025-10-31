"""
JSON一括インポートダイアログ
"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTextEdit,
                               QPushButton, QLabel, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from utils.json_bulk_importer import JSONBulkImporter

class ImportDialog(QDialog):
    """JSON一括インポートダイアログ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("JSON一括インポート")
        self.setMinimumSize(800, 600)
        self.validated_data = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 説明
        info_label = QLabel(
            "Claude から受け取ったJSON形式のデータを貼り付けてください。\n"
            "検証ボタンで内容を確認後、インポートできます。"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # JSON入力エリア
        layout.addWidget(QLabel("JSONデータ:"))
        self.json_edit = QTextEdit()
        self.json_edit.setPlaceholderText('{\n  "issue_updates": [...],\n  "code_requests": [...]\n}')
        font = QFont("Consolas", 10)
        self.json_edit.setFont(font)
        layout.addWidget(self.json_edit)
        
        # プレビューエリア
        layout.addWidget(QLabel("プレビュー:"))
        self.preview_edit = QTextEdit()
        self.preview_edit.setReadOnly(True)
        self.preview_edit.setMaximumHeight(150)
        layout.addWidget(self.preview_edit)
        
        # ボタン群
        button_layout = QHBoxLayout()
        
        validate_btn = QPushButton("検証")
        validate_btn.clicked.connect(self.validate_json)
        button_layout.addWidget(validate_btn)
        
        clear_btn = QPushButton("クリア")
        clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_btn)
        
        button_layout.addStretch()
        
        self.import_btn = QPushButton("インポート")
        self.import_btn.clicked.connect(self.accept)
        self.import_btn.setEnabled(False)
        button_layout.addWidget(self.import_btn)
        
        cancel_btn = QPushButton("キャンセル")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def validate_json(self):
        """JSONを検証"""
        json_text = self.json_edit.toPlainText().strip()
        
        if not json_text:
            QMessageBox.warning(self, "警告", "JSONデータを入力してください")
            return
        
        # 検証実行
        is_valid, message, data = JSONBulkImporter.validate_json(json_text)
        
        if is_valid:
            self.validated_data = data
            
            # プレビュー生成
            preview = JSONBulkImporter.generate_preview(data)
            self.preview_edit.setPlainText(preview)
            
            self.import_btn.setEnabled(True)
            QMessageBox.information(self, "検証成功", "JSONデータは正常です")
        else:
            self.validated_data = None
            self.import_btn.setEnabled(False)
            self.preview_edit.clear()
            QMessageBox.critical(self, "検証エラー", message)
    
    def clear_all(self):
        """全てクリア"""
        self.json_edit.clear()
        self.preview_edit.clear()
        self.validated_data = None
        self.import_btn.setEnabled(False)
    
    def get_data(self):
        """検証済みデータを取得"""
        return self.validated_data