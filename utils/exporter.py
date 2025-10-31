"""
Phase 4へのエクスポート処理（修正版）
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Tuple
from models.implementation_project import ImplementationProject
from utils.validators import Validators
from utils.file_handler import FileHandler

class Exporter:
    """Phase 4へのデータエクスポートを管理するクラス"""
    
    def __init__(self):
        self.file_handler = FileHandler()
        self.validators = Validators()
    
    def export_to_phase4(self, project: ImplementationProject) -> Tuple[bool, str, str]:
        """Phase 4用にエクスポート"""
        try:
            # エクスポート準備完了チェック
            is_ready, errors = self.validators.validate_export_readiness(project)
            if not is_ready:
                return False, "エクスポート準備が完了していません:\n" + "\n".join(errors), ""
            
            # エクスポートデータ作成（Issueオブジェクトを辞書に変換）
            export_data = {
                'project_id': project.project_id,
                'project_name': project.project_name,
                'phase': 'Phase3',
                'export_date': datetime.now().isoformat(),
                'code_requests': project.code_requests,
                'deployed_files': project.deployed_files,
                'test_results': project.test_results,
                'bugs': project.bugs,
                'ui_ux_notes': project.ui_ux_notes,
                'issues': [issue.to_dict() for issue in project.issues],
                'import_info': project.import_info
            }
            
            # チェックサム計算
            data_str = json.dumps(export_data, sort_keys=True, ensure_ascii=False)
            checksum = self.validators.calculate_checksum(data_str)
            export_data['checksum'] = checksum
            
            # エクスポートファイル保存
            export_dir = Path('data/exports')
            export_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f"export_{project.project_id}_Phase3.json"
            filepath = export_dir / filename
            
            self.file_handler.save_json(export_data, str(filepath))
            
            # エクスポート履歴を記録
            project.export_history.append({
                'export_date': datetime.now().isoformat(),
                'filename': filename,
                'checksum': checksum
            })
            
            return True, "エクスポートが完了しました", str(filepath)
            
        except Exception as e:
            return False, f"エクスポートエラー: {str(e)}", ""
