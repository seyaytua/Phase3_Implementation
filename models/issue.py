"""
問題（Issue）モデル
"""
from datetime import datetime
from typing import Dict, List

class IssueHistory:
    """問題履歴エントリ"""
    
    def __init__(self, data: Dict = None):
        if data:
            self.timestamp = data.get('timestamp', datetime.now().isoformat())
            self.status = data.get('status', '発見')
            self.notes = data.get('notes', '')
            self.resolution = data.get('resolution', '')
            self.user = data.get('user', 'manual')
        else:
            self.timestamp = datetime.now().isoformat()
            self.status = '発見'
            self.notes = ''
            self.resolution = ''
            self.user = 'manual'
    
    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp,
            'status': self.status,
            'notes': self.notes,
            'resolution': self.resolution,
            'user': self.user
        }


class Issue:
    """問題モデル"""
    
    def __init__(self, data: Dict = None):
        if data:
            self.issue_id = data.get('issue_id', '')
            self.title = data.get('title', '')
            self.description = data.get('description', '')
            self.impact = data.get('impact', '中')
            self.created_at = data.get('created_at', datetime.now().isoformat())
            self.history = [IssueHistory(h) for h in data.get('history', [])]
            self.current_status = data.get('current_status', '発見')
            self.recurrence_count = data.get('recurrence_count', 0)
            self.last_updated = data.get('last_updated', datetime.now().isoformat())
            self.related_requests = data.get('related_requests', [])
        else:
            self.issue_id = ''
            self.title = ''
            self.description = ''
            self.impact = '中'
            self.created_at = datetime.now().isoformat()
            self.history = []
            self.current_status = '発見'
            self.recurrence_count = 0
            self.last_updated = datetime.now().isoformat()
            self.related_requests = []
    
    def to_dict(self) -> Dict:
        return {
            'issue_id': self.issue_id,
            'title': self.title,
            'description': self.description,
            'impact': self.impact,
            'created_at': self.created_at,
            'history': [h.to_dict() for h in self.history],
            'current_status': self.current_status,
            'recurrence_count': self.recurrence_count,
            'last_updated': self.last_updated,
            'related_requests': self.related_requests
        }
    
    def add_history(self, status: str, notes: str = '', resolution: str = '', user: str = 'manual'):
        """履歴を追加"""
        history_entry = IssueHistory()
        history_entry.timestamp = datetime.now().isoformat()
        history_entry.status = status
        history_entry.notes = notes
        history_entry.resolution = resolution
        history_entry.user = user
        
        self.history.append(history_entry)
        self.current_status = status
        self.last_updated = datetime.now().isoformat()
        
        # 再発カウント
        if status == '再発':
            self.recurrence_count += 1
    
    def get_status_color(self) -> str:
        """ステータスに応じた色を返す"""
        status_colors = {
            '発見': 'orange',
            '対応中': 'yellow',
            '解決': 'green',
            '再発': 'red'
        }
        return status_colors.get(self.current_status, 'gray')
    
    def is_unresolved(self) -> bool:
        """未解決かどうか"""
        return self.current_status in ['発見', '対応中', '再発']
    
    def get_timeline_summary(self) -> str:
        """タイムライン要約を取得"""
        summary = []
        for h in self.history:
            date = h.timestamp[:10]
            summary.append(f"{date} [{h.status}] {h.notes[:30]}")
        return "\n".join(summary)