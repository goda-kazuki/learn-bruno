# Postman vs Bruno 比較（実践ベース）

このリポジトリで実際に検証した機能をもとに、Postman との違いをまとめる。

## 全体比較

| 観点           | Postman                          | Bruno                            |
| -------------- | -------------------------------- | -------------------------------- |
| 保存形式       | JSON（クラウド or エクスポート） | `.bru` テキストファイル          |
| バージョン管理 | クラウド履歴 / Git 連携は手動    | そのまま Git 管理                |
| 編集方法       | GUI のみ                         | GUI + テキストエディタ + AI 生成 |
| 実行順序       | Runner で並べ替え                | `meta.seq` でファイル内に定義    |
| 環境変数       | GUI で設定                       | `environments/*.bru` ファイル    |
| CLI            | `newman`                         | `@usebruno/cli`                  |

## テスト機能の対応表

| 機能             | Postman                 | Bruno                                 |
| ---------------- | ----------------------- | ------------------------------------- |
| 簡易アサーション | JS で記述               | `assert` ブロック（宣言的）           |
| スクリプトテスト | `pm.test()` + Chai      | `test()` + Chai                       |
| Pre-request      | Pre-request Script タブ | `script:pre-request` ブロック         |
| Post-response    | Tests タブ              | `script:post-response` ブロック       |
| 変数セット       | `pm.variables.set()`    | `bru.setVar()` / `vars:post-response` |

## Bruno 固有の宣言的記法

Postman では JS が必須な処理を、Bruno では宣言的に書ける。

```bru
# アサーション（Postman だと pm.test() で 10 行かかる）
assert {
  res.status: eq 200
  res.body.name: eq New Item
  res.body.id: isNumber
}

# 変数抽出（Postman だと pm.variables.set() が必要）
vars:post-response {
  itemName: res.body.name
}
```

## まとめ

| 観点             | Postman の強み      | Bruno の強み                              |
| ---------------- | ------------------- | ----------------------------------------- |
| ファイル管理     | GUI で完結          | Git フレンドリー、テキスト編集・AI 生成可 |
| テスト記述       | 慣れた `pm.*` API   | `assert` / `vars` の宣言的記法            |
| 実行順制御       | Runner の柔軟な制御 | `seq` + フォルダ分けのシンプルな構成      |
| コラボレーション | クラウド共有        | Git ベースの共有                          |
