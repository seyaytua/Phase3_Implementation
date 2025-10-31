"""
Phase 3 実装管理ツール - メインエントリーポイント
"""
import sys
import json
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from ui.main_window import MainWindow
from utils.file_handler import FileHandler

def setup_directories():
    """必要なディレクトリを作成"""
    directories = [
        'data',
        'data/imports',
        'data/exports',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def initialize_data_file():
    """データファイルを初期化"""
    data_file = Path('data/phase3_implementations.json')
    
    if not data_file.exists():
        initial_data = {
            "version": "1.0",
            "projects": [],
            "last_updated": None
        }
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, indent=2, ensure_ascii=False)

def main():
    """メインアプリケーション起動"""
    try:
        # ディレクトリとデータファイルの初期化
        setup_directories()
        initialize_data_file()
        
        # アプリケーション起動
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        
        # メインウィンドウ表示
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec())
        
    except Exception as e:
        QMessageBox.critical(
            None,
            "起動エラー",
            f"アプリケーションの起動に失敗しました:\n{str(e)}"
        )
        sys.exit(1)

if __name__ == '__main__':
    main()