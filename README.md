# 特記事項

## データベース
- マイグレーションの作成: `python manage.py makemigrations`
  - posts/migrations/0001_initial.py
  - posts/migrations/0002_auto_20200908_0228.py
  - posts/fixture/sample.json
- マイグレーションの実行: `python manage.py migrate`
- 管理者の追加: `python manage.py createsuperuser`
- データベースの削除: `rm -d -r db.sqlite3` (*DBをPostgreSQLにした後変更する必要あり)

## ルーティング
|-- /admin : 管理者ページ \
| \
|--(ユーザー認証周りのルーティング) \
| \
|-- /posts : 投稿一覧 \
|　　|-- /{post_id} : 投稿詳細 \
|　　| \
|　　|-- /create : 投稿 \
|　　| \
|　　|-- /edit/{post_id} : 投稿編集 \
|　　| \
|　　|-- /delete/{post_id} : 投稿削除 \
|　　| \
|　　|-- /hoge/{post_id} : コメント作成
