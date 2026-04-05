import os
import random
import unicodedata
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "fish_quiz_pro_key_777"

FISH_DATA = [
    {"id": 1, "name": "トラフグ"}, {"id": 2, "name": "ウスバハギ"},
    {"id": 3, "name": "ウマヅラハギ"}, {"id": 4, "name": "マルソウダ"},
    {"id": 5, "name": "ショウサイフグ"}, {"id": 6, "name": "キタマクラ"},
    {"id": 7, "name": "イワナ"}, {"id": 8, "name": "ヤマメ"},
    {"id": 9, "name": "メイチダイ"}, {"id": 10, "name": "トラギス"},
    {"id": 11, "name": "オキトラギス"}, {"id": 12, "name": "クラカケトラギス"},
    {"id": 13, "name": "コウライトラギス"}, {"id": 14, "name": "オシャレコショウダイ"},
    {"id": 15, "name": "イシダイ"}, {"id": 16, "name": "イシガキダイ"},
    {"id": 17, "name": "キジハタ"}, {"id": 18, "name": "コモンフグ"},
    {"id": 19, "name": "ニュウドウカジカ"}, {"id": 20, "name": "ヒゲダイ"},
    {"id": 21, "name": "ダントウボウ"},{"id": 22, "name": "マハタ"},
    {"id": 23, "name": "カサゴ"}, {"id": 24, "name": "イサキ"},
    {"id": 25, "name": "カワハギ"}, {"id": 26, "name": "マダイ"},
    {"id": 27, "name": "チダイ"}, {"id": 28, "name": "メジナ"},
    {"id": 29, "name": "クロメジナ"},
]

# ひらがなをカタカナに変換する関数
def to_katakana(text):
    # unicodeの「ひらがな」の範囲を「カタカナ」にずらす処理
    return "".join([chr(ord(c) + 96) if "ぁ" <= c <= "ん" else c for c in text])

@app.route("/", methods=["GET", "POST"])
def index():
    # 難易度選択画面（セッションにクイズリストがない場合）
    if "quiz_list" not in session:
        return render_template("index.html", select_level=True)

    current_step = session.get("current_step", 0)
    total_questions = session.get("total_questions", 5)
    
    # 終了判定
    if current_step >= total_questions:
        score = session.get("score", 0)
        session.pop("quiz_list", None)
        return render_template("index.html", finished=True, score=score, total=total_questions)

    fish = FISH_DATA[session["quiz_list"][current_step]]
    last_result = session.get("last_result")
    session["last_result"] = None

    if request.method == "POST":
        user_input = request.form.get("answer", "").strip()
        # 入力をカタカナに変換してから判定
        user_answer_katakana = to_katakana(user_input)
        
        if user_answer_katakana == fish["name"]:
            session["score"] += 1
            session["last_result"] = {"status": "correct", "msg": f"正解！これは {fish['name']} です。"}
        else:
            session["last_result"] = {"status": "wrong", "msg": f"残念！正解は {fish['name']} でした。"}
        
        session["current_step"] += 1
        return redirect(url_for("index", next="step"))

    return render_template("index.html", fish=fish, finished=False, last_result=last_result, step=current_step + 1, total=total_questions)

@app.route("/start/<level>")
def start_game(level):
    # 難易度に応じた問題数を設定
    level_map = {"easy": 3, "normal": 5, "hard": 10}
    num = level_map.get(level, 5)
    
    all_indices = list(range(len(FISH_DATA)))
    random.shuffle(all_indices)
    
    session["quiz_list"] = all_indices[:num]
    session["total_questions"] = num
    session["current_step"] = 0
    session["score"] = 0
    session["last_result"] = None
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)