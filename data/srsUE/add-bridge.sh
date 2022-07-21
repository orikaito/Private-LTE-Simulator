#!/bin/bash
# career
ip netns add ue-career
ip link add UE-C_to_app type veth peer name app_to_UE-C
ip link set UE-C_to_app netns ue-career up
ip addr add 10.10.2.2/24 dev app_to_UE-C
ip link set app_to_UE-C up
ip netns exec ue-career ip addr add 10.10.2.1/24 dev UE-C_to_app
ip route add default via 10.10.2.1
# edge
ip netns add ue-edge
ip link add UE-E_to_app type veth peer name app_to_UE-E
ip link set UE-E_to_app netns ue-edge up
ip addr add 10.12.2.2/24 dev app_to_UE-E
ip link set app_to_UE-E up
ip netns exec ue-edge ip addr add 10.12.2.1/24 dev UE-E_to_app
ip route add 192.168.32.0/24 via 10.12.2.1