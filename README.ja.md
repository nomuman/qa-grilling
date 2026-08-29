# qa-grilling

[English](README.md)

`qa-grilling` は、仕様や設計を実装前にQAするためのAgent Skillです。

状態漏れ、境界値、通信失敗、二重実行、データ消失、権限、アクセシビリティ、性能、プライバシーなど、実装後のQAで見つかりやすい問題を先に探します。

Grillingの考え方をベースにしていますが、見るポイントはシンプルです。

> この設計は、どう壊れるか？

## 対象

次のようなものをレビューできます。

- PRD、仕様書
- Issue、User Story
- Figma、画面遷移
- API仕様
- アーキテクチャ
- 実装計画
- 既存コード

## 進め方

1. 仕様、設計、コード、既存テストを読む
2. 状態、遷移、データ、副作用、依存関係を整理する
3. 複数のQA観点から壊れ方を探す
4. リスク順に並べる
5. 仕様判断が必要なものだけ、1問ずつ確認する
6. 仕様変更、Acceptance Criteria、テスト観点に落とす

探索には `Feature × Quality × Event` を使います。

たとえば動画アップロードなら:

```text
upload × reliability × interruption
→ アップロード中にアプリが終了したらどうなる？

upload × correctness × concurrency
→ 同じ動画を二重送信したらどうなる？
```

チェックリストを上から消化するのではなく、対象の機能に合わせて壊れ方を探します。

## QA観点

主に次を確認します。

- 状態遷移
- 境界値、不正入力
- Retry、Cancel、Recovery
- Network、Timeout
- 二重実行、Concurrency、Idempotency
- 永続化、Data Integrity
- App / Browser Lifecycle
- Compatibility、Migration
- Performance、Memory、Storage、Battery
- Security、Privacy
- Accessibility、Localization
- UX、破壊的操作、誤操作
- ユーザーの信頼、安心感、コントロール感
- Observability、Supportability
- Rollout、Rollback

対象に応じて、Mobile、Web、API、Offline Sync、Media、Notification、Payment、AI、Location、Authentication、Analytics向けの観点も追加します。

詳しくはこちらです。

- [`references/qa-lenses.md`](references/qa-lenses.md)
- [`references/domain-packs.md`](references/domain-packs.md)
- [`references/exploration-model.md`](references/exploration-model.md)

## 出力

レビュー結果として、必要に応じて次を残します。

- 優先度付きの指摘
- 未決事項
- 仕様変更
- Acceptance Criteria
- テスト観点
- Observability Requirements
- 残るリスク

テンプレート: [`templates/qa-design-report.md`](templates/qa-design-report.md)

## 使い方

Agent Skillsに対応したコーディングエージェントのSkillディレクトリに、このリポジトリをコピーまたはcloneします。

あとは普通に依頼します。

```text
この機能を実装前にqa-grillingして。
```

```text
このPRDをqa-grillingでレビューして。あとでQAに指摘されそうなところを先に見つけて。
```

```text
このFigmaとAPI設計を実装前にレビューして。
```

## Example

- [`examples/video-upload-review.md`](examples/video-upload-review.md)
- [`examples/ui-form-review.md`](examples/ui-form-review.md)

## Grilling

仕様、設計、コード、既存テストを読めば分かることは質問しません。

それでも決まっていないことだけ、1問ずつ確認します。回答は記録してから次に進みます。

詳しくは [`references/grilling-protocol.md`](references/grilling-protocol.md) を参照してください。

## Inspiration

Grillingの考え方はこちらの記事を参考にしています。

https://zenn.dev/sato_frontend/articles/1a85841505b9bb

`qa-grilling` はQA向けに独立して作ったSkillで、元実装のforkではありません。
