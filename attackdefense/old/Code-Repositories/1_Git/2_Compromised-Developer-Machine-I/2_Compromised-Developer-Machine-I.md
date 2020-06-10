#### 2. Compromised Developer Machine I

----

- You have access to a developer machine on the network. A secret flag is hidden in the Gitlab repo used for app development.
- Objective: Find the flag in the source code repo!

----

```sh
root@attackdefense:/# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
1373: eth0@if1374: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:03 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.3/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
1376: eth1@if1377: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:2d:cb:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.45.203.2/24 brd 192.45.203.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:/#
```

```sh
root@attackdefense:~# ls -l
total 4
drwxr-xr-x 1 root root 4096 May 16 17:34 projects
root@attackdefense:~#
```

```sh
root@attackdefense:~# tree
.
`-- projects
    `-- root
        `-- project-code
            |-- README.md
            |-- files
            |-- functions.php
            `-- index.php

4 directories, 3 files
root@attackdefense:~#
```

```sh`
root@attackdefense:~# ls -lah
total 24K
drwx------ 1 root root 4.0K May 16 17:34 .
drwxr-xr-x 1 root root 4.0K Jul 29 02:39 ..
-rw-r--r-- 1 root root 3.1K Apr  9  2018 .bashrc
-rw-r--r-- 1 root root  148 Aug 17  2015 .profile
drwxr-xr-x 1 root root 4.0K May 16 17:36 .ssh
drwxr-xr-x 1 root root 4.0K May 16 17:34 projects
root@attackdefense:~#
root@attackdefense:~# cd .ssh/
root@attackdefense:~/.ssh# ls -lah
total 16K
drwxr-xr-x 1 root root 4.0K May 16 17:36 .
drwx------ 1 root root 4.0K May 16 17:34 ..
-rw-r--r-- 1 root root   93 May 16 15:34 config
-rw-r--r-- 1 root root  399 May 16 15:03 id_rsa.pub
root@attackdefense:~/.ssh# cat config
Host gitlab
    Hostname gitlab
    IdentityFile ~/.ssh/id_rsa.gitlab
    IdentitiesOnly yes
root@attackdefense:~/.ssh#
```

```sh
root@attackdefense:~/.ssh# find / -name id_rsa.gitlab 2>/dev/null
/var/opt/id_rsa.gitlab
root@attackdefense:~/.ssh#
```

```sh
root@attackdefense:~/.ssh# cat /var/opt/id_rsa.gitlab
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAn+OpQ0CJVMwktMmn/NHfojbMLl6oShIk+IG6hjq3YB0h5/lp
i9l+0K3j4hScadrgTwODqcjOiDcZ4xNF5pdmJ1SFdc3IFggDbVdV54cLkh65SrsG
ikSx79wxXsJsGRlI/MP5dHD9Q8rw2eA5Gg/szcDB6f+gUqLdqZpKYpOsVlbAkmAG
MmAEU7OkG5Jvbqnk56Kw4bNNMHdfL28GPi8n5y2Iho9AiL3BI1ryhqJTAvBmxwaL
ud/7bY2oh2MIdhzTDttQsuL1l5jTfCLoh/AL+JkapL7gg09csY2eYRIo/72JspwY
YNH99Hzj3/pYVhYque5CAQ53V3+fZxSKGAGwtwIDAQABAoIBAC26t1Z8xspx+K2c
X2d3vzZt5cf9WrSUq+5HbEmn0Xqz2la2hvFwq0yT73Fh47qC11TB9I5C2I8s80J2
6K8i7hyhl+oxiOCEOjazm+Y0QaLxFp3BEAXLz/iCSbyIbtJe4PkqM9aR2l3hVTF7
Z9mEZH4Ue2Gpsvjvi+ZOMqgvBENM6NtRHSZOuwxY3dCD/rnv+vj81Ph0LZWy8RFc
j4iqd4TDStOFVUZFnSksx+Llbg+qAZbaJDZ1fjwlCpwPq4U1/UtyrVXVgDuK070D
otM0LYZSKOtSVwEKm6Mud7CEXBomLiyMEdam24GoFssyteZrZ7mEy9vlnlnlHFSM
p2rD/AECgYEAzAG72Q4MmqKzZLAONzkCi/xDCR1pHNYE2BB/iDvWpYGZc1SfOXLl
vVflmG0hl65+5olfZsf7z3ps+ITfTkKtN5tSQsFcP9Tow5gAyWG5+97fr+Va6hV5
EH+iMCDyicf4TXwzRlRrLRDXtNlup307YNdD44EKZjuGm2dqrdu+GsECgYEAyKOE
Q/xId9p3iCta7dSlpC/+HNKyV413IjatfGh6YME156Ywlyb1W/xFlxJwAGxC8Djn
WSnrUZ9jdqHlabe7Lptqj01gYrUY9otr4B8Ddv2l+pIAnK3Xp3VqIovJWfdiWVkf
vxvoQvOMYAoFgKWzzrwkxynJzLfXfx0mlTkogXcCgYBN9UungmrmnM4Y5/5GtA55
GAk17ntAfbiUKJnToapAzOmq3OeLuJB6bqBaQznXEOOFjXFbgYiEnLAPuBbtfSVc
Xops4B80dVQNioSicCn2ShEI0oiPc200FNIRukV0yWnlklS1x4S9T/ZeMcjLUFvk
gd57jdA/iPfDYx2tGo/nAQKBgEstWaXPpaei6B7Rf+SVROtcQC60k7ZSf00Gh8KR
sykFvBjsIFDCfDTXNYwBkI3YAszXxXeXSWDwA+iziK4v9abk/Oxs5ayWhp/6ZZU4
iafQKpzUj/4k9ST9zaLcFbnsA6HOzyJgZoqPjw19M8qcS98uh+lIMyDN0aUDWy2W
mSLJAoGBAKLfb1tNKlbKnwcitCThokBb5AQLIfk9MCWnEvLDKB+ZCTCJs4GWVrft
to3qVpmRLqyljhQhlH8Vq12Q7WrQ+vc5ZPfIF+B9siDIy7hvQtaziyGt45P67Ujt
GrALqG8TeASj2Tp3RLeK47/6AgnKmzEN4kqc41YlCr9xNCJ1tGVP
-----END RSA PRIVATE KEY-----
root@attackdefense:~/.ssh#
```

```sh
root@attackdefense:~/.ssh# cp /var/opt/id_rsa.gitlab .
root@attackdefense:~/.ssh# ls -lah
total 24K
drwxr-xr-x 1 root root 4.0K Jul 29 02:48 .
drwx------ 1 root root 4.0K May 16 17:34 ..
-rw-r--r-- 1 root root   93 May 16 15:34 config
-rw------- 1 root root 1.7K Jul 29 02:48 id_rsa.gitlab
-rw-r--r-- 1 root root  399 May 16 15:03 id_rsa.pub
root@attackdefense:~/.ssh#
```

```sh
root@attackdefense:~# git clone git@gitlab:root/project-code.git
Cloning into 'project-code'...
The authenticity of host 'gitlab (192.45.203.3)' can't be established.
ECDSA key fingerprint is SHA256:cHQO1keq/jr/nQh58gC9cll/Y/NAd+eE9esaZyjVaMg.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'gitlab,192.45.203.3' (ECDSA) to the list of known hosts.
remote: Enumerating objects: 11, done.
remote: Counting objects: 100% (11/11), done.
remote: Compressing objects: 100% (8/8), done.
remote: Total 11 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (11/11), 33.21 KiB | 6.64 MiB/s, done.
root@attackdefense:~#
```

```sh
root@attackdefense:~# ls
project-code  projects
root@attackdefense:~# cd project-code/
root@attackdefense:~/project-code# ls -lah
total 164K
drwxr-xr-x 3 root root 4.0K Jul 29 02:49 .
drwx------ 1 root root 4.0K Jul 29 02:49 ..
drwxr-xr-x 8 root root 4.0K Jul 29 02:49 .git
-rw-r--r-- 1 root root 8.5K Jul 29 02:49 README
-rw-r--r-- 1 root root   16 Jul 29 02:49 README.md
-rw-r--r-- 1 root root   34 Jul 29 02:49 flag.txt
-rw-r--r-- 1 root root  40K Jul 29 02:49 functions.php
-rw-r--r-- 1 root root  57K Jul 29 02:49 index.php
-rw-r--r-- 1 root root 5.2K Jul 29 02:49 mobile.css
-rw-r--r-- 1 root root  19K Jul 29 02:49 zipstream.php
root@attackdefense:~/project-code# cat flag.txt
f9a1e58bde48c2b79c712dc4208a3630
root@attackdefense:~/project-code#
```

----

EOF