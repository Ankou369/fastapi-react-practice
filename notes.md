# アプリ開発セットアップメモ（Python Web）

## フォルダ構成の例
```text
プロジェクト名/
├── backend/
│   ├── .venv/              ← プロジェクト専用の仮想環境
│   ├── main.py             ← FastAPIの場合。Flaskなら app.py
│   └── requirements.txt    ← 使ったライブラリの一覧
├── frontend/               ← Reactの場合に使う
├── notes.md
└── .gitignore
```

## 1. 新規プロジェクトの最初だけやること
```powershell
mkdir プロジェクト名
cd プロジェクト名
mkdir backend
New-Item notes.md -ItemType File
New-Item .gitignore -ItemType File

cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install fastapi "uvicorn[standard]"   # Flaskなら flask など
pip freeze > requirements.txt
New-Item main.py -ItemType File
```

`.gitignore` の中身（GitHubに上げる前に必ず書く）：
```text
.venv/
__pycache__/
*.db
node_modules/
.env
```

ポイント：
- `.venv` はプロジェクトごとに作る。他のアプリと混ぜない
- `requirements.txt` は「使ったライブラリのメモ」。これがあると再現できる
- プロンプトの頭に `(.venv)` が出ていれば仮想環境に入れている

## 2. 開発する日は毎回やること
これだけ。新規の手順は繰り返さない。
```powershell
cd backend
.venv\Scripts\Activate.ps1
uvicorn main:app --reload        # FastAPIの場合
# Flaskの場合: flask --app app --debug run
```
終わるときは `Ctrl + C` でサーバー停止、`deactivate` で仮想環境を抜ける。

## 3. ライブラリを追加したときだけ
```powershell
pip install ライブラリ名
pip freeze > requirements.txt
```
この2行目を忘れると、別のPCで動かしたときにエラーになる。

## 4. 別のPCで始めるとき／GitHubからクローンしたとき
`.venv` はGitHubに上がっていないので作り直す。ただし中身は一発で復元できる。
```powershell
git clone リポジトリのURL
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 5. よくあるトラブル
- **ModuleNotFoundError: No module named '〇〇'**
  → だいたい「(.venv)に入っていない」か「requirements.txt からインストールしていない」
  → まず `(.venv)` 表示を確認。次に `python -m pip install -r requirements.txt`
- **New-Item で「既に存在します」**
  → 既にあるだけ。ファイルかフォルダかはこれで確認できる
  → `Get-Item -Force 名前 | Select-Object Name, PSIsContainer`
  → True = フォルダ、False = ファイル
- **ポートが使用中と言われる**
  → 前のサーバーが動きっぱなし。別ウィンドウのサーバーを `Ctrl + C` で止める

## 6. React側も考え方は同じ
| Python | React |
|---|---|
| `.venv/` | `node_modules/` |
| `requirements.txt` | `package.json` |
| `pip install` | `npm install` |
| `uvicorn main:app --reload` | `npm run dev` |

どちらも `.venv/` と `node_modules/` はGitHubに上げない。

データベース接続やテーブル作成、スキーマ（受け取るデータの形）を main.py から別ファイルへ移したことで、main.py にはエンドポイントだけが残り、読みやすくなった。