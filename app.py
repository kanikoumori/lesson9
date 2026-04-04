import os
import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "fish_quiz_secret"

# 魚のデータセット
FISH_DATA = [
    {"id": 1, "name": "トラフグ"},
    {"id": 2, "name": "ウスバハギ"},
    {"id": 3, "name": "ウマヅラハギ"},
    {"id": 4, "name": "マルソウダ"},
    {"id": 5, "name": "ショウサイフグ"},
    {"id": 6, "name": "キタマクラ"},
    {"id": 7, "name": "イワナ"},
    {"id": 8, "name": "ヤマメ"},
    {"id": 9, "name": "メイチダイ"},
    {"id": 10, "name": "トラギス"},
]

@app.route("/", methods=["GET", "POST"])
def index():
    if "quiz_list" not in session or request.method == "GET":
        # クイズをシャッフルして初期化
        indices = list(range(len(FISH_DATA)))
        random.shuffle(indices)
        session["quiz_list"] = indices
        session["current_index"] = 0
        session["score"] = 0
        session["last_result"] = None

    current_idx = session["current_index"]
    
    # 全問終了時
    if current_idx >= len(FISH_DATA):
        return render_template("index.html", finished=True, score=session["score"], total=len(FISH_DATA))

    fish = FISH_DATA[session["quiz_list"][current_idx]]
    last_result = session.get("last_result")
    session["last_result"] = None

    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip()
        if user_answer == fish["name"]:
            session["score"] += 1
            session["last_result"] = {"status": "correct", "msg": f"正解！これは {fish['name']} です。"}
        else:
            session["last_result"] = {"status": "wrong", "msg": f"残念！正解は {fish['name']} でした。"}
        
        session["current_index"] += 1
        return redirect(url_for("index"))

    return render_template("index.html", fish=fish, finished=False, last_result=last_result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)