"""
Phase 3 メインウィンドウ v3.0（設定機能追加版）
"""
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QComboBox, QLabel, QTabWidget,
                               QMessageBox, QFileDialog, QStatusBar, QApplication)
from PySide6.QtCore import Qt
from models.implementation_manager import ImplementationManager
from utils.importer import Importer
from utils.exporter import Exporter
from utils.prompt_generator import PromptGenerator
from utils.json_bulk_importer import JSONBulkImporter
from utils.config_manager import ConfigManager
from ui.request_tab import RequestTab
from ui.deploy_tab import DeployTab
from ui.test_tab import TestTab
from ui.issue_tab import IssueTab
from ui.import_dialog import ImportDialog
from ui.settings_dialog import SettingsDialog

class MainWindow(QMainWindow):
    """メインウィンドウクラス v3.0"""
    
    def __init__(self):
        super().__init__()
        self.manager = ImplementationManager()
        self.importer = Importer()
        self.exporter = Exporter()
        self.prompt_generator = PromptGenerator()
        self.json_importer = JSONBulkImporter()
        self.config_manager = ConfigManager()
        self.current_project = None
        
        self.init_ui()
        self.load_projects()
    
    def init_ui(self):
        """UIを初期化"""
        self.setWindowTitle("Phase 3 - 実装管理ツール v3.0")
        self.setGeometry(100, 100, 1400, 900)
        
        # 中央ウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # メインレイアウト
        main_layout = QVBoxLayout(central_widget)
        
        # ヘッダー部分
        header_layout = self.create_header()
        main_layout.addLayout(header_layout)
        
        # タブウィジェット
        self.tab_widget = QTabWidget()
        
        # 各タブを作成
        self.request_tab = RequestTab(self)
        self.deploy_tab = DeployTab(self)
        self.test_tab = TestTab(self)
        self.issue_tab = IssueTab(self)
        
        self.tab_widget.addTab(self.request_tab, "コード依頼管理")
        self.tab_widget.addTab(self.deploy_tab, "コード配置記録")
        self.tab_widget.addTab(self.test_tab, "テスト・バグ管理")
        self.tab_widget.addTab(self.issue_tab, "問題追跡（履歴型）")
        
        main_layout.addWidget(self.tab_widget)
        
        # ステータスバー
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status_bar()
    
    def create_header(self) -> QHBoxLayout:
        """ヘッダー部分を作成"""
        header_layout = QHBoxLayout()
        
        # プロジェクト選択
        header_layout.addWidget(QLabel("プロジェクト:"))
        self.project_combo = QComboBox()
        self.project_combo.setMinimumWidth(300)
        self.project_combo.currentTextChanged.connect(self.on_project_changed)
        header_layout.addWidget(self.project_combo)
        
        header_layout.addStretch()
        
        # Phase 2インポートボタン
        import_phase2_btn = QPushButton("Phase 2からインポート")
        import_phase2_btn.clicked.connect(self.import_phase2_project)
        header_layout.addWidget(import_phase2_btn)
        
        # 設定ボタン（新機能）
        settings_btn = QPushButton("⚙️ 設定")
        settings_btn.setToolTip("作業ディレクトリとシェルタイプを設定")
        settings_btn.clicked.connect(self.open_settings)
        header_layout.addWidget(settings_btn)
        
        # プロンプト生成ボタン
        prompt_btn = QPushButton("📋 プロンプト生成")
        prompt_btn.setToolTip("Claude用のプロンプトを生成してクリップボードにコピー")
        prompt_btn.clicked.connect(self.generate_prompt)
        header_layout.addWidget(prompt_btn)
        
        # JSON取り込みボタン
        json_import_btn = QPushButton("📥 JSON取り込み")
        json_import_btn.setToolTip("Claudeからの回答JSONを一括インポート")
        json_import_btn.clicked.connect(self.import_json_bulk)
        header_layout.addWidget(json_import_btn)
        
        # Phase 4エクスポートボタン
        export_btn = QPushButton("Phase 4へエクスポート")
        export_btn.clicked.connect(self.export_to_phase4)
        header_layout.addWidget(export_btn)
        
        return header_layout
    
    def update_status_bar(self):
        """ステータスバーを更新"""
        config = self.config_manager.get_config()
        work_dir = config.get('work_directory', '未設定')
        shell_type = config.get('shell_type', '未設定')
        
        self.status_bar.showMessage(
            f"作業ディレクトリ: {work_dir} | シェル: {shell_type} | v3.0"
        )
    
    def open_settings(self):
        """設定ダイアログを開く（新機能）"""
        dialog = SettingsDialog(self)
        if dialog.exec():
            # 設定を再読み込み（重要！）
            self.config_manager.config = self.config_manager.load_config()
            
            # RequestTabのconfig_managerも同じインスタンスなので自動で反映される
            # ステータスバーを更新
            self.update_status_bar()
            
            QMessageBox.information(
                self,
                "設定保存完了",
                "✅ 設定が保存されました。\n\n"
                "作業ディレクトリとシェルタイプがすぐに使用可能です。"
            )
    
    def load_projects(self):
        """プロジェクトリストを読み込み"""
        self.project_combo.clear()
        project_names = self.manager.get_project_names()
        
        if project_names:
            self.project_combo.addItems(project_names)
        else:
            self.project_combo.addItem("(プロジェクトなし)")
    
    def on_project_changed(self, project_name: str):
        """プロジェクト選択変更時"""
        if project_name and project_name != "(プロジェクトなし)":
            for project in self.manager.projects:
                if project.project_name == project_name:
                    self.current_project = project
                    self.refresh_all_tabs()
                    self.status_bar.showMessage(f"プロジェクト '{project_name}' を選択しました")
                    break
        else:
            self.current_project = None
            self.refresh_all_tabs()
    
    def refresh_all_tabs(self):
        """全タブをリフレッシュ"""
        self.request_tab.refresh()
        self.deploy_tab.refresh()
        self.test_tab.refresh()
        self.issue_tab.refresh()
    
    def import_phase2_project(self):
        """Phase 2プロジェクトをインポート"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Phase 2エクスポートファイルを選択",
            "",
            "JSON Files (*.json)"
        )
        
        if not filepath:
            return
        
        success, message, project = self.importer.import_phase2_project(filepath)
        
        if success:
            if self.manager.project_exists(project.project_id):
                QMessageBox.warning(
                    self,
                    "重複エラー",
                    "このプロジェクトは既にインポート済みです"
                )
                return
            
            self.manager.add_project(project)
            self.load_projects()
            
            index = self.project_combo.findText(project.project_name)
            if index >= 0:
                self.project_combo.setCurrentIndex(index)
            
            QMessageBox.information(self, "成功", message)
            self.status_bar.showMessage("インポート完了")
        else:
            QMessageBox.critical(self, "エラー", message)
    
    def generate_prompt(self):
        """プロンプトを生成してクリップボードにコピー"""
        if not self.current_project:
            QMessageBox.warning(self, "警告", "プロジェクトが選択されていません")
            return
        
        try:
            prompt = self.prompt_generator.generate_full_prompt(self.current_project)
            
            clipboard = QApplication.clipboard()
            clipboard.setText(prompt)
            
            QMessageBox.information(
                self,
                "成功",
                "プロンプトをクリップボードにコピーしました。\n\n"
                "Claude に貼り付けて質問してください。"
            )
            self.status_bar.showMessage("プロンプトをクリップボードにコピーしました", 5000)
            
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"プロンプト生成エラー:\n{str(e)}")
    
    def import_json_bulk(self):
        """JSON一括インポート"""
        if not self.current_project:
            QMessageBox.warning(self, "警告", "プロジェクトが選択されていません")
            return
        
        dialog = ImportDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            
            if not data:
                QMessageBox.warning(self, "警告", "データが検証されていません")
                return
            
            success, message, stats = self.json_importer.import_to_project(
                self.current_project, data
            )
            
            if success:
                self.save_current_project()
                self.refresh_all_tabs()
                
                QMessageBox.information(self, "成功", message)
                self.status_bar.showMessage("JSON一括インポート完了", 5000)
            else:
                QMessageBox.critical(self, "エラー", message)
    
    def export_to_phase4(self):
        """Phase 4へエクスポート"""
        if not self.current_project:
            QMessageBox.warning(self, "警告", "プロジェクトが選択されていません")
            return
        
        success, message, filepath = self.exporter.export_to_phase4(self.current_project)
        
        if success:
            self.manager.update_project(self.current_project)
            
            QMessageBox.information(
                self,
                "成功",
                f"{message}\n\nファイル: {filepath}"
            )
            self.status_bar.showMessage("エクスポート完了")
        else:
            QMessageBox.warning(self, "エクスポート不可", message)
    
    def save_current_project(self):
        """現在のプロジェクトを保存"""
        if self.current_project:
            self.manager.update_project(self.current_project)
            self.status_bar.showMessage("保存しました", 3000)
