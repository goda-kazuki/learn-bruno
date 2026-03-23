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
