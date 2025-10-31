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

## 📋 追加情報の提供方法

**以下の情報があれば、チェック時に一緒に提供してください：**

1. **ターミナル出力:** コマンド実行結果やエラーメッセージ
2. **エラースクリーンショット:** エラー画面や問題箇所の画像
3. **作成したファイル:** 確認が必要なコードファイルの内容
4. **実行ログ:** アプリケーションの実行ログやデバッグ情報

これらの情報により、より正確な確認が可能になります。

---

## ✅ チェック項目（簡潔に）

### 1. 実装確認
- ファイルが作成されたか
- コードに明らかなエラーがないか

### 2. 動作確認
- 基本動作が正常か
- エラーハンドリングは適切か

### 3. 問題検出
- 新たなバグや問題はないか
- 追加で必要な機能はあるか

---

## 📤 出力形式（最小限）

**重要: 変更があった項目のみ記載してください。変更がない項目は省略可能です。**

```json
{{
  "deployed_files": [
    {{
      "filename": "user_model.py",
      "filepath": "./models/user_model.py",
      "status": "OK",
      "notes": "正常動作確認"
    }}
  ],
  "test_results": [
    {{
      "function_name": "ユーザー登録機能",
      "result": "OK",
      "notes": "正常系・異常系ともにOK"
    }}
  ],
  "bugs": [],
  "issue_updates": [],
  "code_requests": []
}}
```

**フィールドの説明:**
- `deployed_files`: 配置したファイルの状態（OK/NG/未確認）
- `test_results`: テスト結果（OK/NG）
- `bugs`: 発見されたバグ（なければ空配列）
- `issue_updates`: 問題の更新（なければ空配列）
- `code_requests`: 新しい依頼（なければ空配列）

---

## 💡 詳細フォーマット（必要時のみ）

**新しい依頼が必要な場合:**
```json
{{
  "code_requests": [
    {{
      "function_name": "パスワードリセット機能",
      "details": "詳細な依頼内容",
      "status": "依頼中"
    }}
  ]
}}
```

**バグが見つかった場合:**
```json
{{
  "bugs": [
    {{
      "title": "バグのタイトル",
      "description": "詳細",
      "severity": "低/中/高/致命的",
      "status": "未対応"
    }}
  ]
}}
```

**問題がある場合:**
```json
{{
  "issue_updates": [
    {{
      "issue_id": null,
      "action": "create",
      "title": "問題タイトル",
      "description": "詳細",
      "impact": "低/中/高",
      "new_status": "発見",
      "notes": "状況説明"
    }}
  ]
}}
```

---

## ⚠️ 分割ルール

**回答が10,000文字を超える場合のみ分割してください：**

**【パート 1/2】**
```json
{{
  "deployed_files": [...],
  "test_results": [...]
}}
```

**【パート 2/2】**
```json
{{
  "bugs": [...],
  "code_requests": [...]
}}
```

---

それでは、上記の項目に基づいて**簡潔に**確認結果を報告してください。
**変更があった項目のみ記載**し、冗長な情報は省略してください。
"""
        
        return prompt
