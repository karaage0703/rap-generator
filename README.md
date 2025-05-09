# Rap Generator

日本語ラップの韻を生成するためのツール。[in-note.com](https://in-note.com)から韻のデータを収集し、類似した発音の語句を検索できます。

## セットアップ

1. Pythonの環境を準備 (Python 3.12以上が必要)

2. uvをインストール:
```sh
pip install uv
```

3. レポジトリをクローンし、依存関係をインストール:
```sh
git clone https://github.com/yourusername/rap-generator.git
cd rap-generator
uv venv
source .venv/bin/activate  # Unix系の場合
.venv\Scripts\activate  # Windowsの場合
uv pip install -r requirements.txt
```

## 機能

### データ収集 (`rhyme_scraper.py`)

in-noteから韻のデータを収集します。収集したデータは`data/in_note_rhymes.csv`に保存されます。

### 韻サーバー (`rhyme_mcp_server.py`)

mcpを使用して韻検索サーバーを実装しています。

主な機能:
- `get_rhymes`: 指定した単語に対する韻を検索
- `get_available_words`: 利用可能な単語のリストを取得

## データ構造

韻データは以下のCSVフォーマットで保存:
- target_word: 対象となる単語
- rhyme_word: 韻を踏む単語
- reading: 読み方（ひらがな）
- n_chars: 文字数

## 依存パッケージ

- beautifulsoup4 >= 4.13.4
- mcp[cli] >= 1.7.1
- pandas >= 2.2.3
- requests >= 2.32.3