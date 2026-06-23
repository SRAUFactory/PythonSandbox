# MongoDB PyMongo サンプルプロジェクト

このディレクトリは、PyMongoを使用してMongoDBの基本的なCRUD操作を行うためのサンプルプロジェクトです。

## 前提条件

1. **MongoDBのインストールと起動**
   まだインストールが完了していない場合は、以下のコマンドでインストールと起動を行ってください。

   ```bash
   # MongoDBのインストール (未インストールの前提)
   brew install mongodb-community

   # MongoDBサービスの起動
   brew services start mongodb-community
   ```

2. **Python 3.x** がインストールされていること。

## セットアップ手順

このディレクトリ内で動作させるために、Python仮想環境を作成してPyMongoをインストールします。

### 1. 仮想環境の作成と有効化

> [!NOTE]
> 既にプロジェクト全体などで仮想環境（`venv`）を作成し、アクティベート済みの場合は、この「1.」の手順はスキップして「2. 依存ライブラリのインストール」に進んでください。

```bash
# mongodb_sample ディレクトリに移動します
cd mongodb_sample

# 仮想環境を構築します
python3 -m venv venv

# 仮想環境をアクティベートします
source venv/bin/activate
```

### 2. 依存ライブラリのインストール

```bash
pip install -r requirements.txt
```

## サンプルスクリプトの実行

MongoDBが起動している状態で、以下のスクリプトを実行します。

```bash
python sample.py
```

### 実行結果のイメージ

正常に動作すると、以下のようにコンソールに出力されます。

```text
MongoDB (PyMongo) サンプルスクリプトを開始します...
MongoDBへの接続に成功しました！

--- 準備: 既存のデータを削除しました ---

--- 1. CREATE (挿入) ---
1件のドキュメントを挿入しました。ID: ...
2件のドキュメントを挿入しました。IDs: [...]

--- 2. READ (検索) ---
Aliceのデータ: {'_id': ..., 'name': 'Alice', 'age': 25, 'email': 'alice@example.com', 'skills': ['Python', 'SQL']}
Pythonスキルを持つユーザー一覧:
 - Alice (年齢: 25, スキル: ['Python', 'SQL'])
 - Charlie (年齢: 35, スキル: ['Python', 'Go', 'Docker'])

--- 3. UPDATE (更新) ---
更新されたドキュメント数: 1
更新後のAliceのデータ: {'_id': ..., 'name': 'Alice', 'age': 26, 'email': 'alice@example.com', 'skills': ['Python', 'SQL', 'MongoDB']}

--- 4. DELETE (削除) ---
削除されたドキュメント数: 1

--- 最終データ一覧 ---
{'_id': ..., 'name': 'Alice', 'age': 26, 'email': 'alice@example.com', 'skills': ['Python', 'SQL', 'MongoDB']}
{'_id': ..., 'name': 'Charlie', 'age': 35, 'email': 'charlie@example.com', 'skills': ['Python', 'Go', 'Docker']}

接続を閉じました。サンプルスクリプトを終了します。
```
