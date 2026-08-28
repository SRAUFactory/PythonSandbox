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
if user == GU and computer == GU:
    result = "あいこ"
elif user == GU and computer == CHOKI:
    result = "ユーザーの勝ち"
elif user == GU and computer == PA:
    result = "ユーザーの負け"
elif user == CHOKI and computer == GU:
    result = "ユーザーの負け"
elif user == CHOKI and computer == CHOKI:
    result = "あいこ"
elif user == CHOKI and computer == PA:
    result = "ユーザーの勝ち"
elif user == PA and computer == GU:
    result = "ユーザーの勝ち"
elif user == PA and computer == CHOKI:
    result = "ユーザーの負け"
elif user == PA and computer == PA:
    result = "あいこ"

# 勝敗の判定結果を表示する
print(result)
