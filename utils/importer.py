"""
Phase 2データインポート処理
"""
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Tuple
from models.implementation_project import ImplementationProject
from utils.validators import Validators
from utils.file_handler import FileHandler

class Importer:
    """Phase 2からのデータインポートを管理するクラス"""
    
    def __init__(self):
        self.file_handler = FileHandler()
        self.validators = Validators()
    
    def import_phase2_project(self, filepath: str) -> Tuple[bool, str, ImplementationProject]:
        """Phase 2プロジェクトをインポート"""
        try:
            # ファイル存在確認
            if not self.file_handler.file_exists(filepath):
                return False, "ファイルが見つかりません", None
            
            # JSONデータ読み込み
            data = self.file_handler.load_json(filepath)
            
            # バリデーション
            is_valid, errors = self.validators.validate_phase2_export(data)
            if not is_valid:
                return False, "\n".join(errors), None
            
            # チェックサム検証
            if 'checksum' in data:
                data_without_checksum = {k: v for k, v in data.items() if k != 'checksum'}
                data_str = json.dumps(data_without_checksum, sort_keys=True, ensure_ascii=False)
                if not self.validators.verify_checksum(data_str, data['checksum']):
                    return False, "チェックサムが一致しません。ファイルが改ざんされている可能性があります", None
            
            # Phase 2の実際の構造に対応してプロジェクトオブジェクト作成
            project_data = data['project']
            
            project = ImplementationProject()
            project.project_id = project_data['project_id']
            project.project_name = project_data['project_name']
            project.import_info = {
                'source_file': Path(filepath).name,
                'import_date': datetime.now().isoformat(),
                'phase2_export_date': data.get('exported_at'),
                'original_phase1_id': project_data.get('original_phase1_id'),
                'phase1_data': project_data.get('phase1_data', {}),
                'design_data': project_data.get('design_data', {}),
                'original_data': data
            }
            
            # インポートファイルをコピー
            import_dir = Path('data/imports')
            import_dir.mkdir(parents=True, exist_ok=True)
            dest_file = import_dir / Path(filepath).name
            self.file_handler.copy_file(filepath, str(dest_file))
            
            return True, "インポートが完了しました", project
            
        except Exception as e:
            return False, f"インポートエラー: {str(e)}", None