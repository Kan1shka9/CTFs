#### 1. Samba Recon: Basics

----

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2358: eth0@if2359: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:04 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.4/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
2361: eth1@if2362: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:de:33:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.222.51.2/24 brd 192.222.51.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# nmap -sV -sC 192.222.51.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 03:53 UTC
Nmap scan report for 5hzk9w3gss5jg82uyegyc2tr5.temp-network_a-222-51 (192.222.51.3)
Host is up (0.000014s latency).
Not shown: 998 closed ports
PORT    STATE SERVICE     VERSION
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: RECONLABS)
445/tcp open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: RECONLABS)
MAC Address: 02:42:C0:DE:33:03 (Unknown)
Service Info: Host: SAMBA-RECON

Host script results:
|_nbstat: NetBIOS name: SAMBA-RECON, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery:
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: victim-1
|   NetBIOS computer name: SAMBA-RECON\x00
|   Domain name: \x00
|   FQDN: victim-1
|_  System time: 2019-07-24T03:54:01+00:00
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2019-07-24 03:54:01
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.89 seconds
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# nmap -sU 192.222.51.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 03:57 UTC
Nmap scan report for 5hzk9w3gss5jg82uyegyc2tr5.temp-network_a-222-51 (192.222.51.3)
Host is up (0.00012s latency).
Not shown: 998 closed ports
PORT    STATE         SERVICE
137/udp open          netbios-ns
138/udp open|filtered netbios-dgm
MAC Address: 02:42:C0:DE:33:03 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 1093.52 seconds
root@attackdefense:~#
```

```sh
root@attackdefense:~# nmap -sU --top-ports 25 192.222.51.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 04:42 UTC
Nmap scan report for 5hzk9w3gss5jg82uyegyc2tr5.temp-network_a-222-51 (192.222.51.3)
Host is up (0.000093s latency).

PORT      STATE         SERVICE
53/udp    closed        domain
67/udp    closed        dhcps
68/udp    closed        dhcpc
69/udp    closed        tftp
111/udp   closed        rpcbind
123/udp   open|filtered ntp
135/udp   open|filtered msrpc
137/udp   open          netbios-ns
138/udp   open|filtered netbios-dgm
139/udp   open|filtered netbios-ssn
161/udp   closed        snmp
162/udp   open|filtered snmptrap
445/udp   open|filtered microsoft-ds
500/udp   open|filtered isakmp
514/udp   open|filtered syslog
520/udp   closed        route
631/udp   closed        ipp
998/udp   open|filtered puparp
1434/udp  open|filtered ms-sql-m
1701/udp  closed        L2TP
1900/udp  closed        upnp
4500/udp  closed        nat-t-ike
5353/udp  closed        zeroconf
49152/udp open|filtered unknown
49154/udp closed        unknown
MAC Address: 02:42:C0:DE:33:03 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 8.32 seconds
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# ls -l /usr/share/nmap/scripts/*smb*
-rw-r--r-- 1 root root 45163 Nov 12  2018 /usr/share/nmap/scripts/smb-brute.nse
-rw-r--r-- 1 root root  5289 Nov 12  2018 /usr/share/nmap/scripts/smb-double-pulsar-backdoor.nse
-rw-r--r-- 1 root root  4846 Nov 12  2018 /usr/share/nmap/scripts/smb-enum-domains.nse
-rw-r--r-- 1 root root  5931 Nov 12  2018 /usr/share/nmap/scripts/smb-enum-groups.nse
-rw-r--r-- 1 root root  8045 Nov 12  2018 /usr/share/nmap/scripts/smb-enum-processes.nse
-rw-r--r-- 1 root root 27262 Nov 12  2018 /usr/share/nmap/scripts/smb-enum-services.nse
-rw-r--r-- 1 root root 12057 Nov 12  2018 /usr/share/nmap/scripts/smb-enum-sessions.nse
-rw-r--r-- 1 root root  6923 Nov 12  2018 /usr/share/nmap/scripts/smb-enum-shares.nse
-rw-r--r-- 1 root root 12531 Nov 12  2018 /usr/share/nmap/scripts/smb-enum-users.nse
-rw-r--r-- 1 root root  1706 Nov 12  2018 /usr/share/nmap/scripts/smb-flood.nse
-rw-r--r-- 1 root root  7388 Nov 12  2018 /usr/share/nmap/scripts/smb-ls.nse
-rw-r--r-- 1 root root  8792 Nov 12  2018 /usr/share/nmap/scripts/smb-mbenum.nse
-rw-r--r-- 1 root root  8220 Nov 12  2018 /usr/share/nmap/scripts/smb-os-discovery.nse
-rw-r--r-- 1 root root  5083 Nov 12  2018 /usr/share/nmap/scripts/smb-print-text.nse
-rw-r--r-- 1 root root  1898 Nov 12  2018 /usr/share/nmap/scripts/smb-protocols.nse
-rw-r--r-- 1 root root 63595 Nov 12  2018 /usr/share/nmap/scripts/smb-psexec.nse
-rw-r--r-- 1 root root  5190 Nov 12  2018 /usr/share/nmap/scripts/smb-security-mode.nse
-rw-r--r-- 1 root root  2424 Nov 12  2018 /usr/share/nmap/scripts/smb-server-stats.nse
-rw-r--r-- 1 root root 14150 Nov 12  2018 /usr/share/nmap/scripts/smb-system-info.nse
-rw-r--r-- 1 root root  7554 Nov 12  2018 /usr/share/nmap/scripts/smb-vuln-conficker.nse
-rw-r--r-- 1 root root 23153 Nov 12  2018 /usr/share/nmap/scripts/smb-vuln-cve-2017-7494.nse
-rw-r--r-- 1 root root  6432 Nov 12  2018 /usr/share/nmap/scripts/smb-vuln-cve2009-3103.nse
-rw-r--r-- 1 root root  6586 Nov 12  2018 /usr/share/nmap/scripts/smb-vuln-ms06-025.nse
-rw-r--r-- 1 root root  5444 Nov 12  2018 /usr/share/nmap/scripts/smb-vuln-ms07-029.nse
-rw-r--r-- 1 root root  5746 Nov 12  2018 /usr/share/nmap/scripts/smb-vuln-ms08-067.nse
-rw-r--r-- 1 root root  5620 Nov 12  2018 /usr/share/nmap/scripts/smb-vuln-ms10-054.nse
-rw-r--r-- 1 root root  7322 Nov 12  2018 /usr/share/nmap/scripts/smb-vuln-ms10-061.nse
-rw-r--r-- 1 root root  7145 Nov 12  2018 /usr/share/nmap/scripts/smb-vuln-ms17-010.nse
-rw-r--r-- 1 root root  4458 Nov 12  2018 /usr/share/nmap/scripts/smb-vuln-regsvc-dos.nse
-rw-r--r-- 1 root root  3355 Nov 12  2018 /usr/share/nmap/scripts/smb2-capabilities.nse
-rw-r--r-- 1 root root  3075 Nov 12  2018 /usr/share/nmap/scripts/smb2-security-mode.nse
-rw-r--r-- 1 root root  1447 Nov 12  2018 /usr/share/nmap/scripts/smb2-time.nse
-rw-r--r-- 1 root root  5238 Nov 12  2018 /usr/share/nmap/scripts/smb2-vuln-uptime.nse
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# nmap --script=smb-os-discovery 192.222.51.3
Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-24 04:35 UTC
Nmap scan report for 5hzk9w3gss5jg82uyegyc2tr5.temp-network_a-222-51 (192.222.51.3)
Host is up (0.000013s latency).
Not shown: 998 closed ports
PORT    STATE SERVICE
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
MAC Address: 02:42:C0:DE:33:03 (Unknown)

Host script results:
| smb-os-discovery:
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: victim-1
|   NetBIOS computer name: SAMBA-RECON\x00
|   Domain name: \x00
|   FQDN: victim-1
|_  System time: 2019-07-24T04:35:38+00:00

Nmap done: 1 IP address (1 host up) scanned in 0.54 seconds
root@attackdefense:~#
```

----

```sh
root@attackdefense:~# msfconsole
msf5 > search smb_version

Matching Modules
================

   Name                               Disclosure Date  Rank    Check  Description
   ----                               ---------------  ----    -----  -----------
   auxiliary/scanner/smb/smb_version                   normal  Yes    SMB Version Detection


msf5 > use auxiliary/scanner/smb/smb_version
msf5 auxiliary(scanner/smb/smb_version) > show options

Module options (auxiliary/scanner/smb/smb_version):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   RHOSTS                      yes       The target address range or CIDR identifier
   SMBDomain  .                no        The Windows domain to use for authentication
   SMBPass                     no        The password for the specified username
   SMBUser                     no        The username to authenticate as
   THREADS    1                yes       The number of concurrent threads

msf5 auxiliary(scanner/smb/smb_version) > set RHOSTS 192.222.51.3
RHOSTS => 192.222.51.3
msf5 auxiliary(scanner/smb/smb_version) > run

[*] 192.222.51.3:445      - Host could not be identified: Windows 6.1 (Samba 4.3.11-Ubuntu)
[*] 192.222.51.3:445      - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf5 auxiliary(scanner/smb/smb_version) >
```

----

```sh
root@attackdefense:~# nmblookup -A 192.222.51.3
Looking up status of 192.222.51.3
        SAMBA-RECON     <00> -         H <ACTIVE>
        SAMBA-RECON     <03> -         H <ACTIVE>
        SAMBA-RECON     <20> -         H <ACTIVE>
        ..__MSBROWSE__. <01> - <GROUP> H <ACTIVE>
        RECONLABS       <00> - <GROUP> H <ACTIVE>
        RECONLABS       <1d> -         H <ACTIVE>
        RECONLABS       <1e> - <GROUP> H <ACTIVE>

        MAC Address = 00-00-00-00-00-00

root@attackdefense:~#
```

----

```sh
root@attackdefense:~# smbclient -L 192.222.51.3
Enter WORKGROUP\GUEST's password:

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
root@attackdefense:~# rpcclient -U "" -N 192.222.51.3
rpcclient $>
```

----

###### Questions

- Find the default tcp ports used by smbd.

```
# nmap -sV -sC 192.222.51.3
139, 445
```

- Find the default udp ports used by nmbd.

```
# nmap -sU 192.222.51.3
# nmap -sU --top-ports 25 192.222.51.3
137, 138
```

- What is the workgroup name of samba server?

```
# nmap -sV -p 445 192.222.51.3
RECONLABS
```

- Find the exact version of samba server by using appropriate nmap script.

```
# nmap --script=smb-os-discovery 192.222.51.3
Samba 4.3.11-Ubuntu
```

- Find the exact version of samba server by using smb_version metasploit module.

```
# auxiliary/scanner/smb/smb_version
Samba 4.3.11-Ubuntu
```

- What is the NetBIOS computer name of samba server? Use appropriate nmap scripts.

```
# nmap --script=smb-os-discovery 192.222.51.3
SAMBA-RECON
```

- Find the NetBIOS computer name of samba server using nmblookup

```
# nmblookup -A 192.222.51.3
SAMBA-RECON
```

[`How to interpret output of nmblookup -A`](https://superuser.com/questions/710304/how-to-interpret-output-of-nmblookup-a)

- Using smbclient determine whether anonymous connection (null session)  is allowed on the samba server or not.

```
# smbclient -L 192.222.51.3
Allowed
```

- Using rpcclient determine whether anonymous connection (null session) is allowed on the samba server or not.

```
# rpcclient -U "" -N 192.222.51.3
Allowed
```

----

###### References

- [Penetration Testing Tools Cheat Sheet](https://highon.coffee/blog/penetration-testing-tools-cheat-sheet/)
- [PWK Notes: SMB Enumeration Checklist [Updated]](https://0xdf.gitlab.io/2018/12/02/pwk-notes-smb-enumeration-checklist-update1.html#check-null-sessions)
- [How to interpret output of nmblookup -A](https://superuser.com/questions/710304/how-to-interpret-output-of-nmblookup-a)

EOF