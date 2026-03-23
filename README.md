# learn-bruno

Bruno の検証用リポジトリ

## セットアップ

```bash
uv sync
```

## 起動

```bash
uv run uvicorn main:app --reload
```

http://localhost:8000/docs で Swagger UI を確認できます。

## API仕様書の出力

```bash
uv run python -c "
import json
from main import app
spec = app.openapi()
print(json.dumps(spec, indent=2, ensure_ascii=False))
" > openapi.json
```

## コレクション構成

```
bruno-collection/
  items/                      ← 単体リクエスト（API クライアント）
  flows/
    アイテムCRUD/              ← フローテスト（Runner / CLI で seq 順に実行）
```

### items/ — API クライアント

各リクエストを単独で実行できます。URL は固定値（`/items/1` 等）を使用しており、`assert` で基本的なレスポンス検証を行います。

### flows/アイテムCRUD/ — フローテスト

リセット→一覧取得→作成→取得→更新→削除を seq 順に実行する一連のテストです。
`script:post-response` や `vars:post-response` で変数を受け渡し（`{{createdId}}`、`itemName`）、リクエスト間の連携をテストします。

#### テストフロー（seq 順）

| seq | リクエスト | テスト機能                                             |
| --- | ---------- | ------------------------------------------------------ |
| 1   | リセット   | `assert`                                               |
| 2   | 一覧取得   | `assert` + `tests`（JS/Chai）                          |
| 3   | 作成       | `assert` + `script:post-response`（`createdId` セット）|
| 4   | 取得       | `script:pre-request` + `assert` + `vars:post-response` |
| 5   | 更新       | `assert` + `tests`（`itemName` との比較）              |
| 6   | 削除       | `assert` + `tests`                                     |

#### GUI で実行

Bruno GUI で `flows/アイテムCRUD` フォルダを Runner（▶ Run）で実行します。

#### CLI で実行

```bash
(cd bruno-collection && npx @usebruno/cli run --env local flows/アイテムCRUD)
```

## Bruno リクエストファイルの作成

`.bru` ファイルはテキストファイルなので、以下の方法で作成できます。

### 1. Bruno GUI から作成（通常の運用）

コレクション内で「+ Add request」からリクエストを追加します。

### 2. AI（Claude Code）で OpenAPI 仕様書から生成

OpenAPI 仕様書（`openapi.json`）をもとに、Claude Code で `.bru` ファイルを直接生成できます。
GUI のインポート機能と違い、Git リポジトリ内に直接作成されるため移動の手間がありません。

```
# Claude Code に依頼する例
「openapi.json をもとに bru ファイルを作成して」
```

### 3. 手動で `.bru` ファイルを作成

`.bru` ファイルの基本構造：

```bru
meta {
  name: リクエスト名
  type: http
  seq: 1
}

get {
  url: {{baseUrl}}/endpoint
  body: none
  auth: none
}
```

POST/PUT でリクエストボディがある場合：

```bru
post {
  url: {{baseUrl}}/endpoint
  body: json
  auth: none
}

body:json {
  {
    "key": "value"
  }
}
```
