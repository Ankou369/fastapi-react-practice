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

# フロントエンド初期設定メモ（React + Vite）

## 0. 前提（PCに1回だけ）
- Node.js（LTS）を入れる。入れ方は公式インストーラー、または：
  ```powershell
  winget install -e --id OpenJS.NodeJS.LTS
  ```
- 入れたら PowerShell を開き直して（PATH反映のため）確認：
  ```powershell
  node -v
  npm -v
  ```
  両方バージョンが出ればOK。`.venv` は関係ない（Python側の話）。

## 1. 新規プロジェクトの最初だけやること
**必ずプロジェクトのルート**（backend と並ぶ場所）で実行する：
```powershell
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm run dev
```
- `frontend` フォルダはこのコマンドが作る。先に手で作らない
- 途中の選択肢（linterなど）はデフォルトでOK。アプリの動きには影響しない
- 表示された Local の URL（通常 http://localhost:5173/）を開いて初期画面を確認
- 作った直後に確認：`ls frontend` で `package.json` が見えること、`git status` で `frontend/` が Untracked に出ること

## 2. 開発する日は毎回やること
```powershell
cd frontend
npm run dev
```
- 終わるときは `Ctrl + C`
- サーバー起動中のターミナルでは他のコマンドを打てない。git操作やバックエンド起動は別ターミナルで

## 3. ライブラリを追加したときだけ
```powershell
npm install ライブラリ名
```
- Python と違い、`package.json` への記録は自動。`pip freeze` のような手順はない
- 削除は `npm uninstall ライブラリ名`

## 4. 別のPCで始めるとき／GitHubからクローンしたとき
`node_modules` は GitHub に上がっていないので作り直す。中身は一発で復元できる：
```powershell
cd frontend
npm install
npm run dev
```

## 5. よくあるトラブル
- **node が「用語として認識されません」**
  → 未インストールか、PATHが未反映。PowerShellを開き直す
  → 本体の有無は `Test-Path "C:\Program Files\nodejs\node.exe"` で確認できる
- **git status が clean でコミットできない**
  → プロジェクトをルートと違う場所（1つ上のフォルダなど）に作っている可能性大
  → `pwd` と `ls frontend`（package.json があるか）で確認。探すときは：
  ```bash
  find ~/Documents -name package.json -not -path "*/node_modules/*"
  ```
- **ポートが使用中**
  → 前のサーバーが動きっぱなし。止めるか、表示された別の Local URL を使う

## Python 側との対応（再掲）
| Python | React |
|---|---|
| `.venv/` | `node_modules/` |
| `requirements.txt` | `package.json` |
| `pip install` | `npm install` |
| `uvicorn main:app --reload` | `npm run dev` |

どちらも `.venv/` と `node_modules/` は GitHub に上げない。
