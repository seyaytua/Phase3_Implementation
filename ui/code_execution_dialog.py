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
        self.parsed_files = []  # パース済みファイル情報を保存
        
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
        
        # 生成ボタン群
        button_row = QHBoxLayout()
        
        generate_btn = QPushButton("🔧 コマンド生成")
        generate_btn.clicked.connect(self.generate_commands)
        generate_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; font-weight: bold;")
        button_row.addWidget(generate_btn)
        
        ai_check_btn = QPushButton("✅ AI確認用プロンプト")
        ai_check_btn.setToolTip("生成したコマンドをAIに確認してもらうプロンプトを生成")
        ai_check_btn.clicked.connect(self.generate_ai_check_prompt)
        ai_check_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px; font-weight: bold;")
        button_row.addWidget(ai_check_btn)
        
        single_file_btn = QPushButton("📄 1ファイルずつ生成")
        single_file_btn.setToolTip("エラー時用：各ファイルを個別に生成")
        single_file_btn.clicked.connect(self.generate_single_file_commands)
        single_file_btn.setStyleSheet("background-color: #FF5722; color: white; padding: 8px; font-weight: bold;")
        button_row.addWidget(single_file_btn)
        
        layout.addLayout(button_row)
        
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
            
            # ファイル情報を保存（AI確認や1ファイルずつ生成で使用）
            self.parsed_files = files
            
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
    
    def generate_ai_check_prompt(self):
        """AI確認用プロンプトを生成"""
        if not self.generated_commands:
            QMessageBox.warning(
                self,
                "警告",
                "先にコマンドを生成してください"
            )
            return
        
        # 現在のタブに応じたシェルタイプを取得
        current_index = self.tab_widget.currentIndex()
        shell_types = ['powershell', 'terminal', 'cmd']
        current_shell = shell_types[current_index]
        
        shell_names = {
            'powershell': 'PowerShell',
            'terminal': 'Terminal (Mac/Linux)',
            'cmd': 'Command Prompt (Windows)'
        }
        
        current_command = self.generated_commands.get(current_shell, '')
        
        if not current_command:
            QMessageBox.warning(self, "警告", "コマンドが空です")
            return
        
        # AI確認用プロンプトを生成
        ai_prompt = f"""# シェルコマンド構文チェック依頼

## 依頼内容
以下の**{shell_names[current_shell]}**コマンドの構文が正しいか確認してください。
エラーがあれば修正し、正しいコマンドを提供してください。

---

## 確認対象コマンド

```bash
{current_command}
```

---

## チェック項目

1. **構文エラーの確認**
   - クォート（'、"、`）の対応
   - 改行文字の適切な処理
   - エスケープシーケンスの確認
   - EOF、'@などのヒアドキュメント終端の正確性

2. **ファイル作成の確実性**
   - ディレクトリ作成コマンドの確認
   - ファイルパスの正確性
   - 文字エンコーディング（UTF-8）の指定

3. **実行可能性**
   - コマンドが{shell_names[current_shell]}で正常に実行できるか
   - 特殊文字の適切な処理

---

## 出力形式

**エラーがない場合:**
```
✅ コマンドは正しいです。そのまま実行可能です。
```

**エラーがある場合:**
```
❌ 以下のエラーを発見しました：

【エラー内容】
- エラー1の説明
- エラー2の説明

【修正版コマンド】
```bash
修正されたコマンド全体
```
```

---

それでは、上記のコマンドを確認してください。
"""
        
        # クリップボードにコピー
        clipboard = QApplication.clipboard()
        clipboard.setText(ai_prompt)
        
        # ダイアログで表示
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel
        
        dialog = QDialog(self)
        dialog.setWindowTitle("✅ AI確認用プロンプト")
        dialog.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(dialog)
        
        info = QLabel(
            "以下のプロンプトをクリップボードにコピーしました。\n"
            "Claude に貼り付けて、コマンドの構文を確認してもらってください。"
        )
        info.setWordWrap(True)
        info.setStyleSheet("background-color: #fff3cd; padding: 10px; border-radius: 5px;")
        layout.addWidget(info)
        
        text_edit = QTextEdit()
        text_edit.setPlainText(ai_prompt)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        
        close_btn = QPushButton("閉じる")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.exec()
    
    def generate_single_file_commands(self):
        """1ファイルずつのコマンドを生成"""
        if not self.parsed_files:
            QMessageBox.warning(
                self,
                "警告",
                "先にJSON入力からコマンドを生成してください"
            )
            return
        
        # 現在のタブに応じたシェルタイプを取得
        current_index = self.tab_widget.currentIndex()
        shell_types = ['powershell', 'terminal', 'cmd']
        current_shell = shell_types[current_index]
        
        shell_names = {
            'powershell': 'PowerShell',
            'terminal': 'Terminal (Mac/Linux)',
            'cmd': 'Command Prompt (Windows)'
        }
        
        # 各ファイルごとにコマンドを生成
        single_commands = []
        
        for i, file_info in enumerate(self.parsed_files, 1):
            single_file_list = [file_info]
            
            if current_shell == 'powershell':
                cmd = self.code_generator.generate_powershell_commands(self.work_dir, single_file_list)
            elif current_shell == 'terminal':
                cmd = self.code_generator.generate_terminal_commands(self.work_dir, single_file_list)
            else:  # cmd
                cmd = self.code_generator.generate_cmd_commands(self.work_dir, single_file_list)
            
            single_commands.append(f"# ========== ファイル {i}/{len(self.parsed_files)}: {file_info['filename']} ==========\n\n{cmd}\n")
        
        result_text = "\n".join(single_commands)
        
        # AI用プロンプトを生成
        ai_prompt = f"""# 1ファイルずつ確実に作成する依頼

## 状況
一括でファイル作成を試みましたがエラーが発生しました。
各ファイルを個別に確実に作成するため、1ファイルずつコマンドを提供します。

---

## {shell_names[current_shell]} コマンド（1ファイルずつ）

{result_text}

---

## 実行手順の指示

**以下の手順で、1ファイルずつ確実に作成してください：**

1. **ファイル1のコマンドをコピー**してシェルに貼り付け → Enter で実行
2. **エラーがないか確認** → エラーがあれば報告してください
3. **成功したら次のファイル2へ進む**
4. 全ファイルが成功するまで繰り返し

---

## エラーが発生した場合

**以下の情報を提供してください：**
- エラーメッセージ全文
- どのファイルで発生したか（ファイル名）
- エラーが発生した行番号（あれば）

修正したコマンドを個別に提供します。

---

それでは、ファイル1から順番に実行を開始してください。
各ファイルの実行結果を報告してください。
"""
        
        # クリップボードにコピー
        clipboard = QApplication.clipboard()
        clipboard.setText(ai_prompt)
        
        # ダイアログで表示
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel
        
        dialog = QDialog(self)
        dialog.setWindowTitle("📄 1ファイルずつ生成")
        dialog.setMinimumSize(900, 700)
        
        layout = QVBoxLayout(dialog)
        
        info = QLabel(
            f"✅ {len(self.parsed_files)} 個のファイルを個別に作成するプロンプトを生成しました。\n"
            "クリップボードにコピー済みです。Claude に貼り付けて指示に従ってください。"
        )
        info.setWordWrap(True)
        info.setStyleSheet("background-color: #d4edda; padding: 10px; border-radius: 5px;")
        layout.addWidget(info)
        
        text_edit = QTextEdit()
        text_edit.setPlainText(ai_prompt)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        
        close_btn = QPushButton("閉じる")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.exec()
