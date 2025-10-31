"""
コード依頼管理タブ v3.0（プロンプト生成機能付き）
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QMessageBox, QApplication, QTextEdit, QDialog,
                               QLabel)
from PySide6.QtCore import Qt
from datetime import datetime
from typing import Dict
from ui.dialogs import RequestDialog
from utils.implementation_prompt_generator import ImplementationPromptGenerator
from utils.code_generator import CodeGenerator

class PromptDisplayDialog(QDialog):
    """生成されたプロンプトを表示するダイアログ"""
    
    def __init__(self, prompt: str, title: str = "生成されたプロンプト", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(800, 600)
        self.prompt = prompt
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        info_label = QLabel("以下のプロンプトがクリップボードにコピーされました。\nClaude に貼り付けて質問してください。")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(self.prompt)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)
        
        button_layout = QHBoxLayout()
        
        copy_btn = QPushButton("再コピー")
        copy_btn.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(copy_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("閉じる")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
    
    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.prompt)
        QMessageBox.information(self, "成功", "クリップボードにコピーしました")


class RequestTab(QWidget):
    """コード依頼管理タブ v3.0"""
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.prompt_gen = ImplementationPromptGenerator()
        self.code_gen = CodeGenerator()
        self.init_ui()
    
    def init_ui(self):
        """UIを初期化"""
        layout = QVBoxLayout(self)
        
        # ボタン群
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("新規依頼")
        add_btn.clicked.connect(self.add_request)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("編集")
        edit_btn.clicked.connect(self.edit_request)
        button_layout.addWidget(edit_btn)
        
        update_btn = QPushButton("ステータス更新")
        update_btn.clicked.connect(self.update_status)
        button_layout.addWidget(update_btn)
        
        delete_btn = QPushButton("削除")
        delete_btn.clicked.connect(self.delete_request)
        button_layout.addWidget(delete_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # テーブル
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "機能名", "依頼内容", "依頼日", "受領日", "ステータス",
            "依頼コピー", "プロンプト生成", "チェック"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        
        self.table.doubleClicked.connect(self.edit_request)
        
        layout.addWidget(self.table)
    
    def refresh(self):
        """テーブルをリフレッシュ"""
        self.table.setRowCount(0)
        
        if not self.main_window.current_project:
            return
        
        requests = self.main_window.current_project.code_requests
        self.table.setRowCount(len(requests))
        
        for row, request in enumerate(requests):
            # 基本情報
            self.table.setItem(row, 0, QTableWidgetItem(str(request['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(request['function_name']))
            self.table.setItem(row, 2, QTableWidgetItem(request['details'][:50] + "..."))
            self.table.setItem(row, 3, QTableWidgetItem(request['request_date'][:10]))
            
            received = request.get('received_date', '')
            self.table.setItem(row, 4, QTableWidgetItem(received[:10] if received else '-'))
            
            status_item = QTableWidgetItem(request['status'])
            if request['status'] == '依頼中':
                status_item.setBackground(Qt.yellow)
            elif request['status'] == '受領済み':
                status_item.setBackground(Qt.green)
            self.table.setItem(row, 5, status_item)
            
            # 依頼コピーボタン
            copy_btn = QPushButton("📋 コピー")
            copy_btn.clicked.connect(lambda checked, r=request: self.copy_request_details(r))
            self.table.setCellWidget(row, 6, copy_btn)
            
            # プロンプト生成ボタン
            prompt_btn = QPushButton("🤖 プロンプト")
            prompt_btn.clicked.connect(lambda checked, r=request: self.generate_implementation_prompt(r))
            self.table.setCellWidget(row, 7, prompt_btn)
            
            # チェックボタン
            check_btn = QPushButton("✅ チェック")
            check_btn.clicked.connect(lambda checked, r=request: self.generate_check_prompt(r))
            self.table.setCellWidget(row, 8, check_btn)
    
    def copy_request_details(self, request: Dict):
        """依頼内容をクリップボードにコピー"""
        details = f"""【機能名】
{request['function_name']}

【依頼内容】
{request['details']}
"""
        clipboard = QApplication.clipboard()
        clipboard.setText(details)
        QMessageBox.information(self, "成功", "依頼内容をクリップボードにコピーしました")
    
    def generate_implementation_prompt(self, request: Dict):
        """実装用プロンプトを生成"""
        if not self.main_window.current_project:
            return
        
        # 作業ディレクトリチェック
        work_dir = self.main_window.config_manager.get_work_directory()
        if not work_dir:
            QMessageBox.warning(
                self,
                "警告",
                "作業ディレクトリが設定されていません。\n"
                "メニューの「設定」から作業ディレクトリを設定してください。"
            )
            return
        
        # シェルタイプ取得
        shell_type = self.main_window.config_manager.get_shell_type()
        
        # Phase 2データ取得
        phase2_data = self.main_window.current_project.import_info.get('original_data', {})
        
        # プロンプト生成
        prompt = self.prompt_gen.generate_implementation_prompt(
            request, phase2_data, shell_type
        )
        
        # クリップボードにコピー
        clipboard = QApplication.clipboard()
        clipboard.setText(prompt)
        
        # ダイアログで表示
        dialog = PromptDisplayDialog(prompt, "実装依頼プロンプト", self)
        dialog.exec()
    
    def generate_check_prompt(self, request: Dict):
        """チェック用プロンプトを生成"""
        if not self.main_window.current_project:
            return
        
        # 作業ディレクトリチェック
        work_dir = self.main_window.config_manager.get_work_directory()
        if not work_dir:
            QMessageBox.warning(
                self,
                "警告",
                "作業ディレクトリが設定されていません。"
            )
            return
        
        # プロンプト生成
        prompt = self.prompt_gen.generate_check_prompt(request, work_dir)
        
        # クリップボードにコピー
        clipboard = QApplication.clipboard()
        clipboard.setText(prompt)
        
        # ダイアログで表示
        dialog = PromptDisplayDialog(prompt, "チェック用プロンプト", self)
        dialog.exec()
    
    def add_request(self):
        """新規依頼を追加"""
        if not self.main_window.current_project:
            QMessageBox.warning(self, "警告", "プロジェクトが選択されていません")
            return
        
        dialog = RequestDialog(self)
        if dialog.exec():
            function_name, details = dialog.get_data()
            self.main_window.current_project.add_code_request(function_name, details)
            self.main_window.save_current_project()
            self.refresh()
    
    def edit_request(self):
        """依頼を編集"""
        if not self.main_window.current_project:
            return
        
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "行を選択してください")
            return
        
        request_id = int(self.table.item(current_row, 0).text())
        
        request = None
        for r in self.main_window.current_project.code_requests:
            if r['id'] == request_id:
                request = r
                break
        
        if not request:
            return
        
        dialog = RequestDialog(self, edit_data=request)
        if dialog.exec():
            function_name, details = dialog.get_data()
            request['function_name'] = function_name
            request['details'] = details
            self.main_window.save_current_project()
            self.refresh()
    
    def update_status(self):
        """ステータスを更新"""
        if not self.main_window.current_project:
            return
        
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "行を選択してください")
            return
        
        request_id = int(self.table.item(current_row, 0).text())
        
        from PySide6.QtWidgets import QInputDialog
        statuses = ['依頼中', '受領済み', '保留中']
        status, ok = QInputDialog.getItem(
            self, "ステータス更新", "新しいステータス:", statuses, 0, False
        )
        
        if ok:
            received_date = datetime.now().isoformat() if status == '受領済み' else None
            self.main_window.current_project.update_request_status(
                request_id, status, received_date
            )
            self.main_window.save_current_project()
            self.refresh()
    
    def delete_request(self):
        """依頼を削除"""
        if not self.main_window.current_project:
            return
        
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "行を選択してください")
            return
        
        reply = QMessageBox.question(
            self, "確認", "この依頼を削除しますか?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            request_id = int(self.table.item(current_row, 0).text())
            requests = self.main_window.current_project.code_requests
            self.main_window.current_project.code_requests = [
                r for r in requests if r['id'] != request_id
            ]
            self.main_window.save_current_project()
            self.refresh()
