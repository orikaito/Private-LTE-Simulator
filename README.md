Private-LTE-Simulator

鈴鹿高専専攻科特別研究

# ファイル構造
要点だけピックアップ
```
Private-LTE-Simulator/
├── data/
│      ├── oaisim1/
│      └── oaisim2/
└── docker/
        ├── ubuntu-original-base/
        └── docker-compose.yml

```

# Docker ビルド手順

ディレクトリは雰囲気で

## 1. `ubuntu-original-base`イメージを作成する

ビルド時間短縮のため共通のイメージを作成し、継承することにする
まず、

```bash
cd docker/ubuntu-original-image
docker-compose up --build -d
docker exec -it oaisim bash
```
<!--docker build ./ -t ubuntu-original-base-->

作業終了後、イメージを作成する

```bash
docker-compose stop
docker commit oaisim_image:latest
```

## 2. あとはdocker-composeにおまかせ
```bash
cd ..
docker-compose up --build -d
```