# lazy-product-lab

> 一週間に一個、雑にプロダクトを考える仕組み。

## なに

毎週金曜 19:00 (JST) に Claude が雑なプロダクトアイデアを 3 案投げ込んで、その中から 1 案をピックして深掘りする個人実験場。

完璧主義を捨てて、量から質を引き出す。

## ルール

- 雑であることを許す。エッジケース無視で OK。
- 1 週間で MVP に到達できないアイデアは却下。
- 5 人にデモして「使いたい」が 3 人取れたら成功。
- つまんなかったら撤退してよし。

## 構造

```
ideas/
└── 2026/
    ├── W19/
    │   ├── candidates.md   # 自動生成された 3 案
    │   └── selected.md     # 採用案の深掘り
    └── W20/
        └── ...
```

ISO 週番号 (`W01`-`W53`) を採用。

## ワークフロー

| タイミング | アクション | 担当 |
|-----------|-----------|------|
| 毎週金曜 19:00 JST | `/lazy-product-generate` で 3 案生成 | Claude (cron) |
| 金〜土 | `/lazy-product-pick <1\|2\|3>` で 1 案を深掘り | わたし |
| 翌週木まで | 実装するか撤退するか決断 | わたし |
| 全部つまらない週 | `/lazy-product-generate` を再実行 | わたし |

## スキル

`~/.claude/commands/` にローカル定義:

- `/lazy-product-generate` — 3 案生成 → `candidates.md` に書いて push
- `/lazy-product-pick <1|2|3>` — 1 案を深掘り → `selected.md` に書いて push

## 関連

- [Claude Code](https://claude.com/code) のスケジュール機能で自動化
- ジャンル制約なし（雑食系）
