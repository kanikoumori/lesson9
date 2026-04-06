import os
import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "fish_quiz_final_stable_key_101"

# 魚のデータセット
FISH_DATA = [
    {"id": 1, "name": "トラフグ", "choices": ["トラフグ", "マンボウ", "バンドウイルカ"]},
    {"id": 2, "name": "ウスバハギ"}, {"id": 3, "name": "ウマヅラハギ"},
    {"id": 4, "name": "マルソウダ"}, {"id": 5, "name": "ショウサイフグ"},
    {"id": 6, "name": "キタマクラ"},
    {"id": 7, "name": "イワナ", "choices": ["イワナ", "マハゼ", "シマウシノシタ"]},
    {"id": 8, "name": "ヤマメ"}, {"id": 9, "name": "メイチダイ"},
    {"id": 10, "name": "トラギス"}, {"id": 11, "name": "オキトラギス"},
    {"id": 12, "name": "クラカケトラギス"}, {"id": 13, "name": "コウライトラギス"},
    {"id": 14, "name": "オシャレコショウダイ"},
    {"id": 15, "name": "イシダイ", "choices": ["イシダイ", "マダイ", "スズキ"]},
    {"id": 16, "name": "イシガキダイ"}, {"id": 17, "name": "キジハタ"},
    {"id": 18, "name": "コモンフグ"}, {"id": 19, "name": "ニュウドウカジカ"},
    {"id": 20, "name": "ヒゲダイ"}, {"id": 21, "name": "ダントウボウ"},
    {"id": 22, "name": "マハタ", "choices": ["マハタ", "ホオジロザメ", "マアジ"]},
    {"id": 23, "name": "カサゴ"}, {"id": 24, "name": "イサキ"},
    {"id": 25, "name": "カワハギ", "choices": ["カワハギ", "アカマンボウ", "シイラ"]},
    {"id": 26, "name": "マダイ", "choices": ["マダイ", "ヒラメ", "スズキ"]},
    {"id": 27, "name": "チダイ"}, {"id": 28, "name": "メジナ"},
    {"id": 29, "name": "クロメジナ"},
]

# ひらがなをカタカナに変換する関数
def to_katakana(text):
    if not text:
        return ""
    return "".join([chr(ord(c) + 96) if "ぁ" <= c <= "ん" else c for c in text])

@app.route("/", methods=["GET", "POST"])
def index():
    # 難易度選択チェック
    if "quiz_list" not in session:
        return render_template("index.html", select_level=True)

    current_step = session.get("current_step", 0)
    total_questions = session.get("total_questions", 5)
    
    # 全問終了判定
    if current_step >= total_questions:
        score = session.get("score", 0)
        return render_template("index.html", finished=True, score=score, total=total_questions)

    # 現在の問題データを取得
    fish_index = session["quiz_list"][current_step]
    fish = FISH_DATA[fish_index]
    
    # 3択の準備
    if "choices" in fish and "current_choices" not in session:
        shuffled = list(fish["choices"])
        random.shuffle(shuffled)
        session["current_choices"] = shuffled

    last_result = session.get("last_result")

    if request.method == "POST":
        action = request.form.get("action")
        
        # 「次の問題へ」ボタンが押された場合
        if action == "next":
            session["current_step"] = current_step + 1
            session.pop("last_result", None)
            session.pop("current_choices", None)
            return redirect(url_for("index"))
        
        # 回答が送信された場合
        user_input = request.form.get("answer", "").strip()
        if to_katakana(user_input) == fish["name"]:
            session["score"] = session.get("score", 0) + 1
            session["last_result"] = {"status": "correct", "msg": f"正解！これは {fish['name']} です。"}
        else:
            session["last_result"] = {"status": "wrong", "msg": f"残念！正解は {fish['name']} でした。"}
        
        return redirect(url_for("index"))

    return render_template("index.html", 
                           fish=fish, 
                           finished=False, 
                           last_result=last_result, 
                           step=current_step + 1, 
                           total=total_questions,
                           choices=session.get("current_choices"))

@app.route("/start/<level>")
def start_game(level):
    level_map = {"easy": 3, "normal": 5, "hard": 10}
    num = level_map.get(level, 5)
    
    choice_ids = [1, 7, 15, 22, 25, 26]
    other_ids = [f["id"] for f in FISH_DATA if f["id"] not in choice_ids]
    
    random.shuffle(choice_ids)
    random.shuffle(other_ids)
    
    if level == "easy":
        q_list = choice_ids[:2] + other_ids[:1]
    elif level == "normal":
        q_list = choice_ids[:3] + other_ids[:2]
    else:
        q_list = choice_ids[:3] + other_ids[:7]
    
    session["quiz_list"] = [i for i, f in enumerate(FISH_DATA) if f["id"] in q_list]
    # 出題順をシャッフル（3択が最初に来すぎないようにする場合）
    random.shuffle(session["quiz_list"])
    
    session["total_questions"] = num
    session["current_step"] = 0
    session["score"] = 0
    session.pop("current_choices", None)
    session.pop("last_result", None)
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)