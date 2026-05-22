# Week 2026-W21 Selected: NoiseSleepLog

> Picked: 2026-05-23 08:26 JST
> From: candidates-3.md #3
> Status: picked
> Selected via: #1

## TL;DR

_未深掘り (Stage 1 スタブ)。ローカルで `/lazy-product-pick` を実行すると深掘り版で上書きされる。_

## 元の候補

<details>
<summary>candidates から転記</summary>

## 3. NoiseSleepLog

- カテゴリ: ガジェット
- 対象ユーザー: 睡眠が浅い気がするが高価なスマートウォッチを持たない人
- 一行で: RPi と USB マイクで夜の騒音タイムラインをグラフ化

### 解決する痛み

「なんか眠りが浅い」と感じているが原因不明。朝の車の音なのか、隣室の物音なのか、パートナーのいびきなのか、データがなければ改善策もとれない。高価なスマートウォッチは充電が面倒で続かない。マイクと RPi があれば夜間の騒音ログを取れるはずなのに、ちょうどいい OSS ツールが見当たらない。

### 1 週間で作るならこれ

- Raspberry Pi Zero 2W + USB マイクを枕元に置くだけのセットアップ
- 夜間の指定時間帯に 1 秒ごとの音量デシベルを SQLite に記録
- 朝 LAN 内 Web UI を開くと昨夜の音量タイムラインをグラフ表示
- 90 dB 超えた時刻を「騒音イベント」として赤くハイライト表示
- 録音データは保存せずデシベル値のみ記録（プライバシー配慮）

### なぜ雑か

音量だけで睡眠フェーズは判定しない（加速度センサーなし）。マイク感度は機種依存でキャリブレーションなし。リアルタイム表示は未対応。Web UI はローカル LAN 限定で外部公開は自己責任。Raspberry Pi の入手性問題は自力解決してほしいのだ。

### 雑な技術スタック候補

Python + PyAudio + SQLite + Flask + Chart.js、Raspberry Pi OS Lite 上で systemd サービスとして常時起動

</details>

## 次のアクション

- [ ] ローカルで `/lazy-product-pick` を実行して深掘り (Stage 2)
- [ ] `/lazy-product-bootstrap` で雛形リポを作成 (Stage 3)
