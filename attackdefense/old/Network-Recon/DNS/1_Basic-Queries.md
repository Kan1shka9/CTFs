#### 1. Basic Queries

###### Attacker Info

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
6133: eth0@if6134: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:03 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.3/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
6136: eth1@if6137: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:e6:e9:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.230.233.2/24 brd 192.230.233.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~#
```

###### Recon

- What is the ip address of primary Name server of witrap.com ?

```sh
root@attackdefense:~# nmap -sP 192.230.233.2/24
Starting Nmap 7.70 ( https://nmap.org ) at 2018-11-27 22:35 UTC
Nmap scan report for 192.230.233.1
Host is up (0.000039s latency).
MAC Address: 02:42:6C:5B:4C:89 (Unknown)
Nmap scan report for noa2osjml2jxcjzy2o618xx0j.temp-network_a-230-233 (192.230.233.3)
Host is up (0.000014s latency).
MAC Address: 02:42:C0:E6:E9:03 (Unknown)
Nmap scan report for attackdefense.com (192.230.233.2)
Host is up.
Nmap done: 256 IP addresses (3 hosts up) scanned in 15.02 seconds
root@attackdefense:~#
```

```sh
root@attackdefense:~# nmap 192.230.233.3
Starting Nmap 7.70 ( https://nmap.org ) at 2018-11-27 22:38 UTC
Nmap scan report for noa2osjml2jxcjzy2o618xx0j.temp-network_a-230-233 (192.230.233.3)
Host is up (0.000012s latency).
Not shown: 999 closed ports
PORT   STATE SERVICE
53/tcp open  domain
MAC Address: 02:42:C0:E6:E9:03 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.32 seconds
root@attackdefense:~#
```

```sh
root@attackdefense:~# nslookup
> server 192.230.233.3
Default server: 192.230.233.3
Address: 192.230.233.3#53
> set type=NS
> witrap.com
Server:         192.230.233.3
Address:        192.230.233.3#53

witrap.com      nameserver = ns2.witrap.com.
witrap.com      nameserver = ns.witrap.com.
> set type=A
> ns.witrap.com
Server:         192.230.233.3
Address:        192.230.233.3#53

Name:   ns.witrap.com
Address: 192.168.66.4
>
```

IP address of primary name server of witrap.com &rarr; `192.168.66.4` / `ns.witrap.com`

----

- What is the ipv4 address of witrap.com ?

```sh
root@attackdefense:~# nslookup
> server 192.230.233.3
Default server: 192.230.233.3
Address: 192.230.233.3#53
> witrap.com
Server:         192.230.233.3
Address:        192.230.233.3#53

Name:   witrap.com
Address: 192.168.66.2
Name:   witrap.com
Address: 2001:db8::1:0:0:13
>
```

IPv4 Address &rarr; `192.168.66.2`

----

- What is the ipv6 address of witrap.com ?

```sh
root@attackdefense:~# nslookup
> server 192.230.233.3
Default server: 192.230.233.3
Address: 192.230.233.3#53
> witrap.com
Server:         192.230.233.3
Address:        192.230.233.3#53

Name:   witrap.com
Address: 192.168.66.2
Name:   witrap.com
Address: 2001:db8::1:0:0:13
>
```

IPv6 Address &rarr; `2001:db8::1:0:0:13`

----

- How many mail server does witrap.com have?

```sh
root@attackdefense:~# nslookup
> server 192.230.233.3
Default server: 192.230.233.3
Address: 192.230.233.3#53
> set type=MX
> witrap.com
Server:         192.230.233.3
Address:        192.230.233.3#53

witrap.com      mail exchanger = 20 mail2.witrap.com.
witrap.com      mail exchanger = 10 mail.witrap.com.
>
```

Mail servers &rarr; `mail.witrap.com` & `mail2.witrap.com`

Smaller preference number has higher priority. So `mail.witrap.com` has higher priority as the preference number is 10

----

- What is the IP address of Mail Server of witrap.com which has highest priority?

```sh
root@attackdefense:~# nslookup
> server 192.230.233.3
Default server: 192.230.233.3
Address: 192.230.233.3#53
> set type=MX
> witrap.com
Server:         192.230.233.3
Address:        192.230.233.3#53

witrap.com      mail exchanger = 20 mail2.witrap.com.
witrap.com      mail exchanger = 10 mail.witrap.com.
> set type=A
> mail.witrap.com
Server:         192.230.233.3
Address:        192.230.233.3#53

Name:   mail.witrap.com
Address: 192.168.66.10
>
```

IP address of Mail Server of witrap.com which has highest priority &rarr; `192.168.66.10`

----

- What is the Canonical Name of www.witrap.com?

```sh
root@attackdefense:~# nslookup
> server 192.230.233.3
Default server: 192.230.233.3
Address: 192.230.233.3#53
> set type=CNAME
> www.witrap.com
Server:         192.230.233.3
Address:        192.230.233.3#53

www.witrap.com  canonical name = public.witrap.com.
>
```

Canonical Name of www.witrap.com &rarr; `public.witrap.com`

----

- Which Certificate Authorities can Issue certificate for witrap.com?

```sh
root@attackdefense:~# nslookup
> server 192.230.233.3
Default server: 192.230.233.3
Address: 192.230.233.3#53
> set type=ANY
> witrap.com
Server:         192.230.233.3
Address:        192.230.233.3#53

witrap.com
        origin = ns.witrap.com
        mail addr = root.witrap.com
        serial = 2011071001
        refresh = 3600
        retry = 1800
        expire = 604800
        minimum = 86400
witrap.com      nameserver = ns.witrap.com.
witrap.com      nameserver = ns2.witrap.com.
witrap.com      mail exchanger = 20 mail2.witrap.com.
witrap.com      mail exchanger = 10 mail.witrap.com.
Name:   witrap.com
Address: 2001:db8::1:0:0:13
witrap.com      text = "FLAG: txt_r3c0rd_0f_witr4p"
witrap.com      rdata_257 = 0 issue "witrapselfcert.com"
witrap.com      loc = 37 46 29.744 N 122 25 9.904 W 32.00m 1m 10000m 10m
Name:   witrap.com
Address: 192.168.66.2
>
```

Certificate Authorities that can Issue certificate for witrap.com &rarr; `witrapselfcert.com`

----

- What is the Geographical location of witrap.com ?

```sh
root@attackdefense:~# nslookup
> server 192.230.233.3
Default server: 192.230.233.3
Address: 192.230.233.3#53
> set type=ANY
> witrap.com
Server:         192.230.233.3
Address:        192.230.233.3#53

witrap.com
        origin = ns.witrap.com
        mail addr = root.witrap.com
        serial = 2011071001
        refresh = 3600
        retry = 1800
        expire = 604800
        minimum = 86400
witrap.com      nameserver = ns.witrap.com.
witrap.com      nameserver = ns2.witrap.com.
witrap.com      mail exchanger = 20 mail2.witrap.com.
witrap.com      mail exchanger = 10 mail.witrap.com.
Name:   witrap.com
Address: 2001:db8::1:0:0:13
witrap.com      text = "FLAG: txt_r3c0rd_0f_witr4p"
witrap.com      rdata_257 = 0 issue "witrapselfcert.com"
witrap.com      loc = 37 46 29.744 N 122 25 9.904 W 32.00m 1m 10000m 10m
Name:   witrap.com
Address: 192.168.66.2
>
```

Geographical location of witrap.com &rarr; `37 46 29.744 N 122 25 9.904 W 32.00m 1m 10000m 10m`

----

- Can you find the flag provided in the information of witrap.com?

```sh
root@attackdefense:~# nslookup
> server 192.230.233.3
Default server: 192.230.233.3
Address: 192.230.233.3#53
> set type=ANY
> witrap.com
Server:         192.230.233.3
Address:        192.230.233.3#53

witrap.com
        origin = ns.witrap.com
        mail addr = root.witrap.com
        serial = 2011071001
        refresh = 3600
        retry = 1800
        expire = 604800
        minimum = 86400
witrap.com      nameserver = ns.witrap.com.
witrap.com      nameserver = ns2.witrap.com.
witrap.com      mail exchanger = 20 mail2.witrap.com.
witrap.com      mail exchanger = 10 mail.witrap.com.
Name:   witrap.com
Address: 2001:db8::1:0:0:13
witrap.com      text = "FLAG: txt_r3c0rd_0f_witr4p"
witrap.com      rdata_257 = 0 issue "witrapselfcert.com"
witrap.com      loc = 37 46 29.744 N 122 25 9.904 W 32.00m 1m 10000m 10m
Name:   witrap.com
Address: 192.168.66.2
>
```

Flag provided in the information of witrap.com &rarr; `FLAG: txt_r3c0rd_0f_witr4p`

----

- What is the IP address of machine which support sip over TCP on witrap.com?

```sh
root@attackdefense:~# nslookup
> server 192.230.233.3
Default server: 192.230.233.3
Address: 192.230.233.3#53
> set type=A
> sip.witrap.com
Server:         192.230.233.3
Address:        192.230.233.3#53

Name:   sip.witrap.com
Address: 192.168.66.155
>
```

IP address of machine which support sip over TCP on witrap.com &rarr; `192.168.66.155`

----

- What is the administrative email of witrap.com?

```sh
root@attackdefense:~# nslookup
> server 192.230.233.3
Default server: 192.230.233.3
Address: 192.230.233.3#53
> set type=ANY
> witrap.com
Server:         192.230.233.3
Address:        192.230.233.3#53

witrap.com
        origin = ns.witrap.com
        mail addr = root.witrap.com
        serial = 2011071001
        refresh = 3600
        retry = 1800
        expire = 604800
        minimum = 86400
witrap.com      nameserver = ns.witrap.com.
witrap.com      nameserver = ns2.witrap.com.
witrap.com      mail exchanger = 20 mail2.witrap.com.
witrap.com      mail exchanger = 10 mail.witrap.com.
Name:   witrap.com
Address: 2001:db8::1:0:0:13
witrap.com      text = "FLAG: txt_r3c0rd_0f_witr4p"
witrap.com      rdata_257 = 0 issue "witrapselfcert.com"
witrap.com      loc = 37 46 29.744 N 122 25 9.904 W 32.00m 1m 10000m 10m
Name:   witrap.com
Address: 192.168.66.2
>
```

Administrative email of witrap.com &rarr; `root.witrap.com`

----

- Which domain corresponds to 192.168.67.8 ?

```sh
root@attackdefense:~# nslookup
> server 192.230.233.3
Default server: 192.230.233.3
Address: 192.230.233.3#53
> set type=A
> 192.168.67.8
Server:         192.230.233.3
Address:        192.230.233.3#53

8.67.168.192.in-addr.arpa       name = private.witrap.com.
>
```

Domain corresponds to 192.168.67.8 &rarr; `private.witrap.com`

----

EOF