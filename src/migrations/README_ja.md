# マイグレーション ガイド (日本語訳)

このドキュメントは `app/migrations/README.md` の日本語訳です。マイグレーションの基本的な使い方や命名規則を示します。

## 基本コマンド

```bash
# マイグレーションディレクトリを初期化
uv run sqlspec --config app.config init

# 新しいマイグレーションを作成
uv run sqlspec --config app.config create-migration -m "Add users table"

# マイグレーションを適用
uv run sqlspec --config app.config upgrade
```

## 命名規則

### ファイル名

フォーマット: `{version}_{description}.sql`

- version: UTC の YYYYMMDDHHmmss 形式のタイムスタンプ
- description: 処理内容を表す短い説明（単語はアンダースコア区切り）
- 例: `20251011120000_create_users_table.sql`

### クエリ名

- アップグレード: `migrate-{version}-up`
- ダウングレード: `migrate-{version}-down`

## バージョン形式

マイグレーションは **タイムスタンプ形式** (YYYYMMDDHHmmss) を使用します。

- **形式**: 14 桁の UTC タイムスタンプ
- **例**: `20251011120000` (2025年10月11日 12:00:00 UTC)
- **利点**: 複数開発者が同時にマイグレーションを作成してもマージ競合が発生しにくい

### マイグレーションの作成

タイムスタンプ付きマイグレーションの生成には CLI を使用します。

```bash
uv run sqlspec --config app.config create-migration -m "add user table"
```

生成されるファイルは空のテンプレートです。スキーマ変更の SQL（または Python コード）は手動で追記してください。

## 参考リンク

- [SQLSpec ドキュメント: Database Migrations](../../sqlspec/docs/usage/migrations.rst)
- [SQLSpec ドキュメント: Database Migrations (日本語訳)](../../sqlspec/docs/usage/migrations_ja.rst)
