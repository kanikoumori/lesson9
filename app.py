import os
import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "fish_quiz_mega_key_888"

# 魚のデータセット（choicesがあるものは3択、ないものは入力形式）
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

def to_katakana(text):
    return "".join([chr(ord(c) + 96) if "ぁ" <= c <= "ん" else c for c in text])

@app.route("/", methods=["GET", "POST"])
def index():
    if "quiz_list" not in session:
        return render_template("index.html", select_level=True)

    current_step = session.get("current_step", 0)
    total_questions = session.get("total_questions", 5)
    
    if current_step >= total_questions:
        score = session.get("score", 0)
        session.pop("quiz_list", None)
        return render_template("index.html", finished=True, score=score, total=total_questions)

    fish = FISH_DATA[session["quiz_list"][current_step]]
    
    # 3択が必要な場合、選択肢をシャッフルして保持（リロードで変わらないようsessionに保存）
    if "choices" in fish and "current_choices" not in session:
        shuffled = list(fish["choices"])
        random.shuffle(shuffled)
        session["current_choices"] = shuffled

    last_result = session.get("last_result")
    session["last_result"] = None

    if request.method == "POST":
        user_input = request.form.get("answer", "").strip()
        session.pop("current_choices", None) # 回答したら選択肢をクリア
        
        if to_katakana(user_input) == fish["name"]:
            session["score"] += 1
            session["last_result"] = {"status": "correct", "msg": f"正解！これは {fish['name']} です。"}
        else:
            session["last_result"] = {"status": "wrong", "msg": f"残念！正解は {fish['name']} でした。"}
        
        session["current_step"] += 1
        return redirect(url_for("index", next="step"))

    return render_template("index.html", fish=fish, finished=False, last_result=last_result, 
                           step=current_step + 1, total=total_questions,
                           choices=session.get("current_choices"))

@app.route("/start/<level>")
def start_game(level):
    level_map = {"easy": 3, "normal": 5, "hard": 10}
    num = level_map.get(level, 5)
    
    # --- 出題順の制御 ---
    # 3択用のID
    choice_ids = [1, 7, 15, 22, 25, 26]
    # それ以外のID
    other_ids = [f["id"] for f in FISH_DATA if f["id"] not in choice_ids]
    
    random.shuffle(choice_ids)
    random.shuffle(other_ids)
    
    # 各レベルの指定数に応じて3択問題を先頭に混ぜる
    if level == "easy": # 1-2問目
        q_list = choice_ids[:2] + other_ids[:1]
    elif level == "normal": # 1-3問目
        q_list = choice_ids[:3] + other_ids[:2]
    else: # hard: 1-3問目
        q_list = choice_ids[:3] + other_ids[:7]
    
    # IDをFISH_DATAのインデックスに変換
    session["quiz_list"] = [next(i for i, f in enumerate(FISH_DATA) if f["id"] == qid) for qid in q_list]
    session["total_questions"] = num
    session["current_step"] = 0
    session["score"] = 0
    session.pop("current_choices", None)
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)