# lazy-product-lab

> 月水金、雑にプロダクトを考える仕組み。

## なに

月・水・金の朝 7:00 (JST) に Claude が雑なプロダクトアイデアを 3 案投げ込んで、その中から気に入った案をピックして深掘りする個人実験場。

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
    │   ├── candidates.md     # 月曜分の 3 案
    │   ├── candidates-2.md   # 水曜分の 3 案
    │   ├── candidates-3.md   # 金曜分の 3 案
    │   └── selected.md       # 採用案の深掘り
    └── W20/
        └── ...
```

ISO 週番号 (`W01`-`W53`) を採用。

## ワークフロー

| タイミング | アクション | 担当 |
|-----------|-----------|------|
| 月・水・金 朝 7:00 JST | 3 案生成 → push → Discord 通知 | Claude (Routine) + GitHub Actions |
| 気が向いたとき | `/lazy-product-pick <1\|2\|3>` で 1 案を深掘り | わたし |
| 次の生成までに | 実装するか撤退するか決断 | わたし |
| 全部つまらない | 次のサイクルを待つか `/lazy-product-generate` を手動再実行 | わたし |

## スキル

`~/.claude/commands/` にローカル定義:

- `/lazy-product-generate` — 3 案生成 → `candidates.md` に書いて push
- `/lazy-product-pick <1|2|3>` — 1 案を深掘り → `selected.md` に書いて push

## 関連

- [Claude Code](https://claude.com/code) のスケジュール機能で自動化
- ジャンル制約なし（雑食系）
