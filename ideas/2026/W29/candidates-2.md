# Week 2026-W29 Candidates

> Generated: 2026-07-17 07:06 JST
> Generator: Claude (lazy-product-lab / scheduled)

## 1. ReadQueue

- カテゴリ: Browser Extension
- 対象ユーザー: 「後で読む」タブが常時 20 本以上開いているエンジニア・リサーチャー
- 一行で: 全タブの読了時間を計算して今日読める分だけ並べ直す

### 解決する痛み

タブを大量に開いたまま「後でまとめて読もう」と思い続けて、結局どれも読まずに全部閉じる。Pocket 等の外部ツールは管理コストが高くて習慣化できない。「この記事は 3 分で読める、あれは 15 分かかる」が一目で分かれば優先順位がつけられるのに、タブのタイトルだけでは全くわからない。

### 1 週間で作るならこれ

- 各タブのページ本文 (document.body.innerText) を content_script で取得し文字数→読了分数を計算（平均 400 字/分）
- ポップアップに「タイトル + 読了 X 分」のリストを表示
- 「5 分以内」「15 分以内」フィルタボタンで絞り込み
- 読んだタブをチェックしてリストから除外（chrome.storage.local に保存）
- タブをクリックするとそのタブにフォーカス移動

### なぜ雑か

PDF・YouTube・認証壁のあるページは未対応で「取得失敗」と表示するだけ。読了時間は 400 字/分固定で個人差は無視。本文抽出は document.body.innerText そのままなのでナビゲーションや広告テキストも混入する。

### 雑な技術スタック候補

Chrome Extension Manifest V3 + content_script + Vanilla JS + chrome.storage.local（ビルドツール不要、ファイル 6 本以下）

---

## 2. ClipVault

- カテゴリ: デスクトップアプリ
- 対象ユーザー: コピペで作業するエンジニア・ライター・データ入力担当者
- 一行で: コピーした直近 20 件を Ctrl+Shift+V でいつでも呼び戻す

### 解決する痛み

Ctrl+C を 2 回打つと 1 回目がなくなる。「さっきコピーしてたあれ」を取り戻すためにブラウザ履歴やチャットを漁る作業が 1 日に何十回もある。Alfred/Raycast は Mac 専用かつ有料。Windows で使える軽量なクリップボード履歴ツールが少ない。組み込みの「クリップボード履歴 (Win+V)」はクラウド同期が必要で嫌だという人もいる。

### 1 週間で作るならこれ

- システムトレイ常駐、クリップボードの変化を 500ms ポーリングで監視し最新 20 件を SQLite に記録
- Ctrl+Shift+V でランチャーウィンドウが前面に浮き上がり、上下キーで選択・Enter で貼り付け
- 各エントリに先頭 60 文字のプレビューと「X 分前」の時刻を表示
- 「記録停止モード」トグルでパスワード入力時など一時的に記録をオフ
- テキストのみ対応（画像・ファイルパスは無視）

### なぜ雑か

画像・ファイルのクリップボードは完全無視。検索機能は 20 件しかないので省略。クロスデバイス同期なし。パスワードらしき文字列の自動除外なし。動作確認は Windows のみ、macOS は「たぶん動く」。

### 雑な技術スタック候補

Tauri 2 + Rust（clipboard クレート + rusqlite + tray-icon）+ SvelteKit（UI）、MSI インストーラー自動生成

---

## 3. README.party

- カテゴリ: Web
- 対象ユーザー: OSS 作者・個人開発者で「GitHub の README を LP っぽく見せたい」人
- 一行で: GitHub の README URL を貼るだけで LP 風プレビューを即生成

### 解決する痛み

GitHub の README はコード文化で書かれており非技術者には伝わらない。かといって Webflow や Framer で別途 LP を作るのはコストが高い。「README をそのままもうちょっと綺麗に見せたい」だけなのに手段がない。個人プロジェクトの紹介 URL を誰かに送るとき、いきなり GitHub の画面は野暮ったい。

### 1 週間で作るならこれ

- GitHub の README URL を入力すると raw テキストを取得して Markdown レンダリング
- 見出し構造に基づいてセクションを Hero / Features / Usage / License に自動マッピング
- Light / Dark / Terminal の 3 テーマを切り替え
- 「このURL でシェア」ボタンでクエリパラメータ付き URL を生成（永続ホスティングなし）
- OGP メタタグを自動付与して SNS シェア時にタイトルと概要を表示

### なぜ雑か

README の構造推測はヒューリスティック（h1 = Hero タイトル、最初の ul = Features リストと仮定）なので崩れることがある。HTML が混入している README は部分的にレイアウトが壊れる可能性あり。カスタムドメイン・独自ホスティング機能なし、URL シェアのみ。Private リポジトリの README は取得不可。

### 雑な技術スタック候補

Next.js (App Router) + Tailwind + marked.js（Markdown パーサ）+ Vercel、GitHub raw.githubusercontent.com を直叩き（認証なし）

---

## 選び方

- どれを 1 週間使う? ローカルで `/lazy-product-pick 1` か `2` か `3` で選んで深掘りするのだ
- 全部却下なら `/lazy-product-generate` を再実行で OK なのだ
