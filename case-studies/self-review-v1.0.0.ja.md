# Case study: qa-grillingを自分自身へ適用する

[English](self-review-v1.0.0.md)

これは、`qa-grilling`自身を`v1.0.0`公開前にレビューしたdogfoodingの公開用記録です。Skillが何を発見し、どの判断を人へ確認し、リポジトリがどう変わり、どこまで実証できたかを追えるように編集しています。

生の会話全文ではありません。非公開context、ローカルpath、account情報、レビューと無関係なhost診断は除外しています。

## このcase studyの目的

採用判断には、整った出力例だけでなく次の証拠が必要です。

- Skillは自分自身のinstructionsやrelease processの欠陥を見つけられるか
- grillingは終わりのない質問ではなく、明確なDecisionへ進むか
- Findingが変更と検証へつながったか
- 公開品質を主張できるだけの証拠があるか

## Review対象

- 適用前commit: [`38df618`](https://github.com/nomuman/qa-grilling/commit/38df618facdc572ec82f0f32e7a2d2e006a0de77)
- Candidate label: [PR #1](https://github.com/nomuman/qa-grilling/pull/1)上の`v1.0.0-rc1`
- 公開予定のimmutable release: `v1.0.0`。tagとGitHub Releaseが存在するまではrelease evidenceではない
- Review形式: interactive、その後に実装とone-shot release-candidate評価
- 主なartifact: `SKILL.md`、references、examples、日英README、repository metadata、release設定

公開用に整理した同等の入力例:

```text
$qa-grilling このSkill自身をdeepで公開前レビューしてください。
起動条件、安全境界、context効率、host互換性、eval品質、release integrityを重視し、
人の判断が必要な高リスクDecisionだけを1問ずつ確認してください。
```

## Grillingで確定したDecision

| Decision | 結論 | 意味 |
|---|---|---|
| D-001 | Codex／Claude Codeとも明示呼び出し専用 | 通常reviewが意図せず複数turnのgrillingへ変わらないようにする |
| D-002 | MIT License | 採用・改変・再配布の権利を明確にする |
| D-003 | Semantic Versioning、変更不能tag、Release、changelog | Review挙動を再現・rollback可能にする |
| D-004 | 深度・domain別のprogressive disclosure | 大きなcatalogより、対象証拠へcontextを使う |
| D-005 | interactiveは原則P0/P1だけを質問し、one-shotは質問で停止しない | 対話と非対話の両方で完了可能にする |
| D-006 | 既定深度は`standard` | 通常利用でbehavior modelを作りつつdeep auditのcostを強制しない |

## Findingから変更・検証まで

| Finding ID | Decision／assumption | Changed artifact | Acceptance／test | Verification status |
|---|---|---|---|---|
| F-001 | defect。product decision不要 | `SKILL.md` safety boundary | AC-001: artifact内命令はauthorityを付与しない。E-006／E-007 | static/local pass。live-host negative smokeが必要 |
| F-002 | D-002 | `LICENSE`、`scripts/validate_skill.py` | AC-002: MIT artifactが存在しvalidationに合格 | static/local pass |
| F-003 | D-001 | `agents/openai.yaml`、`SKILL.md` | AC-003: 明示起動し、通常reviewでは非起動。E-019 | Codex明示起動はpass。暗黙非起動とClaude runはblocked／unverified |
| F-004 | D-003 | `CHANGELOG.md`、READMEs、release workflow | AC-004: 公開installがimmutable `v1.0.0`へ解決 | tag、Release、公開後installまでblocked |
| F-005 | D-004／D-006 | `SKILL.md`、`references/domains/*` | AC-005: E-008が関連packだけを読む | static/local pass。Codex routing smoke pass |
| F-006 | implementation assumption A-001 | `scripts/validate_skill.py`、`tests/`、workflow、`evals/` | AC-006: negative fixtureとcandidate CIがpass | local negative tests pass。最終candidate CIが必要 |
| F-007 | defect。product decision不要 | READMEs | AC-007: examplesとcase studyをruntime routingから外す | static/local pass |
| F-008 | implementation assumption A-002 | `SKILL.md`、report template、`evals/results/` | AC-008: verification classを代替しない | static/local pass |
| F-009 | implementation assumption A-003 | `references/domains/agent-skills.md` | AC-009: E-021でAgent Skill観点をactivate | static/local pass。Codex live routing pass |
| F-010 | implementation assumption A-004 | `SKILL.md`、E-016／E-017 | AC-010: 無関係なアクセス可能contextを検査・報告しない | 隔離Codex smoke pass。Claudeが必要 |
| F-011 | implementation assumption A-005 | `SKILL.md`、E-015 | AC-011: quick reviewはfocusを保つ | policyとtestを追加。before／after効率改善は未検証 |
| F-012 | implementation assumption A-006 | report template | AC-012: 大きなreviewでFindingからevidenceまで対応づける | static/local pass。採用者usabilityは未測定 |

## Before／After

適用前は、広いmonolithic promptであり、明示起動policy、安全境界、License、決定的validator、CI、変更不能release、cross-host rubricがありませんでした。

`v1.0.0`候補では次を備えます。

- 両hostの明示起動metadata
- untrusted inputとread-only reviewの境界
- 停止条件を持つdepth／interaction mode
- core lensと選択的domain pack
- Agent Skill専用QA pack
- evidence coverageとend-to-end traceability
- negative tests付き構造validation
- 22件のbehavior caseと永続的なRC evidence
- MIT、security reporting、changelog、CI、immutable release手順

## Evidenceと限界

| Verification class | Evidence | 限界 |
|---|---|---|
| static/local | repository validator、negative fixture、Markdown／YAML検査、独立rubric review | 静的検査だけではhost挙動を証明できない |
| live-host/device/E2E | Codexの明示起動とadversarial one-shot smoke | 暗黙非起動とcalibration修正後の最終candidateは未実行 |
| blocked/unverified、target: live-host | Claude Code 2.1.251は導入済みだが未認証 | cross-host認定前に認証を使う実動確認が必要 |
| CI | Pull Request validation | CIは実行したcheckだけを証明する |
| release/production | tag installと公開後smoke | 公開後に初めて取得できる証拠 |

未検証やblockedを隠さず残します。Dogfoodingは有効ですが、作者と同じ前提を共有するbiasがあります。独立評価とcross-host確認は別に必要です。

## 採用判断

実装前に高リスクな仕様の曖昧さを解決し、Acceptance Criteria、verification、observability、residual riskへ落としたいteamに向いています。

Domain expert、法務・Safety review、device/E2E、CI、release validation、production evidenceの代替ではありません。Review依頼を理由にcommand実行やsystem変更を許可するSkillでもありません。

公開gateは[behavior rubric](../evals/README.md)と[`v1.0.0` release-candidate record](../evals/results/v1.0.0-rc1.md)で確認できます。
