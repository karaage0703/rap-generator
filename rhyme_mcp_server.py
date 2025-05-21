# rhyme_server.py
from pathlib import Path
import random
from typing import List, Tuple

import pandas as pd
from mcp.server.fastmcp import FastMCP

# --------------------------------------------------
# データ読み込み
# --------------------------------------------------
# DATA_PATH = Path("data/in_note_rhymes.csv") #フルサイズのcsvを作成した場合はそちらを指定
DATA_PATH = Path("data/in_note_rhymes_compressed.csv")
df = pd.read_csv(DATA_PATH)

# target_word ➜ [(rhyme_word, reading, n_chars), ...]
_rhyme_dict = {
    target: list(zip(g["rhyme_word"], g["reading"], g["n_chars"])) for target, g in df.groupby("target_word", sort=False)
}

# --------------------------------------------------
# MCP サーバ初期化
# --------------------------------------------------
mcp = FastMCP("rhyme_server")


@mcp.tool()
def get_rhymes(word: str, top_k: int | None = 100) -> List[Tuple[str, str]]:
    """
    指定した単語と韻を踏める候補 (rhyme_word, reading) を返す。

    ソート規則:
        1. 文字数が多い順
        2. 同じ文字数の単語間はランダム抽出

    Args:
        word (str): インプット単語
        top_k (int | None, optional): 返す最大件数。None で全件

    Returns:
        List[Tuple[str, str]]: (rhyme_word, reading) のタプル列。
                               該当がなければ空リスト。
    """
    candidates = _rhyme_dict.get(word, [])
    if not candidates:
        return []

    # シャッフルしてから n_chars で降順ソート
    random.shuffle(candidates)
    candidates.sort(key=lambda x: x[2], reverse=True)  # x[2] は n_chars

    # n_chars を落として (word, reading) だけ返す
    result = [(w, r) for w, r, _ in candidates]
    return result[:top_k] if top_k is not None else result


@mcp.tool()
def get_available_words(n: int = 100) -> List[str]:
    """
    韻データベースの中から、対応可能な target_word をランダムに選んで返す。

    条件:
        - 対応する rhyme_word が10個以上あるもののみ対象
        - ランダム抽出
        - デフォルトは最大100件

    Args:
        n (int): 返す単語数の上限（デフォルト100）

    Returns:
        List[str]: 韻データの対象になっている target_word のリスト
    """
    valid_targets = [t for t, rhymes in _rhyme_dict.items() if len(rhymes) >= 10]
    return random.sample(valid_targets, min(n, len(valid_targets)))


# --------------------------------------------------
# エントリポイント
# --------------------------------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")
