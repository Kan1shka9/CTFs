#### 6. Opensnoop: Trace Analysis

----

Performance monitoring and tracking tools can provide a wealth of information about a running system. In some cases, they can help identify anomalies which could have been caused by a security incident.

----

In this lab, we will analyze Opensnoop script's trace logs to unearth suspicious activity. Please start the lab, answer the below questions and submit the flags to verify:

- A malicious process was searching for some files on the system. What is the name of that process?

```sh
root@attackdefense:~# less logs
Tracing open()s. Ctrl-C to end.
COMM                  PID      FD FILE
<...>                 56784   0x3
<...>                 56788   0x3 /etc/ld.so.cache
<...>                 56788   0x3 /lib/x86_64-linux-gnu/libm.so.6
<...>                 56788   0x3 /lib/x86_64-linux-gnu/libc.so.6
<...>                 56789   0x3 /etc/ld.so.cache
<...>                 56789   0x3 /lib/x86_64-linux-gnu/libc.so.6
<...>                 56789   0x3 trace_pipe
<...>                 56790   0x3 /etc/ld.so.cache
<...>                 56790   0x3 /lib/x86_64-linux-gnu/libc.so.6
<...>                 56791   0x3 /etc/ld.so.cache
<...>                 56791   0x3 /lib/x86_64-linux-gnu/libc.so.6
<...>                 56791   0x3 /lib/x86_64-linux-gnu/libdl.so.2
<...>                 56791   0x0 /var/lib/xkb/server-0.xkm
Xorg                  6054   0x25 /var/lib/xkb/server-0.xkm
125316097e            56793   0x3 /etc/ld.so.cache
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libpthread.so.0
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libc.so.6
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libdl.so.2
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libutil.so.1
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libz.so.1
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libm.so.6
125316097e            56793   0x3 ./125316097e
125316097e            56793   0x3 ./125316097e
125316097e            56793   0x4 /etc/localtime
125316097e            56793   0x3 /etc
125316097e            56793    -1 /etc/.simple-miner
125316097e            56793    -1 /etc/.dummy-snooper
125316097e            56793    -1 /etc/.escalator
125316097e            56793    -1 /etc/.logger
125316097e            56793    -1 /etc/.encryptor
125316097e            56793    -1 /etc/.silent-snooper
125316097e            56793    -1 /etc/.spy-adsadsdfrg
125316097e            56793    -1 /etc/.sync-sdfsd
125316097e            56793    -1 /etc/.session-logger
125316097e            56793   0x3 /etc/libpaper.d
125316097e            56793    -1 /etc/libpaper.d/.simple-miner
125316097e            56793    -1 /etc/libpaper.d/.dummy-snooper
125316097e            56793    -1 /etc/libpaper.d/.escalator
125316097e            56793    -1 /etc/libpaper.d/.logger
125316097e            56793    -1 /etc/libpaper.d/.encryptor
125316097e            56793    -1 /etc/libpaper.d/.silent-snooper
125316097e            56793    -1 /etc/libpaper.d/.spy-adsadsdfrg
125316097e            56793    -1 /etc/libpaper.d/.sync-sdfsd
125316097e            56793    -1 /etc/libpaper.d/.session-logger
125316097e            56793   0x3 /etc/init
125316097e            56793    -1 /etc/init/.simple-miner
125316097e            56793    -1 /etc/init/.dummy-snooper
125316097e            56793    -1 /etc/init/.escalator
125316097e            56793    -1 /etc/init/.logger
125316097e            56793    -1 /etc/init/.encryptor
125316097e            56793    -1 /etc/init/.silent-snooper
125316097e            56793    -1 /etc/init/.spy-adsadsdfrg
125316097e            56793    -1 /etc/init/.sync-sdfsd
125316097e            56793    -1 /etc/init/.session-logger
125316097e            56793   0x3 /etc/rc6.d
125316097e            56793    -1 /etc/rc6.d/.simple-miner
125316097e            56793    -1 /etc/rc6.d/.dummy-snooper
125316097e            56793    -1 /etc/rc6.d/.escalator
125316097e            56793    -1 /etc/rc6.d/.logger
125316097e            56793    -1 /etc/rc6.d/.encryptor
125316097e            56793    -1 /etc/rc6.d/.silent-snooper
logs
```

The process named `125316097e` is opening a lot of files and has a lot of unsuccessful
attempts, indicated by -1.

```
125316097e
```

- The malicious process was successful in finding one of the files it was searching for. Provide the complete path of that file.

```sh
root@attackdefense:~# less logs
125316097e            56793    -1 /etc/.simple-miner
125316097e            56793    -1 /etc/.dummy-snooper
125316097e            56793    -1 /etc/.escalator
125316097e            56793    -1 /etc/.logger
125316097e            56793    -1 /etc/.encryptor
125316097e            56793    -1 /etc/.silent-snooper
125316097e            56793    -1 /etc/.spy-adsadsdfrg
125316097e            56793    -1 /etc/.sync-sdfsd
125316097e            56793    -1 /etc/.session-logger
```

```sh
root@attackdefense:~#  grep 125316097e logs | grep -v '\-1'
125316097e            56793   0x3 /etc/ld.so.cache
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libpthread.so.0
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libc.so.6
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libdl.so.2
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libutil.so.1
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libz.so.1
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libm.so.6
125316097e            56793   0x3 ./125316097e
125316097e            56793   0x3 ./125316097e
125316097e            56793   0x4 /etc/localtime
125316097e            56793   0x3 /etc
125316097e            56793   0x3 /etc/libpaper.d
125316097e            56793   0x3 /etc/init
125316097e            56793   0x3 /etc/rc6.d
125316097e            56793   0x3 /etc/rcS.d
125316097e            56793   0x3 /etc/rc0.d
125316097e            56793   0x3 /etc/rc4.d
125316097e            56793   0x3 /etc/libnl-3
125316097e            56793   0x3 /etc/rc5.d
125316097e            56793   0x3 /etc/alternatives
125316097e            56793   0x3 /etc/profile.d
125316097e            56793   0x3 /etc/rc1.d
125316097e            56793   0x3 /etc/rc3.d
125316097e            56793   0x3 /etc/udev
125316097e            56793   0x3 /etc/udev/rules.d
125316097e            56793   0x3 /etc/udev/hwdb.d
125316097e            56793   0x3 /etc/opt
125316097e            56793   0x3 /etc/ld.so.conf.d
125316097e            56793   0x3 /etc/calendar
125316097e            56793   0x3 /etc/grub.d
125316097e            56793   0x3 /etc/rc2.d
125316097e            56793   0x3 /etc/ssl
125316097e            56793   0x3 /etc/ssl/certs
125316097e            56793   0x3 /etc/ssl/private
125316097e            56793   0x3 /etc/john
125316097e            56793   0x3 /home/oscar
125316097e            56793   0x3 /sbin
125316097e            56793   0x3 /sbin/.silent-snooper
125316097e            56793   0x3 /tmp/.dsdnfsjcnaskdasda/id_rsa
125316097e            56793   0x3 /home/oscar/.ssh/id_rsa
125316097e            56793   0x3 /bin
125316097e            56793   0x3 /opt
125316097e            56793   0x3 /opt/containerd
125316097e            56793   0x3 /opt/containerd/bin
125316097e            56793   0x3 /opt/containerd/lib
root@attackdefense:~# 
```

```
/sbin/.silent-snooper
```

- The malware had stored some secret in the file it had successfully found. Locate the file and retrieve the secret flag.

```sh
root@attackdefense:~# cat /sbin/.silent-snooper
-== Silent-Snooper ==-
DATE: Tue Jun 18 15:36:56 UTC 2018
FLAG: e98bc2aedf7b513f9e97dcfce3176d7b
root@attackdefense:~#
```

```
e98bc2aedf7b513f9e97dcfce3176d7b
```

- The malware had generated a set of private ssh keys somewhere in the /tmp directory. Provide the complete path where the generated keys were stored?

```sh
root@attackdefense:~# grep id_rsa logs
125316097e            56793   0x3 /tmp/.dsdnfsjcnaskdasda/id_rsa
125316097e            56793   0x3 /home/oscar/.ssh/id_rsa
root@attackdefense:~#
```

```sh
root@attackdefense:~# grep 125316097e logs | grep -v '\-1'
125316097e            56793   0x3 /etc/ld.so.cache
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libpthread.so.0
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libc.so.6
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libdl.so.2
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libutil.so.1
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libz.so.1
125316097e            56793   0x3 /lib/x86_64-linux-gnu/libm.so.6
125316097e            56793   0x3 ./125316097e
125316097e            56793   0x3 ./125316097e
125316097e            56793   0x4 /etc/localtime
125316097e            56793   0x3 /etc
125316097e            56793   0x3 /etc/libpaper.d
125316097e            56793   0x3 /etc/init
125316097e            56793   0x3 /etc/rc6.d
125316097e            56793   0x3 /etc/rcS.d
125316097e            56793   0x3 /etc/rc0.d
125316097e            56793   0x3 /etc/rc4.d
125316097e            56793   0x3 /etc/libnl-3
125316097e            56793   0x3 /etc/rc5.d
125316097e            56793   0x3 /etc/alternatives
125316097e            56793   0x3 /etc/profile.d
125316097e            56793   0x3 /etc/rc1.d
125316097e            56793   0x3 /etc/rc3.d
125316097e            56793   0x3 /etc/udev
125316097e            56793   0x3 /etc/udev/rules.d
125316097e            56793   0x3 /etc/udev/hwdb.d
125316097e            56793   0x3 /etc/opt
125316097e            56793   0x3 /etc/ld.so.conf.d
125316097e            56793   0x3 /etc/calendar
125316097e            56793   0x3 /etc/grub.d
125316097e            56793   0x3 /etc/rc2.d
125316097e            56793   0x3 /etc/ssl
125316097e            56793   0x3 /etc/ssl/certs
125316097e            56793   0x3 /etc/ssl/private
125316097e            56793   0x3 /etc/john
125316097e            56793   0x3 /home/oscar
125316097e            56793   0x3 /sbin
125316097e            56793   0x3 /sbin/.silent-snooper
125316097e            56793   0x3 /tmp/.dsdnfsjcnaskdasda/id_rsa
125316097e            56793   0x3 /home/oscar/.ssh/id_rsa
125316097e            56793   0x3 /bin
125316097e            56793   0x3 /opt
125316097e            56793   0x3 /opt/containerd
125316097e            56793   0x3 /opt/containerd/bin
125316097e            56793   0x3 /opt/containerd/lib
root@attackdefense:~#
```

```
/tmp/.dsdnfsjcnaskdasda/id_rsa
```

- The malware had replaced the private ssh keys of a user with the private keys it had generated. What is the name of that user?

```sh
root@attackdefense:~# grep id_rsa logs
125316097e            56793   0x3 /tmp/.dsdnfsjcnaskdasda/id_rsa
125316097e            56793   0x3 /home/oscar/.ssh/id_rsa
root@attackdefense:~#
```

```
/home/oscar/.ssh/id_rsa
```

----

EOF