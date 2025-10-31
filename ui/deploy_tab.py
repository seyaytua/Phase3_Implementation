"""
コード配置記録タブ（編集機能追加版）
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QMessageBox)
from PySide6.QtCore import Qt
from ui.dialogs import DeployDialog

class DeployTab(QWidget):
    """コード配置記録タブ（編集機能追加版）"""
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        """UIを初期化"""
        layout = QVBoxLayout(self)
        
        # ボタン群
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("ファイル追加")
        add_btn.clicked.connect(self.add_file)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("編集")
        edit_btn.clicked.connect(self.edit_file)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("削除")
        delete_btn.clicked.connect(self.delete_file)
        button_layout.addWidget(delete_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # テーブル
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "ファイル名", "配置パス", "配置日", "動作確認", "備考"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        
        # ダブルクリックで編集
        self.table.doubleClicked.connect(self.edit_file)
        
        layout.addWidget(self.table)
    
    def refresh(self):
        """テーブルをリフレッシュ"""
        self.table.setRowCount(0)
        
        if not self.main_window.current_project:
            return
        
        files = self.main_window.current_project.deployed_files
        self.table.setRowCount(len(files))
        
        for row, file_entry in enumerate(files):
            self.table.setItem(row, 0, QTableWidgetItem(str(file_entry['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(file_entry['filename']))
            self.table.setItem(row, 2, QTableWidgetItem(file_entry['filepath']))
            self.table.setItem(row, 3, QTableWidgetItem(file_entry['deployed_date'][:10]))
            
            status_item = QTableWidgetItem(file_entry['status'])
            if file_entry['status'] == 'OK':
                status_item.setBackground(Qt.green)
            elif file_entry['status'] == 'NG':
                status_item.setBackground(Qt.red)
            self.table.setItem(row, 4, status_item)
            
            self.table.setItem(row, 5, QTableWidgetItem(file_entry.get('notes', '')))
    
    def add_file(self):
        """ファイルを追加"""
        if not self.main_window.current_project:
            QMessageBox.warning(self, "警告", "プロジェクトが選択されていません")
            return
        
        dialog = DeployDialog(self)
        if dialog.exec():
            filename, filepath, status, notes = dialog.get_data()
            self.main_window.current_project.add_deployed_file(
                filename, filepath, status, notes
            )
            self.main_window.save_current_project()
            self.refresh()
    
    def edit_file(self):
        """ファイルを編集"""
        if not self.main_window.current_project:
            return
        
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "行を選択してください")
            return
        
        file_id = int(self.table.item(current_row, 0).text())
        
        # 既存データを取得
        file_entry = None
        for f in self.main_window.current_project.deployed_files:
            if f['id'] == file_id:
                file_entry = f
                break
        
        if not file_entry:
            return
        
        # 編集ダイアログを表示
        dialog = DeployDialog(self, edit_data=file_entry)
        if dialog.exec():
            filename, filepath, status, notes = dialog.get_data()
            
            # データを更新
            file_entry['filename'] = filename
            file_entry['filepath'] = filepath
            file_entry['status'] = status
            file_entry['notes'] = notes
            
            self.main_window.save_current_project()
            self.refresh()
    
    def delete_file(self):
        """ファイルを削除"""
        if not self.main_window.current_project:
            return
        
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "行を選択してください")
            return
        
        reply = QMessageBox.question(
            self, "確認", "このファイル記録を削除しますか?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            file_id = int(self.table.item(current_row, 0).text())
            files = self.main_window.current_project.deployed_files
            self.main_window.current_project.deployed_files = [
                f for f in files if f['id'] != file_id
            ]
            self.main_window.save_current_project()
            self.refresh()