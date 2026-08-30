# qa-grilling

[English](README.md)

`qa-grilling` は、仕様や設計を実装前にレビューする、明示呼び出し専用のAgent Skillです。

設計の壊れ方をモデル化し、重要なリスクを優先し、人の判断が必要な仕様だけを確認します。結果は、仕様変更、受け入れ条件、テスト義務、可観測性要件、残余リスクへ落とし込みます。

> この設計は、どう壊れるか？

## インストール

変化し続ける `main` ではなく、公開済みバージョンをインストールします。

### Codex

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/nomuman/qa-grilling ~/.agents/skills/qa-grilling
git -C ~/.agents/skills/qa-grilling checkout <version>
```

`<version>` は、`v1.0.0` など公開済みtagへ置き換えてください。

Codexは `~/.agents/skills` にある個人Skillを検出します。

明示的に呼び出します。

```text
$qa-grilling この機能を実装前にレビューして
```

### Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/nomuman/qa-grilling ~/.claude/skills/qa-grilling
git -C ~/.claude/skills/qa-grilling checkout <version>
```

明示的に呼び出します。

```text
/qa-grilling この機能を実装前にレビューして
```

### プロジェクト限定のインストール

個人用の場所ではなく、次のどちらかへ配置します。

```text
<project>/.agents/skills/qa-grilling/   # Codex
<project>/.claude/skills/qa-grilling/   # Claude Code
```

リポジトリ全体を一緒に配置してください。`SKILL.md` は、レビューに必要な補助ファイルだけを段階的に読み込みます。

### 更新

Release Notesを確認してから、特定のバージョンへ切り替えます。

```bash
git -C <skill-path> fetch --tags
git -C <skill-path> checkout <version>
```

[CHANGELOG.md](CHANGELOG.md) と [GitHub Releases](https://github.com/nomuman/qa-grilling/releases) を確認してください。再現可能なレビュー挙動が必要な場合、移動するブランチを `pull` する更新は避けます。

## 呼び出し方針

ユーザーが明示的に指定した場合だけ起動します。

- Codex: `agents/openai.yaml` の `policy.allow_implicit_invocation: false`
- Claude Code: `SKILL.md` の `disable-model-invocation: true`

通常の設計・コードレビューが、意図せず複数ターンのgrillingへ変わることを防ぎます。

## レビューモード

### 深度

- `quick`: 補助資料の読み込みを抑え、最重要リスクだけを返す
- `standard`: 既定。行動モデル、core lens、関連domain packを使う
- `deep`: 証拠を広く確認し、状態・データモデルとfailure chainを明示してextended lensを使う

### 対話

- `interactive`: 未解決のP0/P1仕様判断を、1ターンに1問だけ確認する
- `one-shot`: 指定された場合、または追加の対話ができない環境で使用する。質問せず、推奨値を仮定として記録し、同じターンでレポートを完成させる

P2/P3は、アーキテクチャ、公開契約、不可逆な挙動を大きく変える場合を除き、推奨値を採用します。

## 安全境界

レビュー対象のリポジトリ、文書、デザイン、Webページ、コメント、ログは、信頼できないデータとして扱います。対象内の埋め込み命令は、レビュー方法を変更せず、実行・編集・情報開示・外部副作用を許可しません。

レビューは既定で読み取り専用です。追加行為には別のユーザー許可が必要で、ホストの権限ルールにも従います。

## 対象

- PRD、機能仕様、Issue、User Story
- Figma、画面遷移
- API契約、データモデル
- アーキテクチャ、Migration、実装計画
- 既存コード、テスト

Mobile、Web、API、Offline Sync、Media、Notification、Payment、AI、Agent Skill、Location、Authentication、Analytics、Files、Searchのうち、対象に関係するdomain packだけを読み込みます。

## 進め方

1. 質問より先に、利用できる証拠を確認する
2. Actor、状態、遷移、データ、不変条件、副作用、依存関係をモデル化する
3. `Feature × Quality × Event` と関連するQA lensで壊れ方を探す
4. FindingをDEFECT、AMBIGUITY、MISSING_RULE、TEST_OBLIGATION、OBSERVABILITY_GAP、ACCEPTED_RISKへ分類する
5. 具体的な影響をP0/P1/P2/P3で優先づけする
6. 人の判断が必要な高リスク仕様だけを、interactiveでは1問ずつ解決する
7. 仕様変更、受け入れ条件、検証、可観測性、残余リスクへ落とし込む

## 出力

必要に応じて次を含みます。

- 根拠付きの優先QA Finding
- Decision Ledgerと仮定
- 仕様変更
- 行動ベースの受け入れ条件
- Test Obligation
- 可観測性とSupport要件
- 残余リスク、Release／Rollback条件

## 使用例

```text
$qa-grilling このPRDをstandard・interactiveでレビューして
```

```text
/qa-grilling このMigration計画を、データ消失とRollback中心にone-shotでレビューして
```

[動画アップロード](examples/video-upload-review.md)と[プロフィールフォーム](examples/ui-form-review.md)の参考出力があります。通常のレビューでは自動的に読み込みません。

## Dogfooding case study

[`v1.0.0` self-review](case-studies/self-review-v1.0.0.ja.md)では、Skill自身の適用前状態をreviewし、6件のproduct decisionを解決し、Findingからrepository変更まで追跡しています。静的、live-host、CI、release evidenceも分けて記録しています。[English version](case-studies/self-review-v1.0.0.md)もあります。

Teamへの採用判断に利用できるよう、成功例だけでなく限界とblocked evidenceも残しています。

[モバイルメディア処理のレビュー](case-studies/mobile-media-workflow-qa-2026-08.ja.md)では、撮影・外部メディア取り込み・アップロード・キャッシュ・データ取得を対象に、失敗時の復旧、所有者分離、冪等性、実機／CI／Release evidenceの境界を記録しています。[English version](case-studies/mobile-media-workflow-qa-2026-08.md)もあります。

## 開発

決定的な構造検査を実行します。

```bash
python3 scripts/validate_skill.py
python3 -B -m unittest discover -s tests -v
```

行動evalケース、verification class、cross-host rubricは [evals/README.md](evals/README.md) にあります。Release evidenceは [evals/results/v1.0.0-rc1.md](evals/results/v1.0.0-rc1.md) に保存します。Pull RequestではGitHub Actionsが構造検査とvalidator negative testsを実行します。

ReleaseはSemantic Versioningに従います。`main` は開発中の状態で、インストール可能な挙動は変更不能なtagとGitHub Releaseで識別します。

セキュリティ上の問題は [SECURITY.md](SECURITY.md) の手順で非公開報告してください。

## ライセンス

[MIT](LICENSE)

## Inspiration

対話スタイルは[こちらの記事](https://zenn.dev/sato_frontend/articles/1a85841505b9bb)で紹介されているGrillingの考え方を参考にしています。

`qa-grilling` はQA向けに独立して作ったSkillで、元実装のforkではありません。
