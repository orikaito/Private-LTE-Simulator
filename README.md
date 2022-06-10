**Private-LTE-Simulator**

鈴鹿高専専攻科特別研究

# ディレクトリ構造

## `data` ディレクトリ

`lte-softmodem` `lte-uesoftmodem` `NextEPC` それぞれのconfファイル類  
それぞれの仮想マシンのホームディレクトリ上に `~/data` としてマウント

## `docker` ディレクトリ

コンテンツサーバー用ディレクトリ

# 環境構築

## 1. NextEPC (VirtualBox)

ネットワークはSSH、eNBとの通信兼用で `192.168.56.103` を、P-GWからコンテンツサーバー用に `192.168.58.103` を割当

- Ubuntu 18.04 Server版をインストール
- NextEPCをaptでインストール

```bash
sudo apt install nextepc
```

- 共有フォルダをマウント
```bash
sudo apt update
sudo apt install virtualbox-guest-utils
mkdir data
sudo mount -t vboxsf lte-softmodem /home/user/data
sudo su
echo "NextEPC /home/user/data vboxsf defaults 0 0" >> /etc/fstab
exit
```

- ネットワーク設定
```bash
sudo cp ./data/99-manual.yaml /etc/netplan/
sudo netpaln apply
```

- confファイルを上書きコピー
```bash
sudo cp -f ./data/
```

- デーモンを再起動

```bash
sudo systemctl restart nextepc-mmed
sudo systemctl restart nextepc-pgwd
sudo systemctl restart nextepc-sgwd
sudo systemctl restart nextepc-hssd
sudo systemctl restart nextepc-pcrfd
```

## 2. lte-softmodem lte-uesoftmodem (VirtualBox)

lte-softmodemとlte-uesoftmodemは共通マシン上で動作させる(localhostでL2nFAPI通信)  
ネットワークはSSH、EPCとの通信兼用で `192.168.56.102` を割当  
ゲストホスト間の共有フォルダとして `data`を `/home/user/data` に手動マウント

- Ubuntu 18.04 Server版をインストール
- OpenAirInterfaceをダウンロード
- 共有フォルダをマウント
```bash
sudo apt update
sudo apt install virtualbox-guest-utils
mkdir data
sudo mount -t vboxsf lte-softmodem /home/user/data
sudo echo "lte-softmodem /home/user/data vboxsf defaults 0 0" >> /etc/fstab
```

- ネットワーク設定
```bash
sudo cp ./data/99-manual.yaml /etc/netplan/
sudo netpaln apply
```

- confファイルを上書きコピー
```bash
sudo cp -f ./data/
```

- ビルド

## 3. Dockerコンテナ

```bash
cd ~/docker/nginx
docker-compose build
```

# 実行

## 1. NextEPC

起動するだけでEPCがデーモンとして実行される。

```
```

## 2. lte-softmodem lte-uesoftmodem

```bash
sudo ip addr add 127.0.0.2/8 dev lo
source init_nas_s1 UE
sudo -E ./lte_build_oai/build/lte-softmodem -O ../ci-scripts/conf_files/rcc.band7.tm1.nfapi.conf > /dev/null
sudo -E ./lte_build_oai/build/lte-uesoftmodem -O ../ci-scripts/conf_files/ue.nfapi.conf --L2-emul 3 --num-ues 1 --nums_ue_thread 1 > /dev/null
```

```bash
sudo ip route add 192.168.58.0/24 via 45.45.0.1 dev oip1
```

## srsRAN

```bash
sudo srsepc ~/data/epc.conf --hss.db_file ~/data/user_db.csv
sudo ip netns exec ue1 ip route add 192.168.56.0/24 via 0.0.0.0 dev tun_srsue
sudo iptables -t nat -A POSTROUTING -o enp0s8 -j MASQUERADE
sudo iptables -I INPUT -i srs_spgw_sgi -j ACCEPT
```

## host

```bash
sudo sed -i '/net.ipv4.ip_forward/s/^#//' /etc/sysctl.conf
sudo sysctl -p
sudo iptables -t nat -A POSTROUTING -s 192.168.60.0/24 -d 192.168.30.0/24 -o br_career -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -s 192.168.60.0/24 -d 192.168.32.0/24 -o br_edge -j MASQUERADE
```
<!--
```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -A FORWARD -s 192.168.58.0/24 -i vboxnet1 -j ACCEPT
```
-->

## application

```bash
sudo ip route add 192.168.30.0/24 via 192.168.58.1 dev enp0s8
```

# 参考URL

- [OpenAirInterface](https://gitlab.eurecom.fr/oai/openairinterface5g)
- [NextEPC](https://nextepc.org/)
- [LTEを自作してみる(Part3) @K5K Qiita](https://qiita.com/K5K/items/d74bd78931ba2ccd3107)
- [OAI L2 nFAPI + Free5GCによるNSA 5GC構築方法 metaMD HatenaBlog](https://metonymical.hatenablog.com/entry/2020/01/03/151233)