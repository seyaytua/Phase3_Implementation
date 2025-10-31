"""
問題追跡タブ v2.0（履歴型）
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QMessageBox, QLabel, QTextEdit, QDialog,
                               QSplitter, QGroupBox, QFormLayout, QComboBox,
                               QLineEdit)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from ui.dialogs import IssueDialog

class IssueHistoryDialog(QDialog):
    """問題履歴詳細ダイアログ"""
    
    def __init__(self, issue, parent=None):
        super().__init__(parent)
        self.issue = issue
        self.setWindowTitle(f"問題履歴: {issue.issue_id}")
        self.setMinimumSize(700, 500)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 基本情報
        info_group = QGroupBox("基本情報")
        info_layout = QFormLayout()
        info_layout.addRow("問題ID:", QLabel(self.issue.issue_id))
        info_layout.addRow("タイトル:", QLabel(self.issue.title))
        info_layout.addRow("影響範囲:", QLabel(self.issue.impact))
        info_layout.addRow("現在のステータス:", QLabel(self.issue.current_status))
        info_layout.addRow("再発回数:", QLabel(str(self.issue.recurrence_count)))
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # 説明
        desc_group = QGroupBox("説明")
        desc_layout = QVBoxLayout()
        desc_text = QTextEdit()
        desc_text.setPlainText(self.issue.description)
        desc_text.setReadOnly(True)
        desc_text.setMaximumHeight(100)
        desc_layout.addWidget(desc_text)
        desc_group.setLayout(desc_layout)
        layout.addWidget(desc_group)
        
        # 履歴タイムライン
        history_group = QGroupBox("履歴タイムライン")
        history_layout = QVBoxLayout()
        
        timeline_text = QTextEdit()
        timeline_text.setReadOnly(True)
        
        timeline_content = ""
        for h in self.issue.history:
            date = h.timestamp[:16].replace('T', ' ')
            timeline_content += f"● {date} [{h.status}]\n"
            timeline_content += f"  {h.notes}\n"
            if h.resolution:
                timeline_content += f"  解決策: {h.resolution}\n"
            timeline_content += f"  記録者: {h.user}\n\n"
        
        timeline_text.setPlainText(timeline_content)
        history_layout.addWidget(timeline_text)
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
        
        # 閉じるボタン
        close_btn = QPushButton("閉じる")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


class IssueUpdateDialog(QDialog):
    """問題ステータス更新ダイアログ"""
    
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
        form_layout.addRow("新しいステータス:", self.status_combo)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setMinimumHeight(100)
        self.notes_edit.setPlaceholderText("状況説明を入力してください")
        form_layout.addRow("状況説明:", self.notes_edit)
        
        self.resolution_edit = QTextEdit()
        self.resolution_edit.setMinimumHeight(100)
        self.resolution_edit.setPlaceholderText("解決策を入力してください（解決時のみ）")
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
            self.notes_edit.toPlainText(),
            self.resolution_edit.toPlainText()
        )


class IssueTab(QWidget):
    """問題追跡タブ v2.0"""
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        """UIを初期化"""
        layout = QVBoxLayout(self)
        
        # ヘッダー
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("<b>問題追跡（履歴型）</b>"))
        
        self.issue_count_label = QLabel("未解決: 0件 | 再発: 0件")
        self.issue_count_label.setStyleSheet("color: red; font-weight: bold;")
        header_layout.addWidget(self.issue_count_label)
        
        header_layout.addStretch()
        
        add_btn = QPushButton("問題追加")
        add_btn.clicked.connect(self.add_issue)
        header_layout.addWidget(add_btn)
        
        update_btn = QPushButton("ステータス更新")
        update_btn.clicked.connect(self.update_issue)
        header_layout.addWidget(update_btn)
        
        history_btn = QPushButton("履歴詳細")
        history_btn.clicked.connect(self.show_history)
        header_layout.addWidget(history_btn)
        
        layout.addLayout(header_layout)
        
        # テーブル
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "タイトル", "影響", "現在のステータス", "再発回数", "最終更新", "履歴数"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.table)
    
    def refresh(self):
        """テーブルをリフレッシュ"""
        self.table.setRowCount(0)
        
        if not self.main_window.current_project:
            self.issue_count_label.setText("未解決: 0件 | 再発: 0件")
            return
        
        issues = self.main_window.current_project.issues
        self.table.setRowCount(len(issues))
        
        unresolved_count = 0
        recurrent_count = 0
        
        for row, issue in enumerate(issues):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(issue.issue_id))
            
            # タイトル
            self.table.setItem(row, 1, QTableWidgetItem(issue.title))
            
            # 影響範囲
            impact_item = QTableWidgetItem(issue.impact)
            if issue.impact == '高':
                impact_item.setBackground(QColor(255, 200, 200))
            self.table.setItem(row, 2, impact_item)
            
            # ステータス
            status_item = QTableWidgetItem(issue.current_status)
            if issue.current_status == '発見':
                status_item.setBackground(QColor(255, 200, 100))
            elif issue.current_status == '対応中':
                status_item.setBackground(QColor(255, 255, 100))
            elif issue.current_status == '解決':
                status_item.setBackground(QColor(100, 255, 100))
            elif issue.current_status == '再発':
                status_item.setBackground(QColor(255, 100, 100))
            self.table.setItem(row, 3, status_item)
            
            # 再発回数
            recur_item = QTableWidgetItem(str(issue.recurrence_count))
            if issue.recurrence_count > 0:
                recur_item.setBackground(QColor(255, 150, 150))
                recurrent_count += 1
            self.table.setItem(row, 4, recur_item)
            
            # 最終更新
            self.table.setItem(row, 5, QTableWidgetItem(issue.last_updated[:16].replace('T', ' ')))
            
            # 履歴数
            self.table.setItem(row, 6, QTableWidgetItem(str(len(issue.history))))
            
            if issue.is_unresolved():
                unresolved_count += 1
        
        self.issue_count_label.setText(f"未解決: {unresolved_count}件 | 再発: {recurrent_count}件")
    
    def add_issue(self):
        """問題を追加"""
        if not self.main_window.current_project:
            QMessageBox.warning(self, "警告", "プロジェクトが選択されていません")
            return
        
        dialog = IssueDialog(self)
        if dialog.exec():
            title, description, impact = dialog.get_data()
            self.main_window.current_project.add_issue(title, description, impact)
            self.main_window.save_current_project()
            self.refresh()
    
    def update_issue(self):
        """問題ステータスを更新"""
        if not self.main_window.current_project:
            return
        
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "行を選択してください")
            return
        
        issue_id = self.table.item(current_row, 0).text()
        
        dialog = IssueUpdateDialog(self)
        if dialog.exec():
            status, notes, resolution = dialog.get_data()
            self.main_window.current_project.update_issue_status(
                issue_id, status, notes, resolution, 'manual'
            )
            self.main_window.save_current_project()
            self.refresh()
    
    def show_history(self):
        """履歴詳細を表示"""
        if not self.main_window.current_project:
            return
        
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "行を選択してください")
            return
        
        issue_id = self.table.item(current_row, 0).text()
        issue = self.main_window.current_project.get_issue_by_id(issue_id)
        
        if issue:
            dialog = IssueHistoryDialog(issue, self)
            dialog.exec()