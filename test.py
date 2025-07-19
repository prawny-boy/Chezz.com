import json

user = 'test'

with open("user_info.json", "r") as f:
    d = json.load(f)
    print(d[user]['board_colors']['light'])