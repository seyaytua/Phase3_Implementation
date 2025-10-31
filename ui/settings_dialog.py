"""
設定ダイアログ
"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QComboBox, QFileDialog,
                               QFormLayout, QGroupBox)
from PySide6.QtCore import Qt
from utils.config_manager import ConfigManager

class SettingsDialog(QDialog):
    """設定ダイアログ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = ConfigManager()
        self.setWindowTitle("設定")
        self.setMinimumWidth(600)
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 作業ディレクトリ設定
        dir_group = QGroupBox("作業ディレクトリ")
        dir_layout = QHBoxLayout()
        
        self.work_dir_edit = QLineEdit()
        self.work_dir_edit.setReadOnly(True)
        dir_layout.addWidget(self.work_dir_edit)
        
        browse_btn = QPushButton("参照...")
        browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(browse_btn)
        
        dir_group.setLayout(dir_layout)
        layout.addWidget(dir_group)
        
        # シェルタイプ設定
        shell_group = QGroupBox("シェルタイプ")
        shell_layout = QFormLayout()
        
        self.shell_combo = QComboBox()
        self.shell_combo.addItems(['PowerShell', 'Terminal (macOS/Linux)', 'Command Prompt'])
        shell_layout.addRow("使用するシェル:", self.shell_combo)
        
        shell_group.setLayout(shell_layout)
        layout.addWidget(shell_group)
        
        # 説明
        info_label = QLabel(
            "作業ディレクトリ: コード生成時の出力先ディレクトリ\n"
            "シェルタイプ: コマンド生成時に使用するシェル形式"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: gray; font-size: 10pt;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        # ボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton("保存")
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("キャンセル")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def load_settings(self):
        """現在の設定を読み込み"""
        config = self.config_manager.get_config()
        
        work_dir = config.get('work_directory', '')
        if work_dir:
            self.work_dir_edit.setText(work_dir)
        
        shell_type = config.get('shell_type', 'powershell')
        
        # shell_typeをコンボボックスのインデックスにマッピング
        shell_mapping = {
            'powershell': 0,
            'terminal': 1,
            'cmd': 2
        }
        
        index = shell_mapping.get(shell_type, 0)
        self.shell_combo.setCurrentIndex(index)
    
    def browse_directory(self):
        """ディレクトリを選択"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "作業ディレクトリを選択",
            self.work_dir_edit.text()
        )
        
        if directory:
            self.work_dir_edit.setText(directory)
    
    def save_settings(self):
        """設定を保存"""
        work_dir = self.work_dir_edit.text()
        shell_index = self.shell_combo.currentIndex()
        
        # インデックスをshell_typeにマッピング
        shell_types = ['powershell', 'terminal', 'cmd']
        shell_type = shell_types[shell_index]
        
        if not work_dir:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "警告",
                "作業ディレクトリを設定してください"
            )
            return
        
        self.config_manager.update_config({
            'work_directory': work_dir,
            'shell_type': shell_type
        })
        
        self.accept()
