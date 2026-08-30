---
title: "実装前に仕様をgrillingするAgent Skill『qa-grilling』を作った"
emoji: "🔥"
type: "tech"
topics: ["ai", "claudecode", "codex", "qa"]
published: false
---

最近、PMとして仕様を詰めたり、QAに関わったりすることが増えた。

実装後に「この状態はどうする？」「通信に失敗したら？」「二重に実行されたら？」と気づくと、コードだけでなく設計まで戻ることになる。この手戻りを、できるだけ実装前に減らしたいと思った。

そこで、仕様や設計を実装前にレビューするAgent Skill、[`qa-grilling`](https://github.com/nomuman/qa-grilling)を作った。

## Grillingとは

元になった[Grillingの記事](https://zenn.dev/sato_frontend/articles/1a85841505b9bb)では、AIに設計を問い詰めてもらい、曖昧な前提や未決定の仕様を詰めていく。

このやり方がよかった。自分が気にしている箇所だけを壁打ちするより、自分の視野の外にある分岐や前提を拾いやすい。

## qa-grillingでやること

`qa-grilling`は、PRD、画面設計、API契約、実装計画、既存コードなどを対象にする。

状態、遷移、データ、副作用、依存関係を整理し、次のような組み合わせで壊れ方を探す。

```text
upload × reliability × interruption
→ アップロード中にアプリが終了したら？

upload × correctness × concurrency
→ 同じ動画が二重に登録されたら？
```

見つけたものは、単なる指摘で終わらせず、仕様変更、受け入れ条件、テスト観点、可観測性、残るリスクに落とし込む。

## 使い方

インストール後に明示的に呼び出す。

Codex:

```text
$qa-grilling この機能を実装前にレビューして
```

Claude Code:

```text
/qa-grilling この機能を実装前にレビューして
```

普通のレビューで勝手に起動しないよう、明示呼び出し専用にしている。

## おわりに

QAで見つかる問題を、すべて実装前に防げるわけではない。それでも、状態の抜けや失敗時の挙動のように、仕様の段階で考えられるものは多い。

`qa-grilling`は、実装を急ぐ前に「この設計は、どう壊れるか？」を考えるための道具。

[GitHub - nomuman/qa-grilling](https://github.com/nomuman/qa-grilling)
