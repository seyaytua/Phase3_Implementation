"""
実装用プロンプト生成ユーティリティ
"""
from typing import Dict

class ImplementationPromptGenerator:
    """実装依頼用プロンプトを生成するクラス"""
    
    @staticmethod
    def generate_mvp_prompt(project_name: str, phase2_data: Dict, work_dir: str, shell_type: str = 'powershell') -> str:
        """最小構成（MVP）用プロンプトを生成"""
        
        # Phase 2の設計情報を抽出
        phase1_data = phase2_data.get('phase1_data', {})
        design_data = phase2_data.get('design_data', {})
        tech_stack = design_data.get('tech_stack', {})
        
        purpose = phase1_data.get('purpose', '')
        main_features = phase1_data.get('main_features', [])
        constraints = phase1_data.get('constraints', [])
        
        prompt = f"""# 🎯 最小構成（MVP）実装依頼

## プロジェクト概要
**プロジェクト名:** {project_name}

**目的:** {purpose}

**主要機能:** {', '.join(main_features[:3]) if main_features else '未定義'}

---

## 🚀 Phase 3 の段階的実装戦略

### Phase 3 の強み
✅ **ID順に進捗確認** - 各ステップで動作確認できる
✅ **早期問題発見** - 小さく作って確実に動かす
✅ **リスク最小化** - 全体を作ってから動かないリスクを回避

### 実装方針
**「最小構成から徐々に機能追加」**

1️⃣ **まず起動させる（MVP）**
2️⃣ **次に基本機能を追加（ID002）**
3️⃣ **段階的に高度な機能を追加（ID003以降）**

---

## 📋 今回の依頼：最小構成（MVP）

### 目標
**「とりあえず起動して画面が表示される」**

### 実装内容
以下の**最小限のファイル**のみ作成してください：

1. **main.py** - アプリケーション起動
   - ウィンドウを表示
   - タイトルとメニューバー
   - 空の画面でOK
   - データ保存機能は不要

2. **基本画面1つ** - メイン画面またはログイン画面
   - シンプルなUI
   - ボタンは動作しなくてOK
   - 後で機能追加予定

**これだけです！** データベース、複雑な機能、全画面は不要です。

---

## 技術スタック
- **GUIフレームワーク:** {tech_stack.get('gui_framework', 'PySide6 6.10.0')}
- **データ保存:** 今回は不要（後で追加）
- **使用ライブラリ:** 標準ライブラリのみ

**制約条件:**
"""
        
        if constraints:
            for constraint in constraints:
                prompt += f"- {constraint}\n"
        else:
            prompt += "- WinPython標準環境で動作すること\n"
        
        prompt += f"""
---

## 🏗️ ファイル構成（最小）

```
{work_dir}/
├── main.py              # 起動ファイル（今回作成）
└── ui/
    └── main_window.py   # メイン画面（今回作成）
```

**これだけ！** models/, utils/ などは後で追加します。

---

## 💡 重要な設計指針

### 1. main.py の役割
```python
# main.py は「起動するだけ」
# 複雑なロジックは書かない
# 後で変更しないように設計

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
```

### 2. モジュール分離の原則
- **main.py は極力変更しない**
- 新機能は**別ファイル**に作る
- 既存ファイルへの追加は**import文のみ**

### 3. 段階的拡張の設計
- 最初はシンプルに
- 後で機能を追加しやすく
- 拡張ポイントを明確に

---

## 📤 出力形式

以下のJSON形式で回答してください：

```json
{{
  "files": [
    {{
      "filename": "main.py",
      "filepath": "./main.py",
      "description": "アプリケーション起動ファイル",
      "content": "完全なPythonコード"
    }},
    {{
      "filename": "main_window.py",
      "filepath": "./ui/main_window.py",
      "description": "メインウィンドウ（最小構成）",
      "content": "完全なPythonコード"
    }}
  ],
  "dependencies": [
    "必要なインポート文"
  ],
  "installation_notes": "セットアップ手順",
  "test_instructions": "python main.py で起動確認"
}}
```

---

## ⚠️ 注意事項

**今回は最小構成です。以下は実装しないでください：**
- ❌ データベース保存機能
- ❌ 複雑なビジネスロジック
- ❌ 全ての画面
- ❌ 認証機能
- ❌ 詳細なエラーハンドリング

**これらは後のID（ID002, ID003...）で段階的に追加します。**

---

## 🎯 成功条件

✅ `python main.py` で起動する
✅ ウィンドウが表示される
✅ クラッシュしない
✅ シンプルで読みやすいコード

**これだけクリアすればOK！**

---

それでは、上記の最小構成（MVP）を実装してください。
シンプルで確実に動くコードをお願いします。
"""
        
        return prompt
    
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
        
        # 段階的実装の指示を追加
        prompt += """---

## 🏗️ 段階的実装の原則

### Phase 3 は「小さく作って確実に動かす」

**このIDを実装する際の注意点：**

1. **main.py の変更は最小限に**
   - 新機能は別ファイル・別モジュールに作成
   - main.py には import 追加程度に留める
   - 既存の動作を壊さない

2. **モジュール分離**
   - 新機能は ui/, models/, utils/ などに分離
   - 1ファイル1責任の原則
   - 後で拡張しやすい設計

3. **既存ファイルへの追加**
   - 既存ファイルを修正する場合は差分を明確に
   - 「〇〇の後に以下を追加」のように指示
   - 全体を書き直さない

4. **依存関係を意識**
   - 前のID（ID001, ID002...）で作ったファイルを活用
   - 重複した実装を避ける
   - 既存の機能を呼び出す

---

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
    def generate_next_request_prompt(all_requests: list, completed_ids: list, phase2_data: Dict, shell_type: str = 'powershell') -> str:
        """次の未完了依頼のプロンプトを生成"""
        
        # 完了していない最初の依頼を見つける
        next_request = None
        for req in all_requests:
            if req['id'] not in completed_ids and req.get('status') != '完了':
                next_request = req
                break
        
        if not next_request:
            return "✅ 全ての依頼が完了しています！"
        
        # 完了済みの依頼リスト
        completed_requests = [r for r in all_requests if r['id'] in completed_ids or r.get('status') == '完了']
        
        # 通常のプロンプトを生成
        base_prompt = ImplementationPromptGenerator.generate_implementation_prompt(
            next_request, phase2_data, shell_type
        )
        
        # 前提情報を追加
        context = f"""
---

## 📚 これまでの実装状況

**完了済みの依頼: {len(completed_requests)} 件**

"""
        
        if completed_requests:
            context += "**既に実装済みの機能:**\n"
            for req in completed_requests[-3:]:  # 直近3件のみ表示
                context += f"- ID{req['id']:03d}: {req['function_name']}\n"
            context += "\n"
        
        context += f"""**今回の依頼: ID{next_request['id']:03d}**

---

## 🔧 既存ファイルの活用

**以下のファイルは既に作成済みです（前のIDで作成）:**
- main.py
- ui/ 配下のファイル
- models/ 配下のファイル（あれば）
- utils/ 配下のファイル（あれば）

**これらを活用して、今回の機能を追加してください。**

**重要:**
- 既存ファイルを全て書き直さない
- 必要な部分だけ追加・修正
- main.py の変更は最小限に

---

"""
        
        # プロンプトに挿入
        return base_prompt.replace("## 依頼内容", context + "## 依頼内容")

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
