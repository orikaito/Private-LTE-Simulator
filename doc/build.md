# 環境構築

[READMEに戻る](../README.md)

## 1.1 EPC + eNB  (Careerルート)

Ubuntu 18.04 Server版をインストール  

システム構成図を参考にVirtualBoxイメージの設定からネットワークを設定

- インターネット接続用NAT（環境構築終了後オフにする）
- ホストオンリーネットワーク2つ
- 内部ネットワーク1つ

ネットワーク設定

 ```bash
sudo cp ./data/99-manual.yaml /etc/netplan/
sudo netpaln apply
```

共有フォルダをマウント
```bash
sudo apt update
sudo apt install virtualbox-guest-utils
mkdir data
sudo mount -t vboxsf srsEPC-career /home/user/data
sudo nano /etc/fstab
# srsEPC-career /home/user/data vboxsf defaults 0 0 を末尾に追加
```

[srsRANドキュメント](https://docs.srslte.com/en/latest/general/source/1_installation.html#gen-installation)と
[ZeroMQインストールガイド](https://docs.srslte.com/en/latest/app_notes/source/zeromq/source/index.html#introduction)を参考にsrsRANとZeroMQをインストール

インターネット接続用NATの解除を忘れずに

## 1.2 EPC + eNB  (Careerルート)

1.1のEPC + eNB  (Careerルート)と同様

1.1の仮想マシンをクローンしてもよい

## 2. UE

1.1のEPC + eNB (Careerルート)と手順は同様

1.1の仮想マシンをクローンしてもよい

## 3. アプリケーション（Dockerコンテナ）

ホストPCに `docker-ce`、 `docker-compose`をインストール

ビルド

```bash
cd ./docker
docker-compose build
```