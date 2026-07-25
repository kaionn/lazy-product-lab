# Week 2026-W29 Selected: README.party

> Picked: 2026-07-25 18:41 JST
> From: candidates-2.md #3
> Status: picked
> Selected via: #5

## TL;DR

_未深掘り (Stage 1 スタブ)。ローカルで `/lazy-product-pick` を実行すると深掘り版で上書きされる。_

## 元の候補

<details>
<summary>candidates から転記</summary>

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

</details>

## 次のアクション

- [ ] ローカルで `/lazy-product-pick` を実行して深掘り (Stage 2)
- [ ] `/lazy-product-bootstrap` で雛形リポを作成 (Stage 3)
