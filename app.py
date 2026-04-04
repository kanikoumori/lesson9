import os
import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
# セッションを維持するための秘密鍵（適当な文字列でOK）
app.secret_key = os.environ.get("SECRET_KEY", "fish_quiz_12345")

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
    # ゲームの初期化：セッションにクイズリストがない場合のみ作成
    if "quiz_list" not in session:
        all_indices = list(range(len(FISH_DATA)))
        random.shuffle(all_indices)
        session["quiz_list"] = all_indices[:5]  # ランダムに5問選ぶ
        session["current_step"] = 0
        session["score"] = 0

    current_step = session.get("current_step", 0)
    
    # 5問終了判定
    if current_step >= 5:
        score = session.get("score", 0)
        # 終了時はセッションをクリアして、次回のアクセスでリセットされるようにする
        session.pop("quiz_list", None)
        return render_template("index.html", finished=True, score=score, total=5)

    # 現在の問題を取得
    fish_index = session["quiz_list"][current_step]
    fish = FISH_DATA[fish_index]
    
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
        return redirect(url_for("index"))

    return render_template("index.html", 
                           fish=fish, 
                           finished=False, 
                           last_result=last_result, 
                           step=current_step + 1)

# リセット用ボタンなどを作りたい場合
@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Render環境ではPORT環境変数が必要
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)