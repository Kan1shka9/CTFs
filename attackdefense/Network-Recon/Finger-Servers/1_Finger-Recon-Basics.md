#### 1. Finger Recon: Basics

----

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2370: eth0@if2371: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:06 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.6/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
2373: eth1@if2374: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:1f:cd:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.31.205.2/24 brd 192.31.205.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# nmap -sC -sV 192.31.205.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-25 09:39 UTC
Nmap scan report for et6mhw2bgln3qe7xagpew8av0.temp-network_a-31-205 (192.31.205.3)
Host is up (0.000013s latency).
Not shown: 999 closed ports
PORT   STATE SERVICE VERSION
79/tcp open  finger  Linux fingerd
|_finger: No one logged on.\x0D
MAC Address: 02:42:C0:1F:CD:03 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.67 seconds
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# msfconsole
msf5 > search finger

Matching Modules
================

   Name                                           Disclosure Date  Rank    Check  Description
   ----                                           ---------------  ----    -----  -----------
   auxiliary/gather/mybb_db_fingerprint           2014-02-13       normal  Yes    MyBB Database Fingerprint
   auxiliary/scanner/finger/finger_users                           normal  Yes    Finger Service User Enumerator
   auxiliary/scanner/oracle/isqlplus_login                         normal  Yes    Oracle iSQL*Plus Login Utility
   auxiliary/scanner/oracle/isqlplus_sidbrute                      normal  Yes    Oracle iSQLPlus SID Check
   auxiliary/scanner/vmware/esx_fingerprint                        normal  Yes    VMWare ESX/ESXi Fingerprint Scanner
   auxiliary/server/browser_autopwn                                normal  No     HTTP Client Automatic Exploiter
   exploit/bsd/finger/morris_fingerd_bof          1988-11-02       normal  Yes    Morris Worm fingerd Stack Buffer Overflow
   exploit/windows/http/bea_weblogic_post_bof     2008-07-17       great   Yes    Oracle Weblogic Apache Connector POST Request Buffer Overflow
   post/windows/gather/enum_putty_saved_sessions                   normal  No     PuTTY Saved Sessions Enumeration Module


msf5 > use auxiliary/scanner/finger/finger_users
msf5 auxiliary(scanner/finger/finger_users) > show options

Module options (auxiliary/scanner/finger/finger_users):

   Name        Current Setting                                                Required  Description
   ----        ---------------                                                --------  -----------
   RHOSTS                                                                     yes       The target address range or CIDR identifier
   RPORT       79                                                             yes       The target port (TCP)
   THREADS     1                                                              yes       The number of concurrent threads
   USERS_FILE  /usr/share/metasploit-framework/data/wordlists/unix_users.txt  yes       The file that contains a list of default UNIX accounts.

msf5 auxiliary(scanner/finger/finger_users) > set RHOSTS 192.31.205.3
RHOSTS => 192.31.205.3
msf5 auxiliary(scanner/finger/finger_users) > exploit

[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: admin
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: administrator
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: backup
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: bin
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: daemon
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: dbadmin
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: diag
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: games
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: gnats
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: gopher
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: irc
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: list
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: lp
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: mail
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: man
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: news
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: nobody
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: proxy
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: systemd-bus-proxy
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: root
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: saned
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: sync
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: sys
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: udadmin
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: uucp
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: webmaster
[+] 192.31.205.3:79       - 192.31.205.3:79 - Found user: www-data
[+] 192.31.205.3:79       - 192.31.205.3:79 Users found: admin, administrator, backup, bin, daemon, dbadmin, diag, games, gnats, gopher, irc, list, lp, mail, man, news, nobody, proxy, root, saned, sync, sys, systemd-bus-proxy, udadmin, uucp, webmaster, www-data
[*] 192.31.205.3:79       - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf5 auxiliary(scanner/finger/finger_users) >
```

----

```sh
root@attackdefense:~# finger admin@192.31.205.3
Login: admin                            Name: Jason L. Nawrocki
Directory: /home/admin                  Shell: /bin/bash
Office: 5877, 989-905-2731              Home Phone: 978-272-5420
Never logged in.
No mail.
No Plan.
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# finger gopher@192.31.205.3
Login: gopher                           Name: Flag1 098F6BCD4621D373CADE4E832627B4F6
Directory: /home/gopher                 Shell: /bin/bash
Office: 5423, 954-540-8052              Home Phone: 423-553-2085
Never logged in.
No mail.
No Plan.
root@attackdefense:~#
```

```sh
root@attackdefense:~# finger diag@192.31.205.3
Login: diag                             Name: Flag2 F765F7A0A169F4F6654EE72A84A9EB
Directory: /home/diag                   Shell: /bin/bash
Office: 353, 567-537-1198               Home Phone: 410-364-2969
Never logged in.
No mail.
No Plan.
root@attackdefense:~#
```

```sh
root@attackdefense:~# finger webmaster@192.31.205.3
Login: webmaster                        Name: Flag3 C4CA4238A0B923820DCC509A6F75849B
Directory: /home/webmaster              Shell: /bin/bash
Office: 65, 318-240-8507                Home Phone: 608-848-1401
Never logged in.
No mail.
No Plan.
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# finger tom@192.31.205.3
Login: tom                              Name: tom
Directory: /home/tom                    Shell: /bin/bash
Never logged in.
Mail forwarded to camilia
No mail.
No Plan.
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# finger tim@192.31.205.3
Login: tim                              Name: tim
Directory: /home/tim                    Shell: /bin/bash
Last login Tue Dec 18 07:52 2018 (UTC) on pts/0
No mail.
Project:
Project FingerReconLab
No Plan.
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# finger jim@192.31.205.3
Login: jim                              Name: jim
Directory: /home/jim                    Shell: /bin/bash
Never logged in.
No mail.
PGP key:
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: Keybase OpenPGP v1.0.0
Comment: https://keybase.io/crypto

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
A9RaIu1MfyHOwU0EXBiX/gEQAL5PvPk7sbVKz8+HUdxlSxMws6MPMLOCwoyJdJbk
1Qy6PJdRGwtmqL3bu570O4vTDbJS6btIfSmr9uHwInQd09BXSLydKy3IVvITE24/
5rGGUVlHmL9nxINMujJ6vX2zCqKp/JAHWWB6z418QXaNA33aDNj54dfI2nbZBwSH
mPTRKPmRQvEWXYPiievQSQ8pQY/hgOmk3KCeuF+zbZsY6ZhTUENZ4rb8BKEr+yoU
xXN9JSbv4O3uJTdZegTJ8d2YvVe/SS8WGhK0ICsk39FozjBI7jyghRpBofk6Pt6K
9nbXxR/vh8O6Ymz9fNT5cjLCosGC1cGCZoin3ODZnZld9pEjENzA1n++C8quqXNR
esKWBd10+fT3SjqWF8Gh05NcuLUy/RMUwd2kYUcmHE07hcfR2Yi1DqpiH3BP+y6n
XN70PWNY8b8wwOECIpLCi6cnLBSdpGEJIQoammNbLBa2afSnD4IcxeTZ/5pCzRCv
k0vsaTwyJdEw8/3HbCcxStiAIMUzh1dPK7vpkOM4Ejc1PnqytYgoUKPKw+bGhrFw
h11VVdCosOkSyUnTyFPTg9IlS/NUoeZErpaS30+daJg58hT9dpzOffeqr+EhQAkf
a+5TyWsNhZZjrOe5Noy8UcvcCcVmv2Jt9m+jluTxwwgJ96ZdkEPXQp2yilBmuZSX
DjAbABEBAAHCw4QEGAEKAA8FAlwYl/4FCQ8JnAACGy4CKQkQ18dfLSSDPD/BXSAE
GQEKAAYFAlwYl/4ACgkQPs2jJIAwA6I+JQ//az7iPtR0tTmo65QK06ro64N0ZFs0
FIlHQ5mDj+FNctYBWhw6qnWtWboiDCcxkxy+LgqdVQaFr/b/FWySG71YwJ91aDlc
QQsy6OP29OWNrIjynx4tFI+cAhP9pPSUbR9zvC8MHzGFRXZCOfCSEXQtj48/bIZ+
wHXGRrf6uDu6pOeR2Xv/fQ1qAqk5vhpzBJ28zI0m//EpN8w8ELAgAUtCKIfsTog7
V5GIZu91FLwU+uuStQxdW5SPetaHF8Xo/JUZSaZgSCNGp/GABLqPjoGHe5FbNtyb
dzM8aTfTFqYJ89nOj2pMo/FsUH+9tvJki8ou5+VXlbyg8W9p0MvtXVjXyxBco85j
jBdfVkWqLtVxmKG3IihVAj57Cyo6OOT8Dfy/g7I/6TACaVyQAWeNqCVquRpGWvOa
k0Zmasiq63Romzn7G6KM6MsqWfX+Qn1WDkh3HQFp7+GHOdm69jzQSpjdR0BP2AOG
E3F311/AvXweZgzHkQSabb5gi3aKimPtNXUJHP2RwhJX6sbIWLuGfQ3Tm9q9ThqI
7M/XmTvWASYnlY2M4jGWXa2WRVxmRIKupVDIuxgXnLxcb8W++lo7OHX+Dpe/6Tie
8CCpgEW+6apHpwfB++iwFRPUilzBiKUiEd637o4LqfNaenphiA7OgitYcaR0cplG
rohydtUX+jSbf5Zv6Q/9ExU4QihX1CrP5TAmIcGW8XYLpZl+4rfiKzL8qLPontcy
QB7k1gBPywyiW/I0K9Zs5dz2GnSIUSDOPO3X+Txij6ZXLhlu6p911BYZOU2IAnNf
cQLTx8VaYk+qOYDJn7OKBz2ypPfW/X6whEF1prUr8t+79aJ8KoxZHNL6WMJRdoEL
tq6bN0TFeU1NoSSNsJeZBl52wFyL599VuP4PeBSCZYcMi7aps7VPCnJdUoN6j9wx
Xu+mZOylNZ3CynVZNYNjZEVE4+8YY66Ag7hCrVr6VQqB4JJUM/jq5AiLG/EUIa5i
2LLTbb8crKUpIbq94N74XtADVAq/rEpuV9ftmF3IjV4+ajqKnuKMIMA6wLqJeOc4
C65VFgWwgmkERxxR17s/wnRJ3aDX5fl14J7G85seKUGj4znv8HlnjHy9txTp5MJo
uTpBTOYTrAb7U/jcJx1cbBBTdd8B3slOmuE2QPc+cnQUNJXE7EeUHkhrf4m7WXcr
u9Xg9f0y6k2FqsCyeFEMQ/sx9nWz9JbdhP2Sz5L7oIzBPZ7dGokKvHRFI8QDtOKm
VmxxeAxd3lAH5VQJQLSkv1/z4RaIOOhtvSMKZXqNyqkP3L+HSN9i3XmIwzaySCLT
s/ybKBh7UG+eyd7q8tXyXpLeY+Z4s0vhcBRtbmJTj2V6f0N6yN4NrPyfG8mfokg=
=lYVV
-----END PGP PUBLIC KEY BLOCK-----

No Plan.
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# finger jil@192.31.205.3
Login: jil                              Name: jil
Directory: /home/jil                    Shell: /bin/bash
Never logged in.
No mail.
Plan:
Call John
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# finger tim@192.31.205.3
Login: tim                              Name: tim
Directory: /home/tim                    Shell: /bin/bash
Last login Tue Dec 18 07:52 2018 (UTC) on pts/0
No mail.
Project:
Project FingerReconLab
No Plan.
root@attackdefense:~#
```

----

###### Questions

- How many of users present in user list /usr/share/metasploit-framework/data/wordlist/unix_users.txt, are also present on the server?

```
# auxiliary/scanner/finger/finger_users
27
```

- What is the office phone number of user admin?

```
# finger admin@192.31.205.3
978-272-5420
```

- Three flags are deliberately hidden in the information served by finger service. Find all three flags.

```
# finger gopher@192.31.205.3
# finger diag@192.31.205.3
# finger webmaster@192.31.205.3
098F6BCD4621D373CADE4E832627B4F6
F765F7A0A169F4F6654EE72A84A9EB
C4CA4238A0B923820DCC509A6F75849B
```

- The email of user “tom” are forwarded to which user?

```
# finger tom@192.31.205.3
camilia
```

- Find the details of project on which user “tim” is working.

```
# finger tim@192.31.205.3
FingerReconLab
```

- Which users among “tim”,”jim”,”jil”,”tom” and “john” have a pgpkey?

```
# finger jim@192.31.205.3
jim
```

- What is the plan of user “jil”?

```
# finger jil@192.31.205.3
Call John
```

- Find the date and time at which user “tim” logged in to the system.

```
# finger tim@192.31.205.3
Tue Dec 18 07:52 2018 (UTC)
```

----

EOF