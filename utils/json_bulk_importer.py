"""
JSON一括インポートユーティリティ
"""
import json
from datetime import datetime
from typing import Dict, List, Tuple
from models.implementation_project import ImplementationProject

class JSONBulkImporter:
    """JSON一括インポートを管理するクラス"""
    
    @staticmethod
    def validate_json(json_text: str) -> Tuple[bool, str, Dict]:
        """JSONの形式を検証"""
        try:
            data = json.loads(json_text)
            
            # 必須フィールドの確認
            if not isinstance(data, dict):
                return False, "JSONはオブジェクト形式である必要があります", None
            
            # 各セクションの確認
            valid_sections = [
                'issue_updates',
                'code_requests',
                'deployed_files',
                'test_results',
                'bugs'
            ]
            
            # 少なくとも1つのセクションが必要
            has_data = any(section in data for section in valid_sections)
            if not has_data:
                return False, "有効なデータセクションが見つかりません", None
            
            return True, "検証成功", data
            
        except json.JSONDecodeError as e:
            return False, f"JSON形式エラー: {str(e)}", None
        except Exception as e:
            return False, f"検証エラー: {str(e)}", None
    
    @staticmethod
    def import_to_project(project: ImplementationProject, data: Dict) -> Tuple[bool, str, Dict]:
        """プロジェクトにデータをインポート"""
        try:
            stats = {
                'issue_updates': 0,
                'issue_creates': 0,
                'code_requests': 0,
                'deployed_files': 0,
                'test_results': 0,
                'bugs': 0,
                'errors': []
            }
            
            # 問題の更新・作成
            if 'issue_updates' in data:
                for issue_data in data['issue_updates']:
                    try:
                        success = JSONBulkImporter._process_issue_update(
                            project, issue_data
                        )
                        if success:
                            if issue_data.get('action') == 'create':
                                stats['issue_creates'] += 1
                            else:
                                stats['issue_updates'] += 1
                    except Exception as e:
                        stats['errors'].append(f"問題処理エラー: {str(e)}")
            
            # コード依頼
            if 'code_requests' in data:
                for req_data in data['code_requests']:
                    try:
                        project.add_code_request(
                            req_data.get('function_name', ''),
                            req_data.get('details', ''),
                            req_data.get('related_issues', []),
                            req_data.get('status', '依頼中')
                        )
                        stats['code_requests'] += 1
                    except Exception as e:
                        stats['errors'].append(f"コード依頼エラー: {str(e)}")
            
            # 配置ファイル
            if 'deployed_files' in data:
                for file_data in data['deployed_files']:
                    try:
                        project.add_deployed_file(
                            file_data.get('filename', ''),
                            file_data.get('filepath', ''),
                            file_data.get('status', 'OK'),
                            file_data.get('notes', '')
                        )
                        stats['deployed_files'] += 1
                    except Exception as e:
                        stats['errors'].append(f"ファイル配置エラー: {str(e)}")
            
            # テスト結果
            if 'test_results' in data:
                for test_data in data['test_results']:
                    try:
                        project.add_test_result(
                            test_data.get('function_name', ''),
                            test_data.get('result', 'OK'),
                            test_data.get('notes', '')
                        )
                        stats['test_results'] += 1
                    except Exception as e:
                        stats['errors'].append(f"テスト結果エラー: {str(e)}")
            
            # バグ
            if 'bugs' in data:
                for bug_data in data['bugs']:
                    try:
                        project.add_bug(
                            bug_data.get('title', ''),
                            bug_data.get('description', ''),
                            bug_data.get('severity', '中')
                        )
                        stats['bugs'] += 1
                    except Exception as e:
                        stats['errors'].append(f"バグ登録エラー: {str(e)}")
            
            # インポート履歴を記録
            project.add_import_record('json_bulk_import', {
                'issue_updates': stats['issue_updates'],
                'issue_creates': stats['issue_creates'],
                'code_requests': stats['code_requests'],
                'deployed_files': stats['deployed_files'],
                'test_results': stats['test_results'],
                'bugs': stats['bugs']
            })
            
            # 結果メッセージ
            message = f"""インポート完了:
- 問題更新: {stats['issue_updates']}件
- 問題新規作成: {stats['issue_creates']}件
- コード依頼: {stats['code_requests']}件
- 配置ファイル: {stats['deployed_files']}件
- テスト結果: {stats['test_results']}件
- バグ: {stats['bugs']}件
"""
            
            if stats['errors']:
                message += f"\nエラー: {len(stats['errors'])}件\n"
                message += "\n".join(stats['errors'][:5])
            
            return True, message, stats
            
        except Exception as e:
            return False, f"インポートエラー: {str(e)}", None
    
    @staticmethod
    def _process_issue_update(project: ImplementationProject, issue_data: Dict) -> bool:
        """問題の更新または作成を処理"""
        action = issue_data.get('action', 'create')
        issue_id = issue_data.get('issue_id')
        
        if action == 'update' and issue_id:
            # 既存問題の更新
            project.update_issue_status(
                issue_id,
                issue_data.get('new_status', '対応中'),
                issue_data.get('notes', ''),
                issue_data.get('resolution', ''),
                'json_import'
            )
            return True
            
        elif action == 'create':
            # 新規問題の作成
            issue = project.add_issue(
                issue_data.get('title', ''),
                issue_data.get('description', ''),
                issue_data.get('impact', '中')
            )
            
            # 初回以外のステータスがある場合は追加
            if issue_data.get('new_status') and issue_data.get('new_status') != '発見':
                project.update_issue_status(
                    issue.issue_id,
                    issue_data.get('new_status'),
                    issue_data.get('notes', ''),
                    issue_data.get('resolution', ''),
                    'json_import'
                )
            
            return True
        
        return False
    
    @staticmethod
    def generate_preview(data: Dict) -> str:
        """インポート内容のプレビューを生成"""
        preview = "=== インポート内容プレビュー ===\n\n"
        
        if 'issue_updates' in data:
            preview += f"【問題更新・作成】 {len(data['issue_updates'])}件\n"
            for issue in data['issue_updates'][:3]:
                action_text = "更新" if issue.get('action') == 'update' else "新規"
                issue_id = issue.get('issue_id', '(新規)')
                title = issue.get('title', issue.get('notes', ''))[:30]
                preview += f"  - [{action_text}] {issue_id}: {title}\n"
            if len(data['issue_updates']) > 3:
                preview += f"  ... 他 {len(data['issue_updates']) - 3}件\n"
            preview += "\n"
        
        if 'code_requests' in data:
            preview += f"【コード依頼】 {len(data['code_requests'])}件\n"
            for req in data['code_requests'][:3]:
                preview += f"  - {req.get('function_name', '')}[:30]\n"
            if len(data['code_requests']) > 3:
                preview += f"  ... 他 {len(data['code_requests']) - 3}件\n"
            preview += "\n"
        
        if 'deployed_files' in data:
            preview += f"【配置ファイル】 {len(data['deployed_files'])}件\n"
            for file in data['deployed_files'][:3]:
                preview += f"  - {file.get('filename', '')}\n"
            if len(data['deployed_files']) > 3:
                preview += f"  ... 他 {len(data['deployed_files']) - 3}件\n"
            preview += "\n"
        
        if 'test_results' in data:
            preview += f"【テスト結果】 {len(data['test_results'])}件\n"
        
        if 'bugs' in data:
            preview += f"【バグ】 {len(data['bugs'])}件\n"
        
        return preview