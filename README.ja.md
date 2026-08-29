# qa-grilling

**実装してから壊すのではなく、設計のうちに壊す。**

`qa-grilling` は、PRD・仕様書・Figma・アーキテクチャ・実装計画・既存コードを、QAの観点から実装前にレビューするためのAgent Skillです。

発想のベースは **Grilling** です。まず手元の情報を調べ、重要な未決事項を見つけ、人間の判断が必要なものだけを1問ずつ詰めていきます。

ただし目的は少し違います。

- Grilling: **この設計は考え切れているか？**
- qa-grilling: **この設計は、どう壊れるか？**

巨大なチェックリストを順番に消化するSkillではありません。機能の状態やデータフローをモデル化し、故障条件を探索し、リスク順に並べ、本当に決める必要があるところだけ質問します。

> 「どんなテストを書く？」から始めない。まず「この設計はどう壊れる？」を考える。

## 何をするSkillか

PRD、Issue、Figma、API仕様、実装計画、コードなどを渡すと、次の順番でレビューします。

1. 質問する前に、参照できる仕様・コード・設計・既存テストを調べる
2. Actor、State、Transition、Invariant、Data、Side Effect、Dependencyを整理する
3. `Feature × Quality × Event` で故障条件を探索する
4. 状態遷移、境界値、通信、並行処理、永続化、ライフサイクル、Security、Privacy、Accessibility、UX、感情・信頼、ObservabilityなどのQA Lensを当てる
5. Mobile、Web、API、Media、Payment、Notification、Offline Sync、AIなど必要なDomain Packを追加する
6. 発見事項を「バグ」「曖昧」「仕様不足」「テスト義務」「観測性不足」「受容リスク」に分類する
7. リスク順に並べる
8. 人間の意思決定が必要なものだけ、1問ずつgrillingする
9. QA Design Report、Acceptance Criteria、Test Obligations、Observability Requirements、Residual Risksを出す

## なぜ実装前QAなのか

実装の速度が上がるほど、後から仕様の穴が見つかったときの手戻りが目立ちます。

たとえば「アップロード中にアプリを終了した場合」が未定義だっただけでも、後から見つかれば、DB、API、状態管理、UI、バックグラウンド処理、リトライ、テストまで一緒に直すことがあります。

qa-grillingは、QAを開発の後ろから前に持ってきます。

```text
Idea
  ↓
PRD / Design
  ↓
qa-grilling   ← ここで壊す
  ↓
Resolved Spec
  ↓
Implementation
  ↓
Runtime QA
  ↓
Release
```

## QAの探索方法

単純なチェックリストではなく、3軸を掛け合わせます。

```text
Feature × Quality × Event
```

動画アップロードなら、たとえばこうなります。

```text
upload × reliability × interruption
→ 73%でアプリがkillされたら？

upload × correctness × concurrency
→ 同じ動画を二重送信したら？

compression × resource × boundary
→ 端末ストレージがほぼ空いていない状態なら？
```

この方法なら、未知の機能でも「QA担当者が経験的に思いつく壊し方」を広く探索できます。

詳しくは [`references/exploration-model.md`](references/exploration-model.md) を参照してください。

## QA Lens

Core Lensでは、少なくとも次を見ます。

- 正常系・機能正当性
- 状態遷移・不正状態
- 入力・Validation・境界値・同値分割
- Data Integrity・永続化
- 二重実行・Race Condition・Idempotency
- Retry・Recovery・Cancel・Partial Failure
- Network・Timeout・再接続
- App / Browser Lifecycle
- Compatibility・Migration
- Performance・Memory・CPU・Storage・発熱・Battery
- Authentication・Authorization・Security・Abuse
- Privacy・PII・ログ
- Accessibility
- Localization・時刻・Timezone
- UX・誤操作・破壊的操作・エラー復帰
- Expectation・Trust・Anxiety・Confusion・User Control
- Observability・Supportability・Testability
- Release・Rollout・Rollback

全観点は [`references/qa-lenses.md`](references/qa-lenses.md) にまとめています。

## Domain Pack

すべての機能にすべての観点を薄く当てるのではなく、対象に応じて追加します。

- Mobile
- Web
- API / Distributed Systems
- Offline / Sync
- Media / Camera / Audio / Video
- Notification / Background Work
- Payment / Transaction
- AI / LLM
- Location / Sensor
- Authentication / Account Lifecycle
- Analytics / Experiment

詳しくは [`references/domain-packs.md`](references/domain-packs.md) を参照してください。

## Grilling

qa-grillingは、コードや仕様を読めば分かることをユーザーに聞きません。

本当に仕様判断が必要な場合だけ、1問ずつ聞きます。

```text
アップロード中断後の挙動が定義されていません。

推奨: upload sessionを永続化し、次回起動時に最後に確認できたoffsetから再開する。

理由: 大容量ファイルの再送を避けられ、ユーザーから見ても「中断 = 最初からやり直し」にならないためです。

中断したアップロードは自動再開する仕様でよいですか？
```

回答はDecision Ledgerに残してから次へ進みます。

詳しくは [`references/grilling-protocol.md`](references/grilling-protocol.md) を参照してください。

## 「指摘」を分ける

エッジケースが見つかったからといって、全部をバグ扱いしません。

- **Defect**: 設計上すでに矛盾・不正・危険がある
- **Ambiguity**: 複数の挙動が考えられるが意図が未定義
- **Missing rule**: 到達可能な状態・イベントに対する仕様がない
- **Test obligation**: 仕様は決まっているので、確認すべきテストとして残す
- **Observability gap**: 問題は起こり得るが、発生後に追えない
- **Accepted risk**: 意図的に残すことを決めたリスク

これによって「QAから指摘が100件出た」だけのレビューにならないようにします。

## 最終成果物

レビュー後は次を残します。

- QA Design Report
- P0 / P1 / P2 / P3 Findings
- Grillingで解決したDecision
- 未決事項
- Spec Changes
- Acceptance Criteria
- Test Obligations
- Observability Requirements
- Residual Risks

テンプレートは [`templates/qa-design-report.md`](templates/qa-design-report.md) にあります。

## 使い方

Agent Skillsに対応したコーディングエージェントのSkillディレクトリに、このリポジトリをコピーまたはcloneしてください。`SKILL.md` と `references/` の構造は維持してください。

あとは普通に依頼します。

```text
この機能を実装前にqa-grillingして。
```

```text
このPRDをqa-grillingでレビューして。あとでQAに指摘されそうな設計漏れを先に潰したい。
```

```text
このFigmaとAPI設計を実装前にgrillして。
```

```text
テストケースを先に作らず、まず設計がどう壊れるかをqa-grillingで探して。
```

## Example

- [`examples/video-upload-review.md`](examples/video-upload-review.md)
- [`examples/ui-form-review.md`](examples/ui-form-review.md)

## 原則

1. **質問する前に調べる。** 手元で分かることを人間に聞かない。
2. **テストを考える前にモデル化する。** 状態・Invariant・依存・データフローを把握する。
3. **件数よりリスク。** 汎用的な100指摘より、重要な10リスクを優先する。
4. **1回に1つ決める。** Grillingは集中でき、途中で止めても再開できる形にする。
5. **プロダクト仕様を勝手に作らない。** 推奨案は出すが、意思決定が必要なら明示する。
6. **QAを機能正当性だけにしない。** 信頼性、Privacy、Accessibility、Performance、運用性、ユーザーの信頼までQualityとして扱う。
7. **指摘で終わらない。** Spec、Acceptance Criteria、Test、Telemetryへつなげる。

## Inspiration

Grillingの考え方はこちらの記事を参考にしています。

https://zenn.dev/sato_frontend/articles/1a85841505b9bb

qa-grillingはQA向けに独立して設計したSkillで、元実装のforkではありません。
