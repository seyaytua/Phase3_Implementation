"""
ファイル操作ユーティリティ
"""
import json
import shutil
from pathlib import Path
from typing import Dict, Any

class FileHandler:
    """ファイル操作を管理するクラス"""
    
    @staticmethod
    def load_json(filepath: str) -> Dict[str, Any]:
        """JSONファイルを読み込み"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"JSONファイルの読み込みに失敗しました: {str(e)}")
    
    @staticmethod
    def save_json(data: Dict[str, Any], filepath: str):
        """JSONファイルに保存"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"JSONファイルの保存に失敗しました: {str(e)}")
    
    @staticmethod
    def copy_file(src: str, dst: str):
        """ファイルをコピー"""
        try:
            shutil.copy2(src, dst)
        except Exception as e:
            raise Exception(f"ファイルのコピーに失敗しました: {str(e)}")
    
    @staticmethod
    def file_exists(filepath: str) -> bool:
        """ファイルの存在確認"""
        return Path(filepath).exists()
    
    @staticmethod
    def create_directory(dirpath: str):
        """ディレクトリを作成"""
        Path(dirpath).mkdir(parents=True, exist_ok=True)