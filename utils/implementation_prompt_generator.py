"""
実装用プロンプト生成ユーティリティ
"""
from typing import Dict

class ImplementationPromptGenerator:
    """実装依頼用プロンプトを生成するクラス"""
    
    @staticmethod
    def generate_implementation_prompt(request: Dict, phase2_data: Dict, shell_type: str = 'powershell') -> str:
        """実装依頼用プロンプトを生成"""
        
        # Phase 2の設計情報を抽出
        design_data = phase2_data.get('design_data', {})
        tech_stack = design_data.get('tech_stack', {})
        data_models = design_data.get('data_models', [])
        screens = design_data.get('screens', [])
        
        prompt = f"""# コード実装依頼

## 依頼内容
**機能名:** {request.get('function_name', '')}

**詳細:**
{request.get('details', '')}

---

## プロジェクト情報

**技術スタック:**
- GUIフレームワーク: {tech_stack.get('gui_framework', 'PySide6 6.10.0')}
- データ保存形式: {tech_stack.get('data_storage', 'JSON')}
- 使用可能ライブラリ: WinPython標準ライブラリのみ

**重要な制約:**
1. 外部ライブラリの追加インストール不可
2. データベースはJSON形式のみ使用
3. ファイル操作は標準ライブラリ（os, pathlib, shutil）のみ

---

## 設計情報（参考）

"""
        
        # データモデル情報を追加
        if data_models:
            prompt += "**データモデル:**\n"
            for model in data_models[:3]:  # 最初の3つのみ
                prompt += f"- {model.get('model_name', '')}: {model.get('description', '')}\n"
            prompt += "\n"
        
        # 画面情報を追加
        if screens:
            prompt += "**関連画面:**\n"
            for screen in screens[:3]:  # 最初の3つのみ
                prompt += f"- {screen.get('screen_name', '')}: {screen.get('description', '')}\n"
            prompt += "\n"
        
        prompt += """---

## 出力形式の指定

以下のJSON形式で回答してください：

```json
{
  "files": [
    {
      "filename": "ファイル名（例: user_manager.py）",
      "filepath": "相対パス（例: ./models/user_manager.py）",
      "description": "ファイルの説明",
      "content": "ファイルの完全なコード内容"
    }
  ],
  "dependencies": [
    "必要なインポート文のリスト"
  ],
  "installation_notes": "セットアップ手順や注意事項",
  "test_instructions": "動作確認方法"
}
```

**重要:**
- `content` フィールドには完全なコードを含めてください
- コメントは日本語で記述してください
- エラーハンドリングを含めてください
- 型ヒント（typing）を使用してください

**シェル環境:**
"""
        
        shell_names = {
            'powershell': 'PowerShell (Windows)',
            'terminal': 'Terminal (Mac/Linux)',
            'cmd': 'コマンドプロンプト (Windows)'
        }
        
        prompt += f"使用シェル: {shell_names.get(shell_type, 'PowerShell')}\n\n"
        
        # 文字数制限の注意を追加
        prompt += """---

## ⚠️ 重要: 回答の分割について

**プロンプトが長い場合、以下のルールで回答を分割してください：**

1. **1回の回答は10,000文字以内**に収めてください
2. 複数ファイルがある場合は、**1～2ファイルずつ**分けて回答してください
3. 分割する場合は以下の形式で：

**【パート 1/3】**
```json
{
  "files": [
    {
      "filename": "file1.py",
      "filepath": "./models/file1.py",
      "content": "..."
    }
  ]
}
```

**【パート 2/3】**
```json
{
  "files": [
    {
      "filename": "file2.py",
      "filepath": "./models/file2.py",
      "content": "..."
    }
  ]
}
```

4. **最後のパート**に `dependencies`、`installation_notes`、`test_instructions` を含めてください
5. 各パートは**独立して実行可能な完全なJSON**として提供してください

---

それでは、上記の依頼内容に基づいてコードを生成してください。
必要に応じて複数パートに分割してください。
"""
        
        return prompt

    @staticmethod
    def generate_check_prompt(request: Dict, work_dir: str) -> str:
        """チェック用プロンプトを生成"""
        
        prompt = f"""# 実装完了チェック

## チェック対象
**機能名:** {request.get('function_name', '')}

**依頼内容:** {request.get('details', '')}

**作業ディレクトリ:** {work_dir}

---

## チェック項目
以下の項目を確認し、JSON形式で報告してください：

### 1. 実装状況の確認
- 依頼された機能が実装されているか
- ファイルが正しい場所に配置されているか
- コードにエラーがないか

### 2. 動作確認
- 正常系のテストが通るか
- エラーハンドリングが適切か
- UIが正しく表示されるか

### 3. 問題の検出
- 新たなバグや問題が発見されたか
- 追加で必要な機能はあるか
- 改善すべき点はあるか

---

## 出力形式
以下のJSON形式で回答してください：

```json
{{
  "issue_updates": [
    {{
      "issue_id": "ISS001 または null（新規の場合）",
      "action": "update または create",
      "title": "問題タイトル（新規の場合のみ）",
      "description": "詳細説明（新規の場合のみ）",
      "impact": "低/中/高",
      "new_status": "発見/対応中/解決/再発",
      "notes": "今回の状況説明",
      "resolution": "解決策（解決時のみ）"
    }}
  ],
  "code_requests": [
    {{
      "function_name": "新たに必要な機能名",
      "details": "詳細な依頼内容",
      "related_issues": ["ISS001"],
      "status": "依頼中"
    }}
  ],
  "deployed_files": [
    {{
      "filename": "配置したファイル名",
      "filepath": "配置パス",
      "status": "OK/NG/未確認",
      "notes": "動作確認結果"
    }}
  ],
  "test_results": [
    {{
      "function_name": "テストした機能名",
      "result": "OK/NG",
      "notes": "テスト内容と結果"
    }}
  ],
  "bugs": [
    {{
      "title": "発見されたバグ",
      "description": "詳細",
      "severity": "低/中/高/致命的",
      "status": "未対応"
    }}
  ],
  "ui_ux_notes": [
    {{
      "category": "UI/UX/パフォーマンス",
      "content": "改善メモ"
    }}
  ]
}}
```

**注意:**
- 問題がない場合は空の配列 [] を返してください
- 既存の問題を更新する場合は issue_id を指定してください
- 新規問題の場合は issue_id を null にしてください

---

## ⚠️ 重要: 回答の分割について

**回答が長くなる場合は、以下のルールで分割してください：**

1. **1回の回答は10,000文字以内**に収めてください
2. 複数の更新項目がある場合は、**カテゴリごと**に分けて回答してください
3. 分割する場合は以下の形式で：

**【パート 1/2】**
```json
{
  "deployed_files": [...],
  "test_results": [...]
}
```

**【パート 2/2】**
```json
{
  "bugs": [...],
  "issue_updates": [...],
  "code_requests": [...]
}
```

4. 各パートは**独立して取り込み可能な完全なJSON**として提供してください
5. 空の配列は省略せず、必ず含めてください（例: `"bugs": []`）

---

それでは、上記のチェック項目に基づいて確認結果を報告してください。
必要に応じて複数パートに分割してください。
"""
        
        return prompt
