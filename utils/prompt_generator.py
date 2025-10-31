"""
プロンプト自動生成ユーティリティ
"""
from models.implementation_project import ImplementationProject

class PromptGenerator:
    """Claude 用プロンプトを自動生成するクラス"""
    
    @staticmethod
    def generate_full_prompt(project):
        """完全なプロンプトを生成"""
        project_info = PromptGenerator._generate_project_info(project)
        issue_history = PromptGenerator._generate_issue_history(project)
        request_status = PromptGenerator._generate_request_status(project)
        json_schema = PromptGenerator._get_json_schema()
        
        prompt = "# Phase 3 実装管理 - 問題追跡と次の対応依頼\n\n"
        prompt += project_info + "\n\n"
        prompt += issue_history + "\n\n"
        prompt += request_status + "\n\n"
        prompt += "## 今回の依頼\n\n"
        prompt += "上記の全履歴を踏まえて、以下のJSON形式で次の対応を提案してください：\n\n"
        prompt += "```json\n"
        prompt += json_schema + "\n"
        prompt += "```\n\n"
        prompt += "特に以下の点を確認してください：\n"
        prompt += "1. 未解決の問題に対する具体的な対応策\n"
        prompt += "2. 再発している問題の根本原因分析\n"
        prompt += "3. 新たに必要なコード依頼\n"
        prompt += "4. 実装済み機能のテスト計画\n"
        
        return prompt
    
    @staticmethod
    def _generate_project_info(project):
        """プロジェクト情報セクションを生成"""
        phase1_data = project.import_info.get('phase1_data', {})
        main_features = phase1_data.get('main_features', [])
        features_str = ', '.join(main_features) if main_features else '未設定'
        import_date = project.import_info.get('import_date', '未設定')[:10]
        
        info = "## プロジェクト情報\n"
        info += f"- プロジェクトID: {project.project_id}\n"
        info += f"- プロジェクト名: {project.project_name}\n"
        info += f"- Phase 1主要機能: {features_str}\n"
        info += f"- Phase 2インポート日: {import_date}\n"
        
        return info
    
    @staticmethod
    def _generate_issue_history(project):
        """問題履歴セクションを生成"""
        if not project.issues:
            return "## これまでの問題履歴\n\n（まだ問題は記録されていません）"
        
        history_text = "## これまでの問題履歴（全て）\n\n"
        
        for issue in project.issues:
            recurrence_mark = f" ⚠️ 再発{issue.recurrence_count}回" if issue.recurrence_count > 0 else ""
            status_mark = "🔴" if issue.is_unresolved() else "✅"
            
            history_text += f"### {status_mark} {issue.issue_id}: {issue.title}{recurrence_mark}\n"
            history_text += f"- 影響範囲: {issue.impact}\n"
            history_text += f"- 現在のステータス: {issue.current_status}\n"
            history_text += "- 履歴:\n"
            
            for h in issue.history:
                date = h.timestamp[:16].replace('T', ' ')
                resolution_text = f" - 解決策: {h.resolution}" if h.resolution else ""
                history_text += f"  - {date} [{h.status}] {h.notes}{resolution_text}\n"
            
            history_text += "\n"
        
        return history_text
    
    @staticmethod
    def _generate_request_status(project):
        """コード依頼状況セクションを生成"""
        if not project.code_requests:
            return "## 現在のコード依頼状況\n\n（まだコード依頼はありません）"
        
        status_text = "## 現在のコード依頼状況\n\n"
        
        pending = [r for r in project.code_requests if r['status'] == '依頼中']
        received = [r for r in project.code_requests if r['status'] == '受領済み']
        
        status_text += f"- 依頼中: {len(pending)}件\n"
        status_text += f"- 受領済み: {len(received)}件\n\n"
        
        if pending:
            status_text += "### 未受領の依頼\n"
            for req in pending:
                related_issues = req.get('related_issues', [])
                related = f" (関連問題: {', '.join(related_issues)})" if related_issues else ""
                status_text += f"- {req['function_name']}{related}\n"
        
        return status_text
    
    @staticmethod
    def _get_json_schema():
        """JSONスキーマを返す"""
        schema = '{\n'
        schema += '  "issue_updates": [\n'
        schema += '    {\n'
        schema += '      "issue_id": "ISS001 または null（新規の場合）",\n'
        schema += '      "action": "update または create",\n'
        schema += '      "title": "問題タイトル（新規の場合のみ）",\n'
        schema += '      "description": "詳細説明（新規の場合のみ）",\n'
        schema += '      "impact": "低/中/高",\n'
        schema += '      "new_status": "発見/対応中/解決/再発",\n'
        schema += '      "notes": "今回の状況説明",\n'
        schema += '      "resolution": "解決策（解決時のみ）"\n'
        schema += '    }\n'
        schema += '  ],\n'
        schema += '  "code_requests": [\n'
        schema += '    {\n'
        schema += '      "function_name": "機能名",\n'
        schema += '      "details": "詳細な依頼内容",\n'
        schema += '      "related_issues": ["ISS001", "ISS002"],\n'
        schema += '      "status": "依頼中"\n'
        schema += '    }\n'
        schema += '  ],\n'
        schema += '  "deployed_files": [\n'
        schema += '    {\n'
        schema += '      "filename": "ファイル名",\n'
        schema += '      "filepath": "配置パス",\n'
        schema += '      "status": "OK/NG/未確認",\n'
        schema += '      "notes": "備考"\n'
        schema += '    }\n'
        schema += '  ],\n'
        schema += '  "test_results": [\n'
        schema += '    {\n'
        schema += '      "function_name": "機能名",\n'
        schema += '      "result": "OK/NG",\n'
        schema += '      "notes": "テスト内容"\n'
        schema += '    }\n'
        schema += '  ],\n'
        schema += '  "bugs": [\n'
        schema += '    {\n'
        schema += '      "title": "バグタイトル",\n'
        schema += '      "description": "詳細",\n'
        schema += '      "severity": "低/中/高/致命的",\n'
        schema += '      "status": "未対応"\n'
        schema += '    }\n'
        schema += '  ]\n'
        schema += '}'
        
        return schema