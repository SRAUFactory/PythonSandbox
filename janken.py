# 乱数の機能を提供するモジュールをインポートする
import random

# 手を表す定数を定義する
GU = 0
CHOKI = 1
PA = 2

# ユーザーはキー入力で手を選ぶ
user = int(input("ユーザーの手-->"))

# コンピュータは乱数で手を選ぶ
computer = random.randint(GU, PA)
print(f"コンピュータの手-->{computer}")

# 勝敗を判定する
if user == computer:
    result = "あいこ"
elif user == GU and computer == CHOKI or \
     user == CHOKI and computer == PA or \
     user == PA and computer == GU:
    result = "ユーザーの勝ち"
else:
    result = "ユーザーの負け"

# 勝敗の判定結果を表示する
print(result)
