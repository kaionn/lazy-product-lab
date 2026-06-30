# Week 2026-W27 Candidates

> Generated: 2026-07-01 07:04 JST
> Generator: Claude (lazy-product-lab / scheduled)

## 1. DepWatcher

- カテゴリ: SaaS
- 対象ユーザー: 外部ライブラリに依存している個人開発者・スモールチーム
- 一行で: package.json の breaking change を週次メールで AI 要約通知

### 解決する痛み

Dependabot はセキュリティ脆弱性は教えてくれるが「v3 で API が全部変わった」という breaking change の文脈を届けてくれない。リリースノートを全ライブラリ分追うのは非現実的で、気づいたら `npm install` 後にビルドが壊れている。package.json を登録するだけで、新リリースの Changelog を AI で要約して重大度スコア（breaking / deprecated / minor）を付けて週次メールで届けてほしい。

### 1 週間で作るならこれ
- package.json をフォームにペーストして登録（認証なし・メールアドレスのみ）
- GitHub Releases API で dependencies の最新リリースノートを取得
- Claude API で「breaking change あり？」「何が変わった？」を 3 行要約 + 重大度判定
- 週次でメール送信（breaking change があった場合のみ）
- ダッシュボード（簡易）で最後に確認した日時を表示

### なぜ雑か

npm のみ対応で pip / cargo / go.mod は無視。`devDependencies` はスキャンしない。リリースノートが英語のみで日本語要約の品質は運任せ。メール HTML テンプレートはプレーンテキスト。GitHub API のレート制限を超えたら黙って翌日に後回し。

### 雑な技術スタック候補
FastAPI + Claude API (claude-haiku-4-5) + APScheduler + SQLite + SendGrid 無料枠、Render 無料枠でデプロイ

---

## 2. IssueInk

- カテゴリ: ガジェット
- 対象ユーザー: デスクに物理的な「今日のタスク」表示がほしいエンジニア
- 一行で: E-ink 卓上フレームに今日の GitHub Issues を毎朝表示

### 解決する痛み

PC 画面は Slack・メール・通知でうるさい。「今日これだけやる」を物理で表示するデバイスがあると余計な情報をシャットアウトして集中できる。電子ペーパーは充電不要で目に優しく、電源を切っても表示が消えない。TODO アプリより「物理的に見える」ほうが心理的重さがある。GitHub Issues がすでにタスク管理の中心なら、そこから引っ張るだけで運用コストゼロ。

### 1 週間で作るならこれ
- Raspberry Pi Zero 2W + 7.5 インチ電子ペーパー（Waveshare 製）
- 毎朝 7:00 に GitHub API で「自分に assigned・open」の Issues を最大 5 件取得
- タイトル・リポジトリ名・ラベルを電子ペーパーに描画して更新
- 右上に今日の日付と天気アイコン（wttr.in API）を追加
- systemd タイマーで毎朝自動実行

### なぜ雑か

Wi-Fi 環境必須でセットアップは SSH のみ。解像度の制約でフォントが小さめになる場合あり。Issues のタイトルが長いと途中で切れる。PR・Discussions には非対応。電子ペーパーの書き換え速度は遅いので更新時にちらつく。

### 雑な技術スタック候補
Python + Waveshare e-Paper ライブラリ + Pillow + GitHub API + wttr.in API、systemd タイマーで常時運用

---

## 3. LocalLLM Compare

- カテゴリ: Web
- 対象ユーザー: Ollama でローカル LLM を複数入れて実験しているエンジニア
- 一行で: 同じプロンプトを複数 LLM に同時送信して出力を並べて比較

### 解決する痛み

Ollama を使っていると `llama3`・`qwen2.5`・`phi4` など複数モデルが手元にある。「どのモデルが日本語に強い？」「コード補完の精度は？」を確かめるにはターミナルを往復する必要がある。モデルごとに同じプロンプトを手で叩き直して出力をメモ帳に貼り比べる作業が苦痛。ブラウザで横並びに ストリーミング表示されるだけで実験サイクルが 10 倍速くなる。

### 1 週間で作るならこれ
- `localhost:11434` の Ollama API から `/api/tags` でローカルモデル一覧を自動取得
- チェックボックスで比較したいモデルを選択（最大 4 つ）
- プロンプト送信後、各モデルの出力をカラムに並べてストリーミング表示
- 出力速度（トークン/秒）と応答完了時間をカラム下部に表示
- 各カラムにコピーボタン

### なぜ雑か

Ollama のみ対応で llama.cpp サーバー・LM Studio・OpenAI API には非対応。会話履歴なし・1 ターン完結のみ。モデル 4 つ同時リクエストで CPU/GPU が詰まっても待つだけ。モバイルレイアウト未対応。エラーは画面に生 JSON を表示して終わり。

### 雑な技術スタック候補
Vite + React + EventSource（SSE でストリーミング）、ビルド済み静的ファイルを Ollama と同じ PC で `npx serve dist` で起動

---

## 選び方

- どれを 1 週間使う? ローカルで `/lazy-product-pick 1` か `2` か `3` で選んで深掘りするのだ
- 全部却下なら `/lazy-product-generate` を再実行で OK なのだ
