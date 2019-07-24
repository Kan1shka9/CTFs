#### 2. Samba Recon: Basics II

----

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2463: eth0@if2464: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:08 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.8/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
2466: eth1@if2467: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:5d:b8:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.93.184.2/24 brd 192.93.184.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# nmap -sV -sC 192.93.184.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 08:03 UTC
Nmap scan report for hzinr84sah8qdw9u75l4c4qer.temp-network_a-93-184 (192.93.184.3)
Host is up (0.000013s latency).
Not shown: 998 closed ports
PORT    STATE SERVICE     VERSION
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: RECONLABS)
445/tcp open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: RECONLABS)
MAC Address: 02:42:C0:5D:B8:03 (Unknown)
Service Info: Host: SAMBA-RECON

Host script results:
|_nbstat: NetBIOS name: SAMBA-RECON, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery:
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: victim-1
|   NetBIOS computer name: SAMBA-RECON\x00
|   Domain name: \x00
|   FQDN: victim-1
|_  System time: 2019-07-24T08:03:20+00:00
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2019-07-24 08:03:20
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.89 seconds
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# rpcclient -U "" -N 192.93.184.3
rpcclient $> srvinfo
        SAMBA-RECON    Wk Sv PrQ Unx NT SNT samba.recon.lab
        platform_id     :       500
        os version      :       6.1
        server type     :       0x809a03
rpcclient $>
```

----

```sh
root@attackdefense:~# enum4linux 192.93.184.3
Starting enum4linux v0.8.9 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Wed Jul 24 08:09:26 2019

 ==========================
|    Target Information    |
 ==========================
Target ........... 192.93.184.3
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ====================================================
|    Enumerating Workgroup/Domain on 192.93.184.3    |
 ====================================================
[+] Got domain/workgroup name: RECONLABS

 ============================================
|    Nbtstat Information for 192.93.184.3    |
 ============================================
Looking up status of 192.93.184.3
        SAMBA-RECON     <00> -         H <ACTIVE>  Workstation Service
        SAMBA-RECON     <03> -         H <ACTIVE>  Messenger Service
        SAMBA-RECON     <20> -         H <ACTIVE>  File Server Service
        ..__MSBROWSE__. <01> - <GROUP> H <ACTIVE>  Master Browser
        RECONLABS       <00> - <GROUP> H <ACTIVE>  Domain/Workgroup Name
        RECONLABS       <1d> -         H <ACTIVE>  Master Browser
        RECONLABS       <1e> - <GROUP> H <ACTIVE>  Browser Service Elections

        MAC Address = 00-00-00-00-00-00

 =====================================
|    Session Check on 192.93.184.3    |
 =====================================
[+] Server 192.93.184.3 allows sessions using username '', password ''

 ===========================================
|    Getting domain SID for 192.93.184.3    |
 ===========================================
Domain Name: RECONLABS
Domain Sid: (NULL SID)
[+] Can't determine if host is part of domain or part of a workgroup

 ======================================
|    OS information on 192.93.184.3    |
 ======================================
Use of uninitialized value $os_info in concatenation (.) or string at ./enum4linux.pl line 464.
[+] Got OS info for 192.93.184.3 from smbclient:
[+] Got OS info for 192.93.184.3 from srvinfo:
        SAMBA-RECON    Wk Sv PrQ Unx NT SNT samba.recon.lab
        platform_id     :       500
        os version      :       6.1
        server type     :       0x809a03

 =============================
|    Users on 192.93.184.3    |
 =============================
index: 0x1 RID: 0x3e8 acb: 0x00000010 Account: john     Name:   Desc:
index: 0x2 RID: 0x3ea acb: 0x00000010 Account: elie     Name:   Desc:
index: 0x3 RID: 0x3ec acb: 0x00000010 Account: aisha    Name:   Desc:
index: 0x4 RID: 0x3e9 acb: 0x00000010 Account: shawn    Name:   Desc:
index: 0x5 RID: 0x3eb acb: 0x00000010 Account: emma     Name:   Desc:
index: 0x6 RID: 0x3ed acb: 0x00000010 Account: admin    Name:   Desc:

user:[john] rid:[0x3e8]
user:[elie] rid:[0x3ea]
user:[aisha] rid:[0x3ec]
user:[shawn] rid:[0x3e9]
user:[emma] rid:[0x3eb]
user:[admin] rid:[0x3ed]

 =========================================
|    Share Enumeration on 192.93.184.3    |
 =========================================

        Sharename       Type      Comment
        ---------       ----      -------
        public          Disk
        john            Disk
        aisha           Disk
        emma            Disk
        everyone        Disk
        IPC$            IPC       IPC Service (samba.recon.lab)
Reconnecting with SMB1 for workgroup listing.

        Server               Comment
        ---------            -------

        Workgroup            Master
        ---------            -------
        RECONLABS            SAMBA-RECON

[+] Attempting to map shares on 192.93.184.3
//192.93.184.3/public   Mapping: OK, Listing: OK
//192.93.184.3/john     Mapping: DENIED, Listing: N/A
//192.93.184.3/aisha    Mapping: DENIED, Listing: N/A
//192.93.184.3/emma     Mapping: DENIED, Listing: N/A
//192.93.184.3/everyone Mapping: DENIED, Listing: N/A
//192.93.184.3/IPC$     [E] Can't understand response:
NT_STATUS_OBJECT_NAME_NOT_FOUND listing \*

 ====================================================
|    Password Policy Information for 192.93.184.3    |
 ====================================================


[+] Attaching to 192.93.184.3 using a NULL share

[+] Trying protocol 445/SMB...

[+] Found domain(s):

        [+] SAMBA-RECON
        [+] Builtin

[+] Password Info for Domain: SAMBA-RECON

        [+] Minimum password length: 5
        [+] Password history length: None
        [+] Maximum password age: 37 days 6 hours 21 minutes
        [+] Password Complexity Flags: 000000

                [+] Domain Refuse Password Change: 0
                [+] Domain Password Store Cleartext: 0
                [+] Domain Password Lockout Admins: 0
                [+] Domain Password No Clear Change: 0
                [+] Domain Password No Anon Change: 0
                [+] Domain Password Complex: 0

        [+] Minimum password age: None
        [+] Reset Account Lockout Counter: 30 minutes
        [+] Locked Account Duration: 30 minutes
        [+] Account Lockout Threshold: None
        [+] Forced Log off Time: 37 days 6 hours 21 minutes


[+] Retieved partial password policy with rpcclient:

Password Complexity: Disabled
Minimum Password Length: 5


 ==============================
|    Groups on 192.93.184.3    |
 ==============================

[+] Getting builtin groups:

[+] Getting builtin group memberships:

[+] Getting local groups:
group:[Testing] rid:[0x3f0]

[+] Getting local group memberships:

[+] Getting domain groups:
group:[Maintainer] rid:[0x3ee]
group:[Reserved] rid:[0x3ef]

[+] Getting domain group memberships:

 =======================================================================
|    Users on 192.93.184.3 via RID cycling (RIDS: 500-550,1000-1050)    |
 =======================================================================
[I] Found new SID: S-1-22-2
[I] Found new SID: S-1-22-1
[I] Found new SID: S-1-5-21-4056189605-2085045094-1961111545
[I] Found new SID: S-1-5-32
[+] Enumerating users using SID S-1-5-32 and logon username '', password ''
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
[+] Enumerating users using SID S-1-22-2 and logon username '', password ''
S-1-22-2-1000 Unix Group\admins (Domain Group)
S-1-22-2-1001 Unix Group\Maintainer (Domain Group)
S-1-22-2-1002 Unix Group\Reserved (Domain Group)
S-1-22-2-1003 Unix Group\Testing (Domain Group)
[+] Enumerating users using SID S-1-22-1 and logon username '', password ''
S-1-22-1-1000 Unix User\john (Local User)
S-1-22-1-1001 Unix User\shawn (Local User)
S-1-22-1-1002 Unix User\elie (Local User)
S-1-22-1-1003 Unix User\emma (Local User)
S-1-22-1-1004 Unix User\aisha (Local User)
S-1-22-1-1005 Unix User\admin (Local User)
[+] Enumerating users using SID S-1-5-21-4056189605-2085045094-1961111545 and logon username '', password ''
S-1-5-21-4056189605-2085045094-1961111545-500 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-501 SAMBA-RECON\nobody (Local User)
S-1-5-21-4056189605-2085045094-1961111545-502 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-503 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-504 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-505 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-506 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-507 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-508 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-509 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-510 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-511 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-512 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-513 SAMBA-RECON\None (Domain Group)
S-1-5-21-4056189605-2085045094-1961111545-514 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-515 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-516 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-517 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-518 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-519 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-520 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-521 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-522 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-523 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-524 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-525 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-526 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-527 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-528 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-529 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-530 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-531 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-532 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-533 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-534 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-535 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-536 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-537 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-538 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-539 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-540 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-541 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-542 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-543 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-544 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-545 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-546 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-547 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-548 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-549 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-550 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1000 SAMBA-RECON\john (Local User)
S-1-5-21-4056189605-2085045094-1961111545-1001 SAMBA-RECON\shawn (Local User)
S-1-5-21-4056189605-2085045094-1961111545-1002 SAMBA-RECON\elie (Local User)
S-1-5-21-4056189605-2085045094-1961111545-1003 SAMBA-RECON\emma (Local User)
S-1-5-21-4056189605-2085045094-1961111545-1004 SAMBA-RECON\aisha (Local User)
S-1-5-21-4056189605-2085045094-1961111545-1005 SAMBA-RECON\admin (Local User)
S-1-5-21-4056189605-2085045094-1961111545-1006 SAMBA-RECON\Maintainer (Domain Group)
S-1-5-21-4056189605-2085045094-1961111545-1007 SAMBA-RECON\Reserved (Domain Group)
S-1-5-21-4056189605-2085045094-1961111545-1008 SAMBA-RECON\Testing (Local Group)
S-1-5-21-4056189605-2085045094-1961111545-1009 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1010 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1011 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1012 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1013 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1014 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1015 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1016 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1017 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1018 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1019 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1020 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1021 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1022 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1023 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1024 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1025 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1026 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1027 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1028 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1029 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1030 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1031 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1032 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1033 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1034 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1035 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1036 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1037 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1038 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1039 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1040 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1041 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1042 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1043 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1044 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1045 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1046 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1047 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1048 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1049 *unknown*\*unknown* (8)
S-1-5-21-4056189605-2085045094-1961111545-1050 *unknown*\*unknown* (8)

 =============================================
|    Getting printer info for 192.93.184.3    |
 =============================================
No printers returned.


enum4linux complete on Wed Jul 24 08:09:47 2019

root@attackdefense:~#
```

----

```sh
root@attackdefense:~# smbclient -L //192.93.184.3 -N

        Sharename       Type      Comment
        ---------       ----      -------
        public          Disk
        john            Disk
        aisha           Disk
        emma            Disk
        everyone        Disk
        IPC$            IPC       IPC Service (samba.recon.lab)
Reconnecting with SMB1 for workgroup listing.

        Server               Comment
        ---------            -------

        Workgroup            Master
        ---------            -------
        RECONLABS            SAMBA-RECON
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# nmap -p445 --script smb-protocols 192.93.184.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 08:12 UTC
Nmap scan report for hzinr84sah8qdw9u75l4c4qer.temp-network_a-93-184 (192.93.184.3)
Host is up (0.000053s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds
MAC Address: 02:42:C0:5D:B8:03 (Unknown)

Host script results:
| smb-protocols:
|   dialects:
|     NT LM 0.12 (SMBv1) [dangerous, but default]
|     2.02
|     2.10
|     3.00
|     3.02
|_    3.11

Nmap done: 1 IP address (1 host up) scanned in 0.51 seconds
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# msfconsole
msf5 > use auxiliary/scanner/smb/smb2
msf5 auxiliary(scanner/smb/smb2) > show info

       Name: SMB 2.0 Protocol Detection
     Module: auxiliary/scanner/smb/smb2
    License: Metasploit Framework License (BSD)
       Rank: Normal

Provided by:
  hdm <x@hdm.io>

Check supported:
  Yes

Basic options:
  Name     Current Setting  Required  Description
  ----     ---------------  --------  -----------
  RHOSTS                    yes       The target address range or CIDR identifier
  RPORT    445              yes       The target port (TCP)
  THREADS  1                yes       The number of concurrent threads

Description:
  Detect systems that support the SMB 2.0 protocol

msf5 auxiliary(scanner/smb/smb2) > set RHOSTS 192.93.184.3
RHOSTS => 192.93.184.3
msf5 auxiliary(scanner/smb/smb2) > run

[+] 192.93.184.3:445      - 192.93.184.3 supports SMB 2 [dialect 255.2] and has been online for 3669008 hours
[*] 192.93.184.3:445      - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf5 auxiliary(scanner/smb/smb2) >
```

----

```sh
root@attackdefense:~# nmap --script smb-enum-users.nse -p445 192.93.184.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 08:20 UTC
Nmap scan report for hzinr84sah8qdw9u75l4c4qer.temp-network_a-93-184 (192.93.184.3)
Host is up (0.000056s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds
MAC Address: 02:42:C0:5D:B8:03 (Unknown)

Host script results:
| smb-enum-users:
|   SAMBA-RECON\admin (RID: 1005)
|     Full name:
|     Description:
|     Flags:       Normal user account
|   SAMBA-RECON\aisha (RID: 1004)
|     Full name:
|     Description:
|     Flags:       Normal user account
|   SAMBA-RECON\elie (RID: 1002)
|     Full name:
|     Description:
|     Flags:       Normal user account
|   SAMBA-RECON\emma (RID: 1003)
|     Full name:
|     Description:
|     Flags:       Normal user account
|   SAMBA-RECON\john (RID: 1000)
|     Full name:
|     Description:
|     Flags:       Normal user account
|   SAMBA-RECON\shawn (RID: 1001)
|     Full name:
|     Description:
|_    Flags:       Normal user account

Nmap done: 1 IP address (1 host up) scanned in 0.60 seconds
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# msfconsole
msf5 > search smb_enumusers

Matching Modules
================

   Name                                        Disclosure Date  Rank    Check  Description
   ----                                        ---------------  ----    -----  -----------
   auxiliary/scanner/smb/smb_enumusers                          normal  Yes    SMB User Enumeration (SAM EnumUsers)
   auxiliary/scanner/smb/smb_enumusers_domain                   normal  Yes    SMB Domain User Enumeration


msf5 > use auxiliary/scanner/smb/smb_enumusers
msf5 auxiliary(scanner/smb/smb_enumusers) > show options

Module options (auxiliary/scanner/smb/smb_enumusers):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   RHOSTS                      yes       The target address range or CIDR identifier
   SMBDomain  .                no        The Windows domain to use for authentication
   SMBPass                     no        The password for the specified username
   SMBUser                     no        The username to authenticate as
   THREADS    1                yes       The number of concurrent threads

msf5 auxiliary(scanner/smb/smb_enumusers) > set RHOSTS 192.93.184.3
RHOSTS => 192.93.184.3
msf5 auxiliary(scanner/smb/smb_enumusers) > run

[+] 192.93.184.3:139      - SAMBA-RECON [ john, elie, aisha, shawn, emma, admin ] ( LockoutTries=0 PasswordMin=5 )
[*] 192.93.184.3:         - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf5 auxiliary(scanner/smb/smb_enumusers) >
```

----

```sh
root@attackdefense:~# rpcclient -U "" 192.93.184.3 -N
rpcclient $> enumdomusers
user:[john] rid:[0x3e8]
user:[elie] rid:[0x3ea]
user:[aisha] rid:[0x3ec]
user:[shawn] rid:[0x3e9]
user:[emma] rid:[0x3eb]
user:[admin] rid:[0x3ed]
rpcclient $>
```
----

```
root@attackdefense:~# rpcclient -U "" 192.93.184.3 -N
rpcclient $> lookupnames admin
admin S-1-5-21-4056189605-2085045094-1961111545-1005 (User: 1)
rpcclient $>
```

----

###### Questions

- Find the OS version of samba server using rpcclient.

```
# rpcclient -U "" -N 192.93.184.3
6.1
```

- Find the OS version of samba server using enum4Linux.

```
# enum4linux 192.93.184.3
6.1
```

- Find the server description of samba server using smbclient.

```
# smbclient -L //192.93.184.3 -N
samba.recon.lab
```

- Is NT LM 0.12 (SMBv1) dialects supported by the samba server? Use appropriate nmap script.

```
# nmap -p445 --script smb-protocols 192.93.184.3
Supported
```

- Is SMB2 protocol supported by the samba server? Use smb2 metasploit module.

```
# auxiliary/scanner/smb/smb2
Supported
```

- List all users that exists on the samba server using appropriate nmap script.

```
# nmap --script smb-enum-users.nse -p445 192.93.184.3
```

- List all users that exists on the samba server using smb_enumusers metasploit modules.

```
auxiliary/scanner/smb/smb_enumusers
```

- List all users that exists on the samba server using enum4Linux.

```
# enum4linux 192.93.184.3
```

- List all users that exists on the samba server using rpcclient.

```
# rpcclient -U "" 192.93.184.3 -N
```

- Find SID of user “admin” using rpcclient.

```
# rpcclient -U "" 192.93.184.3 -N
S-1-5-21-4056189605-2085045094-1961111545-1005
```

----

EOF