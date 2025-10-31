"""
設定管理ユーティリティ
"""
import json
from pathlib import Path
from typing import Dict, Optional

class ConfigManager:
    """アプリケーション設定を管理するクラス"""
    
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = Path(config_file)
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """設定を読み込み"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.get_default_config()
        return self.get_default_config()
    
    def save_config(self):
        """設定を保存"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get_default_config(self) -> Dict:
        """デフォルト設定を取得"""
        return {
            'work_directory': '',
            'shell_type': 'powershell',  # powershell, terminal, cmd
            'last_project_id': '',
            'window_geometry': {},
            'recent_projects': []
        }
    
    def get_work_directory(self) -> str:
        """作業ディレクトリを取得"""
        return self.config.get('work_directory', '')
    
    def set_work_directory(self, directory: str):
        """作業ディレクトリを設定"""
        self.config['work_directory'] = directory
        self.save_config()
    
    def get_shell_type(self) -> str:
        """シェルタイプを取得"""
        return self.config.get('shell_type', 'powershell')
    
    def set_shell_type(self, shell_type: str):
        """シェルタイプを設定"""
        if shell_type in ['powershell', 'terminal', 'cmd']:
            self.config['shell_type'] = shell_type
            self.save_config()
    
    def get_last_project_id(self) -> str:
        """最後に開いたプロジェクトIDを取得"""
        return self.config.get('last_project_id', '')
    
    def set_last_project_id(self, project_id: str):
        """最後に開いたプロジェクトIDを設定"""
        self.config['last_project_id'] = project_id
        self.save_config()
