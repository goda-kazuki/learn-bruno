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
