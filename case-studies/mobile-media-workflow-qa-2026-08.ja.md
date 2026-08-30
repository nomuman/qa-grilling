# Case study: qa-grillingをモバイルメディア処理へ適用する

[English](mobile-media-workflow-qa-2026-08.md)

これは、撮影・外部メディア取り込み・アップロードを含むモバイルアプリへ `qa-grilling` を適用した公開用の編集記録です。対象プロジェクト、内部環境、実装識別子、アカウント情報は開示しません。

## 目的

通常時の成功だけでなく、次の失敗連鎖を実装前に見つけることを目的にしました。

```text
処理が失敗・中断する
  → 画面やプロセスが終了する
  → 状態が不明になる、または元データが失われる
  → 再試行できない、重複する、別の所有者へ混ざる
```

## Review profile

| 項目 | 内容 |
|---|---|
| Review depth | `standard` |
| Interaction | `interactive`で高リスクな判断を確認 |
| 主な観点 | state、persistence、retry、lifecycle、ownership、idempotency、cache、observability |
| Domain packs | mobile、media、files/imports、offline/sync、API/distributed |
| Skill | `qa-grilling v1.0.0` |

この記録では、対象リポジトリ名、commit、PR番号、内部テスト情報、バックエンド識別子、ローカルpathを意図的に省いています。

## Behavior model

### Actors and dependencies

- ユーザー: 撮影、取り込み、再試行、破棄、元データの削除を選択する
- モバイルアプリ: ローカルファイル、処理状態、永続キュー、キャッシュを管理する
- 外部メディア: 読み出し元であり、ユーザーが明示的に削除する対象でもある
- 認証、リモートストレージ、データベース: 所有者、メディア、メタデータのsource of truth
- OS管理のバックグラウンド処理: 画面やプロセスをまたぐ再開を担う

### States and transitions

```text
captured / imported
  → local copy or durable queue
  → processing / uploading
  → completed
       → explicit deletion, or keep
  → failed / retryable
       → retry with the same logical identity, or explicit discard
```

### Invariants

- 成功が確認できない元データは、再試行または明示的な破棄まで残る
- 元データの削除は、成功確認とユーザーの明示操作の後にだけ行う
- 所有者が変わった状態で、古い所有者向けの処理を開始しない
- 同じ論理処理の再試行で、別の結果を重複作成しない
- キャッシュは完全なデータだけを返し、期限切れや空のエントリを返さない
- 一時障害や遅い依存先で、画面全体が無期限に待ち続けない

## Findings and decisions

| Finding | 分類／優先度 | 決定 | 改善の要約 |
|---|---|---|---|
| F-001 | DEFECT / P1 | D-001 | 失敗・中断時に元データを保持し、再試行と明示的な破棄を可能にする |
| F-002 | DEFECT / P1 | D-002 | 状態と所有者を永続化し、画面終了後も安全に再開できるようにする |
| F-003 | DEFECT / P2 | D-003 | 再試行の論理IDを固定し、重複作成を防ぐ |
| F-004 | DEFECT / P2 | D-004 | キャッシュ書き込みをatomicにし、期限・容量・空データを扱う |
| F-005 | MISSING_RULE / P2 | D-005 | リスナー終了、ページング、大量データ、並列数に上限を設ける |
| F-006 | TEST_OBLIGATION / P2 | A-001 | 失敗、再試行、削除、再開、所有者境界をテストで固定する |

### F-001／F-002: durability and recovery

画面の寿命だけに処理を依存すると、エラー、バックグラウンド化、プロセス終了、ネットワーク断で「処理中」の状態が孤児化します。先に元データを削除すると、失敗がそのままデータ消失になります。

改善後は、失敗した処理をユーザーが確認でき、元データを保持したまま再試行または破棄を選べます。OSのバックグラウンド実行機構と永続状態を使い、画面の終了と処理の終了を分離しました。

### F-003: ownership and idempotency

再開時に認証ユーザーが変わる可能性や、再試行で新しいIDを発行する可能性を確認しました。これらは、別所有者への混入や同じメディアの重複作成につながります。

改善後は、処理の所有者と論理IDを保持し、開始前に所有者を確認します。再試行は同じ論理IDを使います。

### F-004／F-005: cache and dependency boundaries

直接書き込まれたキャッシュは、読み手から部分データに見える可能性があります。また、一時的なリスナー終了や無制限の取得は、空表示、無期限待機、過剰なリソース使用につながります。

改善後は、完全な一時ファイルをcache slotへ移す方式にし、期限・容量・空データを検査します。再接続、ページング、並列数にも上限を置きます。

## Decision ledger

| ID | 決定 | 理由 |
|---|---|---|
| D-001 | 成功確認前は元データを削除しない | 復旧不能なデータ消失を避ける |
| D-002 | 状態と所有者を永続化する | OS lifecycleとアカウント切替に耐える |
| D-003 | 再試行では論理IDを再利用する | 重複作成を防ぐ |
| D-004 | キャッシュはatomicに保存する | 部分データを読ませない |
| D-005 | 再接続、ページング、並列数に上限を置く | 一時障害と大量データの影響を限定する |

## Before / After

| 観点 | Before | After |
|---|---|---|
| 失敗時 | 状態や元データの扱いが不明確 | 保持、可視化、再試行、明示的破棄 |
| lifecycle | 画面終了と処理終了が結び付いていた | 永続状態とOS管理処理で分離 |
| ownership | 再開時の所有者境界が暗黙的 | 開始前に所有者を確認 |
| retry | 重複作成の可能性があった | 論理IDを再利用 |
| cache | 部分書き込みや空データの境界が弱い | atomic保存、期限・容量・空データ検査 |
| dependency | 終了・大量取得・無制限並列への規則が不足 | bounded retry、pagination、concurrency上限 |

## Acceptance criteria

```text
AC-001: 失敗または中断した処理は、元データを保持したまま再試行または明示的な破棄を選べる。
AC-002: 元データの削除は、成功確認後の明示操作に限定される。
AC-003: 画面やプロセスが終了しても、永続状態から安全に処理を再開できる。
AC-004: 同じ論理処理の再試行は同じ論理IDを使い、意図しない重複を作らない。
AC-005: キャッシュ読み取りは完全なデータだけを返し、期限切れ・空データを除外する。
AC-006: 一時障害、大量データ、遅い依存先に対して、再接続・取得量・並列数の上限が働く。
AC-007: 検証結果はlocal、device/E2E、CI、release、blockedを混同しない。
```

## Test obligations

- T-001: 失敗、timeout、cancel、background、process termination後の元データ保持
- T-002: 再試行、破棄、成功後の削除、削除失敗時の再試行
- T-003: アカウント切替、認証期限切れ、owner mismatch、同一論理IDの再試行
- T-004: 重複ファイル名、malformed input、空データ、期限、容量超過、atomic store
- T-005: リスナー終了、再接続上限、ページング、空データ、遅延データ、大量データ
- T-006: 実機の外部メディア、OS lifecycle、ネットワーク断、バックグラウンド復帰

## Evidence coverage

| Evidence | Verification class | 状態 |
|---|---|---|
| 構造確認、unit test、差分確認 | static/local | pass |
| サポート対象端末での外部メディア・lifecycle確認 | live-host/device/E2E | blocked / unverified |
| main向け自動検証 | CI | 環境依存。local passで代替しない |
| 配布後の実環境・production traffic | release/production | 未確認 |

## Residual risks

- 実機固有の外部メディア、権限、background制限はlocal testだけでは保証できない
- 認証、リモートストレージ、OSの制約が変わると、再試行の結果がunknownになる可能性がある
- キューの長期滞留、端末容量、運用上の手動recoveryは別途監視が必要
- 本番設定や配布後の挙動は、local／CIの結果から推測しない

## Adoption judgment

`qa-grilling` は、通常時のテスト一覧ではなく、失敗イベントと守るべき不変条件を起点に、実装と検証の抜けを整理するのに有効でした。

この公開版では、採用判断に必要な方法と結果の型だけを残し、対象プロジェクトを特定できる情報や内部情報は省いています。case study自体もdevice、CI、release、productionの証明にはならないため、各環境のgateは別に実施します。
