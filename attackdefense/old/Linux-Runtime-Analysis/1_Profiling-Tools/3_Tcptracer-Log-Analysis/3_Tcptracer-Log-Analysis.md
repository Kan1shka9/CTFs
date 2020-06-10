#### 3. Tcptracer: Log Analysis

----

- Performance monitoring and tracking tools can provide a wealth of information about a running system. In some cases, they can help identify anomalies which could have been caused by a security incident.

----

In this lab, we will analyze [`Tcptracer script's`](https://github.com/iovisor/bcc/blob/master/tools/tcptracer.py) trace logs to unearth suspicious activity. Please start the lab, answer the below questions and submit the flags to verify:

- Identify the port on which SSH is running.

```sh
root@attackdefense:~# grep ssh logs
A  1341   sshd             4  192.168.161.139  192.168.161.36   3603   34989
X  1341   sshd             4  192.168.161.139  192.168.161.36   3603   34989
root@attackdefense:~#
```

```
3603
```

- What is the IP address of the client that logged into the machine using SSH?

```
# grep ssh logs
192.168.161.36
```

- A remote machine is running a service on port 2701. The local system downloads some files from that service. What is the IP address of the remote machine?

```sh
root@attackdefense:~# grep 2701 logs
C  21734  wget             4  192.168.161.139  10.10.79.35      45700  2701
C  21734  wget             4  192.168.161.139  10.10.79.35      45702  2701
X  21734  wget             4  192.168.161.139  10.10.79.35      45700  2701
X  21734  wget             4  192.168.161.139  10.10.79.35      45702  2701
root@attackdefense:~#
```

```
10.10.79.35
```

- What the name of the utility used to download the files from the remote service running on port 2701?

```sh
# grep 2701 logs
wget
```

- The machine sends system metrics to a remote machine using curl. What is the IP address of the remote machine?

```sh
root@attackdefense:~# grep curl logs
C  21735  curl             4  192.168.161.139  172.17.3.36      42670  80
X  21735  curl             4  192.168.161.139  172.17.3.36      42670  80
root@attackdefense:~#
```

```
172.17.3.36
```

----

###### Reference

- [`Tcptracer script`](https://github.com/iovisor/bcc/blob/master/tools/tcptracer.py)
- [`Tcptracer Examples`](https://github.com/iovisor/bcc/blob/master/tools/tcptracer_example.txt)
- [`BCC Tools`](https://github.com/iovisor/bcc)

----

EOF