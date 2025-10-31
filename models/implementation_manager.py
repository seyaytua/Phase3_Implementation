"""
Phase 3 実装プロジェクト管理マネージャー
"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from models.implementation_project import ImplementationProject
from utils.file_handler import FileHandler

class ImplementationManager:
    """実装プロジェクトの管理を行うクラス"""
    
    def __init__(self, data_file: str = 'data/phase3_implementations.json'):
        self.data_file = Path(data_file)
        self.file_handler = FileHandler()
        self.projects: List[ImplementationProject] = []
        self.load_projects()
    
    def load_projects(self):
        """プロジェクトデータを読み込み"""
        if self.data_file.exists():
            data = self.file_handler.load_json(str(self.data_file))
            self.projects = [ImplementationProject(p) for p in data.get('projects', [])]
    
    def save_projects(self):
        """プロジェクトデータを保存"""
        data = {
            'version': '1.0',
            'projects': [p.to_dict() for p in self.projects],
            'last_updated': datetime.now().isoformat()
        }
        
        # バックアップ作成
        if self.data_file.exists():
            backup_file = self.data_file.with_suffix('.json.backup')
            self.file_handler.copy_file(str(self.data_file), str(backup_file))
        
        # 保存
        self.file_handler.save_json(data, str(self.data_file))
    
    def get_project_by_id(self, project_id: str) -> Optional[ImplementationProject]:
        """IDでプロジェクトを取得"""
        for project in self.projects:
            if project.project_id == project_id:
                return project
        return None
    
    def get_project_names(self) -> List[str]:
        """プロジェクト名リストを取得"""
        return [p.project_name for p in self.projects]
    
    def add_project(self, project: ImplementationProject):
        """プロジェクトを追加"""
        self.projects.append(project)
        self.save_projects()
    
    def update_project(self, project: ImplementationProject):
        """プロジェクトを更新"""
        for i, p in enumerate(self.projects):
            if p.project_id == project.project_id:
                self.projects[i] = project
                self.save_projects()
                break
    
    def delete_project(self, project_id: str) -> bool:
        """プロジェクトを削除"""
        for i, p in enumerate(self.projects):
            if p.project_id == project_id:
                self.projects.pop(i)
                self.save_projects()
                return True
        return False
    
    def project_exists(self, project_id: str) -> bool:
        """プロジェクトが存在するかチェック"""
        return any(p.project_id == project_id for p in self.projects)