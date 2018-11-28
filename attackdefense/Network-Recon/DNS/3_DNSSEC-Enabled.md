#### 3. DNSSEC Enabled

###### Attacker Info

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
6210: eth0@if6211: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:0a:01:01:06 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.6/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
6213: eth1@if6214: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:c0:f2:fa:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.242.250.2/24 brd 192.242.250.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~#
```

###### DNSSEC Interrogation

```sh
root@attackdefense:~# nmap -sP 192.242.250.2/24
Starting Nmap 7.70 ( https://nmap.org ) at 2018-11-28 02:09 UTC
Nmap scan report for 192.242.250.1
Host is up (0.000040s latency).
MAC Address: 02:42:E2:EC:F1:1D (Unknown)
Nmap scan report for 6u9tckadrvhrx3u7x0mxhfg8i.temp-network_a-242-250 (192.242.250.3)
Host is up (0.000017s latency).
MAC Address: 02:42:C0:F2:FA:03 (Unknown)
Nmap scan report for attackdefense.com (192.242.250.2)
Host is up.
Nmap done: 256 IP addresses (3 hosts up) scanned in 14.99 seconds
root@attackdefense:~#
```

```sh
root@attackdefense:~# nmap 192.242.250.3
Starting Nmap 7.70 ( https://nmap.org ) at 2018-11-28 02:09 UTC
Nmap scan report for 6u9tckadrvhrx3u7x0mxhfg8i.temp-network_a-242-250 (192.242.250.3)
Host is up (0.000012s latency).
Not shown: 999 closed ports
PORT   STATE SERVICE
53/tcp open  domain
MAC Address: 02:42:C0:F2:FA:03 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.22 seconds
root@attackdefense:~#
```

- What is the key ID of key signing key of witrap.com?

[`Can I extract the key tag from a DNSKEY obtained via dig?`](https://deepthought.isc.org/article/AA-00610/0/Can-I-extract-the-key-tag-from-a-DNSKEY-obtained-via-dig.html)

```sh
root@attackdefense:~# dig +multi witrap.com DNSKEY @192.242.250.3

; <<>> DiG 9.11.4-4-Debian <<>> +multi witrap.com DNSKEY @192.242.250.3
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 32555
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;witrap.com.            IN DNSKEY

;; ANSWER SECTION:
witrap.com.             86400 IN DNSKEY 256 3 7 (
                                AwEAAc/J2KXA4dkUSBce20Mm+hbWUfZpWJ7lAyDDafc0
                                VovbYE/ROEIiOURFcn1yZfjWE55OtupRHx6rqq8eNEov
                                sb8ELB8BXVqNhR/b/ilgq6cKzuTFC+vCMbdFHKj/swdp
                                2DNEFtr+3Ojpz5jGa4JrN15j5/L02vrcRbb3VUDVyu8m
                                mSMUqlAozTkqHiFb490Qk5tPrHvd9Hu19NTAxlcfy4UY
                                63Zj4I7+KfuTPkt4ENdLyIqy4jXhp7cQ2uZCzOp2tJge
                                dC6Vmd9vP1sdUwuv3wRy4PBaVtM0VhMtacISfWxG4qyJ
                                VqcOVwl6Pa4pfIeRtYp7J9EV4/29M7yWS2POl3E=
                                ) ; ZSK; alg = NSEC3RSASHA1 ; key id = 47204
witrap.com.             86400 IN DNSKEY 257 3 7 (
                                AwEAAbtM3NZHtVK+rrzBYOOVTf5OV6WogTSPEhzVeNdv
                                qQnjDzawTJSUgzzmkNSII1BkMuuI4QwlXGy0ZZgg9/lf
                                zGWHzCpC6uEV8BrNKT2+04TgJ48/LAGiNi/qRRc2jUQp
                                EMo5tSnXWMDOc56C2n2g0Wq521pdiPskTWe4lwNbE4cG
                                GSwWvnnY+0QFJInYDv7vR5MSnQUyGlFfTTW6WX16fvyN
                                QMPJAiTBnqyNP2+GkjWX+5xm+rtp91hTEvKQONTsYryL
                                YhlFdzkSMFbBD8Rz+6Eu7Cxc3BJknBysxRA2AKmWaGD8
                                0HLSM3d1p920p4iC6YwhZ02HmjmXcZzGZzm9BTyNFcfy
                                HDxa7Qp4L2oF7h8aNCPgNB4Y70vM8UH6huejOHgR6Wkk
                                aOGwX8Ds3oKYWRhuyTael99EmsAfCiCyb0c2a0I4nwoh
                                t6XE9XEJHx5gxCXnH6MSQYrJmOzU1jefnoDcEOhiXO7n
                                Ss1TiUun482Ch3rHK9vCYPfGwhrLsYzGRRGtWZA87GST
                                CMFKCGvPzRPaB8Nj1o9TASJ9pQ2UGk8enAbYg6RSUtdb
                                zMv8t1OfaGt1dkZgrFeWkuA5I+Q0uSmBFceMgEsrDjgf
                                TQ8WwkJ9wS1bemPRJYK7yhne0bt/x7LLkyzWmcWoYnxL
                                BbR0ExESGKVurMzfHlCYtwFIvhP3
                                ) ; KSK; alg = NSEC3RSASHA1 ; key id = 47466

;; Query time: 0 msec
;; SERVER: 192.242.250.3#53(192.242.250.3)
;; WHEN: Wed Nov 28 02:27:52 UTC 2018
;; MSG SIZE  rcvd: 847

root@attackdefense:~#
```

Key ID of key signing key of witrap.com &rarr; `47466`

----

- What is the algorithm used for to create KSK and ZSK for witrap.com?

```sh
root@attackdefense:~# dig +multi witrap.com DNSKEY @192.242.250.3

; <<>> DiG 9.11.4-4-Debian <<>> +multi witrap.com DNSKEY @192.242.250.3
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 32555
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;witrap.com.            IN DNSKEY

;; ANSWER SECTION:
witrap.com.             86400 IN DNSKEY 256 3 7 (
                                AwEAAc/J2KXA4dkUSBce20Mm+hbWUfZpWJ7lAyDDafc0
                                VovbYE/ROEIiOURFcn1yZfjWE55OtupRHx6rqq8eNEov
                                sb8ELB8BXVqNhR/b/ilgq6cKzuTFC+vCMbdFHKj/swdp
                                2DNEFtr+3Ojpz5jGa4JrN15j5/L02vrcRbb3VUDVyu8m
                                mSMUqlAozTkqHiFb490Qk5tPrHvd9Hu19NTAxlcfy4UY
                                63Zj4I7+KfuTPkt4ENdLyIqy4jXhp7cQ2uZCzOp2tJge
                                dC6Vmd9vP1sdUwuv3wRy4PBaVtM0VhMtacISfWxG4qyJ
                                VqcOVwl6Pa4pfIeRtYp7J9EV4/29M7yWS2POl3E=
                                ) ; ZSK; alg = NSEC3RSASHA1 ; key id = 47204
witrap.com.             86400 IN DNSKEY 257 3 7 (
                                AwEAAbtM3NZHtVK+rrzBYOOVTf5OV6WogTSPEhzVeNdv
                                qQnjDzawTJSUgzzmkNSII1BkMuuI4QwlXGy0ZZgg9/lf
                                zGWHzCpC6uEV8BrNKT2+04TgJ48/LAGiNi/qRRc2jUQp
                                EMo5tSnXWMDOc56C2n2g0Wq521pdiPskTWe4lwNbE4cG
                                GSwWvnnY+0QFJInYDv7vR5MSnQUyGlFfTTW6WX16fvyN
                                QMPJAiTBnqyNP2+GkjWX+5xm+rtp91hTEvKQONTsYryL
                                YhlFdzkSMFbBD8Rz+6Eu7Cxc3BJknBysxRA2AKmWaGD8
                                0HLSM3d1p920p4iC6YwhZ02HmjmXcZzGZzm9BTyNFcfy
                                HDxa7Qp4L2oF7h8aNCPgNB4Y70vM8UH6huejOHgR6Wkk
                                aOGwX8Ds3oKYWRhuyTael99EmsAfCiCyb0c2a0I4nwoh
                                t6XE9XEJHx5gxCXnH6MSQYrJmOzU1jefnoDcEOhiXO7n
                                Ss1TiUun482Ch3rHK9vCYPfGwhrLsYzGRRGtWZA87GST
                                CMFKCGvPzRPaB8Nj1o9TASJ9pQ2UGk8enAbYg6RSUtdb
                                zMv8t1OfaGt1dkZgrFeWkuA5I+Q0uSmBFceMgEsrDjgf
                                TQ8WwkJ9wS1bemPRJYK7yhne0bt/x7LLkyzWmcWoYnxL
                                BbR0ExESGKVurMzfHlCYtwFIvhP3
                                ) ; KSK; alg = NSEC3RSASHA1 ; key id = 47466

;; Query time: 0 msec
;; SERVER: 192.242.250.3#53(192.242.250.3)
;; WHEN: Wed Nov 28 02:27:52 UTC 2018
;; MSG SIZE  rcvd: 847

root@attackdefense:~#
```

Algorithm used for to create KSK and ZSK for witrap.com &rarr; `NSEC3RSASHA1`

----

- What is the RRSIG A Record of witrap.com?

```sh
root@attackdefense:~# dig -t RRSIG witrap.com @192.242.250.3 | grep -w "A"
witrap.com.             86400   IN      RRSIG   A 7 2 86400 20181120150154 20181021150154 47204 witrap.com. oheCda/JJlTjPDYoskGh/YW+o8Tixx0hAHs0UtMPy91o6vZttrL0SA/5 LLmYgmTwMioBq2fhPm19tX4
NBdBec/HRHNad/yKmZYp/kC/qqMesthhg 1kKPOKrVKvtbMvW7tmMXRjaVTFIQADg2/gCnPfp8PkwwSmcJMWTS0h0i vbnoUXARddTPMY5Gnaxy2CxQK3cBHsjVnBosmChHqabNUdPPqP+X53fd Q4z2GxYkO9Y4KmVLbljIYnb45Tl+J1lL4nLxCHgI
XXL7Fzs7bziwR8bs WD0lXaJWha1MF8R9u9USS+CQzGhtOIWcZikY3RxXrBu+PmrJcHx7TaOb ssLgXw==
ns.witrap.com.          86400   IN      A       192.168.63.4
ns2.witrap.com.         86400   IN      A       192.168.67.14
root@attackdefense:~#
```

RRSIG A Record of witrap.com &rarr; `oheCda/JJlTjPDYoskGh/YW+o8Tixx0hAHs0UtMPy91o6vZttrL0SA/5 LLmYgmTwMioBq2fhPm19tX4
NBdBec/HRHNad/yKmZYp/kC/qqMesthhg 1kKPOKrVKvtbMvW7tmMXRjaVTFIQADg2/gCnPfp8PkwwSmcJMWTS0h0i vbnoUXARddTPMY5Gnaxy2CxQK3cBHsjVnBosmChHqabNUdPPqP+X53fd Q4z2GxYkO9Y4KmVLbljIYnb45Tl+J1lL4nLxCHgI
XXL7Fzs7bziwR8bs WD0lXaJWha1MF8R9u9USS+CQzGhtOIWcZikY3RxXrBu+PmrJcHx7TaOb ssLgXw==`

----

- What is the Salt used for hash Calculation for NSEC3?

```sh
root@attackdefense:~# dig -t NSEC3PARAM witrap.com @192.242.250.3

; <<>> DiG 9.11.4-4-Debian <<>> -t NSEC3PARAM witrap.com @192.242.250.3
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 40385
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 3

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;witrap.com.                    IN      NSEC3PARAM

;; ANSWER SECTION:
witrap.com.             0       IN      NSEC3PARAM 1 0 10 DBF4725BEF433A41

;; AUTHORITY SECTION:
witrap.com.             86400   IN      NS      ns2.witrap.com.
witrap.com.             86400   IN      NS      ns.witrap.com.

;; ADDITIONAL SECTION:
ns.witrap.com.          86400   IN      A       192.168.63.4
ns2.witrap.com.         86400   IN      A       192.168.67.14

;; Query time: 0 msec
;; SERVER: 192.242.250.3#53(192.242.250.3)
;; WHEN: Wed Nov 28 02:14:49 UTC 2018
;; MSG SIZE  rcvd: 131

root@attackdefense:~#
```

Salt used for hash Calculation for NSEC3 &rarr; `DBF4725BEF433A41`

----

- How many RRSIG records exists for witrap.com?

```sh
root@attackdefense:~# dig -t RRSIG witrap.com @192.242.250.3

; <<>> DiG 9.11.4-4-Debian <<>> -t RRSIG witrap.com @192.242.250.3
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 39080
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 11, AUTHORITY: 2, ADDITIONAL: 3

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;witrap.com.                    IN      RRSIG

;; ANSWER SECTION:
witrap.com.             86400   IN      RRSIG   SOA 7 2 86400 20181120150154 20181021150154 47204 witrap.com. Je4u3kbWJrLNH3AMIkAYZDG5qb81UJGRx2Fp7JFRJib5rUxxXNaIaNZE pBJbxG/UdJIeIjJTrVttJ8MgsWH3V9wpmw1ZxZGq91Gl4jjRVx4nuG/S H4EZ865GA9rh78KOWZ8MA3DkTHJl/3FFZOBhjUfJBeppReV0g5qQKhip Pj51eA3/a+F010JUGNxk1hCBgj7Pl97BzzpMHNNe28UFEloB6SgoGwhO rSUv5GxUA6keBGnaFh+CICQSKKj8AKUbbvanrI9pkNvduQntzOTrE9XW S/SifdgnJc7ssiHtnLr/1ZQv1vfGbE5oJklXl8DJ+6zr2wvWosAn0hmq pZMRvw==
witrap.com.             86400   IN      RRSIG   NS 7 2 86400 20181120150154 20181021150154 47204 witrap.com. vH0aJMa1lHeMcffiP6VyBoHkQUjRtsnRwFxeQaoqesykAgSMOXGDpJGD kt0Dqk3LGIystMqC/ZMWgZJGyim2jPJJN9/vry47AuUFQe5maXn3vA5u Urj+VJEaAx3Q1C6Cot188GXHHAJxFEtHcA8U7TIi8Iic91isuuUuLcat N9Yax/BAVJ65xRE4MV2LkqzngffocVjo2qOPBB9TLvitpF9sklspyPIx m7XCRJ9ZPRAOLu1Wd6U/q0xE7MG28mw1e1bO88+XPCJYB4eEnji7aDe0 PwwRK5zTFX6iVwyqVtl4VpiLaUX/8aeByfLKCOnZEDwmstrtAcWa4UpX 910g7w==
witrap.com.             86400   IN      RRSIG   A 7 2 86400 20181120150154 20181021150154 47204 witrap.com. oheCda/JJlTjPDYoskGh/YW+o8Tixx0hAHs0UtMPy91o6vZttrL0SA/5 LLmYgmTwMioBq2fhPm19tX4NBdBec/HRHNad/yKmZYp/kC/qqMesthhg 1kKPOKrVKvtbMvW7tmMXRjaVTFIQADg2/gCnPfp8PkwwSmcJMWTS0h0i vbnoUXARddTPMY5Gnaxy2CxQK3cBHsjVnBosmChHqabNUdPPqP+X53fd Q4z2GxYkO9Y4KmVLbljIYnb45Tl+J1lL4nLxCHgIXXL7Fzs7bziwR8bs WD0lXaJWha1MF8R9u9USS+CQzGhtOIWcZikY3RxXrBu+PmrJcHx7TaOb ssLgXw==
witrap.com.             86400   IN      RRSIG   MX 7 2 86400 20181120150154 20181021150154 47204 witrap.com. QX0T7yjc8VbalWM6UcusO+03Zoiu5ibmyryKxgXICt/Bz54buBTuf5Mf qWrAE2LEqWvhEecc7WENR6j7NYN90S9dCMaUTfpN6GjkJQ6oSR0/gscl NvThyu7gqEel/8PAMugIc//VHb/wHT2J7umx4AmYl1vtnzM5sj6X1LzS G1VAtliwB+LJRky0TjhNAGBLJccLP33DK2H/UAFKfNK/SJOXbN4UTZ0E xg5vyTTAnrPibV74kSwfm55ahi7eHVm/nMS7/zW+ARB3Fcwiq61Oq7N3 dfzQgFWPMZW/rgPNr3iMwZV3Jq4J6D3EZcV3iGZM7Rdd2XewUIRQpZ4m J/+R2Q==
witrap.com.             86400   IN      RRSIG   TXT 7 2 86400 20181120150154 20181021150154 47204 witrap.com. UCuzhWRgvsLfDoS3mCBxKsVWMUTa6WbiKHL6B5dyMrPvv3pzcbdMRxjI IurOswr70PjfiuO7uXm+nf0QnpUZyQLH56Ks3ylAJjz5WOhPbjnN6cH9 Ehd2stojKlQkeWxRDp2xJkGLGQ6kU3HA6/aDBruxVhh4z9z3rI8sMrbX jiSK1huUh8Igc8C/95mhlyOXBjzNARIyz7tiLfBLjAxZV+Bv36GwAfEq /thu/DGQUmnNqq7JObrGNd4UArQss0shQ54vG9b4gOUKfujsU6+4u+SM gYLGWJIEzKowRomvIPrJ06QE4KPDB8JqpxjkIPlKQEfTeNS9EB6odxP+ cMYe0g==
witrap.com.             86400   IN      RRSIG   AAAA 7 2 86400 20181120150154 20181021150154 47204 witrap.com. PXfPbMJXDz5PuLsP7BArY6SnYsd9LMGT2t0ra0Z4dxc8KOImcgaO4qQG JdIP2m+6jUJbTjgb4KIKYtUiffkrmWJgr6B+33PWsQowI9yVwILitM4L dW1UKleJ18c35R6mJo9T64/bqZSUyhKT2uU+GsRToL4OphXyHs0IQvRK TjYINwtoliyX+EO99C6OalC0FzjIFbvYTuCCWphMn1ujlyCtd0UWWuy/ 3jd5K31VoYSw0t5hR3t5zLum0RfvYvHYwTsg9I1WYi6PBlKTojgKNh/F UscQSWhI0cEaJeXetsS24TAd3ev2NZpaxgHI1OZNX5v3oK7QS2oVLk3y lw0Pgw==
witrap.com.             86400   IN      RRSIG   LOC 7 2 86400 20181120150154 20181021150154 47204 witrap.com. fPrC6PqBORHZV4SBUx+Pvh3wi1nc14zVJIMJUHqYdlkNk3/AoKnbJ3Uk P1nH9PGeieim19QeyMLdei1qACoR2SPO7A58u8Vv7qFsrBHcM1QqNBhY 5Eht1f7qu1RWG70CnAgd18e3+kXWo56xjyhUm/pb46ccw692bihF9HDg QJ8pWIH7kYSYk8PbaMR6ADqhHd/j+c9xwLhttxRiITv51Q5Ioinecx3X gSeZztbT46igTAzJ6tEsgsrEnPVm+9CjaE+vfGtLp/d3mdMYRppSzwSr 3NXc9+2txrb715WrjTeAVTnTD+7rsBqDAzBSAhVgtmEh3ZB3+x6pqhCa Qtf4xg==
witrap.com.             86400   IN      RRSIG   DNSKEY 7 2 86400 20181120150154 20181021150154 47204 witrap.com. quZLXwrOX7hxcPhhIY2OvCNzEl5xP7p7HLJHmH64D/rHPDw7jtz/tc1K zgeyQdA+PgS0Pugi8v9u1jZR66B9KClZHxwGe+15u2wDvdUOitFT1QL4 tqlSp2os0A/FVRGfjhS1bFKsgCavnWytSZQFtdvSA/0UXntNqu8ihpXj KYJcvwgcOZb2x25irwY7VxZtNWWIoZetKVhXtEgj+UagGJQisR2iNVvv 8roBbAmGiWrJCl19ezmQAomZQ+Bf/JyFbHFBGABpIyP0J/MSs2zawYRc iHMWvF20oSvGwY+AgaeZbPR4Pp1kYqnKBG4ylLIpH9LxCZVAor9EIl2Y Z5/O4g==
witrap.com.             86400   IN      RRSIG   DNSKEY 7 2 86400 20181120150154 20181021150154 47466 witrap.com. A8kFmJ0mqrxMR+QZGbXfWNyf4jHqV4+F3iPAON+mXH+A6z5Ba3dCaTXi oBgxJK8WdcDzqOuPcYjfCmu7gEq7vl/I/RXbLe0ckmaKSL/tsEvDvG2X 1U8d2HTM5gxdMzzqRWEInQ2A0CnayzHDUNHAXfg/DpcoXuhgKOPkfZE3 hazetFGUmD/IoAjuj0955FKdTkyXl9+/GzKh39uGkrm3rdD9GKSRr+Js CsatJvx74CBPjA7qNHCRhsmuhrIhACBpvH6/nG5SB6/CvmyQ/qtynbKS EHUVae9fgRvMNeXmxhFn5l2M1qneJCnvjR0SMHwEAeUiR6rkZHKDbA84 NgVVj5mH7RAXHHRsMPMiAXzos1iFdIThLk+KdZocotetM4+qv7BcPEAp n8egRAdyRFQrXnUfknk8kyu5Yl9FWSuqNZX7XjRdD2UYXtUehP7fsmXb ZRws3oPGKOY4LtthGBC0kKqBZgk/L9q+lq2ZBASCyobzZZcUhCmQCdJZ GL2foZt2DYl4AlWu/mUGKQ9gPKEKxPqe6vVWj+JumRQqL4L6C0PO/csN YcAjMIBZM7pcRyzuWHdC95B93RahxCVG0ZgFk2jpqOhTsr4tDExTseP2 hMag8Rkr74T2TK2d3MDC4bXZ5e4MbdiHGhz7J22pSGarz8JjxQqI91cH 9gifFY/9q30=
witrap.com.             0       IN      RRSIG   NSEC3PARAM 7 2 0 20181120150154 20181021150154 47204 witrap.com. CRJZvX0Ovxa855N+/sj+XCyVRfyzFqz/OY9GaK9J1HERgrV5Afn+turj zkpv6W0IHJDr4aPjS6lb43jXexx2bBrYOaa57/mtmk7HQcz8ef/ivdGr TfLCCgPnUq9M17Gk325tnEq3roF2+qb8U3OF2KiCxpMr5nbUBuJz3fxj QK3yLggRxA2g9uMF6R+cyH+OGoBcIefJ19wTOGTGNm2lG+BFtFBngcYY OpopbGWUWwjNV3pD4PQ654J8RJhgzDaLpS9VMzIQjyjiff1bdtiDaYVK 2cW0F6/ugglTm9b8K7/TMHaUDwApIRvfTggIB5y3zgFJi/4HI/B5KyW2 Mf7ShA==
witrap.com.             86400   IN      RRSIG   CAA 7 2 86400 20181120150154 20181021150154 47204 witrap.com. Csvr2Tm3HGkXoOeYPqzGkMumcCWcGxaReN7QNzqY9utLs7FSy5Jf3vNJ 4XeX/qSw02/Rtyrk0Ej3h7sGIy0C+gXaDO5fiPgqKkBoAczsDpG37lRz IJTmebbqLu4G2Kb8MgLsVb2VWZ8Eo0xBMOvEduP6uMD4yC85g8NZfrmj S5JB0/31TWbW3GkTSCZ/mYFjG8m4lS4V1LoKcrSdzPP6Vah1SH/Bohyc kaMpd2VT4h3kaCbpX/elT+mHNbpdRFvFhzjPfG0tKDFdpbZf3jYGMCH5 Wc2LGHH5TriCjVwOZzEsL2BftoGNv8A0Bldx9oWs7lgBdxYWOhBbgbJC GOnhjA==

;; AUTHORITY SECTION:
witrap.com.             86400   IN      NS      ns2.witrap.com.
witrap.com.             86400   IN      NS      ns.witrap.com.

;; ADDITIONAL SECTION:
ns.witrap.com.          86400   IN      A       192.168.63.4
ns2.witrap.com.         86400   IN      A       192.168.67.14

;; Query time: 0 msec
;; SERVER: 192.242.250.3#53(192.242.250.3)
;; WHEN: Wed Nov 28 02:10:26 UTC 2018
;; MSG SIZE  rcvd: 3640

root@attackdefense:~#
```

No. of RRSIG records for witrap.com &rarr; `11`

----

###### References

- [`dnssec-primer`](https://www.ayrx.me/dnssec-primer)

----

EOF