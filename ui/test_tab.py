"""
テスト・バグ管理タブ（編集機能追加版）
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QMessageBox, QLabel, QSplitter)
from PySide6.QtCore import Qt
from ui.dialogs import TestDialog, BugDialog

class TestTab(QWidget):
    """テスト・バグ管理タブ（編集機能追加版）"""
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        """UIを初期化"""
        layout = QVBoxLayout(self)
        
        # スプリッターで上下分割
        splitter = QSplitter(Qt.Vertical)
        
        # テスト結果セクション
        test_widget = self.create_test_section()
        splitter.addWidget(test_widget)
        
        # バグ管理セクション
        bug_widget = self.create_bug_section()
        splitter.addWidget(bug_widget)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
    
    def create_test_section(self) -> QWidget:
        """テスト結果セクションを作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # ヘッダー
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("<b>テスト結果</b>"))
        header_layout.addStretch()
        
        add_test_btn = QPushButton("テスト追加")
        add_test_btn.clicked.connect(self.add_test)
        header_layout.addWidget(add_test_btn)
        
        edit_test_btn = QPushButton("編集")
        edit_test_btn.clicked.connect(self.edit_test)
        header_layout.addWidget(edit_test_btn)
        
        delete_test_btn = QPushButton("削除")
        delete_test_btn.clicked.connect(self.delete_test)
        header_layout.addWidget(delete_test_btn)
        
        layout.addLayout(header_layout)
        
        # テーブル
        self.test_table = QTableWidget()
        self.test_table.setColumnCount(5)
        self.test_table.setHorizontalHeaderLabels([
            "ID", "機能名", "テスト日", "結果", "備考"
        ])
        
        header = self.test_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        
        # ダブルクリックで編集
        self.test_table.doubleClicked.connect(self.edit_test)
        
        layout.addWidget(self.test_table)
        
        return widget
    
    def create_bug_section(self) -> QWidget:
        """バグ管理セクションを作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # ヘッダー
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("<b>バグ管理</b>"))
        
        self.bug_count_label = QLabel("未解決: 0件")
        self.bug_count_label.setStyleSheet("color: red; font-weight: bold;")
        header_layout.addWidget(self.bug_count_label)
        
        header_layout.addStretch()
        
        add_bug_btn = QPushButton("バグ追加")
        add_bug_btn.clicked.connect(self.add_bug)
        header_layout.addWidget(add_bug_btn)
        
        edit_bug_btn = QPushButton("編集")
        edit_bug_btn.clicked.connect(self.edit_bug)
        header_layout.addWidget(edit_bug_btn)
        
        update_bug_btn = QPushButton("ステータス更新")
        update_bug_btn.clicked.connect(self.update_bug_status)
        header_layout.addWidget(update_bug_btn)
        
        delete_bug_btn = QPushButton("削除")
        delete_bug_btn.clicked.connect(self.delete_bug)
        header_layout.addWidget(delete_bug_btn)
        
        layout.addLayout(header_layout)
        
        # テーブル
        self.bug_table = QTableWidget()
        self.bug_table.setColumnCount(6)
        self.bug_table.setHorizontalHeaderLabels([
            "ID", "タイトル", "説明", "重要度", "発見日", "ステータス"
        ])
        
        header = self.bug_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        # ダブルクリックで編集
        self.bug_table.doubleClicked.connect(self.edit_bug)
        
        layout.addWidget(self.bug_table)
        
        return widget
    
    def refresh(self):
        """テーブルをリフレッシュ"""
        self.refresh_tests()
        self.refresh_bugs()
    
    def refresh_tests(self):
        """テスト結果テーブルをリフレッシュ"""
        self.test_table.setRowCount(0)
        
        if not self.main_window.current_project:
            return
        
        tests = self.main_window.current_project.test_results
        self.test_table.setRowCount(len(tests))
        
        for row, test in enumerate(tests):
            self.test_table.setItem(row, 0, QTableWidgetItem(str(test['id'])))
            self.test_table.setItem(row, 1, QTableWidgetItem(test['function_name']))
            self.test_table.setItem(row, 2, QTableWidgetItem(test['test_date'][:10]))
            
            result_item = QTableWidgetItem(test['result'])
            if test['result'] == 'OK':
                result_item.setBackground(Qt.green)
            elif test['result'] == 'NG':
                result_item.setBackground(Qt.red)
            self.test_table.setItem(row, 3, result_item)
            
            self.test_table.setItem(row, 4, QTableWidgetItem(test.get('notes', '')))
    
    def refresh_bugs(self):
        """バグテーブルをリフレッシュ"""
        self.bug_table.setRowCount(0)
        
        if not self.main_window.current_project:
            self.bug_count_label.setText("未解決: 0件")
            return
        
        bugs = self.main_window.current_project.bugs
        self.bug_table.setRowCount(len(bugs))
        
        unresolved_count = 0
        
        for row, bug in enumerate(bugs):
            self.bug_table.setItem(row, 0, QTableWidgetItem(str(bug['id'])))
            self.bug_table.setItem(row, 1, QTableWidgetItem(bug['title']))
            self.bug_table.setItem(row, 2, QTableWidgetItem(bug['description']))
            self.bug_table.setItem(row, 3, QTableWidgetItem(bug['severity']))
            self.bug_table.setItem(row, 4, QTableWidgetItem(bug['found_date'][:10]))
            
            status_item = QTableWidgetItem(bug['status'])
            if bug['status'] == '未対応':
                status_item.setBackground(Qt.red)
                unresolved_count += 1
            elif bug['status'] == '対応中':
                status_item.setBackground(Qt.yellow)
                unresolved_count += 1
            elif bug['status'] == '解決済み':
                status_item.setBackground(Qt.green)
            self.bug_table.setItem(row, 5, status_item)
        
        self.bug_count_label.setText(f"未解決: {unresolved_count}件")
    
    def add_test(self):
        """テストを追加"""
        if not self.main_window.current_project:
            QMessageBox.warning(self, "警告", "プロジェクトが選択されていません")
            return
        
        dialog = TestDialog(self)
        if dialog.exec():
            function_name, result, notes = dialog.get_data()
            self.main_window.current_project.add_test_result(function_name, result, notes)
            self.main_window.save_current_project()
            self.refresh_tests()
    
    def edit_test(self):
        """テストを編集"""
        if not self.main_window.current_project:
            return
        
        current_row = self.test_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "行を選択してください")
            return
        
        test_id = int(self.test_table.item(current_row, 0).text())
        
        # 既存データを取得
        test = None
        for t in self.main_window.current_project.test_results:
            if t['id'] == test_id:
                test = t
                break
        
        if not test:
            return
        
        # 編集ダイアログを表示
        dialog = TestDialog(self, edit_data=test)
        if dialog.exec():
            function_name, result, notes = dialog.get_data()
            
            # データを更新
            test['function_name'] = function_name
            test['result'] = result
            test['notes'] = notes
            
            self.main_window.save_current_project()
            self.refresh_tests()
    
    def delete_test(self):
        """テストを削除"""
        if not self.main_window.current_project:
            return
        
        current_row = self.test_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "行を選択してください")
            return
        
        reply = QMessageBox.question(
            self, "確認", "このテスト記録を削除しますか?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            test_id = int(self.test_table.item(current_row, 0).text())
            tests = self.main_window.current_project.test_results
            self.main_window.current_project.test_results = [
                t for t in tests if t['id'] != test_id
            ]
            self.main_window.save_current_project()
            self.refresh_tests()
    
    def add_bug(self):
        """バグを追加"""
        if not self.main_window.current_project:
            QMessageBox.warning(self, "警告", "プロジェクトが選択されていません")
            return
        
        dialog = BugDialog(self)
        if dialog.exec():
            title, description, severity = dialog.get_data()
            self.main_window.current_project.add_bug(title, description, severity)
            self.main_window.save_current_project()
            self.refresh_bugs()
    
    def edit_bug(self):
        """バグを編集"""
        if not self.main_window.current_project:
            return
        
        current_row = self.bug_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "行を選択してください")
            return
        
        bug_id = int(self.bug_table.item(current_row, 0).text())
        
        # 既存データを取得
        bug = None
        for b in self.main_window.current_project.bugs:
            if b['id'] == bug_id:
                bug = b
                break
        
        if not bug:
            return
        
        # 編集ダイアログを表示
        dialog = BugDialog(self, edit_data=bug)
        if dialog.exec():
            title, description, severity = dialog.get_data()
            
            # データを更新
            bug['title'] = title
            bug['description'] = description
            bug['severity'] = severity
            
            self.main_window.save_current_project()
            self.refresh_bugs()
    
    def update_bug_status(self):
        """バグステータスを更新"""
        if not self.main_window.current_project:
            return
        
        current_row = self.bug_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "行を選択してください")
            return
        
        bug_id = int(self.bug_table.item(current_row, 0).text())
        
        from PySide6.QtWidgets import QInputDialog
        from datetime import datetime
        
        statuses = ['未対応', '対応中', '解決済み']
        status, ok = QInputDialog.getItem(
            self, "ステータス更新", "新しいステータス:", statuses, 0, False
        )
        
        if ok:
            resolved_date = datetime.now().isoformat() if status == '解決済み' else None
            self.main_window.current_project.update_bug_status(bug_id, status, resolved_date)
            self.main_window.save_current_project()
            self.refresh_bugs()
    
    def delete_bug(self):
        """バグを削除"""
        if not self.main_window.current_project:
            return
        
        current_row = self.bug_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "行を選択してください")
            return
        
        reply = QMessageBox.question(
            self, "確認", "このバグ記録を削除しますか?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            bug_id = int(self.bug_table.item(current_row, 0).text())
            bugs = self.main_window.current_project.bugs
            self.main_window.current_project.bugs = [
                b for b in bugs if b['id'] != bug_id
            ]
            self.main_window.save_current_project()
            self.refresh_bugs()