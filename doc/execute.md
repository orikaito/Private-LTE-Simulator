
# 実行

[READMEに戻る](../README.md)

## 1. ホスト（アプリケーション類Dockerコンテナ）

```bash
cd ./docker
docker-compose up
```

ホスト側のNATはufwで行う

```bash
sudo ufw allow from 192.168.60.0/24
sudo ufw allow from 192.168.62.0/24

sudo nano /etc/default/ufw
# DEFAULT_FORWARD_POLICY=“ACCEPT"に変更

sudo sed -i '/net.ipv4.ip_forward/s/^#//' /etc/sysctl.conf

sudo nano /etc/ufw/before.rules
# 下記内容を追記

sudo ufw enable
```

`/etc/ufw/before.rules` の末尾に追記する内容
``` /etc/ufw/before.rules
*nat
-F
:POSTROUTING ACCEPT [0:0]
-A POSTROUTING -s 192.168.60.0/24 -d 192.168.30.0/24 -o br_career -j MASQUERADE
-A POSTROUTING -s 192.168.62.0/24 -d 192.168.32.0/24 -o br_edge -j MASQUERADE
COMMIT
```
<!--
```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -A FORWARD -s 192.168.58.0/24 -i vboxnet1 -j ACCEPT
```
-->

模擬遅延を設定
```bash
sudo tc qdisc add dev vboxnet1 root handle 1:0 netem delay 50ms
```

## 2.1 EPC + eNB (Careerルート)

EPCを起動

```bash
cd srsRAN/build/
sudo ./srsepc/src/srsepc ~/data/epc.conf
```
<!--
sudo iptables -I INPUT -i srs_spgw_sgi -j ACCEPT
-->

別端末でeNBを起動  
実行にsudoは不要だが、スレッド優先度に関するWarningがでるため、sudo有りで実行

```bash
cd srsRAN/build/
sudo ./srsenb/src/srsenb ~/data/enb.conf
```


別端末でNATを設定
```bash
sudo iptables -t nat -A POSTROUTING -s 172.16.0.0/24 -d 192.168.30.0/24 -o enp0s9 -j MASQUERADE
```

## 2.2 EPC + eNB (Edgeルート)

2.1 EPC + eNB (Careerルート)と同様

## 3. UE

Career側のUEを起動

```bash
sudo ip netns add ue-career
cd srsRAN-career/build/
sudo ./srsue/src/srsue ~/data/ue-career.conf
```

別端末でブリッジネットワークやNAT、ルートを設定

```bash
sudo ip link add UE_to_app type veth peer name app_to_UE
sudo ip link set UE_to_app netns ue-career up
sudo ip addr add 10.10.2.2/24 dev app_to_UE
sudo ip link set app_to_UE up

sudo ip netns exec ue-career bash
ip route add default via 172.16.0.1
ip addr add 10.10.2.1/24 dev UE_to_app
iptables -t nat -A POSTROUTING -s 10.10.2.0/24 -d 192.168.30.0/24 -o tun_srsue -j MASQUERADE
```

Edge側も同様に行う

DNSサーバを設定

```bash
sudo nano /etc/systemd/resolved.conf
# DNS= にアドレスを記入
sudo systemctl restart systemd-resolved
sudo systemd-resolve --status
```

模擬遅延の設定

```bash
sudo tc qdisc add dev enp0s9 root handle 1:0 netem delay 50ms
```

# 5. PINGテスト

UE側からアプリケーションサーバーへのPINGテストを行う。

応答時間をCSV出力するには以下のコマンドで行う。

```bash
touch ping.pcap
sudo tshark -i インターフェース -w ./ping.pcap -F pcap

# 別端末でpingを実行
ping 宛先アドレス -p 5A5A5A5A -s 2056 -i 0.2 -c 100

# pingを終了後、元のtsharkプロセスを終了し、以下コマンドでPCAPからCSVを出力
tshark -r ping.pcap -Y "ip.src == 宛先アドレス and icmp" -T fields -E separator=',' -e "icmp.resptime" > ping.csv
```

# 6. アプリケーションクライアント

UE側で `~/data/srsUE/mnist_request.py` を実行すると、0~9の画像ファイルを10ms秒ごとにサーバに送信し、返ってきた結果を標準出力する。

もしくは、 `~/data/srsUE/mnist_test` ディレクトリに認識用画像ファイル (`*.png`) があるのでそこに移動し、以下のコマンドで画像をPOSTする。

認識結果・認識精度・認識所要時間がJSONで返ってくる。

```bash
# Career route
curl -X POST -F "file=@./ファイル名.png" "http://api.career-izuka.lab/predict"

# Edge route
curl -X POST -F "file=@./ファイル名.png" "http://api.edge-izuka.lab/predict"
```