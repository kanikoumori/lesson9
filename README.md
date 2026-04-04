# 魚の名前当てクイズ (漢字でGO風)

## 準備手順
1. `static/images/` フォルダを作成し、手元の画像を `1.jpg` 〜 `10.jpg` という名前で保存してください。
2. GitHubにこのプロジェクトをプッシュします。
3. Render (render.com) で "Web Service" を新規作成します。

## Renderの設定
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

## 遊び方
- 表示される魚の写真を見て、名前を全角カタカナで入力してください。
- 全10問終了後にスコアが表示されます。