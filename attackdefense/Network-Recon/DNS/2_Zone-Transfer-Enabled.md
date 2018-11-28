#### 2. Zone Transfer Enabled

###### Attacker Info

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
5253: eth0@if5254: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:08 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.8/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
5256: eth1@if5257: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:6f:5a:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.111.90.2/24 brd 192.111.90.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~#
```

###### Zone Transfer

```sh
root@attackdefense:~# nmap -sP 192.111.90.2/24
Starting Nmap 7.70 ( https://nmap.org ) at 2018-11-28 01:35 UTC
Nmap scan report for 192.111.90.1
Host is up (0.000054s latency).
MAC Address: 02:42:10:0E:C1:4C (Unknown)
Nmap scan report for gx5ejib8nxwmfwfarv9uznsc7.temp-network_a-111-90 (192.111.90.3)
Host is up (0.000018s latency).
MAC Address: 02:42:C0:6F:5A:03 (Unknown)
Nmap scan report for attackdefense.com (192.111.90.2)
Host is up.
Nmap done: 256 IP addresses (3 hosts up) scanned in 14.99 seconds
root@attackdefense:~#
```

```sh
root@attackdefense:~# nmap 192.111.90.3
Starting Nmap 7.70 ( https://nmap.org ) at 2018-11-28 01:36 UTC
Nmap scan report for gx5ejib8nxwmfwfarv9uznsc7.temp-network_a-111-90 (192.111.90.3)
Host is up (0.000012s latency).
Not shown: 999 closed ports
PORT   STATE SERVICE
53/tcp open  domain
MAC Address: 02:42:C0:6F:5A:03 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.26 seconds
root@attackdefense:~#
```

```sh
root@attackdefense:~# dig -t AXFR witrap.com @192.111.90.3

; <<>> DiG 9.11.4-4-Debian <<>> -t AXFR witrap.com @192.111.90.3
;; global options: +cmd
witrap.com.             86400   IN      SOA     primary.witrap.com. root.witrap.com. 2011071001 3600 1800 604800 86400
witrap.com.             86400   IN      CAA     0 issue "witrapselfcert.com"
witrap.com.             86400   IN      LOC     37 46 29.744 N 122 25 9.904 W 32.00m 1m 10000m 10m
witrap.com.             86400   IN      A       192.168.60.5
witrap.com.             86400   IN      NS      primary.witrap.com.
witrap.com.             86400   IN      NS      secondary.witrap.com.
witrap.com.             86400   IN      MX      10 mx.witrap.com.
witrap.com.             86400   IN      MX      20 mx2.witrap.com.
witrap.com.             86400   IN      AAAA    2001:db8::11:0:0:11
_ldap._tcp.witrap.com.  3600    IN      SRV     10 10 389 ldap.witrap.com.
free.witrap.com.        86400   IN      A       192.168.60.100
ldap.witrap.com.        86400   IN      A       192.168.62.111
mx.witrap.com.          86400   IN      A       192.168.65.110
mx2.witrap.com.         86400   IN      A       192.168.65.150
open.witrap.com.        86400   IN      CNAME   free.witrap.com.
primary.witrap.com.     86400   IN      A       192.168.60.14
reserved.witrap.com.    86400   IN      A       192.168.62.81
secondary.witrap.com.   86400   IN      A       192.168.66.15
th3s3cr3tflag.witrap.com. 86400 IN      A       192.168.61.35
th3s3cr3tflag.witrap.com. 86400 IN      TXT     "Here is your secret flag: my_s3cr3t_fl4g"
witrap.com.             86400   IN      SOA     primary.witrap.com. root.witrap.com. 2011071001 3600 1800 604800 86400
;; Query time: 0 msec
;; SERVER: 192.111.90.3#53(192.111.90.3)
;; WHEN: Wed Nov 28 01:36:34 UTC 2018
;; XFR size: 21 records (messages 1, bytes 584)

root@attackdefense:~#
```

- How many A Records are present for witrap.com and its subdomains?

```sh
root@attackdefense:~# dig -t AXFR witrap.com @192.111.90.3 | grep -w "A" | wc -l
9
root@attackdefense:~#
```

Number of A Records are present for witrap.com and its subdomains &rarr; `9`

----

- What is the IP address of machine which support LDAP over TCP on witrap.com?

```sh
root@attackdefense:~# dig -t AXFR witrap.com @192.111.90.3 | grep ldap
_ldap._tcp.witrap.com.  3600    IN      SRV     10 10 389 ldap.witrap.com.
ldap.witrap.com.        86400   IN      A       192.168.62.111
root@attackdefense:~#
```

IP address of machine which support LDAP over TCP on witrap.com &rarr; `192.168.62.111`

----

- Can you find the secret flag in TXT record of a subdomain of witrap.com?

```sh
root@attackdefense:~# dig -t AXFR witrap.com @192.111.90.3 | grep TXT
th3s3cr3tflag.witrap.com. 86400 IN      TXT     "Here is your secret flag: my_s3cr3t_fl4g"
root@attackdefense:~#
```

Secret flag in TXT record of a subdomain of witrap.com &rarr; `my_s3cr3t_fl4g`

----

- What is the subdomain for which only reverse dns entry exists for witrap.com? witrap owns the ip address range: `192.168.*.*`

[`DNS Resolution using nmap`](https://nmap.org/book/host-discovery-dns.html)

[`Is there any Nmap script for Reverse DNS Lookup ? Thanks`](https://seclists.org/nmap-dev/2012/q2/422)

```sh
root@attackdefense:~# nmap -R -sL --dns-servers 192.111.90.3 -Pn 192.168.*.* | grep '('
Starting Nmap 7.70 ( https://nmap.org ) at 2018-11-28 01:40 UTC
Nmap scan report for witrap.com.168.192.in-addr.arpa (192.168.60.5)
Nmap scan report for primary.witrap.com (192.168.60.14)
Nmap scan report for free.witrap.com (192.168.60.100)
Nmap scan report for th3s3cr3tflag.witrap.com (192.168.61.35)
Nmap scan report for reserved.witrap.com (192.168.62.81)
Nmap scan report for ldap.witrap.com (192.168.62.111)
Nmap scan report for temp.witrap.com (192.168.62.118)
Nmap scan report for mx.witrap.com (192.168.65.110)
Nmap scan report for mx2.witrap.com (192.168.65.150)
Nmap scan report for secondary.witrap.com (192.168.66.15)
Nmap done: 65536 IP addresses (0 hosts up) scanned in 5.50 seconds
root@attackdefense:~#
```

Subdomain for which only reverse dns entry exists for witrap.com &rarr; `temp.witrap.com`

----

- How many records are present in reverse zone for witrap.com (excluding SOA)? witrap owns the ip address range: `192.168.*.*`

```sh
root@attackdefense:~# nmap -R -sL --dns-servers 192.111.90.3 -Pn 192.168.*.* | grep '(' | grep "Nmap scan report for" | wc -l
10
root@attackdefense:~#
```

No. of records are present in reverse zone for witrap.com &rarr; `10`

----

EOF