# Week 2026-W30 Selected: OnboardBuddy

> Picked: 2026-07-25 18:41 JST
> From: candidates-5.md #3
> Status: picked
> Selected via: #7

## TL;DR

_未深掘り (Stage 1 スタブ)。ローカルで `/lazy-product-pick` を実行すると深掘り版で上書きされる。_

## 元の候補

<details>
<summary>candidates から転記</summary>

## 3. OnboardBuddy

- カテゴリ: 業務ツール (Web)
- 対象ユーザー: 新しいエンジニアが加わるたびにオンボーディング資料を手作業で更新しているテックリード
- 一行で: リポジトリのURLを貼るだけで初日セットアップ手順書が自動生成されるのだ

### 解決する痛み

オンボーディング資料はREADMEの片隅に古い手順が残ったままで、新メンバーは結局Slackで「これどうやって動かすんですか」と同じ質問を繰り返す。テックリードは毎回同じ説明を書くか口頭で伝えるかの二択で消耗する。リポジトリの中身自体は最新なのだから、そこから自動的に「初日ガイド」を作れれば説明の手間が省ける。

### 1 週間で作るならこれ

- GitHubリポジトリURLとread-only権限のPersonal Access Tokenを入力するだけのフォーム
- `package.json` / `README.md` / `.env.example` / `.github/workflows` の内容をGitHub API経由で取得
- Claude APIに投げて「必要なツールのインストール手順」「環境変数の設定方法」「起動コマンド」「最初に読むべきファイル」をMarkdownで生成
- 生成結果を専用URL（`/onboard/:id`）で常時閲覧できるようにして新メンバーに共有
- 「情報が古くなった」ボタンで手動リフレッシュ（再生成）のみ対応、自動更新はしない

### なぜ雑か

private repoの認証はPersonal Access Token直貼りでOAuth連携は作らない。生成された手順の正確性は保証せず、実際に実行して検証する機能もない。モノレポや複数言語混在プロジェクトは想定外（単一`package.json`前提）。生成後のガイドは新メンバー本人が編集することはできず、リード側が再生成するだけの一方通行にする。

### 雑な技術スタック候補

Next.js + GitHub REST API (Octokit) + Anthropic API (Claude) + Supabase(生成結果保存) + Vercel

</details>

## 次のアクション

- [ ] ローカルで `/lazy-product-pick` を実行して深掘り (Stage 2)
- [ ] `/lazy-product-bootstrap` で雛形リポを作成 (Stage 3)
