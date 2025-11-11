# Litestar + SQLSpec Todo API

LitestarとSQLSpecで構築したモダンな非同期Todo API

## 概要

このプロジェクトは、ORMを使わずにRaw SQLを直接記述しながら、型安全性とマイグレーション管理を実現する **SQLSpec** ライブラリのサンプル実装です。

> ⚠️ **注意**: SQLSpecは実験的なライブラリです。本番環境での使用前に十分な検証を行ってください。

## 機能

- ✅ タスクの完全なCRUD操作
- ✅ SQLSpecによる非同期データベース操作（Raw SQL）
- ✅ SQLite 3データベース
- ✅ Pydantic v2によるデータ検証
- ✅ SQLSpecによるマイグレーション管理
- ✅ 自動APIドキュメント生成（OpenAPI/Swagger UI）

## 前提条件

- DockerとDocker Compose
- Python 3.12+
- Poetry（ローカル開発の場合）

## プロジェクト構成

```
litestar-sqlspec-app/
├── app/
│   ├── __init__.py
│   ├── main.py           # Litestarアプリのエントリーポイント
│   ├── db.py             # データベース設定
│   ├── models.py         # Pydanticモデル定義
│   ├── routes.py         # APIルート定義
│   └── migrations/       # SQLマイグレーションファイル
│       └── 20251111125634_init.sql
├── data/                 # SQLiteデータベース保存先
│   └── app.db
├── sqlspec/              # SQLSpecライブラリ（サブモジュール）
├── pyproject.toml        # 依存関係管理
├── docker-compose.yml
└── README.md
```

## クイックスタート

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/litestar-sqlspec-sample.git
cd litestar-sqlspec-sample
```

### 2. 依存関係のインストール

```bash
# Poetryを使用
poetry install

# または、pipを使用
pip install -e .
```

### 3. マイグレーションの実行

> **重要**: SQLSpecではマイグレーションファイルは自動生成されません。`app/migrations/` ディレクトリに手動でSQLファイルを作成する必要があります。

```bash
# コンフィグモジュールを明示的に指定してマイグレーションを実行
poetry run sqlspec --config db.config upgrade

# マイグレーションステータス確認
poetry run sqlspec --config db.config current

# マイグレーションをロールバック
poetry run sqlspec --config db.config downgrade -1
```

### 4. アプリケーションの起動

**Dockerを使用する場合:**

```bash
docker-compose up --build
```

**ローカルで実行する場合:**

```bash
poetry run litestar run --reload
```

APIは `http://localhost:8000` で利用可能です。

## VSCode REST Clientの使用

VSCodeに「REST Client」拡張機能をインストール後、`api.http`ファイルでAPIテストが可能です。

環境の切り替え：
1. VSCodeで`Ctrl+Shift+P`を押下
2. 「Rest Client: Switch Environment」を選択
3. `development`, `production`, `local`から選択

各環境のポート設定：
- development: 8000（デフォルト）
- production: 8080
- local: 9000

## APIドキュメント

- OpenAPIスキーマ: `http://localhost:{{APP_PORT}}/schema`
- Swagger UI: `http://localhost:{{APP_PORT}}/schema/swagger`
- ReDoc: `http://localhost:{{APP_PORT}}/schema/redoc`

## マイグレーション管理

### マイグレーションファイルの作成

SQLSpecでは、マイグレーションファイルは手動で作成する必要があります。

**ファイル命名規則:**
```
{timestamp}_{description}.sql
例: 20251111125634_init.sql
```

**マイグレーションファイルの構造:**

```sql
-- upgrade --
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT 0,
    priority TEXT NOT NULL DEFAULT 'medium',
    due_date TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER IF NOT EXISTS update_tasks_updated_at
AFTER UPDATE ON tasks
FOR EACH ROW
BEGIN
    UPDATE tasks SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- downgrade --
DROP TRIGGER IF EXISTS update_tasks_updated_at;
DROP TABLE IF EXISTS tasks;
```

### マイグレーションコマンド

```bash
# 最新バージョンまでアップグレード
poetry run sqlspec --config db.config upgrade

# 特定のバージョンまでアップグレード
poetry run sqlspec --config db.config upgrade 20251111125634

# 1つ前のバージョンにダウングレード
poetry run sqlspec --config db.config downgrade -1

# 現在のマイグレーションバージョンを確認
poetry run sqlspec --config db.config current

# マイグレーション履歴を表示
poetry run sqlspec --config db.config history
```


## APIエンドポイント

| メソッド | パス | 説明 | クエリパラメータ |
|---------|------|------|----------------|
| GET | `/tasks` | タスク一覧取得 | `completed`, `limit`, `offset` |
| POST | `/tasks` | 新規タスク作成 | - |
| GET | `/tasks/{id}` | 特定タスク取得 | - |
| PUT | `/tasks/{id}` | タスク更新（部分更新） | - |
| DELETE | `/tasks/{id}` | タスク削除 | - |

## サンプルリクエスト

### タスク作成
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "買い物に行く",
    "description": "牛乳と卵を買う",
    "priority": "high",
    "due_date": "2024-12-31T23:59:59"
  }'
```

### タスク一覧取得
```bash
# 全タスク取得
curl http://localhost:8000/tasks

# 完了済みタスクのみ取得
curl http://localhost:8000/tasks?completed=true

# ページネーション（5件ずつ、2ページ目）
curl http://localhost:8000/tasks?limit=5&offset=5
```

### タスク詳細取得
```bash
curl http://localhost:8000/tasks/1
```

### タスク更新（部分更新）
```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "買い物に行く（更新）",
    "completed": true
  }'
```

### タスク削除
```bash
curl -X DELETE http://localhost:8000/tasks/1
```

## SQLSpec使用時の注意点

### パラメータの渡し方

```python
# ✅ execute()の場合: *params で展開
params = [10, 0]
result = await db_session.execute(query, *params)
# schema_typeは結果オブジェクトで指定
tasks = result.get_data(schema_type=Task)

# ✅ select_one()の場合: schema_typeを直接指定可能
task = await db_session.select_one(query, param1, param2, schema_type=Task)
```

### トランザクション管理

```python
# 変更を確定する場合は明示的にコミット
await db_session.commit()

# SELECT のみの場合はcommit不要
```

## 技術スタック

- **Webフレームワーク**: [Litestar](https://litestar.dev/) - FastAPI類似の非同期フレームワーク
- **データベースライブラリ**: [SQLSpec](https://github.com/litestar-org/sqlspec) - Raw SQLベースのデータベースライブラリ（実験的）
- **データベース**: SQLite 3
- **バリデーション**: [Pydantic](https://docs.pydantic.dev/) v2
- **パッケージ管理**: [Poetry](https://python-poetry.org/)

## ライセンス

MIT

## 参考リンク

- [SQLSpec GitHub](https://github.com/litestar-org/sqlspec)
- [Litestar Documentation](https://docs.litestar.dev/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 注意事項

このプロジェクトは、SQLSpecの評価・学習目的のサンプル実装です。SQLSpecは実験的なライブラリであるため、本番環境での使用前に以下の点を確認してください：

- ✅ 十分なテストの実施
- ✅ パフォーマンスの検証
- ✅ セキュリティの確認
- ✅ ライブラリの更新状況の確認
