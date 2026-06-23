import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# MongoDB接続設定
# デフォルトのローカルホスト接続。ポートは27017
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "sandbox_db"
COLLECTION_NAME = "users"

def main():
    print("MongoDB (PyMongo) サンプルスクリプトを開始します...")

    # 1. MongoDBクライアントの作成
    try:
        # serverSelectionTimeoutMS=2000 で接続タイムアウトを2秒に設定
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        
        # 接続確認（実際にコマンドを送信して接続できるかテストする）
        client.admin.command('ping')
        print("MongoDBへの接続に成功しました！")
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"MongoDBへの接続に失敗しました: {e}", file=sys.stderr)
        print("MongoDBが起動しているか確認してください。", file=sys.stderr)
        print("起動コマンド: brew services start mongodb-community", file=sys.stderr)
        sys.exit(1)

    # データベースとコレクションの取得（存在しない場合は自動的に作成されます）
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # データ操作の前に既存のデータをクリーンアップ（サンプル動作確認用）
    collection.delete_many({})
    print("\n--- 準備: 既存のデータを削除しました ---")

    # 2. CREATE (データの挿入)
    print("\n--- 1. CREATE (挿入) ---")
    user_alice = {
        "name": "Alice",
        "age": 25,
        "email": "alice@example.com",
        "skills": ["Python", "SQL"]
    }
    insert_result = collection.insert_one(user_alice)
    print(f"1件のドキュメントを挿入しました。ID: {insert_result.inserted_id}")

    users_list = [
        {"name": "Bob", "age": 30, "email": "bob@example.com", "skills": ["Java", "Spring"]},
        {"name": "Charlie", "age": 35, "email": "charlie@example.com", "skills": ["Python", "Go", "Docker"]}
    ]
    insert_many_result = collection.insert_many(users_list)
    print(f"{len(insert_many_result.inserted_ids)}件のドキュメントを挿入しました。IDs: {insert_many_result.inserted_ids}")

    # 3. READ (データの検索)
    print("\n--- 2. READ (検索) ---")
    # 単一ドキュメントの検索
    alice_doc = collection.find_one({"name": "Alice"})
    print(f"Aliceのデータ: {alice_doc}")

    # 複数ドキュメントの検索 (条件: Pythonスキルを持つユーザー)
    print("Pythonスキルを持つユーザー一覧:")
    python_users = collection.find({"skills": "Python"})
    for user in python_users:
        print(f" - {user['name']} (年齢: {user['age']}, スキル: {user['skills']})")

    # 4. UPDATE (データの更新)
    print("\n--- 3. UPDATE (更新) ---")
    # Aliceの年齢を26に更新し、新しいスキルを追加
    update_result = collection.update_one(
        {"name": "Alice"},
        {
            "$set": {"age": 26},
            "$push": {"skills": "MongoDB"}
        }
    )
    print(f"更新されたドキュメント数: {update_result.modified_count}")
    
    # 更新後の確認
    updated_alice = collection.find_one({"name": "Alice"})
    print(f"更新後のAliceのデータ: {updated_alice}")

    # 5. DELETE (データの削除)
    print("\n--- 4. DELETE (削除) ---")
    # Bobのデータを削除
    delete_result = collection.delete_one({"name": "Bob"})
    print(f"削除されたドキュメント数: {delete_result.deleted_count}")

    # 最終的な全データ確認
    print("\n--- 最終データ一覧 ---")
    all_users = collection.find()
    for user in all_users:
        print(user)

    # クライアントを閉じる
    client.close()
    print("\n接続を閉じました。サンプルスクリプトを終了します。")

if __name__ == "__main__":
    main()
