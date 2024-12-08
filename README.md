# mailbot

### 開発環境

| 名前         | バージョン    |
|------------|----------|
| rockylinux | 9.5      |
| Python     | 3.12     |
| minio      | 1.9      |
| mysql      | 8.0+     |
| PyCharm    | 2023.3.3 |

### ディレクトリ構造

| ディレクトリ名/ファイル名                                          | 説明                |
|--------------------------------------------------------|-------------------|
| api                                                    | 各種APIロジックを格納      |
| libs                                                   | 依存ライブラリ、データベースモデル |
| tmp                                                    | 添付ファイルキャッシュ       |
| config.py                                              | 各種設定              |
| main.py                                                | メインプログラム          |
| db-list-structure.sql                                  | データベーステーブル構造      |
| docker-compose.yaml                                    | Docker一括デプロイ      |
| Dockerfile                                             | イメージ作成設定          |
| mailbot.yaml, mariadb.yaml, minio.yaml, namespace.yaml | k8s Pods設定ファイル    |

### Docker/Kubernetes環境変数リスト

| 名前                   | 説明                     | パラメータタイプ      |
|----------------------|------------------------|---------------|
| DB_URL               | データベースURL              | string        |
| UVICRON_HOST         | Uvicornリスニングアドレス       | string        |
| UVICRON_PORT         | Uvicornリスニングポート        | int           |
| UVICRON_DEBUG        | Uvicorn/FastAPIデバッグモード | string on/off |
| AWS_ENDPOINT         | S3バケットアドレス             | string        |
| AWS_ACCESS_KEY       | S3バケットアクセスキー           | string        |
| AWS_SECRET_KEY       | S3バケットシークレットキー         | string        |
| AWS_BUCKET_NAME      | S3バケット名                | string        |
| MAIL_USER            | メールユーザー名               | string        |
| MAIL_PASSWORD        | メールパスワード               | string        |
| MAIL_FROM            | メール送信元アドレス             | string        |
| MAIL_SERVER          | メールサーバー                | string        |
| MAIL_PORT            | メールサーバーポート             | string        |
| MAIL_SEND_SLEEP_TIME | メール送信間隔 (秒)            | int           |

# インターフェースURI説明

| URI            | リクエスト方法 | 説明                    |
|----------------|---------|-----------------------|
| /api/docs      | GET     | Swaggerインターフェースドキュメント |
| /api/redoc     | GET     | Redocインターフェースドキュメント   |
| /api/mail/send | POST    | メール送信                 |
| /api/mail/get  | GET     | 送信メール履歴情報取得           |

### レスポンスステータスコード説明

| ステータスコード | 説明      |
|----------|---------|
| 200      | OK      |
| 500      | サーバーエラー |

### ホスト環境でのデプロイ

```
1. MySQLとMinIOをインストール
2. テーブル構造をデータベースにインポート
3. MinIOでバケットとリージョンを作成
$ pip install -r requirements.txt
$ python main.py
```

### コンテナデプロイ

### イメージビルド

```
$ docker build -t xxx:latest .
```

docker-compose.yaml

```
version: '3.8'
services:
  minio:
    image: minio/minio:latest
    container_name: minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      - MINIO_ROOT_USER=adminadmin
      - MINIO_ROOT_PASSWORD=adminadmin
    volumes:
      - /root/minio-data:/data
      - /root/minio-data/config:/root/.minio
    command: server /data --console-address ":9001"
    restart: always
  mariadb:
    image: mariadb:latest
    container_name: mariadb
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: 111111
      MYSQL_DATABASE: mailbot
      MYSQL_USER: mailboot
      MYSQL_PASSWORD: 111111
    volumes:
      - /root/mysql-data:/var/lib/mysql
    restart: always
  mailbot:
    container_name: mailbot
    image: mailbot:latest
    environment:
      - DB_URL=mysql://root:111111@mariadb:3306/mailbot
      - UVICRON_HOST=0.0.0.0
      - UVICRON_PORT=8000
      - UVICRON_DEBUG=on
      - AWS_ENDPOINT=http://minio:9000
      - AWS_ACCESS_KEY=adminadmin
      - AWS_SECRET_KEY=adminadmin
      - AWS_BUCKET_NAME=email-attachment-file
      - MAIL_USER=no-reply@aizhao.pro
      - MAIL_PASSWORD=tfMrFVxaP3U64tab8sPa
      - MAIL_FROM=no-reply@aizhao.pro
      - MAIL_SERVER=smtp.qiye.aliyun.com
      - MAIL_PORT=465
      - MAIL_SEND_SLEEP_TIME=10

```

```
$ docker-compose up -d
```

### Kubernetesデプロイ

```
1. minikubeでKubernetesのコンポーネント、etcd、Calicoをインストールし、CoreDNSの外部DNS、Nginx proxy_passを設定する。
2. 名前空間を設定
3. YAMLファイルを作成し、レプリカセット、アンチアフィニティポリシー、クラスター、およびNodePortを定義
4. Podを実行: kubectl apply -f xxx.yaml
5. データベーステーブル構造をMySQLにインポートし、MinIOのバケットとリージョンを設定する。
5. トラブルシューティング: kubectl describe pod pod名前 -n namespace
6. Podログを確認: kubectl logs -f pod名前 -n namespace
```

### プログラムのプロセス

```
1. フロントエンドで送信ボタンがクリックされると、ファイルのMD5値を計算し、ファイル名をMD5値に変更してオブジェクトストレージにアップロードする。  
2. 受信者、実際の添付ファイル名、対応するMD5値、メール本文情報をAPI/mail/sendインターフェースに送信する。  
3. サーバー側ではAPI/mail/sendインターフェースでJSON情報を受け取り、メールデータ、添付ファイルの実際のファイル名とMD5値の対応、メール送信フラグをデータベースに保存する。  
4. send_mail関数を用いてオブジェクトストレージからすべての添付ファイルをダウンロードし、MD5値のファイル名を実際のファイル名に変更する。  
5. メールを1対1で送信し、複数の添付ファイルがある場合はリスト形式で追加する。  
6. すべてのメール送信が完了すると、送信成功をフロントエンドに返し、送信済みフラグをデータベースに保存する。  
```