# qa-grilling

[English](README.md)

`qa-grilling` は、仕様や設計を実装前にQAするためのAgent Skillです。

状態漏れ、境界値、通信失敗、二重実行、データ消失、権限、アクセシビリティ、性能、プライバシーなど、実装後のQAで見つかりやすい問題を先に探します。

> この設計は、どう壊れるか？

## インストール

### Codex

自分の環境で常に使えるようにする場合:

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/nomuman/qa-grilling ~/.agents/skills/qa-grilling
```

Codexは `~/.agents/skills` にあるSkillを読み込みます。

インストール後は、Codexでそのまま使えます。

```text
$qa-grilling を使って、この機能を実装前にレビューして
```

PRD、実装計画、Figmaの情報、コードなどと一緒に依頼してください。

更新するとき:

```bash
git -C ~/.agents/skills/qa-grilling pull
```

### Claude Code

自分の環境で常に使えるようにする場合:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/nomuman/qa-grilling ~/.claude/skills/qa-grilling
```

Claude Codeは `~/.claude/skills` にあるSkillを読み込みます。

インストール後は:

```text
/qa-grilling
```

で直接呼び出せます。

普通に文章で依頼しても使えます。

```text
qa-grillingを使って、この機能を実装前にレビューして
```

更新するとき:

```bash
git -C ~/.claude/skills/qa-grilling pull
```

### 特定のプロジェクトだけで使う

Codexの場合:

```text
<project>/.agents/skills/qa-grilling/
```

Claude Codeの場合:

```text
<project>/.claude/skills/qa-grilling/
```

`SKILL.md` だけではなく、このリポジトリ全体を配置してください。`references/`、`templates/`、`examples/` もSkillから参照します。

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

## 主なQA観点

- 状態、状態遷移
- 境界値、不正入力
- 通信失敗、Retry
- 二重実行、Race Condition
- 永続化、Data Integrity
- App / Browser Lifecycle
- Compatibility、Migration
- Performance、Memory、Storage、Battery
- Security、Privacy
- Accessibility
- UX、誤操作、破壊的操作
- ユーザーの不安、信頼、Control
- Observability、Recovery

Mobile、Web、API、Offline Sync、Media、Notification、Payment、AI、Location、Authentication、Analyticsなどは、対象に応じて追加で確認します。

詳しくは:

- [`references/qa-lenses.md`](references/qa-lenses.md)
- [`references/domain-packs.md`](references/domain-packs.md)
- [`references/exploration-model.md`](references/exploration-model.md)

## 出力

レビュー後は必要に応じて次を残します。

- 優先度付きQA指摘
- 未決の仕様判断
- 仕様変更
- Acceptance Criteria
- Test Obligations
- Observability Requirements
- Residual Risks

レポートのテンプレートは [`templates/qa-design-report.md`](templates/qa-design-report.md) にあります。

## 使い方の例

```text
$qa-grilling を使って、このPRDを実装前にレビューして
```

```text
このFigmaをqa-grillingして。あとでQAに指摘されそうなところを先に探して
```

```text
この実装計画をqa-grillingして。データ消失と復旧を重点的に見て
```

レビュー例:

- [`examples/video-upload-review.md`](examples/video-upload-review.md)
- [`examples/ui-form-review.md`](examples/ui-form-review.md)

## Inspiration

Grillingの考え方はこちらの記事を参考にしています。

https://zenn.dev/sato_frontend/articles/1a85841505b9bb

`qa-grilling` はQA向けに独立して作ったSkillで、元実装のforkではありません。
