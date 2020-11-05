**Private-LTE-Simulator**

鈴鹿高専専攻科特別研究

# ファイル構造
要点だけピックアップ

```
Private-LTE-Simulator/
│
├── data/
│      ├── oaisim/
│      └── srslte/
│
├── docker/
│      ├── oaisim/
│      │      ├── Dockerfile
│      │      ├── Dockerfile_for_base
│      │      └── docker-compose.yml
│      ├── srslte/
│      │      ├── Dockerfile
│      │      └── docker-compose.yml
│      └── docker-compose.yml
│
└── README.md

```

# Docker ビルド手順

ディレクトリは雰囲気で置き換え理解お願いします。
`~`=`Private-LTE-Simulator/`

## 1. `oaisim`イメージを作成する

ビルド時間短縮のため共通のイメージを作成し、継承することにする
まず、

```bash
cd ~/docker/oaisim
docker-compose up --build -d
docker exec -it oaisim bash
```

作業終了後、イメージを作成する

```bash
docker-compose stop
docker commit oaisim_image:latest
```

## 2. `srslte`イメージを作成する

ビルド時間短縮のため共通のイメージを作成し、継承することにする
まず、

```bash
cd ~/docker/srslte
docker-compose up --build -d
docker exec -it srslte bash
```

作業終了後、イメージを作成する

```bash
docker-compose stop
docker commit srslte_image:latest
```

## 3. 作成したイメージ2つをdocker-composeで起動
```bash
cd ~/docker
docker-compose up --build -d
```
