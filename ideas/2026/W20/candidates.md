# Week 2026-W20 Candidates

> Generated: 2026-05-13 07:10 JST
> Generator: Claude (lazy-product-lab / scheduled)

## 1. CommitSculptor

- カテゴリ: CLI
- 対象ユーザー: コミットメッセージが雑なエンジニア
- 一行で: 雑コミットを AI が conventional commits に整形

### 解決する痛み
`fix`, `update`, `wip` みたいな意味のないコミットを積み重ねた後、PR を出す前に慌ててスカッシュしようとするが何を書けばいいか分からない。チームレビューで「コミットメッセージちゃんと書いて」と毎回怒られる。

### 1 週間で作るならこれ
- `git log --oneline -10` の出力を自動取得して LLM に渡す
- Conventional Commits 形式（feat/fix/chore/docs）に変換して候補を 3 つ表示
- 選択したメッセージで `git commit --amend` を実行
- `--staged` モードで差分からコミットメッセージを生成
- `.commitsculptor.yml` でチーム独自プレフィックスを追加できる

### なぜ雑か
amend 確認ダイアログなしでそのまま上書きする。push 済みコミットへの amend も止めない。LLM 呼び出しが失敗したら無言で終了。

### 雑な技術スタック候補
Python + Click + litellm (Claude Haiku) + subprocess

---

## 2. StandupShuffle

- カテゴリ: Bot
- 対象ユーザー: リモートチームのスクラムマスター・チームリード
- 一行で: 毎朝違うスタンドアップ質問を Slack に自動投稿

### 解決する痛み
毎日同じ「昨日やったこと・今日やること・ブロッカー」の 3 点セットで完全に飽き、誰も真剣に答えなくなる。でも質問を考えるコストを毎日払いたくない。スタンドアップが形骸化してチームの温度感が分からなくなる。

### 1 週間で作るならこれ
- Slack Slash Command で `/standup-setup #channel` してチャンネル登録
- 平日朝 9:00 に質問をランダムで 1 問投稿（100 問ハードコード）
- 「技術負債どこにある?」「今週一番テンション上がったこと?」など多様な質問セット
- スレッドに回答を収集して週金曜に自動サマリ投稿
- `/standup-skip today` で今日だけスキップ

### なぜ雑か
質問は JSON にハードコードした 100 問で固定。チーム固有の質問追加は手動でソース編集が必要。Slack の rate limit に引っかかったら silent fail。

### 雑な技術スタック候補
Node.js + Slack Bolt + Vercel (Functions + Cron) + Upstash Redis

---

## 3. CodeTypist

- カテゴリ: 学習ツール
- 対象ユーザー: プログラミング学習中の学生・コードを速く打ちたいエンジニア
- 一行で: コードスニペットを打ち込んで指に染み込ませる TUI

### 解決する痛み
タイピング練習サイトは英文ばかりでコード特有のキー（`{}[]<>|`）が全然練習できない。LeetCode の解答をコピペする癖がついて自力でコードを打つのが遅いまま。IDE の補完に頼りすぎて構文を手で書けない。

### 1 週間で作るならこれ
- Python / JavaScript / Go / Rust のスニペットをランダム出題（各言語 30 問ハードコード）
- リアルタイムでミスキーを赤ハイライト表示
- WPM（Words Per Minute）と精度(%)を計測してセッション後に表示
- 言語フィルタ: `codotypist --lang python` で絞り込み
- `.codotypist_scores.json` にローカル保存してベストスコア更新を通知

### なぜ雑か
スニペットは 120 問ハードコードで更新なし。タブ/スペース混在の判定が適当。ターミナル幅が狭いと表示が崩れる。Windows 未対応。

### 雑な技術スタック候補
Go + tview (TUI ライブラリ) + embed でスニペット同梱

---

## 選び方

- どれを 1 週間使う? ローカルで `/lazy-product-pick 1` か `2` か `3` で選んで深掘りするのだ
- 全部却下なら `/lazy-product-generate` を再実行で OK なのだ
