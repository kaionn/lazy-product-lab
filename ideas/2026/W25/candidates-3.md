# Week 2026-W25 Candidates

> Generated: 2026-06-19 07:04 JST
> Generator: Claude (lazy-product-lab / scheduled)

## 1. SerialSpy Box

- カテゴリ: ハードウェア
- 対象ユーザー: ESP32 / Arduino で組み込み開発しているエンジニア
- 一行で: UART ログを Wi-Fi 経由でブラウザにストリームする 800 円デバイス

### 解決する痛み

シリアルモニターを閉じた瞬間に過去のログが全部消える。デバイスが別の部屋で動いているとき、ノートPCを持ち歩かずに USB ケーブルを刺さずにリアルタイムで挙動を確認したい。組み込みデバイスを複数台同時にデバッグすると USB ポートと IDE ウィンドウが足りなくなる。`printf` デバッグをもっと楽にしたい。

### 1 週間で作るならこれ

- ESP32 の UART1 ピンを受信してオンメモリのリングバッファ（最大 2000 行）に保存
- `http://spybox.local/` でブラウザから EventSource でリアルタイムストリーミング
- URLクエリパラム `?filter=ERROR` でキーワードフィルタリング表示
- `/download` エンドポイントでバッファ全件を `.txt` でダウンロード
- ブレッドボード配線 + 3.3V/5V 変換ロジックレベルシフタで汎用 UART に接続

### なぜ雑か

バッファが 2000 行を超えたら古い行はサイレントドロップ。複数デバイスの同時監視なし（ESP32 1 台に 1 デバイス専用）。Wi-Fi が切れると再接続するまでログが取れない。ケースなしのブレッドボード剥き出し運用。UART ボーレートは 115200 bps 固定（変更はソース書き換え）。

### 雑な技術スタック候補

MicroPython + ESP32 + asyncio + utemplate + UART(machine.UART) + Wi-Fi AP モード or STA モード

---

## 2. ClosureReport

- カテゴリ: その他（GitHub Actions）
- 対象ユーザー: 実験リポジトリが 50 本以上溜まって整理できていない個人エンジニア
- 一行で: 半年放置リポジトリをまとめてアーカイブ提案 Issue を毎月自動投稿

### 解決する痛み

GitHub のリポジトリ一覧を開くと「あれどこに行ったっけ」状態の実験リポが山積みになっている。「このリポジトリ消していいんだっけ？」を判断するために 1 個ずつ開くのが面倒で何もしないまま年を越す。GitHub の archive 機能は知っているが「何をアーカイブするか決める」作業自体が億劫で先送りにしてしまう。

### 1 週間で作るならこれ

- GitHub API で自分の全 public リポジトリを取得し `last_pushed_at` でソート
- 6 ヶ月以上更新なし + スターなし + フォークなし を「お墓候補」として判定
- お墓候補を Markdown 表（名前・最終更新日・言語・説明）にまとめてレポート生成
- 毎月 1 日 0:00 JST に cron で起動し、指定リポジトリの Issues にレポートを自動 POST
- Issue タイトル: `[Graveyard Report] 2026-06 — N 件のお墓候補があるのだ`

### なぜ雑か

重要度判定は「更新日・スター・フォーク数」の 3 つだけ。コードの複雑さ・依存関係・CI 結果は無視。private リポジトリには手を出さない（public のみ）。アーカイブ実行は自動化せず手動操作が必要（Issue を Close したら完了、というフロー）。

### 雑な技術スタック候補

Python + PyGithub + GitHub Actions (schedule: cron) + Jinja2 (Markdown テンプレート) + GitHub Secrets で PAT 管理

---

## 3. QueryChef

- カテゴリ: 学習ツール
- 対象ユーザー: JOIN は書けるが WINDOW 関数・HAVING の使い所に自信がないバックエンドエンジニア / データ分析入門者
- 一行で: 架空 EC サイト DB を題材に SQL 難問をブラウザだけで毎日 1 問解くのだ

### 解決する痛み

LeetCode の SQL 問題は実務との乖離が大きくてモチベーションが続かない。MySQL Workbench や Docker を入れるハードルが高くて練習環境を作れないまま放置してしまう。GROUP BY と HAVING の違い、ROW_NUMBER と RANK の差を何度読んでも腑に落ちない。「WINDOW 関数を使ったことはあるが人に説明できない」状態が続いている。

### 1 週間で作るならこれ

- ブラウザ内 SQLite（sql.js WASM）で EC サイト架空 DB（orders / users / products / reviews 4 テーブル）をオンメモリ展開
- 問題 40 問ハードコード（SELECT → JOIN → GROUP BY → HAVING → WINDOW 関数の難易度順）
- 書いた SQL を実行 → 期待結果 JSON と照合して正誤判定、失敗時はエラー行ハイライト
- 不正解時にヒントを 3 段階で開示（最後はほぼ答え）
- 進捗と達成バッジ（8 種）を localStorage に保存、インストール不要でどこでも動く

### なぜ雑か

正誤判定はカラム順まで含めた完全一致比較なので正解でも列順が違うと不正解になる。EXPLAIN やインデックスの学習は範囲外。問題は固定 40 問でユーザー追加不可。DB スキーマの変更は手動でソース内の JSON を書き換えるしかない。スマホの横幅では SQL エディタが崩れる。

### 雑な技術スタック候補

Vanilla JS + sql.js (SQLite WASM) + CSS Grid + CodeMirror（エディタ） + GitHub Pages で静的ホスト

---

## 選び方

- どれを 1 週間使う? ローカルで `/lazy-product-pick 1` か `2` か `3` で選んで深掘りするのだ
- 全部却下なら `/lazy-product-generate` を再実行で OK なのだ
