# Phase 3アプリ設計書 v2.0 - 実装管理ツール（改訂版）

## 変更履歴
- v2.0 (2025-10-29): 問題管理を履歴追跡型に全面改修、JSON一括インポート機能追加

---

## 1. プロジェクト概要

**プロジェクト名:** Phase 3 - 実装管理ツール v2.0

**目的:**
Phase 2で確定した設計・仕様に基づくコード実装の進捗を管理するツール。Claude との対話を通じて構造化されたデータを取得し、コード依頼、配置記録、テスト、バグ、問題を一元管理する。特に問題管理は履歴追跡型とし、再発や根本原因の未解決を検知できる仕組みを実装する。

**主要機能:**
- 機能1: Phase 2からのプロジェクト読込
- 機能2: プロンプト自動生成（全履歴含む）
- 機能3: JSON一括インポート
- 機能4: コード依頼管理
- 機能5: コード配置記録
- 機能6: テスト管理
- 機能7: バグ管理
- 機能8: 問題追跡（履歴型）
- 機能9: Phase 4への移行

---

## 2. 主要な改善点

### 問題管理の履歴追跡
- 各問題に一意のID（ISS001, ISS002...）を自動採番
- 全ての状態変化を履歴として記録
- 再発カウント機能
- タイムライン表示

### Claude との連携強化
- プロンプト自動生成機能
- 全問題履歴を含むプロンプト
- JSON一括インポート機能
- 構造化データによる確実な取り込み

### データ整合性
- JSON検証機能
- プレビュー機能
- インポート履歴の記録

---

## 3. ワークフロー

1. Phase 2からプロジェクトをインポート
2. 「プロンプト生成」で全履歴を含むプロンプトを作成
3. Claude に貼り付けて相談
4. Claude から構造化JSONで回答を受け取る
5. 「JSON取り込み」で一括インポート
6. 各タブで詳細確認・編集
7. 問題が解決したらPhase 4へエクスポート

---

## 4. データモデル

### Issue（問題）
```python
{
  "issue_id": "ISS001",
  "title": "問題タイトル",
  "description": "詳細説明",
  "impact": "低/中/高",
  "created_at": "2025-10-29T10:00:00",
  "history": [
    {
      "timestamp": "2025-10-29T10:00:00",
      "status": "発見/対応中/解決/再発",
      "notes": "状況説明",
      "resolution": "解決策",
      "user": "manual/json_import"
    }
  ],
  "current_status": "解決",
  "recurrence_count": 0,
  "last_updated": "2025-10-29T12:00:00",
  "related_requests": ["REQ001"]
}
5. 技術スタック
言語: Python 3.x (WinPython環境)
GUI: PySide6 6.10.0
データ保存: JSON形式（BOMなしUTF-8）
使用ライブラリ: json, datetime, hashlib, shutil, pathlib
6. ファイル構成
/Phase3_Implementation/
├── main.py
├── ui/
│   ├── main_window.py (v2.0)
│   ├── request_tab.py
│   ├── deploy_tab.py
│   ├── test_tab.py
│   ├── issue_tab.py (v2.0)
│   ├── import_dialog.py (新規)
│   └── dialogs.py
├── models/
│   ├── implementation_project.py (v2.0)
│   ├── implementation_manager.py
│   └── issue.py (新規)
├── utils/
│   ├── file_handler.py
│   ├── validators.py
│   ├── importer.py
│   ├── exporter.py
│   ├── prompt_generator.py (新規)
│   └── json_bulk_importer.py (新規)
└── data/
    ├── phase3_implementations.json
    ├── imports/
    └── exports/
作成日: 2025-10-29 作成者: Claude & User バージョン: 2.0