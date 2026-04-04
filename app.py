import os
import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "fish_quiz_secret"

# 魚のデータセット（全10種）
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

# 出題数（5問で終わるように設定）
QUESTIONS_TO_SHOW = 5

@app.route("/", methods=["GET", "POST"])
def index():
    # ゲームの初期化（初めてアクセスした時、またはリセット時）
    if "quiz_list" not in session or request.method == "GET" and not request.args.get("continue"):
        # 0〜9のインデックスをシャッフルし、先頭の5つだけを取り出す（これで重複なしの5問が決定）
        all_indices = list(range(len(FISH_DATA)))
        random.shuffle(all_indices)
        session["quiz_list"] = all_indices[:QUESTIONS_TO_SHOW]
        
        session["current_step"] = 0  # 0から4まで進む
        session["score"] = 0
        session["last_result"] = None

    current_step = session.get("current_step", 0)
    
    # 5問終了判定
    if current_step >= QUESTIONS_TO_SHOW:
        return render_template("index.html", finished=True, score=session["score"], total=QUESTIONS_TO_SHOW)

    # 現在の問題の魚データを取得
    fish_index = session["quiz_list"][current_step]
    fish = FISH_DATA[fish_index]
    
    last_result = session.get("last_result")
    session["last_result"] = None

    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip()
        
        # 正誤判定
        if user_answer == fish["name"]:
            session["score"] += 1
            session["last_result"] = {"status": "correct", "msg": f"正解！これは {fish['name']} です。"}
        else:
            session["last_result"] = {"status": "wrong", "msg": f"残念！正解は {fish['name']} でした。"}
        
        # 次の問題へ進む
        session["current_step"] += 1
        # redirect時にリセットされないようクエリパラメータを付ける
        return redirect(url_for("index", continue=True))

    return render_template("index.html", fish=fish, finished=False, last_result=last_result, step=current_step + 1)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)