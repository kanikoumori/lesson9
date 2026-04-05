import os
import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
# 秘密鍵を固定値に設定（Renderでのエラー回避用）
app.secret_key = "fish_quiz_fixed_key_12345"

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
    # ゲームの初期化
    if "quiz_list" not in session or (request.method == "GET" and not request.args.get("continue")):
        all_indices = list(range(len(FISH_DATA)))
        random.shuffle(all_indices)
        session["quiz_list"] = all_indices[:5]
        session["current_step"] = 0
        session["score"] = 0
        session["last_result"] = None

    current_step = session.get("current_step", 0)
    
    # 5問終了判定
    if current_step >= 5:
        score = session.get("score", 0)
        # 終了時にリストを消してリセット可能にする
        session.pop("quiz_list", None)
        return render_template("index.html", finished=True, score=score, total=5)

    fish_index = session["quiz_list"][current_step]
    fish = FISH_DATA[fish_index]
    
    # 表示用の判定結果を取得し、セッションからは消す（一回切り表示）
    last_result = session.get("last_result")
    session["last_result"] = None

    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip()
        
        if user_answer == fish["name"]:
            session["score"] = session.get("score", 0) + 1
            session["last_result"] = {"status": "correct", "msg": f"正解！これは {fish['name']} です。"}
        else:
            session["last_result"] = {"status": "wrong", "msg": f"残念！正解は {fish['name']} でした。"}
        
        session["current_step"] = current_step + 1
        return redirect(url_for("index", continue="true"))

    return render_template("index.html", 
                           fish=fish, 
                           finished=False, 
                           last_result=last_result, 
                           step=current_step + 1)

if __name__ == "__main__":
    # Renderのポート指定に対応
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)