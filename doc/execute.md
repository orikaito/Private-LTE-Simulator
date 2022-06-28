
# 実行

[READMEに戻る](../README.md)

## 1. アプリケーション（Dockerコンテナ）

```bash
cd ./docker
docker-compose up
```

ホスト側でNATの設定をしておく

```bash
sudo sed -i '/net.ipv4.ip_forward/s/^#//' /etc/sysctl.conf
sudo sysctl -p
sudo iptables -t nat -A POSTROUTING -s 192.168.60.0/24 -d 192.168.30.0/24 -o br_career -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -s 192.168.62.0/24 -d 192.168.32.0/24 -o br_edge -j MASQUERADE
```
<!--
```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -A FORWARD -s 192.168.58.0/24 -i vboxnet1 -j ACCEPT
```
-->

## 2. EPC + eNB

EPCを起動

```bash
cd srsRAN/build/
sudo ./srsepc/src/srsepc ~/data/epc.conf --hss.db_file ~/data/user_db.csv
```
<!--
sudo iptables -I INPUT -i srs_spgw_sgi -j ACCEPT
-->

別端末でeNBを起動

```bash
cd srsRAN/build/
./srsenb/src/srsenb ~/data/enb.conf
```

別端末でルート、NATを設定
```bash
sudo ip route add 192.168.30.0/24 via 192.168.60.1 dev enp0s9
sudo iptables -t nat -A POSTROUTING -s 172.16.0.0/24 -d 192.168.30.0/24 -o enp0s9 -j MASQUERADE
```

## 3. UE

UEを起動

```bash
sudo ip netns add ue1
cd srsRAN/build/
sudo ./srsue/src/srsue ~/data/ue.conf
```

別端末でブリッジネットワークやNAT、ルートを設定

```bash
sudo ip link add UE_to_app type veth peer name app_to_UE
sudo ip link set UE_to_app netns ue1 up
sudo ip addr add 10.10.2.2/24 dev app_to_UE
sudo ip link set app_to_UE up

sudo ip netns exec ue1 bash
ip route add default via 172.16.0.1
ip addr add 10.10.2.1/24 dev UE_to_app
iptables -t nat -A POSTROUTING -s 10.10.2.0/24 -d 192.168.30.0/24 -o tun_srsue -j MASQUERADE
```

DNSサーバを設定

```bash
sudo nano /etc/systemd/resolved.conf
sudo systemctl restart systemd-resolved
sudo systemd-resolve --status
```