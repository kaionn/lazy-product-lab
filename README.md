# lazy-product-lab

> 月水金、雑にプロダクトを考える仕組み。

## なに

月・水・金の朝 7:00 (JST) に Claude が雑なプロダクトアイデアを 3 案投げ込んで、Discord 通知の「Select」リンクを 1 タップするだけで深掘り → 雛形リポ作成まで一気通貫で実行できる個人実験場。

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
    │   └── selected.md       # 採用案 (スタブ / 深掘り済み)
    └── W20/
        └── ...
poc/                          # 撤退コスト重視の雛形置き場 (bootstrap で生成)
└── {slug}/
```

ISO 週番号 (`W01`-`W53`) を採用。

## ワークフロー (3 ステージ)

| ステージ | タイミング | アクション | 担当 |
|---------|-----------|-----------|------|
| **0. 生成** | 月・水・金 朝 7:00 JST | 3 案生成 → push → Discord 通知 (Select リンク付き) | Claude (Routine) + Actions |
| **1. Quick Pick** | Discord で気になった瞬間 | :arrow_forward: 「Select」リンク click → Issue Submit (1 タップ) | わたし |
| 〃 | Issue 発火後 | `selected.md` スタブ生成 + push + Issue close | Actions (`select-issue.yml`) |
| **2. Deep Dive** | 深掘りしたくなったら | `/lazy-product-pick` (引数なしで一覧 or タイトル指定) | わたし (Claude Code) |
| **3. Bootstrap** | プロト着手したくなったら | `/lazy-product-bootstrap` で雛形リポ作成 (CLI / Web / Mobile) | わたし (Claude Code) |
| **撤退判断** | 次の生成までに | 実装するか撤退するか決断 | わたし |

### Stage 1: Quick Pick (Discord → Issue → スタブ)

Discord に届く通知の各案末尾に「:arrow_forward: これを Select する」リンクがある。クリックすると GitHub の Issue 作成画面が開き、タイトル・本文・`select` ラベルが prefill 済み。**Submit するだけ**で Actions が `selected.md` スタブを生成し、Issue が自動でクローズされる。

スタブ時点ではアイデアの中身は深掘りされていない (`> Status: picked`)。「とりあえず候補に残した」状態。

### Stage 2: Deep Dive (`/lazy-product-pick`)

Claude Code で `/lazy-product-pick` を実行すると、ペルソナ・MVP 機能・技術スケッチ・1 週間スケジュールまで深掘りされた `selected.md` (`> Status: idea`) に上書きされる。

引数は 4 形式対応:

```bash
/lazy-product-pick                       # 直近の全候補から一覧 → 番号で選択
/lazy-product-pick BarShelf              # タイトル部分一致
/lazy-product-pick 2026-W21-3#2          # 完全 ID
/lazy-product-pick 2                      # 最新 candidates の #N
```

### Stage 3: Bootstrap (`/lazy-product-bootstrap`)

Deep Dive 済みの `selected.md` を起点に、雛形リポを作成して初回コミットまで一気通貫。

```bash
/lazy-product-bootstrap                  # 直近の selected.md
/lazy-product-bootstrap 2026-W21         # 週 ID 指定
```

雛形種別:

| 雛形 | 中身 | 用途 |
|------|------|------|
| **CLI** | TypeScript + Node + `bin/index.ts` | コマンドラインツール |
| **Web (Next.js)** | `create-next-app` + Tailwind | Web アプリ |
| **Mobile (Expo)** | `create-expo-app` (blank-typescript) | iOS / Android |

配置先:

| 選択肢 | 配置先 |
|--------|--------|
| **新規リポ** | `kaionn/{slug}` (`gh repo create` で作成) |
| **PoC** | `lazy-product-lab/poc/{slug}/` (撤退時の廃棄が楽) |

## スキル

`~/.claude/commands/` にローカル定義:

- `/lazy-product-generate` — 3 案生成 → `candidates.md` に書いて push
- `/lazy-product-pick` — Deep Dive → `selected.md` 生成 / スタブ上書き
- `/lazy-product-bootstrap` — selected.md → リポ雛形作成

## Actions

- `notify-discord.yml` — `candidates*.md` push 時に Discord 通知 (Select リンク付き)
- `select-issue.yml` — `select` ラベル付き Issue 発火で `selected.md` スタブ生成

## 関連

- [Claude Code](https://claude.com/code) のスケジュール機能で生成を自動化
- ジャンル制約なし (雑食系)
