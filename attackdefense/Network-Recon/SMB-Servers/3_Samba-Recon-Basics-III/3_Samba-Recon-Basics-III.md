#### 3. Samba Recon: Basics III

----

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
1864: eth0@if1865: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:08 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.8/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
1867: eth1@if1868: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:f4:de:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.244.222.2/24 brd 192.244.222.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# nmap -sC -sV 192.244.222.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 08:33 UTC
Nmap scan report for u31hic39sfpozjn8kpebmkku7.temp-network_a-244-222 (192.244.222.3)
Host is up (0.000013s latency).
Not shown: 998 closed ports
PORT    STATE SERVICE     VERSION
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: RECONLABS)
445/tcp open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: RECONLABS)
MAC Address: 02:42:C0:F4:DE:03 (Unknown)
Service Info: Host: SAMBA-RECON

Host script results:
|_nbstat: NetBIOS name: SAMBA-RECON, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery:
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: victim-1
|   NetBIOS computer name: SAMBA-RECON\x00
|   Domain name: \x00
|   FQDN: victim-1
|_  System time: 2019-07-24T08:34:10+00:00
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2019-07-24 08:34:10
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.88 seconds
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# nmap --script smb-enum-shares.nse -p445 192.244.222.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 08:37 UTC
Nmap scan report for u31hic39sfpozjn8kpebmkku7.temp-network_a-244-222 (192.244.222.3)
Host is up (0.000049s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds
MAC Address: 02:42:C0:F4:DE:03 (Unknown)

Host script results:
| smb-enum-shares:
|   account_used: guest
|   \\192.244.222.3\IPC$:
|     Type: STYPE_IPC_HIDDEN
|     Comment: IPC Service (samba.recon.lab)
|     Users: 1
|     Max Users: <unlimited>
|     Path: C:\tmp
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\192.244.222.3\aisha:
|     Type: STYPE_DISKTREE
|     Comment:
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\samba\aisha
|     Anonymous access: <none>
|     Current user access: <none>
|   \\192.244.222.3\emma:
|     Type: STYPE_DISKTREE
|     Comment:
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\samba\emma
|     Anonymous access: <none>
|     Current user access: <none>
|   \\192.244.222.3\everyone:
|     Type: STYPE_DISKTREE
|     Comment:
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\samba\everyone
|     Anonymous access: <none>
|     Current user access: <none>
|   \\192.244.222.3\john:
|     Type: STYPE_DISKTREE
|     Comment:
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\samba\john
|     Anonymous access: <none>
|     Current user access: <none>
|   \\192.244.222.3\public:
|     Type: STYPE_DISKTREE
|     Comment:
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\samba\public
|     Anonymous access: READ/WRITE
|_    Current user access: READ/WRITE

Nmap done: 1 IP address (1 host up) scanned in 1.09 seconds
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# msfconsole
msf5 > use auxiliary/scanner/smb/smb_enumshares
msf5 auxiliary(scanner/smb/smb_enumshares) > show options

Module options (auxiliary/scanner/smb/smb_enumshares):

   Name            Current Setting  Required  Description
   ----            ---------------  --------  -----------
   LogSpider       3                no        0 = disabled, 1 = CSV, 2 = table (txt), 3 = one liner (txt) (Accepted: 0, 1, 2, 3)
   MaxDepth        999              yes       Max number of subdirectories to spider
   RHOSTS                           yes       The target address range or CIDR identifier
   SMBDomain       .                no        The Windows domain to use for authentication
   SMBPass                          no        The password for the specified username
   SMBUser                          no        The username to authenticate as
   ShowFiles       false            yes       Show detailed information when spidering
   SpiderProfiles  true             no        Spider only user profiles when share = C$
   SpiderShares    false            no        Spider shares recursively
   THREADS         1                yes       The number of concurrent threads

msf5 auxiliary(scanner/smb/smb_enumshares) > set RHOSTS 192.244.222.3
RHOSTS => 192.244.222.3
msf5 auxiliary(scanner/smb/smb_enumshares) > run

[+] 192.244.222.3:139     - public - (DS)
[+] 192.244.222.3:139     - john - (DS)
[+] 192.244.222.3:139     - aisha - (DS)
[+] 192.244.222.3:139     - emma - (DS)
[+] 192.244.222.3:139     - everyone - (DS)
[+] 192.244.222.3:139     - IPC$ - (I) IPC Service (samba.recon.lab)
[*] 192.244.222.3:        - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf5 auxiliary(scanner/smb/smb_enumshares) >
```

----

```sh
root@attackdefense:~# enum4linux -S 192.244.222.3
Starting enum4linux v0.8.9 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Wed Jul 24 08:51:27 2019

 ==========================
|    Target Information    |
 ==========================
Target ........... 192.244.222.3
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 =====================================================
|    Enumerating Workgroup/Domain on 192.244.222.3    |
 =====================================================
[+] Got domain/workgroup name: RECONLABS

 ======================================
|    Session Check on 192.244.222.3    |
 ======================================
[+] Server 192.244.222.3 allows sessions using username '', password ''

 ============================================
|    Getting domain SID for 192.244.222.3    |
 ============================================
Domain Name: RECONLABS
Domain Sid: (NULL SID)
[+] Can't determine if host is part of domain or part of a workgroup

 ==========================================
|    Share Enumeration on 192.244.222.3    |
 ==========================================

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

[+] Attempting to map shares on 192.244.222.3
//192.244.222.3/public  Mapping: OK, Listing: OK
//192.244.222.3/john    Mapping: DENIED, Listing: N/A
//192.244.222.3/aisha   Mapping: DENIED, Listing: N/A
//192.244.222.3/emma    Mapping: DENIED, Listing: N/A
//192.244.222.3/everyone        Mapping: DENIED, Listing: N/A
//192.244.222.3/IPC$    [E] Can't understand response:
NT_STATUS_OBJECT_NAME_NOT_FOUND listing \*
enum4linux complete on Wed Jul 24 08:51:27 2019

root@attackdefense:~#
```

----

```sh
root@attackdefense:~# smbclient -L 192.244.222.3 -N

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
root@attackdefense:~# enum4linux -G 192.244.222.3
Starting enum4linux v0.8.9 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Wed Jul 24 08:52:15 2019

 ==========================
|    Target Information    |
 ==========================
Target ........... 192.244.222.3
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 =====================================================
|    Enumerating Workgroup/Domain on 192.244.222.3    |
 =====================================================
[+] Got domain/workgroup name: RECONLABS

 ======================================
|    Session Check on 192.244.222.3    |
 ======================================
[+] Server 192.244.222.3 allows sessions using username '', password ''

 ============================================
|    Getting domain SID for 192.244.222.3    |
 ============================================
Domain Name: RECONLABS
Domain Sid: (NULL SID)
[+] Can't determine if host is part of domain or part of a workgroup

 ===============================
|    Groups on 192.244.222.3    |
 ===============================

[+] Getting builtin groups:

[+] Getting builtin group memberships:

[+] Getting local groups:
group:[Testing] rid:[0x3f0]

[+] Getting local group memberships:

[+] Getting domain groups:
group:[Maintainer] rid:[0x3ee]
group:[Reserved] rid:[0x3ef]

[+] Getting domain group memberships:
enum4linux complete on Wed Jul 24 08:52:16 2019

root@attackdefense:~#
```

----

```sh
root@attackdefense:~# rpcclient -U "" -N 192.244.222.3
rpcclient $> enumdomgroups
group:[Maintainer] rid:[0x3ee]
group:[Reserved] rid:[0x3ef]
rpcclient $>
```

----

```sh
root@attackdefense:~# enum4linux -i 192.244.222.3
Starting enum4linux v0.8.9 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Wed Jul 24 08:54:22 2019

 ==========================
|    Target Information    |
 ==========================
Target ........... 192.244.222.3
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 =====================================================
|    Enumerating Workgroup/Domain on 192.244.222.3    |
 =====================================================
[+] Got domain/workgroup name: RECONLABS

 ======================================
|    Session Check on 192.244.222.3    |
 ======================================
[+] Server 192.244.222.3 allows sessions using username '', password ''

 ============================================
|    Getting domain SID for 192.244.222.3    |
 ============================================
Domain Name: RECONLABS
Domain Sid: (NULL SID)
[+] Can't determine if host is part of domain or part of a workgroup

 ==============================================
|    Getting printer info for 192.244.222.3    |
 ==============================================
No printers returned.


enum4linux complete on Wed Jul 24 08:54:22 2019

root@attackdefense:~#
```

----

```sh
root@attackdefense:~# smbclient //192.244.222.3/public -N
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Wed Jul 24 08:37:46 2019
  ..                                  D        0  Tue Nov 27 13:36:13 2018
  dev                                 D        0  Tue Nov 27 13:36:13 2018
  secret                              D        0  Tue Nov 27 13:36:13 2018

                1981832052 blocks of size 1024. 1464820164 blocks available
smb: \>
```

----

```sh
root@attackdefense:~# smbclient //192.244.222.3/public -N
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Wed Jul 24 08:37:46 2019
  ..                                  D        0  Tue Nov 27 13:36:13 2018
  dev                                 D        0  Tue Nov 27 13:36:13 2018
  secret                              D        0  Tue Nov 27 13:36:13 2018

                1981832052 blocks of size 1024. 1464819988 blocks available
smb: \> cd secret
smb: \secret\> ls
  .                                   D        0  Tue Nov 27 13:36:13 2018
  ..                                  D        0  Wed Jul 24 08:37:46 2019
  flag                                N       33  Tue Nov 27 13:36:13 2018

                1981832052 blocks of size 1024. 1464819980 blocks available
smb: \secret\> get flag
getting file \secret\flag of size 33 as flag (32.2 KiloBytes/sec) (average 32.2 KiloBytes/sec)
smb: \secret\> exit
root@attackdefense:~# cat flag
03ddb97933e716f5057a18632badb3b4
root@attackdefense:~#
```

----

###### Questions

- List all available shares on the samba server using nmap script.

```
# nmap --script smb-enum-shares.nse -p445 192.244.222.3
IPC$, aisha, emma, everyone, john, public
```

- List all available shares on the samba server using smb_enumshares metasploit module.

```
# auxiliary/scanner/smb/smb_enumshares
public, john, aisha, emma, everyone, IPC$
```

- List all available shares on the samba server using enum4Linux.

```sh
# enum4linux -S 192.244.222.3
public, john, aisha, emma, everyone, IPC$
```

- List all available shares on the samba server using smbclient.

```
# smbclient -L 192.244.222.3 -N
public, john, aisha, emma, everyone, IPC$
```

- Find domain groups that exists on the samba server by using enum4Linux.

```
# enum4linux -G 192.244.222.3
Maintainer, Reserved
```

- Find domain groups that exists on the samba server by using rpcclient.

```
# rpcclient -U "" -N 192.244.222.3 
# enumdomgroups
Maintainer, Reserved
```

- Is samba server configured for printing?

```
# enum4linux -i 192.244.222.3
No
```

- How many directories are present inside share “public”?

```
# smbclient //192.244.222.3/public -N
dev, secret
```

- Fetch the flag from samba server.

```
# smbclient //192.244.222.3/public -N
03ddb97933e716f5057a18632badb3b4
```

----

EOF