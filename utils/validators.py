"""
バリデーションユーティリティ
"""
import hashlib
from typing import Dict, List, Tuple

class Validators:
    """データ検証を行うクラス"""
    
    @staticmethod
    def calculate_checksum(data: str) -> str:
        """チェックサムを計算"""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    @staticmethod
    def verify_checksum(data: str, expected_checksum: str) -> bool:
        """チェックサムを検証"""
        actual_checksum = Validators.calculate_checksum(data)
        return actual_checksum == expected_checksum
    
    @staticmethod
    def validate_phase2_export(data: Dict) -> Tuple[bool, List[str]]:
        """Phase 2エクスポートファイルを検証"""
        errors = []
        
        # Phase 2の実際の構造に対応
        if 'project' in data:
            project = data['project']
            
            # 必須フィールドチェック（project内）
            if 'project_id' not in project:
                errors.append("必須フィールド 'project.project_id' が見つかりません")
            
            if 'project_name' not in project:
                errors.append("必須フィールド 'project.project_name' が見つかりません")
            
            # プロジェクトIDチェック
            if not project.get('project_id'):
                errors.append("プロジェクトIDが空です")
        else:
            errors.append("'project' フィールドが見つかりません")
        
        # ソースチェック（Phase 2からのエクスポートか確認）
        if data.get('source') != 'Phase2_Design':
            errors.append("Phase 2のエクスポートファイルではありません")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_export_readiness(project) -> Tuple[bool, List[str]]:
        """エクスポート準備完了を検証"""
        return project.is_ready_for_export()