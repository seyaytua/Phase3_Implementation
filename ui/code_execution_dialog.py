"""
コード実行ダイアログ - JSON からファイル作成コマンドを生成
"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QTextEdit, QPushButton, QMessageBox, QApplication,
                               QTabWidget, QWidget)
from PySide6.QtCore import Qt
import json
from typing import Dict, List
from utils.code_generator import CodeGenerator


class CodeExecutionDialog(QDialog):
    """JSON から実行コマンドを生成するダイアログ"""
    
    def __init__(self, work_dir: str, shell_type: str, parent=None):
        super().__init__(parent)
        self.work_dir = work_dir
        self.shell_type = shell_type
        self.code_generator = CodeGenerator()
        self.generated_commands = {}
        
        self.setWindowTitle("🚀 JSON実行 - ファイル作成コマンド生成")
        self.setMinimumSize(900, 700)
        self.init_ui()
    
    def init_ui(self):
        """UIを初期化"""
        layout = QVBoxLayout(self)
        
        # 説明ラベル
        info_label = QLabel(
            "📋 Claude から受け取った JSON を貼り付けて、ファイル作成コマンドを生成します。\n"
            f"📁 作業ディレクトリ: {self.work_dir}\n"
            f"💻 シェルタイプ: {self.shell_type}"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("background-color: #e3f2fd; padding: 10px; border-radius: 5px;")
        layout.addWidget(info_label)
        
        # JSON入力エリア
        layout.addWidget(QLabel("📥 JSON 入力:"))
        self.json_input = QTextEdit()
        self.json_input.setPlaceholderText(
            '{\n'
            '  "files": [\n'
            '    {\n'
            '      "filename": "user_model.py",\n'
            '      "filepath": "./models/user_model.py",\n'
            '      "description": "ユーザーデータモデル",\n'
            '      "content": "class User:\\n    pass"\n'
            '    }\n'
            '  ]\n'
            '}'
        )
        self.json_input.setMinimumHeight(150)
        layout.addWidget(self.json_input)
        
        # 生成ボタン
        generate_btn = QPushButton("🔧 コマンド生成")
        generate_btn.clicked.connect(self.generate_commands)
        generate_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; font-weight: bold;")
        layout.addWidget(generate_btn)
        
        # タブウィジェット（各シェル用）
        self.tab_widget = QTabWidget()
        
        # PowerShell タブ
        self.powershell_tab = QWidget()
        powershell_layout = QVBoxLayout(self.powershell_tab)
        self.powershell_output = QTextEdit()
        self.powershell_output.setReadOnly(True)
        self.powershell_output.setStyleSheet("font-family: 'Courier New', monospace; background-color: #1e1e1e; color: #d4d4d4;")
        powershell_layout.addWidget(self.powershell_output)
        
        powershell_copy_btn = QPushButton("📋 PowerShell コマンドをコピー")
        powershell_copy_btn.clicked.connect(lambda: self.copy_to_clipboard('powershell'))
        powershell_layout.addWidget(powershell_copy_btn)
        
        self.tab_widget.addTab(self.powershell_tab, "PowerShell")
        
        # Terminal タブ
        self.terminal_tab = QWidget()
        terminal_layout = QVBoxLayout(self.terminal_tab)
        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setStyleSheet("font-family: 'Courier New', monospace; background-color: #1e1e1e; color: #d4d4d4;")
        terminal_layout.addWidget(self.terminal_output)
        
        terminal_copy_btn = QPushButton("📋 Terminal コマンドをコピー")
        terminal_copy_btn.clicked.connect(lambda: self.copy_to_clipboard('terminal'))
        terminal_layout.addWidget(terminal_copy_btn)
        
        self.tab_widget.addTab(self.terminal_tab, "Terminal (Mac/Linux)")
        
        # CMD タブ
        self.cmd_tab = QWidget()
        cmd_layout = QVBoxLayout(self.cmd_tab)
        self.cmd_output = QTextEdit()
        self.cmd_output.setReadOnly(True)
        self.cmd_output.setStyleSheet("font-family: 'Courier New', monospace; background-color: #1e1e1e; color: #d4d4d4;")
        cmd_layout.addWidget(self.cmd_output)
        
        cmd_copy_btn = QPushButton("📋 CMD コマンドをコピー")
        cmd_copy_btn.clicked.connect(lambda: self.copy_to_clipboard('cmd'))
        cmd_layout.addWidget(cmd_copy_btn)
        
        self.tab_widget.addTab(self.cmd_tab, "CMD (Windows)")
        
        layout.addWidget(self.tab_widget)
        
        # 現在のシェルタイプに合わせてタブを選択
        if self.shell_type == 'powershell':
            self.tab_widget.setCurrentIndex(0)
        elif self.shell_type == 'terminal':
            self.tab_widget.setCurrentIndex(1)
        elif self.shell_type == 'cmd':
            self.tab_widget.setCurrentIndex(2)
        
        # 閉じるボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("閉じる")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
    
    def generate_commands(self):
        """JSON からコマンドを生成"""
        json_text = self.json_input.toPlainText().strip()
        
        if not json_text:
            QMessageBox.warning(self, "警告", "JSON を入力してください")
            return
        
        try:
            # JSON をパース
            data = json.loads(json_text)
            
            # files フィールドをチェック
            if 'files' not in data:
                QMessageBox.warning(
                    self, 
                    "警告", 
                    "JSON に 'files' フィールドが見つかりません"
                )
                return
            
            files = data['files']
            if not files:
                QMessageBox.warning(self, "警告", "ファイルリストが空です")
                return
            
            # 各シェル用のコマンドを生成
            self.generated_commands['powershell'] = self.code_generator.generate_powershell_commands(
                self.work_dir, files
            )
            self.generated_commands['terminal'] = self.code_generator.generate_terminal_commands(
                self.work_dir, files
            )
            self.generated_commands['cmd'] = self.code_generator.generate_cmd_commands(
                self.work_dir, files
            )
            
            # 各タブに表示
            self.powershell_output.setPlainText(self.generated_commands['powershell'])
            self.terminal_output.setPlainText(self.generated_commands['terminal'])
            self.cmd_output.setPlainText(self.generated_commands['cmd'])
            
            QMessageBox.information(
                self,
                "成功",
                f"✅ {len(files)} 個のファイル作成コマンドを生成しました！\n\n"
                f"各タブからコマンドをコピーして、シェルで実行してください。"
            )
            
        except json.JSONDecodeError as e:
            QMessageBox.critical(
                self,
                "JSON エラー",
                f"JSON の解析に失敗しました:\n{str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "エラー",
                f"コマンド生成中にエラーが発生しました:\n{str(e)}"
            )
    
    def copy_to_clipboard(self, shell_type: str):
        """指定されたシェルのコマンドをクリップボードにコピー"""
        if shell_type not in self.generated_commands:
            QMessageBox.warning(self, "警告", "先にコマンドを生成してください")
            return
        
        commands = self.generated_commands[shell_type]
        if not commands:
            QMessageBox.warning(self, "警告", "コマンドが空です")
            return
        
        clipboard = QApplication.clipboard()
        clipboard.setText(commands)
        
        shell_names = {
            'powershell': 'PowerShell',
            'terminal': 'Terminal',
            'cmd': 'CMD'
        }
        
        QMessageBox.information(
            self,
            "成功",
            f"✅ {shell_names[shell_type]} コマンドをクリップボードにコピーしました！\n\n"
            f"シェルに貼り付けて実行してください。"
        )
