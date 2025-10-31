"""
Phase 3 実装プロジェクトモデル v2.0
"""
from datetime import datetime
from typing import Dict, List, Optional
from models.issue import Issue

class ImplementationProject:
    """実装プロジェクトを表すクラス（v2.0）"""
    
    def __init__(self, data: Dict = None):
        if data:
            self.project_id = data.get('project_id', '')
            self.project_name = data.get('project_name', '')
            self.import_info = data.get('import_info', {})
            self.code_requests = data.get('code_requests', [])
            self.deployed_files = data.get('deployed_files', [])
            self.test_results = data.get('test_results', [])
            self.bugs = data.get('bugs', [])
            self.ui_ux_notes = data.get('ui_ux_notes', [])
            
            # 問題管理（履歴型）
            self.issues = [Issue(i) for i in data.get('issues', [])]
            self.issue_counter = data.get('issue_counter', 1)
            
            # インポート履歴
            self.import_history = data.get('import_history', [])
            
            self.export_history = data.get('export_history', [])
            self.created_at = data.get('created_at', datetime.now().isoformat())
            self.updated_at = data.get('updated_at', datetime.now().isoformat())
        else:
            self.project_id = ''
            self.project_name = ''
            self.import_info = {}
            self.code_requests = []
            self.deployed_files = []
            self.test_results = []
            self.bugs = []
            self.ui_ux_notes = []
            self.issues = []
            self.issue_counter = 1
            self.import_history = []
            self.export_history = []
            self.created_at = datetime.now().isoformat()
            self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """辞書形式に変換"""
        return {
            'project_id': self.project_id,
            'project_name': self.project_name,
            'import_info': self.import_info,
            'code_requests': self.code_requests,
            'deployed_files': self.deployed_files,
            'test_results': self.test_results,
            'bugs': self.bugs,
            'ui_ux_notes': self.ui_ux_notes,
            'issues': [i.to_dict() for i in self.issues],
            'issue_counter': self.issue_counter,
            'import_history': self.import_history,
            'export_history': self.export_history,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def generate_issue_id(self) -> str:
        """新しい問題IDを生成"""
        issue_id = f"ISS{self.issue_counter:03d}"
        self.issue_counter += 1
        return issue_id
    
    def add_issue(self, title: str, description: str, impact: str = '中') -> Issue:
        """新しい問題を追加"""
        issue = Issue()
        issue.issue_id = self.generate_issue_id()
        issue.title = title
        issue.description = description
        issue.impact = impact
        issue.created_at = datetime.now().isoformat()
        issue.add_history('発見', description, '', 'manual')
        
        self.issues.append(issue)
        self.updated_at = datetime.now().isoformat()
        return issue
    
    def get_issue_by_id(self, issue_id: str) -> Optional[Issue]:
        """IDで問題を取得"""
        for issue in self.issues:
            if issue.issue_id == issue_id:
                return issue
        return None
    
    def update_issue_status(self, issue_id: str, status: str, notes: str = '', resolution: str = '', user: str = 'manual'):
        """問題のステータスを更新（履歴追加）"""
        issue = self.get_issue_by_id(issue_id)
        if issue:
            issue.add_history(status, notes, resolution, user)
            self.updated_at = datetime.now().isoformat()
    
    def get_unresolved_issues(self) -> List[Issue]:
        """未解決の問題を取得"""
        return [i for i in self.issues if i.is_unresolved()]
    
    def get_recurrent_issues(self) -> List[Issue]:
        """再発した問題を取得"""
        return [i for i in self.issues if i.recurrence_count > 0]
    
    def add_code_request(self, function_name: str, details: str, related_issues: List[str] = None, status: str = '依頼中') -> Dict:
        """コード依頼を追加"""
        request = {
            'id': len(self.code_requests) + 1,
            'function_name': function_name,
            'details': details,
            'request_date': datetime.now().isoformat(),
            'received_date': None,
            'status': status,
            'related_issues': related_issues or []
        }
        self.code_requests.append(request)
        self.updated_at = datetime.now().isoformat()
        return request
    
    def update_request_status(self, request_id: int, status: str, received_date: str = None):
        """依頼ステータスを更新"""
        for request in self.code_requests:
            if request['id'] == request_id:
                request['status'] = status
                if received_date:
                    request['received_date'] = received_date
                self.updated_at = datetime.now().isoformat()
                break
    
    def add_deployed_file(self, filename: str, filepath: str, status: str, notes: str = '') -> Dict:
        """配置ファイルを追加"""
        file_entry = {
            'id': len(self.deployed_files) + 1,
            'filename': filename,
            'filepath': filepath,
            'deployed_date': datetime.now().isoformat(),
            'status': status,
            'notes': notes
        }
        self.deployed_files.append(file_entry)
        self.updated_at = datetime.now().isoformat()
        return file_entry
    
    def add_test_result(self, function_name: str, result: str, notes: str = '') -> Dict:
        """テスト結果を追加"""
        test = {
            'id': len(self.test_results) + 1,
            'function_name': function_name,
            'test_date': datetime.now().isoformat(),
            'result': result,
            'notes': notes
        }
        self.test_results.append(test)
        self.updated_at = datetime.now().isoformat()
        return test
    
    def add_bug(self, title: str, description: str, severity: str = '中') -> Dict:
        """バグを追加"""
        bug = {
            'id': len(self.bugs) + 1,
            'title': title,
            'description': description,
            'severity': severity,
            'found_date': datetime.now().isoformat(),
            'status': '未対応',
            'resolved_date': None
        }
        self.bugs.append(bug)
        self.updated_at = datetime.now().isoformat()
        return bug
    
    def update_bug_status(self, bug_id: int, status: str, resolved_date: str = None):
        """バグステータスを更新"""
        for bug in self.bugs:
            if bug['id'] == bug_id:
                bug['status'] = status
                if resolved_date:
                    bug['resolved_date'] = resolved_date
                self.updated_at = datetime.now().isoformat()
                break
    
    def get_unresolved_bugs_count(self) -> int:
        """未解決バグ数を取得"""
        return sum(1 for bug in self.bugs if bug['status'] != '解決済み')
    
    def get_unresolved_issues_count(self) -> int:
        """未解決問題数を取得"""
        return len(self.get_unresolved_issues())
    
    def is_ready_for_export(self) -> tuple[bool, List[str]]:
        """エクスポート準備完了チェック"""
        errors = []
        
        # 未解決バグチェック
        unresolved_bugs = self.get_unresolved_bugs_count()
        if unresolved_bugs > 0:
            errors.append(f"未解決バグが{unresolved_bugs}件あります")
        
        # 未解決問題チェック
        unresolved_issues = self.get_unresolved_issues_count()
        if unresolved_issues > 0:
            errors.append(f"未解決問題が{unresolved_issues}件あります")
        
        # 未受領依頼チェック
        pending_requests = sum(1 for req in self.code_requests if req['status'] == '依頼中')
        if pending_requests > 0:
            errors.append(f"未受領の依頼が{pending_requests}件あります")
        
        return len(errors) == 0, errors
    
    def add_import_record(self, source: str, items_count: Dict):
        """インポート履歴を追加"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'items_count': items_count
        }
        self.import_history.append(record)
        self.updated_at = datetime.now().isoformat()