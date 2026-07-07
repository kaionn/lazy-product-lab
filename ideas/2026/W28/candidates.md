# Week 2026-W28 Candidates

> Generated: 2026-07-08 07:06 JST
> Generator: Claude (lazy-product-lab / scheduled)

## 1. PairUp Bot

- カテゴリ: Bot (Slack)
- 対象ユーザー: フルリモートで孤独感を感じているエンジニアチーム・スタートアップ
- 一行で: 週1でランダムにペアを組む雑談促進Bot

### 解決する痛み

フルリモートで働くと「隣の人に話しかける」ができず、チームメンバーのことを知らないまま半年たつ。1on1はマネージャーとだけで、同僚との雑談チャンスがゼロ。孤独感と「あの人何してるんだろう」感が積もる一方で、ランチ雑談会を企画するほどのモチベーションも湧かない。

### 1 週間で作るならこれ

- `/pairup join` で参加登録、毎週月曜 9 時に 2 人ペアを自動生成して両者に DM 通知
- DM には「相手の名前」と「話のネタ（ハードコード 50 問からランダム）」を添付
- 過去ペア履歴を Vercel KV に保存し、同じペアを 2 週間は繰り返さない
- `/pairup skip` で今週をパス（有休・繁忙期向け）
- `/pairup stats` でチーム全体の「接続済みペア一覧」をテキスト表示

### なぜ雑か

ペアは 2 人固定でグループチャット未対応。話のネタは AI 生成なくハードコード。スケジュールは月曜 9 時 JST 固定でタイムゾーン未考慮。単一 Slack ワークスペース専用で OAuth フロー実装なし。

### 雑な技術スタック候補

Bolt for JS + Vercel Serverless Functions + Vercel KV + cron-job.org で週次トリガー

---

## 2. EnvDeck

- カテゴリ: デスクトップアプリ (Tauri)
- 対象ユーザー: dev/staging/prod など複数環境の .env を使い分ける個人開発者
- 一行で: メニューバーから.envをワンクリックで切り替え

### 解決する痛み

ローカル開発で「.env.dev」「.env.staging」「.env.prod」を手動でコピペしてリネームしている。git stash した後に間違えた .env が残っていて、うっかり本番 DB に接続してしまったことがある。毎回 `cp .env.dev .env` を打つのが地味に面倒で、ミスのリスクが消えない。

### 1 週間で作るならこれ

- 初回起動時にプロジェクトディレクトリを選択、`.env.*` ファイルを自動検出
- メニューバーのドロップダウンに検出した環境ファイルを一覧表示
- 選択するとアクティブな `.env` にシンボリックリンクで即切り替え
- 現在アクティブな環境名をメニューバーアイコンに常時表示 (例: `🟢 dev`)
- 複数プロジェクトをドロップダウンのグループで管理

### なぜ雑か

Mac 専用（Windows / Linux 未対応）。Docker Compose の `env_file` は追跡しない。環境間の diff 表示なし。シンボリックリンクが張れないファイルシステムは未対応。`.gitignore` チェックなしで誰かが `.env.prod` を git 管理していても黙って動く。

### 雑な技術スタック候補

Tauri v2 + React + TypeScript、GitHub Releases で .dmg 直配布

---

## 3. LocaleSync

- カテゴリ: VSCode Extension
- 対象ユーザー: i18n 対応中の Next.js / React 開発者
- 一行で: 翻訳キーの抜けを保存時に即座に赤で警告

### 解決する痛み

`en.json`・`ja.json`・`zh.json` があるプロジェクトで、新しいキーを en.json に追加したのに ja.json に追加し忘れる。ビルド後に画面が文字化けして初めて気づく。`grep -r "missing_key" locales/` を手動で走らせるのが面倒で、CI で落ちるまで誰も気づかない。

### 1 週間で作るならこれ

- `locales/*.json` を自動検出し、保存時に全言語ファイルのキーを比較
- 欠けているキーを VSCode の Problems パネルにエラーとして表示
- Problems パネルの項目をダブルクリックで対象 JSON ファイルにカーソルジャンプ
- コマンドパレットから「欠けているキーを空文字列で一括補完」を実行可能
- `localeSync.baseLocale` 設定で基準言語（デフォルト `en`）を変更可能

### なぜ雑か

JSON only（YAML / POT / gettext 未対応）。配列形式のロケールファイルは非対応（オブジェクト形式のみ）。自動翻訳機能なし（空文字列補完のみ）。locale ファイルのパスは慣習的な `locales/` か `messages/` のみ自動検出、それ以外は手動設定が必要。

### 雑な技術スタック候補

TypeScript + VSCode Extension API（vscode-languageclient 不要）、vsce で VSCode Marketplace に公開

---

## 選び方

- どれを 1 週間使う? ローカルで `/lazy-product-pick 1` か `2` か `3` で選んで深掘りするのだ
- 全部却下なら `/lazy-product-generate` を再実行で OK なのだ
