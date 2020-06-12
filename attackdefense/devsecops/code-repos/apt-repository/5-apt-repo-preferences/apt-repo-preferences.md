# apt-repo-preferences

## Objective:  Get the packages from both repositories and retrieve the flags! 

- Two flags are hidden in "auditd" packages hosted on two different APT repositories (one flag in each package archive) on the same network. Your machine is configured to use these repositories.

---

```sh
student@attackdefense:~$ cat /etc/apt/sources.list
deb http://repo1/repo/ /
deb http://repo2/repo/ /
student@attackdefense:~$
```

```sh
student@attackdefense:~$ sudo -l
Matching Defaults entries for student on attackdefense:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User student may run the following commands on attackdefense:
    (root) NOPASSWD: /usr/bin/apt-get
    (root) NOPASSWD: /bin/add-entry.sh
    (root) NOPASSWD: sudoedit /etc/apt/preferences.d/student_user
student@attackdefense:~$
```

```sh
student@attackdefense:~$ sudo apt-get update
Get:1 http://repo1/repo  InRelease [1956 B]
Get:2 http://repo2/repo  InRelease [1956 B]
Get:3 http://repo1/repo  Packages [6185 B]
Get:4 http://repo2/repo  Packages [4435 B]
Fetched 14.5 kB in 0s (62.5 kB/s)
Reading package lists... Done
student@attackdefense:~$
```

```sh
student@attackdefense:~$ apt-cache policy
Package files:
 100 /var/lib/dpkg/status
     release a=now
 500 http://repo2/repo  Packages
     release c=
     origin repo2
 500 http://repo1/repo  Packages
     release c=
     origin repo1
Pinned packages:
student@attackdefense:~$
```

```sh
student@attackdefense:~$ apt-cache policy auditd
auditd:
  Installed: (none)
  Candidate: 1:2.8.2-1ubuntu1
  Version table:
     1:2.8.2-1ubuntu1 500
        500 http://repo1/repo  Packages
     1:2.8.2-1ubuntu1 500
        500 http://repo2/repo  Packages
student@attackdefense:~$
```

```sh
student@attackdefense:~$ sudo apt-get clean
```

```sh
student@attackdefense:~$ sudo apt-get install -d auditd
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following additional packages will be installed:
  libauparse0
Suggested packages:
  audispd-plugins
The following NEW packages will be installed:
  auditd libauparse0
0 upgraded, 2 newly installed, 0 to remove and 0 not upgraded.
Need to get 242 kB of archives.
After this operation, 803 kB of additional disk space will be used.
Do you want to continue? [Y/n]
Get:1 http://repo1/repo  libauparse0 1:2.8.2-1ubuntu1 [48.6 kB]
Get:2 http://repo1/repo  auditd 1:2.8.2-1ubuntu1 [194 kB]
Fetched 242 kB in 0s (0 B/s)
Download complete and in download only mode
student@attackdefense:~$
```

```sh
student@attackdefense:~$ mkdir repo-1
student@attackdefense:~$ cp /var/cache/apt/archives/auditd_1%3a2.8.2-1ubuntu1_amd64.deb repo-1/
student@attackdefense:~$ cd repo-1/
student@attackdefense:~/repo-1$ ls -l
total 192
-rw-r--r-- 1 student student 193716 Jun 12 12:41 auditd_1%3a2.8.2-1ubuntu1_amd64.deb
student@attackdefense:~/repo-1$ mkdir extracted
student@attackdefense:~/repo-1$ dpkg-deb -R auditd_1%3a2.8.2-1ubuntu1_amd64.deb extracted/
student@attackdefense:~/repo-1$ cd extracted/
student@attackdefense:~/repo-1/extracted$ ls -l
total 24
drwxr-xr-x 2 student student 4096 Feb  7  2018 DEBIAN
drwxr-xr-x 6 student student 4096 Jun 16  2019 etc
drwxr-xr-x 3 student student 4096 Feb  7  2018 lib
drwxr-xr-x 2 student student 4096 Jun 16  2019 sbin
drwxr-xr-x 4 student student 4096 Feb  7  2018 usr
drwxr-xr-x 3 student student 4096 Feb  7  2018 var
student@attackdefense:~/repo-1/extracted$ find . -name "*flag*"
./etc/flag.txt
student@attackdefense:~/repo-1/extracted$ cat ./etc/flag.txt
99819465f1f26cc5e17a6d71363a4301
student@attackdefense:~/repo-1/extracted$
```

----

```sh
student@attackdefense:~$ sudoedit /etc/apt/preferences.d/student_user
student@attackdefense:~$ cat /etc/apt/preferences.d/student_user
Package: *
Pin: origin repo2
Pin-Priority: 1001
student@attackdefense:~$
```

```sh
student@attackdefense:~$ sudo apt-get update
Hit:1 http://repo1/repo  InRelease
Hit:2 http://repo2/repo  InRelease
Reading package lists... Done
student@attackdefense:~$
```

```sh
student@attackdefense:~$ apt-cache policy auditd
auditd:
  Installed: (none)
  Candidate: 1:2.8.2-1ubuntu1
  Version table:
     1:2.8.2-1ubuntu1 500
        500 http://repo1/repo  Packages
     1:2.8.2-1ubuntu1 1001
       1001 http://repo2/repo  Packages
student@attackdefense:~$
```

```sh
student@attackdefense:~$ sudo apt-get clean
```

```sh
student@attackdefense:~$ sudo apt-get install -d auditd
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following additional packages will be installed:
  libauparse0
Suggested packages:
  audispd-plugins
The following NEW packages will be installed:
  auditd libauparse0
0 upgraded, 2 newly installed, 0 to remove and 2 not upgraded.
Need to get 242 kB of archives.
After this operation, 803 kB of additional disk space will be used.
Do you want to continue? [Y/n]
Get:1 http://repo1/repo  libauparse0 1:2.8.2-1ubuntu1 [48.6 kB]
Get:2 http://repo2/repo  auditd 1:2.8.2-1ubuntu1 [194 kB]
Fetched 242 kB in 0s (0 B/s)
Download complete and in download only mode
student@attackdefense:~$
```

```sh
student@attackdefense:~$ cp /var/cache/apt/archives/auditd_1%3a2.8.2-1ubuntu1_amd64.deb repo-2/
student@attackdefense:~$ cd repo-2/
student@attackdefense:~/repo-2$ mkdir extracted
student@attackdefense:~/repo-2$ dpkg-deb -R auditd_1%3a2.8.2-1ubuntu1_amd64.deb extracted/
student@attackdefense:~/repo-2$ cd extracted/
student@attackdefense:~/repo-2/extracted$ ls -l
total 24
drwxr-xr-x 2 student student 4096 Feb  7  2018 DEBIAN
drwxr-xr-x 6 student student 4096 Jun 16  2019 etc
drwxr-xr-x 3 student student 4096 Feb  7  2018 lib
drwxr-xr-x 2 student student 4096 Jun 16  2019 sbin
drwxr-xr-x 4 student student 4096 Feb  7  2018 usr
drwxr-xr-x 3 student student 4096 Feb  7  2018 var
student@attackdefense:~/repo-2/extracted$ find . -name "*flag*"
./etc/flag.txt
student@attackdefense:~/repo-2/extracted$ cat ./etc/flag.txt
ec35bf3b19570d46ed3d1e27e22d0a8a
student@attackdefense:~/repo-2/extracted$
```

----

#### References

- [apt_preferences](http://manpages.ubuntu.com/manpages/disco/en/man5/apt_preferences.5.html)

----

EOF