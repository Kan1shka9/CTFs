#### linux.offsec.club

- [user1](#user1)
- [user2](#user2)
- [user3](#user3)
- [user4](#user4)
- [user5](#user5)
- [user6](#user6)
- [user7](#user7)
- [user8](#user8)
- [user9](#user9)
- [user10](#user10)
- [user11](#user11)
- [user12](#user12)
- [user13](#user13)
- [user14](#user14)
- [user15](#user15)

----

###### user1

![](images/1.png)

```sh
➜  linux.offsec.club ssh user1@linux.offsec.club
The authenticity of host 'linux.offsec.club (45.63.64.214)' can't be established.
ECDSA key fingerprint is SHA256:wRvsADd282C1pBu+BvWzBWkL9reCVN2bAFKbo0FwQ8U.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'linux.offsec.club,45.63.64.214' (ECDSA) to the list of known hosts.
user1@linux.offsec.club's password:
Linux webserver 4.9.0-5-amd64 #1 SMP Debian 4.9.65-3+deb9u2 (2018-01-04) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Fri Jun 29 23:11:18 2018 from 178.59.42.252
user1@webserver:~$ ls
user1@webserver:~$ ls -lah
total 28K
dr-x------  4 user1 challenges 4.0K Feb 22 21:07 .
drwxr-xr-x 24 root  root       4.0K Apr 15 23:04 ..
lrwxrwxrwx  1 root  root          9 Feb 16 00:04 .bash_history -> /dev/null
-r--r--r--  1 user1 challenges  220 May 15  2017 .bash_logout
-r--r--r--  1 user1 challenges 3.5K May 15  2017 .bashrc
dr-x------  2 user1 challenges 4.0K Feb 16 00:14 .here
-r--r--r--  1 user1 challenges  675 May 15  2017 .profile
dr--------  2 user1 challenges 4.0K Feb 22 21:10 .ssh
user1@webserver:~$ cd .here/
user1@webserver:~/.here$ ls -lah
total 12K
dr-x------ 2 user1 challenges 4.0K Feb 16 00:14 .
dr-x------ 4 user1 challenges 4.0K Feb 22 21:07 ..
-r-xr-x--- 1 root  challenges   18 Feb 16 00:14 pass
user1@webserver:~/.here$ cat pass
CentsMaybeCarry55
user1@webserver:~/.here$ exit
logout
Connection to linux.offsec.club closed.
➜  linux.offsec.club
```

----

###### user2

```sh
➜  linux.offsec.club ssh user2@linux.offsec.club
user2@linux.offsec.club's password:
Linux webserver 4.9.0-5-amd64 #1 SMP Debian 4.9.65-3+deb9u2 (2018-01-04) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Jun 30 17:08:48 2018 from 75.140.84.109
user2@webserver:~$ ls -l
total 4
-r-xr-x--- 1 root challenges 16 Feb 20 21:50 $!\Password&
user2@webserver:~$ cat *
WereElseLabor80
user2@webserver:~$ exit
logout
Connection to linux.offsec.club closed.
➜  linux.offsec.club
```

----

###### user3

```sh
➜  linux.offsec.club ssh user3@linux.offsec.club
user3@linux.offsec.club's password:
Linux webserver 4.9.0-5-amd64 #1 SMP Debian 4.9.65-3+deb9u2 (2018-01-04) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Fri Jun 29 23:12:59 2018 from ::1
user3@webserver:~$ ls -l
total 4
-r-xr-x--- 1 root challenges 1675 Feb 20 21:27 password
user3@webserver:~$ cat password
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAtXZeXbYolBYItGEg+VMyd20Jtln2J7GVW2CYhbfX1qmr1iFS
B2bD//ns4mQNGBQE30wfsIXsvPd0Lc1ptKALZo2LhItTlb2/eQ1jxl8Y/Rnbihex
c1s+9Dq2j+kHzHh4Kh74iFP9rnZG3KQHs56KDAP4CtxvDwanwHjzucekbwNOBY0w
bx6VtQ1bhNV0paPkoI9PXR8YZx9ME6uQv70LxAdti292P+DNM1L/qeHGc3QWBQk1
+K0Iyy/bzp0BqgnJlYiFT0Jsst6zzGQ0QL1+7XXtt5NYH55neoEzaM1/WwCunNLP
gdWz20e4AbbA87JNZ+wyrfKtA40VsCMOdOX0FwIDAQABAoIBAE5tg2mTQkSGpWp4
lEzOJYCyUsFKbnZHbVsaC7G3fITdvlQFALQMOWgX98b9IR+n/1cXSpb7uw8NEFx/
bFFR3ruLL6KwqQaOBQRnwhjJnz48/8LWbK6D4FikS6U1PValNqJV0mrxijHuEsBn
8KA0REvfJ0Ric2mWIcixPf2siKglljDDM/r5t/oiTQPPCvd29ZIX4G+bIwyjvdmq
XJ4n1o0HD1fKKOkf/bnr2EgLjr/lyAnc46fVu83DpMzdZu4lSQxgWJ2fjxrdREvN
mWS6fVKfRApr0GfhamXdqwGiHa9qGlQ9vkb36aecFRKhIBxr/l0SU6efQD9wUgq0
o381pmkCgYEA2abPkAQWpCrVrprp6CalR0hTxe2qkRgDTJvwdhlOX+YpWZCxhWlK
pw6V4zDBA+0DQkg9+n9EnVBLQku2OYxXOHvo76weHq9HR6FyErJuNI6zW6Y2dh9j
SpkZzHxlKc8XbaNK1x+JvNlyy/Sd83BSIraoNqkWDSRC0d5hFrBdv7UCgYEA1W89
j6j9KWMCIh3u2YWevV2bKaNDvFrTDqXU4LZRIQI/r0C6MVbq07DphZqGT+koUPGF
ngkd6gsEY9uB+7e/Wo8hmsVnMnQXsl1qKY+A+L9Vk291UGAI6dvTr9kVU6TNt60U
FLh2fel1cGDgfVnDk7+/RgygUw+8x8zjnUNVTBsCgYAw5wb538FKj4lFWu81RwGZ
u4l/DkBlq1SKcPsdPeBbMbaWtij8xcSNNny8+CZWAHnb+albUB8VjYXrVmGSGpM6
ULTsrOpzkIRedsrPoqGaU3m/HOBdt/2yNCYUyNpeA3bLHoZhQWfMM7tUUhjvKox5
2jp/VYxr1Xrh9qov096shQKBgBxCJy9vG12waybjOa15IIRH8XQ41o4IpGsLD71U
xjcNmir08fH4ZQz0Hmb/B4tq/liBMcSzxk8neERUWsheEqrFypg4TKqEbmLCNX0d
L+E/S/BCUJD8thFodoWQw18YsdgAxWjc52tSTqc7XF2cVeWo/IUkxNFagw8dFIHM
2W1DAoGACjRXhS1rGiEBBzC0pNVVL/9EAXrUE81Z/IJzX85vE6NEA0o3yTkKH22w
HOgbHfdzyuPu/QZa3IaPx0U3f8/OopSSm9Cf6dPrhMFHnIfG8DsO6qZmgrpXYhDz
LvkzagJrpVlAkkHvY/Py1aDRdF2M4hZAT0oSFYramT0eUdNAtSs=
-----END RSA PRIVATE KEY-----
user3@webserver:~$ exit
logout
Connection to linux.offsec.club closed.
➜  linux.offsec.club
```

----

###### user4

```sh
➜  linux.offsec.club cat private.key
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAtXZeXbYolBYItGEg+VMyd20Jtln2J7GVW2CYhbfX1qmr1iFS
B2bD//ns4mQNGBQE30wfsIXsvPd0Lc1ptKALZo2LhItTlb2/eQ1jxl8Y/Rnbihex
c1s+9Dq2j+kHzHh4Kh74iFP9rnZG3KQHs56KDAP4CtxvDwanwHjzucekbwNOBY0w
bx6VtQ1bhNV0paPkoI9PXR8YZx9ME6uQv70LxAdti292P+DNM1L/qeHGc3QWBQk1
+K0Iyy/bzp0BqgnJlYiFT0Jsst6zzGQ0QL1+7XXtt5NYH55neoEzaM1/WwCunNLP
gdWz20e4AbbA87JNZ+wyrfKtA40VsCMOdOX0FwIDAQABAoIBAE5tg2mTQkSGpWp4
lEzOJYCyUsFKbnZHbVsaC7G3fITdvlQFALQMOWgX98b9IR+n/1cXSpb7uw8NEFx/
bFFR3ruLL6KwqQaOBQRnwhjJnz48/8LWbK6D4FikS6U1PValNqJV0mrxijHuEsBn
8KA0REvfJ0Ric2mWIcixPf2siKglljDDM/r5t/oiTQPPCvd29ZIX4G+bIwyjvdmq
XJ4n1o0HD1fKKOkf/bnr2EgLjr/lyAnc46fVu83DpMzdZu4lSQxgWJ2fjxrdREvN
mWS6fVKfRApr0GfhamXdqwGiHa9qGlQ9vkb36aecFRKhIBxr/l0SU6efQD9wUgq0
o381pmkCgYEA2abPkAQWpCrVrprp6CalR0hTxe2qkRgDTJvwdhlOX+YpWZCxhWlK
pw6V4zDBA+0DQkg9+n9EnVBLQku2OYxXOHvo76weHq9HR6FyErJuNI6zW6Y2dh9j
SpkZzHxlKc8XbaNK1x+JvNlyy/Sd83BSIraoNqkWDSRC0d5hFrBdv7UCgYEA1W89
j6j9KWMCIh3u2YWevV2bKaNDvFrTDqXU4LZRIQI/r0C6MVbq07DphZqGT+koUPGF
ngkd6gsEY9uB+7e/Wo8hmsVnMnQXsl1qKY+A+L9Vk291UGAI6dvTr9kVU6TNt60U
FLh2fel1cGDgfVnDk7+/RgygUw+8x8zjnUNVTBsCgYAw5wb538FKj4lFWu81RwGZ
u4l/DkBlq1SKcPsdPeBbMbaWtij8xcSNNny8+CZWAHnb+albUB8VjYXrVmGSGpM6
ULTsrOpzkIRedsrPoqGaU3m/HOBdt/2yNCYUyNpeA3bLHoZhQWfMM7tUUhjvKox5
2jp/VYxr1Xrh9qov096shQKBgBxCJy9vG12waybjOa15IIRH8XQ41o4IpGsLD71U
xjcNmir08fH4ZQz0Hmb/B4tq/liBMcSzxk8neERUWsheEqrFypg4TKqEbmLCNX0d
L+E/S/BCUJD8thFodoWQw18YsdgAxWjc52tSTqc7XF2cVeWo/IUkxNFagw8dFIHM
2W1DAoGACjRXhS1rGiEBBzC0pNVVL/9EAXrUE81Z/IJzX85vE6NEA0o3yTkKH22w
HOgbHfdzyuPu/QZa3IaPx0U3f8/OopSSm9Cf6dPrhMFHnIfG8DsO6qZmgrpXYhDz
LvkzagJrpVlAkkHvY/Py1aDRdF2M4hZAT0oSFYramT0eUdNAtSs=
-----END RSA PRIVATE KEY-----
➜  linux.offsec.club chmod 600 private.key
➜  linux.offsec.club ls -l
total 8
-rw-------  1 kan1shka9  staff  1675 Jun 30 10:11 private.key
➜  linux.offsec.club ssh user4@linux.offsec.club -i private.key
Linux webserver 4.9.0-5-amd64 #1 SMP Debian 4.9.65-3+deb9u2 (2018-01-04) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Fri Jun 29 23:22:31 2018 from ::1
user4@webserver:~$ ls
user4@webserver:~$ ls -lah
total 32K
dr-x------  4 user4 challenges 4.0K Feb 20 22:16 .
drwxr-xr-x 24 root  root       4.0K Apr 15 23:04 ..
lrwxrwxrwx  1 root  root          9 Feb 16 00:04 .bash_history -> /dev/null
-r--r--r--  1 user4 challenges  220 May 15  2017 .bash_logout
-r--r--r--  1 user4 challenges 3.6K Jun 16 21:43 .bashrc
drwxr-xr-x  3 root  root       4.0K Feb 20 20:38 .git
-rw-r--r--  1 root  root         26 Feb 20 22:16 .inputrc
-r--r--r--  1 user4 challenges  675 May 15  2017 .profile
dr-x--x--x  2 root  challenges 4.0K Feb 20 21:17 .ssh
user4@webserver:~$ cd .git
user4@webserver:~/.git$ ls -lah
total 12K
drwxr-xr-x 3 root  root       4.0K Feb 20 20:38 .
dr-x------ 4 user4 challenges 4.0K Feb 20 22:16 ..
drwxr-xr-x 6 root  root       4.0K Feb 20 22:10 .nolook
user4@webserver:~/.git$ cd .nolook
user4@webserver:~/.git/.nolook$ ls -lah
total 24K
drwxr-xr-x 6 root root 4.0K Feb 20 22:10 .
drwxr-xr-x 3 root root 4.0K Feb 20 20:38 ..
drwxr-xr-x 2 root root 4.0K Feb 20 22:09 .Bm@^[
drwxr-xr-x 3 root root 4.0K Feb 20 22:10 !:{g5Z
drwxr-xr-x 2 root root 4.0K Feb 20 22:09 .l@<X`
drwxr-xr-x 2 root root 4.0K Feb 20 22:09 .N~WSM
user4@webserver:~/.git/.nolook$ find
.
./.Bm@^[
./!:{g5Z
./!:{g5Z/e^z|,>
./!:{g5Z/e^z|,>/G_4)xg
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ/EWm'ES
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ/EWm'ES/pGk+)z
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ/EWm'ES/pGk+)z/oHkKcb
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ/EWm'ES/pGk+)z/oHkKcb/zP)ct8
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ/EWm'ES/pGk+)z/oHkKcb/zP)ct8/bR:ad'
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ/EWm'ES/pGk+)z/oHkKcb/zP)ct8/bR:ad'/`?#Ph|
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ/EWm'ES/pGk+)z/oHkKcb/zP)ct8/bR:ad'/`?#Ph|/4uo^~:
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ/EWm'ES/pGk+)z/oHkKcb/zP)ct8/bR:ad'/`?#Ph|/4uo^~:/%'F;r5
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ/EWm'ES/pGk+)z/oHkKcb/zP)ct8/bR:ad'/`?#Ph|/4uo^~:/%'F;r5/%FU67O
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ/EWm'ES/pGk+)z/oHkKcb/zP)ct8/bR:ad'/`?#Ph|/4uo^~:/%'F;r5/%FU67O/(3bLI2
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ/EWm'ES/pGk+)z/oHkKcb/zP)ct8/bR:ad'/`?#Ph|/4uo^~:/%'F;r5/%FU67O/(3bLI2/cVknT0
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ/EWm'ES/pGk+)z/oHkKcb/zP)ct8/bR:ad'/`?#Ph|/4uo^~:/%'F;r5/%FU67O/(3bLI2/cVknT0/nX4?_m
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ/EWm'ES/pGk+)z/oHkKcb/zP)ct8/bR:ad'/`?#Ph|/4uo^~:/%'F;r5/%FU67O/(3bLI2/cVknT0/nX4?_m/}8*BW,
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ/EWm'ES/pGk+)z/oHkKcb/zP)ct8/bR:ad'/`?#Ph|/4uo^~:/%'F;r5/%FU67O/(3bLI2/cVknT0/nX4?_m/}8*BW,/.password
./!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ/EWm'ES/pGk+)z/oHkKcb/zP)ct8/bR:ad'/`?#Ph|/4uo^~:/%'F;r5/%FU67O/(3bLI2/cVknT0/nX4?_m/}8*BW,/.password/password.txt
./.l@<X`
./.N~WSM
user4@webserver:~/.git/.nolook$ grep -R .
!:{g5Z/e^z|,>/G_4)xg/|y3\!E/){gy#~/TnWY[R/nT*K,8/X1TtXj/YM^B]-/i|k(w4/\uUi06/8^h_H*/jx__}2/#*3:z\/i`lAmj/&5&O[[/g?";~F/~<L#}"/\?xCY}/$5o>8x/I&Vksj/$5~fNY/=~_gvs/qLC+l?/So@']s/?TR9J~/WKl-@=/?d,G,!/&_&(<;/'.yEUJ/EWm'ES/pGk+)z/oHkKcb/zP)ct8/bR:ad'/`?#Ph|/4uo^~:/%'F;r5/%FU67O/(3bLI2/cVknT0/nX4?_m/}8*BW,/.password/password.txt:CloudGiftMalta49
user4@webserver:~/.git/.nolook$
user4@webserver:~/.git/.nolook$ exit
logout
Connection to linux.offsec.club closed.
➜  linux.offsec.club
```

----

###### user5

```sh
➜  linux.offsec.club ssh user5@linux.offsec.club
user5@linux.offsec.club's password:
Linux webserver 4.9.0-5-amd64 #1 SMP Debian 4.9.65-3+deb9u2 (2018-01-04) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Fri Jun 29 19:55:41 2018 from 174.115.33.239
user5@webserver:~$ ls -lah
total 32K
dr-x------  3 user5 challenges 4.0K Feb 22 21:09 .
drwxr-xr-x 24 root  root       4.0K Apr 15 23:04 ..
lrwxrwxrwx  1 root  root          9 Feb 16 00:04 .bash_history -> /dev/null
-r--r--r--  1 user5 challenges  220 May 15  2017 .bash_logout
-r--r--r--  1 user5 challenges 3.5K May 15  2017 .bashrc
-r-xr-x---  1 root  challenges 1.4K Feb 21 23:47 group.txt
-r-xr-x---  1 root  password     16 Feb 20 20:33 password.txt
-r--r--r--  1 user5 challenges  675 May 15  2017 .profile
dr--------  2 root  root       4.0K Feb 22 21:09 .ssh
user5@webserver:~$ cat group.txt
SG(1)                                                   User Commands                                                  SG(1)

NAME
       sg - execute command as different group ID

SYNOPSIS
       sg [-] [group [-c ] command]

DESCRIPTION
       The sg command works similar to newgrp but accepts a command. The command will be executed with the /bin/sh shell.
       With most shells you may run sg from, you need to enclose multi-word commands in quotes. Another difference between
       newgrp and sg is that some shells treat newgrp specially, replacing themselves with a new instance of a shell that
       newgrp creates. This doesn't happen with sg, so upon exit from a sg command you are returned to your previous group
       ID.

CONFIGURATION
       The following configuration variables in /etc/login.defs change the behavior of this tool:

       SYSLOG_SG_ENAB (boolean)
           Enable "syslog" logging of sg activity.

FILES
       /etc/passwd
           User account information.

       /etc/shadow
           Secure user account information.

       /etc/group
           Group account information.

       /etc/gshadow
           Secure group account information.

SEE ALSO
       id(1), login(1), newgrp(1), su(1), gpasswd(1), group(5), gshadow(5).

shadow-utils 4.4                                         05/17/2017                                                    SG(1)
user5@webserver:~$ cat password.txt
cat: password.txt: Permission denied
user5@webserver:~$ id
uid=1004(user5) gid=1000(challenges) groups=1000(challenges)
user5@webserver:~$ sg
Usage: sg group [[-c] command]
user5@webserver:~$ sg password -c id
Password:
uid=1004(user5) gid=1001(password) groups=1001(password),1000(challenges)
user5@webserver:~$ sg password -c "cat password.txt"
Password:
SoftBoneFound59
user5@webserver:~$ exit
logout
Connection to linux.offsec.club closed.
➜  linux.offsec.club
```

----

###### user6

```sh
➜  linux.offsec.club ssh user6@linux.offsec.club
user6@linux.offsec.club's password:
Linux webserver 4.9.0-5-amd64 #1 SMP Debian 4.9.65-3+deb9u2 (2018-01-04) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Jun 30 17:26:24 2018 from 75.140.84.109
user6@webserver:~$ ls -l
total 786440
-r-xr-x--- 1 root challenges 805306382 Feb 20 22:53 password.txt
user6@webserver:~$ file password.txt
password.txt: data
user6@webserver:~$ strings password.txt








SaveThanGoes26
^C
user6@webserver:~$ exit
logout
Connection to linux.offsec.club closed.
➜  linux.offsec.club
```

----

###### user7

```sh
➜  linux.offsec.club ssh user7@linux.offsec.club
user7@linux.offsec.club's password:
Linux webserver 4.9.0-5-amd64 #1 SMP Debian 4.9.65-3+deb9u2 (2018-01-04) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Fri Jun 29 19:58:11 2018 from 174.115.33.239
user7@webserver:~$ ls -l
total 4
-r--r----- 1 root challenges 16 Feb 20 22:51 password.txt
user7@webserver:~$ cat password.txt
Nope
user7@webserver:~$ cat
Nope
user7@webserver:~$ cat /etc/groups
Nope
user7@webserver:~$ less password.txt
Nope
user7@webserver:~$ alias
alias ls='ls --color=auto'
user7@webserver:~$ which cat
/usr/local/broke/cat
user7@webserver:~$ which more
/usr/local/broke/more
user7@webserver:~$ which less
/usr/local/broke/less
user7@webserver:~$ cd /usr/local/broke/
user7@webserver:/usr/local/broke$ ls -l
total 84
-rwxr-xr-x 1 root staff 23 Feb 20 22:47 cat
-rwxr-xr-x 1 root staff 23 Feb 20 22:47 dd
-rwxr-xr-x 1 root staff 23 Feb 20 22:47 echo
-rwxr-xr-x 1 root staff 23 Feb 20 22:47 emacs
-rwxr-xr-x 1 root staff 23 Feb 20 22:47 env
-rwxr-xr-x 1 root staff 23 Feb 20 22:47 ENV
-rwxr-xr-x 1 root staff 23 Feb 20 22:47 head
-rwxr-xr-x 1 root staff 23 Feb 22 02:56 hex
-rwxr-xr-x 1 root staff 23 Feb 22 02:56 hexdump
-rwxr-xr-x 1 root staff 23 Feb 20 22:47 less
-rwxr-xr-x 1 root staff 23 Feb 20 22:47 more
-rwxr-xr-x 1 root staff 23 Feb 20 22:47 nano
-rwxr-xr-x 1 root staff 23 Feb 22 02:56 od
-rwxr-xr-x 1 root staff 23 Feb 20 22:47 printf
-rwxr-xr-x 1 root staff 23 Feb 22 01:43 ptx
-rwxr-xr-x 1 root staff 23 Feb 20 22:47 seq
-rwxr-xr-x 1 root staff 23 Feb 20 22:55 strings
-rwxr-xr-x 1 root staff 23 Feb 20 22:47 tail
-rwxr-xr-x 1 root staff 23 Feb 20 22:47 vi
-rwxr-xr-x 1 root staff 23 Feb 20 22:47 vim
-rwxr-xr-x 1 root staff 23 Feb 22 01:22 xxd
user7@webserver:/usr/local/broke$ cat cat
Nope
user7@webserver:/usr/local/broke$ grep . cat
#!/bin/bash
echo Nope
user7@webserver:/usr/local/broke$ echo $PATH
/usr/local/broke:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
user7@webserver:/usr/local/broke$ cd
user7@webserver:~$ /bin/cat password.txt
EachPeaceLand64
user7@webserver:~$ grep . password.txt
EachPeaceLand64
user7@webserver:~$ exit
logout
Connection to linux.offsec.club closed.
➜  linux.offsec.club
```

----

###### user8

[`CyberChef`](https://gchq.github.io/CyberChef/)

```sh
➜  linux.offsec.club ssh user8@linux.offsec.club
user8@linux.offsec.club's password:
Linux webserver 4.9.0-5-amd64 #1 SMP Debian 4.9.65-3+deb9u2 (2018-01-04) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Jun 30 09:00:45 2018 from 87.78.244.158
user8@webserver:~$ ls -l
total 4
-rw-r--r-- 1 root root        0 Feb 22 01:18 go here => cyberchef
-r-xr-x--- 1 root challenges 29 Feb 21 22:49 password.txt
user8@webserver:~$ file *
go here => cyberchef: empty
password.txt:         ASCII text
user8@webserver:~$ cat password.txt
V2Vhcg==
K5XXK3DE
3ro2uVYXCb
user8@webserver:~$ exit
logout
Connection to linux.offsec.club closed.
➜  linux.offsec.club
```

![](images/2.png)

![](images/3.png)

![](images/4.png)

----

###### user9

[`md5-decrypter`](https://hashkiller.co.uk/md5-decrypter.aspx)

```sh
➜  linux.offsec.club ssh user9@linux.offsec.club
user9@linux.offsec.club's password:
Linux webserver 4.9.0-5-amd64 #1 SMP Debian 4.9.65-3+deb9u2 (2018-01-04) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Fri Jun 29 20:04:28 2018 from 174.115.33.239
user9@webserver:~$ ls -l
total 4
-r-xr-x--- 1 root challenges 33 Feb 21 22:35 password.txt
user9@webserver:~$ cat password.txt
a560b1ca4d01f8ebfe89247ff7df6a88
user9@webserver:~$ exit
logout
Connection to linux.offsec.club closed.
➜  linux.offsec.club
```

![](images/5.png)

----

###### user10

```sh
➜  linux.offsec.club ssh user10@linux.offsec.club
user10@linux.offsec.club's password:
Linux webserver 4.9.0-5-amd64 #1 SMP Debian 4.9.65-3+deb9u2 (2018-01-04) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Jun 30 17:52:16 2018 from 75.140.84.109
user10@webserver:~$ ls -l
total 44
-r-xr-x--- 1 root challenges 37709 Feb 22 00:25 password.txt
-r-xr-x--- 1 root challenges     9 Feb 22 00:16 wordcloud.txt
user10@webserver:~$ cat wordcloud.txt
in order
user10@webserver:~$ cat password.txt
the of and to a in for is on that by this with i you it not or be are from at as your all have new more an was we will home can us if page my has free but our one do no time they site he up may what news out use any see only so his when here who web also now help get pm view c e am been how were me s some its like x than find date back top had list name just over year day into two n re next used go b work last most buy data make them post her city t add such best then jan good well d info high m each she very book r read need many user said de does set mail full map life know way days p part real f item ebay must made off line did send type car take area want dvd l long w code show o even much sign file link open case same uk own both g game care down end h him per big law size art shop text rate usa v form love old john main call non k y why cd save low york man card jobs j food u sale job teen room too join men west look left team box gay week note live june air plan tv yes hot cost la say july test come dec pc cart san play tax less got blog let park side act red give q sell key body few east ii age club z road gift ca hard oct pay four war nov blue al easy fax yet star hand sun rss id keep baby run net term film put co try head cell self away once log sure faq cars tell able fun gold feb sep arts lot ask past due et five upon says mar land done pro st url aug ever ago word bill apr talk via kids true else mark rock bad tips plus auto edit fast fact unit tech meet far en feel bank risk jul town jun girl toys golf loan wide sort half step none paul lake sony fire chat html loss face oil bit base near oh stay turn mean king copy drug pics cash bay ad seen port stop bar dog soon held ny eur mind pdf lost tour menu hope wish role came usr dc mon com fine hour gas six bush pre huge sat zip bid kind move logo nice ok sent band ms lead went fri hi mode fund wed male took inn song cnet ltd los hp late fall idea inc win tool eg bed ip hill maps deal hold tue safe feed pa thu sea cut hall anti tel ship tx paid hair kit tree thus wall ie el ma boy wine vote ways est son rule mac iii gmt max told xml feet bin door cool md fl mb asia uses mr java pass van fees skin prev ads mary il ring pop int iraq boys deep rest hit mm pool mini fish eye pack born race usb ed php etc debt core sets wood msn fee rent las dark le min aid host isbn fair az ohio gets un fat saw dead mike trip pst mi poor eyes farm tom lord sub hear goes led fan wife ten hits zone th cat die jack flat flow dr path kb laws pet guy dev cup vol pp na skip diet army gear lee os lots firm jump dvds ball goal sold wind palm bob fit ex met pain xbox www oral ford edge root au fi ice pink shot nc llc sec bus cold bag po va foot mass ibm rd sc heat wild miss task nor bug mid se soft fuel walk wait rose jim di km pick del ga ac ft angry load tags joe guys drop cds rich im vs ipod ar mo seem sa hire gave ones xp rank kong died inch lab cvs snow eu camp des fill cc lcd wa ave dj gone fort cm wi gene disc ct boat icon ends da cast felt pic soul aids flag nj hr em iv atom rw iron void tag mix disk vhs fix desk dave hong vice ne ray du duty bear gain lack iowa dry spa knew con ups zoom blow clip nt es wire tape spam acid cent null zero gb bc pr roll fr bath aa var font mt beta fail won jazz bags doc wear mom rare bars row oz dual rise usd mg bird lady fans eat dell seat aim bids toll les cape ann tip mine whom ski math ch dan dogs sd moon fly fear rs wars kept hey beat bbc arms tea avg sky utah rom hide toy slow src hip faqs nine eric spot grow dot hiv pda rain onto dsl zum dna diff bass hole pets ride tim sql pair don ss runs yeah ap nm mn nd evil gps op acc euro cap ink peak tn salt bell pin raw gnu jeff ben lane kill aol major ce ages plug cook hat perl lib bike ab utc der lose seek tony kits cam soil wet ram matt fox exit iran arm keys wave holy acts mesh dean poll unix bond pub tm sp jean hop visa nh gun pure lens draw fm warm babe crew legs sam pdt rear node lock mile mens bowl ref tank navy kid db pan ph dish ia pt adam slot psp ha ds gray ea und demo lg hate rice loop nfl gary vary rome arab milk nw boot ff push iso sum misc alan dear oak vat major beer jose jane ps sir earn kim twin ky dont spy br bits lo suit ml chip res sit wow char cs echo que grid voip fig sf kg pull ut nasa tab si css mc nick plot qty pump lp anne bio exam ryan beds pcs grey bold von ag scan vi aged bulk sci edt pmid sin cute ba para cr pg seed ee peer meat ing ks alex bang bone bugs ftp med gate sw tone busy leg neck hd wing abc tiny rail jay gap tube belt er jr biz rob era gcc asp luck dial jet par gang nv cake mad semi andy cafe ken su exp till pen shoe sand joy cpu ran seal sr jon lies pipe nr ill lbs lay lol deck mp thin mph sick dose bet def lets li nl cats ya nba greg epa tr bb ron nz folk org okay hist lift lisa mall dad pat fell yard te av sean pour reg tion dust wiki kent adds nsw ear pci tie ward ian roof kiss ra mod rc bmw rush mpeg yoga lamp rico phil cst http ceo glad wins rack ec rep mit boss ross anna solo tall rm pdas sri toe nova api cf vt wake urw lan sms drum nec foto ease tabs gm ri pine watch tend gulf rt rick cp hunt thai fred dd mill den aud pl burn labs lie crm rf ak fe td amp sb ah sole sm laid clay weak usc blvd amd wise wv odds ns eve marc sons leaf pad ja bs rod cuba hrs silk kate bi sad wolf cal fits kick meal ta hurt pot img slip rpm cuts pee mars tvs egg mhz caps pill lat meta mint gi spin sur wash rev ll aims cl ieee ho corp gt sh soap ae nyc jam axis guns rio hs hero rv punk pi duke ai pace wage ot arc dawn carl coat mrs rica yr app roy ion doll ic peru nike fed reed mice ban temp zus vast ent odd wrap mood angry quiz mx gr ext beam tops amy ts shut ge ncaa thou phd mask ng pe coal cry tt zoo aka tee lion goto xl neil beef cad hats tcp surf major dv dir hook cord val crop tu fy lite major ghz hub rr eng ef ace sing tons sue ep hang gbp lb hood jp chi bt fame af rfc sl seo isp ins eggs hb jpg tc ruby mins ssl stem opt drew flu mlb rap tune corn gp puts grew tin trek oem ir ties rat brad jury dos tail lawn soup byte nose oclc plc juan msg cod thru jews trim cv cb gen espn nhl quit lung ti fc gel todd fw doug sees gs aaa bull cole mart tale lynn bp std docs vid oo coin fake fda cure arch ni hdtv asin bomb harm thy deer tri pal um ye fs nn mat oven ted noon gym kde vb cams joel yo proc tan fx mate dl chef isle slim luke comp alt pie ls cbs pete spec bow penn midi tied hon dale oils sept unto lt atm eq pays je lang stud fold uv cms sg vic pos phys pole mega bend moms glen nav cab fa ist lips pond lc dam cnn lil das tire chad sys josh drag icq ripe rely scsi cu dns pty ws nuts nail span sox joke univ tub pads inns cups ash ali np foam tft jvc poem dt cgi asks bean bias por mem gc tap ci swim nano yn vii bee loud rats cfr stat cruz bios pmc thee nb ruth pray pope jeep bare hung mba pit mono tile rx apps mag gsm ddr rec ciao knee prep pb chem ton oe gif pros cant jd gpl irc wy dm sara bra joan duck phi mls cow dive cet fiji audi raid ppc volt div dirt jc acer dist ons geek sink grip avi watt pins reno ide polo rpg horn pd prot frog logs tgp leo diy snap arg ur geo doe jpeg ati wal swap abs flip sim rna buzz nuke rid boom calm fork troy ln uc rip zope gmbh buf ld sims tray sol sage eco bat lip sap suse mf cave wool mw nu ict dp eyed ou grab oops xi sku ht za trap fool ve karl dies pts rh rrp fg jail ooo hz ipaq bk comm nhs aye lace ste ugly hart ment col dx sk biol yu rows sq oc aj treo gods une tex cia poly ears dod wp fist neo mere cons dig taxi om nat tp jm dpi gis loc worn shaw vp expo cn deny bali judy trio cube rugs fate gui gras ver rn rim zen dis kay oval cg soma ser href benz wifi tier fwd earl aus hwy guam cite nam ix gdp pig mess lit una ada tb rope dump yrs foo gba bm hose sig duo fog str pubs vip yea mild fur tar rj soc clan sync mesa rug ka hull dem wav shed memo ham tide funk fbi reel rp bind rand buck eh tba sie usgs acre lows aqua chen emma eva pest hc rca fp reef gst bon jj chan mas beth len kai dom jill sofa obj dans viii jar ev tent dept hack dare hawk lamb cos pac rl erp gl ui dh vpn fcc eds ro df junk wax lucy hans poet epic nut sake sans irs lean bye cdt ana dude luis ez pf uw alto eau bd mil gore cult dash cage divx hugh lap jake eval ping flux sao muze oman gmc hh rage adsl uh prix fd bo avon rays asn walt acne libs undo wm pk dana halo ppm ant gays apt exec inf eos vcr uri gem maui psi pct wb vids yale sn qld pas dk doom owen bite issn myth gig sas fu weed oecd dice quad dock mods hint msie wn liz ccd sv buys pork zu barn llp boc fare dg asus vg bald fuji leon mold dame fo herb tmp alot ate idle fin io mud uni ul ol js pn cove casa mu eden incl ala hq dip nbc reid wt flex rosa hash lazy mv mpg carb cas cio dow rb upc dui pens yen mh worm lid deaf mats pvc blah mime feof usda keen peas urls enb gg og ko owns til wto hay ww gd zinc guru isa levy grad bras pix mic kyle bw mj pale gaps tear lf ata nil nest pam nato cop gale dim stan idol wc mai hk abu moss ty cork cj mali mtv dome leu heel yang qc lou pgp aw sip tf pj cw wr dumb rg bl vc dee wx mae mel feat ntsc sic usps bg seq conf glow wma cir oaks erik hu acm kw paso norm ips dsc ware mia wan jade foul keno gtk seas ru pose mrna goat ira sen sail dts qt sega cdna major pod wu bolt gage lu dat soa urge smtp kurt neon ours lone cope lm lime kirk bool cho wit bbs spas ind jets qui intl cz yarn knit mug hl ob pike ids hugo gzip ctrl bent laos the of and to a in for is on that by this with i you it not or be are from at as your all have new more an was we will home can us if page my has free but our one do no time they site he up may what news out use any see only so his when here who web also now help get pm view c e am been how were me s some its like x than find date back top had list name just over year day into two n re next used go b work last most buy data make them post her city t add such best then jan good well d info high m each she very book r read need many user said de does set mail full map life know way days p part real f item ebay must made off line did send type car take area want dvd l long w code show o even much sign file link open case same uk own both g game care down end h him per big law size art shop text rate usa v form love old john main call non k y why cd save low york man card jobs j food u sale job teen room too join men west look left team box gay week note live june air plan tv yes hot cost la say july test come dec pc cart san play tax less got blog let park side act red give q sell key body few east ii age club z road gift ca hard oct pay four war nov blue al easy fax major yet star hand sun rss id keep baby run net term film put co try head cell self away once log sure faq cars tell able fun gold feb sep arts lot ask past due et five upon says mar land done pro st url aug ever ago word bill apr talk via kids true else mark rock bad tips plus auto edit fast fact unit tech meet far en feel bank risk jul town jun girl toys golf loan wide sort half step none paul lake sony fire chat html loss face oil bit base near oh stay turn mean king copy drug pics cash bay ad seen port stop bar dog soon held ny eur mind pdf lost tour menu hope wish role came usr dc mon com fine hour gas six bush pre huge sat zip bid kind move logo nice ok sent band ms lead went fri hi mode fund wed male took watch inn song cnet ltd los hp late fall idea inc win tool eg bed ip hill maps deal hold tue safe feed pa thu sea cut hall anti tel ship tx paid hair kit tree thus wall ie el ma boy wine vote ways est son rule mac iii gmt max told xml feet bin door cool md fl mb asia uses mr java pass van fees skin prev ads mary il ring pop int iraq boys deep rest hit mm pool mini fish eye pack born race usb ed php etc debt core sets wood msn fee rent las dark le min aid host isbn fair az ohio gets un fat saw dead mike trip pst mi poor eyes farm tom lord sub hear goes led fan wife ten hits zone th cat die jack flat flow dr path kb laws pet guy dev cup vol pp na skip diet army gear lee os lots firm jump dvds ball goal sold wind palm bob fit ex met pain xbox www oral ford edge root au fi ice pink shot nc llc sec bus cold bag po va foot mass ibm rd sc heat wild miss task nor bug mid se soft fuel walk wait rose jim di km pick del ga ac ft load tags joe guys drop cds rich im vs ipod ar mo seem sa hire gave ones xp rank kong died inch lab cvs snow eu camp des fill cc lcd wa ave dj gone fort cm wi gene disc ct boat icon ends da cast felt pic soul aids flag nj hr em iv atom rw iron void tag mix disk vhs fix desk dave hong vice ne ray du duty bear gain lack iowa dry spa knew con ups zoom blow clip nt es wire tape spam acid cent null zero gb bc pr roll fr bath aa var font mt beta fail won jazz bags doc wear mom rare bars row oz dual rise usd mg bird lady fans eat dell seat aim bids toll les cape ann major tip mine whom ski math ch dan dogs sd moon fly fear rs wars kept hey beat bbc arms tea avg sky utah rom hide toy slow src hip faqs nine eric spot grow dot hiv pda rain onto dsl zum dna diff bass hole pets ride tim sql pair don ss runs yeah ap nm mn nd evil gps op acc euro cap ink peak tn salt bell pin raw gnu jeff ben lane kill aol ce ages plug cook hat perl lib bike ab utc der lose seek tony kits cam soil wet ram matt fox exit iran arm keys wave holy acts mesh dean poll unix bond pub tm sp jean hop visa nh gun pure lens draw fm warm babe crew legs sam pdt rear node lock mile mens bowl ref tank navy kid db pan ph dish ia pt adam slot psp ha ds gray ea und demo lg hate rice loop nfl gary vary rome arab milk nw boot ff push iso sum misc alan dear oak vat beer jose jane ps sir earn kim twin ky dont spy br bits lo suit ml chip res sit wow char cs echo que grid voip fig sf kg pull ut nasa tab si css mc nick plot qty pump lp anne bio exam ryan beds pcs grey bold von ag scan vi aged bulk sci edt pmid sin cute ba para cr pg seed ee peer meat ing ks alex bang bone bugs ftp med gate sw tone busy leg neck hd wing abc tiny rail jay gap tube belt er jr biz rob era gcc asp luck dial jet par gang nv cake mad semi andy cafe ken su exp till pen shoe sand joy cpu ran seal sr jon lies pipe nr ill lbs lay lol deck mp thin mph sick dose bet def lets li nl cats ya nba greg epa tr bb ron nz folk org okay hist lift lisa mall dad pat fell yard te av sean pour reg tion dust wiki kent adds nsw ear pci tie ward ian roof kiss ra mod rc bmw rush mpeg yoga lamp rico phil cst http ceo glad wins rack ec rep mit boss ross anna solo tall rm pdas sri toe nova api cf vt wake urw lan sms drum nec foto ease tabs gm ri pine tend gulf rt rick cp hunt thai fred dd mill den aud pl burn labs lie crm rf ak fe td amp sb ah sole sm angry laid clay weak usc blvd amd wise wv odds ns eve marc sons leaf pad ja bs rod cuba hrs silk kate bi sad wolf cal fits kick meal ta hurt pot img slip rpm cuts pee mars tvs egg mhz caps pill lat meta mint gi spin sur wash rev ll aims cl ieee ho corp gt sh soap ae nyc jam axis guns rio hs hero rv punk pi duke ai pace wage ot arc dawn carl coat mrs rica yr app roy ion doll ic peru nike fed reed mice ban temp zus vast ent odd wrap mood quiz mx gr ext beam tops amy ts shut ge ncaa thou phd mask ng pe coal cry tt zoo aka tee lion goto xl neil beef cad hats tcp surf dv dir hook cord val crop tu fy lite ghz hub rr eng ef ace sing tons sue ep hang gbp lb hood jp chi bt fame af rfc sl seo isp ins eggs hb jpg tc ruby mins ssl stem opt drew flu mlb rap tune corn gp puts grew tin trek oem ir ties rat brad jury dos tail lawn soup byte nose oclc plc juan msg cod thru jews trim cv cb gen espn nhl quit lung ti fc gel todd fw doug sees gs aaa bull cole mart tale lynn bp std docs vid oo coin fake fda cure arch ni hdtv asin bomb harm thy deer tri pal um ye fs nn mat oven ted noon watch gym kde vb cams joel yo proc tan fx mate dl chef isle slim luke comp alt pie ls cbs pete spec bow penn midi tied hon dale oils sept unto lt atm eq pays je lang stud fold uv cms sg vic pos phys pole mega bend moms glen nav cab fa ist lips pond lc dam cnn lil das tire chad sys josh drag icq ripe rely scsi cu dns pty ws nuts nail span sox joke univ tub pads inns cups ash ali np foam tft jvc poem dt cgi asks bean bias por mem gc tap ci swim nano yn vii bee loud rats cfr stat cruz bios pmc thee nb ruth pray pope jeep bare hung mba pit mono tile rx apps mag gsm ddr rec ciao knee prep pb chem ton oe gif pros cant jd gpl irc wy dm sara bra joan duck phi mls cow dive cet fiji audi raid ppc volt div dirt jc acer dist ons geek sink grip avi watt pins reno ide polo rpg horn pd prot frog logs tgp leo diy snap arg ur geo doe jpeg ati wal swap abs flip sim rna buzz nuke rid boom calm fork troy ln uc rip zope gmbh buf ld sims tray sol sage eco bat lip sap suse mf cave wool mw nu ict dp eyed ou grab oops xi sku ht za trap fool ve karl dies pts rh rrp fg jail ooo hz ipaq bk comm nhs aye lace ste ugly hart ment col dx sk biol yu rows sq oc aj treo gods une tex cia poly ears dod wp fist neo mere cons dig taxi om nat tp jm dpi gis loc worn shaw vp expo cn deny bali judy trio cube rugs fate gui gras ver rn rim zen dis kay oval cg soma ser href benz wifi tier fwd earl aus hwy guam cite nam ix gdp pig mess lit una ada tb rope dump yrs foo gba bm hose sig duo fog str pubs vip yea mild fur tar rj soc clan sync mesa rug ka hull dem wav shed memo ham tide funk fbi reel rp bind rand buck eh tba sie usgs acre lows aqua chen emma eva pest hc rca fp reef gst bon jj chan mas beth len kai dom jill sofa obj dans viii jar ev tent dept hack dare hawk lamb cos pac rl erp gl ui dh vpn fcc eds ro df junk wax lucy hans poet epic nut sake sans irs lean bye cdt ana dude luis ez pf uw alto eau bd mil gore cult dash cage divx hugh lap jake eval ping flux sao muze oman gmc hh rage adsl uh prix fd bo avon rays asn walt acne libs undo wm pk dana halo ppm ant gays apt exec inf eos vcr uri gem maui psi pct wb vids yale sn qld pas dk doom owen bite issn myth gig sas fu weed oecd dice quad dock mods hint msie wn liz ccd sv buys pork zu barn llp boc fare dg asus vg bald fuji leon mold dame fo herb tmp alot ate idle fin io mud uni ul ol js pn cove casa mu eden incl ala hq dip nbc reid wt flex rosa hash lazy mv mpg carb cas cio dow rb upc dui pens yen mh worm lid deaf mats pvc blah mime feof usda keen peas urls enb gg og ko owns til wto hay ww gd zinc guru isa levy grad bras pix mic kyle bw mj pale gaps tear lf ata nil nest pam nato cop gale dim stan idol wc mai hk abu moss ty cork cj mali mtv dome leu heel yang qc lou pgp aw sip tf pj cw wr dumb rg bl vc dee wx mae mel feat ntsc sic usps bg seq conf glow wma cir oaks erik hu acm kw paso norm ips dsc ware mia wan jade foul keno gtk seas ru pose mrna goat ira sen sail dts qt sega cdna pod wu bolt gage lu dat soa urge smtp kurt neon ours lone cope lm lime kirk bool cho wit bbs spas ind jets qui intl cz yarn knit mug hl ob pike ids hugo gzip ctrl bent laos the of and to a in for is on that by this with i you it not or be are from at as your all have new more an was we will home can us if page my has free but our one do no time they site he up may what news out use any see only so his when here who web also now help get pm view c e am been how were me s some its like x than find date back top had list name just over year day into two n re next used go b work last most buy data make them post her city t add such best then jan good well d info high m each she very book r read need many user said de does set mail full map life know way days p part real f item ebay must made off line did send type car take area want dvd l long w code show o even much sign file link open case same uk own both g game care down end h him per big law size art shop text rate usa v form love old john main call non k y why cd save low york man card jobs j food u sale job teen room too join men west look left team box gay week note live june air plan tv yes hot cost la say july test come dec pc cart san play tax less got blog let park side act red give q sell key body few east ii age club z road gift ca hard oct pay four war nov blue al easy fax yet star hand sun rss id keep baby angry run net term film put co try head cell self away once log sure faq cars tell able fun gold feb sep arts lot ask past due et five upon says mar land done pro st url aug ever ago word bill apr talk via kids true else mark rock bad tips plus auto edit fast fact unit tech meet far en feel bank risk jul town jun girl toys golf loan wide sort half step none paul lake sony fire chat html loss face oil bit base near oh stay turn mean king copy drug pics cash bay ad seen port stop bar dog soon held ny eur mind pdf lost tour menu hope wish role came usr dc mon com fine hour gas six bush pre huge sat zip bid kind move logo nice ok sent band ms lead went fri hi mode fund wed male took inn song cnet ltd los hp late fall idea inc win tool eg bed ip hill maps deal hold tue safe feed pa thu sea cut hall anti tel ship tx paid hair kit tree thus wall ie el ma boy wine vote ways est son rule mac iii gmt max told xml feet bin door cool md fl mb asia uses mr java pass van fees skin prev ads mary il ring pop int iraq boys deep rest hit mm pool mini fish eye pack born race usb ed php etc debt core sets wood msn fee rent las dark le min aid host isbn fair az ohio gets un fat saw dead mike trip pst mi poor eyes farm tom lord sub hear goes led fan wife ten hits zone th cat die jack flat flow dr path kb laws pet guy dev cup vol pp na skip diet army gear lee os lots firm jump dvds ball goal sold wind palm bob fit ex met pain xbox www oral ford edge root au fi ice pink shot nc llc sec bus cold bag po va foot mass ibm rd sc heat wild miss task nor bug mid se soft fuel walk wait rose jim di km pick del ga ac ft load tags joe guys drop cds rich im vs ipod ar mo seem sa hire gave ones xp rank kong died inch lab cvs snow eu camp des fill cc lcd wa ave dj gone fort cm wi gene disc ct boat icon ends da cast felt pic soul aids flag nj hr em iv atom rw iron void tag mix disk vhs fix desk dave hong vice ne ray du duty bear gain lack iowa dry spa knew con ups zoom blow clip nt es wire tape spam acid cent null zero gb bc pr roll fr bath aa var font mt beta fail won jazz bags doc wear mom rare bars row oz dual rise usd mg bird lady fans eat dell seat aim bids toll les cape ann tip mine whom ski math ch dan dogs sd moon fly fear rs wars kept hey beat bbc arms tea avg sky utah rom hide toy slow src hip faqs nine eric spot grow dot hiv pda rain onto dsl zum dna diff bass hole pets ride tim sql pair don ss runs yeah ap nm mn nd evil gps op acc euro cap ink peak tn salt bell pin raw gnu jeff ben lane kill aol ce ages plug cook hat perl lib bike ab utc der lose seek tony kits cam soil wet ram matt fox exit iran arm keys wave holy acts mesh dean poll unix bond pub tm sp jean hop visa nh gun pure lens draw fm warm babe crew legs sam pdt rear node lock mile mens bowl ref tank navy kid db pan ph dish ia pt adam slot psp ha ds gray ea und demo lg hate rice loop nfl gary vary rome arab milk nw boot ff push iso sum misc alan dear oak vat beer jose jane ps sir earn kim twin ky dont spy br bits lo suit ml chip res sit wow char cs echo que grid voip fig sf kg pull ut nasa tab si css mc nick plot qty pump lp anne bio exam ryan beds pcs grey bold von ag scan vi aged bulk sci edt pmid sin cute ba angry para cr pg seed ee peer meat ing ks alex bang bone bugs ftp med gate sw tone busy leg neck hd wing abc tiny rail jay gap tube belt er jr biz rob era gcc asp luck dial jet par gang nv cake mad semi andy cafe ken su exp till pen shoe sand joy cpu ran seal sr jon lies pipe nr ill lbs lay lol deck mp thin mph sick dose bet def lets li nl cats ya nba greg epa tr bb ron nz folk org okay hist lift lisa mall dad pat fell yard te av sean pour reg tion dust wiki kent adds nsw ear pci tie ward ian roof kiss ra mod rc bmw rush mpeg yoga lamp rico phil cst http ceo glad wins rack ec rep mit boss ross anna solo tall rm pdas sri toe nova api cf vt wake urw lan sms drum nec foto ease tabs gm ri pine tend gulf rt rick cp hunt thai fred dd mill den aud pl burn labs lie crm rf ak fe td amp sb ah sole sm laid clay weak usc blvd amd wise wv odds ns eve marc sons leaf pad ja bs rod cuba hrs silk kate bi sad wolf cal fits kick meal ta hurt pot img slip rpm cuts pee mars tvs egg mhz caps pill lat meta mint gi spin sur wash rev ll aims cl ieee ho corp gt sh soap ae nyc jam axis guns rio hs hero rv punk pi duke ai pace wage ot arc dawn carl coat mrs rica yr app roy ion doll ic peru nike fed reed mice ban temp zus vast ent odd wrap mood quiz mx gr ext beam tops amy ts shut ge ncaa thou phd mask ng pe coal cry tt zoo aka tee lion goto xl neil beef cad hats tcp surf dv dir hook cord val crop tu fy lite ghz hub rr eng ef ace sing tons sue ep hang gbp lb hood jp chi bt fame af rfc sl seo isp ins eggs hb jpg tc ruby mins ssl stem opt drew flu mlb rap tune corn gp puts grew tin trek oem ir ties rat brad jury dos tail lawn soup byte nose oclc plc juan msg cod thru jews trim cv cb gen espn nhl quit lung ti fc gel todd fw doug sees gs aaa bull cole mart tale lynn bp std docs vid oo coin fake fda cure arch ni hdtv asin bomb harm thy deer tri pal um ye fs nn mat oven ted noon gym kde vb cams joel yo proc tan fx mate dl chef isle slim luke comp alt pie ls cbs pete spec bow penn midi tied hon dale oils sept unto lt atm eq pays je lang stud fold uv cms sg vic pos phys pole mega bend moms glen nav cab fa ist lips pond lc dam cnn lil das tire chad sys josh drag icq ripe rely scsi cu dns pty ws nuts nail span sox joke univ tub pads inns cups ash ali np foam tft jvc poem watch dt cgi asks bean bias por mem gc tap ci swim nano yn vii bee loud rats cfr stat cruz bios pmc thee nb ruth pray pope jeep bare hung mba pit mono tile rx apps mag gsm ddr rec ciao knee prep pb chem ton oe gif pros cant jd gpl irc wy dm sara bra joan duck phi mls cow dive cet fiji audi raid ppc volt div dirt jc acer dist ons geek sink grip avi watt pins reno ide polo rpg horn pd prot frog logs tgp leo diy snap arg ur geo doe jpeg ati wal swap abs flip sim rna buzz nuke rid boom calm fork troy ln uc rip zope gmbh buf ld sims tray sol sage eco bat lip sap suse mf cave wool mw nu ict dp eyed ou grab oops xi sku ht za trap fool ve karl dies pts rh rrp fg jail ooo hz ipaq bk comm nhs aye lace ste ugly hart ment col dx sk biol yu rows sq oc aj treo gods une tex cia poly ears dod wp fist neo mere cons dig taxi om nat tp jm dpi gis loc worn shaw vp expo cn deny bali judy trio cube rugs fate gui gras ver rn rim zen dis kay oval cg soma ser href benz wifi tier fwd earl aus hwy guam cite nam ix gdp pig mess lit una ada tb rope dump yrs foo gba bm hose sig duo fog str pubs vip yea mild fur tar rj soc clan sync mesa rug ka hull dem wav shed memo ham tide funk fbi reel rp bind rand buck eh tba sie usgs acre lows aqua chen emma eva pest hc rca fp reef gst bon jj chan mas beth len kai dom jill sofa obj dans viii jar ev tent dept hack dare hawk lamb cos pac rl erp gl ui dh vpn fcc eds ro df junk wax lucy hans poet epic nut sake sans irs lean bye cdt ana dude luis ez pf uw alto eau bd mil gore cult dash cage divx hugh lap jake eval ping flux sao muze oman gmc hh rage adsl uh prix fd bo avon rays asn walt acne libs undo wm pk dana halo ppm ant gays apt exec inf eos vcr uri gem maui psi pct wb vids yale sn qld pas dk doom owen bite issn myth gig sas fu weed oecd dice quad dock mods hint msie wn liz ccd sv buys pork zu barn llp boc fare dg asus vg bald fuji leon mold dame fo herb tmp alot ate idle fin io mud uni ul ol js pn cove casa mu eden incl ala hq dip nbc reid wt flex rosa hash lazy mv mpg carb cas cio dow rb upc dui pens yen mh worm lid deaf mats pvc blah mime feof usda keen peas urls enb gg og ko owns til wto hay ww gd zinc guru isa levy grad bras pix mic kyle bw mj pale major gaps tear lf ata nil nest pam nato cop gale dim stan idol wc mai hk abu moss ty cork cj mali mtv dome leu heel yang qc lou pgp aw sip tf pj cw wr dumb rg bl vc dee wx mae mel feat ntsc sic usps bg seq conf glow wma cir oaks erik hu acm kw paso norm ips dsc ware mia wan jade foul keno gtk seas ru pose mrna goat ira sen sail dts qt sega cdna pod wu bolt gage lu dat soa urge smtp kurt neon ours lone cope lm lime kirk bool cho wit bbs spas ind jets qui intl cz yarn knit mug hl ob pike ids hugo gzip ctrl bent laos the of and to a in for is on that by this with i you it not or be are from at as your all have new more an was we will home can us if page my has free but our one do no time they site he up may what news out use any see only so his when here who web also now help get pm view c e am been how were me s some its like x than find date back top had list name just over year day into two n re next used go b work last most buy data make them post her city t add such best then jan good well d info high m each she very book r read need many user said de does set mail full map life know way days p part real f item ebay must made off line did send type car take area want dvd l long w code show o even much sign file link open case same uk own both g game care down end h him per big law size art shop text rate usa v form love old john main call non k y why cd save low york man card jobs j food u sale job teen room too join men west look left team box gay week note live june air plan tv yes hot cost la say july test come dec pc cart san play tax less got blog let park side act red give q sell key body few east ii age club z road gift ca hard oct pay angry four war nov blue al easy fax yet star hand sun rss id keep baby run net term film put co try head cell self away once log sure faq cars tell able fun gold feb sep arts lot ask past due et five upon says mar land done pro st url aug ever ago word bill apr talk via kids true else mark rock bad tips plus auto edit fast fact unit tech meet far en feel bank risk jul town jun girl toys golf loan wide sort half step none paul lake sony fire chat html loss face oil bit base near oh stay turn mean king copy drug pics cash bay ad seen port stop bar dog soon held ny eur mind pdf lost tour menu hope wish role came usr dc mon com fine hour gas six bush pre huge sat zip bid kind move logo nice ok sent band ms lead went fri hi mode fund wed male took inn song cnet ltd los hp late fall idea inc win tool eg bed ip hill maps deal hold tue safe feed pa thu sea cut hall anti tel ship tx paid hair kit tree thus wall ie el ma boy wine vote ways est son rule mac iii gmt max told xml feet bin door cool md fl mb asia uses mr java pass van fees skin prev ads mary il ring pop int iraq boys deep rest hit mm pool mini fish eye pack born race usb ed php etc debt core sets wood msn fee rent las dark le min aid host isbn fair az ohio gets un fat saw dead mike trip pst mi poor eyes farm tom lord sub hear goes led fan wife ten hits zone th cat die jack flat flow dr path kb laws pet guy dev cup vol pp na skip diet army gear lee os lots firm jump dvds ball goal sold wind palm bob fit ex met pain xbox www oral ford edge root au fi ice pink shot nc llc sec bus cold bag po va foot mass ibm rd sc heat wild miss task nor bug mid se soft fuel walk wait rose jim di km pick del ga ac ft load tags joe guys drop cds rich im vs ipod ar mo seem sa hire gave ones xp rank kong died inch lab cvs snow eu camp des fill cc lcd wa ave dj gone fort cm wi gene disc ct boat icon ends da cast felt pic soul aids flag nj hr em iv atom rw iron void tag mix disk vhs fix desk dave hong vice ne ray du duty bear gain lack iowa dry spa knew con ups zoom blow clip nt es wire tape spam acid cent null zero gb bc pr roll fr bath aa var font mt beta fail won jazz bags doc wear mom rare bars row oz dual rise usd mg bird lady fans eat dell seat aim bids toll les cape ann tip mine whom ski math ch dan dogs sd moon fly fear rs wars kept hey beat bbc arms tea avg sky utah rom hide toy slow src hip faqs watch nine eric spot grow dot hiv pda rain onto dsl zum dna diff bass hole pets ride tim sql pair don ss runs yeah ap nm mn nd evil gps op acc euro cap ink peak tn salt bell pin raw gnu jeff ben lane kill aol ce ages plug cook hat perl lib bike ab utc der lose seek tony kits cam soil wet ram matt fox exit iran arm keys wave holy acts mesh dean poll unix bond pub tm sp jean hop visa nh gun pure lens draw fm warm babe crew legs sam pdt rear node lock mile mens bowl ref tank navy kid db pan ph dish ia pt adam slot psp ha ds gray ea und demo lg hate rice loop nfl gary vary rome arab milk nw boot ff push iso sum misc alan dear oak vat beer jose jane angry ps sir earn kim twin ky dont spy br bits lo suit ml chip res sit wow char cs echo que grid voip fig sf kg pull ut nasa tab si css mc nick plot qty pump lp anne bio exam ryan beds pcs grey bold von ag scan vi aged bulk sci edt pmid sin cute ba para cr pg seed ee peer meat ing ks alex bang bone bugs angry ftp med gate sw tone busy leg neck hd wing abc tiny rail jay gap tube belt er jr biz rob era gcc asp luck dial jet par gang nv cake mad semi andy cafe ken su exp till pen shoe sand joy cpu ran seal sr jon lies pipe nr ill lbs lay lol deck mp thin mph sick dose bet def lets li nl cats ya nba greg epa tr bb ron nz folk org okay hist lift lisa mall dad pat fell yard te av sean pour reg tion dust wiki kent adds nsw ear pci tie ward ian roof kiss ra mod rc bmw rush mpeg yoga lamp rico phil cst http ceo glad wins rack ec rep mit boss ross anna solo tall rm pdas sri toe nova api cf vt wake urw lan sms drum nec foto ease tabs gm ri pine tend gulf rt rick cp hunt thai fred dd mill den aud pl burn labs lie crm rf ak fe td amp sb ah sole sm laid clay weak usc blvd amd wise wv odds ns eve marc sons leaf pad ja bs rod cuba hrs silk kate bi sad wolf cal fits kick meal ta hurt pot img slip rpm cuts pee mars tvs egg mhz caps pill lat meta mint gi spin sur wash rev ll aims cl ieee ho corp gt sh soap ae nyc jam axis guns rio hs hero rv punk pi duke ai pace wage ot arc dawn carl coat mrs rica yr app roy ion doll ic peru nike fed reed mice ban temp zus vast ent odd wrap mood quiz mx gr ext beam tops amy ts shut ge ncaa thou phd mask ng pe coal cry tt zoo aka tee lion goto xl neil beef cad hats tcp surf dv dir hook cord val crop tu fy lite ghz hub rr eng ef ace sing tons sue ep hang gbp lb hood jp chi bt fame af rfc sl seo isp ins eggs hb jpg tc ruby mins ssl stem opt drew flu mlb rap tune corn gp puts grew tin trek oem ir ties rat brad jury dos tail lawn soup byte nose oclc plc juan msg cod thru jews trim cv watch cb gen espn nhl quit lung ti fc gel todd fw doug sees gs aaa bull cole mart tale lynn bp std docs vid oo coin fake fda cure arch ni hdtv asin bomb harm thy deer tri pal um ye fs nn mat oven watch ted noon gym kde vb cams joel yo proc tan fx mate dl chef isle slim luke comp alt pie ls cbs pete spec bow penn midi tied hon dale oils sept unto lt atm eq pays je lang stud fold uv cms sg vic pos phys pole mega bend moms glen nav cab fa ist lips pond lc dam cnn lil das tire chad sys josh drag icq ripe rely scsi cu dns pty ws nuts nail span sox joke univ tub pads inns cups ash ali np foam tft jvc poem dt cgi asks bean bias por mem gc tap ci swim nano yn vii bee loud rats cfr stat cruz bios pmc thee nb ruth pray pope jeep bare hung mba pit mono tile rx apps mag gsm ddr rec ciao knee prep pb chem ton oe gif pros cant jd gpl irc wy dm sara bra joan duck phi mls cow dive cet fiji audi raid ppc volt div dirt jc acer dist ons geek sink grip avi angry watt pins reno ide polo rpg horn pd prot frog logs tgp leo diy snap arg ur geo doe jpeg ati wal swap abs flip sim rna buzz nuke rid boom calm fork troy ln uc rip zope gmbh buf ld sims tray sol sage eco bat lip sap suse mf cave wool mw nu ict dp eyed ou grab oops xi sku ht za trap fool ve karl dies pts rh rrp fg jail ooo hz ipaq bk comm nhs aye lace ste ugly hart ment col dx sk biol yu rows sq oc aj treo gods une tex cia poly ears dod wp fist neo mere cons dig taxi om nat tp jm dpi gis loc worn shaw vp expo cn deny bali judy trio cube rugs fate gui gras ver rn rim zen dis kay oval cg soma ser href benz wifi tier fwd earl aus hwy guam cite nam ix gdp pig mess lit una ada tb rope dump yrs foo gba bm hose sig duo fog str pubs vip yea mild fur tar rj soc clan sync mesa rug ka hull dem wav shed memo ham tide funk fbi reel rp bind rand buck eh tba sie usgs acre lows aqua chen emma eva pest hc rca fp reef gst bon jj chan mas beth len kai dom angry jill sofa obj dans viii jar ev tent dept hack dare hawk lamb cos pac rl erp gl ui dh vpn fcc eds ro df junk wax lucy hans poet epic nut sake sans irs lean bye cdt ana dude luis ez pf uw alto eau bd mil gore cult dash cage divx hugh lap jake eval ping flux sao muze oman gmc hh rage adsl uh prix fd bo avon rays asn walt acne libs undo wm pk dana halo ppm ant gays apt exec inf eos vcr uri gem maui psi pct wb vids yale sn qld pas dk doom owen bite issn myth gig sas fu weed oecd dice quad dock mods hint msie wn liz ccd sv buys pork zu barn llp boc fare dg asus vg bald fuji leon mold dame fo herb tmp alot ate idle fin io mud uni ul ol js pn cove casa mu eden incl ala hq dip nbc reid wt flex rosa hash lazy mv mpg carb cas cio dow rb upc dui pens yen mh worm lid deaf mats pvc blah mime feof usda keen peas urls enb gg og ko owns til wto hay ww gd zinc guru isa levy grad bras pix mic kyle bw mj pale gaps tear lf ata nil nest pam nato cop gale dim stan idol wc mai hk abu moss ty cork cj mali mtv dome leu heel yang qc lou pgp aw sip tf pj cw wr dumb rg bl vc dee wx mae mel feat ntsc sic usps bg seq conf glow wma cir oaks erik hu acm kw paso norm ips dsc ware mia wan jade foul keno gtk seas ru pose mrna goat ira sen sail dts qt sega cdna pod wu bolt gage lu dat soa urge smtp kurt neon ours lone cope lm lime kirk bool cho wit bbs spas ind jets qui intl cz yarn knit mug hl ob pike ids hugo gzip ctrl bent laos
user10@webserver:~$
user10@webserver:~$ cat password.txt | tr " " "\n" | sort | uniq -c
      4 a
      4 aa
      4 aaa
      4 ab
      4 abc
      4 able
      4 abs
      4 abu
      4 ac
      4 acc
      4 ace
      4 acer
      4 acid
      4 acm
      4 acne
      4 acre
      4 act
      4 acts
      4 ad
      4 ada
      4 adam
      4 add
      4 adds
      4 ads
      4 adsl
      4 ae
      4 af
      4 ag
      4 age
      4 aged
      4 ages
      4 ago
      4 ah
      4 ai
      4 aid
      4 aids
      4 aim
      4 aims
      4 air
      4 aj
      4 ak
      4 aka
      4 al
      4 ala
      4 alan
      4 alex
      4 ali
      4 all
      4 alot
      4 also
      4 alt
      4 alto
      4 am
      4 amd
      4 amp
      4 amy
      4 an
      4 ana
      4 and
      4 andy
     10 angry
      4 ann
      4 anna
      4 anne
      4 ant
      4 anti
      4 any
      4 aol
      4 ap
      4 api
      4 app
      4 apps
      4 apr
      4 apt
      4 aqua
      4 ar
      4 arab
      4 arc
      4 arch
      4 are
      4 area
      4 arg
      4 arm
      4 arms
      4 army
      4 art
      4 arts
      4 as
      4 ash
      4 asia
      4 asin
      4 ask
      4 asks
      4 asn
      4 asp
      4 asus
      4 at
      4 ata
      4 ate
      4 ati
      4 atm
      4 atom
      4 au
      4 aud
      4 audi
      4 aug
      4 aus
      4 auto
      4 av
      4 ave
      4 avg
      4 avi
      4 avon
      4 aw
      4 away
      4 axis
      4 aye
      4 az
      4 b
      4 ba
      4 babe
      4 baby
      4 back
      4 bad
      4 bag
      4 bags
      4 bald
      4 bali
      4 ball
      4 ban
      4 band
      4 bang
      4 bank
      4 bar
      4 bare
      4 barn
      4 bars
      4 base
      4 bass
      4 bat
      4 bath
      4 bay
      4 bb
      4 bbc
      4 bbs
      4 bc
      4 bd
      4 be
      4 beam
      4 bean
      4 bear
      4 beat
      4 bed
      4 beds
      4 bee
      4 beef
      4 been
      4 beer
      4 bell
      4 belt
      4 ben
      4 bend
      4 bent
      4 benz
      4 best
      4 bet
      4 beta
      4 beth
      4 bg
      4 bi
      4 bias
      4 bid
      4 bids
      4 big
      4 bike
      4 bill
      4 bin
      4 bind
      4 bio
      4 biol
      4 bios
      4 bird
      4 bit
      4 bite
      4 bits
      4 biz
      4 bk
      4 bl
      4 blah
      4 blog
      4 blow
      4 blue
      4 blvd
      4 bm
      4 bmw
      4 bo
      4 boat
      4 bob
      4 boc
      4 body
      4 bold
      4 bolt
      4 bomb
      4 bon
      4 bond
      4 bone
      4 book
      4 bool
      4 boom
      4 boot
      4 born
      4 boss
      4 both
      4 bow
      4 bowl
      4 box
      4 boy
      4 boys
      4 bp
      4 br
      4 bra
      4 brad
      4 bras
      4 bs
      4 bt
      4 buck
      4 buf
      4 bug
      4 bugs
      4 bulk
      4 bull
      4 burn
      4 bus
      4 bush
      4 busy
      4 but
      4 buy
      4 buys
      4 buzz
      4 bw
      4 by
      4 bye
      4 byte
      4 c
      4 ca
      4 cab
      4 cad
      4 cafe
      4 cage
      4 cake
      4 cal
      4 call
      4 calm
      4 cam
      4 came
      4 camp
      4 cams
      4 can
      4 cant
      4 cap
      4 cape
      4 caps
      4 car
      4 carb
      4 card
      4 care
      4 carl
      4 cars
      4 cart
      4 cas
      4 casa
      4 case
      4 cash
      4 cast
      4 cat
      4 cats
      4 cave
      4 cb
      4 cbs
      4 cc
      4 ccd
      4 cd
      4 cdna
      4 cds
      4 cdt
      4 ce
      4 cell
      4 cent
      4 ceo
      4 cet
      4 cf
      4 cfr
      4 cg
      4 cgi
      4 ch
      4 chad
      4 chan
      4 char
      4 chat
      4 chef
      4 chem
      4 chen
      4 chi
      4 chip
      4 cho
      4 ci
      4 cia
      4 ciao
      4 cio
      4 cir
      4 cite
      4 city
      4 cj
      4 cl
      4 clan
      4 clay
      4 clip
      4 club
      4 cm
      4 cms
      4 cn
      4 cnet
      4 cnn
      4 co
      4 coal
      4 coat
      4 cod
      4 code
      4 coin
      4 col
      4 cold
      4 cole
      4 com
      4 come
      4 comm
      4 comp
      4 con
      4 conf
      4 cons
      4 cook
      4 cool
      4 cop
      4 cope
      4 copy
      4 cord
      4 core
      4 cork
      4 corn
      4 corp
      4 cos
      4 cost
      4 cove
      4 cow
      4 cp
      4 cpu
      4 cr
      4 crew
      4 crm
      4 crop
      4 cruz
      4 cry
      4 cs
      4 css
      4 cst
      4 ct
      4 ctrl
      4 cu
      4 cuba
      4 cube
      4 cult
      4 cup
      4 cups
      4 cure
      4 cut
      4 cute
      4 cuts
      4 cv
      4 cvs
      4 cw
      4 cz
      4 d
      4 da
      4 dad
      4 dale
      4 dam
      4 dame
      4 dan
      4 dana
      4 dans
      4 dare
      4 dark
      4 das
      4 dash
      4 dat
      4 data
      4 date
      4 dave
      4 dawn
      4 day
      4 days
      4 db
      4 dc
      4 dd
      4 ddr
      4 de
      4 dead
      4 deaf
      4 deal
      4 dean
      4 dear
      4 debt
      4 dec
      4 deck
      4 dee
      4 deep
      4 deer
      4 def
      4 del
      4 dell
      4 dem
      4 demo
      4 den
      4 deny
      4 dept
      4 der
      4 des
      4 desk
      4 dev
      4 df
      4 dg
      4 dh
      4 di
      4 dial
      4 dice
      4 did
      4 die
      4 died
      4 dies
      4 diet
      4 diff
      4 dig
      4 dim
      4 dip
      4 dir
      4 dirt
      4 dis
      4 disc
      4 dish
      4 disk
      4 dist
      4 div
      4 dive
      4 divx
      4 diy
      4 dj
      4 dk
      4 dl
      4 dm
      4 dna
      4 dns
      4 do
      4 doc
      4 dock
      4 docs
      4 dod
      4 doe
      4 does
      4 dog
      4 dogs
      4 doll
      4 dom
      4 dome
      4 don
      4 done
      4 dont
      4 doom
      4 door
      4 dos
      4 dose
      4 dot
      4 doug
      4 dow
      4 down
      4 dp
      4 dpi
      4 dr
      4 drag
      4 draw
      4 drew
      4 drop
      4 drug
      4 drum
      4 dry
      4 ds
      4 dsc
      4 dsl
      4 dt
      4 dts
      4 du
      4 dual
      4 duck
      4 dude
      4 due
      4 dui
      4 duke
      4 dumb
      4 dump
      4 duo
      4 dust
      4 duty
      4 dv
      4 dvd
      4 dvds
      4 dx
      4 e
      4 ea
      4 each
      4 ear
      4 earl
      4 earn
      4 ears
      4 ease
      4 east
      4 easy
      4 eat
      4 eau
      4 ebay
      4 ec
      4 echo
      4 eco
      4 ed
      4 eden
      4 edge
      4 edit
      4 eds
      4 edt
      4 ee
      4 ef
      4 eg
      4 egg
      4 eggs
      4 eh
      4 el
      4 else
      4 em
      4 emma
      4 en
      4 enb
      4 end
      4 ends
      4 eng
      4 ent
      4 eos
      4 ep
      4 epa
      4 epic
      4 eq
      4 er
      4 era
      4 eric
      4 erik
      4 erp
      4 es
      4 espn
      4 est
      4 et
      4 etc
      4 eu
      4 eur
      4 euro
      4 ev
      4 eva
      4 eval
      4 eve
      4 even
      4 ever
      4 evil
      4 ex
      4 exam
      4 exec
      4 exit
      4 exp
      4 expo
      4 ext
      4 eye
      4 eyed
      4 eyes
      4 ez
      4 f
      4 fa
      4 face
      4 fact
      4 fail
      4 fair
      4 fake
      4 fall
      4 fame
      4 fan
      4 fans
      4 faq
      4 faqs
      4 far
      4 fare
      4 farm
      4 fast
      4 fat
      4 fate
      4 fax
      4 fbi
      4 fc
      4 fcc
      4 fd
      4 fda
      4 fe
      4 fear
      4 feat
      4 feb
      4 fed
      4 fee
      4 feed
      4 feel
      4 fees
      4 feet
      4 fell
      4 felt
      4 feof
      4 few
      4 ff
      4 fg
      4 fi
      4 fig
      4 fiji
      4 file
      4 fill
      4 film
      4 fin
      4 find
      4 fine
      4 fire
      4 firm
      4 fish
      4 fist
      4 fit
      4 fits
      4 five
      4 fix
      4 fl
      4 flag
      4 flat
      4 flex
      4 flip
      4 flow
      4 flu
      4 flux
      4 fly
      4 fm
      4 fo
      4 foam
      4 fog
      4 fold
      4 folk
      4 font
      4 foo
      4 food
      4 fool
      4 foot
      4 for
      4 ford
      4 fork
      4 form
      4 fort
      4 foto
      4 foul
      4 four
      4 fox
      4 fp
      4 fr
      4 fred
      4 free
      4 fri
      4 frog
      4 from
      4 fs
      4 ft
      4 ftp
      4 fu
      4 fuel
      4 fuji
      4 full
      4 fun
      4 fund
      4 funk
      4 fur
      4 fw
      4 fwd
      4 fx
      4 fy
      4 g
      4 ga
      4 gage
      4 gain
      4 gale
      4 game
      4 gang
      4 gap
      4 gaps
      4 gary
      4 gas
      4 gate
      4 gave
      4 gay
      4 gays
      4 gb
      4 gba
      4 gbp
      4 gc
      4 gcc
      4 gd
      4 gdp
      4 ge
      4 gear
      4 geek
      4 gel
      4 gem
      4 gen
      4 gene
      4 geo
      4 get
      4 gets
      4 gg
      4 ghz
      4 gi
      4 gif
      4 gift
      4 gig
      4 girl
      4 gis
      4 give
      4 gl
      4 glad
      4 glen
      4 glow
      4 gm
      4 gmbh
      4 gmc
      4 gmt
      4 gnu
      4 go
      4 goal
      4 goat
      4 gods
      4 goes
      4 gold
      4 golf
      4 gone
      4 good
      4 gore
      4 got
      4 goto
      4 gp
      4 gpl
      4 gps
      4 gr
      4 grab
      4 grad
      4 gras
      4 gray
      4 greg
      4 grew
      4 grey
      4 grid
      4 grip
      4 grow
      4 gs
      4 gsm
      4 gst
      4 gt
      4 gtk
      4 guam
      4 gui
      4 gulf
      4 gun
      4 guns
      4 guru
      4 guy
      4 guys
      4 gym
      4 gzip
      4 h
      4 ha
      4 hack
      4 had
      4 hair
      4 half
      4 hall
      4 halo
      4 ham
      4 hand
      4 hang
      4 hans
      4 hard
      4 harm
      4 hart
      4 has
      4 hash
      4 hat
      4 hate
      4 hats
      4 have
      4 hawk
      4 hay
      4 hb
      4 hc
      4 hd
      4 hdtv
      4 he
      4 head
      4 hear
      4 heat
      4 heel
      4 held
      4 help
      4 her
      4 herb
      4 here
      4 hero
      4 hey
      4 hh
      4 hi
      4 hide
      4 high
      4 hill
      4 him
      4 hint
      4 hip
      4 hire
      4 his
      4 hist
      4 hit
      4 hits
      4 hiv
      4 hk
      4 hl
      4 ho
      4 hold
      4 hole
      4 holy
      4 home
      4 hon
      4 hong
      4 hood
      4 hook
      4 hop
      4 hope
      4 horn
      4 hose
      4 host
      4 hot
      4 hour
      4 how
      4 hp
      4 hq
      4 hr
      4 href
      4 hrs
      4 hs
      4 ht
      4 html
      4 http
      4 hu
      4 hub
      4 huge
      4 hugh
      4 hugo
      4 hull
      4 hung
      4 hunt
      4 hurt
      4 hwy
      4 hz
      4 i
      4 ia
      4 ian
      4 ibm
      4 ic
      4 ice
      4 icon
      4 icq
      4 ict
      4 id
      4 ide
      4 idea
      4 idle
      4 idol
      4 ids
      4 ie
      4 ieee
      4 if
      4 ii
      4 iii
      4 il
      4 ill
      4 im
      4 img
      4 in
      4 inc
      4 inch
      4 incl
      4 ind
      4 inf
      4 info
      4 ing
      4 ink
      4 inn
      4 inns
      4 ins
      4 int
      4 intl
      4 into
      4 io
      4 ion
      4 iowa
      4 ip
      4 ipaq
      4 ipod
      4 ips
      4 ir
      4 ira
      4 iran
      4 iraq
      4 irc
      4 iron
      4 irs
      4 is
      4 isa
      4 isbn
      4 isle
      4 iso
      4 isp
      4 issn
      4 ist
      4 it
      4 item
      4 its
      4 iv
      4 ix
      4 j
      4 ja
      4 jack
      4 jade
      4 jail
      4 jake
      4 jam
      4 jan
      4 jane
      4 jar
      4 java
      4 jay
      4 jazz
      4 jc
      4 jd
      4 je
      4 jean
      4 jeep
      4 jeff
      4 jet
      4 jets
      4 jews
      4 jill
      4 jim
      4 jj
      4 jm
      4 joan
      4 job
      4 jobs
      4 joe
      4 joel
      4 john
      4 join
      4 joke
      4 jon
      4 jose
      4 josh
      4 joy
      4 jp
      4 jpeg
      4 jpg
      4 jr
      4 js
      4 juan
      4 judy
      4 jul
      4 july
      4 jump
      4 jun
      4 june
      4 junk
      4 jury
      4 just
      4 jvc
      4 k
      4 ka
      4 kai
      4 karl
      4 kate
      4 kay
      4 kb
      4 kde
      4 keen
      4 keep
      4 ken
      4 keno
      4 kent
      4 kept
      4 key
      4 keys
      4 kg
      4 kick
      4 kid
      4 kids
      4 kill
      4 kim
      4 kind
      4 king
      4 kirk
      4 kiss
      4 kit
      4 kits
      4 km
      4 knee
      4 knew
      4 knit
      4 know
      4 ko
      4 kong
      4 ks
      4 kurt
      4 kw
      4 ky
      4 kyle
      4 l
      4 la
      4 lab
      4 labs
      4 lace
      4 lack
      4 lady
      4 laid
      4 lake
      4 lamb
      4 lamp
      4 lan
      4 land
      4 lane
      4 lang
      4 laos
      4 lap
      4 las
      4 last
      4 lat
      4 late
      4 law
      4 lawn
      4 laws
      4 lay
      4 lazy
      4 lb
      4 lbs
      4 lc
      4 lcd
      4 ld
      4 le
      4 lead
      4 leaf
      4 lean
      4 led
      4 lee
      4 left
      4 leg
      4 legs
      4 len
      4 lens
      4 leo
      4 leon
      4 les
      4 less
      4 let
      4 lets
      4 leu
      4 levy
      4 lf
      4 lg
      4 li
      4 lib
      4 libs
      4 lid
      4 lie
      4 lies
      4 life
      4 lift
      4 like
      4 lil
      4 lime
      4 line
      4 link
      4 lion
      4 lip
      4 lips
      4 lisa
      4 list
      4 lit
      4 lite
      4 live
      4 liz
      4 ll
      4 llc
      4 llp
      4 lm
      4 ln
      4 lo
      4 load
      4 loan
      4 loc
      4 lock
      4 log
      4 logo
      4 logs
      4 lol
      4 lone
      4 long
      4 look
      4 loop
      4 lord
      4 los
      4 lose
      4 loss
      4 lost
      4 lot
      4 lots
      4 lou
      4 loud
      4 love
      4 low
      4 lows
      4 lp
      4 ls
      4 lt
      4 ltd
      4 lu
      4 luck
      4 lucy
      4 luis
      4 luke
      4 lung
      4 lynn
      4 m
      4 ma
      4 mac
      4 mad
      4 made
      4 mae
      4 mag
      4 mai
      4 mail
      4 main
      8 major
      4 make
      4 male
      4 mali
      4 mall
      4 man
      4 many
      4 map
      4 maps
      4 mar
      4 marc
      4 mark
      4 mars
      4 mart
      4 mary
      4 mas
      4 mask
      4 mass
      4 mat
      4 mate
      4 math
      4 mats
      4 matt
      4 maui
      4 max
      4 may
      4 mb
      4 mba
      4 mc
      4 md
      4 me
      4 meal
      4 mean
      4 meat
      4 med
      4 meet
      4 mega
      4 mel
      4 mem
      4 memo
      4 men
      4 mens
      4 ment
      4 menu
      4 mere
      4 mesa
      4 mesh
      4 mess
      4 met
      4 meta
      4 mf
      4 mg
      4 mh
      4 mhz
      4 mi
      4 mia
      4 mic
      4 mice
      4 mid
      4 midi
      4 mike
      4 mil
      4 mild
      4 mile
      4 milk
      4 mill
      4 mime
      4 min
      4 mind
      4 mine
      4 mini
      4 mins
      4 mint
      4 misc
      4 miss
      4 mit
      4 mix
      4 mj
      4 ml
      4 mlb
      4 mls
      4 mm
      4 mn
      4 mo
      4 mod
      4 mode
      4 mods
      4 mold
      4 mom
      4 moms
      4 mon
      4 mono
      4 mood
      4 moon
      4 more
      4 moss
      4 most
      4 move
      4 mp
      4 mpeg
      4 mpg
      4 mph
      4 mr
      4 mrna
      4 mrs
      4 ms
      4 msg
      4 msie
      4 msn
      4 mt
      4 mtv
      4 mu
      4 much
      4 mud
      4 mug
      4 must
      4 muze
      4 mv
      4 mw
      4 mx
      4 my
      4 myth
      4 n
      4 na
      4 nail
      4 nam
      4 name
      4 nano
      4 nasa
      4 nat
      4 nato
      4 nav
      4 navy
      4 nb
      4 nba
      4 nbc
      4 nc
      4 ncaa
      4 nd
      4 ne
      4 near
      4 nec
      4 neck
      4 need
      4 neil
      4 neo
      4 neon
      4 nest
      4 net
      4 new
      4 news
      4 next
      4 nfl
      4 ng
      4 nh
      4 nhl
      4 nhs
      4 ni
      4 nice
      4 nick
      4 nike
      4 nil
      4 nine
      4 nj
      4 nl
      4 nm
      4 nn
      4 no
      4 node
      4 non
      4 none
      4 noon
      4 nor
      4 norm
      4 nose
      4 not
      4 note
      4 nov
      4 nova
      4 now
      4 np
      4 nr
      4 ns
      4 nsw
      4 nt
      4 ntsc
      4 nu
      4 nuke
      4 null
      4 nut
      4 nuts
      4 nv
      4 nw
      4 ny
      4 nyc
      4 nz
      4 o
      4 oak
      4 oaks
      4 ob
      4 obj
      4 oc
      4 oclc
      4 oct
      4 odd
      4 odds
      4 oe
      4 oecd
      4 oem
      4 of
      4 off
      4 og
      4 oh
      4 ohio
      4 oil
      4 oils
      4 ok
      4 okay
      4 ol
      4 old
      4 om
      4 oman
      4 on
      4 once
      4 one
      4 ones
      4 only
      4 ons
      4 onto
      4 oo
      4 ooo
      4 oops
      4 op
      4 open
      4 opt
      4 or
      4 oral
      4 org
      4 os
      4 ot
      4 ou
      4 our
      4 ours
      4 out
      4 oval
      4 oven
      4 over
      4 owen
      4 own
      4 owns
      4 oz
      4 p
      4 pa
      4 pac
      4 pace
      4 pack
      4 pad
      4 pads
      4 page
      4 paid
      4 pain
      4 pair
      4 pal
      4 pale
      4 palm
      4 pam
      4 pan
      4 par
      4 para
      4 park
      4 part
      4 pas
      4 paso
      4 pass
      4 past
      4 pat
      4 path
      4 paul
      4 pay
      4 pays
      4 pb
      4 pc
      4 pci
      4 pcs
      4 pct
      4 pd
      4 pda
      4 pdas
      4 pdf
      4 pdt
      4 pe
      4 peak
      4 peas
      4 pee
      4 peer
      4 pen
      4 penn
      4 pens
      4 per
      4 perl
      4 peru
      4 pest
      4 pet
      4 pete
      4 pets
      4 pf
      4 pg
      4 pgp
      4 ph
      4 phd
      4 phi
      4 phil
      4 php
      4 phys
      4 pi
      4 pic
      4 pick
      4 pics
      4 pie
      4 pig
      4 pike
      4 pill
      4 pin
      4 pine
      4 ping
      4 pink
      4 pins
      4 pipe
      4 pit
      4 pix
      4 pj
      4 pk
      4 pl
      4 plan
      4 play
      4 plc
      4 plot
      4 plug
      4 plus
      4 pm
      4 pmc
      4 pmid
      4 pn
      4 po
      4 pod
      4 poem
      4 poet
      4 pole
      4 poll
      4 polo
      4 poly
      4 pond
      4 pool
      4 poor
      4 pop
      4 pope
      4 por
      4 pork
      4 port
      4 pos
      4 pose
      4 post
      4 pot
      4 pour
      4 pp
      4 ppc
      4 ppm
      4 pr
      4 pray
      4 pre
      4 prep
      4 prev
      4 prix
      4 pro
      4 proc
      4 pros
      4 prot
      4 ps
      4 psi
      4 psp
      4 pst
      4 pt
      4 pts
      4 pty
      4 pub
      4 pubs
      4 pull
      4 pump
      4 punk
      4 pure
      4 push
      4 put
      4 puts
      4 pvc
      4 q
      4 qc
      4 qld
      4 qt
      4 qty
      4 quad
      4 que
      4 qui
      4 quit
      4 quiz
      4 r
      4 ra
      4 race
      4 rack
      4 rage
      4 raid
      4 rail
      4 rain
      4 ram
      4 ran
      4 rand
      4 rank
      4 rap
      4 rare
      4 rat
      4 rate
      4 rats
      4 raw
      4 ray
      4 rays
      4 rb
      4 rc
      4 rca
      4 rd
      4 re
      4 read
      4 real
      4 rear
      4 rec
      4 red
      4 reed
      4 reef
      4 reel
      4 ref
      4 reg
      4 reid
      4 rely
      4 reno
      4 rent
      4 rep
      4 res
      4 rest
      4 rev
      4 rf
      4 rfc
      4 rg
      4 rh
      4 ri
      4 rica
      4 rice
      4 rich
      4 rick
      4 rico
      4 rid
      4 ride
      4 rim
      4 ring
      4 rio
      4 rip
      4 ripe
      4 rise
      4 risk
      4 rj
      4 rl
      4 rm
      4 rn
      4 rna
      4 ro
      4 road
      4 rob
      4 rock
      4 rod
      4 role
      4 roll
      4 rom
      4 rome
      4 ron
      4 roof
      4 room
      4 root
      4 rope
      4 rosa
      4 rose
      4 ross
      4 row
      4 rows
      4 roy
      4 rp
      4 rpg
      4 rpm
      4 rr
      4 rrp
      4 rs
      4 rss
      4 rt
      4 ru
      4 ruby
      4 rug
      4 rugs
      4 rule
      4 run
      4 runs
      4 rush
      4 ruth
      4 rv
      4 rw
      4 rx
      4 ryan
      4 s
      4 sa
      4 sad
      4 safe
      4 sage
      4 said
      4 sail
      4 sake
      4 sale
      4 salt
      4 sam
      4 same
      4 san
      4 sand
      4 sans
      4 sao
      4 sap
      4 sara
      4 sas
      4 sat
      4 save
      4 saw
      4 say
      4 says
      4 sb
      4 sc
      4 scan
      4 sci
      4 scsi
      4 sd
      4 se
      4 sea
      4 seal
      4 sean
      4 seas
      4 seat
      4 sec
      4 see
      4 seed
      4 seek
      4 seem
      4 seen
      4 sees
      4 sega
      4 self
      4 sell
      4 semi
      4 sen
      4 send
      4 sent
      4 seo
      4 sep
      4 sept
      4 seq
      4 ser
      4 set
      4 sets
      4 sf
      4 sg
      4 sh
      4 shaw
      4 she
      4 shed
      4 ship
      4 shoe
      4 shop
      4 shot
      4 show
      4 shut
      4 si
      4 sic
      4 sick
      4 side
      4 sie
      4 sig
      4 sign
      4 silk
      4 sim
      4 sims
      4 sin
      4 sing
      4 sink
      4 sip
      4 sir
      4 sit
      4 site
      4 six
      4 size
      4 sk
      4 ski
      4 skin
      4 skip
      4 sku
      4 sky
      4 sl
      4 slim
      4 slip
      4 slot
      4 slow
      4 sm
      4 sms
      4 smtp
      4 sn
      4 snap
      4 snow
      4 so
      4 soa
      4 soap
      4 soc
      4 sofa
      4 soft
      4 soil
      4 sol
      4 sold
      4 sole
      4 solo
      4 soma
      4 some
      4 son
      4 song
      4 sons
      4 sony
      4 soon
      4 sort
      4 soul
      4 soup
      4 sox
      4 sp
      4 spa
      4 spam
      4 span
      4 spas
      4 spec
      4 spin
      4 spot
      4 spy
      4 sq
      4 sql
      4 sr
      4 src
      4 sri
      4 ss
      4 ssl
      4 st
      4 stan
      4 star
      4 stat
      4 stay
      4 std
      4 ste
      4 stem
      4 step
      4 stop
      4 str
      4 stud
      4 su
      4 sub
      4 such
      4 sue
      4 suit
      4 sum
      4 sun
      4 sur
      4 sure
      4 surf
      4 suse
      4 sv
      4 sw
      4 swap
      4 swim
      4 sync
      4 sys
      4 t
      4 ta
      4 tab
      4 tabs
      4 tag
      4 tags
      4 tail
      4 take
      4 tale
      4 talk
      4 tall
      4 tan
      4 tank
      4 tap
      4 tape
      4 tar
      4 task
      4 tax
      4 taxi
      4 tb
      4 tba
      4 tc
      4 tcp
      4 td
      4 te
      4 tea
      4 team
      4 tear
      4 tech
      4 ted
      4 tee
      4 teen
      4 tel
      4 tell
      4 temp
      4 ten
      4 tend
      4 tent
      4 term
      4 test
      4 tex
      4 text
      4 tf
      4 tft
      4 tgp
      4 th
      4 thai
      4 than
      4 that
      4 the
      4 thee
      4 them
      4 then
      4 they
      4 thin
      4 this
      4 thou
      4 thru
      4 thu
      4 thus
      4 thy
      4 ti
      4 tide
      4 tie
      4 tied
      4 tier
      4 ties
      4 til
      4 tile
      4 till
      4 tim
      4 time
      4 tin
      4 tiny
      4 tion
      4 tip
      4 tips
      4 tire
      4 tm
      4 tmp
      4 tn
      4 to
      4 todd
      4 toe
      4 told
      4 toll
      4 tom
      4 ton
      4 tone
      4 tons
      4 tony
      4 too
      4 took
      4 tool
      4 top
      4 tops
      4 tour
      4 town
      4 toy
      4 toys
      4 tp
      4 tr
      4 trap
      4 tray
      4 tree
      4 trek
      4 treo
      4 tri
      4 trim
      4 trio
      4 trip
      4 troy
      4 true
      4 try
      4 ts
      4 tt
      4 tu
      4 tub
      4 tube
      4 tue
      4 tune
      4 turn
      4 tv
      4 tvs
      4 twin
      4 two
      4 tx
      4 ty
      4 type
      4 u
      4 uc
      4 ugly
      4 uh
      4 ui
      4 uk
      4 ul
      4 um
      4 un
      4 una
      4 und
      4 undo
      4 une
      4 uni
      4 unit
      4 univ
      4 unix
      4 unto
      4 up
      4 upc
      4 upon
      4 ups
      4 ur
      4 urge
      4 uri
      4 url
      4 urls
      4 urw
      4 us
      4 usa
      4 usb
      4 usc
      4 usd
      4 usda
      4 use
      4 used
      4 user
      4 uses
      4 usgs
      4 usps
      4 usr
      4 ut
      4 utah
      4 utc
      4 uv
      4 uw
      4 v
      4 va
      4 val
      4 van
      4 var
      4 vary
      4 vast
      4 vat
      4 vb
      4 vc
      4 vcr
      4 ve
      4 ver
      4 very
      4 vg
      4 vhs
      4 vi
      4 via
      4 vic
      4 vice
      4 vid
      4 vids
      4 view
      4 vii
      4 viii
      4 vip
      4 visa
      4 void
      4 voip
      4 vol
      4 volt
      4 von
      4 vote
      4 vp
      4 vpn
      4 vs
      4 vt
      4 w
      4 wa
      4 wage
      4 wait
      4 wake
      4 wal
      4 walk
      4 wall
      4 walt
      4 wan
      4 want
      4 war
      4 ward
      4 ware
      4 warm
      4 wars
      4 was
      4 wash
      7 watch
      4 watt
      4 wav
      4 wave
      4 wax
      4 way
      4 ways
      4 wb
      4 wc
      4 we
      4 weak
      4 wear
      4 web
      4 wed
      4 weed
      4 week
      4 well
      4 went
      4 were
      4 west
      4 wet
      4 what
      4 when
      4 who
      4 whom
      4 why
      4 wi
      4 wide
      4 wife
      4 wifi
      4 wiki
      4 wild
      4 will
      4 win
      4 wind
      4 wine
      4 wing
      4 wins
      4 wire
      4 wise
      4 wish
      4 wit
      4 with
      4 wm
      4 wma
      4 wn
      4 wolf
      4 won
      4 wood
      4 wool
      4 word
      4 work
      4 worm
      4 worn
      4 wow
      4 wp
      4 wr
      4 wrap
      4 ws
      4 wt
      4 wto
      4 wu
      4 wv
      4 ww
      4 www
      4 wx
      4 wy
      4 x
      4 xbox
      4 xi
      4 xl
      4 xml
      4 xp
      4 y
      4 ya
      4 yale
      4 yang
      4 yard
      4 yarn
      4 ye
      4 yea
      4 yeah
      4 year
      4 yen
      4 yes
      4 yet
      4 yn
      4 yo
      4 yoga
      4 york
      4 you
      4 your
      4 yr
      4 yrs
      4 yu
      4 z
      4 za
      4 zen
      4 zero
      4 zinc
      4 zip
      4 zone
      4 zoo
      4 zoom
      4 zope
      4 zu
      4 zum
      4 zus
user10@webserver:~$ cat password.txt | tr " " "\n" | sort | uniq -c | grep -v "4"
     10 angry
      8 major
      7 watch
user10@webserver:~$
user10@webserver:~$ exit
logout
Connection to linux.offsec.club closed.
➜  linux.offsec.club
```

----

###### user11

```sh
➜  ~ ssh user11@linux.offsec.club
user11@linux.offsec.club's password:
Linux webserver 4.9.0-5-amd64 #1 SMP Debian 4.9.65-3+deb9u2 (2018-01-04) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Fri Jun 29 20:07:49 2018 from 174.115.33.239
user11@webserver:~$ ls -l
total 1248
-r-xr-x--- 1 root challenges 1276246 Feb 21 23:03 password.txt
user11@webserver:~$ cat password.txt | grep password
user11@webserver:~$ cat password.txt | grep -i password
spirally coiled away in the tub, not Password: EarlyHersCase97 like the worm-pipe of a still
user11@webserver:~$ exit
logout
Connection to linux.offsec.club closed.
➜  ~
```

----

###### user12

```sh
➜  ~ ssh user12@linux.offsec.club
user12@linux.offsec.club's password:
Linux webserver 4.9.0-5-amd64 #1 SMP Debian 4.9.65-3+deb9u2 (2018-01-04) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Fri Jun 29 20:16:23 2018 from 174.115.33.239
user12@webserver:~$ ls -l
total 11480
-r-xr-x--- 1 root challenges 11754815 Feb 21 23:44 password.txt
user12@webserver:~$ mkdir /tmp/kanishka
user12@webserver:~$ cp password.txt /tmp/kanishka/
user12@webserver:~$ cd /tmp/kanishka/
user12@webserver:/tmp/kanishka$ ls -l
total 11480
-r-xr-x--- 1 user12 challenges 11754815 Jun 30 18:07 password.txt
user12@webserver:/tmp/kanishka$
```

`decode.sh`

```sh
#!/bin/bash

for i in {1..50}
do
    let p=$i-1;
    base64 -d $p.txt > $i.txt;
done
```

```sh
user12@webserver:/tmp/kanishka$ cp password.txt 0.txt
user12@webserver:/tmp/kanishka$ ls
decode.sh  password.txt
user12@webserver:/tmp/kanishka$ bash decode.sh
base64: invalid input
user12@webserver:/tmp/kanishka$ ls
0.txt   12.txt  15.txt  18.txt  20.txt  23.txt  26.txt  29.txt  31.txt  34.txt  37.txt  3.txt   42.txt  45.txt  48.txt  50.txt  7.txt  decode.sh
10.txt  13.txt  16.txt  19.txt  21.txt  24.txt  27.txt  2.txt   32.txt  35.txt  38.txt  40.txt  43.txt  46.txt  49.txt  5.txt   8.txt  password.txt
11.txt  14.txt  17.txt  1.txt   22.txt  25.txt  28.txt  30.txt  33.txt  36.txt  39.txt  41.txt  44.txt  47.txt  4.txt   6.txt   9.txt
user12@webserver:/tmp/kanishka$ ls -l
total 55776
-r-xr-x--- 1 user12 challenges 11754815 Jun 30 18:10 0.txt
-rw-r--r-- 1 user12 challenges   580839 Jun 30 18:10 10.txt
-rw-r--r-- 1 user12 challenges   429972 Jun 30 18:10 11.txt
-rw-r--r-- 1 user12 challenges   318289 Jun 30 18:10 12.txt
-rw-r--r-- 1 user12 challenges   235615 Jun 30 18:10 13.txt
-rw-r--r-- 1 user12 challenges   174417 Jun 30 18:10 14.txt
-rw-r--r-- 1 user12 challenges   129112 Jun 30 18:10 15.txt
-rw-r--r-- 1 user12 challenges    95577 Jun 30 18:10 16.txt
-rw-r--r-- 1 user12 challenges    70750 Jun 30 18:10 17.txt
-rw-r--r-- 1 user12 challenges    52372 Jun 30 18:10 18.txt
-rw-r--r-- 1 user12 challenges    38767 Jun 30 18:10 19.txt
-rw-r--r-- 1 user12 challenges  8701615 Jun 30 18:10 1.txt
-rw-r--r-- 1 user12 challenges    28696 Jun 30 18:10 20.txt
-rw-r--r-- 1 user12 challenges    21243 Jun 30 18:10 21.txt
-rw-r--r-- 1 user12 challenges    15724 Jun 30 18:10 22.txt
-rw-r--r-- 1 user12 challenges    11639 Jun 30 18:10 23.txt
-rw-r--r-- 1 user12 challenges     8615 Jun 30 18:10 24.txt
-rw-r--r-- 1 user12 challenges     6378 Jun 30 18:10 25.txt
-rw-r--r-- 1 user12 challenges     4721 Jun 30 18:10 26.txt
-rw-r--r-- 1 user12 challenges     3493 Jun 30 18:10 27.txt
-rw-r--r-- 1 user12 challenges     2585 Jun 30 18:10 28.txt
-rw-r--r-- 1 user12 challenges     1912 Jun 30 18:10 29.txt
-rw-r--r-- 1 user12 challenges  6441455 Jun 30 18:10 2.txt
-rw-r--r-- 1 user12 challenges     1414 Jun 30 18:10 30.txt
-rw-r--r-- 1 user12 challenges     1045 Jun 30 18:10 31.txt
-rw-r--r-- 1 user12 challenges      774 Jun 30 18:10 32.txt
-rw-r--r-- 1 user12 challenges      571 Jun 30 18:10 33.txt
-rw-r--r-- 1 user12 challenges      421 Jun 30 18:10 34.txt
-rw-r--r-- 1 user12 challenges      312 Jun 30 18:10 35.txt
-rw-r--r-- 1 user12 challenges      230 Jun 30 18:10 36.txt
-rw-r--r-- 1 user12 challenges      170 Jun 30 18:10 37.txt
-rw-r--r-- 1 user12 challenges      125 Jun 30 18:10 38.txt
-rw-r--r-- 1 user12 challenges       93 Jun 30 18:10 39.txt
-rw-r--r-- 1 user12 challenges  4768350 Jun 30 18:10 3.txt
-rw-r--r-- 1 user12 challenges       68 Jun 30 18:10 40.txt
-rw-r--r-- 1 user12 challenges       49 Jun 30 18:10 41.txt
-rw-r--r-- 1 user12 challenges        0 Jun 30 18:10 42.txt
-rw-r--r-- 1 user12 challenges        0 Jun 30 18:10 43.txt
-rw-r--r-- 1 user12 challenges        0 Jun 30 18:10 44.txt
-rw-r--r-- 1 user12 challenges        0 Jun 30 18:10 45.txt
-rw-r--r-- 1 user12 challenges        0 Jun 30 18:10 46.txt
-rw-r--r-- 1 user12 challenges        0 Jun 30 18:10 47.txt
-rw-r--r-- 1 user12 challenges        0 Jun 30 18:10 48.txt
-rw-r--r-- 1 user12 challenges        0 Jun 30 18:10 49.txt
-rw-r--r-- 1 user12 challenges  3529817 Jun 30 18:10 4.txt
-rw-r--r-- 1 user12 challenges        0 Jun 30 18:10 50.txt
-rw-r--r-- 1 user12 challenges  2612982 Jun 30 18:10 5.txt
-rw-r--r-- 1 user12 challenges  1934284 Jun 30 18:10 6.txt
-rw-r--r-- 1 user12 challenges  1431871 Jun 30 18:10 7.txt
-rw-r--r-- 1 user12 challenges  1059957 Jun 30 18:10 8.txt
-rw-r--r-- 1 user12 challenges   784642 Jun 30 18:10 9.txt
-rw-r--r-- 1 user12 challenges       85 Jun 30 18:10 decode.sh
-r-xr-x--- 1 user12 challenges 11754815 Jun 30 18:07 password.txt
user12@webserver:/tmp/kanishka$ cat 41.txt
���Zpassword.txt
                ,�L���/-r-K-22�c�,
user12@webserver:/tmp/kanishka$
user12@webserver:/tmp/kanishka$ file 41.txt
41.txt: gzip compressed data, was "password.txt", last modified: Wed Feb 21 23:24:40 2018, from Unix
user12@webserver:/tmp/kanishka$ cp 41.txt out.gz
user12@webserver:/tmp/kanishka$ gunzip out.gz
user12@webserver:/tmp/kanishka$ ls
0.txt   12.txt  15.txt  18.txt  20.txt  23.txt  26.txt  29.txt  31.txt  34.txt  37.txt  3.txt   42.txt  45.txt  48.txt  50.txt  7.txt  decode.sh
10.txt  13.txt  16.txt  19.txt  21.txt  24.txt  27.txt  2.txt   32.txt  35.txt  38.txt  40.txt  43.txt  46.txt  49.txt  5.txt   8.txt  out
11.txt  14.txt  17.txt  1.txt   22.txt  25.txt  28.txt  30.txt  33.txt  36.txt  39.txt  41.txt  44.txt  47.txt  4.txt   6.txt   9.txt  password.txt
user12@webserver:/tmp/kanishka$ cat out
QuickHourEver20
user12@webserver:/tmp/kanishka$ exit
logout
Connection to linux.offsec.club closed.
➜  ~
```

----

###### user13

```sh
➜  ~ ssh user13@linux.offsec.club
user13@linux.offsec.club's password:
Linux webserver 4.9.0-5-amd64 #1 SMP Debian 4.9.65-3+deb9u2 (2018-01-04) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Fri Jun 29 23:59:02 2018 from 174.115.33.239
user13@webserver:~$ ls -l
total 20
-r-sr-x--- 1 user14 challenges 8888 Feb 21 23:29 challenge
-r-xr-x--- 1 root   challenges  393 Feb 21 23:29 challenge.c
-r-xr-x--- 1 user14 root         16 Feb 21 23:21 password.txt
user13@webserver:~$ cat password.txt
cat: password.txt: Permission denied
user13@webserver:~$ cat challenge.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {

    int c;
    char buff[1001] = {0};

    for(c=1; c<1000; c++) {

        fgets(buff, 1000, stdin);
        if(strlen(buff) != c) {
            printf("Fail %d != %d\n", strlen(buff), c);
            exit(1);
        }

    }

    system("/bin/cat /home/user14/password.txt");

    return 0;

}
user13@webserver:~$ file challenge
challenge: setuid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=436d911632507a6dfe029f419cbc2d2e080566e6, not stripped
user13@webserver:~$ ./challenge
asdf
Fail 5 != 1
user13@webserver:~$
user13@webserver:~$ ./challenge

1
11
111
1111
11111

Fail 1 != 7
user13@webserver:~$
user13@webserver:~$ python -c "for i in range(1000): print 'A'*i" | ./challenge
BookVerbLeast61
user13@webserver:~$
```

----

###### user14

```sh
➜  ~ ssh user14@linux.offsec.club
user14@linux.offsec.club's password:
Linux webserver 4.9.0-5-amd64 #1 SMP Debian 4.9.65-3+deb9u2 (2018-01-04) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Jun 30 18:21:31 2018 from 75.140.84.109
user14@webserver:~$ ls -l
total 20
-r-sr-x--- 1 user15 challenges 8800 Feb 21 23:36 challenge
-r-xr-x--- 1 root   challenges  389 Feb 21 23:35 challenge.c
-r-xr-x--- 1 user14 root         16 Feb 21 23:28 password.txt
user14@webserver:~$ cat challenge.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {

        int c, tmp;
        char password[] = "YouCantGetIt";

        for(c=0; c<strlen(password); c+=4) {
                scanf("%d", &tmp);
                if(tmp != *(int *)&password[c])
                        exit(0);
        }

        system("/bin/cat /home/user15/password.txt");

}

user14@webserver:~$ cat password.txt
BookVerbLeast61
user14@webserver:~$ file challenge
challenge: setuid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=99463d5b5ca207c45df4d48208d55c7cd505a69d, not stripped
user14@webserver:~$
user14@webserver:~$ cp challenge.c /dev/shm/
user14@webserver:~$ cd /dev/shm/
user14@webserver:/dev/shm$ ls
challenge.c
user14@webserver:/dev/shm$
```

`challenge.c`

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {

        int c, tmp;
        char password[] = "YouCantGetIt";

        for(c=0; c<strlen(password); c+=4) {
                // scanf("%d", &tmp);
                tmp = *(int *)&password[c];
                printf("%d\n", tmp);
                        // exit(0);
        }

        // system("/bin/cat /home/user15/password.txt");

}
```

![](images/6.png)

```sh
user14@webserver:/dev/shm$ gcc challenge.c
user14@webserver:/dev/shm$ ls -l
total 16
-rwxr-xr-x 1 user14 challenges 8688 Jun 30 18:37 a.out
-r-xr-x--- 1 user14 challenges  417 Jun 30 18:37 challenge.c
user14@webserver:/dev/shm$ ./a.out
1131769689
1198812769
1950970981
user14@webserver:/dev/shm$ cd
user14@webserver:~$ ./challenge
1131769689
1198812769
1950970981
ClassPlacePress16
user14@webserver:~$ exit
logout
Connection to linux.offsec.club closed.
➜  ~
```

----

###### user15


```sh
➜  ~ ssh user15@linux.offsec.club
user15@linux.offsec.club's password:
Linux webserver 4.9.0-5-amd64 #1 SMP Debian 4.9.65-3+deb9u2 (2018-01-04) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Fri Jun 29 13:38:26 2018 from 88.193.142.145
user15@webserver:~$ ls -l
total 4
-r-xr-x--- 1 user15 challenges 18 Feb 21 23:35 password.txt
user15@webserver:~$ cat password.txt
ClassPlacePress16
user15@webserver:~$ exit
logout
Connection to linux.offsec.club closed.
➜  ~
```

---- 

EOF