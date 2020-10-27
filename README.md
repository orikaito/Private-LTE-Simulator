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

## 1. `ubuntu-original-base`イメージを作成する

ビルド時間短縮のため共通のイメージを作成し、継承する

```bash
cd docker/ubuntu-original-image
docker build ./ -t ubuntu-original-base
```

## 2. あとはdocker-composeにおまかせ
```bash
docker-compose build
docker-compose up -d
```