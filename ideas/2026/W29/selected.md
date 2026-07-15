# Week 2026-W29 Selected: ci-digest

> Picked: 2026-07-15 19:40 JST
> From: candidates.md #1
> Status: picked
> Selected via: #2

## TL;DR

_未深掘り (Stage 1 スタブ)。ローカルで `/lazy-product-pick` を実行すると深掘り版で上書きされる。_

## 元の候補

<details>
<summary>candidates から転記</summary>

# Week 2026-W29 Candidates

> Generated: 2026-07-15 07:07 JST
> Generator: Claude (lazy-product-lab / scheduled)

## 1. ci-digest

- カテゴリ: Bot (GitHub App)
- 対象ユーザー: CI ログ解読に時間を溶かしている個人・小チーム開発者
- 一行で: CI 失敗ログを AI が 3 行に圧縮して PR にコメント

### 解決する痛み

GitHub Actions の CI が落ちるたびに、ANSI エスケープだらけの数百行ログをスクロールして「どの行でなぜ落ちたか」を探す作業が地味につらい。エラー行を発見しても「なぜそうなったか」の文脈がなく、Stack Overflow を漁るのに 20 分溶かすことが週に何度もある。「ログを貼れば AI が読んでくれる」のに、わざわざコピペして ChatGPT に投げるのも面倒だ。

### 1 週間で作るならこれ

- `check_run.completed` イベントを受け取る GitHub App (Webhook) を Vercel Serverless で立てる
- GitHub API でジョブログを取得（末尾 300 行のみ）し Claude API に投げる
- 「原因・該当ファイル・提案 Fix」の 3 項目を日本語で返させ PR コメントとして自動投稿
- 同じワークフローが連続 3 回以上失敗したら「環境問題の可能性あり」バッジをつける
- `.ci-digest.yml` にコメントを投稿しない CI ジョブ名の除外リスト設定

### なぜ雑か

ログが 300 行超えたら末尾だけ食わせるので前半のエラーは見落とす。マトリクスビルドの並列ジョブは最初に完了したジョブしか解析しない。日本語固定でロケール設定なし。GitHub Enterprise 非対応。API レートリミットに当たったら黙ってスキップするだけ。

### 雑な技術スタック候補

Node.js + @octokit/webhooks + Vercel Serverless Functions + Claude API (claude-haiku-4-5)、GitHub Apps として手動インストール

</details>

## 次のアクション

- [ ] ローカルで `/lazy-product-pick` を実行して深掘り (Stage 2)
- [ ] `/lazy-product-bootstrap` で雛形リポを作成 (Stage 3)
