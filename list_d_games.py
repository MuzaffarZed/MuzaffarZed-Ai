import os

d_games = r"D:\KANPIYUTER O'YINLARI"
if os.path.exists(d_games):
    for item in os.listdir(d_games):
        print(item)
else:
    print("D:\\KANPIYUTER O'YINLARI not found")
