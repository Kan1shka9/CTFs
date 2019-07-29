#### 1. PyPi Server: Recon Basics

----

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
85: eth0@if86: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:03 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.3/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
88: eth1@if89: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:59:fb:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.89.251.2/24 brd 192.89.251.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# nmap -sC -sV 192.89.251.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-29 03:41 UTC
Nmap scan report for ht0y4uksd1dso8ry0rt56vk4u.temp-network_a-89-251 (192.89.251.3)
Host is up (0.000011s latency).
Not shown: 999 closed ports
PORT   STATE SERVICE VERSION
80/tcp open  http    WSGIServer 0.2 (Python 3.6.7)
|_http-title: Welcome to pypiserver!
MAC Address: 02:42:C0:59:FB:03 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.99 seconds
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# curl http://192.89.251.3
<html><head><title>Welcome to pypiserver!</title></head><body>
<h1>Welcome to pypiserver!</h1>
<p>This is a PyPI compatible package index serving 12 packages.</p>

<p> To use this server with pip, run the the following command:
<blockquote><pre>
pip install --extra-index-url http://192.89.251.3/ PACKAGE [PACKAGE2...]
</pre></blockquote></p>

<p> To use this server with easy_install, run the the following command:
<blockquote><pre>
easy_install -i http://192.89.251.3/simple/ PACKAGE
</pre></blockquote></p>

<p>The complete list of all packages can be found <a href="/packages/">here</a>
or via the <a href="/simple/">simple</a> index.</p>

<p>This instance is running version 1.3.0 of the
  <a href="https://pypi.org/project/pypiserver/">pypiserver</a> software.</p>
</body></html>

root@attackdefense:~#
```

----

```sh
root@attackdefense:~# pip install --trusted-host 192.89.251.3 --index-url http://192.89.251.3 pywinwifi
Looking in indexes: http://192.89.251.3
Collecting pywinwifi
  Downloading http://192.89.251.3/packages/pywinwifi-1.0.0.zip
Building wheels for collected packages: pywinwifi
  Running setup.py bdist_wheel for pywinwifi ... done
  Stored in directory: /root/.cache/pip/wheels/91/f6/0b/8bd8d4beac08cecace519e988877d1c39b6f1a244dca331140
Successfully built pywinwifi
Installing collected packages: pywinwifi
Successfully installed pywinwifi-1.0.0
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# cat /etc/pip.conf
[global]
index = http://192.89.251.3
index-url = http://192.89.251.3
trusted-host = http://192.89.251.3
root@attackdefense:~#
```

```sh
root@attackdefense:~# pip search awscli
awscli (1.16.170)  - 1.16.170
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# curl http://192.89.251.3
<html><head><title>Welcome to pypiserver!</title></head><body>
<h1>Welcome to pypiserver!</h1>
<p>This is a PyPI compatible package index serving 12 packages.</p>

<p> To use this server with pip, run the the following command:
<blockquote><pre>
pip install --extra-index-url http://192.89.251.3/ PACKAGE [PACKAGE2...]
</pre></blockquote></p>

<p> To use this server with easy_install, run the the following command:
<blockquote><pre>
easy_install -i http://192.89.251.3/simple/ PACKAGE
</pre></blockquote></p>

<p>The complete list of all packages can be found <a href="/packages/">here</a>
or via the <a href="/simple/">simple</a> index.</p>

<p>This instance is running version 1.3.0 of the
  <a href="https://pypi.org/project/pypiserver/">pypiserver</a> software.</p>
</body></html>
```

```sh
root@attackdefense:~# curl http://192.89.251.3/simple/
    <html>
        <head>
            <title>Simple Index</title>
        </head>
        <body>
            <h1>Simple Index</h1>
                 <a href="awscli/">awscli</a><br>
                 <a href="docutils/">docutils</a><br>
                 <a href="pywinwifi/">pywinwifi</a><br>
                 <a href="requests/">requests</a><br>
                 <a href="s3transfer/">s3transfer</a><br>
                 <a href="urllib3/">urllib3</a><br>
        </body>
    </html>
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# pip download --trusted-host 192.89.251.3 --index-url http://192.89.251.3 pywinwifi
Looking in indexes: http://192.89.251.3
Collecting pywinwifi
  Downloading http://192.89.251.3/packages/pywinwifi-1.0.0.zip
  Saved ./pywinwifi-1.0.0.zip
Successfully downloaded pywinwifi
root@attackdefense:~#
```

```sh
root@attackdefense:~# unzip pywinwifi-1.0.0.zip
Archive:  pywinwifi-1.0.0.zip
   creating: pywinwifi-1.0.0/
  inflating: pywinwifi-1.0.0/setup.py
  inflating: pywinwifi-1.0.0/PKG-INFO
   creating: pywinwifi-1.0.0/pywinwifi/
  inflating: pywinwifi-1.0.0/pywinwifi/WindowsWifi.py
 extracting: pywinwifi-1.0.0/pywinwifi/__init__.py
  inflating: pywinwifi-1.0.0/pywinwifi/pywinwifi.py
 extracting: pywinwifi-1.0.0/pywinwifi/flag
  inflating: pywinwifi-1.0.0/pywinwifi/WindowsNativeWifiApi.py
root@attackdefense:~#
```

```sh
root@attackdefense:~# cd pywinwifi-1.0.0
root@attackdefense:~/pywinwifi-1.0.0# cat pywinwifi/flag
ab437d40430985a1abd69b1747f37a12
root@attackdefense:~/pywinwifi-1.0.0#
```

----

###### Questions

- Which service is running on the target machine? State the complete name.

```
# nmap -sC -sV 192.89.251.3
WSGIServer 0.2
```

- What is hosted on the HTTP server of the target machine?

```
# curl http://192.89.251.3
pypiserver
```

- Install pywinwifi from local repository to attacker machine.

```
# pip install --trusted-host 192.89.251.3 --index-url http://192.89.251.3 pywinwifi
```

- Which version of awscli is available on the remote server?

```
# nano /etc/pip.conf
# pip search awscli
1.16.170
```

- How many packages are present on the PyPi server?

```
# curl http://192.89.251.3/
# curl http://192.89.251.3/simple/
# browsh --startup-url 192.89.251.3/simple/
6
```

- There is a flag hidden in pywinwifi package. Retrieve and submit that flag.

```
# pip download --trusted-host 192.89.251.3 --index-url http://192.89.251.3 pywinwifi
ab437d40430985a1abd69b1747f37a12
```

----

EOF