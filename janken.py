# 乱数の機能を提供するモジュールをインポートする
import random

# 手を表す定数を定義する
GU = 0
CHOKI = 1
PA = 2

# 勝敗の判定結果を格納した配列を用意しておく
result = ["あいこ", "ユーザーの負け", "ユーザーの勝ち"]

# ユーザーはキー入力で手を選ぶ
user = int(input("ユーザーの手-->"))

# コンピュータは乱数で手を選ぶ
computer = random.randint(GU, PA)
print(f"コンピュータの手-->{computer}")

# 勝敗を判定する
idx = (user - computer + 3) % 3

# 勝敗の判定結果を表示する
print(result[idx])
